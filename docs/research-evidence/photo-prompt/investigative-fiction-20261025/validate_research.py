"""Research integrity checks only, not source qualification or image evaluation."""
from pathlib import Path
import collections, hashlib, json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
def read(name):return json.loads((HERE/name).read_text())
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
 errors=[];warnings=[]
 def check(ok,message):
  if not ok: errors.append(message)
 s=read('sources.json');src={r['id'] for r in s};cards=read('semantic-cards.json');vis=cards['visual_cards'];ctx=cards['context_cards'];ids={r['id'] for r in vis+ctx};routes=read('keyword-routes.json');drafts=read('candidate-drafts.json');dev=read('development-cases.json');snap=read('corpus-snapshot.json');dec=read('existing-source-decisions.json')
 check(len(ids)==len(vis)+len(ctx),'duplicate card ID')
 check(len({r['id'] for r in routes})==len(routes),'duplicate keyword ID')
 check(len({r['id'] for r in dev})==len(dev),'duplicate development ID')
 check(sum(r['row_kind']=='keyword' for r in routes)==321,'incomplete source keyword rows')
 check(sum(r['row_kind']=='confusion' for r in routes)==10,'incomplete confusion rows')
 check(sum(r['row_kind']=='authored_scene_example' for r in routes)==8,'incomplete scene examples')
 capture=read('reference-capture.json')
 check(sum(capture['table_rows_including_headers'])-24+1==len(routes),'capture/route count mismatch')
 slots=json.loads((ASSETS/'photo_candidate_slot_catalog.json').read_text())['slot_catalog']
 for c in vis+ctx:
  check(set(c['source_ids'])<=src,c['id']+' unknown source')
  check(c['native_approval'] is False,c['id']+' false approval')
  check(c['runtime_registration']=='NOT_APPLIED',c['id']+' false runtime state')
  if not c['source_keyword_ids']:warnings.append(c['id']+' has no direct original term route; review scope')
 for c in vis:
  check(c['positive_en']!=c['positive_ko'],c['id']+' bilingual duplication')
  check(bool(c['positive_en'].strip()) and bool(c['positive_ko'].strip()),c['id']+' missing bilingual text')
  check(set(c['suggested_slots'])<=set(slots),c['id']+' unknown slot')
  check(all(t['from'] in c['owner_nodes'] and t['to'] in c['owner_nodes'] for t in c['relations']),c['id']+' disconnected relation')
  check(c['pixel_status']==c['retrieval_status']==c['native_qualification']=='NOT_RUN',c['id']+' false execution status')
 for r in routes:
  check(set(r['optional_or_adjacent_visual_cards']+r['context_cards'])<=ids,r['id']+' unknown card route')
  check(bool(r['context_cards']),r['id']+' missing boundary route')
 for d in drafts:
  c=next(x for x in vis if x['id']==d['source_card_id'])
  check(d['positive_en']==c['positive_en'] and d['positive_ko']==c['positive_ko'],d['draft_id']+' incomplete source proposition')
  check(d['candidate_id'] is None and d['native_approval'] is False,d['draft_id']+' runtime ID/approval leak')
  check(d['runtime_registration']=='NOT_APPLIED',d['draft_id']+' false registration')
 check(all(x['status']=='NOT_RUN' and not x['independent_holdout'] for x in dev),'false evaluation/holdout claim')
 changed=[]
 for mod in snap['modules']:
  p=ASSETS/mod['file']
  if not p.exists() or sha(p.read_bytes())!=mod['sha256']:changed.append(mod['file'])
 check(not changed,'runtime source module drift: '+', '.join(changed))
 check(sha((ASSETS/'photo_candidate_corpus_manifest.json').read_bytes())==snap['manifest_sha256'],'manifest drift')
 runtime=ROOT/'skills/photo-prompt-image-generator/retrieval-runtime.json'
 check(sha(runtime.read_bytes())==snap['runtime_selector_sha256'],'runtime selector drift')
 current={}
 for mod in snap['modules']:
  if mod['kind']=='candidates':current.update(json.loads((ASSETS/mod['file']).read_text())['candidates'])
 for d in dec:
  check(d['cid'] in current,d['cid']+' no longer exists')
  if d['cid'] in current:check(current[d['cid']]==d['source_snapshot']['record'],d['cid']+' decision/source drift')
  check(d['runtime_change']=='NOT_APPLIED',d['cid']+' false source modification')
 required=['README.md','RESEARCH.md','IMPLEMENTATION-PLAN.md','PIXEL-PLAN.md','CORPUS-FINDINGS.md','KEYWORD-ATLAS.md','SOURCES.md','VISUAL-CARDS.md']
 for f in required:check((HERE/f).is_file(),'missing report '+f)
 for f in required:
  p=HERE/f
  if p.exists():
   import re
   for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
    if target.startswith(('http:','https:','#')):continue
    generated_here={'VALIDATION.json','FILES.sha256.json'}
    check(target in generated_here or (p.parent/target.split('#')[0]).exists(),f+' broken local link '+target)
 report={'research_integrity':'PASS' if not errors else 'FAIL','errors':errors,'warnings':warnings,'counts':{'keywords':321,'all_routes':len(routes),'visual_cards':len(vis),'visual_mode_counts':dict(collections.Counter(c['mode'] for c in vis)),'context_cards':len(ctx),'sources_including_reference':len(s),'existing_source_decisions':len(dec),'development_requests':len(dev)},'source_modules_compared':len(snap['modules']),'runtime_source_modules_unchanged_from_snapshot':not changed,'runtime_selector_unchanged_from_snapshot':sha(runtime.read_bytes())==snap['runtime_selector_sha256'],'limits':['No independent verification of every original term','No exhaustive semantic duplicate detection','No native qualification','No runtime retrieval/composition execution','No image generation or saved pixel review','No user acceptance','Hash equality verifies compared source bytes, not correctness or a globally clean checkout']}
 (HERE/'VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 hashes={str(p.relative_to(HERE)):sha(p.read_bytes()) for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in str(p) and p.name!='FILES.sha256.json'}
 (HERE/'FILES.sha256.json').write_text(json.dumps(hashes,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report,ensure_ascii=False,indent=2))
 if errors:raise SystemExit(1)
if __name__=='__main__':main()
