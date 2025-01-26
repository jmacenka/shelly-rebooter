import asyncio
import datetime
import subprocess
import time

import requests
from twilio.rest import Client

from app.config import settings
from app.logging_handler import add_log

# Global in-memory store for snooze
snooze_until = None

def send_sms(message: str):
    try:
        ip = subprocess.check_output(["hostname", "-I"]).decode().strip().split()[0]
    except Exception:
        ip = "Unknown"
    prefix = f"Message from Internet-Rebooter ({ip}) "
    prefixed_message = prefix + message

    if not all([
        settings.twilio_account_sid,
        settings.twilio_auth_token,
        settings.twilio_from_number,
        settings.twilio_to_number
    ]):
        add_log("Twilio config incomplete, skipping SMS.")
        return

    try:
        client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
        msg_obj = client.messages.create(
            body=prefixed_message,
            from_=settings.twilio_from_number,
            to=settings.twilio_to_number
        )
        add_log(f"SMS sent successfully: SID {msg_obj.sid}")
    except Exception as e:
        add_log(f"Error sending SMS: {e}", level=40)

async def is_internet_up() -> bool:
    """
    Checks connectivity by calling ping.
    Make sure iputils-ping is installed in the container/host.
    """
    try:
        subprocess.run(["ping", "-c", "2", "8.8.8.8"],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL,
                       check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def trigger_reboot_via_shelly():
    shelly_base_url = f"http://{settings.shelly_ip}"
    add_log("Turning OFF the Shelly plug to cut power to the Vodafone Station.")
    try:
        off_resp = requests.get(f"{shelly_base_url}/relay/0?turn=off", timeout=10)
        off_resp.raise_for_status()
    except Exception as ex:
        add_log(f"Error turning OFF Shelly plug: {ex}", level=40)

    time.sleep(10)

    add_log("Turning ON the Shelly plug to power up the Vodafone Station.")
    try:
        on_resp = requests.get(f"{shelly_base_url}/relay/0?turn=on", timeout=10)
        on_resp.raise_for_status()
        add_log("Shelly plug reboot command successful.")
    except Exception as ex:
        add_log(f"Error turning ON Shelly plug: {ex}", level=40)

async def reboot_sequence():
    add_log("Starting reboot sequence.")
    sms_first_sent = False
    sequence_start = datetime.datetime.now()
    attempts = 0

    while attempts < settings.max_attempts:
        attempts += 1
        elapsed = (datetime.datetime.now() - sequence_start).total_seconds()
        if elapsed > settings.total_duration:
            add_log("Total duration exceeded. Stopping attempts.")
            send_sms("Maximum duration exceeded, connectivity not restored.")
            break

        add_log(f"Reboot attempt {attempts} of {settings.max_attempts} (elapsed: {int(elapsed)}s).")
        if not sms_first_sent:
            send_sms("Rebooting attempted: first attempt to restore connectivity.")
            sms_first_sent = True

        trigger_reboot_via_shelly()

        await asyncio.sleep(settings.wait_time)
        if await is_internet_up():
            end_time = datetime.datetime.now()
            total_time = (end_time - sequence_start).total_seconds()
            add_log("Internet connectivity restored. Ending reboot sequence.")
            send_sms(f"Connectivity re-established after {int(total_time)}s, "
                     f"with {attempts} reboot attempt(s).")
            return

        await asyncio.sleep(settings.check_interval)

    add_log("Reboot sequence ended without restoring connectivity.")
    send_sms("Maximum number of reboot attempts reached, connectivity not restored.")

async def connectivity_monitor():
    global snooze_until

    add_log("Starting connectivity monitor.")
    fail_count = 0
    while True:
        # If disabled or snoozed, skip checks
        now = datetime.datetime.now()
        if not settings.enabled:
            add_log("Reboot logic is disabled. Skipping checks.")
        elif snooze_until and now < snooze_until:
            time_left = (snooze_until - now).total_seconds()
            add_log(f"Snooze active for {int(time_left)} more seconds. Skipping checks.")
        else:
            # Normal check
            if await is_internet_up():
                if fail_count > 0:
                    add_log("Internet connectivity check succeeded. Resetting fail count.")
                fail_count = 0
                add_log("Internet connectivity OK.")
            else:
                fail_count += 1
                add_log(f"Connectivity failed (count={fail_count}).")
                if fail_count >= 3:
                    add_log("3 consecutive fails -> triggering reboot sequence.")
                    asyncio.create_task(reboot_sequence())
                    fail_count = 0
        await asyncio.sleep(settings.check_interval)

def snooze_for(duration_seconds: int):
    """
    Sets snooze_until to now + duration_seconds
    """
    global snooze_until
    snooze_until = datetime.datetime.now() + datetime.timedelta(seconds=duration_seconds)
    add_log(f"Reboot logic snoozed for {duration_seconds} seconds.")
