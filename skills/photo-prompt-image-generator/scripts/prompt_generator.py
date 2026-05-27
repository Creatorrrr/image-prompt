#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Photo prompt generator
- Tags are managed in a JSON file.
- Generates Korean, English, or both using the same random choices.
- Uses presets, slot filters, weights, subject compatibility, priority-biased optional slots,
  and user-forced slot selections.

Usage examples:
  python prompt_generator.py --tags photo_prompt_tags.json --n 5 --lang both
  python prompt_generator.py --tags photo_prompt_tags.json --preset street_documentary --n 3 --seed 42
  python prompt_generator.py --tags photo_prompt_tags.json --list-presets
  python prompt_generator.py --tags photo_prompt_tags.json --show-slots
  python prompt_generator.py --tags photo_prompt_tags.json --list-tags camera_type
  python prompt_generator.py --tags photo_prompt_tags.json --preset tiktok_vertical_snapshot --set subject=influencer_creator --set person_origin=south_korea --set appearance_type=idol_like
  python prompt_generator.py --tags photo_prompt_tags.json --json-output --include-negative --include-choices --n 10 > prompts.json
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set

JsonDict = Dict[str, Any]
Entry = Dict[str, Any]


# -----------------------------------------------------------------------------
# Basic helpers
# -----------------------------------------------------------------------------

def load_json(path: str | Path) -> JsonDict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Tag JSON not found: {p}")
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def localize(item: JsonDict, lang: str) -> str:
    """Return localized text from {'ko': '...', 'en': '...'} style objects."""
    if lang in item and item[lang]:
        return str(item[lang])
    if "en" in item and item["en"]:
        return str(item["en"])
    if "ko" in item and item["ko"]:
        return str(item["ko"])
    if "id" in item:
        return str(item["id"])
    return ""


def last_hangul_char(text: str) -> Optional[str]:
    for ch in reversed(text.strip()):
        if "\uac00" <= ch <= "\ud7a3":
            return ch
    return None


def has_batchim(text: str) -> bool:
    ch = last_hangul_char(text)
    if ch is None:
        return False
    return (ord(ch) - 0xAC00) % 28 != 0


def josa(text: str, with_batchim: str, without_batchim: str) -> str:
    """Very small Korean particle helper: 을/를, 이/가, 은/는, etc."""
    return with_batchim if has_batchim(text) else without_batchim


def clean_spaces(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)
    text = re.sub(r"([.!?]){2,}", r"\1", text)
    return text


def ensure_period(text: str) -> str:
    text = clean_spaces(text)
    if text and text[-1] not in ".!?。":
        text += "."
    return text


def entry_tags(entry: Entry) -> Set[str]:
    return set(entry.get("tags", []))


def entry_kinds(entry: Entry) -> Set[str]:
    kinds = set(entry.get("kind", []))
    return kinds or entry_tags(entry)


# -----------------------------------------------------------------------------
# Filtering and weighted choices
# -----------------------------------------------------------------------------

def apply_filter(pool: Sequence[Entry], flt: Optional[JsonDict]) -> List[Entry]:
    if not flt:
        return list(pool)

    out = list(pool)

    if flt.get("ids"):
        ids = set(flt["ids"])
        out = [x for x in out if x.get("id") in ids]

    if flt.get("tags_any"):
        tags_any = set(flt["tags_any"])
        out = [x for x in out if entry_tags(x) & tags_any]

    if flt.get("tags_all"):
        tags_all = set(flt["tags_all"])
        out = [x for x in out if tags_all.issubset(entry_tags(x))]

    if flt.get("kinds_any"):
        kinds_any = set(flt["kinds_any"])
        out = [x for x in out if entry_kinds(x) & kinds_any]

    if flt.get("kinds_all"):
        kinds_all = set(flt["kinds_all"])
        out = [x for x in out if kinds_all.issubset(entry_kinds(x))]

    if flt.get("exclude_tags"):
        exclude = set(flt["exclude_tags"])
        out = [x for x in out if not (entry_tags(x) & exclude)]

    if flt.get("exclude_kinds"):
        exclude_kinds = set(flt["exclude_kinds"])
        out = [x for x in out if not (entry_kinds(x) & exclude_kinds)]

    return out


