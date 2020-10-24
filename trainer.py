from game import Game
from model import PolicyNet
import os


class Trainer:
    def __init__(self, model_file=None):
        self.model_dir = "models/"
        if not model_file:
            model_file = self.find_latest_model("model")
        if model_file == "init":
            self.net = PolicyNet()
        else:
            self.net = PolicyNet(model_file)

    def find_latest_model(self, prefix):
        biggest_timestamp = 0
        latest_model = ""
        for filename in os.listdir(self.model_dir):
            pat = prefix + r"(.+)\.h5$"
            match = re.match(pat, filename)
            if match:
                timestamp = int(match.group(1))
                if timestamp > biggest_timestamp:
                    biggest_timestamp = timestamp
                    latest_model = filename
        return self.model_dir + latest_model if latest_model else None

    def self_play(self, ):

