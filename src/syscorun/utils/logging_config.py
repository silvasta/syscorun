import sys
import tomllib
from pathlib import Path
from loguru import logger

from .find_project_root import find_project_root


def setup_logging(
    project_root: Path | None = None,
    log_level_override: str | None = None,
    log_to_file: bool = True,
    log_to_stderr: bool = True,
):
    """Configures Loguru based on pyproject.toml settings"""

    project_root: Path = project_root or find_project_root("pyproject.toml")

    # Load TOML configuration
    toml_path = project_root / "pyproject.toml"
    config = {}
    default_name = "app"

    if toml_path.exists():
        with open(toml_path, "rb") as f:
            full_toml = tomllib.load(f)
            project_name: str = full_toml.get("project", {}).get("name", default_name)
            config = full_toml.get("tool", {}).get(project_name, {}).get("logging", {})

    # Priority: Override Arg > TOML > Default "INFO"
    level: str = log_level_override or config.get("level", "INFO")

    # Clear existing handlers
    logger.remove()

    if log_to_stderr:
        # Terminal output (Clean & Colorful)
        logger.add(
            sys.stderr,
            level=level,
            # TESTING: is this useful?
            format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
            colorize=True,
        )
    if log_to_file:
        # Paths
        # TODO: later on, setup for logs in xdg_data_home
        log_dir = project_root / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / config.get("file_name", "debug.log")
        # File output (Detailed & Persistent)
        logger.add(
            log_path,
            level="DEBUG",  # Always keep debug detail in files
            rotation=config.get("rotation", "5 MB"),
            retention=config.get("retention", "1 week"),
            compression="zip",
            backtrace=True,  # Full stack trace
            # WARNING: set this to false for critical data!
            # use f.e. environment variable for that
            diagnose=True,  # Shows variable values in logs!
            # TESTING: is this useful?
            enqueue=True,  # Thread-safe
        )
    if not log_to_stderr and not log_to_file:
        print("Warning: Logging is completely disabled.")

    return logger
