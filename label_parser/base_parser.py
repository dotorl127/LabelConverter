from abc import ABC, abstractmethod
from utils import label_dict


class base_parser(ABC):
    def __init__(self, config):
        self.config = config
        self.label_dict = label_dict.label_
        self.p_bar = None

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
                if isinstance(key, list):
                    value = int(value)
                    assert value < len(key), f'{value} out of range {len(key)}'
                    key = key[value]
                elif isinstance(key, dict):
                    assert value in key, f'{value} not in {key}'
                    key = key[value]
            return key

    @staticmethod
    def ccwh2xyxy(coord):
        cx, cy, w, h = list(map(float, coord))
        return [round(cx - w / 2, 3),
                round(cy - h / 2, 3),
                round(cx + w / 2, 3),
                round(cy + h / 2, 3)]

    @staticmethod
    def xywh2xyxy(coord):
        x, y, w, h = list(map(float, coord))
        return [round(x, 3),
                round(y, 3),
                round(x + w, 3),
                round(y + h, 3)]

    @abstractmethod
    def parse(self, user_label_path, p_bar_need):
        pass
