from game import *
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
        self.actions = []  # uncompleted, action名称映射到其index
        self.data = []

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

    @staticmethod
    def one_hot(action):
        p = Player(0)
        coded_action = [0 for i in range(14)]
        coded_action[list(p.all_actions).index(action)] = 1
        return coded_action

    def abstract_state(self, game: Game, player: int):
        """
        jue(10) ta(5) bingYing(bool) bing(10) baoTou(5) defended_rush(5)
        then last three steps of each using one-hot coding
        following the order of "my resources, his resources, my steps, his steps“
        """
        state = []
        for i in [player, 1 - player]:    # 先自己 再对方的顺序
            p = game.players[i]
            state += [p.jue/10, p.ta/5, int(p.bingYing()), p.bing/10, p.baotou/5, p.defended_rush/5]
        for i in [player, 1 - player]:
            his = game.histories[i]
            his = [his[0]] * 2 + his
            for action in his:
                state += self.one_hot(action)
        return state

    def self_play(self):
        game = Game(2)
        cache = [[], []]
        while True:
            for i in range(2):
                # p0, p1 = game.players[0], game.players[1]
                p = game.players[i]
                state = self.abstract_state(game, i)
                actions = self.net.predict(state)
                # choose max
                max_val = 0
                act = None
                for action in p.aActions():
                    val = actions[self.actions[action]]
                    if val > max_val:
                        max_val = val
                        act = action
                game.do(i, act, [1-i])
                cache[i].append((state, act))
            if len(game.players) == 1:
                winner = list(game.players.keys())[0]
                break
        self.data += cache[winner]
