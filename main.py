import click

from client.cli_client import CliClient


@click.command()
@click.option("--hints", default=True, help="Print possible answers.")
def main(hints):
    """A CLI based Wordle game, with optional hints."""
    cli_client = CliClient()
    cli_client.play(hints)


if __name__ == "__main__":
    main()
