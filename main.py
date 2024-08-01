import threading
import time
from canson.canson import CANson
from canson.canFilter import CANFilter
from ui.app import UI


class CANVisualizer:
    def __init__(self) -> None:
        self.ui = UI()
        self.interface = "socketcan"
        self.channel = "vcan0"
        self.can_filter = CANFilter(channel=self.channel, interface=self.interface)
        self.can_filter.newData.connect(self.ui.add_new_frame)
        self.can_filter.noDevice.connect(self.ui.enable_start_button)
        self.can_filter.initialization()
        # self.ui.enable_start_button(False)
        self.ui.startBtn.clicked.connect(self.can_filter.start)
        self.ui.populateFrameNames(self.can_filter.canson.get_gui_frame_details())
        # self.can_filter.start()


# interface = "socketcan"
# channel = "vcan0"
# lock = threading.Lock()
# canson = CANson()
# can_filter = CANFilter(canson, channel=channel, interface=interface)


# all_filters = canson.get_filters()
# # can_filter.set_filters(all_filters)


# def new_filters(all_filters, index_list):
#     filters = []
#     for index in index_list:
#         filters.append(all_filters[index])
#     return filters


# def gui(can_filter: CANFilter):
#     # gui_list = can_filter.get_gui_list()
#     # print(f"{gui_list=}")
#     time.sleep(5)
#     gui_list = can_filter.get_gui_list()
#     print(f"{gui_list=}")
#     index_list = [0, 2]
#     can_filter.set_filters(new_filters(all_filters, index_list))
#     print("filters changed")
#     # time.sleep(10)
#     # gui_list = can_filter.get_gui_list()
#     # print(f"{gui_list=}")
#     # index_list = [0, 1, 2, 3]
#     # can_filter.set_filters(new_filters(all_filters, index_list))
#     # print("filters changed")
#     while True:
#         time.sleep(1)
#         gui_list = can_filter.get_gui_list()
#         print(f"{gui_list=}")


# can_thread = threading.Thread(target=can_filter.recv)
# gui_thread = threading.Thread(target=gui, args=[can_filter])

# can_thread.start()
# gui_thread.start()
# # def can_thread():


if __name__ == "__main__":
    canviz = CANVisualizer()
    canviz.ui.start()
