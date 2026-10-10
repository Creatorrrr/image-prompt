"""Restore original effective contract fields; retain semantics-only refinements."""
import copy
import json
from pathlib import Path
import sys
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / "skills/photo-prompt-image-generator"
ASSETS = SKILL / "assets"
sys.path.insert(0, str(SKILL / "scripts"))
from photo_candidate_semantics import digest
from photo_retry_projection import visual_obligation
from photo_runtime_sources import source_update
from visual_profile_contracts import compile_visual_profile


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


name = "photo_prompt_visual_obligations_wardrobe_owner_relations.json"
with zipfile.ZipFile(HERE / "SCOPED-BEFORE.zip") as archive:
    before = json.loads(archive.read("skills/photo-prompt-image-generator/assets/" + name))
profiles = read(ASSETS / name)
old_by_id = {r["id"]: r for r in before["profiles"]}
restored = []
for row in profiles["profiles"]:
    if row["id"] not in old_by_id:
        continue
    old = old_by_id[row["id"]]
    if row["reject_substitutes"] != old["reject_substitutes"]:
        restored.append(row["id"])
        row["reject_substitutes"] = copy.deepcopy(old["reject_substitutes"])
    assert visual_obligation(compile_visual_profile(row)) == visual_obligation(compile_visual_profile(old))
    assert row["activation"] == old["activation"]
assert len(restored) == 6

extension_path = ASSETS / "photo_prompt_wardrobe_owner_relations_extension.json"
extension = read(extension_path)
prior_ref = extension.pop("maintenance_ref")
record = read(HERE.parent / "extension-maintenance" / (prior_ref["record_id"] + ".json"))
changes = read(HERE / "DATA-CHANGES.json")
changes.update(complete_old_effective_contract_projections_preserved=True,
               existing_hard_reject_substitutes_restored=restored,
               refined_contrasts_location="semantics.contrast_examples and ordinary candidate bundle confusion_boundaries",
               inherited_contract_comparison_count=len(old_by_id))
record.update(record_id="wardrobe-owner-relations-20261010-v8", prior_maintenance_ref=prior_ref,
              authored_source_sha256=digest(extension), profile_source_sha256=digest(profiles), decisions_sha256=digest(changes),
              reason="Keep all inherited effective obligation projection fields exact; retain new contrast explanations in semantics-only data.")
extension["maintenance_ref"] = {"contract_version": "photo-extension-maintenance-ref/v1", "record_id": record["record_id"], "sha256": digest(record)}
publication = HERE / "runtime-publication.json"
(HERE / "runtime-publication-before-contract-restoration.json").write_bytes(publication.read_bytes())
with source_update(SKILL):
    write(HERE.parent / "extension-maintenance" / (record["record_id"] + ".json"), record)
    write(ASSETS / name, profiles)
    write(extension_path, extension)
write(HERE / "DATA-CHANGES.json", changes)
write(HERE / "INHERITED-CONTRACT-PRESERVATION.json", {
    "status": "PASS", "compared_existing_compiled_obligation_projections": len(old_by_id),
    "restored_hard_contract_fields": restored, "all_existing_activation_exact": True,
    "all_existing_effective_obligation_projection_fields_exact": True,
    "new_semantic_contrasts_retained": True, "prior_runtime_generation_retained": True})
errors_path = HERE / "PROVISIONAL-VALIDATION-ERRORS.json"
errors = read(errors_path)
errors["errors"].append({"stage": "inherited_contract_compatibility", "kind": "maintenance_data_error",
                         "failure": "Six added reject_substitutes entries changed closed effective obligations; caught by direct projection comparison before image invocation.",
                         "resolution": "Restore those hard fields, retain contrast in semantics-only fields, rebuild indexes and publish a successor before revised qualification.",
                         "image_calls": 0, "resolved": True})
write(errors_path, errors)
print(json.dumps({"status": "PASS", "restored": restored, "compared": len(old_by_id)}))
