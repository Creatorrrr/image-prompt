"""Research integrity and read-only drift check, never native qualification."""
import collections, csv, hashlib, json, re, subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def read(name): return json.loads((HERE/name).read_text())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def require(value,label):
 if not value: raise AssertionError(label)

def main():
 cards_doc=read('semantic-cards.json');drafts_doc=read('candidate-drafts.json');routes=read('keyword-routes.json')['routes'];sources=read('sources.json')
 cards=cards_doc['cards'];drafts=drafts_doc['drafts'];cardmap={c['id']:c for c in cards};sourcemap={s['id']:s for s in sources}
 require(len(cardmap)==len(cards)==74,'unique cards');require(len(drafts)==64,'64 visual drafts');require(len(sourcemap)==len(sources)==40,'40 unique sources')
 require(cards_doc['runtime_importable'] is False and drafts_doc['runtime_importable'] is False,'not runtime importable')
 require([r['reference_id'] for r in routes]==list(range(1,131)),'complete ordered 130 terms')
 require(all(r['optional_visual_cards'] or r['context_cards'] for r in routes),'no unhandled keyword')
 require(all(set(r['optional_visual_cards']+r['context_cards'])<=set(cardmap) for r in routes),'route targets')
 require(all(r['term_kind']=='conversation_authored_motif_not_established_theory' for r in routes if r['reference_id']>=117),'creative motif provenance')
 require(all(c['native_approval'] is False for c in cards),'no native approval')
 catalog=json.loads((ROOT/'skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json').read_text())['slot_catalog']
 for c in cards:
  require(set(c['source_refs'])<=set(sourcemap),'source refs '+c['id'])
  require(set(c['proposed_slots'])<=set(catalog),'current slot IDs '+c['id'])
  require(c['claim_limit_ko'],'claim limit '+c['id'])
  if c['evidence_mode']=='context':
   require(not c['owners'] and not c['relations'] and not c['gates'] and c['phrase_en'] is None,'inert context '+c['id']);continue
  require(c['phrase_en'] and c['phrase_ko'] and c['owners'] and c['relations'],'complete draft '+c['id'])
  vertices=set(c['owners']);adj={x:set() for x in vertices}
  for r in c['relations']:
   require(r['subject'] in vertices and r['object'] in vertices,'graph endpoints '+c['id'])
   adj[r['subject']].add(r['object']);adj[r['object']].add(r['subject'])
  seen=set();todo=[next(iter(vertices))]
  while todo:
   node=todo.pop()
   if node in seen:continue
   seen.add(node);todo.extend(adj[node]-seen)
  require(seen==vertices,'disconnected or orphan owner '+c['id']+': '+str(vertices-seen))
  require(c['review_policy']['partial_is_fail'] and c['review_policy']['unobservable']=='UNOBSERVABLE_NOT_PASS','pixel boundary '+c['id'])
  require(len(c['gates'])==len(c['owners'])+len(c['relations']),'component and relation gates '+c['id'])
 for d in drafts:
  c=cardmap[d['research_id']]
  require(d['native_cid'] is None and d['native_rid'] is None and d['native_approval'] is False,'not a native record')
  require(d['phrase_en']==c['phrase_en'] and d['phrase_ko']==c['phrase_ko'],'card/draft byte equality')
  require(d['owners']==c['owners'] and d['relations']==c['relations'],'no draft graph loss')
 with (HERE/'EVALUATION-CASES.tsv').open() as f:cases=list(csv.DictReader(f,delimiter='\t'))
 require(len(cases)==len({c['id'] for c in cases})==124,'124 unique evaluation cases')
 require(all(c['status']=='NOT_RUN' and c['ko'] and c['en'] for c in cases),'evaluation has no fabricated run')
 require(all(c['card'] in cardmap for c in cases if c['card']),'evaluation card refs')
 require(len([x for x in cases if x['split']=='development_authored_with_card'])==64,'64 development cases')
 ledger=read('adoption-ledger.json')['entries'];require({x['card_id'] for x in ledger}==set(cardmap),'complete adoption ledger')
 neighbors=read('reviewed-neighbors.json')['records'];require(len(neighbors)==17,'17 reviewed neighbors')
 for n in neighbors:
  raw=json.dumps(n['record'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
  require(hashlib.sha256(raw).hexdigest()==n['record_sha256'],'source snapshot hash '+n['cid'])
  require(all(b['record']['candidate_id']==n['cid'] for b in n['bindings']),'binding source linkage '+n['cid'])
  require(set(n['related_research_cards'])<=set(cardmap),'neighbor card refs '+n['cid'])
 broken=[]
 for path in HERE.glob('*.md'):
  for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
   if '://' in link or link.startswith('#'):continue
   target=link.split('#')[0]
   if target and not (path.parent/target).exists() and target not in ['VALIDATION.json','SHA256SUMS']:broken.append([path.name,target])
 require(not broken,'broken local links '+str(broken))
 baseline=read('BASELINE.json');changed=[];missing=[]
 for rel,digest in baseline['tracked_sha256'].items():
  path=ROOT/rel
  if not path.is_file():missing.append(rel)
  elif sha(path)!=digest:changed.append(rel)
 protected_changed=[rel for rel,digest in baseline['protected_sha256'].items() if not (ROOT/rel).is_file() or sha(ROOT/rel)!=digest]
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 summary=read('SUMMARY.json');require(summary['gates']==sum(len(c['gates']) for c in cards),'summary gates')
 result=dict(schema='metafiction-research-validation/v1',research_integrity='PASS',
  overall_status='STRUCTURE_PASS_SOURCE_DRIFT_REQUIRES_REBASELINE' if changed or missing or protected_changed or head!=baseline['head'] else 'STRUCTURE_PASS',
  counts=summary,checks=['130 original routes','74 unique cards','64 bilingual draft/card byte matches','40 scoped source references','connected owner graphs and endpoint gates','124 unrun evaluation cases','17 hashed source snapshots and exact binding links','74 draft dispositions','local report links'],
  head_at_start=baseline['head'],head_at_validation=head,
  observed_external_state=dict(changed_tracked_files=changed,missing_tracked_files=missing,changed_protected_files=protected_changed,
   attribution='Observed differences, including concurrent work; not attributed to this research. Never revert to the old snapshot.'),
  writes_owned_by_this_task='only docs/research-evidence/photo-prompt/metafiction-existential-litrpg-20261022/',
  activity_boundary=dict(operating_source_registration='NOT_PERFORMED',embedding_inference='NOT_RUN',index_build_publish='NOT_RUN',h_f2_retrieval='NOT_RUN',image_generation='NOT_RUN',native_pixel_review='NOT_RUN',commit_push='NOT_PERFORMED',user_acceptance='not_yet_received'),
  limitations=['Integrity validates references, graphs, snapshots and non-live status only.','No exhaustive corpus semantic approval, native source approval, retrieval gain, pixel fidelity or artistic acceptance.'])
 (HERE/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 rows=[]
 for p in sorted(HERE.rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS':rows.append(sha(p)+'  '+str(p.relative_to(HERE)))
 (HERE/'SHA256SUMS').write_text('\n'.join(rows)+'\n')
 print(json.dumps(dict(research_integrity='PASS',overall_status=result['overall_status'],cards=len(cards),drafts=len(drafts),sources=len(sources),cases=len(cases),changed_tracked=len(changed),protected_drift=len(protected_changed),checksummed_files=len(rows)),ensure_ascii=False))
if __name__=='__main__':main()
