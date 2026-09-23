"""Compile everyday event relations into optional photo candidate data.

The research JSON owns the scenarios. This compiler adds only seven narrow
visual profiles; existing background/action profiles stay the source of truth.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
MAINTENANCE = ROOT / "docs/research-evidence/photo-prompt/extension-maintenance"


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


# Only these seven relations add meaning that the current generic action/use
# profiles cannot test precisely. A complete relation, never its short label,
# is the exact hard-activation term.
HARD_COMPONENTS = {
    "ed_cafe_pickup_wait": [
        "a customer waits facing the cafe pickup point",
        "a prepared drink remains on the service side of the counter",
        "an open handoff gap connects the service side and customer side",
        "the prepared drink remains separate from the customer's hands",
    ],
    "ed_market_compare": [
        "two comparable products are simultaneously visible at one shopping area",
        "the shopper holds one product beside the second alternative",
        "the shopper's hand or gaze connects both products as one choice",
        "the compared products have visible support from hands, basket, or shelf",
    ],
    "ed_subway_exit": [
        "an open train door separates the carriage from the platform",
        "the passenger crosses the doorway toward the platform",
        "the passenger's step has a plausible floor and threshold support",
        "the exit path remains navigable for the passenger",
    ],
    "ed_rain_threshold": [
        "a doorway visibly separates the sheltered interior from the wet exterior",
        "the person's hand folds a damp umbrella just inside the doorway",
        "water stays on the weather exposed umbrella and exterior route",
        "a nearby floor mat or stable surface receives the folded umbrella",
    ],
    "ed_clean_room_reset": [
        "a person returns one used item to its place in a clean room",
        "one recently cleared work surface remains visible",
        "one small remaining task stays active beside the cleared area",
        "an open walking path connects the active area to the room",
    ],
    "ed_shared_phone": [
        "one phone screen lies between two reachable people",
        "the presenting hand angles that same screen toward the recipient",
        "both people's gaze directions converge on the shared screen",
        "the recipient shows a small visible response to the shared view",
    ],
    "ed_independent_bystander": [
        "the focal person performs a legible foreground task",
        "a background person performs a different legible task",
        "the two tasks have separate targets or walking routes",
        "the requested foreground hand action remains visible",
    ],
}

LABELS = {
    "ed_home_departure": ("현관 외출 전 신발 조정", "adjusting a shoe before leaving home", "relational_action", ["action"]),
    "ed_kitchen_prep": ("주방 조리 중간 단계", "preparing food at a home kitchen worktop", "relational_action", ["action"]),
    "ed_laundry_sort": ("세탁 전 옷 분류", "sorting clothes before a wash", "relational_action", ["action"]),
    "ed_clean_room_reset": ("정돈 중인 깨끗한 방", "tidying a clean actively used room", "space_condition", ["setting"]),
    "ed_cafe_pickup_wait": ("카페 픽업 대기", "waiting at a cafe pickup counter", "relational_action", ["action"]),
    "ed_market_compare": ("매장 두 상품 비교", "comparing two items at a market shelf", "relational_action", ["action"]),
    "ed_checkout_handoff": ("계산대 결제 접점", "bringing payment to a checkout terminal", "relational_action", ["action"]),
    "ed_bus_stop_ready": ("버스 탑승 직전", "boarding at an open bus doorway", "relational_action", ["action"]),
    "ed_subway_exit": ("열차 문턱에서 하차", "stepping out through an open train door", "relational_action", ["action"]),
    "ed_rain_threshold": ("비 온 뒤 실내 진입과 우산 접기", "folding a wet umbrella just inside a doorway", "relational_action", ["action"]),
    "ed_office_return": ("공용 구역에서 자리로 복귀", "carrying a drink back to an office desk", "relational_action", ["action"]),
    "ed_library_page_turn": ("도서관 책장 넘기는 순간", "turning one page at a library table", "relational_action", ["action"]),
    "ed_clinic_wait": ("진료 공간의 접수 전 대기", "waiting in a clean clinic reception area", "space_condition", ["setting"]),
    "ed_laundromat_transfer": ("세탁기에서 바구니로 옮기기", "moving laundry from an open washer to a basket", "relational_action", ["action"]),
    "ed_civic_form": ("공공 서비스 서류 작성", "completing a form before a public service counter", "relational_action", ["action"]),
    "ed_park_rest": ("산책하다 잠시 쉬기", "briefly resting beside a walking path", "relational_action", ["action"]),
    "ed_shared_phone": ("한 휴대폰 화면을 함께 보며 반응", "sharing one phone screen and reacting", "relational_action", ["relationship"]),
    "ed_shop_closing": ("작은 가게 영업 종료 정리", "tidying a small shop after service", "relational_action", ["action"]),
    "ed_parcel_open": ("택배를 막 연 순간", "opening a parcel at a home table", "relational_action", ["action"]),
    "ed_independent_bystander": ("주변인의 독립적인 과업", "a bystander doing a different task", "crowd_density", ["setting"]),
}

# Short phrases support ordinary grammatical variants during optional bundle
# discovery. They do not activate the hard visual profiles.
NATURAL_ALIASES = {
    "ed_cafe_pickup_wait": ["a cafe pickup counter", "waits at a cafe pickup counter"],
    "ed_market_compare": ["compares two items", "two items at a market shelf"],
    "ed_subway_exit": ["steps out through an open train door"],
    "ed_rain_threshold": ["folds a wet umbrella just inside a doorway"],
    "ed_clean_room_reset": ["tidying a clean room"],
    "ed_shared_phone": ["shows a phone screen", "one phone screen between two people"],
    "ed_independent_bystander": ["background person performs a different task"],
}

POSITIVE_OVERRIDES = {
    "ed_clean_room_reset": {2: "an open walking path remains beside the active work area"},
    "ed_cafe_pickup_wait": {2: "the prepared drink remains on the service side, apart from the customer's hands"},
    "ed_clinic_wait": {2: "the visitor remains in the waiting zone before the service threshold"},
    "ed_civic_form": {2: "a visible form and the service route occupy the same work area"},
    "ed_independent_bystander": {2: "the requested focal action remains visible in front of the background activity"},
}


def profile_for(row: dict, label_ko: str, label_en: str) -> dict:
    pid = row["id"]
    units = HARD_COMPONENTS[pid]
    definition = "; ".join(units)
    profile = {
        "id": pid,
        "category": "everyday_event_relation",
        "activation": {
            "exact_terms": [definition],
            "requires_adult_character": True,
            "semantic_discovery_requires_component_evidence": False,
        },
        "semantics": {
            "definition": definition,
            "paraphrase_examples": [label_ko, label_en, row["prompt_seed_en"]],
            "visual_components": [label_ko, label_en, *units],
            "contrast_examples": row["reject_substitutes"],
            "claim_limits": [
                "Every component must refer to the same visible people, objects and scene.",
                "A still image cannot establish an unshown motive, prior event or capture authenticity.",
                "A broad everyday or candid label does not activate this narrow relation.",
            ],
        },
        "concept_candidate": {"concept_terms": [label_ko, label_en, *units]},
        "runtime_expression": {
            "default_mode": "definition_with_optional_label",
            "prompt_label_terms": [], "forbidden_prompt_terms": [], "runtime_forbidden_labels": [],
        },
        "reject_substitutes": row["reject_substitutes"],
        "authored_components": {"contract_version": "photo-authored-visual-components/v1", "components": []},
    }
    for index, phrase in enumerate(units, 1):
        profile["authored_components"]["components"].append({
            "id": f"component_{index}",
            "match_terms": [phrase], "evidence_field": f"component_{index}_phrase",
            "evidence_terms": [phrase], "min_content_words": 3,
            "instruction": "Show this relation on its named owner: " + phrase,
            "render_gate": {
                "id": f"vo_{pid}_{index}", "review_scale": "both",
                "description": phrase + ". Missing, substituted or partly realized evidence fails.",
            },
        })
    return profile


def main() -> None:
    research = read(HERE / "candidate-bundles.json")
    source_rows = research["candidate_bundles"]
    if set(LABELS) != {row["id"] for row in source_rows}:
        raise ValueError("runtime mapping and research candidate IDs differ")
    slots: dict[str, list[dict]] = {}
    bundles: list[dict] = []
    profiles: list[dict] = []
    coverage: list[dict] = []
    for row in source_rows:
        pid = row["id"]
        label_ko, label_en, semantic_slot, dimensions = LABELS[pid]
        # The relational_action slot requires a resolved human subject, while
        # joint bundle admission checks the still-generic frozen core. Store
        # these optional event candidates in the broadly usable action slot;
        # their relation and dimension ownership remain explicit below.
        slot = "action" if semantic_slot == "relational_action" else semantic_slot
        if pid in HARD_COMPONENTS:
            profiles.append(profile_for(row, label_ko, label_en))
        candidate_id = pid + "_candidate"
        requirements = list(row["visible_requirements"])
        for index, phrase in POSITIVE_OVERRIDES.get(pid, {}).items():
            requirements[index] = phrase
        entry = {
            "id": candidate_id, "ko": label_ko, "en": label_en,
            "weight": 0.45,
            "tags": ["photographic_scene", "everyday_event", semantic_slot, "human"],
            "aliases": [label_ko, label_en, *NATURAL_ALIASES.get(pid, [])],
            "keywords": [label_ko, label_en, *NATURAL_ALIASES.get(pid, []), *row["role_graph"]],
            "embedding_text": "; ".join([label_ko, label_en, *NATURAL_ALIASES.get(pid, []), *row["role_graph"], *requirements]),
            "concept_units": [label_ko, label_en, *NATURAL_ALIASES.get(pid, []), *row["role_graph"]],
            "relations": [{
                "id": pid + "_actor_target_state",
                "type": "one_visible_everyday_event",
                "subject": row["role_graph"][0],
                "object": "the selected action target and its supported scene state",
            }],
            "affected_dimensions": dimensions,
        }
        slots.setdefault(slot, []).append(entry)
        bundles.append({
            "id": pid,
            "primary_visual_proposition": label_ko,
            "component_groups": [
                {"id": f"{pid}_component_{index}", "visible_evidence": [phrase]}
                for index, phrase in enumerate(requirements, 1)
            ],
            "candidate_ids": [candidate_id],
            "candidate_slots": {candidate_id: slot},
            "hard_profile_ids": [pid] if pid in HARD_COMPONENTS else row["existing_profile_ids"],
            "confusion_boundaries": [
                *row["reject_substitutes"],
                "This selected event cannot replace a locked requester action, setting or people count.",
            ],
            "source_keywords": [label_ko, label_en, pid],
            "relations": [{
                "id": pid + "_joint_event",
                "type": "co_realized_in_one_frame",
                "subject": "the selected actor and action target",
                "object": "one coherent setting and visible event phase",
            }],
        })
        coverage.append({
            "research_id": pid,
            "candidate_id": candidate_id,
            "bundle_id": pid,
            "slot": slot,
            "new_profile_id": pid if pid in HARD_COMPONENTS else None,
            "existing_profile_ids": row["existing_profile_ids"],
            "source_ids": row["source_ids"],
        })
    extension = {
        "schema_version": "photo-prompt-research-extension/v1",
        "slots": slots,
        "visual_semantics": bundles,
    }
    record = {
        "record_id": "photo_prompt_everyday_scene_extension",
        "authored_source_sha256": digest(extension),
        "maintenance_only": {
            "research_path": str(HERE.relative_to(ROOT)),
            "coverage": coverage,
            "source_urls": research["sources"],
            "source_scope": research["selection_policy"]["source_scope"],
            "broad_policy": research["selection_policy"]["broad_everyday_terms"],
            "pixel_status": "not_run",
        },
    }
    write(MAINTENANCE / "photo_prompt_everyday_scene_extension.json", record)
    extension["maintenance_ref"] = {
        "contract_version": "photo-extension-maintenance-ref/v1",
        "record_id": record["record_id"],
        "sha256": digest(record),
    }
    write(ASSETS / "photo_prompt_everyday_scene_extension.json", extension)
    write(ASSETS / "photo_prompt_visual_obligations_everyday_scene.json", {
        "schema_version": "photo-visual-obligation-registry-extension/v1",
        "relation_contract_version": "photo-visual-relation/v1",
        "description": "Narrow everyday event relations; broad everyday labels stay advisory.",
        "profiles": profiles,
    })
    write(HERE / "implementation-coverage.json", {
        "new_profiles": len(profiles),
        "optional_candidates": sum(map(len, slots.values())),
        "optional_bundles": len(bundles),
        "rows": coverage,
    })
    print(json.dumps({"profiles": len(profiles), "candidates": sum(map(len, slots.values())), "bundles": len(bundles)}))


if __name__ == "__main__":
    main()
