"""Verify a later shared default retains this task's exact source extension."""
from pathlib import Path
import datetime,json,sys
O=Path(__file__).resolve().parent
R=Path('/Users/chasoik/Projects/image-prompt')
read=lambda p:json.loads(p.read_bytes())
config_path=R/'skills/photo-prompt-image-generator/retrieval-runtime.json'
config=read(config_path)
store=Path(read(O/'BASELINE.json')['store'])
native=store/'generations'/config['native_generation_id']
sys.path.insert(0,str(native/'scripts'))
from photo_h_f2_generation import Generation
import photo_canonical_source as canonical
g=Generation(store,config['generation_id'],full=True)
fresh=read(O/'new-native-records.json')
for cid,record in fresh.items():
    assert canonical.native_snapshot(g.body.record(cid))==record
positive={row['cid'] for row in g.metadata}
visual={cid for cid,record in fresh.items() if record['record_kind']!='diagnostic'}
diagnostic=set(fresh)-visual
assert visual<=positive and diagnostic.isdisjoint(positive)
actual=read(native/'assets/photo_candidate_romcom_bindings_20261024.json')
expected=read(R/'skills/photo-prompt-image-generator/assets/photo_candidate_romcom_bindings_20261024.json')
assert actual['slot_bindings']==expected['slot_bindings']
publication=read(O/'current-default-successor/successor.json')
old=store/'generations'/publication['native_generation_id']
old_manifest=read(old/'assets/photo_candidate_corpus_manifest.json')
manifest=read(native/'assets/photo_candidate_corpus_manifest.json')
assert all(module in manifest['modules'] for module in old_manifest['modules'])
assert config['code_sha256']==read(O/'BASELINE.json')['config']['code_sha256']
result={'status':'later_default_verified_retains_romcom','time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'observed_default':config,'default_unchanged_during_check':read(config_path)==config,
        'complete_H_F2_verification':True,'new_source_snapshots_exact':len(fresh),
        'new_visual_CIDs_present':len(visual),'new_diagnostics_excluded':len(diagnostic),
        'new_bindings_exact':len(actual['slot_bindings']),
        'published_parent_modules_preserved':True,
        'additional_modules':[m for m in manifest['modules'] if m not in old_manifest['modules']],
        'positive_CIDs':g.manifest['CID_count'],'RIDs':g.manifest['RID_count'],
        'config_writes':0,'CURRENT_writes':0,
        'limit':'This verifies source retention and the sealed search structure. The authored rank probes were run on this task’s prior publication; no new rank or pixel claim is transferred to this later population.'}
(O/'inherited-default-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['limit']},ensure_ascii=False))
