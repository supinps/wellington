import json


class CANson:
    def __init__(self, config_file="canson.json") -> None:
        self.config_file = config_file
        self.frame_desc = json.load(open(self.config_file))

    def get_frame_index(self, frame_id):
        i = 0
        for frame in self.frame_desc:
            if frame["id"] == frame_id:
                break
            i += 1
        return i

    def get_frame_name(self, index):
        frame_name = ""
        try:
            frame_name = self.frame_desc[index]["name"]
        except IndexError:
            frame_name = "unkown"
        return frame_name

    def get_frame_type(self, index):
        frame_type = ""
        try:
            frame_type = self.frame_desc[index]["type"]
        except IndexError:
            frame_type = "unknown"
        return frame_type

    def get_frame_data(self, frame_type, index, data):
        frame_data = None
        if frame_type == "int":
            frame_data = str(int.from_bytes(data, "little"))
        elif frame_type == "enum":
            key = str(int.from_bytes(data, "little"))
            if "categories" in self.frame_desc[index]:
                dict = self.frame_desc[index]["categories"]
                if key in dict:
                    frame_data = self.frame_desc[index]["categories"][key]
                else:
                    print("enum out of range")
            else:
                print("enum not defined in json file")
        elif frame_type == "intList":
            frame_data = str(list(data))
        return frame_data


if __name__ == "__main__":
    cs = CANson()
    data = 2
    index = cs.get_frame_index(101)
    print(cs.get_frame_name(index))
    print(
        cs.get_frame_data(cs.get_frame_type(index), index, data.to_bytes(4, "little"))
    )
