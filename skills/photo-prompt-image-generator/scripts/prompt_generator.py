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
import hashlib
import json
import math
import os
import random
import re
import sys
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Set

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
SELECTION_MODES = ("rule", "semantic", "hybrid")
DEFAULT_SELECTION_MODE = "semantic"
DEFAULT_SEMANTIC_INTENT = (
    "photorealistic image-ready photo prompt with coherent subject, location, "
    "lighting, mood, camera, composition, texture, and format"
)
NOVELTY_LEVELS = ("low", "medium", "high")
FILTER_STRICTNESS_MODES = ("hard", "soft", "off")
SEMANTIC_PROFILES = ("conservative", "balanced", "exploratory")
SEMANTIC_AXIS_MODES = ("auto", "off")
INTENT_STEERING_MODES = ("auto", "off")
LLM_POLISH_MODES = ("off", "strict")
SEMANTIC_PROVIDER = "gemini"
DEFAULT_SEMANTIC_DIMENSIONS = 768
SEMANTIC_MODEL_ID = "gemini-embedding-2"
SEMANTIC_TEXT_RECIPE_VERSION = "semantic-text-v2"

SEMANTIC_PROFILE_CONFIGS: Dict[str, Dict[str, float]] = {
    "conservative": {
        "preset_window": 0.08,
        "preset_candidate_limit": 5,
        "preset_weight_floor": 0.86,
        "preset_overall_weight": 0.35,
        "preset_axis_mean_weight": 0.35,
        "preset_axis_floor_weight": 0.30,
        "axis_coverage_target": 0.70,
        "axis_coverage_weight": 0.14,
        "slot_window": 0.08,
        "slot_candidate_limit": 5,
        "slot_weight_floor": 0.86,
        "filter_bonus": 0.12,
        "filter_penalty": 0.55,
        "temperature_multiplier": 1.2,
    },
    "balanced": {
        "preset_window": 0.14,
        "preset_candidate_limit": 8,
        "preset_weight_floor": 0.82,
        "preset_overall_weight": 0.45,
        "preset_axis_mean_weight": 0.35,
        "preset_axis_floor_weight": 0.20,
        "axis_coverage_target": 0.68,
        "axis_coverage_weight": 0.22,
        "slot_window": 0.14,
        "slot_candidate_limit": 8,
        "slot_weight_floor": 0.82,
        "filter_bonus": 0.18,
        "filter_penalty": 0.35,
        "temperature_multiplier": 1.0,
    },
    "exploratory": {
        "preset_window": 0.24,
        "preset_candidate_limit": 14,
        "preset_weight_floor": 0.72,
        "preset_overall_weight": 0.55,
        "preset_axis_mean_weight": 0.30,
        "preset_axis_floor_weight": 0.15,
        "axis_coverage_target": 0.64,
        "axis_coverage_weight": 0.28,
        "slot_window": 0.24,
        "slot_candidate_limit": 14,
        "slot_weight_floor": 0.72,
        "filter_bonus": 0.08,
        "filter_penalty": 0.12,
        "temperature_multiplier": 0.82,
    },
}

SEMANTIC_AXIS_FAMILY_KEYWORDS: Dict[str, tuple[str, ...]] = {
    "human": ("human", "person", "people", "portrait", "model", "actor", "commuter", "traveler", "인간", "사람", "인물"),
    "urban": ("urban", "city", "street", "alley", "subway", "neon", "rooftop", "도시", "거리", "골목", "지하철"),
    "horror": ("horror", "fear", "nightmare", "terror", "scary", "eerie", "uncanny", "noir", "gothic", "공포", "악몽", "두려움"),
    "fantasy": ("fantasy", "magic", "magical", "surreal", "dream", "impossible", "환상", "마법", "초현실"),
}

SEMANTIC_AXIS_SLOT_ROUTES: Dict[str, tuple[str, ...]] = {
    "human": ("subject", "appearance_type", "expression", "subject_framing"),
    "urban": ("location", "world", "weather", "lighting"),
    "horror": ("mood", "lighting", "light_shape", "weather", "color", "texture"),
    "fantasy": ("surreal_concept", "surreal_anchor", "surreal_physics_detail", "mood"),
}

SEMANTIC_SLOT_CAPTION_TEMPLATES: Dict[str, str] = {
    "subject": "Photo subject concept: {description}. It should retrieve visual subjects by identity, role, species, object type, and scene relevance.",
    "location": "Photographic location concept: {description}. It should retrieve places by setting, environment, city or nature context, interior or exterior space, and atmosphere.",
    "lighting": "Photographic lighting concept: {description}. It should retrieve light by source, mood, shadow behavior, color temperature, and photographic realism.",
    "light_type": "Specific light-source concept: {description}. It should retrieve lamps, neon, flash, sun, screens, strobes, and practical light sources.",
    "light_shape": "Light-shape concept: {description}. It should retrieve visible beam shapes, shadow patterns, edge light, caustics, diffusion, and photographic light geometry.",
    "mood": "Image mood concept: {description}. It should retrieve emotional tone, genre feeling, tension, romance, nostalgia, horror, calm, or surreal atmosphere.",
    "film_emulation": "Film and camera-emulation concept: {description}. It should retrieve analog film stocks, halation, grain, color cast, instant film, disposable camera, or CCD looks.",
    "weather": "Weather and atmosphere concept: {description}. It should retrieve rain, fog, snow, humidity, frost, sea spray, heat haze, and environmental air effects.",
    "surreal_concept": "Photoreal surreal event concept: {description}. It should retrieve impossible events that still look like real photographed scenes.",
    "surreal_anchor": "Physical anchor for a photoreal surreal scene: {description}. It should retrieve the real object or surface where the impossible event is grounded.",
}

DEFAULT_FACET_VOCAB: JsonDict = {
    "subject_kind": ["human", "animal", "object", "food", "environment", "plant", "sign"],
    "place_type": ["urban", "street", "interior", "nature", "studio", "commercial", "transport", "home"],
    "time_of_day": ["day", "night", "dawn", "dusk", "indoor_unspecified"],
    "weather": ["clear", "rain", "snow", "fog", "underwater", "none"],
    "lighting_family": ["natural_light", "artificial_light", "colored_light", "flash", "studio_light", "low_light"],
    "mood_family": ["calm", "tense", "romantic", "surreal", "nostalgic", "commercial", "documentary"],
    "camera_register": ["phone", "professional", "surveillance", "vintage", "studio", "macro"],
    "safety_tier": ["general", "adult_compatible", "adult_only"],
}


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


def has_cli_option(args: Sequence[str], name: str) -> bool:
    return name in args or any(arg.startswith(name + "=") for arg in args)


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


def normalize_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(x) for x in value]
    return [str(value)]


def semantic_description_for_entry(entry: Entry) -> str:
    if entry.get("embedding_text"):
        return " ".join(normalize_list(entry.get("embedding_text")))
    if entry.get("en"):
        return str(entry["en"])
    if entry.get("ko"):
        return str(entry["ko"])
    return str(entry.get("id", ""))


def semantic_caption_for_entry(entry: Entry, slot: Optional[str] = None) -> str:
    description = semantic_description_for_entry(entry)
    if slot:
        template = SEMANTIC_SLOT_CAPTION_TEMPLATES.get(
            slot,
            "Photo prompt slot concept for {slot}: {description}. It should retrieve visually compatible photographic details for this slot.",
        )
        return template.format(slot=slot, description=description)
    return (
        f"Photo prompt preset concept: {description}. It should retrieve a coherent photographic recipe "
        "including subject, place, lighting, camera, mood, and style."
    )


