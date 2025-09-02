from __future__ import annotations

import argparse
import json
import os
import sys
from typing import NoReturn

from .. import __version__
from ..client import ZeppClient


def main(argv: list[str] | None = None) -> NoReturn:
    parser = argparse.ArgumentParser(prog="zepp-cloud", description="Zepp Cloud SDK CLI")
    parser.add_argument("--version", action="store_true", help="Print version and exit")

    subparsers = parser.add_subparsers(dest="command")
    _register_band(subparsers)

    args = parser.parse_args(argv)

    if getattr(args, "version", False):
        print(__version__)
        raise SystemExit(0)

    if args.command == "band":
        return _handle_band(args)

    parser.print_help()
    raise SystemExit(0)


def _register_band(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    band = subparsers.add_parser("band", help="Band-related commands")
    band_sub = band.add_subparsers(dest="band_cmd")

    summary = band_sub.add_parser("summary", help="Fetch band daily summaries")
    summary.add_argument("--from", dest="from_date", required=True, help="From date YYYY-MM-DD")
    summary.add_argument("--to", dest="to_date", required=True, help="To date YYYY-MM-DD")
    summary.add_argument("--tz", dest="timezone", default=os.environ.get("TZ", "UTC"))
    summary.add_argument("--token", dest="apptoken", default=os.environ.get("HUAMI_TOKEN"))
    summary.add_argument("--user", dest="user_id", default=os.environ.get("HUAMI_USER_ID"))
    summary.add_argument(
        "--pretty",
        dest="pretty",
        action="store_true",
        help="Pretty-print JSON array instead of JSONL",
    )


def _handle_band(args: argparse.Namespace) -> NoReturn:
    if args.band_cmd == "summary":
        apptoken = args.apptoken
        user_id = args.user_id
        if not apptoken or not user_id:
            msg = (
                "error: missing apptoken or user_id (use --token/--user or set "
                "HUAMI_TOKEN/HUAMI_USER_ID)"
            )
            print(msg, file=sys.stderr)
            raise SystemExit(2)

        client = ZeppClient(apptoken=apptoken, user_id=user_id, timezone=args.timezone)
        try:
            rows = client.band.get_summary(args.from_date, args.to_date)
        finally:
            client.close()

        if getattr(args, "pretty", False):
            print(json.dumps([r.model_dump() for r in rows], indent=2, ensure_ascii=False))
        else:
            for r in rows:
                print(json.dumps(r.model_dump()))
        raise SystemExit(0)

    print("error: missing band subcommand", file=sys.stderr)
    raise SystemExit(2)
