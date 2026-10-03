"""Integrate reviewed acting data through existing authored-data contracts."""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
RESEARCH = HERE.parent / "acting-expression-semantics-20261003"
RECORDS = HERE.parent / "extension-maintenance"
VISUAL = "photo_prompt_visual_obligations_acting_expression.json"
CANDIDATES = "photo_prompt_acting_expression_extension.json"


def read(path):
    return json.loads(path.read_text())


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def digest(data):
    return hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main():
    for name in (VISUAL, CANDIDATES):
        if (ASSETS / name).exists():
            raise RuntimeError(f"Refusing to overwrite an existing integrated file: {name}")
    extension = copy.deepcopy(read(RESEARCH / "DRAFT-CANDIDATE-EXTENSION.json"))
    visual = copy.deepcopy(read(RESEARCH / "DRAFT-VISUAL-PROFILES.json"))
    proposals = {r["id"]:r for r in read(RESEARCH / "PROPOSED-DATA.json")["concepts"]}
    record_id = "acting-expression-20261003-v1"
    record = dict(contract_version="photo-extension-maintenance-record/v1", record_id=record_id, maintenance_only=True,
        based_on_commit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        research_reference="docs/research-evidence/photo-prompt/acting-expression-semantics-20261003/RESEARCH.md",
        source_records=read(RESEARCH / "SOURCES.json"),
        concept_proposals=list(proposals.values()),
        routing=read(RESEARCH / "TERM-DECISIONS.json"),
        judgment_boundary="Terminology and authored forms are not verified feelings, sincerity, consent, timing, voice, or universal preferences.",
        integration_decisions=["Merge the duplicate own-hand/own-mouth idiom into the local form candidate.", "Keep broad emotions and media functions advisory; no new fixed emotion-to-face hard profiles.", "Keep temporal/audio/method/explicit-reference terms in external maintenance records, not static render candidates.", "Context guards depend on frozen primary context, never the candidate's own tags.", "All actual pose/expression/eyeline effects are declared; owner is bound at composition."])
    write(RECORDS / (record_id + ".json"), record)
    extension["maintenance_ref"] = dict(contract_version="photo-extension-maintenance-ref/v1", record_id=record_id, sha256=digest(record))
    # Both draft rows denote the same own-hand/own-mouth configuration.
    extension["slots"]["hand_pose"] = [r for r in extension["slots"]["hand_pose"] if r["id"] != "ae_mouth_cover_idiom"]
    own = next(r for r in extension["slots"]["hand_pose"] if r["id"] == "ae_hand_mouth")
    own["aliases"].extend(["입틀막", "손으로 자기 입 가리기"])
    own["keywords"] = own["aliases"][:]

    context_cues = {
        "ae_polite_smile": ["polite", "courteous", "politeness", "공손", "예의"],
        "ae_sneer_variant": ["contempt", "contemptuous", "disdain", "경멸"],
        "ae_wry_variant": ["wry", "irony", "ironic", "difficult", "씁쓸", "곤란"],
        "ae_bashful_direct": ["shy", "bashful", "shyness", "수줍"],
        "ae_coy_variant": ["coy", "reserve", "reserved", "새침"],
        "ae_coquettish_variant": ["flirting", "flirtatious", "flirtation", "coquettish", "플러팅", "교태"],
        "ae_sultry_variant": ["attraction", "alluring", "seductive", "sensual", "매혹", "유혹"],
        "ae_smolder_anger": ["anger", "angry", "restrained", "분노"],
        "ae_smolder_attraction": ["attraction", "alluring", "flirting", "seductive", "매혹", "유혹"],
        "ae_deadpan_form": ["deadpan", "impassive", "데드팬"],
        "ae_restrained_anger": ["anger", "angry", "분노"],
        "ae_smile_tears": ["tears", "tearful", "crying", "눈물", "울음"],
        "ae_service_smile": ["service", "customer", "reception", "응대"],
        "ae_mugging_variant": ["mugging", "comic", "comedy", "reaction", "코미디", "리액션"],
    }
    contexts = {}
    for slot, rows in extension["slots"].items():
        for row in rows:
            proposal = proposals[row["id"]]
            row["tags"] = ["human", "acting_expression", slot]
            row["relations"][0]["object"] = "the declared actor's stated " + ("hand-to-own-mouth contact" if slot == "hand_pose" else "head orientation and eyeline" if slot == "body_orientation" else "local face and eye configuration")
            if row["id"] in context_cues:
                row["requires_primary_any_tags"] = context_cues[row["id"]]
                row["contextual_usage"] = dict(contexts=[dict(id=row["id"] + "_portrayal_context", application_conditions=proposal["context_requirements"], limits=proposal["confusion_boundaries"], status="optional_contextual_portrayal_not_hidden_state_inference")])
            if row["id"] in {"ae_coquettish_variant", "ae_sultry_variant", "ae_smolder_attraction"}:
                row["requires_all_tags"] = ["adult"]
            if row["id"] == "ae_lip_tighten":
                row["concept_units"][1] = "a relatively straight mouth line accompanies the taut lip margins"
                row["en"] = "; ".join(row["concept_units"])
            if row["id"] == "ae_polite_smile":
                row["en"] = "a small closed-mouth smile within the established polite encounter"
                row["concept_units"] = ["the actor forms a small closed-mouth smile", "the polite encounter and addressee are already established"]
            # Index positive form/context text, never limitations or source prose.
            row["embedding_text"] = "; ".join([row["ko"], row["en"], *row["aliases"]])

    # Extend only equivalent positive forms. Context notes do not rewrite labels, effects or guards.
    for target in read(RESEARCH / "REUSE-PLAN.json")["reuse"]:
        proposal = proposals[target["concept_id"]]
        contexts.setdefault(target["slot"], {})[target["existing_candidate_id"]] = dict(paraphrases=[proposal["en"]], contexts=[dict(id=proposal["id"] + "_acting_reuse", limits=proposal["confusion_boundaries"], application_conditions=proposal["context_requirements"], status="optional_interpretation_not_emotion_diagnosis")])
    # playful_smirk is playful, not every self-satisfied/dominance smile.
    contexts["expression"]["playful_smirk"]["paraphrases"] = ["a small smile within the already established playful portrayal"]
    contexts["expression"]["ctx_c126"] = dict(contexts=[dict(id="ae_task_lip_bite_reuse", application_conditions=["Only an established adult concentrating on the requested task; preserve original action/expression effects."], limits=["Lip contact alone is not sexual tone, anxiety level or real desire."], status="task_context_preserved")])
    extension["existing_slot_context_extensions"] = contexts

    for profile in visual["profiles"]:
        profile["concept_candidate"]["concept_terms"] = list(dict.fromkeys(profile["concept_candidate"]["concept_terms"]))
        if profile["id"] == "ae_profile_lip_tighten":
            old = "the mouth is not rounded into a protruding pucker"
            new = "a relatively straight mouth line accompanies the taut lip margins"
            for key in ("definition",):
                profile["semantics"][key] = profile["semantics"][key].replace(old, new)
            profile["semantics"]["visual_components"] = [v.replace(old,new) for v in profile["semantics"]["visual_components"]]
            profile["concept_candidate"]["concept_terms"] = [v.replace(old,new) for v in profile["concept_candidate"]["concept_terms"]]
            component = profile["authored_components"]["components"][1]
            for key in ("match_terms", "evidence_terms"):
                component[key] = [v.replace(old,new) for v in component[key]]
            component["instruction"] = component["instruction"].replace(old,new)
            component["render_gate"]["description"] = component["render_gate"]["description"].replace(old,new)
    for bundle in extension["visual_semantics"]:
        if bundle["id"] == "ae_bundle_lip_tighten":
            old = "the mouth is not rounded into a protruding pucker"
            new = "a relatively straight mouth line accompanies the taut lip margins"
            bundle["primary_visual_proposition"] = bundle["primary_visual_proposition"].replace(old,new)
            bundle["component_groups"][1]["visible_evidence"] = [new]

    write(ASSETS / VISUAL, visual)
    write(ASSETS / CANDIDATES, extension)
    tags = read(ASSETS / "photo_prompt_tags.json")
    required = tags["candidate_semantic_policy"]["required_extensions"]
    if CANDIDATES not in required:
        required.append(CANDIDATES)
    write(ASSETS / "photo_prompt_tags.json", tags)
    write(HERE / "INTEGRATION-RECEIPT.json", dict(source_commit=record["based_on_commit"], visual_profiles=len(visual["profiles"]), new_candidates=sum(map(len,extension["slots"].values())), bundles=len(extension["visual_semantics"]), reused_context_targets=sum(map(len,contexts.values())), context_guard_ids=list(context_cues), metadata_record=record_id, deduplicated_candidate="ae_mouth_cover_idiom merged into ae_hand_mouth", status="authored_data_written; manifests and indexes pending"))
    print(json.dumps(dict(profiles=len(visual["profiles"]),new_candidates=sum(map(len,extension["slots"].values())),reused_targets=sum(map(len,contexts.values())))))


if __name__ == "__main__":
    main()
