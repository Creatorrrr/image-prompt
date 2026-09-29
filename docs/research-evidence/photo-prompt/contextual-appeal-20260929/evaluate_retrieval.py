#!/usr/bin/env python3
"""Run the returned queries as lexical discoverability probes, not meaning evals.

The external reports include interpretation, lock, temporal and image duties.
Those duties cannot be scored by retrieval hits and remain unexecuted here.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "skills/photo-prompt-image-generator/scripts"))
import prompt_generator as generator
from bm25f_retrieval import rank_bm25f


def main():
    ledger = json.loads((HERE / "integration-ledger.json").read_text())
    mappings = {(row["origin"], row["research_id"]): row["runtime_ids"] for row in ledger["records"]}
    data = generator.load_json(ROOT / "skills/photo-prompt-image-generator/assets/photo_prompt_tags.json")
    corpus = generator.build_semantic_bm25f_payload(data)
    result = []
    sources = [("academic", "academic/retrieval-evaluation-cases.json"),
               ("community", "community/community-retrieval-cases.json")]
    for origin, relative in sources:
        cases = json.loads((HERE / "research" / relative).read_text())["cases"]
        for case in cases:
            query = case.get("query") or {"ko": case.get("query_ko"), "en": case.get("query_en")}
            if isinstance(query, str):
                query = {"original": query}
            references = case.get("relevant_research_ids", case.get("related_candidate_research_ids", []))
            expected = sorted({eid for rid in references for eid in mappings.get((origin, rid), [])})
            record = {"origin": origin, "case_id": case["case_id"], "research_ids": references,
                      "mapped_runtime_ids": expected, "languages": {},
                      "nonretrieval_expected_behavior": "not_scored_by_this_probe"}
            for language, text in query.items():
                if not text:
                    continue
                hits = rank_bm25f(corpus, {"global_context": text}, limit=20)
                ids = [row["document_id"].split(":")[-1] for row in hits]
                found = sorted(set(ids) & set(expected))
                record["languages"][language] = {"query": text, "top20_document_ids": [row["document_id"] for row in hits],
                                                  "matched_runtime_ids": found,
                                                  "status": "hit" if found else "miss" if expected else "no_runtime_target"}
            result.append(record)
    language_rows = [row for case in result for row in case["languages"].values()]
    report = {"schema_version": "photo-research-lexical-probes/v1", "mode": "BM25F only; no embedding API and no composer",
              "dictionary_sha256": generator.dictionary_hash(data), "case_count": len(result),
              "query_count": len(language_rows), "hit_queries": sum(row["status"] == "hit" for row in language_rows),
              "miss_queries": sum(row["status"] == "miss" for row in language_rows),
              "no_runtime_target_queries": sum(row["status"] == "no_runtime_target" for row in language_rows),
              "limitations": ["This checks proposed records' top-20 lexical discoverability only.",
                              "Not a pass rate for the reports' full expected behaviors, hybrid production packs or images.",
                              "Queries and records were authored together by external researchers; this is not an independent holdout."],
              "cases": result}
    (HERE / "lexical-retrieval-results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: value for key, value in report.items() if key != "cases"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
