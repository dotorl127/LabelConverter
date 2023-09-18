import os
from .base_converter import base_converter
from copy import deepcopy
import json
from tqdm import tqdm

default_label = {
    "segmentation": [[float]],
    "area": float,
    "iscrowd": bool,
    "image_id": int,
    "bbox": [float],
    "category_id": int,
    "id": int
}


class converter(base_converter):
    def __init__(self, add_extra=True):
        super().__init__(default_label=default_label, add_extra=add_extra)
        self.converted_dict = {}

    def convert(self, parsed_user_label):
        """
        original COCO dataset label format :
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
        for label in tqdm(parsed_user_label, desc="convert", leave=False):
            converted_label = deepcopy(default_label)
            converted_label["category_id"] = label["class"]
            converted_label["bbox"] = label["2dbbox"]
            converted_label["id"] = label["file_name"]

            if self.add_extra:
                for key, value in label["extra"].items():
                    converted_label[key] = value

            if not self.split_file:
                if "annotations" not in self.converted_dict:
                    self.converted_dict["annotations"] = []
                self.converted_dict["annotations"].append(converted_label)
            else:
                if label["file_name"] not in self.converted_dict:
                    self.converted_dict["file_name"] = []
                self.converted_dict[label["file_name"]]["annotations"].append(converted_label)

    def save(self, tgt_path):
        if not os.path.exists(tgt_path):
            os.makedirs(tgt_path)

        if not self.split_file:
            with open(f'{tgt_path}/annotations.{self.extension}', 'w') as f:
                json.dump(self.converted_dict, f, indent=4)
        else:
            for key, value in self.converted_dict.items():
                file_name, _ = os.path.splitext(key)
                with open(f'{tgt_path}/{key}.{self.extension}', 'w') as f:
                    json.dump(value, f, indent=4)

    def run(self, parsed_user_label, tgt_path):
        if parsed_user_label["file_name"] is not None:
            self.split_file = True
        self.convert(parsed_user_label)
        self.save(tgt_path)
