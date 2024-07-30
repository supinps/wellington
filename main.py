import threading
import time
from canson.canson import CANson
from canson.canFilter import CANFilter


interface = "socketcan"
channel = "vcan0"
lock = threading.Lock()
canson = CANson()
can_filter = CANFilter(canson, channel=channel, interface=interface)


all_filters = canson.get_filters()
# can_filter.set_filters(all_filters)


def new_filters(all_filters, index_list):
    filters = []
    for index in index_list:
        filters.append(all_filters[index])
    return filters


def gui(can_filter: CANFilter):
    # gui_list = can_filter.get_gui_list()
    # print(f"{gui_list=}")
    time.sleep(5)
    gui_list = can_filter.get_gui_list()
    print(f"{gui_list=}")
    index_list = [0, 2]
    can_filter.set_filters(new_filters(all_filters, index_list))
    print("filters changed")
    # time.sleep(10)
    # gui_list = can_filter.get_gui_list()
    # print(f"{gui_list=}")
    # index_list = [0, 1, 2, 3]
    # can_filter.set_filters(new_filters(all_filters, index_list))
    # print("filters changed")
    while True:
        time.sleep(1)
        gui_list = can_filter.get_gui_list()
        print(f"{gui_list=}")


can_thread = threading.Thread(target=can_filter.recv)
gui_thread = threading.Thread(target=gui, args=[can_filter])

can_thread.start()
gui_thread.start()
# def can_thread():
