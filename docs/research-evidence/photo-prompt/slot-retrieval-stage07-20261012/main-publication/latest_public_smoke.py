"""Exercise the actual public CLI, view, receipt and source audit on the final snapshot."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = Path('/Users/chasoik/.codex/worktrees/slot-retrieval-stage07-integration/image-prompt')
PYTHON = Path('/Users/chasoik/Projects/image-prompt/.venv/bin/python')
meta = json.loads((OUT/'LATEST-RUNTIME.json').read_text())
source = OUT/'repaired-public-natural/dev-02-blue-cup-en'
folder = OUT/'latest-public-cli/dev-02-blue-cup-en'
folder.mkdir(parents=True, exist_ok=True)
argv = json.loads((source/'generate-command.json').read_text())
for i, value in enumerate(argv):
    if value.startswith(str(source)):
        relative = Path(value).relative_to(source)
        if (source/relative).is_file() and relative.name != 'candidate-pack.json':
            shutil.copy2(source/relative, folder/relative)
        argv[i] = str(folder/relative)
    if i and argv[i-1] == '--runtime-store':
        argv[i] = meta['store']
command = [str(PYTHON), str(ROOT/'skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py'), *argv]
(folder/'generate-command.json').write_text(json.dumps(command, indent=2)+'\n')
result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
(folder/'generate.log').write_text(result.stdout+result.stderr)
assert result.returncode == 0, result.stderr
pack_path = folder/'candidate-pack.json'
command = [str(PYTHON), str(ROOT/'skills/photo-prompt-image-generator/scripts/compose_pack_view.py'),
           '--pack', str(pack_path), '--output', str(folder/'composer-view.json')]
view = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
(folder/'view.log').write_text(view.stdout+view.stderr)
assert view.returncode == 0, view.stderr
sys.path.insert(0, str(ROOT/'skills/photo-prompt-image-generator/scripts'))
from photo_runtime_sources import RuntimeSnapshotProvider
import audit_composed_prompt as audit
pack = json.loads(pack_path.read_text())[0]
receipt = json.loads(Path(str(pack_path)+'.runtime-receipt.json').read_text())
snapshot = RuntimeSnapshotProvider(ROOT/'skills/photo-prompt-image-generator', Path(meta['store'])).from_receipt(pack, receipt)
assert snapshot.generation_id == meta['generation_id']
issues = audit.audit_core_retrieval(pack, snapshot.data)
assert not issues, issues
api = OUT/'latest-api-natural/dev-02-blue-cup-en/candidate-pack.json'
if api.exists():
    assert pack == json.loads(api.read_text())[0]
record = dict(case='dev-02-blue-cup-en', cli_exit=result.returncode, view_exit=view.returncode,
              actual_receipt_verified=True, generation_id=snapshot.generation_id,
              source_recomputation_errors=issues, api_pack_byte_meaning_identical=api.exists(),
              pack_sha256=hashlib.sha256(pack_path.read_bytes()).hexdigest())
(OUT/'LATEST-PUBLIC-CLI-SMOKE.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(record), flush=True)
