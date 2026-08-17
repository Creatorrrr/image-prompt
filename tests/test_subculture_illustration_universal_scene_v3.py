"""Focused contracts for the topic-independent illustration scene layer.

Prompt checks below prove deterministic planning and literal binding only.  The
separate six-case render holdout remains the authority for pixel legibility.
"""

from __future__ import annotations

import copy
from collections import Counter
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "subculture-illustration-image-generator"
SCRIPT_ROOT = SKILL_ROOT / "scripts"
ASSET_ROOT = SKILL_ROOT / "assets"
sys.path.insert(0, str(SCRIPT_ROOT))

from illustration_audit import (  # noqa: E402
    audit_universal_scene_evidence,
    computed_pack_id,
    validate_pack_integrity,
)
import illustration_audit as illustration_audit_module  # noqa: E402
from illustration_runtime import (  # noqa: E402
    CONTRACT_VERSION,
    InputContractError,
    ResolutionError,
    V1_CONTRACT_VERSION,
    V2_CONTRACT_VERSION,
    build_candidate_pack,
    load_runtime_assets,
)
from universal_scene_runtime import (  # noqa: E402
    InputContractError as UniversalInputContractError,
    canonical_sha256,
    load_universal_scene_assets,
    validate_scene_contract,
    validate_universal_scene_selection,
)
import universal_scene_runtime as universal_runtime_module  # noqa: E402
from validate_illustration_assets import (  # noqa: E402
    ValidationFailure,
    evaluate_universal_scene_compiled_obligations,
    validate_all,
    validate_legacy_prompt_qualification,
    validate_photo_regression_baseline,
    validate_prompt_qualification,
    validate_universal_scene_current_oracle_v2,
    validate_universal_scene_holdouts,
    validate_universal_scene_research,
    validate_universal_scene_runtime_assets,
)
import validate_illustration_assets as validator_module  # noqa: E402


def _json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _rehash(pack: dict[str, object]) -> None:
    pack["pack_id"] = computed_pack_id(pack)


def _checks(issues: list[dict[str, object]]) -> set[str]:
    return {str(issue.get("check")) for issue in issues}


def _role_by_id(pack: dict[str, object]) -> dict[str, dict[str, object]]:
    scene = pack["universal_scene"]
    assert isinstance(scene, dict)
    event = scene["selected_event"]
    assert isinstance(event, dict)
    roles = event["roles"]
    assert isinstance(roles, list)
    return {str(role["role_id"]): role for role in roles if isinstance(role, dict)}


def _literal_universal_evidence(
    pack: dict[str, object],
) -> tuple[dict[str, object], str]:
    """Build compact literal bindings for direct evidence-audit mutations."""

    scene = pack["universal_scene"]
    assert isinstance(scene, dict)
    carriers = scene["composition_carriers"]
    assert isinstance(carriers, dict)

    def carrier_record(
        section: str,
        predicate: object,
    ) -> dict[str, object]:
        records = carriers[section]
        assert isinstance(records, list)
        record = next(item for item in records if predicate(item))
        assert isinstance(record, dict)
        return record

    identity = scene["identity_core"]
    assert isinstance(identity, dict)
    identity_ids = [
        fact["id"]
        for entity in identity["entities"]
        for fact in entity["feature_facts"]
    ] + [
        fact["id"]
        for collection in ("scene_facts", "forbidden_facts")
        for fact in identity[collection]
    ]
    fixed_slots = [
        (slot["slot_id"], value_id)
        for slot in scene["slot_states"]
        if slot["state"] == "fixed"
        for value_id in slot["value_ids"]
    ]
    roles = scene["selected_event"]["roles"]
    distance = scene["semantic_distance_trace"]
    remote = distance["fixed_remote_count"] + distance["optional_remote_count"] > 0
    consequence_required = (
        next(role for role in roles if role["role_id"] == "result")["value_id"]
        is not None
        or bool(scene["pixel_evidence_contract"]["consequence_item_ids"])
        or any(atom["facet"] == "consequence" for atom in scene["atoms"])
    )
    links: list[tuple[dict[str, object], dict[str, object]]] = []

    def linked(
        output: dict[str, object],
        section: str,
        predicate: object,
    ) -> dict[str, object]:
        links.append((output, carrier_record(section, predicate)))
        return output

    identity_phrases = [
        linked(
            {"fact_id": fact_id},
            "identity_core",
            lambda item, fact_id=fact_id: item["fact_id"] == fact_id,
        )
        for fact_id in identity_ids
    ]
    fixed_slot_phrases = [
        linked(
            {"slot_id": slot_id, "value_id": value_id},
            "fixed_slots",
            lambda item, slot_id=slot_id, value_id=value_id: (
                item["slot_id"] == slot_id and item["value_id"] == value_id
            ),
        )
        for slot_id, value_id in fixed_slots
    ]
    event_role_phrases = [
        linked(
            {"role_id": role["role_id"]},
            "event_roles",
            lambda item, role_id=role["role_id"]: item["role_id"] == role_id,
        )
        for role in roles
        if role["value_id"] is not None
    ]
    atom_phrases = [
        linked(
            {"instance_id": atom["instance_id"]},
            "atoms",
            lambda item, instance_id=atom["instance_id"]: (
                item["instance_id"] == instance_id
            ),
        )
        for atom in scene["atoms"]
    ]
    bridge_phrases = [
        linked(
            {"bridge_id": bridge["bridge_id"]},
            "bridges",
            lambda item, bridge_id=bridge["bridge_id"]: item["bridge_id"] == bridge_id,
        )
        for bridge in scene["bridges"]
    ]
    resource_phrases = [
        linked(
            {"claim_id": claim["claim_id"]},
            "resources",
            lambda item, claim_id=claim["claim_id"]: item["claim_id"] == claim_id,
        )
        for claim in scene["resource_claims"]
        if claim["evidence_required"] is True
    ]

    # One authenticated phrase may bind at most eight records.  Repeated
    # event/atom/bridge/resource anchors are the useful compression boundary:
    # merge the records whose union removes the most lexical units, then bind
    # every record in that cluster to the same causal clause.  The optimizer is
    # deliberately ID/prose agnostic and its tie breaks are fully deterministic.
    term_cache: dict[tuple[int, ...], tuple[str, ...]] = {}
    phrase_cache: dict[tuple[int, ...], str] = {}
    cost_cache: dict[tuple[int, ...], int] = {}

    def cluster_terms(indices: tuple[int, ...]) -> tuple[str, ...]:
        key = tuple(sorted(indices))
        if key in term_cache:
            return term_cache[key]
        groups: list[tuple[str, ...]] = []
        for index in key:
            raw_groups = links[index][1]["required_lexeme_groups"]
            assert isinstance(raw_groups, list) and raw_groups
            for raw_group in raw_groups:
                assert isinstance(raw_group, list) and raw_group
                group = tuple(str(value) for value in raw_group)
                if group not in groups:
                    groups.append(group)
        alternatives = sorted({value for group in groups for value in group})
        covered: set[int] = set()
        chosen: list[str] = []
        while len(covered) < len(groups):
            choices: list[tuple[float, int, int, str, set[int]]] = []
            for alternative in alternatives:
                normalized = illustration_audit_module._normalized_literal_text(
                    alternative
                )
                newly_covered = {
                    group_index
                    for group_index, group in enumerate(groups)
                    if group_index not in covered
                    and any(
                        illustration_audit_module.text_contains_term(
                            normalized,
                            member,
                        )
                        for member in group
                    )
                }
                if not newly_covered:
                    continue
                lexical_cost = illustration_audit_module._universal_lexical_unit_count(
                    alternative
                )
                choices.append(
                    (
                        lexical_cost / len(newly_covered),
                        lexical_cost,
                        -len(newly_covered),
                        alternative,
                        newly_covered,
                    )
                )
            assert choices
            _ratio, _cost, _coverage, alternative, newly_covered = min(
                choices,
                key=lambda item: item[:4],
            )
            chosen.append(alternative)
            covered.update(newly_covered)

        # Greedy selection can make an earlier term redundant after a later,
        # longer authenticated alternative is chosen.  Remove only terms whose
        # deletion still covers the complete closed group set.
        for alternative in tuple(reversed(chosen)):
            remainder = list(chosen)
            remainder.remove(alternative)
            normalized_remainder = " ".join(
                illustration_audit_module._normalized_literal_text(value)
                for value in remainder
            )
            if all(
                any(
                    illustration_audit_module.text_contains_term(
                        normalized_remainder,
                        member,
                    )
                    for member in group
                )
                for group in groups
            ):
                chosen = remainder

        # Preserve every authenticated alternative while overlapping an
        # exact token suffix/prefix.  This avoids mechanically duplicating a
        # shared anchor such as ``... stable object`` + ``stable object
        # support`` and is independent of record IDs or case prose.
        while len(chosen) > 1:
            best_overlap: (
                tuple[
                    tuple[object, ...],
                    int,
                    int,
                    str,
                ]
                | None
            ) = None
            for left_index, left in enumerate(chosen):
                left_tokens = left.split()
                for right_index, right in enumerate(chosen):
                    if left_index == right_index:
                        continue
                    right_tokens = right.split()
                    overlap = max(
                        (
                            size
                            for size in range(
                                1,
                                min(len(left_tokens), len(right_tokens)) + 1,
                            )
                            if [value.casefold() for value in left_tokens[-size:]]
                            == [value.casefold() for value in right_tokens[:size]]
                        ),
                        default=0,
                    )
                    if overlap == 0:
                        continue
                    merged = " ".join((*left_tokens, *right_tokens[overlap:]))
                    rank = (
                        -overlap,
                        illustration_audit_module._universal_lexical_unit_count(merged),
                        merged,
                        left_index,
                        right_index,
                    )
                    if best_overlap is None or rank < best_overlap[0]:
                        best_overlap = (
                            rank,
                            left_index,
                            right_index,
                            merged,
                        )
            if best_overlap is None:
                break
            _rank, left_index, right_index, merged = best_overlap
            chosen = [
                value
                for index, value in enumerate(chosen)
                if index not in {left_index, right_index}
            ]
            chosen.append(merged)
        term_cache[key] = tuple(chosen)
        return term_cache[key]

    def cluster_phrase(indices: tuple[int, ...]) -> str:
        """Join authenticated terms without repeating an adjacent token run.

        Every retained term still appears after literal normalization.  The
        overlap removal is independent of case, carrier ID, and prose: it only
        removes a suffix/prefix token run already present at the join boundary.
        For example, ``stable object`` plus ``stable object support`` becomes
        ``stable object support`` while authenticating both source groups.
        """

        key = tuple(sorted(indices))
        if key in phrase_cache:
            return phrase_cache[key]
        merged: list[str] = []
        for term in cluster_terms(key):
            tokens = illustration_audit_module._normalized_literal_text(term).split()
            assert tokens
            if any(
                merged[start : start + len(tokens)] == tokens
                for start in range(len(merged) - len(tokens) + 1)
            ):
                continue
            if (
                merged
                and len(merged) <= len(tokens)
                and any(
                    tokens[start : start + len(merged)] == merged
                    for start in range(len(tokens) - len(merged) + 1)
                )
            ):
                merged = tokens
                continue
            overlap = next(
                (
                    size
                    for size in range(min(len(merged), len(tokens)), 0, -1)
                    if merged[-size:] == tokens[:size]
                ),
                0,
            )
            merged.extend(tokens[overlap:])
        assert merged
        phrase_cache[key] = " ".join(merged)
        return phrase_cache[key]

    def cluster_cost(indices: tuple[int, ...]) -> int:
        key = tuple(sorted(indices))
        if key not in cost_cache:
            # Keep optimization ranking on the conservative, uncompressed
            # source-term cost.  Boundary overlap compaction is a final prose
            # serialization step and must not change which authenticated
            # records are clustered together.
            cost_cache[key] = sum(
                illustration_audit_module._universal_lexical_unit_count(term)
                for term in cluster_terms(key)
            )
        return cost_cache[key]

    positive_indices = [
        index
        for index, (_output, carrier) in enumerate(links)
        if carrier.get("polarity") not in {"forbidden", "asserted_absence"}
    ]
    positive_clusters: list[tuple[int, ...]] = [(index,) for index in positive_indices]
    while True:
        best_merge: (
            tuple[
                tuple[int, int, tuple[int, ...], int, int],
                int,
                int,
                tuple[int, ...],
            ]
            | None
        ) = None
        for left_index, left in enumerate(positive_clusters):
            for right_index in range(left_index + 1, len(positive_clusters)):
                right = positive_clusters[right_index]
                if len(left) + len(right) > 8:
                    continue
                merged = tuple(sorted((*left, *right)))
                saving = cluster_cost(left) + cluster_cost(right) - cluster_cost(merged)
                # Zero-cost merges are retained: they can expose a later
                # three-way shared anchor while never increasing the total
                # lexical cost, and they reduce the sentence/link surface.
                if saving < 0:
                    continue
                rank = (
                    -saving,
                    cluster_cost(merged),
                    merged,
                    left_index,
                    right_index,
                )
                if best_merge is None or rank < best_merge[0]:
                    best_merge = (
                        rank,
                        left_index,
                        right_index,
                        merged,
                    )
        if best_merge is None:
            break
        _rank, left_index, right_index, merged = best_merge
        positive_clusters = [
            cluster
            for index, cluster in enumerate(positive_clusters)
            if index not in {left_index, right_index}
        ]
        positive_clusters.append(merged)
        positive_clusters.sort()

    negative_indices = [
        index
        for index, (_output, carrier) in enumerate(links)
        if carrier.get("polarity") in {"forbidden", "asserted_absence"}
    ]

    # A global ``No`` before a multi-record union does not scope negation to
    # later anchors.  Negative records therefore keep one explicit scoped
    # segment apiece; the exact multi-segment phrase may still be reused by at
    # most eight typed links without repeating it in the scene block.
    negative_clusters = [(index,) for index in negative_indices]
    used_phrases: dict[str, int] = {}
    positive_phrases: list[str] = []
    for cluster in [*positive_clusters, *negative_clusters]:
        if cluster in negative_clusters:
            phrase = "; ".join(f"No {cluster_phrase((index,))}" for index in cluster)
        else:
            phrase = cluster_phrase(cluster)
        linked_count = used_phrases.get(phrase, 0)
        if linked_count + len(cluster) > 8:
            variant_index = 2
            base_phrase = phrase
            while phrase in used_phrases:
                phrase = f"{base_phrase} variation{variant_index}"
                variant_index += 1
            linked_count = 0
        used_phrases[phrase] = linked_count + len(cluster)
        for index in cluster:
            links[index][0]["phrase"] = phrase
        if cluster not in negative_clusters:
            positive_phrases.append(phrase)

    # Salience and consequence fields are typed references to literal scene
    # evidence, not additional prose obligations.  Reuse the shortest positive
    # carrier clause so they consume no extra lexical budget.
    assert positive_phrases
    primary_phrase = min(
        positive_phrases,
        key=lambda value: (
            illustration_audit_module._universal_lexical_unit_count(value),
            value,
        ),
    )
    controlled_rest_phrase = primary_phrase
    remote_phrase = primary_phrase if remote else None
    result_record = next(
        (item for item in event_role_phrases if item["role_id"] == "result"),
        None,
    )
    consequence_phrase = (
        str(result_record["phrase"])
        if consequence_required and result_record is not None
        else primary_phrase
        if consequence_required
        else None
    )
    scene_parts = [
        *(
            str(record["phrase"])
            for records in (
                identity_phrases,
                fixed_slot_phrases,
                event_role_phrases,
                atom_phrases,
                bridge_phrases,
                resource_phrases,
            )
            for record in records
        ),
    ]
    if remote_phrase is not None:
        scene_parts.append(remote_phrase)
    if consequence_phrase is not None:
        scene_parts.append(consequence_phrase)
    scene_block = "; ".join(dict.fromkeys(scene_parts)) + "."
    evidence = {
        "schema": "illustration-universal-scene-evidence/v1",
        "scene_block_phrase": scene_block,
        "identity_core_phrases": identity_phrases,
        "fixed_slot_phrases": fixed_slot_phrases,
        "event_role_phrases": event_role_phrases,
        "atom_phrases": atom_phrases,
        "bridge_phrases": bridge_phrases,
        "resource_phrases": resource_phrases,
        "salience_phrases": {
            "primary_core_event_phrase": primary_phrase,
            "secondary_discovery_phrase": None,
            "controlled_rest_phrase": controlled_rest_phrase,
            "remote_carrier_phrase": remote_phrase,
        },
        "consequence_phrase": consequence_phrase,
    }
    return (
        {
            "schema": "subculture-illustration-composed-prompt/v3",
            "universal_scene_evidence": evidence,
        },
        scene_block,
    )


def _with_linked_evidence_phrase(
    composed: dict[str, object],
    *,
    section: str,
    id_key: str,
    record_id: str,
    phrase: str,
) -> tuple[dict[str, object], str]:
    mutated = copy.deepcopy(composed)
    evidence = mutated["universal_scene_evidence"]
    record = next(item for item in evidence[section] if item[id_key] == record_id)
    old_phrase = str(record["phrase"])
    record["phrase"] = phrase
    scene_block = str(evidence["scene_block_phrase"])
    if phrase not in scene_block:
        linked_sections = (
            "identity_core_phrases",
            "fixed_slot_phrases",
            "event_role_phrases",
            "atom_phrases",
            "bridge_phrases",
            "resource_phrases",
        )
        remaining_references = sum(
            1
            for linked_section in linked_sections
            for item in evidence[linked_section]
            if item is not record and item.get("phrase") == old_phrase
        )
        salience_references = sum(
            1
            for value in evidence["salience_phrases"].values()
            if value == old_phrase
        )
        consequence_reference = evidence.get("consequence_phrase") == old_phrase
        if (
            old_phrase in scene_block
            and remaining_references == 0
            and salience_references == 0
            and not consequence_reference
        ):
            scene_block = scene_block.replace(old_phrase, phrase, 1)
        else:
            scene_block = f"{scene_block} {phrase}"
        evidence["scene_block_phrase"] = scene_block
    return mutated, scene_block


def _with_scene_phrase(
    composed: dict[str, object],
    phrase: str,
) -> tuple[dict[str, object], str]:
    mutated = copy.deepcopy(composed)
    evidence = mutated["universal_scene_evidence"]
    scene_block = str(evidence["scene_block_phrase"])
    if phrase not in scene_block:
        scene_block = f"{scene_block} {phrase}"
        evidence["scene_block_phrase"] = scene_block
    return mutated, scene_block


class UniversalSceneDataContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.research = validate_universal_scene_research(ASSET_ROOT)
        cls.holdouts = validate_universal_scene_holdouts(ASSET_ROOT, cls.research)

    def test_research_counts_provenance_and_all_six_raw_shard_hashes(self) -> None:
        self.assertEqual(60, self.research["record_count"])
        self.assertEqual(20, self.research["topic_count"])
        self.assertEqual(40, self.research["independent_source_count"])
        self.assertEqual(167, self.research["mechanism_count"])
        self.assertEqual(220, self.research["candidate_count"])
        self.assertEqual(97, self.research["pixel_evidence_count"])
        self.assertEqual(
            {"guard": 52, "metric": 33, "router": 38, "visual_atom": 97},
            self.research["candidate_role_counts"],
        )
        self.assertEqual(6, len(self.research["shards"]))
        for shard in self.research["shards"]:
            path = ASSET_ROOT / "research_evidence_universal_scene" / shard["path"]
            self.assertEqual(
                shard["sha256"], hashlib.sha256(path.read_bytes()).hexdigest()
            )

    def test_scene_contracts_are_literal_hash_bound_and_cover_all_topics(self) -> None:
        self.assertEqual(24, self.holdouts["prompt_case_count"])
        self.assertEqual(24, self.holdouts["scene_contract_case_count"])
        self.assertEqual(6, self.holdouts["render_case_count"])
        self.assertEqual(20, self.holdouts["covered_topic_count"])
        self.assertGreater(self.holdouts["fixed_literal_count"], 0)
        self.assertGreater(self.holdouts["closed_literal_count"], 0)
        for row in self.holdouts["prompt_rows"]:
            case_id = row["case_id"]
            contract = self.holdouts["scene_contracts_by_case"][case_id]
            self.assertEqual(
                hashlib.sha256(str(row["request_ko"]).encode("utf-8")).hexdigest(),
                contract["request_text_sha256"],
            )

    def test_pre_universal_v2_and_cli_baseline_hashes_fail_closed(self) -> None:
        baseline_path = ASSET_ROOT / "universal_scene_baseline_v1.json"
        baseline = _json(baseline_path)
        legacy_contracts = baseline["legacy_contracts"]
        self.assertIsInstance(legacy_contracts, dict)
        original_loader = validator_module._load_json
        for field in (
            "current_runtime_sha256",
            "current_audit_sha256",
            "generator_cli_sha256",
            "audit_cli_sha256",
        ):
            with self.subTest(field=field):
                mutated = copy.deepcopy(baseline)
                mutated["legacy_contracts"][field] = "0" * 64

                def load_with_mutated_baseline(path: Path) -> object:
                    if path == baseline_path:
                        return mutated
                    return original_loader(path)

                with (
                    mock.patch.object(
                        validator_module,
                        "_load_json",
                        side_effect=load_with_mutated_baseline,
                    ),
                    self.assertRaisesRegex(ValidationFailure, field),
                ):
                    validate_universal_scene_holdouts(ASSET_ROOT, self.research)

    def test_executable_assets_cover_topics_and_all_typed_refs(self) -> None:
        result = validate_universal_scene_runtime_assets(
            ASSET_ROOT,
            self.research,
            self.holdouts,
        )
        self.assertEqual("pass", result["status"])
        self.assertEqual(20, result["topic_count"])
        self.assertEqual(127, result["candidate_count"])
        self.assertEqual(
            {"guard": 32, "metric": 9, "router": 21, "visual_atom": 65},
            result["role_counts"],
        )
        self.assertEqual(76, result["pixel_evidence_count"])
        self.assertEqual(4, result["prop_count"])
        self.assertGreaterEqual(result["embodiment_profile_count"], 11)
        self.assertEqual(12, result["proposal_profile_count"])
        self.assertEqual(18, result["context_distance_profile_count"])
        self.assertEqual(
            {"mapping_count": 20, "sibling_target_count": 58},
            result["visual_owner_mapping_policy"],
        )
        self.assertEqual(
            {
                "candidate_ids": ["uer_role_bearing_contact"],
                "selection_required": False,
            },
            result["fixed_prop_eligibility_policy"],
        )
        self.assertEqual(
            {
                "policy_source_contract_count": 37,
                "policy_source_contracts_sha256": (
                    "57207aee7bd2f4ffd77c6ecb0953aa7e50711efd2c6bcbf23afd01d386f0df5e"
                ),
                "guard_source_contract_count": 32,
                "guard_source_contracts_sha256": (
                    "a346b1666a33c9d26c08525e53fb5024cd7bd1d658df79b5f94aba85680a8e53"
                ),
                "cardinality_limit_count": 20,
                "cardinality_limits_sha256": (
                    "8456d99d3fc3e9006dcf23ca9ae77230fcf85e85477d4cf6d19c866bd6c9e086"
                ),
                "cardinality_limit_ids_sha256": (
                    "7ff62e93cf77e097af7c5d313d0f4ef58bfb22056f71fd9922661d4e6466ed78"
                ),
            },
            result["trace_source_authorities"],
        )

    def test_frozen_trace_source_authorities_fail_closed(self) -> None:
        candidates = _json(
            ASSET_ROOT / "illustration_universal_scene_candidates_v1.json"
        )
        compatibility = _json(
            ASSET_ROOT / "illustration_universal_compatibility_graph_v1.json"
        )
        semantic = _json(
            ASSET_ROOT / "illustration_universal_semantic_bindings_v1.json"
        )

        def validate(
            candidate_asset: dict[str, object],
            compatibility_asset: dict[str, object],
            semantic_asset: dict[str, object],
        ) -> dict[str, object]:
            return validator_module._validate_universal_trace_source_authorities(
                candidate_asset,
                compatibility_asset,
                semantic_asset,
                {
                    str(candidate["id"]): candidate
                    for candidate in candidate_asset["candidates"]
                },
            )

        self.assertEqual(
            20,
            validate(candidates, compatibility, semantic)["cardinality_limit_count"],
        )

        mutations: list[
            tuple[str, dict[str, object], dict[str, object], dict[str, object]]
        ] = []
        budget_drift = copy.deepcopy(compatibility)
        budget_drift["budgets"]["event_spines"] = 2
        mutations.append(
            (
                "budget value",
                copy.deepcopy(candidates),
                budget_drift,
                copy.deepcopy(semantic),
            )
        )
        resource_policy_drift = copy.deepcopy(compatibility)
        resource_policy_drift["resource_policy"]["same_phase_double_booking"] = "allow"
        mutations.append(
            (
                "resource policy",
                copy.deepcopy(candidates),
                resource_policy_drift,
                copy.deepcopy(semantic),
            )
        )
        per_band_remote = copy.deepcopy(compatibility)
        per_band_remote["distance_policy"]["creativity_bands"][0][
            "max_optional_remote"
        ] = 1
        mutations.append(
            (
                "per-band remote ceiling",
                copy.deepcopy(candidates),
                per_band_remote,
                copy.deepcopy(semantic),
            )
        )
        ambiguous_remote_alias = copy.deepcopy(compatibility)
        ambiguous_remote_alias["distance_policy"][
            "max_remote_or_high_load_optional_premises"
        ] = 1
        mutations.append(
            (
                "ambiguous remote alias",
                copy.deepcopy(candidates),
                ambiguous_remote_alias,
                copy.deepcopy(semantic),
            )
        )
        missing_guard_profile = copy.deepcopy(semantic)
        missing_guard_profile["guard_execution_profiles"].pop()
        mutations.append(
            (
                "missing guard profile",
                copy.deepcopy(candidates),
                copy.deepcopy(compatibility),
                missing_guard_profile,
            )
        )
        duplicate_guard_predicate = copy.deepcopy(semantic)
        duplicate_guard_predicate["guard_execution_profiles"][1]["predicate_id"] = (
            duplicate_guard_predicate["guard_execution_profiles"][0]["predicate_id"]
        )
        mutations.append(
            (
                "duplicate guard predicate",
                copy.deepcopy(candidates),
                copy.deepcopy(compatibility),
                duplicate_guard_predicate,
            )
        )
        for label, candidate_asset, compatibility_asset, semantic_asset in mutations:
            with self.subTest(label=label), self.assertRaises(ValidationFailure):
                validate(candidate_asset, compatibility_asset, semantic_asset)

    def test_asset_ref_predicate_topic_and_pair_mutations_fail_closed(self) -> None:
        candidates = _json(
            ASSET_ROOT / "illustration_universal_scene_candidates_v1.json"
        )
        compatibility = _json(
            ASSET_ROOT / "illustration_universal_compatibility_graph_v1.json"
        )

        mutations: list[tuple[str, dict[str, object], dict[str, object]]] = []
        unknown_ref = copy.deepcopy(candidates)
        unknown_ref["candidates"][0]["provenance_record_ids"].append("unknown_record")
        mutations.append(
            ("unknown research ref", unknown_ref, copy.deepcopy(compatibility))
        )

        bad_predicate = copy.deepcopy(candidates)
        bad_predicate["candidates"][0]["runtime_contract"]["requires_all"] = [
            ["slot", "action"]
        ]
        mutations.append(
            ("predicate arity", bad_predicate, copy.deepcopy(compatibility))
        )

        missing_topic = copy.deepcopy(candidates)
        missing_topic["topic_contributions"].pop(
            next(iter(missing_topic["topic_contributions"]))
        )
        mutations.append(
            ("topic coverage", missing_topic, copy.deepcopy(compatibility))
        )

        pair_matrix = copy.deepcopy(compatibility)
        pair_matrix["pair_matrix"] = []
        mutations.append(("pair matrix", copy.deepcopy(candidates), pair_matrix))

        proposal_ref = copy.deepcopy(candidates)
        proposal_ref["proposal_profiles"][0]["candidate_ids"].append(
            "unknown_proposal_candidate"
        )
        mutations.append(
            ("proposal candidate ref", proposal_ref, copy.deepcopy(compatibility))
        )

        proposal_pixel = copy.deepcopy(candidates)
        proposal_pixel["proposal_profiles"][0]["pixel_evidence_ids"].pop()
        mutations.append(
            ("proposal pixel coverage", proposal_pixel, copy.deepcopy(compatibility))
        )

        creativity_gate = copy.deepcopy(candidates)
        creativity_gate["proposal_profiles"][0]["requires_all"].append(
            ["context", "creativity", "high"]
        )
        mutations.append(
            (
                "creativity-dependent eligibility",
                creativity_gate,
                copy.deepcopy(compatibility),
            )
        )

        context_ref = copy.deepcopy(candidates)
        context_ref["context_distance_profiles"][0]["candidate_ids"].append(
            "unknown_context_carrier"
        )
        mutations.append(
            ("context carrier ref", context_ref, copy.deepcopy(compatibility))
        )

        context_pixel = copy.deepcopy(candidates)
        context_pixel["context_distance_profiles"][0]["pixel_evidence_ids"].pop()
        mutations.append(
            ("context pixel coverage", context_pixel, copy.deepcopy(compatibility))
        )

        holdout_gate = copy.deepcopy(candidates)
        holdout_gate["context_distance_profiles"][0]["requires_all"].append(
            ["context", "case_id", "universal_scene_07"]
        )
        mutations.append(
            ("context holdout gate", holdout_gate, copy.deepcopy(compatibility))
        )

        candidate_bridge_escape = copy.deepcopy(candidates)
        bridge_candidate = next(
            candidate
            for candidate in candidate_bridge_escape["candidates"]
            if candidate["role"] == "visual_atom"
            and candidate["runtime_contract"]["bridge_types"]
        )
        bridge_candidate["runtime_contract"]["bridge_types"].append("capability")
        mutations.append(
            (
                "candidate bridge closed-enum escape",
                candidate_bridge_escape,
                copy.deepcopy(compatibility),
            )
        )

        profile_bridge_escape = copy.deepcopy(candidates)
        profile_bridge_escape["proposal_profiles"][0]["bridge_types"].append(
            "capability"
        )
        mutations.append(
            (
                "profile bridge closed-enum escape",
                profile_bridge_escape,
                copy.deepcopy(compatibility),
            )
        )

        compatibility_bridge_escape = copy.deepcopy(compatibility)
        compatibility_bridge_escape["bridge_policy"]["bridge_type_ids"].append(
            "capability"
        )
        mutations.append(
            (
                "compatibility bridge closed-enum escape",
                copy.deepcopy(candidates),
                compatibility_bridge_escape,
            )
        )

        duplicated_resource_kind = copy.deepcopy(compatibility)
        duplicated_resource_kind["resource_kind_ids"].append("mouth")
        mutations.append(
            (
                "compatibility duplicate resource kind",
                copy.deepcopy(candidates),
                duplicated_resource_kind,
            )
        )

        missing_decision_reason = copy.deepcopy(compatibility)
        missing_decision_reason["decision_reason_code_ids"].remove(
            "capability_unsatisfied"
        )
        mutations.append(
            (
                "missing frozen decision reason",
                copy.deepcopy(candidates),
                missing_decision_reason,
            )
        )

        reordered_decision_reasons = copy.deepcopy(compatibility)
        reordered_decision_reasons["decision_reason_code_ids"][0:2] = reversed(
            reordered_decision_reasons["decision_reason_code_ids"][0:2]
        )
        mutations.append(
            (
                "reordered frozen decision reasons",
                copy.deepcopy(candidates),
                reordered_decision_reasons,
            )
        )

        trace_budget_drift = copy.deepcopy(compatibility)
        trace_budget_drift["budgets"]["event_spines"] = 2
        mutations.append(
            (
                "trace budget source drift",
                copy.deepcopy(candidates),
                trace_budget_drift,
            )
        )

        trace_resource_policy_drift = copy.deepcopy(compatibility)
        trace_resource_policy_drift["resource_policy"]["same_phase_double_booking"] = (
            "allow"
        )
        mutations.append(
            (
                "trace resource-policy source drift",
                copy.deepcopy(candidates),
                trace_resource_policy_drift,
            )
        )

        universal_rule_reason_drift = copy.deepcopy(compatibility)
        universal_rule_reason_drift["universal_rules"][0]["reason_code"] = (
            "rule_satisfied"
        )
        mutations.append(
            (
                "universal-rule reason source drift",
                copy.deepcopy(candidates),
                universal_rule_reason_drift,
            )
        )

        universal_rule_allow = copy.deepcopy(compatibility)
        universal_rule_allow["universal_rules"][0]["outcome"] = "allow"
        mutations.append(
            (
                "universal-rule allow outcome escape",
                copy.deepcopy(candidates),
                universal_rule_allow,
            )
        )

        semantic_null_collision = copy.deepcopy(candidates)
        semantic_null_collision["proposal_profiles"][0]["event_roles"]["recipient"] = (
            "null"
        )
        mutations.append(
            (
                "semantic-family literal null collision",
                semantic_null_collision,
                copy.deepcopy(compatibility),
            )
        )

        quiet_profile_load = copy.deepcopy(candidates)
        next(
            profile
            for profile in quiet_profile_load["context_distance_profiles"]
            if profile["id"] == "context_quiet_theme_guard_middle"
        )["load_profile"]["theme_displacement"] = 1
        mutations.append(
            (
                "quiet-theme profile displacement load",
                quiet_profile_load,
                copy.deepcopy(compatibility),
            )
        )

        quiet_profile_distance = copy.deepcopy(candidates)
        next(
            profile
            for profile in quiet_profile_distance["context_distance_profiles"]
            if profile["id"] == "context_quiet_theme_guard_middle"
        )["distance_profile"]["theme"] = 1
        mutations.append(
            (
                "quiet-theme profile distance",
                quiet_profile_distance,
                copy.deepcopy(compatibility),
            )
        )

        quiet_carrier_load = copy.deepcopy(candidates)
        quiet_profile = next(
            profile
            for profile in quiet_carrier_load["context_distance_profiles"]
            if profile["id"] == "context_quiet_theme_guard_middle"
        )
        quiet_carrier = next(
            candidate
            for candidate in quiet_carrier_load["candidates"]
            if candidate["id"] == quiet_profile["candidate_ids"][0]
        )
        quiet_carrier["semantic_load"]["theme_displacement"] = 1
        quiet_carrier["runtime_contract"]["load_profile"]["theme_displacement"] = 1
        mutations.append(
            (
                "quiet-theme carrier displacement load",
                quiet_carrier_load,
                copy.deepcopy(compatibility),
            )
        )

        fixed_prop_reverted = copy.deepcopy(candidates)
        next(
            candidate
            for candidate in fixed_prop_reverted["candidates"]
            if candidate["id"] == "uer_role_bearing_contact"
        )["triggers"] = [["slot", "prop", "open"]]
        mutations.append(
            (
                "fixed-prop generic carrier trigger reverted",
                fixed_prop_reverted,
                copy.deepcopy(compatibility),
            )
        )

        fixed_prop_named_escape = copy.deepcopy(candidates)
        named_prop_candidate = next(
            candidate
            for candidate in fixed_prop_named_escape["candidates"]
            if candidate["id"] == "uao_global_prop_apple"
        )
        named_prop_candidate["triggers"].append(["slot", "prop", "open_or_fixed"])
        mutations.append(
            (
                "fixed-prop named carrier whitelist escape",
                fixed_prop_named_escape,
                copy.deepcopy(compatibility),
            )
        )

        for label, candidate_asset, compatibility_asset in mutations:
            with self.subTest(label=label):

                def injected_load(path: Path) -> dict[str, object]:
                    if path.name == "illustration_universal_scene_candidates_v1.json":
                        return candidate_asset
                    if (
                        path.name
                        == "illustration_universal_compatibility_graph_v1.json"
                    ):
                        return compatibility_asset
                    return _json(path)

                with mock.patch.object(
                    validator_module,
                    "_load_json",
                    side_effect=injected_load,
                ):
                    with self.assertRaises(ValidationFailure):
                        validate_universal_scene_runtime_assets(
                            ASSET_ROOT,
                            self.research,
                            self.holdouts,
                        )

    def test_semantic_effect_registry_is_independently_empty_for_all_126_sources(
        self,
    ) -> None:
        candidates = _json(
            ASSET_ROOT / "illustration_universal_scene_candidates_v1.json"
        )
        compatibility = _json(
            ASSET_ROOT / "illustration_universal_compatibility_graph_v1.json"
        )
        semantic = _json(
            ASSET_ROOT / "illustration_universal_semantic_bindings_v1.json"
        )
        policy = validator_module._validate_universal_semantic_effect_policy(
            candidates,
            compatibility,
            semantic,
        )
        self.assertEqual(126, policy["profile_count"])
        self.assertEqual(0, policy["nonempty_effect_profile_count"])

        contract_effects = semantic["contract_effect_profiles"]
        positive_paraphrases = {
            "살색의 다섯 손가락 집게가 돋아나": "human_hand_attachment",
            "a flesh colored palm sprouts": "human_hand_attachment",
            "肌色の五本指の把持器が生える": "human_hand_attachment",
            "长出肤色五指抓握器": "human_hand_attachment",
        }
        for phrase, expected_effect in positive_paraphrases.items():
            with self.subTest(phrase=phrase):
                self.assertIn(
                    expected_effect,
                    validator_module._classify_universal_contract_effects(
                        [phrase],
                        contract_effects,
                    ),
                )
        for phrase in (
            "살색의 다섯 손가락 집게가 돋아나지 않는다",
            "a flesh colored palm does not sprout",
            "肌色の五本指の把持器が生えない",
            "不要长出肤色五指抓握器",
            "사람 손을 붙이는 대신 날개를 사용",
            "instead of attaching human hands, use wings",
            "人間の手を付ける代わりに翼を使う",
            "人間の手を付けるのではなく翼を使う",
            "使用翅膀，而不是添加人手",
            "不是添加人手，而是使用翅膀",
        ):
            with self.subTest(negative_phrase=phrase):
                self.assertNotIn(
                    "human_hand_attachment",
                    validator_module._classify_universal_contract_effects(
                        [phrase],
                        contract_effects,
                    ),
                )

        self.assertNotIn(
            "navigation_instrument_use",
            validator_module._classify_universal_contract_effects(
                ["나침반을 길 찾는 도구가 아니라 장면의 증거로만 사용"],
                contract_effects,
            ),
        )
        self.assertIn(
            "human_hand_attachment",
            validator_module._classify_universal_contract_effects(
                ["use wings, then attach human hands"],
                contract_effects,
            ),
        )
        self.assertIn(
            "human_hand_attachment",
            validator_module._classify_universal_contract_effects(
                ["添加人手，而不是使用翅膀"],
                contract_effects,
            ),
        )
        for phrase in (
            "사람 손을 붙여 날개 대신 사용한다",
            "사람 손을 붙여, 날개 대신 사용한다",
        ):
            self.assertIn(
                "human_hand_attachment",
                validator_module._classify_universal_contract_effects(
                    [phrase],
                    contract_effects,
                ),
            )

        negative_clause = {
            "ko": lambda phrase: f"{phrase} 금지",
            "en": lambda phrase: f"do not include {phrase}",
            "ja": lambda phrase: f"{phrase} 禁止",
            "zh": lambda phrase: f"不要{phrase}",
        }
        runtime_candidates = copy.deepcopy(candidates)
        runtime_compatibility = copy.deepcopy(compatibility)
        semantic_hash = universal_runtime_module.canonical_sha256(semantic)
        runtime_candidates["semantic_bindings_asset_sha256"] = semantic_hash
        runtime_compatibility["semantic_bindings_asset_sha256"] = semantic_hash
        runtime_assets = universal_runtime_module.validate_universal_scene_assets(
            runtime_candidates,
            runtime_compatibility,
            semantic_bindings_asset=semantic,
        )
        base_prompt = _jsonl(ASSET_ROOT / "universal_scene_prompt_holdout_v1.jsonl")[0]
        base_oracle = _jsonl(ASSET_ROOT / "universal_scene_current_holdout_v2.jsonl")[0]
        validated_runtime_contract = universal_runtime_module.validate_scene_contract(
            str(base_prompt["request_ko"]),
            base_oracle["canonical_scene_contract"],
            assets=runtime_assets,
        )
        visual_source = next(
            item for item in candidates["candidates"] if item["role"] == "visual_atom"
        )
        for profile in contract_effects:
            effect_id = profile["effect_id"]
            for aliases in profile["literal_aliases"]:
                locale = aliases["locale"]
                positive = aliases["values"][0]
                negative = negative_clause[locale](positive)
                corpora = {
                    "negative_then_positive": f"{negative}. {positive}.",
                    "positive_then_negative": f"{positive}. {negative}.",
                    "all_negative": f"{negative}. {negative}.",
                }
                for order, corpus in corpora.items():
                    with self.subTest(
                        effect_id=effect_id,
                        locale=locale,
                        order=order,
                    ):
                        classified = (
                            validator_module._classify_universal_contract_effects(
                                [corpus],
                                contract_effects,
                            )
                        )
                        runtime_projection = universal_runtime_module._contract_effect_projection_records(
                            request_text=corpus,
                            validated=validated_runtime_contract,
                            assets=runtime_assets,
                        )
                        runtime_effects = {
                            effect["effect_id"]
                            for item in runtime_projection
                            if item["instance_id"] == "request::concept"
                            for effect in item["effect_occurrences"]
                        }
                        self.assertEqual(
                            classified,
                            runtime_effects,
                            (effect_id, locale, order, corpus),
                        )
                        if order == "all_negative":
                            self.assertNotIn(effect_id, classified)
                        else:
                            self.assertIn(effect_id, classified)

                        mutated_candidates = copy.deepcopy(candidates)
                        mutated_visual = next(
                            item
                            for item in mutated_candidates["candidates"]
                            if item["id"] == visual_source["id"]
                        )
                        mutated_visual["definition"] = corpus
                        if order == "all_negative":
                            validator_module._validate_universal_semantic_effect_policy(
                                mutated_candidates,
                                compatibility,
                                semantic,
                            )
                        else:
                            with self.assertRaises(ValidationFailure):
                                validator_module._validate_universal_semantic_effect_policy(
                                    mutated_candidates,
                                    compatibility,
                                    semantic,
                                )

        coordinated_corpora = {
            "ko": lambda phrase: {
                "shared_negative_scope": (
                    f"{phrase} 금지 그리고 {phrase} 금지",
                    False,
                ),
                "independent_reassertion": (
                    f"{phrase} 금지 그러나 장면은 {phrase}",
                    True,
                ),
            },
            "en": lambda phrase: {
                "shared_negative_scope": (
                    f"do not include {phrase} and repeat {phrase}",
                    False,
                ),
                "independent_reassertion": (
                    f"do not include {phrase} and the scene explicitly includes {phrase}",
                    True,
                ),
            },
            "ja": lambda phrase: {
                "shared_negative_scope": (
                    f"{phrase} 禁止 そして {phrase} 禁止",
                    False,
                ),
                "independent_reassertion": (
                    f"{phrase} 禁止 しかし場面は {phrase}",
                    True,
                ),
            },
            "zh": lambda phrase: {
                "shared_negative_scope": (
                    f"不要包含{phrase}并且重复{phrase}",
                    False,
                ),
                "independent_reassertion": (
                    f"不要包含{phrase}但是场景明确包含{phrase}",
                    True,
                ),
            },
        }
        for profile in contract_effects:
            effect_id = profile["effect_id"]
            for aliases in profile["literal_aliases"]:
                locale = aliases["locale"]
                positive = aliases["values"][0]
                for order, (corpus, expected_positive) in coordinated_corpora[locale](
                    positive
                ).items():
                    with self.subTest(
                        coordinated_effect_id=effect_id,
                        locale=locale,
                        order=order,
                    ):
                        classified = (
                            validator_module._classify_universal_contract_effects(
                                [corpus],
                                contract_effects,
                            )
                        )
                        runtime_projection = universal_runtime_module._contract_effect_projection_records(
                            request_text=corpus,
                            validated=validated_runtime_contract,
                            assets=runtime_assets,
                        )
                        runtime_effects = {
                            effect["effect_id"]
                            for item in runtime_projection
                            if item["instance_id"] == "request::concept"
                            for effect in item["effect_occurrences"]
                        }
                        self.assertEqual(
                            classified,
                            runtime_effects,
                            (effect_id, locale, order, corpus),
                        )
                        self.assertEqual(
                            expected_positive,
                            effect_id in classified,
                            (effect_id, locale, order, corpus),
                        )

        for corpus in (
            "No weapon fires. A weapon fires a round.",
            "Weapon firing must not appear and the weapon fires a round.",
            "No weapon fires — a weapon fires a round.",
            "No weapon fires—A weapon fires a round.",
        ):
            with self.subTest(mixed_occurrence_corpus=corpus):
                self.assertIn(
                    "active_weapon_discharge",
                    validator_module._classify_universal_contract_effects(
                        [corpus],
                        contract_effects,
                    ),
                )
        for corpus in (
            "No weapon fires. No weapon fires a round.",
            "Weapon firing must not appear and weapon firing must not appear.",
            "Do not fire the machine gun and shoot the gun.",
            "No weapon fires — no weapon fires a round.",
            "No weapon fires—no weapon fires a round.",
        ):
            with self.subTest(all_negative_corpus=corpus):
                self.assertNotIn(
                    "active_weapon_discharge",
                    validator_module._classify_universal_contract_effects(
                        [corpus],
                        contract_effects,
                    ),
                )

        semantic_source_mutations = []
        candidate_meaning = copy.deepcopy(candidates)
        visual = next(
            item
            for item in candidate_meaning["candidates"]
            if item["role"] == "visual_atom"
        )
        visual["definition"] = "A flesh colored five digit hand sprouts from the actor."
        semantic_source_mutations.append(candidate_meaning)
        for mutated_candidates in semantic_source_mutations:
            with self.assertRaises(ValidationFailure):
                validator_module._validate_universal_semantic_effect_policy(
                    mutated_candidates,
                    compatibility,
                    semantic,
                )

        for source_kind, effect_id in (
            ("context_profile", "scene_promise_hijack"),
            ("resource_kind", "human_hand_attachment"),
        ):
            with self.subTest(source_kind=source_kind, effect_id=effect_id):
                mutated = copy.deepcopy(semantic)
                profile = next(
                    row
                    for row in mutated["semantic_effect_registry"]["profiles"]
                    if row["source_kind"] == source_kind
                )
                profile["effect_ids"] = [effect_id]
                # Cross-file container hashes can be refreshed, but this
                # independent semantic policy remains authoritative.
                with self.assertRaises(ValidationFailure):
                    validator_module._validate_universal_semantic_effect_policy(
                        candidates,
                        compatibility,
                        mutated,
                    )

    def test_literal_visual_realization_profiles_are_exact_and_fail_closed(
        self,
    ) -> None:
        candidates = _json(
            ASSET_ROOT / "illustration_universal_scene_candidates_v1.json"
        )
        compatibility = _json(
            ASSET_ROOT / "illustration_universal_compatibility_graph_v1.json"
        )
        semantic = _json(
            ASSET_ROOT / "illustration_universal_semantic_bindings_v1.json"
        )
        candidate_by_id = {str(item["id"]): item for item in candidates["candidates"]}
        result = validator_module._validate_universal_literal_realization_profiles(
            semantic,
            candidate_by_id,
            compatibility["resource_kind_ids"],
        )
        self.assertEqual(
            {"profile_count": 19, "candidate_owner_count": 19},
            result,
        )

        def assert_mutation_rejects(mutator: object) -> None:
            mutated_semantic = copy.deepcopy(semantic)
            mutated_candidates = copy.deepcopy(candidate_by_id)
            mutator(mutated_semantic, mutated_candidates)
            with self.assertRaises(ValidationFailure):
                validator_module._validate_universal_literal_realization_profiles(
                    mutated_semantic,
                    mutated_candidates,
                    compatibility["resource_kind_ids"],
                )

        def empty_groups(asset: dict[str, object], _candidates: object) -> None:
            asset["literal_visual_realization_profiles"][0][
                "required_literal_groups"
            ] = []

        def add_case_fingerprint(asset: dict[str, object], _candidates: object) -> None:
            asset["literal_visual_realization_profiles"][0]["case_id"] = (
                "universal_scene_06_explicit_machine_gun"
            )

        def wrong_slot_facet(asset: dict[str, object], _candidates: object) -> None:
            asset["literal_visual_realization_profiles"][0]["realized_facet"] = "prop"

        def duplicate_candidate_owner(
            asset: dict[str, object], _candidates: object
        ) -> None:
            asset["literal_visual_realization_profiles"][1]["candidate_group"] = asset[
                "literal_visual_realization_profiles"
            ][0]["candidate_group"]

        def reorder_participants(asset: dict[str, object], _candidates: object) -> None:
            profile = next(
                item
                for item in asset["literal_visual_realization_profiles"]
                if item["id"] == "lvr_protective_recipient_path"
            )
            profile["participant_roles"].reverse()

        def orphan_owned_pixel(asset: dict[str, object], _candidates: object) -> None:
            asset["literal_visual_realization_profiles"][0]["owned_pixel_kinds"] = [
                "residue"
            ]

        def owner_candidate_facet_drift(
            asset: dict[str, object],
            candidate_map: dict[str, object],
        ) -> None:
            candidate_id = asset["literal_visual_realization_profiles"][0][
                "candidate_group"
            ][0]
            candidate_map[candidate_id]["facet"] = "prop"

        def mallet_sense_targets_banana(
            asset: dict[str, object], _candidates: object
        ) -> None:
            asset["prop_literal_sense_bindings"][0]["catalog_prop_id"] = "prop_banana"

        def mallet_activation_disabled(
            asset: dict[str, object], _candidates: object
        ) -> None:
            asset["prop_literal_sense_bindings"][0]["activation_target"] = None

        def contact_commitment_group_missing(
            asset: dict[str, object],
            _candidates: object,
        ) -> None:
            profile = next(
                item
                for item in asset["literal_visual_realization_profiles"]
                if item["id"] == "lvr_insert_resistance_contact_commitment"
            )
            profile["required_literal_groups"].pop()

        def contact_commitment_polarity_flip(
            asset: dict[str, object],
            _candidates: object,
        ) -> None:
            profile = next(
                item
                for item in asset["literal_visual_realization_profiles"]
                if item["id"] == "lvr_insert_resistance_contact_commitment"
            )
            profile["required_literal_groups"][0]["required_polarity"] = "negated"

        def contact_commitment_candidate_swap(
            asset: dict[str, object],
            _candidates: object,
        ) -> None:
            profile = next(
                item
                for item in asset["literal_visual_realization_profiles"]
                if item["id"] == "lvr_insert_resistance_contact_commitment"
            )
            profile["candidate_group"] = ["action_temporal_phases_release_recovery"]

        for label, mutator in (
            ("empty fixed catch-all groups", empty_groups),
            ("case fingerprint field", add_case_fingerprint),
            ("wrong slot-facet adjacency", wrong_slot_facet),
            ("duplicate matching candidate owner", duplicate_candidate_owner),
            ("participant role order drift", reorder_participants),
            ("orphan owned pixel", orphan_owned_pixel),
            ("candidate facet drift", owner_candidate_facet_drift),
            ("wooden mallet sense targets banana", mallet_sense_targets_banana),
            ("wooden mallet activation disabled", mallet_activation_disabled),
            ("contact commitment group missing", contact_commitment_group_missing),
            ("contact commitment polarity flip", contact_commitment_polarity_flip),
            ("contact commitment candidate swap", contact_commitment_candidate_swap),
        ):
            with self.subTest(label=label):
                assert_mutation_rejects(mutator)

    def test_quiet_theme_source_is_independently_zero_displacement(self) -> None:
        candidates = _json(
            ASSET_ROOT / "illustration_universal_scene_candidates_v1.json"
        )
        candidate_by_id = {str(item["id"]): item for item in candidates["candidates"]}
        profile = next(
            item
            for item in candidates["context_distance_profiles"]
            if item["id"] == "context_quiet_theme_guard_middle"
        )
        validator_module._validate_universal_quiet_theme_source_contract(
            profile,
            candidate_by_id,
        )

        profile_load = copy.deepcopy(profile)
        profile_load["load_profile"]["theme_displacement"] = 1
        with self.assertRaises(ValidationFailure):
            validator_module._validate_universal_quiet_theme_source_contract(
                profile_load,
                candidate_by_id,
            )

        profile_distance = copy.deepcopy(profile)
        profile_distance["distance_profile"]["theme"] = 1
        with self.assertRaises(ValidationFailure):
            validator_module._validate_universal_quiet_theme_source_contract(
                profile_distance,
                candidate_by_id,
            )

        mutated_candidates = copy.deepcopy(candidate_by_id)
        carrier_id = profile["candidate_ids"][0]
        mutated_candidates[carrier_id]["runtime_contract"]["load_profile"][
            "theme_displacement"
        ] = 1
        with self.assertRaises(ValidationFailure):
            validator_module._validate_universal_quiet_theme_source_contract(
                profile,
                mutated_candidates,
            )

    def test_fixed_prop_eligibility_uses_only_the_generic_carrier(self) -> None:
        candidates = _json(
            ASSET_ROOT / "illustration_universal_scene_candidates_v1.json"
        )
        candidate_by_id = {str(item["id"]): item for item in candidates["candidates"]}
        self.assertEqual(
            {
                "candidate_ids": ["uer_role_bearing_contact"],
                "selection_required": False,
            },
            validator_module._validate_universal_fixed_prop_eligibility_source_contract(
                candidate_by_id
            ),
        )

        reverted = copy.deepcopy(candidate_by_id)
        reverted["uer_role_bearing_contact"]["triggers"] = [["slot", "prop", "open"]]
        with self.assertRaises(ValidationFailure):
            validator_module._validate_universal_fixed_prop_eligibility_source_contract(
                reverted
            )

        named_escape = copy.deepcopy(candidate_by_id)
        named_escape["uao_global_prop_apple"]["triggers"].append(
            ["slot", "prop", "open_or_fixed"]
        )
        with self.assertRaises(ValidationFailure):
            validator_module._validate_universal_fixed_prop_eligibility_source_contract(
                named_escape
            )

    def test_existing_render_manifests_keep_historical_failure_labels(self) -> None:
        result = validate_all(str(ASSET_ROOT), verify_local_images=False)
        self.assertEqual("pass", result["status"])
        self.assertEqual(
            ("partial", 1, 5, 6),
            (
                result["render_qualification"]["qualification_status"],
                result["render_qualification"]["failed_case_count"],
                result["render_qualification"]["passed_case_count"],
                result["render_qualification"]["case_count"],
            ),
        )
        self.assertEqual(
            ("partial", 1, 2, 1),
            (
                result["render_v2_qualification"]["qualification_status"],
                result["render_v2_qualification"]["failed_case_count"],
                result["render_v2_qualification"]["attempt_count"],
                result["render_v2_qualification"]["repair_count"],
            ),
        )
        self.assertEqual(
            ("pass", 0, 1, 0),
            (
                result["render_v3_qualification"]["qualification_status"],
                result["render_v3_qualification"]["failed_case_count"],
                result["render_v3_qualification"]["attempt_count"],
                result["render_v3_qualification"]["repair_count"],
            ),
        )


