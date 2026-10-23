"""Verify actual selected release and exact harem source snapshots without searching."""
from pathlib import Path
import json,sys,hashlib,datetime
R=Path('/Users/chasoik/Projects/image-prompt');O=Path(__file__).resolve().parent;S=R/'skills/photo-prompt-image-generator'
read=lambda p:json.loads(p.read_bytes())
sys.path.insert(0,str(S/'scripts'))
from photo_installed_h_f2 import release,default_store,digest
cfg=read(S/'retrieval-runtime.json');store=default_store();native,m,nm=release(store,cfg['generation_id'],full=True)
assert m['native_generation_id']==cfg['native_generation_id'] and digest(nm['source']['code'])==cfg['code_sha256']
sys.path.insert(0,str(native/'scripts'))
import photo_canonical_source as canonical
fresh=read(O/'new-native-records.json');records=read(native/'assets/photo_candidate_harem_20261023.json')['candidates']
assert set(records)==set(fresh)
for cid,r in fresh.items():assert canonical.native_snapshot(records[cid])==r
changed=read(O/'changed-native-records.json');changed_seen=set();manifest=read(native/'assets/photo_candidate_corpus_manifest.json')
for row in manifest['modules']:
 if row['kind']!='candidates':continue
 if row['file'] not in ['photo_candidate_candidates_000.json','photo_candidate_candidates_001.json','photo_candidate_candidates_013.json']:continue
 body=read(native/'assets'/row['file'])['candidates']
 for cid in set(changed)&set(body):
  assert canonical.native_snapshot(body[cid])['content']['ko']==changed[cid]['content']['ko'];changed_seen.add(cid)
assert changed_seen==set(changed)
base=read(O/'final-default-successor/sealed-base.json');base_manifest=read(Path(base['native'])/'assets/photo_candidate_corpus_manifest.json');assert all(row in manifest['modules'] for row in base_manifest['modules'])
assert cfg==read(S/'retrieval-runtime.json'),'Concurrent selection changed while inspecting'
skill_sha=hashlib.sha256((S/'SKILL.md').read_bytes()).hexdigest();assert skill_sha==read(O/'independent-freeze-summary.json')['skill_sha256']
out={'status':'pass','time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'config':cfg,'store':str(store),'sealed_release_full_validation':True,'new_90_source_snapshots_exact':True,'updated_3_Korean_literals_exact':True,'latest_base_modules_preserved':True,'positive_CIDs':m['CID_count'],'RIDs':m['RID_count'],'skill_sha256':skill_sha,'additional_search_calls':0,'note':'Moment-of-inspection selection proof; external future default changes are outside this observation.'}
(O/'final-active-verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