def dictionary_hash(data: JsonDict) -> str:
    material = {
        "version": data.get("version"),
        "presets": data.get("presets", []),
        "preset_families": data.get("preset_families", []),
        "recipes": data.get("recipes", []),
        "slots": data.get("slots", {}),
        "facet_vocab": data.get("facet_vocab", {}),
    }
    payload = json.dumps(material, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def semantic_text_for_entry(entry: Entry, slot: Optional[str] = None) -> str:
    parts: List[str] = [semantic_caption_for_entry(entry, slot)]
    for key in ("en", "ko"):
        if entry.get(key):
            parts.append(f"{key} label: {entry[key]}.")
    for key in ("aliases", "keywords", "tags", "kind"):
        values = normalize_list(entry.get(key))
        if values:
            parts.append(f"{key}: {', '.join(values)}.")
    if slot:
        parts.append(f"slot: {slot}.")
    if entry.get("id"):
        parts.append(f"stable id: {entry['id']}.")
    facets = entry.get("facets", {}) or {}
    if isinstance(facets, dict):
        for key, values in facets.items():
            normalized = normalize_list(values)
            if normalized:
                parts.append(f"facet {key}: {', '.join(normalized)}.")
    return " ".join(parts)


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    if not a or not b:
        return 0.0
    numerator = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a <= 0 or norm_b <= 0:
        return 0.0
    return numerator / (norm_a * norm_b)


def semantic_dimensions_value(dimensions: int) -> int:
    try:
        dims = int(dimensions)
    except (TypeError, ValueError) as exc:
        raise ValueError("embedding dimensions must be an integer") from exc
    if dims < 1:
        raise ValueError("embedding dimensions must be at least 1")
    return dims


def get_gemini_api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError(
            "GEMINI_API_KEY or GOOGLE_API_KEY is required for Gemini semantic embeddings."
        )
    return key


def extract_embedding_values(response: Any) -> List[List[float]]:
    embeddings = getattr(response, "embeddings", None)
    if embeddings is None and isinstance(response, dict):
        embeddings = response.get("embeddings")
    if embeddings is None:
        embedding = getattr(response, "embedding", None)
        if embedding is None and isinstance(response, dict):
            embedding = response.get("embedding")
        embeddings = [embedding] if embedding is not None else []

    values_list: List[List[float]] = []
    for embedding in embeddings:
        values = getattr(embedding, "values", None)
        if values is None and isinstance(embedding, dict):
            values = embedding.get("values")
        if values is None:
            raise RuntimeError("Gemini embedding response did not include vector values.")
        values_list.append([float(value) for value in values])
    return values_list


def round_embedding_vector(vector: Sequence[float], dimensions: int) -> List[float]:
    if len(vector) != dimensions:
        raise ValueError(
            f"Gemini returned {len(vector)} embedding dimensions, expected {dimensions}."
        )
    return [round(float(value), 6) for value in vector]


def embed_texts_with_gemini(
    texts: Sequence[str],
    model: str = SEMANTIC_MODEL_ID,
    dimensions: int = DEFAULT_SEMANTIC_DIMENSIONS,
    api_key: Optional[str] = None,
    retry_attempts: int = 4,
    retry_initial_delay: float = 15.0,
) -> List[List[float]]:
    if not texts:
        return []
    dims = semantic_dimensions_value(dimensions)
    key = get_gemini_api_key(api_key)

    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:
        raise RuntimeError(
            "google-genai is required for Gemini semantic embeddings. "
            "Install it with `python3 -m pip install -r requirements.txt`."
        ) from exc

    client = genai.Client(api_key=key)
    config = types.EmbedContentConfig(
        output_dimensionality=dims,
        task_type="SEMANTIC_SIMILARITY",
    )
    response = None
    attempts = max(1, int(retry_attempts) + 1)
    for attempt in range(attempts):
        try:
            response = client.models.embed_content(
                model=model,
                contents=[str(text) for text in texts],
                config=config,
            )
            break
        except Exception as exc:
            message = str(exc)
            retryable = (
                "429" in message
                or "503" in message
                or "RESOURCE_EXHAUSTED" in message
                or "UNAVAILABLE" in message
            )
            if not retryable or attempt >= attempts - 1:
                raise
            delay = max(0.0, float(retry_initial_delay)) * (2 ** attempt)
            if delay > 0:
                time.sleep(delay)
    if response is None:
        raise RuntimeError("Gemini embedding request did not return a response.")
    vectors = extract_embedding_values(response)
    if len(vectors) != len(texts):
        raise RuntimeError(
            f"Gemini returned {len(vectors)} embeddings for {len(texts)} input texts."
        )
    return [round_embedding_vector(vector, dims) for vector in vectors]


def semantic_entry_key(kind: str, entry: Entry, slot: Optional[str] = None) -> str:
    if kind == "preset":
        return f"preset:{entry.get('id')}"
    if kind == "virtual_preset":
        return f"preset:virtual:{entry.get('id')}"
    return f"slot:{slot}:{entry.get('id')}"


def iter_semantic_entries(data: JsonDict) -> List[tuple[str, str, Entry, Optional[str]]]:
    entries: List[tuple[str, str, Entry, Optional[str]]] = []
    for preset in data.get("presets", []):
        key = semantic_entry_key("preset", preset)
        entries.append((key, "preset", preset, None))
    for recipe in data.get("recipes", []):
        key = semantic_entry_key("virtual_preset", recipe)
        entries.append((key, "virtual_preset", recipe, None))
    for slot, slot_entries in data.get("slots", {}).items():
        for entry in slot_entries:
            key = semantic_entry_key("slot", entry, slot)
            entries.append((key, "slot", entry, slot))
    return entries


def build_semantic_index_payload(
    data: JsonDict,
    dimensions: int = DEFAULT_SEMANTIC_DIMENSIONS,
    provider: str = SEMANTIC_PROVIDER,
    model: str = SEMANTIC_MODEL_ID,
    api_key: Optional[str] = None,
    batch_size: int = 1,
    request_interval: float = 0.0,
    retry_attempts: int = 4,
    retry_initial_delay: float = 15.0,
    progress_callback: Optional[Callable[[int, int], None]] = None,
) -> JsonDict:
    if provider != SEMANTIC_PROVIDER:
        raise ValueError(f"Unsupported semantic provider '{provider}'. Only '{SEMANTIC_PROVIDER}' is supported.")
    dims = semantic_dimensions_value(dimensions)
    batch = max(1, int(batch_size))
    rows = iter_semantic_entries(data)
    texts = [semantic_text_for_entry(entry, slot) for _, _, entry, slot in rows]
    vectors: List[List[float]] = []
    for start in range(0, len(texts), batch):
        vectors.extend(
            embed_texts_with_gemini(
                texts[start : start + batch],
                model=model,
                dimensions=dims,
                api_key=api_key,
                retry_attempts=retry_attempts,
                retry_initial_delay=retry_initial_delay,
            )
        )
        done = min(start + batch, len(texts))
        if progress_callback:
            progress_callback(done, len(texts))
        if request_interval > 0 and done < len(texts):
            time.sleep(request_interval)
    if len(vectors) != len(rows):
        raise RuntimeError(f"Expected {len(rows)} semantic vectors, received {len(vectors)}.")

    entries: JsonDict = {}
    for (key, kind, entry, slot), text, vector in zip(rows, texts, vectors):
        entries[key] = {
            "kind": kind,
            "slot": slot,
            "id": entry.get("id"),
            "text": text,
            "vector": vector,
        }
    return {
        "provider": provider,
        "dictionary_hash": dictionary_hash(data),
        "semantic_text_recipe": SEMANTIC_TEXT_RECIPE_VERSION,
        "embedding_model": model,
        "embedding_dimensions": dims,
        "entries": entries,
    }


def validate_semantic_index_metadata(
    payload: JsonDict,
    data: JsonDict,
    provider: str = SEMANTIC_PROVIDER,
    model: str = SEMANTIC_MODEL_ID,
    dimensions: int = DEFAULT_SEMANTIC_DIMENSIONS,
) -> None:
    expected = dictionary_hash(data)
    if payload.get("dictionary_hash") != expected:
        raise ValueError(
            "Semantic index dictionary_hash does not match the tag dictionary. "
            "Regenerate it with build_semantic_index.py."
        )
    if payload.get("semantic_text_recipe") != SEMANTIC_TEXT_RECIPE_VERSION:
        raise ValueError(
            f"Semantic index semantic_text_recipe is {payload.get('semantic_text_recipe')!r}, "
            f"expected {SEMANTIC_TEXT_RECIPE_VERSION!r}. Regenerate it with build_semantic_index.py."
        )
    if payload.get("provider", SEMANTIC_PROVIDER) != provider:
        raise ValueError(
            f"Semantic index provider is {payload.get('provider')!r}, expected {provider!r}."
        )
    if payload.get("embedding_model") != model:
        raise ValueError(
            f"Semantic index embedding_model is {payload.get('embedding_model')!r}, expected {model!r}."
        )
    expected_dims = semantic_dimensions_value(dimensions)
    if int(payload.get("embedding_dimensions", -1)) != expected_dims:
        raise ValueError(
            f"Semantic index embedding_dimensions is {payload.get('embedding_dimensions')!r}, "
            f"expected {expected_dims}."
        )


def load_semantic_index(
    path: Optional[str | Path],
    data: JsonDict,
    semantic_index: Optional[JsonDict] = None,
    provider: str = SEMANTIC_PROVIDER,
    model: str = SEMANTIC_MODEL_ID,
    dimensions: int = DEFAULT_SEMANTIC_DIMENSIONS,
) -> JsonDict:
    if semantic_index is not None:
        payload = semantic_index
    else:
        if not path:
            raise FileNotFoundError(
                "Semantic index is required for semantic or hybrid selection. "
                "Build it with build_semantic_index.py."
            )
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Semantic index not found: {p}")
        payload = json.loads(p.read_text(encoding="utf-8"))
    validate_semantic_index_metadata(payload, data, provider, model, dimensions)
    return payload


def facet_tokens(entry: Entry) -> Set[str]:
    tokens: Set[str] = set()
    facets = entry.get("facets", {}) or {}
    if not isinstance(facets, dict):
        return tokens
    for key, values in facets.items():
        for value in normalize_list(values):
            tokens.add(f"{key}:{value}")
    return tokens


def guard_values(entry: Entry, key: str) -> Set[str]:
    guards = entry.get("hard_guards", {}) or {}
    if not isinstance(guards, dict):
        return set()
    return set(normalize_list(guards.get(key)))


def compatible_with_facet_guards(item: Entry, preset: JsonDict, picked: Dict[str, Entry]) -> bool:
    context: Set[str] = set()
    context |= facet_tokens(preset)
    for entry in picked.values():
        context |= facet_tokens(entry)
    item_facets = facet_tokens(item)

    preset_excludes = guard_values(preset, "exclude_facets")
    if preset_excludes & item_facets:
        return False

    requires = guard_values(item, "requires_facets")
    if requires and not requires.issubset(context | item_facets):
        return False

    excludes = guard_values(item, "exclude_facets")
    if excludes & context:
        return False

    return True


def novelty_settings(novelty: str) -> tuple[float, float]:
    if novelty == "low":
        return (1.8, 0.05)
    if novelty == "high":
        return (0.75, 0.45)
    return (1.15, 0.18)


def semantic_profile_config(profile: str) -> Dict[str, float]:
    return SEMANTIC_PROFILE_CONFIGS.get(profile, SEMANTIC_PROFILE_CONFIGS["balanced"])


def default_filter_strictness(selection_mode: str) -> str:
    if selection_mode == "semantic":
        return "soft"
    return "hard"


def default_semantic_profile(selection_mode: str) -> str:
    if selection_mode == "semantic":
        return "balanced"
    return "conservative"


def default_semantic_weight(selection_mode: str) -> float:
    if selection_mode == "semantic":
        return 0.75
    if selection_mode == "hybrid":
        return 0.35
    return 0.0


def default_intent_steering(selection_mode: str) -> str:
    if selection_mode in {"semantic", "hybrid"}:
        return "auto"
    return "off"


def resolve_semantic_runtime_options(
    selection_mode: str,
    filter_strictness: Optional[str],
    semantic_weight: Optional[float],
    semantic_profile: Optional[str],
) -> tuple[str, float, str]:
    resolved_filter = filter_strictness or default_filter_strictness(selection_mode)
    resolved_profile = semantic_profile or default_semantic_profile(selection_mode)
    resolved_weight = default_semantic_weight(selection_mode) if semantic_weight is None else float(semantic_weight)
    if resolved_filter not in FILTER_STRICTNESS_MODES:
        raise ValueError(f"Invalid filter_strictness '{resolved_filter}'.")
    if resolved_profile not in SEMANTIC_PROFILES:
        raise ValueError(f"Invalid semantic_profile '{resolved_profile}'.")
    if not 0.0 <= resolved_weight <= 1.0:
        raise ValueError("--semantic-weight must be between 0 and 1")
    return resolved_filter, resolved_weight, resolved_profile


def clean_intent_axis(text: str) -> str:
    return clean_spaces(text.strip(" \t\r\n,;+/|"))


def unique_axes(values: Sequence[str]) -> List[str]:
    axes: List[str] = []
    seen: Set[str] = set()
    for value in values:
        axis = clean_intent_axis(str(value))
        key = axis.lower()
        if axis and key not in seen:
            axes.append(axis)
            seen.add(key)
    return axes[:6]


def delimiter_intent_axes(intent: str) -> List[str]:
    chunks = re.split(r"\s*(?:[,+|/;\n]+|\band\b|\bwith\b|및)\s*", intent, flags=re.IGNORECASE)
    axes = unique_axes(chunks)
    return axes if len(axes) > 1 else []


def fallback_intent_axes(intent: str) -> List[str]:
    lowered = intent.lower()
    labels = {
        "human": "human portrait",
        "urban": "urban city street",
        "horror": "horror fear nightmare",
        "fantasy": "fantasy magic surreal",
    }
    return [labels[family] for family in labels if axis_text_has_family(lowered, family)][:6]


def axis_text_has_family(text: str, family: str) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in SEMANTIC_AXIS_FAMILY_KEYWORDS.get(family, ()))


