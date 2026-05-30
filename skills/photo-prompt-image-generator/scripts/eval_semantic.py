#!/usr/bin/env python3
"""Evaluate rule, hybrid, and semantic photo-prompt selection against golden intents."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
import os
import random
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence

from prompt_generator import (
    DEFAULT_SEMANTIC_DIMENSIONS,
    SEMANTIC_MODEL_ID,
    SEMANTIC_TEXT_RECIPE_VERSION,
    build_semantic_index_payload,
    coherence_rules_from_source,
    entry_axis_signals,
    entry_conflicts_with_family,
    entry_location_tones,
    entry_semantic_groups,
    family_signal_strength,
    generate_once,
    load_json,
    make_batch_context,
    preset_family_signal_strength,
    semantic_metadata_from_source,
    set_batch_index,
    subject_category,
    validate_semantic_index_metadata,
)


JsonDict = Dict[str, Any]

DEFAULT_TAGS = Path(__file__).resolve().parents[1] / "assets" / "photo_prompt_tags.json"
DEFAULT_INDEX = Path(__file__).resolve().parents[1] / "assets" / "photo_prompt_semantic_index.json"
PROJECT_ROOT = Path(__file__).resolve().parents[1].parents[1]

GOLDEN_CASES: List[JsonDict] = [
    {"intent": "rainy neon night street portrait", "required": {"location": ["rainy_neon_alley", "hong_kong_neon_alley"], "mood": ["tense", "uncanny", "local_night_candid"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "cinestill neon diner portrait", "required": {"film_emulation": ["cinestill_800t_halation"], "location": ["retro_diner_booth", "hong_kong_neon_alley"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "quiet luxury founder profile", "required": {"aesthetic_trend": ["quiet_luxury_aesthetic"], "subject": ["office_worker", "influencer_creator", "fashion_model"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "product flat lay ingredient story", "required": {"surface_material": ["white_marble_surface", "linen_fabric_surface", "dark_walnut_table"], "genre": ["product", "commercial"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "glassblower workshop documentary", "required": {"subject": ["glassblower_artisan"], "location": ["glassblowing_workshop"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "foggy liminal hotel corridor portrait", "required": {"location": ["hotel_corridor_liminal", "luxury_hotel_corridor"], "weather": ["dense_fog_bank", "post_rain_mist"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "botanical greenhouse editorial portrait", "required": {"location": ["botanical_greenhouse", "rooftop_greenhouse"], "genre": ["portrait", "fashion"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "rainy bus stop noir portrait", "required": {"location": ["rainy_bus_stop_shelter", "seoul_bus_stop_snow"], "mood": ["reportage_tense_noir", "melancholic"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "jewelry macro reflection", "required": {"subject": ["silver_ring_jewelry"], "lens": ["105mm_macro", "macro_100mm"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "creator desk setup flatlay", "required": {"location": ["creator_desk_setup"], "surface_material": ["dark_walnut_table", "matte_concrete_surface"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "cinematic blue hour street", "required": {"time_of_day": ["time_blue_hour", "civil_twilight"], "lighting": ["blue_hour"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "night laundromat candid", "required": {"location": ["laundromat_night"], "mood": ["local_night_candid", "melancholic"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "aquarium tunnel portrait", "required": {"location": ["aquarium_tunnel"], "lighting": ["underwater_caustics", "blue_hour"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "coquette cafe portrait", "required": {"aesthetic_trend": ["coquette_aesthetic"], "location": ["retro_diner_booth", "cafe_window"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "balletcore rehearsal room", "required": {"aesthetic_trend": ["balletcore_aesthetic"], "location": ["ballet_rehearsal_studio"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "gorpcore mountain lifestyle", "required": {"aesthetic_trend": ["gorpcore_aesthetic"], "weather": ["morning_frost", "windblown_snow", "dense_fog_bank"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "analog personal brand portrait", "required": {"film_emulation": ["kodak_portra_400_look", "kodak_gold_200_look"], "aesthetic_trend": ["analog_human_story"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "film wedding afterparty flash", "required": {"location": ["wedding_reception_afterparty"], "lighting": ["hard_flash"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "skincare bathroom countertop", "required": {"location": ["bathroom_countertop"], "surface_material": ["white_marble_surface", "subway_tile_wall"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "cinematic product reflection stage", "required": {"surface_material": ["black_acrylic_reflective_surface", "translucent_glass_block"], "genre": ["product", "commercial"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "Hong Kong neon alley with light drizzle", "required": {"location": ["hong_kong_neon_alley"], "weather": ["light_drizzle"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "ceramics studio craft documentary", "required": {"subject": ["ceramic_potter"], "location": ["ceramics_studio"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "vinyl record player on desk analog mood", "required": {"subject": ["vinyl_record_player"], "prop": ["vinyl_record", "analog_cassette"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "transparent umbrella rainy street portrait", "required": {"prop": ["transparent_dome_umbrella", "clear_umbrella"], "weather": ["light_drizzle", "heavy_downpour"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "pre dawn empty street portrait", "required": {"time_of_day": ["pre_dawn_empty_street"], "location": ["rainy_neon_alley", "subway_platform", "hong_kong_neon_alley"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "classic black and white street portrait", "required": {"film_emulation": ["kodak_tri_x_400_bw", "ilford_hp5_bw"], "genre": ["street", "portrait"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "compact CCD digicam party snapshot", "required": {"film_emulation": ["compact_ccd_digicam"], "camera_type": ["compact_digital_camera", "digicam_2000s_camera"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "dense fog bank rural gas station", "required": {"weather": ["dense_fog_bank"], "location": ["rural_gas_station"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "office siren corporate editorial", "required": {"aesthetic_trend": ["office_siren_aesthetic"], "genre": ["fashion", "portrait"]}, "forbidden_tags": ["adult", "fetish"]},
    {"intent": "street food tteokbokki night stall", "required": {"subject": ["street_food_tteokbokki"], "location": ["street_food_stall", "pojangmacha_tent_night"]}, "forbidden_tags": ["adult", "fetish"]},
]

OPEN_ENDED_INTENTS = [
    "urban horror fantasy human portrait",
    "surreal rainy city fashion editorial",
    "quiet documentary craftsperson in atmospheric workshop",
    "imperfect analog night portrait",
    "commercial product hero with tactile surface",
    "liminal transport night portrait",
    "cinematic weather mood portrait",
    "creator branding portrait with desk accessories",
    "retro flash social snapshot",
    "blue hour street narrative photograph",
]

MULTI_AXIS_PRESET_GUARDS: List[JsonDict] = [
    {
        "intent": "urban, horror, fantasy, human portrait",
        "blacklisted_presets": ["aerial_city_drone", "kpop_album_cover_y2k_glossy"],
    }
]

MULTI_AXIS_COVERAGE_CASES: List[JsonDict] = [
    {
        "intent": "urban, horror, fantasy, human portrait",
        "runs": 10,
        "minimum_subject_diversity": 3,
        "minimum_preset_diversity": 3,
        "minimum_location_diversity": 4,
        "minimum_mood_diversity": 2,
        "minimum_surreal_concept_diversity": 3,
        "minimum_strong_horror_rate": 0.9,
        "maximum_weak_only_horror_rate": 0.1,
        "maximum_horror_diluting_lighting_rate": 0.1,
        "minimum_subject_group_diversity": 3,
        "minimum_lighting_diversity": 3,
        "maximum_warm_location_horror_conflict_rate": 0.1,
        "minimum_fantasy_axis_coverage_rate": 0.8,
    }
]

BLEED_CHECK_CASES: List[JsonDict] = [
    {
        "name": "jewelry_macro_reflection_product",
        "intent": "jewelry macro reflection product",
        "preset": "jewelry_macro_reflection",
        "forced_choices": {
            "subject": ["silver_ring_jewelry"],
            "lens": ["105mm_macro"],
            "location": ["dark_studio"],
        },
        "forbidden_terms": ["stems", "leaves", "spores", "makeup", "wardrobe", "influencer"],
        "forbidden_slots": ["appearance_type", "hair_style", "makeup_style", "wardrobe_style", "costume_style"],
    },
    {
        "name": "documentary_craftsperson_workshop",
        "intent": "documentary craftsperson workshop",
        "preset": "documentary_craftsperson_workshop",
        "forced_choices": {
            "subject": ["glassblower_artisan"],
            "location": ["glassblowing_workshop"],
        },
        "forbidden_terms": ["idol", "office siren", "fashion editorial", "runway", "glam makeup"],
        "forbidden_slots": ["appearance_type", "makeup_style", "wardrobe_style", "costume_style", "aesthetic_trend"],
    },
    {
        "name": "wildlife_blizzard_documentary",
        "intent": "wildlife blizzard documentary",
        "preset": "nature_wildlife",
        "forced_choices": {
            "subject": ["eagle_perched"],
            "location": ["blizzard_open_plain"],
            "weather": ["windblown_snow"],
        },
        "forbidden_terms": ["product packshot", "fashion", "runway", "makeup", "wardrobe", "studio model"],
        "forbidden_slots": ["appearance_type", "hair_style", "makeup_style", "wardrobe_style", "costume_style", "surface_material"],
    },
    {
        "name": "street_food_night_analog_film",
        "intent": "street food night analog film",
        "preset": "pojangmacha_street_food_night",
        "forced_choices": {
            "subject": ["street_food_tteokbokki"],
            "location": ["pojangmacha_tent_night"],
            "film_emulation": ["kodak_gold_200_look"],
        },
        "forbidden_terms": ["idol", "makeup", "wardrobe", "wearing", "fashion model", "influencer"],
        "forbidden_slots": ["appearance_type", "hair_style", "makeup_style", "wardrobe_style", "costume_style"],
    },
]

DIVERSITY_CHECK_CASES: List[JsonDict] = [
    {
        "name": "urban_horror_fantasy_human_free_slots",
        "intent": "urban, horror, fantasy, human portrait",
        "runs": 12,
        "free_slots": ["lighting", "light_shape", "color", "texture", "lens", "action"],
        "minimum_preservation_rate": 0.85,
        "maximum_top1_dominance": 0.72,
        "minimum_unique_per_slot": 2,
        "maximum_render_suppression_rate": 0.25,
    },
    {
        "name": "jewelry_product_free_slots",
        "intent": "jewelry macro reflection product",
        "preset": "jewelry_macro_reflection",
        "runs": 10,
        "free_slots": ["lighting", "light_shape", "color", "texture", "lens"],
        "minimum_preservation_rate": 0.9,
        "maximum_top1_dominance": 0.75,
        "minimum_unique_per_slot": 2,
        "maximum_render_suppression_rate": 0.25,
    },
    {
        "name": "street_food_analog_free_slots",
        "intent": "street food night analog film",
        "preset": "pojangmacha_street_food_night",
        "runs": 10,
        "free_slots": ["lighting", "color", "texture", "camera_type", "film_emulation", "action"],
        "minimum_preservation_rate": 0.9,
        "maximum_top1_dominance": 0.75,
        "minimum_unique_per_slot": 2,
        "maximum_render_suppression_rate": 0.15,
    },
]


def fake_vectors(texts: Sequence[str], dimensions: int = DEFAULT_SEMANTIC_DIMENSIONS, **_: Any) -> List[List[float]]:
    vectors = []
    for text in texts:
        digest = hashlib.sha256(str(text).encode("utf-8")).digest()
        vector = [0.0] * dimensions
        for index, byte in enumerate(digest):
            vector[(byte + index) % dimensions] += 1.0 if index % 2 == 0 else -1.0
        norm = sum(value * value for value in vector) ** 0.5
        vectors.append([round(value / norm, 6) if norm else 0.0 for value in vector])
    return vectors


def choice_ids(result: JsonDict) -> Dict[str, str]:
    return {slot: choice.get("id", "") for slot, choice in result.get("choices", {}).items()}


def choice_tags(result: JsonDict) -> set[str]:
    tags: set[str] = set()
    for choice in result.get("choices", {}).values():
        tags |= set(choice.get("tags", []))
        tags |= set(choice.get("kind", []))
    return tags


def choice_payload(result: JsonDict, slot: str) -> JsonDict:
    return result.get("choices", {}).get(slot, {}) or {}


def dictionary_entry(data: JsonDict, slot: str, entry_id: str | None) -> JsonDict:
    if not entry_id:
        return {}
    for entry in data.get("slots", {}).get(slot, []):
        if entry.get("id") == entry_id:
            return entry
    return choice_payload({"choices": {slot: {"id": entry_id}}}, slot)


def text_blob(*parts: Any) -> str:
    return " ".join(str(part or "") for part in parts).lower()


def has_human_subject(result: JsonDict) -> bool:
    subject = choice_payload(result, "subject")
    return "human" in set(subject.get("tags", [])) or "human" in set(subject.get("kind", []))


def has_urban_location(result: JsonDict) -> bool:
    location = choice_payload(result, "location")
    tags = set(location.get("tags", [])) | set(location.get("kind", []))
    blob = text_blob(location.get("id"), location.get("en"), location.get("ko"))
    return bool(tags & {"urban", "street", "city"} or any(term in blob for term in ("urban", "city", "street", "alley", "subway", "neon")))


def has_horror_atmosphere(result: JsonDict) -> bool:
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
        "dread",
        "ritual",
        "occult",
        "liminal",
        "haunted",
        "panic",
    }
    for slot in ("mood", "lighting", "light_shape", "weather", "color", "texture"):
        choice = choice_payload(result, slot)
        tags = set(choice.get("tags", [])) | set(choice.get("kind", []))
        blob = text_blob(choice.get("id"), choice.get("en"), choice.get("ko"))
        if tags & horror_terms or any(term in blob for term in horror_terms):
            return True
    return False


def has_strong_horror_signal(data: JsonDict, result: JsonDict) -> bool:
    rules = coherence_rules_from_source(data)
    for slot in ("mood", "lighting", "light_shape", "weather", "color", "texture"):
        choice = choice_payload(result, slot)
        entry = dictionary_entry(data, slot, choice.get("id")) if choice else {}
        if entry and family_signal_strength(entry, "horror", rules, slot, data) == "strong":
            return True
    return False


def has_weak_only_horror_signal(data: JsonDict, result: JsonDict) -> bool:
    return has_horror_atmosphere(result) and not has_strong_horror_signal(data, result)


def has_horror_diluting_lighting(data: JsonDict, result: JsonDict) -> bool:
    rules = coherence_rules_from_source(data)
    mood = dictionary_entry(data, "mood", choice_payload(result, "mood").get("id"))
    if family_signal_strength(mood, "horror", rules, "mood", data) != "strong":
        return False
    for slot in ("lighting", "light_intensity", "light_shape", "color", "texture"):
        choice = choice_payload(result, slot)
        entry = dictionary_entry(data, slot, choice.get("id")) if choice else {}
        if entry and entry_conflicts_with_family(entry, slot, "horror", rules, data):
            return True
    return False


def subject_groups(data: JsonDict, result: JsonDict) -> set[str]:
    entry = dictionary_entry(data, "subject", choice_payload(result, "subject").get("id"))
    return set(entry_semantic_groups(entry, "subject", data))


def location_tones(data: JsonDict, result: JsonDict) -> set[str]:
    entry = dictionary_entry(data, "location", choice_payload(result, "location").get("id"))
    return set(entry_location_tones(entry, "location", data))


def has_warm_location_horror_conflict(data: JsonDict, result: JsonDict) -> bool:
    if not has_strong_horror_signal(data, result):
        return False
    tone_conflicts = ((semantic_metadata_from_source(data).get("family_tone_conflicts", {}) or {}).get("horror", {}) or {})
    return bool(location_tones(data, result) & set(tone_conflicts.get("location_tone", [])))


def has_fantasy_axis_coverage(data: JsonDict, result: JsonDict) -> bool:
    rules = coherence_rules_from_source(data)
    for slot in ("surreal_concept", "surreal_anchor", "wardrobe_style", "subject", "location", "mood"):
        choice = choice_payload(result, slot)
        entry = dictionary_entry(data, slot, choice.get("id")) if choice else {}
        if entry and family_signal_strength(entry, "fantasy", rules, slot, data) == "strong":
            return True
        if entry and "fantasy_strong" in set(entry_axis_signals(entry, slot, data)):
            return True
    return False


def preset_has_horror_strength(data: JsonDict, preset_id: str | None) -> bool:
    if not preset_id:
        return False
    rules = coherence_rules_from_source(data)
    preset = next((item for item in data.get("presets", []) if item.get("id") == preset_id), None)
    return bool(preset and preset_family_signal_strength(preset, "horror", rules, data) in {"strong", "ambient"})


def horror_terms_in_result(result: JsonDict) -> set[str]:
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
        "dread",
        "ritual",
        "occult",
        "liminal",
        "haunted",
        "panic",
        "shadow",
        "fog",
        "grime",
        "decay",
    }
    found: set[str] = set()
    for slot in ("mood", "lighting", "light_shape", "weather", "color", "texture"):
        choice = choice_payload(result, slot)
        tags = set(choice.get("tags", [])) | set(choice.get("kind", []))
        blob = text_blob(choice.get("id"), choice.get("en"), choice.get("ko"))
        found |= tags & horror_terms
        found |= {term for term in horror_terms if term in blob}
    return found


def has_surreal_layer(result: JsonDict) -> bool:
    return "surreal_concept" in result.get("choices", {})


def coverage(result: JsonDict, case: JsonDict) -> float:
    choices = choice_ids(result)
    required = case.get("required", {})
    if not required:
        return 1.0
    hits = 0
    for slot, ids in required.items():
        if choices.get(slot) in set(ids):
            hits += 1
    return hits / len(required)


def forbidden_hits(result: JsonDict, case: JsonDict) -> List[str]:
    tags = choice_tags(result)
    return sorted(tags & set(case.get("forbidden_tags", [])))


def build_mock_index(data: JsonDict, generator_module: Any) -> JsonDict:
    original = generator_module.embed_texts_with_gemini
    generator_module.embed_texts_with_gemini = lambda texts, dimensions=DEFAULT_SEMANTIC_DIMENSIONS, **kwargs: fake_vectors(texts, dimensions=dimensions)
    try:
        return build_semantic_index_payload(data, dimensions=DEFAULT_SEMANTIC_DIMENSIONS, api_key="mock")
    finally:
        generator_module.embed_texts_with_gemini = original


def load_project_env() -> None:
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key not in {"GEMINI_API_KEY", "GOOGLE_API_KEY"} or key in os.environ:
            continue
        value = value.strip().strip("\"'")
        if value:
            os.environ[key] = value


def forbidden_term_hits(prompt: str, forbidden_terms: Sequence[str]) -> List[str]:
    lowered = prompt.lower()
    return [term for term in forbidden_terms if term.lower() in lowered]


def evaluate_bleed_check(
    data: JsonDict,
    cases: Sequence[JsonDict],
    seed: int,
    semantic_index: JsonDict,
    gemini_api_key: str | None = None,
    runs: int = 10,
) -> JsonDict:
    results: List[JsonDict] = []
    for case_index, case in enumerate(cases):
        rows: List[JsonDict] = []
        forced_choices = case.get("forced_choices", {}) or {}
        forced_slots = set(forced_choices)
        for run_index in range(runs):
            result = generate_once(
                data=data,
                rng=random.Random(seed + 4000 + (case_index * 100) + run_index),
                preset_id=case.get("preset"),
                langs=["en"],
                include_negative=False,
                negative_count=12,
                include_choices=True,
                detail_level="detailed",
                forced_choices=forced_choices,
                intent=case["intent"],
                selection_mode="semantic",
                novelty="medium",
                include_trace=True,
                semantic_index=semantic_index,
                gemini_api_key=gemini_api_key,
            )
            choices = choice_ids(result)
            prompt = str(result.get("prompt_en", ""))
            term_hits = forbidden_term_hits(prompt, case.get("forbidden_terms", []))
            slot_hits = [
                slot
                for slot in case.get("forbidden_slots", [])
                if slot in choices and slot not in forced_slots
            ]
            picked_subject = dictionary_entry(data, "subject", choices.get("subject"))
            contract = result.get("semantic_trace", {}).get("generation_contract", {}) or {}
            rows.append(
                {
                    "run_index": run_index,
                    "preset_id": result.get("preset_id"),
                    "subject_category": subject_category({"subject": picked_subject}, data) if picked_subject else "generic",
                    "term_hits": term_hits,
                    "slot_hits": slot_hits,
                    "choices": choices,
                    "skipped_slots": contract.get("skipped_slots", []),
                    "render_suppressed_slots": contract.get("render_suppressed_slots", []),
                    "leaked": bool(term_hits or slot_hits),
                }
            )
        leak_count = sum(1 for row in rows if row["leaked"])
        results.append(
            {
                "name": case.get("name", case.get("intent")),
                "intent": case["intent"],
                "preset": case.get("preset"),
                "runs": runs,
                "leak_count": leak_count,
                "leak_rate": round(leak_count / max(len(rows), 1), 4),
                "passed": leak_count == 0,
                "results": rows,
            }
        )
    return {
        "case_count": len(results),
        "failed_case_count": sum(1 for item in results if not item["passed"]),
        "results": results,
    }


def shannon_entropy(values: Sequence[str]) -> float:
    cleaned = [value for value in values if value]
    if not cleaned:
        return 0.0
    counts = Counter(cleaned)
    total = len(cleaned)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def coverage_preservation_rate(contract: JsonDict) -> float:
    must_cover = contract.get("must_cover_axes", []) or []
    if not must_cover:
        return 1.0
    covered = contract.get("covered_axes", []) or []
    return len(covered) / max(len(must_cover), 1)


def evaluate_diversity_check(
    data: JsonDict,
    cases: Sequence[JsonDict],
    seed: int,
    semantic_index: JsonDict,
    gemini_api_key: str | None = None,
) -> JsonDict:
    results: List[JsonDict] = []
    for case_index, case in enumerate(cases):
        runs = int(case.get("runs", 10))
        free_slots = list(case.get("free_slots", []))
        rows: List[JsonDict] = []
        batch_context = make_batch_context("semantic", "high", runs)
        rng = random.Random(seed + 6000 + (case_index * 100))
        for run_index in range(runs):
            set_batch_index(batch_context, run_index)
            result = generate_once(
                data=data,
                rng=rng,
                preset_id=case.get("preset"),
                langs=["en"],
                include_negative=False,
                negative_count=12,
                include_choices=True,
                detail_level="detailed",
                intent=case["intent"],
                selection_mode="semantic",
                novelty="high",
                include_trace=True,
                semantic_index=semantic_index,
                gemini_api_key=gemini_api_key,
                batch_context=batch_context,
                batch_index=run_index,
            )
            trace = result.get("semantic_trace", {}) or {}
            contract = trace.get("generation_contract", {}) or {}
            choices = choice_ids(result)
            rows.append(
                {
                    "run_index": run_index,
                    "preset_id": result.get("preset_id"),
                    "choices": {slot: choices.get(slot) for slot in free_slots if choices.get(slot)},
                    "preservation_rate": round(coverage_preservation_rate(contract), 4),
                    "render_suppressed_count": len(contract.get("render_suppressed_slots", []) or []),
                    "coverage_gaps": contract.get("coverage_gaps", []),
                }
            )
        slot_metrics: Dict[str, JsonDict] = {}
        for slot in free_slots:
            values = [row["choices"].get(slot, "") for row in rows if row["choices"].get(slot)]
            counts = Counter(values)
            top_count = max(counts.values(), default=0)
            slot_metrics[slot] = {
                "observed": len(values),
                "unique": len(counts),
                "entropy": round(shannon_entropy(values), 4),
                "top1_dominance": round(top_count / max(len(values), 1), 4),
                "top": counts.most_common(5),
            }
        preservation_rate = round(sum(row["preservation_rate"] for row in rows) / max(len(rows), 1), 4)
        render_suppression_rate = round(
            sum(1 for row in rows if row["render_suppressed_count"] > 0) / max(len(rows), 1),
            4,
        )
        minimum_preservation = float(case.get("minimum_preservation_rate", 0.9))
        maximum_top1 = float(case.get("maximum_top1_dominance", 0.75))
        minimum_unique = int(case.get("minimum_unique_per_slot", 2))
        maximum_suppression = float(case.get("maximum_render_suppression_rate", 0.25))
        checked_slots = [slot for slot, metrics in slot_metrics.items() if metrics["observed"] >= 3]
        diversity_passed = all(
            slot_metrics[slot]["unique"] >= minimum_unique
            and slot_metrics[slot]["top1_dominance"] <= maximum_top1
            for slot in checked_slots
        )
        passed = (
            preservation_rate >= minimum_preservation
            and render_suppression_rate <= maximum_suppression
            and diversity_passed
        )
        results.append(
            {
                "name": case.get("name", case["intent"]),
                "intent": case["intent"],
                "runs": runs,
                "preservation_rate": preservation_rate,
                "minimum_preservation_rate": minimum_preservation,
                "render_suppression_rate": render_suppression_rate,
                "maximum_render_suppression_rate": maximum_suppression,
                "slot_metrics": slot_metrics,
                "checked_slots": checked_slots,
                "passed": passed,
                "results": rows,
            }
        )
    return {
        "case_count": len(results),
        "failed_case_count": sum(1 for item in results if not item["passed"]),
        "results": results,
    }


def evaluate_mode(
    data: JsonDict,
    mode: str,
    cases: Sequence[JsonDict],
    seed: int,
    semantic_index: JsonDict | None,
    gemini_api_key: str | None = None,
) -> JsonDict:
    results = []
    for index, case in enumerate(cases):
        result = generate_once(
            data=data,
            rng=random.Random(seed + index),
            preset_id=None,
            langs=["en"],
            include_negative=False,
            negative_count=12,
            include_choices=True,
            detail_level="detailed",
            intent=case["intent"] if mode != "rule" else None,
            selection_mode=mode,
            novelty="medium",
            include_trace=True,
            semantic_index=semantic_index if mode != "rule" else None,
            gemini_api_key=gemini_api_key if mode != "rule" else None,
        )
        results.append(
            {
                "intent": case["intent"],
                "preset_id": result.get("preset_id"),
                "coverage": coverage(result, case),
                "forbidden_hits": forbidden_hits(result, case),
                "choices": choice_ids(result),
            }
        )
    return {
        "mode": mode,
        "average_coverage": round(sum(item["coverage"] for item in results) / max(len(results), 1), 4),
        "forbidden_case_count": sum(1 for item in results if item["forbidden_hits"]),
        "unique_presets": len({item["preset_id"] for item in results}),
        "results": results,
    }


def evaluate_preset_guards(
    data: JsonDict,
    cases: Sequence[JsonDict],
    seed: int,
    semantic_index: JsonDict,
    gemini_api_key: str | None = None,
) -> JsonDict:
    results = []
    for index, case in enumerate(cases):
        result = generate_once(
            data=data,
            rng=random.Random(seed + 1000 + index),
            preset_id=None,
            langs=["en"],
            include_negative=False,
            negative_count=12,
            include_choices=True,
            detail_level="detailed",
            intent=case["intent"],
            selection_mode="semantic",
            novelty="medium",
            include_trace=True,
            semantic_index=semantic_index,
            gemini_api_key=gemini_api_key,
        )
        selected = result.get("preset_id")
        blacklisted = set(case.get("blacklisted_presets", []))
        results.append(
            {
                "intent": case["intent"],
                "preset_id": selected,
                "blacklisted": selected in blacklisted,
                "blacklisted_presets": sorted(blacklisted),
                "intent_axes": result.get("semantic_trace", {}).get("preset_score", {}).get("intent_axes"),
            }
        )
    return {
        "case_count": len(results),
        "blacklisted_case_count": sum(1 for item in results if item["blacklisted"]),
        "results": results,
    }


def evaluate_multi_axis_coverage(
    data: JsonDict,
    cases: Sequence[JsonDict],
    seed: int,
    semantic_index: JsonDict,
    gemini_api_key: str | None = None,
) -> JsonDict:
    results = []
    for case_index, case in enumerate(cases):
        runs = int(case.get("runs", 10))
        rows = []
        rng = random.Random(seed + 2000 + (case_index * 100))
        batch_context = make_batch_context("semantic", "medium", runs)
        for run_index in range(runs):
            set_batch_index(batch_context, run_index)
            result = generate_once(
                data=data,
                rng=rng,
                preset_id=None,
                langs=["en"],
                include_negative=False,
                negative_count=12,
                include_choices=True,
                detail_level="detailed",
                intent=case["intent"],
                selection_mode="semantic",
                novelty="medium",
                include_trace=True,
                semantic_index=semantic_index,
                gemini_api_key=gemini_api_key,
                batch_context=batch_context,
                batch_index=run_index,
            )
            coverage = {
                "human_subject": has_human_subject(result),
                "urban_location": has_urban_location(result),
                "horror_atmosphere": has_horror_atmosphere(result),
                "surreal_layer": has_surreal_layer(result),
            }
            strong_horror = has_strong_horror_signal(data, result)
            weak_only_horror = has_weak_only_horror_signal(data, result)
            horror_diluting_lighting = has_horror_diluting_lighting(data, result)
            groups = sorted(subject_groups(data, result))
            tones = sorted(location_tones(data, result))
            warm_location_horror_conflict = has_warm_location_horror_conflict(data, result)
            fantasy_axis_coverage = has_fantasy_axis_coverage(data, result)
            rows.append(
                {
                    "preset_id": result.get("preset_id"),
                    "subject": choice_payload(result, "subject").get("id"),
                    "subject_groups": groups,
                    "location": choice_payload(result, "location").get("id"),
                    "location_tones": tones,
                    "mood": choice_payload(result, "mood").get("id"),
                    "lighting": choice_payload(result, "lighting").get("id"),
                    "color": choice_payload(result, "color").get("id"),
                    "surreal_concept": choice_payload(result, "surreal_concept").get("id"),
                    "coverage": coverage,
                    "strong_horror": strong_horror,
                    "weak_only_horror": weak_only_horror,
                    "horror_diluting_lighting": horror_diluting_lighting,
                    "warm_location_horror_conflict": warm_location_horror_conflict,
                    "fantasy_axis_coverage": fantasy_axis_coverage,
                    "horror_preset_signal": preset_has_horror_strength(data, result.get("preset_id")),
                    "horror_terms": sorted(horror_terms_in_result(result)),
                }
            )
        category_rates = {
            key: round(sum(1 for row in rows if row["coverage"][key]) / max(len(rows), 1), 4)
            for key in ("human_subject", "urban_location", "horror_atmosphere", "surreal_layer")
        }
        unique_subjects = len({row.get("subject") for row in rows if row.get("subject")})
        unique_presets = len({row.get("preset_id") for row in rows if row.get("preset_id")})
        unique_locations = len({row.get("location") for row in rows if row.get("location")})
        unique_subject_groups = len({group for row in rows for group in row.get("subject_groups", [])})
        unique_lighting = len({row.get("lighting") for row in rows if row.get("lighting")})
        unique_moods = len({row.get("mood") for row in rows if row.get("mood")})
        unique_surreal_concepts = len({row.get("surreal_concept") for row in rows if row.get("surreal_concept")})
        unique_horror_terms = sorted({term for row in rows for term in row.get("horror_terms", [])})
        strong_horror_rate = round(sum(1 for row in rows if row.get("strong_horror")) / max(len(rows), 1), 4)
        weak_only_horror_rate = round(sum(1 for row in rows if row.get("weak_only_horror")) / max(len(rows), 1), 4)
        horror_diluting_lighting_rate = round(sum(1 for row in rows if row.get("horror_diluting_lighting")) / max(len(rows), 1), 4)
        warm_location_horror_conflict_rate = round(sum(1 for row in rows if row.get("warm_location_horror_conflict")) / max(len(rows), 1), 4)
        fantasy_axis_coverage_rate = round(sum(1 for row in rows if row.get("fantasy_axis_coverage")) / max(len(rows), 1), 4)
        horror_preset_signal_rate = round(sum(1 for row in rows if row.get("horror_preset_signal")) / max(len(rows), 1), 4)
        minimum_subjects = int(case.get("minimum_subject_diversity", 1))
        minimum_presets = int(case.get("minimum_preset_diversity", 1))
        minimum_locations = int(case.get("minimum_location_diversity", 1))
        minimum_moods = int(case.get("minimum_mood_diversity", 1))
        minimum_surreal = int(case.get("minimum_surreal_concept_diversity", 1))
        minimum_subject_groups = int(case.get("minimum_subject_group_diversity", 1))
        minimum_lighting = int(case.get("minimum_lighting_diversity", 1))
        minimum_strong_horror_rate = float(case.get("minimum_strong_horror_rate", 0.0))
        maximum_weak_only_horror_rate = float(case.get("maximum_weak_only_horror_rate", 1.0))
        maximum_horror_diluting_lighting_rate = float(case.get("maximum_horror_diluting_lighting_rate", 1.0))
        maximum_warm_location_horror_conflict_rate = float(case.get("maximum_warm_location_horror_conflict_rate", 1.0))
        minimum_fantasy_axis_coverage_rate = float(case.get("minimum_fantasy_axis_coverage_rate", 0.0))
        results.append(
            {
                "intent": case["intent"],
                "runs": runs,
                "category_rates": category_rates,
                "strong_horror_rate": strong_horror_rate,
                "weak_only_horror_rate": weak_only_horror_rate,
                "horror_diluting_lighting_rate": horror_diluting_lighting_rate,
                "warm_location_horror_conflict_rate": warm_location_horror_conflict_rate,
                "fantasy_axis_coverage_rate": fantasy_axis_coverage_rate,
                "horror_preset_signal_rate": horror_preset_signal_rate,
                "unique_subjects": unique_subjects,
                "unique_subject_groups": unique_subject_groups,
                "unique_presets": unique_presets,
                "unique_locations": unique_locations,
                "unique_lighting": unique_lighting,
                "unique_moods": unique_moods,
                "unique_surreal_concepts": unique_surreal_concepts,
                "unique_horror_terms": len(unique_horror_terms),
                "horror_terms": unique_horror_terms,
                "minimum_subject_diversity": minimum_subjects,
                "minimum_subject_group_diversity": minimum_subject_groups,
                "minimum_preset_diversity": minimum_presets,
                "minimum_location_diversity": minimum_locations,
                "minimum_lighting_diversity": minimum_lighting,
                "minimum_mood_diversity": minimum_moods,
                "minimum_surreal_concept_diversity": minimum_surreal,
                "minimum_strong_horror_rate": minimum_strong_horror_rate,
                "maximum_weak_only_horror_rate": maximum_weak_only_horror_rate,
                "maximum_horror_diluting_lighting_rate": maximum_horror_diluting_lighting_rate,
                "maximum_warm_location_horror_conflict_rate": maximum_warm_location_horror_conflict_rate,
                "minimum_fantasy_axis_coverage_rate": minimum_fantasy_axis_coverage_rate,
                "passed": all(rate >= 0.9 for rate in category_rates.values())
                and unique_subjects >= minimum_subjects
                and unique_subject_groups >= minimum_subject_groups
                and unique_presets >= minimum_presets
                and unique_locations >= minimum_locations
                and unique_lighting >= minimum_lighting
                and unique_moods >= minimum_moods
                and unique_surreal_concepts >= minimum_surreal
                and strong_horror_rate >= minimum_strong_horror_rate
                and weak_only_horror_rate <= maximum_weak_only_horror_rate
                and horror_diluting_lighting_rate <= maximum_horror_diluting_lighting_rate
                and warm_location_horror_conflict_rate <= maximum_warm_location_horror_conflict_rate
                and fantasy_axis_coverage_rate >= minimum_fantasy_axis_coverage_rate,
                "results": rows,
            }
        )
    return {
        "case_count": len(results),
        "failed_case_count": sum(1 for item in results if not item["passed"]),
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate semantic prompt selection against golden intents.")
    parser.add_argument("--tags", default=DEFAULT_TAGS)
    parser.add_argument("--semantic-index", default=DEFAULT_INDEX)
    parser.add_argument("--seed", type=int, default=20260529)
    parser.add_argument("--limit", type=int, default=0, help="Limit golden cases for a quick run.")
    parser.add_argument("--mock-embeddings", action="store_true", help="Use deterministic mock embeddings for CI structure checks, not quality evaluation.")
    parser.add_argument("--dry-run", action="store_true", help="Print case counts and exit without generating prompts.")
    parser.add_argument("--check-index", action="store_true", help="Validate semantic index metadata without embedding API calls.")
    parser.add_argument("--bleed-check", action="store_true", help="Run cross-category leakage checks for product, craft, wildlife, and food scenarios.")
    parser.add_argument("--bleed-runs", type=int, default=10, help="Number of seeds per bleed-check case.")
    parser.add_argument("--diversity-check", action="store_true", help="Run V8 keyword preservation and free-slot diversity checks.")
    args = parser.parse_args()

    load_project_env()
    data = load_json(args.tags)
    cases = GOLDEN_CASES[: args.limit] if args.limit else GOLDEN_CASES
    if args.check_index:
        semantic_index = json.loads(Path(args.semantic_index).read_text(encoding="utf-8"))
        validate_semantic_index_metadata(
            semantic_index,
            data,
            model=SEMANTIC_MODEL_ID,
            dimensions=DEFAULT_SEMANTIC_DIMENSIONS,
        )
        print(
            json.dumps(
                {
                    "status": "ok",
                    "dictionary_hash": semantic_index.get("dictionary_hash"),
                    "semantic_text_recipe": semantic_index.get("semantic_text_recipe"),
                    "expected_semantic_text_recipe": SEMANTIC_TEXT_RECIPE_VERSION,
                    "embedding_model": semantic_index.get("embedding_model"),
                    "embedding_dimensions": semantic_index.get("embedding_dimensions"),
                    "entry_count": len(semantic_index.get("entries", {})),
                },
                indent=2,
            )
        )
        return 0
    if args.dry_run:
        print(
            json.dumps(
                {
                    "golden_cases": len(cases),
                    "open_ended_intents": len(OPEN_ENDED_INTENTS),
                    "multi_axis_preset_guards": len(MULTI_AXIS_PRESET_GUARDS),
                    "multi_axis_coverage_cases": len(MULTI_AXIS_COVERAGE_CASES),
                    "bleed_check_cases": len(BLEED_CHECK_CASES),
                    "diversity_check_cases": len(DIVERSITY_CHECK_CASES),
                },
                indent=2,
            )
        )
        return 0

    import prompt_generator as generator_module

    semantic_index = build_mock_index(data, generator_module) if args.mock_embeddings else json.loads(Path(args.semantic_index).read_text(encoding="utf-8"))
    original_embed_texts = generator_module.embed_texts_with_gemini
    if args.mock_embeddings:
        generator_module.embed_texts_with_gemini = lambda texts, dimensions=DEFAULT_SEMANTIC_DIMENSIONS, **kwargs: fake_vectors(texts, dimensions=dimensions)
    gemini_api_key = "mock" if args.mock_embeddings else None

    try:
        if args.bleed_check:
            bleed_cases = BLEED_CHECK_CASES[: args.limit] if args.limit else BLEED_CHECK_CASES
            summary = {
                "warning": "mock embeddings are deterministic test doubles, not retrieval-quality evidence" if args.mock_embeddings else None,
                "bleed_check": evaluate_bleed_check(
                    data,
                    bleed_cases,
                    args.seed,
                    semantic_index,
                    gemini_api_key,
                    runs=max(1, args.bleed_runs),
                ),
            }
            print(json.dumps(summary, ensure_ascii=False, indent=2))
            return 0 if summary["bleed_check"]["failed_case_count"] == 0 else 6
        if args.diversity_check:
            diversity_cases = DIVERSITY_CHECK_CASES[: args.limit] if args.limit else DIVERSITY_CHECK_CASES
            diversity_result = evaluate_diversity_check(
                data,
                diversity_cases,
                args.seed,
                semantic_index,
                gemini_api_key,
            )
            if args.mock_embeddings:
                diversity_result["failed_case_count"] = 0
                for row in diversity_result.get("results", []):
                    row["passed"] = True
                    row["mock_quality_gate_skipped"] = True
            summary = {
                "warning": "mock embeddings are deterministic test doubles, not retrieval-quality evidence" if args.mock_embeddings else None,
                "diversity_check": diversity_result,
            }
            print(json.dumps(summary, ensure_ascii=False, indent=2))
            return 0 if args.mock_embeddings or summary["diversity_check"]["failed_case_count"] == 0 else 7
        summary = {
            "warning": "mock embeddings are deterministic test doubles, not retrieval-quality evidence" if args.mock_embeddings else None,
            "modes": [
                evaluate_mode(data, "rule", cases, args.seed, None),
                evaluate_mode(data, "hybrid", cases, args.seed, semantic_index, gemini_api_key),
                evaluate_mode(data, "semantic", cases, args.seed, semantic_index, gemini_api_key),
            ],
            "preset_guards": evaluate_preset_guards(data, MULTI_AXIS_PRESET_GUARDS, args.seed, semantic_index, gemini_api_key),
            "multi_axis_coverage": evaluate_multi_axis_coverage(data, MULTI_AXIS_COVERAGE_CASES, args.seed, semantic_index, gemini_api_key),
        }
    finally:
        if args.mock_embeddings:
            generator_module.embed_texts_with_gemini = original_embed_texts

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if args.mock_embeddings:
        return 0
    semantic = next(item for item in summary["modes"] if item["mode"] == "semantic")
    rule = next(item for item in summary["modes"] if item["mode"] == "rule")
    if semantic["average_coverage"] < rule["average_coverage"]:
        print("semantic average coverage is below rule average coverage", file=sys.stderr)
        return 2
    if semantic["forbidden_case_count"] > 0:
        print("semantic produced forbidden facet/tag hits", file=sys.stderr)
        return 3
    if not args.mock_embeddings and summary["preset_guards"]["blacklisted_case_count"] > 0:
        print("semantic selected a blacklisted single-axis preset for a multi-axis guard case", file=sys.stderr)
        return 4
    if not args.mock_embeddings and summary["multi_axis_coverage"]["failed_case_count"] > 0:
        print("semantic failed multi-axis category coverage", file=sys.stderr)
        return 5
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
