"""Whole-record lexical navigation only; no absence, native or semantic approval claim."""
from pathlib import Path
import sys,json,re,collections
R=Path('/Users/chasoik/Projects/image-prompt');D=Path(__file__).resolve().parent;S=R/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(S/'scripts'));import photo_candidate_corpus as c
corpus=c.load(S/'assets');old=json.loads((D.parent/'espionage-20261023/keyword-routes.json').read_bytes());targets=[x for x in old if x['status']=='defer_specific_component_review']
def fixed(r):
 x=r.get('content',{});return ' '.join(str(x.get(f,'')) for f in ['en','ko','definition','aliases','phrase_en','phrase_ko']).lower()
def norm(s):return re.sub(r'[^\w]+',' ',s.casefold()).strip()
texts={cid:norm(fixed(v)) for cid,v in corpus['candidates'].items() if v['record_kind']!='diagnostic'}
report=[];snapshots={}
for t in targets:
 phrases=[norm(t['term_ko']),norm(t['term_en'])]+[norm(x) for x in t['term_en'].split('/') if len(x)>3]
 terms=set(norm(t['term_en']).split())-{'the','of','a','to','and','with','pose','gesture','clothing','wear'}
 scores=[]
 for cid,txt in texts.items():
  exact=sum(20+len(p) for p in phrases if p and (' '+p+' ') in (' '+txt+' '))
  if exact or terms:
   score=exact+sum(min(len(w),10) for w in terms if w in txt.split())
   if score:scores.append((score,cid))
 ranked=sorted(scores,reverse=True)[:3]
 for _,cid in ranked:snapshots[cid]={'record':corpus['candidates'][cid],'bindings':{k:v for k,v in corpus['slot_bindings'].items() if v['candidate_id']==cid}}
 report.append({'route_id':t['id'],'term':t['term_ko'],'english':t['term_en'],'navigation_only':True,'neighbors':[{'cid':cid,'finding_score_not_rank':s} for s,cid in ranked]})
(D/'neighbor-snapshots.json').write_text(json.dumps(snapshots,ensure_ascii=False,indent=2)+'\n');(D/'neighbor-findings.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
for row in report:
 cid=row['neighbors'][0]['cid'];r=snapshots[cid]['record'];print(json.dumps({'id':row['route_id'],'term':row['term'],'cid':cid,'kind':r['record_kind'],'content':r['content'],'conditions':r['conditions'],'effects':r['effects']},ensure_ascii=False))
