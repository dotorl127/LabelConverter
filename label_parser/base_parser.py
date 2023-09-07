from abc import ABC, abstractmethod
from utlis import label_dict


class base_Parser(ABC):
    def __init__(self, config):
        self.config = config
        self.label_dict = label_dict.label_

    @staticmethod
    def check_none_txt(lst, idx):
        assert idx < len(lst), 'Invalid index list'

        if lst[idx] is None:
            return None
        else:
            return lst[idx]

    @staticmethod
    def check_none_json(key, key_in_dict):
        if key_in_dict is None:
            return None
        else:
            for value in key_in_dict:
                key = key[value]
            return key

    @abstractmethod
    def parse(self, user_label_path):
        pass
