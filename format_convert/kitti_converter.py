from base_converter import base_Converter


class kitti_converter(base_Converter):
    def __init__(self):
        super().__init__()

    @classmethod
    def converter(cls, user_label):
        kitti_label_dict = user_label
        return kitti_label_dict

    @classmethod
    def save(cls, tgt_path, converted_label):
        pass
