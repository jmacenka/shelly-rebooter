import os
from dotenv import load_dotenv

def _load_env():
    # Re-reads the .env file, overriding any existing environment variables.
    load_dotenv(override=True)

class Settings:
    """
    Loads configuration from environment variables and sets defaults.
    Changes made via the FastAPI UI update .env and are reloaded upon restart
    or on-demand by calling settings.__init__().
    """
    def __init__(self):
        _load_env()
        self.max_attempts = int(os.getenv("MAX_ATTEMPTS", 10))
        self.total_duration = int(os.getenv("TOTAL_DURATION", 7200))  # seconds
        self.check_interval = int(os.getenv("CHECK_INTERVAL", 30))   # seconds
        self.wait_time = int(os.getenv("WAIT_TIME", 180))           # seconds
        self.shelly_ip = os.getenv("SHELLY_IP", "192.168.1.100")
        self.twilio_to_number = os.getenv("TWILIO_TO_NUMBER", "+0987654321")

        # Twilio config:
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_from_number = os.getenv("TWILIO_FROM_NUMBER")

        # App listening port:
        self.port = int(os.getenv("PORT", 80))

settings = Settings()
