from flask import Flask
from flask import request
from flask import session
from trainer import Trainer
from game import Game, Player

app = Flask(__name__)
app.secret_key = b"fasdfqwef4r42c32coyecrnhqwu9d83d"

games = {}
trainer = Trainer()


@app.route("/hello")
def hello():
    return "hello from dig backend!"


@app.route("/api/register", methods=["POST"])
def register():
    if session.new:
        session["id"] = len(games)
    return refresh()


@app.route("/api/refresh", methods=["POST"])
def refresh():
    gameId = session["id"]
    game = Game()
    playersInfo = getPlayersInfo(game)
    game.do(1, "j")
    try:
        noise = request.get_json()["noise"]
    except TypeError:
        noise = 0.5
    games[gameId] = (game, noise)
    print(len(games))
    return {"status": "ok",
            "players": playersInfo,
            "action": "j",
            }


@app.route("/api/action", methods=["POST"])
def postAction():
    gameId = session["id"]
    game, noise = games[gameId]
    game.do(0, request.get_json()["action"], [1])
    game.settle()
    print(game.info())
    playersInfo = getPlayersInfo(game)
    print(playersInfo)
    if len(game.players) == 1:
        winner = list(game.players.keys())[0]
        return {"isWin": True,
                "winner": winner,
                "players": playersInfo}
    sActions = Player.sActions(*game.players.values())
    act, _ = trainer.choose_action(game, 1, trainer.net, noise, sActions[1])
    game.do(1, act, [0])
    return {"isWin": False,
            "availableActions": sActions[0],
            "players": playersInfo,
            "action": act,
            }


def getPlayersInfo(game: Game):
    players = {}
    for i, player in game.players.items():
        players[player.uid] = ({attr: getattr(player, attr) for attr in
                                ["jue", "tower", "baotou", "defended_rush", "soldier", "died"]})
    return players


if __name__ == '__main__':
    app.run(debug=True)