def axis_families_for_text(text: str) -> List[str]:
    return [
        family
        for family in SEMANTIC_AXIS_FAMILY_KEYWORDS
        if axis_text_has_family(text, family)
    ]


def semantic_axis_embedding_text(axis: str) -> str:
    expansions = {
        "human": "human person portrait subject, model or actor, readable face and body presence",
        "urban": "urban city street location, alley, subway, neon, concrete, metropolitan environment",
        "horror": "horror fear nightmare mood, eerie uncanny tension, analog horror unease, dark suspense",
        "fantasy": "fantasy magic surreal impossible event, photoreal dreamlike phenomenon, supernatural atmosphere",
    }
    matched = [expansions[family] for family in axis_families_for_text(axis)]
    if matched:
        return "; ".join(matched)
    return axis


def extract_intent_axes(
    intent: str,
    explicit_axes: Optional[Sequence[str]] = None,
    semantic_axis_mode: str = "auto",
) -> JsonDict:
    if semantic_axis_mode not in SEMANTIC_AXIS_MODES:
        raise ValueError(f"Invalid semantic_axis_mode '{semantic_axis_mode}'.")
    explicit = unique_axes(explicit_axes or [])
    if explicit:
        source = "explicit"
        axes = explicit
    elif semantic_axis_mode == "off":
        source = "off"
        axes = [clean_intent_axis(intent)]
    else:
        axes = delimiter_intent_axes(intent)
        if axes:
            source = "delimiter"
        else:
            axes = fallback_intent_axes(intent)
            source = "fallback" if axes else "full_intent"
    if not axes:
        axes = [clean_intent_axis(intent)]
        source = "full_intent"
    return {
        "mode": semantic_axis_mode,
        "source": source,
        "items": [{"text": axis, "source": source} for axis in axes[:6]],
    }


def embed_single_semantic_text(
    text: str,
    model: str,
    dimensions: int,
    api_key: Optional[str],
) -> List[float]:
    return embed_texts_with_gemini(
        [text],
        model=model,
        dimensions=dimensions,
        api_key=api_key,
    )[0]


def semantic_profile_float(context: JsonDict, key: str, default: float) -> float:
    config = semantic_profile_config(str(context.get("semantic_profile", "balanced")))
    try:
        return float(config.get(key, default))
    except (TypeError, ValueError):
        return default


def initial_axis_coverage(axis_vectors: Sequence[JsonDict], profile: str) -> JsonDict:
    config = semantic_profile_config(profile)
    target = float(config.get("axis_coverage_target", 0.68))
    return {
        "target": target,
        "items": [
            {
                "index": index,
                "text": item.get("text", ""),
                "families": item.get("families", []),
                "best_score": 0.0,
                "best_slot": None,
                "best_entry": None,
            }
            for index, item in enumerate(axis_vectors)
        ],
    }


def semantic_axis_coverage_trace(context: JsonDict) -> JsonDict:
    coverage = context.get("axis_coverage", {}) or {}
    return {
        "target": round(float(coverage.get("target", 0.0)), 4),
        "items": [
            {
                "text": item.get("text", ""),
                "families": item.get("families", []),
                "best_score": round(float(item.get("best_score", 0.0)), 4),
                "best_slot": item.get("best_slot"),
                "best_entry": item.get("best_entry"),
            }
            for item in coverage.get("items", [])
        ],
    }


def update_axis_coverage(context: JsonDict, slot: str, entry_id: str, vector: Sequence[float]) -> None:
    coverage = context.get("axis_coverage")
    if not coverage or not vector:
        return
    axis_vectors = context.get("axis_vectors", [])
    for item in coverage.get("items", []):
        index = int(item.get("index", -1))
        if index < 0 or index >= len(axis_vectors):
            continue
        score = cosine_similarity(axis_vectors[index].get("vector", []), vector)
        if score > float(item.get("best_score", 0.0)):
            item["best_score"] = score
            item["best_slot"] = slot
            item["best_entry"] = entry_id


def context_axis_families(context: JsonDict) -> Set[str]:
    families: Set[str] = set()
    for axis in context.get("axis_vectors", []):
        families |= set(axis.get("families", []))
    return families


def intent_steering_enabled(context: Optional[JsonDict]) -> bool:
    if not context:
        return False
    return context.get("intent_steering", {}).get("mode") == "auto"


def make_semantic_context(
    data: JsonDict,
    intent: Optional[str],
    selection_mode: str,
    novelty: str,
    filter_strictness: Optional[str] = None,
    semantic_weight: Optional[float] = None,
    semantic_profile: Optional[str] = None,
    semantic_index_path: Optional[str | Path] = None,
    semantic_index: Optional[JsonDict] = None,
    semantic_provider: str = SEMANTIC_PROVIDER,
    semantic_model: str = SEMANTIC_MODEL_ID,
    semantic_dimensions: int = DEFAULT_SEMANTIC_DIMENSIONS,
    gemini_api_key: Optional[str] = None,
    semantic_axis_mode: str = "auto",
    intent_axes: Optional[Sequence[str]] = None,
    intent_steering: Optional[str] = None,
) -> Optional[JsonDict]:
    resolved_filter, resolved_weight, resolved_profile = resolve_semantic_runtime_options(
        selection_mode,
        filter_strictness,
        semantic_weight,
        semantic_profile,
    )
    if selection_mode == "rule":
        return None
    if not intent:
        raise ValueError("--intent is required when --selection-mode is semantic or hybrid")
    resolved_steering = intent_steering or default_intent_steering(selection_mode)
    if resolved_steering not in INTENT_STEERING_MODES:
        raise ValueError(f"Invalid intent_steering '{resolved_steering}'.")
    index = load_semantic_index(
        semantic_index_path,
        data,
        semantic_index,
        semantic_provider,
        semantic_model,
        semantic_dimensions,
    )
    dimensions = int(index.get("embedding_dimensions", semantic_dimensions))
    axis_payload = extract_intent_axes(intent, intent_axes, semantic_axis_mode)
    query_vector = embed_single_semantic_text(
        intent,
        model=semantic_model,
        dimensions=dimensions,
        api_key=gemini_api_key,
    )
    axis_vectors = []
    for item in axis_payload["items"]:
        text = str(item["text"])
        embedding_text = semantic_axis_embedding_text(text)
        families = axis_families_for_text(text) or axis_families_for_text(embedding_text)
        if clean_intent_axis(embedding_text).lower() == clean_intent_axis(intent).lower():
            vector = query_vector
        else:
            vector = embed_single_semantic_text(
                embedding_text,
                model=semantic_model,
                dimensions=dimensions,
                api_key=gemini_api_key,
            )
        axis_vectors.append(
            {
                "text": text,
                "embedding_text": embedding_text,
                "source": item.get("source", axis_payload["source"]),
                "families": families,
                "vector": vector,
            }
        )
    family_set = sorted({family for item in axis_vectors for family in item.get("families", [])})
    return {
        "selection_mode": selection_mode,
        "intent": intent,
        "novelty": novelty,
        "filter_strictness": resolved_filter,
        "semantic_weight": resolved_weight,
        "semantic_profile": resolved_profile,
        "index": index,
        "query_vector": query_vector,
        "semantic_axis_mode": semantic_axis_mode,
        "intent_axes": axis_payload,
        "axis_vectors": axis_vectors,
        "axis_coverage": initial_axis_coverage(axis_vectors, resolved_profile),
        "intent_steering": {
            "mode": resolved_steering,
            "enabled": resolved_steering == "auto",
            "families": family_set,
            "decisions": [],
        },
        "surreal_activation_reason": "not_evaluated",
        "surreal_activation_active": False,
        "slot_scores": [],
        "preset_score": None,
        "picked_vectors": [],
        "hard_rejected_count": 0,
        "hard_rejected": [],
        "soft_out_of_filter_selected_count": 0,
        "dictionary_hash": index.get("dictionary_hash"),
        "semantic_text_recipe": index.get("semantic_text_recipe"),
        "embedding_provider": index.get("provider", SEMANTIC_PROVIDER),
        "embedding_model": index.get("embedding_model", SEMANTIC_MODEL_ID),
        "embedding_dimensions": dimensions,
    }


def semantic_vector(context: JsonDict, key: str) -> List[float]:
    entry = context["index"].get("entries", {}).get(key, {})
    return entry.get("vector", [])


def item_base_weight(item: Entry) -> float:
    try:
        return max(float(item.get("weight", 1)), 0.0)
    except (TypeError, ValueError):
        return 1.0


def preset_filter_match(item: Entry, flt: Optional[JsonDict]) -> Optional[bool]:
    if not flt:
        return None
    return bool(apply_filter([item], flt))


def adult_semantic_tokens(item: Entry) -> Set[str]:
    tokens = entry_tags(item) | entry_kinds(item)
    item_id = str(item.get("id", ""))
    if "adult" in item_id:
        tokens.add("adult")
    if "fetish" in item_id:
        tokens.add("fetish")
    return tokens


def compatible_with_semantic_hard_guards(
    item: Entry,
    preset: JsonDict,
    picked: Dict[str, Entry],
    slot: str,
) -> bool:
    if not compatible_with_facet_guards(item, preset, picked):
        return False
    if not preset_uses_adult_context(preset):
        tokens = adult_semantic_tokens(item)
        if tokens & {"adult", "fetish", "suggestive"}:
            return False
        if slot in {"adult_context", "fetish_styling", "body_framing", "caption_context"}:
            return False
    return True


def semantic_facet_match_score(item: Entry, preset: JsonDict, picked: Dict[str, Entry]) -> float:
    item_facets = facet_tokens(item)
    if not item_facets:
        return 0.0
    context = facet_tokens(preset)
    for entry in picked.values():
        context |= facet_tokens(entry)
    if not context:
        return 0.0
    return len(item_facets & context) / max(len(item_facets), 1)


def semantic_filter_factor(context: JsonDict, filter_match: Optional[bool]) -> float:
    strictness = context.get("filter_strictness", "hard")
    if strictness == "off" or filter_match is None:
        return 1.0
    config = semantic_profile_config(str(context.get("semantic_profile", "balanced")))
    if filter_match:
        return 1.0 + float(config["filter_bonus"])
    return max(0.01, 1.0 - float(config["filter_penalty"]))


def routed_axis_items(context: JsonDict, slot: str) -> List[JsonDict]:
    routed_families = {
        family
        for family, slots in SEMANTIC_AXIS_SLOT_ROUTES.items()
        if slot in slots
    }
    if not routed_families:
        return []
    return [
        axis
        for axis in context.get("axis_vectors", [])
        if routed_families & set(axis.get("families", []))
    ]


