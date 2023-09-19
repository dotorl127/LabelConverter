import os
from .base_converter import base_converter
from copy import deepcopy
from tqdm import tqdm
from collections import OrderedDict


class converter(base_converter):
    def __init__(self, add_extra=True, tgt_path=None):
        super().__init__(default_label=[-99] * 9, add_extra=add_extra, tgt_path=tgt_path, extension='txt')
        self.converted_dict = {}

    def convert(self, parsed_user_label):
        """
        original MOT17 label format :
        Frame number, Identity number, Bounding box left, Bounding box top, Bounding box width, Bounding box height, Confidence score, Class, Visibility
        """
        p_bar = tqdm(total=len(parsed_user_label), desc="annotations converting", leave=True)

        while parsed_user_label:
            converted_label = deepcopy(self.default_label)
            label = parsed_user_label.pop(0)

            file_name, _ = os.path.splitext(label["file_name"])
            file_name = f'{int(file_name)}' if file_name.isdecimal() else file_name
            converted_label[0] = file_name
            x1, y1, x2, y2 = list(map(float, label["2dbbox"]))
            converted_label[2:6] = x1, y1, round(x2 - x1, 3), round(y2 - y1, 3)
            converted_label[7] = label["class"]

            if self.add_extra:
                for _, value in label["extra"].items():
                    if type(value) is list:
                        converted_label += value
                    else:
                        converted_label += [value]

            if file_name not in self.converted_dict:
                self.converted_dict[file_name] = ''
            self.converted_dict[file_name] += ' '.join(list(map(str, converted_label))) + '\n'

            p_bar.update(1)

        p_bar.close()

    def save(self):
        with open(f'{self.tgt_path}/annotations.{self.extension}', 'w') as f:
            for key, value in tqdm(sorted(self.converted_dict.items(), key=lambda x: int(x[0])),
                                   desc="annotations saving", leave=True):
                f.write(value)
