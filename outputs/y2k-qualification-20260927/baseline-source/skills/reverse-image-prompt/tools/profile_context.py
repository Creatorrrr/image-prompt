#!/usr/bin/env python3
"""Read explicit profile views of instruction files without changing source text.

Only standalone ``<!-- profile:prompt -->``, ``<!-- profile:audited -->``,
and ``<!-- /profile -->`` lines are directives. Whitespace around a directive
is allowed; all retained non-directive characters are preserved exactly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "reverse-image-prompt/profile-context"
VERSION = 1
ANALYSIS_PROFILES = ("prompt", "audited")
_RENDER_PROFILES = (*ANALYSIS_PROFILES, "combined")
_OPEN_MARKERS = {
    f"<!-- profile:{profile} -->": profile for profile in ANALYSIS_PROFILES
}
_CLOSE_MARKER = "<!-- /profile -->"
# Search the complete text so split comments and broken comment delimiters fail.
# The profile namespace is reserved; unrelated comments and prose are untouched.
_MARKER_CANDIDATE = re.compile(r"<[!\s-]+/?\s*profile\b", re.IGNORECASE)


def render_profile_text(text: str, profile: str) -> str:
    """Return shared text plus the selected explicit blocks, without markers.

    ``combined`` is available to source builders, but is not a CLI analysis
    profile. Unknown, malformed, nested, or unbalanced markers raise ValueError,
    including markers within blocks excluded from the requested view.
    """
    if profile not in _RENDER_PROFILES:
        raise ValueError(f"unknown profile {profile!r}; expected {_RENDER_PROFILES}")

    candidates = iter(_MARKER_CANDIDATE.finditer(text))
    candidate = next(candidates, None)
    active: str | None = None
    opening_line: int | None = None
    position = 0
    output: list[str] = []

    for line_number, line in enumerate(text.splitlines(keepends=True), 1):
        marker = line.strip(" \t\r\n")
        is_marker = marker in _OPEN_MARKERS or marker == _CLOSE_MARKER
        if candidate is not None and candidate.start() < position + len(line):
            if not is_marker:
                raise ValueError(
                    f"line {line_number}: malformed or unknown profile marker; "
                    "use a standalone canonical profile directive"
                )
            candidate = next(candidates, None)

        if marker in _OPEN_MARKERS:
            if active is not None:
                raise ValueError(
                    f"line {line_number}: nested profile block "
                    f"inside {active!r} block opened at line {opening_line}"
                )
            active = _OPEN_MARKERS[marker]
            opening_line = line_number
        elif marker == _CLOSE_MARKER:
            if active is None:
                raise ValueError(f"line {line_number}: closing profile marker without an open block")
            active = None
            opening_line = None
        elif active is None or active == profile or profile == "combined":
            output.append(line)

        position += len(line)

    if active is not None:
        raise ValueError(f"line {opening_line}: unclosed {active!r} profile block")
    return "".join(output)


def read_profile_files(
    files: Sequence[str | Path],
    profile: str,
    root: str | Path = ROOT,
) -> dict[str, Any]:
    """Fully read and validate every requested file before returning a bundle.

    Paths resolve within ``root``, including symlink targets. Source hashes cover
    original bytes; view hashes cover the UTF-8 encoding of the exact view. Word
    counts use whitespace splitting, including directive words in source counts.
    """
    if profile not in ANALYSIS_PROFILES:
        raise ValueError(f"unknown analysis profile {profile!r}; expected {ANALYSIS_PROFILES}")
    if not files:
        raise ValueError("at least one file is required")
    resolved_root = Path(root).resolve(strict=True)
    if not resolved_root.is_dir():
        raise ValueError(f"skill root is not a directory: {root}")

    entries: list[dict[str, Any]] = []
    for file in files:
        requested = Path(file)
        resolved = (resolved_root / requested).resolve(strict=True)
        try:
            relative = resolved.relative_to(resolved_root).as_posix()
        except ValueError as exc:
            raise ValueError(f"file path escapes skill root: {file}") from exc
        try:
            source = resolved.read_bytes()
            source_text = source.decode("utf-8")
            content = render_profile_text(source_text, profile)
        except (OSError, UnicodeError, ValueError) as exc:
            raise ValueError(f"{relative}: {exc}") from exc
        entries.append(
            {
                "path": relative,
                "source_sha256": hashlib.sha256(source).hexdigest(),
                "view_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
                "source_words": len(source_text.split()),
                "view_words": len(content.split()),
                "content": content,
            }
        )
    return {"schema": SCHEMA, "version": VERSION, "profile": profile, "files": entries}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--analysis-profile", choices=ANALYSIS_PROFILES, required=True)
    parser.add_argument("--files", nargs="+", required=True, help="instruction paths within the skill root")
    parser.add_argument("--root", type=Path, default=ROOT, help="skill root (defaults to this tool's skill)")
    args = parser.parse_args(argv)
    try:
        bundle = read_profile_files(args.files, args.analysis_profile, args.root)
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        parser.error(str(exc))
    print(json.dumps(bundle, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
