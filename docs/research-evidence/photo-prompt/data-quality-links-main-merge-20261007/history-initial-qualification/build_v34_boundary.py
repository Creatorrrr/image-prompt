"""Author V34 from upstream V33 while retaining independent local V33 evidence."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
ASSETS = ROOT / "skills/subculture-illustration-image-generator/assets"
PHOTO = "skills/photo-prompt-image-generator/assets/"
ILLUSTRATION = "skills/subculture-illustration-image-generator/"


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def delta(before, after, pointer=""):
    if isinstance(before, dict) and isinstance(after, dict):
        rows = []
        for key in sorted(set(before) | set(after)):
            child = pointer + "/" + key.replace("~", "~0").replace("/", "~1")
            if key not in before:
                rows.append(dict(operation="add", pointer=child, after=after[key]))
            elif key not in after:
                raise AssertionError("Deletion is not authorized")
            else:
                rows.extend(delta(before[key], after[key], child))
        return rows
    if isinstance(before, list) and isinstance(after, list) and len(before) == len(after):
        return [row for i, (old, new) in enumerate(zip(before, after))
                for row in delta(old, new, pointer + "/" + str(i))]
    return [] if before == after else [dict(operation="replace", pointer=pointer,
                                           before=before, after=after)]


def entries(manifest, asset_root):
    merged = {}
    for row in manifest["shards"]:
        payload = asset_root / row["path"]
        if sha(payload) != row["sha256"]:
            raise AssertionError("Index shard checksum drift")
        part = json.loads(payload.read_bytes())["entries"]
        if set(part) & set(merged):
            raise AssertionError("Duplicate index entry")
        merged.update(part)
    if set(merged) != set(manifest["entry_order"]):
        raise AssertionError("Index entry order inventory drift")
    return merged


def main():
    parent_path = HERE / "SOURCE-UPSTREAM-V33.json"
    parent = json.loads(parent_path.read_bytes())
    records = {row["path"]: row for row in parent["members"]}
    old_proof_path = ROOT / "docs/research-evidence/photo-prompt/color-palette-main-merge-20261007/V33-PALETTE-DATA-PROOF.json"
    old_proof = json.loads(old_proof_path.read_bytes())
    old_baseline = json.loads((ASSETS / "photo_regression_baseline_v33.json").read_bytes())
    previous_raw = (ASSETS / "photo_regression_baseline_v33_pack.json").read_bytes()
    current_raw = (HERE / "CURRENT-BOUNDARY-PACK.json").read_bytes()
    previous, current = json.loads(previous_raw), json.loads(current_raw)
    receipt_path = HERE / "CURRENT-BOUNDARY-RECEIPT.json"
    receipt = json.loads(receipt_path.read_bytes())
    data_names = {
        PHOTO + "photo_prompt_visual_obligations.json",
        PHOTO + "photo_prompt_photorealism_elements_extension.json",
        PHOTO + "photo_prompt_realistic_background_extension.json",
    }
    source_delta = {name: delta(json.loads((ROOT / records[name]["source_path"]).read_bytes()),
                                json.loads((ROOT / name).read_bytes())) for name in sorted(data_names)}
    indices = {}
    for name, count in (("photo_prompt_semantic_index.json", 10433),
                        ("photo_prompt_visual_profile_index.json", 2206)):
        row = records[PHOTO + name]
        before = json.loads((ROOT / row["source_path"]).read_bytes())
        after = json.loads((ROOT / PHOTO / name).read_bytes())
        for field in ("provider", "embedding_model", "embedding_dimensions", "semantic_text_recipe"):
            if before[field] != after[field]:
                raise AssertionError("Embedding recipe changed")
        old_entries, new_entries = entries(before, ROOT / PHOTO), entries(after, ROOT / PHOTO)
        if len(old_entries) != count or set(old_entries) != set(new_entries):
            raise AssertionError("Index inventory changed")
        for key, entry in old_entries.items():
            if entry["text"] != new_entries[key]["text"] or entry["vector"] != new_entries[key]["vector"]:
                raise AssertionError(f"Text/vector changed: {key}")
        indices[name] = dict(entry_count=count, exact_text_vector_reuse=count,
                             before_sha256=row["sha256"], after_sha256=sha(ROOT / PHOTO / name),
                             provider=before["provider"], embedding_model=before["embedding_model"],
                             embedding_dimensions=before["embedding_dimensions"],
                             semantic_text_recipe=before["semantic_text_recipe"])
    index_proof_path = HERE / "INDEX-VECTOR-REUSE-PROOF.json"
    index_proof_path.write_bytes(encoded(dict(schema="photo-merged-data-scope-index-reuse/v1", indices=indices,
                                            proof_boundary="All 12639 exact texts and vectors are equal to upstream V33; this comparison does not prove API call counts or image quality.")))
    source_files_after = {name: sha(ROOT / name) for name in old_proof["source_files_after"]}
    active = {}
    for name in ("photo_prompt_semantic_index.json", "photo_prompt_visual_profile_index.json"):
        manifest = json.loads((ROOT / PHOTO / name).read_bytes())
        active.update({PHOTO + row["path"]: row["sha256"] for row in manifest["shards"]})
    proof = dict(
        schema="photo-data-scope-transition/v34",
        previous_qualified_commit=parent["source_pin"], previous_qualified_tree=parent["source_tree"],
        parent_manifest=parent_path.relative_to(ROOT).as_posix(), parent_manifest_sha256=sha(parent_path),
        parent_member_count=parent["member_count"],
        previous_manifest_sha256=sha(ASSETS / "photo_regression_baseline_v33.json"),
        previous_pack_sha256=hashlib.sha256(previous_raw).hexdigest(), previous_pack_id=previous[0]["pack_id"],
        current_pack_sha256=hashlib.sha256(current_raw).hexdigest(), current_pack_id=current[0]["pack_id"],
        previous_validator_sha256=records[ILLUSTRATION + "scripts/validate_illustration_assets.py"]["sha256"],
        previous_universal_descriptor_sha256=records[ILLUSTRATION + "assets/universal_scene_baseline_v2.json"]["sha256"],
        reviewed_pack_delta=delta(previous, current),
        preserved_source_paths=sorted(data_names | {PHOTO + "photo_prompt_semantic_index.json",
                                                   PHOTO + "photo_prompt_visual_profile_index.json"}),
        source_leaf_delta=source_delta, source_files_after=source_files_after,
        upstream_proof=old_proof_path.relative_to(ROOT).as_posix(), upstream_proof_sha256=sha(old_proof_path),
        parallel_local_qualification=dict(source_pin="d9dc3df7012f395c48d536ee9df80df060cd24f9",
            source_manifest=(HERE / "SOURCE-LOCAL-V33.json").relative_to(ROOT).as_posix(),
            source_manifest_sha256=sha(HERE / "SOURCE-LOCAL-V33.json"),
            original_pack_sha256="d6f893dfeecad5968ba80db4e44689c09f99ab16f4b4aa6ae9b88fcc84a6e525",
            original_proof="docs/research-evidence/photo-prompt/data-quality-links-20261007/history/V33-DATA-SCOPE-PROOF.json",
            original_proof_sha256="ece1b90ed71faa5f1f12d29bddf674ffa300cfcd6da1283782c534dbe01fa3d6"),
        source_inventory_after={path.name: sha(path) for path in sorted((ROOT / PHOTO).glob("*.json"))},
        active_shards_after=active, retained_shards_before=old_proof["active_shards_after"],
        frozen_inputs=old_baseline["frozen_inputs"],
        evidence_files={p.relative_to(ROOT).as_posix(): sha(p) for p in (
            receipt_path, HERE / "CURRENT-BOUNDARY-PACK.json", index_proof_path,
            HERE / "preserve_merge_sources.py", Path(__file__).resolve())},
        generation_id=receipt["generation_id"], source_fingerprint=receipt["source_fingerprint"],
        receipt_sha256=sha(receipt_path), algorithm_sha256=receipt["algorithm_sha256"],
        proof_boundary="Three authored scope restrictions only. Six added DATA leaves; five reviewed pack leaves include motion candidate_count 34 to 33. Candidate objects/order and all frozen scene inputs are exact. Upstream V1-V33 and parallel local V33 assertions and qualification outcomes remain unchanged. No image-quality or user-acceptance claim.",
    )
    proof_path = HERE / "V34-DATA-SCOPE-PROOF.json"
    proof_path.write_bytes(encoded(proof))
    baseline = dict(old_baseline)
    baseline.update(schema="photo_regression_baseline/v34", created_at="2026-10-07",
        historical_baseline=dict(path="photo_regression_baseline_v33.json", schema="photo_regression_baseline/v33",
                                 sha256=proof["previous_manifest_sha256"]),
        change_scope="Restrict seated cello performance activation and two human-only advisory candidates; preserve upstream V1-V33 and the parallel local original V33 unchanged.",
        sha256=proof["current_pack_sha256"], pack_id=proof["current_pack_id"], purpose=proof["proof_boundary"])
    baseline.pop("palette_data_transition")
    baseline["command"] = list(old_baseline["command"])
    baseline["command"][baseline["command"].index("--output-file") + 1] = "/tmp/subculture-illustration-photo-baseline-v34.json"
    baseline["data_scope_transition"] = dict(evidence_path=proof_path.relative_to(ROOT).as_posix(),
                                            evidence_sha256=sha(proof_path),
                                            previous_qualified_commit=parent["source_pin"],
                                            parent_manifest_sha256=sha(parent_path))
    (ASSETS / "photo_regression_baseline_v34_pack.json").write_bytes(current_raw)
    (ASSETS / "photo_regression_baseline_v34.json").write_bytes(encoded(baseline))
    print("proof_sha256=" + sha(proof_path))
    print(json.dumps(dict(pack_delta=len(proof["reviewed_pack_delta"]),
                          data_delta={name: len(rows) for name, rows in source_delta.items()}, indices=indices)))


if __name__ == "__main__":
    main()