class UniversalSceneCurrentOracleV2Tests(unittest.TestCase):
    ORACLE_FILES = (
        "universal_scene_prompt_holdout_v1.jsonl",
        "universal_scene_contract_holdout_v1.jsonl",
        "universal_scene_contract_holdout_v2.jsonl",
        "universal_scene_baseline_v1.json",
        "universal_scene_current_holdout_v2.jsonl",
        "universal_scene_expectation_crosswalk_v2.json",
        "universal_scene_current_holdout_v2_manifest.json",
        "universal_scene_baseline_v2.json",
    )
    HISTORICAL_FIXED_ROLE_ROWS = [
        (
            "universal_scene_04_explicit_apple",
            "instrument",
            "small_kitchen_knife",
            "/expected_event_frame/fixed_roles/instrument",
        ),
        (
            "universal_scene_05_explicit_hammer",
            "result",
            "mount_partially_reseated",
            "/expected_event_frame/fixed_roles/result",
        ),
        (
            "universal_scene_06_explicit_machine_gun",
            "instrument",
            "gloved_hands",
            "/expected_event_frame/fixed_roles/instrument",
        ),
        (
            "universal_scene_06_explicit_machine_gun",
            "result",
            "safe_transport_readiness_assessed",
            "/expected_event_frame/fixed_roles/result",
        ),
        (
            "universal_scene_07_fixed_facial_motion",
            "result",
            "fault_noticed",
            "/expected_event_frame/fixed_roles/result",
        ),
        (
            "universal_scene_08_ambiguous_display_affect",
            "result",
            "message_handoff_pending",
            "/expected_event_frame/fixed_roles/result",
        ),
        (
            "universal_scene_09_shared_attention",
            "result",
            "shared_hypothesis_and_next_move",
            "/expected_event_frame/fixed_roles/result",
        ),
        (
            "universal_scene_10_pose_support",
            "instrument",
            "rope_and_body_weight",
            "/expected_event_frame/fixed_roles/instrument",
        ),
        (
            "universal_scene_10_pose_support",
            "result",
            "crate_moves_while_beam_flexes",
            "/expected_event_frame/fixed_roles/result",
        ),
        (
            "universal_scene_11_gesture_function",
            "result",
            "colleague_halts_before_hazard",
            "/expected_event_frame/fixed_roles/result",
        ),
        (
            "universal_scene_12_nonhuman_display",
            "result",
            "reduced_wind_on_climber",
            "/expected_event_frame/fixed_roles/result",
        ),
        (
            "universal_scene_17_relation_topology",
            "recipient",
            "axis_holder",
            "/expected_event_frame/fixed_roles/recipient",
        ),
        (
            "universal_scene_18_prop_lexical_normalization",
            "result",
            "root_fragments_in_mortar",
            "/expected_event_frame/fixed_roles/result",
        ),
        (
            "universal_scene_22_theme_hijack_guard",
            "result",
            "orders_sorted",
            "/expected_event_frame/fixed_roles/result",
        ),
    ]

    @staticmethod
    def _write_json(path: Path, value: object) -> None:
        path.write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
        path.write_text(
            "".join(
                json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
                for row in rows
            ),
            encoding="utf-8",
        )

    def _copy_oracle(self, destination: Path) -> None:
        for filename in self.ORACLE_FILES:
            shutil.copy2(ASSET_ROOT / filename, destination / filename)

    def _assert_semantic_mutation_rejected(self, mutate: object) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._copy_oracle(root)
            mutate(root)
            prompt_digest = hashlib.sha256(
                (root / "universal_scene_prompt_holdout_v1.jsonl").read_bytes()
            ).hexdigest()
            contract_digest = hashlib.sha256(
                (root / "universal_scene_contract_holdout_v1.jsonl").read_bytes()
            ).hexdigest()
            current_contract_digest = hashlib.sha256(
                (root / "universal_scene_contract_holdout_v2.jsonl").read_bytes()
            ).hexdigest()
            current_digest = hashlib.sha256(
                (root / "universal_scene_current_holdout_v2.jsonl").read_bytes()
            ).hexdigest()
            crosswalk_digest = hashlib.sha256(
                (root / "universal_scene_expectation_crosswalk_v2.json").read_bytes()
            ).hexdigest()

            manifest_path = root / "universal_scene_current_holdout_v2_manifest.json"
            manifest = _json(manifest_path)
            manifest["source_lineage"]["prompt_holdout"]["sha256"] = prompt_digest
            manifest["source_lineage"]["historical_scene_contract_holdout"][
                "sha256"
            ] = contract_digest
            manifest["source_lineage"]["current_scene_contract_holdout"]["sha256"] = (
                current_contract_digest
            )
            manifest["artifacts"]["current_holdout"]["sha256"] = current_digest
            manifest["artifacts"]["crosswalk"]["sha256"] = crosswalk_digest
            self._write_json(manifest_path, manifest)
            manifest_digest = hashlib.sha256(manifest_path.read_bytes()).hexdigest()

            baseline_path = root / "universal_scene_baseline_v2.json"
            baseline = _json(baseline_path)
            baseline["source_lineage"]["prompt_holdout"]["sha256"] = prompt_digest
            baseline["source_lineage"]["historical_scene_contract_holdout"][
                "sha256"
            ] = contract_digest
            baseline["source_lineage"]["current_scene_contract_holdout"]["sha256"] = (
                current_contract_digest
            )
            baseline["current_oracle"]["current_holdout"]["sha256"] = current_digest
            baseline["current_oracle"]["crosswalk"]["sha256"] = crosswalk_digest
            baseline["current_oracle"]["manifest"]["sha256"] = manifest_digest
            baseline["compiled_obligations"]["obligation_reference_count"] = manifest[
                "counts"
            ]["compiled_obligation_reference_count"]
            baseline["compiled_obligations"]["per_row_unique_obligation_count_sum"] = (
                manifest["counts"]["compiled_obligation_per_row_unique_count_sum"]
            )
            baseline["compiled_obligations"]["global_unique_obligation_count"] = (
                manifest["counts"]["compiled_obligation_global_unique_count"]
            )
            baseline["validator_contract"]["sha256"] = hashlib.sha256(
                Path(validator_module.__file__).read_bytes()
            ).hexdigest()
            self._write_json(baseline_path, baseline)

            with (
                mock.patch.multiple(
                    validator_module,
                    UNIVERSAL_V1_PROMPT_HOLDOUT_SHA256=prompt_digest,
                    UNIVERSAL_V1_SCENE_CONTRACT_HOLDOUT_SHA256=contract_digest,
                    UNIVERSAL_V2_SCENE_CONTRACT_HOLDOUT_SHA256=current_contract_digest,
                    UNIVERSAL_V2_CURRENT_HOLDOUT_SHA256=current_digest,
                    UNIVERSAL_V2_EXPECTATION_CROSSWALK_SHA256=crosswalk_digest,
                    UNIVERSAL_V2_CURRENT_MANIFEST_SHA256=manifest_digest,
                ),
                self.assertRaises(ValidationFailure),
            ):
                validate_universal_scene_current_oracle_v2(root)

    def test_current_oracle_exact_projection_lineage_and_mapping_totals(self) -> None:
        result = validate_universal_scene_current_oracle_v2(ASSET_ROOT)
        self.assertEqual(24, result["case_count"])
        self.assertEqual(144, result["projected_slot_count"])
        self.assertEqual(192, result["projected_event_role_count"])
        self.assertEqual(229, result["resolution_ledger_entry_count"])
        self.assertEqual(424, result["compiled_obligation_reference_count"])
        self.assertEqual(403, result["compiled_obligation_per_row_unique_count_sum"])
        self.assertEqual(178, result["compiled_obligation_global_unique_count"])
        self.assertEqual(9, result["guard_source_contract_count"])
        self.assertEqual(30, result["event_mapping_count"])
        self.assertEqual(35, result["bridge_mapping_count"])
        self.assertEqual(7, result["closed_runtime_bridge_type_count"])

        current_rows = _jsonl(ASSET_ROOT / "universal_scene_current_holdout_v2.jsonl")
        prompt_rows = _jsonl(ASSET_ROOT / "universal_scene_prompt_holdout_v1.jsonl")
        contract_rows = _jsonl(ASSET_ROOT / "universal_scene_contract_holdout_v2.jsonl")
        for current, prompt, wrapper in zip(current_rows, prompt_rows, contract_rows):
            self.assertEqual(prompt, current["legacy_prompt_record"])
            self.assertEqual(
                wrapper["scene_contract"], current["canonical_scene_contract"]
            )
            self.assertEqual(
                wrapper["scene_contract"]["slot_states"],
                current["canonical_projection"]["slot_states"],
            )
            self.assertEqual(
                wrapper["scene_contract"]["event_roles"],
                current["canonical_projection"]["event_roles"],
            )
            self.assertEqual(6, len(current["canonical_projection"]["slot_states"]))
            self.assertEqual(8, len(current["canonical_projection"]["event_roles"]))
        self.assertEqual(
            {
                "absent_atom_facet_v1",
                "absent_blocked_semantic_v1",
                "absent_event_role_v1",
                "absent_resource_kind_v1",
                "absent_slot_materialization_v1",
                "canonical_context_profile_projection_v1",
                "canonical_embodiment_profile_projection_v1",
                "canonical_event_role_projection_v1",
                "canonical_slot_projection_v1",
                "eligible_atom_facet_v1",
                "eligible_event_role_v1",
                "eligible_pixel_evidence_kind_v1",
                "eligible_resource_kind_v1",
                "eligible_runtime_bridge_type_v1",
                "eligible_slot_v1",
                "eligible_visual_candidate_v1",
                "required_atom_facet_v1",
                "required_event_role_v1",
                "required_guard_binding_v1",
                "required_pixel_evidence_kind_v1",
                "required_resource_kind_v1",
                "required_runtime_bridge_type_v1",
                "required_visual_candidate_v1",
                "zero_semantic_load_axis_v1",
            },
            {
                obligation["evaluator_id"]
                for row in current_rows
                for obligation in row["runtime_expectations"][
                    "compiled_obligation_contract"
                ]["obligations"]
            },
        )

    def test_crosswalk_guards_closed_outcomes_and_tone_carriers_are_typed(self) -> None:
        crosswalk = _json(ASSET_ROOT / "universal_scene_expectation_crosswalk_v2.json")
        mappings = [
            *crosswalk["legacy_event_label_mappings"],
            *crosswalk["legacy_bridge_label_mappings"],
        ]
        guard_targets = [
            target
            for mapping in mappings
            for target in mapping["targets"]
            if target["target_kind"] == "guard_contract"
        ]
        self.assertEqual(15, len(guard_targets))
        self.assertEqual(
            {"required"}, {target["enforcement"] for target in guard_targets}
        )
        self.assertFalse(
            any(
                all(
                    target["target_kind"] == "guard_contract"
                    for target in mapping["targets"]
                )
                for mapping in mappings
            )
        )
        closed = [
            mapping
            for mapping in crosswalk["legacy_event_label_mappings"]
            if mapping["allowed_legacy_states"] == ["closed"]
        ]
        self.assertEqual(7, len(closed))
        direct_absence_kinds = {
            "slot",
            "event_role",
            "atom_facet",
            "resource_kind",
            "blocked_semantic",
            "semantic_load_axis",
        }
        for mapping in closed:
            self.assertTrue(
                any(
                    target["enforcement"] == "absent"
                    and target["target_kind"] in direct_absence_kinds
                    for target in mapping["targets"]
                ),
                mapping,
            )
        tone = next(
            mapping
            for mapping in crosswalk["legacy_bridge_label_mappings"]
            if mapping["legacy_label"] == "tone"
        )
        self.assertEqual(
            [
                ("context_profile_field", ["tone"], "canonical_projection"),
                ("blocked_semantic", ["scene_promise_hijack"], "absent"),
                ("semantic_load_axis", ["theme_displacement"], "absent"),
                ("atom_facet", ["environment", "salience"], "required"),
                (
                    "visual_candidate",
                    ["usc_sptg_context_anchor_relation"],
                    "required",
                ),
                ("pixel_evidence_kind", ["display", "path"], "required"),
                ("guard_contract", ["usl_theme_hijack_guard"], "required"),
            ],
            [
                (
                    target["target_kind"],
                    target["target_ids"],
                    target["enforcement"],
                )
                for target in tone["targets"]
            ],
        )
        nonhuman_display = next(
            mapping
            for mapping in crosswalk["legacy_event_label_mappings"]
            if mapping["legacy_label"] == "nonhuman_display_channel"
        )
        self.assertEqual(
            [
                (
                    "slot",
                    ["expression"],
                    ["body_direction_and_light_intensity_display"],
                    "all",
                    "canonical_projection",
                ),
                (
                    "resource_kind",
                    [
                        "body_orientation",
                        "body_contour_display",
                        "internal_luminance_display",
                        "light_emission",
                    ],
                    [],
                    "any",
                    "eligible",
                ),
                (
                    "pixel_evidence_kind",
                    ["display", "orientation"],
                    [],
                    "any",
                    "required",
                ),
            ],
            [
                (
                    target["target_kind"],
                    target["target_ids"],
                    target["target_values"],
                    target["quantifier"],
                    target["enforcement"],
                )
                for target in nonhuman_display["targets"]
            ],
        )
        self.assertEqual(1, crosswalk["band_policy"]["global_max_optional_remote"])
        self.assertNotIn(
            "max_optional_remote_or_high_load_premises",
            crosswalk["band_policy"],
        )
        self.assertTrue(
            all(
                "max_optional_remote" not in band
                for band in crosswalk["band_policy"]["creativity_bands"]
            )
        )

    def test_current_contract_v2_is_literal_partitioned_and_case12_is_actor_scoped(
        self,
    ) -> None:
        historical_rows = _jsonl(
            ASSET_ROOT / "universal_scene_contract_holdout_v1.jsonl"
        )
        current_rows = _jsonl(ASSET_ROOT / "universal_scene_contract_holdout_v2.jsonl")
        self.assertEqual(24, len(current_rows))
        state_deltas: list[tuple[str, str, str, str]] = []
        phrase_order_deltas: list[tuple[str, str]] = []
        context_deltas: list[tuple[str, str, str, str]] = []
        for historical, current in zip(historical_rows, current_rows):
            case_id = current["case_id"]
            scene_contract = current["scene_contract"]
            self.assertEqual(
                "subculture_illustration_scene_contract_holdout/v2",
                current["schema"],
            )
            self.assertFalse(current["revision"]["runtime_outputs_used"])
            self.assertEqual(
                historical["scene_contract"]["request_text_sha256"],
                current["source_lineage"]["request_text_sha256"],
            )
            self.assertEqual(
                [
                    "schema",
                    "request_text_sha256",
                    "identity_core",
                    "participant_bindings",
                    "slot_states",
                    "event_roles",
                    "context_profile",
                ],
                list(scene_contract),
            )
            entities = scene_contract["identity_core"]["entities"]
            self.assertTrue(
                all(
                    list(entity)
                    == [
                        "entity_id",
                        "quantity",
                        "embodiment_profile_id",
                        "capability_projection_mode",
                        "feature_facts",
                        "capabilities",
                    ]
                    for entity in entities
                )
            )
            participants = scene_contract["participant_bindings"]
            self.assertEqual(
                [
                    "actor",
                    "action",
                    "target",
                    "instrument",
                    "recipient",
                    "result",
                    "location",
                    "phase",
                ],
                [binding["role_id"] for binding in participants],
            )
            self.assertTrue(participants[0]["entity_ids"])
            self.assertTrue(
                all(
                    list(binding) == ["role_id", "entity_ids", "primary_entity_id"]
                    and binding["entity_ids"] == sorted(set(binding["entity_ids"]))
                    and (
                        binding["primary_entity_id"] in binding["entity_ids"]
                        if binding["entity_ids"]
                        else binding["primary_entity_id"] is None
                    )
                    for binding in participants
                )
            )
            historical_slots = {
                slot["slot_id"]: slot
                for slot in historical["scene_contract"]["slot_states"]
            }
            for slot in scene_contract["slot_states"]:
                prior = historical_slots[slot["slot_id"]]
                if slot["state"] != prior["state"]:
                    state_deltas.append(
                        (case_id, slot["slot_id"], prior["state"], slot["state"])
                    )
                if (
                    slot["state"] == prior["state"]
                    and slot["request_phrases"] != prior["request_phrases"]
                ):
                    phrase_order_deltas.append((case_id, slot["slot_id"]))
                bindings = slot["value_phrase_bindings"]
                if slot["state"] == "fixed":
                    self.assertEqual(
                        slot["value_ids"],
                        [binding["value_id"] for binding in bindings],
                    )
                    flattened = [
                        phrase
                        for binding in bindings
                        for phrase in binding["request_phrases"]
                    ]
                    self.assertEqual(slot["request_phrases"], flattened)
                    self.assertEqual(len(flattened), len(set(flattened)))
                    self.assertTrue(
                        all(binding["request_phrases"] for binding in bindings)
                    )
                    self.assertTrue(
                        all(
                            binding["semantic_anchor_groups"]
                            and all(
                                group["required_polarity"] in {"affirmative", "negated"}
                                and group["alternatives"]
                                for group in binding["semantic_anchor_groups"]
                            )
                            for binding in bindings
                        )
                    )
                else:
                    self.assertEqual([], bindings)
            historical_roles = {
                role["role_id"]: role
                for role in historical["scene_contract"]["event_roles"]
            }
            for role in scene_contract["event_roles"]:
                prior = historical_roles[role["role_id"]]
                if role["state"] != prior["state"]:
                    state_deltas.append(
                        (case_id, role["role_id"], prior["state"], role["state"])
                    )
                self.assertEqual(
                    role["state"] == "fixed",
                    bool(role["semantic_anchor_groups"]),
                )
            for field_id, prior_value in historical["scene_contract"][
                "context_profile"
            ].items():
                current_value = current["scene_contract"]["context_profile"][field_id]
                if current_value != prior_value:
                    context_deltas.append(
                        (case_id, field_id, prior_value, current_value)
                    )
        self.assertEqual(
            [
                ("universal_scene_12_nonhuman_display", "prop", "closed", "open"),
                (
                    "universal_scene_12_nonhuman_display",
                    "instrument",
                    "closed",
                    "open",
                ),
                (
                    "universal_scene_24_closed_no_prop_consequence",
                    "expression",
                    "closed",
                    "fixed",
                ),
            ],
            state_deltas,
        )
        self.assertEqual(
            [("universal_scene_17_relation_topology", "relation")],
            phrase_order_deltas,
        )
        self.assertEqual(
            [
                (
                    "universal_scene_15_action_phase",
                    "scale",
                    "intimate",
                    "unknown",
                ),
                (
                    "universal_scene_18_prop_lexical_normalization",
                    "scale",
                    "intimate",
                    "unknown",
                ),
            ],
            context_deltas,
        )

        oracle = next(
            row
            for row in _jsonl(ASSET_ROOT / "universal_scene_current_holdout_v2.jsonl")
            if row["case_id"] == "universal_scene_12_nonhuman_display"
        )
        self.assertEqual(
            "literal_binding_schema_migration_and_resource_scope_and_custom_embodiment_scope_correction",
            next(
                row
                for row in current_rows
                if row["case_id"] == "universal_scene_12_nonhuman_display"
            )["revision"]["reason_id"],
        )
        superseded = [
            entry
            for entry in oracle["resolution_ledger"]
            if entry["runtime_authority"] is False
        ]
        self.assertEqual(7, len(superseded))
        self.assertEqual(
            {
                "historical_only_no_literal_role_binding",
                "superseded_by_literal_scope_correction",
                "superseded_by_reviewed_custom_embodiment_scope_correction",
            },
            {entry["resolution"] for entry in superseded},
        )
        correction = next(
            entry
            for entry in oracle["resolution_ledger"]
            if entry["legacy_kind"] == "scene_contract_resource_scope"
        )
        self.assertEqual("actor_01", correction["legacy_label"])
        self.assertEqual(
            ["actor_01"],
            correction["targets"][1]["target_values"],
        )
        obligations = oracle["runtime_expectations"]["compiled_obligation_contract"][
            "obligations"
        ]
        self.assertFalse(
            any(
                obligation["enforcement"] == "absent"
                and (
                    (
                        obligation["target_kind"] == "slot"
                        and "prop" in obligation["target_ids"]
                    )
                    or (
                        obligation["target_kind"] == "event_role"
                        and "instrument" in obligation["target_ids"]
                    )
                    or (
                        obligation["target_kind"] == "atom_facet"
                        and "prop" in obligation["target_ids"]
                    )
                )
                for obligation in obligations
            )
        )
        self.assertEqual(
            {
                "policy": "open",
                "load": "bounded_unknown",
                "named_prop": None,
            },
            oracle["runtime_expectations"]["prop"],
        )

        custom_profiles = {
            "universal_scene_04_explicit_apple": (
                "recipient_01",
                "custom_unknown_guest_embodiment",
                [],
            ),
            "universal_scene_08_ambiguous_display_affect": (
                "recipient_01",
                "custom_unspecified_handoff_recipient",
                [],
            ),
            "universal_scene_09_shared_attention": (
                "actor_02",
                "custom_winged_nonhuman_unspecified_life_stage",
                ["attention_channel", "wing_appendage"],
            ),
            "universal_scene_11_gesture_function": (
                "recipient_01",
                "custom_unspecified_colleague",
                [],
            ),
            "universal_scene_12_nonhuman_display": (
                "actor_01",
                "custom_faceless_limbless_adult_cloud_nonhuman",
                [
                    "facial_display",
                    "manipulator",
                    "appendage",
                    "body_contour_display",
                    "internal_luminance_display",
                ],
            ),
        }
        contract_by_case = {row["case_id"]: row for row in current_rows}
        fixed_recipient_cases = {
            "universal_scene_04_explicit_apple",
            "universal_scene_08_ambiguous_display_affect",
            "universal_scene_11_gesture_function",
            "universal_scene_12_nonhuman_display",
            "universal_scene_14_event_roles",
            "universal_scene_24_closed_no_prop_consequence",
        }
        for case_id, wrapper in contract_by_case.items():
            participants = {
                item["role_id"]: item
                for item in wrapper["scene_contract"]["participant_bindings"]
            }
            expected_actor_ids = (
                ["actor_01", "actor_02"]
                if case_id
                in {
                    "universal_scene_09_shared_attention",
                    "universal_scene_21_prop_narrative_role",
                }
                else ["team_01"]
                if case_id == "universal_scene_17_relation_topology"
                else ["actor_01"]
            )
            self.assertEqual(expected_actor_ids, participants["actor"]["entity_ids"])
            self.assertEqual(
                ["recipient_01"] if case_id in fixed_recipient_cases else [],
                participants["recipient"]["entity_ids"],
            )
            self.assertTrue(
                all(
                    participants[role_id]["entity_ids"] == []
                    for role_id in (
                        "action",
                        "target",
                        "instrument",
                        "result",
                        "location",
                        "phase",
                    )
                )
            )
        for case_id, (entity_id, profile_id, capability_ids) in custom_profiles.items():
            with self.subTest(custom_profile_case=case_id):
                wrapper = contract_by_case[case_id]
                entity = next(
                    item
                    for item in wrapper["scene_contract"]["identity_core"]["entities"]
                    if item["entity_id"] == entity_id
                )
                self.assertEqual(profile_id, entity["embodiment_profile_id"])
                self.assertEqual(
                    "declared_subset",
                    entity["capability_projection_mode"],
                )
                self.assertEqual(
                    capability_ids,
                    [item["id"] for item in entity["capabilities"]],
                )
                self.assertIn(
                    "custom_embodiment_scope_correction",
                    wrapper["revision"]["reason_id"],
                )

        case16_wrapper = contract_by_case["universal_scene_16_contact_resource"]
        case16_actor = case16_wrapper["scene_contract"]["identity_core"]["entities"][0]
        corrected_profile = "four_armed_adult_equivalent_mechanical_humanoid"
        self.assertEqual(corrected_profile, case16_actor["embodiment_profile_id"])
        self.assertEqual("catalog_exact", case16_actor["capability_projection_mode"])
        self.assertEqual(
            [
                ("manipulator", 4),
                ("attention_channel", 1),
                ("head_orientation", 1),
                ("support_contact", 2),
                ("mechanical_state_displacement", 2),
            ],
            [(item["id"], item["capacity"]) for item in case16_actor["capabilities"]],
        )
        self.assertTrue(
            all(
                item["source"] == "embodiment_profile"
                and item["source_fact_id"] == corrected_profile
                for item in case16_actor["capabilities"]
            )
        )

        oracle_by_case = {
            row["case_id"]: row
            for row in _jsonl(ASSET_ROOT / "universal_scene_current_holdout_v2.jsonl")
        }
        observed_historical_fixed_roles = []
        for case_id, oracle_row in oracle_by_case.items():
            historical_indices = {
                index
                for index, entry in enumerate(oracle_row["resolution_ledger"])
                if entry["runtime_authority"] is False
            }
            compiled_source_indices = {
                source_ref["ledger_entry_index"]
                for obligation in oracle_row["runtime_expectations"][
                    "compiled_obligation_contract"
                ]["obligations"]
                for source_ref in obligation["source_refs"]
            }
            self.assertTrue(historical_indices.isdisjoint(compiled_source_indices))
            for entry in oracle_row["resolution_ledger"]:
                if (
                    entry["source_id"] == "legacy_prompt_record"
                    and entry["legacy_kind"] == "event_role_state"
                    and entry["legacy_state"] == "fixed"
                ):
                    self.assertFalse(entry["runtime_authority"])
                    self.assertEqual(
                        "historical_non_authoritative_expectation",
                        entry["disposition"],
                    )
                    self.assertEqual(
                        "historical_only_no_literal_role_binding",
                        entry["resolution"],
                    )
                    self.assertEqual([], entry["targets"][0]["target_values"])
                    observed_historical_fixed_roles.append(
                        (
                            case_id,
                            entry["legacy_label"],
                            entry["legacy_value"],
                            entry["source_pointer"],
                        )
                    )
        self.assertEqual(
            self.HISTORICAL_FIXED_ROLE_ROWS,
            observed_historical_fixed_roles,
        )
        for case_id in (
            "universal_scene_15_action_phase",
            "universal_scene_18_prop_lexical_normalization",
        ):
            context_entries = [
                entry
                for entry in oracle_by_case[case_id]["resolution_ledger"]
                if entry["legacy_kind"]
                in {
                    "scene_contract_context_profile_value",
                    "scene_contract_context_scope",
                }
            ]
            self.assertEqual(2, len(context_entries))
            context_by_kind = {entry["legacy_kind"]: entry for entry in context_entries}
            self.assertFalse(
                context_by_kind["scene_contract_context_profile_value"][
                    "runtime_authority"
                ]
            )
            self.assertTrue(
                context_by_kind["scene_contract_context_scope"]["runtime_authority"]
            )
            self.assertEqual(
                ["unknown"],
                context_by_kind["scene_contract_context_scope"]["targets"][0][
                    "target_values"
                ],
            )

        case24 = oracle_by_case["universal_scene_24_closed_no_prop_consequence"]
        expression = next(
            slot
            for slot in case24["canonical_scene_contract"]["slot_states"]
            if slot["slot_id"] == "expression"
        )
        self.assertEqual(
            {
                "slot_id": "expression",
                "state": "fixed",
                "value_ids": ["body_direction_and_light_intensity_display"],
                "request_phrases": ["몸의 방향, 빛의 세기"],
                "value_phrase_bindings": [
                    {
                        "value_id": "body_direction_and_light_intensity_display",
                        "request_phrases": ["몸의 방향, 빛의 세기"],
                        "semantic_anchor_groups": [
                            {
                                "alternatives": ["몸의 방향, 빛의 세기"],
                                "required_polarity": "affirmative",
                            }
                        ],
                    }
                ],
            },
            expression,
        )
        display_entry = next(
            entry
            for entry in case24["resolution_ledger"]
            if entry["legacy_kind"] == "scene_contract_display_scope"
        )
        self.assertEqual(
            [
                (
                    "slot",
                    ["expression"],
                    ["body_direction_and_light_intensity_display"],
                    "canonical_projection",
                ),
                (
                    "resource_kind",
                    [
                        "body_orientation",
                        "body_contour_display",
                        "internal_luminance_display",
                        "light_emission",
                    ],
                    [],
                    "eligible",
                ),
                (
                    "pixel_evidence_kind",
                    ["display", "orientation"],
                    [],
                    "required",
                ),
            ],
            [
                (
                    target["target_kind"],
                    target["target_ids"],
                    target["target_values"],
                    target["enforcement"],
                )
                for target in display_entry["targets"]
            ],
        )

    def test_current_contract_scope_binding_and_relative_pointer_mutations_reject(
        self,
    ) -> None:
        def reclose_case12(root: Path) -> None:
            path = root / "universal_scene_contract_holdout_v2.jsonl"
            rows = _jsonl(path)
            row = next(
                item
                for item in rows
                if item["case_id"] == "universal_scene_12_nonhuman_display"
            )
            prop = next(
                slot
                for slot in row["scene_contract"]["slot_states"]
                if slot["slot_id"] == "prop"
            )
            prop["state"] = "closed"
            instrument = next(
                role
                for role in row["scene_contract"]["event_roles"]
                if role["role_id"] == "instrument"
            )
            instrument["state"] = "closed"
            self._write_jsonl(path, rows)

        def collapse_case16_value_bindings(root: Path) -> None:
            path = root / "universal_scene_contract_holdout_v2.jsonl"
            rows = _jsonl(path)
            row = next(
                item
                for item in rows
                if item["case_id"] == "universal_scene_16_contact_resource"
            )
            prop = next(
                slot
                for slot in row["scene_contract"]["slot_states"]
                if slot["slot_id"] == "prop"
            )
            for binding in prop["value_phrase_bindings"]:
                binding["request_phrases"] = ["난간"]
            self._write_jsonl(path, rows)

        def restore_old_prefixed_pointer(root: Path) -> None:
            path = root / "universal_scene_current_holdout_v2.jsonl"
            rows = _jsonl(path)
            entry = next(
                entry
                for entry in rows[0]["resolution_ledger"]
                if entry["source_id"] == "legacy_prompt_record"
            )
            entry["source_pointer"] = "/legacy_prompt_record" + entry["source_pointer"]
            self._write_jsonl(path, rows)

        def claim_runtime_authorship(root: Path) -> None:
            path = root / "universal_scene_contract_holdout_v2.jsonl"
            rows = _jsonl(path)
            rows[0]["revision"]["runtime_outputs_used"] = True
            self._write_jsonl(path, rows)

        def restore_unbound_scale_inference(root: Path) -> None:
            path = root / "universal_scene_contract_holdout_v2.jsonl"
            rows = _jsonl(path)
            for row in rows:
                if row["case_id"] in {
                    "universal_scene_15_action_phase",
                    "universal_scene_18_prop_lexical_normalization",
                }:
                    row["scene_contract"]["context_profile"]["scale"] = "intimate"
            self._write_jsonl(path, rows)

        def reclose_case24_display_channel(root: Path) -> None:
            path = root / "universal_scene_contract_holdout_v2.jsonl"
            rows = _jsonl(path)
            row = next(
                item
                for item in rows
                if item["case_id"] == "universal_scene_24_closed_no_prop_consequence"
            )
            expression = next(
                slot
                for slot in row["scene_contract"]["slot_states"]
                if slot["slot_id"] == "expression"
            )
            expression.update(
                {
                    "state": "closed",
                    "value_ids": [],
                    "request_phrases": ["얼굴 표정이나 사람 손 대신"],
                    "value_phrase_bindings": [],
                }
            )
            self._write_jsonl(path, rows)

        def restore_unknown_noncustom_profile(root: Path) -> None:
            path = root / "universal_scene_contract_holdout_v2.jsonl"
            rows = _jsonl(path)
            row = next(
                item
                for item in rows
                if item["case_id"] == "universal_scene_04_explicit_apple"
            )
            recipient = row["scene_contract"]["identity_core"]["entities"][1]
            recipient["embodiment_profile_id"] = "unknown_guest_embodiment"
            self._write_jsonl(path, rows)

        def drift_case16_profile_capabilities(root: Path) -> None:
            path = root / "universal_scene_contract_holdout_v2.jsonl"
            rows = _jsonl(path)
            row = next(
                item
                for item in rows
                if item["case_id"] == "universal_scene_16_contact_resource"
            )
            actor = row["scene_contract"]["identity_core"]["entities"][0]
            actor["embodiment_profile_id"] = (
                "four_armed_adult_equivalent_mechanical_entity"
            )
            actor["capabilities"][0]["capacity"] = 5
            actor["capabilities"][1]["source"] = "explicit"
            actor["capabilities"][2]["source_fact_id"] = "wrong_profile"
            actor["capabilities"].reverse()
            self._write_jsonl(path, rows)

        def disable_custom_canonical_authority(root: Path) -> None:
            path = root / "universal_scene_current_holdout_v2.jsonl"
            rows = _jsonl(path)
            row = next(
                item
                for item in rows
                if item["case_id"] == "universal_scene_09_shared_attention"
            )
            entry = next(
                item
                for item in row["resolution_ledger"]
                if item["legacy_kind"] == "scene_contract_custom_embodiment_scope"
                and item["runtime_authority"] is True
            )
            entry["runtime_authority"] = False
            self._write_jsonl(path, rows)

        def reorder_participant_bindings(root: Path) -> None:
            path = root / "universal_scene_contract_holdout_v2.jsonl"
            rows = _jsonl(path)
            bindings = rows[0]["scene_contract"]["participant_bindings"]
            bindings[0], bindings[1] = bindings[1], bindings[0]
            self._write_jsonl(path, rows)

        def bind_unknown_duplicate_participant(root: Path) -> None:
            path = root / "universal_scene_contract_holdout_v2.jsonl"
            rows = _jsonl(path)
            actor = rows[0]["scene_contract"]["participant_bindings"][0]
            actor["entity_ids"] = ["actor_01", "actor_01", "unknown_01"]
            actor["primary_entity_id"] = "unknown_01"
            self._write_jsonl(path, rows)

        def bind_closed_role_participant(root: Path) -> None:
            path = root / "universal_scene_contract_holdout_v2.jsonl"
            rows = _jsonl(path)
            row = next(
                item
                for item in rows
                if item["case_id"] == "universal_scene_24_closed_no_prop_consequence"
            )
            instrument = next(
                item
                for item in row["scene_contract"]["participant_bindings"]
                if item["role_id"] == "instrument"
            )
            instrument["entity_ids"] = ["actor_01"]
            instrument["primary_entity_id"] = "actor_01"
            self._write_jsonl(path, rows)

        def omit_fixed_semantic_anchor(root: Path) -> None:
            path = root / "universal_scene_contract_holdout_v2.jsonl"
            rows = _jsonl(path)
            row = next(
                item
                for item in rows
                if item["case_id"] == "universal_scene_04_explicit_apple"
            )
            prop = next(
                item
                for item in row["scene_contract"]["slot_states"]
                if item["slot_id"] == "prop"
            )
            binding = prop["value_phrase_bindings"][0]
            binding["semantic_anchor_groups"] = []
            self._write_jsonl(path, rows)

        def reorder_default_semantic_anchors(root: Path) -> None:
            path = root / "universal_scene_contract_holdout_v2.jsonl"
            rows = _jsonl(path)
            row = next(
                item
                for item in rows
                if item["case_id"] == "universal_scene_11_gesture_function"
            )
            environment = next(
                item
                for item in row["scene_contract"]["slot_states"]
                if item["slot_id"] == "environment"
            )
            environment["value_phrase_bindings"][0]["semantic_anchor_groups"].reverse()
            self._write_jsonl(path, rows)

        def flip_reviewed_semantic_polarity(root: Path) -> None:
            path = root / "universal_scene_contract_holdout_v2.jsonl"
            rows = _jsonl(path)
            row = next(
                item
                for item in rows
                if item["case_id"] == "universal_scene_19_affordance_repurpose"
            )
            prop = next(
                item
                for item in row["scene_contract"]["slot_states"]
                if item["slot_id"] == "prop"
            )
            prop["value_phrase_bindings"][0]["semantic_anchor_groups"][1][
                "required_polarity"
            ] = "affirmative"
            self._write_jsonl(path, rows)

        def borrow_semantic_anchor_from_sibling_value(root: Path) -> None:
            path = root / "universal_scene_contract_holdout_v2.jsonl"
            rows = _jsonl(path)
            row = next(
                item
                for item in rows
                if item["case_id"] == "universal_scene_16_contact_resource"
            )
            prop = next(
                item
                for item in row["scene_contract"]["slot_states"]
                if item["slot_id"] == "prop"
            )
            first, second = prop["value_phrase_bindings"][:2]
            first["semantic_anchor_groups"][0]["alternatives"] = [
                second["request_phrases"][0]
            ]
            self._write_jsonl(path, rows)

        def drift_capability_projection_mode(root: Path) -> None:
            path = root / "universal_scene_contract_holdout_v2.jsonl"
            rows = _jsonl(path)
            rows[0]["scene_contract"]["identity_core"]["entities"][0][
                "capability_projection_mode"
            ] = "catalog_exact"
            self._write_jsonl(path, rows)

        def restore_historical_fixed_role_authority(root: Path) -> None:
            path = root / "universal_scene_current_holdout_v2.jsonl"
            rows = _jsonl(path)
            row = next(
                item
                for item in rows
                if item["case_id"] == "universal_scene_17_relation_topology"
            )
            entry = next(
                item
                for item in row["resolution_ledger"]
                if item["source_id"] == "legacy_prompt_record"
                and item["legacy_kind"] == "event_role_state"
                and item["legacy_label"] == "recipient"
            )
            entry["disposition"] = "literal_contract_authority"
            entry["runtime_authority"] = True
            entry["resolution"] = "enforced_current_projection"
            self._write_jsonl(path, rows)

        def inject_historical_fixed_role_target_value(root: Path) -> None:
            path = root / "universal_scene_current_holdout_v2.jsonl"
            rows = _jsonl(path)
            row = next(
                item
                for item in rows
                if item["case_id"] == "universal_scene_17_relation_topology"
            )
            entry = next(
                item
                for item in row["resolution_ledger"]
                if item["source_id"] == "legacy_prompt_record"
                and item["legacy_kind"] == "event_role_state"
                and item["legacy_label"] == "recipient"
            )
            entry["targets"][0]["target_values"] = ["axis_holder"]
            self._write_jsonl(path, rows)

        for label, mutate in (
            ("reclose case12 prop and instrument", reclose_case12),
            ("collapse case16 value bindings", collapse_case16_value_bindings),
            ("restore old prefixed ledger pointer", restore_old_prefixed_pointer),
            ("claim runtime-authored current contract", claim_runtime_authorship),
            ("restore unbound scale inference", restore_unbound_scale_inference),
            ("reclose case24 display channel", reclose_case24_display_channel),
            ("restore unknown noncustom profile", restore_unknown_noncustom_profile),
            ("drift case16 profile capabilities", drift_case16_profile_capabilities),
            ("disable custom canonical authority", disable_custom_canonical_authority),
            ("reorder participant bindings", reorder_participant_bindings),
            ("bind unknown duplicate participant", bind_unknown_duplicate_participant),
            ("bind a participant to a closed role", bind_closed_role_participant),
            ("omit fixed semantic anchor", omit_fixed_semantic_anchor),
            ("reorder default semantic anchors", reorder_default_semantic_anchors),
            ("flip reviewed semantic polarity", flip_reviewed_semantic_polarity),
            (
                "borrow semantic anchor from sibling fixed value",
                borrow_semantic_anchor_from_sibling_value,
            ),
            ("drift capability projection mode", drift_capability_projection_mode),
            (
                "restore historical fixed-role runtime authority",
                restore_historical_fixed_role_authority,
            ),
            (
                "inject a value into a historical fixed-role target",
                inject_historical_fixed_role_target_value,
            ),
        ):
            with self.subTest(label=label):
                self._assert_semantic_mutation_rejected(mutate)

    def test_all_14_historical_fixed_roles_reject_authority_and_value_mutations(
        self,
    ) -> None:
        def mutation(
            case_id: str,
            role_id: str,
            legacy_value: str,
            source_pointer: str,
            mode: str,
        ) -> object:
            def apply(root: Path) -> None:
                path = root / "universal_scene_current_holdout_v2.jsonl"
                rows = _jsonl(path)
                row = next(item for item in rows if item["case_id"] == case_id)
                entry = next(
                    item
                    for item in row["resolution_ledger"]
                    if item["source_id"] == "legacy_prompt_record"
                    and item["legacy_kind"] == "event_role_state"
                    and item["legacy_label"] == role_id
                    and item["legacy_value"] == legacy_value
                    and item["source_pointer"] == source_pointer
                )
                if mode == "authority":
                    entry["disposition"] = "literal_contract_authority"
                    entry["runtime_authority"] = True
                    entry["resolution"] = "enforced_current_projection"
                else:
                    entry["targets"][0]["target_values"] = [legacy_value]
                self._write_jsonl(path, rows)

            return apply

        for (
            case_id,
            role_id,
            legacy_value,
            source_pointer,
        ) in self.HISTORICAL_FIXED_ROLE_ROWS:
            for mode in ("authority", "target_value"):
                with self.subTest(case_id=case_id, role_id=role_id, mode=mode):
                    self._assert_semantic_mutation_rejected(
                        mutation(
                            case_id,
                            role_id,
                            legacy_value,
                            source_pointer,
                            mode,
                        )
                    )

    def test_raw_source_current_crosswalk_manifest_and_v1_baseline_hashes_fail_closed(
        self,
    ) -> None:
        filenames = (
            "universal_scene_prompt_holdout_v1.jsonl",
            "universal_scene_contract_holdout_v1.jsonl",
            "universal_scene_contract_holdout_v2.jsonl",
            "universal_scene_baseline_v1.json",
            "universal_scene_current_holdout_v2.jsonl",
            "universal_scene_expectation_crosswalk_v2.json",
            "universal_scene_current_holdout_v2_manifest.json",
        )
        for filename in filenames:
            with (
                self.subTest(filename=filename),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                self._copy_oracle(root)
                path = root / filename
                path.write_bytes(path.read_bytes() + b" ")
                with self.assertRaises(ValidationFailure):
                    validate_universal_scene_current_oracle_v2(root)

    def test_projection_lineage_revision_mapping_and_closed_bridge_mutations_reject(
        self,
    ) -> None:
        def projection_omission(root: Path) -> None:
            path = root / "universal_scene_current_holdout_v2.jsonl"
            rows = _jsonl(path)
            rows[0]["canonical_projection"]["slot_states"].pop()
            self._write_jsonl(path, rows)

        def lineage_drift(root: Path) -> None:
            path = root / "universal_scene_current_holdout_v2.jsonl"
            rows = _jsonl(path)
            rows[0]["source_lineage"]["prompt_holdout"]["raw_record_sha256"] = "0" * 64
            self._write_jsonl(path, rows)

        def revision_claim(root: Path) -> None:
            path = root / "universal_scene_current_holdout_v2.jsonl"
            rows = _jsonl(path)
            rows[0]["revision"]["frozen_before_implementation"] = True
            self._write_jsonl(path, rows)

        def missing_mapping(root: Path) -> None:
            path = root / "universal_scene_expectation_crosswalk_v2.json"
            crosswalk = _json(path)
            crosswalk["legacy_event_label_mappings"].pop()
            self._write_json(path, crosswalk)

        def weakened_band(root: Path) -> None:
            path = root / "universal_scene_expectation_crosswalk_v2.json"
            crosswalk = _json(path)
            crosswalk["band_policy"]["band_requirements"]["far"][
                "minimum_distinct_type_count"
            ] = 2
            self._write_json(path, crosswalk)

        def nonclosed_runtime_bridge(root: Path) -> None:
            path = root / "universal_scene_current_holdout_v2.jsonl"
            rows = _jsonl(path)
            rows[0]["runtime_expectations"]["runtime_bridge_contract"][
                "required_type_ids"
            ].append("capability")
            self._write_jsonl(path, rows)

        def guard_made_absent(root: Path) -> None:
            path = root / "universal_scene_expectation_crosswalk_v2.json"
            crosswalk = _json(path)
            mapping = next(
                item
                for item in crosswalk["legacy_event_label_mappings"]
                if item["legacy_label"] == "combat_opponent"
            )
            guard = next(
                target
                for target in mapping["targets"]
                if target["target_kind"] == "guard_contract"
            )
            guard["enforcement"] = "absent"
            self._write_json(path, crosswalk)

        def closed_mapping_guard_only(root: Path) -> None:
            path = root / "universal_scene_expectation_crosswalk_v2.json"
            crosswalk = _json(path)
            mapping = next(
                item
                for item in crosswalk["legacy_event_label_mappings"]
                if item["legacy_label"] == "firing"
            )
            mapping["targets"] = [
                target
                for target in mapping["targets"]
                if target["target_kind"] == "guard_contract"
            ]
            self._write_json(path, crosswalk)

        def tone_loses_load_evidence(root: Path) -> None:
            path = root / "universal_scene_expectation_crosswalk_v2.json"
            crosswalk = _json(path)
            mapping = next(
                item
                for item in crosswalk["legacy_bridge_label_mappings"]
                if item["legacy_label"] == "tone"
            )
            mapping["targets"] = [
                target
                for target in mapping["targets"]
                if target["target_kind"] != "semantic_load_axis"
            ]
            self._write_json(path, crosswalk)

        def missing_compiled_source_ref(root: Path) -> None:
            path = root / "universal_scene_current_holdout_v2.jsonl"
            rows = _jsonl(path)
            contract = rows[5]["runtime_expectations"]["compiled_obligation_contract"]
            record = next(
                item for item in contract["obligations"] if len(item["source_refs"]) > 1
            )
            record["source_refs"].pop()
            self._write_jsonl(path, rows)

        def duplicate_compiled_source_ref(root: Path) -> None:
            path = root / "universal_scene_current_holdout_v2.jsonl"
            rows = _jsonl(path)
            record = rows[0]["runtime_expectations"]["compiled_obligation_contract"][
                "obligations"
            ][0]
            record["source_refs"].append(copy.deepcopy(record["source_refs"][0]))
            self._write_jsonl(path, rows)

        def wrong_compiled_target_index(root: Path) -> None:
            path = root / "universal_scene_current_holdout_v2.jsonl"
            rows = _jsonl(path)
            ref = rows[0]["runtime_expectations"]["compiled_obligation_contract"][
                "obligations"
            ][0]["source_refs"][0]
            ref["target_index"] += 1
            self._write_jsonl(path, rows)

        def wrong_evaluator_id(root: Path) -> None:
            path = root / "universal_scene_current_holdout_v2.jsonl"
            rows = _jsonl(path)
            rows[0]["runtime_expectations"]["compiled_obligation_contract"][
                "obligations"
            ][0]["evaluator_id"] = "wrong_evaluator_v1"
            self._write_jsonl(path, rows)

        def altered_compiled_guard_source(root: Path) -> None:
            path = root / "universal_scene_current_holdout_v2.jsonl"
            rows = _jsonl(path)
            row = next(
                item
                for item in rows
                if item["runtime_expectations"]["compiled_obligation_contract"][
                    "guard_source_contracts"
                ]
            )
            row["runtime_expectations"]["compiled_obligation_contract"][
                "guard_source_contracts"
            ][0]["outcome"] = "allow"
            self._write_jsonl(path, rows)

        def altered_reviewed_guard_source(root: Path) -> None:
            path = root / "universal_scene_expectation_crosswalk_v2.json"
            crosswalk = _json(path)
            crosswalk["guard_source_contracts"][0]["stage"] = "wrong_stage"
            self._write_json(path, crosswalk)

        def reordered_mapping_targets(root: Path) -> None:
            path = root / "universal_scene_expectation_crosswalk_v2.json"
            crosswalk = _json(path)
            mapping = next(
                item
                for item in crosswalk["legacy_bridge_label_mappings"]
                if item["legacy_label"] == "tone"
            )
            mapping["targets"][0], mapping["targets"][1] = (
                mapping["targets"][1],
                mapping["targets"][0],
            )
            self._write_json(path, crosswalk)

        def per_band_remote_gate_reintroduced(root: Path) -> None:
            path = root / "universal_scene_expectation_crosswalk_v2.json"
            crosswalk = _json(path)
            crosswalk["band_policy"]["creativity_bands"][0]["max_optional_remote"] = 0
            self._write_json(path, crosswalk)

        def global_remote_ceiling_weakened(root: Path) -> None:
            path = root / "universal_scene_expectation_crosswalk_v2.json"
            crosswalk = _json(path)
            crosswalk["band_policy"]["global_max_optional_remote"] = 0
            self._write_json(path, crosswalk)

        def visual_candidate_kind_removed(root: Path) -> None:
            path = root / "universal_scene_expectation_crosswalk_v2.json"
            crosswalk = _json(path)
            crosswalk["canonical_domains"]["target_kind_ids"].remove("visual_candidate")
            self._write_json(path, crosswalk)

        def event_role_reintroduces_optional_roles(root: Path) -> None:
            path = root / "universal_scene_expectation_crosswalk_v2.json"
            crosswalk = _json(path)
            mapping = next(
                item
                for item in crosswalk["legacy_bridge_label_mappings"]
                if item["legacy_label"] == "event_role"
            )
            target = next(
                item
                for item in mapping["targets"]
                if item["target_kind"] == "event_role"
            )
            target["target_ids"].extend(
                ["instrument", "recipient", "location", "phase"]
            )
            self._write_json(path, crosswalk)

        def handoff_ownership_bridge_removed(root: Path) -> None:
            path = root / "universal_scene_expectation_crosswalk_v2.json"
            crosswalk = _json(path)
            mapping = next(
                item
                for item in crosswalk["legacy_bridge_label_mappings"]
                if item["legacy_label"] == "handoff"
            )
            mapping["targets"] = [
                target
                for target in mapping["targets"]
                if target["target_kind"] != "runtime_bridge_type"
            ]
            self._write_json(path, crosswalk)

        for label, mutate in (
            ("projection omission", projection_omission),
            ("lineage drift", lineage_drift),
            ("pre-implementation revision claim", revision_claim),
            ("missing mapping", missing_mapping),
            ("weakened far band", weakened_band),
            ("nonclosed runtime bridge", nonclosed_runtime_bridge),
            ("guard made absent", guard_made_absent),
            ("closed mapping guard only", closed_mapping_guard_only),
            ("tone loses load evidence", tone_loses_load_evidence),
            ("missing compiled source ref", missing_compiled_source_ref),
            ("duplicate compiled source ref", duplicate_compiled_source_ref),
            ("wrong compiled target index", wrong_compiled_target_index),
            ("wrong evaluator id", wrong_evaluator_id),
            ("altered compiled guard source", altered_compiled_guard_source),
            ("altered reviewed guard source", altered_reviewed_guard_source),
            ("reordered mapping targets", reordered_mapping_targets),
            ("per-band remote gate reintroduced", per_band_remote_gate_reintroduced),
            ("global remote ceiling weakened", global_remote_ceiling_weakened),
            ("visual candidate target kind removed", visual_candidate_kind_removed),
            (
                "event role reintroduces optional roles",
                event_role_reintroduces_optional_roles,
            ),
            ("handoff ownership bridge removed", handoff_ownership_bridge_removed),
        ):
            with self.subTest(label=label):
                self._assert_semantic_mutation_rejected(mutate)

    def test_descriptive_baseline_cannot_override_module_or_manifest_authority(
        self,
    ) -> None:
        original_loader = validator_module._load_json
        baseline_path = ASSET_ROOT / "universal_scene_baseline_v2.json"
        baseline = _json(baseline_path)
        for path_keys in (
            ("historical_baseline", "sha256"),
            ("source_lineage", "prompt_holdout", "sha256"),
            ("source_lineage", "current_scene_contract_holdout", "sha256"),
            ("current_oracle", "current_holdout", "sha256"),
            ("current_oracle", "crosswalk", "sha256"),
            ("current_oracle", "manifest", "sha256"),
            ("validator_contract", "sha256"),
        ):
            with self.subTest(path=".".join(path_keys)):
                mutated = copy.deepcopy(baseline)
                cursor = mutated
                for key in path_keys[:-1]:
                    cursor = cursor[key]
                cursor[path_keys[-1]] = "0" * 64

                def injected_load(path: Path) -> object:
                    if path == baseline_path:
                        return mutated
                    return original_loader(path)

                with (
                    mock.patch.object(
                        validator_module,
                        "_load_json",
                        side_effect=injected_load,
                    ),
                    self.assertRaises(ValidationFailure),
                ):
                    validate_universal_scene_current_oracle_v2(ASSET_ROOT)

    def test_production_runtime_cannot_load_holdout_or_branch_on_case_id(self) -> None:
        runtime_path = SCRIPT_ROOT / "universal_scene_runtime.py"
        original_read_text = Path.read_text
        for injected_marker in (
            "universal_scene_current_holdout_v2.jsonl",
            "universal_scene_01_same_core_low",
        ):
            with self.subTest(marker=injected_marker):

                def injected_read_text(
                    path: Path,
                    *args: object,
                    **kwargs: object,
                ) -> str:
                    text = original_read_text(path, *args, **kwargs)
                    if path.resolve() == runtime_path.resolve():
                        return f"{text}\n{injected_marker}\n"
                    return text

                with (
                    mock.patch.object(
                        Path,
                        "read_text",
                        new=injected_read_text,
                    ),
                    self.assertRaises(ValidationFailure),
                ):
                    validate_universal_scene_current_oracle_v2(ASSET_ROOT)



class UniversalSceneRuntimeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.legacy_assets = load_runtime_assets(ASSET_ROOT)
        cls.universal_assets = load_universal_scene_assets(ASSET_ROOT)
        cls.research = validate_universal_scene_research(ASSET_ROOT)
        cls.holdouts = validate_universal_scene_holdouts(ASSET_ROOT, cls.research)
        cls.prompt_by_case = {
            str(row["case_id"]): row for row in cls.holdouts["prompt_rows"]
        }
        cls.current_oracle_by_case = {
            str(row["case_id"]): row
            for row in _jsonl(ASSET_ROOT / "universal_scene_current_holdout_v2.jsonl")
        }
        cls.current_contract_by_case = {
            case_id: row["canonical_scene_contract"]
            for case_id, row in cls.current_oracle_by_case.items()
        }
        cls.packs: dict[str, dict[str, object]] = {}
        for case_id, row in cls.prompt_by_case.items():
            scene_contract = cls.current_contract_by_case[case_id]
            cls.packs[case_id] = build_candidate_pack(
                str(row["request_ko"]),
                topic=str(row["expected_topic_id"]),
                format_id=str(row["expected_format"]),
                seed=int(row["seed"]),
                creativity=float(row["creativity"]),
                scene_contract=scene_contract,
                assets=cls.legacy_assets,
            )

    def assert_integrity_failure(
        self,
        pack: dict[str, object],
        expected_check: str,
    ) -> list[dict[str, object]]:
        _rehash(pack)
        errors = validate_pack_integrity(pack)
        self.assertIn(expected_check, _checks(errors), errors)
        return errors

    def test_all_24_v3_packs_are_exactly_deterministic_and_integrity_clean(
        self,
    ) -> None:
        self.assertEqual("subculture-illustration-candidate-pack/v3", CONTRACT_VERSION)
        self.assertEqual(24, len(self.packs))
        for case_id, first in self.packs.items():
            with self.subTest(case_id=case_id):
                row = self.prompt_by_case[case_id]
                contract = self.current_contract_by_case[case_id]
                second = build_candidate_pack(
                    str(row["request_ko"]),
                    topic=str(row["expected_topic_id"]),
                    format_id=str(row["expected_format"]),
                    seed=int(row["seed"]),
                    creativity=float(row["creativity"]),
                    scene_contract=contract,
                    assets=self.legacy_assets,
                )
                self.assertEqual(first, second)
                self.assertEqual(CONTRACT_VERSION, first["contract_version"])
                self.assertEqual(
                    row["expected_topic_id"], first["request_contract"]["route_id"]
                )
                self.assertEqual(
                    row["expected_format"], first["format_profile"]["variant_id"]
                )
                self.assertEqual([], first["request_contract"]["prior_exposure_ids"])
                self.assertEqual([], validate_pack_integrity(first))
                scene = first["universal_scene"]
                self.assertEqual(
                    scene,
                    validate_universal_scene_selection(
                        scene,
                        str(row["request_ko"]),
                        self.universal_assets,
                        topic_id=str(row["expected_topic_id"]),
                        format_id=str(row["expected_format"]),
                        creativity=float(row["creativity"]),
                        seed=int(row["seed"]),
                        prior_exposure_ids=first["request_contract"][
                            "prior_exposure_ids"
                        ],
                    ),
                )
                validated = validate_scene_contract(
                    str(row["request_ko"]),
                    contract,
                    assets=self.universal_assets,
                )
                self.assertEqual(validated.contract, scene["scene_contract"])
                self.assertEqual(
                    validated.sha256,
                    first["request_contract"]["scene_contract_sha256"],
                )
                self.assertEqual(
                    validated.sha256,
                    scene["selection_trace"]["scene_contract_sha256"],
                )
                self.assertEqual(
                    validated.request_sha256,
                    scene["scene_contract"]["request_text_sha256"],
                )
                for identity_field in (
                    "entities",
                    "scene_facts",
                    "forbidden_facts",
                ):
                    self.assertEqual(
                        validated.contract["identity_core"][identity_field],
                        scene["identity_core"][identity_field],
                    )
                self.assertEqual(
                    validated.contract["slot_states"],
                    scene["slot_states"],
                )
                self.assertEqual(
                    validated.contract["context_profile"],
                    scene["context_profile"],
                )
                roles_by_id = _role_by_id(first)
                for fixed_role in validated.contract["event_roles"]:
                    if fixed_role["state"] != "fixed":
                        continue
                    selected_role = roles_by_id[fixed_role["role_id"]]
                    self.assertEqual(fixed_role["value_id"], selected_role["value_id"])
                    self.assertEqual("user_fixed", selected_role["source"])
                    self.assertEqual(fixed_role["role_id"], selected_role["source_id"])
                self.assertEqual("event_01", scene["selected_event"]["event_id"])
                self.assertEqual(8, len(scene["selected_event"]["roles"]))
                self.assertTrue(scene["selected_event"]["spine_edges"])
                self.assertTrue(all(atom["event_edge_ids"] for atom in scene["atoms"]))
                self.assertEqual(
                    row["semantic_distance_expectation"]["band"],
                    scene["semantic_distance_trace"]["selected_band"],
                )

    def test_all_24_packs_satisfy_reviewed_bridge_obligations_and_additive_bands(
        self,
    ) -> None:
        self.assertEqual(set(self.packs), set(self.current_oracle_by_case))
        for case_id, pack in self.packs.items():
            with self.subTest(case_id=case_id):
                oracle = self.current_oracle_by_case[case_id]
                expected = oracle["runtime_expectations"]["runtime_bridge_contract"]
                scene = pack["universal_scene"]
                actual_types = {bridge["bridge_type"] for bridge in scene["bridges"]}
                self.assertLessEqual(
                    actual_types,
                    set(expected["allowed_type_ids"]),
                )
                self.assertLessEqual(
                    set(expected["required_type_ids"]),
                    actual_types,
                )
                self.assertGreaterEqual(
                    len(actual_types),
                    expected["minimum_distinct_type_count"],
                )
                for category_id in expected["required_category_ids"]:
                    self.assertTrue(
                        actual_types & set(expected["category_members"][category_id]),
                        (case_id, category_id, sorted(actual_types)),
                    )
                self.assertTrue(
                    all(bridge["pixel_evidence_ids"] for bridge in scene["bridges"])
                )
                ledger_mapping_ids = list(
                    dict.fromkeys(
                        entry["mapping_id"]
                        for entry in oracle["resolution_ledger"]
                        if entry["legacy_kind"] == "research_bridge_label"
                    )
                )
                self.assertEqual(
                    ledger_mapping_ids,
                    expected["mapped_research_obligation_ids"],
                )

    def test_all_24_execute_every_compiled_obligation_deterministically(self) -> None:
        research_ids = set(self.research["record_ids"])
        evaluator_ids: set[str] = set()
        total_obligations = 0
        for case_id, pack in self.packs.items():
            with self.subTest(case_id=case_id):
                oracle = self.current_oracle_by_case[case_id]
                scene = pack["universal_scene"]
                first = evaluate_universal_scene_compiled_obligations(
                    scene,
                    oracle,
                    self.universal_assets,
                    research_record_ids=research_ids,
                )
                second = evaluate_universal_scene_compiled_obligations(
                    scene,
                    oracle,
                    self.universal_assets,
                    research_record_ids=research_ids,
                )
                self.assertEqual(first, second)
                self.assertEqual("pass", first["status"], first["failures"])
                self.assertEqual(0, first["failed_count"])
                self.assertEqual(first["obligation_count"], first["passed_count"])
                self.assertEqual(
                    len(
                        oracle["runtime_expectations"]["compiled_obligation_contract"][
                            "obligations"
                        ]
                    ),
                    first["obligation_count"],
                )
                evaluator_ids.update(first["evaluator_counts"])
                total_obligations += first["obligation_count"]
        manifest = _json(
            ASSET_ROOT / "universal_scene_current_holdout_v2_manifest.json"
        )
        self.assertEqual(
            manifest["counts"]["compiled_obligation_per_row_unique_count_sum"],
            total_obligations,
        )
        self.assertEqual(
            {
                obligation["evaluator_id"]
                for oracle in self.current_oracle_by_case.values()
                for obligation in oracle["runtime_expectations"][
                    "compiled_obligation_contract"
                ]["obligations"]
            },
            evaluator_ids,
        )

    def test_frozen_traces_replay_at_runtime_and_independent_audit_boundaries(
        self,
    ) -> None:
        for case_id, pack in self.packs.items():
            with self.subTest(case_id=case_id):
                row = self.prompt_by_case[case_id]
                scene = pack["universal_scene"]
                self.assertEqual(
                    scene,
                    validate_universal_scene_selection(
                        scene,
                        str(row["request_ko"]),
                        self.universal_assets,
                        topic_id=str(row["expected_topic_id"]),
                        format_id=str(row["expected_format"]),
                        creativity=float(row["creativity"]),
                        seed=int(row["seed"]),
                        prior_exposure_ids=pack["request_contract"][
                            "prior_exposure_ids"
                        ],
                    ),
                )
                self.assertEqual([], validate_pack_integrity(pack))

        case_id = next(iter(self.packs))
        row = self.prompt_by_case[case_id]
        mutated_pack = copy.deepcopy(self.packs[case_id])
        mutated_scene = mutated_pack["universal_scene"]
        invariant = mutated_scene["creativity_invariant_trace"]
        invariant["reason_code_registry"].pop()
        invariant["trace_sha256"] = canonical_sha256(
            {key: value for key, value in invariant.items() if key != "trace_sha256"}
        )
        postselection = mutated_scene["postselection_run_trace"]
        postselection["invariant_trace_sha256"] = invariant["trace_sha256"]
        postselection["trace_sha256"] = canonical_sha256(
            {
                key: value
                for key, value in postselection.items()
                if key != "trace_sha256"
            }
        )
        _rehash(mutated_pack)
        with self.assertRaises(universal_runtime_module.SelectionError):
            validate_universal_scene_selection(
                mutated_scene,
                str(row["request_ko"]),
                self.universal_assets,
                topic_id=str(row["expected_topic_id"]),
                format_id=str(row["expected_format"]),
                creativity=float(row["creativity"]),
                seed=int(row["seed"]),
                prior_exposure_ids=mutated_pack["request_contract"][
                    "prior_exposure_ids"
                ],
            )
        self.assertIn(
            "universal_creativity_invariant",
            _checks(validate_pack_integrity(mutated_pack)),
        )

    def test_compiled_obligation_owner_joins_reject_global_substitutions(self) -> None:
        research_ids = set(self.research["record_ids"])
        base_outputs = {
            case_id: evaluate_universal_scene_compiled_obligations(
                pack["universal_scene"],
                self.current_oracle_by_case[case_id],
                self.universal_assets,
                research_record_ids=research_ids,
                validate_selection_replay=False,
            )
            for case_id, pack in self.packs.items()
        }

        def mapping_ids(result: dict[str, object]) -> set[str]:
            return {
                str(ref["mapping_id"])
                for ref in result["source_refs"]
                if isinstance(ref["mapping_id"], str)
            }

        def visual_targets(oracle: dict[str, object], mapping_id: str) -> set[str]:
            obligations = oracle["runtime_expectations"][
                "compiled_obligation_contract"
            ]["obligations"]
            return {
                str(target_id)
                for obligation in obligations
                if obligation["target_kind"] == "visual_candidate"
                and any(
                    ref["mapping_id"] == mapping_id for ref in obligation["source_refs"]
                )
                for target_id in obligation["target_ids"]
            }

        def find_owner_result(evaluator_id: str):
            for case_id, output in base_outputs.items():
                oracle = self.current_oracle_by_case[case_id]
                scene = self.packs[case_id]["universal_scene"]
                for result in output["results"]:
                    mids = mapping_ids(result)
                    if (
                        result["evaluator_id"] != evaluator_id
                        or not result["passed"]
                        or len(mids) != 1
                    ):
                        continue
                    mapping_id = next(iter(mids))
                    candidate_ids = visual_targets(oracle, mapping_id)
                    owner_atoms = [
                        atom
                        for atom in scene["atoms"]
                        if atom["candidate_id"] in candidate_ids
                    ]
                    if candidate_ids and owner_atoms:
                        return (
                            case_id,
                            oracle,
                            scene,
                            result,
                            mapping_id,
                            candidate_ids,
                            owner_atoms,
                        )
            self.fail(f"no passing owner-joined obligation for {evaluator_id}")

        def assert_result_flips(
            case_id: str,
            oracle: dict[str, object],
            scene: dict[str, object],
            obligation_id: str,
            assets: object | None = None,
        ) -> None:
            output = evaluate_universal_scene_compiled_obligations(
                scene,
                oracle,
                self.universal_assets if assets is None else assets,
                research_record_ids=research_ids,
                validate_selection_replay=False,
            )
            result = next(
                item
                for item in output["results"]
                if item["obligation_id"] == obligation_id
            )
            self.assertFalse(result["passed"], (case_id, result))

        # A required role without a visual-owner sibling is still a material
        # role obligation.  Keeping the role record while erasing its value
        # must fail the typed result; unrelated canonical/global evidence may
        # not turn mere record presence into materialization.
        no_owner_role_probe = None
        for case_id, output in base_outputs.items():
            oracle = self.current_oracle_by_case[case_id]
            scene = self.packs[case_id]["universal_scene"]
            obligations = oracle["runtime_expectations"][
                "compiled_obligation_contract"
            ]["obligations"]
            obligation_by_id = {item["obligation_id"]: item for item in obligations}
            selected_role_by_id = {
                item["role_id"]: item for item in scene["selected_event"]["roles"]
            }
            for result in output["results"]:
                if (
                    result["evaluator_id"] != "required_event_role_v1"
                    or not result["passed"]
                ):
                    continue
                obligation = obligation_by_id[result["obligation_id"]]
                mids = mapping_ids(result)
                if obligation["target_values"] or any(
                    visual_targets(oracle, mapping_id) for mapping_id in mids
                ):
                    continue
                target_role = next(
                    (
                        item["target_id"]
                        for item in result["target_results"]
                        if item["passed"]
                        and selected_role_by_id[item["target_id"]]["value_id"]
                        is not None
                    ),
                    None,
                )
                if target_role is None:
                    continue
                if (
                    obligation["quantifier"] != "all"
                    and len(obligation["target_ids"]) != 1
                ):
                    continue
                no_owner_role_probe = (
                    case_id,
                    oracle,
                    scene,
                    result,
                    target_role,
                )
                break
            if no_owner_role_probe is not None:
                break
        self.assertIsNotNone(no_owner_role_probe)
        (
            no_owner_role_case,
            no_owner_role_oracle,
            no_owner_role_scene,
            no_owner_role_result,
            no_owner_target_role,
        ) = no_owner_role_probe
        mutated = copy.deepcopy(no_owner_role_scene)
        selected_role = next(
            item
            for item in mutated["selected_event"]["roles"]
            if item["role_id"] == no_owner_target_role
        )
        selected_role["value_id"] = None
        assert_result_flips(
            no_owner_role_case,
            no_owner_role_oracle,
            mutated,
            str(no_owner_role_result["obligation_id"]),
        )

        (
            atom_case,
            atom_oracle,
            atom_scene,
            atom_result,
            _atom_mapping,
            atom_candidate_ids,
            atom_owners,
        ) = find_owner_result("required_atom_facet_v1")
        mutated = copy.deepcopy(atom_scene)
        target_atom = next(
            item
            for item in mutated["atoms"]
            if item["instance_id"] == atom_owners[0]["instance_id"]
        )
        alternate = next(
            candidate_id
            for candidate_id, candidate in self.universal_assets.candidate_by_id.items()
            if candidate["role"] == "visual_atom"
            and candidate["facet"] == target_atom["facet"]
            and candidate_id not in atom_candidate_ids
        )
        target_atom["candidate_id"] = alternate
        assert_result_flips(
            atom_case,
            atom_oracle,
            mutated,
            str(atom_result["obligation_id"]),
        )

        (
            pixel_case,
            pixel_oracle,
            pixel_scene,
            pixel_result,
            _pixel_mapping,
            _pixel_candidate_ids,
            pixel_owners,
        ) = find_owner_result("required_pixel_evidence_kind_v1")
        mutated = copy.deepcopy(pixel_scene)
        target_kinds = {item["target_id"] for item in pixel_result["target_results"]}
        target_atom = next(
            item
            for item in mutated["atoms"]
            if item["instance_id"] == pixel_owners[0]["instance_id"]
        )
        pixel_by_id = {
            item["item_id"]: item
            for item in mutated["pixel_evidence_contract"]["items"]
        }
        original_ids = [
            item_id
            for item_id in target_atom["pixel_evidence_ids"]
            if pixel_by_id[item_id]["kind"] in target_kinds
        ]
        unrelated_atom = next(
            item
            for item in mutated["atoms"]
            if item["instance_id"] != target_atom["instance_id"]
        )
        transplanted_ids = []
        for index, original_id in enumerate(original_ids):
            transplanted = copy.deepcopy(pixel_by_id[original_id])
            transplanted["item_id"] = f"pixel_owner_substitution_probe_{index}"
            transplanted["source_id"] = unrelated_atom["instance_id"]
            mutated["pixel_evidence_contract"]["items"].append(transplanted)
            transplanted_ids.append(transplanted["item_id"])
        target_atom["pixel_evidence_ids"] = [
            item_id
            for item_id in target_atom["pixel_evidence_ids"]
            if item_id not in original_ids
        ] + transplanted_ids
        assert_result_flips(
            pixel_case,
            pixel_oracle,
            mutated,
            str(pixel_result["obligation_id"]),
        )

        (
            resource_case,
            resource_oracle,
            resource_scene,
            resource_result,
            _resource_mapping,
            _resource_candidate_ids,
            resource_owners,
        ) = find_owner_result("required_resource_kind_v1")
        mutated = copy.deepcopy(resource_scene)
        target_kind = next(
            item["target_id"]
            for item in resource_result["target_results"]
            if item["passed"]
        )
        target_atom = next(
            item
            for item in mutated["atoms"]
            if item["instance_id"] == resource_owners[0]["instance_id"]
        )
        claim_by_id = {item["claim_id"]: item for item in mutated["resource_claims"]}
        original_id = next(
            claim_id
            for claim_id in target_atom["resource_claim_ids"]
            if claim_by_id[claim_id]["resource_kind"] == target_kind
        )
        unrelated_atom = next(
            item
            for item in mutated["atoms"]
            if item["instance_id"] != target_atom["instance_id"]
        )
        transplanted = copy.deepcopy(claim_by_id[original_id])
        transplanted["claim_id"] = "claim_owner_substitution_probe"
        transplanted["claimant_id"] = unrelated_atom["instance_id"]
        mutated["resource_claims"].append(transplanted)
        target_atom["resource_claim_ids"] = [
            transplanted["claim_id"] if claim_id == original_id else claim_id
            for claim_id in target_atom["resource_claim_ids"]
        ]
        assert_result_flips(
            resource_case,
            resource_oracle,
            mutated,
            str(resource_result["obligation_id"]),
        )

        (
            role_case,
            role_oracle,
            role_scene,
            role_result,
            _role_mapping,
            role_candidate_ids,
            role_owners,
        ) = find_owner_result("required_event_role_v1")
        mutated = copy.deepcopy(role_scene)
        target_role = next(
            item["target_id"]
            for item in role_result["target_results"]
            if item["passed"]
        )
        target_atom = next(
            item
            for item in mutated["atoms"]
            if item["instance_id"] == role_owners[0]["instance_id"]
        )
        binding = next(
            item for item in target_atom["bindings"] if item["role_id"] == target_role
        )
        binding["node_id"] = "unrelated_role_value_probe"
        assert_result_flips(
            role_case,
            role_oracle,
            mutated,
            str(role_result["obligation_id"]),
        )

        # Preserve the exact required role/value binding globally on a
        # different selected atom while corrupting it only on the reviewed
        # mapping owner.  Scene-global role evidence must not substitute for
        # the mapping-local visual owner edge.
        mutated = copy.deepcopy(role_scene)
        target_atom = next(
            item
            for item in mutated["atoms"]
            if item["instance_id"] == role_owners[0]["instance_id"]
        )
        binding = next(
            item for item in target_atom["bindings"] if item["role_id"] == target_role
        )
        unrelated_atom = next(
            item
            for item in mutated["atoms"]
            if item["instance_id"] != target_atom["instance_id"]
            and item["candidate_id"] not in role_candidate_ids
        )
        if not any(item == binding for item in unrelated_atom["bindings"]):
            unrelated_atom["bindings"].append(copy.deepcopy(binding))
        binding["node_id"] = "unrelated_role_value_probe"
        assert_result_flips(
            role_case,
            role_oracle,
            mutated,
            str(role_result["obligation_id"]),
        )

        (
            bridge_case,
            bridge_oracle,
            bridge_scene,
            bridge_result,
            _bridge_mapping,
            _bridge_candidate_ids,
            bridge_owners,
        ) = find_owner_result("required_runtime_bridge_type_v1")
        mutated = copy.deepcopy(bridge_scene)
        target_type = next(
            item["target_id"]
            for item in bridge_result["target_results"]
            if item["passed"]
        )
        owner_atom = bridge_owners[0]
        bridge = next(
            item
            for item in mutated["bridges"]
            if item["bridge_type"] == target_type
            and owner_atom["instance_id"] in {item["from_node_id"], item["to_node_id"]}
        )
        bridge["candidate_id"] = next(
            item["candidate_id"]
            for item in mutated["atoms"]
            if item["candidate_id"] != owner_atom["candidate_id"]
            and target_type
            not in self.universal_assets.candidate_by_id[item["candidate_id"]][
                "runtime_contract"
            ]["bridge_types"]
        )
        assert_result_flips(
            bridge_case,
            bridge_oracle,
            mutated,
            str(bridge_result["obligation_id"]),
        )

        mutated = copy.deepcopy(bridge_scene)
        bridge = next(
            item
            for item in mutated["bridges"]
            if item["bridge_type"] == target_type
            and owner_atom["instance_id"] in {item["from_node_id"], item["to_node_id"]}
        )
        unrelated_instance_id = next(
            item["instance_id"]
            for item in mutated["atoms"]
            if item["instance_id"] != owner_atom["instance_id"]
        )
        if bridge["from_node_id"] == owner_atom["instance_id"]:
            bridge["from_node_id"] = unrelated_instance_id
        if bridge["to_node_id"] == owner_atom["instance_id"]:
            bridge["to_node_id"] = unrelated_instance_id
        assert_result_flips(
            bridge_case,
            bridge_oracle,
            mutated,
            str(bridge_result["obligation_id"]),
        )

        mutated = copy.deepcopy(bridge_scene)
        bridge = next(
            item
            for item in mutated["bridges"]
            if item["bridge_type"] == target_type
            and owner_atom["instance_id"] in {item["from_node_id"], item["to_node_id"]}
        )
        pixel_by_id = {
            item["item_id"]: item
            for item in mutated["pixel_evidence_contract"]["items"]
        }
        pixel_by_id[bridge["pixel_evidence_ids"][0]]["source_id"] = (
            "unrelated_bridge_probe"
        )
        assert_result_flips(
            bridge_case,
            bridge_oracle,
            mutated,
            str(bridge_result["obligation_id"]),
        )

        mutated_candidates = copy.deepcopy(dict(self.universal_assets.candidate_by_id))
        mutated_candidates[owner_atom["candidate_id"]]["runtime_contract"][
            "bridge_types"
        ] = [
            bridge_type
            for bridge_type in mutated_candidates[owner_atom["candidate_id"]][
                "runtime_contract"
            ]["bridge_types"]
            if bridge_type != target_type
        ]
        mutated_assets = replace(
            self.universal_assets,
            candidate_by_id=mutated_candidates,
        )
        assert_result_flips(
            bridge_case,
            bridge_oracle,
            copy.deepcopy(bridge_scene),
            str(bridge_result["obligation_id"]),
            mutated_assets,
        )

        eligible_case = eligible_oracle = eligible_scene = eligible_result = None
        for case_id, output in base_outputs.items():
            for result in output["results"]:
                if (
                    result["evaluator_id"] == "eligible_visual_candidate_v1"
                    and result["passed"]
                    and len(result["target_results"]) == 1
                ):
                    eligible_case = case_id
                    eligible_oracle = self.current_oracle_by_case[case_id]
                    eligible_scene = self.packs[case_id]["universal_scene"]
                    eligible_result = result
                    break
            if eligible_result is not None:
                break
        self.assertIsNotNone(eligible_result)
        mutated = copy.deepcopy(eligible_scene)
        target_id = eligible_result["target_results"][0]["target_id"]
        facet = self.universal_assets.candidate_by_id[target_id]["facet"]
        trace = mutated["selection_trace"]
        rejection_by_id = {
            item["candidate_id"]: item for item in trace["candidate_rejections"]
        }
        replacement_reason = next(iter(rejection_by_id.values()))["reason_code"]
        trace["eligible_candidate_ids_by_facet"][facet] = sorted(
            set(trace["eligible_candidate_ids_by_facet"][facet]) - {target_id}
        )
        trace["candidate_rejections"] = sorted(
            trace["candidate_rejections"]
            + [{"candidate_id": target_id, "reason_code": replacement_reason}],
            key=lambda item: item["candidate_id"],
        )
        trace["eligible_count_by_facet"][facet] = len(
            trace["eligible_candidate_ids_by_facet"][facet]
        )
        trace["rejection_count_by_code"] = dict(
            sorted(
                Counter(
                    item["reason_code"] for item in trace["candidate_rejections"]
                ).items()
            )
        )
        assert_result_flips(
            str(eligible_case),
            eligible_oracle,
            mutated,
            str(eligible_result["obligation_id"]),
        )

        fixed_prop_case = "universal_scene_11_gesture_function"
        fixed_prop_scene = self.packs[fixed_prop_case]["universal_scene"]
        fixed_prop_oracle = self.current_oracle_by_case[fixed_prop_case]
        fixed_prop_output = base_outputs[fixed_prop_case]
        fixed_prop_result = next(
            result
            for result in fixed_prop_output["results"]
            if result["evaluator_id"] == "eligible_atom_facet_v1"
            and [item["target_id"] for item in result["target_results"]] == ["prop"]
        )
        self.assertTrue(fixed_prop_result["passed"], fixed_prop_result)
        self.assertFalse(
            any(atom["facet"] == "prop" for atom in fixed_prop_scene["atoms"]),
            "fixed-prop eligibility must not require selecting a prop atom",
        )
        self.assertEqual(
            ["uer_role_bearing_contact"],
            fixed_prop_scene["selection_trace"]["eligible_candidate_ids_by_facet"][
                "prop"
            ],
        )
        mutated = copy.deepcopy(fixed_prop_scene)
        trace = mutated["selection_trace"]
        trace["eligible_candidate_ids_by_facet"]["prop"] = []
        trace["eligible_count_by_facet"]["prop"] = 0
        trace["candidate_rejections"].append(
            {
                "candidate_id": "uer_role_bearing_contact",
                "reason_code": "fixed_prop_eligibility_probe",
            }
        )
        trace["candidate_rejections"].sort(key=lambda item: item["candidate_id"])
        trace["rejection_count_by_code"] = dict(
            sorted(
                Counter(
                    item["reason_code"] for item in trace["candidate_rejections"]
                ).items()
            )
        )
        assert_result_flips(
            fixed_prop_case,
            fixed_prop_oracle,
            mutated,
            str(fixed_prop_result["obligation_id"]),
        )

    def test_runtime_selected_role_sources_reject_authority_substitution(self) -> None:
        def role(scene: dict[str, object], role_id: str) -> dict[str, object]:
            selected_event = scene["selected_event"]
            self.assertIsInstance(selected_event, dict)
            roles = selected_event["roles"]
            self.assertIsInstance(roles, list)
            selected = next(
                item
                for item in roles
                if isinstance(item, dict) and item["role_id"] == role_id
            )
            self.assertEqual("runtime_selected", selected["source"])
            self.assertIsNotNone(selected["value_id"])
            return selected

        def assert_both_boundaries_reject(
            pack: dict[str, object], role_id: str
        ) -> None:
            scene = pack["universal_scene"]
            self.assertIsInstance(scene, dict)
            selected_role = role(scene, role_id)
            validated = validate_scene_contract(
                str(pack["request_contract"]["request_text"]),
                scene["scene_contract"],
                assets=self.universal_assets,
            )
            with self.assertRaises(universal_runtime_module.SelectionError):
                universal_runtime_module._runtime_selected_role_authority(
                    selected_role,
                    selection=scene,
                    validated=validated,
                    assets=self.universal_assets,
                )
            failures = (
                illustration_audit_module._audit_runtime_selected_role_source_failures(
                    scene, self.universal_assets
                )
            )
            self.assertTrue(failures, (role_id, selected_role))
            self.assertEqual({"universal_event_spine"}, _checks(failures))
            self.assert_integrity_failure(pack, "universal_event_spine")

        proposal = copy.deepcopy(self.packs["universal_scene_01_same_core_low"])
        proposal_scene = proposal["universal_scene"]
        proposal_role = role(proposal_scene, "action")
        proposal_role["source_id"] = next(
            atom["instance_id"]
            for atom in proposal_scene["atoms"]
            if atom["instance_id"] != proposal_role["source_id"]
        )
        assert_both_boundaries_reject(proposal, "action")

        bridge_swap = copy.deepcopy(self.packs["universal_scene_05_explicit_hammer"])
        bridge_scene = bridge_swap["universal_scene"]
        bridge_role = role(bridge_scene, "result")
        bridge_role["source_id"] = next(
            bridge["bridge_id"]
            for bridge in bridge_scene["bridges"]
            if bridge["bridge_id"] != bridge_role["source_id"]
            and bridge["to_node_id"] == bridge_role["value_id"]
            and bridge["bridge_type"] in {"state_change", "consequence"}
        )
        assert_both_boundaries_reject(bridge_swap, "result")

        bridge_to_premise = copy.deepcopy(
            self.packs["universal_scene_05_explicit_hammer"]
        )
        premise_scene = bridge_to_premise["universal_scene"]
        premise_role = role(premise_scene, "result")
        source_bridge = next(
            bridge
            for bridge in premise_scene["bridges"]
            if bridge["bridge_id"] == premise_role["source_id"]
        )
        premise_role["source_id"] = source_bridge["from_node_id"]
        assert_both_boundaries_reject(bridge_to_premise, "result")

        atom_swap = copy.deepcopy(self.packs["universal_scene_05_explicit_hammer"])
        atom_scene = atom_swap["universal_scene"]
        atom_role = role(atom_scene, "phase")
        atom_role["source_id"] = next(
            atom["instance_id"]
            for atom in atom_scene["atoms"]
            if atom["instance_id"] != atom_role["source_id"]
        )
        assert_both_boundaries_reject(atom_swap, "phase")

        duplicate_binding = copy.deepcopy(
            self.packs["universal_scene_05_explicit_hammer"]
        )
        duplicate_scene = duplicate_binding["universal_scene"]
        duplicate_role = role(duplicate_scene, "phase")
        source_atom = next(
            atom
            for atom in duplicate_scene["atoms"]
            if atom["instance_id"] == duplicate_role["source_id"]
        )
        emitted_binding = next(
            binding
            for binding in source_atom["bindings"]
            if binding["role_id"] == "phase"
        )
        source_atom["bindings"].append(copy.deepcopy(emitted_binding))
        assert_both_boundaries_reject(duplicate_binding, "phase")

        missing_source = copy.deepcopy(self.packs["universal_scene_05_explicit_hammer"])
        role(missing_source["universal_scene"], "phase")["source_id"] = (
            "missing_selected_authority_source"
        )
        assert_both_boundaries_reject(missing_source, "phase")

    def test_mixed_contract_effect_reassertion_is_blocked_at_ingress_and_audit(
        self,
    ) -> None:
        case_id = "universal_scene_01_same_core_low"
        row = self.prompt_by_case[case_id]
        contract = copy.deepcopy(self.current_contract_by_case[case_id])
        probe = "No weapon fires. A weapon fires a round."
        request_text = f"{row['request_ko']} {probe}"
        contract["request_text_sha256"] = hashlib.sha256(
            request_text.encode("utf-8")
        ).hexdigest()
        contract["identity_core"]["scene_facts"][1]["request_phrases"].append(probe)
        with mock.patch.object(
            universal_runtime_module,
            "load_universal_scene_assets",
            return_value=self.universal_assets,
        ):
            with self.assertRaisesRegex(
                ResolutionError,
                "uao_weapon_event_guard",
            ):
                build_candidate_pack(
                    request_text,
                    topic=str(row["expected_topic_id"]),
                    format_id=str(row["expected_format"]),
                    seed=int(row["seed"]),
                    creativity=float(row["creativity"]),
                    scene_contract=contract,
                    assets=self.legacy_assets,
                )

        stale = copy.deepcopy(self.packs[case_id])
        stale["request_contract"]["request_text"] = request_text
        stale_contract = stale["universal_scene"]["scene_contract"]
        stale_contract["request_text_sha256"] = contract["request_text_sha256"]
        stale_contract["identity_core"]["scene_facts"][1]["request_phrases"].append(
            probe
        )
        stale["universal_scene"]["identity_core"]["scene_facts"] = copy.deepcopy(
            stale_contract["identity_core"]["scene_facts"]
        )
        scene_contract_sha256 = canonical_sha256(stale_contract)
        stale["request_contract"]["scene_contract_sha256"] = scene_contract_sha256
        stale["universal_scene"]["selection_trace"]["scene_contract_sha256"] = (
            scene_contract_sha256
        )
        _rehash(stale)
        with mock.patch.object(
            universal_runtime_module,
            "load_universal_scene_assets",
            return_value=self.universal_assets,
        ):
            issues = validate_pack_integrity(stale)
        self.assertIn("universal_hard_gate", _checks(issues), issues)

        semantic = _json(
            ASSET_ROOT / "illustration_universal_semantic_bindings_v1.json"
        )
        effect_case_ids = {
            "active_weapon_discharge": "universal_scene_06_explicit_machine_gun",
            "combat_opponent_assignment": "universal_scene_22_theme_hijack_guard",
            "combat_target_assignment": "universal_scene_22_theme_hijack_guard",
            "navigation_instrument_use": "universal_scene_21_prop_narrative_role",
            "romantic_contact": "universal_scene_22_theme_hijack_guard",
            "scene_promise_hijack": "universal_scene_22_theme_hijack_guard",
            "human_face_attachment": "universal_scene_12_nonhuman_display",
            "human_hand_attachment": "universal_scene_12_nonhuman_display",
            "human_limb_attachment": "universal_scene_12_nonhuman_display",
        }
        negative_clause = {
            "ko": lambda phrase: f"{phrase} 금지",
            "en": lambda phrase: f"do not include {phrase}",
            "ja": lambda phrase: f"{phrase} 禁止",
            "zh": lambda phrase: f"不要{phrase}",
        }
        coordinated_corpora = {
            "ko": lambda phrase: (
                f"{phrase} 금지 그리고 {phrase} 금지",
                f"{phrase} 금지 그러나 장면은 {phrase}",
            ),
            "en": lambda phrase: (
                f"do not include {phrase} and repeat {phrase}",
                f"do not include {phrase} and the scene explicitly includes {phrase}",
            ),
            "ja": lambda phrase: (
                f"{phrase} 禁止 そして {phrase} 禁止",
                f"{phrase} 禁止 しかし場面は {phrase}",
            ),
            "zh": lambda phrase: (
                f"不要包含{phrase}并且重复{phrase}",
                f"不要包含{phrase}但是场景明确包含{phrase}",
            ),
        }
        with mock.patch.object(
            universal_runtime_module,
            "load_universal_scene_assets",
            return_value=self.universal_assets,
        ):
            for profile in semantic["contract_effect_profiles"]:
                effect_id = profile["effect_id"]
                profile_case_id = effect_case_ids[effect_id]
                profile_row = self.prompt_by_case[profile_case_id]
                base_request = str(profile_row["request_ko"])
                for alias_record in profile["literal_aliases"]:
                    locale = alias_record["locale"]
                    positive = alias_record["values"][0]
                    negative = negative_clause[locale](positive)
                    all_negative = f"{negative}. {negative}."
                    negative_request = f"{base_request} {all_negative}"
                    negative_contract = copy.deepcopy(
                        self.current_contract_by_case[profile_case_id]
                    )
                    negative_contract["request_text_sha256"] = hashlib.sha256(
                        negative_request.encode("utf-8")
                    ).hexdigest()
                    negative_pack = build_candidate_pack(
                        negative_request,
                        topic=str(profile_row["expected_topic_id"]),
                        format_id=str(profile_row["expected_format"]),
                        seed=int(profile_row["seed"]),
                        creativity=float(profile_row["creativity"]),
                        scene_contract=negative_contract,
                        assets=self.legacy_assets,
                    )
                    self.assertNotIn(
                        effect_id,
                        negative_pack["universal_scene"]["hard_gate_snapshot"][
                            "observed_effect_ids"
                        ],
                        (effect_id, locale, all_negative),
                    )
                    self.assertEqual(
                        [],
                        validate_pack_integrity(negative_pack),
                        (effect_id, locale, all_negative),
                    )

                    for order, mixed in (
                        (
                            "negative_then_positive",
                            f"{negative}. {positive}.",
                        ),
                        (
                            "positive_then_negative",
                            f"{positive}. {negative}.",
                        ),
                    ):
                        mixed_request = f"{base_request} {mixed}"
                        mixed_contract = copy.deepcopy(
                            self.current_contract_by_case[profile_case_id]
                        )
                        mixed_contract["request_text_sha256"] = hashlib.sha256(
                            mixed_request.encode("utf-8")
                        ).hexdigest()
                        with self.subTest(
                            effect_id=effect_id,
                            locale=locale,
                            order=order,
                        ):
                            with self.assertRaises(
                                (InputContractError, ResolutionError)
                            ):
                                build_candidate_pack(
                                    mixed_request,
                                    topic=str(profile_row["expected_topic_id"]),
                                    format_id=str(profile_row["expected_format"]),
                                    seed=int(profile_row["seed"]),
                                    creativity=float(profile_row["creativity"]),
                                    scene_contract=mixed_contract,
                                    assets=self.legacy_assets,
                                )

                            stale_mixed = copy.deepcopy(negative_pack)
                            stale_mixed["request_contract"]["request_text"] = (
                                mixed_request
                            )
                            stale_contract = stale_mixed["universal_scene"][
                                "scene_contract"
                            ]
                            stale_contract["request_text_sha256"] = mixed_contract[
                                "request_text_sha256"
                            ]
                            stale_contract_sha256 = canonical_sha256(stale_contract)
                            stale_mixed["request_contract"]["scene_contract_sha256"] = (
                                stale_contract_sha256
                            )
                            stale_mixed["universal_scene"]["selection_trace"][
                                "scene_contract_sha256"
                            ] = stale_contract_sha256
                            _rehash(stale_mixed)
                            stale_issues = validate_pack_integrity(stale_mixed)
                            self.assertIn(
                                "universal_hard_gate",
                                _checks(stale_issues),
                                stale_issues,
                            )

                    coordinated_negative, coordinated_mixed = coordinated_corpora[
                        locale
                    ](positive)
                    coordinated_negative_request = (
                        f"{base_request} {coordinated_negative}"
                    )
                    coordinated_negative_contract = copy.deepcopy(
                        self.current_contract_by_case[profile_case_id]
                    )
                    coordinated_negative_contract["request_text_sha256"] = (
                        hashlib.sha256(
                            coordinated_negative_request.encode("utf-8")
                        ).hexdigest()
                    )
                    coordinated_negative_pack = build_candidate_pack(
                        coordinated_negative_request,
                        topic=str(profile_row["expected_topic_id"]),
                        format_id=str(profile_row["expected_format"]),
                        seed=int(profile_row["seed"]),
                        creativity=float(profile_row["creativity"]),
                        scene_contract=coordinated_negative_contract,
                        assets=self.legacy_assets,
                    )
                    self.assertNotIn(
                        effect_id,
                        coordinated_negative_pack["universal_scene"][
                            "hard_gate_snapshot"
                        ]["observed_effect_ids"],
                        (effect_id, locale, coordinated_negative),
                    )
                    self.assertEqual(
                        [],
                        validate_pack_integrity(coordinated_negative_pack),
                        (effect_id, locale, coordinated_negative),
                    )

                    coordinated_mixed_request = f"{base_request} {coordinated_mixed}"
                    coordinated_mixed_contract = copy.deepcopy(
                        self.current_contract_by_case[profile_case_id]
                    )
                    coordinated_mixed_contract["request_text_sha256"] = hashlib.sha256(
                        coordinated_mixed_request.encode("utf-8")
                    ).hexdigest()
                    with self.subTest(
                        effect_id=effect_id,
                        locale=locale,
                        order="coordinated_independent_reassertion",
                    ):
                        with self.assertRaises((InputContractError, ResolutionError)):
                            build_candidate_pack(
                                coordinated_mixed_request,
                                topic=str(profile_row["expected_topic_id"]),
                                format_id=str(profile_row["expected_format"]),
                                seed=int(profile_row["seed"]),
                                creativity=float(profile_row["creativity"]),
                                scene_contract=coordinated_mixed_contract,
                                assets=self.legacy_assets,
                            )

                        stale_coordinated = copy.deepcopy(coordinated_negative_pack)
                        stale_coordinated["request_contract"]["request_text"] = (
                            coordinated_mixed_request
                        )
                        stale_contract = stale_coordinated["universal_scene"][
                            "scene_contract"
                        ]
                        stale_contract["request_text_sha256"] = (
                            coordinated_mixed_contract["request_text_sha256"]
                        )
                        stale_contract_sha256 = canonical_sha256(stale_contract)
                        stale_coordinated["request_contract"][
                            "scene_contract_sha256"
                        ] = stale_contract_sha256
                        stale_coordinated["universal_scene"]["selection_trace"][
                            "scene_contract_sha256"
                        ] = stale_contract_sha256
                        _rehash(stale_coordinated)
                        stale_issues = validate_pack_integrity(stale_coordinated)
                        self.assertIn(
                            "universal_hard_gate",
                            _checks(stale_issues),
                            stale_issues,
                        )

    def test_mixed_hand_and_navigation_effects_are_blocked_at_ingress(self) -> None:
        probes = (
            (
                "universal_scene_12_nonhuman_display",
                "Do not attach a flesh colored palm. A flesh colored palm sprouts.",
                "Do not attach a flesh colored palm. "
                "A flesh colored palm must not sprout.",
                "ubp_embodiment_capability_guard",
            ),
            (
                "universal_scene_21_prop_narrative_role",
                "Do not use a compass as a tool. Use the compass as a navigation tool.",
                "Do not use a compass as a tool. "
                "Do not use the compass as a navigation tool.",
                "uer_narrative_inference_guard",
            ),
        )
        with mock.patch.object(
            universal_runtime_module,
            "load_universal_scene_assets",
            return_value=self.universal_assets,
        ):
            for case_id, mixed, all_negative, expected_guard in probes:
                row = self.prompt_by_case[case_id]
                for corpus, should_block in (
                    (mixed, True),
                    (all_negative, False),
                ):
                    request_text = f"{row['request_ko']} {corpus}"
                    contract = copy.deepcopy(self.current_contract_by_case[case_id])
                    contract["request_text_sha256"] = hashlib.sha256(
                        request_text.encode("utf-8")
                    ).hexdigest()
                    kwargs = {
                        "topic": str(row["expected_topic_id"]),
                        "format_id": str(row["expected_format"]),
                        "seed": int(row["seed"]),
                        "creativity": float(row["creativity"]),
                        "scene_contract": contract,
                        "assets": self.legacy_assets,
                    }
                    with self.subTest(
                        case_id=case_id,
                        should_block=should_block,
                    ):
                        if should_block:
                            with self.assertRaisesRegex(
                                ResolutionError,
                                expected_guard,
                            ):
                                build_candidate_pack(request_text, **kwargs)
                        else:
                            build_candidate_pack(request_text, **kwargs)

    def test_coordinated_weapon_negative_list_keeps_scope_at_ingress(self) -> None:
        case_id = "universal_scene_06_explicit_machine_gun"
        row = self.prompt_by_case[case_id]
        contract = self.current_contract_by_case[case_id]
        corpora = (
            ("Do not fire the machine gun and shoot the gun.", False),
            (
                "Weapon firing must not appear and the weapon fires a round.",
                True,
            ),
        )
        with mock.patch.object(
            universal_runtime_module,
            "load_universal_scene_assets",
            return_value=self.universal_assets,
        ):
            for corpus, should_block in corpora:
                request_text = f"{row['request_ko']} {corpus}"
                mutated_contract = copy.deepcopy(contract)
                mutated_contract["request_text_sha256"] = hashlib.sha256(
                    request_text.encode("utf-8")
                ).hexdigest()
                kwargs = {
                    "topic": str(row["expected_topic_id"]),
                    "format_id": str(row["expected_format"]),
                    "seed": int(row["seed"]),
                    "creativity": float(row["creativity"]),
                    "scene_contract": mutated_contract,
                    "assets": self.legacy_assets,
                }
                with self.subTest(corpus=corpus):
                    if should_block:
                        with self.assertRaisesRegex(
                            InputContractError,
                            "context_profile.violence=nonviolent",
                        ):
                            build_candidate_pack(request_text, **kwargs)
                    else:
                        build_candidate_pack(request_text, **kwargs)

    def test_all_24_composition_carriers_support_clean_literal_evidence(self) -> None:
        for case_id, pack in self.packs.items():
            with self.subTest(case_id=case_id):
                composed, prompt = _literal_universal_evidence(pack)
                self.assertEqual(
                    [],
                    audit_universal_scene_evidence(pack, composed, prompt),
                )

    def test_v1_v2_exact_replay_and_photo_baseline_remain_immutable(self) -> None:
        v1 = validate_legacy_prompt_qualification(ASSET_ROOT, self.legacy_assets)
        v2 = validate_prompt_qualification(ASSET_ROOT, self.legacy_assets)
        photo = validate_photo_regression_baseline(ASSET_ROOT)
        self.assertEqual(24, v1["case_count"])
        self.assertEqual(24, v2["case_count"])
        self.assertEqual("pass", photo["status"])

        concept = "Adult rescue partners exchange a repaired tool."
        for version in (V1_CONTRACT_VERSION, V2_CONTRACT_VERSION):
            with self.subTest(version=version):
                first = build_candidate_pack(
                    concept,
                    topic="ensemble_relationship_staging",
                    format_id="ensemble_key_art",
                    seed=42,
                    creativity=0.5,
                    contract_version=version,
                    assets=self.legacy_assets,
                )
                second = build_candidate_pack(
                    concept,
                    topic="ensemble_relationship_staging",
                    format_id="ensemble_key_art",
                    seed=42,
                    creativity=0.5,
                    contract_version=version,
                    assets=self.legacy_assets,
                )
                self.assertEqual(first, second)
                self.assertNotIn("universal_scene", first)

    def test_prior_exposure_ids_are_unique_recorded_and_replayed(self) -> None:
        case_id = "universal_scene_02_same_core_mid"
        row = self.prompt_by_case[case_id]
        contract = self.current_contract_by_case[case_id]
        exposure_ids = ("uao_global_prop_apple",)
        first = build_candidate_pack(
            str(row["request_ko"]),
            topic=str(row["expected_topic_id"]),
            format_id=str(row["expected_format"]),
            seed=int(row["seed"]),
            creativity=float(row["creativity"]),
            scene_contract=contract,
            prior_exposure_ids=exposure_ids,
            assets=self.legacy_assets,
        )
        second = build_candidate_pack(
            str(row["request_ko"]),
            topic=str(row["expected_topic_id"]),
            format_id=str(row["expected_format"]),
            seed=int(row["seed"]),
            creativity=float(row["creativity"]),
            scene_contract=contract,
            prior_exposure_ids=exposure_ids,
            assets=self.legacy_assets,
        )
        self.assertEqual(first, second)
        self.assertEqual(
            list(exposure_ids), first["request_contract"]["prior_exposure_ids"]
        )
        self.assertEqual([], validate_pack_integrity(first))
        with self.assertRaises(InputContractError):
            build_candidate_pack(
                str(row["request_ko"]),
                topic=str(row["expected_topic_id"]),
                format_id=str(row["expected_format"]),
                seed=int(row["seed"]),
                creativity=float(row["creativity"]),
                scene_contract=contract,
                prior_exposure_ids=(exposure_ids[0], exposure_ids[0]),
                assets=self.legacy_assets,
            )

    def test_same_core_creativity_changes_distribution_not_identity_or_hard_gates(
        self,
    ) -> None:
        case_ids = [
            "universal_scene_01_same_core_low",
            "universal_scene_02_same_core_mid",
            "universal_scene_03_same_core_high",
        ]
        scenes = [self.packs[case_id]["universal_scene"] for case_id in case_ids]
        identities = [scene["identity_core"] for scene in scenes]
        slots = [scene["slot_states"] for scene in scenes]
        traces = [scene["selection_trace"] for scene in scenes]
        distances = [scene["semantic_distance_trace"] for scene in scenes]
        self.assertEqual(identities[0], identities[1])
        self.assertEqual(identities[1], identities[2])
        self.assertEqual(slots[0], slots[1])
        self.assertEqual(slots[1], slots[2])
        self.assertEqual(
            traces[0]["eligible_count_by_facet"], traces[1]["eligible_count_by_facet"]
        )
        self.assertEqual(
            traces[1]["eligible_count_by_facet"], traces[2]["eligible_count_by_facet"]
        )
        self.assertEqual(
            traces[0]["rejection_count_by_code"], traces[1]["rejection_count_by_code"]
        )
        self.assertEqual(
            traces[1]["rejection_count_by_code"], traces[2]["rejection_count_by_code"]
        )
        self.assertEqual(
            [len(scenes[0]["atoms"])] * 3,
            [len(scene["atoms"]) for scene in scenes],
        )
        self.assertEqual(
            ["near", "middle", "far"], [trace["target_band"] for trace in distances]
        )
        self.assertEqual(
            [1, 1, 1], [trace["max_optional_remote_count"] for trace in distances]
        )
        for scene in scenes:
            distance = scene["semantic_distance_trace"]
            self.assertLessEqual(distance["optional_remote_count"], 1)
            if distance["fixed_remote_count"]:
                self.assertEqual(0, distance["optional_remote_count"])
        self.assertEqual(
            ["near", "middle", "far"], [trace["selected_band"] for trace in distances]
        )
        self.assertGreaterEqual(len(scenes[0]["bridges"]), 1)
        self.assertGreaterEqual(
            len({bridge["bridge_type"] for bridge in scenes[1]["bridges"]}), 2
        )
        high_types = {bridge["bridge_type"] for bridge in scenes[2]["bridges"]}
        self.assertTrue(high_types & {"affordance", "motivation", "identity_contrast"})
        self.assertTrue(high_types & {"mechanics", "ownership"})
        self.assertTrue(high_types & {"state_change", "consequence"})

    def test_apple_hammer_machine_gun_preserve_roles_with_increasing_load(self) -> None:
        cases = [
            "universal_scene_04_explicit_apple",
            "universal_scene_05_explicit_hammer",
            "universal_scene_06_explicit_machine_gun",
        ]
        expected_terms = ("apple", "hammer", "machine_gun")
        expected_bands = ("near", "middle", "far")
        expected_prop_roles = (
            {"target": "one_apple", "instrument": None},
            {"target": "loose_halo_mount", "instrument": "small_hammer"},
            {
                "target": "unmarked_decommissioned_machine_gun",
                "instrument": None,
            },
        )
        previous_load = -1
        category_members = {
            "entry": {"affordance", "motivation", "identity_contrast"},
            "mediation": {"mechanics", "ownership"},
            "exit": {"state_change", "consequence"},
        }
        band_requirements = {
            "near": (1, ("entry",)),
            "middle": (2, ("entry", "exit")),
            "far": (3, ("entry", "mediation", "exit")),
        }
        for case_id, expected_term, expected_band, expected_roles in zip(
            cases,
            expected_terms,
            expected_bands,
            expected_prop_roles,
        ):
            with self.subTest(case_id=case_id):
                pack = self.packs[case_id]
                scene = pack["universal_scene"]
                serialized = (
                    json.dumps(scene, ensure_ascii=False).casefold().replace(" ", "_")
                )
                self.assertIn(expected_term, serialized)
                roles = _role_by_id(pack)
                for role_id, value_id in expected_roles.items():
                    self.assertEqual(value_id, roles[role_id]["value_id"])
                contract = self.current_contract_by_case[case_id]
                for fixed_role in contract["event_roles"]:
                    if fixed_role["state"] == "fixed":
                        self.assertEqual(
                            fixed_role["value_id"],
                            roles[fixed_role["role_id"]]["value_id"],
                        )
                self.assertEqual(
                    expected_band, scene["semantic_distance_trace"]["selected_band"]
                )
                load = sum(scene["semantic_distance_trace"]["vector"].values())
                bridge_types = {
                    bridge["bridge_type"] for bridge in scene["bridges"]
                }
                self.assertGreater(load, previous_load)
                minimum_count, required_categories = band_requirements[expected_band]
                self.assertGreaterEqual(len(bridge_types), minimum_count)
                for category in required_categories:
                    self.assertTrue(
                        bridge_types & category_members[category],
                        (case_id, category, bridge_types),
                    )
                previous_load = load

    def test_human_nonhuman_faceless_limbless_four_arm_and_no_prop_resources(
        self,
    ) -> None:
        for case_id in (
            "universal_scene_11_gesture_function",
            "universal_scene_12_nonhuman_display",
            "universal_scene_16_contact_resource",
            "universal_scene_24_closed_no_prop_consequence",
        ):
            with self.subTest(case_id=case_id):
                pack = self.packs[case_id]
                self.assertEqual([], validate_pack_integrity(pack))
                scene = pack["universal_scene"]
                capacities = {
                    (item["entity_id"], item["resource_kind"]): item["capacity"]
                    for item in scene["identity_core"]["capability_capacities"]
                }
                usage: dict[tuple[str, str], int] = {}
                for claim in scene["resource_claims"]:
                    key = (claim["owner_id"], claim["resource_kind"])
                    if claim["mode"] == "exclusive":
                        usage[key] = usage.get(key, 0) + claim["amount"]
                    else:
                        usage[key] = max(usage.get(key, 0), claim["amount"])
                for key, amount in usage.items():
                    self.assertLessEqual(amount, capacities[key])

        for case_id in (
            "universal_scene_12_nonhuman_display",
            "universal_scene_24_closed_no_prop_consequence",
        ):
            scene = self.packs[case_id]["universal_scene"]
            self.assertFalse(
                {"prop", "prop_state"} & {atom["facet"] for atom in scene["atoms"]}
            )
            self.assertIsNone(
                _role_by_id(self.packs[case_id])["instrument"]["value_id"]
            )

        nonhuman_scene = self.packs["universal_scene_12_nonhuman_display"][
            "universal_scene"
        ]
        self.assertFalse(
            any(
                claim["resource_kind"] in {"manipulator", "facial_display"}
                and claim["amount"] > 0
                for claim in nonhuman_scene["resource_claims"]
            )
        )
        four_arm = self.packs["universal_scene_16_contact_resource"]["universal_scene"]
        manipulator_caps = [
            value["capacity"]
            for value in four_arm["identity_core"]["capability_capacities"]
            if value["resource_kind"] == "manipulator"
        ]
        self.assertIn(4, manipulator_caps)

    def test_scene_contract_hash_literal_and_closed_slot_mutations_reject(self) -> None:
        fixed_case_id = "universal_scene_12_nonhuman_display"
        original = self.current_contract_by_case[fixed_case_id]
        mutations: list[tuple[str, str, dict[str, object]]] = []

        bad_hash = copy.deepcopy(original)
        bad_hash["request_text_sha256"] = "0" * 64
        mutations.append(("request hash", fixed_case_id, bad_hash))

        missing_literal = copy.deepcopy(original)
        missing_literal["identity_core"]["entities"][0]["feature_facts"][0][
            "request_phrases"
        ] = ["원문에 없는 정체성"]
        mutations.append(("identity overwrite", fixed_case_id, missing_literal))

        open_case_id = "universal_scene_01_same_core_low"
        open_inference = copy.deepcopy(self.current_contract_by_case[open_case_id])
        open_slot = next(
            slot for slot in open_inference["slot_states"] if slot["state"] == "open"
        )
        open_slot["value_ids"] = ["agent_inferred_value"]
        mutations.append(("open slot inference", open_case_id, open_inference))

        closed_case_id = "universal_scene_24_closed_no_prop_consequence"
        closed_selection = copy.deepcopy(self.current_contract_by_case[closed_case_id])
        closed_slot = next(
            slot
            for slot in closed_selection["slot_states"]
            if slot["state"] == "closed"
        )
        closed_slot["value_ids"] = ["selected_into_closed_slot"]
        mutations.append(("closed slot selection", closed_case_id, closed_selection))

        apple_case_id = "universal_scene_04_explicit_apple"
        rebound_known_prop = copy.deepcopy(self.current_contract_by_case[apple_case_id])
        apple_fact = next(
            fact
            for fact in rebound_known_prop["identity_core"]["scene_facts"]
            if fact["id"] == "one_apple"
        )
        apple_fact["id"] = "decommissioned_machine_gun"
        apple_slot = next(
            slot
            for slot in rebound_known_prop["slot_states"]
            if slot["slot_id"] == "prop"
        )
        apple_slot["value_ids"] = ["unmarked_decommissioned_machine_gun"]
        apple_target = next(
            role
            for role in rebound_known_prop["event_roles"]
            if role["role_id"] == "target"
        )
        apple_target["value_id"] = "unmarked_decommissioned_machine_gun"
        mutations.append(
            ("known prop semantic rebound", apple_case_id, rebound_known_prop)
        )

        for label, case_id, contract in mutations:
            with self.subTest(label=label):
                row = self.prompt_by_case[case_id]
                with self.assertRaises(
                    (UniversalInputContractError, InputContractError)
                ):
                    validate_scene_contract(
                        str(row["request_ko"]),
                        contract,
                        assets=self.universal_assets,
                    )

    def test_pack_mutations_reject_core_orphan_remote_closed_and_resources(
        self,
    ) -> None:
        rebound_contract = copy.deepcopy(self.packs["universal_scene_01_same_core_low"])
        embedded_contract = rebound_contract["universal_scene"]["scene_contract"]
        embedded_contract["context_profile"]["tone"] = "quiet_everyday"
        rebound_hash = canonical_sha256(embedded_contract)
        rebound_contract["request_contract"]["scene_contract_sha256"] = rebound_hash
        rebound_contract["universal_scene"]["selection_trace"][
            "scene_contract_sha256"
        ] = rebound_hash
        self.assert_integrity_failure(rebound_contract, "universal_scene_contract")

        known_prop_rebound = copy.deepcopy(
            self.packs["universal_scene_04_explicit_apple"]
        )
        rebound_scene = known_prop_rebound["universal_scene"]
        rebound_embedded = rebound_scene["scene_contract"]
        rebound_fact = next(
            fact
            for fact in rebound_embedded["identity_core"]["scene_facts"]
            if fact["id"] == "one_apple"
        )
        rebound_fact["id"] = "decommissioned_machine_gun"
        rebound_slot = next(
            slot
            for slot in rebound_embedded["slot_states"]
            if slot["slot_id"] == "prop"
        )
        rebound_slot["value_ids"] = ["unmarked_decommissioned_machine_gun"]
        rebound_target = next(
            role
            for role in rebound_embedded["event_roles"]
            if role["role_id"] == "target"
        )
        rebound_target["value_id"] = "unmarked_decommissioned_machine_gun"
        rebound_scene["identity_core"]["scene_facts"] = copy.deepcopy(
            rebound_embedded["identity_core"]["scene_facts"]
        )
        rebound_scene["slot_states"] = copy.deepcopy(rebound_embedded["slot_states"])
        _role_by_id(known_prop_rebound)["target"]["value_id"] = (
            "unmarked_decommissioned_machine_gun"
        )
        known_prop_hash = canonical_sha256(rebound_embedded)
        known_prop_rebound["request_contract"]["scene_contract_sha256"] = (
            known_prop_hash
        )
        rebound_scene["selection_trace"]["scene_contract_sha256"] = known_prop_hash
        self.assert_integrity_failure(
            known_prop_rebound,
            "universal_slot_state",
        )

        context = copy.deepcopy(self.packs["universal_scene_01_same_core_low"])
        context["universal_scene"]["context_profile"].pop("tone")
        self.assert_integrity_failure(context, "universal_scene_contract")

        identity = copy.deepcopy(self.packs["universal_scene_07_fixed_facial_motion"])
        identity["universal_scene"]["identity_core"]["entities"][0]["feature_facts"][0][
            "request_phrases"
        ] = ["not literal in request"]
        self.assert_integrity_failure(identity, "universal_identity_core")

        orphan = copy.deepcopy(self.packs["universal_scene_03_same_core_high"])
        atom = copy.deepcopy(orphan["universal_scene"]["atoms"][0])
        atom["instance_id"] = "atom_orphan_mutation"
        atom["event_edge_ids"] = []
        atom["resource_claim_ids"] = []
        atom["pixel_evidence_ids"] = []
        orphan["universal_scene"]["atoms"].append(atom)
        self.assert_integrity_failure(orphan, "universal_event_spine")

        remote = copy.deepcopy(self.packs["universal_scene_03_same_core_high"])
        trace = remote["universal_scene"]["semantic_distance_trace"]
        trace["optional_remote_count"] = 2
        self.assert_integrity_failure(remote, "universal_semantic_distance")

        closed = copy.deepcopy(
            self.packs["universal_scene_24_closed_no_prop_consequence"]
        )
        atom = next(
            item
            for item in closed["universal_scene"]["atoms"]
            if "literal_realization_profile_id" not in item["parameters"]
        )
        atom["facet"] = "prop"
        self.assert_integrity_failure(closed, "universal_slot_state")

        resource_cases = (
            ("universal_scene_12_nonhuman_display", "manipulator"),
            ("universal_scene_09_shared_attention", "attention_channel"),
            ("universal_scene_10_pose_support", "support_contact"),
        )
        for case_id, resource_kind in resource_cases:
            with self.subTest(case_id=case_id, resource_kind=resource_kind):
                pack = copy.deepcopy(self.packs[case_id])
                scene = pack["universal_scene"]
                capacity = next(
                    item
                    for item in scene["identity_core"]["capability_capacities"]
                    if item["resource_kind"] == resource_kind
                )
                claim_id = f"claim_mutation_{resource_kind}"
                atom = scene["atoms"][0]
                scene["resource_claims"].append(
                    {
                        "claim_id": claim_id,
                        "resource_kind": resource_kind,
                        "owner_id": capacity["entity_id"],
                        "amount": capacity["capacity"] + 1,
                        "mode": "exclusive",
                        "claimant_id": atom["instance_id"],
                        "phase_id": scene["selected_event"]["phase_id"],
                        "evidence_required": False,
                    }
                )
                atom["resource_claim_ids"].append(claim_id)
                self.assert_integrity_failure(pack, "universal_resource_capacity")

        salience = copy.deepcopy(self.packs["universal_scene_03_same_core_high"])
        salience["universal_scene"]["pixel_evidence_contract"][
            "core_anchor_item_ids"
        ] = []
        self.assert_integrity_failure(salience, "universal_bridge_contract")

        weapon_bypass = copy.deepcopy(self.packs["universal_scene_01_same_core_low"])
        prop_atom = next(
            atom
            for atom in weapon_bypass["universal_scene"]["atoms"]
            if atom["facet"] == "prop"
        )
        prop_atom["candidate_id"] = "uao_global_prop_machine_gun"
        # The substituted atom no longer owns the retained event-role source;
        # the auditor correctly rejects that broken authority edge first.
        self.assert_integrity_failure(
            weapon_bypass,
            "universal_event_spine",
        )

        removed_selection = copy.deepcopy(
            self.packs["universal_scene_01_same_core_low"]
        )
        removed_selection["universal_scene"]["atoms"].pop()
        self.assert_integrity_failure(
            removed_selection,
            "composition_contract",
        )

        unknown_exposure = copy.deepcopy(
            self.packs["universal_scene_01_same_core_low"]
        )
        unknown_exposure["request_contract"]["prior_exposure_ids"] = [
            "unknown_visual_candidate"
        ]
        self.assert_integrity_failure(
            unknown_exposure,
            "universal_candidate_eligibility",
        )

    def test_fixed_slot_composition_evidence_cannot_be_omitted(self) -> None:
        pack = self.packs["universal_scene_04_explicit_apple"]
        composed, prompt = _literal_universal_evidence(pack)
        self.assertEqual([], audit_universal_scene_evidence(pack, composed, prompt))
        omitted = copy.deepcopy(composed)
        omitted_evidence = omitted["universal_scene_evidence"]
        self.assertTrue(omitted_evidence["fixed_slot_phrases"])
        omitted_evidence["fixed_slot_phrases"].pop()
        failures = audit_universal_scene_evidence(pack, omitted, prompt)
        self.assertIn("universal_composition_evidence", _checks(failures), failures)

        substituted = copy.deepcopy(composed)
        substituted_fixed = substituted["universal_scene_evidence"][
            "fixed_slot_phrases"
        ]
        prop_record = next(
            record for record in substituted_fixed if record["slot_id"] == "prop"
        )
        relation_record = next(
            record for record in substituted_fixed if record["slot_id"] == "relation"
        )
        prop_record["phrase"] = relation_record["phrase"]
        failures = audit_universal_scene_evidence(pack, substituted, prompt)
        self.assertIn("universal_composition_semantics", _checks(failures), failures)

        generic = copy.deepcopy(composed)
        generic["universal_scene_evidence"]["atom_phrases"][0]["phrase"] = (
            "visible evidence"
        )
        failures = audit_universal_scene_evidence(pack, generic, prompt)
        self.assertIn("universal_composition_semantics", _checks(failures), failures)

        generic_two_anchor, generic_prompt = _with_linked_evidence_phrase(
            composed,
            section="identity_core_phrases",
            id_key="fact_id",
            record_id="actor_fallen_angel_maid",
            phrase="evidence",
        )
        failures = audit_universal_scene_evidence(
            pack,
            generic_two_anchor,
            generic_prompt,
        )
        self.assertIn("universal_composition_semantics", _checks(failures), failures)

    def test_forbidden_identity_polarity_requires_scoped_negation(self) -> None:
        pack = self.packs["universal_scene_23_soft_prior_remote_bridge"]
        composed, prompt = _literal_universal_evidence(pack)
        self.assertEqual([], audit_universal_scene_evidence(pack, composed, prompt))

        natural, natural_prompt = _with_linked_evidence_phrase(
            composed,
            section="identity_core_phrases",
            id_key="fact_id",
            record_id="chain_used_for_multiple_events",
            phrase="The chain is not used for multiple events.",
        )
        self.assertEqual(
            [],
            audit_universal_scene_evidence(pack, natural, natural_prompt),
        )

        invalid_phrases = (
            "The chain is used for multiple events.",
            "The not-red chain is used for multiple events.",
            "Without red paint, the chain is used for multiple events.",
            "No chain is used for multiple events; chain is used for multiple events.",
            "No chain is used for multiple events, but the chain is used for multiple events.",
            "No chain is used for multiple events and the chain is used for multiple events.",
            "No chain is used for multiple events while the chain is used for multiple events.",
            "No chain is used for multiple events — then the chain is used for multiple events.",
            "No chain is used for multiple events even though the chain is used for multiple events.",
        )
        for phrase in invalid_phrases:
            with self.subTest(phrase=phrase):
                mutated, mutated_prompt = _with_linked_evidence_phrase(
                    composed,
                    section="identity_core_phrases",
                    id_key="fact_id",
                    record_id="chain_used_for_multiple_events",
                    phrase=phrase,
                )
                failures = audit_universal_scene_evidence(
                    pack,
                    mutated,
                    mutated_prompt,
                )
                self.assertIn(
                    "universal_composition_semantics",
                    _checks(failures),
                    failures,
                )

        negative_repeats = (
            "No chain is used for multiple events and no chain is used for multiple events.",
            "The chain is not used for multiple events — the chain is not used for multiple events.",
        )
        for phrase in negative_repeats:
            with self.subTest(phrase=phrase):
                mutated, mutated_prompt = _with_linked_evidence_phrase(
                    composed,
                    section="identity_core_phrases",
                    id_key="fact_id",
                    record_id="chain_used_for_multiple_events",
                    phrase=phrase,
                )
                self.assertEqual(
                    [],
                    audit_universal_scene_evidence(pack, mutated, mutated_prompt),
                )

    def test_asserted_identity_polarity_rejects_absence_not_contrast(self) -> None:
        pack = self.packs["universal_scene_04_explicit_apple"]
        composed, prompt = _literal_universal_evidence(pack)
        self.assertEqual([], audit_universal_scene_evidence(pack, composed, prompt))

        rejected_phrases = (
            "There is not one apple.",
            "The scene lacks one apple.",
            "One apple fails to appear.",
            "Pineapple is visible.",
            "One apple is visible and there is no one apple.",
            "One apple is visible — then no one apple appears.",
        )
        for phrase in rejected_phrases:
            with self.subTest(phrase=phrase):
                mutated, mutated_prompt = _with_linked_evidence_phrase(
                    composed,
                    section="identity_core_phrases",
                    id_key="fact_id",
                    record_id="one_apple",
                    phrase=phrase,
                )
                failures = audit_universal_scene_evidence(
                    pack,
                    mutated,
                    mutated_prompt,
                )
                self.assertIn(
                    "universal_composition_semantics",
                    _checks(failures),
                    failures,
                )

        accepted_phrases = (
            "One apple is not rotten.",
            "Exclude everything except one apple.",
            "One apple is visible and one apple remains visible.",
            "One apple remains visible — then one apple stays visible.",
        )
        for phrase in accepted_phrases:
            with self.subTest(phrase=phrase):
                mutated, mutated_prompt = _with_linked_evidence_phrase(
                    composed,
                    section="identity_core_phrases",
                    id_key="fact_id",
                    record_id="one_apple",
                    phrase=phrase,
                )
                self.assertEqual(
                    [],
                    audit_universal_scene_evidence(
                        pack,
                        mutated,
                        mutated_prompt,
                    ),
                )

    def test_exact_evidence_phrase_reuse_is_bounded_at_eight_links(self) -> None:
        for link_count in (8, 9):
            with self.subTest(link_count=link_count):
                failures = illustration_audit_module._universal_phrase_reuse_failures(
                    {
                        "identity_core": {
                            f"fact_{index}": "shared authenticated carrier phrase"
                            for index in range(link_count)
                        }
                    }
                )
                if link_count == 8:
                    self.assertEqual([], failures)
                else:
                    self.assertIn(
                        "universal_composition_semantics",
                        _checks(failures),
                        failures,
                    )

    def test_unicode_lexical_and_newline_sentence_budgets_fail_closed(self) -> None:
        self.assertEqual(
            150,
            illustration_audit_module._universal_lexical_unit_count("word " * 150),
        )
        self.assertEqual(
            151,
            illustration_audit_module._universal_lexical_unit_count("가" * 151),
        )
        pack = self.packs["universal_scene_08_ambiguous_display_affect"]
        composed, prompt = _literal_universal_evidence(pack)
        self.assertEqual([], audit_universal_scene_evidence(pack, composed, prompt))

        cjk_composed, cjk_prompt = _with_scene_phrase(composed, "가" * 151)
        cjk_failures = audit_universal_scene_evidence(pack, cjk_composed, cjk_prompt)
        self.assertIn("universal_scene_word_budget", _checks(cjk_failures))

        nine_lines = "\n".join(f"line{index}" for index in range(1, 10))
        line_composed, line_prompt = _with_scene_phrase(composed, nine_lines)
        line_failures = audit_universal_scene_evidence(
            pack,
            line_composed,
            line_prompt,
        )
        self.assertIn("universal_scene_word_budget", _checks(line_failures))

    def test_unsupported_emotion_culture_age_gaze_and_weapon_inference_rejects(
        self,
    ) -> None:
        pack = self.packs["universal_scene_07_fixed_facial_motion"]
        phrases = (
            "Her lifted brows prove that her true emotion is fear.",
            "Her lifted brows certify that her true emotion is fear.",
            "Her lifted brows verify that her age is adult.",
            "His eyes reveal that his cultural personality is Japanese.",
            "Her smile confirms that she is adult.",
            "Their gaze proves that they own each other.",
            "The machine gun is safe because its low-salience narrative role is creative.",
            "Fictional styling renders the machine gun safe.",
            "Narrative creativity qualifies the machine gun as allowed.",
        )
        for phrase in phrases:
            with self.subTest(phrase=phrase):
                evidence = {
                    "schema": "illustration-universal-scene-evidence/v1",
                    "scene_block_phrase": phrase,
                    "identity_core_phrases": [],
                    "fixed_slot_phrases": [],
                    "event_role_phrases": [],
                    "atom_phrases": [],
                    "bridge_phrases": [],
                    "resource_phrases": [],
                    "salience_phrases": {
                        "primary_core_event_phrase": phrase,
                        "secondary_discovery_phrase": None,
                        "controlled_rest_phrase": phrase,
                        "remote_carrier_phrase": None,
                    },
                    "consequence_phrase": phrase,
                }
                composed = {
                    "schema": "subculture-illustration-composed-prompt/v3",
                    "universal_scene_evidence": evidence,
                }
                failures = audit_universal_scene_evidence(pack, composed, phrase)
                self.assertIn(
                    "universal_unsupported_inference", _checks(failures), failures
                )

        gun_pack = self.packs["universal_scene_06_explicit_machine_gun"]
        gun_composed, gun_prompt = _literal_universal_evidence(gun_pack)
        self.assertEqual(
            [],
            audit_universal_scene_evidence(gun_pack, gun_composed, gun_prompt),
        )
        contrast = (
            "The machine gun is safe, not because it is fictional, "
            "but because its firing mechanism is removed."
        )
        contrast_composed, contrast_prompt = _with_scene_phrase(
            gun_composed,
            contrast,
        )
        self.assertEqual(
            [],
            audit_universal_scene_evidence(
                gun_pack,
                contrast_composed,
                contrast_prompt,
            ),
        )


if __name__ == "__main__":
    unittest.main()
