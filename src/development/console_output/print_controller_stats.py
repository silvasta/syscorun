from rich.console import Console
from sysco.controller import BaseController

from sysco import LQR, MPC

# from rich import print
from rich.panel import Panel

console = Console()
header = "bold white on cyan"
# header = "bold cyan on white"
description = "white on green"
# description = "green on white"

base = BaseController()
lqr = LQR()
mpc = MPC()

controllers = [
    base,
    lqr,
    mpc,
]

for c in controllers:
    print()
    console.print(
        Panel(
            c.__class__.__name__,
            title="sysco",
            title_align="right",
            subtitle=c.__module__,
        ),
        style=header,
    )
    print()
    console.print(Panel(c.__doc__), style=description, justify="left")
