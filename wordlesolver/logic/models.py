from dataclasses import dataclass, field
from enum import Enum

from typing import List, Dict

from wordlesolver.logic.constants import ALPHABET

"""
Tiles and Letters are structurally similar but should not be conflated.

For example, SPOON has two O's. If I guess BOOTH, the first O will be yellow, the
second will be green. The letter O has a status of "USED", but the tiles will have 
different statuses. 
"""


class LetterStatus(str, Enum):
    USED = "USED"
    UNUSED = "UNUSED"
    UNKNOWN = "UNKNOWN"


class TileStatus(str, Enum):
    USED = "USED"
    MISPLACED = "MISPLACED"
    UNUSED = "UNUSED"
    UNKNOWN = "UNKNOWN"


@dataclass
class Letter:
    status: LetterStatus
    value: str


@dataclass
class Tile:
    status: LetterStatus
    value: str


@dataclass
class Row:
    letters: List[Tile] = field(default_factory=list)

    @staticmethod
    def build_from_string(string: str):
        row = Row()
        for character in string:
            row.letters.append(Tile(value=character, status=LetterStatus.UNKNOWN))
        return row

    def __repr__(self):
        return "".join([character.value for character in self.letters])


@dataclass
class Board:
    rows: List[Row] = field(default_factory=list)


class Keyboard:
    keys: Dict[str, LetterStatus]

    def __init__(self):
        self.keys = {
            char: Letter(value=char, status=LetterStatus.UNKNOWN)
            for char in ALPHABET
        }
