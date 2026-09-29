"""Post-core retrieval of possible expressions, never an aesthetic classifier.

Candidate labels/tags are not admission gates. The composer interprets a visual
idea in the current scene; search scores establish discoverability only.
"""
from __future__ import annotations

import math
from typing import Any

from bm25f_retrieval import build_bm25f_index, rank_bm25f, tokenize_bm25f_text

VERSION = "photo-contextual-appeal/v2"
SCOPE_VERSION = "photo-adult-appeal-dimension-scope/v4"
QUERY_CACHE = "_contextual_appeal_query_vectors"
AXES = ("sensual", "fetish")
DIMENSIONS = frozenset({
    "sexual_tone", "style", "appearance", "material", "action", "pose",
    "body_geometry", "expression", "lighting", "framing", "composition",
    "camera", "color", "atmosphere",
})
AXIS_DIMENSIONS = {axis: DIMENSIONS for axis in AXES}
EXPLICIT_OPEN_DIMENSIONS = frozenset({"role", "setting", "relationship", "timing"})
READINGS = frozenset({"relevant", "potential", "irrelevant", "conflicting", "uncertain"})


def allowed_dimensions(lock: dict) -> set[str]:
    """A broad definition never implicitly unlocks a role or situation."""
    return (DIMENSIONS | (EXPLICIT_OPEN_DIMENSIONS & set(lock.get("open_dimensions", [])))) - set(lock.get("locked_dimensions", []))


def queries(core: dict, definitions: dict, intensities: dict, retrieval_text) -> dict[str, dict[str, str]]:
    """Keep agent wardrobe choices out of the alternatives lane.

    The existing positive-query builder removes exclusions. Request anchors and
    definitions retain ownership; interpreted_intent/baseline remain only in the
    coherence lane so a corset draft does not become a corset search constraint.
    """
    request_core = {key: value for key, value in core.items() if key in {
        "contract_version", "request_binding", "source_request", "user_definitions",
        "user_exclusions",
    }}
    request_core["visual_priorities"] = [
        anchor.get("prompt_evidence", "")
        for anchor in (core.get("intent_lock") or {}).get("semantic_anchors", [])
    ]
    independent, _ = retrieval_text(request_core)
    baseline, _ = retrieval_text(core)
    # Select short, requester-owned relations, not a fixed category menu or
    # agent-authored wardrobe. Their effects still pass the same scope guards.
    anchors = (core.get("intent_lock") or {}).get("semantic_anchors", [])
    focuses = []
    for dimension in ("event", "relationship", "action", "setting", "role", "concept"):
        phrases = list(dict.fromkeys(str(row.get("prompt_evidence", "")).strip()
                                    for row in anchors if row.get("dimension") == dimension))
        text = "; ".join(phrase for phrase in phrases if phrase)
        if text and len(text.split()) <= 48 and text not in [item[1] for item in focuses]:
            positive, _ = retrieval_text({**request_core, "request_binding": {"active_spans": []},
                                          "source_request": "", "user_definitions": [],
                                          "visual_priorities": [text]})
            if positive.strip():
                focuses.append((dimension, positive))
        if len(focuses) == 2:
            break
    result = {}
    for axis in AXES:
        if intensities.get(axis, 0) <= 0:
            continue
        definition = definitions["controls"][axis]
        meaning = definition["definition"] + " " + definition["levels"][str(intensities[axis])]
        result[axis] = {"coherence": baseline + " " + meaning,
                        "alternatives": independent + " " + meaning}
        short_meaning = definition["definition"].split(";")[0].split(", including")[0]
        result[axis].update({"relation_" + dimension: text + " " + short_meaning
                             for dimension, text in focuses})
    return result


def expression_scope(slot: str) -> str:
    if slot in {"wardrobe_style", "costume_style", "fetish_styling"}:
        return "whole_direction"
    if slot in {"garment_detail", "surface_material", "wearable_accessory", "footwear"}:
        return "construction_or_material"
    return "portrayal_or_scene_relation"


