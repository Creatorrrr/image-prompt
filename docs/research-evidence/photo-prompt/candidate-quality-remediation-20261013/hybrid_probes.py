"""Actual-query, full-pool BM25F/cosine probes; retain both lanes and oracle ranks.

These are maintenance queries authored from the corrected meanings, not
production requests, independent expert labels or image-quality measurements.
"""
import hashlib
import json
import sys
from contextlib import closing
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "skills/photo-prompt-image-generator/scripts"))
import photo_candidate_corpus as corpus
import photo_global_index as index
import photo_sharded_search as search
from photo_search_reader import SearchReader
from photo_embedding_provider import embed, load_env, atomic
from build_shared_candidate_index import offline_vector_map
from bm25f_retrieval import rank_bm25f, reciprocal_rank_fusion


PROBES = [
    (83, "garment_detail", "aligned hook-and-eye closure rows on both sides of a bra back-band opening"),
    (123, "composition", "a nearly edge-on black-hole accretion disk with bent far-side arcs and approaching-side brightness"),
    (154, "subject", "an experienced adult fabricator working alongside an adult coworker"),
    (278, "composition", "one Cambodian Ardhanarishvara body with Shiva's mustache and third eye and Parvati's hairstyle and long skirt"),
    (503, "prop", "a flexible electroluminescent EL wire following a continuous curve into a supply enclosure"),
    (642, "body_marking", "roses painted directly on the skin of a bare leg"),
    (643, "light_shape", "an adult with both hands down whose connected cast shadow raises one hand"),
    (135, "camera_height", "worm's-eye view from a camera placed close to the ground looking upward"),
    (132, "lens_artifact", "blue-white defocused background light discs behind a sharper portrait subject"),
    (396, "light_shape", "patches of dappled sunlight filtered through leaves"),
    (428, "atmosphere", "hanging flexible fabric elements with settled vertical contours and no sideways wind deflection"),
    (451, "mood", "desaturated nineteen-nineties grunge editorial mood"),
    (546, "reflection_logic", "the real hand is lowered while the same mirror image keeps its hand raised at chest height"),
    (995, "capture_context", "macro product photography showing material grain stitch spacing edge finishing and metal surface contrast"),
    (1, "prop", "발광 스틱 소품"),
    (115, "garment_detail", "좁은 소매와 읽을 수 있는 앞여밈을 가진 겉로브"),
]


def main():
    assets = ROOT / "skills/photo-prompt-image-generator/assets"
    source = corpus.load(assets)
    fixes = corpus.decode((HERE / "FIXES.json").read_bytes())
    assert corpus.digest(source) == fixes["after_corpus_sha256"]
    source_sha256 = fixes["after_corpus_sha256"]
    previous_path = HERE / "HYBRID-PROBES.json"
    previous = corpus.decode(previous_path.read_bytes()) if previous_path.exists() else {}
    embedding_source = previous.get("query_embedding_origin_corpus_sha256", previous.get("corpus_sha256", source_sha256))
    samples = {row["sample_number"]: row for row in map(json.loads,
        (HERE.parent / "candidate-quality-random-1000-20261013/samples.jsonl").read_text().splitlines())}
    cache = Path.home() / ".cache/image-prompt/quality-remediation-20261013/probes"
    load_env(ROOT / ".env")

    def query(row):
        number, slot, text = row
        return embed(text, {"evaluation": "candidate-quality-remediation-20261013", "slot": slot,
            "text_recipe": "authored-quality-boundary-query/v1", "corpus_sha256": embedding_source}, cache)

    with ThreadPoolExecutor(max_workers=4) as pool:
        contexts = list(pool.map(query, PROBES))
    lexical = index.lexical(source)
    rows = []
    with closing(SearchReader(assets)) as reader:
        vectors = offline_vector_map(reader, source)
        index.validate(vectors, source)
        allowed = set(vectors["entries"])
        for (number, slot, text), context in zip(PROBES, contexts):
            fields = {"slot_focus": text}
            lexical_hits = search.lexical_rank(reader, fields, allowed, 64)
            cosine_hits, proof = search.cosine_rank(reader, context["vector"], allowed, 64)
            oracle_l = rank_bm25f(lexical, fields, allowed_ids=allowed, limit=64)
            oracle_e = index.cosine_rank(vectors, context["vector"], allowed, 64)
            assert lexical_hits == oracle_l, (number, "lexical oracle")
            assert cosine_hits == oracle_e, (number, "cosine oracle")
            assert search.audit_cosine(reader, context["vector"], allowed, cosine_hits, proof)
            fused = reciprocal_rank_fusion([[r["document_id"] for r in lexical_hits], [r["document_id"] for r in cosine_hits]], k=30)
            target = samples[number]["candidate"]["id"]
            def rank(hits):
                return next((pos for pos, row in enumerate(hits, 1) if row["document_id"] == target), None)
            rows.append({"sample_number": number, "slot": slot, "query": text, "target_candidate_id": target,
                "corpus_scope": "all_shared_positive_records_without_tag_partition", "positive_records": len(allowed),
                "query_vector_sha256": context["vector_sha256"], "query_execution": context["execution"],
                "query_cache_hit": context["cache_hit"], "lexical_rank": rank(lexical_hits), "cosine_rank": rank(cosine_hits),
                "rrf_rank": rank(fused), "lexical": lexical_hits, "cosine": cosine_hits, "rrf": fused,
                "full_scan_oracle_equal": True, "cosine_skip_certificate_verified": True,
                "vector_leaves_read": len(proof["visited_leaves"]), "vector_leaves_total": len(reader.meta["vector_shards"])})
        reader_metrics = dict(reader.metrics)
    report = {"schema": "photo-candidate-quality-hybrid-probes/v1", "corpus_sha256": source_sha256,
        "query_count": len(rows), "provider_calls": sum(not c["cache_hit"] for c in contexts),
        "query_embedding_origin_corpus_sha256": embedding_source,
        "query_vectors_reused_with_exact_text_slot_recipe_and_space": sum(c["cache_hit"] for c in contexts),
        "target_in_rrf_top_20": sum(row["rrf_rank"] is not None and row["rrf_rank"] <= 20 for row in rows),
        "target_in_rrf_top_64": sum(row["rrf_rank"] is not None and row["rrf_rank"] <= 64 for row in rows),
        "reader_metrics": reader_metrics, "probes": rows,
        "boundary": "Authored maintenance queries; ranking does not establish semantic correctness, production precision or pixel quality."}
    atomic(HERE / "HYBRID-PROBES.json", report)
    print(json.dumps({key: value for key, value in report.items() if key not in {"probes", "reader_metrics"}}, ensure_ascii=False))
    for row in rows:
        print(row["sample_number"], "BM25F", row["lexical_rank"], "cosine", row["cosine_rank"], "RRF", row["rrf_rank"])


if __name__ == "__main__":
    main()
