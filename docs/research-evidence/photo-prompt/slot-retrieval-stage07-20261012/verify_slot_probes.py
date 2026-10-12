#!/usr/bin/env python3
"""Exercise actual retrieve_core_slots with the complete verified live corpus.

These source-derived maintenance probes test retrieval only. They are not
independently authored photo requests and do not claim upstream authoring review.
No guard, cap, source data, or production function is mocked or overridden.
"""
from __future__ import annotations

import collections
import copy
import hashlib
import json
import sys
import time
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = Path('/Users/chasoik/.codex/worktrees/slot-retrieval-stage07-integration/image-prompt')
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as g
from photo_runtime_sources import RuntimeSnapshotProvider


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def probe_input(data, slot, entry):
    text = str(entry.get("en") or entry.get("ko"))
    category = "human"
    if slot == "subject":
        inferred = g.subject_category({"subject": entry}, data)
        if inferred != "generic":
            category = inferred
    elif entry.get("for_any") and "human" not in entry["for_any"]:
        category = next((value for value in entry["for_any"] if value in g.VALID_SUBJECT_CATEGORIES), "human")
    subjects = {"human": "one adult human portrait subject", "animal": "one animal",
                "object": "one inanimate object", "food": "one food item",
                "plant": "one botanical plant", "environment": "one landscape environment", "sign": "one printed sign"}
    subject = subjects.get(category, subjects["human"])
    requirements = list(dict.fromkeys(value for key in ("requires_all", "requires_all_tags", "requires_any", "requires_any_tags", "requires_primary_any_tags")
                                     for value in g.normalize_list(entry.get(key))))
    # Context is an explicit synthetic input, never a candidate-established prerequisite.
    context_text = ", ".join(requirements)
    if context_text:
        subject += "; maintenance context " + context_text
    policy = g.slot_applicability_policy(data, slot)
    scoped_domains = sorted({domain for tag, domain in g.INTENT_SCOPED_ENTRY_DOMAIN_TAGS.items()
                             if tag in (g.entry_tags(entry) | g.entry_kinds(entry))})
    domain = next(iter(scoped_domains or g.normalize_list(policy.get("allow_domains"))), "general_photo")
    setting = "a photographic studio with natural window light"
    event = "the subject remains visible in a calm photographic scene"
    priorities = ["clear subject presence", "tactile surface detail"]
    style = {"domain": domain, "family": "literal maintenance retrieval probe", "evidence": []}
    if slot in g.SLOT_FOCUS_SUBJECT_SLOTS:
        subject = text if slot == "subject" else subject + "; " + text
    elif slot in g.SLOT_FOCUS_SETTING_SLOTS:
        setting += "; " + text
    elif slot in g.SLOT_FOCUS_EVENT_SLOTS:
        event += "; " + text
    elif slot in g.SLOT_FOCUS_AFFECT_SLOTS | g.SLOT_FOCUS_LIGHT_SLOTS:
        priorities.append(text)
    else:
        style["evidence"].append(text)
        priorities.append(text)
    # Every fallback DIMENSION_FIELDS projection sees the exact target where appropriate.
    ownership = g.photo_candidate_semantics.slot_dimensions(slot, data.get("candidate_semantic_policy")) or list(dict.fromkeys(
        dim for value in data["slots"][slot] for dim in value.get("affected_dimensions") or []))
    if slot not in (g.SLOT_FOCUS_SUBJECT_SLOTS | g.SLOT_FOCUS_SETTING_SLOTS | g.SLOT_FOCUS_EVENT_SLOTS |
                    g.SLOT_FOCUS_AFFECT_SLOTS | g.SLOT_FOCUS_LIGHT_SLOTS | g.SLOT_FOCUS_STYLE_SLOTS):
        for field in dict.fromkeys(field for dim in ownership for field in g.DIMENSION_FIELDS.get(dim, [])):
            if field == "subject":
                subject += "; " + text
            elif field == "event":
                event += "; " + text
            elif field == "setting":
                setting += "; " + text
    camera_clause = "The capture camera records " + text + "." if slot in {"camera_direction", "camera_height"} else ""
    baseline = g.clean_spaces(f"{subject}. {setting}. {event}. {'; '.join(priorities)}. {camera_clause} This is a source-derived maintenance retrieval input.")
    source_request = f"Maintenance-only retrieval probe for {slot}: {text}. Explicit test context: {context_text or 'none'}."
    controls = g.creative_controls.resolve(source_request,
        context={"subject_category": "human" if category == "human" else "nonhuman", "no_people": False, "explicit_nonsexual": False},
        overrides={"sensual": 1, "fetish": 1, "surreal": 1, "creativity": 1}, seed=7)
    core = {"contract_version": "photo-authorial-core/v3", "provenance": "agent_prepack",
            "source_request": source_request, "creative_controls_sha256": controls["canonical_sha256"],
            "request_binding": {"active_spans": [{"span_id": "probe", "text": source_request}]},
            "interpreted_intent": "Source-derived maintenance probe; does not establish independent artistic authoring.",
            "subject": subject, "setting": setting, "event": event, "visual_priorities": priorities,
            "baseline_prompt_en": baseline, "user_definitions": [], "interpretation_provenance": [],
            "unresolved_ambiguities": [], "user_exclusions": [], "runtime_forbidden_labels": [],
            "intent_lock": {"contract_version": "photo-intent-lock/v2", "priority": "requesting_user",
                            "locked_dimensions": ["concept", "subject", "event"],
                            "open_dimensions": sorted(g.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS - {"concept", "subject", "event"}),
                            "semantic_anchors": []},
            "semantic_assertions": [{"assertion_id": "probe_subject", "dimension": "subject", "polarity": "required",
                "source_span_ids": ["probe"], "affected_dimensions": ["subject"], "axes": {"subject_category": category},
                "evidence": {"subject_phrase": subject}}], "style": style, "request_lineage": None}
    core["canonical_sha256"] = g.canonical_json_sha256(core)
    return core, controls, {"primary_category": category, "explicit_test_context": requirements, "domain": domain}


