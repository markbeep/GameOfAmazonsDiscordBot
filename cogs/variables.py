from enum import Enum


class Player(Enum):
    white = 0
    black = 1


class Piece(Enum):
    nothing = 0
    white_amazon = 1
    white_arrow = 2
    black_amazon = 3
    black_arrow = 4


class MoveState(Enum):
    rejected = 0
    accepted = 1
    game_over = 2
