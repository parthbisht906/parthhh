import argparse
import json
from typing import Iterable

from .checks import check_social_username, lookup_phone, summarize_social


def _print_json(payload: dict) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def _format_social(results: Iterable) -> None:
    summary = summarize_social(results)
    for bucket, items in summary.items():
        if not items:
            continue
        print(f"\n{bucket.upper()}:")
        for item in items:
            status = item.status_code if item.status_code is not None else "n/a"
            print(f"- {item.platform:10} {item.url} (status: {status})")


def handle_phone(args: argparse.Namespace) -> None:
    result = lookup_phone(args.number, args.region)
    if args.json:
        _print_json(result.__dict__)
        return
    print(f"Raw: {result.raw}")
    print(f"E164: {result.e164}")
    print(f"Valid: {result.valid}")
    print(f"Possible: {result.possible}")
    print(f"Region: {result.region}")
    print(f"Description: {result.description}")
    print(f"Carrier: {result.carrier}")
    print(f"Timezones: {', '.join(result.timezones) if result.timezones else 'n/a'}")


def handle_social(args: argparse.Namespace) -> None:
    results = check_social_username(
        args.username,
        timeout=args.timeout,
        delay_s=args.delay,
    )
    if args.json:
        _print_json({"results": [r.__dict__ for r in results]})
        return
    _format_social(results)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="OSINT helper for phone numbers and social media usernames.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    phone_parser = subparsers.add_parser("phone", help="Analyze a phone number")
    phone_parser.add_argument("number", help="Phone number to parse")
    phone_parser.add_argument(
        "--region",
        default="US",
        help="Region hint for parsing (default: US)",
    )
    phone_parser.add_argument("--json", action="store_true", help="JSON output")
    phone_parser.set_defaults(func=handle_phone)

    social_parser = subparsers.add_parser(
        "social",
        help="Check social media username presence",
    )
    social_parser.add_argument("username", help="Username to check")
    social_parser.add_argument(
        "--timeout",
        type=float,
        default=8.0,
        help="HTTP timeout per platform (seconds)",
    )
    social_parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay between requests (seconds)",
    )
    social_parser.add_argument("--json", action="store_true", help="JSON output")
    social_parser.set_defaults(func=handle_social)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
