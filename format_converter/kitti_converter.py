import os
from .base_converter import base_converter
from copy import deepcopy
from tqdm import tqdm


class converter(base_converter):
    def __init__(self, add_extra=True):
        super().__init__(default_label=[-99] * 13, add_extra=add_extra, extension='txt')
        self.converted_str = ''
        self.converted_dict = {}

    def convert(self, parsed_user_label):
        """
        original kitti label format :
        type truncated occluded alpha bbox(x1, y1, x2, y2) dimensions(height, width, length) location(x, y, z) rotation_y socre
        """
        for label in tqdm(parsed_user_label, desc="convert", leave=False):
            converted_label = deepcopy(self.default_label)
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

            self.converted_str += ' '.join(list(map(str, converted_label))) + '\n'

            if label["file_name"] is not None:
                self.converted_dict[label["file_name"]] += self.converted_str
                self.converted_str = ''

    def save(self, tgt_path, file_name):
        if not os.path.exists(tgt_path):
            os.makedirs(tgt_path)

        file_name, _ = os.path.splitext(file_name)
        if self.converted_str != '':
            with open(f'{tgt_path}/{file_name}.{self.extension}', 'w') as f:
                f.write(self.converted_str)
            self.converted_str = ''

        if len(self.converted_dict) != 0:
            for key, value in self.converted_dict.items():
                file_name, _ = os.path.splitext(key)
                with open(f'{tgt_path}/{file_name}.{self.extension}', 'w') as f:
                    f.write(value)

    def run(self, parsed_user_label, tgt_path, file_name):
        self.convert(parsed_user_label)
        self.save(tgt_path, file_name)
