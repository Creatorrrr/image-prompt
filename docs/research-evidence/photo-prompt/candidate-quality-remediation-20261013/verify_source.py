"""Verify exact reviewed changes and guard regressions, without provider calls."""
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "skills/photo-prompt-image-generator/scripts"))
import photo_candidate_corpus as corpus
import photo_global_index as index
from photo_candidate_context import primary_context_alternatives
from photo_candidate_semantics import validate_relations
from photo_global_retrieval import guard_policy
from photo_embedding_provider import atomic


def main():
    assets = ROOT / "skills/photo-prompt-image-generator/assets"
    source = corpus.load(assets)
    fixes = corpus.decode((HERE / "FIXES.json").read_bytes())
    baseline = corpus.decode((HERE / "SOURCE-BEFORE.json").read_bytes())
    assert corpus.digest(source) == fixes["after_corpus_sha256"]
    assert len(source["candidates"]) == fixes["summary"]["candidates"]
    assert len(source["slot_bindings"]) == fixes["summary"]["bindings"]
    for cid, row in fixes["candidates"].items():
        assert source["candidates"][cid] == row["after"]
        assert row["before"]["id"] == row["after"]["id"] == cid
        assert row["before"]["record_kind"] == row["after"]["record_kind"]
        assert row["after"]["provenance"][:-1] == row["before"]["provenance"]
        before = row["before"]["content"]
        after = row["after"]["content"]
        # The reviewed garment bundle repair changes visible components, never
        # silently removes a member, profile or additional member requirement.
        for key in ("member_candidates", "associated_profile_ids"):
            if key in before:
                assert before[key] == after[key]
    for bid, row in fixes["bindings"].items():
        assert source["slot_bindings"][bid] == row["after"]
        assert row["before"]["candidate_id"] == row["after"]["candidate_id"]
        assert row["before"]["role"] == row["after"]["role"]
        assert row["before"]["weight"] == row["after"]["weight"]
    for cid, row in source["candidates"].items():
        content = row["content"]
        primary_context_alternatives(content.get("primary_context_alternatives"))
        if "relations" in content:
            validate_relations(content["relations"], cid)
    probes = []
    for row in fixes["material_cohort"]:
        before = fixes["bindings"][row["binding_id"]]["before"]["conditions"]["subject_applicability"]
        after = source["slot_bindings"][row["binding_id"]]["conditions"]["subject_applicability"]
        for category in row["added_subject_categories"]:
            contract = {"subject_category": category, "domains": ["fashion" if category == "human" else "wildlife"]}
            a, b = guard_policy(before, contract), guard_policy(after, contract)
            assert (a, b) == (False, True), (row, contract, a, b)
            probes.append({**row, "contract": contract, "before": a, "after": b})
    protected = {relative: hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == sha
        for relative, sha in baseline["protected_dirty_files"].items()}
    assert all(protected.values())
    changed_texts = [cid for cid, row in fixes["candidates"].items()
        if index.text(row["before"]) != index.text(row["after"])]
    assert len(changed_texts) == fixes["summary"]["changed_search_texts"]
    samples = list(map(json.loads, (HERE.parent / "candidate-quality-random-1000-20261013/samples.jsonl").read_text().splitlines()))
    unchanged = sum(corpus.digest(source["candidates"][row["candidate"]["id"]]) == row["record_sha256"] for row in samples)
    by_candidate = defaultdict(set)
    for binding in source["slot_bindings"].values():
        by_candidate[binding["candidate_id"]].add(binding["slot_id"])
    bindings = Counter(len(by_candidate[cid]) for cid, r in source["candidates"].items() if r["record_kind"] == "visual_option")
    report = {"schema": "photo-candidate-quality-verification/v1", "verified": True,
        "before_corpus_sha256": fixes["before_corpus_sha256"], "after_corpus_sha256": fixes["after_corpus_sha256"],
        "summary": fixes["summary"], "record_kinds": dict(Counter(r["record_kind"] for r in source["candidates"].values())),
        "material_guard_probes": probes, "changed_search_text_ids": changed_texts,
        "audited_samples_with_unchanged_payload": unchanged, "visual_option_slot_counts": dict(bindings),
        "protected_dirty_files_unchanged": protected, "member_and_profile_references_preserved": True,
        "native_ids_and_binding_ids_preserved": True, "semantic_judgment": "Authored fixes with explicit reasons; structural tests alone do not certify semantic accuracy."}
    atomic(HERE / "SOURCE-VERIFICATION.json", report)
    print(json.dumps({key: value for key, value in report.items() if key not in {"material_guard_probes", "changed_search_text_ids"}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
