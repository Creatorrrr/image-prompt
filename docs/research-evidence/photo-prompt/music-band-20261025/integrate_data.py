"""Register reviewed optional music propositions while preserving all old source bytes."""
from pathlib import Path
import json,hashlib,copy,uuid,os,sys,gc
gc.disable()
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];S=ROOT/'skills/photo-prompt-image-generator';A=S/'assets';O=HERE/'integration-evidence'
sys.path.insert(0,str(S/'scripts'))
import photo_candidate_corpus as corpus
from photo_runtime_sources import source_update
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def write(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_name(p.name+'.music.tmp');tmp.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');os.replace(tmp,p)
NS=uuid.UUID('ca327641-9861-4596-9046-e1a66a4fd093')
def ident(prefix,key):return prefix+uuid.uuid5(NS,'music-band-20261025:'+key).hex
CONTRACT=('One complete optional authored music/band visual proposition, not a genre definition, compulsory styling bundle, real identity, verified musical performance or legal/clinical judgment. '
 'Retain every stated actor, count, limb owner, instrument, instrument part, garment layer, hand/string/bow/key/pedal contact, support, cable endpoint, screen region, depicted-image owner and comparison-view boundary in both languages. '
 'Keep acoustic instruments and model-specific electronic-pad trigger conditions separate; open rimshot is one rimshot variant, not a definition of every rimshot. '
 'Review every source condition and whole-proposition effect against independently frozen requester meaning and dimension/property locks. Roles and research graphs provide no native qualification, owner selection or adoption authority. '
 'Do not merge people, transfer a hand or instrument, omit a support endpoint, combine incompatible variants or count a reflected, photographed or displayed person as a new physical actor. '
 'All selected distinguishing components and both relation endpoints must be jointly visible; partial or hidden required evidence cannot pass. '
 'A still image cannot establish actual sound, timing, groove, repeated motion, chord pitch without tuning/position evidence, successful signal routing, working electronics, crowd consent/safety, biological age, personal identity, sexual orientation, desire, coercion, diagnosis, history, rank, authorship, revenue, rights or material chemistry. '
 'Explicit adult fictional performers remain an authored setting, not inferred age or biography of a reference portrait. Sources support bounded terminology/context, not the complete authored scene geometry.')
# Each entry is the complete source footprint, not the names of its presentation slots.
DIM_TEXT='''
A01 subject pose action appearance relationship
A02 subject pose action setting relationship
A03 subject pose action appearance relationship setting
A04 subject pose action relationship
A05 subject pose action relationship
A06 subject pose action relationship
A07 subject pose action material relationship
A08 subject pose action relationship
A09 subject pose action relationship
A10 subject pose action appearance relationship
A11 subject pose action relationship
A12 subject pose action relationship
A13 subject pose action material relationship
A14 subject count setting appearance relationship composition
A15 subject pose action setting relationship
A16 subject pose action setting relationship
A17 subject pose relationship
A18 subject pose relationship
A19 subject pose action relationship
A20 subject pose action relationship
A21 subject pose action setting relationship
A22 subject pose action relationship
A23 subject pose action setting relationship
A24 subject pose action relationship
A25 subject pose action setting relationship
A26 subject pose action setting relationship
A27 subject pose action relationship
A28 subject pose action appearance relationship
A29 subject pose action relationship
A30 subject count pose action setting relationship
A31 subject pose action setting relationship composition
A32 subject count pose action setting relationship
B01 subject pose setting relationship
B02 subject count pose action appearance setting relationship composition
B03 subject pose action setting appearance count composition
B04 subject count appearance composition format
B05 subject pose action appearance setting count composition
B06 subject appearance count composition
B07 subject setting count relationship
B08 subject setting count relationship
B09 subject count appearance composition format
B10 subject pose action setting relationship
B11 subject appearance count composition
B12 subject count pose action appearance setting relationship
B13 subject pose appearance setting composition relationship
B14 subject pose action setting relationship
C01 subject setting count composition format relationship
C02 subject pose action setting relationship
C03 subject count pose action setting relationship
C04 subject count pose action setting relationship composition
C05 subject pose setting composition
C06 subject count pose setting relationship
C07 subject appearance pose relationship
C08 subject count pose action setting relationship
C09 subject count pose action setting relationship
C10 subject pose action setting relationship
C11 subject setting appearance relationship
C12 subject pose setting count relationship
C13 subject count pose action setting relationship
C14 subject pose action setting relationship
E01 subject appearance format composition
E02 subject appearance
E03 subject appearance material
E04 subject appearance pose setting relationship
E05 subject appearance relationship
E06 subject age appearance pose relationship
E07 subject count appearance composition format
E08 subject age appearance relationship
E09 subject age appearance
E10 subject age appearance relationship
E11 subject appearance relationship
E12 subject age appearance
E13 subject age appearance material lighting
E14 subject age count appearance format composition
E15 subject appearance
E16 subject appearance
E17 subject count appearance pose setting relationship
E18 subject age appearance
E19 subject count appearance material lighting composition format
E20 subject age count appearance pose setting relationship
F01 subject appearance
F02 subject appearance
F03 subject appearance
F04 subject age appearance
F05 subject appearance
F06 subject appearance
F07 subject appearance
F08 subject age appearance
G01 subject count pose action setting relationship
G02 subject pose action setting relationship
G03 subject count pose action appearance relationship
G04 subject count pose action setting relationship
G05 subject pose action appearance setting relationship
G06 subject pose action appearance relationship
G07 subject pose action appearance relationship
G08 subject age pose action appearance relationship
G09 subject pose action appearance setting relationship
G10 subject pose action appearance setting relationship
G11 subject pose action relationship
G12 subject age pose setting
G13 subject count pose action setting relationship
G14 subject count pose action setting relationship
G15 subject age count pose setting relationship
G16 subject age count pose action setting relationship
H01 subject count pose action setting relationship
H02 subject count pose action setting relationship
H03 subject count pose action setting relationship
H04 subject count pose action setting relationship
H05 subject count pose action setting relationship
H06 subject count pose action setting relationship
H07 subject count pose action setting relationship
H08 subject count pose action setting relationship
H09 subject age count pose action setting relationship composition format
H10 subject appearance material
H11 subject age count pose action appearance setting relationship
H12 subject age pose action appearance setting relationship composition
H13 subject age pose appearance setting relationship
H14 subject age pose appearance setting relationship
H15 subject age pose action appearance setting relationship lighting
H16 subject age pose appearance setting relationship
H17 subject count pose action setting relationship
H18 subject age count pose action setting relationship
H19 subject age pose action setting count relationship
H20 subject appearance material setting relationship
'''
DIMS={r.split()[0]:r.split()[1:] for r in DIM_TEXT.strip().splitlines()}
REUSE={'C07':'cand_a49173126daf573f9083c0ae11ebf5c6','G02':'cand_f6c8550411b5540fb9f5ec318d4ef8cd'}
def main():
 O.mkdir(exist_ok=True)
 if (O/'data-integration.json').exists():raise SystemExit('Already integrated; preserve original evidence.')
 before=corpus.load(A);manifest_path=A/corpus.MANIFEST_NAME;manifest=read(manifest_path)
 protected={str(p.relative_to(ROOT)):sha(p) for p in [S/'SKILL.md',S/'retrieval-runtime.json',S/'precore/creative_controls.json',*A.glob('*.json')]}
 write(O/'integration-baseline.json',{'protected':protected,'manifest':manifest,'candidate_sha256':{cid:digest(r) for cid,r in before['candidates'].items()},'binding_sha256':{bid:digest(r) for bid,r in before['slot_bindings'].items()},'catalog_sha256':digest(before['slot_catalog']),'policies_sha256':digest(before['policies'])})
 cards=read(HERE/'semantic-cards.json');contexts=read(HERE/'context-distinctions.json');holds=read(HERE/'remaining-research.json');records={};bindings={};mapping={};decisions=[]
 exact={(r['content'].get('en'),r['content'].get('ko')):cid for cid,r in before['candidates'].items() if r['record_kind']!='diagnostic'}
 registered=[]
 for card in cards:
  key=card['id'];cid=REUSE.get(key) or exact.get((card['phrase_en'],card['phrase_ko']))
  if cid:
   old=before['candidates'][cid];mapping[key]=cid
   registered.append({**copy.deepcopy(card),'candidate_id':cid,'registration_status':'reused_complete_existing_source','registered_phrase_en':old['content']['en'],'registered_phrase_ko':old['content']['ko'],'native_approval':False})
   decisions.append({'card_id':key,'candidate_id':cid,'decision':'reuse_original_complete_source','preserved_conditions_effects_bindings':True,'native_approval':False});continue
  cid=ident('cand_',key);mapping[key]=cid
  meta={**copy.deepcopy(card),'runtime_importable':True,'candidate_id':cid,'native_approval':False,'native_qualification':'not_qualified','registration_status':'authored_optional_visual_source','source_conditions_and_effects_are_separate_from_research_metadata':True}
  conditions={'requires_adult_context':True} if 'adult' in card['phrase_en'].lower() else {}
  record={'id':cid,'record_kind':'visual_option','content':{'en':card['phrase_en'],'ko':card['phrase_ko'],'definition':card['phrase_en'],'aliases':[card['name_ko']],'application_contract':CONTRACT,'research_semantics':meta},'conditions':conditions,'effects':{'dimensions':DIMS[key],'properties':[]},'provenance':[{'source':'authored research docs/research-evidence/photo-prompt/music-band-20261025/semantic-cards.json#'+key,'sha256':sha(HERE/'semantic-cards.json')}]}
  records[cid]=record;registered.append(meta)
  for slot in card['proposed_slots']:
   assert slot in before['slot_catalog'];bid=ident('bind_',cid+':'+slot)
   bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional','semantic_role':before['slot_catalog'][slot]['semantic_role'],'conditions':{'subject_applicability':{}},'weight':1}
  decisions.append({'card_id':key,'candidate_id':cid,'decision':'new_complete_authored_visual_source','native_approval':False})
 for row in contexts+holds:
  key=row['id'];cid=ident('cand_',key);mapping[key]=cid
  text=row.get('meaning_boundary_ko') or row['reason_and_next_ko'];title=row.get('name_ko') or row['topic']
  records[cid]={'id':cid,'record_kind':'diagnostic','content':{'definition':'Music/band context or research hold, excluded from positive visual retrieval: '+title+'. '+text,'research_semantics':{**copy.deepcopy(row),'runtime_registration':True,'native_approval':False}},'conditions':{},'effects':{'dimensions':[],'properties':[]},'provenance':[{'source':'research music-band-20261025 '+key,'sha256':sha(HERE/('context-distinctions.json' if key.startswith('N') else 'remaining-research.json'))}]}
 cm='photo_candidate_music_band_20261025.json';bm='photo_candidate_music_band_bindings_20261025.json';sm='photo_music_band_semantics_20261025.json'
 for name in [cm,bm,sm]:assert not (A/name).exists(),name
 registry={'schema':'photo-music-band-visual-semantics/v1','cards':registered,'context_distinctions':contexts,'holds':holds,'sources':read(HERE/'sources.json'),'keyword_routes':[{**copy.deepcopy(k),'component_candidate_ids':[mapping[x] for x in k['optional_visual_components']],'contrast_candidate_ids':[mapping[x] for x in k['contrast_visual_cards']],'context_candidate_ids':[mapping[x] for x in k['context_ids']],'adoption_authority':False,'automatic_hard_activation':False} for k in read(HERE/'keyword-atlas.json')],'native_approval':False,'automatic_hard_activation':False,'research_snapshot_sha256':sha(HERE/'semantic-cards.json')}
 assert set(records).isdisjoint(before['candidates']) and set(bindings).isdisjoint(before['slot_bindings'])
 with source_update(S):
  assert sha(manifest_path)==protected[str(manifest_path.relative_to(ROOT))]
  write(A/cm,{'schema':corpus.MODULE_SCHEMAS['candidates'],'candidates':records});write(A/bm,{'schema':corpus.MODULE_SCHEMAS['slot_bindings'],'slot_bindings':bindings});write(A/sm,registry)
  manifest['modules'] += [{'file':cm,'kind':'candidates'},{'file':bm,'kind':'slot_bindings'}];write(manifest_path,manifest)
 after=corpus.load(A)
 assert all(after['candidates'][cid]==r for cid,r in before['candidates'].items())
 assert all(after['slot_bindings'][bid]==r for bid,r in before['slot_bindings'].items())
 assert all(after[k]==before[k] for k in ['slot_catalog','policies'])
 for name,data in [('card-candidate-map.json',mapping),('new-native-records.json',records),('changed-native-records.json',{}),('changed-native-prior.json',{})]:write(O/name,data)
 report={'status':'authored_source_integrated','positive_new':sum(r['record_kind']=='visual_option' for r in records.values()),'diagnostic_new':sum(r['record_kind']=='diagnostic' for r in records.values()),'bindings_new':len(bindings),'reused_complete_sources':len(REUSE),'semantic_cards':len(cards),'keyword_rows':len(registry['keyword_routes']),'before_candidates':len(before['candidates']),'after_candidates':len(after['candidates']),'existing_candidates_bindings_catalog_policies_preserved':True,'native_approval':False,'source_only_not_installed_yet':True,'decisions':decisions}
 write(O/'data-integration.json',report);print(json.dumps({k:v for k,v in report.items() if k!='decisions'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
