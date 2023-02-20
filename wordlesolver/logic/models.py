from dataclasses import dataclass, field
from enum import Enum

from typing import List

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


@dataclass
class WordleBoard:
    rows: List[Row] = field(default_factory=list)
