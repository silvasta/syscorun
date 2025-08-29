from functools import partial
import numpy as np
from sysco import LQR
# from syscovis import plotter

from rich.console import Console
from rich.panel import Panel
from rich.align import AlignMethod
from syscovis import Plotter

console = Console()


plotter = Plotter(task_name="LQR", show=False)


def print_cyan_panel(
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
    print_cyan_panel,
    console,
    "LQR",
    "Simulation",
    subtitle=f"{LQR.__module__}.{LQR.__name__}",
)

print_step = partial(console.print, style="green")

HORIZON = 30

print_LQR_H1_sim(text=f"run for {HORIZON} steps")


def apply_dynamics(A, x, B, u) -> np.ndarray:
    A = np.atleast_2d(A)
    x = np.atleast_2d(x).reshape(len(x), 1)
    B = np.atleast_2d(B)
    u = np.atleast_2d(u)
    x_next = A @ x + B @ u
    return x_next


# system params
A = [[1, 2], [3, 4]]
B = [[2], [3]]
# cost params
Q = [[3, 0], [0, 4]]
R = 1

# initial condition
x_0 = [2, 1]

lqr = LQR(A, B, Q, R)
x = np.atleast_2d(x_0).reshape(len(x_0), 1)
# store the values
x_trajcetory = []
u_trajcetory = []
cost_development = []

print_siumulaton = False
save_simulation = True
for step in range(HORIZON):
    # TODO: Management for subtask selection!
    # base task == simulation, x,u
    # extended: J,print|save steps
    if print_siumulaton:
        print_step(f"start with iteration: {step}")
    J = lqr.get_optimal_cost(x)
    if save_simulation:
        x_trajcetory += [x]
        cost_development += [J]
    if print_siumulaton:
        print(f"state: {x.flatten()}")
        print(f"cost {J}")
    if step == HORIZON - 1:
        break
    u = lqr.get_input(x)
    if save_simulation:
        u_trajcetory += [u]
    if print_siumulaton:
        print(f"input: {u.flatten()}")
    x = apply_dynamics(A, x, B, u)

# print(x_trajcetory, cost_development, u_trajcetory, sep="\n\n")

plotter.plot(x_trajcetory, name="2d_trajectory")
