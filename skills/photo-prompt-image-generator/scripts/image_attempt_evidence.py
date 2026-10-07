"""Error evidence shared by the API adapter and the external-attempt recorder."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import sys
import urllib.error
from pathlib import Path

CONTRACT_VERSION = "photo-image-attempt-evidence/v1"
BLOCK_CODES = {"moderation_blocked", "content_policy_violation"}
CAPTURE_FIDELITIES = {"exact_string", "exact_bytes", "typed_capture", "limited_capture", "unavailable"}


def _message(error: BaseException) -> str:
    try:
        return str(error)
    except Exception:
        return f"<{type(error).__name__}: message conversion failed>"


def error_details(text: str, *, http_status=None, request_id=None) -> dict:
    """Only explicit provider codes classify a safety block; raw text stays separate."""
    value = None
    try:
        candidate = text
        wrapped = re.search(r"Some\((.*)\)\s*$", text, re.DOTALL)
        if wrapped:
            candidate = wrapped.group(1)
        value = json.loads(candidate)
        for _ in range(2):
            if isinstance(value, str):
                value = json.loads(value)
        if isinstance(value, dict) and isinstance(value.get("error"), dict):
            value = value["error"]
    except (ValueError, TypeError):
        value = None
    provider = value if isinstance(value, dict) else {}
    moderation = provider.get("moderation_details")
    moderation = moderation if isinstance(moderation, dict) else {}
    code = provider.get("code") if isinstance(provider.get("code"), str) else None
    body_id = provider.get("request_id")
    body_id = body_id if isinstance(body_id, str) and body_id else None
    message_id = re.search(r"request ID ([A-Za-z0-9_-]+)", str(provider.get("message") or ""))
    if request_id:
        id_source = "response_header"
    elif body_id:
        request_id, id_source = body_id, "error.request_id"
    elif message_id:
        request_id, id_source = message_id.group(1), "error.message"
    else:
        id_source = None
    categories = moderation.get("categories")
    categories = categories if isinstance(categories, list) and all(isinstance(x, str) for x in categories) else []
    return {
        "http_status": http_status,
        "error_code": code,
        "error_type": provider.get("type") if isinstance(provider.get("type"), str) else None,
        "request_id": request_id,
        "request_id_source": id_source,
        "moderation_stage": moderation.get("moderation_stage") if isinstance(moderation.get("moderation_stage"), str) else None,
        "categories": categories,
        "classification_source": "structured_error_code" if code in BLOCK_CODES else "unclassified",
    }


def capture_api_error(error: Exception, context: dict) -> dict:
    message = _message(error)
    raw = {"kind": "python_exception", "fidelity": "limited_capture", "value": {"type": type(error).__name__, "message": message}, "limitations": ["exception_attributes_not_captured"]}
    http_status, request_id, text = None, None, ""
    if isinstance(error, urllib.error.HTTPError):
        http_status = error.code
        if error.headers is not None:
            request_id = error.headers.get("x-request-id") or error.headers.get("request-id")
        try:
            body = error.read()
            raw = {"kind": "http_response_bytes", "fidelity": "exact_bytes", "value": {"base64": base64.b64encode(body).decode("ascii"), "byte_length": len(body)}, "limitations": []}
            try:
                text = body.decode("utf-8")
            except UnicodeDecodeError:
                # Replacement is for display/parsing only; the original bytes are above.
                text = body.decode("utf-8", errors="replace")
                raw["limitations"].append("display_utf8_replacement")
            message = text or message
        except Exception as capture_error:
            raw["fidelity"] = "unavailable"
            raw["limitations"] = ["http_body_read_failed: " + _message(capture_error)]
    details = error_details(text, http_status=http_status, request_id=request_id)
    status = "safety_block" if details["error_code"] in BLOCK_CODES else "error"
    return {
        "contract_version": CONTRACT_VERSION,
        **context,
        "outcome": {"status": status, "display_message": message.replace("\n", " ")[:280], **details},
        "raw_error": raw,
    }


def write_evidence(path: Path, evidence: dict) -> str:
    """Do not replace a previous attempt's evidence."""
    # JSON escapes preserve even an unpaired UTF-16 surrogate from native JS.
    content = (json.dumps(evidence, ensure_ascii=True, indent=2) + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(content)
    return hashlib.sha256(content).hexdigest()


def validate_evidence(path: Path, *, expected_sha256: str | None, attempt: int,
                      tool: str | None, status: str, prompt_en: str,
                      negative_en: str | None, generation_environment: str | None,
                      failure_reason: str | None = None) -> dict:
    content = path.read_bytes()
    sha256 = hashlib.sha256(content).hexdigest()
    if expected_sha256 and sha256 != expected_sha256:
        raise ValueError("attempt evidence SHA-256 mismatch")
    value = json.loads(content)
    if not isinstance(value, dict) or value.get("contract_version") != CONTRACT_VERSION:
        raise ValueError("attempt evidence contract version mismatch")
    request, outcome, raw = value.get("request"), value.get("outcome"), value.get("raw_error")
    if not all(isinstance(x, dict) for x in (request, outcome, raw)):
        raise ValueError("attempt evidence requires request, outcome and raw_error objects")
    display = outcome.get("display_message")
    if not isinstance(display, str) or (failure_reason is not None and failure_reason != display):
        raise ValueError("attempt evidence display message mismatch")
    checks = {"attempt": (value.get("attempt"), attempt), "tool": (value.get("tool"), tool),
              "status": (outcome.get("status"), status), "prompt_en": (request.get("prompt_en"), prompt_en),
              "negative_en": (request.get("negative_en"), negative_en)}
    for field, (actual, expected) in checks.items():
        if actual != expected:
            raise ValueError(f"attempt evidence {field} mismatch")
    if value.get("invocation_outcome") not in {"rejected", "returned"}:
        raise ValueError("attempt evidence must describe an observed invocation outcome")
    environment = value.get("generation_environment")
    if not isinstance(environment, str) or not environment or (generation_environment and environment != generation_environment):
        raise ValueError("attempt evidence generation_environment mismatch")
    if raw.get("fidelity") not in CAPTURE_FIDELITIES or not isinstance(raw.get("limitations"), list) or not all(isinstance(x, str) for x in raw["limitations"]):
        raise ValueError("attempt evidence requires capture fidelity and limitations")
    if "value" not in raw or not isinstance(request.get("runtime_prompt_en"), str):
        raise ValueError("attempt evidence requires raw value and exact runtime prompt")
    runtime = prompt_en + (f"\n\nAvoid: {negative_en}" if negative_en is not None else "")
    if request["runtime_prompt_en"] != runtime:
        raise ValueError("attempt evidence runtime prompt mismatch")
    if raw["fidelity"] == "exact_string" and not isinstance(raw["value"], str):
        raise ValueError("exact_string evidence must retain the string")
    if raw["fidelity"] == "exact_bytes":
        body = raw["value"]
        if not isinstance(body, dict) or not isinstance(body.get("base64"), str):
            raise ValueError("exact_bytes evidence must retain base64 bytes")
        if len(base64.b64decode(body["base64"], validate=True)) != body.get("byte_length"):
            raise ValueError("attempt evidence raw byte length mismatch")
    details = {key: outcome.get(key) for key in ("http_status", "error_code", "error_type", "request_id", "request_id_source", "moderation_stage", "categories", "classification_source")}
    categories = details["categories"]
    if not isinstance(categories, list) or not all(isinstance(x, str) for x in categories):
        raise ValueError("attempt evidence categories must be a string array")
    for key in ("error_code", "error_type", "request_id", "request_id_source", "moderation_stage"):
        if details[key] is not None and not isinstance(details[key], str):
            raise ValueError(f"attempt evidence {key} must be a string or null")
    if details["http_status"] is not None and (type(details["http_status"]) is not int or not 100 <= details["http_status"] <= 599):
        raise ValueError("attempt evidence http_status must be a valid integer or null")
    if details["classification_source"] not in {"structured_error_code", "unclassified"}:
        raise ValueError("attempt evidence classification_source is invalid")
    if status not in {"safety_block", "error"}:
        raise ValueError("error evidence cannot be attached to a successful attempt")
    expected_status = "safety_block" if details["error_code"] in BLOCK_CODES else "error"
    if status != expected_status:
        raise ValueError("attempt evidence status must match its explicit provider code")
    expected_source = "structured_error_code" if expected_status == "safety_block" else "unclassified"
    if details["classification_source"] != expected_source:
        raise ValueError("attempt evidence classification source mismatch")
    return {"attempt_evidence_path": str(path.resolve()), "attempt_evidence_sha256": sha256,
            "generation_environment": environment, "error_capture_fidelity": raw["fidelity"], "error_details": details,
            "failure_reason": display}


def main() -> int:
    parser = argparse.ArgumentParser(description="Save native error evidence from stdin without replacing an earlier attempt.")
    parser.add_argument("--write-json", type=Path, required=True)
    args = parser.parse_args()
    try:
        value = json.load(sys.stdin)
        if not isinstance(value, dict) or value.get("contract_version") != CONTRACT_VERSION:
            raise ValueError("attempt evidence contract version mismatch")
        digest = write_evidence(args.write_json, value)
    except Exception as error:
        print(f"Evidence save failed: {_message(error)}", file=sys.stderr)
        return 2
    print(json.dumps({"path": str(args.write_json.resolve()), "sha256": digest}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
