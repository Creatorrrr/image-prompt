"""Real provider queries and offline full-scan checks for taxonomy maintenance.

Frozen authoring fixtures are inputs, never claims of a production user run.
No image generation or expert semantic precision measurement is performed.
"""
import argparse
from contextlib import closing
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT), str(ROOT / "skills/photo-prompt-image-generator/scripts")]
import photo_candidate_corpus as c
import photo_global_index as index
import photo_global_retrieval as guards
import photo_slot_queries as queries
import photo_slot_retrieval as retrieval
import photo_sharded_search as search
import photo_runtime_sources as runtime
import prompt_generator as g
from photo_embedding_provider import load_env, atomic
from build_shared_candidate_index import offline_vector_map
from tests.photo_slot_oracle import PreparedFullScan
from tests.photo_native_runtime import compose_native
import audit_global_retrieval as audit
import audit_composed_prompt as composed_audit


def frozen(case):
    path = (ROOT / "docs/research-evidence/photo-prompt/shared-candidate-pool-20261012/stage01/inputs/dev-02-blue-cup-en"
            if case == "object" else ROOT / "tests/fixtures/photo_prompt/camera_authoring_path_v1/en_open")
    controls = c.decode((path / "creative-controls.json").read_bytes())
    core = g.load_authorial_core_arg(path / "authorial-core.json",
        request_envelope=g.load_request_envelope_arg(path / "request-envelope.json"),
        creative_control_snapshot=controls)
    return core, controls, c.decode((path / "embodiment-review.json").read_bytes())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["02", "03"], required=True)
    args = parser.parse_args()
    load_env(ROOT / ".env")
    source = c.load(ROOT / "skills/photo-prompt-image-generator/assets")
    provider = runtime.RuntimeSnapshotProvider(ROOT / "skills/photo-prompt-image-generator")
    snapshot = provider.acquire()
    cache = Path.home() / (".cache/image-prompt/slot-taxonomy-stage" + args.stage + "-queries")
    rows, proofs, calls, cache_hits = [], [], 0, 0
    vectors = offline_vector_map(snapshot.data.reader, source)
    index.validate(vectors, source)
    oracle = PreparedFullScan(index.lexical(source), vectors["entries"])
    # Offline oracle materialization is separate from a cold runtime reader.
    from photo_search_reader import SearchReader, LazyRuntimeData
    with closing(SearchReader(snapshot.root / "assets")) as reader:
        initial_metrics = dict(reader.metrics)
        assert reader.metrics["payload_reads"] == reader.metrics["vector_reads"] == reader.metrics["posting_reads"] == 0
        for case, language in ([("object", "en"), ("object", "ko")] if args.stage == "02" else
                               [("object", "en"), ("human", "en"), ("human", "ko")]):
            core, controls, embodiment = frozen(case)
            data = LazyRuntimeData(reader).for_core(core)
            slots = (["lighting", "light_direction", "color", "texture"] if args.stage == "02" else
                     sorted(source["slot_catalog"]) if language == "en" else
                     ["hair_color", "light_direction", "light_shape", "surface_material", "image_artifact",
                      "camera_distance", "subject_framing", "depth_of_field", "focus", "visible_text",
                      "publication_caption_context", "narrative_clue", "physical_motion", "motion_rendering"])
            context = queries.prepare(core, controls, data["slot_catalog"], slots, cache, language=language)
            atomic(HERE / ("stage" + args.stage + "-" + case + "-" + language + "-contexts.json"), context)
            allowed = set(guards.eligible(data, core, controls)[0])
            # These four context records must never enter a nonhuman source pool,
            # independent of requested role, vector score or empty role conditions.
            intrinsic_adult_ids = {cid for cid, record in source["candidates"].items()
                                   if record["conditions"].get("requires_adult_context")}
            if case == "object":
                assert allowed.isdisjoint(intrinsic_adult_ids)
            cards, record, _ = retrieval.retrieve(data, core, controls, context,
                requested_slots=slots, language=language)
            atomic(HERE / ("stage" + args.stage + "-" + case + "-" + language + "-retrieval.json"), record)
            assert set(record["slot_searches"]) == set(slots)
            for slot in slots:
                trace, row = record["slot_searches"][slot], context["slots"][slot]
                fields = queries.validate(row, core, controls, data["slot_catalog"], slot)
                expected = oracle.rank(fields, row["vector"], allowed, limit=trace["lane_limit"])
                assert trace["lanes"]["bm25f"]["ranks"] == expected["bm25f"], (case, language, slot, "BM25F")
                assert trace["lanes"]["embedding"]["ranks"] == expected["embedding"], (case, language, slot, "cosine")
                assert trace["rrf"] == expected["rrf"], (case, language, slot, "RRF")
                assert search.audit_cosine(reader, row["vector"], allowed,
                    trace["lanes"]["embedding"]["ranks"], trace["cosine_proof"])
                assert not trace["tag_admission_filter"]
                assert reader.cache_bytes <= reader.cache_limit and len(reader.descriptors) <= 64
                proofs.append({"case": case, "language": language, "slot": slot,
                    "eligible_positive_records": len(allowed), "full_scan_oracle_equal": True,
                    "certificate_verified": True, "role_status": cards[slot]["status"],
                    "vector_leaves_read": len(trace["cosine_proof"]["visited_leaves"]),
                    "vector_leaves_total": len(reader.meta["vector_shards"]),
                    "presented_candidates": len(cards[slot]["candidates"])})
            calls += sum(not row["cache_hit"] for row in context["slots"].values())
            cache_hits += sum(row["cache_hit"] for row in context["slots"].values())
            if case == "object" and language == "en":
                pack = g.generate_candidate_pack(snapshot.data, core, controls, embodiment, seed=5,
                    query_context=context, requested_slots=slots)
                receipt = provider.receipt(snapshot, pack)
                replay = runtime.RuntimeSnapshotProvider(ROOT / "skills/photo-prompt-image-generator").from_receipt(pack, receipt)
                assert audit.audit(pack, replay.data, replay.query_context) == []
                result = composed_audit.audit_composed_prompt(pack, compose_native(pack), source_data=replay.data,
                    query_context=replay.query_context)
                assert result["status"] == "pass", result["failures"]
                atomic(HERE / ("stage" + args.stage + "-native-pack.json"), pack)
                atomic(HERE / ("stage" + args.stage + "-native-receipt.json"), receipt)
                rows.append({"native_pack_version": pack["contract_version"], "receipt_replay_audit": "pass",
                    "decline_optional_composition_audit": result["status"]})
            print(case, language, len(slots), "independent hybrid queries and full-scan oracles passed", flush=True)
        report = {"verified": True, "stage": args.stage, "corpus_sha256": c.digest(source),
            "generation_id": snapshot.generation_id, "query_count": len(proofs), "provider_calls": calls,
            "exact_context_cache_hits": cache_hits, "reader_initial_metrics": initial_metrics,
            "reader_final_metrics": dict(reader.metrics), "cache_limit_bytes": reader.cache_limit,
            "descriptor_count": len(reader.descriptors), "positive_records": len(vectors["entries"]),
            "results": proofs, "native_checks": rows,
            "boundary": "Maintenance fixtures, real embeddings, mechanical guard/oracle/I/O verification; not full-corpus semantic review or pixel quality."}
        atomic(HERE / ("STAGE" + args.stage + "-HYBRID-VERIFICATION.json"), report)
        print(json.dumps({k:v for k,v in report.items() if k not in {"results","reader_final_metrics"}}), flush=True)


if __name__ == "__main__":
    main()
