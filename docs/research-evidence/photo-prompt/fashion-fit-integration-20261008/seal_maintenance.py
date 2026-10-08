"""Create a metadata-only successor without rewriting any prior evidence."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
from photo_candidate_semantics import digest, MAINTENANCE_VERSION
from photo_runtime_sources import source_update

path = SKILL / "assets/photo_prompt_fashion_fit_extension.json"
source = json.loads(path.read_text())
prior = source.pop("maintenance_ref")
record_id = "fashion-fit-maintenance-seal-20261008"
record_path = ROOT / "docs/research-evidence/photo-prompt/extension-maintenance" / (record_id + ".json")
if record_path.exists():
    raise SystemExit("successor already exists; no immutable evidence overwrite")
record = {
    "schema_version": "photo-extension-maintenance/v1",
    "record_id": record_id,
    "source_filename": path.name,
    "authored_source_sha256": digest(source),
    "prior_maintenance_ref": prior,
    "maintenance_only": True,
    "scope": "External maintenance metadata; the candidate text, relations, properties and activation remain byte-equivalent after removal of maintenance_ref.",
    "reason": "Declare the external-only maintenance contract required by the existing candidate-semantics regression. Preserve every earlier record and its hash-bound ancestry.",
}
source["maintenance_ref"] = {
    "contract_version": MAINTENANCE_VERSION,
    "record_id": record_id,
    "sha256": digest(record),
}
with source_update(SKILL):
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    path.write_text(json.dumps(source, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"record_id": record_id, "prior_record_id": prior["record_id"], "authored_source_sha256": record["authored_source_sha256"], "candidate_meaning_change": False}))
