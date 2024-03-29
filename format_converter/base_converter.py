from abc import ABC, abstractmethod


class base_converter(ABC):
    def __init__(self, default_label=None, add_extra=True, tgt_path=None, extension=None):
        self.default_label = default_label
        self.add_extra = add_extra
        self.extension = extension
        self.tgt_path = tgt_path

    @abstractmethod
    def convert(self, parsed_user_label):
        pass

    @abstractmethod
    def save(self):
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
