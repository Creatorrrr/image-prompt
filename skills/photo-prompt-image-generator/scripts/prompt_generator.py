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

SURREAL_LAYER_SLOTS = (
    "surreal_concept",
    "surreal_anchor",
    "scale_relation",
    "surreal_physics_detail",
)

SURREAL_INTENSITY_SLOTS = {
    "subtle": ("surreal_concept", "surreal_physics_detail"),
    "moderate": ("surreal_concept", "surreal_anchor", "surreal_physics_detail"),
    "bold": SURREAL_LAYER_SLOTS,
}

REFERENCE_EDIT_MODES = ("off", "identity", "younger_self", "brand_board")
TREND_LAYERS = (
    "off",
    "scrapbook_collage",
    "action_figure_packaging",
    "retro_flash",
    "clean_brand_portrait",
)


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


def article_for(phrase: str) -> str:
    """Return a simple English indefinite article for a rendered noun phrase."""
    word = clean_spaces(phrase).lower().split(" ", 1)[0] if phrase else ""
    if not word:
        return "a"
    if word.startswith(("honest", "hour", "heir")):
        return "an"
    if word.startswith(("uni", "use", "user", "euro", "one")):
        return "a"
    return "an" if word[0] in "aeiou" else "a"


def with_indefinite_article(phrase: str) -> str:
    phrase = clean_spaces(phrase)
    if not phrase:
        return ""
    if phrase.lower().startswith(("a ", "an ", "the ")):
        return phrase
    return f"{article_for(phrase)} {phrase}"


def entry_tags(entry: Entry) -> Set[str]:
    return set(entry.get("tags", []))


def entry_kinds(entry: Entry) -> Set[str]:
    kinds = set(entry.get("kind", []))
    return kinds or entry_tags(entry)


def entry_context_tokens(entry: Entry) -> Set[str]:
    tokens = set(entry_tags(entry)) | set(entry_kinds(entry))
    if entry.get("id"):
        tokens.add(str(entry["id"]))
    return tokens


def picked_context_tokens(picked: Dict[str, Entry]) -> Set[str]:
    tokens: Set[str] = set()
    for slot, entry in picked.items():
        tokens.add(slot)
        tokens.add(f"slot:{slot}")
        tokens |= entry_context_tokens(entry)
        if entry.get("id"):
            tokens.add(f"{slot}:{entry['id']}")
    return tokens


def picked_core_context_tokens(picked: Dict[str, Entry]) -> Set[str]:
    tokens: Set[str] = set()
    for slot in ("medium", "genre", "subject", "location"):
        entry = picked.get(slot)
        if entry:
            tokens |= entry_context_tokens(entry)
    return tokens


def picked_scene_context_tokens(picked: Dict[str, Entry]) -> Set[str]:
    tokens: Set[str] = set()
    for slot in ("medium", "genre", "location"):
        entry = picked.get(slot)
        if entry:
            tokens |= entry_context_tokens(entry)
    return tokens


def subject_category(picked: Dict[str, Entry]) -> str:
    subject = picked.get("subject")
    if not subject:
        return "generic"

    tokens = entry_context_tokens(subject)
    subject_id = str(subject.get("id", ""))
    if "human" in tokens:
        return "human"
    if "animal" in tokens:
        return "animal"
    if "food" in tokens:
        return "food"
    if "sign" in subject_id or "screen" in tokens or "text" in tokens:
        return "sign"
    if tokens & {"landscape", "nature", "interior", "architecture", "urban"} and not tokens & {"object", "product", "vehicle"}:
        return "environment"
    if tokens & {"plant", "macro"}:
        return "plant"
    if tokens & {"object", "product", "vehicle", "robot", "technology", "science"}:
        return "object"
    return "generic"


def values_as_set(item: JsonDict, *keys: str) -> Set[str]:
    values: Set[str] = set()
    for key in keys:
        raw = item.get(key)
        if isinstance(raw, str):
            values.add(raw)
        elif isinstance(raw, list):
            values |= {str(x) for x in raw}
    return values


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


def preset_uses_adult_context(preset: JsonDict) -> bool:
    if "adult" in entry_tags(preset):
        return True
    if str(preset.get("id", "")).startswith("adult_"):
        return True
    required = set(preset.get("required_slots", []))
    return bool(required & {"adult_context", "fetish_styling", "body_framing", "caption_context"})


def has_forced_surreal_slot(forced_choices: Optional[Dict[str, List[str]]]) -> bool:
    return bool(set((forced_choices or {}).keys()) & set(SURREAL_LAYER_SLOTS))


