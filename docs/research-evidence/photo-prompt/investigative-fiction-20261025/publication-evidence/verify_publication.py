from pathlib import Path
import gc,json,sys,subprocess,hashlib
# Allocation scheduling only; every normal source validator remains enabled.
gc.disable();P=Path(__file__).resolve().parent;ROOT=P.parents[4];S=ROOT/'skills/photo-prompt-image-generator';sys.path.insert(0,str(S/'scripts'));import photo_candidate_corpus as c
read=lambda p:json.loads(p.read_bytes());write=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
base=read(P/'scope.json')['base'];m=json.loads(subprocess.check_output(['git','show',base+':skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json'],cwd=ROOT));current=c.load(S/'assets');old={};bindings={}
for mod in m['modules']:
 raw=json.loads(subprocess.check_output(['git','show',base+':skills/photo-prompt-image-generator/assets/'+mod['file']],cwd=ROOT))
 if mod['kind']=='candidates':old.update(raw['candidates'])
 if mod['kind']=='slot_bindings':bindings.update(raw['slot_bindings'])
changes=read(P.parent/'integration-evidence/changed-native-records.json');new={**read(P.parent/'integration-evidence/new-native-records.json'),**read(P.parent/'retest-20261025/integration-evidence/new-native-records.json')}
assert all(current['candidates'][cid]==record for cid,record in old.items() if cid not in changes)
for cid,record in changes.items():
 assert current['candidates'][cid]==record
 assert all(current['candidates'][cid][k]==old[cid][k] for k in ['conditions','effects','provenance'])
assert all(current['candidates'][cid]==record for cid,record in new.items());assert all(current['slot_bindings'][cid]==record for cid,record in bindings.items())
assert len(new)==134 and sum(v['record_kind']!='diagnostic' for v in new.values())==84
exports=read(P/'durable-export.json');images=[]
for arm in exports['exports']:
 for row in arm['images']:
  p=ROOT/row['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'];images.append(row)
 for row in arm['bound_artifacts']:assert hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256']
result={'status':'pass','base':base,'old_candidates':len(old),'current_candidates':len(current['candidates']),'new_candidates_exact':len(new),'new_positive':84,'new_diagnostics':50,'five_existing_edits_guards_effects_provenance_preserved':True,'unrelated_existing_records_preserved':len(old)-len(changes),'old_bindings_preserved':len(bindings),'durable_actual_images':len(images),'immutable_bound_artifacts_verified':sum(len(a['bound_artifacts']) for a in exports['exports']),'historical_strict_results_preserved':'original0/3; retest0/3, new generic pixel2/6; no native whole-source qualification','native_approval':False}
write(P/'source-and-evidence-validation.json',result);print(json.dumps(result,ensure_ascii=False))
