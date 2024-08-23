# Project Description

This project leverages an embedded system to create a dual-function vehicle dashboard with advanced data handling capabilities. The device performs two key functions:

1. **Digital Display**: It directly displays real-time vehicle data such as speed, estimated fuel usage per 100km, and fuel percentage on a built-in 3.5-inch screen.
  
2. **Website Dashboard**: Simultaneously, the device hosts a web interface accessible via Wi-Fi. This dashboard, built with React for the frontend and Express.js for the backend, provides detailed statistical data, including graphs, averages, and diagnostic codes. Data is managed using PostgreSQL, and there is an option to upload the data to Amazon S3 buckets for permanent storage and further analysis.

## Features

- **Real-Time Speed Display**: Continuously reads and displays the vehicle's speed on the device's built-in screen.
- **Estimated Fuel Usage**: Calculates and displays the estimated fuel usage per 100km on the screen.
- **Fuel Percentage**: Displays the remaining fuel as a percentage of the tank's capacity on the screen.
- **Diagnostic Codes**: Provides real-time diagnostic codes from the vehicle's OBD system, accessible via the hosted website.
- **Statistical Dashboard**: Displays detailed graphs and averages of vehicle data through a web interface hosted by the device. The frontend is built with React, and the backend uses Express.js.
- **Wi-Fi Connectivity**: The device hosts a local network, allowing users to connect via Wi-Fi and automatically display the dashboard on a connected device.
- **Automatic Startup**: The program runs automatically on system startup using a systemd service.
- **Portable Power**: Capable of running on a battery pack for portability.
- **Flexible Display Options**: Data is displayed on both the device's built-in screen and the web interface.

## Software Components
- **Data Management**: Uses PostgreSQL to store and manage vehicle data, enabling complex queries and data integrity.
- **Python Data Handling**: Maintains a live connection to the car's OBD-II system to retrieve data and perform initial analysis before serving it to the digvital display and storing it in PostgreSQL (which is further supported by a data buffer)
- **Rest API For Data Retrival** A service built with golag to interact with postgres database and retrieve requested data
- **Gateway API** Service to handle user interactions with frontend
- **Front end:** The dashbored user interface is built with Express.js
- **Data bufer:** Python script to increamently store data before uploading to postgress and serving to digital disaply
- **Cloud Integration**: Option to upload data to Amazon S3 buckets for permanent storage, accessible through a public website.

## Physical Components

- **Embedded System Board** (e.g., Raspberry Pi Zero W)
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
     sudo pip3 install obd Pillow ST7789 Flask psycopg2-binary
     ```
   - Set up the Python environment for data retrieval and analysis, placing the `obd_reader.py` script in the home directory.

4. **Database Setup**:
   - Install PostgreSQL on the embedded system:
     ```bash
     sudo apt-get install postgresql postgresql-contrib
     ```
   - Configure the PostgreSQL database to store vehicle data.
   - Integrate Python with PostgreSQL using `psycopg2`.

5. **Backend Setup**:
   - Set up the Express.js backend to serve the web interface and interact with the PostgreSQL database.
   - Create necessary API endpoints to retrieve data from the PostgreSQL database and serve it to the frontend.

6. **Frontend Setup**:
   - Develop the React frontend to display vehicle data, graphs, averages, and diagnostic codes.
   - Configure the frontend to fetch data from the Express.js backend.

7. **Systemd Service Configuration**:
   - Create a systemd service file to run the Python script on startup:
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

## Cloud Integration

### Amazon S3 Buckets

- Configure the system to upload vehicle data to Amazon S3 buckets for permanent storage.
- Set up access permissions and bucket policies to ensure data security.
- Integrate the public website with S3 to allow users to view stored data.

## Running the Project

Once everything is set up, the system will automatically start reading and displaying the vehicle's speed, estimated fuel usage per 100km, and fuel percentage on the built-in screen upon boot. Simultaneously, the device hosts a local website, accessible via Wi-Fi, where users can view additional statistics and diagnostic codes. Data can be stored in PostgreSQL and, if enabled, uploaded to Amazon S3 buckets for permanent access via a public website.