def should_activate_surreal_layer(
    preset: JsonDict,
    rng: random.Random,
    mode: str,
    probability: float,
    forced_choices: Optional[Dict[str, List[str]]] = None,
) -> bool:
    if has_forced_surreal_slot(forced_choices):
        return True
    if mode == "off":
        return False
    if mode == "on":
        return True
    if preset_uses_adult_context(preset):
        return False
    return rng.random() < max(0.0, min(1.0, probability))


def apply_surreal_layer(
    data: JsonDict,
    preset: JsonDict,
    rng: random.Random,
    picked: Dict[str, Entry],
    forced_choices: Optional[Dict[str, List[str]]] = None,
    intensity: str = "moderate",
) -> None:
    for slot in SURREAL_INTENSITY_SLOTS[intensity]:
        if slot in picked:
            continue
        entry = choose_slot(slot, data, preset, rng, picked, forced_choices)
        if entry is not None:
            picked[slot] = entry


def has_surreal_layer(picked: Dict[str, Entry]) -> bool:
    return any(slot in picked for slot in SURREAL_LAYER_SLOTS)


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


def compatible_with_slot_context(slot: str, item: Entry, picked: Dict[str, Entry]) -> bool:
    context = picked_context_tokens(picked)
    scene_context = picked_scene_context_tokens(picked)
    item_tokens = entry_context_tokens(item)
    item_id = str(item.get("id", ""))

    if values_as_set(item, "requires_any_tags", "requires_any") and not (
        values_as_set(item, "requires_any_tags", "requires_any") & context
    ):
        return False
    if not values_as_set(item, "requires_all_tags", "requires_all").issubset(context):
        return False
    if values_as_set(item, "exclude_any_tags", "exclude_any") & context:
        return False

    if slot in {"camera_type", "composition", "lens", "motion"}:
        if "surveillance" in item_tokens and not (context & {"surveillance", "cctv_frame", "dashcam_still", "bodycam_frame"}):
            return False
        if "vehicle" in item_tokens and not (context & {"vehicle", "automotive", "dashcam_still", "highway_dashcam"}):
            return False

    if slot == "lens" and context & {"phone", "front_facing_phone", "smartphone_camera", "selfie_camera_photo"}:
        if not (item_tokens & {"phone", "selfie", "social", "wide", "general"}):
            return False

    if slot in {"lighting", "light_type"}:
        if item_id == "headlights" and not (scene_context & {"street", "urban", "vehicle", "night", "surveillance"}):
            return False
        if item_id == "moonlight" and not (scene_context & {"nature", "night", "landscape", "wild"}):
            return False
        if item_id == "underwater_caustics" and not (scene_context & {"nature", "aquatic", "wild", "travel", "landscape"}):
            return False
        if item_id == "streetlamp" and not (scene_context & {"street", "urban", "night"}):
            return False
        if item_id == "lab_led" and not (context & {"science", "technology", "laboratory", "biolab", "data_center"}):
            return False
        if item_id == "monitor_glow" and not (context & {"technology", "gaming", "creator", "creator_room", "esports_room", "glass_office"}):
            return False
        if item_id in {"studio_strobe", "studio_flash", "softbox"} and not (
            context & {"studio", "commercial", "fashion", "beauty", "product", "portrait"}
        ):
            return False

    if slot == "light_shape":
        if item_id == "small_point_light" and not (context & {"flash", "night", "stage", "concert"}):
            return False
        if item_id in {"large_softbox_shape", "strip_light_shape", "gobo_pattern"} and not (
            context & {"studio", "commercial", "fashion", "beauty", "product", "portrait"}
        ):
            return False

    if slot == "body_framing" and "adult" in item_tokens and "adult" not in context:
        return False

    return True


