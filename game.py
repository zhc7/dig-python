# -*- coding: utf-8 -*-


class Game:
    def __init__(self, players=2):
        self.players = {}
        self.events = {}  # {target: [(from, attack_name, afraid_of), ...], ...}
        self.actions = {}
        self.histories = [[] for _ in range(players)]
        for i in range(players):
            self.players[i] = Player(uid=i)
        self.refresh()

    def do(self, player, action, targets=None):
        # 动作阶段
        p = self.players[player]
        if action not in p.aActions():
            raise ExplodeError("你爆了")
        attack, afraid = getattr(p, p.all_actions[action])()
        self.actions[player] = (action, targets, attack)
        if action in p.actions_to_other:
            for i in targets:
                self.events[i] += [(player, attack, afraid)]

    def settle(self):
        # 结算阶段
        for i in self.events:
            attacks = self.events[i]
            respond = self.actions[i]
            for source, attack, afraid in attacks:
                if respond[0] in afraid:
                    if respond[0] == "fm":
                        self.players[i].defended_rush += 1
                    continue
                if source in respond[1]:
                    if respond[2] >= attack:
                        continue
                    isDied = self.players[i].die()
                    if isDied:
                        break
        self.refresh()

    def refresh(self):
        self.events = {}
        for p in self.actions:
            self.histories[p].append(self.actions[p][0])
        self.actions = {}
        keys = list(self.players.keys())
        for p in keys:
            if self.players[p].died:
                self.players.pop(p)
                continue
            i = self.players[p].uid
            self.events[i] = []
            self.actions[i] = None

    def info(self):
        infos = ""
        infos += "|||j  t  bt dr b  died\n"
        for p in self.players.keys():
            player = self.players[p]
            infos += str(p) + ": " + "  ".join(
                [str(getattr(player, attr)) for attr in ["jue", "tower", "baotou", "defended_rush", "soldier", "died"]])
            infos += "\n"
        return infos


class Player:
    def __init__(self, uid):
        self.uid = uid
        self.jue = 0
        self.tower = 0
        self.defended_rush = 0
        self.baotou = 0
        self.camp = False
        self.soldier = 0
        self.died = False
        self.actions_to_self = {"j": "Jue", "t": "ta", "by": "bingYing", "b": "bing", "bt": "baoTou", "fs": "fangShe",
                                "fm": "fangMeng", "fg": "fangGao", "fk": "fangKan"}
        self.actions_to_other = {"s": "she", "gs": "gaoShe", "mj": "mengJin", "k": "kan", "xd": "xiaDi"}
        self.all_actions = dict(self.actions_to_self)
        self.all_actions.update(self.actions_to_other)

    def aActions(self):
        available = ["j", "fs", "fm", "fg", "fk"]
        # basic
        if self.jue >= 1:
            available += ["t", "bt"]
            if self.camp:
                available += ["b"]
        if self.jue >= 2:
            available += ["mj", "by"]

        # xd
        if self.baotou >= 2:
            available += ["xd"]

        # tower
        if self.tower >= 1:
            available.append("s")
        if self.tower >= 2:
            available.append("gs")

        # camp
        if self.soldier >= 1:
            available += ["k"]

        # 2rush
        if self.defended_rush >= 2:
            available += self.all_actions.keys()

        return available

    def die(self):
        if self.soldier >= 2:
            self.soldier -= 2
            return False
        self.died = True
        return True

    def Jue(self):
        self.jue += 1
        return 0, []

    def ta(self):
        self.tower += 1
        self.jue -= 1
        return 0, []

    def she(self):
        self.tower -= 1
        return 2, ["fs", "bt"]

    def gaoShe(self):
        self.tower -= 2
        return 5, ["fg", "bt"]

    def mengJin(self):
        self.jue -= 2
        return 3, ["fm", "bt"]

    def bingYing(self):
        self.jue -= 2
        self.camp = True
        return 0, []

    def bing(self):
        self.jue -= 1
        self.soldier += 1
        return 0, []

    def kan(self):
        self.soldier -= 1
        return 4, ["fk", "bt"]

    def baoTou(self):
        self.jue -= 1
        self.baotou += 1
        return 0, []

    def xiaDi(self):
        self.baotou -= 2
        return 1, ["fs"]

    def fangShe(self):
        return 0, []

    def fangMeng(self):
        return 0, []

    def fangGao(self):
        return 0, []

    def fangKan(self):
        return 0, []


class ExplodeError(Exception):
    pass


if __name__ == "__main__":
    game = Game()
    import random

    while True:
        game.do(0, input("action for %s: " % "you"), [1])
        game.do(1, random.choice(game.players[1].aActions()), [0])
        game.settle()
        if len(game.players) == 1:
            print(list(game.players.keys())[0], "赢了！")
            break
        print(game.info())
    while True:
        for i in range(2):
            game.do(i, input("action for %s: " % i), [1 - i])
        game.settle()
        if len(game.players) == 1:
            print(list(game.players.keys())[0], "赢了！")
            break
        print(game.info())