def _cosine(left, right):
    if not left or len(left) != len(right):
        return 0.0
    scale = math.sqrt(sum(v * v for v in left) * sum(v * v for v in right))
    return sum(a * b for a, b in zip(left, right)) / scale if scale else 0.0


def rank_candidates(rows: list[dict], lane_queries: dict, *, policy: dict,
                    query_vectors: dict | None = None, index: dict | None = None,
                    limit: int = 12, scene_query: str = "") -> tuple[list[dict], dict]:
    """BM25F + available embedding ranks, with bounded soft diversity.

    Stable IDs break ties; source order, preset membership, aesthetic tags and
    intensity thresholds never do. Missing embedding coverage is explicit.
    """
    documents = {row["source_candidate_id"]: row["search_fields"] for row in rows}
    lexical_index = build_bm25f_index(documents, policy=policy)
    by_id = {row["source_candidate_id"]: row for row in rows}
    scores: dict[str, float] = {}
    evidence: dict[str, set[str]] = {}
    entries = (index or {}).get("entries") or {}
    lane_modes = {}
    semantic_coverage = {}
    for lane, query in lane_queries.items():
        # One scoring pass suffices: filtering these ranks by expression scope
        # is identical to scoring each subset against this same corpus index.
        lexical = rank_bm25f(lexical_index, {"global_context": query}, limit=max(1, len(rows)))
        vector = (query_vectors or {}).get(lane)
        semantic = []
        if vector:
            semantic = sorted(
                ((key, _cosine(vector, entries[key].get("vector", [])))
                 for key in by_id if key in entries and len(entries[key].get("vector", [])) == len(vector)),
                key=lambda item: (-item[1], item[0]),
            )
            semantic = [(key, score) for key, score in semantic if score > 0]
        lane_modes[lane] = "hybrid" if semantic else "keyword"
        semantic_coverage[lane] = len(semantic)
        # A long tail of zero-evidence candidates never pads the public pack.
        for source, ordered in (("keyword", [row["document_id"] for row in lexical]),
                                ("semantic", [key for key, _ in semantic])):
            for rank, key in enumerate(ordered[:max(limit * 8, 48)]):
                scores[key] = scores.get(key, 0.0) + 1.0 / (30 + rank)
                evidence.setdefault(key, set()).add(lane + ":" + source)
        # A full-frame query otherwise lets verbose camera/action entries bury
        # short garment and material descriptions before diversity can act.
        # Search each expressive scope with the same query, then softly fuse
        # supported hits; no group must be adopted or even returned.
        for scope in sorted({row["expression_scope"] for row in rows}):
            group_ids = {key for key, row in by_id.items() if row["expression_scope"] == scope}
            focused = [hit for hit in lexical if hit["document_id"] in group_ids][:limit]
            for rank, hit in enumerate(focused):
                key = hit["document_id"]
                scores[key] = scores.get(key, 0.0) + 0.6 / (30 + rank)
                evidence.setdefault(key, set()).add(lane + ":keyword_scope")
            if semantic:
                for rank, (key, _) in enumerate([hit for hit in semantic if hit[0] in group_ids][:limit]):
                    scores[key] = scores.get(key, 0.0) + 0.6 / (30 + rank)
                    evidence.setdefault(key, set()).add(lane + ":semantic_scope")
    tokens = {key: set(tokenize_bm25f_text(" ".join(row["visual_text"]))) for key, row in by_id.items()}
    scene_ranks = rank_bm25f(lexical_index, {"global_context": scene_query}, limit=max(1, len(rows))) if scene_query else []
    scene_support = {hit["document_id"]: 1.0 / (1 + rank) for rank, hit in enumerate(scene_ranks)}
    selected = []
    remaining = set(scores)
    maximum = max(scores.values(), default=1.0)
    while remaining and len(selected) < limit:
        def utility(key):
            similarity = max((len(tokens[key] & tokens[other]) / max(1, len(tokens[key] | tokens[other]))
                              for other in selected), default=0.0)
            same_scope = sum(by_id[other]["expression_scope"] == by_id[key]["expression_scope"] for other in selected)
            return scores[key] / maximum + 0.12 * scene_support.get(key, 0.0) - 0.35 * similarity - 0.06 * same_scope
        key = min(remaining, key=lambda key: (-utility(key), key))
        remaining.remove(key)
        selected.append(key)
    result = []
    for key in selected:
        row = dict(by_id[key])
        row.pop("search_fields", None)
        row.pop("visual_text", None)
        row["retrieval_evidence"] = sorted(evidence[key])
        row["contextual_status"] = "unassessed"
        row["scene_retrieval_support"] = key in scene_support
        result.append(row)
    return result, {
        "lanes": lane_modes, "semantic_candidate_coverage": semantic_coverage,
        "eligible_corpus_count": len(rows), "retrieved_count": len(scores),
        "returned_count": len(result), "ranking": "reciprocal_rank_fusion_with_soft_visual_diversity",
        "classification": "not_performed", "membership_tags_required": False,
        "intensity_admission_thresholds": False,
        "scene_reranking": "bounded_request_overlap_preference;_not_applicability_proof",
    }


