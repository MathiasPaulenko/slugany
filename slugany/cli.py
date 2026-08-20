from __future__ import annotations

import argparse
import sys
from typing import Any

from slugany import slugify


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="slugany",
        description="Slugify text into URL-friendly slugs.",
    )
    parser.add_argument("text", nargs="?", default=None, help="Text to slugify.")
    parser.add_argument("--separator", "-s", default=None, help="Separator between words.")
    parser.add_argument("--style", default=None, help="Case style preset.")
    parser.add_argument("--lang", default=None, help="Language for transliteration.")
    parser.add_argument("--max-length", type=int, default=None, help="Maximum slug length.")
    parser.add_argument(
        "--word-boundary",
        action="store_true",
        default=None,
        help="Truncate at word boundary.",
    )
    parser.add_argument(
        "--lowercase",
        dest="lowercase",
        action="store_true",
        default=None,
        help="Lowercase output.",
    )
    parser.add_argument(
        "--no-lowercase",
        dest="lowercase",
        action="store_false",
        default=None,
        help="Keep original case.",
    )
    parser.add_argument(
        "--allow-unicode",
        action="store_true",
        default=None,
        help="Allow Unicode characters.",
    )
    parser.add_argument("--fallback", default=None, help="Fallback string when result is empty.")
    parser.add_argument(
        "--emoji-mode",
        default=None,
        choices=["strip", "text", "keep"],
        help="Emoji handling mode.",
    )
    parser.add_argument("--css-safe", action="store_true", default=None, help="CSS-safe output.")
    parser.add_argument("--batch", action="store_true", help="Read stdin line by line.")
    return parser


def _build_kwargs(args: argparse.Namespace) -> dict[str, Any]:
    kwargs: dict[str, Any] = {}
    if args.separator is not None:
        kwargs["separator"] = args.separator
    if args.style is not None:
        kwargs["style"] = args.style
    if args.lang is not None:
        kwargs["lang"] = args.lang
    if args.max_length is not None:
        kwargs["max_length"] = args.max_length
    if args.word_boundary is not None:
        kwargs["word_boundary"] = args.word_boundary
    if args.lowercase is not None:
        kwargs["lowercase"] = args.lowercase
    if args.allow_unicode is not None:
        kwargs["allow_unicode"] = args.allow_unicode
    if args.fallback is not None:
        kwargs["fallback"] = args.fallback
    if args.emoji_mode is not None:
        kwargs["emoji_mode"] = args.emoji_mode
    if args.css_safe is not None:
        kwargs["css_safe"] = args.css_safe
    return kwargs


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdin, sys.stdout):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass
    parser = _build_parser()
    args = parser.parse_args(argv)
    kwargs = _build_kwargs(args)

    try:
        if args.batch:
            for line in sys.stdin:
                line = line.rstrip("\n")
                print(slugify(line, **kwargs))
            return 0

        if args.text is not None:
            print(slugify(args.text, **kwargs))
            return 0

        if not sys.stdin.isatty():
            for line in sys.stdin:
                line = line.rstrip("\n")
                print(slugify(line, **kwargs))
            return 0
    except (ValueError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    parser.print_help()
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
