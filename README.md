ESP32S3 16-Channel Relay Control System
This project provides a complete hardware-to-software solution for controlling up to 16 relays using an ESP32S3. It includes an Arduino-based firmware and a modern Python-based Graphical User Interface (GUI) for desktop control.

🚀 Features
Multi-Channel Control: Supports individual control of 16 different relay channels.

Serial Communication: Uses a robust command-parsing protocol via USB-Serial.

Cross-Platform UI: Python/Tkinter GUI that works on Windows, macOS, and Linux.

Real-time Feedback: The UI updates only after receiving a confirmation ("OK") from the hardware.

🛠 Hardware Setup
Components
ESP32S3 Development Board.

16-Channel Relay Module (Active Low or Active High).

External 5V/12V Power Supply (Crucial: Do not power 16 relays directly from the ESP32).

Pin Mapping
The firmware uses the following GPIO pins on the ESP32S3: | Relay | GPIO | Relay | GPIO | | :--- | :--- | :--- | :--- | | 1-4 | 4, 5, 6, 7 | 9-12 | 12, 13, 14, 15 | | 5-8 | 8, 9, 10, 11 | 13-16 | 16, 17, 18, 19 |

💻 Software Installation
1. ESP32 Firmware
Open the esp32_relay_control.ino file in the Arduino IDE.

Ensure you have the ESP32 board support installed.

Select ESP32S3 Dev Module from the Boards menu.

Upload the code to your device.

2. Python UI Setup
Install Python 3.x.

Install the required pyserial library:

Bash

pip install pyserial
Update the SERIAL_PORT variable in the Python script (e.g., COM3 for Windows or /dev/ttyUSB0 for Linux).

Run the application:

Bash

python relay_gui.py
🛰 Communication Protocol
The system communicates via Serial at 115200 Baud.

Command Format: RELAY <index> <state>

index: 1 to 16

state: 1 (ON) or 0 (OFF)

Example: Sending RELAY 15 1 will turn on the 15th relay.

Response: The ESP32 will return OK: Relay 15 ON upon success.

Here is the step-by-step breakdown of how that communication works.1. The Physical ConnectionWhen you plug your ESP32S3 into your computer, an onboard chip (like the CP2102 or CH340) converts the USB signals into Serial data. Windows assigns this a "COM Port" (e.g., COM3), while Linux/Mac assigns it a device path (e.g., /dev/ttyUSB0).2. The Python Protocol (pySerial)The Python script uses the pyserial library to open this port. The "magic" happens in three steps:Encoding: Python strings (like "RELAY 1 1") are Unicode. The ESP32 expects raw bytes. Python must "encode" the string into bytes using command.encode().Termination: The ESP32 code uses Serial.readStringUntil('\n'). Therefore, Python must add a newline character (\n) at the end of every command so the ESP32 knows the message is finished.The Buffer: When Python calls ser.write(), the data travels through the USB cable into the ESP32's Serial buffer.Python# Simplified Logic Example
import serial

# 1. Open the connection
ser = serial.Serial('COM3', 115200)

# 2. Format the instruction
command = "RELAY 5 1\n" 

# 3. Send as bytes
ser.write(command.encode('utf-8')) 
3. The ESP32 Reception LogicInside the void loop(), the ESP32 is constantly checking Serial.available().Detection: When bytes arrive in the buffer, Serial.available() becomes true.Reading: Serial.readStringUntil('\n') pulls the bytes out and reconstructs the string.Parsing: The sscanf function scans the string for the pattern "RELAY", followed by two integers.Action: The ESP32 then maps the "Relay Number" (1–16) to the actual physical GPIO Pin using the array we created and uses digitalWrite() to flip the electronic switch.4. The Feedback Loop (The "Handshake")To ensure the UI doesn't get out of sync with the hardware, the Python script waits for a response:ESP32: After switching the pin, it sends back Serial.println("OK").Python: Uses ser.readline() to wait for that "OK". Once received, the Python GUI updates the button color from Red to Green.Summary TableStepActionPython SideESP32 Side1User clicks buttontoggle_relay(5)Waiting...2Send Dataser.write(b"RELAY 5 1\n")Serial.readStringUntil()3ProcessWaiting for response...digitalWrite(GPIO8, HIGH)4Acknowledgeser.readline()Serial.println("OK")5Update UIButton turns GreenReady for next command
