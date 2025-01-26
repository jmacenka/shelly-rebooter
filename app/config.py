import os
from dotenv import load_dotenv

def _load_env():
    # Re-reads the .env file, overriding any existing environment variables.
    load_dotenv(override=True)

class Settings:
    """
    Loads configuration from environment variables and sets defaults.
    Changes made via the FastAPI UI update .env and are reloaded immediately.
    """
    def __init__(self):
        _load_env()
        # Default to port 443 for HTTPS
        self.port = int(os.getenv("PORT", 443))

        self.max_attempts = int(os.getenv("MAX_ATTEMPTS", 10))
        self.total_duration = int(os.getenv("TOTAL_DURATION", 7200))  # seconds
        self.check_interval = int(os.getenv("CHECK_INTERVAL", 30))   # seconds
        self.wait_time = int(os.getenv("WAIT_TIME", 180))           # seconds
        self.shelly_ip = os.getenv("SHELLY_IP", "192.168.1.100")
        self.twilio_to_number = os.getenv("TWILIO_TO_NUMBER", "+0987654321")

        # Twilio
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_from_number = os.getenv("TWILIO_FROM_NUMBER")

        # SSL cert/key for HTTPS
        self.ssl_certfile = os.getenv("SSL_CERTFILE", "/app/certs/cert.pem")
        self.ssl_keyfile = os.getenv("SSL_KEYFILE", "/app/certs/key.pem")

        # Enabled/Disabled toggle (if previously patched for snooze/disable features)
        enabled_str = os.getenv("ENABLED", "true").lower()
        self.enabled = (enabled_str not in ["false", "0", "no"])

        # Snooze duration (in seconds); default 2h if not set
        self.snooze_duration = int(os.getenv("SNOOZE_DURATION", 7200))

# Create a global instance of Settings so other modules can import
settings = Settings()
