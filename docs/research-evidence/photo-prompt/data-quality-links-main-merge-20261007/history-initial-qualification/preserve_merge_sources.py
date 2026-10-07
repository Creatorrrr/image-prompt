"""Offline authoring: pin V32, upstream V33 and local V33 without replacing either."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
BASE = '96e20422316276a4e0b5ed97f44152e4931e7504'
LOCAL = 'd9dc3df7012f395c48d536ee9df80df060cd24f9'
UPSTREAM = 'c4c0e4ed25981fc46c09de6e138247b5788ea43c'
PHOTO = 'skills/photo-prompt-image-generator/assets/'
ILLUSTRATION = 'skills/subculture-illustration-image-generator/'
LOCAL_ROOT = 'docs/research-evidence/photo-prompt/data-quality-links-20261007/history/'
UPSTREAM_ROOT = 'docs/research-evidence/photo-prompt/color-palette-main-merge-20261007/'
MUTABLE = frozenset({
    'tests/photo_prompt_fixtures.py', 'tests/test_photo_data_scope_boundary_history.py',
    'tests/test_photo_palette_boundary_history.py', 'tests/test_photo_robe_source_boundary_history.py',
    ILLUSTRATION + 'scripts/validate_illustration_assets.py',
    ILLUSTRATION + 'assets/universal_scene_baseline_v2.json',
})


def git_bytes(pin, name):
    return subprocess.check_output(['git', 'show', pin + ':' + name], cwd=ROOT)


def load(pin, name):
    return json.loads(git_bytes(pin, name))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def blob(raw):
    return hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def raw_changes(pin):
    # git show is read-only. Use full blob identities and the newest mode per path.
    raw = subprocess.check_output(['git', 'show', '--raw', '--no-abbrev', '--format=', BASE + '..' + pin], cwd=ROOT, text=True)
    changes = {}
    for line in raw.splitlines():
        if not line.startswith(':') or '\t' not in line:
            continue
        fields, name = line.split('\t', 1)
        old_mode, mode, old_blob, git_blob, status = fields[1:].split()
        if status not in ('A', 'M', 'D'):
            raise AssertionError('Unsupported source overlay status: ' + status)
        changes.setdefault(name, (mode, git_blob, status))
    return changes


def reusable_path(name, raw, mode, candidates):
    for candidate in dict.fromkeys(candidates):
        if candidate == name and name in MUTABLE:
            continue
        path = ROOT / candidate
        if (path.is_file() and not path.is_symlink()
                and path.stat().st_mode & 0o7777 == int(mode[-3:], 8)
                and path.read_bytes() == raw):
            return candidate
    return None


def backing(stage, name, raw, mode, candidates):
    source = reusable_path(name, raw, mode, candidates)
    if source is not None:
        return source, 'reuse_exact_authenticated_bytes'
    source = (HERE / 'source-files' / stage / name).relative_to(ROOT).as_posix()
    path = ROOT / source
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != raw:
        raise AssertionError('Refusing to revise preserved source: ' + source)
    path.write_bytes(raw)
    path.chmod(int(mode[-3:], 8))
    return source, 'new_immutable_snapshot_same_git_blob'


def save(stage, pin, rows, environment, **extra):
    tree = subprocess.check_output(['git', 'show', '-s', '--format=%T', pin], cwd=ROOT, text=True).strip()
    result = dict(schema='photo-merge-history-source/v1', stage=stage, source_pin=pin, source_tree=tree,
                  environment=environment, member_count=len(rows), total_member_bytes=sum(r['bytes'] for r in rows),
                  counts={kind: sum(r['kind'] == kind for r in rows) for kind in sorted({r['kind'] for r in rows})},
                  members=sorted(rows, key=lambda r: r['path']), **extra)
    path = HERE / ('SOURCE-' + stage.upper() + '.json')
    path.write_bytes(encoded(result))
    print(stage, len(rows), result['total_member_bytes'], sha(path.read_bytes()), result['counts'])
    return result, path


def main():
    old = load(LOCAL, LOCAL_ROOT + 'V32-PARENT-SOURCE.json')
    palette_parent = load(UPSTREAM, UPSTREAM_ROOT + 'V32-PARENT-SOURCE.json')
    old_rows = {r['path']: r for r in old['members']}
    palette_rows = {r['path']: r for r in palette_parent['members']}
    v32_environment = load(BASE, 'docs/research-evidence/photo-prompt/robe-back-source-consistency-20261006/CURRENT-GENERATION.json')['source']['environment']
    base_rows = []
    for name, row in old_rows.items():
        candidates = [row['source_path'], palette_rows.get(name, {}).get('source_path', ''), name]
        raw = None
        for candidate in candidates:
            path = ROOT / candidate
            if candidate and path.is_file() and not path.is_symlink():
                candidate_raw = path.read_bytes()
                if sha(candidate_raw) == row['sha256'] and blob(candidate_raw) == row['git_blob']:
                    raw = candidate_raw
                    break
        if raw is None:
            raw = git_bytes(BASE, name)
        if len(raw) != row['bytes'] or sha(raw) != row['sha256'] or blob(raw) != row['git_blob']:
            raise AssertionError('Original V32 identity drift: ' + name)
        source, kind = backing('v32', name, raw, row['mode'], candidates)
        base_rows.append(dict(row, source_path=source, kind=kind))
    base, base_path = save('v32', BASE, base_rows, v32_environment)
    for stage, pin, root, proof_name, tests in (
        ('local-v33', LOCAL, LOCAL_ROOT, 'V33-DATA-SCOPE-PROOF.json', ['tests/test_photo_data_scope_boundary_history.py']),
        ('upstream-v33', UPSTREAM, UPSTREAM_ROOT, 'V33-PALETTE-DATA-PROOF.json', ['tests/photo_palette_history.py', 'tests/test_photo_palette_boundary_history.py']),
    ):
        proof = load(pin, root + proof_name)
        needed = set(old_rows) | set(tests) | {'tests/photo_prompt_fixtures.py',
            'tests/test_photo_robe_source_boundary_history.py', ILLUSTRATION + 'scripts/validate_illustration_assets.py',
            ILLUSTRATION + 'assets/universal_scene_baseline_v2.json', ILLUSTRATION + 'assets/photo_regression_baseline_v33.json',
            ILLUSTRATION + 'assets/photo_regression_baseline_v33_pack.json', root + proof_name, root + 'V32-PARENT-SOURCE.json'}
        for field in ('source_files_after', 'active_shards_after', 'retained_shards_before', 'frozen_inputs', 'evidence_files'):
            needed.update(proof[field])
        parent = load(pin, root + 'V32-PARENT-SOURCE.json')
        needed.update(row['source_path'] for row in parent['members'])
        if 'maintenance_successor' in proof:
            needed.add(proof['maintenance_successor']['path'])
        if stage == 'local-v33':
            # Exact original helper constants bind these preserved support/evidence files.
            changes = raw_changes(pin)
            needed.update(name for name in changes if name.startswith(LOCAL_ROOT))
        else:
            changes = raw_changes(pin)
        current = {r['path']: r for r in base_rows}
        rows = []
        for name in sorted(needed):
            changed = changes.get(name)
            if name in current and changed is None:
                rows.append(dict(current[name], git_commit=pin, git_path=name))
                continue
            raw = git_bytes(pin, name)
            mode = changed[0] if changed else current.get(name, {}).get('mode', '100644')
            if changed and (changed[2] == 'D' or blob(raw) != changed[1]):
                raise AssertionError('Overlay Git identity drift: ' + name)
            candidates = [name]
            if name in current:
                candidates.append(current[name]['source_path'])
            source, kind = backing(stage, name, raw, mode, candidates)
            rows.append(dict(path=name, source_path=source, git_commit=pin, git_path=name,
                             mode=mode, bytes=len(raw), sha256=sha(raw), git_blob=blob(raw), kind=kind))
        receipt = load(pin, root + 'CURRENT-BOUNDARY-RECEIPT.json')
        # Both qualified V33 branches recorded the same 3.14.3 algorithm binding.
        environment = dict(implementation='cpython', python=[3, 14, 3], unicode='16.0.0')
        save(stage, pin, rows, environment, base_manifest=base_path.relative_to(ROOT).as_posix(),
             base_manifest_sha256=sha(base_path.read_bytes()), original_proof=root + proof_name,
             original_proof_sha256=sha(git_bytes(pin, root + proof_name)),
             original_receipt_sha256=sha(git_bytes(pin, root + 'CURRENT-BOUNDARY-RECEIPT.json')),
             original_generation_id=receipt['generation_id'])


if __name__ == '__main__':
    main()
