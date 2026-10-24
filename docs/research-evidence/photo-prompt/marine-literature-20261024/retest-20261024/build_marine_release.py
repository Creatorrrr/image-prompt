"""Data-only successor; preserve baseline kernel and all original source records.
New authored V3 source is converted by exact literal ownership, not semantic inference.
"""
from pathlib import Path
import gc
gc.disable()
import json,hashlib,sys,shutil,collections,os,copy,time,ast
import numpy as np
O=Path(__file__).resolve().parent;B=json.loads((O/'release-base.json').read_bytes());N=Path(B['native']);STORE=O/'successor-store';STAGE=O/'successor-skill';WORK=O/'build'
ROOT=O.parents[4]; LIVE=ROOT/'skills/photo-prompt-image-generator'
base_manifest=json.loads((N/'manifest.json').read_bytes())
for rel,row in base_manifest['members'].items():
 dst=STAGE/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(N/rel,dst)
 assert hashlib.sha256(dst.read_bytes()).hexdigest()==row['sha256']
# Port only the current candidate-free query-scope/ownership wire additions.
# Retain the installed canonical-v4 corpus and all unrelated deployed code.
ported=[]
for rel in ['precore/photo_authoring_wire.py','precore/prepare_photo_run.py','precore/photo_feature_selection.py','precore/photo_request_query_scope.py','precore/photo_request_ownership.py','scripts/photo_h_f2_queries.py']:
 shutil.copyfile(LIVE/rel,STAGE/rel);ported.append(rel)
rel='scripts/prompt_generator.py'
def function_source(path,name):
 text=path.read_text();lines=text.splitlines(keepends=True)
 node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name==name)
 return node,lines
node,lines=function_source(STAGE/rel,'authorial_core_retrieval_text')
fresh,newlines=function_source(LIVE/rel,'authorial_core_retrieval_text')
(STAGE/rel).write_text(''.join(lines[:node.lineno-1]+newlines[fresh.lineno-1:fresh.end_lineno]+lines[node.end_lineno:]))
ported.append(rel)
(O/'runtime-compatibility-port.json').write_text(json.dumps({'scope':'Latest neutral request query scope and ownership review, exact latest projection function only. Canonical-v4 deployed data kernel retained.','ported_files':{p:hashlib.sha256((STAGE/p).read_bytes()).hexdigest() for p in ported},'all_other_original_members_unchanged':all(hashlib.sha256((STAGE/p).read_bytes()).hexdigest()==r['sha256'] for p,r in base_manifest['members'].items() if p not in ported),'ranking_sampling_policy_changed':False},indent=2)+'\n')
# The model package must be real files inside this skill, never a directory link.
runtime=STAGE/'.runtime'
if runtime.is_symlink():runtime.unlink()
runtime.mkdir(exist_ok=True)
env=runtime/'embedding-python'
if not env.exists():env.symlink_to(LIVE/'.runtime/embedding-python',target_is_directory=True)
lock=json.loads((STAGE/'embedding-runtime.lock.json').read_bytes())
for name,row in lock['files'].items():
 src=LIVE/lock['package']/name;dst=STAGE/lock['package']/name;dst.parent.mkdir(parents=True,exist_ok=True)
 if not dst.is_file() or hashlib.sha256(dst.read_bytes()).hexdigest()!=row['sha256']:shutil.copyfile(src,dst)
 assert not dst.is_symlink() and hashlib.sha256(dst.read_bytes()).hexdigest()==row['sha256']
sys.path.insert(0,str(STAGE/'scripts'))
import photo_candidate_corpus as c,photo_canonical_source as canonical,photo_recall_first as rf
from photo_recall_generation import read,write,file_sha,build_documents
from photo_h_f2_generation import stage as seal_h,configs,WEIGHTS,MEANING,CUES
from photo_h_f2_encoder import LocalEncoder
from photo_runtime_sources import SnapshotPublisher

