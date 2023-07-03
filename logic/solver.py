from logic.constants import (
    VALID_WORDLE_WORDS,
    ALPHABET,
    MAX_LETTERS,
    COMMON_ENGLISH_WORDS,
)
from logic.models import Board, Keyboard, TileStatus


class Solver:
    possible_words: {str}

    def __init__(self, hard_mode: bool):
        self.board = Board()
        self.keyboard = Keyboard()
        self.possible_words = (
            VALID_WORDLE_WORDS.copy() if hard_mode else COMMON_ENGLISH_WORDS.copy()
        )
        self.unused_letters = set()
        self.used_letters = set()
        self.required_letter_positions: dict[int, str] = {}
        self.misplaced_letter_positions: dict[str, set[int]] = {
            letter: set() for letter in ALPHABET
        }
        self.misplaced_letter_positions_reverse_mapping = {
            index: set() for index in range(MAX_LETTERS)
        }
        self.misplaced_letters = set()

    def _update_possible_words(self, board: Board):
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
                    self.misplaced_letter_positions_reverse_mapping[index].add(letter)
        words = self.possible_words.copy()
        for word in words:
            for index in range(MAX_LETTERS):
                letter = word[index]
                required_letter: str | None = self.required_letter_positions.get(index)
                if required_letter and not letter == required_letter:
                    is_misplaced_letter = (
                        index in self.misplaced_letter_positions[letter]
                    )
                    if word in self.possible_words and not is_misplaced_letter:
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

    def find_possible_words(self, board: Board) -> [str]:
        """
        Finds and returns all possible Wordle words given the state of the board.
        """
        self._update_possible_words(board)
        return list(self.possible_words)
