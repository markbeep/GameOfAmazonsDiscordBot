from copy import deepcopy
from math import copysign
from cogs.variables import MoveState, Piece, Player


class Game:
    def __init__(self, game_id: int, player_white: int, player_black: int):
        self.board = self._setup()
        self.id = game_id
        self.player_white = player_white
        self.player_black = player_black
        self.finished = False
        self.current_player = Player.white

    def _setup(self):
        board = [[Piece.nothing for _ in range(10)] for _ in range(10)]
        board[0][3] = board[0][6] = board[3][0] = board[3][9] = Piece.black_amazon
        board[9][3] = board[9][6] = board[6][0] = board[6][9] = Piece.white_amazon
        return board

    def is_over(self, player: Player):
        lf = Piece.white_amazon
        if player == Player.black:
            Piece.black_amazon

        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if piece == lf and self._canMove(x, y):
                    return False
        return True

    def _canMove(self, x, y):
        # checks if a piece can move
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == y and j == x:
                    continue
                if self.board[y+i][x+j] == Piece.nothing:
                    return True
        return False

    def format(self):
        board = [[x.value for x in row] for row in self.board]
        return str(
            {
                "id": self.id,
                "board": board,
                "playerWhite": self.player_white,
                "playerBlack": self.player_black
            }
        )

    def move(self, player_id: int, move_from, move_to, arrow_to):
        """Handles the movement of a piece and its arrow
        """
        if self.finished:
            return MoveState.rejected, "This game is already over"
        if player_id not in [self.player_white, self.player_black]:
            return MoveState.rejected, "Not an active player"

        # to determine what pieces should be used
        current_allowed = self.player_white
        own_piece = Piece.white_amazon
        own_arrow = Piece.white_arrow
        if self.current_player == Player.black:
            current_allowed = self.player_black
            own_piece = Piece.black_amazon
            own_arrow = Piece.white_arrow

        if player_id != current_allowed:
            return MoveState.rejected, "Not the player's turn"

        x1, y1 = move_from
        x2, y2 = move_to
        x3, y3 = arrow_to
        # check if the move_from is an own piece
        if self.board[y1][x1] != own_piece:
            return MoveState.rejected, "Not a valid piece to move. (Remember **x y**, not y x)"

        # check if moving the amazon is valid
        if not self._is_valid_move(self.board, move_from, move_to):
            return MoveState.rejected, "Can't move the amazon that way"
        # moves the amazon (without saving yet)
        tmp_board = deepcopy(self.board)
        tmp_board[y1][x1] = Piece.nothing
        tmp_board[y2][x2] = own_piece

        # check if shooting the arrow is valid
        if not self._is_valid_move(tmp_board, move_to, arrow_to):
            return MoveState.rejected, "Can't shoot the arrow like that"

        # move the piece on the board and shoot the arrow (with saving)
        self.board[y1][x1] = Piece.nothing
        self.board[y2][x2] = own_piece
        self.board[y3][x3] = own_arrow

        if self.current_player == Player.white:
            self.current_player = Player.black
        else:
            self.current_player = Player.white

        # check if the game is over
        if self.is_over(self.current_player):
            self.finished = True
            return MoveState.game_over, "Game Over"

        return MoveState.accepted, "Move accepted"

    def _is_valid_move(board, move_from, move_to):
        """Checks if a move is valid with the current board configuration
        """
        x1, y1 = move_from
        x2, y2 = move_to
        if x1 == x2 and y1 == y2:
            return False
        if x1 == x2:  # check along the horizontal
            for i in range(min(y1, y2)+1, max(y1, y2)+1):
                if board[i][x1] != Piece.nothing:
                    return False
            return True
        if y1 == y2:  # check along the vertical
            for i in range(min(x1, x2)+1, max(x1, x2)+1):
                if board[y1][i] != Piece.nothing:
                    return False
            return True

        # checks along the diagonals
        diff = x2 - x1
        if y2 - y1 != diff:  # check if diagonal coordinates are diagonal
            return False

        sign = copysign(1, diff)
        for i in range(1, abs(diff)):
            if board[y1+sign][x1+sign] != Piece.nothing:
                return False
        return True
