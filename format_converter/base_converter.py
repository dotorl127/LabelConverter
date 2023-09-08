from abc import ABC, abstractmethod


class base_converter(ABC):
    def __init__(self, default_label, add_extra=True, extension=None):
        self.default_label = default_label
        self.add_extra = add_extra
        self.extension = extension

    @abstractmethod
    def convert(self, parsed_user_label):
        pass

    @abstractmethod
    def save(self, tgt_path, file_name):
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

    @abstractmethod
    def run(self, parsed_user_label, tgt_path, file_name):
        pass
