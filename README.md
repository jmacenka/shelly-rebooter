# Shelly Rebooter

This project is a containerized automation and monitoring solution built with FastAPI. It automatically reboots your Vodafone Station using a Shelly Smartplug S when Internet connectivity is lost. Key features:

- **Environment Reload:** Changes made via the web UI are written to `.env` **and** immediately reloaded (no container restart needed).
- **Three Consecutive Failures** needed to trigger a reboot sequence.
- **Wait Time after Reboot**: Default 180 seconds, configured in `.env`.
- **Detailed Reconnection Notification**:  
  "Connectivity re-established after X seconds, with Y reboot attempt(s)."
- **Disk-Based Logs** in `logs/shelly-rebooter.log` + in-memory logs for the UI.
- **Volumes for .env & logs** in Docker, so you can edit .env or view logs directly on the host.
- **Refactored Code** in `app/` folder.

## Project Structure

```
shelly-rebooter/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── core.py
│   ├── logging_handler.py
│   ├── main.py
│   └── routes.py
├── logs/
│   └── shelly-rebooter.log
├── templates/
│   └── index.html
├── static/
│   ├── css/bootstrap.min.css
│   └── js/bootstrap.bundle.min.js
├── .env
├── .env.TEMPLATE
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── service_setup.sh
└── README.md
```

## Getting Started

1. **Clone & Run Initialization Script**  
   ```bash
   git clone https://github.com/yourusername/shelly-rebooter.git
   cd shelly-rebooter
   ```

2. **Configure `.env`**  
   Edit the newly created `.env` or use `.env.TEMPLATE`. Adjust:
   - `MAX_ATTEMPTS`, `TOTAL_DURATION` (in seconds), `WAIT_TIME`, `CHECK_INTERVAL`, `SHELLY_IP`, etc.
   - Twilio credentials if you want SMS notifications.

3. **Local Development**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 80
   ```

4. **Docker Deployment**  
   - Your `.env` file and `logs/` are mounted as volumes. This means you can edit `.env` locally to update settings, and the logs are persisted on the host.  
   ```bash
   docker-compose up -d
   ```

5. **Systemd Setup (Non-Docker)**  
   ```bash
   sudo ./service_setup.sh
   ```
   This script creates a dedicated user `shelly-rebooter` and writes a systemd unit. Follow the instructions to finalize the deployment in `/opt/shelly-rebooter`.

6. **Access the Web Dashboard**  
   Navigate to [http://localhost:80](http://localhost:80) (or your chosen `PORT`) to view logs, edit configuration, and manually trigger a reboot.

## License

This project is licensed under the MIT License.

> Created by ChatGPT o1-min @ 14 Jan 2025
