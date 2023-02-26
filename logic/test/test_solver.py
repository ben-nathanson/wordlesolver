import unittest
from typing import List

from logic.constants import STARTER_WORDS
from logic.models import Board
from logic.solver import Solver

"""
We want an internal interface that, given some state S, where S consists of:
- The statuses (Yellow, Green, Black, Blank) of each square on the board and/or their values.
- The statuses (Yellow, Green, Black) of each letter on the keyboard.

Calculates the next most likely wordle word. This will be a naive approach but a basic 
recipe should consist of:
1. Start with a random, but powerful starting word such as CRANE. 
2. Rank the most likely next words. 
3. Don't use a letter that has already been marked as black, only consider letters that 
are unknown or used (letters may be re-used).

More advanced considerations might require us to store some state such as previously 
used Wordle words. 

"""


class SolveNextRound(unittest.TestCase):
    def test_returns_starter_word_on_empty_board(self):
        solver = Solver()
        updated_board: Board = solver.solve_next_round()
        [first_row] = updated_board.rows
        assert str(first_row) in STARTER_WORDS, f"{str(first_row)} is not a starter word."


class FindCandidates(unittest.TestCase):
    def test_returns_starter_words_on_empty_board(self):
        solver = Solver()
        candidates: List[str] = solver.find_candidates()
        assert candidates == STARTER_WORDS


