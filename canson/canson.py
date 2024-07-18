import json

class CANson:
    def __init__(self, config_file="canson.json") -> None:
        self.config_file = config_file
        self.frame_desc = json.load(open(self.config_file))

    def get_frame_index(self, frame_id):
        i = 0 
        for frame in self.frame_desc:            
            if frame['id'] == frame_id:
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
    

if __name__=="__main__":
    cs = CANson()
    print(cs.get_frame_name(cs.get_frame_index(102)))