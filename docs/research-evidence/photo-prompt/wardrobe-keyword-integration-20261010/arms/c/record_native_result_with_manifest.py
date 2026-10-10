"""Attach arm provenance through the maintained native-result and recorder APIs."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[6]
SCRIPTS = ROOT / "skills/photo-prompt-image-generator/scripts"
sys.path.insert(0, str(SCRIPTS))
import photo_workflow
import generate_images_via_api

arm = Path(__file__).resolve().parent
state = json.loads((arm / "run/workflow.json").read_text())
identity = json.loads((arm / "independent_source_identity.json").read_text())
source_ref = "runtime-receipt:" + state["artifacts"]["runtime_receipt"]["sha256"]
extra = ["--arm-id", "c", "--worktree-id", identity["worktree_id"],
         "--skill-sha256", identity["skill_sha256"], "--source-ref", source_ref,
         "--candidate-pack-version", "v6", "--independent-no-cross-arm-inputs",
         "--manifest", str(arm / "run_manifest.json")]
composed = json.loads(Path(state["artifacts"]["composed"]["path"]).read_text())
if composed.get("augmentation_brief"):
    extra += ["--augmentation-brief-json", json.dumps(composed["augmentation_brief"], ensure_ascii=False)]
original_record = generate_images_via_api.record

def record_with_provenance(flags):
    exact = flags + extra
    (arm / "native_record_arguments.json").write_text(json.dumps(exact, ensure_ascii=False, indent=2) + "\n")
    return original_record(exact)

generate_images_via_api.record = record_with_provenance
p = argparse.ArgumentParser()
p.add_argument("--result", type=Path, required=True)
a = p.parse_args()
args = argparse.Namespace(run=arm / "run", ledger=arm / "image_runs.ndjson", result=a.result)
result = photo_workflow.native_result(args)
print(json.dumps(result, ensure_ascii=False, indent=2))
