from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import subprocess
import sys

run = Path(__file__).resolve().parent
label = sys.argv[1]
assert re.fullmatch(r"[a-z0-9_-]+", label)
argv = sys.argv[2:]
if argv and argv[0] == "--": argv = argv[1:]
evidence = run / "evidence"
evidence.mkdir(exist_ok=True)
started = datetime.now(timezone.utc).isoformat()
completed = subprocess.run(argv, cwd=run.parent, capture_output=True, text=True, encoding="utf-8")
ended = datetime.now(timezone.utc).isoformat()
stdout_path = evidence / (label + ".stdout.txt")
stderr_path = evidence / (label + ".stderr.txt")
stdout_path.write_text(completed.stdout, encoding="utf-8")
stderr_path.write_text(completed.stderr, encoding="utf-8")
result = {"label": label, "argv": argv, "cwd": str(run.parent), "started_at_utc": started, "ended_at_utc": ended, "exit_code": completed.returncode, "stdout_path": str(stdout_path), "stderr_path": str(stderr_path), "stdout_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(), "stderr_sha256": hashlib.sha256(completed.stderr.encode()).hexdigest()}
(evidence / (label + ".result.json")).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
with (run / "commands.ndjson").open("a", encoding="utf-8") as stream: stream.write(json.dumps(result, ensure_ascii=False) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
if completed.stdout: print(completed.stdout)
if completed.stderr: print(completed.stderr, file=sys.stderr)
raise SystemExit(completed.returncode)
