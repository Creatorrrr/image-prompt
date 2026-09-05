"""Recheck frozen replay bindings without generation or runtime edits."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from PIL import Image

RUN = Path(__file__).resolve().parent
REPO = RUN.parent.parent
SKILL = REPO / "skills/reverse-image-prompt"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


snapshot = read(RUN / "candidate-snapshot-v3.json")
snapshot_checks = []
for base in [SKILL, *(RUN / "cases" / f"case-{n:02d}" / "skill-v3" for n in range(1, 4))]:
    mismatches = []
    for item in snapshot["files"]:
        path = base / item["path"]
        if not path.is_file() or sha(path.read_bytes()) != item["sha256"]:
            mismatches.append(item["path"])
    snapshot_checks.append({"root": str(base), "checked_files": len(snapshot["files"]), "mismatches": mismatches})

configs = [
    ("case-01", "cf1cd9cd11ccc5748e03f75e6d9c6b01943728d03651712c1d84f3f13a75874d", "analysis-bundle.json", ["generation-request.json"]),
    ("case-02", "9f22a88255115bd33062593568a9773626ccb23f8e482824752a09b91f20fc71", "bundle.json", ["generation-request.json", "generation-request.raw.json"]),
    ("case-03", "a3e2b2dcf5d8aa7b8d78e564452f48c60e579db1282e090bd3dcaa9015e83aa9", "analysis-bundle.json", ["generation-input.json", "generation-request.attempt-01.json", "generation-request.attempt-02.json"]),
]
cases = []
jobs = []
for case, source_sha, bundle_name, request_names in configs:
    base = RUN / "cases" / case
    out = base / "output"
    prompt = (out / "prompt.txt").read_bytes()
    plan = read(out / "plan.json")
    canonical = json.dumps(plan, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    critic = read(out / "critic-root.json")
    requests = []
    for name in request_names:
        request = read(out / name)
        requests.append({"file": name, "fields": sorted(request), "only_prompt": set(request) == {"prompt"}, "prompt_matches_frozen_bytes": request["prompt"].encode("utf-8") == prompt})
    sources = [{"file": str(path), "sha256": sha(path.read_bytes()), "matches_selected_input": sha(path.read_bytes()) == source_sha} for path in [RUN / "inputs" / f"{case}.jpg", base / "source.jpg"]]
    render_path = out / "render.png"
    render = None
    if render_path.exists():
        with Image.open(render_path) as image:
            render = {"file": str(render_path), "sha256": sha(render_path.read_bytes()), "bytes": render_path.stat().st_size, "dimensions": list(image.size), "mode": image.mode}
    row = {"case_id": case, "sources": sources, "prompt_bytes": len(prompt), "prompt_words": len(prompt.decode("utf-8").split()), "prompt_sha256": sha(prompt), "plan_canonical_sha256": sha(canonical), "critic_status": critic["status"], "critic_prompt_matches": sha(prompt) == critic["prompt_sha256"], "critic_plan_matches": sha(canonical) == critic["integrated_plan_sha256"], "requests": requests, "render": render}
    cases.append(row)
    for tool, args in [
        ("analysis_bundle.py", [str(out / bundle_name)]),
        ("salience_plan.py", [str(out / "plan.json"), "--prompt", str(out / "prompt.txt")]),
        ("prompt_lint.py", [str(out / "prompt.txt")]),
    ]:
        jobs.append((case, tool, [sys.executable, str(base / "skill-v3/tools" / tool), *args], base / "skill-v3"))


def run_check(job):
    case, tool, command, cwd = job
    result = subprocess.run(command, cwd=cwd, env=ENV, capture_output=True, text=True)
    return {"case_id": case, "tool": tool, "command": command, "exit_code": result.returncode, "stdout": result.stdout.strip(), "stderr": result.stderr.strip()}


with ThreadPoolExecutor(max_workers=3) as pool:
    checks = list(pool.map(run_check, jobs))
passed = (
    all(not row["mismatches"] for row in snapshot_checks)
    and all(row["critic_prompt_matches"] and row["critic_plan_matches"] and row["critic_status"] == "pass" and all(x["matches_selected_input"] for x in row["sources"]) and all(x["only_prompt"] and x["prompt_matches_frozen_bytes"] for x in row["requests"]) for row in cases)
    and all(row["exit_code"] == 0 for row in checks)
    and cases[0]["render"] is not None
    and cases[1]["render"] is not None
    and cases[2]["render"] is None
)
record = {"schema_version": "reverse-skill-final-integrity/v1", "recorded_at": datetime.now(timezone.utc).isoformat(), "status": "pass" if passed else "fail", "candidate_snapshot_sha256": snapshot["manifest_sha256"], "snapshot_checks": snapshot_checks, "cases": cases, "final_frozen_artifact_checks": checks, "scope": "Checks the listed snapshot files, final critic bindings and saved exact request bodies. Extra files are not asserted absent. Raw tool event provenance and every generation outcome remain in each case report. These checks do not establish visual fidelity."}
save(RUN / "final-integrity.json", record)
print(json.dumps({"status": record["status"], "snapshot_files_per_root": len(snapshot["files"]), "snapshot_roots": len(snapshot_checks), "frozen_artifact_checks": len(checks), "cases": [{"case": row["case_id"], "words": row["prompt_words"], "render": bool(row["render"])} for row in cases]}))
raise SystemExit(0 if passed else 1)
