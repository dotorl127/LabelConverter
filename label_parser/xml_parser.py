from .base_parser import base_parser
import json
from copy import deepcopy
import xmltodict


class parser(base_parser):
    def __init__(self, config):
        super().__init__(config)

    def parse(self, user_label_path):
        label_list = []

        with open(user_label_path, 'r') as f:
            labels = f.read()
            labels = xmltodict.parse(labels)

            for label in self.check_none_json(labels, self.config["anno_key"]):
                label_parsed = deepcopy(self.label_dict)

                class_label = label
                label_parsed["class"] = self.check_none_json(class_label, self.config['class'])

                for k_in_d in self.config["2Dbox"]["coord"]:
                    bbox2d_label = label
                    label_parsed["2dbbox"].append(self.check_none_json(bbox2d_label, k_in_d))

                    if self.config["2Dbox"]["is_center"] and None not in label_parsed["2dbbox"]:
                        label_parsed["2dbbox"] = self.ccwh2xyxy(label_parsed["2dbbox"])

                if self.config["extra"] is not None:
                    for key, value in self.config["extra"].items():
                        extra_label = label
                        label_parsed["extra"][key] = self.check_none_json(extra_label, value)

                if self.config["file_name"] is not None:
                    file_name_label = label
                    label_parsed["file_name"] = self.check_none_json(file_name_label, self.config["file_name"])

            label_list.append(label_parsed)

        return label_list
