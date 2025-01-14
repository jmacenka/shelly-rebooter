import os
import asyncio
import datetime
import subprocess
from typing import List

import requests
from fastapi import FastAPI, Form, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv, set_key
from twilio.rest import Client

# Load environment variables from .env file.
load_dotenv()

# --- Twilio Configuration ---
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")

def send_sms(message: str):
    # Check that all Twilio settings and the destination phone are defined.
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, os.getenv("TWILIO_TO_NUMBER")]):
        print("Twilio configuration not complete. SMS notification skipped.")
        return
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message_obj = client.messages.create(
            body=message,
            from_=TWILIO_FROM_NUMBER,
            to=os.getenv("TWILIO_TO_NUMBER")
        )
        print(f"SMS sent: SID {message_obj.sid}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

# --- Configuration parameters and shared state ---
class Config:
    max_attempts: int = 10
    total_duration: int = 7200  # in seconds (default 02:00 hours)
    check_interval: int = 30    # in seconds
    wait_time: int = 10         # in seconds after reboot before checking connectivity
    shelly_ip: str = os.getenv("SHELLY_IP", "192.168.1.100")
    twilio_to_number: str = os.getenv("TWILIO_TO_NUMBER", "+0987654321")

# Global in-memory log storage.
LOGS: List[str] = []

def add_log(message: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    LOGS.append(entry)
    print(entry)

# --- Connectivity and Reboot Logic ---
async def is_internet_up() -> bool:
    try:
        subprocess.run(
            ["ping", "-c", "2", "8.8.8.8"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False

def trigger_reboot_via_shelly():
    """Send the reboot command sequence to the Shelly plug."""
    shelly_base_url = f"http://{Config.shelly_ip}"
    try:
        add_log("Turning OFF the Shelly plug to cut power to the Vodafone Station.")
        r_off = requests.get(f"{shelly_base_url}/relay/0?turn=off", timeout=10)
        r_off.raise_for_status()
        import time
        time.sleep(10)  # Wait 10 seconds before turning it back on.
        add_log("Turning ON the Shelly plug to power up the Vodafone Station.")
        r_on = requests.get(f"{shelly_base_url}/relay/0?turn=on", timeout=10)
        r_on.raise_for_status()
        add_log("Shelly plug reboot sequence issued successfully.")
    except Exception as ex:
        add_log(f"Error communicating with Shelly plug: {ex}")

async def reboot_sequence():
    add_log("Starting reboot sequence.")
    sms_first_sent = False
    start_time = datetime.datetime.now()
    attempts = 0

    while attempts < Config.max_attempts:
        attempts += 1
        elapsed = (datetime.datetime.now() - start_time).total_seconds()
        if elapsed > Config.total_duration:
            add_log("Total duration for reboot sequence exceeded. Stopping attempts.")
            send_sms("Maximum duration exceeded, connectivity not restored.")
            break

        add_log(f"Reboot attempt {attempts} of {Config.max_attempts} (elapsed: {int(elapsed)} sec).")
        if not sms_first_sent:
            send_sms("Rebooting attempted: first attempt to restore connectivity.")
            sms_first_sent = True

        trigger_reboot_via_shelly()

        # Wait after reboot before checking connectivity.
        await asyncio.sleep(Config.wait_time)
        if await is_internet_up():
            add_log("Internet connectivity restored. Ending reboot sequence.")
            send_sms("Successful reboot: connectivity restored.")
            return

        await asyncio.sleep(Config.check_interval)

    add_log("Reboot sequence ended without restoring connectivity.")
    send_sms("Maximum number of reboot attempts reached, connectivity not restored.")

# Background monitoring task.
async def connectivity_monitor():
    add_log("Starting connectivity monitor.")
    while True:
        if await is_internet_up():
            add_log("Internet connectivity OK.")
        else:
            add_log("Internet connectivity lost. Initiating reboot sequence.")
            asyncio.create_task(reboot_sequence())
        await asyncio.sleep(Config.check_interval)

# --- FastAPI Application Setup ---
app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(connectivity_monitor())
    add_log("Application startup complete.")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Format total_duration as hh:mm for the UI.
    hours = Config.total_duration // 3600
    minutes = (Config.total_duration % 3600) // 60
    total_duration_str = f"{hours:02d}:{minutes:02d}"
    return templates.TemplateResponse("index.html", {
        "request": request,
        "logs": list(reversed(LOGS[-50:])),
        "config": Config,
        "total_duration_str": total_duration_str,
    })

@app.post("/update-config")
async def update_config(
    max_attempts: int = Form(...),
    total_duration_str: str = Form(...),  # Format "hh:mm"
    check_interval: int = Form(...),
    wait_time: int = Form(...),
    shelly_ip: str = Form(...),
    twilio_to_number: str = Form(...)
):
    Config.max_attempts = max_attempts
    try:
        hh, mm = total_duration_str.split(":")
        Config.total_duration = int(hh) * 3600 + int(mm) * 60
    except Exception as e:
        add_log(f"Error parsing total duration: {e}")
    Config.check_interval = check_interval
    Config.wait_time = wait_time
    Config.shelly_ip = shelly_ip
    Config.twilio_to_number = twilio_to_number

    add_log(
        f"Configuration updated:\n"
        f"Max Attempts: {max_attempts}\n"
        f"Total Duration: {total_duration_str}\n"
        f"Check Interval: {check_interval}\n"
        f"Wait Time: {wait_time}\n"
        f"Shelly IP: {shelly_ip}\n"
        f"Twilio To Number: {twilio_to_number}"
    )
    # Persist the Shelly IP and Twilio destination phone number in the .env file.
    set_key(".env", "SHELLY_IP", shelly_ip)
    set_key(".env", "TWILIO_TO_NUMBER", twilio_to_number)
    return RedirectResponse("/", status_code=303)

@app.post("/manual-reboot")
async def manual_reboot(background_tasks: BackgroundTasks):
    add_log("Manual reboot triggered via Web UI.")
    background_tasks.add_task(reboot_sequence)
    return RedirectResponse("/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 80))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
