import time
import can
import threading

interface = "socketcan"
channel = "vcan0"

filters = [
    {"can_id": 451, "can_mask": 0x7FF, "extended": False},
    {"can_id": 451, "can_mask": 0x1FFFFFFF, "extended": True},
]
# bus = can.interface.Bus(channel=channel, interface=interface, can_filters=filters)

filters_changed = False


class FilterCan:
    def __init__(self, channel, interface, **kwargs) -> None:
        self.channel = channel
        self.interface = interface
        self.bus = can.Bus(channel, interface)
        # super().__init__(channel, can_interface=interface, **kwargs)

    # def send(self, msg: can.Message, timeout: float | None = None) -> None:
    #     try:
    #         super().send(msg, timeout)
    #     except NotImplementedError:
    #         pass
    # def send(self, msg: can.Message, timeout: float | None = None) -> None:
    #     pass
    # return super().send(msg, timeout)

    def set_filters(self, filters):
        self.bus.set_filters(filters)

    # def get_frame_info(self):
    #     pass

    def recv(self):
        global filters_changed
        global filters
        while True:
            if filters_changed:
                self.bus.set_filters(filters=filters)
                print("filters changed")
                filters_changed = False
            msg = self.bus.recv(timeout=1)
            if msg != None:
                print(msg.arbitration_id)
                print(msg)
        # while True:
        #     if filters_changed:
        #         bus.set_filters(filters=filters)
        #         print("filters changed")
        #         filters_changed = False
        #     with self.bus as bus:
        #         for msg in bus:
        #             data, id = msg.arbitration_id, msg.data
        #             print(f"{data=} {id=}")


def get_frame_info(id):
    return "humidity", "int", None


def filter():
    fc = FilterCan(channel, interface)
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


# bus = can.interface.Bus(channel=channel, interface=interface)

# bus = can.Bus(channel=channel, interface=interface)
# with bus:
#     for msg in bus:
#         # print(msg.arbitration_id)
#         data, id = msg.arbitration_id, msg.data
#         frame_name, data_type, enum_list = get_frame_info(id)
#         if frame_name == None:
#             print(f"{id} is doesn't exist in json file")
#         if data_type == None:
#             data_type = "int"
#         if data_type == "int":
#             decoded_data = int.from_bytes(data, "little")
#             print(decoded_data)

#         # print(msg.data)
#         # print(type(msg))
#         # print(str(msg))
#         # print(msg.data.decode())
#         # print(list(msg.data))
#         print(int.from_bytes(msg.data, "little"))
