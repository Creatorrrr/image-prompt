"""Merge authored records by identity without copying any generated index."""
from __future__ import annotations
import copy
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

PRIMARY = Path('/Users/chasoik/Projects/image-prompt')
DEST = Path('/Users/chasoik/.codex/worktrees/vocaloid-main-merge/image-prompt')
E = Path('docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004')
HERE = PRIMARY / E / 'main-merge'
LOCAL_HEAD = 'b9b28a680b7db4c30f07fae780ae8b6fc8a9b031'
REMOTE_HEAD = subprocess.check_output(['git', 'rev-parse', 'origin/main'], cwd=PRIMARY, text=True).strip()
MISSING = object()
conflicts = []
ref_conflicts = []
def sha(b): return hashlib.sha256(b).hexdigest()
def canonical(x): return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
def identity(x):
    if isinstance(x, dict) and x.get('id'): return ('id', x['id'])
    if isinstance(x, dict) and {'dimension', 'target', 'property'} <= set(x):
        return ('effect', x['dimension'], x['target'], x['property'])
    return ('value', canonical(x))
def merge(b, o, t, path):
    if o == b: return copy.deepcopy(t) if t is not MISSING else MISSING
    if t == b or o == t: return copy.deepcopy(o) if o is not MISSING else MISSING
    if path.endswith('/maintenance_ref'):
        ref_conflicts.append({'path': path, 'local': o, 'remote': t})
        return copy.deepcopy(o)
    if isinstance(o, dict) and isinstance(t, dict) and (isinstance(b, dict) or b is MISSING):
        b = {} if b is MISSING else b
        result = {}
        for key in dict.fromkeys([*b, *t, *o]):
            v = merge(b.get(key, MISSING), o.get(key, MISSING), t.get(key, MISSING), path + '/' + key)
            if v is not MISSING: result[key] = v
        return result
    if isinstance(o, list) and isinstance(t, list) and (isinstance(b, list) or b is MISSING):
        b = [] if b is MISSING else b
        maps = [{identity(x): x for x in items} for items in (b, o, t)]
        if any(len(m) != len(items) for m, items in zip(maps, (b, o, t))):
            conflicts.append({'path': path, 'reason': 'duplicate list identity'})
            return copy.deepcopy(o)
        bm, om, tm = maps
        result = []
        for key in dict.fromkeys([*bm, *tm, *om]):
            v = merge(bm.get(key, MISSING), om.get(key, MISSING), tm.get(key, MISSING), path + '/' + str(key))
            if v is not MISSING: result.append(v)
        return result
    conflicts.append({'path': path, 'base': None if b is MISSING else b,
                      'local': None if o is MISSING else o, 'remote': None if t is MISSING else t})
    return copy.deepcopy(o)

ledger = json.loads((PRIMARY / E / 'INTEGRATION-LEDGER.json').read_text())
outputs = []
for item in ledger['source_files']:
    path = item['path']
    previous = subprocess.run(['git', 'show', LOCAL_HEAD + ':' + path], cwd=PRIMARY, capture_output=True)
    base_bytes = previous.stdout if previous.returncode == 0 else b'null'
    ours_bytes = (PRIMARY / path).read_bytes()
    theirs_bytes = (DEST / path).read_bytes() if (DEST / path).exists() else b'null'
    b = json.loads(base_bytes) if previous.returncode == 0 else MISSING
    o = json.loads(ours_bytes)
    t = json.loads(theirs_bytes) if (DEST / path).exists() else MISSING
    result = merge(b, o, t, path)
    outputs.append((path, result))
    for side, content in [('local', ours_bytes), ('remote', theirs_bytes), ('base', base_bytes)]:
        dst = HERE / 'source-parents' / side / Path(path).name
        dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(content)
(HERE / 'AUTHORED-MERGE-REVIEW.json').write_text(json.dumps({
    'local_head': LOCAL_HEAD, 'remote_head': REMOTE_HEAD,
    'authored_files': len(outputs), 'conflicts': conflicts,
    'deferred_maintenance_refs': ref_conflicts,
}, ensure_ascii=False, indent=2) + '\n')
if conflicts: raise SystemExit('Inspect real authored-field conflicts before applying.')
for path, result in outputs:
    (DEST / path).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')

# This existing local registry is a dependency of six reused ca_ profiles.
# It is kept byte-identical, and its separate research directory stays local.
dependency = 'skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_character_appearance.json'
shutil.copy2(PRIMARY / dependency, DEST / dependency)
script = DEST / 'skills/photo-prompt-image-generator/scripts/prompt_generator.py'
text = script.read_text()
needle = '    "photo_prompt_visual_obligations_subculture_appearance.json",\n'
assert text.count(needle) == 1
assert '"photo_prompt_visual_obligations_character_appearance.json"' not in text
script.write_text(text.replace(needle, needle + '    "photo_prompt_visual_obligations_character_appearance.json",\n'))

maintenance = Path('docs/research-evidence/photo-prompt/extension-maintenance')
for name in ledger['maintenance_records']:
    # The recorded values may be paths or descriptive objects.
    path = name if isinstance(name, str) else name.get('path') or name.get('file')
    if path:
        source = PRIMARY / path
        if not source.exists(): source = PRIMARY / maintenance / path
        target = DEST / maintenance / source.name
        target.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(source, target)
for source in (PRIMARY / maintenance).glob('*vocaloid-equivalents-20261004.json'):
    target = DEST / maintenance / source.name
    target.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(source, target)
for path, result in outputs:
    ref = result.get('maintenance_ref')
    if not ref: continue
    source_hash = sha(canonical({k: v for k, v in result.items() if k != 'maintenance_ref'}))
    old_path = DEST / maintenance / (ref['record_id'] + '.json')
    old = json.loads(old_path.read_text())
    if old.get('authored_source_sha256') == source_hash: continue
    new = copy.deepcopy(old)
    new['record_id'] = Path(path).stem + '-vocaloid-main-merge-20261004'
    new['authored_source_sha256'] = source_hash
    new['merge_lineage'] = {
        'local_head': LOCAL_HEAD, 'remote_head': REMOTE_HEAD,
        'local_reference': ref,
        'remote_reference': json.loads((HERE / 'source-parents/remote' / Path(path).name).read_text()).get('maintenance_ref'),
        'preserved': 'both authored meanings and all historical maintenance records',
    }
    new_path = DEST / maintenance / (new['record_id'] + '.json')
    assert not new_path.exists()
    new_path.write_text(json.dumps(new, ensure_ascii=False, indent=2) + '\n')
    result['maintenance_ref'] = {**ref, 'record_id': new['record_id'], 'sha256': sha(canonical(new))}
    (DEST / path).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'authored_files': len(outputs), 'conflicts': len(conflicts),
                  'deferred_refs_resolved': len(ref_conflicts), 'dependency_sha256': sha((DEST / dependency).read_bytes())}))
