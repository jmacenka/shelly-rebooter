# Shelly Rebooter (Snooze + Rate-Limit + Enable/Disable)

This project is a containerized FastAPI solution that monitors Internet connectivity and reboots your Vodafone Station using a Shelly Smartplug S. **Key Features**:

1. **HTTPS (Self-Signed)** on port **443** (by default).
2. **Disk-Based Logging** – logs are read on startup into an in-memory UI buffer.
3. **Enable/Disable Switch** – manually turn the entire reboot logic on/off.
4. **Rate-Limit** – if **5 reboots** occur within **2 hours**, the system **pauses** all automatic reboots for **20 hours**.
5. **Snooze** – a button to temporarily pause checks for 2 hours (configurable via \`SNOOZE_DURATION\` in \`.env\`).
6. **Manual Reboot** – always possible, even if paused or snoozed.
7. **iputils-ping** fix in Docker** so \`ping\` works.

## Project Structure

\`\`\`
shelly-rebooter/
├── app/
│   ├── config.py
│   ├── core.py
│   ├── logging_handler.py
│   ├── main.py
│   └── routes.py
├── certs/
│   ├── cert.pem
│   └── key.pem
├── logs/
│   └── shelly-rebooter.log
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── bootstrap.min.css
│   └── js/
│       └── bootstrap.bundle.min.js
├── .env
├── .env.TEMPLATE
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── service_setup.sh
└── README.md
\`\`\`

## Usage

1. **Clone & Run**  
   \`\`\`
   git clone https://github.com/yourusername/shelly-rebooter.git
   cd shelly-rebooter
   ./init_project.sh
   \`\`\`
2. **Edit \`.env\`**  
   - \`SNOOZE_DURATION=7200\` for 2 hours  
   - \`ENABLED=true\` or \`false\`  
   - Twilio, port, etc.
3. **Docker**  
   \`\`\`bash
   docker-compose up -d
   \`\`\`
   Volumes: \`.env\`, \`logs/\`, \`certs/\`.
4. **Systemd**  
   \`\`\`bash
   sudo ./service_setup.sh
   \`\`\`
   Then follow instructions to deploy in \`/opt/shelly-rebooter\`.
5. **Access**  
   [https://localhost:443](https://localhost:443) (self-signed cert).
   - If \`SNOOZE\` is active or \`ENABLED=false\`, no automatic reboots occur.
   - If **5** reboots happen in **2 hours**, it **pauses** for **20 hours** automatically.

## License

This project is licensed under the MIT License.

> Created by ChatGPT o1-min @ 14 Jan 2025
