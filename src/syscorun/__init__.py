import sysco
from syscovis import plotter
from loguru import logger


def main() -> None:
    print("Hello from syscorun!")
    print(sysco.main())
    logger.debug(f"Start executing {__name__}")
    print(plotter.__dict__)
