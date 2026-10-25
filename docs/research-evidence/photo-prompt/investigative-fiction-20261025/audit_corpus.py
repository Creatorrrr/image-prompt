"""Read manifest-owned source. Lexical navigation only; never a retrieval score."""
from pathlib import Path
import collections, hashlib, json, re, subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
PATTERNS = {
 'investigation': r'\bdetective\b|\binvestigat(?:or|ion|ive)\b|\bpolice\b|수사|형사|탐정|경찰',
 'scene_evidence': r'crime.scene|evidence.marker|chain.of.custody|forensic.scale|현장감식|증거.{0,5}(봉|표지|인계|봉인)|검체',
 'forensic': r'\bforensic\b|\bautopsy\b|\bmorgue\b|\bluminol\b|fingerprint|법의|부검|루미놀|지문',
 'interview': r'interrogat|witness.interview|investigative.interview|피의자|신문실|목격자|진술',
 'digital_finance': r'write.block|forensic.image|hash.verification|beneficial.owner|money.launder|디지털 포렌식|자금.추적|실소유자',
 'narrative': r'whodunit|howdunit|howcatchem|locked.room|cold.case|red.herring|미제|밀실|알리바이|레드.헤링',
 'noir': r'\bnoir\b|hard.boiled|femme.fatale|누아르|느와르|하드보일드|팜므.파탈',
 'wardrobe': r'deerstalker|inverness|trench.coat|fedora|duty.belt|ballistic.vest|니트릴|감식복|디어스토커|인버네스|트렌치|페도라',
 'harm_context': r'sextortion|trafficking|sexual.assault|necrophil|dismember|torture|섹스토션|인신매매|성폭력|시체성애|시신.절단|고문',
}

def digest(raw): return hashlib.sha256(raw).hexdigest()
def main():
 target=HERE/'corpus-snapshot.json'
 if target.exists(): raise SystemExit('Snapshot already exists; preserve it and use another baseline path.')
 mp=ASSETS/'photo_candidate_corpus_manifest.json'; mr=mp.read_bytes(); manifest=json.loads(mr)
 records={}; bindings=collections.defaultdict(list); modules=[]; errors=[]
 for mod in manifest['modules']:
  p=ASSETS/mod['file']
  if not p.exists(): errors.append({'missing':mod['file']}); continue
  raw=p.read_bytes(); d=json.loads(raw)
  modules.append({**mod,'sha256':digest(raw),'bytes':len(raw)})
  if mod['kind']=='candidates':
   for cid,rec in d['candidates'].items():
    if cid in records: errors.append({'duplicate_cid':cid})
    records[cid]={'file':mod['file'],'record':rec}
  elif mod['kind']=='slot_bindings':
   for bid,b in d['slot_bindings'].items(): bindings[b['candidate_id']].append(b)
 hits={}; stats={}
 for name,pattern in PATTERNS.items():
  rx=re.compile(pattern,re.I); rows=[]
  for cid,item in records.items():
   c=item['record'].get('content',{}); searchable=json.dumps(c,ensure_ascii=False)
   if rx.search(searchable): rows.append({'cid':cid,'file':item['file'],'en':c.get('en'),'ko':c.get('ko'),'record_kind':item['record'].get('record_kind'),'binding_slots':sorted({b['slot_id'] for b in bindings[cid]})})
  hits[name]=rows; stats[name]=len(rows)
 status=subprocess.run(['git','status','--porcelain'],cwd=ROOT,capture_output=True,text=True,check=True).stdout
 runtime=ROOT/'skills/photo-prompt-image-generator/retrieval-runtime.json'
 report={'date_kst':'2026-10-25','scope':'working-tree manifest-owned source; lexical navigation only','git_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'git_status_counts':dict(collections.Counter(x[:2] for x in status.splitlines())),'manifest_sha256':digest(mr),'modules':modules,'candidate_count':len(records),'record_kind_counts':dict(collections.Counter(x['record'].get('record_kind','missing') for x in records.values())),'binding_count':sum(map(len,bindings.values())),'errors':errors,'patterns':PATTERNS,'lexical_counts':stats,'hits':hits,'runtime_selector':json.loads(runtime.read_text()) if runtime.exists() else None,'runtime_selector_sha256':digest(runtime.read_bytes()) if runtime.exists() else None,'claims_not_tested':['semantic absence','BM25F rank','cosine rank','native qualification','installed snapshot equality','composition','pixels','user acceptance']}
 target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 (HERE/'corpus-hit-details.json').write_text(json.dumps({cid:{**records[cid],'bindings':bindings[cid]} for cid in sorted({x['cid'] for rows in hits.values() for x in rows})},ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ['git_head','candidate_count','binding_count','record_kind_counts','errors','lexical_counts']},ensure_ascii=False,indent=2))
 for key in ['investigation','scene_evidence','forensic','digital_finance','narrative','noir','wardrobe']:
  print(key)
  for row in hits[key][:25]: print(row['cid'],row['en'],row['ko'])
if __name__=='__main__': main()
