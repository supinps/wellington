import time
import can
import threading
from .canson import CANson
from PySide6.QtCore import QThread, Signal

__all__ = ["CANFilter"]

interface = "socketcan"
channel = "vcan0"

filters = [
    {"can_id": 451, "can_mask": 0x7FF, "extended": False},
    {"can_id": 451, "can_mask": 0x1FFFFFFF, "extended": True},
]


class CANFilter(QThread):
    newData = Signal(str, str)
    noDevice = Signal(bool)

    def __init__(self, channel="vcan0", interface="socketcan", filters=None) -> None:
        super().__init__()
        self.canson = CANson()
        self.channel = channel
        self.interface = interface
        self.bus = None
        self.filters = filters
        self.timeout = 0.5
        self._key_lock = threading.Lock()
        # self.initialization()

    def initialization(self):
        try:
            self.bus = can.Bus(channel, interface)
            self.set_filters()
            return "CAN device connected successfully"
        except OSError:
            self.noDevice.emit(False)
            return "CAN device connection failed"

    def set_filters(self, filters=None):
        if filters == None:
            filters = self.canson.get_filters()
        with self._key_lock:
            self.bus.set_filters(filters)

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