def weighted_choice(pool: Sequence[Entry], rng: random.Random) -> Entry:
    if not pool:
        raise ValueError("weighted_choice() received an empty pool")

    weights = []
    for item in pool:
        w = item.get("weight", 1)
        try:
            w = float(w)
        except (TypeError, ValueError):
            w = 1.0
        weights.append(max(w, 0.0))

    if sum(weights) <= 0:
        return rng.choice(list(pool))
    return rng.choices(list(pool), weights=weights, k=1)[0]


def choose_preset(data: JsonDict, rng: random.Random, preset_id: Optional[str] = None) -> JsonDict:
    presets = data.get("presets", [])
    if not presets:
        raise ValueError("No presets found in JSON.")

    if preset_id:
        for p in presets:
            if p.get("id") == preset_id:
                return p
        valid = ", ".join(p.get("id", "?") for p in presets)
        raise ValueError(f"Unknown preset '{preset_id}'. Available presets: {valid}")

    return weighted_choice(presets, rng)


# -----------------------------------------------------------------------------
# Priority-biased slot selection
# -----------------------------------------------------------------------------

def get_generation_settings(data: JsonDict) -> JsonDict:
    return data.get("generation_settings", {}) or {}


def get_slot_priorities(data: JsonDict) -> Dict[str, float]:
    raw = data.get("slot_priorities", data.get("slot_priority", {})) or {}
    priorities: Dict[str, float] = {}
    for k, v in raw.items():
        try:
            priorities[str(k)] = float(v)
        except (TypeError, ValueError):
            priorities[str(k)] = 0.0
    return priorities


def boosted_probability(base: float, slot: str, data: JsonDict, priority_bias: Optional[float]) -> float:
    """
    Boost optional-slot probability according to global slot priority.

    base=0.45, priority=max, priority_bias=0.5 -> 0.725
    base=0.45, priority=half, priority_bias=0.5 -> 0.5875
    """
    base = max(0.0, min(1.0, float(base)))
    priorities = get_slot_priorities(data)
    if not priorities:
        return base

    if priority_bias is None:
        settings = get_generation_settings(data)
        priority_bias = float(settings.get("priority_bias", 0.0))

    bias = max(0.0, float(priority_bias))
    if bias <= 0:
        return base

    max_priority = max(max(priorities.values()), 1.0)
    slot_priority = max(priorities.get(slot, 0.0), 0.0)
    ratio = min(slot_priority / max_priority, 1.0)
    return max(0.0, min(1.0, base + (1.0 - base) * ratio * bias))


def optional_slot_specs(preset: JsonDict, data: JsonDict) -> List[JsonDict]:
    settings = get_generation_settings(data)
    default_p = float(settings.get("default_optional_probability", 0.5))

    specs: List[JsonDict] = []

    def normalize(opt: Any, source: str) -> Optional[JsonDict]:
        if isinstance(opt, str):
            return {"slot": opt, "probability": default_p, "source": source}
        if isinstance(opt, dict) and opt.get("slot"):
            spec = dict(opt)
            spec.setdefault("probability", spec.get("prob", default_p))
            spec["source"] = source
            return spec
        return None

    for opt in preset.get("optional_slots", []):
        spec = normalize(opt, "preset")
        if spec:
            specs.append(spec)

    if not preset.get("disable_auto_optional", False):
        disabled = set(preset.get("skip_auto_slots", []))
        already = set(preset.get("required_slots", [])) | {s["slot"] for s in specs}
        for opt in settings.get("auto_optional_slots", []):
            spec = normalize(opt, "auto")
            if not spec:
                continue
            slot = spec["slot"]
            if slot in disabled or slot in already:
                continue
            specs.append(spec)
            already.add(slot)

    return specs


