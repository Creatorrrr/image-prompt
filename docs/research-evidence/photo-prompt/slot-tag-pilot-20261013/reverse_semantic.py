"""Role-only offline discovery over all positives, using real query embeddings.

Native request queries are tested separately. The maintenance recipe removes
request/core relevance so a folded blanket cannot dominate every role's cue.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import sys
from sample import HERE, ROOT, SKILL
from ledger import authored, frozen_rows

sys.path[:0] = [str(ROOT), str(SKILL / "scripts")]
import photo_candidate_corpus as c
import photo_global_index as index
import photo_runtime_sources as runtime
from photo_embedding_provider import embed, atomic, load_env, SPACE
from build_shared_candidate_index import offline_vector_map
from tests.photo_slot_oracle import PreparedFullScan


def main():
    load_env(ROOT / ".env")
    source = c.validate(c.load(SKILL / "assets"))
    snapshot = runtime.RuntimeSnapshotProvider(SKILL).acquire()
    vectors = offline_vector_map(snapshot.data.reader, source)
    index.validate(vectors, source)
    oracle = PreparedFullScan(index.lexical(source), vectors["entries"])
    samples = {row["candidate_id"]: row for row in frozen_rows()}
    reviews = authored()
    cache = Path.home() / ".cache/image-prompt/slot-tag-pilot-stage04-role-discovery"
    contexts = {}
    def prepare(slot):
        spec = source["slot_catalog"][slot]
        focus = " ".join([spec["description"], spec["description_ko"], *spec["includes"], *spec["evidence_terms"]])
        text = "Find visual candidates whose complete authored meaning expresses this role on its declared owner: " + focus
        binding = {"recipe": "photo-maintenance-role-discovery/v1", "slot_id": slot, "slot_spec_sha256": c.digest(spec)}
        result = embed(text, binding, cache)
        return slot, {"recipe": binding["recipe"], "text": text, "text_sha256": hashlib.sha256(text.encode()).hexdigest(),
            "fields": {"slot_focus": focus}, "binding": binding, "space": SPACE, "vector": result["vector"],
            "execution": result["execution"], "cache_hit": result["cache_hit"]}
    with ThreadPoolExecutor(max_workers=4) as pool:
        for slot, row in pool.map(prepare, sorted(source["slot_catalog"])):
            contexts[slot] = row
    atomic(HERE / "ROLE-DISCOVERY-CONTEXTS.json", contexts)
    print("prepared", len(contexts), "real, role-only maintenance queries", flush=True)
    results, questions = {}, []
    for count, (slot, context) in enumerate(contexts.items(), 1):
        assert context["binding"]["slot_spec_sha256"] == c.digest(source["slot_catalog"][slot])
        ranked = oracle.rank(context["fields"], context["vector"], set(vectors["entries"]), limit=384)
        ranks = {lane: {row["document_id"]: number for number, row in enumerate(ranked[lane], 1)}
            for lane in ("bm25f", "embedding", "rrf")}
        hits = [{"number": samples[cid]["number"], "candidate_id": cid,
            "approved_for_role": slot in reviews[samples[cid]["number"]]["approved"],
            **{lane + "_rank": ranks[lane].get(cid) for lane in ranks}}
            for cid in samples if any(cid in lane for lane in ranks.values())]
        hits.sort(key=lambda row: (row["rrf_rank"] or 9999, row["number"]))
        results[slot] = {"pool": "offline_all_positive_without_request_guards", "pool_count": len(vectors["entries"]),
            "full_positive_pool_scored": True, "lane_limit": 384, "pilot_hits": hits,
            "top20": {lane: ranked[lane][:20] for lane in ranked}}
        for hit in hits:
            if not hit["approved_for_role"] and reviews[hit["number"]]["approved"]:
                questions.append({"slot": slot, **hit})
                break
        if count % 25 == 0:
            print("reverse discovery", count, "/", len(contexts), flush=True)
    assert c.digest(c.load(SKILL / "assets")) == c.digest(source)
    atomic(HERE / "ROLE-REVERSE-DISCOVERY.json", results)
    atomic(HERE / "ROLE-REVERSE-QUESTIONS.json", questions)
    atomic(HERE / "ROLE-REVERSE-VERIFICATION.json", {"verified": True, "source_sha256": c.digest(source),
        "generation_id": snapshot.generation_id, "recipe": "photo-maintenance-role-discovery/v1", "query_count": len(contexts),
        "positive_pool_count": len(vectors["entries"]), "diagnostic_excluded": 64,
        "provider_calls": sum(not row["cache_hit"] for row in contexts.values()),
        "exact_cache_hits": sum(row["cache_hit"] for row in contexts.values()),
        "candidate_centred_review_count": len(samples), "reverse_rereading_cues": len(questions),
        "boundary": "Offline maintenance discovery, with true provider vectors and whole-pool BM25F/exact cosine/RRF. Rankings never create approval or bypass native request guards."})
    print("completed", len(results), "roles and", len(questions), "rereading cues", flush=True)


if __name__ == "__main__":
    main()
