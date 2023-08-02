import typer
import random
from memory import MemoryFile

app = typer.Typer()


def load_data():
    memory = MemoryFile()
    response = memory.load()
    if response.error_message:
        typer.echo(response.error_message)
        raise typer.Exit()

    return response.data


def save_data(data):
    memory = MemoryFile()
    response = memory.save(data)
    if response.error_message:
        typer.echo(response.error_message)


def get_options(category, tags=None):
    data = load_data()
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
    data = load_data()
    options = data[category]

    tags = [tag for option in options for tag in option["tags"]]
    return tags


def validate(category, option=None, tags=None):
    data = load_data()
    if category not in data:
        typer.echo(f"Error: Category '{category}' does not exist.")
        raise typer.Abort()

    if option and (option not in data[category]):
        typer.echo(f"Error: Option '{option}' does not exist in '{category}' category.")
        raise typer.Abort()

    if tags:
        available_tags = get_tags(category)
        for tag in tags:
            if tag not in available_tags:
                typer.echo(f"Error: Tag '{tag}' does not exist in '{category}' category.")
                raise typer.Abort()


def _add(category, option=None, tags=None):
    # TODO
    pass



if __name__ == "__main__":
    app()