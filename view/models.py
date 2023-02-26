from enum import Enum
from typing import List

from pydantic import BaseModel

from logic.models import Board


class ViewLetterStatus(str, Enum):
    USED = "USED"
    UNUSED = "UNUSED"
    UNKNOWN = "UNKNOWN"


class ViewTileStatus(str, Enum):
    USED = "USED"
    MISPLACED = "MISPLACED"
    UNUSED = "UNUSED"


class ViewTile(BaseModel):
    value: str
    status: ViewTileStatus


class ViewRow(BaseModel):
    tiles: List[ViewTile] = list()


class ViewBoard(BaseModel):
    rows: List[ViewRow] = list()

    @staticmethod
    def from_board(board: Board):
        view_rows: List[ViewRow] = list()
        for row in board.rows:
            view_row = ViewRow()
            for tile in row.tiles:
                view_tile = ViewTile(
                    value=tile.value, status=ViewTileStatus(tile.status)
                )
                view_row.tiles.append(view_tile)
            view_rows.append(view_row)
        return ViewBoard(rows=view_rows)
