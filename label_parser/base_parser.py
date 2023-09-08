from abc import ABC, abstractmethod
from utlis import label_dict


class base_parser(ABC):
    def __init__(self, config):
        self.config = config
        self.label_dict = label_dict.label_

    @staticmethod
    def check_none_txt(lst, idx):
        if idx is None:
            return None
        else:
            assert idx < len(lst), 'Invalid index list'
            return lst[idx]

    @staticmethod
    def check_none_json(key, key_in_dict):
        if key_in_dict is None:
            return None
        else:
            for value in key_in_dict:
                if type(key) is list:
                    value = int(value)
                    if value < len(key):
                        key = key[value]
                elif type(key) is dict:
                    if value in key:
                        key = key[value]
            return key

    @staticmethod
    def ccwh2xyxy(coord):
        cx, cy, w, h = float(coord)
        return [cx - w / 2,
                cy - h / 2,
                cx + w / 2,
                cy + h / 2]

    @abstractmethod
    def parse(self, user_label_path):
        pass
