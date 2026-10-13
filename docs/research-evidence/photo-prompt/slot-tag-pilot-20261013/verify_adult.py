"""Supplement the two object fixtures with a genuinely adult human request."""
from contextlib import closing
import json
from pathlib import Path
import sys
from sample import HERE, ROOT, SKILL
from trace_io import write_trace
sys.path[:0] = [str(ROOT), str(SKILL / "scripts")]
import photo_candidate_corpus as c
import photo_global_index as index
import photo_global_retrieval as guards
import photo_slot_queries as queries
import photo_slot_retrieval as retrieval
import photo_sharded_search as search
import photo_runtime_sources as runtime
import photo_role_proposals as roles
from photo_search_reader import SearchReader, LazyRuntimeData
from photo_embedding_provider import load_env, atomic
from build_shared_candidate_index import offline_vector_map
from tests.photo_slot_oracle import PreparedFullScan
import prompt_generator as g


def main():
    load_env(ROOT / ".env")
    path = ROOT / "docs/research-evidence/photo-prompt/shared-candidate-pool-20261012/stage01/inputs/holdout-11-neutral-fashion-en"
    controls = c.decode((path / "creative-controls.json").read_bytes())
    core = g.load_authorial_core_arg(path / "authorial-core.json",
        request_envelope=g.load_request_envelope_arg(path / "request-envelope.json"), creative_control_snapshot=controls)
    assert core["subject"] == "An adult model"
    source = c.validate(c.load(SKILL / "assets"))
    snapshot = runtime.RuntimeSnapshotProvider(SKILL).acquire()
    vectors = offline_vector_map(snapshot.data.reader, source)
    index.validate(vectors, source)
    oracle = PreparedFullScan(index.lexical(source), vectors["entries"])
    cache = Path.home() / ".cache/image-prompt/slot-tag-pilot-stage04-adult-queries"
    proofs, counts = [], {"calls": 0, "cache_hits": 0}
    with closing(SearchReader(snapshot.root / "assets")) as reader:
        initial = dict(reader.metrics)
        assert all(initial[name] == 0 for name in ("payload_reads", "posting_reads", "vector_reads"))
        data = LazyRuntimeData(reader).for_core(core)
        allowed, bindings, contract = guards.eligible(data, core, controls)
        allowed = set(allowed)
        assert contract["subject_category"] == "human"
        assert g.candidate_pack_visual_obligation_adult_context([{"text": g.authorial_core_retrieval_text(core)[0]}], None)
        # Adult age declaration does not itself authorize sexual treatment.
        # This neutral request has no adult domain or positive appeal level;
        # it need not contain an explicit nonsexual prohibition.
        assert not contract["adult_allowed"]
        assert not allowed & {cid for cid, row in source["candidates"].items() if row["conditions"].get("requires_adult_context")}
        assert "cand_d7545a1e45d552089cc62b53e0e204a6" in allowed
        # Original profile activation remains a constraint; the extra role
        # never changes canonical guards, effects or persistent bindings.
        for cid, slot in [("cand_d7545a1e45d552089cc62b53e0e204a6", "gaze_direction"),
                          ("cand_a1daf9c0c5eb5f2c8f71a7589c6390a8", "nail_appearance"),
                          ("cand_d1b3e62299925401ab645e95b86c5a81", "body_form")]:
            p = roles.propose(data, slot, cid, bindings.get(cid, []))
            assert p["conditions"] == source["candidates"][cid]["conditions"]
            assert p["effects"] == source["candidates"][cid]["effects"]
            assert not p["persistent_tag_write"] and p["adoption"] == "optional"
        for language, slots in [("en", ["gaze_direction", "nail_appearance", "body_form", "skin_tone",
                "adult_presentation_context", "fetish_styling", "garment_detail", "color"]),
                ("ko", ["gaze_direction", "nail_appearance", "body_form", "skin_tone"])]:
            context = queries.prepare(core, controls, data["slot_catalog"], slots, cache, language=language)
            cards, record, _ = retrieval.retrieve(data, core, controls, context, requested_slots=slots, language=language)
            atomic(HERE / ("adult-human-" + language + "-contexts.json"), context)
            write_trace(HERE / ("adult-human-" + language + "-retrieval.json.gz"), record)
            for slot in slots:
                row, trace = context["slots"][slot], record["slot_searches"][slot]
                fields = queries.validate(row, core, controls, data["slot_catalog"], slot)
                expected = oracle.rank(fields, row["vector"], allowed, limit=trace["lane_limit"])
                assert trace["lanes"]["bm25f"]["ranks"] == expected["bm25f"]
                assert trace["lanes"]["embedding"]["ranks"] == expected["embedding"]
                assert trace["rrf"] == expected["rrf"]
                assert search.audit_cosine(reader, row["vector"], allowed,
                    trace["lanes"]["embedding"]["ranks"], trace["cosine_proof"])
                assert not trace["tag_admission_filter"]
                assert reader.cache_bytes <= reader.cache_limit and len(reader.descriptors) <= 64
                proofs.append({"case": "adult_human", "language": language, "slot": slot,
                    "subject_category": contract["subject_category"], "declared_adult_subject": True,
                    "sexual_appeal_allowed": contract["adult_allowed"],
                    "eligible_positive_records": len(allowed), "full_scan_oracle_equal": True,
                    "certificate_verified": True, "role_block_reason": trace["role_block_reason"],
                    "status": cards[slot]["status"], "vector_leaves_read": len(trace["cosine_proof"]["visited_leaves"]),
                    "vector_leaves_total": len(reader.meta["vector_shards"])})
            counts["calls"] += sum(not row["cache_hit"] for row in context["slots"].values())
            counts["cache_hits"] += sum(row["cache_hit"] for row in context["slots"].values())
            print("adult human", language, len(slots), "native hybrid/oracles and source preservation passed", flush=True)
        atomic(HERE / "ADULT-HUMAN-VERIFICATION.json", {"verified": True, "source_sha256": c.digest(source),
            "generation_id": snapshot.generation_id, "fixture": str(path.relative_to(ROOT)), "subject": core["subject"],
            "query_count": len(proofs), "query_provider_calls": counts["calls"], "exact_context_cache_hits": counts["cache_hits"],
            "results": proofs, "initial_reader_metrics": initial, "final_reader_metrics": dict(reader.metrics),
            "cache_limit_bytes": reader.cache_limit, "descriptor_count": len(reader.descriptors),
            "source_guards_effects_preserved_in_new_roles": True,
            "boundary": "Actual adult-human maintenance fixture and real queries; no automatic fetish approval, native tag writes or pixel assessment."})


if __name__ == "__main__":
    main()
