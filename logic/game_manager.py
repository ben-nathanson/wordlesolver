import random
from typing import Set, Dict

from logic.constants import VALID_WORDLE_WORDS, MAX_ROUNDS, MAX_LETTERS
from logic.models import (
    Board,
    Keyboard,
    GameStatus,
    LetterStatus,
    Row,
    Tile,
    TileStatus,
)


class GameManager:
    board: Board
    keyboard: Keyboard
    game_status: GameStatus = GameStatus.INDETERMINATE
    winning_word: str
    _letters_in_word: Set[str]
    _last_index_of_letter: Dict[str, int]

    _round: int = 0

    def __init__(self):
        self.board = Board()
        self.keyboard = Keyboard()
        self.winning_word = random.choice(list(VALID_WORDLE_WORDS))
        self._letters_in_word = set(self.winning_word)
        self._last_index_of_letter = {
            letter: self.winning_word.rindex(letter) for letter in self._letters_in_word
        }

    def _update(self, word: str):
        self._update_board(word)
        self._update_keyboard(word)

    def _update_board(self, word: str):
        row: Row = Row()
        for index, letter in enumerate(word):
            tile: Tile = Tile(letter, TileStatus.UNUSED)
            if letter == self.winning_word[index]:
                tile.status = TileStatus.USED
            elif letter in self._letters_in_word:
                if word.count(letter) <= self.winning_word.count(letter):
                    tile.status = TileStatus.MISPLACED
                else:
                    tile.status = TileStatus.ALREADY_USED
            row.tiles.append(tile)
        self.board.rows.append(row)

    def _update_keyboard(self, word: str):
        for index, letter in enumerate(word):
            if letter not in self._letters_in_word:
                self.keyboard.set_status(letter, LetterStatus.UNUSED)
            elif self.winning_word[index] == letter:
                self.keyboard.set_status(letter, LetterStatus.USED)
            elif letter in self._letters_in_word:
                if self.keyboard.get_status(letter) == LetterStatus.USED:
                    return
                else:
                    self.keyboard.set_status(letter, LetterStatus.MISPLACED)

    @staticmethod
    def _validate_word(word: str):
        if len(word) > MAX_LETTERS:
            raise ValueError("This word is too long.")

        if word not in VALID_WORDLE_WORDS:
            raise ValueError("This is not a recognized word.")

    def play(self, word: str) -> GameStatus:
        if self._round >= MAX_ROUNDS or self.game_status in {
            GameStatus.LOSS,
            GameStatus.WIN,
        }:
            raise RuntimeError("Game already completed.")

        self._round += 1
        self._validate_word(word)
        self._update(word)

        if word == self.winning_word:
            self.game_status = GameStatus.WIN
        elif self._round == MAX_ROUNDS:
            self.game_status = GameStatus.LOSS

        return self.game_status
