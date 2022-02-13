import serial
from PyQt5.QtCore import QThread, pyqtSignal
import serial.tools.list_ports


class UpdatePortsThread(QThread):
    ports = pyqtSignal(list)  # Pass data through threads with pyqtSignal

    def __init__(self):
        super(UpdatePortsThread, self).__init__()
        self.old_ports = None
        self.on_changed_event = self.empty_func

    def empty_func(self):
        pass

    def on_changed(self, event):
        self.on_changed_event = event

    def run(self):
        while True:
            new_ports = self.find_USB_device()
            if new_ports != self.old_ports:
                self.old_ports = new_ports
                self.on_changed_event()
                self.ports.emit(new_ports)

    def find_USB_device(self):
        ports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        usb_port_list = [p[0] for p in ports]
        return usb_port_list