def compatible_with_picked(
    pool: Sequence[Entry],
    picked: Dict[str, Entry],
    forced: bool = False,
    slot: str = "",
) -> List[Entry]:
    """
    Generic compatibility check.
    - for_any: keep item only if selected subject kind/tag intersects.
    - exclude_for_any: remove item if selected subject kind/tag intersects.
    - requires/excludes metadata and built-in slot guards compare against all picked tags.

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
        if slot and not compatible_with_slot_context(slot, item, picked):
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
    compatible = compatible_with_picked(pool, picked, forced=forced, slot=slot)
    if compatible:
        pool = compatible
    elif slot == "action":
        fallback = compatible_with_picked(full_pool, picked, forced=False, slot=slot)
        pool = fallback or pool or full_pool
    elif forced:
        # Forced choices should already be in pool; allow them even if odd.
        pass
    else:
        # Optional incompatible slots, such as person_origin for an animal subject, are skipped.
        if any(
            item.get("for_any")
            or item.get("exclude_for_any")
            or item.get("requires_any_tags")
            or item.get("requires_all_tags")
            or item.get("exclude_any_tags")
            for item in full_pool
        ):
            return None

    # If preset filters are too narrow, fall back to the full slot.
    if not pool:
        if forced:
            return None
        pool = compatible_with_picked(full_pool, picked, forced=False, slot=slot) or full_pool

    return weighted_choice(pool, rng)


# -----------------------------------------------------------------------------
# Rendering
# -----------------------------------------------------------------------------

DETAIL_REINFORCEMENT_SLOTS = (
    "camera_type",
    "camera_direction",
    "focus",
    "motion",
    "light_direction",
    "light_type",
    "light_intensity",
    "light_shape",
    "texture",
    "format",
)


def reinforce_detail_slots(
    data: JsonDict,
    preset: JsonDict,
    rng: random.Random,
    picked: Dict[str, Entry],
    forced_choices: Optional[Dict[str, List[str]]] = None,
) -> None:
    """Add compatible high-signal slots so detailed prompts are consistently specific."""
    minimum_slots = {
        "lighting": 3,
        "camera": 4,
        "finish": 2,
    }
    slot_groups = {
        "lighting": ("lighting", "light_direction", "light_type", "light_intensity", "light_shape"),
        "camera": ("camera_type", "camera_direction", "composition", "lens", "focus", "motion", "body_framing"),
        "finish": ("texture", "format", "quality"),
    }

    def group_count(group: str) -> int:
        return sum(1 for slot in slot_groups[group] if slot in picked)

    for slot in DETAIL_REINFORCEMENT_SLOTS:
        if slot in picked:
            continue
        if slot in slot_groups["lighting"] and group_count("lighting") >= minimum_slots["lighting"]:
            continue
        if slot in slot_groups["camera"] and group_count("camera") >= minimum_slots["camera"]:
            continue
        if slot in slot_groups["finish"] and group_count("finish") >= minimum_slots["finish"]:
            continue

        entry = choose_slot(slot, data, preset, rng, picked, forced_choices)
        if entry is not None:
            picked[slot] = entry


def build_fields(picked: Dict[str, Entry], lang: str) -> Dict[str, str]:
    values = {slot: localize(entry, lang) for slot, entry in picked.items()}

    subject = values.get("subject", "")
    action = values.get("action", "")
    costume = values.get("costume_style", "")

    if lang == "ko":
        subject_mods = [values[s] for s in ("person_origin", "appearance_type") if values.get(s)]
        if costume:
            subject_mods.append(costume + josa(costume, "을", "를") + " 입은")
        subject_with_mods = clean_spaces(" ".join(subject_mods + ([subject] if subject else [])))
        subject_phrase = clean_spaces(f"{action} {subject_with_mods}")
        object_phrase = subject_phrase + josa(subject_phrase, "을", "를") if subject_phrase else ""
    else:
        subject_suffixes = [values[s] for s in ("person_origin", "appearance_type") if values.get(s)]
        if costume:
            subject_suffixes.append(f"wearing {costume}")
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
    camera_slots = ("camera_type", "camera_direction", "composition", "body_framing", "lens", "focus", "motion")
    style_slots = (
        "world",
        "color",
        "mood",
        "surreal_concept",
        "surreal_anchor",
        "scale_relation",
        "surreal_physics_detail",
        "adult_context",
        "caption_context",
    )
    detail_slots = ("costume_style", "fetish_styling", "texture", "format", "quality")

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


def join_parts(parts: Sequence[str], fallback: str = "") -> str:
    return ", ".join(part for part in parts if part) or fallback


def render_surreal_layer_detail(picked: Dict[str, Entry], lang: str) -> str:
    if not has_surreal_layer(picked):
        return ""

    values = {slot: localize(entry, lang) for slot, entry in picked.items()}
    concept = values.get("surreal_concept", "")
    anchor = values.get("surreal_anchor", "")
    scale = values.get("scale_relation", "")
    physics = values.get("surreal_physics_detail", "")

    if lang == "ko":
        parts = []
        if concept:
            parts.append(f"초현실 사건은 {concept}")
        if anchor:
            parts.append(f"현실 앵커는 {anchor}")
        if scale:
            parts.append(f"스케일 관계는 {scale}")
        if physics:
            parts.append(f"물리 단서는 {physics}")
        body = "; ".join(parts)
        return ensure_period(
            f"포토리얼 초현실 레이어: {body}; 불가능한 장면이지만 합성이나 일러스트가 아니라 "
            "실제 카메라로 촬영된 순간처럼 보이게 하고, 스케일 단서, 그림자, 반사, 초점, "
            "경계면 가림, 현실 조명의 일관성을 분명히 유지한다."
        )

    parts = []
    if concept:
        parts.append(f"surreal event: {concept}")
    if anchor:
        parts.append(f"real-world anchor: {anchor}")
    if scale:
        parts.append(f"scale relation: {scale}")
    if physics:
        parts.append(f"physical realism cue: {physics}")
    body = "; ".join(parts)
    return ensure_period(
        f"Photoreal surreal layer: {body}; make the impossible scene read as a real camera capture, "
        "not a collage or illustration, with clear scale cues, shadows, reflections, focus behavior, "
        "boundary occlusion, and consistent real-world lighting."
    )


def render_subject_guidance(category: str, lang: str) -> str:
    if lang == "ko":
        guidance = {
            "human": "피사체의 자세, 시선, 표정, 손동작, 즉각적인 동작 의도가 한눈에 읽히게 하고, 주변 소품과 배경 요소는 그 행동을 설명하도록 배치한다",
            "animal": "동물의 자세, 움직임, 시선 방향, 털이나 깃의 질감이 자연스럽게 읽히게 하고, 주변 환경은 행동의 맥락을 설명하도록 배치한다",
            "food": "음식의 형태, 표면 질감, 온도감, 수분, 김, 소스나 부스러기 같은 식감 단서가 실제 촬영처럼 읽히게 한다",
            "object": "사물의 형태, 재질, 가장자리, 접지면, 스케일, 사용 흔적이 분명하게 보이게 하고, 주변 소품은 크기와 용도를 설명하도록 배치한다",
            "sign": "문자나 발광면의 가독성, 반사, 표면 오염, 주변 벽이나 바닥에 번지는 빛이 실제 장소 안에 자연스럽게 통합되게 한다",
            "plant": "식물의 줄기, 잎, 포자, 물방울, 표면 결이 실제 매크로 사진처럼 읽히게 한다",
            "environment": "공간의 구조, 주요 형태, 바닥/벽/천장 또는 하늘의 관계, 전경/중경/후경의 거리감이 명확히 읽히게 한다",
        }
        return guidance.get(category, "중심 피사체의 형태, 위치, 동작 또는 상태가 사진 안에서 명확히 읽히게 한다")

    guidance = {
        "human": "make the pose, gaze, expression, hand placement, and immediate intention readable, with nearby props and background details supporting the action",
        "animal": "make the animal posture, motion, eye direction, and fur or feather texture read naturally, with the environment supporting the behavior",
        "food": "make the shape, surface texture, temperature cues, moisture, steam, sauce, crumbs, and edible detail read like a real food photograph",
        "object": "make the object's form, material, edges, contact surface, scale, and signs of use clear, with nearby props explaining size and purpose",
        "sign": "make lettering or illuminated surfaces readable, with reflections, surface grime, and spill light integrated into the real location",
        "plant": "make stems, leaves, spores, droplets, and surface texture read like real macro photographic detail",
        "environment": "make the spatial structure, major forms, floor/wall/ceiling or sky relationships, foreground, midground, and background depth clear",
    }
    return guidance.get(category, "make the main subject's form, placement, action, or state clearly readable in the photograph")


def render_scene_guidance(category: str, lang: str) -> str:
    if lang == "ko":
        if category in {"food", "object", "plant", "sign"}:
            return "촬영 표면, 배경 거리, 접촉 그림자, 주변 소품의 크기 단서를 분명히 보여준다"
        return "공간의 깊이, 바닥/벽/하늘 또는 실내 구조, 전경/중경/후경의 거리감을 분명히 보여준다"

    if category in {"food", "object", "plant", "sign"}:
        return "show the shooting surface, background distance, contact shadows, and scale cues from nearby props"
    return "show clear spatial depth, environmental structure, foreground, midground, and background cues"


def render_finish_guidance(category: str, lang: str) -> str:
    if lang == "ko":
        guidance = {
            "human": "피부, 머리카락, 천, 금속, 유리, 메이크업, 액세서리 같은 소재 단서를 실제 질감으로 표현한다",
            "animal": "털, 깃, 눈, 발, 젖은 표면, 흙, 식물, 배경 질감을 실제 질감으로 표현한다",
            "food": "빵 껍질, 면, 소스, 수분, 김, 접시, 식기, 테이블 표면을 실제 식감과 재질로 표현한다",
            "object": "금속, 유리, 플라스틱, 세라믹, 종이, 먼지, 스크래치, 반사 같은 물성 단서를 정확히 표현한다",
            "sign": "발광면, 유리, 금속 프레임, 빗물, 먼지, 반사광, 표면 스크래치를 실제 재질처럼 표현한다",
            "plant": "잎맥, 줄기, 흙, 이끼, 물방울, 미세한 표면 결을 실제 매크로 질감으로 표현한다",
            "environment": "벽, 바닥, 천장, 창, 먼지, 습기, 반사, 그레인 같은 공간 질감을 실제 사진처럼 표현한다",
        }
        return guidance.get(category, "보이는 소재 단서를 실제 사진 질감으로 표현한다")

    guidance = {
        "human": "render skin, hair, fabric, metal, glass, makeup, and accessories with accurate material detail",
        "animal": "render fur, feathers, eyes, paws, moisture, soil, plants, and background texture with accurate detail",
        "food": "render crust, noodles, sauce, moisture, steam, plates, utensils, and tabletop surfaces with appetizing real texture",
        "object": "render metal, glass, plastic, ceramic, paper, dust, scratches, and reflections with accurate physical detail",
        "sign": "render illuminated panels, glass, metal frames, rain, dust, reflected light, and surface scratches like real materials",
        "plant": "render leaf veins, stems, soil, moss, droplets, and fine surface texture as real macro detail",
        "environment": "render walls, floors, ceilings, windows, dust, moisture, reflections, and grain as real photographic texture",
    }
    return guidance.get(category, "render visible material cues with accurate photographic texture")


def render_reference_edit_detail(mode: str, lang: str) -> str:
    if mode == "off":
        return ""
    if lang == "ko":
        details = {
            "identity": (
                "레퍼런스 편집 지시: 업로드된 인물 사진이 있다면 얼굴의 눈 모양과 간격, 눈썹, 코, 입술, 턱선, "
                "광대, 피부톤, 자연스러운 비대칭, 헤어라인을 유지하고, 조명과 배경만 새 장면에 맞게 바꾼다."
            ),
            "younger_self": (
                "레퍼런스 편집 지시: 현재 모습과 어린 시절 사진 두 장이 있다면 두 인물을 같은 공간 안에 배치하고, "
                "시선 방향, 거리, 중앙 오브젝트, 공통 조명과 그림자를 명확히 맞춰 한 장의 실제 사진처럼 만든다."
            ),
            "brand_board": (
                "레퍼런스 편집 지시: 업로드된 인물이나 제품의 핵심 형태를 유지하며, 같은 색감과 조명으로 여러 컷이 "
                "묶인 개인 브랜드 보드처럼 일관되게 구성한다."
            ),
        }
    else:
        details = {
            "identity": (
                "Reference-edit instruction: if an uploaded portrait is provided, preserve eye shape and spacing, eyebrows, nose, "
                "lips, jawline, cheekbones, skin tone, natural asymmetry, and hairline while changing only lighting, outfit, and setting."
            ),
            "younger_self": (
                "Reference-edit instruction: if current and childhood photos are provided, place both versions in one shared space, "
                "with clear gaze direction, distance, a central anchor object, shared lighting, and matching shadows."
            ),
            "brand_board": (
                "Reference-edit instruction: preserve the uploaded person or product identity while arranging multiple consistent shots "
                "as a personal brand board with unified color, lighting, and crop logic."
            ),
        }
    return ensure_period(details.get(mode, ""))


def render_trend_layer_detail(layer: str, lang: str) -> str:
    if layer == "off":
        return ""
    if lang == "ko":
        details = {
            "scrapbook_collage": (
                "트렌드 레이어: 같은 피사체의 겹쳐진 인화 사진, 테이프, 찢어진 종이, 작은 스티커, 클로즈업 조각을 "
                "포함한 스크랩북 콜라주 구성이며, 모든 조각은 같은 촬영 세계의 빛과 색을 공유한다."
            ),
            "action_figure_packaging": (
                "트렌드 레이어: 피사체를 수집용 액션 피규어 패키지처럼 구성하되, 투명 플라스틱 블리스터, 제품 카드, "
                "작은 액세서리 칸, 실제 제품 사진 같은 반사와 그림자를 명확히 표현한다."
            ),
            "retro_flash": (
                "트렌드 레이어: 2000년대 컴팩트 디지털카메라나 폰 직광 플래시처럼 강한 정면 플래시, 미세한 흔들림, "
                "살짝 과노출된 피부/표면, 어두운 배경 낙차를 사용한다."
            ),
            "clean_brand_portrait": (
                "트렌드 레이어: 개인 브랜드 프로필에 맞게 깨끗한 배경, 안정적인 크롭, 자연스러운 피부/소재 질감, "
                "프로필과 썸네일에서 읽히는 명확한 실루엣을 유지한다."
            ),
        }
    else:
        details = {
            "scrapbook_collage": (
                "Trend layer: build a scrapbook collage with overlapping printed photos of the same subject, tape, torn paper, "
                "small stickers, and close-up fragments, all sharing one coherent lighting and color world."
            ),
            "action_figure_packaging": (
                "Trend layer: stage the subject like a collectible action figure package with clear plastic blister, product card, "
                "small accessory compartments, and realistic product-photo reflections and shadows."
            ),
            "retro_flash": (
                "Trend layer: use a 2000s compact digital camera or phone direct-flash look with hard frontal flash, slight motion blur, "
                "a little overexposure on skin or surfaces, and a dark background falloff."
            ),
            "clean_brand_portrait": (
                "Trend layer: keep a clean personal-brand portrait structure with a tidy background, stable crop, natural skin or material texture, "
                "and a clear silhouette readable as a profile image or thumbnail."
            ),
        }
    return ensure_period(details.get(layer, ""))


def render_detailed_prompt(data: JsonDict, preset: JsonDict, picked: Dict[str, Entry], lang: str) -> str:
    fields = build_fields(picked, lang)
    values = {slot: localize(entry, lang) for slot, entry in picked.items()}
    category = subject_category(picked)

    lighting = join_parts(
        [
            values.get("lighting", ""),
            values.get("light_direction", ""),
            values.get("light_type", ""),
            values.get("light_intensity", ""),
            values.get("light_shape", ""),
        ],
        "natural, believable photographic light" if lang == "en" else "자연스럽고 설득력 있는 사진 조명",
    )
    camera = join_parts(
        [
            values.get("camera_type", ""),
            values.get("camera_direction", ""),
            values.get("composition", ""),
            values.get("body_framing", ""),
            values.get("lens", ""),
            values.get("focus", ""),
            values.get("motion", ""),
        ],
        "clear camera placement, deliberate composition, realistic focus" if lang == "en" else "명확한 카메라 위치, 의도적인 구도, 사실적인 초점",
    )
    mood = join_parts(
        [
            values.get("world", ""),
            values.get("color", ""),
            values.get("mood", ""),
            values.get("adult_context", ""),
            values.get("caption_context", ""),
        ],
        "coherent color, mood, and world context" if lang == "en" else "일관된 색감, 분위기, 세계관 맥락",
    )
    finish = join_parts(
        [
            values.get("costume_style", ""),
            values.get("fetish_styling", ""),
            values.get("texture", ""),
            values.get("format", ""),
            values.get("quality", ""),
        ],
        "photo-ready finish with accurate material detail" if lang == "en" else "정확한 소재 디테일을 가진 이미지 생성용 마감",
    )

    if lang == "ko":
        subject = fields.get("subject_phrase") or values.get("subject", "중심 피사체")
        location = fields.get("location_phrase") or values.get("location", "구체적인 장소")
        genre = values.get("genre", "사진")
        medium = values.get("medium", "실사 사진")
        surreal_detail = render_surreal_layer_detail(picked, lang)
        subject_guidance = render_subject_guidance(category, lang)
        scene_guidance = render_scene_guidance(category, lang)
        finish_guidance = render_finish_guidance(category, lang)
        prompt = (
            f"{medium}로 렌더링할 {genre}. "
            f"중심 피사체와 상태: {subject}; {subject_guidance}. "
            f"장면과 장소: {location}; {scene_guidance}. "
            f"카메라와 구도: {camera}; 피사체 크기, 프레임 가장자리, 원근감, 초점 위치, 움직임 처리를 명확히 한다. "
            f"조명: {lighting}; 그림자 방향, 하이라이트, 반사광, 노출 균형, 대기감을 실제 촬영처럼 보이게 한다. "
            f"색감과 분위기: {mood}; 색 대비, 감정 톤, 세계관 맥락이 피사체와 장소에 맞아야 한다. "
            f"{surreal_detail} "
            f"질감과 마감: {finish}; {finish_guidance}. "
            "이미지 생성 시 요구사항을 빠뜨리지 말고, 막연한 스타일 요약보다 구체적인 사진 결과를 우선한다."
        )
    else:
        subject = fields.get("subject_phrase") or values.get("subject", "the main subject")
        location = fields.get("location_phrase") or values.get("location", "a specific location")
        genre = values.get("genre", "photography")
        medium = values.get("medium", "photograph")
        surreal_detail = render_surreal_layer_detail(picked, lang)
        subject_guidance = render_subject_guidance(category, lang)
        scene_guidance = render_scene_guidance(category, lang)
        finish_guidance = render_finish_guidance(category, lang)
        prompt = (
            f"Create {with_indefinite_article(medium)} in the style of {genre}. "
            f"Subject and state: {subject}; {subject_guidance}. "
            f"Scene and location: {location}; {scene_guidance}. "
            f"Camera and composition: {camera}; define subject scale, frame edges, perspective, focus behavior, and any motion treatment clearly. "
            f"Lighting: {lighting}; make shadow direction, highlights, reflected light, exposure balance, and atmosphere feel like a real photographic capture. "
            f"Color and mood: {mood}; keep the palette, emotional tone, and world context coherent with the subject and setting. "
            f"{surreal_detail} "
            f"Texture, format, and finish: {finish}; {finish_guidance}. "
            "Prioritize a specific, image-ready photographic result over a vague style summary."
        )

    return clean_spaces(prompt)


def unique_join(parts: Sequence[str], separator: str = ", ") -> str:
    seen: Set[str] = set()
    unique: List[str] = []
    for part in parts:
        cleaned = clean_spaces(part)
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(cleaned)
    return separator.join(unique)


def render_compact_prompt(data: JsonDict, preset: JsonDict, picked: Dict[str, Entry], lang: str) -> str:
    fields = build_fields(picked, lang)
    values = {slot: localize(entry, lang) for slot, entry in picked.items()}
    category = subject_category(picked)

    lighting = unique_join(
        [
            values.get("lighting", ""),
            values.get("light_direction", ""),
            values.get("light_type", ""),
            values.get("light_intensity", ""),
            values.get("light_shape", ""),
        ]
    )
    camera = unique_join(
        [
            values.get("camera_type", ""),
            values.get("camera_direction", ""),
            values.get("composition", ""),
            values.get("body_framing", ""),
            values.get("lens", ""),
            values.get("focus", ""),
            values.get("motion", ""),
        ]
    )
    mood = unique_join([values.get("color", ""), values.get("mood", ""), values.get("world", "")])
    finish = unique_join([values.get("texture", ""), values.get("quality", "")])
    location = fields.get("location_phrase") or values.get("location", "")
    prop = values.get("prop", "")
    hair = values.get("hair_style", "")
    costume = values.get("costume_style", "")

    if lang == "ko":
        subject_mods = [
            values.get("person_origin", ""),
            values.get("appearance_type", ""),
            hair,
            costume + josa(costume, "을", "를") + " 입은" if costume else "",
        ]
        subject = clean_spaces(" ".join([part for part in subject_mods if part] + [values.get("subject", "중심 피사체")]))
        action_parts = [values.get("action", ""), f"{prop}와 함께" if prop else ""]
        details = [
            unique_join(action_parts),
            location,
            lighting,
            camera,
            mood,
            values.get("adult_context", ""),
            values.get("fetish_styling", ""),
            values.get("caption_context", ""),
            finish,
            "자연스러운 피부 질감" if category == "human" else "",
            "텍스트와 워터마크 없음",
        ]
        lead = unique_join(
            ["초사실적", values.get("format", ""), values.get("genre", ""), values.get("medium", "실사 사진")],
            " ",
        )
        prompt = f"{lead}, {subject}, {unique_join(details)}"
        return ensure_period(prompt)

    subject_suffixes = [
        values.get("person_origin", ""),
        values.get("appearance_type", ""),
        hair,
        f"wearing {costume}" if costume else "",
    ]
    subject = values.get("subject", "the main subject")
    suffix = unique_join(subject_suffixes)
    if suffix:
        subject = clean_spaces(f"{subject} {suffix}")
    action_parts = [values.get("action", ""), f"with {prop}" if prop else ""]
    details = [
        unique_join(action_parts),
        location,
        lighting,
        camera,
        mood,
        values.get("adult_context", ""),
        values.get("fetish_styling", ""),
        values.get("caption_context", ""),
        finish,
        "natural skin texture" if category == "human" else "",
        "no text or watermark",
    ]
    lead = unique_join(
        ["Ultra-realistic", values.get("format", ""), values.get("genre", ""), values.get("medium", "photograph")],
        " ",
    )
    prompt = f"{lead} of {subject}, {unique_join(details)}"
    return ensure_period(prompt)


def render_prompt(
    data: JsonDict,
    preset: JsonDict,
    picked: Dict[str, Entry],
    lang: str,
    rng: random.Random,
    detail_level: str = "standard",
    reference_edit_mode: str = "off",
    trend_layer: str = "off",
) -> str:
    if detail_level == "detailed":
        prompt = render_detailed_prompt(data, preset, picked, lang)
        additions = [
            render_reference_edit_detail(reference_edit_mode, lang),
            render_trend_layer_detail(trend_layer, lang),
        ]
        return clean_spaces(" ".join([prompt] + [part for part in additions if part]))

    if detail_level == "compact":
        prompt = render_compact_prompt(data, preset, picked, lang)
        additions = [
            render_reference_edit_detail(reference_edit_mode, lang),
            render_trend_layer_detail(trend_layer, lang),
        ]
        return clean_spaces(" ".join([prompt] + [part for part in additions if part]))

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
    surreal_detail = render_surreal_layer_detail(picked, lang)
    if surreal_detail:
        prompt = clean_spaces(f"{prompt} {surreal_detail}")
    reference_detail = render_reference_edit_detail(reference_edit_mode, lang)
    if reference_detail:
        prompt = clean_spaces(f"{prompt} {reference_detail}")
    trend_detail = render_trend_layer_detail(trend_layer, lang)
    if trend_detail:
        prompt = clean_spaces(f"{prompt} {trend_detail}")
    return clean_spaces(prompt)


def choose_negative_entries(
    data: JsonDict,
    rng: random.Random,
    count: int = 12,
    include_surreal: bool = False,
    picked: Optional[Dict[str, Entry]] = None,
) -> List[Entry]:
    picked = picked or {}
    negative_pools = data.get("negative_prompt_pools", {})
    if negative_pools:
        pool_names = ["base"]
        category = subject_category(picked)
        context = picked_context_tokens(picked)
        core_context = picked_core_context_tokens(picked)
        if category == "human":
            pool_names.append("human")
        if category == "animal":
            pool_names.append("animal")
        if category == "food":
            pool_names.extend(["object_product", "food"])
        if category in {"object", "plant"}:
            pool_names.append("object_product")
        if category == "sign":
            pool_names.extend(["object_product", "text_signage"])
        if core_context & {"architecture", "real_estate"} or (category == "environment" and "interior" in core_context):
            pool_names.append("architecture_interior")

        seen: Set[str] = set()
        negatives: List[Entry] = []
        for pool_name in pool_names:
            for entry in negative_pools.get(pool_name, []):
                key = localize(entry, "en")
                if key and key not in seen:
                    negatives.append(entry)
                    seen.add(key)
    else:
        negatives = data.get("negative_prompt", [])

    if not negatives:
        entries: List[Entry] = []
    else:
        count = min(max(count, 1), len(negatives))
        entries = rng.sample(negatives, k=count)

    if include_surreal:
        seen = {localize(entry, "en") for entry in entries}
        surreal_pool = data.get("surreal_negative_prompt", [])
        if negative_pools:
            surreal_pool = negative_pools.get("surreal", surreal_pool)
        for entry in surreal_pool:
            if localize(entry, "en") not in seen:
                entries.append(entry)
                seen.add(localize(entry, "en"))

    return entries


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
    detail_level: str = "standard",
    surreal_mode: str = "off",
    surreal_probability: float = 0.35,
    surreal_intensity: str = "moderate",
    reference_edit_mode: str = "off",
    trend_layer: str = "off",
) -> JsonDict:
    preset = choose_preset(data, rng, preset_id)
    picked: Dict[str, Entry] = {}

    for slot in selected_slots_for_preset(preset, data, rng, forced_choices, priority_bias):
        entry = choose_slot(slot, data, preset, rng, picked, forced_choices)
        if entry is not None:
            picked[slot] = entry

    if should_activate_surreal_layer(preset, rng, surreal_mode, surreal_probability, forced_choices):
        apply_surreal_layer(data, preset, rng, picked, forced_choices, surreal_intensity)

    if detail_level == "detailed":
        reinforce_detail_slots(data, preset, rng, picked, forced_choices)

    result: JsonDict = {
        "preset_id": preset.get("id"),
        "preset": {lang: localize(preset, lang) for lang in langs},
    }

    for lang in langs:
        result[f"prompt_{lang}"] = render_prompt(
            data,
            preset,
            picked,
            lang,
            rng,
            detail_level,
            reference_edit_mode,
            trend_layer,
        )

    if include_negative:
        negative_entries = choose_negative_entries(data, rng, negative_count, has_surreal_layer(picked), picked)
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
    parser.add_argument(
        "--detail-level",
        choices=["standard", "detailed", "compact"],
        default="standard",
        help="Prompt rendering detail level. Use detailed for a longer image-ready prompt or compact for a ReactorPrompt-style single paragraph.",
    )
    parser.add_argument("--surreal-mode", choices=["off", "auto", "on"], default="off", help="Apply a photoreal surreal layer: off disables it, auto applies by probability, on always applies it.")
    parser.add_argument("--surreal-probability", type=float, default=0.35, help="Probability for --surreal-mode auto. Clamped to 0..1.")
    parser.add_argument("--surreal-intensity", choices=["subtle", "moderate", "bold"], default="moderate", help="How many surreal layer slots to add when the layer is active.")
    parser.add_argument("--reference-edit-mode", choices=REFERENCE_EDIT_MODES, default="off", help="Append reference-image editing instructions for uploaded-photo workflows.")
    parser.add_argument("--trend-layer", choices=TREND_LAYERS, default="off", help="Append a social trend layout layer without changing the base photo preset.")
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
            detail_level=args.detail_level,
            surreal_mode=args.surreal_mode,
            surreal_probability=args.surreal_probability,
            surreal_intensity=args.surreal_intensity,
            reference_edit_mode=args.reference_edit_mode,
            trend_layer=args.trend_layer,
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
