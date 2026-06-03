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
- Programming Languages: **Python, MicroPython** - Telemetry & API: **psutil, discord.py** - Communication Protocols: **Serial (USB), I2C** - Hardware: **Raspberry Pi Pico (RP2040), 16x2 LCD, Active Buzzer, Push Button, LEDs** - Circuit Simulation: **Wokwi**

## Notes on Deployment & Scalability  
For the system to function correctly, the host Python script (`discord_bridge.py`) requires a valid Discord Bot Token configured with the **Message Content Intent** enabled in the Discord Developer Portal. 

On the hardware side, the microcontroller must have the provided code saved exactly as `main.py` to ensure it automatically starts listening to the serial port upon booting. To guarantee long-term reproducibility, the complete circuit schematic is backed up in the included `diagram.json` file, allowing the hardware setup to be scalable and easily rebuilt without depending on external links.

## Author  
Santiago Velasco García – *June 2026*
