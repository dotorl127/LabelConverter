import os
from .base_converter import base_converter
from copy import deepcopy


class converter(base_converter):
    def __init__(self, add_extra=True, tgt_path=None):
        super().__init__(default_label=None, add_extra=add_extra, tgt_path=tgt_path, extension=None)
        self.converted_label = None

    def convert(self, parsed_user_label):
        """
        original some dataset label format :
        description
        """
        self.converted_label = deepcopy(self.default_label)

    def save(self):
        self.converted_label = None
