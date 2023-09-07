from .base_parser import base_Parser


class Parser(base_Parser):
    def __init__(self, config):
        super().__init__(config)

    def parse(self, user_label_path):
        label_list = []

        with open(user_label_path, 'r') as f:
            labels = f.readlines()

        for label in labels:
            label_parsed = self.label_dict.copy()

            split_label = label.split(self.config["split"])

            label_parsed["class"] = self.check_none_txt(split_label, self.config["class"])

            label_parsed["2dbbox"] = [self.check_none_txt(split_label, self.config["2Dbox"]["coord"][0]),
                                      self.check_none_txt(split_label, self.config["2Dbox"]["coord"][1]),
                                      self.check_none_txt(split_label, self.config["2Dbox"]["coord"][2]),
                                      self.check_none_txt(split_label, self.config["2Dbox"]["coord"][3])]
            if self.config["2Dbox"]["center"] and None not in label_parsed["2dbbox"]:
                cx, cy, w, h = list(map(float, label_parsed["2dbbox"]))
                label_parsed["2dbbox"] = [cx - w / 2,
                                          cy - h / 2,
                                          cx + w / 2,
                                          cy + h / 2]

            label_parsed["3dbbox"]["loc"] = [self.check_none_txt(split_label, self.config["3Dbox"]["loc"]["x"]),
                                             self.check_none_txt(split_label, self.config["3Dbox"]["loc"]["y"]),
                                             self.check_none_txt(split_label, self.config["3Dbox"]["loc"]["z"])]
            label_parsed["3dbbox"]["dim"] = [self.check_none_txt(split_label, self.config["3Dbox"]["dim"]["length"]),
                                             self.check_none_txt(split_label, self.config["3Dbox"]["dim"]["width"]),
                                             self.check_none_txt(split_label, self.config["3Dbox"]["dim"]["height"])]
            label_parsed["3dbbox"]["rot"] = [self.check_none_txt(split_label, self.config["3Dbox"]["dim"]["roll"]),
                                             self.check_none_txt(split_label, self.config["3Dbox"]["dim"]["pitch"]),
                                             self.check_none_txt(split_label, self.config["3Dbox"]["dim"]["yaw"])]

            label_parsed["extra"] += [self.check_none_txt(split_label, i) for i in self.config["extra"]]

            label_list.append(label_parsed)

        return label_list
