"""Register complete reviewed Lovecraftian research realizations, preserving unrelated data."""
import copy,hashlib,json,sys,uuid
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parents[2];S=R/'skills/photo-prompt-image-generator';A=S/'assets'
Q=R/'docs/research-evidence/photo-prompt/lovecraftian-horror-20261022'
sys.path.insert(0,str(S/'scripts'))
import photo_candidate_corpus as c
from photo_runtime_sources import source_update
read=lambda p:json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

# Full-proposition footprints reviewed from both authored languages, not inferred
# from slot membership or the copied research owner graph.
FOOTPRINTS='''
R01:subject age count pose setting material composition relationship
R02:subject count expression pose setting relationship body_geometry composition
R03:setting material appearance composition relationship count
R04:setting material appearance color count relationship composition
R05:setting material appearance count composition relationship body_geometry
R06:setting material appearance body_geometry count relationship composition
R07:setting material appearance text count relationship composition
R08:setting material appearance body_geometry count pose relationship composition
R09:setting material text count relationship composition
R10:setting material text count relationship composition appearance
R11:setting material appearance count relationship composition
R12:setting material appearance count relationship composition
R13:setting material lighting color appearance composition relationship
R14:setting lighting color appearance count composition relationship
R15:subject age pose setting material relationship composition
R16:setting material appearance relationship composition
R17:setting material lighting appearance count composition relationship
R18:setting material appearance count relationship composition
R19:setting material appearance body_geometry count relationship composition
R20:setting material appearance lighting count relationship composition
R21:subject setting material appearance body_geometry relationship composition
R22:subject setting material appearance body_geometry count pose relationship composition
R23:setting material appearance body_geometry count relationship composition
R24:subject body_geometry material appearance count relationship composition
R25:subject body_geometry appearance count relationship composition
R26:subject material appearance body_geometry count relationship setting composition
R27:subject material appearance body_geometry count relationship composition
R28:subject material appearance color body_geometry count relationship
R29:subject material appearance body_geometry count relationship composition
R30:subject material appearance body_geometry count relationship lighting composition
R31:subject age count pose action setting material relationship composition
R32:subject material appearance body_geometry setting relationship composition
R33:setting material appearance body_geometry count relationship composition
R34:subject material appearance body_geometry relationship composition
R35:subject body_geometry count pose relationship composition
R36:subject material appearance body_geometry count relationship setting lighting composition
R37:subject age appearance body_geometry material relationship
R38:subject age count pose action setting relationship composition
R39:setting material appearance count relationship composition
R40:setting material appearance body_geometry count relationship composition
R41:subject age pose appearance setting material relationship composition
R42:subject age pose appearance body_geometry setting material relationship composition
R43:subject pose action setting material appearance body_geometry relationship composition
R44:setting material appearance body_geometry relationship composition
R45:subject material appearance color body_geometry setting relationship composition
R46:setting material appearance text count relationship composition
R47:setting material appearance text count relationship composition
R48:setting material appearance color body_geometry count relationship composition
R49:setting material appearance text count relationship composition
R50:setting material appearance color relationship composition
R51:setting material appearance color relationship composition
R52:subject age count pose setting appearance relationship composition
R53:subject age count pose action expression setting appearance relationship composition
R54:subject age count pose setting material appearance relationship composition
R55:subject age count pose appearance setting material relationship composition sexual_tone
R56:setting material appearance lighting text count relationship composition
R57:subject count pose setting material appearance body_geometry relationship composition
'''.strip()
EFFECTS={k:set(v.split()) for k,v in (line.split(':') for line in FOOTPRINTS.splitlines())}
CONTEXT_EN=[
'Lovecraftian horror and cosmic horror are expressive modes; cosmicism is a perspective and the Cthulhu Mythos a shared fictional network. Nihilism and anti-anthropocentrism are separate interpretive axes. A broad label never requires tentacles, green, space, violence, or a particular creature.',
'The unknown, the unknowable, dangerous knowledge and failed naming retain distinct epistemic meanings. Partial concealment or limited disclosure is an optional staging and cannot prove intrinsic unknowability.',
'Obsession, missing memory, mind exchange, identity dissolution and literary madness need their declared narrative evidence. Appearance, ethnicity, disability, eye shape or expression does not establish mental health, cognition, memory or the owner of consciousness.',
'Epistolary form, frame narrative, delayed disclosure, negative description, limited narration and survival without restoration concern presentation of information. Physical frames or documents do not prove narrative order, truth, narrator reliability or audience discovery in a single still.',
'Deep time, prehuman civilization, posthuman futures, cosmic cycles and astronomical return conditions retain distinct durations, histories and causal claims. Layers, ruins and charts can be visible proxies but do not establish their age or efficacy.',
'Mathematical non-Euclidean geometry, higher-dimensional fiction, perceptual disturbance, impossible objects and lens perspective are distinct. Spherical or hyperbolic geometry is not logical contradiction, and a label does not prescribe a staircase or portal.',
'Arkham, Miskatonic, Innsmouth, Dunwich, Kingsport, Rlyeh, Dreamlands, Leng and Yuggoth retain work-specific geography. A name alone does not prescribe architecture, population, ethnicity, class, morality or exact coordinates; ambiguous places are not one fixed map.',
'Great Old Ones, Outer Gods, Elder Gods, Other Gods and the biological Elder Things belong to different textual and authorial layers. Preserve the chosen original work or later game version rather than retroactively unifying every Old One classification.',
'Azathoth and Yog-Sothoth retain their work-specific names, poetic images and threshold relations without one canonical anatomy, orb count or dream-universe equation. The original text does not establish that Azathoth waking destroys the entire universe; further version-specific evidence is required.',
'Shub-Niggurath, Father Dagon and Mother Hydra retain names, titles and cult relations separately from an encountered body. A black goat or the Greek multi-headed hydra is not automatically their original canonical anatomy; unresolved designs remain deferred.',
'Nodens, Tsathoggua, Hastur and the King in Yellow retain distinct author, work and later-version provenance. Smith and Bierce originals were not fully checked in this research; the King equals Hastur and universal deity anatomy remain unverified.',
'The Necronomicon has invented bibliographical history, distinct from actual occult publications. Book of Eibon, De Vermis Mysteriis, Unaussprechlichen Kulten and Pnakotic Manuscripts require separate first-author, work and version checks; they are not aliases of one book or one fixed cover.',
'Aklo references, visible marks, pronounceable words and alleged perceptual or magical effects are separate claims. Random runes are not verified Aklo, the Yellow Sign is not the Elder Sign, and a copied design does not prove comprehension or summoning.',
'Cult membership, the Order of Dagon, Starry Wisdom, invocation, summoning, chanting, sacrificial bargains and apocalypse retain separate roles and causes. Robes, a circle or religious clothing do not establish affiliation, evil, consent or efficacy, and real ethnic or religious appearance is not proof.',
'Body horror, abjection, metamorphosis, atavism, degeneration, engineered life, reanimation, necromancy and decay retain different forms, histories and causes. A mixed body does not establish inferiority, disease, malice, genetics, life or death; original racist or eugenic assumptions are not neutral appearance categories.',
'Cannibalism, necrophagy, human livestock, dissection, grave robbing and corpse desecration retain different targets, actions, permissions and histories. Bones, fangs, a ghoul or a specimen do not establish species, feeding, death, coercion or ownership.',
'Reproductive horror, interspecies reproduction, hybridity, reproductive coercion, incest, inbreeding and monstrous birth are distinct. Appearance cannot establish sexual acts, kinship, consent, perpetrators or ancestry; the unspecified circumstances of Lavinias pregnancy are not asserted facts.',
'Necrophilia, sexual violence, erotic horror, tentacle erotica and Cthulhurotica retain literary or later-genre context. Tentacles do not imply sex, nudity does not imply non-consent, and proximity to a corpse does not establish necrophilia. No sexual violence or sexual act with a corpse is authored as a visual option here.',
'The monstrous-feminine and queer or feminist rewritings are critical perspectives, not claims that women, motherhood or hybridity are inherently monstrous. Creed, Project LC.RC research and modern novels require further primary reading before theory-specific canonical visual approval.',
'Eldritch, ineffable, unspeakable, unnamable, primordial, antediluvian, chthonic, Stygian, tenebrous and blasphemous concern language and interpretation. They do not fix anatomy, green, morality or an actual geological period; not every dictionary sense was independently checked.',
'Fetid and mephitic concern smell or atmosphere; gibbering and ululation concern sound. Charnel and sepulchral have spatial and metaphorical uses. Fog, green gas or an open mouth cannot prove odor, toxicity, an actual sound or emotional and religious intent in a still.',
'Protean forms, metamorphosis, reanimation and disintegration can concern change through time. One mixed boundary, blurred body, resting figure or gel does not prove transformation, resurrection or living protoplasm; temporal claims need separate sequence evidence.',
'SAN and sanity loss are game mechanics, not mental-health diagnoses or facial traits. A legible game display or document can depict a stated number; appearance cannot establish actual resilience, illness or psychological change.',
'SCP cognitohazards and infohazards are later community terms, distinct from original forbidden knowledge. Seeing a pattern, reading a book and an apparent reaction do not prove supernatural danger or propagation; do not ascribe real hazardous efficacy to the image.',
'Ecohorror, posthuman horror, New Weird, pastiche, critical rewriting and symbiosis are independent interpretive axes. A caring or interdependent encounter is an authored alternative rather than proof of biological mutual benefit or a particular modern novel; aliens are not automatically hostile.',
'Flying polyps and ghouls retain different textual sensory, material and feeding relations. Their entire original descriptions were not rigorously compared here; ghosts are not automatically polyps, bones do not establish feeding, and full canonical designs remain deferred.',
'Batrachian, ichthyoid and fungoid can express resemblance rather than biological classification. Amorphous, gelatinous and protoplasmic have distinct form, texture and scientific senses; a frog-like form, gel or filament does not establish a real species, cell composition, toxicity or life.'
]
KO_UPDATES={
'C126':'니알라토텝의 한 선택형 실현: 인간형 시연자 한 명, 눈에 보이는 투사 장치, 시연을 바라보는 작은 관중들이 서로 분리된다. 시연자는 장치 옆에 서고 관중은 시연자를 향한다.',
'C119':'크툴루의 한 선택형 실현: 촉수성 문어 유사 머리, 비늘로 덮인 대체로 인간형인 몸, 몸 뒤에 부착된 길고 좁은 날개가 구분된다. 머리는 몸에 연결되고 날개는 그 몸에 붙는다.',
'C120':'엘더 싱의 한 선택형 실현: 다섯 세로 능선이 있는 통 모양 몸통, 위쪽의 다섯 꼭짓점 기관, 몸통 둘레에 부착된 분기 부속지 계통이 구분된다. 상부 기관은 몸통과 연결되고 부속지는 몸통 주위에 배열된다.',
'C169':'뇌 원통의 한 선택형 실현: 불투명 금속 원통, 이등변삼각형 배열의 오목한 소켓 세 개, 그중 두 소켓에 꽂힌 케이블 두 개, 대응하는 케이블 말단이 있는 가까운 장치 두 개가 보인다. 소켓은 원통에 박혀 있고 케이블은 소켓과 장치에 각각 연결된다.',
'C173':'의례적 나체·제물 신부·입문자·도취적 숭배의 한 선택형 배치: 명시된 성인 참가자 한 명, 공동 중심을 향하는 별도의 성인 집단, 참가자와 집단 사이 읽을 수 있는 간격이 구분된다. 참가자는 집단을 향하고 간격은 참가자와 집단 사이에 놓인다.',
'C174':'기억 덮어쓰기·파편 단서·기록 모순의 한 선택형 실현: 크게 만든 가상의 원 세 개 식별자가 있는 경계 명확한 기록 한 장과 같은 식별자를 가진 별도 기록 한 장이 있다. 대응 위치의 국소 도식은 분명하게 다르다. 두 기록을 표식으로 대응시키고 같은 위치의 도식을 두 기록 사이에서 비교한다.'}

