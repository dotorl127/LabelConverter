from .base_parser import base_parser
import json
from copy import deepcopy
import xml.etree.ElementTree as Et
from xml.etree.ElementTree import Element, ElementTree


class parser(base_parser):
    def __init__(self, config):
        super().__init__(config)

    def parse(self, user_label_path):
        label_list = []

        with open(user_label_path, 'r') as f:
            tree = Et.parse(f)
            root = tree.getroot()
            objects = root.findall(self.config['anno_key'])

            for object in objects:
                label_parsed = deepcopy(self.label_dict)
                label_parsed["class"] = object.find(self.config['class']).text

                for idx, k in enumerate(self.config['2Dbox']['cood']):
                    if idx == 1:
                        bndbox = object.find(k)
                    if idx == 2:
                        label_parsed["2dbbox"].append(bndbox.find(k).text)

                for k, v in self.config["extra"].items():
                    label_parsed[k] = object.find(v).text

            label_list.append(label_parsed)

        return label_list
