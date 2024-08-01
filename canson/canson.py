import json
import sys
import os


__all__ = ["CANson"]
canson_dir = os.path.dirname(__file__)
# Construct the full path to the JSON file
json_path = os.path.join(canson_dir, "canson.json")


class CANson:
    def __init__(self, config_file=json_path) -> None:
        self.config_file = config_file
        self.frame_desc = json.load(open(self.config_file))
        self.mask_dict = {True: 0x1FFFFFFF, False: 0x7FF}
        self.valid_frame_id_dict = {True: 2**29, False: 2**11}
        self.valid_frame_list = self.__get_valid_frames()

    def get_frame(self, frame_id):
        for frame in self.valid_frame_list:
            if int(frame["id"], 0) == frame_id:
                return frame
        return None

    def get_frame_name(self, frame):
        return frame["name"]

    def get_frame_type(self, frame):
        return frame["type"]

    def __isValid(self, frame):
        if not all(key in frame for key in ["name", "id", "type"]):
            return False
        if not isinstance(frame["name"], (str)):
            return False
        extended = False
        if "extended" in frame:
            ext = frame["extended"]
            if not isinstance(ext, (bool)):
                return False
            else:
                extended = ext
        try:
            frame_id = int(frame["id"], 0)
            if not (0 <= frame_id < self.valid_frame_id_dict[extended]):
                return False
        except ValueError:
            return False

        if frame["type"] not in ["int", "intlist", "enum"]:
            return False
        elif frame["type"] == "enum":
            if not "categories" in frame:
                return False
            elif not isinstance(frame["categories"], (dict)):
                return False
        return True

    def __get_valid_frames(self):
        valid_frames = []
        for frame in self.frame_desc:
            if self.__isValid(frame):
                valid_frames.append(frame)
        return valid_frames

    def get_frame_data(self, frame, data):
        frame_type = self.get_frame_type(frame)

        match frame_type:

            case "int":
                frame_data = str(int.from_bytes(data, "little"))

            case "enum":
                key = str(int.from_bytes(data, "little"))
                enum_dict = frame["categories"]
                if key in enum_dict:
                    frame_data = frame["categories"][key]
                else:
                    frame_data = None
                    print("enum out of range")

            case "intlist":
                frame_data = str(list(data))

            case _:
                frame_data = None

        return frame_data

    def get_filters(self):
        filter_list = []
        for frame in self.valid_frame_list:
            extended = False
            if "extended" in frame:
                extended = frame["extended"]
            frame_id = int(frame["id"], 0)
            filter_list.append(
                {
                    "can_id": frame_id,
                    "can_mask": self.mask_dict[extended],
                    "extended": extended,
                }
            )
        return filter_list

class ConfigSon:
    def __init__(self) -> None:
        self.json_path = os.path.join(canson_dir, "config.json")
        self.file = json.load(open(self.json_path))
        self.validItems = self.get_valid_items()
    
    def get_valid_items(self) -> list:
        valid_items = []
        for item in self.file:
            if self.__isValid(item):
                valid_items.append(item)
        return valid_items
    
    @staticmethod
    def __isValid(item: dict) -> bool:
        if not all(key in item for key in ["interface", "channel"]):
            print("l")
            return False
        if not isinstance(item["interface"], (str)):
            return False
        if not all(isinstance(i, (str, int)) for i in item["channel"]):
            return False
        return True


if __name__ == "__main__":
    # cs = CANson()
    # data = 2
    # frame = cs.get_frame(0x101)
    # print(cs.get_frame_name(frame))
    # print(cs.get_frame_data(frame, data.to_bytes(4, "little")))
    # print(cs.get_frame_type(frame))
    # print(cs.get_filters())
    # print(cs.valid_frame_list)

    cs = ConfigSon()
    print(cs.file)
    print(cs.validItems)
