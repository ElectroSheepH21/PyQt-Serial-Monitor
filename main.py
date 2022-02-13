import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

from serial_thread import SerialThread
from update_ports_thread import UpdatePortsThread


class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        uic.loadUi("gui.ui", self)
        self.show()

        baudrates = ["9600", "115200"]
        self.cbx_baudrates.addItems(baudrates)

        self.serial = None

        # Init button click events
        self.btn_connect.clicked.connect(self.connect)
        self.btn_disconnect.clicked.connect(self.disconnect)
        self.btn_clear_output.clicked.connect(self.clear_output)
        self.btn_send.clicked.connect(self.send_data)

        self.txt_send.returnPressed.connect(self.send_data)  # Enter hit on send line edit

        # Init updating ports thread
        self.update_ports = UpdatePortsThread()
        self.update_ports.ports.connect(self.cbx_ports.addItems)
        self.update_ports.on_changed(self.ports_changed)
        self.update_ports.start()

    def clear_output(self):
        self.txt_protocol.clear()

    def ports_changed(self):
        self.cbx_ports.clear()
        self.cbx_ports.setCurrentIndex(self.cbx_ports.count() - 1)

    def connect(self):
        self.txt_protocol.clear()
        try:
            # Start serial communication
            port = self.cbx_ports.currentText()
            baud = int(self.cbx_baudrates.currentText())
            self.serial = SerialThread(port, baud)

            # Serial connected
            self.txt_protocol.setText("[CONNECTED]")
            self.connected()  # Update connection buttons

            # Init serial communication
            self.serial.rec_msg.connect(self.txt_protocol.append)
            self.serial.on_disconnected(self.disconnected)
            self.serial.start()
        except Exception:
            self.txt_protocol.setText("[UNABLE TO CONNECT]")
            self.disconnected()  # Update connection buttons

    def disconnect(self):
        self.serial.kill()

    def connected(self):
        self.btn_connect.setEnabled(False)
        self.btn_disconnect.setEnabled(True)

    def disconnected(self):
        self.btn_connect.setEnabled(True)
        self.btn_disconnect.setEnabled(False)

    def send_data(self):
        data = self.txt_send.text()
        try:
            self.serial.send_serial(data)
        except Exception:
            self.txt_protocol.setText("[PORT NOT FOUND]")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = GUI()
    app.exec_()
