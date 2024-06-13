## Fall Detection of Package using Decision Tree with Arduino

This project implements a fall detection system for packages using a Decision Tree algorithm on an Arduino. The Arduino IDE is connected to InfluxDB using MQTT to save detection data to the Influx database.

### System Overview
1. **Fall Detection**: The system uses a Decision Tree algorithm to detect falls. The algorithm is implemented on an Arduino device, which processes sensor data to determine if a fall has occurred.

2. **Data Transmission**: Once a fall is detected, the Arduino sends the data using the MQTT protocol.

3. **Data Storage**: The MQTT data is received by InfluxDB, where it is stored for further analysis and monitoring.

### Components
- **Arduino**: Used for running the Decision Tree algorithm and detecting falls.
- **MQTT**: A lightweight messaging protocol for sending data from the Arduino to InfluxDB.
- **InfluxDB**: A time-series database used to store detection data.

### Steps to Setup
1. **Arduino Setup**:
    - Install the necessary libraries for the Decision Tree algorithm.
    - Write the code to process sensor data and detect falls.
    - Configure the Arduino to send data via MQTT.

2. **MQTT Setup**:
    - Set up an MQTT broker to handle the messages from the Arduino.
    - Ensure the Arduino is correctly publishing data to the MQTT broker.

3. **InfluxDB Setup**:
    - Install and configure InfluxDB to receive data from the MQTT broker.
    - Set up the database and retention policies as needed.

### Conclusion
This project demonstrates how to use a Decision Tree algorithm on an Arduino to detect falls and save the data to an InfluxDB database using MQTT. The system provides a reliable way to monitor package falls in real-time.
