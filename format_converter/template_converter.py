import os
from .base_converter import base_converter
from copy import deepcopy


class Converter(base_converter):
    def __init__(self, add_extra=True):
        super().__init__(default_label=None, add_extra=add_extra)
        self.converted_label = None

    def convert(self, parsed_user_label):
        """
        original some dataset label format :
        description
        """
        self.converted_label = deepcopy(self.default_label)

    def save(self, tgt_path, file_name):
        self.converted_label = None

    def run(self, parsed_user_label, tgt_path, file_name):
        self.convert(parsed_user_label)
        self.save(tgt_path, file_name)
