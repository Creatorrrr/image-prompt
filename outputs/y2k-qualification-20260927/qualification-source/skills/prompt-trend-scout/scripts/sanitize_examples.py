#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from common import SKILL_DIR, default_data_dir, load_json, normalize_space, read_records, run_id, utc_now, write_json


def compile_rules() -> dict[str, list[dict[str, Any]]]:
    rules = load_json(SKILL_DIR / "assets" / "stripping_rules.json")
    return {
        "remove": rules.get("remove_patterns", []),
        "license": rules.get("license_signal_patterns", []),
        "risk": rules.get("risk_patterns", []),
    }


def strip_text(text: str, rules: dict[str, list[dict[str, Any]]]) -> tuple[str, list[dict[str, str]]]:
    stripped: list[dict[str, str]] = []
    sanitized = text
    for rule in rules["remove"]:
        pattern = re.compile(rule["pattern"])
        matches = list(pattern.finditer(sanitized))
        for match in matches:
            value = match.group(0)
            stripped.append({"type": rule["type"], "value": value})
        sanitized = pattern.sub(" ", sanitized)
    return normalize_space(sanitized), stripped


def detect_flags(text: str, rules: dict[str, list[dict[str, Any]]], group: str) -> list[str]:
    flags: list[str] = []
    for rule in rules[group]:
        if re.search(rule["pattern"], text):
            flags.append(rule["flag"])
    return sorted(set(flags))


def extract_visual_grammar(text: str, image_description: str = "") -> dict[str, Any]:
    combined = f"{text} {image_description}".lower()
    elements: list[str] = []
    facets: dict[str, str] = {}
    if any(word in combined for word in ["android", "robot", "synthetic", "panel seam", "sensor eyes"]):
        facets["subject_kind"] = "robot"
        facets["mood_family"] = "uncanny"
        elements.append("robot_visible_proof")
    if any(word in combined for word in ["neon", "cyan", "magenta", "rim light", "colored rim"]):
        facets["lighting_family"] = "colored_light"
        elements.append("neon_colored_rim_light")
    if any(word in combined for word in ["wet asphalt", "puddle", "rain reflection", "glossy street"]):
        facets["weather"] = "rain"
        facets["place_type"] = "street"
        elements.append("wet_reflection_surface")
    if any(word in combined for word in ["scrapbook", "prompt card", "multi panel", "caption overlay"]):
        facets["camera_register"] = "phone"
        elements.append("phone_prompt_collage")
    if any(word in combined for word in ["raw documentary", "phone flash", "casual snapshot", "unpolished flash"]):
        facets["camera_register"] = "phone"
        facets["mood_family"] = "documentary"
        elements.append("raw_documentary_ai_style")
    return {"facets": facets, "visual_elements": sorted(set(elements))}


def sanitize_records(input_path: str, output: str | None = None, data_dir: str | None = None) -> dict[str, Any]:
    rules = compile_rules()
    records = read_records(Path(input_path))
    sanitized_records: list[dict[str, Any]] = []
    for record in records:
        raw_text = str(record.get("raw_text") or "")
        image_description = str(record.get("image_description") or "")
        cleaned_text, stripped_segments = strip_text(raw_text, rules)
        license_flags = detect_flags(raw_text, rules, "license")
        risk_flags = detect_flags(raw_text + " " + image_description, rules, "risk")
        flags = sorted(set(record.get("flags", []) + risk_flags))
        no_raw_reuse = False
        if license_flags:
            flags.extend(["no_raw_reuse", "no_republish"])
            no_raw_reuse = True
        license_signals = {
            "explicit_no_repost": "explicit_no_repost" in license_flags,
            "watermark_detected": "watermark_detected" in license_flags,
            "credit_required": "credit_required" in license_flags,
        }
        grammar = extract_visual_grammar(cleaned_text, image_description)
        sanitized_records.append(
            {
                "id": record["id"] + "-sanitized",
                "from_harvest_id": record["id"],
                "adapter": record.get("adapter", ""),
                "source_url_hash": record["id"],
                "sanitized_prompt": cleaned_text,
                "stripped_segments": stripped_segments,
                "image_observation": {
                    "observed": grammar["visual_elements"],
                    "note": normalize_space(image_description),
                },
                "abstract_visual_grammar": grammar,
                "license_signals": license_signals,
                "no_raw_reuse": no_raw_reuse,
                "flags": sorted(set(flags)),
            }
        )
    data_root = default_data_dir(data_dir)
    rid = run_id("sanitized")
    out = Path(output) if output else data_root / "sanitized" / f"{rid}.json"
    write_json(out, {"run_id": rid, "generated_at": utc_now(), "records": sanitized_records})
    return {"run_id": rid, "output": str(out), "records": sanitized_records}


def main() -> int:
    parser = argparse.ArgumentParser(description="Sanitize harvested prompt trend records.")
    parser.add_argument("input")
    parser.add_argument("--output")
    parser.add_argument("--data-dir")
    args = parser.parse_args()
    result = sanitize_records(args.input, output=args.output, data_dir=args.data_dir)
    print(result["output"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
