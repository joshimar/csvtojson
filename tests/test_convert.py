from __future__ import annotations
from pathlib import Path
import io
import json

from csvtojson.convert import rows_from_csv, csv_file_to_json_str, csv_file_to_json_file


def test_rows_from_csv_infers_types():
    text = "name,age,active\nAlice,30,true\nBob,5,false\n"
    rows = list(rows_from_csv(io.StringIO(text)))
    assert rows == [
        {"name": "Alice", "age": 30, "active": True},
        {"name": "Bob", "age": 5, "active": False},
    ]


def test_csv_file_to_json_str_roundtrip(tmp_path: Path):
    csv_path = tmp_path / "in.csv"
    csv_path.write_text("x,y\n1,2\n3,4\n", encoding="utf-8")
    s = csv_file_to_json_str(csv_path)
    assert json.loads(s) == [{"x": 1, "y": 2}, {"x": 3, "y": 4}]


def test_csv_file_to_json_file_default_name(tmp_path: Path):
    csv_path = tmp_path / "data.csv"
    csv_path.write_text("k,v\nfoo,42\n", encoding="utf-8")
    out = csv_file_to_json_file(csv_path)
    assert out.name == "data.json"
    assert json.loads(out.read_text(encoding="utf-8")) == [{"k": "foo", "v": 42}]
