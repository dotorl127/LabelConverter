import os
from .base_converter import base_converter
from copy import deepcopy


class converter(base_converter):
    def __init__(self, add_extra=True):
        super().__init__(default_label=None, add_extra=add_extra)
        self.converted_label = None

    def convert(self, parsed_user_label):
        """
        original some dataset label format :
        description
        """
        self.converted_label = deepcopy(self.default_label)

    def save(self, tgt_path):
        self.converted_label = None

    def run(self, parsed_user_label, tgt_path):
        if parsed_user_label["file_name"] is not None:
            self.split_file = True
        self.convert(parsed_user_label)
        self.save(tgt_path)
