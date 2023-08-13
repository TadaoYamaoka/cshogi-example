from cshogi import *
import random


def run():
    board = Board()
    while True:
        cmd_line = input().strip()
        cmd = cmd_line.split(" ", 1)

        if cmd[0] == "usi":
            print("id name random_engine")
            print("usiok", flush=True)
        elif cmd[0] == "isready":
            print("readyok", flush=True)
        elif cmd[0] == "position":
            board.set_position(cmd[1])
        elif cmd[0] == "go":
            if board.is_game_over():
                bestmove = "resign"
            elif board.is_nyugyoku():
                bestmove = "win"
            else:
                move = random.choice(list(board.legal_moves))
                bestmove = move_to_usi(move)
            print("bestmove " + bestmove, flush=True)
        elif cmd[0] == "quit":
            break


if __name__ == "__main__":
    run()
