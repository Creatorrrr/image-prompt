import hashlib, json, subprocess, sys
from pathlib import Path
from datetime import datetime, timezone
root=Path(__file__).resolve().parents[1]
label=sys.argv[1]
argv=sys.argv[2:]
logs=root/'run'/'command-logs'
logs.mkdir(exist_ok=True)
started=datetime.now(timezone.utc).isoformat(timespec='microseconds')
result=subprocess.run(argv,cwd=root,capture_output=True)
ended=datetime.now(timezone.utc).isoformat(timespec='microseconds')
stdout_path=logs/(label+'.stdout')
stderr_path=logs/(label+'.stderr')
stdout_path.write_bytes(result.stdout)
stderr_path.write_bytes(result.stderr)
row={'label':label,'started_at_utc':started,'ended_at_utc':ended,'cwd':str(root),'argv':argv,'returncode':result.returncode,'stdout_path':str(stdout_path),'stderr_path':str(stderr_path),'stdout_sha256':hashlib.sha256(result.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(result.stderr).hexdigest()}
with (root/'run'/'command-evidence.ndjson').open('a',encoding='utf-8') as f:
 f.write(json.dumps(row,ensure_ascii=False)+'\n')
print(json.dumps(row,ensure_ascii=False))
print(result.stdout.decode('utf-8',errors='replace')[:12000])
print(result.stderr.decode('utf-8',errors='replace')[:12000])
sys.exit(result.returncode)
