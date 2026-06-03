# PicoDeck: Hardware Dashboard & Telemetry Hub

## Dependencies  
This project uses the following libraries and frameworks to manage hardware communication and data extraction:  
- [`discord.py`](https://discordpy.readthedocs.io/) (for asynchronous Discord API access)  
- [`pyserial`](https://pythonhosted.org/pyserial/) (for USB serial communication)  
- [`psutil`](https://psutil.readthedocs.io/) (for OS-level telemetry extraction)  
- [`python-dotenv`](https://pypi.org/project/python-dotenv/) (for environment variable management)  
- [`MicroPython`](https://micropython.org/) (for the Raspberry Pi Pico firmware)

## Introduction  
This project is a **physical monitoring system and non-intrusive notification hub** for your desk. The main goal is to project OS performance metrics (CPU/RAM) and asynchronous Discord messages onto a physical display, keeping the main computer screen free of distractions.

To achieve this, we built a bidirectional Extract, Transform, Load (ETL) pipeline using Python. The system extracts data from the host PC, formats it with specific routing flags, and sends it via serial connection to a Raspberry Pi Pico, which acts as the local brain to process and display the information on an I2C matrix.

## Features  
- Authentication and data collection from the Discord API  
- Real-time host telemetry extraction (CPU and RAM usage)  
- Hardware-controlled state machine isolating different contexts (Discord Mode, Overlay Mode, Offline Mode)  
- Custom ETL pipeline routing data packets with `D|` and `O|` prefix flags  
- Tactical audio feedback via an active buzzer for non-intrusive alerts  
- Interactive vertical scroll animations for reading long messages on the 16x2 LCD  

## Technologies  
- Programming Languages: **Python, MicroPython**
- Telemetry & API: **psutil, discord.py**
- Communication Protocols: **Serial (USB), I2C**
- Hardware: **Raspberry Pi Pico (RP2040), 16x2 LCD, Active Buzzer, Push Button, LEDs**
- Circuit Simulation: **Wokwi**

> 🔗 **Interactive Circuit Schematic:** [View hardware diagram on Wokwi](https://wokwi.com/projects/465771827052196865)

## Discord Bot Setup & Authentication
Before running the system, you must register a bot application on Discord to generate your authorization token:

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and log in.
2. Click **New Application**, give it a name, and accept the terms.
3. On the left sidebar, navigate to the **Bot** tab.
4. ⚠️ **CRITICAL:** Scroll down to **Privileged Gateway Intents** and toggle **ON** the **Message Content Intent**. If you skip this, the PicoDeck won't be able to read incoming messages.
5. Click **Reset Token**, copy the generated string, and paste it into a `.env` file in your project root as `DISCORD_TOKEN=your_token_here`.
6. To invite the bot to your server, go to **OAuth2 -> URL Generator** on the left menu.
7. Select the `bot` scope, then under Bot Permissions select `Read Messages/View Channels`. 
8. Copy the generated URL at the bottom, paste it into your browser, and authorize the bot into your server.

## Notes on Deployment & Scalability  
For the system to function correctly, the host Python script (`discord_bridge.py`) requires the aforementioned Discord Bot Token configured with the **Message Content Intent**. 

On the hardware side, the microcontroller must have the provided code saved exactly as `main.py` to ensure it automatically starts listening to the serial port upon booting. To guarantee long-term reproducibility, the complete circuit schematic is backed up in the included `diagram.json` file, allowing the hardware setup to be scalable and easily rebuilt without depending on external links. 

## Author  
Santiago Velasco García – *June 2026*
