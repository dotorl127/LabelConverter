import os
from .base_parser import base_parser
from copy import deepcopy
from tqdm import tqdm


class parser(base_parser):
    def __init__(self, config):
        super().__init__(config)

    def parse(self, user_label_path, p_bar_need):
        label_list = []

        with open(user_label_path, 'r') as f:
            labels = f.readlines()

        if p_bar_need:
            self.p_bar = tqdm(total=len(labels), desc="annotations parsing", leave=True)

        for label in labels:
            label_parsed = deepcopy(self.label_dict)

            split_label = label.strip().split(self.config["split_key"])

            label_parsed["class"] = self.check_none_txt(split_label, self.config["class"])

            label_parsed["2dbbox"] = [self.check_none_txt(split_label, self.config["2Dbox"]["coord"][0]),
                                      self.check_none_txt(split_label, self.config["2Dbox"]["coord"][1]),
                                      self.check_none_txt(split_label, self.config["2Dbox"]["coord"][2]),
                                      self.check_none_txt(split_label, self.config["2Dbox"]["coord"][3])]

            if self.config["2Dbox"]["coord_type"] != 'xyxy':
                label_parsed["2dbbox"] \
                    = self.__getattribute__(f'{self.config["2Dbox"]["coord_type"]}2xyxy')(label_parsed["2dbbox"])

            label_parsed["3dbbox"]["loc"]["x"] = self.check_none_txt(split_label, self.config["3Dbox"]["loc"]["x"])
            label_parsed["3dbbox"]["loc"]["y"] = self.check_none_txt(split_label, self.config["3Dbox"]["loc"]["y"])
            label_parsed["3dbbox"]["loc"]["z"] = self.check_none_txt(split_label, self.config["3Dbox"]["loc"]["z"])
            label_parsed["3dbbox"]["dim"]["width"] = self.check_none_txt(split_label, self.config["3Dbox"]["dim"]["width"])
            label_parsed["3dbbox"]["dim"]["length"] = self.check_none_txt(split_label, self.config["3Dbox"]["dim"]["length"])
            label_parsed["3dbbox"]["dim"]["height"] = self.check_none_txt(split_label, self.config["3Dbox"]["dim"]["height"])
            label_parsed["3dbbox"]["rot"]["roll"] = self.check_none_txt(split_label, self.config["3Dbox"]["rot"]["roll"])
            label_parsed["3dbbox"]["rot"]["pitch"] = self.check_none_txt(split_label, self.config["3Dbox"]["rot"]["pitch"])
            label_parsed["3dbbox"]["rot"]["yaw"] = self.check_none_txt(split_label, self.config["3Dbox"]["rot"]["yaw"])

            if self.config["extra"] is not None:
                for key, value in self.config["extra"].items():
                    label_parsed["extra"][key] = self.check_none_txt(split_label, value)

            if self.config["file_name"] is not None:
                label_parsed["file_name"] = str(self.check_none_txt(split_label, self.config["file_name"]))
            else:
                label_parsed["file_name"] = str(os.path.basename(user_label_path))

            label_list.append(label_parsed)

            if self.p_bar:
                self.p_bar.update(1)

        if self.p_bar:
            self.p_bar.close()

        return label_list
