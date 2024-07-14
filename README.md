## Project Description

This project leverages an embedded system to create a real-time digital speedometer display for vehicles. By interfacing with the vehicle's OBD-II port, the system reads and displays the current speed, estimated fuel usage per 100km, and fuel percentage on a 3.5-inch screen.

## Features

- **Real-Time Speed Display**: Continuously reads and displays the vehicle's speed in real-time.
- **Estimated Fuel Usage**: Calculates and displays the estimated fuel usage per 100km.
- **Fuel Percentage**: Displays the remaining fuel as a percentage of the tank's capacity.
- **Automatic Startup**: The program runs automatically on system startup using a systemd service.
- **Portable Power**: Capable of running on a battery pack for portability.
- **Flexible Display Options**: Can use a dedicated 3.5-inch screen or a smartphone as a display.

## Components

- **Embedded System Board** (I used a Rapberry Pi Zero W for simplicity)
- **3.5-inch Display** (SPI or HDMI)
- **ELM327 OBD-II to USB Interface**
- **PowerBoost 1000C** (or similar)
- **LiPo or Li-Ion Battery Pack** (Optional for portable power)
- **MicroSD Card** (16GB or larger)

## Setup Instructions

1. **Prepare the Embedded System**:
   - Flash the operating system onto the microSD card.
   - Insert the microSD card into the embedded system board.

2. **Hardware Connections**:
   - Connect the 3.5-inch display to the embedded system board.
   - Connect the ELM327 OBD-II to USB interface to the car’s OBD-II port and the embedded system board.
   - (Optional) Connect the battery pack to the PowerBoost 1000C and power the embedded system board.

3. **Software Setup**:
   - Install necessary libraries:
     ```bash
     sudo apt-get update
     sudo apt-get install python3-pip
     sudo pip3 install obd Pillow ST7789
     ```
   - Write and place the `obd_reader.py` script in the home directory.

4. **Systemd Service Configuration**:
   - Create a systemd service file to run the script on startup:
     ```ini
     [Unit]
     Description=OBD-II Reader Service
     After=network.target

     [Service]
     ExecStart=/usr/bin/python3 /home/pi/obd_reader.py
     WorkingDirectory=/home/pi
     StandardOutput=inherit
     StandardError=inherit
     Restart=always
     User=pi

     [Install]
     WantedBy=multi-user.target
     ```
   - Save this as `/etc/systemd/system/obd_reader.service`.
   - Enable and start the service:
     ```bash
     sudo systemctl enable obd_reader.service
     sudo systemctl start obd_reader.service
     ```

## Running the Project

Once everything is set up, the system will automatically start reading and displaying the vehicle's speed, estimated fuel usage per 100km, and fuel percentage upon boot. The systemd service ensures that the program runs continuously and restarts if it crashes.

## Future Enhancements

- **Data Logging**: Implement functionality to log speed, fuel usage, and other OBD-II data for later analysis.
- **Additional Sensors**: Read and display additional vehicle data such as RPM and engine temperature.
