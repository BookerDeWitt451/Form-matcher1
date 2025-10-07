from __future__ import annotations
import argparse
from typing import Dict
from core import match_template, pretty_inferred_types
from tinydb import TinyDB
from tinydb.storages import JSONStorage  # исправлено

def parse_kv_args(argv: list[str]) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for token in argv:
        if token.startswith("--") and "=" in token:
            key, value = token[2:].split("=", 1)
            if key:
                result[key] = value
    return result

def main():
    parser = argparse.ArgumentParser(description="Form template matcher")
    parser.add_argument("command", choices=["get_tpl"], help="Command to run")
    parser.add_argument("--db", default="db/templates.json", help="Path to TinyDB JSON file")
    known, unknown = parser.parse_known_args()
    if known.command == "get_tpl":
        provided = parse_kv_args(unknown)
        db = TinyDB(known.db, storage=JSONStorage, encoding='utf-8')  # utf-8 для кириллицы на Windows
        templates = db.table("templates").all()
        name = match_template(templates, provided)
        if name is not None:
            print(name)
        else:
            print(pretty_inferred_types(provided))

if __name__ == "__main__":
    main()
