# src/csvtojson/convert.py
from __future__ import annotations
import csv
import json
from pathlib import Path
from typing import Any, Dict, Iterable, TextIO


def _infer(value: str) -> Any:
    """Tiny, safe type inference: bool, int, float, else string."""
    v = value.strip()
    if v.lower() in {"true", "false"}:
        return v.lower() == "true"
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        pass
    return v


def rows_from_csv(fp: TextIO, *, infer_types: bool = True) -> Iterable[Dict[str, Any]]:
    """Yield dict rows from a CSV with headers."""
    reader = csv.DictReader(fp)
    for row in reader:
        yield {k: (_infer(v) if infer_types and v is not None else v) for k, v in row.items()}


def csv_file_to_json_str(
    csv_path: Path,
    *,
    infer_types: bool = True,
    indent: int | None = 2,
    ensure_ascii: bool = False,
) -> str:
    """Read a CSV file and return JSON string (list of dicts)."""
    with csv_path.open(newline="", encoding="utf-8") as f:
        data = list(rows_from_csv(f, infer_types=infer_types))
    return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)


def csv_file_to_json_file(
    csv_path: Path,
    json_path: Path | None = None,
    *,
    infer_types: bool = True,
    indent: int | None = 2,
    ensure_ascii: bool = False,
) -> Path:
    """
    Convert CSV → JSON file.
    If json_path not provided, write next to CSV using same name with .json extension.
    """
    if json_path is None:
        json_path = csv_path.with_suffix(".json")
    json_str = csv_file_to_json_str(
        csv_path, infer_types=infer_types, indent=indent, ensure_ascii=ensure_ascii
    )
    json_path.write_text(json_str, encoding="utf-8")
    return json_path
