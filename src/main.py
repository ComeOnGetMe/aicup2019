import socket
import sys
from stream_wrapper import StreamWrapper

from aicup2019 import model
from aicup2019.debug import Debug
from aicup2019.agent.quickstart import QuickAgent


class Runner:
    def __init__(self, host, port, token):
        self.socket = socket.socket()
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        self.socket.connect((host, port))
        socket_stream = self.socket.makefile('rwb')
        self.reader = StreamWrapper(socket_stream)
        self.writer = StreamWrapper(socket_stream)
        self.token = token
        self.writer.write_string(self.token)
        self.writer.flush()

    def run(self):
        strategy = QuickAgent()
        debug = Debug(self.writer)

        while True:
            message = model.ServerMessageGame.read_from(self.reader)
            if message.player_view is None:
                break
            player_view = message.player_view
            actions = {}
            for unit in player_view.game.units:
                if unit.player_id == player_view.my_id:
                    actions[unit.id] = strategy.get_action(
                        unit, player_view.game, debug)
            model.PlayerMessageGame.ActionMessage(
                model.Versioned(actions)).write_to(self.writer)
            self.writer.flush()


if __name__ == "__main__":
    host = "127.0.0.1" if len(sys.argv) < 2 else sys.argv[1]
    port = 31001 if len(sys.argv) < 3 else int(sys.argv[2])
    token = "0000000000000000" if len(sys.argv) < 4 else sys.argv[3]
    Runner(host, port, token).run()
