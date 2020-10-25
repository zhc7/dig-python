from trainer import *


if __name__ == '__main__':
    trainer = Trainer()
    game = Game()
    game.do(0, "j")
    game.do(1, "j")
    game.settle()
    while True:
        # choose max
        act, _ = trainer.choose_action(game, 1, trainer.net)
        game.do(1, act, [0])
        game.do(0, input("action for %s: " % "you"), [1])
        print(act)
        game.settle()
        if len(game.players) == 1:
            print(list(game.players.keys())[0], "赢了！")
            quit(1)
        print(game.info())
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