def selected_slots_for_preset(
    preset: JsonDict,
    data: JsonDict,
    rng: random.Random,
    forced_choices: Optional[Dict[str, List[str]]] = None,
    priority_bias: Optional[float] = None,
) -> List[str]:
    required = list(preset.get("required_slots", []))
    slots = required[:]

    for spec in optional_slot_specs(preset, data):
        slot = spec.get("slot")
        if not slot:
            continue
        base_probability = float(spec.get("probability", spec.get("prob", 0.5)))
        if spec.get("priority_boost", True):
            probability = boosted_probability(base_probability, slot, data, priority_bias)
        else:
            probability = max(0.0, min(1.0, base_probability))
        if rng.random() < probability:
            slots.append(slot)

    # Forced slots must be present even if the preset did not select them.
    for slot in (forced_choices or {}):
        if slot not in slots:
            slots.append(slot)

    # Make sure dependencies are available before compatible slots are picked.
    order = data.get("slot_pick_order", [])
    order_index = {slot: i for i, slot in enumerate(order)}
    fallback_order = {
        "medium": 0,
        "genre": 1,
        "subject": 2,
        "person_origin": 3,
        "appearance_type": 4,
        "action": 5,
        "location": 6,
    }

    def priority(s: str) -> int:
        if s in order_index:
            return order_index[s]
        return fallback_order.get(s, 100)

    deduped = []
    seen = set()
    for s in sorted(slots, key=priority):
        if s not in seen:
            deduped.append(s)
            seen.add(s)
    return deduped


# -----------------------------------------------------------------------------
# Compatibility and forced choices
# -----------------------------------------------------------------------------

def parse_forced_choices(items: Optional[Sequence[str]]) -> Dict[str, List[str]]:
    forced: Dict[str, List[str]] = {}
    for raw in items or []:
        if "=" not in raw:
            raise ValueError(f"Invalid --set value '{raw}'. Use --set slot=id or --set slot=id1,id2")
        slot, ids_raw = raw.split("=", 1)
        slot = slot.strip()
        ids = [x.strip() for x in re.split(r"[,|]", ids_raw) if x.strip()]
        if not slot or not ids:
            raise ValueError(f"Invalid --set value '{raw}'. Use --set slot=id or --set slot=id1,id2")
        forced[slot] = ids
    return forced


def load_forced_choices_from_json(raw: Optional[str]) -> Dict[str, List[str]]:
    if not raw:
        return {}

    candidate = Path(raw)
    if candidate.exists():
        payload = json.loads(candidate.read_text(encoding="utf-8"))
    else:
        payload = json.loads(raw)

    if not isinstance(payload, dict):
        raise ValueError("--set-json must be a JSON object, e.g. '{\"subject\":\"fashion_model\"}'")

    forced: Dict[str, List[str]] = {}
    for slot, value in payload.items():
        if isinstance(value, str):
            forced[str(slot)] = [value]
        elif isinstance(value, list):
            forced[str(slot)] = [str(x) for x in value]
        else:
            raise ValueError(f"Invalid --set-json value for slot '{slot}': expected string or list")
    return forced


def merge_forced_choices(*choices: Dict[str, List[str]]) -> Dict[str, List[str]]:
    merged: Dict[str, List[str]] = {}
    for choice in choices:
        for slot, ids in choice.items():
            merged[slot] = list(ids)
    return merged


def forced_required_subject_kinds(data: JsonDict, forced_choices: Dict[str, List[str]]) -> Set[str]:
    """If a forced slot item declares for_any, use it to steer random subject choice."""
    required: Set[str] = set()
    slots = data.get("slots", {})
    for slot, ids in forced_choices.items():
        if slot == "subject" or slot not in slots:
            continue
        id_set = set(ids)
        for item in slots[slot]:
            if item.get("id") in id_set and item.get("for_any"):
                allowed = set(item.get("for_any", []))
                required = allowed if not required else required & allowed
    return required


def compatible_with_picked(pool: Sequence[Entry], picked: Dict[str, Entry], forced: bool = False) -> List[Entry]:
    """
    Generic compatibility check.
    - for_any: keep item only if selected subject kind/tag intersects.
    - exclude_for_any: remove item if selected subject kind/tag intersects.

    Forced choices bypass this check because user intent should win.
    """
    if forced:
        return list(pool)

    subject = picked.get("subject")
    if not subject:
        # Do not remove generic items when the subject is not chosen yet.
        return [item for item in pool if not item.get("for_any")]

    subject_kinds = entry_kinds(subject)
    compatible: List[Entry] = []
    for item in pool:
        allowed = set(item.get("for_any", []))
        excluded = set(item.get("exclude_for_any", []))
        if allowed and not (allowed & subject_kinds):
            continue
        if excluded and (excluded & subject_kinds):
            continue
        compatible.append(item)
    return compatible


