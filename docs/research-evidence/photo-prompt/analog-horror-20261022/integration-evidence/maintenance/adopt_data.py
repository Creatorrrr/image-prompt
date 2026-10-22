"""Bounded analog-horror source adoption; preserve every preexisting record."""
from pathlib import Path
import copy,hashlib,json,sys,uuid
ROOT=Path('/Users/chasoik/Projects/image-prompt');S=ROOT/'skills/photo-prompt-image-generator';A=S/'assets'
Q=ROOT/'docs/research-evidence/photo-prompt/analog-horror-20261022';O=Path(__file__).resolve().parent
sys.path.insert(0,str(S/'scripts'))
import photo_candidate_corpus as c
from photo_runtime_sources import source_update
read=lambda p:json.loads(p.read_bytes())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

# Full-proposition changes reviewed from both languages. The footprint includes
# added setting, text, counts and participants, rather than the presentation slot.
FOOTPRINTS='''
A001:material appearance text count relationship
A003:material appearance count relationship composition
A004:appearance text count composition
A005:material appearance lighting composition
A006:appearance style composition
A007:subject age pose action camera material relationship composition
A008:material appearance count relationship composition
A009:material appearance count relationship composition
A010:framing composition appearance
A011:appearance text count composition style
A013:appearance text composition style
A014:appearance text count composition style
A016:appearance text composition
A017:appearance text count composition
A018:appearance style composition
A019:appearance style composition
A020:appearance style composition
A021:setting appearance body_geometry composition
A022:appearance count composition
A023:appearance color text composition
A024:appearance color composition
A025:appearance color composition
A026:setting appearance count composition
A027:appearance lighting composition
A028:subject body_geometry appearance composition
A029:setting appearance lighting composition
A030:appearance text count composition framing
A031:subject appearance count composition
A032:appearance color composition
A033:appearance style
A034:appearance style composition
A035:setting appearance lighting composition
A036:setting appearance lighting composition
A037:appearance color composition
A038:subject age count pose setting composition relationship
A039:subject age count setting camera composition
A040:appearance text count composition relationship
A041:setting material appearance text count composition relationship
A042:subject appearance text count composition relationship
A043:subject appearance setting text count composition relationship
A044:material appearance text count composition relationship
A045:material appearance text count composition relationship
A046:subject age pose setting appearance text relationship composition
A047:subject age pose material setting relationship composition
A048:subject age appearance text count composition relationship
A049:subject age pose setting material count relationship composition
A050:material appearance text count composition relationship
A051:setting material appearance text count relationship composition
A052:subject age pose setting relationship composition
A053:appearance text count composition relationship
A054:setting material appearance text count relationship composition
A055:setting material appearance text relationship composition
A056:setting material appearance body_geometry relationship composition
A057:subject material appearance body_geometry count relationship composition
A059:subject age count appearance pose relationship composition
A060:subject material appearance body_geometry relationship composition
A062:subject material appearance body_geometry count relationship composition
A063:subject age count pose relationship composition
A064:setting material appearance body_geometry relationship composition
A065:material appearance text relationship composition
A066:setting material appearance text relationship composition
A067:subject age appearance pose setting camera composition relationship
A068:setting material appearance lighting composition
A069:setting appearance text count composition relationship
A070:setting subject appearance text count composition relationship
A071:subject material appearance body_geometry count relationship composition
A072:subject age appearance setting material relationship composition
A073:appearance text count composition relationship
A074:appearance color text count composition relationship
A075:setting material appearance count relationship composition
A077:appearance text count composition relationship
A078:appearance text count composition relationship
'''.strip()
EFFECTS={k:set(v.split()) for k,v in (line.split(':') for line in FOOTPRINTS.splitlines())}
REUSE={'A064':'cand_8ed5a9486be65af9b7a3e3d39ca477fb'}
APP='One optional complete authored realization. Preserve all named components, counts, materials, text carriers, projected boundaries and directed endpoint relations in both languages. Use only when compatible with the independently frozen scene and all affected dimensions. Sibling alternatives are not all required together. Hidden, merged, reversed or cropped required endpoints are unobservable, not passed; partial_is_fail; UNOBSERVABLE_NOT_PASS. The research graph and citations are metadata and grant no typed native fact, owner permission, role approval or native qualification. A still appearance does not establish actual recording provenance, device failure, audio, motion through time, identity, consent, intention, life/death, institutional truth or supernatural effect.'

