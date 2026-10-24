"""Copy only the verified derived closure while preserving all authored files."""
from pathlib import Path
import json,hashlib,shutil,os,gc
gc.disable()
O=Path(__file__).resolve().parent;R=O.parents[4]
A=R/'skills/photo-prompt-image-generator/assets';S=O/'working-source-skill/assets'
read=lambda p:json.loads(p.read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report=read(O/'working-source-index-cache/BUILD-REPORT.json')
assert report['verification']['verified']
m=read(S/'photo_candidate_search.json');assert m['layout_id']==report['layout_id']
source=read(S/'photo_candidate_corpus_manifest.json')
names=['photo_candidate_corpus_manifest.json']+[x['file'] for x in source['modules']]
protected={name:sha(S/name) for name in names}
def check():
 assert all((A/name).is_file() and sha(A/name)==h for name,h in protected.items()),'Working source advanced; rebuild before index activation.'
check()
rows={}
def paths(v):
 if isinstance(v,dict):
  if 'path' in v and 'sha256' in v:rows[v['path']]=v
  for x in v.values():paths(x)
 elif isinstance(v,list):
  for x in v:paths(x)
paths(m)
for rel,row in rows.items():
 assert not Path(rel).is_absolute() and '..' not in Path(rel).parts
 assert rel.startswith('photo_candidate_search_shards/'+m['layout_id']+'/')
 src=S/rel;dst=A/rel;assert sha(src)==row['sha256']
 dst.parent.mkdir(parents=True,exist_ok=True)
 if dst.exists():assert sha(dst)==row['sha256'],'Existing derived file differs'
 else:shutil.copyfile(src,dst)
 assert sha(dst)==row['sha256']
check()
prior=read(A/'photo_candidate_search.json')
(O/'working-index-before.json').write_text(json.dumps(prior,indent=2)+'\n')
temp=A/'photo_candidate_search.marine-20261024.partial'
shutil.copyfile(S/'photo_candidate_search.json',temp)
check();os.replace(temp,A/'photo_candidate_search.json')
(O/'working-index-activation.json').write_text(json.dumps({'status':'pass','layout_id':m['layout_id'],'source_files_exact':len(protected),'derived_members_copied_or_verified':len(rows),'source_sha256':m['corpus_sha256'],'authored_files_written':0,'old_shards_deleted':0,'builder_report':report},indent=2)+'\n')
print('activated',m['layout_id'],len(rows),'derived members')
