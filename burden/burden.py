import typer
import random
from memory import MemoryFile
from typing import List, Optional
from typing_extensions import Annotated

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


def get_tags(category, option=None):
    data = load_data()
    options = data[category]
    if option:
        options = [entry for entry in options if entry["name"] == option]

    tags = [tag for entry in options for tag in entry["tags"]]
    return tags


def validate(category, option=None, tags=None):
    data = load_data()
    if category not in data:
        typer.echo(f"Error: Category '{category}' does not exist.")
        raise typer.Abort()

    if option and (option not in data[category]):
        typer.echo(f"Error: Option '{option}' does not exist in '{category}'.")
        raise typer.Abort()

    if tags:
        available_tags = get_tags(category, option)
        for tag in tags:
            if tag not in available_tags:
                typer.echo(f"Error: Tag '{tag}' does not exist in '{category}'.")
                raise typer.Abort()


def add_category(category):
    data = load_data()
    if category in data:
        typer.echo(f"Warning: Category '{category}' already exists.")
        return

    data[category] = []
    save_data(data)
    typer.echo(f"Category '{category}' added.")


def add_option(category, option, tags=None):
    data = load_data()
    options = get_options(category)
    if option in options:
        typer.echo(f"Option '{option}' already exists in '{category}'.")
        return

    new_entry = {"name": option, "tags": tags}
    data[category].append(new_entry)
    save_data(data)
    typer.echo(f"Option '{option}' added to '{category}' with tags: {', '.join(tags)}")


def add_tag(category, option, tags):
    data = load_data()
    for i, entry in enumerate(data[category]):
        if entry["name"] == option:
            data[category][i] = {"name": option, "tags": entry["tags"]+tags}
    save_data(data)
    typer.echo(f"Tag(s) {', '.join(tags)} added to '{option}' in '{category}'")


@app.command(name="add")
def add_cmd(add_type: str, category: str, 
            option: Annotated[Optional[str], typer.Argument()] = None, 
            tags: Annotated[Optional[List[str]], typer.Argument()] = None):
    """
    Add a new type, category, option, or tags.

    Usage: 
        $ burden.py add category category_name
        $ burden.py add option category_name option_name
        $ burden.py add option category_name option_name tag_name tag_name2 ...
        $ burden.py add tag category_name option_name tag_name
        $ burden.py add tag category_name option_name tag_name tag_name2 ...

    Parameters:
        add_type (str): Type of the item being added (e.g., 'category', 'option', or 'tag').
        category (str): Category to add or add to (required for 'category', 'option', and 'tag' types).
        option (str, optional): Option to add or add to (required for 'option' and 'tag' types).
        tags (List[str], optional): Additional tags to bind to an option (required for 'tag' type and optional for 'option' type).
    """
    if not category:
        typer.echo("Error: 'category' field can't be empty")
        raise typer.Abort()

    if not option and add_type in ['option', 'tag']:
        typer.echo("Error: 'option' field can't be empty when trying to add an option or a tag.")
        raise typer.Abort()

    if not tags and add_type == "tag":
        typer.echo("Error: 'tags' field can't be empty when trying to add a tag.")
        raise typer.Abort()

    if add_type == 'category':
        if option or tags:
            typer.echo("Warning: 'add category' command doesn't take options or tags.")
        add_category(category)
    elif add_type == 'option':
        validate(category)
        add_option(category, option)
    elif add_type == 'tag':
        validate(category, option)
        add_tag(category, option, tags)
    else:
        typer.echo(f"Error: Invalid item type '{add_type}'.")
        raise typer.Abort()


if __name__ == "__main__":
    app()