def choose_slot(
    slot: str,
    data: JsonDict,
    preset: JsonDict,
    rng: random.Random,
    picked: Dict[str, Entry],
    forced_choices: Optional[Dict[str, List[str]]] = None,
) -> Optional[Entry]:
    slots = data.get("slots", {})
    if slot not in slots:
        raise ValueError(f"Slot '{slot}' is referenced but not defined in JSON.")

    full_pool = list(slots[slot])
    filters = preset.get("filters", {}).get(slot)
    pool = apply_filter(full_pool, filters)

    forced_ids = (forced_choices or {}).get(slot)
    forced = bool(forced_ids)
    if forced_ids:
        ids = set(forced_ids)
        forced_pool = [x for x in full_pool if x.get("id") in ids]
        if not forced_pool:
            valid = ", ".join(x.get("id", "?") for x in full_pool[:30])
            raise ValueError(f"Unknown id for slot '{slot}': {forced_ids}. Example valid ids: {valid}")
        pool = forced_pool

    # If a human-only forced modifier is given, steer subject choice toward human.
    if slot == "subject" and not forced:
        required_kinds = forced_required_subject_kinds(data, forced_choices or {})
        if required_kinds:
            steered = [x for x in pool if entry_kinds(x) & required_kinds]
            if steered:
                pool = steered

    # Compatibility is generic, but action keeps the older generous fallback.
    compatible = compatible_with_picked(pool, picked, forced=forced)
    if compatible:
        pool = compatible
    elif slot == "action":
        fallback = compatible_with_picked(full_pool, picked, forced=False)
        pool = fallback or pool or full_pool
    elif forced:
        # Forced choices should already be in pool; allow them even if odd.
        pass
    else:
        # Optional incompatible slots, such as person_origin for an animal subject, are skipped.
        if any(item.get("for_any") or item.get("exclude_for_any") for item in full_pool):
            return None

    # If preset filters are too narrow, fall back to the full slot.
    if not pool:
        if forced:
            return None
        pool = full_pool

    return weighted_choice(pool, rng)


# -----------------------------------------------------------------------------
# Rendering
# -----------------------------------------------------------------------------

def build_fields(picked: Dict[str, Entry], lang: str) -> Dict[str, str]:
    values = {slot: localize(entry, lang) for slot, entry in picked.items()}

    subject = values.get("subject", "")
    action = values.get("action", "")

    if lang == "ko":
        subject_mods = [values[s] for s in ("person_origin", "appearance_type") if values.get(s)]
        subject_with_mods = clean_spaces(" ".join(subject_mods + ([subject] if subject else [])))
        subject_phrase = clean_spaces(f"{action} {subject_with_mods}")
        object_phrase = subject_phrase + josa(subject_phrase, "을", "를") if subject_phrase else ""
    else:
        subject_suffixes = [values[s] for s in ("person_origin", "appearance_type") if values.get(s)]
        subject_with_mods = clean_spaces(" ".join(([subject] if subject else []) + subject_suffixes))
        subject_phrase = clean_spaces(f"{subject_with_mods} {action}")
        object_phrase = subject_phrase

    location_entry = picked.get("location")
    if location_entry and lang == "ko":
        location_phrase = location_entry.get("phrase_ko") or (localize(location_entry, "ko") + "에서")
    elif location_entry:
        location_phrase = location_entry.get("phrase_en") or ("in " + localize(location_entry, "en"))
    else:
        location_phrase = ""

    lighting_slots = ("lighting", "light_direction", "light_type", "light_intensity", "light_shape")
    camera_slots = ("camera_type", "camera_direction", "composition", "lens", "focus", "motion")
    style_slots = ("world", "color", "mood")
    detail_slots = ("texture", "format", "quality")

    lighting_parts = [values[s] for s in lighting_slots if values.get(s)]
    camera_parts = [values[s] for s in camera_slots if values.get(s)]

    if lang == "ko":
        technique_chunks = []
        if lighting_parts:
            technique_chunks.append("조명은 " + ", ".join(lighting_parts))
        if camera_parts:
            technique_chunks.append("카메라는 " + ", ".join(camera_parts))
        technique_sentence = ensure_period("; ".join(technique_chunks)) if technique_chunks else ""

        style_parts = [values[s] for s in style_slots if values.get(s)]
        style_sentence = ensure_period("전체 분위기는 " + ", ".join(style_parts)) if style_parts else ""

        detail_parts = [values[s] for s in detail_slots if values.get(s)]
        detail_sentence = ensure_period("디테일은 " + ", ".join(detail_parts)) if detail_parts else ""
    else:
        technique_chunks = []
        if lighting_parts:
            technique_chunks.append("Lighting: " + ", ".join(lighting_parts))
        if camera_parts:
            technique_chunks.append("Camera: " + ", ".join(camera_parts))
        technique_sentence = ensure_period("; ".join(technique_chunks)) if technique_chunks else ""

        style_parts = [values[s] for s in style_slots if values.get(s)]
        style_sentence = ensure_period("Overall mood: " + ", ".join(style_parts)) if style_parts else ""

        detail_parts = [values[s] for s in detail_slots if values.get(s)]
        detail_sentence = ensure_period("Finishing details: " + ", ".join(detail_parts)) if detail_parts else ""

    fields = {
        **values,
        "location_phrase": location_phrase,
        "subject_with_mods": subject_with_mods,
        "subject_phrase": subject_phrase,
        "object_phrase": object_phrase,
        "technique_sentence": technique_sentence,
        "style_sentence": style_sentence,
        "detail_sentence": detail_sentence,
    }
    return fields


