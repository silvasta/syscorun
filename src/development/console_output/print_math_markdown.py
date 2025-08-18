from rich.console import Console
from rich.markdown import Markdown
from sympy import (
    symbols,
    pretty,
    MatrixSymbol,
)  # Assuming you can express equations as sympy objects

console = Console()

# NOTE: no results for math symbols, find unicode, maybe throw in sympy

# Define your equation as a sympy expression (parse from string if needed)
u_k, u_k1, alpha = symbols("u_k u_{k+1} alpha")
nabla_u_Phi, nabla_u_h, nabla_y_Phi = symbols(
    (r"\nabla_u\Phi(u,y) \nabla_uh(u,w) \nabla_y\Phi(u,y)")
)
# eq = (
#     u_k1 - u_k + alpha * (nabla_u_Phi + nabla_u_h.T * nabla_y_Phi)
# )  # Adapt to your actual math

# Render the math part
# math_rendered = pretty(nabla_u_Phi, use_unicode=True)
math_rendered = alpha

# Combine with Markdown text
full_md = f"""
# Unconstrained Feedback Optimization

Remember:

{math_rendered}

The choice of the right step size is crucial. ...
"""

markdown = Markdown(full_md)
console.print(markdown)
