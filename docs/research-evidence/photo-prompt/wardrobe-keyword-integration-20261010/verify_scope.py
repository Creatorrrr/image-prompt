"""Compare pre-existing work with the task's declared source/index writes."""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = 'skills/photo-prompt-image-generator/assets/'
ALLOWED = {ASSETS + name for name in (
    'photo_prompt_source_manifest.json',
    'photo_prompt_semantic_index.json',
    'photo_prompt_visual_profile_index.json',
)}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    before = json.loads((HERE / 'PRIMARY-BEFORE.json').read_text())
    changed, missing, unchanged, unchecked = [], [], [], []
    for row in before['existing_dirty']:
        path = ROOT / row['path']
        if row.get('is_directory') or not row.get('sha256'):
            unchecked.append(row['path'])
        elif not path.is_file():
            missing.append(row['path'])
        elif sha(path) != row['sha256']:
            changed.append(row['path'])
        else:
            unchanged.append(row['path'])
    asset_changes = []
    for relative, digest in before['assets_before'].items():
        path = ROOT / relative
        if not path.is_file() or sha(path) != digest:
            asset_changes.append(relative)
    manifest_path = ASSETS + 'photo_prompt_source_manifest.json'
    with ZipFile(HERE / 'PRIMARY-ASSETS-BEFORE.zip') as archive:
        old = json.loads(archive.read(manifest_path))
        skill_same = archive.read('skills/photo-prompt-image-generator/SKILL.md') == (ROOT / 'skills/photo-prompt-image-generator/SKILL.md').read_bytes()
    new = json.loads((ROOT / manifest_path).read_text())
    retained = all(row in new['sources'] for row in old['sources'])
    additions = [row for row in new['sources'] if row not in old['sources']]
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    violations = sorted((set(changed) | set(asset_changes)) - ALLOWED)
    result = {
        'status': 'PASS' if not missing and not violations and retained and len(additions) == 2 and skill_same and head == before['head'] else 'FAIL',
        'original_head': before['head'], 'current_head': head,
        'existing_dirty_files_byte_unchanged': len(unchanged),
        'allowed_preexisting_files_changed': sorted(set(changed) & ALLOWED),
        'existing_asset_files_checked': len(before['assets_before']),
        'asset_files_changed': sorted(asset_changes),
        'unrelated_changed': violations, 'missing_original_files': missing,
        'directory_status_entries_not_byte_snapshotted': unchecked,
        'all_original_manifest_rows_retained_exactly': retained,
        'new_manifest_rows': additions, 'canonical_skill_byte_unchanged': skill_same,
        'canonical_skill_sha256': sha(ROOT / 'skills/photo-prompt-image-generator/SKILL.md'),
        'commit_created': False, 'push_performed': False,
        'boundary': 'Compares all individually hashed initial dirty files and the 142 asset files; directory-only status rows are explicitly not byte snapshots.',
    }
    (HERE / 'SCOPE-VERIFICATION.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print({k: result[k] for k in ('status', 'existing_dirty_files_byte_unchanged', 'unrelated_changed', 'missing_original_files', 'all_original_manifest_rows_retained_exactly', 'canonical_skill_byte_unchanged')})
    raise SystemExit(0 if result['status'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
