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
            for d in self.config["class"]:
                class_label = class_label[d]
            label_parsed["class"] = class_label

            for dd in self.config["2Dbox"]["coord"]:
                bbox2d_label = label
                for d in dd:
                    bbox2d_label = bbox2d_label[d]
                label_parsed["2dbbox"].append(bbox2d_label)

            if self.config["2Dbox"]["center"]:
                cx, cy, w, d = label_parsed["2dbbox"]
                label_parsed["2dbbox"] = [cx - w / 2,
                                    cy - h / 2,
                                    cx + w / 2,
                                    cy + h / 2]

            for dd in self.config["3Dbox"]["loc"]:
                bbox3d_label = label
                for d in dd:
                    bbox3d_label = bbox3d_label[d]
                label_parsed["3dbbox"]["loc"].append(bbox3d_label)

            for dd in self.config["3Dbox"]["dim"]:
                bbox3d_label = label
                for d in dd:
                    bbox3d_label = bbox3d_label[d]
                label_parsed["3dbbox"]["dim"].append(bbox3d_label)

            for dd in self.config["3Dbox"]["rot"]:
                bbox3d_label = label
                for d in dd:
                    bbox3d_label = bbox3d_label[d]
                label_parsed["3dbbox"]["rot"].append(bbox3d_label)

            for dd in self.config["extra"]:
                extra_label = label
                for d in dd:
                    extra_label = extra_label[d]
                label_parsed["extra"].append(extra_label)

            label_list.append(label_parsed)

        return label_list
