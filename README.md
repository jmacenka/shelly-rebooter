# Shelly Rebooter – Extended Rate Limit + Enable/Disable

This project is a containerized FastAPI solution that reboots your Vodafone Station via a Shelly Smartplug S upon repeated connectivity failures. **New features**:

- **Enable/Disable Switch**: A button to manually turn all automatic reboots on/off.
- **Reboot Rate Limit**: If 5 reboots occur within 2 hours, the system automatically pauses all reboots for 20 hours.
- **HTTPS**: Self-signed cert, running on port 443 by default (see \`.env\`).
- **Disk-based Logs**: \`logs/shelly-rebooter.log\`, loaded on startup for UI display.
- **Docker**: A \`docker-compose.yml\` that volume-mounts \`.env\`, \`logs/\`, and \`certs/\`.

## Key Points

1. **5 reboots in 2 hours** ⇒ **pause 20 hours**  
   During that pause, no automatic reboots occur unless manually triggered.
2. **Enable/Disable Switch**  
   If disabled, the app ignores connectivity failures.
3. **Local \`.env\`**  
   Edit to change default wait time, maximum attempts, or port.
4. **Self-Signed SSL**  
   The Docker container starts on \`https://0.0.0.0:443\`.
   Browsers may warn about the untrusted certificate.

## Setup

1. **Clone & Run This Script**  
   \`\`\`bash
   git clone https://github.com/yourusername/shelly-rebooter.git
   cd shelly-rebooter
   ./init_project.sh
   \`\`\`
2. **Adjust \`.env\`**  
   e.g., set \`ENABLED=false\` if you want to disable reboots initially.
3. **Docker**  
   \`\`\`
   docker-compose up -d
   \`\`\`
4. **Systemd**  
   \`\`\`
   sudo ./service_setup.sh
   \`\`\`
   Then follow instructions to finalize your system service at \`/opt/shelly-rebooter\`.

5. **Access the App**  
   \`https://<your-host-or-ip>:443\`. The certificate is self-signed, so you may have to bypass a security warning.

Enjoy your extended Shelly Rebooter solution!

> Created by ChatGPT o1-min @ 14 Jan 2025
