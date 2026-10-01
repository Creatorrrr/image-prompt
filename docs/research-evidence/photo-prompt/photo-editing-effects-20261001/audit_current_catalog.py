#!/usr/bin/env python3
"""Read-only survey of the current merged catalog; writes only research artifacts."""
from __future__ import annotations
import hashlib, importlib.util, json, pathlib, re, subprocess, sys, unicodedata
ROOT = pathlib.Path(__file__).resolve().parents[4]
OUT = pathlib.Path(__file__).resolve().parent
SCRIPTS = ROOT / "skills/photo-prompt-image-generator/scripts"
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
sys.path.insert(0, str(SCRIPTS))
import prompt_generator as pg

def norm(text):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", unicodedata.normalize("NFKC", str(text)).casefold())).strip()

def strings(value):
    if isinstance(value, str): return [value]
    if isinstance(value, list): return [x for x in value if isinstance(x, str)]
    return []

def labels(row):
    return [v for k in ("id", "en", "ko", "label_en", "label_ko", "keywords", "paraphrases", "concept_terms", "concept_units") for v in strings(row.get(k))]

data = pg.load_json(ASSETS / "photo_prompt_tags.json")
registry = pg.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
source_names = list(dict.fromkeys(["photo_prompt_tags.json", *pg.RESEARCH_EXTENSION_FILENAMES, "photo_prompt_visual_obligations.json", *pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES]))
origins = {}
for name in source_names:
    p = ASSETS / name
    if not p.exists(): continue
    source = json.loads(p.read_text())
    for slot, entries in source.get("slots", {}).items():
        for row in entries:
            origins.setdefault((slot, row["id"]), []).append(name)
candidates = []
for slot, entries in data["slots"].items():
    for row in entries:
        candidates.append({"id": "slot:" + slot + ":" + row["id"], "slot": slot, "entry_id": row["id"], "source_files": origins.get((slot, row["id"]), []), "labels": [norm(v) for v in labels(row)], "text": norm(json.dumps(row, ensure_ascii=False))})
profiles = []
for row in registry["profiles"]:
    sem = row.get("semantics", {})
    values = [row["id"], sem.get("definition", ""), *strings(sem.get("paraphrase_examples")), *strings(sem.get("visual_components")), *strings(row.get("activation", {}).get("exact_terms"))]
    profiles.append({"id": row["id"], "labels": [norm(v) for v in values], "text": norm(" ".join(values))})
terms = json.loads((OUT / "reference-keywords.json").read_text())["rows"]
coverage = []
for term in terms:
    label = term["label"]
    english = label.split(" / ")[0]
    aliases = [norm(english)]
    if " / " in label: aliases.append(norm(label.split(" / ", 1)[1]))
    aliases = [v for v in aliases if v]
    exact = [c for c in candidates if any(a in c["labels"] for a in aliases)]
    partial = [c for c in candidates if c not in exact and any(len(a) >= 4 and (" " + a + " ") in (" " + c["text"] + " ") for a in aliases)]
    phits = [p["id"] for p in profiles if any(len(a) >= 4 and (" " + a + " ") in (" " + p["text"] + " ") for a in aliases)]
    slim = lambda c: {k:c[k] for k in ("id", "slot", "entry_id", "source_files")}
    coverage.append({**term, "exact_label_or_alias_count": len(exact), "exact_label_or_alias_hits": [slim(c) for c in exact[:12]], "text_mention_count": len(partial), "text_mention_hits": [slim(c) for c in partial[:8]], "profile_text_mention_count": len(phits), "profile_text_mention_ids": phits[:12], "coverage_status": "lexical_hits_require_semantic_review" if exact or partial or phits else "no_lexical_hit", "runtime_retrieval_tested": False, "native_pixel_tested": False})
snapshot = {"schema_version":"photo-editing-current-catalog-survey/v1", "survey_date":"2026-10-01", "timezone":"Asia/Seoul", "git_head":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(), "method":"load_json + load_visual_obligation_registry from current prompt_generator; casefolded label/alias and bounded phrase mentions; no retrieval or image generation", "interpretation_limit":"Lexical presence is not a verified definition, an activated profile, runtime exposure, adoption, or pixel quality.", "source_files":[{"path":str((ASSETS/name).relative_to(ROOT)),"sha256":hashlib.sha256((ASSETS/name).read_bytes()).hexdigest()} for name in source_names if (ASSETS/name).exists()], "slot_counts":{k:len(v) for k,v in data["slots"].items()}, "preset_count":len(data.get("presets", [])), "candidate_count":len(candidates), "bundle_count":len(data.get("candidate_bundles", [])), "profile_count":len(profiles), "reference_row_count":len(coverage), "exact_label_or_alias_rows":sum(bool(r["exact_label_or_alias_count"]) for r in coverage), "mention_only_rows":sum(not r["exact_label_or_alias_count"] and bool(r["text_mention_count"] or r["profile_text_mention_count"]) for r in coverage), "no_lexical_hit_rows":sum(r["coverage_status"] == "no_lexical_hit" for r in coverage), "relevant_slot_dimensions":{k:data["candidate_semantic_policy"]["slot_dimensions"].get(k,[]) for k in ["lighting","light_shape","camera_type","lens","focus","motion","color","color_grading","texture","grain_profile","film_emulation","quality","format","skin_finish","composition"]}, "bundle_ids":[r["id"] for r in data.get("candidate_bundles", [])]}
(OUT/"current-catalog-snapshot.json").write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+"\n")
(OUT/"keyword-catalog-coverage.json").write_text(json.dumps({"schema_version":"photo-editing-lexical-coverage/v1","rows":coverage},ensure_ascii=False,indent=2)+"\n")
print(json.dumps({k:v for k,v in snapshot.items() if k not in {"source_files","bundle_ids","slot_counts"}},ensure_ascii=False,indent=2))
print("Relevant slots:",json.dumps({k:snapshot["slot_counts"].get(k,0) for k in snapshot["relevant_slot_dimensions"]},ensure_ascii=False))
print("No lexical hits:", [r["label"] for r in coverage if r["coverage_status"] == "no_lexical_hit"])

