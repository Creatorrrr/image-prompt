"""Check both main's authored meaning and this task's original evidence."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PIN = 'f6b2f88fc9adeae0dfe59b78a7a0ecafc7b4c03a'
FEATURE = 'b93bcbbb76cf33669f9edc341ca7d449e8fe4fde'
PHOTO = Path('skills/photo-prompt-image-generator')
ILL = Path('skills/subculture-illustration-image-generator')

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def main():
    paths = git('ls-tree', '-r', '--name-only', PIN).decode().splitlines()
    protected = [n for n in paths if (
        n.startswith(str(PHOTO / 'assets') + '/') and n.endswith('.json')
        and '_index_shards/' not in n
        and Path(n).name not in {'photo_prompt_source_manifest.json', 'photo_prompt_semantic_index.json', 'photo_prompt_visual_profile_index.json'}
    ) or (
        n.startswith(str(ILL / 'assets/photo_regression_baseline_v')) and n.endswith('.json')
    ) or (
        n.startswith(str(PHOTO / 'scripts') + '/') and n.endswith('.py')
    ) or n == str(PHOTO / 'SKILL.md')]
    changed = [n for n in protected if (ROOT / n).read_bytes() != git('show', PIN + ':' + n)]
    assert not changed, ('Main authored source, historical baseline or runtime was rewritten', changed)
    evidence_prefixes = (
        'docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007/',
        'docs/research-evidence/photo-prompt/ethereal-gothic-research-20261007/',
    )
    feature_paths = git('ls-tree', '-r', '--name-only', FEATURE).decode().splitlines()
    original_evidence = [n for n in feature_paths if n.startswith(evidence_prefixes)]
    assert all((ROOT / n).read_bytes() == git('show', FEATURE + ':' + n) for n in original_evidence)
    photo_sources = [PHOTO / 'assets' / n for n in ('photo_prompt_ethereal_gothic_scene_extension.json', 'photo_prompt_visual_obligations_ethereal_gothic_scene.json')]
    assert all((ROOT / n).read_bytes() == git('show', FEATURE + ':' + str(n)) for n in photo_sources)
    parent = json.loads((HERE / 'history/V34-PARENT-SOURCE.json').read_text())
    for row in parent['members']:
        path = ROOT / row['source_path']
        raw = path.read_bytes()
        assert sha(raw) == row['sha256']
        assert hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest() == row['git_blob']
        assert path.stat().st_mode & 0o7777 == int(row['mode'][-3:], 8)
    active = []
    for name in ('photo_prompt_semantic_index.json', 'photo_prompt_visual_profile_index.json'):
        manifest = json.loads((ROOT / PHOTO / 'assets' / name).read_text())
        active.extend((PHOTO / 'assets' / row['path']).as_posix() for row in manifest['shards'])
    assert len(active) == 32 and len(set(active)) == 32
    assert not (ROOT / PHOTO / 'assets/photo_prompt_intellectual_observation_extension.json').exists()
    result = dict(status='PASS',remote_parent=PIN,feature_parent=FEATURE,protected_main_files=len(protected),main_source_rewrites=changed,original_task_evidence_files_preserved=len(original_evidence),exact_parent_members=parent['member_count'],active_generated_shards=active,unrelated_intellectual_drafts_absent=True)
    (HERE / 'FINAL-SCOPE-VERIFICATION.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'active_generated_shards'}))

if __name__ == '__main__':
    main()
