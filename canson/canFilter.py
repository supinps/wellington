import time
import can
import threading
from .canson import CANson, ConfigSon
from PySide6.QtCore import QThread, Signal, QTimer
import contextlib
import sys
import os

__all__ = ["CANFilter"]

interface = "socketcan"
channel = "vcan0"

filters = [
    {"can_id": 451, "can_mask": 0x7FF, "extended": False},
    {"can_id": 451, "can_mask": 0x1FFFFFFF, "extended": True},
]


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
        # self.timer = QTimer()
        # self.initialization()

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
            # return "CAN device connected successfully"
        except (OSError, can.exceptions.CanInterfaceNotImplementedError):
            self.Device.emit(False)
            self.connected = False
            # return "CAN device connection failed"

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
        # self.timer.start(500)
        self.exec()


def filter():
    fc = CANFilter(channel, interface)
    fc.set_filters(filters)
    fc.recv()


def gui():
    global filters_changed, filters
    time.sleep(10)
    filters = [
        {"can_id": 452, "can_mask": 0x7FF, "extended": False},
        {"can_id": 452, "can_mask": 0x1FFFFFFF, "extended": True},
    ]
    filters_changed = True
    print("changing filters....")


if __name__ == "__main__":
    filter_thread = threading.Thread(target=filter)
    gui_thread = threading.Thread(target=gui)
    filter_thread.start()
    gui_thread.start()
