"""Declared scene prerequisites and final evidence, never an appeal classifier.

Search may return a conditional idea. This module validates the source contract,
literal witness binding and declared ownership; the composer still judges whether
the witness actually means the prerequisite in the final scene.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Any

from photo_contracts import property_effects_allowed

VERSION = "photo-candidate-context/v1"
RAW_FIELDS = (
    "requires_any_tags", "requires_any", "requires_all_tags", "requires_all",
    "requires_primary_any_tags", "exclude_any_tags", "exclude_any",
    "for_any", "for_all", "exclude_for_any", "not_for", "hard_guards",
)
PRESERVED_FIELDS = (
    "source_candidate_id", "entry_id", "affected_dimensions",
    "context_requirements", "context_prerequisites", "context_preflight",
    "contextual_status", "scene_retrieval_support", "retrieval_status",
    "affected_properties", "expression_scope", "contextual_usage",
)


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode("utf-8")).hexdigest()


def strings(value: Any) -> list[str]:
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list):
        return []
    return sorted({item.strip() for item in value or []
                   if isinstance(item, str) and item.strip()})


def compile_context(entry: dict, source_id: str, quality_sources: list[dict] | None = None) -> dict:
    """Preserve explicit prerequisites and derived guards without admission tags."""
    raw = {key: copy.deepcopy(entry[key]) for key in RAW_FIELDS if entry.get(key)}
    requirements = []

    def add(identifier, operator, context, values, sources):
        if values:
            requirements.append({"id": identifier, "operator": operator,
                                 "context": context, "values": sorted(set(values)),
                                 "sources": sources})

    groups = (
        ("any", "any", "scene", ("requires_any_tags", "requires_any")),
        ("all", "all", "scene", ("requires_all_tags", "requires_all")),
        ("primary_any", "any", "primary", ("requires_primary_any_tags",)),
        ("exclude", "none", "scene", ("exclude_any_tags", "exclude_any")),
        ("subject_any", "any", "subject", ("for_any",)),
        ("subject_all", "all", "subject", ("for_all",)),
        ("subject_exclude", "none", "subject", ("exclude_for_any", "not_for")),
    )
    for name, operator, context, fields in groups:
        values = [value for field in fields for value in strings(raw.get(field))]
        sources = [{"kind": "entry", "id": source_id, "field": field}
                   for field in fields if raw.get(field)]
        add("entry:" + name, operator, context, values, sources)
    hard = raw.get("hard_guards") or {}
    if not isinstance(hard, dict):
        hard = {}
    for field, operator in (("requires_facets", "all"), ("exclude_facets", "none")):
        add("entry:hard_guards:" + field, operator, "facet",
            strings(hard.get(field)), [{"kind": "entry", "id": source_id,
                                      "field": "hard_guards." + field}])
    quality_sources = sorted(copy.deepcopy(quality_sources or []), key=lambda row: row["id"])
    quality_values = [value for row in quality_sources
                      for value in strings(row.get("requires_primary_any_tags"))]
    if quality_values:
        # Preserve the existing quality-layer union/any semantics separately
        # from the entry's own primary-any prerequisite.
        raw["quality_layer_requires_primary_any_tags"] = sorted(set(quality_values))
        add("quality:primary_any", "any", "primary", quality_values,
            [{"kind": "quality_guard", "id": row["id"],
              "field": "requires_primary_any_tags"} for row in quality_sources])
    material = {"contract_version": VERSION, "source_id": source_id,
                "raw_requirements": raw, "requirements": requirements,
                "quality_layer_sources": quality_sources,
                "evaluation": "final_scene_literal_evidence_and_declared_scope",
                "semantic_truth_owner": "composer_review"}
    material["canonical_sha256"] = digest(material)
    return {"context_requirements": raw, "context_prerequisites": material,
            "context_preflight": {"status": "unassessed", "evaluation": "final_scene"}}


def _contains(text: str, phrase: str) -> bool:
    return bool(phrase.strip()) and phrase in text


def audit_context(candidate: dict, review: dict, *, prompt_en: str, core: dict,
                  brief: dict, subject_category: str, allowed: set[str]) -> list[dict]:
    """Validate grounded declarations, not semantic truth or perceptual strength."""
    contract = candidate.get("context_prerequisites")
    if contract is None:
        # Legacy packs do not carry the derived source contract. Their explicit
        # conditions still require evidence when adopted; no source is invented.
        raw = candidate.get("context_requirements") or {}
        contract = compile_context(raw, str(candidate.get("source_candidate_id")
                                           or candidate.get("id") or ""))["context_prerequisites"]
    failures = []
    cid = candidate.get("id")

    def fail(reason, requirement_id=None, status="unsupported"):
        item = {"check": "adult_contextual_prerequisites", "candidate_id": cid,
                "status": status, "reason": reason}
        if requirement_id:
            item["requirement_id"] = requirement_id
        failures.append(item)

    source_id = str(candidate.get("source_candidate_id") or candidate.get("id") or "")
    if (not isinstance(contract, dict) or contract.get("contract_version") != VERSION
            or contract.get("source_id") != source_id
            or contract.get("canonical_sha256") != digest(
                {key: value for key, value in contract.items() if key != "canonical_sha256"})
            or contract.get("raw_requirements") != (candidate.get("context_requirements") or {})):
        fail("declared prerequisite contract must match its source-bound requirements")
        return failures
    raw = contract["raw_requirements"]
    quality = contract.get("quality_layer_sources", [])
    def valid_values(value, allow_empty=False):
        return (isinstance(value, str) and bool(value.strip())) or (
            isinstance(value, list) and (allow_empty or bool(value))
            and all(isinstance(item, str) and item.strip() for item in value))
    if (not isinstance(raw, dict) or not isinstance(quality, list)
            or any(not isinstance(row, dict) or not isinstance(row.get("id"), str)
                   or not row["id"].strip() or not valid_values(row.get("requires_primary_any_tags"))
                   for row in quality)
            or any(not valid_values(value)
                   for key, value in raw.items() if key != "hard_guards")
            or ("hard_guards" in raw and (
                not isinstance(raw["hard_guards"], dict)
                or set(raw["hard_guards"]) - {"requires_facets", "exclude_facets"}
                or any(not valid_values(value, allow_empty=True) for value in raw["hard_guards"].values())))):
        fail("source prerequisites and derived guard sources must keep their declared shape")
        return failures
    expected = compile_context(raw, source_id, quality)["context_prerequisites"]
    if contract != expected:
        fail("all declared entry and derived prerequisites must survive canonical compilation")
        return failures
    requirements = contract.get("requirements")
    if not isinstance(requirements, list):
        fail("declared prerequisites must be a list")
        return failures
    by_id = {row.get("id"): row for row in requirements if isinstance(row, dict)}
    if (len(by_id) != len(requirements) or any(
            not isinstance(key, str) or row.get("operator") not in {"any", "all", "none"}
            or not strings(row.get("values")) or strings(row.get("values")) != row.get("values")
            or not row.get("sources") for key, row in by_id.items())):
        fail("prerequisites require unique source-backed any/all/none conditions")
        return failures
    evidence = review.get("requirement_evidence", [])
    if not isinstance(evidence, list):
        fail("requirement_evidence must be a list")
        return failures
    present: dict[str, set[str]] = {}
    absent: dict[str, set[str]] = {}
    unresolved: dict[str, set[str]] = {}
    # These facts come from declared requester context and the already-audited
    # literal adult-subject brief, never from a candidate's own tags.
    adult_phrase = str(brief.get("adult_subject_phrase") or "")
    known = set()
    if subject_category == "human" and _contains(prompt_en, adult_phrase) and re.search(
            r"\badult\b", adult_phrase, flags=re.IGNORECASE):
        known = {"human", "adult", "subject:human", "subject:adult"}
    baseline = str(core.get("baseline_prompt_en") or "")
    lock = core.get("intent_lock") or {}
    seen = set()
    axis = (brief.get("axes") or {}).get(candidate.get("axis")) or {}
    axis_effects = {value for value in axis.get("affected_dimensions") or [] if isinstance(value, str)}
    for witness in evidence:
        if not isinstance(witness, dict):
            fail("each final-context witness must be an object")
            continue
        rid, fact = witness.get("requirement_id"), witness.get("fact")
        if not isinstance(rid, str) or not isinstance(fact, str):
            fail("witness requirement_id and fact must be declared strings")
            continue
        requirement = by_id.get(rid)
        state = witness.get("state")
        key = (rid, fact)
        if (not requirement or fact not in requirement["values"] or key in seen
                or not isinstance(state, str)
                or state not in {"present", "absent", "pending", "unsupported"}):
            fail("witness must name one unique declared condition and fact", rid)
            continue
        seen.add(key)
        if state in {"pending", "unsupported"}:
            unresolved.setdefault(rid, set()).add(state)
            continue
        phrase = witness.get("prompt_evidence")
        reason = witness.get("reason")
        origin = witness.get("origin")
        effects = witness.get("affected_dimensions")
        properties = witness.get("affected_properties", [])
        if (not isinstance(phrase, str) or not _contains(prompt_en, phrase)
                or (phrase.strip() == fact and ("_" in fact or ":" in fact))
                or not isinstance(reason, str) or not reason.strip()):
            fail("final context needs a literal witness and contextual explanation, not a serialized tag assertion", rid)
            continue
        if (not isinstance(effects, list) or any(not isinstance(value, str) for value in effects)
                or len(set(effects)) != len(effects)):
            fail("final-context witness must declare its actual affected dimensions", rid)
            continue
        if (not isinstance(properties, list) or any(
                not isinstance(row, dict) or set(row) != {"dimension", "target", "property"}
                or any(not isinstance(value, str) or not value.strip() for value in row.values())
                or row["dimension"] not in effects for row in properties)):
            fail("final-context property effects must declare a dimension, target and property", rid)
            continue
        if origin == "retained":
            if effects or properties or not _contains(baseline, phrase):
                fail("retained context must occur in both baseline and final prompt with no new effects", rid)
                continue
        elif origin == "authored":
            if (not effects or not set(effects) <= allowed
                    or not set(effects) <= axis_effects
                    or not property_effects_allowed(lock, effects, properties)):
                fail("authored final context must preserve requester scope and property locks and be covered by the axis brief", rid)
                continue
        else:
            fail("context origin must be retained or authored", rid)
            continue
        target = present if state == "present" else absent
        target.setdefault(rid, set()).add(fact)
    all_present = known | {value for values in present.values() for value in values}
    all_absent = {value for values in absent.values() for value in values}
    if all_present & all_absent:
        fail("final-context witnesses contradict each other")
    for rid, requirement in by_id.items():
        values = set(requirement["values"])
        operator = requirement["operator"]
        supported = present.get(rid, set()) | known
        if operator == "any":
            satisfied = bool(values & supported)
        elif operator == "all":
            satisfied = values <= supported
        else:
            satisfied = values <= absent.get(rid, set()) and not (values & all_present)
        if not satisfied:
            fail("adoption requires grounded final evidence for every declared prerequisite", rid,
                 "pending" if "pending" in unresolved.get(rid, set()) else "unsupported")
    return failures