def semantic_axis_relevance(vector: Sequence[float], context: JsonDict, slot: str) -> JsonDict:
    axis_vectors = context.get("axis_vectors", [])
    scored_axes = [
        {
            "text": axis.get("text", ""),
            "families": axis.get("families", []),
            "score": cosine_similarity(axis.get("vector", []), vector),
        }
        for axis in axis_vectors
    ]
    axis_max_item = max(scored_axes, key=lambda item: item["score"], default=None)
    routed = [
        item
        for item in scored_axes
        if set(item.get("families", [])) & {
            family for family, slots in SEMANTIC_AXIS_SLOT_ROUTES.items() if slot in slots
        }
    ]
    routed_item = max(routed, key=lambda item: item["score"], default=None)
    return {
        "axis_max": float(axis_max_item["score"]) if axis_max_item else 0.0,
        "axis_max_text": axis_max_item.get("text") if axis_max_item else None,
        "routed_axis_score": float(routed_item["score"]) if routed_item else None,
        "routed_axis": routed_item.get("text") if routed_item else None,
        "routed_families": sorted({family for item in routed for family in item.get("families", [])}),
    }


def semantic_axis_coverage_bonus(vector: Sequence[float], context: JsonDict, slot: str) -> float:
    coverage = context.get("axis_coverage", {}) or {}
    axis_vectors = context.get("axis_vectors", [])
    if not coverage or not axis_vectors:
        return 0.0
    routed = routed_axis_items(context, slot)
    routed_indices = {
        index
        for index, axis in enumerate(axis_vectors)
        if any(axis is routed_axis for routed_axis in routed)
    }
    if not routed_indices:
        routed_indices = set(range(len(axis_vectors)))
    target = max(float(coverage.get("target", 0.68)), 0.01)
    bonuses: List[float] = []
    for item in coverage.get("items", []):
        index = int(item.get("index", -1))
        if index not in routed_indices or index < 0 or index >= len(axis_vectors):
            continue
        current = float(item.get("best_score", 0.0))
        deficit = max(0.0, target - current) / target
        if deficit <= 0:
            continue
        axis_score = max(0.0, cosine_similarity(axis_vectors[index].get("vector", []), vector))
        bonuses.append(deficit * axis_score)
    return sum(bonuses) / len(bonuses) if bonuses else 0.0


def semantic_contextual_affinity(slot: str, vector: Sequence[float], context: JsonDict, picked: Dict[str, Entry]) -> float:
    if slot != "surreal_anchor":
        return 0.0
    context_vectors: List[List[float]] = []
    for context_slot in ("surreal_concept", "location"):
        entry = picked.get(context_slot)
        if entry:
            context_vectors.append(semantic_vector(context, semantic_entry_key("slot", entry, context_slot)))
    if not context_vectors:
        return 0.0
    return max(cosine_similarity(vector, context_vector) for context_vector in context_vectors)


def semantic_candidate_weight(
    item: Entry,
    vector: Sequence[float],
    context: JsonDict,
    preset_vector: Sequence[float],
    preset: JsonDict,
    picked: Dict[str, Entry],
    slot: str,
    filter_match: Optional[bool] = None,
) -> tuple[float, JsonDict]:
    query_score = cosine_similarity(context["query_vector"], vector)
    axis = semantic_axis_relevance(vector, context, slot)
    axis_max = float(axis["axis_max"])
    routed_axis_score = axis.get("routed_axis_score")
    if routed_axis_score is not None:
        effective_query_score = (0.72 * float(routed_axis_score)) + (0.18 * axis_max) + (0.10 * query_score)
    else:
        effective_query_score = max(query_score, (0.65 * axis_max) + (0.35 * query_score))
    coverage_bonus = semantic_axis_coverage_bonus(vector, context, slot)
    contextual_score = semantic_contextual_affinity(slot, vector, context, picked)
    preset_score = cosine_similarity(preset_vector, vector) if preset_vector else 0.0
    facet_score = semantic_facet_match_score(item, preset, picked)
    redundancy = 0.0
    if context.get("picked_vectors"):
        redundancy = max(cosine_similarity(vector, picked) for picked in context["picked_vectors"])
    temperature, novelty_scale = novelty_settings(context["novelty"])
    temperature *= semantic_profile_config(str(context.get("semantic_profile", "balanced")))["temperature_multiplier"]
    novelty_weight = 0.0
    try:
        novelty_weight = float(item.get("novelty_weight", 0.0))
    except (TypeError, ValueError):
        novelty_weight = 0.0

    semantic_weight = float(context.get("semantic_weight", default_semantic_weight(context["selection_mode"])))
    coverage_weight = semantic_profile_float(context, "axis_coverage_weight", 0.22)
    relevance = (
        (0.54 * effective_query_score)
        + (0.18 * query_score)
        + (0.18 * preset_score)
        + (0.10 * facet_score)
        + (coverage_weight * coverage_bonus)
        + (0.12 * contextual_score)
    )
    redundancy_scale = 0.55 if slot in SURREAL_LAYER_SLOTS else 1.0
    mmr_affinity = (semantic_weight * relevance) - ((1.0 - semantic_weight) * redundancy * redundancy_scale)
    affinity = mmr_affinity + (novelty_scale * novelty_weight)
    semantic_multiplier = math.exp(max(min(affinity, 3.0), -3.0) / max(temperature, 0.1))
    base_power = max(0.15, 1.0 - (semantic_weight * 0.85))
    weighted = (max(item_base_weight(item), 0.01) ** base_power) * (semantic_multiplier ** semantic_weight)
    weighted *= semantic_filter_factor(context, filter_match)
    return weighted, {
        "id": item.get("id"),
        "weight": round(weighted, 6),
        "query": round(query_score, 4),
        "effective_query": round(effective_query_score, 4),
        "preset": round(preset_score, 4),
        "facet": round(facet_score, 4),
        "contextual": round(contextual_score, 4),
        "relevance": round(relevance, 4),
        "redundancy": round(redundancy, 4),
        "axis": {
            "axis_max": round(axis_max, 4),
            "axis_max_text": axis.get("axis_max_text"),
            "routed_axis": axis.get("routed_axis"),
            "routed_score": None if routed_axis_score is None else round(float(routed_axis_score), 4),
            "routed_families": axis.get("routed_families", []),
            "coverage_bonus": round(coverage_bonus, 4),
        },
        "filter": "none" if filter_match is None else ("in" if filter_match else "out"),
    }


def semantic_preset_candidate_weight(preset: Entry, score: float, context: JsonDict) -> float:
    temperature, novelty_scale = novelty_settings(context["novelty"])
    temperature *= semantic_profile_config(str(context.get("semantic_profile", "balanced")))["temperature_multiplier"]
    base = max(item_base_weight(preset), 0.01)
    novelty_weight = 0.0
    try:
        novelty_weight = float(preset.get("novelty_weight", 0.0))
    except (TypeError, ValueError):
        novelty_weight = 0.0
    affinity = max(min(score + (novelty_scale * novelty_weight), 3.0), -3.0)
    semantic_weight = float(context.get("semantic_weight", default_semantic_weight(context["selection_mode"])))
    return (base ** 0.35) * (math.exp(affinity / max(temperature * 0.45, 0.1)) ** semantic_weight)


def semantic_preset_score_window(context: JsonDict) -> float:
    base = semantic_profile_config(str(context.get("semantic_profile", "balanced")))["preset_window"]
    novelty = context.get("novelty", "medium")
    if novelty == "low":
        return max(0.04, base * 0.65)
    if novelty == "high":
        return min(0.32, base * 1.35)
    return base


def semantic_preset_candidate_limit(context: JsonDict) -> int:
    config = semantic_profile_config(str(context.get("semantic_profile", "balanced")))
    limit = int(config.get("preset_candidate_limit", 8))
    novelty = context.get("novelty", "medium")
    if novelty == "low":
        return max(3, int(round(limit * 0.7)))
    if novelty == "high":
        return max(limit + 2, int(round(limit * 1.35)))
    return limit


def semantic_preset_weight_floor(context: JsonDict) -> float:
    config = semantic_profile_config(str(context.get("semantic_profile", "balanced")))
    floor = float(config.get("preset_weight_floor", 0.82))
    novelty = context.get("novelty", "medium")
    if novelty == "low":
        return min(0.94, floor + 0.06)
    if novelty == "high":
        return max(0.55, floor - 0.10)
    return floor


def semantic_preset_score_breakdown(vector: Sequence[float], context: JsonDict) -> tuple[float, JsonDict]:
    overall = cosine_similarity(context["query_vector"], vector)
    axis_vectors = context.get("axis_vectors") or [
        {"text": context.get("intent", ""), "source": "full_intent", "vector": context["query_vector"]}
    ]
    axis_scores = [
            {
                "text": item.get("text", ""),
                "embedding_text": item.get("embedding_text", item.get("text", "")),
                "source": item.get("source", "full_intent"),
                "score": cosine_similarity(item.get("vector", []), vector),
            }
        for item in axis_vectors
    ]
    raw_scores = [item["score"] for item in axis_scores]
    axis_mean = sum(raw_scores) / len(raw_scores) if raw_scores else overall
    axis_floor = min(raw_scores) if raw_scores else overall
    config = semantic_profile_config(str(context.get("semantic_profile", "balanced")))
    overall_weight = float(config.get("preset_overall_weight", 0.45))
    axis_mean_weight = float(config.get("preset_axis_mean_weight", 0.35))
    axis_floor_weight = float(config.get("preset_axis_floor_weight", 0.20))
    total = max(overall_weight + axis_mean_weight + axis_floor_weight, 0.01)
    semantic_score = (
        (overall_weight * overall)
        + (axis_mean_weight * axis_mean)
        + (axis_floor_weight * axis_floor)
    ) / total
    return semantic_score, {
        "query": round(overall, 4),
        "overall": round(overall, 4),
        "axis_mean": round(axis_mean, 4),
        "axis_floor": round(axis_floor, 4),
        "axis_scores": [
            {
                "text": item["text"],
                "embedding_text": item["embedding_text"],
                "source": item["source"],
                "score": round(float(item["score"]), 4),
            }
            for item in axis_scores
        ],
        "semantic_score": round(semantic_score, 4),
    }


def semantic_intent_allows_adult_context(context: JsonDict) -> bool:
    axis_text = " ".join(
        str(item.get("text", ""))
        for item in (context.get("intent_axes", {}) or {}).get("items", [])
    )
    text = f"{context.get('intent', '')} {axis_text}".lower()
    adult_terms = {
        "adult",
        "fetish",
        "boudoir",
        "lingerie",
        "sensual",
        "suggestive",
        "성인",
        "페티시",
    }
    return any(term in text for term in adult_terms)


