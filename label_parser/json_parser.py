from .base_parser import base_parser
import json
from copy import deepcopy


class parser(base_parser):
    def __init__(self, config):
        super().__init__(config)

    def parse(self, user_label_path):
        label_list = []

        with open(user_label_path, 'r') as f:
            labels = json.load(f)

        for label in labels[self.config["split"]]:
            label_parsed = deepcopy(self.label_dict)

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
                label_parsed["3dbbox"]["rot"].append(self.check_none_json(bbox3d_label, k_in_d))

            if self.config["extra"] is not None:
                for key, value in self.config["extra"].items():
                    extra_label = label
                    label_parsed["extra"][key] = self.check_none_json(extra_label, value)

            label_list.append(label_parsed)

        return label_list
