from typing import Set, List

from logic.constants import STARTER_WORDS, POSSIBLE_WORDS, ALPHABET
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
        self.misplaced_letter_positions: dict[str, set[int]] = {
            letter: set() for letter in ALPHABET
        }

    def update_possible_words(self, board: Board):
        for row in board.rows:
            for index, tile in enumerate(row.tiles):
                letter = tile.value
                if tile.status == TileStatus.UNUSED:
                    self.unused_letters.add(letter)
                elif tile.status == TileStatus.USED:
                    self.used_letters.add(letter)
                    self.required_letter_positions[index] = letter
                elif tile.status == TileStatus.MISPLACED:
                    self.used_letters.add(letter)
                    self.misplaced_letter_positions[letter].add(index)
        words = self.possible_words.copy()
        for word in words:
            for index in range(5):
                letter = word[index]
                required_letter: str | None = self.required_letter_positions.get(index)
                if required_letter and not letter == required_letter:
                    if word in self.possible_words:
                        self.possible_words.remove(word)
                    continue
                elif index in self.misplaced_letter_positions[letter]:
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
