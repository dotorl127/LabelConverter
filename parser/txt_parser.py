from label_dict import label_


class parser:
    def __init__(self, config):
        self.config = config
        self.label_dict = label_.copy()

    def parse(self, user_label_path):
        with open(user_label_path, 'r') as f:
            labels = f.readlines()

        for label in labels:
            split_label = label.split(' ')
            label_["class"] = split_label[self.config["class"]]

            if not self.config["2Dbox"]["center"]:
                label_["2dbbox"] = [float(split_label[self.config["2Dbox"]["coord"][0]]),
                                    float(split_label[self.config["2Dbox"]["coord"][1]]),
                                    float(split_label[self.config["2Dbox"]["coord"][2]]),
                                    float(split_label[self.config["2Dbox"]["coord"][3]])]
            else:
                cx = float(split_label[self.config["2Dbox"]["coord"][0]])
                cy = float(split_label[self.config["2Dbox"]["coord"][1]])
                w = float(split_label[self.config["2Dbox"]["coord"][2]])
                h = float(split_label[self.config["2Dbox"]["coord"][3]])
                label_["2dbbox"] = [cx - w / 2,
                                    cy - h / 2,
                                    cx + w / 2,
                                    cy + h / 2]

            label_["3dbbox"]["loc"] = [float(split_label[self.config["3Dbox"]["loc"]["x"]]),
                                       float(split_label[self.config["3Dbox"]["loc"]["y"]]),
                                       float(split_label[self.config["3Dbox"]["loc"]["z"]])]
            label_["3dbbox"]["dim"] = [float(split_label[self.config["3Dbox"]["dim"]["length"]]),
                                       float(split_label[self.config["3Dbox"]["dim"]["width"]]),
                                       float(split_label[self.config["3Dbox"]["dim"]["height"]])]
            label_["3dbbox"]["rot"] = [float(split_label[self.config["3Dbox"]["dim"]["roll"]]),
                                       float(split_label[self.config["3Dbox"]["dim"]["pitch"]]),
                                       float(split_label[self.config["3Dbox"]["dim"]["yaw"]])]

            label_["extra"] += [split_label[self.config["extra"][i]] for i in self.config["extra"]]
