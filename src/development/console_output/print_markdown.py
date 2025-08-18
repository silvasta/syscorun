from rich.console import Console
from rich.markdown import Markdown

console = Console()

markdown = Markdown(
    """
### Unconstrained Feedback Optimization

Remember:
$$
	u_{k+1} = u_k - \\alpha \\Big(
		\\nabla_u \\Phi(u,y) +
		\\nabla_u h(u; w)^\\top \\nabla_y \\Phi(u,y)
		   \\Big)
$$

The choice of the right step size is crucial. Convergence to the closest local minimum of $\\Phi(y)$ is only guaranteed for step sizes small enough. By increasing the step size, can you:
- make the system instable?
- converge to a different local minimum?
"""
)
console.print(markdown)
