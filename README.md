# Shelly Rebooter

This project is a containerized automation and monitoring solution built with FastAPI. It automatically reboots your Vodafone Station using a Shelly Smartplug S when Internet connectivity is lost. Key features include:

- **Connectivity Monitoring:** Pings 8.8.8.8 periodically to detect outages.
- **Automated Reboot:** Power-cycles the Shelly Smartplug S if connectivity is lost.
- **Manual Reboot:** Provides a web UI button to manually trigger a reboot.
- **Configurable Parameters:** Update the following via the web dashboard:
  - **Max Attempts**
  - **Total Duration** (entered as **hh:mm**)
  - **Check Interval** (in seconds)
  - **Wait Time After Reboot** (in seconds)
  - **Shelly IP**
  - **Twilio To Number**
- **SMS Notifications via Twilio:** SMS notifications are sent when:
  - The first reboot attempt is made ("Rebooting attempted: first attempt to restore connectivity.")
  - Connectivity is restored after a reboot ("Successful reboot: connectivity restored.")
  - The maximum number of reboot attempts is reached or the total duration is exceeded.
- **Offline Web Resources:** Local copies of Bootstrap assets enable operation without an active Internet connection.
- **Environment Variables:** Sensitive settings (including the Shelly IP, PORT, and Twilio credentials) are loaded from a **.env** file. A template is provided as **.env.TEMPLATE**.
- **Containerized Deployment:** Fully containerized using Docker with Docker Compose support. The PORT setting (from the **.env** file) is respected in both the Dockerfile and the docker-compose configuration.

## Project Structure

```
shelly-rebooter/
├── Dockerfile
├── docker-compose.yml
├── init_project.sh
├── main.py
├── requirements.txt
├── .env            # Sensitive configuration (ignored by Git)
├── .env.TEMPLATE   # Template for environment variables
├── .gitignore
├── README.md
├── static/
│   ├── css/
│   │   └── bootstrap.min.css
│   └── js/
│       └── bootstrap.bundle.min.js
└── templates/
    └── index.html
```

## Setup and Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/shelly-rebooter.git
   cd shelly-rebooter
   ```

2. **Initialize the Project:**

   Run the initialization script to create the necessary folders, download local assets, and set up environment variable files:

   ```bash
   ./init_project.sh
   ```

3. **Update Environment Variables:**

   Edit the **.env** file (or copy **.env.TEMPLATE** to **.env** and modify) to set your Shelly Smartplug IP, the app port, and your Twilio credentials.

4. **Build and Run with Docker Compose:**

   ```bash
   docker-compose up -d
   ```

5. **Access the Web UI:**

   Open your browser and navigate to [http://localhost:${PORT}](http://localhost:${PORT}) (or use your container/LXC IP) to access the dashboard.

## Local Development

For local development, you can run the FastAPI server directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port ${PORT}
```

## License

This project is licensed under the MIT License.

> Created by ChatGPT o1-min @ 14 Jan 2025
