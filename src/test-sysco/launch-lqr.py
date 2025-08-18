import time
from collections import namedtuple

from rich.console import Console
from rich.panel import Panel
from sysco import LQR

header_console = Console(style="bold white on cyan")
hp = header_console.print

result_concole = Console(style="black on white")
rp = result_concole.print

# print description somewhen
# hp(Panel(LQR.__doc__), style=description, justify="left")  # type:ignore

ITERATIONS = 100

# TODO: system generator
# HACK: Neotest? and pytest!

LQR_PARAM = namedtuple("LQR_PARAM", ("A", "B", "Q", "R", "x_0"))
LQR_P1 = LQR_PARAM(
    # system params
    A=[[1, 2], [3, 4]],
    B=[[2], [3]],
    # cost params
    Q=[[3, 0], [0, 4]],
    R=1,
    x_0=[2, 1],
)

LQR_P2 = LQR_PARAM(
    # system params
    A=[[1, 2, 0], [2, 3, 4], [7, 0, 3]],
    B=[[2], [3], [5]],
    # cost params
    Q=[[1, 0, 0], [0, 3, 0], [0, 0, 4]],
    R=2,
    x_0=[2, 1, 5],
)

LQR_P3 = LQR_PARAM(
    # system params
    A=[
        [1, 2, 0, 0, 5],
        [0, 2, 3, 4, 2],
        [2, 0, 4, 0, 3],
        [0, 3, 0, 1, 3],
        [2, 3, 2, 0, 3],
    ],
    B=[
        [1],
        [6],
        [0],
        [0],
        [2],
    ],
    # cost params
    Q=[
        [1, 0, 0, 0, 0],
        [0, 3, 0, 0, 0],
        [0, 0, 4, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 7],
    ],
    R=2,
    x_0=[2, 1, 5, 9, 2],
)

SYSTEMS = [LQR_P1, LQR_P2, LQR_P3]


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        return time.time() - start

    return wrapper


@timer
def loop_lqr_iterations(method: LQR.DARE_Method):
    for param in SYSTEMS:
        for _ in range(ITERATIONS):
            lqr = LQR(*param, method=method)
            _ = lqr.get_input()


for method in [LQR.DARE_Method.scipy, LQR.DARE_Method.scipy_direct]:
    print_text = f"LQR - Run [bold cyan on white] {method} [/bold cyan on white] for {ITERATIONS} rounds on {len(SYSTEMS)} systems"
    hp(Panel(print_text, title="sysco", title_align="right", subtitle=LQR.__module__))
    duration = loop_lqr_iterations(method)
    rp(f"duration: {duration}", end="\n", justify="full")
    print()
