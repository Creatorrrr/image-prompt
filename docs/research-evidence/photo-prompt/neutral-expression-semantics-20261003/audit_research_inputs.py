"""Build a read-only research inventory and a checkout-specific corpus audit."""
from pathlib import Path
from collections import Counter
import hashlib, json, re, subprocess, sys, unicodedata

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as pg

def write(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def norm(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", s).casefold()).strip()

receipt = json.loads((OUT / "CONVERSATION-RECEIPT.json").read_text())
terms = []
for turn in receipt["thread"]["turns"]:
    for item in turn.get("items", []):
        if item["type"] != "agentMessage":
            continue
        domain = "morphology" if turn["id"].startswith("f1209") else "evaluation_behavior_relation"
        chapter = subsection = ""
        for lineno, line in enumerate(item["text"].splitlines(), 1):
            if line.startswith("## "):
                chapter = line[3:]; subsection = ""
            elif line.startswith("### "):
                subsection = line[4:]
            if not line.startswith("|"):
                continue
            cells = [x.strip() for x in re.split(r"(?<!\\)\|", line)[1:-1]]
            if not cells or not cells[0].startswith("**"):
                continue
            label = re.sub(r"\*\*", "", cells[0])
            label = re.sub(r"^\d+\.\s*", "", label)
            is_example = (domain == "morphology" and chapter.startswith("10.")) or (
                domain != "morphology" and chapter.startswith("8."))
            if domain == "morphology":
                if chapter.startswith(("1.", "2.", "4.", "5.", "6.")):
                    disposition = "decompose_and_review_existing_morphology_owner"
                elif chapter.startswith("3.") and subsection.startswith("3-2"):
                    disposition = "region_name_only_no_geometry_added"
                elif chapter.startswith("3."):
                    disposition = "relative_size_or_region_context"
                elif chapter.startswith("7."):
                    disposition = "separate_surface_from_temporal_or_material_property"
                elif chapter.startswith("8."):
                    disposition = "separate_local_shape_expression_and_evaluation"
                else:
                    disposition = "garment_body_boundary_or_authoring_example"
            else:
                if chapter.startswith(("1.", "2.")):
                    disposition = "evaluation_register_context_not_visual_prototype"
                elif chapter.startswith("3."):
                    disposition = "split_attention_behavior_intention_temporal_and_linguistic_meaning"
                elif chapter.startswith("4."):
                    disposition = "attributed_dehumanizing_evaluation_no_appearance_default"
                elif chapter.startswith("5."):
                    disposition = "genre_content_metadata_not_scene_recipe"
                elif chapter.startswith("6."):
                    disposition = "separate_role_agreement_activity_prop_and_observer_access"
                elif chapter.startswith("7."):
                    disposition = "context_supported_directed_relation_not_fixed_appearance"
                else:
                    disposition = "authoring_example_not_requester_definition"
            terms.append({
                "id": f"NE{len(terms)+1:03d}", "domain": domain,
                "source_turn_id": turn["id"], "source_item_id": item["id"],
                "source_line": lineno, "chapter": chapter, "subsection": subsection,
                "expression_group": label, "source_columns": cells[1:],
                "source_row": line, "row_kind": "authoring_example" if is_example else "keyword_group",
                "original_definition_status": "unverified_cached_assistant_research",
                "original_neutral_text_status": "assistant_authored_interpretation",
                "research_disposition": disposition,
                "runtime_export_allowed": False,
                "coverage_mapping_status": "chapter_level_triage_only_pending_term_specific_review",
            })
write("TERM-INVENTORY.json", {
    "schema_version": "neutral-expression-term-inventory/v1", "checked_on": "2026-10-03",
    "conversation_id": receipt["conversation_id"], "counts": dict(Counter(x["row_kind"] for x in terms)),
    "notes": ["Expression groups are table rows, not a count of distinct words or definitions.",
              "Cached assistant definitions and neutral examples are not independently verified source definitions.",
              "Chapter-level triage is not a term-to-profile equivalence or an activation map."],
    "terms": terms,
})

registry = pg.load_visual_obligation_registry(SKILL / "assets/photo_prompt_visual_obligations.json")
corpus = pg.load_json(SKILL / "assets/photo_prompt_tags.json")
profile_owners = {}
profile_paths = [SKILL / "assets/photo_prompt_visual_obligations.json"]
profile_paths += [SKILL / "assets" / n for n in pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES]
for path in profile_paths:
    for p in json.loads(path.read_text()).get("profiles", []):
        profile_owners[p["id"]] = str(path.relative_to(ROOT))

candidate_owners = {}
candidate_paths = [SKILL / "assets/photo_prompt_tags.json"]
candidate_paths += [SKILL / "assets" / n for n in pg.RESEARCH_EXTENSION_FILENAMES]
for path in candidate_paths:
    d = json.loads(path.read_text())
    for slot, entries in d.get("slots", {}).items():
        for entry in entries:
            candidate_owners[(slot, entry["id"])] = str(path.relative_to(ROOT))
    for slot, entries in d.get("existing_slot_context_extensions", {}).items():
        for entry_id in entries:
            key = (slot, entry_id)
            candidate_owners.setdefault(key, str(path.relative_to(ROOT)))

selected_ids = {
    "curvilinear_figure_relation", "bust_prominence_relation", "toned_muscular_build",
    "inner_thigh_negative_space", "waist_hip_transition", "upper_lip_philtral_contour",
    "self_possessed_sensual_presence", "target_directed_seductive_display",
    "playful_flirtation_interaction", "embodied_corruption_transition",
    "pfe_lateral_chest", "pfe_lower_chest", "decolletage_neckline_exposure",
    "sheer_garment_optical_layering",
}
selected_ids.update(p["id"] for p in registry["profiles"] if p["id"].startswith("bm_"))
selected = [{"owner_file": profile_owners[p["id"]], **p} for p in registry["profiles"] if p["id"] in selected_ids]
exact = {}
for p in registry["profiles"]:
    for alias in p["activation"].get("exact_terms", []) + p["activation"].get("project_glossary_aliases", []):
        exact.setdefault(norm(alias), []).append(p["id"])

queries = [
    "lewd", "prurient", "salacious", "raunchy", "bimbo", "bimbofication",
    "slutty", "thirst trap", "leer", "ogle", "down bad", "gooning",
    "dominant", "submissive", "collar", "bondage", "safeword", "aftercare",
    "PWP", "Dead Dove", "NTR", "dub-con", "non-con",
    "pouty", "pouty lips", "doe-eyed", "bedroom eyes", "bombshell",
    "callipygian", "busty figure", "curvy figure", "petite",
    "thicc", "glamour", "글래머 체형", "꿀벅지", "sideboob", "underboob",
    "resilient", "jiggly", "cellulite", "stretch marks", "타락",
]
probe = []
for term in queries:
    t = norm(term)
    profile_hits = []
    for p in registry["profiles"]:
        s = p["semantics"]
        fields = [s.get("definition", ""), *s.get("paraphrase_examples", []),
                  *p.get("concept_candidate", {}).get("concept_terms", [])]
        if any(t in norm(f) for f in fields):
            profile_hits.append(p["id"])
    candidate_hits = []
    for slot, entries in corpus["slots"].items():
        for c in entries:
            fields = [c.get(k, "") for k in ("ko", "en", "embedding_text")]
            fields += c.get("aliases", []) + c.get("keywords", [])
            if any(t in norm(f) for f in fields):
                candidate_hits.append({"slot": slot, "id": c["id"],
                    "owner_file": candidate_owners.get((slot, c["id"]))})
    probe.append({"term": term, "literal_exact_owners": exact.get(t, []),
                  "positive_substring_profile_hits": profile_hits,
                  "candidate_substring_hits": candidate_hits})

paths = set(profile_paths + candidate_paths + [
    SKILL / "scripts/prompt_generator.py", SKILL / "references/retrieval-contract.md",
    SKILL / "references/composition-contract.md", SKILL / "assets/photo_prompt_visual_profile_index.json",
    SKILL / "assets/photo_prompt_semantic_index.json",
])
snapshot = {
    "schema_version": "neutral-expression-live-corpus-audit/v1", "checked_on": "2026-10-03",
    "head": subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
    "branch": subprocess.check_output(["git","branch","--show-current"],cwd=ROOT,text=True).strip(),
    "dirty_status_at_audit": subprocess.check_output(["git","status","--short"],cwd=ROOT,text=True).splitlines(),
    "counts": {"profiles": len(registry["profiles"]), "profile_ids": len({p["id"] for p in registry["profiles"]}),
               "ordinary_candidates": sum(len(v) for v in corpus["slots"].values()),
               "slots": len(corpus["slots"])},
    "source_files": [{"path": str(p.relative_to(ROOT)), "sha256": sha(p), "bytes": p.stat().st_size}
                     for p in sorted(paths) if p.exists()],
    "selected_profile_contracts": selected,
    "selected_slots": {slot: [
        {"owner_file": candidate_owners.get((slot, c["id"])), **c} for c in corpus["slots"][slot]
    ] for slot in ["expression", "gaze_target", "gaze_engagement", "relational_action",
                  "partner_role", "fetish_styling", "adult_context", "intent_state",
                  "silhouette_proportion", "skin_condition", "garment_detail"]},
    "term_probes": probe,
    "limits": ["Substring matches are inventories, not ranking, eligibility, selection, or render evidence.",
               "No substring hit is not proof of missing semantics; inspect paraphrases/components and owners.",
               "Audit includes pre-existing uncommitted body-morphology work; counts are this checkout, not remote main.",
               "No index regeneration, candidate pack, runtime prompt, image generation, or quality test is run."],
}
write("CURRENT-DATA-AUDIT.json", snapshot)
write("CORPUS-RECEIPT.json", {k:v for k,v in snapshot.items() if k not in ["selected_profile_contracts","selected_slots","term_probes"]})

index = pg.build_visual_profile_index_payload(registry)
diagnostic_queries = [
    ("M01", "an adult woman with a busty figure", "large regional volume lexical trigger"),
    ("M02", "an adult woman with a curvy figure", "whole-body curvature lexical trigger"),
    ("M03", "an adult woman described as a bombshell", "evaluation without determined geometry"),
    ("M04", "an adult with pouty lips", "expression/local lip polysemy"),
    ("M05", "a bawdy joke on a sign", "language register rather than body styling"),
    ("M06", "an adult with a collar", "polysemous accessory or role"),
    ("M07", "an adult dominant role in a story", "role without fixed physical staging"),
    ("M08", "a thirst trap portrait of an adult", "publishing intention not prescribed pose"),
    ("M09", "이익 때문에 원칙을 포기한 성인 인물의 타락", "moral narrative rather than on-body transformation"),
    ("M10", "성인 인물의 흑화, 몸에 번지는 변화", "explicit embodied transformation"),
    ("M11", "not a busty figure, an adult with a straight torso silhouette", "negated region size"),
    ("M12", "a supple leather glove, no people", "nonhuman material homonym"),
]
diagnostics = []
for case_id, query, purpose in diagnostic_queries:
    rows = [{"id": case_id+"-request", "source": "user_requirement", "polarity": "included", "text": query},
            {"id": case_id+"-context", "source": "authorial_core_interpreted_intent", "polarity": "included", "text": query}]
    resolved = pg.resolve_visual_profile_hits(registry, rows, visual_profile_index=index,
        query_text="", query_fields=None, query_vector=None, adult_context=(case_id != "M12"))
    diagnostics.append({"id":case_id,"query":query,"purpose":purpose,
        "actual": resolved, "status":"diagnostic_observation_not_full_core_regression"})
write("EXACT-ROUTING-DIAGNOSTICS.json", {
    "schema_version":"neutral-expression-exact-diagnostic/v1", "checked_on":"2026-10-03",
    "method":"Current resolver; exact-only generated in-memory index; artificial source rows with an authorial-core-context marker.",
    "limits":["These rows are diagnostic inputs, not an envelope or valid frozen authorial core.",
              "They cannot prove production pack behavior, semantic retrieval, runtime or pixels.",
              "Both moral and physical transformation inputs require later full-core regression."],
    "cases": diagnostics,
})
print(json.dumps({"inventory_rows":len(terms),"kind_counts":dict(Counter(x["row_kind"] for x in terms)),
    "domains":dict(Counter(x["domain"] for x in terms)), "corpus":snapshot["counts"],
    "selected_profiles":len(selected), "source_files":len(snapshot["source_files"]),
    "diagnostics":[{"id":x["id"],"hard":[h["profile_id"] for h in x["actual"]["hits"] if h.get("hard_eligible")]}
                    for x in diagnostics]},ensure_ascii=False))
