import click

from client.cli_client import CliClient


@click.command()
@click.option("--hints", default=False, help="Print possible answers.")
@click.option("--hard-mode", default=False, help="Use more obscure English words.")
def main(hints: bool, hard_mode: bool):
    """A CLI based Wordle game, with optional hints."""
    cli_client = CliClient()
    cli_client.play(hints, hard_mode)


if __name__ == "__main__":
    main()
