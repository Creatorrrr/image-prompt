"""Compare every individually snapshotted preexisting file without restoring edits."""
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
before = json.loads((HERE / "PRIMARY-BEFORE.json").read_text())
intended = {
    "skills/photo-prompt-image-generator/SKILL.md",
    "skills/photo-prompt-image-generator/references/embodiment-preflight.md",
    "skills/photo-prompt-image-generator/references/image-runtime.md",
    "skills/photo-prompt-image-generator/scripts/photo_workflow.py",
    "skills/photo-prompt-image-generator/assets/photo_prompt_wardrobe_owner_relations_extension.json",
    "skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_wardrobe_owner_relations.json",
    "skills/photo-prompt-image-generator/assets/photo_prompt_clothing_structure_extension.json",
    "skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_clothing_structure.json",
    "skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index.json",
    "skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json",
    "tests/test_photo_wardrobe_owner_relations.py",
}
unchanged, changed, missing = [], [], []
for row in before["files"]:
    path = ROOT / row["path"]
    if not path.is_file():
        missing.append(row["path"])
        continue
    current = hashlib.sha256(path.read_bytes()).hexdigest()
    if current == row["sha256"]:
        unchanged.append(row["path"])
    else:
        changed.append({"path": row["path"], "before_sha256": row["sha256"],
                        "current_sha256": current, "intended": row["path"] in intended})
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
unexpected = [row for row in changed if not row["intended"]]
old_evidence = "docs/research-evidence/photo-prompt/wardrobe-keyword-integration-20261010/"
result = {"schema_version": "wardrobe-preexisting-file-preservation/v1",
          "status": "PASS" if not missing and not unexpected and head == before["head"] and branch == before["branch"] else "REVIEW_REQUIRED",
          "snapshotted_file_count": len(before["files"]), "unchanged_file_count": len(unchanged),
          "intended_changed_files": [r for r in changed if r["intended"]], "unexpected_changed_files": unexpected,
          "missing_files": missing, "head_before": before["head"], "head_after": head,
          "branch_before": before["branch"], "branch_after": branch,
          "preexisting_old_integration_files_unchanged": sum(p.startswith(old_evidence) for p in unchanged),
          "scope": "Every individual preexisting dirty/untracked file captured before this task; newly created files and external runtime cache are separate.",
          "commit_created": False, "push_performed": False}
(HERE / "PRESERVATION-VERIFICATION.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k:v for k,v in result.items() if k not in {"intended_changed_files"}}, ensure_ascii=False))