def main():
 before=read(O/'before.json');original=c.load(A);assert c.digest(original)==before['corpus_sha256'],'Concurrent source drift before adoption'
 cards=read(Q/'semantic-cards.json');routes=read(Q/'keyword-routes.json');sources={s['source_id']:s for s in read(Q/'sources.json')};seed={x['seed_id']:x for x in routes}
 visual={x['card_id'] for x in cards if x.get('candidate_eligible')};assert visual==EFFECTS.keys()
 records={};bindings={};registry=[];decisions=[];contextn=0
 app='One complete optional authored visual realization. Preserve every English and Korean material, count, part, state, owner and directed relationship together, including each actual connection endpoint and comparison witness. Apply only when compatible with independently frozen requester meaning and every affected dimension/property. Sibling alternatives never become all-of requirements. Hidden or cropped required parts are unobservable, not passed; partial evidence fails the whole case. Research graphs and citations are review metadata and create no typed native facts, guard support, owner permission or native qualification. Visible form does not establish identity, consciousness, consent, kinship, mental health, historical age, sound, smell, causation or supernatural efficacy.'
 for card in cards:
  key=card['card_id'];isvisual=key in visual;cid='cand_'+uuid.uuid5(uuid.NAMESPACE_URL,'image-prompt/lovecraftian-horror/20261022/'+key).hex;assert cid not in original['candidates']
  en=card['proposal_en'] if isvisual else CONTEXT_EN[contextn];ko=card['proposal_ko'] if isvisual else card['meaning_ko']+' '+card['claim_limit_ko'];contextn+=not isvisual
  aliases=[card['title_ko']]
  for sid in card['seed_refs']:
   aliases.extend(seed[sid]['original_term'].split(' — '))
  meta={**copy.deepcopy(card),'schema':'photo-lovecraftian-horror-visual-semantics/v1','candidate_id':cid,'registration_status':'authored_source_module' if isvisual else 'authored_diagnostic_module','native_qualification':'not_qualified','graph_scope':'Research-only visible relations; not typed facts or selected-owner permissions.','source_details':[sources[x] for x in card['source_refs']]}
  rec={'id':cid,'record_kind':'visual_option' if isvisual else 'diagnostic','content':{'en':en,'ko':ko,'definition':('Optional complete authored visual realization: '+en) if isvisual else 'Context-only distinction excluded from positive material retrieval.','aliases':list(dict.fromkeys(aliases)),'application_contract':app if isvisual else 'Diagnostic context only. Retain distinctions and deferred claims without creating a positive still-image appearance recipe, native approval or requester lock.','research_semantics':meta},'conditions':({'requires_adult_context':True} if isvisual and 'adult' in en.lower() else {}),'effects':{'dimensions':sorted(EFFECTS[key]) if isvisual else [],'properties':[]},'provenance':[{'source':sources[s]['url'],'sha256':sha(Q/'semantic-cards.json')} for s in card['source_refs']]}
  meta['provenance_digest_scope']='research specification bytes; source_details separately retain actually fetched body hashes where available'
  records[cid]=rec;registry.append(meta)
  for slot in card['proposed_slots'] if isvisual else []:
   assert slot in original['slot_catalog'];bid='bind_'+uuid.uuid5(uuid.NAMESPACE_URL,cid+'/'+slot).hex
   bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional','semantic_role':original['slot_catalog'][slot]['semantic_role'],'conditions':{'subject_applicability':{}},'weight':2}
  decisions.append({'card_id':key,'candidate_id':cid,'research_proposal':card['adoption'],'actual_decision':'complete_bounded_optional_variant' if isvisual else 'diagnostic_context','reason':'Research phrases introduce exact framing, age, count, endpoints or material scope beyond the nearby old source. Preserve old complete sources and add the exact bilingual proposition; no exhaustive novelty or same-contract reuse claim.' if isvisual else 'Invisible or unresolved meaning remains outside positive appearance retrieval.','native_approval':False})
 assert len(records)==84 and contextn==27
 mod='photo_candidate_cosmic_horror_20261021.json';legacy=read(A/mod);changed={}
 sem=read(A/'photo_cosmic_horror_semantics_20261021.json');semby={x['id']:x for x in sem['cards']}
 for cid,rec in legacy['candidates'].items():
  key=rec['content'].get('research_semantics',{}).get('card_id')
  if key not in KO_UPDATES:continue
  new=copy.deepcopy(rec);new['content']['ko']=KO_UPDATES[key]
  if key in ('C173','C174'):
   old='boundary between adult.' if key=='C173' else 'local_field differs between document_a.'
   replacement='boundary lies between adult and group.' if key=='C173' else 'local_field differs between document_a and document_b.'
   for field in ('en','definition'):
    assert old in new['content'][field];new['content'][field]=new['content'][field].replace(old,replacement)
   relations=new['content']['research_semantics']['relations'];relations[-1]['predicate']='separates_from' if key=='C173' else 'compared_in'
   relations.append({'id':'r3','subject':'boundary' if key=='C173' else 'local_field','predicate':'separates_from' if key=='C173' else 'compared_in','object':'group' if key=='C173' else 'document_b'})
   semby[key]['relations']=copy.deepcopy(relations)
  changed[cid]=new;legacy['candidates'][cid]=new
 assert len(changed)==6
 candidate_module='photo_candidate_lovecraftian_horror_20261022.json';binding_module='photo_candidate_lovecraftian_horror_bindings_20261022.json';manifest=read(A/c.MANIFEST_NAME)
 for name,kind in [(candidate_module,'candidates'),(binding_module,'slot_bindings')]:manifest['modules'].append({'file':name,'kind':kind})
 proposed=copy.deepcopy(original);proposed['candidates'].update(records);proposed['candidates'].update(changed);proposed['slot_bindings'].update(bindings);c.validate(proposed)
 with source_update(S):
  assert c.digest(c.load(A))==before['corpus_sha256']
  write(A/candidate_module,{'schema':c.MODULE_SCHEMAS['candidates'],'candidates':records});write(A/binding_module,{'schema':c.MODULE_SCHEMAS['slot_bindings'],'slot_bindings':bindings});write(A/mod,legacy);write(A/'photo_cosmic_horror_semantics_20261021.json',sem);write(A/c.MANIFEST_NAME,manifest)
  now=c.load(A);assert now==proposed
 write(O/'new-native-records.json',records);write(O/'changed-native-records.json',changed)
 lookup={x['card_id']:x['candidate_id'] for x in registry}
 result={'schema':'photo-lovecraftian-horror-semantic-registry/v1','cards':registry,'keyword_routes':[{**r,'candidate_ids':[lookup[x] for x in r['card_refs']],'activation':'advisory; no automatic hard obligations'} for r in routes],'decisions':decisions,'counts':{'semantic_cards':84,'new_visual_options':57,'new_diagnostics':27,'updated_existing_bilingual_sources':6,'new_bindings':len(bindings),'keyword_routes':185},'native_approval':False}
 write(A/'photo_lovecraftian_horror_semantics_20261022.json',result);write(O/'data-integration.json',result)
 preserved=[cid for cid in original['candidates'] if cid not in changed];assert all(now['candidates'][cid]==original['candidates'][cid] for cid in preserved)
 assert all(now[k]==original[k] for k in ('slot_catalog','policies')) and all(now['slot_bindings'][k]==v for k,v in original['slot_bindings'].items())
 write(O/'source-preservation.json',{'status':'pass','old_CIDs_preserved_exactly':len(preserved),'reviewed_existing_CIDs_changed':list(changed),'old_bindings_preserved':len(original['slot_bindings']),'old_guards_effects_provenance_preserved':all(all(original['candidates'][cid][k]==rec[k] for k in ('conditions','effects','provenance')) for cid,rec in changed.items()),'counts':result['counts'],'after_corpus_sha256':c.digest(now)})
 print(json.dumps(result['counts']))
if __name__=='__main__':main()
