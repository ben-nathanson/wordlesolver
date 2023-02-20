import random
from typing import Set, List

from wordlesolver.logic.constants import STARTER_WORDS, POSSIBLE_WORDS
from wordlesolver.logic.models import Board, Keyboard, Row


class Solver:
    board: Board
    keyboard: Keyboard
    possible_words: Set[str]

    def __init__(self):
        self.board = Board()
        self.keyboard = Keyboard()
        self.possible_words = POSSIBLE_WORDS.copy()

    def solve_next_round(self) -> Board:
        if len(self.board.rows) < 1:
            random_starter_word: str = random.choice(STARTER_WORDS)
            next_row = Row.build_from_string(random_starter_word)
            self.board.rows.append(next_row)
            return self.board

    def find_candidates(self) -> List[str]:
        if len(self.board.rows) < 1:
            return STARTER_WORDS



