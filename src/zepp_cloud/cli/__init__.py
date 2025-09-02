from __future__ import annotations

import argparse
from typing import NoReturn

from .. import __version__


def main(argv: list[str] | None = None) -> NoReturn:
    parser = argparse.ArgumentParser(prog="zepp-cloud", description="Zepp Cloud SDK CLI")
    parser.add_argument("--version", action="store_true", help="Print version and exit")
    args = parser.parse_args(argv)

    if args.version:
        print(__version__)
        raise SystemExit(0)

    parser.print_help()
    raise SystemExit(0)
