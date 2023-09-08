import os
from .base_converter import base_converter
from copy import deepcopy


class Converter(base_converter):
    def __init__(self, add_extra=True):
        super().__init__(default_label=[-99] * 13, add_extra=add_extra, extension='.txt')
        self.converted_label = None

    def convert(self, parsed_user_label):
        """
        original kitti label format :
        type truncated occluded alpha bbox(x1, y1, x2, y2) dimensions(height, width, length) location(x, y, z) rotation_y socre
        """
        for label in parsed_user_label:
            self.converted_label = deepcopy(self.default_label)
            self.converted_label[0] = label["class"]
            self.converted_label[4:8] = label["2dbbox"]
            self.converted_label[8] = label["3dbbox"]["dim"]["height"]
            self.converted_label[9] = label["3dbbox"]["dim"]["width"]
            self.converted_label[10] = label["3dbbox"]["dim"]["length"]
            self.converted_label[11] = label["3dbbox"]["rot"]["yaw"]

            if self.add_extra:
                for _, value in label["extra"].items():
                    self.converted_label += value

            self.converted_label = ' '.join(list(map(str, self.converted_label)))

    def save(self, tgt_path, file_name):
        file_name, _ = os.path.splitext(file_name)
        if self.converted_label is not None:
            with open(f'{tgt_path}/{file_name}.{self.extension}', 'w') as f:
                f.write(self.converted_label)
            self.converted_label = None

    def run(self, parsed_user_label, tgt_path, file_name):
        self.convert(parsed_user_label)
        self.save(tgt_path, file_name)