def review_ids(rows: list[dict], limit: int = 4) -> list[str]:
    """Expose expression alternatives independently of the general sampler."""
    selected = []
    scopes = set()
    for row in rows:
        scope = row["expression_scope"]
        if scope not in scopes:
            selected.append(row["id"])
            scopes.add(scope)
    for row in rows:
        if len(selected) >= limit:
            break
        if row["id"] not in selected:
            selected.append(row["id"])
    return selected[:limit]


def audit_review(contract: dict, brief: dict, chosen: set[str]) -> list[dict[str, Any]]:
    """Check recorded consideration, not whether an interpretation is true."""
    retrieval = contract.get("contextual_retrieval") or {}
    if retrieval.get("contract_version") != VERSION:
        return []  # Historical packs have no contextual-review contract.
    required = set(retrieval.get("review_candidate_ids") or [])
    inventory = {row["id"]: row for axis in contract["axes"].values() for row in axis["candidate_inventory"]}
    required |= chosen & inventory.keys()
    if not required:
        return []
    failures = []
    records = brief.get("contextual_review") or []
    if not isinstance(records, list):
        records = []
    seen = set()
    for row in records:
        if not isinstance(row, dict):
            failures.append({"check": "adult_contextual_review", "reason": "review rows must be objects"})
            continue
        candidate_id = row.get("candidate_id")
        reading = row.get("reading")
        if not isinstance(candidate_id, str):
            failures.append({"check": "adult_contextual_review", "reason": "candidate_id must be a supplied string ID"})
            continue
        if (candidate_id not in inventory or candidate_id in seen or not isinstance(reading, str) or reading not in READINGS
                or not isinstance(row.get("reason"), str) or not row["reason"].strip()):
            failures.append({"check": "adult_contextual_review", "reason": "review needs a unique supplied candidate, contextual reading and reason"})
            continue
        if reading == "potential" and (not isinstance(row.get("proposed_application"), str) or not row["proposed_application"].strip()):
            failures.append({"check": "adult_contextual_review", "reason": "potential relevance needs a concrete application within open properties"})
        if candidate_id in chosen and reading not in {"relevant", "potential"}:
            failures.append({"check": "adult_contextual_review", "reason": "uncertain, irrelevant or conflicting candidates cannot be adopted"})
        seen.add(candidate_id)
    if required - seen:
        failures.append({"check": "adult_contextual_review", "reason": "expression shortlist and adopted candidates must be considered", "missing_candidate_ids": sorted(required - seen)})
    if not isinstance(brief.get("contextual_comparison"), str) or not brief["contextual_comparison"].strip():
        failures.append({"check": "adult_contextual_comparison", "reason": "record the baseline-versus-alternatives judgment at the same requested strengths"})
    return failures
