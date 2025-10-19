import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton 
import serial
from pymata4 import pymata4

class MainDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Dialog")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Distance:")
        layout.addWidget(self.label)

        self.dist_textbox = QLineEdit(self)
        self.dist_textbox.setText("0")
        layout.addWidget(self.dist_textbox)

        self.update_button = QPushButton("Update", self)
        self.update_button.clicked.connect(self.update_distance)
        layout.addWidget(self.update_button)

        self.setLayout(layout)

        # Initialize the Pymata4 board
        self.board = pymata4.Pymata4()

        # Set up the ultrasonic sensor
        self.trigger_pin = 10
        self.echo_pin = 11
        self.board.set_pin_mode_sonar(self.trigger_pin, self.echo_pin, self.callback)

        self.distance = 0

    def callback(self, data):
        self.distance = data[2]

    def update_distance(self):
        # Measure the distance using the ultrasonic sensor
        self.board.sonar_read(self.trigger_pin)
        self.dist_textbox.setText(str(self.distance))
        print(f"Distance updated to: {self.distance}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = MainDialog()
    dialog.show()
    sys.exit(app.exec_())


