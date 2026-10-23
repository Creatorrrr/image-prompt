"""Encode already frozen development queries in the exact installed local space."""
import gc
gc.disable()
import hashlib,json,sys
from pathlib import Path
O=Path(__file__).resolve().parent
ROOT=Path('/Users/chasoik/Projects/image-prompt')
S=ROOT/'skills/photo-prompt-image-generator'
read=lambda p:json.loads(p.read_bytes())
B=read(O/'release-base.json')
sys.path.insert(0,str(Path(B['native'])/'scripts'))
from photo_h_f2_encoder import LocalEncoder
import photo_recall_first as rf
binding=read(Path(B['store'])/'h-f2-generations'/B['config']['generation_id']/'manifest.json')['binding']
cases=read(O/'retrieval-development-cases.json')['cases']
cache=O/'qualification-query-evidence.json'
assert not cache.exists()
encoded={'query_source_sha256':hashlib.sha256((O/'retrieval-development-cases.json').read_bytes()).hexdigest(),'binding':binding,'rows':[]}
with LocalEncoder(S) as enc:
    assert enc.binding==binding
    for offset in range(0,len(cases),12):
        batch=cases[offset:offset+12]
        evidence=enc.encode([row['query'] for row in batch],'query')
        for row,e in zip(batch,evidence,strict=True):
            rf.check_embedding(e,binding,row['query'],'query')
            encoded['rows'].append({'id':row['id'],'query':row['query'],'embedding':e})
        print('encoded',len(encoded['rows']),flush=True)
cache.write_text(json.dumps(encoded,ensure_ascii=False,indent=2)+'\n')
