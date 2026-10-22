"""Register reviewed complete LitRPG variants without changing existing records."""
import copy,hashlib,json,sys,uuid
from pathlib import Path
ROOT=Path('/Users/chasoik/Projects/image-prompt');S=ROOT/'skills/photo-prompt-image-generator';A=S/'assets'
Q=ROOT/'docs/research-evidence/photo-prompt/litrpg-20261022';O=Path(__file__).resolve().parent
sys.path.insert(0,str(S/'scripts'))
import photo_candidate_corpus as c
from photo_runtime_sources import source_update
from photo_installed_h_f2 import default_store,release
def read(p):return json.loads(p.read_bytes())
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def file_sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
# Reviewed whole bilingual proposition footprints, not inferred from slot tags.
FOOTPRINTS='''U01:subject pose material appearance body_geometry composition relationship setting text
U02:setting composition appearance text
U03:subject action pose count material appearance relationship text composition
U04:subject body_geometry appearance material relationship text
U05:subject body_geometry material appearance relationship composition text
U06:subject appearance material body_geometry composition relationship text
U07:material appearance text composition relationship
U08:appearance body_geometry composition relationship text count
I01:text appearance composition relationship
I02:text appearance count body_geometry composition relationship
I03:text appearance composition relationship
I04:text appearance composition relationship
I05:text appearance count body_geometry composition relationship
I06:text appearance count body_geometry composition relationship
I07:subject body_geometry appearance count text composition relationship
I08:text appearance count composition relationship
Q01:material appearance relationship composition setting count
Q02:text appearance composition relationship setting
Q03:text appearance count composition relationship
Q04:text appearance count body_geometry composition relationship
Q05:text appearance body_geometry composition relationship
Q06:material appearance body_geometry count setting composition relationship
Q07:text appearance composition relationship
Q08:material appearance body_geometry composition relationship
Q09:material appearance count action composition relationship setting
Q10:text appearance count composition relationship
Q11:material appearance count pose text composition relationship
Q12:text appearance count composition relationship
C01:subject count pose action material body_geometry composition relationship
C02:subject count action pose appearance relationship composition
C03:text appearance body_geometry composition relationship
C04:subject appearance text composition relationship
C05:subject count pose appearance composition relationship setting
C06:text appearance count composition relationship
C07:subject count body_geometry appearance pose composition relationship setting
C08:subject count text appearance composition relationship
W01:setting material body_geometry appearance composition relationship
W02:setting body_geometry appearance composition relationship
W03:setting material appearance body_geometry count composition relationship
W04:setting appearance text composition relationship
W05:setting material appearance body_geometry composition relationship
W06:subject action pose material appearance composition relationship setting text
D01:setting material appearance count composition relationship
D02:text appearance composition relationship
D03:text appearance count composition relationship
H01:subject material appearance body_geometry composition relationship
H02:subject appearance material body_geometry composition relationship
H03:subject appearance material body_geometry composition relationship
H04:subject appearance text composition relationship
R01:subject count text appearance composition relationship
R02:subject text appearance composition relationship
R03:text appearance composition relationship
R04:text appearance count composition relationship
R05:text appearance count composition relationship
E01:subject count text appearance composition relationship
E02:appearance count body_geometry composition relationship
E03:text appearance composition relationship
E04:appearance body_geometry composition relationship
E05:text appearance composition relationship
E06:text appearance count composition relationship'''
EFFECTS={k:v.split() for k,v in (l.split(':') for l in FOOTPRINTS.splitlines())}
APP='One complete optional authored visual realization. Preserve all English and Korean owners, parts, counts, materials, labels, displayed values, states and directed relationships together, including actual attachment and comparison endpoints. Apply only when compatible with independently frozen requester meaning and every affected dimension/property; do not invent an owner or erase a source condition to force a fit. A displayed label, statistic, probability, relationship or contract depicts a claim made by that display, not its truth, causal efficacy, consent, diagnosis, personal identity or history. Research graphs, keyword routes, citations and proposed slots are review metadata and create no native facts, guard support, permissions or native qualification. All required components and endpoints must be observable together; partial or hidden required evidence fails the whole case.'
def main():
 original=c.load(A);config=read(S/'retrieval-runtime.json');store=default_store();native,h,n=release(store,config['generation_id'])
 before={'config':config,'store':str(store),'native':str(native),'corpus_sha256':c.digest(original),'working_candidate_count':len(original['candidates']),'working_binding_count':len(original['slot_bindings']),'manifest_sha256':file_sha(A/c.MANIFEST_NAME)}
 write(O/'before.json',before)
 cards=read(Q/'semantic-cards.json');routes=read(Q/'keyword-routes.json');sources={s['id']:s for s in read(Q/'sources.json')}
 assert {x['id'] for x in cards if x['evidence_mode'] in ('still','displayed')}==set(EFFECTS)
 records={};bindings={};registry=[];decisions=[]
 for card in cards:
  key=card['id'];visual=key in EFFECTS;cid='cand_'+uuid.uuid5(uuid.NAMESPACE_URL,'image-prompt/litrpg-system/20261022/'+key).hex
  assert cid not in original['candidates']
  terms=[r['label'] for r in routes if key in r['card_ids']]
  aliases=list(dict.fromkeys([card['title_ko']]+terms))
  meta={**copy.deepcopy(card),'schema':'photo-litrpg-system-visual-semantics/v1','candidate_id':cid,'registration_status':'authored_optional_source' if visual else 'diagnostic_context','source_details':[sources[s] for s in card['source_ids']],'native_qualification':'not_qualified','graph_scope':'Advisory research relation graph; no typed native facts or permissions.','provenance_digest_scope':'research specification bytes, not hash of remote pages'}
  records[cid]={'id':cid,'record_kind':'visual_option' if visual else 'diagnostic','content':{'en':card['phrase_en'],'ko':card['phrase_ko'],'definition':('Optional complete authored visual realization: '+card['phrase_en']) if visual else 'Context or sequence distinction excluded from positive material retrieval.','aliases':aliases,'application_contract':APP if visual else 'Context diagnostic only. Retain the nonvisual or sequential claim without imposing a still-image object, pose, genre duty or positive native fact.','research_semantics':meta},'conditions':{},'effects':{'dimensions':sorted(set(EFFECTS[key])) if visual else [],'properties':[]},'provenance':[{'source':sources[s]['url'],'sha256':file_sha(Q/'semantic-cards.json')} for s in card['source_ids']]}
  registry.append(meta)
  for slot in card['proposed_slots'] if visual else []:
   assert slot in original['slot_catalog'];bid='bind_'+uuid.uuid5(uuid.NAMESPACE_URL,cid+'/'+slot).hex
   bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional','semantic_role':original['slot_catalog'][slot]['semantic_role'],'conditions':{'subject_applicability':{}},'weight':2}
  decisions.append({'card_id':key,'candidate_id':cid,'decision':'bounded_optional_variant' if visual else 'context_only','reason':'Preserve all old sources. New whole bilingual proposition differs in information function, carrier, exact owner/endpoint or optional staging. Existing D01-D08 comparison is documented; exhaustive novelty and native qualification are not claimed.','native_approval':False})
 proposed=copy.deepcopy(original);proposed['candidates'].update(records);proposed['slot_bindings'].update(bindings);c.validate(proposed)
 cm='photo_candidate_litrpg_system_20261022.json';bm='photo_candidate_litrpg_system_bindings_20261022.json'
 with source_update(S):
  assert c.digest(c.load(A))==c.digest(original),'Concurrent corpus drift; rebase before writing'
  manifest=read(A/c.MANIFEST_NAME);assert not any(m['file'] in [cm,bm] for m in manifest['modules'])
  write(A/cm,{'schema':c.MODULE_SCHEMAS['candidates'],'candidates':records});write(A/bm,{'schema':c.MODULE_SCHEMAS['slot_bindings'],'slot_bindings':bindings})
  manifest['modules'] += [{'file':cm,'kind':'candidates'},{'file':bm,'kind':'slot_bindings'}];write(A/c.MANIFEST_NAME,manifest)
  actual=c.load(A);assert actual==proposed
 assert all(actual['candidates'][k]==v for k,v in original['candidates'].items())
 assert all(actual['slot_bindings'][k]==v for k,v in original['slot_bindings'].items())
 assert all(actual[k]==original[k] for k in ['slot_catalog','policies'])
 lookup={x['id']:x['candidate_id'] for x in registry}
 result={'schema':'photo-litrpg-system-semantic-registry/v1','cards':registry,'keyword_routes':[{**r,'candidate_ids':[lookup[k] for k in r['card_ids']]} for r in routes],'decisions':decisions,'counts':{'semantic_cards':len(cards),'visual_options':len(EFFECTS),'diagnostics':len(cards)-len(EFFECTS),'bindings':len(bindings),'keyword_routes':len(routes)},'native_approval':False}
 write(A/'photo_litrpg_system_semantics_20261022.json',result);write(O/'data-integration.json',result)
 write(O/'new-native-records.json',records);write(O/'changed-native-records.json',{})
 write(O/'source-preservation.json',{'status':'pass','old_candidate_records_preserved':len(original['candidates']),'old_bindings_preserved':len(original['slot_bindings']),'old_catalog_and_policies_preserved':True,'total_candidate_records':len(actual['candidates']),'total_bindings':len(actual['slot_bindings']),'after_corpus_sha256':c.digest(actual),**result['counts']})
 print(json.dumps(read(O/'source-preservation.json')))
if __name__=='__main__':main()
