"""Scoped data and request-provenance rebinding repair; preserve all other baseline code/source.
New authored V3 source is converted by exact literal ownership, not semantic inference.
"""
from pathlib import Path
import gc
gc.disable()
import json,hashlib,sys,shutil,collections,os,copy,time
import numpy as np
O=Path(__file__).resolve().parent;B=json.loads((O/'release-base.json').read_bytes());N=Path(B['native']);STORE=O/'successor-store';STAGE=O/'successor-skill';WORK=O/'build'
# Bootstrap the reviewed tree before importing its sealed-source implementation.
# Publication rejects a worker imported from the old executable closure.
if not (STAGE/'scripts').is_dir():
 manifest0=json.loads((N/'manifest.json').read_bytes())
 for rel0 in manifest0['members']:
  dst0=STAGE/rel0;dst0.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(N/rel0,dst0)
override0=Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prepare_retry_context.py')
shutil.copyfile(override0,STAGE/'scripts/prepare_retry_context.py')
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
 fresh=read(O/'new-native-records.json');changed=read(O/'changed-native-records.json');prior=read(O/'changed-native-prior.json')
 result={cid:convert(record) for cid,record in fresh.items()}
 originals={}
 for module in read(N/'assets'/c.MANIFEST_NAME)['modules']:
  if module['kind']!='candidates':continue
  body=read(N/'assets'/module['file'])['candidates']
  originals.update({cid:body[cid] for cid in changed if cid in body})
  if set(originals)==set(changed):break
 for cid,record in changed.items():
  original=originals[cid];assert canonical.native_snapshot(original)==prior[cid], 'Installed source drift before narrow update'
  out=copy.deepcopy(original);meaning=out['meaning'];pool=meaning['literals'];tree=out['native']['tree']
  def lit(text):
   for uid,value in pool.items():
    if value==text:return uid
   uid='investigation_u'+str(len(pool));pool[uid]=text;return uid
  for key,value in record['content'].items():
   if value==prior[cid]['content'].get(key):continue
   assert isinstance(value,str) and isinstance(prior[cid]['content'].get(key),str)
   old_uid=tree[key]['$literal'];new_uid=lit(value);tree[key]={'$literal':new_uid}
   for scope in ('primary','evidence'):
    for rid,paths in meaning[scope].items():
     if '/content/'+key in paths:paths['/content/'+key]=new_uid
   for field,units in meaning['search']['fields'].items():meaning['search']['fields'][field]=list(dict.fromkeys(new_uid if uid==old_uid else uid for uid in units))
  assert canonical.native_snapshot(out)==record,'Narrow canonical edit altered other fields'
  meaning['origin']['source_record_sha256']=c.digest(record)
  meaning['origin']['semantic_fingerprint']=canonical.semantic_fingerprint(out)
  canonical.validate(out);result[cid]=out
 return result


def materialize_runtime():
 import subprocess
 lock=read(N/'embedding-runtime.lock.json')
 runtime=STAGE/'.runtime'
 if runtime.is_symlink():runtime.unlink()
 runtime.mkdir(exist_ok=True)
 package=STAGE/lock['package']
 package.mkdir(parents=True,exist_ok=True)
 for rel,row in lock['files'].items():
  src=N/lock['package']/rel;dst=package/rel;dst.parent.mkdir(parents=True,exist_ok=True)
  if not dst.exists():
   result=subprocess.run(['/bin/cp','-c',str(src),str(dst)],capture_output=True)
   if result.returncode:shutil.copyfile(src,dst)
  assert not dst.is_symlink() and dst.stat().st_size==row['bytes'] and file_sha(dst)==row['sha256']
 env=Path(lock['python']).parents[1]
 link=STAGE/env
 if not link.exists():link.symlink_to(Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator')/env,target_is_directory=True)
 write(O/'staged-model-package.json',{'status':'pass','package':str(package),'immutable_files':len(lock['files']),'all_sha256_verified':True,'package_symlink':False,'python_environment_link_only':str(link)})


def main():
 t=time.monotonic();new=collect();WORK.mkdir(exist_ok=True)
 fresh=read(O/'new-native-records.json');changed=read(O/'changed-native-records.json')
 materialize_runtime()
 # Resume after the already completed native-index build. The ordinary publisher
 # still executes its full source/index/code closure verification in this worker.
 assert (O/'native-index-build.json').is_file()
 review=read(O/'code-change-review.json')
 assert file_sha(STAGE/'scripts/prepare_retry_context.py')==review['new_sha256']
 publication=SnapshotPublisher(STAGE,STORE).stage();write(O/'native-staged.json',publication)
 print('native staged',publication['generation_id'],flush=True)
 # Build a fresh source body closure. Existing source data and vectors are unchanged.
 srcgen=WORK/'source';build_documents(STAGE/'assets',srcgen)
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
 gid=seal_h(STORE,inputs);write(O/'successor.json',{'status':'staged_verified','generation_id':gid,'native_generation_id':publication['generation_id'],'store':str(STORE),'new_CIDs':len(fresh),'reviewed_source_updated_CIDs':len(changed),'old_document_vectors_reused_exactly':sum(did in oldi and old_docs[oldi[did]]['text_sha256']==docmap[did]['text_sha256'] for did in ids),'new_document_vectors':len(newvec),'scope':'investigative relationship-repair-only source delta on current installed release; working-tree-only unrelated changes are not published','kernel_code_unchanged':False,'reviewed_code_delta':['scripts/prepare_retry_context.py'],'CURRENT_writes':0,'elapsed_seconds':time.monotonic()-t})
 print(json.dumps(read(O/'successor.json')),flush=True)
if __name__=='__main__':main()
