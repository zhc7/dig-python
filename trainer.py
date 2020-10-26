import re
from game import *
from model import PolicyNet
import os


class Trainer:
    actions = {'j': 0, 't': 1, 'by': 2, 'b': 3, 'bt': 4, 'fs': 5, 'fm': 6, 'fg': 7, 'fk': 8, 's': 9, 'gs': 10,
               'mj': 11, 'k': 12, 'xd': 13}  # action名称映射到其index

    def __init__(self, model_file=None):
        self.model_dir = "models/"
        if not model_file:
            model_file = self.find_latest_model("model")
        if model_file == "init":
            self.net = PolicyNet()
        else:
            self.net = PolicyNet(model_file)
            self.org_net = self.net.copy()
        print("using model from", model_file)
        self.data = []
        self.data_buffer = [[], []]
        self.old_net = None
        self.best_net = self.net
        self.train_noise = 0.5
        self.play_noise = 0.5
        print("train noise: %s, play noise: %s" % (self.train_noise, self.play_noise))

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
        coded_action = [0 for _ in range(14)]
        coded_action[list(p.all_actions).index(action)] = 1
        return coded_action

    @staticmethod
    def abstract_state(game: Game, player: int):
        """
        jue(10) ta(5) bingYing(bool) bing(10) baoTou(5) defended_rush(5)
        then last three steps of each using one-hot coding
        following the order of "my resources, his resources, my steps, his steps“
        """
        state = []
        for i in [player, 1 - player]:  # 先自己 再对方的顺序
            p = game.players[i]
            state += [p.jue / 10, p.tower / 5, int(p.camp), p.soldier / 10, p.baotou / 5, p.defended_rush / 5]
        for i in [player, 1 - player]:
            his = game.histories[i]
            processed_his = [his[0]] * 2 + his
            for action in processed_his[-3:]:
                state += Trainer.one_hot(action)
        return state

    def self_play(self):
        game = Game(2)
        game.do(0, "j")
        game.do(1, "j")
        game.settle()
        cache = [[[], []], [[], []]]
        while True:
            sActions = Player.sActions(*game.players.values())
            for i in range(2):
                # p0, p1 = game.players[0], game.players[1]
                act, state = self.choose_action(game, i, self.net, self.train_noise, sActions[i])
                game.do(i, act, [1 - i])
                cache[i][0].append(state)
                cache[i][1].append(self.one_hot(act))
            game.settle()
            if len(game.players) == 1:
                winner = list(game.players.keys())[0]
                break
        self.data += cache[winner]
        self.data_buffer[0] += cache[winner][0]
        self.data_buffer[1] += cache[winner][1]

    def progress(self, data_size=512):
        print("progress")
        while len(self.data_buffer[0]) < data_size:
            self.self_play()
        self.old_net = self.net.copy()
        self.net.train_step(*self.data_buffer)
        self.data_buffer = [[], []]
        return self.evaluate(self.old_net, self.net, 20)

    def evaluate(self, old_net, new_net, count=100, verbose=0):
        winners = [0, 0]
        for t in range(count):
            game = Game(2)
            game.do(0, "j")
            game.do(1, "j")
            game.settle()
            while True:
                sActions = Player.sActions(*game.players.values())
                for i in range(2):
                    # p0, p1 = game.players[0], game.players[1]
                    net = [old_net, new_net][i]
                    act, _ = self.choose_action(game, i, net, self.play_noise, sActions[i])
                    game.do(i, act, [1 - i])
                    if verbose:
                        print(i, act)
                game.settle()
                if verbose:
                    print(game.info())
                if len(game.players) == 1:
                    winner = list(game.players.keys())[0]
                    winners[winner] += 1
                    break
        if sum(winners) != count:
            raise ValueError
        return winners[1] / sum(winners), winners

    @staticmethod
    def choose_action(game, i, net, noise, sAction):
        p = game.players[i]
        state = Trainer.abstract_state(game, i)
        actions = net.predict(state, noise=noise)
        # choose max
        max_val = 0
        act = None
        available = sAction
        for action in available:
            val = actions[Trainer.actions[action]]
            if val > max_val:
                max_val = val
                act = action
        return act, state

    def main(self):
        count = 0
        while True:
            result = self.progress(2048)
            print(result)
            count += 1
            if count % 5 == 0:
                self.net.save_model()
                print("saved")
                print(self.evaluate(self.org_net, self.net, 100))


if __name__ == '__main__':
    trainer = Trainer()
    # trainer.best_net = PolicyNet("models/good_models/model1603603941.h5")
    trainer.evaluate(trainer.best_net, trainer.net)
    trainer.main()