def compatible_preset_with_semantic_hard_guards(preset: Entry, context: JsonDict) -> tuple[bool, Optional[str]]:
    if preset_uses_adult_context(preset) and not semantic_intent_allows_adult_context(context):
        return False, "adult_context"
    tokens = facet_tokens(preset)
    if "safety_tier:adult_only" in tokens and not semantic_intent_allows_adult_context(context):
        return False, "adult_only"
    return True, None


def semantic_slot_score_window(context: JsonDict) -> float:
    base = semantic_profile_config(str(context.get("semantic_profile", "balanced")))["slot_window"]
    novelty = context.get("novelty", "medium")
    if novelty == "low":
        return max(0.04, base * 0.65)
    if novelty == "high":
        return min(0.34, base * 1.35)
    return base


def semantic_slot_candidate_limit(context: JsonDict) -> int:
    config = semantic_profile_config(str(context.get("semantic_profile", "balanced")))
    limit = int(config.get("slot_candidate_limit", 8))
    novelty = context.get("novelty", "medium")
    if novelty == "low":
        return max(3, int(round(limit * 0.7)))
    if novelty == "high":
        return max(limit + 2, int(round(limit * 1.35)))
    return limit


def semantic_slot_weight_floor(context: JsonDict) -> float:
    config = semantic_profile_config(str(context.get("semantic_profile", "balanced")))
    floor = float(config.get("slot_weight_floor", 0.82))
    novelty = context.get("novelty", "medium")
    if novelty == "low":
        return min(0.94, floor + 0.06)
    if novelty == "high":
        return max(0.55, floor - 0.10)
    return floor


def semantic_weighted_choice(
    pool: Sequence[Entry],
    rng: random.Random,
    slot: str,
    preset: JsonDict,
    context: Optional[JsonDict],
    forced: bool = False,
    slot_filter: Optional[JsonDict] = None,
    picked: Optional[Dict[str, Entry]] = None,
) -> Entry:
    if not context or forced:
        return weighted_choice(pool, rng)

    preset_key = semantic_entry_key("preset", preset)
    preset_vector = semantic_vector(context, preset_key)
    weights: List[float] = []
    scored: List[JsonDict] = []
    vectors: Dict[str, List[float]] = {}
    scored_items: List[tuple[Entry, List[float], Optional[bool], float, float, JsonDict]] = []

    for item in pool:
        key = semantic_entry_key("slot", item, slot)
        vector = semantic_vector(context, key)
        vectors[str(item.get("id"))] = vector
        filter_match = preset_filter_match(item, slot_filter)
        weight, summary = semantic_candidate_weight(
            item,
            vector,
            context,
            preset_vector,
            preset,
            picked or {},
            slot,
            filter_match,
        )
        scored_items.append((item, vector, filter_match, weight, float(summary.get("effective_query", summary["query"])), summary))
        scored.append(summary)

    if context.get("filter_strictness") == "soft" and slot_filter:
        best_query = max((query for _, _, _, _, query, _ in scored_items), default=0.0)
        score_window = semantic_slot_score_window(context)
        eligible = [
            row
            for row in scored_items
            if row[2] is not False or row[4] >= best_query - score_window
        ]
    else:
        score_window = None
        eligible = scored_items

    ordered = sorted(eligible, key=lambda row: row[3], reverse=True)
    if ordered:
        best_weight = max(ordered[0][3], 0.01)
        floor = best_weight * semantic_slot_weight_floor(context)
        floored = [row for row in ordered if row[3] >= floor]
        limit = semantic_slot_candidate_limit(context)
        minimum_size = 1 if context.get("filter_strictness") == "soft" and slot_filter else 3
        minimum = min(minimum_size, len(ordered), limit)
        candidates = floored[:limit]
        if len(candidates) < minimum:
            candidates = ordered[:minimum]
    else:
        candidates = []

    for item, _vector, _filter_match, weight, _query, _summary in candidates:
        weights.append(weight)

    if sum(weights) <= 0:
        selected = rng.choice([item for item, *_ in candidates] or list(pool))
    else:
        selected = rng.choices([item for item, *_ in candidates], weights=weights, k=1)[0]

    selected_id = str(selected.get("id"))
    if vectors.get(selected_id):
        context["picked_vectors"].append(vectors[selected_id])
        update_axis_coverage(context, slot, selected_id, vectors[selected_id])
    selected_filter = preset_filter_match(selected, slot_filter)
    if context.get("filter_strictness") == "soft" and selected_filter is False:
        context["soft_out_of_filter_selected_count"] = int(context.get("soft_out_of_filter_selected_count", 0)) + 1
    top_scores = sorted(scored, key=lambda item: item["weight"], reverse=True)[:5]
    context["slot_scores"].append(
        {
            "slot": slot,
            "selected": selected_id,
            "top": top_scores,
            "candidate_count": len(candidates),
            "score_window": score_window,
            "selected_filter": "none" if selected_filter is None else ("in" if selected_filter else "out"),
        }
    )
    return selected


def materialize_virtual_preset(data: JsonDict, preset_id: str) -> Optional[JsonDict]:
    recipe_id = preset_id.removeprefix("virtual:")
    recipe = next((item for item in data.get("recipes", []) if item.get("id") == recipe_id), None)
    if not recipe:
        return None
    base = next((item for item in data.get("presets", []) if item.get("id") == recipe.get("base_preset")), None)
    if not base:
        return None
    preset = dict(base)
    preset["id"] = f"virtual:{recipe_id}"
    preset["ko"] = recipe.get("ko", base.get("ko"))
    preset["en"] = recipe.get("en", base.get("en"))
    preset["weight"] = recipe.get("weight", base.get("weight", 1))
    preset["semantic_anchor"] = recipe.get("semantic_anchor", recipe.get("embedding_text", ""))
    preset["facets"] = recipe.get("facets", {})
    preset["hard_guards"] = recipe.get("hard_guards", {})
    filters = dict(base.get("filters", {}))
    filters.update(recipe.get("filters", {}))
    preset["filters"] = filters
    return preset


def choose_preset(
    data: JsonDict,
    rng: random.Random,
    preset_id: Optional[str] = None,
    semantic_context: Optional[JsonDict] = None,
) -> JsonDict:
    presets = data.get("presets", [])
    if not presets:
        raise ValueError("No presets found in JSON.")

    if preset_id:
        for p in presets:
            if p.get("id") == preset_id:
                return p
        virtual = materialize_virtual_preset(data, preset_id)
        if virtual:
            return virtual
        valid = ", ".join(p.get("id", "?") for p in presets)
        raise ValueError(f"Unknown preset '{preset_id}'. Available presets: {valid}")

    if semantic_context:
        scored_presets: List[tuple[JsonDict, float, float, JsonDict]] = []
        summaries: List[JsonDict] = []
        rejected_by_reason: Dict[str, int] = {}
        for preset in presets:
            allowed, reason = compatible_preset_with_semantic_hard_guards(preset, semantic_context)
            if not allowed:
                rejected_by_reason[str(reason or "hard_guard")] = rejected_by_reason.get(str(reason or "hard_guard"), 0) + 1
                continue
            vector = semantic_vector(semantic_context, semantic_entry_key("preset", preset))
            score, score_summary = semantic_preset_score_breakdown(vector, semantic_context)
            weight = semantic_preset_candidate_weight(preset, score, semantic_context)
            summary = {"id": preset.get("id"), "weight": round(weight, 6), **score_summary}
            scored_presets.append((preset, weight, score, summary))
            summaries.append(summary)
        rejected_count = sum(rejected_by_reason.values())
        if rejected_count:
            semantic_context["hard_rejected_count"] = int(semantic_context.get("hard_rejected_count", 0)) + rejected_count
            semantic_context.setdefault("hard_rejected", []).append(
                {"scope": "preset", "count": rejected_count, "reasons": rejected_by_reason}
            )
        best_score = max((score for _, _, score, _ in scored_presets), default=0.0)
        score_window = semantic_preset_score_window(semantic_context)
        window_candidates = [
            (preset, weight, score, summary)
            for preset, weight, score, summary in scored_presets
            if score >= best_score - score_window
        ]
        limit = semantic_preset_candidate_limit(semantic_context)
        ordered = sorted(window_candidates, key=lambda row: row[2], reverse=True)[:limit]
        if ordered:
            best_weight = max((row[1] for row in ordered), default=0.01)
            floor = best_weight * semantic_preset_weight_floor(semantic_context)
            candidates = [row for row in ordered if row[1] >= floor][:limit]
            minimum = min(3, len(ordered), limit)
            if len(candidates) < minimum:
                candidates = ordered[:minimum]
        else:
            candidates = []
        candidate_presets = [preset for preset, *_ in candidates]
        candidate_weights = [weight for _, weight, *_ in candidates]
        if candidate_presets and sum(candidate_weights) > 0:
            selected = rng.choices(candidate_presets, weights=candidate_weights, k=1)[0]
        else:
            selected = weighted_choice(presets, rng)
        summary_by_id = {str(summary.get("id")): summary for summary in summaries}
        semantic_context["preset_score"] = {
            "selected": selected.get("id"),
            "selected_summary": summary_by_id.get(str(selected.get("id")), {}),
            "intent_axes": semantic_context.get("intent_axes", {}),
            "top": [
                summary
                for _, _, _, summary in sorted(candidates, key=lambda row: row[2], reverse=True)[:5]
            ],
            "candidate_count": len(candidates),
            "window_candidate_count": len(window_candidates),
            "score_window": score_window,
            "preset_candidate_limit": semantic_preset_candidate_limit(semantic_context),
            "preset_weight_floor": semantic_preset_weight_floor(semantic_context),
            "hard_rejected_count": rejected_count,
            "hard_rejected_by_reason": rejected_by_reason,
        }
        return selected

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
    semantic_context: Optional[JsonDict] = None,
    mode_explicit: bool = False,
) -> bool:
    active = False
    reason = "off"
    if has_forced_surreal_slot(forced_choices):
        active = True
        reason = "forced_slot"
    elif mode == "on":
        active = True
        reason = "explicit"
    elif preset_uses_adult_context(preset):
        active = False
        reason = "adult_preset_blocked"
    elif (
        semantic_context
        and intent_steering_enabled(semantic_context)
        and not mode_explicit
        and mode == "off"
        and "fantasy" in context_axis_families(semantic_context)
    ):
        active = True
        reason = "semantic_axis"
    elif mode == "auto":
        active = rng.random() < max(0.0, min(1.0, probability))
        reason = "probability"
    elif mode == "off" and mode_explicit:
        active = False
        reason = "explicit_off"

    if semantic_context is not None:
        semantic_context["surreal_activation_reason"] = reason
        semantic_context["surreal_activation_active"] = active
    return active


def apply_surreal_layer(
    data: JsonDict,
    preset: JsonDict,
    rng: random.Random,
    picked: Dict[str, Entry],
    forced_choices: Optional[Dict[str, List[str]]] = None,
    intensity: str = "moderate",
    semantic_context: Optional[JsonDict] = None,
) -> None:
    for slot in SURREAL_INTENSITY_SLOTS[intensity]:
        if slot in picked:
            continue
        entry = choose_slot(slot, data, preset, rng, picked, forced_choices, semantic_context)
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


