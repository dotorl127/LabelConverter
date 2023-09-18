from abc import ABC, abstractmethod


class base_converter(ABC):
    def __init__(self, default_label=None, add_extra=True, split_file=True, extension=None):
        self.default_label = default_label
        self.add_extra = add_extra
        self.extension = extension
        self.split_file = split_file

    @abstractmethod
    def convert(self, parsed_user_label, tgt_path):
        pass

    @abstractmethod
    def save(self, tgt_path):
        pass

    @staticmethod
    def xyxy2ccwh(coord):
        x1, y1, x2, y2 = float(coord)
        w = x2 - x1
        h = y2 - y1
        return [x1 + w / 2,
                y1 + h / 2,
                w,
                h]
