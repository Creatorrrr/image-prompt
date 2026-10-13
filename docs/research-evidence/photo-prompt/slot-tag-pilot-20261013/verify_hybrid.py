"""Actual embeddings, candidate-centred reverse discovery and native oracles.

Unrestricted positive-pool searches are offline maintenance discovery only.
Native request searches separately enforce canonical and member conditions.
"""
from contextlib import closing
import argparse
import hashlib
import json
from pathlib import Path
import sys
from sample import HERE, ROOT, SKILL
from ledger import authored, frozen_rows
from trace_io import read_trace, write_trace

sys.path[:0] = [str(ROOT), str(SKILL / "scripts")]
import photo_candidate_corpus as c
import photo_global_index as index
import photo_global_retrieval as guards
import photo_slot_queries as queries
import photo_slot_retrieval as retrieval
import photo_sharded_search as search
import photo_runtime_sources as runtime
from photo_search_reader import SearchReader, LazyRuntimeData
from photo_embedding_provider import load_env, atomic
from build_shared_candidate_index import offline_vector_map
from tests.photo_slot_oracle import PreparedFullScan
from tests.photo_native_runtime import compose_native
import prompt_generator as g
import audit_global_retrieval as audit
import audit_composed_prompt as composed_audit


def frozen(case):
    path = (ROOT / "docs/research-evidence/photo-prompt/shared-candidate-pool-20261012/stage01/inputs/dev-02-blue-cup-en"
            if case == "object" else ROOT / "tests/fixtures/photo_prompt/camera_authoring_path_v1/en_open")
    controls = c.decode((path / "creative-controls.json").read_bytes())
    core = g.load_authorial_core_arg(path / "authorial-core.json",
        request_envelope=g.load_request_envelope_arg(path / "request-envelope.json"), creative_control_snapshot=controls)
    return core, controls, c.decode((path / "embodiment-review.json").read_bytes())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume-initial", action="store_true", help="Reuse the completed 139-query scenario after a later assertion failed.")
    args = parser.parse_args()
    load_env(ROOT / ".env")
    source = c.validate(c.load(SKILL / "assets"))
    source_sha = c.digest(source)
    provider = runtime.RuntimeSnapshotProvider(SKILL)
    snapshot = provider.acquire()
    cache = Path.home() / ".cache/image-prompt/slot-taxonomy-stage03-queries"
    vectors = offline_vector_map(snapshot.data.reader, source)
    index.validate(vectors, source)
    oracle = PreparedFullScan(index.lexical(source), vectors["entries"])
    all_positive = set(vectors["entries"])
    diagnostic = {cid for cid, row in source["candidates"].items() if row["record_kind"] == "diagnostic"}
    assert len(all_positive) == 18186 and not all_positive & diagnostic
    samples = {row["candidate_id"]: row for row in frozen_rows()}
    reviewed = authored()
    proof_rows, reverse, questions, native_checks = [], {}, [], []
    cache_hits, calls = 0, 0
    with closing(SearchReader(snapshot.root / "assets")) as reader:
        initial = dict(reader.metrics)
        assert all(reader.metrics[name] == 0 for name in ("payload_reads", "posting_reads", "vector_reads"))
        scenarios = [("linen", "en", sorted(source["slot_catalog"])),
            ("object", "en", ["gaze_direction", "nail_appearance", "body_form", "skin_tone", "adult_presentation_context",
                "fetish_styling", "garment_detail", "light_quality", "visual_hierarchy", "surface_material"]),
            ("linen", "ko", ["gaze_direction", "nail_appearance", "body_form", "skin_tone"])]
        for case, language, slots in scenarios:
            core, controls, embodiment = frozen(case)
            data = LazyRuntimeData(reader).for_core(core)
            if args.resume_initial and case == "linen" and language == "en":
                # The first execution completed all strict full-scan and
                # certificate assertions before failing in the next case.
                # Pin those exact completed artifacts, rather than silently
                # counting an incomplete run as a pass.
                old_log = (HERE / "HYBRID-INITIAL.log").read_text()
                assert "human en 139 actual query vectors, native hybrid/oracles and certificates passed" in old_log
                context = c.decode((HERE / "linen-en-contexts.json").read_bytes())
                record = read_trace(HERE / "linen-en-retrieval.json.gz")
                assert record["corpus_sha256"] == source_sha and record["query_context_sha256"] == context["canonical_sha256"]
                assert record["source_authorial_core_sha256"] == core["canonical_sha256"]
                assert record["canonical_sha256"] == c.digest({key: value for key, value in record.items() if key != "canonical_sha256"})
                assert set(record["slot_searches"]) == set(slots)
                for slot in slots:
                    queries.validate(context["slots"][slot], core, controls, data["slot_catalog"], slot)
                    trace = record["slot_searches"][slot]
                    proof_rows.append({"case": "linen_object", "language": language, "slot": slot,
                        "eligible_positive_records": trace["eligible_candidates"], "full_scan_oracle_equal": True,
                        "certificate_verified": True, "completion_evidence": "FIRST-SCENARIO-CHECKPOINT.json",
                        "vector_leaves_read": len(trace["cosine_proof"]["visited_leaves"]),
                        "vector_leaves_total": len(reader.meta["vector_shards"])})
                reverse = c.decode((HERE / "REVERSE-DISCOVERY.json").read_bytes())
                questions = c.decode((HERE / "REVERSE-QUESTIONS.json").read_bytes())
                assert set(reverse) == set(slots) and all(row["positive_count"] == len(all_positive) for row in reverse.values())
                atomic(HERE / "FIRST-SCENARIO-CHECKPOINT.json", {"source_sha256": source_sha,
                    "generation_id": snapshot.generation_id, "actual_subject": core["subject"], "query_count": len(slots),
                    "completion_log_sha256": hashlib.sha256((HERE / "HYBRID-INITIAL.log").read_bytes()).hexdigest(),
                    "trace_sha256": c.digest(record), "contexts_sha256": c.digest(context),
                    "later_failure": "Removed an incorrect test assumption that the nail profile carried an adult/human guard. Its source has empty guards/effects, recorded for stage05 carrier refinement."})
                atomic(HERE / "linen-en-contexts.json", context)
                write_trace(HERE / "linen-en-retrieval.json.gz", record)
                cache_hits += sum(row["cache_hit"] for row in context["slots"].values())
                calls += sum(not row["cache_hit"] for row in context["slots"].values())
                print("linen object en", len(slots), "completed native/oracle checkpoint revalidated", flush=True)
                continue
            context = queries.prepare(core, controls, data["slot_catalog"], slots, cache, language=language)
            atomic(HERE / (case + "-" + language + "-contexts.json"), context)
            allowed, binding_map, contract = guards.eligible(data, core, controls)
            allowed = set(allowed)
            if case == "object":
                assert not allowed & {cid for cid, row in source["candidates"].items()
                    if row["conditions"].get("requires_adult_context") or row["conditions"].get("for_any") == ["human"]}
                # A neutral role cannot admit the native dress/bustier bundle
                # while its members require human subjects.
                assert "cand_cb45aeb918bc58e1b6dec41185207523" not in allowed
                assert not allowed & {cid for cid, row in source["candidates"].items()
                    if row["record_kind"] == "visual_profile" and row["content"].get("activation", {}).get("requires_adult_character")}
            cards, record, _ = retrieval.retrieve(data, core, controls, context,
                requested_slots=slots, language=language)
            write_trace(HERE / (case + "-" + language + "-retrieval.json.gz"), record)
            assert set(record["slot_searches"]) == set(slots)
            for slot in slots:
                trace, query = record["slot_searches"][slot], context["slots"][slot]
                fields = queries.validate(query, core, controls, data["slot_catalog"], slot)
                expected = oracle.rank(fields, query["vector"], allowed, limit=trace["lane_limit"])
                assert trace["lanes"]["bm25f"]["ranks"] == expected["bm25f"], (case, language, slot, "BM25F")
                assert trace["lanes"]["embedding"]["ranks"] == expected["embedding"], (case, language, slot, "cosine")
                assert trace["rrf"] == expected["rrf"], (case, language, slot, "RRF")
                assert search.audit_cosine(reader, query["vector"], allowed,
                    trace["lanes"]["embedding"]["ranks"], trace["cosine_proof"])
                assert not trace["tag_admission_filter"] and not diagnostic & {item["id"] for item in cards[slot]["candidates"]}
                assert reader.cache_bytes <= reader.cache_limit and len(reader.descriptors) <= 64
                proof_rows.append({"case": case, "language": language, "slot": slot, "whole_pool_with_intrinsic_guards": True,
                    "eligible_positive_records": len(allowed), "full_scan_oracle_equal": True, "certificate_verified": True,
                    "vector_leaves_read": len(trace["cosine_proof"]["visited_leaves"]),
                    "vector_leaves_total": len(reader.meta["vector_shards"]), "role_status": cards[slot]["status"],
                    "presented": len(cards[slot]["candidates"])})
                if case == "linen" and language == "en":
                    whole = oracle.rank(fields, query["vector"], all_positive, limit=384)
                    by_lane = {lane: {item["document_id"]: number for number, item in enumerate(whole[lane], 1)}
                        for lane in ("bm25f", "embedding", "rrf")}
                    pilot_hits = [{"number": samples[cid]["number"], "candidate_id": cid,
                        "approved_for_role": slot in reviewed[samples[cid]["number"]]["approved"],
                        "bm25f_rank": by_lane["bm25f"].get(cid), "embedding_rank": by_lane["embedding"].get(cid),
                        "rrf_rank": by_lane["rrf"].get(cid)}
                        for cid in sorted(samples) if any(cid in ranks for ranks in by_lane.values())]
                    reverse[slot] = {"eligible_pool": "offline_all_positive_without_request_guards", "positive_count": len(all_positive),
                        "full_positive_pool_scored": True, "lane_limit": 384, "top20": {lane: whole[lane][:20] for lane in whole},
                        "pilot_hits": sorted(pilot_hits, key=lambda item: (item["rrf_rank"] or 9999, item["number"]))}
                    # One highly ranked non-approved pilot association per
                    # role is a re-reading cue, never an automatic tag.
                    for item in reverse[slot]["pilot_hits"]:
                        if not item["approved_for_role"] and reviewed[item["number"]]["approved"]:
                            questions.append({"slot": slot, **item})
                            break
            cache_hits += sum(query["cache_hit"] for query in context["slots"].values())
            calls += sum(not query["cache_hit"] for query in context["slots"].values())
            if case == "object":
                smoke_slots = ["surface_material", "light_quality", "visual_hierarchy"]
                smoke = {"schema": queries.SCHEMA, "slots": {slot: context["slots"][slot] for slot in smoke_slots}}
                smoke["canonical_sha256"] = c.digest(smoke)
                pack = g.generate_candidate_pack(snapshot.data, core, controls, embodiment, seed=5,
                    query_context=smoke, requested_slots=smoke_slots)
                receipt = provider.receipt(snapshot, pack)
                replay = runtime.RuntimeSnapshotProvider(SKILL).from_receipt(pack, receipt)
                assert audit.audit(pack, replay.data, replay.query_context) == []
                composed = composed_audit.audit_composed_prompt(pack, compose_native(pack), source_data=replay.data,
                    query_context=replay.query_context)
                assert composed["status"] == "pass", composed["failures"]
                atomic(HERE / "NATIVE-PACK.json", pack)
                atomic(HERE / "NATIVE-RECEIPT.json", receipt)
                native_checks.append({"pack": pack["contract_version"], "receipt_replay": "pass", "composition_audit": "pass",
                    "slots": smoke_slots, "pixel_generation": "not_performed"})
            atomic(HERE / "REVERSE-DISCOVERY.json", reverse)
            atomic(HERE / "REVERSE-QUESTIONS.json", questions)
            print(case, language, len(slots), "actual query vectors, native hybrid/oracles and certificates passed", flush=True)
        assert c.digest(c.load(SKILL / "assets")) == source_sha
        report = {"schema": "photo-slot-tag-pilot-hybrid-verification/v1", "verified": True,
            "corpus_sha256": source_sha, "generation_id": snapshot.generation_id, "query_count": len(proof_rows),
            "query_provider_calls": calls, "exact_context_cache_hits": cache_hits, "offline_reverse_roles": len(reverse),
            "offline_reverse_pool": len(all_positive), "diagnostic_excluded": len(diagnostic),
            "initial_reader_metrics": initial, "final_reader_metrics": dict(reader.metrics),
            "cache_limit_bytes": reader.cache_limit, "descriptor_count": len(reader.descriptors),
            "native_checks": native_checks, "results": proof_rows,
            "first_scenario_resumed": args.resume_initial,
            "reader_metrics_scope": "resumed scenarios only" if args.resume_initial else "all scenarios",
            "boundary": "Real provider queries and exact mechanical verification on frozen maintenance requests; full-pool discovery is not source guard bypass or semantic approval. No pixel or independent human quality assessment."}
        atomic(HERE / "HYBRID-VERIFICATION.json", report)
        print(json.dumps({key: report[key] for key in ("verified", "query_count", "query_provider_calls", "exact_context_cache_hits", "offline_reverse_roles")}))


if __name__ == "__main__":
    main()
