from pathlib import Path
from typing import Annotated

import sysco
import typer
from loguru import logger
from rich.console import Console
from rich.markdown import Markdown
from syscovis import plotter

from ..utils.find_project_root import find_project_root
from ..utils.logging_config import setup_logging

app = typer.Typer(
    name="project_name",
    help="CLI for ...",
    no_args_is_help=True,
    # pretty_exceptions_enable=False,  # TODO: check this! # Allows Loguru .catch() to work better
)


def main():
    # MOVE: logger here or logger in every command?
    with logger.catch():
        logger.info("Analyzing health data...")
        app()


@app.callback()
def main_callback(
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Show debug logs in terminal"
    ),
):
    """This runs BEFORE any command. It sets up the global logger state."""
    # None lets setup_logging use TOML default
    level = "DEBUG" if verbose else None
    setup_logging(log_level_override=level)


@app.command("base")
def base_controller():
    logger.debug(f"Importing {__name__}")
    console = Console()
    console.print(
        Markdown(
            f"# {sysco.hello_from_rust()}   ",
            style="bold white on cyan",
            # style="bold cyan on white",
            justify="center",
        )
    )
    try:
        controller = sysco.BaseController()
        controller.get_next_input()

    except Exception as e:
        logger.warning(f"{controller.__repr__()} caused: {e}")
        console.print(
            "You would have been better off implementing something than sleeping in class...",
            style="magenta",
        )
    plotter.plot()


@app.command("project-root")
def execute_find_project_root(
    root_indicator: Annotated[
        str, typer.Option("--indicator", "-i")
    ] = "pyproject.toml",
):
    """executes find_project_root with desired indicator"""
    with logger.catch():
        logger.info("...start finding project root!")
        print("found") if find_project_root(root_indicator) else print("no")
        print(find_project_root(root_indicator))


if __name__ == "__main__":
    main()
