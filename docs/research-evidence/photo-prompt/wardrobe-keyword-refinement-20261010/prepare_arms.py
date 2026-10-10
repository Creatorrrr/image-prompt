"""Coordinator-only extraction of verified, closed retry inputs for arms A/C."""
import hashlib
import json
from pathlib import Path
import sys
import argparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path[:0] = [str(SKILL / "scripts"), str(SKILL / "precore")]
import photo_authoring_wire as wire
import photo_authoring_contracts as contracts
from photo_run_files import load_state
from prepare_retry_context import parent_inputs, prepare


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


request = (HERE / "request.txt").read_text()
phrase = "첨부 사진으로 다시 이미지 생성·검증해서 전체 필수 조건을 통과하는지 확인해줘."
old = HERE.parent / "wardrobe-keyword-integration-20261010"
parents = {"a": (old / "arms/a/requalification_run", old / "arms/a/image_runs.ndjson"),
           "c": (old / "arms/c/requalification/run", old / "arms/c/requalification/image_runs.ndjson")}
for arm in ["a", "b", "c"]:
    directory = HERE / "arms" / arm
    directory.mkdir(parents=True, exist_ok=True)
    spans = [{"span_id": "reference_and_complete_validation", "start": request.index(phrase),
              "end": request.index(phrase) + len(phrase), "text": phrase}]
    if arm == "b":
        correction = "차단된 사례는 다른 컨셉으로 바꾸고"
        spans.insert(0, {"span_id": "new_concept", "start": request.index(correction),
                         "end": request.index(correction) + len(correction), "text": correction})
    envelope = {"contract_version": "photo-request-envelope/v1", "provenance": "requesting_user",
                "request_id": "wardrobe-refinement-20261010-" + arm, "request_text": request,
                "request_sha256": hashlib.sha256(request.encode()).hexdigest(), "active_spans": spans}
    wire.normalize_request_envelope(envelope)
    write(directory / "request_envelope.json", envelope)
    if arm not in parents:
        continue
    run, ledger = parents[arm]
    rows = [json.loads(line) for line in ledger.read_text().splitlines() if line.strip()]
    assert len(rows) == 1
    attempt = directory / "parent_attempt.json"
    write(attempt, rows[0])
    parent = parent_inputs(load_state(run), attempt, ledger)
    mappings = {}
    for row in parent["audit"]["effective_visual"]["obligations"]:
        if "wk047" in row["id"]:
            mappings[row["id"]] = ["appearance", "material"]
        elif "face_hands_place" in row["id"]:
            # Preserve the focal legibility relation, not its unprescribed crop.
            mappings[row["id"]] = ["concept"]
        else:
            mappings[row["id"]] = ["appearance"]
    changed = ["pose", "body_geometry", "framing", "composition", "lighting", "camera"]
    preserved = sorted(set(contracts.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS) - set(changed))
    local = sorted(set(contracts.RENDER_REPAIR_ALLOWED_AXES) &
                   {"pose", "body_geometry", "framing", "composition", "lighting", "camera", "contact_geometry", "visibility"})
    decision = {"schema_version": "photo-repair-decision/v1", "current_source_span_ids": [spans[0]["span_id"]],
                "source_text": phrase, "preserved_dimensions": preserved, "allowed_changes": changed,
                "requester_corrected_dimensions": [], "allowed_properties": [], "local_axes": local,
                "failed_gate_ids": parent["failed_gate_ids"], "failure_class": "pixel_realization_mismatch",
                "additional_invocation_limit": 2, "obligation_dimensions": mappings}
    decision_path = directory / "repair_decision.json"
    write(decision_path, decision)
    result = prepare(argparse.Namespace(run=run, decision=decision_path, current_envelope=directory / "request_envelope.json",
                                        attempt=attempt, ledger=ledger, output=directory / "retry_input", parent_manifest=None))
    print(json.dumps({"arm": arm, "result": result}, ensure_ascii=False))
