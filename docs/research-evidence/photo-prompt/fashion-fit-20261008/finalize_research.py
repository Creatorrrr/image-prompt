"""Check this research only; record concurrent state without writing runtime files."""
from datetime import datetime, timezone, timedelta
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REPORT = ROOT / "docs/analysis/2026-10-08-fashion-fit-visual-semantics-research.md"
KST = timezone(timedelta(hours=9))


def dump(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def fingerprint(path):
    if not path.is_file():
        return {"missing": True}
    return {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size, "mode": path.stat().st_mode & 0o777}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def implementation_plan():
    cards = json.loads((HERE / "semantic-cards.json").read_text())["cards"]
    phases = [
        dict(id="FIT-PHASE-1", title_ko="의미 동등성·개별 근거·승격 범위",
             depends_on=[], outputs=["term-plan.csv successor review", "approved variant-to-existing-ID decisions"],
             actions=["Review all 513 terms against meaning, owner, complete effects, visibility and scope.",
                      "Use existing meaning; add equivalent context; split a scoped variant; or retain specification/pending status.",
                      "Confirm lantern panel diagrams, colloquial contexts and individually unconfirmed intimate/product variants before hard promotion.",
                      "Deduplicate 119 draft clauses; do not treat their count as a target for new runtime entries."],
             exit_criteria=["Every promoted variant has directly applicable evidence, confusion boundaries, owner and property scope.",
                            "Every term has an explicit reuse/enrich/new/specification/pending disposition."]),
        dict(id="FIT-PHASE-2", title_ko="원본 확장·시각 구성 요소 작성",
             depends_on=["FIT-PHASE-1"],
             proposed_files=["skills/photo-prompt-image-generator/assets/photo_prompt_fashion_fit_extension.json",
                             "skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_fashion_fit.json"],
             existing_surfaces_to_review=["photo_prompt_source_manifest.json", "existing_slot_context_extensions",
                 "clothing_structure", "portrait_fashion_exposure", "swimwear", "historical_womenswear"],
             actions=["Recheck current dirty state and manifest order before implementation.",
                      "Register extensions only in the canonical manifest; omit generated visual fields from source.",
                      "Bind concrete concept nodes/relations; narrow family templates to all and only selected effects.",
                      "Use authored_components v1 or v2 according to actual evidence duties.",
                      "Keep original authored records and maintenance history; write successor records for changed bodies.",
                      "Keep raw keywords, sources and research text outside runtime relevance fields."],
             exit_criteria=["Dictionary/schema/manifest/reference checks pass.",
                            "No unrequested identity, body, scene, age, color, material or length effect escapes declarations."]),
        dict(id="FIT-PHASE-3", title_ko="인덱스·BM25F·검증된 런타임 세대",
             depends_on=["FIT-PHASE-2"],
             actions=["Use source_update and canonical builders/publication from the current maintenance contract.",
                      "Rebuild source metadata, dictionary/BM25F and visual registry indexes against one source revision.",
                      "Reuse vectors only for identical entry/text/provider/model/dimensions; embed changed text with batch size 1.",
                      "Do not manually merge generated shards or claim a pending generation is current."],
             exit_criteria=["Authored/dictionary and both deep-index checks pass.",
                            "Public receipt and validated runtime generation share the expected source/registry hashes."]),
        dict(id="FIT-PHASE-4", title_ko="공개 검색·선택·구성 회귀",
             depends_on=["FIT-PHASE-3"],
             planned_comparisons=38, planned_mutations=10,
             related_tests=["test_photo_candidate_semantics.py", "test_photo_core_retrieval.py",
                 "test_photo_visual_profile_retrieval.py", "test_photo_womens_casualwear_visual_semantics.py",
                 "test_photo_womens_activewear_visual_semantics.py", "test_photo_body_morphology_semantics.py",
                 "test_photo_swimwear_semantics.py", "test_photo_costume_cosplay_semantics.py"],
             actions=["Write independent ko/en requests, controls and frozen cores before reading candidates.",
                      "Change one fit axis per minimal pair; inspect public exposure, selection, guard rejection and composed evidence.",
                      "Test different-garment owner binding and locked-property rejection.",
                      "Preserve unselected alternatives and existing historical fixtures; broaden tests only for actual impact/risk."],
             exit_criteria=["Planned invariant cases and relevant existing regressions pass.",
                            "Known preexisting failures, retrieval/composition and index integrity are reported separately."]),
        dict(id="FIT-PHASE-5", title_ko="생성 요청 시 이미지·관찰 관계",
             depends_on=["FIT-PHASE-4"], condition="Only when image generation is requested later.",
             planned_pixel_clusters=12,
             actions=["Preserve exact request/core/controls/settings and original images; a shared seed is no pixel identity guarantee.",
                      "Review only selected obligations at native resolution, including same-garment relation endpoints.",
                      "Do not change a locked camera/crop to make a hidden requirement visible.",
                      "Use UNOBSERVABLE_NOT_PASS and partial_is_fail; exclude static claims about hidden measurement/performance.",
                      "Record moderation, meaning preservation, visual quality and requester preference independently."],
             exit_criteria=["Activated observable gates pass without unrelated changes.",
                            "Blocked/unobservable/partial cases are not counted as successful renders."]),
        dict(id="FIT-PHASE-6", title_ko="증거 수준에 맞는 정식 승격·전달",
             depends_on=["FIT-PHASE-4"], optional_dependency="FIT-PHASE-5 for rendered-quality claims",
             actions=["Link each adopted variant to source term, semantic card, runtime ID, successor provenance and validation.",
                      "State authored/retrieval/composition/pixel/preference evidence tiers precisely.",
                      "Preserve concurrent changes and record actual commit/PR/push state only when performed."],
             exit_criteria=["Each adopted record has traceable meaning and validation; deferred evidence remains explicit."])
    ]
    return dict(schema="fashion-fit-implementation-plan/v1", state="planned_not_executed",
        generated_from="semantic-cards.json + bounded research findings",
        counts=dict(seed_terms=513, sources=41, semantic_families=64, candidate_drafts=119),
        priority_card_ids={p:[c["id"] for c in cards if c["priority"]==p] for p in ("P0","P1","P2")},
        runtime_files_created=0, provider_calls=0, phases=phases,
        decision_rules=dict(reuse="Same meaning, concrete owner, complete effects and evidence scope.",
            equivalent_context="Paraphrase/context only; no meaning/effect widening.",
            scoped_variant="Separate meaning, owner or effect requires a distinct reviewed variant.",
            nonvisual="Retain requested specification; never manufacture an observable numerical/performance proof."),
        completion_of_this_request="Research and incorporation plan delivered; implementation is a future task.")


def main():
    text = REPORT.read_text()
    text = text.replace("01:19:52~01:20 KST", "01:19:52~01:20:07 KST")
    text = text.replace("curvy fit / local cup gap / waist gap", "curvy fit / cup gaping / waist gaping")
    REPORT.write_text(text)
    dump("implementation-plan.json", implementation_plan())
    before = json.loads((HERE/"source-snapshot.json").read_text())
    compared = {}
    for key in ("source_files", "tracked_dirty_files"):
        records = {}
        for rel, original in before[key].items():
            current = fingerprint(ROOT/rel)
            records[rel] = {"before":original, "after":current,
                           "identical_bytes_and_mode":original==current}
        compared[key] = {
            "count":len(records),
            "unchanged_count":sum(r["identical_bytes_and_mode"] for r in records.values()),
            "changed_paths":[p for p,r in records.items() if not r["identical_bytes_and_mode"]],
            "records":records}
    # Do not strip the status-column spaces from git output.
    current_status = subprocess.check_output(["git","status","--short"],cwd=ROOT,text=True).splitlines()
    report_rel = str(REPORT.relative_to(ROOT))
    evidence_rel = str(HERE.relative_to(ROOT))+"/"
    changes = sorted({p for b in compared.values() for p in b["changed_paths"]})
    dump("final-preservation.json", dict(
        checked_at_kst=datetime.now(KST).isoformat(),
        baseline_completed_at_kst=before["completed_at_kst"],
        baseline_head=before["head"], current_head=git("rev-parse","HEAD"),
        task_write_scope=[report_rel,evidence_rel],
        writes_outside_task_scope_executed_by_this_research=False,
        source_loader_stable_interval=not before["changed_during_load"],
        comparison=compared,
        workspace_differences_since_baseline=changes,
        interpretation="Content/mode differences are observations, not proof of which concurrent actor wrote them. This research wrote only the listed documentation/evidence scope and performed no restore/reset/stage/commit.",
        untracked_scope_limit="Initial untracked status entries are retained; untracked/ignored file bytes were not comprehensively hashed, so whole-workspace byte preservation is not claimed.",
        baseline_status_entries=len(before["preexisting_git_status"]),
        current_status_entries=len(current_status),
        current_git_status=current_status,
        report_sha256=hashlib.sha256(REPORT.read_bytes()).hexdigest(),
        embedding_calls=0,image_calls=0,index_build_calls=0,runtime_dispatch_calls=0))

    sources=json.loads((HERE/"sources.json").read_text())["sources"]
    cards=json.loads((HERE/"semantic-cards.json").read_text())["cards"]
    proposals=json.loads((HERE/"candidate-proposals.json").read_text())["proposals"]
    terms=json.loads((HERE/"term-plan.json").read_text())["terms"]
    csv_rows=list(csv.DictReader((HERE/"term-plan.csv").open(encoding="utf-8-sig")))
    source_ids={s["id"] for s in sources}; card_ids={c["id"] for c in cards}
    local_targets=[]
    missing=[]
    for p in (REPORT,HERE/"semantic-cards.md"):
        for target in re.findall(r"\]\((/[^)]+)\)",p.read_text()):
            local_targets.append(target)
            if not Path(target).exists(): missing.append(target)
    source_record_paths={}
    def walk_records(value, path):
        if isinstance(value, dict):
            if isinstance(value.get("id"),str):
                source_record_paths.setdefault(value["id"],set()).add(path)
            for child in value.values(): walk_records(child,path)
        elif isinstance(value,list):
            for child in value: walk_records(child,path)
    for rel in before["source_files"]:
        path=ROOT/rel
        if path.suffix==".json" and path.is_file():
            walk_records(json.loads(path.read_text()),rel)
    existing_verification=[]
    for c in cards:
        for existing in c["existing_record_ids_to_review"]:
            existing_verification.append(dict(card_id=c["id"],id=existing,
                found_source_paths=sorted(source_record_paths.get(existing,set()))))
    unresolved_reuse=[row for row in existing_verification if not row["found_source_paths"]]
    dump("existing-id-verification.json",dict(
        checked_at_kst=datetime.now(KST).isoformat(),
        scope="Record ID existence only, across audited authored JSON files read at finalization.",
        source_files=[rel for rel in before["source_files"] if rel.endswith(".json")],
        note="Existence is not semantic equivalence, source completeness or current compiled runtime freshness.",
        count=len(existing_verification),missing=unresolved_reuse,records=existing_verification))
    checks=dict(
        report_sections_1_to_7=all(f"## {n}." in REPORT.read_text() for n in range(1,8)),
        csv_json_term_identity=len(csv_rows)==len(terms)==513 and
            [(r["id"],r["source_term"]) for r in csv_rows]==[(r["id"],r["source_term"]) for r in terms],
        local_links_exist=not missing,
        term_card_refs_valid=all(set(t["semantic_card_ids"])<=card_ids for t in terms),
        card_source_refs_valid=all(set(c["source_ids"])<=source_ids for c in cards),
        proposal_card_and_source_refs_valid=all(p["card_id"] in card_ids and set(p["source_ids"])<=source_ids for p in proposals),
        source_ids_unique=len(source_ids)==len(sources)==41,
        source_limits_present=all(s["access_level"] and s["verified_scope_ko"] and s["claim_limits_ko"] for s in sources),
        proposed_existing_ids_exist=not unresolved_reuse,
        no_broken_scope_marker=all(p["affected_property_templates"] and p["further_review"] for p in proposals),
        no_japanese_typo=not any("地域別" in p.read_text() or "生成 요청" in p.read_text()
            for p in HERE.iterdir() if p.is_file() and p.suffix in {".json",".md",".txt"}))
    dump("report-validation.json",dict(scope="documentation_and_plan_integrity_only",
        checked_at_kst=datetime.now(KST).isoformat(),checks=checks,
        result="PASS" if all(checks.values()) else "FAIL",
        local_link_targets_checked=len(local_targets),missing_local_links=missing,
        existing_ids_missing_from_audited_sources=unresolved_reuse,
        existing_id_note="Source ID existence checked separately; semantic equivalence, complete effects and runtime freshness are not implied.",
        evidence_boundary="No executable schema correctness, embedding, live retrieval, prompt composition, native pixels or user acceptance claim."))
    assert all(checks.values()), checks
    print(json.dumps(dict(report_checks=checks,
        compared_source_files=compared["source_files"]["count"],
        changed_source_files=compared["source_files"]["changed_paths"],
        changed_tracked_dirty_files=compared["tracked_dirty_files"]["changed_paths"],
        existing_ids_missing_from_sources=unresolved_reuse),ensure_ascii=False))


if __name__ == "__main__":
    main()
