"""Compile authored decisions with source, evidence and application boundaries.

Keyword tests and native fit never create a semantic approval in this ledger.
The only approvals are the individually authored TSVs and adjudications.
"""
import collections
import csv
import hashlib
import json
import sys
from sample import HERE, ROOT, SKILL, refs

sys.path.insert(0, str(SKILL / "scripts"))
import photo_candidate_corpus as c
import photo_global_index as index
import photo_slot_semantics as semantics


def frozen_rows():
    return [json.loads(line) for name in ("SAMPLE.jsonl", "SUPPLEMENT.jsonl")
        for line in (HERE / name).read_text().splitlines()]


def authored():
    result = {}
    for path in sorted(HERE.glob("REVIEWS-*.tsv")):
        for line, row in enumerate(csv.DictReader(path.open(), delimiter="\t"), 2):
            assert set(row) == {"number", "approved_slots", "rejected_slots", "rationale_ko"} and None not in row
            number = int(row["number"])
            assert number not in result and row["rationale_ko"].strip()
            approved = row["approved_slots"].split(",") if row["approved_slots"] else []
            rejected = row["rejected_slots"].split(",") if row["rejected_slots"] else []
            assert len(approved) == len(set(approved)) and not set(approved) & set(rejected)
            result[number] = {"approved": approved, "rejected": rejected, "rationale_ko": row["rationale_ko"],
                "source": {"file": str(path.relative_to(ROOT)), "line": line}, "adjudications": []}
    for change in c.decode((HERE / "ADJUDICATIONS.json").read_bytes())["changes"]:
        row = result[change["number"]]
        assert set(change["remove"]) <= set(row["approved"])
        for tag in change["remove"]:
            row["approved"].remove(tag)
            if tag not in row["rejected"]:
                row["rejected"].append(tag)
        for tag in change["add"]:
            assert tag not in row["approved"]
            row["approved"].append(tag)
            if tag in row["rejected"]:
                row["rejected"].remove(tag)
        row["adjudications"].append(change)
    return result


def positive_fragments(record):
    # Each field and exact excerpt is frozen independently of any proposed tag.
    # Field projection has a derivation reference; full native pointers and all
    # guards/negative boundaries remain in the frozen source record.
    return [{"field": field, "value": text, "sha256": hashlib.sha256(text.encode()).hexdigest(),
        "derivation": "photo_global_index.fields(record)/" + field}
        for field, texts in index.fields(record).items() for text in texts]