def entry_has_human_signal(entry: Entry) -> bool:
    tokens = entry_context_tokens(entry) | facet_tokens(entry)
    return "human" in tokens or "subject_kind:human" in tokens


def entry_has_urban_signal(entry: Entry) -> bool:
    tokens = entry_context_tokens(entry) | facet_tokens(entry)
    entry_id = str(entry.get("id", "")).lower()
    return bool(
        tokens & {"urban", "street", "city", "place_type:urban", "place_type:street"}
        or any(fragment in entry_id for fragment in ("urban", "city", "street", "alley", "subway", "neon"))
    )


def entry_has_horror_signal(entry: Entry) -> bool:
    tokens = entry_context_tokens(entry) | facet_tokens(entry)
    blob = " ".join(
        [
            str(entry.get("id", "")),
            str(entry.get("en", "")),
            str(entry.get("ko", "")),
        ]
    ).lower()
    horror_terms = {
        "horror",
        "fear",
        "nightmare",
        "terror",
        "eerie",
        "uncanny",
        "tense",
        "noir",
        "gothic",
        "dark",
        "suspense",
        "공포",
        "악몽",
    }
    return bool(tokens & horror_terms or any(term in blob for term in horror_terms))


def record_intent_steering(context: JsonDict, decision: JsonDict) -> None:
    steering = context.setdefault("intent_steering", {"mode": "off", "enabled": False, "families": [], "decisions": []})
    decisions = steering.setdefault("decisions", [])
    signature = json.dumps(decision, ensure_ascii=False, sort_keys=True)
    existing = {json.dumps(item, ensure_ascii=False, sort_keys=True) for item in decisions}
    if signature not in existing:
        decisions.append(decision)


def steer_semantic_candidate_pool(
    slot: str,
    pool: Sequence[Entry],
    context: Optional[JsonDict],
) -> List[Entry]:
    if not context or not intent_steering_enabled(context):
        return list(pool)
    families = context_axis_families(context)
    steered: List[Entry] = []
    reason = ""
    if slot == "subject" and "human" in families:
        steered = [item for item in pool if entry_has_human_signal(item)]
        reason = "human_subject"
    elif slot == "location" and "urban" in families:
        steered = [item for item in pool if entry_has_urban_signal(item)]
        reason = "urban_location"
    elif slot == "mood" and "horror" in families:
        steered = [item for item in pool if entry_has_horror_signal(item)]
        reason = "horror_mood"
    if steered:
        record_intent_steering(
            context,
            {
                "slot": slot,
                "reason": reason,
                "before": len(pool),
                "after": len(steered),
            },
        )
        return steered
    return list(pool)


def semantic_steering_slots(context: Optional[JsonDict], data: JsonDict) -> List[str]:
    if not context or not intent_steering_enabled(context):
        return []
    available = set(data.get("slots", {}).keys())
    families = context_axis_families(context)
    wanted: List[str] = []
    if "human" in families and "subject" in available:
        wanted.append("subject")
    if "urban" in families and "location" in available:
        wanted.append("location")
    if "horror" in families and "mood" in available:
        wanted.append("mood")
    return wanted


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
    semantic_context: Optional[JsonDict] = None,
) -> Optional[Entry]:
    slots = data.get("slots", {})
    if slot not in slots:
        raise ValueError(f"Slot '{slot}' is referenced but not defined in JSON.")

    full_pool = list(slots[slot])
    filters = preset.get("filters", {}).get(slot)

    forced_ids = (forced_choices or {}).get(slot)
    forced = bool(forced_ids)
    if forced_ids:
        ids = set(forced_ids)
        forced_pool = [x for x in full_pool if x.get("id") in ids]
        if not forced_pool:
            valid = ", ".join(x.get("id", "?") for x in full_pool[:30])
            raise ValueError(f"Unknown id for slot '{slot}': {forced_ids}. Example valid ids: {valid}")
        pool = forced_pool
    else:
        pool = list(full_pool)

    # If a human-only forced modifier is given, steer subject choice toward human.
    if slot == "subject" and not forced:
        required_kinds = forced_required_subject_kinds(data, forced_choices or {})
        if required_kinds:
            steered = [x for x in pool if entry_kinds(x) & required_kinds]
            if steered:
                pool = steered

    if semantic_context and not forced:
        pool = steer_semantic_candidate_pool(slot, pool, semantic_context)

    if semantic_context and not forced:
        before_hard = len(pool)
        pool = [item for item in pool if compatible_with_semantic_hard_guards(item, preset, picked, slot)]
        rejected = before_hard - len(pool)
        if rejected > 0:
            semantic_context["hard_rejected_count"] = int(semantic_context.get("hard_rejected_count", 0)) + rejected
            semantic_context.setdefault("hard_rejected", []).append({"slot": slot, "count": rejected})

    if not semantic_context or forced or semantic_context.get("filter_strictness") == "hard":
        filtered = apply_filter(pool, filters)
        if filtered:
            pool = filtered

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

    return semantic_weighted_choice(
        pool,
        rng,
        slot,
        preset,
        semantic_context,
        forced=forced,
        slot_filter=filters,
        picked=picked,
    )


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
    semantic_context: Optional[JsonDict] = None,
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

        entry = choose_slot(slot, data, preset, rng, picked, forced_choices, semantic_context)
        if entry is not None:
            picked[slot] = entry


def build_fields(picked: Dict[str, Entry], lang: str) -> Dict[str, str]:
    values = {slot: localize(entry, lang) for slot, entry in picked.items()}

    subject = values.get("subject", "")
    action = values.get("action", "")
    hair = values.get("hair_style", "")
    makeup = values.get("makeup_style", "")
    expression = values.get("expression", "")
    facial_hair = values.get("facial_hair", "")
    accessory = values.get("wearable_accessory", "")
    wardrobe = values.get("wardrobe_style", "")
    costume = values.get("costume_style", "")

    if lang == "ko":
        subject_mods = [values[s] for s in ("person_origin", "appearance_type") if values.get(s)]
        if hair:
            subject_mods.append(hair)
        if facial_hair:
            subject_mods.append(facial_hair + "의")
        if makeup:
            subject_mods.append(makeup)
        if expression:
            subject_mods.append(expression + "의")
        if accessory:
            subject_mods.append(accessory + josa(accessory, "을", "를") + " 착용한")
        if wardrobe:
            subject_mods.append(wardrobe + josa(wardrobe, "을", "를") + " 입은")
        if costume:
            subject_mods.append(costume + josa(costume, "을", "를") + " 입은")
        subject_with_mods = clean_spaces(" ".join(subject_mods + ([subject] if subject else [])))
        subject_phrase = clean_spaces(f"{action} {subject_with_mods}")
        object_phrase = subject_phrase + josa(subject_phrase, "을", "를") if subject_phrase else ""
    else:
        subject_suffixes = [values[s] for s in ("person_origin", "appearance_type") if values.get(s)]
        if hair:
            subject_suffixes.append(f"with {hair}")
        if facial_hair:
            subject_suffixes.append(f"with {facial_hair}")
        if makeup:
            subject_suffixes.append(f"with {makeup}")
        if expression:
            subject_suffixes.append(f"with {expression}")
        if accessory:
            subject_suffixes.append(f"wearing {accessory}")
        if wardrobe:
            subject_suffixes.append(f"wearing {wardrobe}")
        if costume:
            subject_suffixes.append(f"wearing {costume}")
        subject_with_mods = clean_spaces(" ".join(([subject] if subject else []) + subject_suffixes))
        subject_phrase = clean_spaces(f"{subject_with_mods} {action}")
        object_phrase = subject_phrase

    location_entry = picked.get("location")
    if location_entry and lang == "ko":
        location_phrase = location_entry.get("phrase_ko") or (localize(location_entry, "ko") + "에서")
    elif location_entry:
        raw_location = localize(location_entry, "en")
        location_phrase = location_entry.get("phrase_en") or (
            raw_location
            if raw_location.lower().startswith(("in ", "inside ", "at ", "on ", "beside ", "near ", "under "))
            else "in " + raw_location
        )
    else:
        location_phrase = ""

    lighting_slots = ("lighting", "light_direction", "light_type", "light_intensity", "light_shape")
    camera_slots = (
        "camera_type",
        "camera_direction",
        "composition",
        "subject_framing",
        "body_framing",
        "lens",
        "focus",
        "motion",
    )
    style_slots = (
        "world",
        "aesthetic_trend",
        "film_emulation",
        "color",
        "mood",
        "surreal_concept",
        "surreal_anchor",
        "scale_relation",
        "surreal_physics_detail",
        "adult_context",
        "caption_context",
    )
    detail_slots = (
        "wearable_accessory",
        "facial_hair",
        "wardrobe_style",
        "makeup_style",
        "costume_style",
        "fetish_styling",
        "surface_material",
        "texture",
        "format",
        "quality",
    )

    lighting_parts = [values[s] for s in lighting_slots if values.get(s)]
    camera_parts = [values[s] for s in camera_slots if values.get(s)]

    if lang == "ko":
        technique_chunks = []
        if camera_parts:
            technique_chunks.append("카메라는 " + ", ".join(camera_parts))
        if lighting_parts:
            technique_chunks.append("조명은 " + ", ".join(lighting_parts))
        technique_sentence = ensure_period("; ".join(technique_chunks)) if technique_chunks else ""

        style_parts = [values[s] for s in style_slots if values.get(s)]
        style_sentence = ensure_period("전체 분위기는 " + ", ".join(style_parts)) if style_parts else ""

        detail_parts = [values[s] for s in detail_slots if values.get(s)]
        detail_sentence = ensure_period("디테일은 " + ", ".join(detail_parts)) if detail_parts else ""
    else:
        technique_chunks = []
        if camera_parts:
            technique_chunks.append("Camera: " + ", ".join(camera_parts))
        if lighting_parts:
            technique_chunks.append("Lighting: " + ", ".join(lighting_parts))
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


PROMPT_SECTION_ORDER = (
    "intent",
    "subject",
    "action",
    "scene",
    "camera",
    "lighting",
    "palette_mood",
    "finish",
    "special_layers",
    "constraints",
)


def inline_constraints(lang: str) -> List[str]:
    if lang == "ko":
        return ["텍스트와 워터마크 없음"]
    return ["no text or watermark"]


def dedupe_parts(parts: Sequence[str]) -> List[str]:
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
    return unique


