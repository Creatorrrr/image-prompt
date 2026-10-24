"""Same immutable corpus/kernel: actual title vs its exact topical substring."""
from pathlib import Path
import gc;gc.disable()
import json,sys
T=Path(__file__).resolve().parent;R=T.parents[4]
read=lambda p:json.loads(Path(p).read_bytes())
succ=read(T/'successor.json');N=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed/generations')/succ['native_generation_id'];sys.path.insert(0,str(N/'scripts'))
from photo_h_f2_generation import Generation
from photo_h_f2_encoder import LocalEncoder
import photo_canonical_source as canonical
g=Generation('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed',succ['generation_id'],full=True);index=g.index();texts=['해병문학 용어 조사','해병문학'];new=set(read(T.parent/'integration-evidence/new-visual-cids.json'))
with LocalEncoder(R/'skills/photo-prompt-image-generator') as encoder:
 assert encoder.binding==g.binding;encoded=encoder.encode(texts,'query')
out=[]
for text,e in zip(texts,encoded,strict=True):
 result=index.search(text,e,g.binding);top=[]
 for rank,row in enumerate(result['order'][:8],1):
  raw=canonical.native_snapshot(g.body.record(row['cid']));content=raw.get('content',{});top.append({'rank':rank,'cid':row['cid'],'source_preview':str(content.get('en',content.get('definition',content)))[:400]})
 out.append({'query':text,'top8':top,'new_in_top32':[{'rank':i+1,'cid':row['cid']} for i,row in enumerate(result['order'][:32]) if row['cid'] in new],'lane_calls':result['lane_calls']})
(T/'topic-repair-ablation.json').write_text(json.dumps({'status':'complete','generation_id':g.id,'queries':out,'claim_limit':'Two exact requester substrings on the same corpus/kernel. No sampling or adoption measurement and no general accuracy claim.'},ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False),flush=True)
