import os
from .base_converter import base_converter
from copy import deepcopy
from tqdm import tqdm
import xmltodict
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ElementTree as EET
from collections import defaultdict

default_label = {
    'name': '',
    'pose': '',
    'truncated': '',
    'difficult': '',
    'bndbox': {
        'xmin': '',
        'ymin': '',
        'xmax': '',
        'ymax': ''
    }
}


class converter(base_converter):
    def __init__(self, add_extra=True):
        super().__init__(default_label=default_label, add_extra=add_extra, extension='txt')
        self.converted_dict = {}

    def convert(self, parsed_user_label):
        """
        original voc12 label format :
        <'annotation'>
            <'object'>
                <'name'></'name'>
                <'pose'></'pose'>,
                <'truncated'></'truncated'>
                <'difficult'></'difficult'>
                <'bndbox'>
                    <'xmin'></'xmin'>
                    <'ymin'></'ymin'>
                    <'xmax'></'xmax'>
                    <'ymax'></'ymax'>
                </'bndbox'>
            </'object'>
        </'annotation'>
        """
        for label in tqdm(parsed_user_label, desc="convert", leave=False):
            converted_label = deepcopy(self.default_label)
            converted_label["name"] = label["class"]
            converted_label["bndbox"]["xmin"] = label["2dbbox"][0]
            converted_label["bndbox"]["ymin"] = label["2dbbox"][1]
            converted_label["bndbox"]["xmax"] = label["2dbbox"][2]
            converted_label["bndbox"]["ymax"] = label["2dbbox"][3]

            if self.add_extra:
                for k, v in label["extra"].items():
                    converted_label[k] = v

            converted_label = {"objects": converted_label}

            if label["file_name"] is not None:
                if label["file_name"] not in self.converted_dict:
                    self.converted_dict[label["file_name"]] = defaultdict(list)
                self.converted_dict[label["file_name"]]["annotations"].append(converted_label)

    def save(self, tgt_path, file_name):
        if not os.path.exists(tgt_path):
            os.makedirs(tgt_path)

        file_name, _ = os.path.splitext(file_name)
        if len(self.converted_dict) != 0:
            xml = ET.fromstring(xmltodict.unparse(self.converted_dict, pretty=True))
            f = EET(xml)
            f.write(f'{tgt_path}/{file_name}.{self.extension}', xml_declaration=False)

    def run(self, parsed_user_label, tgt_path, file_name):
        self.convert(parsed_user_label)
        self.save(tgt_path, file_name)
