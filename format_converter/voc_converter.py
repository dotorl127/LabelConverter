import os
from .base_converter import base_converter
from copy import deepcopy
from tqdm import tqdm
import xmltodict
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ElementTree as EET

default_label = {
    'name': '-99',
    'pose': '-99',
    'truncated': '-99',
    'difficult': '-99',
    'bndbox': {
        'xmin': '-99',
        'ymin': '-99',
        'xmax': '-99',
        'ymax': '-99'
    }
}


class converter(base_converter):
    def __init__(self, add_extra=True, tgt_path=None):
        super().__init__(default_label=default_label, add_extra=add_extra, tgt_path=tgt_path, extension='xml')
        self.converted_dict = {}

    def convert(self, parsed_user_label):
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

            if label["file_name"] not in self.converted_dict:
                self.converted_dict[label["file_name"]] = {"objects": []}

            self.converted_dict[label["file_name"]]["objects"].append(converted_label)

            p_bar.update(1)

    def save(self):
        for key, value in tqdm(self.converted_dict.items(), desc="annotations saving", leave=True):
            file_name, _ = os.path.splitext(key)
            annos = {"annotations": value}
            xml = ET.fromstring(xmltodict.unparse(annos, full_document=False, pretty=True))
            f = EET(xml)
            file_name = f'{int(file_name):06d}' if file_name.isdecimal() else file_name
            f.write(f'{self.tgt_path}/{file_name}.{self.extension}', xml_declaration=False)