def main():
 before=read(O/'before.json');old=c.load(A)
 assert c.digest(old)==before['corpus_sha256'],'Concurrent source change: recapture before implementation'
 cards=read(Q/'semantic-cards.json')['cards'];drafts={d['card_id']:d for d in read(Q/'candidate-drafts.json')['drafts']}
 routes=read(Q/'keyword-routes.json')['routes'];src={x['id']:x for x in read(Q/'sources.json')['sources']}
 assert set(drafts)==set(EFFECTS)
 byseed={x['seed_id']:x for x in routes};records={};bindings={};registry=[];decisions=[]
 for card in cards:
  key=card['id'];meta=copy.deepcopy(card)
  if key not in drafts:
   meta.update(candidate_id=None,registration_status='held_for_detail_reference',native_approval=False)
   registry.append(meta);decisions.append({'card_id':key,'decision':'defer','reason':card['draft_hold_reason']});continue
  if key in REUSE:
   cid=REUSE[key];assert cid in old['candidates']
   existing=old['candidates'][cid];rs=existing['content'].get('research_semantics',{})
   assert rs.get('card_id')=='C081' and len(rs.get('relations',[]))==2
   meta.update(candidate_id=cid,registration_status='reused_complete_existing_source',native_approval=False)
   registry.append(meta);decisions.append({'card_id':key,'candidate_id':cid,'decision':'reuse_complete','reason':'Existing wall/membrane/conduit proposition retained verbatim; analog presentation does not create a second biological-architecture source.'});continue
  cid='cand_'+uuid.uuid5(uuid.NAMESPACE_URL,'image-prompt/analog-horror/20261022/'+key).hex
  assert cid not in old['candidates']
  aliases=[card['title_ko']]
  for n in card['seed_ids']:
   aliases += [byseed[n]['en'],byseed[n]['ko']]
  # Generic and invisible umbrella words are retained as context, not indiscriminate discovery cues.
  if key=='A073':aliases=[card['title_ko'],'redaction','정보 가림']
  if key=='A067':aliases=[card['title_ko'],'occluded domestic viewpoint','가림 뒤 관찰 시점']
  meta.update(schema='photo-analog-horror-visual-semantics/v1',candidate_id=cid,registration_status='authored_source_module',
              native_qualification='not_qualified',native_approval=False,runtime_importable=True,
              source_details=[src[x] for x in card['source_ids']],graph_scope='review metadata only; no native owner or causal fact')
  content={'en':card['positive_en'],'ko':card['positive_ko'],'definition':'Optional complete authored visual realization: '+card['positive_en'],
           'aliases':list(dict.fromkeys(aliases)),'application_contract':APP,'research_semantics':meta}
  record={'id':cid,'record_kind':'visual_option','content':content,
          'effects':{'dimensions':sorted(EFFECTS[key]),'properties':[]},
          'conditions':{'requires_adult_context':True} if 'adult' in card['positive_en'] else {},
          'provenance':[{'source':src[x]['url'],'sha256':sha(Q/'semantic-cards.json')} for x in card['source_ids']]}
  records[cid]=record;registry.append(meta)
  for slot in card['proposed_slots']:
   assert slot in old['slot_catalog'];bid='bind_'+uuid.uuid5(uuid.NAMESPACE_URL,cid+'/'+slot).hex
   bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional','semantic_role':old['slot_catalog'][slot]['semantic_role'],'conditions':{'subject_applicability':{}},'weight':2}
  decisions.append({'card_id':key,'candidate_id':cid,'decision':'new_bounded_variant','reason':'Exact bilingual owner/carrier/count/endpoint proposition; retain neighboring existing complete sources. Not an exhaustive novelty or native qualification claim.'})
 groups={}
 for route in routes:
  if route['route'] not in ('visible_or_proxy',):groups.setdefault(route['category'],[]).append(route)
 for group,rows in groups.items():
  cid='cand_'+uuid.uuid5(uuid.NAMESPACE_URL,'image-prompt/analog-horror/20261022/context/'+group).hex
  assert cid not in old['candidates']
  en='Context-only analog-horror distinction group: '+group+'. '+ '; '.join(r['en'] for r in rows)+'. These terms retain distinct contextual, causal, temporal, audio or versioned meanings. An appearance proxy does not establish the complete meaning. No default visual recipe or automatic genre activation.'
  ko='문맥 구분 '+group+'. '+ ' '.join(r['ko']+': '+r['note_ko'] for r in rows)
  records[cid]={'id':cid,'record_kind':'diagnostic','content':{'en':en,'ko':ko,'definition':'Diagnostic context only; excluded from positive material retrieval.','aliases':list(dict.fromkeys(t for r in rows for t in (r['en'],r['ko']))),'application_contract':'Retain explicit distinctions without claiming a still image proves the underlying event, intention, sensory experience or canon.','research_semantics':{'context_group':group,'routes':rows,'native_approval':False}},'conditions':{},'effects':{'dimensions':[],'properties':[]},'provenance':[{'source':'research:analog-horror-20261022/keyword-routes.json','sha256':sha(Q/'keyword-routes.json')}]}
 candidate_name='photo_candidate_analog_horror_20261022.json';binding_name='photo_candidate_analog_horror_bindings_20261022.json'
 oldhash={m['file']:sha(A/m['file']) for m in read(A/c.MANIFEST_NAME)['modules']}
 with source_update(S):
  assert c.digest(c.load(A))==before['corpus_sha256']
  write(A/candidate_name,{'schema':c.MODULE_SCHEMAS['candidates'],'candidates':records})
  write(A/binding_name,{'schema':c.MODULE_SCHEMAS['slot_bindings'],'slot_bindings':bindings})
  manifest=read(A/c.MANIFEST_NAME);manifest['modules'] += [{'file':candidate_name,'kind':'candidates'},{'file':binding_name,'kind':'slot_bindings'}]
  write(A/c.MANIFEST_NAME,manifest)
  write(A/'photo_analog_horror_semantics_20261022.json',{'schema':'photo-analog-horror-semantic-registry/v1','cards':registry,'keyword_routes':routes,'sources':list(src.values()),'research_sha256':sha(Q/'semantic-cards.json'),'native_approval':False})
 after=c.load(A)
 assert all(after['candidates'][cid]==r for cid,r in old['candidates'].items())
 assert all(after['slot_bindings'][bid]==r for bid,r in old['slot_bindings'].items())
 assert all(after[k]==old[k] for k in ['slot_catalog','policies'])
 assert all(sha(A/f)==h for f,h in oldhash.items())
 result={'status':'source_registered','semantic_cards':len(registry),'keyword_routes':len(routes),'new_visual_options':sum(r['record_kind']=='visual_option' for r in records.values()),'reused_visual_sources':len(REUSE),'diagnostics':len(groups),'held_cards':len(cards)-len(drafts),'bindings':len(bindings),'candidate_count_after':len(after['candidates']),'binding_count_after':len(after['slot_bindings']),'cards':registry,'decisions':decisions,'native_approval':False}
 write(O/'new-native-records.json',records);write(O/'changed-native-records.json',{});write(O/'data-integration.json',result)
 write(O/'source-preservation.json',{'status':'pass','preexisting_candidates_preserved':len(old['candidates']),'preexisting_bindings_preserved':len(old['slot_bindings']),'preexisting_modules_byte_identical':oldhash,'catalog_and_policies_preserved':True,'after_corpus_sha256':c.digest(after)})
 print(json.dumps({k:v for k,v in result.items() if k not in ['cards','decisions']},ensure_ascii=False))
if __name__=='__main__':main()
