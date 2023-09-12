import os
from .base_converter import base_converter
from copy import deepcopy
import json
from tqdm import tqdm

default_label = {"annotations": [{
    "segmentation": [],
    "area": '',
    "iscrowd": '',
    "image_id": '',
    "bbox": [],
    "category_id": '',
    "id": '',
}]}


class converter(base_converter):
    def __init__(self, add_extra=True):
        super().__init__(default_label=default_label, add_extra=add_extra)
        self.converted_label = {}

    def convert(self, parsed_user_label):
        """
        original some dataset label format :
        "annotations": [
            {
                "segmentation": [[float]],
                "area": float,
                "iscrowd": bool,
                "image_id": int,
                "bbox": [float],
                "category_id": int,
                "id": int
            },
        ]
        """
        self.converted_label = deepcopy(self.default_label)
        for label in tqdm(parsed_user_label, desc="convert", leave=False):
            dict = {"category_id": label["class"],
                    "bbox": label["2dbbox"],
                    "id": label["file_name"]}

            if self.add_extra:
                for key, value in label["extra"].items():
                    dict[key] = value

            self.converted_label["annotations"].append(dict)

    def save(self, tgt_path, file_name):
        if not os.path.exists(tgt_path):
            os.makedirs(tgt_path)

        file_name, _ = os.path.splitext(file_name)
        if len(self.converted_label) != 0:
            with open(f'{tgt_path}/{file_name}.{self.extension}', 'w') as f:
                json.dump(self.converted_label, f, indent=4)
            self.converted_label = {}

    def run(self, parsed_user_label, tgt_path, file_name):
        self.convert(parsed_user_label)
        self.save(tgt_path, file_name)