def render_prompt(data: JsonDict, preset: JsonDict, picked: Dict[str, Entry], lang: str, rng: random.Random) -> str:
    style = preset.get("template_style", "natural")
    templates_by_lang = data.get("templates", {}).get(style, {})
    templates = templates_by_lang.get(lang) or templates_by_lang.get("en")

    if not templates:
        # Safe fallback template if JSON has no template section.
        if lang == "ko":
            templates = [
                "{medium}. {location_phrase} {object_phrase} 담은 {genre}. {technique_sentence} {style_sentence} {detail_sentence}"
            ]
        else:
            templates = [
                "{medium}. {genre} featuring {subject_phrase} {location_phrase}. {technique_sentence} {style_sentence} {detail_sentence}"
            ]

    template = rng.choice(templates)
    fields = build_fields(picked, lang)
    prompt = template.format(**fields)
    return clean_spaces(prompt)


def choose_negative_entries(data: JsonDict, rng: random.Random, count: int = 12) -> List[Entry]:
    negatives = data.get("negative_prompt", [])
    if not negatives:
        return []
    count = min(max(count, 1), len(negatives))
    return rng.sample(negatives, k=count)


def render_negative_prompt(entries: Sequence[Entry], lang: str) -> str:
    return ", ".join(localize(x, lang) for x in entries)


def generate_once(
    data: JsonDict,
    rng: random.Random,
    preset_id: Optional[str],
    langs: Sequence[str],
    include_negative: bool,
    negative_count: int,
    include_choices: bool,
    forced_choices: Optional[Dict[str, List[str]]] = None,
    priority_bias: Optional[float] = None,
) -> JsonDict:
    preset = choose_preset(data, rng, preset_id)
    picked: Dict[str, Entry] = {}

    for slot in selected_slots_for_preset(preset, data, rng, forced_choices, priority_bias):
        entry = choose_slot(slot, data, preset, rng, picked, forced_choices)
        if entry is not None:
            picked[slot] = entry

    result: JsonDict = {
        "preset_id": preset.get("id"),
        "preset": {lang: localize(preset, lang) for lang in langs},
    }

    for lang in langs:
        result[f"prompt_{lang}"] = render_prompt(data, preset, picked, lang, rng)

    if include_negative:
        negative_entries = choose_negative_entries(data, rng, negative_count)
        for lang in langs:
            result[f"negative_{lang}"] = render_negative_prompt(negative_entries, lang)

    if include_choices:
        result["choices"] = {
            slot: {
                "id": entry.get("id"),
                "ko": localize(entry, "ko"),
                "en": localize(entry, "en"),
                "tags": entry.get("tags", []),
                "kind": entry.get("kind", []),
            }
            for slot, entry in picked.items()
        }

    return result


# -----------------------------------------------------------------------------
# CLI utilities
# -----------------------------------------------------------------------------

