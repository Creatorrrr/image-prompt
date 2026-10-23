"""Adopted data/source protection checks. Pixel judgments live in arm reviews."""
from pathlib import Path
import hashlib,json,subprocess,sys
H=Path(__file__).resolve().parent;ROOT=H.parents[3];O=H/'integration-evidence';S=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(S/'scripts'))
import photo_candidate_corpus as c
read=lambda p:json.loads(p.read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
digest=lambda x:sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def main():
 checks=[]
 def check(name,ok,detail=None):checks.append({'name':name,'pass':bool(ok),'detail':detail})
 b=read(O/'BASELINE.json');i=read(O/'data-integration.json');raw=c.load(S/'assets');fresh=read(O/'new-native-records.json');patch=read(O/'existing-source-patches.json');changed={x['candidate_id'] for x in patch}
 check('all unrelated old candidate records preserved',all(digest(raw['candidates'][cid])==h for cid,h in b['candidate_hashes'].items() if cid not in changed))
 check('all old bindings preserved',all(digest(raw['slot_bindings'][bid])==h for bid,h in b['binding_hashes'].items()))
 check('old catalog and policies preserved',digest(raw['slot_catalog'])==b['slot_catalog_sha256'] and digest(raw['policies'])==b['policies_sha256'])
 check('new 88 source records exact',len(fresh)==88 and all(raw['candidates'][cid]==v for cid,v in fresh.items()))
 check('reviewed 4 patches exact and intrinsic guards preserved',len(changed)==4 and all(raw['candidates'][x['candidate_id']]==x['after'] and all(x['before'][k]==x['after'][k] for k in ['conditions','effects','provenance']) for x in patch))
 positive={cid for cid,r in fresh.items() if r['record_kind']=='visual_option'};diagnostic=set(fresh)-positive
 check('33 optional visual and 55 nonpositive records',len(positive)==33 and len(diagnostic)==55 and all(not raw['candidates'][cid]['content'].get('aliases') for cid in diagnostic))
 newb={bid:v for bid,v in raw['slot_bindings'].items() if bid not in b['binding_hashes'] and v['candidate_id'] in fresh}
 extra_candidates=set(raw['candidates'])-set(b['candidate_hashes'])-set(fresh)
 extra_bindings=set(raw['slot_bindings'])-set(b['binding_hashes'])-set(newb)
 check('72 optional bindings address only admitted visual sources',len(newb)==72 and all(v['candidate_id'] in positive and v['role']=='optional' for v in newb.values()),{'count':len(newb),'bad':[v for v in newb.values() if v['candidate_id'] not in positive or v['role']!='optional']})
 side=read(S/'assets/photo_court_palace_semantics_20261023.json');cards=side['cards'];routes=side['keyword_routes']
 check('semantic card and route closure',len(cards)==88 and len(routes)==623 and {x['candidate_id'] for x in cards}==set(fresh) and all(set(x['candidate_ids'])<=set(fresh) and not x['automatic_hard_activation'] for x in routes))
 check('no research metadata promoted to approval',not side['native_approval'] and all(not x['native_approval'] for x in cards))
 check('held historical cards excluded from visual candidates',all(x['candidate_id'] in diagnostic for x in cards if x['historical_review_required']))
 allowed=set(i['authored_file_allowlist'])|{'skills/photo-prompt-image-generator/assets/photo_candidate_search.json','skills/photo-prompt-image-generator/retrieval-runtime.json'}
 drift=[name for name,h in b['source_files'].items() if name not in allowed and (not (ROOT/name).is_file() or sha((ROOT/name).read_bytes())!=h)]
 check('protected source files outside allowlist unchanged',not drift,drift)
 check('latest skill document unchanged',sha((S/'SKILL.md').read_bytes())==b['source_files']['skills/photo-prompt-image-generator/SKILL.md'])
 index=read(O/'raw-dictionary-validation.json');check('raw dictionary and index closure at own completed build snapshot',not index['errors'] and index['native_candidates']==20959 and index['bindings']==15911,index)
 original=read(H/'BASELINE.json');head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();check('HEAD unchanged',head==original['head'])
 check('preexisting tracked deletions preserved',all((not (ROOT/line[3:]).exists()) for line in original['tracked_status'] if line[:2].strip()=='D'))
 result={'schema':'court-palace-data-integration-validation/v1','status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','checks':checks,'raw_total_candidates':len(raw['candidates']),'raw_total_bindings':len(raw['slot_bindings']),'concurrent_external_additions':{'candidate_count':len(extra_candidates),'binding_count':len(extra_bindings),'candidate_ids':sorted(extra_candidates),'binding_ids':sorted(extra_bindings),'preserved':True,'current_raw_index_qualification':'superseded_by_external_additions_not_revalidated_by_this_task' if extra_candidates or extra_bindings else 'own_build_snapshot'},'native_semantic_approval':False,'scope':'Data integrity and protected state only; retrieval, transport, pixels and acceptance have separate evidence.'}
 (O/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':result['status'],'checks':len(checks),'failed':[x for x in checks if not x['pass']]},ensure_ascii=False))
 if result['status']!='PASS':raise SystemExit(1)
if __name__=='__main__':main()
