from enum import Enum, auto


class InvalidMove(Exception):
    pass


class GameStates(Enum):
    OPEN = auto()
    DRAW = auto()
    PLAYER_1_WIN = auto()
    PLAYER_2_WIN = auto()


class ConnectFourGame:
    def __init__(self, x_size, y_size, player_1='player_1', player_2='player_2'):
        if x_size <= 0 or y_size <= 0:
            raise ValueError(f'x_size and y_size should be a positive integer')
        self._move_history = []
        self._board = [[] for _ in range(x_size)]
        self._player_names = [player_1, player_2]
        self._x_size = x_size
        self._y_size = y_size
        self._game_state = GameStates.OPEN
        self._winning_row = None

    def move(self, x_coord, player=None):
        if player is not None and self.current_player() != player:
            raise InvalidMove(f'Not {player}\'s turn.')
        if self._game_state != GameStates.OPEN:
            raise InvalidMove('Game already closed.')
        if x_coord < 0 or x_coord >= self._x_size:
            raise InvalidMove(f'Invalid x coordinate: {x_coord}.')
        if len(self._board[x_coord]) >= self._y_size:
            raise InvalidMove(f'Column is full: {x_coord}.')

        self._move(x_coord)

    def current_player(self):
        return self._player_names[self._current_player()]

    def last_player(self):
        return self._player_names[1 - self._current_player()]

    def get_board(self):
        result = [[None] * self._y_size for _ in range(self._x_size)]
        for x_coord, column in enumerate(self._board):
            for y_coord, occupied_by in enumerate(column):
                result[x_coord][y_coord] = occupied_by
        return result

    def occupied_by(self, x_coord, y_coord):
        player = self._occupied_by(x_coord, y_coord)
        if player is None:
            return None
        return self._player_names[player]

    def undo(self, player=None):
        if len(self._move_history) == 0:
            raise InvalidMove('No move to undo.')
        if self._game_state != GameStates.OPEN:
            raise InvalidMove('Game already closed.')
        if player is not None and self.last_player() != player:
            raise InvalidMove(f'It is {player}\'s turn. Undo is not allowed.')

        x_coord = self._move_history.pop()
        self._board[x_coord].pop()

    def get_state(self):
        return self._game_state

    def get_winning_row(self):
        return self._winning_row

    def _move(self, x_coord):
        player = self._current_player()
        new_position = (x_coord, len(self._board[x_coord]))

        self._move_history.append(x_coord)
        self._board[x_coord].append(player)
        directions = ((-1, 1), (0, 1), (1, 1), (1, 0))
        for direction in directions:
            row = set()
            for step in (direction, tuple(-coord for coord in direction)):
                position = new_position
                while self._occupied_by(*position) == player:
                    row.add(position)
                    position = tuple(pos_coord + step_coord
                                     for pos_coord, step_coord in zip(position, step))
            if len(row) >= 4:
                if player == 0:
                    self._game_state = GameStates.PLAYER_1_WIN
                else:
                    self._game_state = GameStates.PLAYER_2_WIN
                self._winning_row = sorted(row)
                break
        if (self._game_state == GameStates.OPEN and
                len(self._move_history) == self._x_size * self._y_size):
            self._game_state = GameStates.DRAW

    def _current_player(self):
        return len(self._move_history) % 2

    def _occupied_by(self, x_coord, y_coord):
        if x_coord < 0 or x_coord >= self._x_size:
            return None
        if y_coord < 0 or y_coord >= len(self._board[x_coord]):
            return None
        return self._board[x_coord][y_coord]
