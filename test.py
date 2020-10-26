from trainer import *


if __name__ == '__main__':
    p = Player(0)
    p.jue = 10000
    dic = dict()
    for i in p.actions_to_other:
        dic[i] = getattr(p, p.actions_to_other[i])()[1]
    print(dic)
    quit(11111)
    trainer = Trainer()
    game = Game()
    random = random.SystemRandom()
    winners = [0, 0]
    probs = []
    up = 11
    for add in range(0, up):
        for count in range(10000):
            game = Game(2)
            game.players[0].jue += add
            while True:
                for i in range(2):
                    action = random.choice(game.players[i].aActions())
                    game.do(i, action, [1-i])
                game.settle()
                if len(game.players) == 1:
                    winner = list(game.players.keys())[0]
                    winners[winner] += 1
                    break
        probs.append(winners[0]/sum(winners))
        print(add, winners[0]/sum(winners))
    print(probs)
    plt.plot(list(range(0, up)), probs)
    plt.show()
