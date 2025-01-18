# Shelly Rebooter

This project is a containerized automation and monitoring solution built with FastAPI. It reboots your Vodafone Station via a Shelly Smartplug S when Internet connectivity fails. **Key updates**:

- **Fixed** `ping` not found by installing `iputils-ping` in Docker.
- **Self-signed SSL** – Running on port 443 by default (`.env` configurable).
- **Immediate Config Reload** – Any updates to `.env` via the web UI are immediately loaded.
- **Disk-based Logs** – Written to `./logs/shelly-rebooter.log`, shown on the UI.
- **Volumes** for `.env`, `logs`, `certs` in Docker Compose.

## Usage

1. **Clone & Init**  
   ```bash
   git clone https://github.com/yourusername/shelly-rebooter.git
   cd shelly-rebooter
   ```

2. **Configure `.env`**  
   Adjust `PORT=443`, `WAIT_TIME=180`, etc.

3. **Local Dev**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 443 \
     --ssl-certfile certs/cert.pem \
     --ssl-keyfile certs/key.pem
   ```

4. **Docker Compose**  
   ```bash
   docker-compose up -d
   ```
   All changes in `.env`, logs in `logs/`, and certificates in `certs/` persist on the host.

5. **Systemd**  
   ```bash
   sudo ./service_setup.sh
   ```
   Follow instructions to finalize setup in `/opt/shelly-rebooter`.

6. **Access**  
   Open [https://localhost:443](https://localhost:443). Browser may warn about the self-signed cert.

## License

This project is licensed under the MIT License.

> Created by ChatGPT o1-min @ 14 Jan 2025
