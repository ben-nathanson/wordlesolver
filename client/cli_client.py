from client.style import AnsiEscapeSequence, QWERTY_LAYOUT
from logic.constants import POSSIBLE_WORDS
from logic.game_manager import GameManager
from logic.models import GameStatus, Board, Keyboard, LetterStatus, TileStatus
from logic.solver import Solver
from view.models import ViewBoard, ViewTile


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
        else:
            rendered_tile += AnsiEscapeSequence.BRIGHT_WHITE_TEXT.value
        rendered_tile += tile.value
        return rendered_tile

    @staticmethod
    def _render_keyboard(keyboard: Keyboard) -> str:
        rendered_keyboard = ""
        for index in range(3):
            left_padding = " " * (index + 1)
            rendered_keyboard += left_padding
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
                else:
                    rendered_key += AnsiEscapeSequence.BRIGHT_WHITE_TEXT.value
                rendered_key += key
                rendered_keyboard += (
                    f"{AnsiEscapeSequence.WHITE_TEXT.value}|{rendered_key}"
                )
            rendered_keyboard += f"{AnsiEscapeSequence.WHITE_TEXT.value}|\n"
        return rendered_keyboard

    def _render_board(self, board: Board) -> str:
        view_board: ViewBoard = ViewBoard.from_board(board)
        rendered_board = "___________\n"
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
                rendered_row += "| | | | | |"
            rendered_row += "\n"
            rendered_board += rendered_row
        rendered_board += "___________\n"
        return rendered_board

    def play(self):
        game_manager = GameManager()
        solver = Solver()
        while game_manager.game_status == GameStatus.INDETERMINATE:
            print(self._render(game_manager.board, game_manager.keyboard))
            possible_words = solver.find_possible_words(game_manager.board)
            suggestion = "\n".join(sorted(possible_words))
            print(f"The solver suggests \n{suggestion}")
            while True:
                next_choice = input("Enter your next choice:\n").strip().lower()
                if len(next_choice) != 5:
                    print("Your choice must be exactly five characters long.")
                elif next_choice not in POSSIBLE_WORDS:
                    print(f"{next_choice} is not a valid Wordle word.")
                else:
                    break
            game_manager.play(next_choice)

        if game_manager.game_status == GameStatus.WIN:
            print("Congratulations, you won!")
        else:
            print(f"Sorry, you lost. The winning word was {game_manager.winning_word}.")

        print(self._render(game_manager.board, game_manager.keyboard))

        choice = input("Play again? y/n\n")

        if choice.lower() in {"y", "yes"}:
            self.play()
