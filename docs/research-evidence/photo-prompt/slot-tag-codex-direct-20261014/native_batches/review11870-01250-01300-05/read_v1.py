"""Bounded lossless source-first reader; no semantic/proof/status generation, no production imports."""
import sys,json,gzip,hashlib
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');D=R/'native-inputs/prepared/review11870-01250-01300-05';canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();digest=lambda x:hashlib.sha256(canon(x)).hexdigest()
I=json.loads((D/'INPUT.json').read_text());P=json.loads((D/'PREPARED-PACKET.json').read_text());assert digest(I)=='8e55650ab768cd287b707bebeb11ba2139b475f6f3b0a3d1d17fe82ab128ea66';assert digest(P)=='316b02b5f157f6dd5401973b8e13226ee35aabf42a5b24932639ff8de509de2b'
sp=Path(I['current_snapshot']['file']);assert hashlib.sha256(sp.read_bytes()).hexdigest()==I['current_snapshot']['file_sha256'];S=json.loads(gzip.decompress(sp.read_bytes()));assert digest(S)==I['current_snapshot']['sha256'];assert S['slot_catalog']==I['catalog_review']['after'];assert digest(S['slot_catalog'])=='d9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15'
C=json.loads(Path('docs/research-evidence/photo-prompt/slot-retrieval-stage05-20261012/CONTROLLED-FINAL-SOURCE.json').read_text());a,b=map(int,sys.argv[1:3]);mode=sys.argv[3]if len(sys.argv)>3 else 'source';assert1250=1250
assert 1250<=a<b<=1300 and b-a<=2 and mode in ['source','prior']
def compact(v):
 seen={}
 def walk(x,p):
  k=canon(x)if isinstance(x,(dict,list,str))else b''
  if len(k)>35:
   if k in seen:return {'$exact_full_canonical_equal_value_at':seen[k]}
   seen[k]=p
  if isinstance(x,dict):return {z:walk(y,p+'/'+z.replace('~','~0').replace('/','~1'))for z,y in x.items()}
  if isinstance(x,list):return [walk(y,p+'/'+str(j))for j,y in enumerate(x)]
  return x
 return walk(v,'')
for n in range(a,b):
 cid=P['ids'][n-1250];rev=I['required_revisions'][cid]
 if mode=='source':
  loc=I['original_decisions'][cid];raw=Path(loc['file']).read_bytes();assert hashlib.sha256(raw).hexdigest()==loc['file_sha256'];oldrow=json.loads(raw)['decisions'][loc['item']-1];assert digest(oldrow)==loc['row_sha256'];out={'ordinal':n,'cid':cid,'original_full':P['original_records'][cid],'current_full':P['current_records'][cid],'exact5B_full':oldrow,'exact5B_locator':loc,'requiredCID_fullclosure':P['references'][cid],'requiredBinding_fullclosure':P['reference_bindings'][cid],'complete_current_ownbindings':{k:v for k,v in S['slot_bindings'].items()if v['candidate_id']==cid},'required_revision':rev,'controlled_wholeorigins':[]}
  assert S['candidates'][cid]==P['current_records'][cid]
  for ref in P['original_records'][cid]['provenance']:
   parts=ref['source'].split(':');assert parts[0]=='slot' and len(parts)==3;entry=next(z for z in C['slots'][parts[1]]if z['id']==parts[2]);same=digest(entry)==ref['sha256'];out['controlled_wholeorigins'].append({'provenance':ref,'exactsha_equal':same,'whole_entry':entry}if same else {'provenance':ref,'exactsha_equal':False,'no_meaning_from_mismatch':True})
 else:
  art=rev['prior_review']['artifact'];raw=Path(art['file']).read_bytes();assert hashlib.sha256(raw).hexdigest()==art['file_sha256'];doc=json.loads(raw);idx=int(rev['prior_review']['pointer'].split('/')[-1]);prior=doc['records'][idx];assert digest(prior)==rev['prior_review']['sha256'];out={'ordinal':n,'cid':cid,'exact_pinned_prior_research_row':prior,'boundary':'History only; no status/proof reused as new approval.'}
 print(json.dumps(compact(out),ensure_ascii=False,indent=2))
