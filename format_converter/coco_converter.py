import os
from .base_converter import base_converter
from copy import deepcopy
import json
from tqdm import tqdm

default_label = {
    "segmentation": [[-99]],
    "area": '-99',
    "iscrowd": '-99',
    "image_id": '-99',
    "bbox": [-99],
    "category_id": '-99',
    "id": '-99',
}


class converter(base_converter):
    def __init__(self, add_extra=True, tgt_path=None):
        super().__init__(default_label=default_label, add_extra=add_extra, tgt_path=tgt_path, extension='json')
        self.converted_dict = {"annotations": []}

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
        p_bar = tqdm(total=len(parsed_user_label), desc="annotations converting", leave=True)

        while parsed_user_label:
            converted_label = deepcopy(self.default_label)
            label = parsed_user_label.pop(0)

            converted_label["category_id"] = label["class"]
            converted_label["bbox"] = label["2dbbox"]
            converted_label["id"] = label["file_name"]

            if self.add_extra:
                for key, value in label["extra"].items():
                    converted_label[key] = value

            self.converted_dict["annotations"].append(converted_label)

            p_bar.update(1)
        p_bar.close()

    def save(self):
        with open(f'{self.tgt_path}/annotations.{self.extension}', 'w') as f:
            json.dump(self.converted_dict, f, indent=4)
