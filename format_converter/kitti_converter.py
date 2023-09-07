from .base_converter import base_converter


class Converter(base_converter):
    def __init__(self):
        super().__init__([-1] * 14)

    def convert(self, user_label):
        # TODO: convert kitti format one line each object
        kitti_label_dict = user_label
        return kitti_label_dict

    def save(self, tgt_path, converted_label):
        pass