def convert(record):
 pool={};reverse={}
 def lit(s):
  if s not in reverse:
   k='u'+str(len(pool));pool[k]=s;reverse[s]=k
  return reverse[s]
 def tree(v):
  if isinstance(v,str):return {'$literal':lit(v)}
  if isinstance(v,dict):return {k:tree(x) for k,x in v.items()}
  if isinstance(v,list):return [tree(x) for x in v]
  return v
 native=tree(record['content']);fields={k:[] for k in canonical.ORDER};primary={}
 for key,value in record['content'].items():
  if key=='aliases':
   assert isinstance(value,list) and all(isinstance(x,str) and x.strip() for x in value)
   fields['aliases'].extend(lit(x) for x in value);continue
  if key=='research_semantics':
   assert isinstance(value,dict);continue
  assert isinstance(value,str) and value.strip()
  primary['/content/'+key]=lit(value)
  if key in ['en','ko']:fields['labels'].append(lit(value))
  elif key=='definition':fields['definition'].append(lit(value))
  elif key=='application_contract':fields['source_requirements'].append(lit(value))
  else:raise ValueError('Unreviewed positive source field '+key)
 fields={name:list(dict.fromkeys(values)) for name,values in fields.items()}
 out={k:copy.deepcopy(v) for k,v in record.items() if k!='content'}
 diagnostic=record['record_kind']=='diagnostic'
 out['native']={'schema':canonical.NATIVE,'tree':native}
 out['meaning']={'schema':canonical.SCHEMA,'literals':pool,'primary':{'base':primary},'evidence':{'base':dict(primary)},'search':{'fields':fields},'graphs':{},'graph_provenance':{},'retrieval_class':'diagnostic' if diagnostic else 'positive','native_contract':'diagnostic' if diagnostic else 'option','origin':{'source_record_sha256':c.digest(record),'semantic_fingerprint':''},'coverage':{'raw_text_preserved':True,'primary_unit_count':len(primary),'unresolved_relations':0,'metadata_role':'Explicit source literals and source/effect/provenance retained. Research graph is review metadata. No native qualification.'}}
 out['meaning']['origin']['semantic_fingerprint']=canonical.semantic_fingerprint(out)
 canonical.validate(out);assert canonical.native_snapshot(out)==record
 return out


def collect():
 raw={**read(O/'release-new-native-records.json'),**read(O/'changed-native-records.json')}
 return {cid:convert(record) for cid,record in raw.items()}