def build_prompt_sections(
    data: JsonDict,
    preset: JsonDict,
    picked: Dict[str, Entry],
    lang: str,
    reference_edit_mode: str = "off",
    trend_layer: str = "off",
) -> Dict[str, List[str]]:
    fields = build_fields(picked, lang)
    values = {slot: localize(entry, lang) for slot, entry in picked.items()}

    def selected(slots: Sequence[str]) -> List[str]:
        return [values[slot] for slot in slots if values.get(slot)]

    sections: Dict[str, List[str]] = {section: [] for section in PROMPT_SECTION_ORDER}
    sections["intent"] = selected(("medium", "genre", "format", "quality"))
    sections["subject"] = [
        fields.get("subject_with_mods") or values.get("subject", "")
    ]
    sections["action"] = selected(("action", "prop"))
    sections["scene"] = [
        fields.get("location_phrase") or values.get("location", ""),
        values.get("time_of_day", ""),
        values.get("weather", ""),
        values.get("surface_material", ""),
        values.get("world", ""),
    ]
    sections["camera"] = selected(
        (
            "camera_type",
            "camera_direction",
            "composition",
            "subject_framing",
            "body_framing",
            "lens",
            "focus",
            "motion",
        )
    )
    sections["lighting"] = selected(
        ("lighting", "light_direction", "light_type", "light_intensity", "light_shape")
    )
    sections["palette_mood"] = selected(("color", "mood", "adult_context", "caption_context"))
    sections["finish"] = selected(
        (
            "film_emulation",
            "aesthetic_trend",
            "wearable_accessory",
            "facial_hair",
            "wardrobe_style",
            "makeup_style",
            "costume_style",
            "fetish_styling",
            "surface_material",
            "texture",
            "format",
            "quality",
        )
    )
    sections["special_layers"] = dedupe_parts(
        [
            render_surreal_layer_detail(picked, lang),
            render_reference_edit_detail(reference_edit_mode, lang),
            render_trend_layer_detail(trend_layer, lang),
        ]
    )
    sections["constraints"] = inline_constraints(lang)
    return {section: dedupe_parts(parts) for section, parts in sections.items()}


def section_text(sections: Dict[str, List[str]], section: str, fallback: str = "") -> str:
    return unique_join(sections.get(section, [])) or fallback


def section_ordered_standard_templates(templates: Sequence[str]) -> List[str]:
    ordered: List[str] = []
    for template in templates:
        subject_positions = [
            pos for pos in (template.find("{subject_phrase}"), template.find("{object_phrase}")) if pos >= 0
        ]
        location_positions = [
            pos for pos in (template.find("{location_phrase}"), template.find("{location}")) if pos >= 0
        ]
        if subject_positions and location_positions and min(subject_positions) < min(location_positions):
            ordered.append(template)
    return ordered


def ensure_standard_section_order(
    prompt: str,
    sections: Dict[str, List[str]],
    fields: Dict[str, str],
    lang: str,
) -> str:
    scene_markers = dedupe_parts(
        list(sections.get("scene", []))
        + [
            fields.get("location_phrase", ""),
            fields.get("location", ""),
        ]
    )
    subject_markers = [
        part
        for part in (
            fields.get("subject_phrase", ""),
            fields.get("object_phrase", ""),
            section_text(sections, "subject"),
        )
        if part
    ]

    subject_positions = [prompt.find(marker) for marker in subject_markers if prompt.find(marker) >= 0]
    scene_positions = [prompt.find(marker) for marker in scene_markers if prompt.find(marker) >= 0]
    if not subject_positions or not scene_positions or min(subject_positions) < min(scene_positions):
        return prompt

    subject = fields.get("subject", "") or section_text(sections, "subject")
    if not subject:
        return prompt
    prefix = ("중심 피사체: " if lang == "ko" else "Subject: ") + subject
    return clean_spaces(f"{ensure_period(prefix)} {prompt}")


