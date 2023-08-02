import typer
import random
from memory import MemoryFile

app = typer.Typer()


def load():
    memory = MemoryFile()
    response = memory.load()
    if response.error_message:
        typer.echo(response.error_message)
        raise typer.Exit()

    return response.data


def save(data):
    memory = MemoryFile()
    response = memory.save(data)
    if response.error_message:
        typer.echo(response.error_message)


if __name__ == "__main__":
    app()