"""Append two reviewed singular shoe lookup forms without broadening hard activation."""
from pathlib import Path
import argparse, copy, hashlib, json, os, sys
OUT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--source-root',type=Path,required=True)
parser.add_argument('--runtime-store',type=Path,required=True)
parser.add_argument('--phase',required=True)
args=parser.parse_args();skill=args.source_root;root=skill.parents[1];assets=skill/'assets'
sys.path.insert(0,str(skill/'scripts'))
from photo_candidate_semantics import digest
from photo_runtime_sources import source_update
cf='photo_prompt_accessory_structure_extension.json';pf='photo_prompt_visual_obligations_accessory_structure.json'
paths=[assets/cf,assets/pf]
raws=[p.read_bytes() for p in paths];c,p=[json.loads(raw) for raw in raws]
forms={'spf_sf107_02':'Mary Jane','spf_sf107_3':'Slingback'}
changed=[]
for cid,label in forms.items():
 row=next(r for rs in c['slots'].values() for r in rs if r['id']==cid)
 assert label not in row['keywords']
 row['keywords'].append(label)
 row['embedding_text']+=' | Optional singular shoe lookup: '+label
 bundle=next(b for b in c['visual_semantics'] if cid in b['candidate_ids'])
 bundle['source_keywords'].append(label)
 profile=next(r for r in p['profiles'] if r['id']==cid.replace('spf_','spring_'))
 before_activation=copy.deepcopy(profile['activation'])
 profile['concept_candidate']['concept_terms'].append(label+' visible variant')
 assert profile['activation']==before_activation
 changed.append({'candidate_id':cid,'profile_id':profile['id'],'bundle_id':bundle['id'],
                 'lookup_form':label,'hard_activation_changed':False})
record_id='photo_prompt_accessory_structure_extension-spring-lookup-20261009-v2'
prior=c['maintenance_ref']
unbound=copy.deepcopy(c);unbound.pop('maintenance_ref')
record={'schema_version':'photo-extension-maintenance/v1','source_filename':cf,
 'prior_maintenance_ref':prior,'change':'Append singular Mary Jane and Slingback optional discovery terms after corpus BM25F qualification.',
 'authored_source_sha256':digest(unbound),'reviewed_changes':changed,
 'candidate_record_sha256':{cid:digest(next(r for rs in c['slots'].values() for r in rs if r['id']==cid)) for cid in forms},
 'bundle_record_sha256':{r['bundle_id']:digest(next(b for b in c['visual_semantics'] if b['id']==r['bundle_id'])) for r in changed},
 'profile_record_sha256':{r['profile_id']:digest(next(q for q in p['profiles'] if q['id']==r['profile_id'])) for r in changed},
 'claim_limit':'Optional lexical lookup only; definitions, owners, properties, activation and native gates are unchanged.'}
c['maintenance_ref']={'contract_version':'photo-extension-maintenance-ref/v1','record_id':record_id,'sha256':digest(record)}
record_path=root/'docs/research-evidence/photo-prompt/extension-maintenance'/(record_id+'.json')
assert not record_path.exists(),'Do not rewrite an existing correction record.'
def write(path,value):
 path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_name(path.name+'.spring-tmp')
 tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');os.replace(tmp,path)
with source_update(skill,args.runtime_store):
 assert all(path.read_bytes()==raw for path,raw in zip(paths,raws)), 'Concurrent source changed; do not overwrite.'
 for path,raw in zip(paths,raws):
  before=OUT/f'lookup-before-{args.phase}'/path.name;before.parent.mkdir(parents=True,exist_ok=True);before.write_bytes(raw)
 write(paths[0],c);write(paths[1],p);write(record_path,record)
receipt={'schema_version':'spring-lookup-correction/v1','phase':args.phase,'status':'PASS','changes':changed,
 'source_files':[{'file':path.name,'before_sha256':hashlib.sha256(raw).hexdigest(),'after_sha256':hashlib.sha256(path.read_bytes()).hexdigest()} for path,raw in zip(paths,raws)],
 'maintenance_record':str(record_path),'maintenance_record_sha256':digest(record)}
write(OUT/f'{args.phase.upper()}-LOOKUP-CORRECTION.json',receipt)
print(json.dumps({'status':'PASS','phase':args.phase,'lookup_forms':list(forms.values()),'hard_activation_changed':False},indent=2))
