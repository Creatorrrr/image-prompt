from pathlib import Path
import gc,json,sys,hashlib,time
W=Path('/Users/chasoik/.codex/worktrees/campus-query-core-publish/image-prompt');R=Path('/Users/chasoik/Projects/image-prompt');S=W/'skills/photo-prompt-image-generator';P=W/'docs/research-evidence/photo-prompt/campus-fiction-20261024/publication-20261024';sys.path.insert(0,str(S/'scripts'));gc.disable()
import photo_candidate_corpus as c,photo_global_index as documents,photo_search_layout as layout
from photo_search_reader import SearchReader
from build_shared_candidate_index import offline_vector_map
from photo_embedding_provider import atomic,embed_many
from photo_local_embedding import space as local_space
start=time.monotonic();corpus=c.load(S/'assets');c.validate(corpus);space=local_space();entries={};counts={}
for label,assets in [('remote-main-before-merge',W/'generated/maintenance/campus-merge-index-input/remote-main'),('committed-campus-index',W/'generated/maintenance/campus-merge-index-input/campus-topic')]:
 reader=SearchReader(assets)
 try:
  assert reader.manifest['space']==space,'incompatible model space'
  rows=offline_vector_map(reader,corpus)['entries'];added=0
  for cid,row in rows.items():
   if cid not in entries:entries[cid]=row;added+=1
  counts[label]=added
 finally:reader.close()
positive={cid:r for cid,r in corpus['candidates'].items() if r['record_kind'] in documents.POSITIVE_KINDS};missing=sorted(set(positive)-set(entries));cache=W/'generated/maintenance/campus-publication-cache';cache.mkdir(parents=True,exist_ok=True)
for offset in range(0,len(missing),16):
 ids=missing[offset:offset+16];projected=[documents.text(positive[cid]) for cid in ids];rows=embed_many([t for _,t in projected],[{'candidate_id':cid,'recipe':recipe} for cid,(recipe,_) in zip(ids,projected)],cache/'requests',space=space,kind='document')
 for cid,(recipe,text),row in zip(ids,projected,rows):entries[cid]={'id':cid,'recipe':recipe,'text':text,'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'vector':row['vector'],'embedding_execution':row['execution']}
 assert all(r['cache_hit'] or r['execution'] for r in rows)
 print('embedded',min(offset+16,len(missing)),len(missing),flush=True)
entries={cid:row for cid,row in entries.items() if cid in positive};vectors={'schema':documents.SCHEMA,'space':space,'corpus_sha256':c.digest(corpus),'entries':entries};documents.validate(vectors,corpus);assert c.digest(c.load(S/'assets'))==c.digest(corpus)
staged=layout.build(S/'assets',corpus,vectors);verification=layout.verify(S/'assets',corpus,staged,vectors);assert c.digest(c.load(S/'assets'))==c.digest(corpus);atomic(S/'assets'/layout.MANIFEST,staged)
report={'status':'pass','layout_id':staged['layout_id'],'corpus_sha256':c.digest(corpus),'candidates':len(corpus['candidates']),'positive_CIDs':len(positive),'bindings':len(corpus['slot_bindings']),'compatible_vectors_reused':counts,'missing_local_vectors':len(missing),'space':space,'verification':verification,'seconds':time.monotonic()-start};(P/'MERGED-INDEX-BUILD.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
