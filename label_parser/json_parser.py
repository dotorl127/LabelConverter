from .base_parser import base_Parser
from utlis.label_dict import label_
import json


class Parser(base_Parser):
    def __init__(self, config):
        super().__init__(config)

    def parse(self, user_label_path):
        label_list = []

        with open(user_label_path, 'r') as f:
            labels = json.load(f)

        for label in labels:
            label_parsed = self.label_dict.copy()

            class_label = label
            label_parsed["class"] = self.check_none_json(class_label, self.config["class"])

            for k_in_d in self.config["2Dbox"]["coord"]:
                bbox2d_label = label
                label_parsed["2dbbox"].append(self.check_none_json(bbox2d_label, k_in_d))

            if self.config["2Dbox"]["center"]:
                cx, cy, w, h = list(map(float, label_parsed["2dbbox"]))
                label_parsed["2dbbox"] = [cx - w / 2,
                                          cy - h / 2,
                                          cx + w / 2,
                                          cy + h / 2]

            for k_in_d in self.config["3Dbox"]["loc"]:
                bbox3d_label = label
                label_parsed["3dbbox"]["loc"].append(self.check_none_json(bbox3d_label, k_in_d))

            for k_in_d in self.config["3Dbox"]["dim"]:
                bbox3d_label = label
                label_parsed["3dbbox"]["dim"].append(self.check_none_json(bbox3d_label, k_in_d))

            for k_in_d in self.config["3Dbox"]["rot"]:
                bbox3d_label = label
                for d in k_in_d:
                    bbox3d_label = bbox3d_label[d]
                label_parsed["3dbbox"]["rot"].append(self.check_none_json(bbox3d_label, k_in_d))

            for k_in_d in self.config["extra"]:
                extra_label = label
                label_parsed["extra"].append(self.check_none_json(extra_label, k_in_d))

            label_list.append(label_parsed)

        return label_list
