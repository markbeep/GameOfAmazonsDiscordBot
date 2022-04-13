from cogs.variables import Piece, Player


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

    def is_over(self, player: int):
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

    def move(self, player_id: int, move_from, move_to):
        if player_id not in [self.player_white, self.player_black]:
            return False, "Not an active player"
        current_allowed = self.player_white
        if self.current_player == Player.black:
            current_allowed = self.player_black
        if player_id != current_allowed:
            return False, "Not the player's turn"

        return True, "Move accepted"
