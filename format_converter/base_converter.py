from abc import ABC, abstractmethod


class base_converter(ABC):
    def __init__(self, default_label):
        self.default_label = default_label

    @abstractmethod
    def convert(self, user_label):
        pass

    @abstractmethod
    def save(self, tgt_path, converted_label):
        pass
