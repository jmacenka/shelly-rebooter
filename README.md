# Shelly Rebooter – Final Comprehensive Edition

This project is a containerized FastAPI solution that monitors Internet connectivity and reboots your Vodafone Station using a Shelly Smartplug S. **Features**:

1. **Self-Signed SSL** on **port 443** (default).
2. **Disk-Based Logging** persisted to \`logs/shelly-rebooter.log\`, loaded on startup for UI display.
3. **Enable/Disable Switch**: Manually turn on/off the entire reboot logic.
4. **Rate-Limit**: If **5** reboots occur within **2 hours**, **pause** automatic reboots for **20 hours** (manual reboots still possible).
5. **Docker**: \`docker-compose.yml\` volume-mounts \`.env\`, \`logs/\`, and \`certs/\`.
6. **Systemd**: \`service_setup.sh\` for non-Docker deployment.

## Usage

1. **Clone & Run**  
   \`\`\`
   git clone https://github.com/yourusername/shelly-rebooter.git
   cd shelly-rebooter
   ./init_project.sh
   \`\`\`
2. **Review/Edit \`.env\`**  
   - Set \`PORT=443\`, \`ENABLED=true\` or \`false\`, etc.
3. **Docker**  
   \`\`\`
   docker-compose up -d
   \`\`\`
4. **Systemd**  
   \`\`\`
   sudo ./service_setup.sh
   \`\`\`
   Follow instructions to finalize your deployment.
5. **Access**  
   [https://localhost:443](https://localhost:443) (self-signed cert).

## License

This project is licensed under the MIT License.

> Created by ChatGPT o1-min @ 14 Jan 2025
