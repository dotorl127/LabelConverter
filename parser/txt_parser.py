from label_dict import label_


class Parser:
    def __init__(self, config):
        self.config = config

    def parse(self, user_label_path):
        label_list = []

        with open(user_label_path, 'r') as f:
            labels = f.readlines()

        for label in labels:
            label_parsed = label_.copy()

            split_label = label.split(' ')
            label_parsed["class"] = split_label[self.config["class"]]

            if not self.config["2Dbox"]["center"]:
                label_parsed["2dbbox"] = [float(split_label[self.config["2Dbox"]["coord"][0]]),
                                          float(split_label[self.config["2Dbox"]["coord"][1]]),
                                          float(split_label[self.config["2Dbox"]["coord"][2]]),
                                          float(split_label[self.config["2Dbox"]["coord"][3]])]
            else:
                cx = float(split_label[self.config["2Dbox"]["coord"][0]])
                cy = float(split_label[self.config["2Dbox"]["coord"][1]])
                w = float(split_label[self.config["2Dbox"]["coord"][2]])
                h = float(split_label[self.config["2Dbox"]["coord"][3]])
                label_parsed["2dbbox"] = [cx - w / 2,
                                          cy - h / 2,
                                          cx + w / 2,
                                          cy + h / 2]

            label_parsed["3dbbox"]["loc"] = [float(split_label[self.config["3Dbox"]["loc"]["x"]]),
                                             float(split_label[self.config["3Dbox"]["loc"]["y"]]),
                                             float(split_label[self.config["3Dbox"]["loc"]["z"]])]
            label_parsed["3dbbox"]["dim"] = [float(split_label[self.config["3Dbox"]["dim"]["length"]]),
                                             float(split_label[self.config["3Dbox"]["dim"]["width"]]),
                                             float(split_label[self.config["3Dbox"]["dim"]["height"]])]
            label_parsed["3dbbox"]["rot"] = [float(split_label[self.config["3Dbox"]["dim"]["roll"]]),
                                             float(split_label[self.config["3Dbox"]["dim"]["pitch"]]),
                                             float(split_label[self.config["3Dbox"]["dim"]["yaw"]])]

            label_parsed["extra"] += [split_label[self.config["extra"][i]] for i in self.config["extra"]]

            label_list.append(label_parsed)

        return label_list