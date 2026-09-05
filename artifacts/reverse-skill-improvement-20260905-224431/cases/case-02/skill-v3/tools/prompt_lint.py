#!/usr/bin/env python3
"""Check a prompt text file for unresolved references to unavailable evidence.

This narrow boundary check needs only the prompt text. It does not validate a
salience plan, score prose style, or establish visual fidelity.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


STANDALONE_PROMPT_BOUNDARY_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "internal provenance label",
        re.compile(
            r"\b(?:current[-\s]+source|source[-\s]+(?:relative|visible|specific|"
            r"supported|derived|based|qualified|matching|evidence[-\s]+qualified))\b",
            re.IGNORECASE,
        ),
    ),
    (
        "unavailable image artifact",
        re.compile(
            r"\b(?:attached|source|reference|input|provided|original)[-\s]+"
            r"(?:image|photo(?:graph)?|picture|render|frame|attachment)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "unresolved comparison target",
        re.compile(
            r"\b(?:match(?:es|ed|ing)?|reproduc(?:e|es|ed|ing)|"
            r"reconstruct(?:s|ed|ing)?|cop(?:y|ies|ied|ying)|mirror(?:s|ed|ing)?|"
            r"preserv(?:e|es|ed|ing)|retain(?:s|ed|ing)?|keep(?:s|ing)?|kept|"
            r"maintain(?:s|ed|ing)?)\s+(?:the\s+)?(?:source|reference|original)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "unresolved source placeholder",
        re.compile(
            r"\bsource[-\s]+(?:side|subject|components?|placement|pose|orientation|"
            r"relation|appearance|reading|aesthetic|silhouette|topology|axis|"
            r"viewpoint|crop|garment|hair|face|body)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "unresolved original-state placeholder",
        re.compile(
            r"\boriginal[-\s]+(?:composition|pose|appearance|lighting|colou?rs?|"
            r"geometry|crop|framing|layout|proportions?|silhouette)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "deictic image instruction",
        re.compile(
            r"\b(?:as|exactly\s+as)\s+(?:shown|seen|pictured|depicted)\s+"
            r"(?:in|on)\s+(?:the\s+)?(?:source|reference|image|photo|picture|attachment)\b",
            re.IGNORECASE,
        ),
    ),
)


def audit_standalone_prompt_text(prompt_text: Any) -> list[str]:
    """Reject literal prompt text that still depends on unavailable evidence.

    This is intentionally a narrow output-boundary check rather than a style
    linter. Physical scene language such as ``light source`` and self-contained
    state verbs such as ``remains outside the frame`` are valid.
    """

    if not isinstance(prompt_text, str):
        return ["authored prompt text must be a string"]

    errors: list[str] = []
    occupied_spans: list[tuple[int, int]] = []
    for category, pattern in STANDALONE_PROMPT_BOUNDARY_PATTERNS:
        for match in pattern.finditer(prompt_text):
            span = match.span()
            if any(span[0] < end and start < span[1] for start, end in occupied_spans):
                continue
            occupied_spans.append(span)
            errors.append(
                "authored prompt is not standalone: "
                f"{category} {match.group(0)!r}; replace it with the literal visible "
                "target state or relation"
            )
    return errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", help="UTF-8 prompt text file")
    args = parser.parse_args(argv)

    try:
        prompt_text = Path(args.prompt).read_text(encoding="utf-8")
        errors = audit_standalone_prompt_text(prompt_text)
    except (OSError, UnicodeError) as exc:
        errors = [f"cannot read prompt file {args.prompt!r}: {exc}"]

    print(
        json.dumps(
            {"status": "ok" if not errors else "failed", "errors": errors}, indent=2
        )
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
