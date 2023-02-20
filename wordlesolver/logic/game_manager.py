import random
from typing import Set

from wordlesolver.logic.constants import POSSIBLE_WORDS, MAX_ROUNDS
from wordlesolver.logic.models import Board, Keyboard, GameStatus, LetterStatus, Row, \
    Tile, TileStatus


class GameManager:
    board: Board
    keyboard: Keyboard
    game_status: GameStatus = GameStatus.INDETERMINATE
    _winning_word: str
    _winning_letters: Set[str]
    _round: int = 0

    def __init__(self):
        self.board = Board()
        self.keyboard = Keyboard()
        self._winning_word = random.choice(list(POSSIBLE_WORDS))
        self._letters_in_word = set(self._winning_word)

    def _update(self, word: str):
        self._update_board(word)
        self._update_keyboard(word)

    def _update_board(self, word: str):
        if not len(self.board.rows):
            return

        row: Row = Row()
        for index, letter in enumerate(word):
            tile: Tile = Tile(letter, TileStatus.UNUSED)
            if letter == self._winning_word[index]:
                tile.status = TileStatus.USED
            elif letter in self._winning_letters:
                tile.status = TileStatus.MISPLACED
            row.tiles.append(tile)

    def _update_keyboard(self, word: str):
        letters: Set[str] = set(word)
        for letter in letters:
            if letter not in self._letters_in_word:
                self.keyboard.set_status(letter, LetterStatus.UNUSED)
            elif letter in self._letters_in_word:
                self.keyboard.set_status(letter, LetterStatus.USED)

    def play(self, word: str) -> GameStatus:
        self._round += 1

        if self._round > MAX_ROUNDS or self.game_status in {GameStatus.LOSS, GameStatus.WIN}:
            raise RuntimeError("Game already completed.")

        self._update(word)

        if word == self._winning_word:
            self.game_status = GameStatus.WIN
        elif self._round == MAX_ROUNDS:
            self.game_status = GameStatus.LOSS

        return self.game_status
