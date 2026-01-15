from pathlib import Path


def recursive_root(path: Path, indicator: str) -> Path | None:
    """Find root by indicator iterating parent paths upwards"""
    if (path / indicator).exists():
        return path
    elif path == path.parent:
        return None
    else:
        return recursive_root(path.parent, indicator)


def find_project_root(indicator: Path | str = "pyproject.toml") -> Path:
    """Call recursive function, return Success, Fail for Error"""

    search_result: Path | None = recursive_root(Path.cwd(), str(indicator))

    if search_result:
        print("Found project root at:", search_result)
        return search_result
    else:
        print(f"Failed with indicator: {indicator}")
        raise FileNotFoundError("Project root not found!")
