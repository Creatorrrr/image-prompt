"""Seal current maintenance metadata without changing a runtime relation."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
RECORDS = ROOT / "docs/research-evidence/photo-prompt/extension-maintenance"

def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()

def main():
    ledger = json.loads((HERE / "INTEGRATION-LEDGER.json").read_text())
    receipts = []
    for row in ledger["source_files"]:
        path = ROOT / row["path"]
        source = json.loads(path.read_text())
        if "slots" not in source:
            continue
        before = copy.deepcopy(source)
        old_ref = source["maintenance_ref"]
        old = json.loads((RECORDS / (old_ref["record_id"] + ".json")).read_text())
        assert digest(old) == old_ref["sha256"]
        plain = {k: v for k, v in source.items() if k != "maintenance_ref"}
        assert digest(plain) == old["authored_source_sha256"]
        record_id = path.stem + "-uniform-maintenance-seal-20261004"
        record = {**old, "record_id": record_id, "maintenance_only": True,
                  "prior_maintenance_ref": old_ref,
                  "scope": "Seal required external maintenance metadata; runtime rows, meanings, aliases, effects and native gates are byte-equivalent."}
        record_path = RECORDS / (record_id + ".json")
        assert not record_path.exists(), "Seal is append-only."
        record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
        source["maintenance_ref"] = {**old_ref, "record_id": record_id, "sha256": digest(record)}
        assert {k: v for k, v in source.items() if k != "maintenance_ref"} == plain
        path.write_text(json.dumps(source, ensure_ascii=False, indent=2) + "\n")
        row["after_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        receipts.append({"file": path.name, "runtime_rows_unchanged": before["slots"] == source["slots"],
                         "plain_source_sha256_unchanged": digest(plain),
                         "old_reference": old_ref, "new_reference": source["maintenance_ref"]})
    (HERE / "maintenance-seal-receipt.json").write_text(json.dumps({"schema_version": "uniform-maintenance-seal/v1", "files": receipts}, ensure_ascii=False, indent=2) + "\n")
    (HERE / "INTEGRATION-LEDGER.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"sealed_records": len(receipts), "runtime_surface_unchanged": True}))

if __name__ == "__main__":
    main()
