from wordlesolver.client.style import AnsiEscapeSequence, QWERTY_LAYOUT
from wordlesolver.logic.game_manager import GameManager
from wordlesolver.logic.models import GameStatus, Board, Keyboard, LetterStatus, \
    TileStatus
from wordlesolver.view.models import ViewBoard, ViewTile


class CliClient:
    def _render(self, board: Board, keyboard: Keyboard) -> str:
        output = "\n"
        output += self._render_board(board)
        output += "\n"
        output += self._render_keyboard(keyboard)
        output += AnsiEscapeSequence.WHITE_TEXT.value
        return output

    @staticmethod
    def _render_tile(tile: ViewTile) -> str:
        rendered_tile = ""
        if tile.status == TileStatus.USED:
            rendered_tile += AnsiEscapeSequence.GREEN_TEXT.value
        elif tile.status == TileStatus.MISPLACED:
            rendered_tile += AnsiEscapeSequence.YELLOW_TEXT.value
        elif tile.status == TileStatus.UNUSED:
            rendered_tile += AnsiEscapeSequence.BLACK_TEXT.value
        rendered_tile += tile.value
        return rendered_tile

    @staticmethod
    def _render_keyboard(keyboard: Keyboard) -> str:
        rendered_keyboard = ""
        for index in range(3):
            row = QWERTY_LAYOUT[index]
            for key in row:
                key_status: LetterStatus = keyboard.keys[key]
                rendered_key = ""
                if key_status == LetterStatus.USED:
                    rendered_key = AnsiEscapeSequence.GREEN_TEXT.value
                elif key_status == LetterStatus.UNUSED:
                    rendered_key = AnsiEscapeSequence.BLACK_TEXT.value
                elif key_status == LetterStatus.MISPLACED:
                    rendered_key = AnsiEscapeSequence.YELLOW_TEXT.value
                rendered_key += key
                rendered_keyboard += f"{AnsiEscapeSequence.WHITE_TEXT.value}|{rendered_key}"
            rendered_keyboard += f"{AnsiEscapeSequence.WHITE_TEXT.value}|\n"
            rendered_keyboard += " " * (index + 1)
        return rendered_keyboard

    def _render_board(self, board: Board) -> str:
        view_board: ViewBoard = ViewBoard.from_board(board)
        rendered_board = "____________\n"
        for row_index in range(5):
            rendered_row = ""
            if row_index < len(view_board.rows):
                row = view_board.rows[row_index]
                for tile in row.tiles:
                    rendered_tile = self._render_tile(tile)
                    rendered_row += (
                        f"{AnsiEscapeSequence.WHITE_TEXT.value}|{rendered_tile}"
                    )
                rendered_row += f"{AnsiEscapeSequence.WHITE_TEXT.value}|"
            else:
                rendered_row += "| | | | |"
            rendered_row += "\n"
            rendered_board += rendered_row
        rendered_board += "\n____________\n"
        return rendered_board

    def play(self):
        game_manager = GameManager()
        while game_manager.game_status == GameStatus.INDETERMINATE:
            print(self._render(game_manager.board, game_manager.keyboard))
            game_manager.play(input("Enter your next choice:\n").strip().lower()[:5])

        if game_manager.game_status == GameStatus.WIN:
            print("Congratulations, you won!")
        else:
            print("Sorry, you lost.")

        choice = input("Play again? y/n")

        if choice.lower() in {"y", "yes"}:
            self.play()
