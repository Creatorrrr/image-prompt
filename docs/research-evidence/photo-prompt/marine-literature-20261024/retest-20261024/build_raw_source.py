"""Rebuild exact working V3 source in isolation, activate only unchanged inputs."""
from pathlib import Path
import gc;gc.disable()
import hashlib,json,os,shutil,sys
T=Path(__file__).resolve().parent;R=T.parents[4];S=R/'skills/photo-prompt-image-generator';A=S/'assets';B=T/'raw-assets';C=T/'raw-index-cache'
sys.path.insert(0,str(S/'scripts'))
import build_shared_candidate_index as builder
from photo_local_embedding import space
read=lambda p:json.loads(p.read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def members(v):
 out={}
 def walk(x):
  if isinstance(x,dict):
   if 'path' in x and 'sha256' in x:out[x['path']]=x['sha256']
   for child in x.values():walk(child)
  elif isinstance(x,list):
   for child in x:walk(child)
 walk(v);return out
def main():
 B.mkdir(exist_ok=True);C.mkdir(exist_ok=True)
 names=['photo_candidate_corpus_manifest.json']+[m['file'] for m in read(A/'photo_candidate_corpus_manifest.json')['modules']]
 protected={name:sha(A/name) for name in names}
 for name in names:shutil.copyfile(A/name,B/name)
 assert protected=={name:sha(A/name) for name in names}
 old=read(B/'photo_candidate_search.json') if (B/'photo_candidate_search.json').exists() else read(A/'photo_candidate_search.json')
 if not (B/'photo_candidate_search.json').exists():shutil.copyfile(A/'photo_candidate_search.json',B/'photo_candidate_search.json')
 for rel,h in members(old).items():
  assert not Path(rel).is_absolute() and '..' not in Path(rel).parts
  dst=B/rel;dst.parent.mkdir(parents=True,exist_ok=True)
  if not dst.exists():shutil.copyfile(A/rel,dst)
  assert sha(dst)==h
 (T/'raw-source-hashes.json').write_text(json.dumps(protected,indent=2)+'\n')
 report=builder.build(B,C,space=space());print('raw staged',report['layout_id'],flush=True)
 new=read(B/'photo_candidate_search.json')
 if protected!={name:sha(A/name) for name in names}:
  (T/'raw-index-activation.json').write_text(json.dumps({'status':'held','reason':'Concurrent authored source advance. Verified staged result preserved; no main pointer write.','report':report},indent=2)+'\n');return
 copied=0
 for rel,h in members(new).items():
  assert rel.startswith('photo_candidate_search_shards/'+new['layout_id']+'/')
  src=B/rel;dst=A/rel;dst.parent.mkdir(parents=True,exist_ok=True);assert sha(src)==h
  if not dst.exists():shutil.copyfile(src,dst);copied+=1
  assert sha(dst)==h
 if protected!={name:sha(A/name) for name in names}:
  (T/'raw-index-activation.json').write_text(json.dumps({'status':'held','reason':'Concurrent authored source advance during derived member copying. Main pointer preserved.','report':report},indent=2)+'\n');return
 temp=A/'photo_candidate_search.marine-retest.partial';shutil.copyfile(B/'photo_candidate_search.json',temp)
 if protected!={name:sha(A/name) for name in names}:
  (T/'raw-index-activation.json').write_text(json.dumps({'status':'held','reason':'Concurrent authored source advance before pointer activation. Main pointer preserved.','report':report},indent=2)+'\n');return
 os.replace(temp,A/'photo_candidate_search.json')
 (T/'raw-index-activation.json').write_text(json.dumps({'status':'pass','layout_id':new['layout_id'],'source_files_exact':len(protected),'derived_members_copied':copied,'old_shards_deleted':0,'authored_files_written':0,'report':report},indent=2)+'\n');print('raw activated',new['layout_id'],flush=True)
if __name__=='__main__':main()
