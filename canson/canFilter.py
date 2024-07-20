import time
import can
import threading
from .canson import CANson

__all__ = ["CANFilter"]

interface = "socketcan"
channel = "vcan0"

filters = [
    {"can_id": 451, "can_mask": 0x7FF, "extended": False},
    {"can_id": 451, "can_mask": 0x1FFFFFFF, "extended": True},
]


class CANFilter:
    def __init__(self, channel="vcan0", interface="socketcan", filters=None) -> None:
        self.channel = channel
        self.interface = interface
        self.bus = can.Bus(channel, interface)
        self.filters = filters
        self.filters_changed = False
        self.timeout = 1
        self.__gui_list = []
        self.max_num_entry = 10
        self._key_lock = threading.Lock()

    def set_filters(self, filters):
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

    def recv(self, canson: CANson):
        while True:
            msg = self.bus.recv(timeout=self.timeout)
            if msg != None:
                # print(msg.arbitration_id)
                # print(msg.data)
                # print(msg)
                frame = canson.get_frame(msg.arbitration_id)
                name = canson.get_frame_name(frame)
                data = canson.get_frame_data(frame, msg.data)
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
