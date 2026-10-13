"""One-time offline native contract migration from the frozen audit input."""
from __future__ import annotations
import copy
import gzip
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
sys.path.insert(0, str(ASSETS.parent / "scripts"))
import photo_candidate_corpus as c
import photo_global_index as index

def baseline():
    source = c.decode(gzip.decompress((OUT / "CORPUS-BEFORE.json.gz").read_bytes()))
    if c.digest(source) != json.loads((OUT / "STAGE01-VERIFICATION.json").read_text())["corpus_sha256"]:
        raise ValueError("frozen source changed")
    return source

def write_source(source, new_binding_owner=None):
    c.validate(source)
    manifest = c.decode((ASSETS / c.MANIFEST_NAME).read_bytes())
    present = {kind: set() for kind in c.MODULE_SCHEMAS}
    payloads = {}
    for module in manifest["modules"]:
        kind = module["kind"]
        payload = c.decode((ASSETS / module["file"]).read_bytes())
        keys = set(payload[kind])
        values = source[kind] if kind in {"slot_catalog", "policies"} else {
            key: source[kind][key] for key in payload[kind] if key in source[kind]}
        payloads[module["file"]] = {"schema": c.MODULE_SCHEMAS[kind], kind: values}
        present[kind].update(values)
    for kind in ("candidates", "slot_bindings"):
        for key in set(source[kind]) - present[kind]:
            if kind != "slot_bindings" or not new_binding_owner or key not in new_binding_owner:
                raise ValueError("unassigned source owner: " + key)
            payloads[new_binding_owner[key]][kind][key] = source[kind][key]
    for name, payload in payloads.items():
        (ASSETS / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    manifest["schema"] = c.MANIFEST_SCHEMA
    (ASSETS / c.MANIFEST_NAME).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    if c.digest(c.load(ASSETS)) != c.digest(source):
        raise ValueError("persisted native source differs")

def upgrade():
    before = baseline()
    target = json.loads((OUT / "TARGET-CATALOG.json").read_text())
    decisions = json.loads((OUT / "SLOT-DECISIONS.json").read_text())
    source = copy.deepcopy(before)
    source["schema"] = c.SCHEMA
    inverse = {decision["targets"][0]: old for old, decision in decisions.items()}
    inverse.update({name: name for name in before["slot_catalog"] if name in target})
    for old, row in before["slot_catalog"].items():
        spec = copy.deepcopy(target[decisions[old]["targets"][0]])
        spec["id"] = old
        spec["applicability"] = row["applicability"]
        spec["neighbors"] = sorted({inverse[name] for name in spec["neighbors"] if name in inverse} - {old})
        if not spec["neighbors"]:
            spec["neighbors"] = ["composition" if old != "composition" else "subject_framing"]
        if decisions[old]["action"] == "retire" or old == "motion":
            spec["semantic_role"] = "contextual"
            spec["description"] = "Unsplit authored relation awaiting its declared taxonomy migration: " + row["description"]
            spec["description_ko"] = "이관할 기존 복합 역할: " + row["description"]
        source["slot_catalog"][old] = spec
    condition_count = 0
    adult_context_ids = {binding["candidate_id"] for binding in before["slot_bindings"].values()
                         if binding["slot_id"] in {"adult_context", "fetish_styling"}}
    for cid, record in source["candidates"].items():
        content = record["content"]
        conditions = {key: content.pop(key) for key in list(content) if key in c.INTRINSIC_CONDITION_FIELDS}
        for key, value in list(conditions.items()):
            if isinstance(value, list):
                conditions[key] = list(dict.fromkeys(value))
        if cid in adult_context_ids:
            conditions["requires_adult_context"] = True
            conditions.setdefault("for_any", ["human"])
        record["conditions"] = conditions
        condition_count += bool(conditions)
        if index.text(record) != index.text(before["candidates"][cid]):
            raise ValueError("condition extraction changed positive text: " + cid)
    for binding in source["slot_bindings"].values():
        if binding.pop("effects") != source["candidates"][binding["candidate_id"]]["effects"]:
            raise ValueError("binding has independently authored effects")
        binding["conditions"].pop("guard_role")
        binding["semantic_role"] = source["slot_catalog"][binding["slot_id"]]["semantic_role"]
    write_source(source)
    report = {"verified": True, "corpus_before_sha256": c.digest(before), "corpus_after_sha256": c.digest(source),
        "candidate_count": len(source["candidates"]), "binding_count": len(source["slot_bindings"]),
        "slot_count": len(source["slot_catalog"]), "candidates_with_intrinsic_conditions": condition_count,
        "adult_context_condition_ids": sorted(adult_context_ids), "duplicate_effect_payloads_removed": len(source["slot_bindings"]),
        "candidate_ids_preserved": set(source["candidates"]) == set(before["candidates"]),
        "all_positive_texts_preserved": True, "source_binding_subject_policies_preserved": True,
        "source_conditions_and_role_policies_are_distinct": True,
        "taxonomy_ids_not_yet_migrated": True}
    (OUT / "STAGE02-SOURCE-VERIFICATION.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))

if __name__ == "__main__":
    upgrade()
