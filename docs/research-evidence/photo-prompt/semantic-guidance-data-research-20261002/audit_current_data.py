"""Read-only, local checks supporting the data-only research agenda.

No prompt construction, retrieval experiment, embedding request, or generation call.
The notebook records the exact executed checks and their observed stdout.
"""
from pathlib import Path
import contextlib
import io
import json

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]

CHECKS = [
    '''from pathlib import Path
from collections import Counter
from datetime import datetime, timezone, timedelta
import hashlib, json, sys
root = Path.cwd()
skill = root / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(skill / "scripts"))
import prompt_generator as pg
profiles = pg.load_visual_obligation_registry(skill / "assets/photo_prompt_visual_obligations.json")["profiles"]
by_id = {p["id"]: p for p in profiles}
counts = {
    "profiles": len(profiles),
    "unique_profile_ids": len(by_id),
    "runtime_expression_default_modes": dict(Counter(p["runtime_expression"].get("default_mode") for p in profiles)),
    "profiles_with_context_disambiguation": sum(bool(p["activation"].get("context_disambiguation")) for p in profiles),
    "profiles_with_runtime_forbidden_labels": sum(bool(p["runtime_expression"].get("runtime_forbidden_labels")) for p in profiles),
}
restricted = [p for p in profiles if p["runtime_expression"].get("runtime_forbidden_labels")]
counts["restricted_profiles_by_category"] = dict(Counter(p["category"] for p in restricted))
counts["restricted_profiles_by_default_mode"] = dict(Counter(p["runtime_expression"].get("default_mode") for p in restricted))
pfe_raw = json.loads((skill / "assets/photo_prompt_visual_obligations_portrait_fashion_exposure.json").read_text())
pfe_ids = {p["id"] for p in pfe_raw["profiles"]}
pfe = [p for p in profiles if p["id"] in pfe_ids]
counts["portrait_fashion_extension"] = {
    "profiles": len(pfe),
    "default_modes": dict(Counter(p["runtime_expression"].get("default_mode") for p in pfe)),
    "nonempty_runtime_forbidden_labels": sum(bool(p["runtime_expression"].get("runtime_forbidden_labels")) for p in pfe),
    "nonempty_forbidden_prompt_terms": sum(bool(p["runtime_expression"].get("forbidden_prompt_terms")) for p in pfe),
    "nonempty_prompt_label_terms": sum(bool(p["runtime_expression"].get("prompt_label_terms")) for p in pfe),
}
print(json.dumps(counts, ensure_ascii=False, indent=2))''',
    '''selected_ids = [
    "aircraft_pilot_operation", "one_piece_dress_construction",
    "embodied_corruption_transition", "kuudere_composed_warmth_relation",
    "pfe_cowl", "clothing_ct037_v1", "pfe_one_shoulder", "pfe_ruching",
    "sheer_garment_optical_layering", "clothing_ct023_v2", "clothing_ct090_v2",
    "split_diopter_dual_focus_planes", "film_halation_highlight_edge_relation",
    "contrapposto_weight_shift", "tribhanga_three_bend_pose",
    "broad_face_light_orientation_relation", "short_face_light_orientation_relation",
    "cr_warm_foreground", "cr_cool_foreground",
]
selected = []
for ident in selected_ids:
    p = by_id[ident]
    semantics = p["semantics"]
    selected.append({
        "id": ident,
        "definition": semantics["definition"],
        "paraphrase_examples": semantics.get("paraphrase_examples", []),
        "contrast_examples": semantics.get("contrast_examples", []),
        "context_disambiguation": p["activation"].get("context_disambiguation"),
        "default_mode": p["runtime_expression"].get("default_mode"),
        "authored_components": p.get("authored_components", []),
        "claim_limits": semantics.get("claim_limits", []),
    })
print(json.dumps({"selected_existing_profiles": len(selected), "ids": selected_ids}, ensure_ascii=False, indent=2))''',
    '''manifest_path = root / "docs/analysis/2026-10-02-visual-semantics-data-audit/source-manifest.json"
manifest = json.loads(manifest_path.read_text())
source_files = []
for entry in manifest["files"]:
    data = (root / entry["path"]).read_bytes()
    observed = hashlib.sha256(data).hexdigest()
    source_files.append({"path": entry["path"], "sha256": observed, "bytes": len(data), "matches_prior_audit": observed == entry["sha256"]})
integrity = {
    "source_files_checked": len(source_files),
    "all_match_prior_audit": all(x["matches_prior_audit"] for x in source_files),
    "mismatches": [x["path"] for x in source_files if not x["matches_prior_audit"]],
    "prior_audit_commit": manifest["commit"],
}
print(json.dumps(integrity, ensure_ascii=False, indent=2))
assert integrity["all_match_prior_audit"], "Source drift requires re-evaluation"''',
]


def main():
    assert Path.cwd().resolve() == ROOT, f"Run from repository root: {ROOT}"
    scope = {}
    cells = [{
        "cell_type": "markdown", "metadata": {},
        "source": [
            "# Data-only semantic guidance research checks\n",
            "Grain: one loaded visual-obligation profile.\n",
            "Counts describe authored metadata, not knowledge gaps, censorship, or image success.\n",
            "Selected profiles are a purposive review sample, not an estimate of dataset-wide quality.\n",
        ],
    }]
    for n, code in enumerate(CHECKS, 1):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            exec(compile(code, f"research-check-{n}", "exec"), scope)
        cells.append({
            "cell_type": "code", "metadata": {}, "execution_count": n,
            "source": code.splitlines(keepends=True),
            "outputs": [{"output_type": "stream", "name": "stdout", "text": stream.getvalue().splitlines(keepends=True)}],
        })
        print(stream.getvalue(), end="")
    captured = scope["datetime"].now(scope["timezone"](scope["timedelta"](hours=9))).isoformat()
    audit = {
        "captured_at_kst": captured,
        "counts": scope["counts"],
        "integrity": scope["integrity"],
        "source_files": scope["source_files"],
        "selected_profiles": scope["selected"],
        "limitations": [
            "Optional metadata sparsity is not evidence of an error.",
            "Runtime-forbidden labels are authoring configuration, not observed model blocking.",
            "No model knowledge, retrieval accuracy, moderation, generated image, or user acceptance was evaluated.",
        ],
    }
    (OUT / "PROFILE-AUDIT.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n")
    notebook = {
        "cells": cells,
        "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}, "language_info": {"name": "python", "version": scope["sys"].version.split()[0]}},
        "nbformat": 4, "nbformat_minor": 4,
    }
    (OUT / "data-research-checks.ipynb").write_text(json.dumps(notebook, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
