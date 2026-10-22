"""Verify scoped Clockpunk deltas against the immutable base Git tree."""
import collections,hashlib,json,subprocess,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
ASSETS=Path('skills/photo-prompt-image-generator/assets')
OUT=Path(__file__).resolve().parent
BASE=sys.argv[1] if len(sys.argv)>1 else 'dc843183caae8abbb3c78a291b34fdc5ed34b599'
def git_json(path):return json.loads(subprocess.check_output(['git','show',BASE+':'+str(path)],cwd=ROOT))
def load(base):
    manifest=git_json(ASSETS/'photo_candidate_corpus_manifest.json') if base else json.loads((ROOT/ASSETS/'photo_candidate_corpus_manifest.json').read_text())
    fields={key:{} for key in ['candidates','slot_bindings','slot_catalog','policies']}
    for module in manifest['modules']:
        data=git_json(ASSETS/module['file']) if base else json.loads((ROOT/ASSETS/module['file']).read_text())
        key=module['kind'];assert not set(fields[key])&set(data[key]);fields[key].update(data[key])
    return manifest,fields
before_manifest,before=load(True)
after_manifest,after=load(False)
patches=json.loads((OUT.parent/'integration-evidence/existing-source-patches.json').read_text())
changed={r['candidate_id'] for r in patches}
expected_new=json.loads((ROOT/ASSETS/'photo_candidate_clockpunk_20261023.json').read_text())['candidates']
expected_bindings=json.loads((ROOT/ASSETS/'photo_candidate_clockpunk_bindings_20261023.json').read_text())['slot_bindings']
assert set(after['candidates'])-set(before['candidates'])==set(expected_new)
assert set(before['candidates'])<=set(after['candidates'])
actual_changed={cid for cid,row in before['candidates'].items() if row!=after['candidates'][cid]}
assert actual_changed==changed,(actual_changed,changed)
for patch in patches:
    cid=patch['candidate_id'];assert before['candidates'][cid]==patch['before']
    assert after['candidates'][cid]==patch['after']
    assert {k:v for k,v in before['candidates'][cid].items() if k!='content'}=={k:v for k,v in after['candidates'][cid].items() if k!='content'}
for key in ['slot_catalog','policies']:assert before[key]==after[key],key
assert set(after['slot_bindings'])-set(before['slot_bindings'])==set(expected_bindings)
assert all(row==after['slot_bindings'][bid] for bid,row in before['slot_bindings'].items())
assert after_manifest['modules'][:len(before_manifest['modules'])]==before_manifest['modules']
new_counts=collections.Counter(r['record_kind'] for r in expected_new.values())
report={'status':'pass','base_commit':BASE,'before_candidates':len(before['candidates']),
 'after_candidates':len(after['candidates']),'before_bindings':len(before['slot_bindings']),
 'after_bindings':len(after['slot_bindings']),'new_candidate_kinds':dict(new_counts),
 'changed_existing_CIDs':sorted(changed),'unchanged_existing_candidates':len(before['candidates'])-len(changed),
 'all_old_bindings_catalogs_policies_preserved':True,
 'corrected_intrinsic_conditions_effects_and_provenance_preserved':True,
 'base_manifest_prefix_preserved':True}
(OUT/'source-preservation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
