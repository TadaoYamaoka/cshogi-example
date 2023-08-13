from cshogi import *
import random


PIECE_VALUES = [
    0,  # NONE
    100,  # BPAWN
    200,  # BLANCE
    200,  # BKNIGHT
    300,  # BSILVER
    1000,  # BBISHOP
    1000,  # BROOK
    300,  # BGOLD
    0,  # BKING
    500,  # BPROM_PAWN
    400,  # BPROM_LANCE
    400,  # BPROM_KNIGHT
    300,  # BPROM_SILVER,
    2000,  # BPROM_BISHOP
    2000,  # BPROM_ROOK
    None,  # NOTUSE
    None,  # NOTUSE
    -100,  # WPAWN
    -200,  # WLANCE
    -200,  # WKNIGHT
    -300,  # WSILVER
    -1000,  # WBISHOP
    -1000,  # WROOK
    -300,  # WGOLD
    0,  # WKING
    -500,  # WPROM_PAWN
    -400,  # WPROM_LANCE
    -400,  # WPROM_KNIGHT
    -300,  # WPROM_SILVER,
    -2000,  # WPROM_BISHOP
    -2000,  # WPROM_ROOK
]

HAND_PIECE_VALUES = [
    100,  # HPAWN
    200,  # HLANCE
    200,  # HKNIGHT
    300,  # HSILVER
    300,  # HGOLD
    1000,  # HBISHOP
    1000,  # HROOK
]


def eval(board):
    value = sum([PIECE_VALUES[piece] for piece in board.pieces])
    for c, pieces_in_hand in enumerate(board.pieces_in_hand):
        hand_value = sum(
            [
                HAND_PIECE_VALUES[hand_piece] * num
                for hand_piece, num in enumerate(pieces_in_hand)
            ]
        )
        value += hand_value if c == 0 else -hand_value
    if board.turn == BLACK:
        return value
    else:
        return -value


def check_board(board):
    if board.is_game_over():
        return -30000
    if board.is_nyugyoku():
        return 30000
    draw = board.is_draw(16)
    if draw == REPETITION_DRAW:
        return 0
    if draw == REPETITION_WIN:
        return 30000
    if draw == REPETITION_LOSE:
        return -30000
    if draw == REPETITION_SUPERIOR:
        return 30000
    if draw == REPETITION_INFERIOR:
        return -30000
    return None


def minmax(board, depth):
    max_value = -9999999
    for move in board.legal_moves:
        board.push(move)
        value = check_board(board)
        if value is None:
            if depth > 1:
                value = -minmax(board, depth - 1)
            else:
                value = -eval(board)
        if value > max_value:
            max_value = value
        board.pop()
    return max_value


def run():
    board = Board()
    while True:
        cmd_line = input().strip()
        cmd = cmd_line.split(" ", 1)

        if cmd[0] == "usi":
            print("id name minmax_engine")
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
                max_value = -9999999
                for move in board.legal_moves:
                    board.push(move)
                    value = check_board(board)
                    if value is None:
                        value = -minmax(board, 2)
                    if value > max_value:
                        max_value = value
                        best_move_list = [move]
                    elif value == max_value:
                        best_move_list.append(move)
                    board.pop()
                move = random.choice(best_move_list)
                bestmove = move_to_usi(move)
            print("bestmove " + bestmove, flush=True)
        elif cmd[0] == "quit":
            break


if __name__ == "__main__":
    run()