def diagnose_eligibility(data, core, contract, picked, slot, entry):
    reason = g.slot_block_reason(data, slot, contract)
    if reason:
        return "slot:" + reason
    reason = g.entry_block_reason(entry, slot, contract)
    if reason and not (reason == "adult_not_allowed" and g.candidate_pack_age_only_subject_match(entry, slot, core)):
        return "entry:" + reason
    subject_tokens = g.entry_tags(picked["subject"]) | g.entry_kinds(picked["subject"])
    if entry.get("for_any") and not set(entry["for_any"]) & subject_tokens:
        return "for_any_not_satisfied"
    if set(entry.get("exclude_for_any") or []) & subject_tokens:
        return "exclude_for_any_matched"
    domains = {domain for tag, domain in g.INTENT_SCOPED_ENTRY_DOMAIN_TAGS.items() if tag in g.entry_tags(entry) | g.entry_kinds(entry)}
    if domains and not domains & set(contract["intent_constraints"].get("domains") or []):
        return "entry_domain_not_satisfied"
    others = {key: value for key, value in picked.items() if key != slot}
    if not g.compatible_with_facet_guards(entry, others):
        return "facet_guard_not_satisfied"
    if not g.compatible_with_slot_context(slot, entry, others, data):
        return "declared_or_primary_context_not_satisfied"
    return "eligible" if g.core_slot_entry_eligible(data, core, contract, picked, slot, entry) else "other_eligibility_guard"


