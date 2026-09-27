#!/usr/bin/env python3
"""Generate images for saved prompt JSON files via the OpenAI Images API.

The prompt text is forwarded byte-identical (prompt_en + "\n\nAvoid: <negative_en>");
no rewriting or safety softening happens here, which is required for prompt-dictionary
testing. Every attempt is appended to the run ledger via record_image_run.py.

Usage:
  python3 generate_images_via_api.py --prompt-json <file.json> --concept "<컨셉>" [--slug <slug>]
  python3 generate_images_via_api.py --prompt-dir <dir> [--attempts 2]

API key resolution: $OPENAI_API_KEY, then the project .env.
"""

from __future__ import annotations

import argparse
import base64
import datetime
import hashlib
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[2]
RECORD = SCRIPT_DIR / "record_image_run.py"


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


def call_api(key: str, model: str, prompt: str, size: str) -> bytes:
    payload = json.dumps({"model": model, "prompt": prompt, "size": size, "n": 1}).encode()
    request = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=payload,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=300) as response:
        data = json.loads(response.read())
    return base64.b64decode(data["data"][0]["b64_json"])


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


def generate_for_file(
    prompt_file: Path,
    *,
    key: str,
    model: str,
    size: str,
    attempts: int,
    concept: str | None,
    slug: str | None,
    out_base: Path,
    timestamp: str,
) -> bool:
    payload = json.loads(prompt_file.read_text(encoding="utf-8"))
    result = payload[0] if isinstance(payload, list) else payload
    prompt_en = str(result.get("prompt_en") or "")
    if not prompt_en:
        print(f"[{prompt_file.name}] prompt_en missing; skipped", file=sys.stderr)
        return False
    negative_raw = result.get("negative_en")
    negative_en = None if negative_raw is None else str(negative_raw)
    provenance = result.get("provenance") if isinstance(result.get("provenance"), dict) else {}
    prompt_id = str(provenance.get("prompt_id") or stable_text_id(prompt_en))
    seed = provenance.get("seed")
    full_prompt = prompt_en + (f"\n\nAvoid: {negative_en}" if negative_en else "")
    pack_id = str(result.get("pack_id") or provenance.get("pack_id") or "")
    chosen_candidate_ids = result.get("chosen_candidate_ids")
    chosen_visual_concept_ids = result.get("chosen_visual_concept_ids")
    effective_visual_contract_sha256 = str(
        result.get("effective_visual_contract_sha256") or ""
    )
    composer = str(result.get("composer") or "")
    audit = result.get("audit") if isinstance(result.get("audit"), dict) else {}
    audit_status = str(result.get("audit_status") or audit.get("status") or "")
    augmentation_brief = result.get("augmentation_brief")
    source_argv = provenance.get("argv")
    resolved_slug = slug_for(prompt_file, slug)
    resolved_concept = concept or str((provenance.get("concept_lock") or [""])[0] or resolved_slug)
    out_dir = out_base / f"{resolved_slug}-{timestamp}"

    previous_run_id: str | None = None
    for attempt in range(1, max(1, attempts) + 1):
        status, failure, dest = None, None, None
        try:
            image = call_api(key, model, full_prompt, size)
            out_dir.mkdir(parents=True, exist_ok=True)
            dest = out_dir / f"{prompt_id}-seed{seed}-attempt{attempt}.png"
            dest.write_bytes(image)
            status = "success"
            print(f"[{resolved_slug}] attempt {attempt} OK → {repo_ledger_path(dest)}")
        except urllib.error.HTTPError as error:
            body = error.read().decode()[:300]
            lowered = body.lower()
            status = (
                "safety_block"
                if ("safety" in lowered or "moderation" in lowered or "content_policy" in lowered)
                else "error"
            )
            failure = body.replace("\n", " ")[:280]
            print(f"[{resolved_slug}] attempt {attempt} {status}: {failure[:120]}")
        except Exception as error:  # noqa: BLE001 - 네트워크/디코딩 등 모든 실패를 레저에 기록
            status, failure = "error", str(error)[:280]
            print(f"[{resolved_slug}] attempt {attempt} error: {failure[:120]}")

        ledger_args = [
            "--ts", datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
            "--concept", resolved_concept,
            "--prompt-en", prompt_en,
            "--attempt", str(attempt),
            "--status", status,
            "--tool", "openai_images_api",
        ]
        ledger_args += ["--prompt-id", prompt_id]
        if seed is not None:
            ledger_args += ["--seed", str(seed)]
        if negative_en is not None:
            ledger_args += ["--negative-en", negative_en]
        if dest is not None and status == "success":
            ledger_args += ["--image-path", repo_ledger_path(dest)]
        if failure:
            ledger_args += ["--failure-reason", failure]
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
        try:
            ledger_result = record(ledger_args)
        except RuntimeError as error:
            print(f"[{resolved_slug}] {error}", file=sys.stderr)
            return False
        previous_run_id = ledger_result["run_id"]
        if status == "success":
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate images for saved prompt JSON via OpenAI Images API.")
    parser.add_argument("--prompt-json", action="append", default=[], help="Prompt JSON file (generator output). Repeatable.")
    parser.add_argument("--prompt-dir", default=None, help="Directory of *.prompt.json or *.json generator outputs.")
    parser.add_argument("--concept", default=None, help="Concept label for the ledger (single-file mode).")
    parser.add_argument("--slug", default=None, help="Filesystem slug override (single-file mode).")
    parser.add_argument("--model", default="gpt-image-2")
    parser.add_argument("--size", default="1024x1536")
    parser.add_argument("--attempts", type=int, default=2, help="Max attempts per prompt with the unchanged text.")
    parser.add_argument("--out-base", default=str(PROJECT_ROOT / "generated_images"))
    args = parser.parse_args()

    files = [Path(item) for item in args.prompt_json]
    if args.prompt_dir:
        directory = Path(args.prompt_dir)
        files += sorted(directory.glob("*.prompt.json")) or sorted(
            path for path in directory.glob("*.json") if not path.name.endswith(".explain.json")
        )
    if not files:
        parser.error("provide --prompt-json or --prompt-dir")
    if (args.concept or args.slug) and len(files) > 1:
        parser.error("--concept/--slug only apply to single-file mode")

    key = load_api_key()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    successes = 0
    for prompt_file in files:
        ok = generate_for_file(
            prompt_file,
            key=key,
            model=args.model,
            size=args.size,
            attempts=args.attempts,
            concept=args.concept,
            slug=args.slug,
            out_base=Path(args.out_base),
            timestamp=timestamp,
        )
        successes += int(ok)
    print(f"done: {successes}/{len(files)} succeeded")
    return 0 if successes == len(files) else 1


if __name__ == "__main__":
    raise SystemExit(main())
