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


def validate_category(category):
    data = load()
    if category not in data:
        typer.echo(f"Error: Category '{category}' does not exist.")
        raise typer.Abort()


def validate_option(option, category):
    validate_category(category)

    data = load()
    if option not in data[category]:
        typer.echo(f"Error: Option '{option}' does not exist in '{category}' category.")
        raise typer.Abort()


if __name__ == "__main__":
    app()