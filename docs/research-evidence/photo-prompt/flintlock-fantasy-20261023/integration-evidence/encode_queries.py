from pathlib import Path
import json,csv,hashlib,sys
O=Path(__file__).resolve().parent;R=O.parents[4];B=json.loads((O/'before.json').read_bytes());sys.path.insert(0,str(Path(B['native'])/'scripts'))
from photo_h_f2_encoder import LocalEncoder
import photo_recall_first as rf
qfile=O.parent/'EVALUATION-CASES.tsv'
cases=[{'id':r['case_id']+'-'+lang,'query':r['query_'+lang]} for r in csv.DictReader(qfile.open(),delimiter='\t') for lang in ('ko','en')]
assert len(cases)==226
out={'query_source_sha256':hashlib.sha256(qfile.read_bytes()).hexdigest(),'rows':[]}
with LocalEncoder(R/'skills/photo-prompt-image-generator') as enc:
 out['binding']=enc.binding
 for start in range(0,len(cases),12):
  batch=cases[start:start+12];es=enc.encode([r['query'] for r in batch],'query')
  for r,e in zip(batch,es,strict=True):
   rf.check_embedding(e,enc.binding,r['query'],'query');out['rows'].append({**r,'embedding':e})
  print('encoded',len(out['rows']),flush=True)
(O/'qualification-query-evidence.json').write_text(json.dumps(out,ensure_ascii=False)+'\n')
