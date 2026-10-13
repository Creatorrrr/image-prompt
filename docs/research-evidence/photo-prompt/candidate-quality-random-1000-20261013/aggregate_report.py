"""Aggregate explicit semantic judgments and verify the frozen audit evidence.

This script does not decide whether a candidate's meaning is correct. Those
decisions are the individually authored rows in reviews/*.json.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import json
import random
import re
import subprocess
import sys
import unicodedata

R = Path(__file__).resolve().parent
ROOT = R.parents[3]
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import photo_candidate_corpus as corpus
import photo_global_index as index
from photo_runtime_sources import RuntimeSnapshotProvider


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    (R / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def normalized(text):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text).casefold()).strip().rstrip(".")


def primary(record):
    content = record["content"]
    if record["record_kind"] == "visual_option":
        return content.get("en") or content.get("ko") or ""
    if record["record_kind"] == "visual_profile":
        return content.get("semantics", {}).get("definition") or ""
    if record["record_kind"] == "visual_bundle":
        units = []
        for component in content.get("components") or []:
            units.extend(component.get("concept_units") or [])
        return "; ".join(dict.fromkeys(units))
    return content.get("definition") or ""


def csv_safe(value):
    value = str(value)
    return "'" + value if value.startswith(("=", "+", "-", "@", "\t", "\r")) else value


manifest = json.loads((R / "SAMPLE-MANIFEST.json").read_text())
samples = [json.loads(line) for line in (R / "samples.jsonl").read_text().splitlines()]
sample_by_number = {row["sample_number"]: row for row in samples}
reviews = [row for path in sorted((R / "reviews").glob("*.json")) for row in json.loads(path.read_text())]
reviews.sort(key=lambda row: row["sample_number"])
assert len(samples) == len(reviews) == 1000
assert len({row["candidate_id"] for row in reviews}) == 1000
assert [row["sample_number"] for row in reviews] == list(range(1, 1001))
assert sha(R / "samples.jsonl") == manifest["samples_sha256"]

live = corpus.load(SKILL / "assets")  # Includes the repository's native structural validator.
assert corpus.digest(live) == manifest["corpus_sha256"]
assert corpus.digest(live["slot_catalog"]) == manifest["catalog_sha256"]
assert json.loads((R / "SLOT-CATALOG.json").read_text()) == live["slot_catalog"]
ids = random.Random(int(manifest["seed_decimal"])).sample(sorted(live["candidates"]), 1000)
assert ids == [row["candidate"]["id"] for row in samples]
assert corpus.digest(ids) == manifest["ordered_sample_ids_sha256"]
source_checks = {name: sha(SKILL / "assets" / name) == expected for name, expected in manifest["source_files_sha256"].items()}
assert all(source_checks.values())
bindings = defaultdict(list)
for row in live["slot_bindings"].values():
    bindings[row["candidate_id"]].append(row)
for sample, review in zip(samples, reviews):
    number = sample["sample_number"]
    record = sample["candidate"]
    assert record == live["candidates"][record["id"]]
    assert corpus.digest(record) == sample["record_sha256"] == review["record_sha256"]
    assert record["id"] == review["candidate_id"] and record["record_kind"] == review["record_kind"]
    assert sorted(bindings[record["id"]], key=lambda row: row["slot_id"]) == sample["bindings"]
    assert review["assigned_slots"] == [row["slot_id"] for row in sample["bindings"]]
    assert (review["slot"] == "unassigned") == (not bool(sample["bindings"]))
    assert all(tag in live["slot_catalog"] for tag in review["suggested_semantic_slots"])
    assert review["reason"] and review["review_method"]
refs = json.loads((R / "REFERENCE-RECORDS.json").read_text())
assert all(live["candidates"][cid] == row for cid, row in refs.items())
snapshot = RuntimeSnapshotProvider().acquire()
assert snapshot.generation_id == manifest["generation_id"]
assert snapshot.manifest["source_fingerprint"] == manifest["source_fingerprint"]
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()
assert head == manifest["head"]

protected = {
    "docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md": "b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359",
    "docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md": "0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b",
}
assert all(sha(ROOT / name) == expected for name, expected in protected.items())
assert not subprocess.check_output(["git", "diff", "--cached", "--name-only"], cwd=ROOT).strip()

# Mechanical comparisons give repeat candidates, not semantic duplicate verdicts.
primary_groups, text_groups, content_groups = defaultdict(list), defaultdict(list), defaultdict(list)
for sample in samples:
    record = sample["candidate"]
    number = sample["sample_number"]
    meaning = normalized(primary(record))
    if len(meaning) >= 20:
        primary_groups[meaning].append(number)
    if record["record_kind"] in index.POSITIVE_KINDS:
        recipe, body = index.text(record)
        text_groups[hashlib.sha256((recipe + "\n" + body).encode()).hexdigest()].append(number)
    content_groups[corpus.digest({"kind": record["record_kind"], "content": record["content"], "effects": record["effects"]})].append(number)


def repeated(groups, include_text=False):
    output = []
    for key, numbers in groups.items():
        if len(numbers) < 2:
            continue
        output.append({
            "sample_numbers": numbers,
            "candidate_ids": [sample_by_number[i]["candidate"]["id"] for i in numbers],
            "record_kinds": [sample_by_number[i]["candidate"]["record_kind"] for i in numbers],
            **({"normalized_primary_meaning": key} if include_text else {"comparison_sha256": key}),
            "interpretation": "Repeat signal only. Different contracts, owners, scopes and provenance must be compared before merging identities.",
        })
    return sorted(output, key=lambda row: row["sample_numbers"])


duplicates = {
    "scope": "Within the frozen random 1000 only; no all-population semantic-dedup claim.",
    "exact_content_and_effects_ignoring_identity_provenance": repeated(content_groups),
    "exact_positive_index_recipe_and_text": repeated(text_groups),
    "normalized_primary_meaning": repeated(primary_groups, True),
}
save("REPETITION-CHECKS.json", duplicates)

flag_counts = Counter(flag for row in reviews for flag in row["flags"])
by_kind = {}
for kind in manifest["sample_kinds"]:
    rows = [row for row in reviews if row["record_kind"] == kind]
    by_kind[kind] = {axis: dict(Counter(row[axis] for row in rows)) for axis in ("meaning", "slot", "translation")}
slot_results = {}
for tag in manifest["sample_slot_counts"]:
    rows = [row for row in reviews if tag in row["assigned_slots"]]
    slot_results[tag] = {"count": len(rows), "verdicts": dict(Counter(row["slot"] for row in rows))}
summary = {
    "audit_date_seoul": "2026-10-13",
    "population": manifest["population"],
    "sample_count": 1000,
    "reviewed_count": len(reviews),
    "unreviewed_count": 0,
    "reviewer": "Codex, individual qualitative semantic reading; no independent human consensus labels",
    "axes": {axis: dict(Counter(row[axis] for row in reviews)) for axis in ("meaning", "slot", "translation")},
    "by_kind": by_kind,
    "slot_binding_denominator": manifest["sample_with_persistent_binding"],
    "catalog_slot_count": len(live["slot_catalog"]),
    "sample_bound_slot_count": len(manifest["sample_slot_counts"]),
    "slot_results": slot_results,
    "flag_counts": dict(flag_counts),
    "confirmed_meaning_inconsistency_samples": [row["sample_number"] for row in reviews if row["meaning"] == "distorted"],
    "weak_meaning_samples": [row["sample_number"] for row in reviews if row["meaning"] == "weak"],
    "uncertain_samples": [row["sample_number"] for row in reviews if row["meaning"] == "uncertain"],
    "wrong_slot_samples": [row["sample_number"] for row in reviews if row["slot"] == "wrong"],
    "human_material_guard_conflict_samples": [row["sample_number"] for row in reviews if "guard_subject_conflict" in row["flags"]],
    "repetition_group_counts": {key: len(value) for key, value in duplicates.items() if isinstance(value, list)},
    "provider_calls": 0,
    "image_calls": 0,
    "limits": [
        "Semantic counts are this reviewer's judgments, not externally labeled accuracy.",
        "Broad related tags and unassigned profile/bundle/mechanism records are not automatically wrong.",
        "KO/EN scope gaps can be deliberate topic-label versus concrete-realization differences; migration corruption is not established.",
        "Guard probes use explicit synthetic contracts and the current policy function, not production retrieval or image tests.",
        "Short meaningful atoms, valid contextual intent and selected visible variants are allowed.",
        "Informational pixel/history/function limits are not automatically counted as data defects.",
        "No diagnostic or relationship_concept records happened to be selected; these rare kinds and all 112 tags are not semantically certified.",
    ],
}
save("RESULTS.json", summary)
(R / "reviews.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in reviews))

columns = ["sample_number", "candidate_id", "record_kind", "ko", "en", "primary_meaning", "assigned_slots", "meaning_verdict", "slot_verdict", "translation_verdict", "flags", "reason", "suggested_existing_roles_advisory", "source_file", "source_record_sha256"]
with (R / "SAMPLE-RESULTS.csv").open("w", encoding="utf-8-sig", newline="") as out:
    writer = csv.DictWriter(out, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    for review in reviews:
        sample = sample_by_number[review["sample_number"]]
        record = sample["candidate"]
        writer.writerow({key: csv_safe(value) for key, value in {
            "sample_number": review["sample_number"], "candidate_id": review["candidate_id"], "record_kind": review["record_kind"],
            "ko": record["content"].get("ko", ""), "en": record["content"].get("en", ""), "primary_meaning": primary(record),
            "assigned_slots": ",".join(review["assigned_slots"]), "meaning_verdict": review["meaning"], "slot_verdict": review["slot"],
            "translation_verdict": review["translation"], "flags": ",".join(review["flags"]), "reason": review["reason"],
            "suggested_existing_roles_advisory": ",".join(review["suggested_semantic_slots"]), "source_file": sample["source_file"],
            "source_record_sha256": review["record_sha256"],
        }.items()})

evidence = {
    "verified_at_utc": datetime.now(timezone.utc).isoformat(),
    "head": head,
    "sample_selection_reproduced": True,
    "all_1000_have_unique_explicit_review_and_matching_id_hash_bindings": True,
    "native_corpus_structural_validation": "pass; not a semantic pass",
    "source_files": source_checks,
    "source_candidate_count": len(live["candidates"]),
    "source_binding_count": len(live["slot_bindings"]),
    "source_corpus_sha256": corpus.digest(live),
    "runtime_generation_unchanged": snapshot.generation_id,
    "runtime_source_fingerprint_unchanged": snapshot.manifest["source_fingerprint"],
    "reference_records_match_live_source": len(refs),
    "protected_preexisting_dirty_documents_unchanged": protected,
    "staged_changes": [],
    "audit_outputs_sha256": {name: sha(R / name) for name in ("samples.jsonl", "reviews.jsonl", "SAMPLE-RESULTS.csv", "RESULTS.json", "REPETITION-CHECKS.json", "GUARD-PROBES.json", "ADJUDICATIONS.json")},
}
save("VERIFICATION.json", evidence)
print(json.dumps({"reviewed": 1000, "axes": summary["axes"], "slot_coverage": summary["sample_bound_slot_count"], "by_kind": by_kind,
    "wrong_slots": summary["wrong_slot_samples"], "guard_conflicts": summary["human_material_guard_conflict_samples"],
    "repeat_groups": summary["repetition_group_counts"], "source_files_verified": len(source_checks), "native_source_bindings": len(live["slot_bindings"]),
    "verification": "passed"}, ensure_ascii=False, indent=2))
