import tkinter as tk
from tkinter import messagebox
import serial
import serial.tools.list_ports

# --- Configuration ---
SERIAL_PORT = 'COM6'  # Change this to /dev/ttyUSB0 on Linux/Mac
BAUD_RATE = 115200
RELAY_COUNT = 16  # Now matches your full hardware set

class RelayControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ESP32S3 Relay Controller")
        
        # Initialize Serial Connection
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not open {SERIAL_PORT}\n{e}")
            self.ser = None

        self.relay_states = [False] * RELAY_COUNT
        self.buttons = []

        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self.root, text="ESP32 Relay Test Panel", font=("Arial", 14, "bold"))
        label.pack(pady=10)

        # Create a grid for buttons
        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)

        for i in range(RELAY_COUNT):
            relay_num = i + 1
            btn = tk.Button(
                frame, 
                text=f"Relay {relay_num}\nOFF", 
                width=10, 
                height=3,
                bg="red",
                fg="white",
                command=lambda n=relay_num: self.toggle_relay(n)
            )
            btn.grid(row=i // 4, column=i % 4, padx=5, pady=5)
            self.buttons.append(btn)

    def toggle_relay(self, index):
        if not self.ser:
            return

        # Toggle state
        current_state = self.relay_states[index-1]
        new_state = not current_state
        val = 1 if new_state else 0
        
        # Format command: "RELAY X Y\n"
        command = f"RELAY {index} {val}\n"
        
        try:
            self.ser.write(command.encode())
            # Wait for "OK" response from ESP32
            response = self.ser.readline().decode().strip()
            
            if "OK" in response:
                self.relay_states[index-1] = new_state
                color = "green" if new_state else "red"
                status = "ON" if new_state else "OFF"
                self.buttons[index-1].config(text=f"Relay {index}\n{status}", bg=color)
            else:
                print(f"Error from ESP: {response}")
        except Exception as e:
            print(f"Failed to send command: {e}")

    def on_closing(self):
        if self.ser:
            self.ser.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RelayControlApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
