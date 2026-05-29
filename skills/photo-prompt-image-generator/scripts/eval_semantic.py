#!/usr/bin/env python3
"""Evaluate rule, hybrid, and semantic photo-prompt selection against golden intents."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence

from prompt_generator import (
    DEFAULT_SEMANTIC_DIMENSIONS,
    SEMANTIC_MODEL_ID,
    build_semantic_index_payload,
    generate_once,
    load_json,
)


JsonDict = Dict[str, Any]

DEFAULT_TAGS = Path(__file__).resolve().parents[1] / "assets" / "photo_prompt_tags.json"
DEFAULT_INDEX = Path(__file__).resolve().parents[1] / "assets" / "photo_prompt_semantic_index.json"

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
    {"intent": "urban, horror, fantasy, human portrait", "runs": 10, "minimum_subject_diversity": 3}
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
    horror_terms = {"horror", "fear", "nightmare", "terror", "eerie", "uncanny", "tense", "noir", "gothic", "dark", "suspense"}
    for slot in ("mood", "lighting", "light_shape", "weather", "color", "texture"):
        choice = choice_payload(result, slot)
        tags = set(choice.get("tags", [])) | set(choice.get("kind", []))
        blob = text_blob(choice.get("id"), choice.get("en"), choice.get("ko"))
        if tags & horror_terms or any(term in blob for term in horror_terms):
            return True
    return False


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
        for run_index in range(runs):
            result = generate_once(
                data=data,
                rng=random.Random(seed + 2000 + (case_index * 100) + run_index),
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
            coverage = {
                "human_subject": has_human_subject(result),
                "urban_location": has_urban_location(result),
                "horror_atmosphere": has_horror_atmosphere(result),
                "surreal_layer": has_surreal_layer(result),
            }
            rows.append(
                {
                    "preset_id": result.get("preset_id"),
                    "subject": choice_payload(result, "subject").get("id"),
                    "location": choice_payload(result, "location").get("id"),
                    "mood": choice_payload(result, "mood").get("id"),
                    "surreal_concept": choice_payload(result, "surreal_concept").get("id"),
                    "coverage": coverage,
                }
            )
        category_rates = {
            key: round(sum(1 for row in rows if row["coverage"][key]) / max(len(rows), 1), 4)
            for key in ("human_subject", "urban_location", "horror_atmosphere", "surreal_layer")
        }
        unique_subjects = len({row.get("subject") for row in rows if row.get("subject")})
        results.append(
            {
                "intent": case["intent"],
                "runs": runs,
                "category_rates": category_rates,
                "unique_subjects": unique_subjects,
                "minimum_subject_diversity": int(case.get("minimum_subject_diversity", 1)),
                "passed": all(rate >= 0.9 for rate in category_rates.values())
                and unique_subjects >= int(case.get("minimum_subject_diversity", 1)),
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
    args = parser.parse_args()

    data = load_json(args.tags)
    cases = GOLDEN_CASES[: args.limit] if args.limit else GOLDEN_CASES
    if args.dry_run:
        print(
            json.dumps(
                {
                    "golden_cases": len(cases),
                    "open_ended_intents": len(OPEN_ENDED_INTENTS),
                    "multi_axis_preset_guards": len(MULTI_AXIS_PRESET_GUARDS),
                    "multi_axis_coverage_cases": len(MULTI_AXIS_COVERAGE_CASES),
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
