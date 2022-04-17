from copy import deepcopy
from math import copysign
from cogs.variables import MoveState, Piece, Player
from random import Random


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
            lf = Piece.black_amazon

        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if piece == lf and self._can_move(x, y):
                    return False
        return True

    def _find_possible_move(self, x, y, board=None):
        """Finds the possible moves allowed from that coordinate"""
        if board is None:
            board = self.board
        possible_movement = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if y+i < 0 or x+j < 0:
                    continue
                if y+i >= len(board) or x+j >= len(board):
                    continue
                if board[y+i][x+j] == Piece.nothing:
                    possible_movement.append([x+j, y+i])
        return possible_movement

    def _can_move(self, x, y):
        # checks if a piece can move
        return len(self._find_possible_move(x, y)) > 0

    def json_format(self):
        board = [[x.value for x in row] for row in self.board]
        return str(
            {
                "id": self.id,
                "board": board,
                "playerWhite": self.player_white,
                "playerBlack": self.player_black
            }
        )

    def format(self):
        chessboard = [
            ["🟨" if (i+j) % 2 == 0 else "🟧" for j in range(10)] for i in range(10)]
        for i in range(10):
            for j in range(10):
                if self.board[i][j] == Piece.black_amazon:
                    chessboard[i][j] = "⬛"
                if self.board[i][j] == Piece.white_amazon:
                    chessboard[i][j] = "⬜"
                if self.board[i][j] == Piece.arrow:
                    chessboard[i][j] = "▫️"

        return "\n".join(["".join(row) for row in chessboard])

    def move(self, player_id: int, move_from, move_to, arrow_to):
        """Handles the movement of a piece and its arrow"""
        if self.finished:
            return MoveState.rejected, "This game is already over"
        if player_id not in [self.player_white, self.player_black]:
            return MoveState.rejected, "Not an active player"

        # to determine what pieces should be used
        current_allowed = self.player_white
        own_piece = Piece.white_amazon
        if self.current_player == Player.black:
            current_allowed = self.player_black
            own_piece = Piece.black_amazon

        if player_id != current_allowed:
            return MoveState.rejected, "Not the player's turn"

        x1, y1 = move_from
        x2, y2 = move_to
        x3, y3 = arrow_to
        # check if the move_from is an own piece
        if self.board[y1][x1] != own_piece:
            return MoveState.rejected, "Not your own piece to move. (Remember **x y**, not y x)"

        # check if moving the amazon is valid
        valid, reason = _is_valid_move(self.board, move_from, move_to)
        if not valid:
            return MoveState.rejected, "Can't move the amazon that way"
        # moves the amazon (without saving yet)
        tmp_board = deepcopy(self.board)
        tmp_board[y1][x1] = Piece.nothing
        tmp_board[y2][x2] = own_piece

        # check if shooting the arrow is valid
        valid, reason = _is_valid_move(tmp_board, move_to, arrow_to)
        if not valid:
            print(reason)
            return MoveState.rejected, "Can't shoot the arrow like that"

        # move the piece on the board and shoot the arrow (with saving)
        self.board[y1][x1] = Piece.nothing
        self.board[y2][x2] = own_piece
        self.board[y3][x3] = Piece.arrow

        if self.current_player == Player.white:
            self.current_player = Player.black
        else:
            self.current_player = Player.white

        # check if the game is over
        if self.is_over(self.current_player):
            self.finished = True
            return MoveState.game_over, "Game Over"

        return MoveState.accepted, "Move accepted"

    def play_ai(self, bot_id):
        # figure out what color we are
        own = Piece.white_amazon
        if bot_id == self.player_black:
            own = Piece.black_amazon

        # makes a list of all the pieces we can move
        potential_pieces = []
        for x in range(10):
            for y in range(10):
                if self.board[y][x] == own and self._can_move(x, y):
                    potential_pieces.append([x, y])

        # finds the movements a random piece can make
        rand = Random()
        x, y = move_from = rand.choice(potential_pieces)
        potential_direction = self._find_possible_move(x, y)
        x, y = move_to = rand.choice(potential_direction)

        # copies the board to find a random arrow place
        tmp_board = deepcopy(self.board)
        tmp_board[y][x] = Piece.nothing
        tmp_board[y][x] = own

        potential_arrow = self._find_possible_move(x, y, tmp_board)
        arrow_to = rand.choice(potential_arrow)

        # moves the piece
        self.move(bot_id, move_from, move_to, arrow_to)

    def get_current_player_id(self):
        if self.current_player == Player.black:
            return self.player_black
        return self.player_white


def _is_valid_move(board, move_from, move_to):
    """Checks if a move is valid with the current board configuration
    """
    x1, y1 = move_from
    x2, y2 = move_to
    if x1 == x2 and y1 == y2:
        return False, "x and y are the same"

    if abs(y2 - y1) == abs(x2 - x1) or x2-x1 == 0 or y2-y1 == 0:
        signx = int(copysign(1, x2-x1))
        if x2-x1 == 0:
            signx = 0
        signy = int(copysign(1, y2-y1))
        if y2-y1 == 0:
            signy = 0
        for i in range(1, abs(x2-x1)+1):
            if board[y1+i*signy][x1+i*signx] != Piece.nothing:
                return False, f"diag: something in the way on {(x1+i*signx, y1+i*signy)}"
        return True, "correct"

    return False, "Invalid movement (not diagonal or straight)"
