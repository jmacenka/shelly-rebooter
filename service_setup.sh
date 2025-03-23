#!/bin/bash
set -e

# Update system packages and install Git.
sudo apt update && sudo apt upgrade -y && sudo apt install -y git

# Create a dedicated system user (if it doesn't exist already)
SERVICE_USER="shelly-rebooter"
if id "$SERVICE_USER" &>/dev/null; then
  echo "User '$SERVICE_USER' already exists. Continuing..."
else
  echo "Creating user '$SERVICE_USER' as a system account with no login shell."
  sudo useradd --system --no-create-home --shell /usr/sbin/nologin "$SERVICE_USER" || {
    echo "Failed to create user '$SERVICE_USER'."
    echo "Please create a suitable user manually or edit this script to use a different username."
    exit 1
  }
  echo "User '$SERVICE_USER' created."
fi

# Create a systemd service file for the Shelly Rebooter application.
SERVICE_FILE="/etc/systemd/system/shelly-rebooter.service"

sudo tee ${SERVICE_FILE} > /dev/null << SERVICE_EOF
[Unit]
Description=Shelly Rebooter FastAPI Application
After=network.target

[Service]
User=$SERVICE_USER
Group=$SERVICE_USER
WorkingDirectory=/opt/shelly-rebooter
EnvironmentFile=/opt/shelly-rebooter/.env
ExecStart=/opt/shelly-rebooter/venv/bin/uvicorn app.main:app \
  --host 0.0.0.0 \
  --port \${PORT:-443} \
  --ssl-certfile \${SSL_CERTFILE:-/opt/shelly-rebooter/certs/cert.pem} \
  --ssl-keyfile \${SSL_KEYFILE:-/opt/shelly-rebooter/certs/key.pem}
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICE_EOF

echo "Service file created at ${SERVICE_FILE}"
echo "If you need a different user or path, edit '${SERVICE_FILE}' accordingly."

# Additional instructions
echo "--------------------------------------------------------------------------"
echo "Place your application in /opt/shelly-rebooter, create a virtualenv, etc."
echo "  1) sudo mkdir -p /opt/shelly-rebooter"
echo "  2) sudo chown -R $SERVICE_USER:$SERVICE_USER /opt/shelly-rebooter"
echo "  3) cd /opt/shelly-rebooter && python3 -m venv venv"
echo "  4) source venv/bin/activate && pip install -r requirements.txt"
echo "  5) (Optional) Copy .env, logs, certs into /opt/shelly-rebooter"
echo "Then run:"
echo "  sudo systemctl daemon-reload"
echo "  sudo systemctl enable shelly-rebooter.service"
echo "  sudo systemctl start shelly-rebooter.service"
echo "--------------------------------------------------------------------------"
