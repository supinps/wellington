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
    def __init__(
        self, canson: CANson, channel="vcan0", interface="socketcan", filters=None
    ) -> None:
        super().__init__()
        self.canson = canson
        self.channel = channel
        self.interface = interface
        self.bus = can.Bus(channel, interface)
        self.filters = filters
        self.filters_changed = False
        self.timeout = 0.5
        self.__gui_list = []
        self.max_num_entry = 10
        self._key_lock = threading.Lock()
        self._key_lock2 = threading.Lock()
        self.set_filters()

    def set_filters(self, filters=None):
        if filters == None:
            filters = self.canson.get_filters()
        with self._key_lock2:
            self.bus.set_filters(filters)

    def get_gui_list(self):
        with self._key_lock:
            return self.__gui_list

    def set_gui_list(self, gui_list):
        with self._key_lock:
            self.__gui_list = gui_list

    def __append_gui_list(self, name, data):
        gui_list = self.get_gui_list()
        if len(gui_list) < self.max_num_entry:
            gui_list.append([name, data])
        else:
            gui_list.pop(0)
            gui_list.append([name, data])
        self.set_gui_list(gui_list)

    def run(self):
        while True:
            self._key_lock2.acquire()
            msg = self.bus.recv(timeout=self.timeout)
            self._key_lock2.release()
            if msg != None:
                # print(msg.arbitration_id)
                # print(msg.data)
                # print(msg)
                frame = self.canson.get_frame(msg.arbitration_id)
                name = self.canson.get_frame_name(frame)
                data = self.canson.get_frame_data(frame, msg.data)
                self.newData.emit(name, data)
                self.__append_gui_list(name, data)


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
