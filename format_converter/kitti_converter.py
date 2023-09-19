import os
from .base_converter import base_converter
from copy import deepcopy
from tqdm import tqdm


class converter(base_converter):
    def __init__(self, add_extra=True, tgt_path=None):
        super().__init__(default_label=[-99] * 13, add_extra=add_extra, tgt_path=tgt_path, extension='txt')
        self.converted_dict = {}

    def convert(self, parsed_user_label):
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

            if label["file_name"] not in self.converted_dict:
                self.converted_dict[label["file_name"]] = ''
            self.converted_dict[label["file_name"]] += ' '.join(list(map(str, converted_label))) + '\n'

            p_bar.update(1)
        p_bar.close()

    def save(self):
        for key, value in tqdm(self.converted_dict.items(), desc="annotations saving", leave=True):
            file_name, _ = os.path.splitext(key)
            file_name = f'{int(file_name):06d}' if file_name.isdecimal() else file_name
            with open(f'{self.tgt_path}/{file_name}.{self.extension}', 'w') as f:
                f.write(value)