def render_detailed_prompt(
    data: JsonDict,
    preset: JsonDict,
    picked: Dict[str, Entry],
    lang: str,
    sections: Dict[str, List[str]],
) -> str:
    fields = build_fields(picked, lang)
    values = {slot: localize(entry, lang) for slot, entry in picked.items()}
    category = subject_category(picked)

    if lang == "ko":
        subject = section_text(sections, "subject", values.get("subject", "중심 피사체"))
        action = section_text(sections, "action")
        subject_state = f"{subject}; 동작과 소품: {action}" if action else subject
        location = section_text(sections, "scene", values.get("location", "구체적인 장소"))
        camera = section_text(sections, "camera", "명확한 카메라 위치, 의도적인 구도, 사실적인 초점")
        lighting = section_text(sections, "lighting", "자연스럽고 설득력 있는 사진 조명")
        mood = section_text(sections, "palette_mood", "일관된 색감, 분위기, 세계관 맥락")
        finish = section_text(sections, "finish", "정확한 소재 디테일을 가진 이미지 생성용 마감")
        special = " ".join(sections.get("special_layers", []))
        constraints = section_text(sections, "constraints")
        genre = values.get("genre", "사진")
        medium = values.get("medium", "실사 사진")
        subject_guidance = render_subject_guidance(category, lang)
        scene_guidance = render_scene_guidance(category, lang)
        finish_guidance = render_finish_guidance(category, lang)
        prompt = " ".join(
            part
            for part in [
                f"{medium}로 렌더링할 {genre}. "
                f"중심 피사체와 상태: {subject_state}; {subject_guidance}. "
                f"장면과 장소: {location}; {scene_guidance}. "
                f"카메라와 구도: {camera}; 피사체 크기, 프레임 가장자리, 원근감, 초점 위치, 움직임 처리를 명확히 한다. "
                f"조명: {lighting}; 그림자 방향, 하이라이트, 반사광, 노출 균형, 대기감을 실제 촬영처럼 보이게 한다. "
                f"색감과 분위기: {mood}; 색 대비, 감정 톤, 세계관 맥락이 피사체와 장소에 맞아야 한다. ",
                special,
                f"질감과 마감: {finish}; {finish_guidance}. "
                f"제약: {constraints}. "
                "이미지 생성 시 요구사항을 빠뜨리지 말고, 막연한 스타일 요약보다 구체적인 사진 결과를 우선한다.",
            ]
            if part
        )
    else:
        subject = section_text(sections, "subject", values.get("subject", "the main subject"))
        action = section_text(sections, "action")
        subject_state = f"{subject}; action and prop: {action}" if action else subject
        location = section_text(sections, "scene", values.get("location", "a specific location"))
        camera = section_text(sections, "camera", "clear camera placement, deliberate composition, realistic focus")
        lighting = section_text(sections, "lighting", "natural, believable photographic light")
        mood = section_text(sections, "palette_mood", "coherent color, mood, and world context")
        finish = section_text(sections, "finish", "photo-ready finish with accurate material detail")
        special = " ".join(sections.get("special_layers", []))
        constraints = section_text(sections, "constraints")
        genre = values.get("genre", "photography")
        medium = values.get("medium", "photograph")
        subject_guidance = render_subject_guidance(category, lang)
        scene_guidance = render_scene_guidance(category, lang)
        finish_guidance = render_finish_guidance(category, lang)
        prompt = " ".join(
            part
            for part in [
                f"Create {with_indefinite_article(medium)} in the style of {genre}. "
                f"Subject and state: {subject_state}; {subject_guidance}. "
                f"Scene and location: {location}; {scene_guidance}. "
                f"Camera and composition: {camera}; define subject scale, frame edges, perspective, focus behavior, and any motion treatment clearly. "
                f"Lighting: {lighting}; make shadow direction, highlights, reflected light, exposure balance, and atmosphere feel like a real photographic capture. "
                f"Color and mood: {mood}; keep the palette, emotional tone, and world context coherent with the subject and setting. ",
                special,
                f"Texture, format, and finish: {finish}; {finish_guidance}. "
                f"Constraints: {constraints}. "
                "Prioritize a specific, image-ready photographic result over a vague style summary.",
            ]
            if part
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


def render_compact_prompt(
    data: JsonDict,
    preset: JsonDict,
    picked: Dict[str, Entry],
    lang: str,
    sections: Dict[str, List[str]],
) -> str:
    values = {slot: localize(entry, lang) for slot, entry in picked.items()}
    category = subject_category(picked)

    def render_with_drops(drop_sections: Set[str]) -> str:
        content_parts: List[str] = []
        for section in ("action", "scene", "camera", "lighting", "palette_mood", "finish", "special_layers"):
            if section in drop_sections:
                continue
            if section == "scene" and "world" in drop_sections:
                content = unique_join(sections.get("scene", [])[:1])
            else:
                content = section_text(sections, section)
            if content:
                content_parts.append(content)
        if category == "human" and "finish" not in drop_sections:
            content_parts.append("자연스러운 피부 질감" if lang == "ko" else "natural skin texture")
        constraints = section_text(sections, "constraints")
        if constraints:
            content_parts.append(constraints)

        subject = section_text(sections, "subject", "중심 피사체" if lang == "ko" else "the main subject")
        if lang == "ko":
            lead = unique_join(
                ["초사실적", values.get("format", ""), values.get("genre", ""), values.get("medium", "실사 사진")],
                " ",
            )
            return ensure_period(f"{lead}, {subject}, {unique_join(content_parts)}")

        lead = unique_join(
            ["Ultra-realistic", values.get("format", ""), values.get("genre", ""), values.get("medium", "photograph")],
            " ",
        )
        return ensure_period(f"{lead} of {subject}, {unique_join(content_parts)}")

    drop_sections: Set[str] = set()
    prompt = render_with_drops(drop_sections)
    for section in ("palette_mood", "finish", "caption_context", "world"):
        if lang != "en" or len(prompt.split()) <= 140:
            break
        drop_sections.add(section)
        prompt = render_with_drops(drop_sections)
    return clean_spaces(prompt)


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
    sections = build_prompt_sections(data, preset, picked, lang, reference_edit_mode, trend_layer)

    if detail_level == "detailed":
        return render_detailed_prompt(data, preset, picked, lang, sections)

    if detail_level == "compact":
        return render_compact_prompt(data, preset, picked, lang, sections)

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

    ordered_templates = section_ordered_standard_templates(templates)
    template = rng.choice(ordered_templates or templates)
    fields = build_fields(picked, lang)
    prompt = template.format(**fields)
    prompt = ensure_standard_section_order(prompt, sections, fields, lang)

    additions: List[str] = []
    action = section_text(sections, "action")
    if action and any(part.lower() not in prompt.lower() for part in sections.get("action", [])):
        additions.append(("동작과 소품: " if lang == "ko" else "Action and prop: ") + action)
    for special in sections.get("special_layers", []):
        if special and special.lower() not in prompt.lower():
            additions.append(special)
    constraints = section_text(sections, "constraints")
    if constraints and constraints.lower() not in prompt.lower():
        additions.append(("제약: " if lang == "ko" else "Constraints: ") + constraints)

    if additions:
        prompt = clean_spaces(" ".join([prompt] + [ensure_period(part) for part in additions]))
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
    intent: Optional[str] = None,
    selection_mode: str = "rule",
    novelty: str = "medium",
    filter_strictness: Optional[str] = None,
    semantic_weight: Optional[float] = None,
    semantic_profile: Optional[str] = None,
    include_trace: bool = False,
    llm_polish: str = "off",
    semantic_index_path: Optional[str | Path] = None,
    semantic_index: Optional[JsonDict] = None,
    semantic_provider: str = SEMANTIC_PROVIDER,
    semantic_model: str = SEMANTIC_MODEL_ID,
    semantic_dimensions: int = DEFAULT_SEMANTIC_DIMENSIONS,
    gemini_api_key: Optional[str] = None,
    semantic_axis_mode: str = "auto",
    intent_axes: Optional[Sequence[str]] = None,
    intent_steering: Optional[str] = None,
    surreal_mode_explicit: bool = False,
) -> JsonDict:
    if intent and selection_mode == "rule":
        raise ValueError("--intent cannot be used with --selection-mode rule")
    semantic_context = make_semantic_context(
        data,
        intent,
        selection_mode,
        novelty,
        filter_strictness,
        semantic_weight,
        semantic_profile,
        semantic_index_path,
        semantic_index,
        semantic_provider,
        semantic_model,
        semantic_dimensions,
        gemini_api_key,
        semantic_axis_mode,
        intent_axes,
        intent_steering,
    )
    preset = choose_preset(data, rng, preset_id, semantic_context)
    picked: Dict[str, Entry] = {}

    slots_to_pick = selected_slots_for_preset(preset, data, rng, forced_choices, priority_bias)
    for slot in semantic_steering_slots(semantic_context, data):
        if slot not in slots_to_pick:
            slots_to_pick.append(slot)
            if semantic_context:
                record_intent_steering(
                    semantic_context,
                    {"slot": slot, "reason": "required_by_axis", "before": len(slots_to_pick) - 1, "after": len(slots_to_pick)},
                )

    for slot in slots_to_pick:
        entry = choose_slot(slot, data, preset, rng, picked, forced_choices, semantic_context)
        if entry is not None:
            picked[slot] = entry

    if should_activate_surreal_layer(
        preset,
        rng,
        surreal_mode,
        surreal_probability,
        forced_choices,
        semantic_context,
        surreal_mode_explicit,
    ):
        apply_surreal_layer(data, preset, rng, picked, forced_choices, surreal_intensity, semantic_context)

    if detail_level == "detailed":
        reinforce_detail_slots(data, preset, rng, picked, forced_choices, semantic_context)

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

    if llm_polish == "strict":
        for lang in langs:
            result[f"polished_prompt_{lang}"] = result[f"prompt_{lang}"]
        result["rewrite_trace"] = {
            "mode": "strict",
            "status": "preserved",
            "provider": "none",
            "fallback": False,
            "preserved_anchors": [
                f"{slot}:{entry.get('id')}"
                for slot, entry in picked.items()
                if entry.get("anchor") or slot in {"subject", "location", "lens", "lighting", "format"}
            ],
        }

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

    if include_trace and semantic_context:
        result["semantic_trace"] = {
            "selection_mode": selection_mode,
            "intent": intent,
            "novelty": novelty,
            "filter_strictness": semantic_context.get("filter_strictness"),
            "semantic_weight": semantic_context.get("semantic_weight"),
            "semantic_profile": semantic_context.get("semantic_profile"),
            "semantic_axis_mode": semantic_context.get("semantic_axis_mode"),
            "intent_axes": semantic_context.get("intent_axes"),
            "intent_steering": semantic_context.get("intent_steering"),
            "axis_coverage": semantic_axis_coverage_trace(semantic_context),
            "surreal_activation_reason": semantic_context.get("surreal_activation_reason"),
            "surreal_activation_active": semantic_context.get("surreal_activation_active"),
            "dictionary_hash": semantic_context.get("dictionary_hash"),
            "semantic_text_recipe": semantic_context.get("semantic_text_recipe"),
            "embedding_provider": semantic_context.get("embedding_provider"),
            "embedding_model": semantic_context.get("embedding_model"),
            "embedding_dimensions": semantic_context.get("embedding_dimensions"),
            "hard_rejected_count": semantic_context.get("hard_rejected_count", 0),
            "hard_rejected": semantic_context.get("hard_rejected", []),
            "soft_out_of_filter_selected_count": semantic_context.get("soft_out_of_filter_selected_count", 0),
            "preset_score": semantic_context.get("preset_score"),
            "slot_scores": semantic_context.get("slot_scores", []),
        }
    elif include_trace:
        result["semantic_trace"] = {
            "selection_mode": selection_mode,
            "intent": intent,
            "novelty": novelty,
            "filter_strictness": filter_strictness,
            "semantic_weight": semantic_weight,
            "semantic_profile": semantic_profile,
            "semantic_axis_mode": semantic_axis_mode,
            "intent_axes": {"mode": semantic_axis_mode, "source": "none", "items": []},
            "intent_steering": {"mode": intent_steering or "off", "enabled": False, "families": [], "decisions": []},
            "axis_coverage": {"target": 0.0, "items": []},
            "surreal_activation_reason": "none",
            "surreal_activation_active": False,
            "slot_scores": [],
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


def list_presets(data: JsonDict, include_virtual: bool = False) -> None:
    for p in data.get("presets", []):
        ko = localize(p, "ko")
        en = localize(p, "en")
        print(f"{p.get('id')}: {ko} / {en}")
    if include_virtual:
        for recipe in data.get("recipes", []):
            ko = localize(recipe, "ko")
            en = localize(recipe, "en")
            print(f"virtual:{recipe.get('id')}: {ko} / {en}")


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
    raw_args = list(argv or sys.argv[1:])
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
    parser.add_argument("--intent", default=None, help="Free-text visual intent for semantic selection. A broad photo intent is used when semantic/hybrid mode has no explicit intent.")
    parser.add_argument("--selection-mode", choices=SELECTION_MODES, default=DEFAULT_SELECTION_MODE, help="Selection mode. semantic is the default; use rule for the original deterministic weighted path.")
    parser.add_argument("--novelty", choices=NOVELTY_LEVELS, default="medium", help="Semantic sampling diversity level. Used only with semantic or hybrid selection.")
    parser.add_argument("--filter-strictness", choices=FILTER_STRICTNESS_MODES, default=None, help="Preset filter behavior for semantic/hybrid selection. Defaults to soft for semantic and hard for hybrid/rule.")
    parser.add_argument("--semantic-weight", type=float, default=None, help="0..1 blend weight for semantic scoring. Defaults by selection mode.")
    parser.add_argument("--semantic-profile", choices=SEMANTIC_PROFILES, default=None, help="Semantic candidate window/profile. Defaults by selection mode.")
    parser.add_argument("--semantic-axis-mode", choices=SEMANTIC_AXIS_MODES, default="auto", help="Intent-axis decomposition for semantic preset scoring. Use off to keep a single intent axis.")
    parser.add_argument("--intent-axis", dest="intent_axes", action="append", default=[], help="Explicit semantic intent axis. Repeat to replace automatic axis extraction.")
    parser.add_argument("--intent-steering", choices=INTENT_STEERING_MODES, default=None, help="Semantic axis-based slot steering. Defaults to auto for semantic/hybrid and off for rule.")
    parser.add_argument("--semantic-index", default=None, help="Path to a precomputed semantic index JSON. Defaults to a sibling asset when present.")
    parser.add_argument("--semantic-model", default=SEMANTIC_MODEL_ID, help="Gemini embedding model required by the semantic index.")
    parser.add_argument("--semantic-dimensions", type=int, default=DEFAULT_SEMANTIC_DIMENSIONS, help="Gemini embedding dimensions required by the semantic index.")
    parser.add_argument("--include-trace", action="store_true", help="Include semantic/rewrite trace metadata in JSON output.")
    parser.add_argument("--llm-polish", choices=LLM_POLISH_MODES, default="off", help="Optional strict prompt polish contract. strict currently preserves the deterministic prompt unless a provider is wired explicitly.")
    parser.add_argument("--priority-bias", type=float, default=None, help="Optional-slot priority boost. Omit to use JSON setting.")
    parser.add_argument("--set", dest="set_values", action="append", default=[], help="Force a slot id, e.g. --set subject=fashion_model. Repeatable. Use commas to randomly choose among ids.")
    parser.add_argument("--set-json", default=None, help="Inline JSON or path to JSON file for forced slots, e.g. '{\"subject\":\"fashion_model\"}'.")
    parser.add_argument("--include-negative", action="store_true", help="Also output a negative prompt.")
    parser.add_argument("--negative-count", type=int, default=12, help="Number of negative tags to sample.")
    parser.add_argument("--include-choices", action="store_true", help="Include chosen slot details in plain or JSON output.")
    parser.add_argument("--json-output", action="store_true", help="Print results as JSON.")
    parser.add_argument("--list-presets", action="store_true", help="List preset ids and exit.")
    parser.add_argument("--include-virtual", action="store_true", help="Include virtual recipe presets when listing presets.")
    parser.add_argument("--show-slots", action="store_true", help="List slots, tag counts, and priorities then exit.")
    parser.add_argument("--list-tags", metavar="SLOT", help="List tag ids for a slot then exit.")
    args = parser.parse_args(raw_args)

    data = load_json(args.tags)

    if args.list_presets:
        list_presets(data, args.include_virtual)
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

    selection_mode = args.selection_mode
    resolved_intent = args.intent
    if args.intent and selection_mode == "rule":
        raise ValueError("--intent cannot be used with --selection-mode rule")
    if selection_mode != "rule" and not resolved_intent:
        resolved_intent = DEFAULT_SEMANTIC_INTENT
    filter_strictness, semantic_weight, semantic_profile = resolve_semantic_runtime_options(
        selection_mode,
        args.filter_strictness,
        args.semantic_weight,
        args.semantic_profile,
    )

    semantic_index_path = args.semantic_index
    if selection_mode != "rule" and semantic_index_path is None:
        candidate = Path(args.tags).resolve().with_name("photo_prompt_semantic_index.json")
        if candidate.exists():
            semantic_index_path = str(candidate)

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
            intent=resolved_intent,
            selection_mode=selection_mode,
            novelty=args.novelty,
            filter_strictness=filter_strictness,
            semantic_weight=semantic_weight,
            semantic_profile=semantic_profile,
            semantic_axis_mode=args.semantic_axis_mode,
            intent_axes=args.intent_axes,
            intent_steering=args.intent_steering,
            surreal_mode_explicit=has_cli_option(raw_args, "--surreal-mode"),
            include_trace=args.include_trace,
            llm_polish=args.llm_polish,
            semantic_index_path=semantic_index_path,
            semantic_model=args.semantic_model,
            semantic_dimensions=args.semantic_dimensions,
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
