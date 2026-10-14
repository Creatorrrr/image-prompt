"""Lossless bounded reader; exact old values reference only previously actually read frozen own drafts. No semantic compression."""
import json,hashlib,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');AD=R/'authored';F=AD/'native_11870_01575_02250.inputs-149v6-v1.json';assert hashlib.sha256(F.read_bytes()).hexdigest()=='236243a76a30860a1a0b6770a8c65596d19fea1f1e0a8dcfb53e6f0f1b345273';I=json.loads(F.read_text());lo,hi=map(int,sys.argv[1:3]);assert 1625<=lo<hi<=2250 and hi-lo<=5
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def dig(x):return hashlib.sha256(canon(x)).hexdigest()
cache={};pins=[]
def add(x,file,pointer):
 key=canon(x)if isinstance(x,(str,list,dict))else b''
 if len(key)>35:cache.setdefault(key,{'file':str(file),'pointer':pointer,'sha256':dig(x)})
 if isinstance(x,dict):
  for k,v in x.items():add(v,file,pointer+'/'+k.replace('~','~0').replace('/','~1'))
 elif isinstance(x,list):
  for n,v in enumerate(x):add(v,file,pointer+'/'+str(n))
# Fixed immutable actual-read baseline; extending it requires a new reader version.
for start in range(1575,1625,5):
 p=AD/f'native_11870_01575_02250.{start:05d}_{start+5:05d}.native-draft-149v6-v1.json';b=json.loads(p.read_text());assert b['range']==[start,start+5]and b['actual_complete_after_reread_count']==5;np=R/f'worker-notes/native-11870-{start:05d}-{start+5:05d}-149v6-v1.json';note=json.loads(np.read_text());assert note['actual_new_source_wholeafter_count']==5
 pins.append({'file':str(p),'file_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sha256':dig(b),'actual_read_note_file':str(np),'actual_read_note_file_sha256':hashlib.sha256(np.read_bytes()).hexdigest()})
 for ix,row in enumerate(b['records']):
  # Only whole values actually printed/read in source or whole-after review, never unseen prepared fields.
  for field in ['original_full','actual_current_full','corrected5B_full','compiled5B_full','compiled5B_locator','original_full_closure','actual_current_full_closure','corrected5B_full_closure','proposed_source_after']:
   add(row[field],p,f'/records/{ix}/{field}')
print(json.dumps({'schema':'lossless-previous-direct-read-reference-index/v1','input_file':str(F),'input_sha256':dig(I),'exact_prior_read_range':[1575,1625],'frozen_previous_actual_read_artifact_pins':pins,'boundary':'References denote canonical-equal full values at real artifact pointers, never meaning summaries. Current new strings/branches/relations print fully. Existing reader v1 remains immutable. No read claimed from digest alone.'},ensure_ascii=False))
origin=json.loads(Path('docs/research-evidence/photo-prompt/slot-retrieval-stage05-20261012/CONTROLLED-FINAL-SOURCE.json').read_text())
def compact(x,pointer,local):
 key=canon(x)if isinstance(x,(str,list,dict))else b''
 if len(key)>35:
  if key in cache:return {'$exact_equal_previously_direct_read':cache[key]}
  if key in local:return {'$exact_full_canonical_equal_value_at':local[key]}
  local[key]=pointer
 if isinstance(x,dict):return {k:compact(v,pointer+'/'+k.replace('~','~0').replace('/','~1'),local)for k,v in x.items()}
 if isinstance(x,list):return [compact(v,pointer+'/'+str(n),local)for n,v in enumerate(x)]
 return x
for n in range(lo,hi):
 cid=I['ids'][n-1575];v=I['records'][cid];out={k:v[k]for k in ['ordinal','candidate_id','original_full','actual_current_full','corrected5B_full','original_actual_rids','current_actual_rids','corrected5B_actual_rids','original_closure','actual_current_closure','corrected5B_closure','compiled5B_full','compiled5B_locator','original_sha256','actual_current_sha256','corrected5B_sha256']};out['controlled_original_whole_if_sha_equal']=[]
 for pr in v['original_full']['provenance']:
  parts=pr['source'].split(':');found=[r for r in origin.get('slots',{}).get(parts[1],[])if len(parts)==3 and parts[0]=='slot'and r.get('id')==parts[2]]if len(parts)==3 else[]
  if len(found)==1 and dig(found[0])==pr['sha256']:out['controlled_original_whole_if_sha_equal'].append({'provenance':pr,'canonical_equality':True,'whole_entry':found[0]})
  else:out['controlled_original_whole_if_sha_equal'].append({'provenance':pr,'canonical_equality':False,'no_meaning_from_mismatch':True})
 print('ORDINAL',n);print(json.dumps(compact(out,'',{}),ensure_ascii=False,indent=2))
