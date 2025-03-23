from fastapi import APIRouter, BackgroundTasks, Form
from fastapi.responses import RedirectResponse
from dotenv import set_key

from app.config import settings
from app.logging_handler import add_log
from app.core import reboot_sequence

router = APIRouter()

@router.post("/update-config")
async def update_config(
    max_attempts: int = Form(...),
    total_duration_str: str = Form(...),
    check_interval: int = Form(...),
    wait_time: int = Form(...),
    shelly_ip: str = Form(...),
    twilio_to_number: str = Form(...)
):
    try:
        hh, mm = total_duration_str.split(":")
        total_duration = int(hh)*3600 + int(mm)*60
    except Exception as e:
        add_log(f"Error parsing total_duration: {e}", level=40)
        total_duration = settings.total_duration

    set_key(".env", "MAX_ATTEMPTS", str(max_attempts))
    set_key(".env", "TOTAL_DURATION", str(total_duration))
    set_key(".env", "CHECK_INTERVAL", str(check_interval))
    set_key(".env", "WAIT_TIME", str(wait_time))
    set_key(".env", "SHELLY_IP", shelly_ip)
    set_key(".env", "TWILIO_TO_NUMBER", twilio_to_number)

    add_log(
        f"Configuration updated:\n"
        f"MAX_ATTEMPTS={max_attempts}, TOTAL_DURATION={total_duration}, "
        f"CHECK_INTERVAL={check_interval}, WAIT_TIME={wait_time}, "
        f"SHELLY_IP={shelly_ip}, TWILIO_TO_NUMBER={twilio_to_number}"
    )

    # Re-initialize settings from .env
    settings.__init__()
    return RedirectResponse("/", status_code=303)

@router.post("/toggle-enabled")
async def toggle_enabled():
    new_value = not settings.enabled
    set_key(".env", "ENABLED", str(new_value).lower())
    add_log(f"Enabled toggled to {new_value}.")
    settings.__init__()
    return RedirectResponse("/", status_code=303)

@router.post("/manual-reboot")
async def manual_reboot(background_tasks: BackgroundTasks):
    add_log("Manual reboot triggered via Web UI.")
    background_tasks.add_task(reboot_sequence)
    return RedirectResponse("/", status_code=303)
