import time
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
import sys
from .find_project_root import find_project_root

console = Console()


def main():
    """The entry point function."""
    root = find_project_root()
    # TODO: "debug.log" read from pyproject.toml
    log_path = root / "logs" / "debug.log"

    if not log_path.exists():
        print(f"No log file found at {log_path}")
        sys.exit(1)

    tail_log(str(log_path))


def tail_log(log_path: str):
    path = Path(log_path)
    if not path.exists():
        console.print(f"[bold red]Error:[/bold red] Log file {log_path} not found.")
        return

    console.print(
        Panel(f"Tailing [bold cyan]{log_path}[/bold cyan]...", title="Loguru Monitor")
    )

    with open(path, "r") as f:
        # Go to the end of the file
        f.seek(0, 2)

        try:
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)  # Sleep briefly to save CPU
                    continue

                # Simple coloring based on Loguru levels
                if "DEBUG" in line:
                    console.print(line.strip(), style="grey50")
                elif "INFO" in line:
                    console.print(line.strip(), style="green")
                elif "WARNING" in line:
                    console.print(line.strip(), style="yellow")
                elif "ERROR" in line:
                    console.print(line.strip(), style="bold red")
                else:
                    console.print(line.strip())
        except KeyboardInterrupt:
            console.print("\n[yellow]Stopped tailing.[/yellow]")


if __name__ == "__main__":
    main()
