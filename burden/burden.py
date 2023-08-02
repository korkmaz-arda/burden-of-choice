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


def get_options(category, tags=None):
    data = load()
    options = data[category]

    if tags:
        filtered_options = [
            option["name"]
            for option in options
            if all(tag in option["tags"] for tag in tags)
        ]
    else:
        filtered_options = [option["name"] for option in data[category]]

    return filtered_options


def get_tags(category):
    data = load()
    options = data[category]

    tags = [tag for option in options for tag in option["tags"]]
    return tags


if __name__ == "__main__":
    app()