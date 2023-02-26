from typing import Set, List

from logic.constants import STARTER_WORDS, POSSIBLE_WORDS
from logic.models import Board, Keyboard, TileStatus


class Solver:
    possible_words: Set[str]

    def __init__(self):
        self.board = Board()
        self.keyboard = Keyboard()
        self.possible_words = POSSIBLE_WORDS.copy()
        self.unused_letters = set()
        self.used_letters = set()
        self.required_letter_positions: dict[int, str] = {}

    def update_possible_words(self, board: Board):
        for row in board.rows:
            for index, tile in enumerate(row.tiles):
                if tile.status == TileStatus.UNUSED:
                    self.unused_letters.add(tile.value)
                elif tile.status == TileStatus.USED:
                    self.used_letters.add(tile.value)
                    self.required_letter_positions[index] = tile.value
                elif tile.status == TileStatus.MISPLACED:
                    self.used_letters.add(tile.value)

        words = self.possible_words.copy()
        for word in words:
            for index in self.required_letter_positions:
                letter = self.required_letter_positions[index]
                if not word[index] == letter:
                    if word in self.possible_words:
                        self.possible_words.remove(word)
                    continue
            for letter in self.unused_letters:
                if letter in word:
                    if word in self.possible_words:
                        self.possible_words.remove(word)
            for letter in self.used_letters:
                if letter not in word:
                    if word in self.possible_words:
                        self.possible_words.remove(word)

    def find_possible_words(self, board: Board) -> List[str]:
        if len(board.rows) < 1:
            return STARTER_WORDS
        else:
            return list(self.possible_words)
