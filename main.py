from canson.canFilter import CANFilter
from ui.app import UI


class CANVisualizer:
    def __init__(self) -> None:
        self.ui = UI()        
        self.can_filter = CANFilter()
        self.can_filter.newData.connect(self.ui.add_new_frame)
        self.can_filter.Device.connect(self.ui.handle_Device)
        self.ui.startBus.connect(self.can_filter.startBus)
        self.ui.stopBus.connect(self.can_filter.stopBus)
        self.ui.populateFrameNames(self.can_filter.canson.get_gui_frame_details())
        self.ui.add_interfaces(self.can_filter.configson.get_interfaces())
        self.ui.get_channel_list(self.can_filter.configson.get_channels_gui())
        self.ui.filterChanged.connect(self.can_filter.set_index_list)
        self.ui.update_channels()
        self.ui.busData.connect(self.can_filter.bus_init)
        self.ui.DisConnect.connect(self.can_filter.quit)
        self.ui.app.aboutToQuit.connect(self.can_filter.quit)

if __name__ == "__main__":
    canviz = CANVisualizer()
    canviz.ui.start()
