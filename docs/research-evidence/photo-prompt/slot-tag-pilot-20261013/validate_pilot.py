"""Audit the authored pilot against live sources and the pinned baseline."""
from collections import Counter
import hashlib
import json
import sys
from sample import HERE, ROOT, SKILL, refs
from ledger import build, frozen_rows

sys.path.insert(0, str(SKILL / "scripts"))
import photo_candidate_corpus as c
import photo_global_index as index
import photo_runtime_sources as runtime


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source, expected = build()
    written = [json.loads(line) for line in (HERE / "REVIEWS.jsonl").read_text().splitlines()]
    assert written == expected
    baseline = c.decode((HERE / "BASELINE.json").read_bytes())
    native_catalog = source["slot_catalog"]
    frozen_catalog = c.decode((HERE / "CATALOG.json").read_bytes())
    changes = c.decode((HERE / "CATALOG-CHANGES.json").read_bytes())
    assert changes["before_corpus_sha256"] == baseline["corpus_sha256"]
    assert changes["after_corpus_sha256"] == c.digest(source)
    assert set(native_catalog) - set(frozen_catalog) == {"gaze_direction", "nail_appearance", "body_form"}
    assert all(native_catalog[tag] == row for tag, row in frozen_catalog.items() if tag != "skin_tone")
    assert {row["slot_id"] for row in changes["changes"]} == {"gaze_direction", "nail_appearance", "body_form", "skin_tone"}
    for change in changes["changes"]:
        assert native_catalog[change["slot_id"]] == change["after"]
    preserved_modules = []
    for name, before in baseline["module_sha256"].items():
        if name == "photo_candidate_slot_catalog.json":
            continue
        assert sha(SKILL / "assets" / name) == before, name
        preserved_modules.append(name)
    assert sha(SKILL / "assets" / c.MANIFEST_NAME) == baseline["manifest_sha256"]
    protected = {name: sha(ROOT / name) for name in baseline["protected_dirty_files"]}
    assert protected == baseline["protected_dirty_files"]
    assert len(source["candidates"]) == 18250 and len(source["slot_bindings"]) == baseline["binding_count"] == 12089
    samples = frozen_rows()
    sampled = {row["candidate_id"]: row for row in samples}
    base_manifest = c.decode((HERE / "SAMPLE-MANIFEST.json").read_bytes())
    assert sha(HERE / "SAMPLE.jsonl") == base_manifest["sample_sha256"]
    original_reviews = [json.loads(line) for line in (ROOT /
        "docs/research-evidence/photo-prompt/candidate-quality-random-1000-20261013/reviews.jsonl").read_text().splitlines()]
    mandatory = [row for row in original_reviews if row["slot"] in {"wrong", "broad"}]
    assert Counter(row["slot"] for row in mandatory) == {"wrong": 9, "broad": 30}
    assert {row["candidate_id"] for row in mandatory} <= set(sampled)
    for sample in samples:
        record = source["candidates"][sample["candidate_id"]]
        assert c.digest(record) == sample["record_sha256"]
        assert sample["meaning_sha256"] == c.digest({key: record[key] for key in ("content", "conditions", "effects")})
        assert sorted(set(refs(record["content"]))) == sample["reference_ids"]
        assert all(source["slot_bindings"][b["id"]] == b for b in sample["source_bindings"])
        owned = c.decode((SKILL / "assets" / sample["payload_owner"]).read_bytes())["candidates"]
        assert owned[sample["candidate_id"]] == record
    assert set().union(*(set(row["approved_slots"]) for row in written)) == set(native_catalog)
    source_diagnostic = {cid for cid, row in source["candidates"].items() if row["record_kind"] == "diagnostic"}
    assert len(source_diagnostic) == 64 and source_diagnostic <= set(sampled)
    assert all(not row["approved_slots"] for row in written if row["candidate_id"] in source_diagnostic)
    proposals = c.decode((HERE / "CORRECTION-PROPOSALS.json").read_bytes())
    assert proposals["source_sha256"] == c.digest(source) and not proposals["native_sources_written"]
    projected = {**source, "candidates": dict(source["candidates"])}
    for change in proposals["changes"]:
        cid = change["candidate_id"]
        assert c.digest(source["candidates"][cid]) == change["before_record_sha256"]
        assert c.digest(change["after"]) == change["after_record_sha256"]
        for key in ("id", "conditions", "effects", "provenance"):
            assert change["before"][key] == change["after"][key]
        assert change["before"] == source["candidates"][cid]
        projected["candidates"][cid] = change["after"]
    c.validate(projected)
    assert c.digest(projected) == proposals["projected_corpus_sha256"]
    assert len(index.documents(projected)) == 18180 and len(index.documents(source)) == 18186
    snapshot = runtime.RuntimeSnapshotProvider(SKILL).acquire()
    publication = c.decode((HERE / "INDEX-PUBLICATION.json").read_bytes())
    assert snapshot.generation_id == publication["publication"]["generation_id"]
    assert snapshot.data.reader.meta["corpus_sha256"] == c.digest(source)
    assert publication["verification"]["verified"] and publication["vector_reuse"] == 18186 and publication["provider_calls"] == 0
    report = {"schema": "photo-slot-tag-pilot-integrity-verification/v1", "verified": True,
        "source_sha256": c.digest(source), "generation_id": snapshot.generation_id,
        "records_reviewed": len(written), "all_authored_decisions_match_ledger": True,
        "all_source_hashes_owners_references_and_conditions_verified": True,
        "mandatory_broad_wrong": dict(Counter(row["slot"] for row in mandatory)), "catalog_roles_covered": len(native_catalog),
        "native_diagnostics_reviewed_and_excluded": 64, "diagnostic_reclassifications_proposed": 6,
        "correction_proposals_shape_and_references_verified": len(proposals["changes"]),
        "native_semantic_correction_writes": 0, "native_tag_writes": 0,
        "preserved_source_modules": preserved_modules, "protected_dirty_file_sha256": protected,
        "native_binding_count": len(source["slot_bindings"]), "native_candidate_count": len(source["candidates"]),
        "native_positive_count": len(index.documents(source)), "reviewed_record_count_by_kind": dict(Counter(row["record_kind_before"] for row in written)),
        "boundary": "Source/reference/evidence integrity and native publication; not independent expert semantic accuracy or pixel quality."}
    (HERE / "INTEGRITY-VERIFICATION.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ("verified", "records_reviewed", "catalog_roles_covered", "native_tag_writes", "native_candidate_count")}))


if __name__ == "__main__":
    main()
