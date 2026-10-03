"""Read-only, source-hashed owner-clause evaluation with production quality layers.

Raw prose extraction, query forwarding, and candidate eligibility are separate
measurements. English prompt-budget padding is candidate-free and never part of
the raw held-out extraction. The supplied authored text and expectations remain
unchanged. This measures text contracts, not pixel quality.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from unittest import mock


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-repo", type=Path, required=True)
    parser.add_argument("--data-repo", type=Path, required=True)
    parser.add_argument("--test-repo", type=Path, required=True)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    scripts = args.runtime_repo / "skills/photo-prompt-image-generator/scripts"
    sys.path.insert(0, str(scripts))
    import prompt_generator as pg
    sys.path.insert(1, str(args.test_repo))
    from tests import photo_prompt_fixtures as fixtures
    camera = getattr(pg, "photo_camera_evidence", None)
    raw = args.fixture.read_bytes()
    inputs = json.loads(raw)
    report = {"runtime_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=args.runtime_repo, text=True).strip(),
              "runtime_sources": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in scripts.glob("*.py")},
              "fixture_sha256": hashlib.sha256(raw).hexdigest(), "authorship": inputs.get("authorship"),
              "provider_calls": 0, "pixel_quality_evaluated": False, "rows": []}
    with mock.patch.object(pg, "cached_gemini_client", side_effect=AssertionError("offline owner evaluation")), \
         mock.patch.object(pg, "embed_texts_with_gemini", side_effect=AssertionError("offline owner evaluation")):
        data = pg.load_runtime_data(args.data_repo / "skills/photo-prompt-image-generator/assets/photo_prompt_tags.json")
        report["quality_layers_loaded"] = pg.QUALITY_LAYERS_DATA_KEY in data
        report["dictionary_hash"] = pg.dictionary_hash(data)
        report["semantic_entries"] = len(data[pg.SEMANTIC_INDEX_DATA_KEY]["entries"])
        report["visual_profiles"] = len(data[pg.VISUAL_OBLIGATIONS_DATA_KEY]["profiles"])
        for case in inputs["cases"]:
            text = case.get("text") or case["baseline_prompt_en"]
            request = case.get("request") or text
            authored = fixtures.core(request, interpreted_intent=text, subject=case["subject"],
                event=text.split(".")[0], visual_priorities=("readable subject structure", "natural material detail"),
                baseline_prompt_en=text)
            controls = pg.creative_controls.resolve(request, overrides={"sensual": 0, "fetish": 0}, seed=47)
            authored["creative_controls_sha256"] = controls["canonical_sha256"]
            normalization_error = None
            try:
                core = pg.normalize_authorial_core(authored,
                    request_envelope=pg.normalize_request_envelope(fixtures.envelope(request)),
                    creative_control_snapshot=controls)
                slots, binding, _ = pg.retrieve_core_slots(data, core, controls)
            except ValueError as exc:
                # Raw KO prose is still an extractor test, but does not stand
                # in for the independently authored English baseline contract.
                normalization_error = str(exc)
                core, slots, binding = authored, {}, {"candidate_adoption": "optional"}
            axes = {}
            for axis in ("direction", "height"):
                extracted = camera.legacy_camera_clauses({"subject": case["subject"], "baseline_prompt_en": text}, axis) if camera else []
                query, fields = pg.core_slot_focus_queries(data, core, "camera_" + axis)
                returned = slots.get("camera_" + axis, {}).get("candidates", [])
                expected = case[axis]
                axes[axis] = {"expected_owned_spans": expected, "extracted_owned_clauses": extracted,
                    "exact_span_match": [s.casefold() for s in extracted] == [s.casefold() for s in expected],
                    "affirmative_owner_found": bool(extracted), "query": query, "query_fields": fields,
                    "legacy_clause_forwarded": "baseline_prompt_en.camera_clause" in fields,
                    "retrieved_ids": [c["id"] for c in returned] if normalization_error is None else None}
            property_lock = {"contract_version": "photo-intent-lock/v2", "semantic_anchors": [
                {"dimension": "camera", "target": "camera", "property": "viewpoint." + axis}
                for axis in ("direction", "height") if case[axis]]}
            camera_rows = data["slots"]["camera_direction"]
            scope = []
            for entry in camera_rows:
                source = pg.photo_candidate_semantics.semantic_source(entry, "camera_direction", data.get("candidate_semantic_policy"))
                scope.append(pg.property_effects_allowed(property_lock, source.get("affected_dimensions") or [], source.get("affected_properties", [])))
            report["rows"].append({"id": case["id"], "raw_text_sha256": hashlib.sha256(text.encode()).hexdigest(),
                "core_sha256": core.get("canonical_sha256"), "axes": axes,
                "production_probe_error": normalization_error,
                "actual_core_property_locks": pg.intent_property_locks(core["intent_lock"]),
                "counterfactual_declared_property_lock_compatible_direction_rows": sum(scope),
                "total_direction_rows": len(camera_rows), "candidate_adoption": binding["candidate_adoption"]})
    positives = [r for r in report["rows"] if any(a["expected_owned_spans"] for a in r["axes"].values())]
    negatives = [r for r in report["rows"] if not any(a["expected_owned_spans"] for a in r["axes"].values())]
    report["summary"] = {"positive_cases": len(positives),
        "positive_cases_owner_found": sum(all(a["affirmative_owner_found"] for a in r["axes"].values() if a["expected_owned_spans"]) for r in positives),
        "positive_cases_exact_spans": sum(all(a["exact_span_match"] for a in r["axes"].values()) for r in positives),
        "negative_cases": len(negatives), "negative_cases_abstained": sum(not any(a["extracted_owned_clauses"] for a in r["axes"].values()) for r in negatives)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report["summary"]), flush=True)


if __name__ == "__main__":
    main()
