import serial
from PyQt5.QtCore import pyqtSignal, QThread


class SerialThread(QThread):
    rec_msg = pyqtSignal(str)  # Pass data through threads with pyqtSignal

    def __init__(self, port, baud):
        super(SerialThread, self).__init__()
        self.serialport = serial.Serial()
        self.serialport.port = port
        self.serialport.baudrate = baud

        self.serialport.open()
        self.on_disconnected_event = self.empty_func

    def empty_func(self):
        pass

    def on_disconnected(self, event):
        self.on_disconnected_event = event

    def run(self):
        while True:
            try:
                msg = self.serialport.readline().decode('utf-8').rstrip("\r\n")
                self.rec_msg.emit(msg)
            except Exception:
                self.on_disconnected_event()
                self.rec_msg.emit("[DISCONNECTED]")
                break

    def kill(self):
        self.exit()
        self.serialport.close()

    def send_serial(self, data):
        self.serialport.write(data.encode('utf-8'))