def main():
 t=time.monotonic();assert read(O/'source-preservation.json')['status']=='pass';new=collect();WORK.mkdir(exist_ok=True)
 manifest=read(N/'manifest.json')
 fresh=read(O/'release-new-native-records.json');changed=read(O/'changed-native-records.json')
 module='photo_candidate_marine_literature_20261024.json'
 write(STAGE/'assets'/module,{'schema':c.MODULE_SCHEMAS['candidates'],'candidates':{cid:new[cid] for cid in fresh}})
 source=read(STAGE/'assets'/c.MANIFEST_NAME);source['modules'].append({'file':module,'kind':'candidates'})
 binding_module='photo_candidate_marine_literature_bindings_20261024.json'
 binding_source=O/'release-bindings.json'
 binding_data=read(binding_source);binding_data['schema']=c.MODULE_SCHEMAS['slot_bindings']
 write(STAGE/'assets'/binding_module,binding_data);source['modules'].append({'file':binding_module,'kind':'slot_bindings'});write(STAGE/'assets'/c.MANIFEST_NAME,source)
 for m in source['modules']:
  if m['kind']!='candidates':continue
  path=STAGE/'assets'/m['file'];body=read(path);owned=set(body['candidates'])&set(changed)
  if owned:
   for cid in owned:body['candidates'][cid]=new[cid]
   write(path,body)
 corpus=c.load(STAGE/'assets');original=c.load(N/'assets');assert set(original['candidates']).isdisjoint(fresh)
 assert all(corpus['candidates'][cid]==r for cid,r in original['candidates'].items() if cid not in changed)
 for cid in changed:
  current=canonical.native_snapshot(corpus['candidates'][cid])
  assert current==changed[cid], 'Changed source not exact reviewed record'
  prior=canonical.native_snapshot(original['candidates'][cid])
  assert all(prior[k]==current[k] for k in ['conditions','effects','provenance']), 'Existing intrinsic guard/effect/provenance changed'
 assert all(corpus[k]==original[k] for k in ['slot_catalog','policies']);assert all(corpus['slot_bindings'][k]==v for k,v in original['slot_bindings'].items())
 write(O/'canonical-source-validation.json',{'status':'pass','old_CIDs':len(original['candidates']),'new_CIDs':len(fresh),'reviewed_source_updated_CIDs':len(changed),'total_CIDs':len(corpus['candidates']),'unchanged_original_records_preserved':len(original['candidates'])-len(changed),'changed_original_intrinsic_guards_effects_provenance_preserved':True,'existing_slot_catalog_bindings_policies_preserved':True,'native_approval':False})
 print('canonical source verified',len(new),'new candidates',flush=True)
 del corpus,original
 gc.collect()
 print('released completed validation corpus copies',flush=True)
 # Build the native guard/source closure with the deployed implementation.
 import build_shared_candidate_index as nativebuild
 native_report=nativebuild.build(STAGE/'assets',WORK/'native-index-cache',space=read(N/'embedding-runtime.lock.json')['space'])
 write(O/'native-index-build.json',native_report);print('native index complete',flush=True)
 from photo_local_embedding import close_worker
 close_worker();gc.collect()
 publication=SnapshotPublisher(STAGE,STORE).stage();write(O/'native-staged.json',publication)
 print('native staged',publication['generation_id'],flush=True)
 # Build a fresh source body closure. Existing source data and vectors are unchanged.
 srcgen=WORK/'source';build_documents(STAGE/'assets',srcgen);gc.collect();print('recall source closure built',flush=True)
 oldG=Path(B['store'])/'h-f2-generations'/B['config']['generation_id']
 oldmeta=read(oldG/'indexed-documents.json.gz');old_docs=read(oldG/'documents.json.gz')['rows'];old_fields=read(oldG/'field-documents.json.gz')['rows'];proofs=read(oldG/'document-proofs.json.gz')['rows'];binding=read(oldG/'manifest.json')['binding']
 docmap={v['id']:v for v in old_docs};fieldmap={v['id']:v for v in old_fields};metamap={v['id']:v for v in oldmeta};newtexts={};projection={}
 for cid,record in new.items():
  if not canonical.positive(record):continue
  for raw in rf.documents(record):
   core=[p for p in raw['parts'] if {s['role'] for s in p['sources']}&MEANING]
   cues=[p for p in raw['parts'] if not ({s['role'] for s in p['sources']}&MEANING) and {s['role'] for s in p['sources']}&CUES]
   selected=core+cues if core+cues else [{'text':raw['text'],'sources':[]}]
   text='\n'.join(p['text'] for p in selected);fields={k:[] for k in WEIGHTS}
   for part in selected:
    roles={v['role'] for v in part['sources']};name=None
    for role in ('source_definition','source_core_meaning','source_concept_units','source_semantic_relations','selected_branch_unit','selected_branch_component'):
     if role in roles:name='concept_units' if role.startswith('selected_branch') else role.removeprefix('source_');break
    if name is None and 'source_labels' in roles:name='labels'
    if name is None:name=next((v.get('ref',{}).get('field') for v in part['sources'] if v['role']=='lookup' and v.get('ref',{}).get('field') in fields),'definition')
    fields[name].append(part['text'])
   d={'schema':'photo-h-f2-authored-literal-document/v1','id':raw['id'],'cid':cid,'rid':raw['rid'],'source_sha256':raw['source_sha256'],'text':text,'text_sha256':rf.sha(text),'original_document_sha256':raw['document_sha256'],'original_text_sha256':raw['text_sha256'],'native_sha256':raw['native_sha256'],'conditions_sha256':raw['conditions_sha256'],'effects_sha256':raw['effects_sha256'],'native_approval':False,'native_source_changed':False,'record_kind':record['record_kind'],'coverage':'complete authored en/ko literal fields; application_contract remains in source body, not a ranking vote'}
   f={'id':d['id'],'cid':cid,'rid':d['rid'],'source_sha256':d['source_sha256'],'fields':fields,'ordered_units':[p['text'] for p in selected]};docmap[d['id']]=d;fieldmap[d['id']]=f;metamap[d['id']]={k:raw[k] for k in ('id','cid','rid','source_sha256','text_sha256','document_sha256')};newtexts[d['text_sha256']]=text
 with LocalEncoder(Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator')) as enc:
  assert enc.binding==binding
  newvec={};ordered=list(newtexts)
  for start in range(0,len(ordered),16):
   hs=ordered[start:start+16];encoded=enc.encode([newtexts[h] for h in hs],'document')
   for h,e in zip(hs,encoded):rf.check_embedding(e,binding,newtexts[h],'document');newvec[h]=e['vector'];proofs[h]=e['execution']
 oldmatrix=np.memmap(oldG/'vectors.f64',dtype='<f8',mode='r',shape=(len(oldmeta),768));oldi={m['id']:i for i,m in enumerate(oldmeta)};ids=sorted(metamap);matrix=np.memmap(WORK/'vectors.f64',dtype='<f8',mode='w+',shape=(len(ids),768))
 for i,did in enumerate(ids):
  unchanged=did in oldi and old_docs[oldi[did]]['text_sha256']==docmap[did]['text_sha256']
  matrix[i]=oldmatrix[oldi[did]] if unchanged else np.asarray(newvec[docmap[did]['text_sha256']])
 matrix.flush();del matrix
 docs=[docmap[i] for i in ids];fdocs=[fieldmap[i] for i in ids];metadata=[metamap[i] for i in ids]
 write(srcgen/'indexed-documents.json.gz',metadata)
 lengths={f:[] for f in WEIGHTS};counts={f:0 for f in WEIGHTS};posting={}
 for i,f in enumerate(fdocs):
  terms={}
  for name in WEIGHTS:
   bag=collections.Counter(t for v in f['fields'][name] for t in rf.tokens(v));size=sum(bag.values());lengths[name].append(size);counts[name]+=bool(size)
   for term,tf in bag.items():terms.setdefault(term,{})[name]=tf
  for term,tf in terms.items():posting.setdefault(term,[]).append([i,tf])
 cfg=configs();fields={'n':len(ids),'fields':cfg,'lengths':lengths,'nonempty_counts':counts,'postings':posting,'average_lengths':{f:(sum(lengths[f])/(counts[f] if 'normalization_population' in cfg[f] else len(ids)) if (counts[f] if 'normalization_population' in cfg[f] else len(ids)) else 0.) for f in WEIGHTS},'tokenizer':read(oldG/'fields.json.gz')['tokenizer']}
 for fn,v in [('documents.json.gz',{'rows':docs}),('field-documents.json.gz',{'rows':fdocs}),('fields.json.gz',fields),('document-proofs.json.gz',{'rows':proofs})]:write(WORK/fn,v)
 inputs={'generation':str(srcgen),'documents':str(WORK/'documents.json.gz'),'field_documents':str(WORK/'field-documents.json.gz'),'fields':str(WORK/'fields.json.gz'),'proofs':str(WORK/'document-proofs.json.gz'),'vectors':str(WORK/'vectors.f64'),'binding':binding,'native_generation_id':publication['generation_id']}
 gid=seal_h(STORE,inputs);write(O/'successor.json',{'status':'staged_verified','generation_id':gid,'native_generation_id':publication['generation_id'],'store':str(STORE),'new_CIDs':len(fresh),'reviewed_source_updated_CIDs':len(changed),'old_document_vectors_reused_exactly':sum(did in oldi and old_docs[oldi[did]]['text_sha256']==docmap[did]['text_sha256'] for did in ids),'new_document_vectors':len(newvec),'kernel_code_unchanged':False,'kernel_changes':'Exact current neutral query-scope and ownership-review compatibility port; no scoring or sampling changes','CURRENT_writes':0,'elapsed_seconds':time.monotonic()-t})
 print(json.dumps(read(O/'successor.json')),flush=True)
if __name__=='__main__':main()
