"""Pure stdlib lossless paged prior-row reader; whole dict partitioned, never selected by semantic keyword."""
import json,hashlib,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');D=R/'native-inputs/prepared/review11870-01250-01300-05';I=json.loads((D/'INPUT.json').read_text());P=json.loads((D/'PREPARED-PACKET.json').read_text())
def dig(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert dig(I)=='8e55650ab768cd287b707bebeb11ba2139b475f6f3b0a3d1d17fe82ab128ea66';assert dig(P)=='316b02b5f157f6dd5401973b8e13226ee35aabf42a5b24932639ff8de509de2b'
n=int(sys.argv[1]);page=int(sys.argv[2]);cid=P['ids'][n-1250];rev=I['required_revisions'][cid]['prior_review'];a=rev['artifact'];raw=Path(a['file']).read_bytes();assert hashlib.sha256(raw).hexdigest()==a['file_sha256'];old=json.loads(raw)['records'][int(rev['pointer'].split('/')[-1])];assert dig(old)==rev['sha256'];proof=old['proof']
pages=[{'row_top_except_proof':{k:v for k,v in old.items()if k!='proof'}},{'proof_except_facts':{k:v for k,v in proof.items()if k!='facts'}}]+[{'proof_facts_index_range':[i,min(i+8,len(proof['facts']))],'facts':proof['facts'][i:i+8]}for i in range(0,len(proof['facts']),8)]
print(json.dumps({'ordinal':n,'candidate_id':cid,'exact_prior_row_sha256':dig(old),'page':page,'total_pages':len(pages),'part':pages[page]},ensure_ascii=False,indent=2))
