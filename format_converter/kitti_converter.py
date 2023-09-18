import os
from .base_converter import base_converter
from copy import deepcopy
from tqdm import tqdm


class converter(base_converter):
    def __init__(self, add_extra=True, split_file=True):
        super().__init__(default_label=[-99] * 13, add_extra=add_extra, split_file=split_file, extension='txt')

    def convert(self, parsed_user_label, tgt_path):
        """
        original KITTI label format :
        type truncated occluded alpha bbox(x1, y1, x2, y2) dimensions(height, width, length) location(x, y, z) rotation_y socre
        """
        p_bar = tqdm(total=len(parsed_user_label), desc="annotations converting", leave=True)

        while parsed_user_label:
            converted_label = deepcopy(self.default_label)
            label = parsed_user_label.pop(0)

            converted_label[0] = label["class"]
            converted_label[4:8] = label["2dbbox"]
            converted_label[8] = label["3dbbox"]["dim"]["height"]
            converted_label[9] = label["3dbbox"]["dim"]["width"]
            converted_label[10] = label["3dbbox"]["dim"]["length"]
            converted_label[11] = label["3dbbox"]["rot"]["yaw"]

            if self.add_extra:
                for _, value in label["extra"].items():
                    if type(value) is list:
                        converted_label += value
                    else:
                        converted_label += [value]

            converted_str = ' '.join(list(map(str, converted_label))) + '\n'
            self.save(tgt_path, label["file_name"], converted_str)
            p_bar.update(1)

    def save(self, tgt_path, suffix, converted_str):
        if not os.path.exists(tgt_path):
            os.makedirs(tgt_path, exist_ok=True)

        with open(f'{tgt_path}/{suffix}.{self.extension}', 'a') as f:
            f.write(converted_str)
