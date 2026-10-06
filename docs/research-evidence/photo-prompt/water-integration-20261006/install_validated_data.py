"""Install this additive scope only if the captured authored baseline survived."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import sys

E = Path(__file__).resolve().parent
B = json.loads((E / 'BASELINE.json').read_text())
ROOT = Path(B['source_root'])
STAGE = Path(B['snapshot_root'])
sys.path.insert(0, str(ROOT / 'scripts'))
from photo_runtime_sources import source_update

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def atomic_copy(source, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    temporary = dest.with_name(dest.name + '.water-install-tmp')
    shutil.copy2(source, temporary)
    os.replace(temporary, dest)

def main():
    prior = json.loads((E/'INSTALLATION.json').read_text()) if '--refresh' in sys.argv and (E/'INSTALLATION.json').is_file() else None
    owned = {str(Path(row['path']).relative_to(ROOT)): row['sha256'] for row in (prior or {}).get('authored_files',[])}
    generated_prefixes = ('assets/photo_prompt_semantic_index', 'assets/photo_prompt_visual_profile_index')
    drift = [n for n, h in B['files'].items() if not n.startswith(generated_prefixes)
             and (not (ROOT / n).is_file() or sha(ROOT / n) != owned.get(n,h))]
    drift += [n for n,h in owned.items() if not (ROOT/n).is_file() or sha(ROOT/n)!=h]
    if drift:
        raise SystemExit('Authored baseline changed. Reconcile before install: ' + repr(drift))
    names = ['photo_prompt_water_relations_extension.json', 'photo_prompt_visual_obligations_water_relations.json']
    if prior is None and any((ROOT/'assets'/name).exists() for name in names):
        raise SystemExit('Water source already exists; refusing replacement')
    index_names = ['photo_prompt_semantic_index.json', 'photo_prompt_visual_profile_index.json']
    # Referenced vector shards are copied before the manifest switch. Existing
    # generations remain available to old readers and are never pruned here.
    copied = []
    with source_update(ROOT):
        for name in index_names:
            for shard in json.loads((STAGE/'assets'/name).read_text())['shards']:
                source=STAGE/'assets'/shard['path'];dest=ROOT/'assets'/shard['path']
                if not dest.is_file() or sha(dest)!=sha(source):
                    atomic_copy(source,dest)
                copied.append({'path':str(dest),'sha256':sha(dest)})
        for name in names + ['photo_prompt_source_manifest.json'] + index_names:
            atomic_copy(STAGE/'assets'/name, ROOT/'assets'/name)
    remaining = [n for n,h in B['files'].items() if n!='assets/photo_prompt_source_manifest.json'
                 and not n.startswith(generated_prefixes) and sha(ROOT/n)!=h]
    if remaining:
        raise SystemExit('Unrelated source drift during install: '+repr(remaining))
    report={'schema':'water-installation/v1','authored_files':[{'path':str(ROOT/'assets'/n),'sha256':sha(ROOT/'assets'/n)} for n in names + ['photo_prompt_source_manifest.json']],
            'index_manifests':[{'path':str(ROOT/'assets'/n),'sha256':sha(ROOT/'assets'/n)} for n in index_names],
            'referenced_shards':copied,'unrelated_authored_changes':remaining,'prior_generations_retained':True}
    (E/'INSTALLATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'installed_candidates':117,'installed_profiles':117,'unrelated_authored_changes':remaining}))

if __name__=='__main__':main()
