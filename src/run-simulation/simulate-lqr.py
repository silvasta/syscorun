from functools import partial
from sysco import LQR

from rich.console import Console
from rich.panel import Panel
from rich.align import AlignMethod

console = Console()


def print_console(
    c: Console,
    subject: str,
    highligted: str,
    text: str = "",
    subtitle: str = "",
    title: str = "sysco",
    title_align: AlignMethod = "right",
    highlight: str = "bold cyan on white",
):
    highligted_text = f"[{highlight}] {highligted} [/{highlight}]"
    print_text = f"{subject} - {highligted_text} {text}"
    c.print(
        Panel(print_text, title=title, title_align=title_align, subtitle=subtitle),
        style="bold white on cyan",
    )


print_LQR_H1_sim = partial(
    print_console,
    console,
    "LQR",
    "Simulation",
    subtitle=f"{LQR.__module__}.{LQR.__name__}",
)

HORIZON = 20
print_LQR_H1_sim(text=f"run for {HORIZON} steps")

