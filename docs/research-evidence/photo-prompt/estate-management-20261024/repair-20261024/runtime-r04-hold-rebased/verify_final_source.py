from pathlib import Path
import json,hashlib,sys,datetime
O=Path(__file__).resolve().parent;ROOT=Path('/Users/chasoik/Projects/image-prompt');S=ROOT/'skills/photo-prompt-image-generator'
read=lambda p:json.loads(p.read_bytes());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
b=read(O/'before.json');r=read(O/'successor.json');cfg=read(S/'retrieval-runtime.json')
assert cfg['generation_id']==r['generation_id'] and cfg['native_generation_id']==r['native_generation_id']
assert cfg['code_sha256']==b['config']['code_sha256']
N=Path(b['native']);D=Path(b['store'])/'generations'/cfg['native_generation_id']
m0=read(N/'assets/photo_candidate_corpus_manifest.json');m1=read(D/'assets/photo_candidate_corpus_manifest.json')
assert {tuple(sorted(x.items())) for x in m0['modules']}=={tuple(sorted(x.items())) for x in m1['modules']}
module='photo_candidate_estate_visibility_repairs_20261024.json';preserved=[]
for m in m0['modules']:
 p=m['file']
 if p==module:continue
 assert sha(N/'assets'/p)==sha(D/'assets'/p),p
 preserved.append(p)
manifest0=read(N/'manifest.json');manifest1=read(D/'manifest.json')
assert manifest0['source']['code']==manifest1['source']['code']
for member in manifest0['source']['code']:
 assert sha(N/member)==sha(D/member),member
sys.path.insert(0,str(D/'scripts'))
import photo_canonical_source as canonical
old=read(N/'assets'/module)['candidates'];new=read(D/'assets'/module)['candidates'];working=read(S/'assets'/module)['candidates']
changed='cand_0c4dd02a43f15558a60acd36ce75307a'
assert set(old)==set(new)==set(working) and len(new)==8
for cid in new:
 assert canonical.native_snapshot(new[cid])==working[cid]
 if cid!=changed:assert old[cid]==new[cid]
 else:
  a=canonical.native_snapshot(old[cid]);z=canonical.native_snapshot(new[cid])
  for key in ['conditions','effects','provenance']:assert a[key]==z[key]
  for key in ['en','ko']:assert a['content'][key]==z['content'][key]
  assert a['record_kind']=='visual_option' and z['record_kind']=='diagnostic'
bind='photo_candidate_estate_visibility_repair_bindings_20261024.json'
a=read(S/'assets'/bind);z=read(D/'assets'/bind)
assert a['slot_bindings']==z['slot_bindings'] and len(z['slot_bindings'])==21
wm=read(S/'assets/photo_candidate_corpus_manifest.json')
for name in [module,bind]:assert sum(m['file']==name for m in wm['modules'])==1
oldhashes=read(O.parent/'original-estate-preservation.json')
for file,row in oldhashes['files'].items():
 assert sha(S/'assets'/file)==row['sha256']
 if file!='photo_estate_management_semantics_20261024.json':assert sha(D/'assets'/file)==sha(N/'assets'/file)
result={'status':'pass','verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'generation_id':cfg['generation_id'],'native_generation_id':cfg['native_generation_id'],'kernel_code_sha256':cfg['code_sha256'],'baseline_config':b['config'],'prior_current_source_modules_byte_equal_except_own_module':True,'preserved_source_module_count':len(preserved),'all_prior_kernel_code_bytes_preserved':True,'same_module_unchanged_records':7,'reviewed_changed_source_records':1,'R04_old_en_ko_conditions_effects_provenance_preserved':True,'final_positive_optional_records':7,'held_diagnostic_records':1,'binding_rows_exact':21,'binding_schema_conversion':{'authoring':a['schema'],'runtime':z['schema'],'all_row_fields_unchanged':True},'working_manifest_new_entries_once':True,'original_estate_78_56_and_sidecar_unchanged':oldhashes,'CURRENT_writes':0,'source_roundtrip_count':8}
(O/'final-source-preservation.json').write_text(json.dumps(result,indent=2)+'\n')
(O/'final-default-selection.json').write_text(json.dumps(cfg,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['original_estate_78_56_and_sidecar_unchanged','baseline_config']}))
