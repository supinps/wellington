import time
import can
import threading
from .canson import CANson, ConfigSon
from PySide6.QtCore import QThread, Signal
import numpy as np

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

    def __init__(self) -> None:
        super().__init__()
        self.canson = CANson()
        self.configson = ConfigSon()
        self.bus = None
        self.filters = self.canson.get_filters()
        self.timeout = 0.5
        self._key_lock = threading.Lock()
        self.interfaces = self.configson.get_interfaces()
        self.channels = self.configson.get_channels()
        self.index_list = np.arange(len(self.filters))
        # self.initialization()

    def bus_init(self, interface_index, channel_index):
        try:
            self.bus = can.Bus(
                interface=self.interfaces[interface_index],
                channel=self.channels[interface_index][channel_index],
            )
            self.set_filters()
            self.Device.emit(True)
            # return "CAN device connected successfully"
        except OSError:
            self.Device.emit(False)
            # return "CAN device connection failed"

    def set_filters(self):
        filter_list = []
        for index in self.index_list:
            filter_list.append(self.filters[index])
        with self._key_lock:
            self.bus.set_filters(filter_list)

    def run(self):
        while True:
            self._key_lock.acquire()
            msg = self.bus.recv(timeout=self.timeout)
            self._key_lock.release()
            if msg != None:
                frame = self.canson.get_frame(msg.arbitration_id)
                name = self.canson.get_frame_name(frame)
                data = self.canson.get_frame_data(frame, msg.data)
                self.newData.emit(name, data)


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
