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
    _register_events(subparsers)

    args = parser.parse_args(argv)

    if getattr(args, "version", False):
        print(__version__)
        raise SystemExit(0)

    if args.command == "band":
        return _handle_band(args)
    if args.command == "events":
        return _handle_events(args)

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

    detail = band_sub.add_parser("detail", help="Fetch band detail windows")
    detail.add_argument("--from", dest="from_date", required=True, help="From date YYYY-MM-DD")
    detail.add_argument("--to", dest="to_date", required=True, help="To date YYYY-MM-DD")
    detail.add_argument("--tz", dest="timezone", default=os.environ.get("TZ", "UTC"))
    detail.add_argument("--token", dest="apptoken", default=os.environ.get("HUAMI_TOKEN"))
    detail.add_argument("--user", dest="user_id", default=os.environ.get("HUAMI_USER_ID"))
    detail.add_argument(
        "--pretty",
        dest="pretty",
        action="store_true",
        help="Pretty-print JSON array instead of JSONL",
    )
    detail.add_argument(
        "--keep-invalid",
        dest="keep_invalid",
        action="store_true",
        help="Include invalid HR samples (254/255/0) as nulls in output",
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

    if args.band_cmd == "detail":
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
            rows = client.band.get_detail(
                args.from_date, args.to_date, keep_invalid=getattr(args, "keep_invalid", False)
            )
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


def _register_events(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    events = subparsers.add_parser("events", help="Events-related commands")
    ev_sub = events.add_subparsers(dest="events_cmd")

    stress = ev_sub.add_parser("stress", help="Fetch stress events")
    stress.add_argument("--days", dest="days", type=int, default=14)
    stress.add_argument("--tz", dest="timezone", default=os.environ.get("TZ", "UTC"))
    stress.add_argument("--token", dest="apptoken", default=os.environ.get("HUAMI_TOKEN"))
    stress.add_argument("--user", dest="user_id", default=os.environ.get("HUAMI_USER_ID"))
    stress.add_argument("--pretty", dest="pretty", action="store_true")

    bo = ev_sub.add_parser("blood-oxygen", help="Fetch blood oxygen events")
    bo.add_argument("--days", dest="days", type=int, default=14)
    bo.add_argument("--tz", dest="timezone", default=os.environ.get("TZ", "UTC"))
    bo.add_argument("--token", dest="apptoken", default=os.environ.get("HUAMI_TOKEN"))
    bo.add_argument("--user", dest="user_id", default=os.environ.get("HUAMI_USER_ID"))
    bo.add_argument("--pretty", dest="pretty", action="store_true")
    bo.add_argument(
        "--subtype",
        dest="subtype",
        choices=["click", "osa_event", "odi"],
        default=None,
    )

    pai = ev_sub.add_parser("pai", help="Fetch PAI events")
    pai.add_argument("--days", dest="days", type=int, default=30)
    pai.add_argument("--tz", dest="timezone", default=os.environ.get("TZ", "UTC"))
    pai.add_argument("--token", dest="apptoken", default=os.environ.get("HUAMI_TOKEN"))
    pai.add_argument("--user", dest="user_id", default=os.environ.get("HUAMI_USER_ID"))
    pai.add_argument("--pretty", dest="pretty", action="store_true")


def _handle_events(args: argparse.Namespace) -> NoReturn:
    if args.events_cmd == "stress":
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
            rows = client.events.stress(days=args.days, time_zone=args.timezone)
        finally:
            client.close()

        if getattr(args, "pretty", False):
            print(json.dumps([r.model_dump() for r in rows], indent=2, ensure_ascii=False))
        else:
            for r in rows:
                print(json.dumps(r.model_dump()))
        raise SystemExit(0)

    if args.events_cmd == "blood-oxygen":
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
            data = client.events.blood_oxygen(days=args.days, time_zone=args.timezone)
        finally:
            client.close()

        subtype = getattr(args, "subtype", None)
        if subtype:
            rows = data.get(subtype, [])
            if getattr(args, "pretty", False):
                print(json.dumps([r.model_dump() for r in rows], indent=2, ensure_ascii=False))
            else:
                for r in rows:
                    print(json.dumps(r.model_dump()))
        elif getattr(args, "pretty", False):
            print(
                json.dumps(
                    {k: [r.model_dump() for r in v] for k, v in data.items()},
                    indent=2,
                    ensure_ascii=False,
                )
            )
        else:
            for k, rows in data.items():
                for r in rows:
                    obj = r.model_dump()
                    obj["subtype"] = k
                    print(json.dumps(obj))
        raise SystemExit(0)

    if args.events_cmd == "pai":
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
            rows = client.events.pai(days=args.days, time_zone=args.timezone)
        finally:
            client.close()

        if getattr(args, "pretty", False):
            print(json.dumps([r.model_dump() for r in rows], indent=2, ensure_ascii=False))
        else:
            for r in rows:
                print(json.dumps(r.model_dump()))
        raise SystemExit(0)

    print("error: missing events subcommand", file=sys.stderr)
    raise SystemExit(2)

    if False:  # unreachable, keeps ruff happy for function shape
        return