def run_probe(data, slot, entry, ordinal, core_overrides=None):
    start = time.monotonic()
    core, controls, metadata = probe_input(data, slot, entry)
    if core_overrides:
        core.update(copy.deepcopy(core_overrides))
        metadata["supplementary_core_override"] = True
        core["canonical_sha256"] = g.canonical_json_sha256({key: value for key, value in core.items() if key != "canonical_sha256"})
    before = g.canonical_json_sha256(core)
    slots, binding, contract = g.retrieve_core_slots(data, core, controls)
    _, picked = g.frozen_core_context(data, core, controls)
    queries, fields = g.core_slot_focus_queries(data, core, slot)
    is_eligible = g.core_slot_entry_eligible(data, core, contract, picked, slot, entry)
    exposed = [row["entry_id"] for row in slots.get(slot, {}).get("candidates", [])]
    result = {"slot": slot, "entry_id": entry["id"], "ordinal": ordinal, "metadata": metadata,
              "eligible": is_eligible, "eligibility_reason": diagnose_eligibility(data, core, contract, picked, slot, entry),
              "focus_queries": queries, "focus_fields": fields, "target_exposed": entry["id"] in exposed,
              "slot_exposed": slot in slots, "exposed_ids": exposed,
              "active_slot_count": len(slots), "total_exposed_candidates": sum(len(row["candidates"]) for row in slots.values()),
              "source_core_unchanged": before == g.canonical_json_sha256(core), "binding": binding,
              "elapsed_seconds": round(time.monotonic() - start, 3)}
    if not result["target_exposed"]:
        if not queries:
            result["nonexposure_reason"] = "missing_slot_ownership_or_focus"
        elif not is_eligible:
            result["nonexposure_reason"] = result["eligibility_reason"]
        else:
            allowed = [f"slot:{slot}:{value['id']}" for value in data["slots"][slot]
                       if g.core_slot_entry_eligible(data, core, contract, picked, slot, value)]
            corpus_json = json.dumps(data["slots"], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            index = data.slot_index(corpus_json)
            expected = f"slot:{slot}:{entry['id']}"
            broad = g.rank_bm25f(index, {"global_context": g.authorial_core_retrieval_text(core)[0]}, allowed_ids=allowed, limit=len(allowed))
            focal = [g.rank_bm25f(index, {"slot_focus": query}, allowed_ids=allowed, limit=len(allowed)) for query in queries]
            result["broad_rank"] = next((i + 1 for i, row in enumerate(broad) if row["document_id"] == expected), None)
            result["focus_ranks"] = [next((i + 1 for i, row in enumerate(rows) if row["document_id"] == expected), None) for rows in focal]
            result["nonexposure_reason"] = "ranking_fusion_or_shared_cap" if result["broad_rank"] and any(result["focus_ranks"]) else "lexical_support_not_retrieved"
    directory = OUT / "slot-probes" / slot
    directory.mkdir(parents=True, exist_ok=True)
    save(directory / f"{ordinal:02d}-{entry['id']}.json", {"test_input_kind": "source_derived_lower_level_maintenance_probe",
         "core": core, "controls": controls, "result": result, "retrieved_slots": slots})
    return result


def main():
    acquired = json.loads((OUT / "runtime-acquisition.json").read_text())
    provider = RuntimeSnapshotProvider(SKILL, OUT / "runtime-store")
    data = provider.load_generation(acquired["generation_id"]).data
    results, summaries = [], []
    with (OUT / "slot-probes.ndjson").open("w") as stream:
        for slot, entries in sorted(data["slots"].items()):
            # First and last include baseline and recently appended source data.
            positions = list(dict.fromkeys((0, len(entries) - 1)))
            slot_results = []
            for ordinal, position in enumerate(positions, 1):
                result = run_probe(data, slot, entries[position], ordinal)
                slot_results.append(result)
                results.append(result)
                stream.write(json.dumps(result, ensure_ascii=False) + "\n")
                stream.flush()
            summary = {"slot": slot, "source_count": len(entries), "probes": len(slot_results),
                       "eligible_probes": sum(row["eligible"] for row in slot_results),
                       "target_hits": sum(row["target_exposed"] for row in slot_results),
                       "slot_hits": sum(row["slot_exposed"] for row in slot_results),
                       "nonexposure_reasons": dict(collections.Counter(row.get("nonexposure_reason") for row in slot_results if not row["target_exposed"]))}
            summaries.append(summary)
            save(OUT / "slot-probe-summary.json", {"completed_slots": len(summaries), "slots": summaries,
                 "probe_count": len(results), "target_hits": sum(row["target_exposed"] for row in results),
                 "slots_with_target_hit": sum(row["target_hits"] > 0 for row in summaries)})
            print(f"Probe {slot}: {summary['target_hits']}/{summary['probes']} target hits; {summary['nonexposure_reasons']}", flush=True)


if __name__ == "__main__":
    main()
