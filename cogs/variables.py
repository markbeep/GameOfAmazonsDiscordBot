from enum import Enum


class Player(Enum):
    white = 0
    black = 1


class Piece(Enum):
    nothing = 0
    white_amazon = 1
    black_amazon = 2
    arrow = 3


class MoveState(Enum):
    rejected = 0
    accepted = 1
    game_over = 2
