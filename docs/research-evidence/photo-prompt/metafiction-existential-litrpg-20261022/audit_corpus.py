"""Fixed-field source inspection; never imports retrieval or writes operating data."""
import collections, hashlib, json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
FIELDS = ('en', 'ko', 'definition', 'phrase_en', 'phrase_ko', 'composition_instruction', 'runtime_expression')
FOCUS = {
 'frame_crossing': r'metaleps|fourth.wall|frame.boundary|picture.frame|그림.*밖|프레임.*밖',
 'recursion': r'mise.en.abyme|recursive|recursion|miniature|재귀|축소.*모형',
 'world_interface': r'\bdiegetic\b|\bholographic\b|status.screen|\bquest\b|상태창|퀘스트',
 'character_sheet': r'character.sheet|skill.tree|ability.score|캐릭터.시트|스킬.트리|능력치',
 'affinity_control': r'affinity|reputation|호감도|평판',
 'copies': r'doppelg|clone|duplicate.*person|도플갱어|복제.*인물|복제인간',
 'erased_records': r'\bredacted\b|\berased\b|crossed.out|\bredaction\b|삭제|말소(?!리)|검열',
 'save_respawn': r'respawn|save.point|checkpoint|time.loop|리스폰|세이브|시간.루프',
 'world_seams': r'wireframe|missing.texture|unfinished.world|와이어프레임|텍스처',
 'restraint_connection': r'puppet|marionette|tether|꼭두각시|인형.실|속박',
 'body_interface': r'prosthetic|body.modification|신체.개조|인공.팔|의수',
 'found_document': r'found.document|palimpsest|marginalia|manuscript|여백|양피지|필사본',
 'spectacle': r'audience|surveillance|spectacle|관객|감시.카메라|구경거리',
 'item_person': r'soul.bind|inventory|인벤토리|영혼.귀속',
}

def sha(raw): return hashlib.sha256(raw).hexdigest()
def dump(name,obj): (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def strings(x,pointer):
 if isinstance(x,str): yield pointer,x
 elif isinstance(x,dict):
  for k,v in x.items(): yield from strings(v,pointer+'/'+k)
 elif isinstance(x,list):
  for i,v in enumerate(x): yield from strings(v,pointer+'/'+str(i))
def selected(record):
 for k in FIELDS:
  if k in record.get('content',{}): yield from strings(record['content'][k],'/content/'+k)
 for rid,branch in record.get('realizations',{}).items():
  if not isinstance(branch,dict): continue
  for box,obj in [('',branch),('/content',branch.get('content',{}))]:
   for k in FIELDS:
    if k in obj: yield from strings(obj[k],'/realizations/'+rid+box+'/'+k)

def main():
 manifest_path=ASSETS/'photo_candidate_corpus_manifest.json';raw=manifest_path.read_bytes();m=json.loads(raw)
 candidates={};bindings={};owners={};hashes={};duplicates=[]
 for mod in m['modules']:
  data_raw=(ASSETS/mod['file']).read_bytes();hashes[mod['file']]=sha(data_raw);d=json.loads(data_raw)
  for cid,r in d.get('candidates',{}).items():
   if cid in candidates: duplicates.append(cid)
   candidates[cid]=r;owners[cid]=mod['file']
  bindings.update(d.get('slot_bindings',{}))
 texts={cid:list(selected(r)) for cid,r in candidates.items()}
 focus=[];chosen=collections.defaultdict(list)
 for name,pattern in FOCUS.items():
  pat=re.compile(pattern,re.I); hits=[]
  for cid,values in texts.items():
   found=[{'pointer':p,'text':v} for p,v in values if pat.search(v)]
   if found: hits.append({'cid':cid,'module':owners[cid],'matched_fields':found})
  # Shortest complete positive record is only an inspectable shortlist, not a relevance rank.
  shortlist=sorted(hits,key=lambda h:(not bool(candidates[h['cid']].get('content',{}).get('en')),len(candidates[h['cid']].get('content',{}).get('en','')),h['cid']))[:3]
  for h in shortlist: chosen[h['cid']].append(name)
  focus.append({'family':name,'pattern':pattern,'lexical_matches':len(hits),'shortlist':shortlist,'interpretation':'fixed-field lexical evidence, not relevance rank or absence proof'})
 refs=json.loads((HERE/'reference-conversation.json').read_text())['tables']
 terms=[r for table in refs for r in table if len(r)==3 and r[0].isdigit()]
 term_results=[]
 for row in terms:
  label=row[1];parts=re.split(r' — | / |·',label);parts=[re.sub(r'\s*\[.*?\]','',s).strip() for s in parts];parts=[s for s in parts if len(s)>=3]
  patterns=[re.compile((r'(?<![a-z])'+re.escape(t)+r'(?![a-z])') if t.isascii() else re.escape(t),re.I) for t in parts]
  hit_ids=[cid for cid,vals in texts.items() if any(p.search(v) for _,v in vals for p in patterns)]
  term_results.append({'seed_id':int(row[0]),'label':label,'patterns':parts,'count':len(hit_ids),'cids':hit_ids})
 mapping=[]
 for cid,reasons in chosen.items():
  r=candidates[cid]; related=[{'binding_id':bid,'record':b} for bid,b in bindings.items() if b.get('candidate_id')==cid]
  mapping.append({'cid':cid,'module':owners[cid],'reasons':reasons,'record':r,'bindings':related,'record_sha256':sha(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()),'decision':'requires_semantic_review','native_approval':False})
 drift=[f for f,h in hashes.items() if sha((ASSETS/f).read_bytes())!=h]
 audit={'schema':'metafiction-corpus-lexical-audit/v1','candidate_count':len(candidates),'binding_count':len(bindings),'module_count':len(m['modules']),'selected_fields':FIELDS,'excluded_fields':['aliases','tags','negative text','metadata','research notes'],'module_sha256':hashes,'manifest_sha256':sha(raw),'duplicate_ids':duplicates,'changes_during_read':drift,'manifest_changed_during_read':sha(manifest_path.read_bytes())!=sha(raw),'focus':focus,'term_results':term_results,'limit':'Source diagnostic only. No H-F2 search, embedding, ranking, exposure or native-image qualification.'}
 dump('CORPUS-LEXICAL-AUDIT.json',audit);dump('existing-source-mapping.json',mapping)
 print(json.dumps({'candidates':len(candidates),'bindings':len(bindings),'modules':len(m['modules']),'mapping_records':len(mapping),'zero_literal_terms':sum(x['count']==0 for x in term_results),'focus_counts':{f['family']:f['lexical_matches'] for f in focus},'read_drift':drift},ensure_ascii=False))
if __name__=='__main__': main()
