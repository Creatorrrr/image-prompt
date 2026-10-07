"""Pinned, audited text-only API inputs and independently verifiable records."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

import audit_composed_prompt as composed_audit
import audit_image_render_request as runtime_audit
from photo_runtime_sources import RuntimeSnapshotProvider

VERSION = "photo-api-render-preflight/v1"


def text_digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


class PreflightError(ValueError):
    def __init__(self, stage: str, detail):
        self.stage, self.detail = stage, detail
        super().__init__(f"{stage}: {json.dumps(detail, ensure_ascii=False)}")


@dataclass(frozen=True)
class PreparedRenderInput:
    # Only immutable bytes are retained; property reads return independent objects.
    document_bytes: bytes

    @property
    def document(self):
        return json.loads(self.document_bytes)


def audit_inputs(inputs: dict, *, model: str, size: str, runtime_store=None) -> dict:
    pack, receipt, composed, request = (inputs[key]["value"] for key in ("pack", "receipt", "composed", "request"))
    try:
        snapshot = RuntimeSnapshotProvider(store=Path(runtime_store) if runtime_store else None).from_receipt(pack, receipt)
    except (ValueError, OSError, KeyError, TypeError) as error:
        raise PreflightError("runtime_receipt", str(error)) from error
    first = composed_audit.audit_composed_prompt(pack, composed, source_data=snapshot.data)
    if first["status"] != "pass" or first["failures"]:
        raise PreflightError("composed_audit", first)
    second = runtime_audit.audit_image_render_request(pack, composed, request, request_path=Path(inputs["request"]["path"]))
    if second["status"] != "pass" or second["failures"]:
        raise PreflightError("runtime_audit", second)
    reference_mode = (((pack.get("creative_controls") or {}).get("controls") or {}).get("reference_edit_mode") or {}).get("value", "off")
    if request["references"] or reference_mode != "off":
        raise PreflightError("unsupported_reference_transport", {"references": len(request["references"]), "reference_edit_mode": reference_mode})
    unsupported = [key for key in ("referenced_image_paths", "num_last_images_to_include", "transparent_background")
                   if request.get(key) not in (None, False, [], 0)]
    if unsupported:
        raise PreflightError("unsupported_transport_parameters", unsupported)
    prompt, negative = composed["prompt_en"], composed.get("negative_en")
    expected = prompt + ("\n\nAvoid: " + negative if negative is not None else "")
    if request["runtime_prompt_en"] != expected:
        raise PreflightError("unsupported_runtime_addition", "text-only API accepts the exact composed prompt and optional Avoid suffix")
    if not isinstance(model, str) or not model.strip() or not isinstance(size, str) or not size.strip():
        raise PreflightError("execution_parameters", "model and size must be nonempty strings")
    core = pack["authorial_core"]
    execution = {"model": model, "size": size, "n": 1, "prompt_en": prompt, "negative_en": negative,
                 "runtime_prompt_en": request["runtime_prompt_en"], "runtime_prompt_sha256": text_digest(request["runtime_prompt_en"]),
                 "pack_id": pack["pack_id"], "chosen_candidate_ids": composed.get("chosen_candidate_ids", []),
                 "chosen_visual_concept_ids": composed.get("chosen_visual_concept_ids", []),
                 "composer": composed.get("composer", "agent"), "audit_status": first["status"],
                 "authorial_core_sha256": core["canonical_sha256"],
                 "intent_lock_sha256": core["intent_lock"]["canonical_sha256"],
                 "render_repair_contract_sha256": first.get("render_repair_contract_sha256"),
                 "effective_visual_contract_sha256": first.get("effective_visual_contract_sha256"),
                 "augmentation_brief": composed.get("augmentation_brief")}
    return {"generation_id": snapshot.generation_id, "source_fingerprint": snapshot.manifest["source_fingerprint"],
            "audit_results": {"composed": first, "runtime": second}, "transport": "text_only", "execution": execution}


def prepare_api_render(pack_path: Path, receipt_path: Path, composed_path: Path, request_path: Path,
                       *, model: str, size: str, runtime_store=None) -> PreparedRenderInput:
    inputs = {}
    for label, path in zip(("pack", "receipt", "composed", "request"), (pack_path, receipt_path, composed_path, request_path)):
        try:
            path = Path(path).resolve()
            raw = path.read_bytes().decode("utf-8")
            value = runtime_audit.one_object(json.loads(raw), label)
        except (ValueError, OSError, TypeError) as error:
            raise PreflightError("input", {"label": label, "error": str(error)}) from error
        inputs[label] = {"path": str(path), "raw_utf8": raw, "sha256": text_digest(raw), "value": value}
    binding = audit_inputs(inputs, model=model, size=size, runtime_store=runtime_store)
    return PreparedRenderInput(json_bytes({"schema_version": VERSION, "status": "pass", "inputs": inputs,
        "runtime_store": str(Path(runtime_store).resolve()) if runtime_store else None, **binding}))


def save_preflight(path: Path, prepared: PreparedRenderInput) -> str:
    # Refuse replacements; this record is the input to every actual attempt.
    with path.open("xb") as handle:
        handle.write(prepared.document_bytes)
    return hashlib.sha256(prepared.document_bytes).hexdigest()


def validate_api_render_input(path: Path, expected_sha256: str, entry: dict) -> dict:
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise ValueError("API preflight file hash mismatch")
    document = json.loads(raw)
    if document.get("schema_version") != VERSION or document.get("status") != "pass":
        raise ValueError("unsupported API preflight version")
    original_inputs = {}
    for label in ("pack", "receipt", "composed", "request"):
        row = document["inputs"][label]
        original = runtime_audit.one_object(json.loads(row["raw_utf8"]), label)
        if text_digest(row["raw_utf8"]) != row["sha256"] or original != row["value"]:
            raise ValueError(f"API preflight {label} bytes/binding mismatch")
        # The saved original bytes are authoritative. JSON previews may sort
        # mapping keys; frozen controls also retain an ordered authoring brief.
        original_inputs[label] = {**row, "value": original}
    execution = document["execution"]
    fresh = audit_inputs(original_inputs, model=execution["model"], size=execution["size"], runtime_store=document["runtime_store"])
    if any(document.get(key) != value for key, value in fresh.items()):
        raise ValueError("API preflight differs from independently recomputed audit/input")
    expected = {"prompt_en": execution["prompt_en"], "negative_en": execution["negative_en"], "pack_id": execution["pack_id"],
        "chosen_candidate_ids": execution["chosen_candidate_ids"], "chosen_visual_concept_ids": execution["chosen_visual_concept_ids"],
        "composer": execution["composer"], "audit_status": "pass", "runtime_prompt_sha256": execution["runtime_prompt_sha256"],
        "requested_image_model": execution["model"], "image_size": execution["size"],
        "authorial_core_sha256": execution["authorial_core_sha256"], "intent_lock_sha256": execution["intent_lock_sha256"]}
    for key in ("render_repair_contract_sha256", "augmentation_brief"):
        if execution.get(key) is not None:
            expected[key] = execution[key]
    if execution["chosen_visual_concept_ids"]:
        expected["effective_visual_contract_sha256"] = execution["effective_visual_contract_sha256"]
    for key, value in expected.items():
        if entry.get(key) != value:
            raise ValueError(f"API attempt/preflight mismatch: {key}")
    # The existing error recorder recomputes runtime text; bind it as well.
    if entry.get("runtime_prompt_en", execution["runtime_prompt_en"]) != execution["runtime_prompt_en"]:
        raise ValueError("API attempt runtime prompt mismatch")
    return {"api_render_input_json": str(Path(path).resolve()), "api_render_input_sha256": expected_sha256}
