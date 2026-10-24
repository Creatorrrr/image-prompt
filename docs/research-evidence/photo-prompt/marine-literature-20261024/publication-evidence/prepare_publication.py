"""Copy only the marine research scope into an isolated publication checkout."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess

PRIMARY = Path('/Users/chasoik/Projects/image-prompt')
WORK = Path('/Users/chasoik/.codex/worktrees/marine-literature-publish/image-prompt')
REL = Path('docs/research-evidence/photo-prompt/marine-literature-20261024')
OUT = PRIMARY / REL / 'publication-evidence'
RECEIPT = PRIMARY / 'generated/publication-receipts/marine-literature-20261024'
ASSETS = Path('skills/photo-prompt-image-generator/assets')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


RECEIPT.mkdir(parents=True, exist_ok=True)
assert subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=PRIMARY) == b''
baseline_path = RECEIPT / 'protected-primary.before.json'
if not baseline_path.exists():
    rows = subprocess.check_output(['git', 'status', '--porcelain=v1', '-z', '-uno'], cwd=PRIMARY).split(b'\0')
    changed = {row[3:].decode() for row in rows if row}
    # Protect authored/code/config files too, including untracked concurrent modules.
    for folder in ['precore', 'scripts', 'references', 'tests', 'assets']:
        for file in (PRIMARY / 'skills/photo-prompt-image-generator' / folder).iterdir():
            if file.is_file() and file.suffix in ('.py', '.json', '.md'):
                changed.add(str(file.relative_to(PRIMARY)))
    changed.add('skills/photo-prompt-image-generator/SKILL.md')
    write(baseline_path, {'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=PRIMARY, text=True).strip(),
                         'index_sha256': sha(PRIMARY / '.git/index'),
                         'files': {name: sha(PRIMARY / name) for name in sorted(changed)},
                         'protection': 'Working bytes/deletions and all authored top-level modules/code; unrelated generated/staging output is never a deletion target.'})

# Preserve the original runtime-dependent regression as research evidence. Its
# newer neutral authoring dependency belongs to an independent unpublished task.
snapshot = OUT / 'runtime-dependent-regression/test_topic_title_discovery_scope.py'
snapshot.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(PRIMARY / 'skills/photo-prompt-image-generator/tests/test_topic_title_discovery_scope.py', snapshot)

originals = []
old = json.loads((PRIMARY / REL / 'integration-evidence/image-tests-summary.json').read_bytes())
for case in old['cases']:
    originals.append(('initial-' + case['arm'], Path(case['image']), case['image_sha256']))
new = json.loads((PRIMARY / REL / 'retest-20261024/test-results-summary.json').read_bytes())
for arm, case in new['arms'].items():
    originals.append(('retest-' + arm, Path(case['original']), case['original_sha256']))
mapping = []
for label, src, digest in originals:
    dest = OUT / 'originals' / (label + '.png')
    dest.parent.mkdir(parents=True, exist_ok=True)
    assert sha(src) == digest
    shutil.copyfile(src, dest)
    assert sha(dest) == digest
    mapping.append({'case': label, 'original_path': str(src), 'published_copy': str(dest.relative_to(PRIMARY)), 'sha256': digest})
write(OUT / 'published-originals.json', mapping)

names = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard', '--', str(REL)], cwd=PRIMARY, text=True).splitlines()
assert names and all(name.startswith(str(REL) + '/') for name in names)
copied = {}
for name in names:
    src, dest = PRIMARY / name, WORK / name
    assert src.is_file() and not src.is_symlink()
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    assert sha(src) == sha(dest)
    copied[name] = sha(dest)

for filename in ['photo_candidate_marine_literature_20261024.json',
                 'photo_candidate_marine_literature_bindings_20261024.json',
                 'photo_marine_literature_semantics_20261024.json']:
    src, dest = PRIMARY / ASSETS / filename, WORK / ASSETS / filename
    shutil.copyfile(src, dest)
    assert sha(src) == sha(dest)
    copied[str(ASSETS / filename)] = sha(dest)

manifest_path = WORK / ASSETS / 'photo_candidate_corpus_manifest.json'
manifest = json.loads(manifest_path.read_bytes())
parent_modules = list(manifest['modules'])
for filename, kind in [('photo_candidate_marine_literature_20261024.json', 'candidates'),
                       ('photo_candidate_marine_literature_bindings_20261024.json', 'slot_bindings')]:
    row = {'file': filename, 'kind': kind}
    assert not any(m['file'] == filename for m in manifest['modules'])
    manifest['modules'].append(row)
write(manifest_path, manifest)
write(WORK / REL / 'publication-evidence/source-scope.json', {
    'copied_files': copied, 'parent_modules_preserved': parent_modules,
    'manifest_added_modules': manifest['modules'][len(parent_modules):],
    'new_runtime_code_or_selected_runtime_config_copied': False,
    'runtime_boundary': 'Retest used an explicitly installed newer kernel. Independent unpublished neutral authoring changes and selected runtime config are preserved in the primary checkout, not silently included in this data publication.',
    'original_regression_snapshot': str(snapshot.relative_to(PRIMARY)),
})
print(json.dumps({'copied_files': len(copied), 'parent_modules': len(parent_modules), 'published_originals': len(mapping), 'worktree': str(WORK)}))
