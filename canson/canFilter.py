import can
import threading
from canson import CANson, ConfigSon
from PySide6.QtCore import QThread, Signal, QTimer
import contextlib
import os

__all__ = ["CANFilter"]

class CANFilter(QThread):
    newData = Signal(str, str)
    Device = Signal(bool)
    stopTimer = Signal()
    start_timer = Signal(int)

    def __init__(self) -> None:
        super().__init__()
        self.canson = CANson()
        self.configson = ConfigSon()
        self.bus = None
        self.all_filters = self.canson.get_filters()
        self.timeout = 0.1
        self._key_lock = threading.Lock()
        self.interfaces = self.configson.get_interfaces()
        self.channels = self.configson.get_channels()
        self.index_list = range(len(self.all_filters))
        self.connected = False

    def bus_init(self, interface_index, channel_index):
        try:
            with open(os.devnull, "w") as devnull:
                with contextlib.redirect_stderr(devnull):
                    self.bus = can.Bus(
                        interface=self.interfaces[interface_index],
                        channel=self.channels[interface_index][channel_index],
                    )
                    self.set_filters()
            self.connected = True
            self.Device.emit(True)
            self.start()
        except (OSError, can.exceptions.CanInterfaceNotImplementedError):
            self.Device.emit(False)
            self.connected = False

    def set_index_list(self, index_list):
        self.index_list = index_list
        if self.connected:
            self.set_filters()

    def set_filters(self):
        filter_list = []
        for index in self.index_list:
            filter_list.append(self.all_filters[index])
        with self._key_lock:
            self.bus.set_filters(filter_list)

    def on_timeout(self):
        self._key_lock.acquire()
        msg = self.bus.recv(timeout=self.timeout)
        self._key_lock.release()
        if msg != None:
            frame = self.canson.get_frame(msg.arbitration_id)
            name = self.canson.get_frame_name(frame)
            data = self.canson.get_frame_data(frame, msg.data)
            self.newData.emit(name, data)

    def quit(self) -> None:
        self.stopTimer.emit()
        with self._key_lock:
            self.bus.shutdown()
        return super().quit()

    def stopBus(self):
        self.stopTimer.emit()

    def startBus(self):
        self.start_timer.emit(500)

    def run(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timeout)
        self.stopTimer.connect(self.timer.stop)
        self.start_timer.connect(self.timer.start)
        self.exec()

if __name__ == "__main__":
    print("CANFilter is a package")
