import random

from wordlesolver.logic.constants import STARTER_WORDS
from wordlesolver.logic.models import Board, Keyboard, Row


def solve_next_round(board: Board, keyboard: Keyboard) -> Board:
    if len(board.rows) < 1:
        random_starter_word: str = random.choice(STARTER_WORDS)
        next_row = Row.build_from_string(random_starter_word)
        board.rows.append(next_row)
        return board
