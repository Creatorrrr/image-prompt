#!/usr/bin/env python3
"""Generate from an exact pack/receipt/composed/runtime input after fresh audits.

Only the audited text-only runtime string is sent. References and raw prompt
inputs fail before key resolution or a paid invocation. Dry-run has no calls.
"""

from __future__ import annotations

import argparse
import base64
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import uuid
from dataclasses import dataclass
import urllib.error
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[2]
RECORD = SCRIPT_DIR / "record_image_run.py"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
from image_attempt_evidence import capture_api_error, write_evidence
from photo_api_render import prepare_api_render, save_preflight, PreflightError


@dataclass(frozen=True)
class ApiImageResult:
    image_bytes: bytes
    observed_model: str | None = None
    request_id: str | None = None


def load_api_key() -> str:
    import os

    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if key:
        return key
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("OPENAI_API_KEY="):
                return line.split("=", 1)[1].strip().strip("\"'")
    raise SystemExit("OPENAI_API_KEY not found in environment or project .env")


def call_api(key: str, model: str, prompt: str, size: str) -> ApiImageResult:
    payload = json.dumps({"model": model, "prompt": prompt, "size": size, "n": 1}).encode()
    request = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=payload,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=300) as response:
        data = json.loads(response.read())
        request_id = response.headers.get("x-request-id")
    observed = data.get("model")
    return ApiImageResult(base64.b64decode(data["data"][0]["b64_json"], validate=True),
        observed if isinstance(observed, str) and observed else None, request_id)


def slug_for(path: Path, override: str | None) -> str:
    if override:
        return override
    stem = re.sub(r"\.prompt$", "", path.stem)
    return re.sub(r"[^A-Za-z0-9가-힣-]+", "-", stem).strip("-") or "prompt"


def stable_text_id(text: str, length: int = 16) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def repo_ledger_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(PROJECT_ROOT.resolve()))
    except ValueError:
        return str(path.resolve())


