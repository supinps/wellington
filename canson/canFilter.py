import time
import can
import threading

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

    def set_filters(self, filters):
        self.bus.set_filters(filters)

    def recv(self):
        while True:
            if self.filters_changed:
                self.bus.set_filters(self.filters)
                print("filters changed")
                self.filters_changed = False
            msg = self.bus.recv(timeout=self.timeout)
            if msg != None:
                print(msg.arbitration_id)
                print(msg)


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
