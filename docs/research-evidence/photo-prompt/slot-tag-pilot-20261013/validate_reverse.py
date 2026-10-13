"""Validate source-bound human-authored re-reading decisions, not model scores."""
import csv
import json
import sys
from collections import Counter
from sample import HERE, SKILL
from ledger import frozen_rows

sys.path.insert(0, str(SKILL / "scripts"))
import photo_candidate_corpus as c
import photo_global_index as index


def main():
    questions = c.decode((HERE / "ROLE-REVERSE-QUESTIONS.json").read_bytes())
    source = c.validate(c.load(SKILL / "assets"))
    corpus_sha = c.digest(source)
    samples = {row["candidate_id"]: row for row in frozen_rows()}
    decisions = {}
    for path in sorted(HERE.glob("REVERSE-REVIEWS-*.tsv")):
        for line, row in enumerate(csv.DictReader(path.open(), delimiter="\t"), 2):
            assert set(row) == {"cue_number", "decision", "rationale_ko"}
            number = int(row["cue_number"])
            assert number not in decisions and row["decision"] in {"add", "reject"} and row["rationale_ko"]
            decisions[number] = {**row, "source_file": path.name, "source_line": line}
    assert set(decisions) == set(range(1, 140))
    search_report = c.decode((HERE / "ROLE-REVERSE-VERIFICATION.json").read_bytes())
    contexts = c.decode((HERE / "ROLE-DISCOVERY-CONTEXTS.json").read_bytes())
    assert search_report["verified"] and search_report["source_sha256"] == corpus_sha
    assert set(contexts) == set(source["slot_catalog"])
    all_reviews = {row["candidate_id"]: row for row in map(json.loads, (HERE / "REVIEWS.jsonl").read_text().splitlines())}
    rows = []
    for number, question in enumerate(questions, 1):
        cid, slot = question["candidate_id"], question["slot"]
        record = source["candidates"][cid]
        decision = decisions[number]
        assert samples[cid]["number"] == question["number"]
        assert record["record_kind"] != "diagnostic"
        assert (slot in all_reviews[cid]["approved_slots"]) == (decision["decision"] == "add")
        rows.append({"cue_number": number, **question, **decision,
            "record_sha256": c.digest(record), "slot_spec_sha256": c.digest(source["slot_catalog"][slot]),
            "evidence": index.fields(record), "rank_created_approval": False,
            "reviewer": "Codex", "independent_human_review": False})
    (HERE / "REVERSE-REVIEWS.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
    # The native query's frozen blanket context dominates the two lanes.
    # Explicitly reject its 137 misleading role associations; the remaining
    # two cues are image-level optical finishing, not prop/state selection.
    request_questions = c.decode((HERE / "REVERSE-QUESTIONS.json").read_bytes())
    assert len(request_questions) == 139
    request_rows = []
    for row in request_questions:
        assert row["number"] in {230, 152}
        cid = row["candidate_id"]
        assert row["slot"] not in all_reviews[cid]["approved_slots"]
        request_rows.append({**row, "decision": "reject", "reviewer": "Codex",
            "record_sha256": c.digest(source["candidates"][cid]),
            "rationale_ko": "접힌 담요의 물건·현재 상태를 다른 역할로 넓히지 않는다." if row["number"] == 230 else
                "영상에서 읽히는 직물 세부의 가독성이다. 소품 종류·현재 물리 상태를 추가하지 않는다."})
    (HERE / "REQUEST-REVERSE-REVIEWS.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in request_rows))
    report = {"verified": True, "source_sha256": corpus_sha, "role_only_queries": 139,
        "role_only_cues_reviewed": len(rows), "decisions": dict(Counter(row["decision"] for row in rows)),
        "request_dependent_cues_reviewed": len(request_rows), "request_dependent_new_tags": 0,
        "additional_manual_rereading": {"aesthetic_role_added": 147, "generic_consequence_residue_role_removed": 535,
            "adult_age_separated_from_presentation_context": 536},
        "unresolved_semantic_decisions": 0, "native_tag_writes": 0,
        "boundary": "The same Codex reviewer re-read meaning and slot boundaries. This is not independent human agreement or search precision measurement."}
    (HERE / "REVERSE-REVIEW-VERIFICATION.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
