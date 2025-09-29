# src/csvtojson/cli.py
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from .convert import csv_file_to_json_file


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="csv2json",
        description="Convert a CSV file (with headers) to a JSON file of records.",
    )
    p.add_argument("csv", type=Path, help="Path to input CSV file.")
    p.add_argument(
        "-o", "--out", type=Path, default=None, help="Optional output JSON path (default: same name)"
    )
    p.add_argument("--no-infer", action="store_true", help="Disable simple type inference.")
    p.add_argument("--indent", type=int, default=2, help="JSON indent; 0 for compact.")
    p.add_argument(
        "--ascii", action="store_true", help="Escape non-ASCII characters (ensure_ascii=True)."
    )
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.csv.exists():
        parser.error(f"CSV not found: {args.csv}")

    try:
        out = csv_file_to_json_file(
            args.csv,
            json_path=args.out,
            infer_types=not args.no_infer,
            indent=(args.indent if args.indent and args.indent > 0 else None),
            ensure_ascii=bool(args.ascii),
        )
        print(out)  # print the output path for scripting
        return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
