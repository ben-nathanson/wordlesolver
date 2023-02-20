from wordlesolver.logic.game_manager import GameManager
from wordlesolver.logic.models import GameStatus


class CliBoard:
    ...


class CliClient:
    @staticmethod
    def play():
        game_manager = GameManager()

        while game_manager.game_status == GameStatus.INDETERMINATE:
            game_manager.play(input("Enter your next choice:"))

        choice = input("Play again? y/n")

        if choice.lower() in {"y", "yes"}:
            CliClient.play()