def build():
    source = c.validate(c.load(SKILL / "assets"))
    samples = frozen_rows()
    reviews = authored()
    assert len(samples) == 609 and len({r["candidate_id"] for r in samples}) == len(samples)
    assert set(reviews) == {r["number"] for r in samples}
    corrections = {r["candidate_id"]: r for r in c.decode((HERE / "CORRECTION-PROPOSALS.json").read_bytes())["changes"]}
    catalog = source["slot_catalog"]
    rows = []
    for sample in samples:
        number, cid = sample["number"], sample["candidate_id"]
        record = source["candidates"][cid]
        review = reviews[number]
        assert sample["record"] == record and c.digest(record) == sample["record_sha256"]
        assert set(review["approved"] + review["rejected"]) <= set(catalog)
        correction = corrections.get(cid)
        reviewed = correction["after"] if correction else record
        assert (reviewed["record_kind"] == "diagnostic") == (not review["approved"])
        original = {b["slot_id"]: b for b in sample["source_bindings"]}
        approved = set(review["approved"])
        positive = " ".join(text for texts in index.fields(record).values() for text in texts)
        pairs = []
        for slot in sorted(set(original) | approved | set(review["rejected"])):
            decision = ("retain" if slot in original else "add") if slot in approved else ("remove" if slot in original else "reject")
            native_fit = semantics.fit(catalog[slot], record, positive)
            pairs.append({"slot_id": slot, "decision": decision, "semantic_role": catalog[slot]["semantic_role"],
                "review_rationale_ko": review["rationale_ko"], "source_binding": original.get(slot),
                "source_intrinsic_conditions": record["conditions"],
                "role_conditions": original[slot]["conditions"] if slot in original else None,
                "reviewed_record_sha256": c.digest(reviewed),
                "support_scope": "whole_authored_record_preserving_original_alternatives_prerequisites_and_owners",
                "native_owned_fit_diagnostic": native_fit,
                "before_stage06_application": ("stage05_correction_and_effect_branch_validation" if correction else
                    "stage05_owned_effect_and_role_condition_refinement" if native_fit["status"] != "eligible" and slot in approved else
                    "stage05_full_review_then_stage06_application"),
                "native_binding_written": False})
        rows.append({"schema": "photo-slot-tag-pilot-review/v1", "number": number, "candidate_id": cid,
            "reviewer": "Codex", "semantic_review": "completed", "independent_human_review": False,
            "record_kind_before": record["record_kind"], "record_kind_reviewed": reviewed["record_kind"],
            "source_record_sha256": c.digest(record), "source_meaning_sha256": sample["meaning_sha256"],
            "reviewed_record_sha256": c.digest(reviewed), "reviewed_meaning_sha256": c.digest({
                key: reviewed[key] for key in ("content", "conditions", "effects")}),
            "payload_owner": sample["payload_owner"], "evidence_file": "SAMPLE.jsonl" if number <= 600 else "SUPPLEMENT.jsonl",
            "positive_source_fragments": positive_fragments(reviewed) if reviewed["record_kind"] != "diagnostic" else [],
            "intrinsic_conditions": record["conditions"], "canonical_effects": record["effects"],
            "provenance": record["provenance"], "reference_ids": sample["reference_ids"],
            "existing_slots": sorted(original), "approved_slots": sorted(approved),
            "retain": sorted(approved & set(original)), "add": sorted(approved - set(original)),
            "remove": sorted(set(original) - approved), "explicit_negative_slots": sorted(review["rejected"]),
            "rationale_ko": review["rationale_ko"], "authored_decision": review["source"],
            "adjudications": review["adjudications"], "role_decisions": pairs,
            "correction_proposal": correction["after_record_sha256"] if correction else None,
            "proposal_only": True})
    return source, rows


def main():
    source, rows = build()
    target = HERE / "REVIEWS.jsonl"
    target.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
    with (HERE / "REVIEW-TABLE.tsv").open("w") as out:
        writer = csv.writer(out, delimiter="\t", lineterminator="\n")
        writer.writerow(["number", "candidate_id", "kind", "existing", "approved", "retain", "add", "remove", "rationale_ko"])
        for row in rows:
            writer.writerow([row["number"], row["candidate_id"], row["record_kind_reviewed"],
                *[",".join(row[key]) for key in ("existing_slots", "approved_slots", "retain", "add", "remove")], row["rationale_ko"]])
    approved_counts = collections.Counter(s for row in rows for s in row["approved_slots"])
    stats = {"schema": "photo-slot-tag-pilot-ledger-summary/v1", "source_sha256": c.digest(source),
        "reviewed_count": len(rows), "sample_files_sha256": {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
            for name in ("SAMPLE.jsonl", "SUPPLEMENT.jsonl")}, "ledger_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "kind_before": dict(collections.Counter(row["record_kind_before"] for row in rows)),
        "kind_reviewed": dict(collections.Counter(row["record_kind_reviewed"] for row in rows)),
        "relationship_decisions": {key: sum(len(row[key]) for row in rows) for key in ("retain", "add", "remove")},
        "approved_role_counts": dict(sorted(approved_counts.items())), "approved_roles": len(approved_counts),
        "zero_approved_roles": sorted(set(source["slot_catalog"]) - set(approved_counts)),
        "native_fit_for_approved_pairs": dict(collections.Counter(pair["native_owned_fit_diagnostic"]["status"]
            for row in rows for pair in row["role_decisions"] if pair["decision"] in {"retain", "add"})),
        "tag_cardinality": dict(sorted(collections.Counter(len(row["approved_slots"]) for row in rows).items())),
        "native_candidate_count": len(source["candidates"]), "native_positive_count": len(index.documents(source)),
        "native_binding_count": len(source["slot_bindings"]), "native_tag_writes": 0,
        "sampling_boundary": "Purposeful regression/role coverage plus stratified random fill; not prevalence or independent expert accuracy."}
    (HERE / "LEDGER-SUMMARY.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: stats[key] for key in ("reviewed_count", "relationship_decisions", "approved_roles", "zero_approved_roles", "native_fit_for_approved_pairs", "native_tag_writes")}))


if __name__ == "__main__":
    main()