def parse_langs(lang: str) -> List[str]:
    if lang == "both":
        return ["ko", "en"]
    if lang in {"ko", "en"}:
        return [lang]
    raise ValueError("--lang must be one of: ko, en, both")


def print_plain(results: Sequence[JsonDict], langs: Sequence[str], include_negative: bool, include_choices: bool) -> None:
    for i, item in enumerate(results, start=1):
        print(f"\n[{i}] preset: {item.get('preset_id')}")
        for lang in langs:
            label = "KO" if lang == "ko" else "EN"
            print(f"{label}: {item.get(f'prompt_{lang}', '')}")
            if include_negative and item.get(f"negative_{lang}"):
                print(f"{label} negative: {item[f'negative_{lang}']}")
        if include_choices and item.get("choices"):
            compact = {slot: choice.get("id") for slot, choice in item["choices"].items()}
            print("choices:", json.dumps(compact, ensure_ascii=False))


def list_presets(data: JsonDict) -> None:
    for p in data.get("presets", []):
        ko = localize(p, "ko")
        en = localize(p, "en")
        print(f"{p.get('id')}: {ko} / {en}")


def show_slots(data: JsonDict) -> None:
    priorities = get_slot_priorities(data)
    for slot, entries in data.get("slots", {}).items():
        priority = priorities.get(slot, 0)
        print(f"{slot}: {len(entries)} tags, priority={priority:g}")


def list_tags(data: JsonDict, slot: str) -> None:
    slots = data.get("slots", {})
    if slot not in slots:
        valid = ", ".join(slots.keys())
        raise ValueError(f"Unknown slot '{slot}'. Available slots: {valid}")
    for item in slots[slot]:
        print(f"{item.get('id')}: {localize(item, 'ko')} / {localize(item, 'en')}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Random photo prompt generator using JSON-managed tags.")
    parser.add_argument("--tags", default="photo_prompt_tags.json", help="Path to tag JSON file.")
    parser.add_argument("--lang", choices=["ko", "en", "both"], default="both", help="Output language.")
    parser.add_argument("--n", type=int, default=5, help="Number of prompts to generate.")
    parser.add_argument("--preset", default=None, help="Preset id. Omit for random preset.")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible output.")
    parser.add_argument("--priority-bias", type=float, default=None, help="Optional-slot priority boost. Omit to use JSON setting.")
    parser.add_argument("--set", dest="set_values", action="append", default=[], help="Force a slot id, e.g. --set subject=fashion_model. Repeatable. Use commas to randomly choose among ids.")
    parser.add_argument("--set-json", default=None, help="Inline JSON or path to JSON file for forced slots, e.g. '{\"subject\":\"fashion_model\"}'.")
    parser.add_argument("--include-negative", action="store_true", help="Also output a negative prompt.")
    parser.add_argument("--negative-count", type=int, default=12, help="Number of negative tags to sample.")
    parser.add_argument("--include-choices", action="store_true", help="Include chosen slot details in plain or JSON output.")
    parser.add_argument("--json-output", action="store_true", help="Print results as JSON.")
    parser.add_argument("--list-presets", action="store_true", help="List preset ids and exit.")
    parser.add_argument("--show-slots", action="store_true", help="List slots, tag counts, and priorities then exit.")
    parser.add_argument("--list-tags", metavar="SLOT", help="List tag ids for a slot then exit.")
    args = parser.parse_args(argv)

    data = load_json(args.tags)

    if args.list_presets:
        list_presets(data)
        return 0
    if args.show_slots:
        show_slots(data)
        return 0
    if args.list_tags:
        list_tags(data, args.list_tags)
        return 0

    rng = random.Random(args.seed)
    langs = parse_langs(args.lang)
    forced_choices = merge_forced_choices(
        parse_forced_choices(args.set_values),
        load_forced_choices_from_json(args.set_json),
    )

    if args.n < 1:
        raise ValueError("--n must be at least 1")

    results = [
        generate_once(
            data=data,
            rng=rng,
            preset_id=args.preset,
            langs=langs,
            include_negative=args.include_negative,
            negative_count=args.negative_count,
            include_choices=args.include_choices,
            forced_choices=forced_choices,
            priority_bias=args.priority_bias,
        )
        for _ in range(args.n)
    ]

    if args.json_output:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_plain(results, langs, args.include_negative, args.include_choices)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
