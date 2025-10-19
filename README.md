ESP32-S3 USB Relay and Sensor Control System
This project enables you to control an 8-channel relay module and read data from both an HC-SR04 ultrasonic distance sensor and an MH series light sensor (LDR) via a graphical user interface (GUI) on your computer. Communication between the PC and the ESP32-S3 microcontroller is achieved through USB serial.

Features
Control up to 8 relays for switching devices on/off from your PC.

Measure distance with an HC-SR04 (ultrasonic) sensor.

Monitor ambient light conditions using an MH or LDR analog light sensor.

Simple GUI-based interface for easy control and monitoring.

Hardware Requirements
ESP32-S3 development board

8-channel relay module

HC-SR04 ultrasonic distance sensor

MH-series analog light sensor (LDR) or similar

Connecting wires, breadboard or PCB

Computer with USB port

Circuit Connections
Relay IN1–IN8: Connect to GPIO4–GPIO7 and GPIO 15 to GPIO18 on ESP32-S3.

HC-SR04 Trig: Connect to GPIO13.

HC-SR04 Echo: Connect to GPIO14.

Light sensor (LDR): Connect the analog output to GPIO12.

Ensure proper GND and VCC connections for all components.

ESP32-S3 Firmware
The ESP32-S3 firmware listens for serial commands. It controls the relay channels and returns readings from the ultrasonic and light sensors on demand.

Supported serial commands:

RELAY <channel> <0/1>: Set relay (e.g., RELAY 1 1 turns on relay 1).

GET_DIST: Responds with the measured distance in centimeters.

GET_LDR: Responds with the current light sensor value (ADC reading).

The example firmware is written for the Arduino framework. See the esp32_s3_relay_sensor.ino file for the complete code.

Python GUI Application
A Python application (example uses Tkinter) communicates with the ESP32-S3 over USB serial. It provides:

Buttons to toggle each relay ON/OFF

Live display of ultrasonic distance and light sensor readings

Install dependencies via pip:

text
pip install pyserial tk
Edit the serial port in the script (e.g., COM3 on Windows, /dev/ttyUSB0 on Linux) to match your system.

Usage
Upload the ESP32-S3 firmware via Arduino IDE.

Connect all hardware as described above.

Run the Python GUI application on your PC.

Use the GUI to control relays and view sensor data in real time.

Notes
Pin numbers and serial port names may vary—adjust accordingly in the source code.

The project can be expanded to include other sensor types or more channels.

Ensure electrical isolation and proper relay module powering for safe operation.

For Linux/MacOS, you may need additional permissions to access serial ports.

This documentation provides all necessary steps and information for setting up and running the ESP32-S3 USB relay & sensor control system, based on your requirements and prior provided code.​
