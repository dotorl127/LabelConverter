from abc import ABC, abstractmethod
from utlis import label_dict


class base_Parser(ABC):
    def __init__(self, config):
        self.config = config
        self.label_dict = label_dict.label_

    @abstractmethod
    def parse(self, user_label_path):
        pass
