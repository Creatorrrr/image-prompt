from pathlib import Path
import json,shutil,hashlib
O=Path(__file__).resolve().parent;B=json.loads((O/'rebase-before.json').read_bytes());N=Path(B['native']);S=O/'rebased-skill'
# Resume only this task-owned staging; every member is reverified below.
manifest=json.loads((N/'manifest.json').read_bytes())
for rel,row in manifest['members'].items():
 p=N/rel;q=S/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
 expected=row['sha256'] if isinstance(row,dict) else row
 assert hashlib.sha256(q.read_bytes()).hexdigest()==expected,rel
lock=json.loads((N/'embedding-runtime.lock.json').read_bytes());oldstage=O/'successor-skill'
for rel,row in lock['files'].items():
 p=oldstage/lock['package']/rel;q=S/lock['package']/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
 assert hashlib.sha256(q.read_bytes()).hexdigest()==row['sha256'],rel
if not (S/'.runtime/embedding-python').exists(): (S/'.runtime/embedding-python').symlink_to(Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/.runtime/embedding-python'),target_is_directory=True)
# Retain the authored review metadata accompanying the new candidate module.
shutil.copyfile(Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_mecha_robot_semantics_20261024.json'),S/'assets/photo_mecha_robot_semantics_20261024.json')
s=(O/'build_release.py').read_text().replace("O/'before.json'","O/'rebase-before.json'").replace("O/'successor-store'","O/'rebased-store'").replace("O/'successor-skill'","O/'rebased-skill'").replace("O/'build'","O/'rebased-build'")
for f in ['canonical-source-validation.json','native-index-build.json','native-staged.json','successor.json']:
 s=s.replace("O/'"+f+"'","O/'rebase-"+f+"'")
s=s.replace(' import build_shared_candidate_index as nativebuild',''' import build_shared_candidate_index as nativebuild
 # Reuse only verified text/recipe matches from both sealed predecessor pools.
 from photo_search_reader import SearchReader
 original_vectors=nativebuild.offline_vector_map
 def union_vectors(reader,corpus):
  prior=read(O/'successor.json');prior_native=Path(prior['store'])/'generations'/prior['native_generation_id'];other=SearchReader(prior_native/'assets')
  try: merged=original_vectors(other,corpus)
  finally: other.close()
  current=original_vectors(reader,corpus)
  for cid,entry in current['entries'].items():
   if cid in merged['entries']: assert merged['entries'][cid]==entry,'Shared vector drift'
   merged['entries'][cid]=entry
  merged['space']=current['space'];return merged
 nativebuild.offline_vector_map=union_vectors''')
start=s.index(" with LocalEncoder(");end=s.index(" oldmatrix=np.memmap",start)
s=s[:start]+''' prior=read(O/'successor.json');priorG=Path(prior['store'])/'h-f2-generations'/prior['generation_id'];prior_meta=read(priorG/'indexed-documents.json.gz');prior_docs=read(priorG/'documents.json.gz')['rows'];prior_proofs=read(priorG/'document-proofs.json.gz')['rows'];prior_matrix=np.memmap(priorG/'vectors.f64',dtype='<f8',mode='r',shape=(len(prior_meta),768))
 assert read(priorG/'manifest.json')['binding']==binding
 prior_text={d['text_sha256']:i for i,d in enumerate(prior_docs)};newvec={}
 for h in newtexts:
  i=prior_text[h];assert prior_docs[i]['text']==newtexts[h]
  newvec[h]=prior_matrix[i].tolist();proofs[h]=prior_proofs[h]
''' +s[end:]
s=s.replace("'new_document_vectors':len(newvec)","'new_document_vectors':0,'mecha_document_vectors_reused_exactly':len(newvec)")
(O/'build_rebased_release.py').write_text(s)
i=(O/'install_release.py').read_text().replace("O/'successor.json'","O/'rebase-successor.json'").replace("O/'before.json'","O/'rebase-before.json'").replace("'install-active.json' if activate else 'install.json'","'rebase-install-active.json' if activate else 'rebase-install.json'").replace("O/'validation-execution.json'","O/'rebase-validation-execution.json'")
(O/'install_rebased_release.py').write_text(i)
print(json.dumps({'stage':str(S),'copied_members':len(manifest['members']),'current_config':B['config'],'preserve_mecha_checkpoint':True}))