def compact_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def record(args_list: list[str]) -> dict[str, str]:
    completed = subprocess.run(
        [sys.executable, str(RECORD), *args_list], capture_output=True, text=True
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip()[-400:] or "recorder returned no error detail"
        raise RuntimeError(f"ledger record failed: {detail}")
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("ledger recorder returned invalid JSON") from exc
    if not isinstance(payload, dict) or not str(payload.get("run_id") or ""):
        raise RuntimeError("ledger recorder returned no run_id")
    return {str(key): str(value) for key, value in payload.items()}


def generate_for_request(pack_file: Path, *, receipt_file: Path, composed_file: Path, request_file: Path,
    model: str, size: str, attempts: int, concept: str | None, slug: str | None, out_base: Path,
    timestamp: str, runtime_store: Path | None = None, dry_run: bool = False,
    ledger: Path | None = None, key: str | None = None, initial_retry_of: str | None = None,
    workflow_operation_id: str | None = None, attempt_event=None, execution_summary: Path | None = None) -> bool:
    summary = {"schema_version": "photo-api-execution/v1", "operation_id": workflow_operation_id,
               "image_call_count": 0, "attempts": [], "status": "preparing"}
    def event(stage, **fields):
        summary["status"] = stage
        row = {"stage": stage, **fields}
        summary["attempts"].append(row)
        if stage == "invocation_started":
            summary["image_call_count"] += 1
        if execution_summary is not None:
            from photo_workflow_state import atomic_write, encode
            atomic_write(execution_summary, encode(summary))
        if attempt_event is not None:
            attempt_event(row)
    resolved_slug = slug_for(pack_file, slug)
    if workflow_operation_id is not None and not re.fullmatch(r"[0-9a-f]{32}", workflow_operation_id):
        raise ValueError("invalid workflow operation ID")
    if attempts < 1:
        print("attempts must be positive", file=sys.stderr)
        return False
    out_dir = out_base / (workflow_operation_id if workflow_operation_id else f"{resolved_slug}-{timestamp}-{uuid.uuid4().hex}")
    try:
        prepared = prepare_api_render(pack_file, receipt_file, composed_file, request_file,
            model=model, size=size, runtime_store=runtime_store)
        out_dir.mkdir(parents=True, exist_ok=False)
        preflight_path = out_dir / "preflight.json"
        preflight_sha = save_preflight(preflight_path, prepared)
    except (ValueError, OSError, KeyError, TypeError) as error:
        try:
            out_dir.mkdir(parents=True, exist_ok=True)
            with (out_dir / "preflight-failure.json").open("x", encoding="utf-8") as handle:
                json.dump({"schema_version": "photo-api-render-preflight/v1", "status": "fail", "image_call_count": 0,
                    "stage": getattr(error, "stage", "input_or_persistence"), "detail": getattr(error, "detail", str(error))}, handle, ensure_ascii=False, indent=2)
        except OSError:
            pass  # Display the original preparation failure; never call to repair it.
        print(f"[{resolved_slug}] preflight failed; API calls: 0; {error}", file=sys.stderr)
        return False
    if dry_run:
        print(compact_json({"status": "pass", "preflight": str(preflight_path), "sha256": preflight_sha, "image_call_count": 0}))
        return True
    execution = prepared.document["execution"]
    prompt_en, negative_en, full_prompt = execution["prompt_en"], execution["negative_en"], execution["runtime_prompt_en"]
    prompt_id, seed = stable_text_id(prompt_en), None
    pack_id = execution["pack_id"]
    chosen_candidate_ids, chosen_visual_concept_ids = execution["chosen_candidate_ids"], execution["chosen_visual_concept_ids"]
    effective_visual_contract_sha256 = execution["effective_visual_contract_sha256"] if chosen_visual_concept_ids else None
    composer, audit_status, augmentation_brief = execution["composer"], execution["audit_status"], execution["augmentation_brief"]
    resolved_concept = concept or resolved_slug
    source_argv = None
    try:
        key = key if key is not None else load_api_key()
    except SystemExit:
        event("preflight_failed", known_no_invocations=True)
        return False

    previous_run_id: str | None = initial_retry_of
    for attempt in range(1, attempts + 1):
        status, failure, dest, evidence = None, None, None, None
        started_at = datetime.datetime.now().astimezone().isoformat(timespec="microseconds")
        call_returned = False
        response = None
        retry_allowed = False
        operation_attempt = f"{workflow_operation_id}:{attempt}" if workflow_operation_id else None
        reserved_run_id = stable_text_id(f"{started_at}|{prompt_id}|{attempt}")
        event("invocation_started", attempt=attempt, timestamp=started_at, run_id=reserved_run_id,
              operation_attempt=operation_attempt, preflight=str(preflight_path), preflight_sha256=preflight_sha)
        try:
            response = call_api(key, execution["model"], full_prompt, execution["size"])
            call_returned = True
            dest = out_dir / f"{prompt_id}-seed{seed}-attempt{attempt}.png"
            # Preserve returned bytes even if the image writer fails.
            recovery = out_dir / f"attempt{attempt}.returned-image.bin"
            with recovery.open("xb") as handle:
                handle.write(response.image_bytes)
                handle.flush()
                os.fsync(handle.fileno())
            event("result_received", attempt=attempt, recovery=str(recovery), sha256=hashlib.sha256(response.image_bytes).hexdigest())
            dest.write_bytes(response.image_bytes)
            descriptor = os.open(dest, os.O_RDWR)
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
            status = "success"
            print(f"[{resolved_slug}] attempt {attempt} OK → {repo_ledger_path(dest)}")
        except Exception as error:  # noqa: BLE001 - 네트워크/디코딩 등 모든 실패를 레저에 기록
            retry_allowed = isinstance(error, urllib.error.HTTPError) and error.code in {429, 500, 502, 503, 504}
            evidence = capture_api_error(error, {
                "tool": "openai_images_api", "generation_environment": "openai_images_api", "attempt": attempt,
                "started_at": started_at, "ended_at": datetime.datetime.now().astimezone().isoformat(timespec="microseconds"),
                "invocation_outcome": "returned" if call_returned else "rejected",
                "provider_outcome": "returned" if call_returned else ("rejected" if isinstance(error, urllib.error.HTTPError) else "unknown"),
                "request": {"prompt_en": prompt_en, "negative_en": negative_en, "runtime_prompt_en": full_prompt, "requested_model": model, "size": size},
            })

        evidence_path, evidence_sha256 = None, None
        if evidence is not None:
            status = evidence["outcome"]["status"]
            failure = evidence["outcome"]["display_message"]
            evidence_path = out_dir / f"{prompt_id}-seed{seed}-attempt{attempt}.error.json"
            try:
                evidence_sha256 = write_evidence(evidence_path, evidence)
            except OSError as error:
                print(f"[{resolved_slug}] attempt {attempt} evidence save failed; stopping: {error}", file=sys.stderr)
                event("persistence_failed", attempt=attempt)
                return False
            print(f"[{resolved_slug}] attempt {attempt} {status}: {failure[:120]}")

        ledger_args = [
            "--ts", started_at,
            "--concept", resolved_concept,
            "--prompt-en", prompt_en,
            "--attempt", str(attempt),
            "--status", status,
            "--tool", "openai_images_api",
            "--generation-environment", "openai_images_api",
        ]
        ledger_args += ["--prompt-id", prompt_id,
            "--api-render-input-json", str(preflight_path), "--api-render-input-sha256", preflight_sha,
            "--runtime-prompt-sha256", execution["runtime_prompt_sha256"],
            "--requested-image-model", execution["model"], "--image-size", execution["size"],
            "--authorial-core-sha256", execution["authorial_core_sha256"],
            "--intent-lock-sha256", execution["intent_lock_sha256"], "--image-call-count", str(attempt)]
        if execution["render_repair_contract_sha256"]:
            ledger_args += ["--render-repair-contract-sha256", execution["render_repair_contract_sha256"]]
        if response is not None:
            if response.observed_model:
                ledger_args += ["--observed-image-model", response.observed_model]
            if response.request_id:
                ledger_args += ["--provider-request-id", response.request_id]
        if ledger is not None:
            ledger_args += ["--ledger", str(ledger)]
        if seed is not None:
            ledger_args += ["--seed", str(seed)]
        if negative_en is not None:
            ledger_args += ["--negative-en", negative_en]
        if dest is not None and status == "success":
            ledger_args += ["--image-path", repo_ledger_path(dest)]
        if failure:
            ledger_args += ["--failure-reason", failure]
        if evidence_path is not None:
            ledger_args += ["--attempt-evidence-json", str(evidence_path), "--attempt-evidence-sha256", evidence_sha256]
        if pack_id:
            ledger_args += ["--pack-id", pack_id]
        if chosen_candidate_ids is not None:
            ledger_args += ["--chosen-candidate-ids-json", compact_json(chosen_candidate_ids)]
        if chosen_visual_concept_ids is not None:
            ledger_args += [
                "--chosen-visual-concept-ids-json",
                compact_json(chosen_visual_concept_ids),
            ]
        if effective_visual_contract_sha256:
            ledger_args += [
                "--effective-visual-contract-sha256",
                effective_visual_contract_sha256,
            ]
        if composer:
            ledger_args += ["--composer", composer]
        if audit_status:
            ledger_args += ["--audit-status", audit_status]
        if isinstance(augmentation_brief, dict):
            ledger_args += ["--augmentation-brief-json", compact_json(augmentation_brief)]
        if isinstance(source_argv, list):
            ledger_args += ["--argv-json", compact_json(source_argv)]
        if previous_run_id:
            ledger_args += ["--retry-of", previous_run_id]
        if operation_attempt:
            ledger_args += ["--workflow-operation-id", operation_attempt]
        event("record_ready", attempt=attempt, ledger_args=ledger_args,
              image_path=str(dest) if dest is not None and status == "success" else None,
              evidence_path=str(evidence_path) if evidence_path else None, outcome=status,
              provider_outcome=evidence.get("provider_outcome") if evidence else "returned")
        try:
            ledger_result = record(ledger_args)
        except RuntimeError as error:
            event("recorder_failed", attempt=attempt)
            print(f"[{resolved_slug}] {error}", file=sys.stderr)
            return False
        previous_run_id = ledger_result["run_id"]
        event("attempt_recorded", attempt=attempt, ledger_run_id=previous_run_id, outcome=status,
              provider_outcome=evidence.get("provider_outcome") if evidence else "returned",
              terminal=(status == "success" or status == "safety_block" or not retry_allowed or call_returned or attempt == attempts))
        if status == "success":
            return True
        if status == "safety_block" or (not call_returned and not retry_allowed):
            return False
        if call_returned:
            # The provider returned an image; retrying a local save failure would
            # generate another image rather than repair its persistence.
            return False
    return False


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ("pack", "runtime-receipt", "composed", "render-request"):
        parser.add_argument("--" + flag, type=Path, required=True)
    parser.add_argument("--runtime-store", type=Path)
    parser.add_argument("--concept")
    parser.add_argument("--slug")
    parser.add_argument("--model", default="gpt-image-2")
    parser.add_argument("--size", default="1024x1536")
    parser.add_argument("--attempts", type=int, default=2)
    parser.add_argument("--out-base", type=Path, default=PROJECT_ROOT / "generated_images")
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    if args.attempts < 1:
        parser.error("--attempts must be positive")
    return 0 if generate_for_request(args.pack, receipt_file=args.runtime_receipt,
        composed_file=args.composed, request_file=args.render_request, runtime_store=args.runtime_store,
        model=args.model, size=args.size, attempts=args.attempts, concept=args.concept, slug=args.slug,
        out_base=args.out_base, timestamp=datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
        dry_run=args.dry_run, ledger=args.ledger) else 1


if __name__ == "__main__":
    raise SystemExit(main())
