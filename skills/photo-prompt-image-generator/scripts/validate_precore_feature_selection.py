#!/usr/bin/env python3
"""Validate the neutral pre-core catalog and an arm-specific feature-selection record."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any






























from photo_precore_bridge import load as _load_precore
_selection = _load_precore("photo_feature_selection")
CATALOG_VERSION = _selection.CATALOG_VERSION
SELECTION_VERSION = _selection.SELECTION_VERSION
CATALOG_PATH = _selection.CATALOG_PATH
CANONICAL_CATALOG_FILE = _selection.CANONICAL_CATALOG_FILE
GROUPS = _selection.GROUPS
CATEGORY_ID = _selection.CATEGORY_ID
SHA256 = _selection.SHA256
SelectionValidationError = _selection.SelectionValidationError
_fail = _selection._fail
_object = _selection._object
_nonempty = _selection._nonempty
_string_list = _selection._string_list
_only_fields = _selection._only_fields
_sha = _selection._sha
validate_catalog = _selection.validate_catalog
_active_spans = _selection._active_spans
_required_evidence_phrases = _selection._required_evidence_phrases
_contains_literal_phrase = _selection._contains_literal_phrase
validate_selection = _selection.validate_selection
clean_spaces = _selection.clean_spaces

def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        _fail(f"could not read {path.name}: {type(exc).__name__}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=CANONICAL_CATALOG_FILE)
    parser.add_argument(
        "--historical-catalog",
        action="store_true",
        help="allow an archived catalog snapshot for historical verification only",
    )
    parser.add_argument("--request-envelope", type=Path, required=True)
    parser.add_argument("--authorial-core", type=Path, required=True)
    parser.add_argument("--embodiment-review", type=Path, required=True)
    parser.add_argument("--selection", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        catalog_bytes = args.catalog.read_bytes()
        if not args.historical_catalog and catalog_bytes != CANONICAL_CATALOG_FILE.read_bytes():
            _fail("catalog bytes differ from the current permitted pre-core catalog")
        result = validate_selection(
            json.loads(catalog_bytes),
            catalog_bytes,
            _read_json(args.selection),
            _read_json(args.request_envelope),
            _read_json(args.authorial_core),
            _read_json(args.embodiment_review),
        )
    except (OSError, UnicodeError, json.JSONDecodeError, SelectionValidationError) as exc:
        print(f"invalid pre-core feature selection: {exc}", file=sys.stderr)
        return 2
    result["catalog_mode"] = "historical" if args.historical_catalog else "current"
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
