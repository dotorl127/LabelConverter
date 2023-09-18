import os
from .base_converter import base_converter
from copy import deepcopy
from tqdm import tqdm
import xmltodict
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ElementTree as EET

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
    def __init__(self, add_extra=True, split_file=True):
        super().__init__(default_label=default_label, split_file=split_file, add_extra=add_extra, extension='xml')
        self.converted_dict = {"annotations": []}

    def convert(self, parsed_user_label, tgt_path):
        """
        original VOC2012 label format :
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
        p_bar = tqdm(total=len(parsed_user_label), desc="annotations converting", leave=True)

        while parsed_user_label:
            converted_label = deepcopy(self.default_label)
            label = parsed_user_label.pop(0)

            converted_label["name"] = label["class"]
            converted_label["bndbox"]["xmin"] = label["2dbbox"][0]
            converted_label["bndbox"]["ymin"] = label["2dbbox"][1]
            converted_label["bndbox"]["xmax"] = label["2dbbox"][2]
            converted_label["bndbox"]["ymax"] = label["2dbbox"][3]

            if self.add_extra:
                for k, v in label["extra"].items():
                    converted_label[k] = v

            converted_label = {"objects": converted_label}

            self.converted_dict["annotations"].append(converted_label)
            p_bar.update(1)
        self.save(tgt_path, 'annotations', None)

    def save(self, tgt_path, suffix, converted_dict):
        if not os.path.exists(tgt_path):
            os.makedirs(tgt_path)

        xml = ET.fromstring(xmltodict.unparse(self.converted_dict, pretty=True))
        f = EET(xml)
        f.write(f'{tgt_path}/annotations.{self.extension}', xml_declaration=False)
