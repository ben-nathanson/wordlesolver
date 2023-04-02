from dataclasses import dataclass, field
from enum import Enum

from typing import List, Dict

from logic.constants import ALPHABET

"""
Tiles and Letters are structurally similar but should not be conflated.

For example, SPOON has two O's. If I guess BOOTH, the first O will be yellow, the
second will be green. The letter O has a status of "USED", but the tiles will have
different statuses.
"""


class LetterStatus(str, Enum):
    USED = "USED"
    MISPLACED = "MISPLACED"
    UNUSED = "UNUSED"
    UNKNOWN = "UNKNOWN"


class TileStatus(str, Enum):
    USED = "USED"
    MISPLACED = "MISPLACED"
    UNUSED = "UNUSED"
    UNKNOWN = "UNKNOWN"
    ALREADY_USED = "ALREADY_USED"


@dataclass
class Letter:
    status: LetterStatus
    value: str


@dataclass
class Tile:
    value: str
    status: TileStatus


@dataclass
class Row:
    tiles: List[Tile] = field(default_factory=list)

    @staticmethod
    def build_from_string(string: str):
        row = Row()
        for character in string:
            row.tiles.append(Tile(value=character, status=TileStatus.UNKNOWN))
        return row

    def __repr__(self):
        return "".join([character.value for character in self.tiles])


@dataclass
class Board:
    rows: List[Row] = field(default_factory=list)


class Keyboard:
    keys: Dict[str, LetterStatus]

    def __init__(self):
        self.keys: Dict[str, LetterStatus] = {
            char: Letter(value=char, status=LetterStatus.UNKNOWN) for char in ALPHABET
        }

    @staticmethod
    def _validate_letter(character: str):
        if not len(character) == 1 and character in ALPHABET:
            raise ValueError(f"{character} is not valid.")

    def get_status(self, character: str) -> LetterStatus:
        self._validate_letter(character)
        return self.keys[character]

    def set_status(self, character: str, status: LetterStatus):
        self._validate_letter(character)
        self.keys[character] = status


class GameStatus(str, Enum):
    WIN = "WIN"
    LOSS = "LOSS"
    INDETERMINATE = "INDETERMINATE"
