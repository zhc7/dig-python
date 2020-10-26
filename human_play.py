from trainer import *


if __name__ == '__main__':
    big_score = [0, 0]
    trainer = Trainer()
    noise = input("configure noise: ")
    if noise:
        trainer.play_noise = float(noise)
    while True:
        game = Game()
        game.do(0, "j")
        game.do(1, "j")
        game.settle()
        while True:
            # choose max
            sActions = Player.sActions(*game.players.values())
            act, _ = trainer.choose_action(game, 1, trainer.net, trainer.play_noise, sActions[1])
            print(sActions)
            game.do(1, act, [0])
            game.do(0, input("action for %s: " % "you"), [1])
            print(act)
            game.settle()
            if len(game.players) == 1:
                winner = list(game.players.keys())[0]
                print(winner, "赢了！")
                break
            print(game.info())
        big_score[winner] += 1
        print("大比分 %d : %d" % tuple(big_score))
