"""Correct physical effect ownership and broaden component vocabulary, never hard terms."""
import json
from pathlib import Path
import sys

EVIDENCE=Path(__file__).resolve().parent
ROOT=EVIDENCE.parents[3]
SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
from photo_runtime_sources import source_update

# General relation phrases: no test-scene locations, wardrobe, props, or quoted
# baseline sentences. These propose meanings; complete adoption proofs/gates
# remain canonical and unmodified.
ALIASES={
 'folk_horror_collective_boundary':[
  ['inward-facing community','community enclosure','human boundary','community closes','residents face inward','공동체 경계'],
  ['visitor outside the gathering','excluded visitor','outside the circle','isolated visitor','traveler','방문자의 고립'],
  ['landscape isolation','only open route','sole exit','alternative routes blocked','single escape route','대체 경로의 차단']],
 'bodily_fusion_shared_junction':[
  ['tissue-metal junction','skin meets metal','organic-to-mechanical','organic mechanical junction','피부와 금속의 접합'],
  ['continuous transition','unbroken tissue-metal continuity','both structures stay connected','continuous anatomical junction','연속된 접합부']],
 'body_horror_uncontrolled_change':[
  ['same body normal and altered','localized bodily transformation','normal and transformed body regions','한 몸의 정상부와 변형부'],
  ['continuous body transition','connected transformation band','visible anatomical transition','보이는 연속 변형']],
 'metamorphosis_transition_band':[
  ['normal to altered bodily structure','linked normal and transformed regions','같은 몸의 변화'],
  ['continuous transition band','unbroken anatomical transition','연속된 전이 구간']],
 'uncanny_familiar_discrepancy':[
  ['same clothing in the mirror','matching reflected wardrobe','aligned ordinary reflection','coherent mirror counterpart','일치하는 인물 반사'],
  ['reflected hand differs','different mirror gesture','mirror hand mismatch','반사 속 다른 손동작'],
  ['coherent mirror geometry','matching room geometry','otherwise consistent reflection','일관된 주변 반사']],
 'reflection_pose_disagreement':[
  ['matching reflected wardrobe','same person in aligned mirror','aligned reflection counterpart','일치하는 인물 반사'],
  ['actual neutral mouth','real mouth stays neutral','neutral unreflected mouth','실제 입은 무표정'],
  ['only reflection smiles','reflected mouth smiling','mirror smile disagreement','거울 속 입만 미소']],
 'shadow_independent_pose':[
  ['actual hands lowered','both hands down','real arms lowered','실제 양손은 아래'],
  ['shadow raises one hand','raised shadow hand','cast shadow lifts an arm','그림자만 손을 듦'],
  ['single light source','consistent shadow direction','readable shadow source','명확한 단일 광원']],
 'recording_local_discrepancy':[
  ['physical room beside its display','room and CCTV comparison','same room landmarks on screen','실제 공간과 대응 화면'],
  ['additional person only on screen','recording-only presence','extra figure on display','화면에만 추가 인물']],
 'psychological_record_conflict':[
  ['person beside live monitor','subject beside corresponding display','인물과 대응 모니터'],
  ['different recorded gesture','local gesture mismatch','화면 속 다른 동작'],
  ['shared room landmarks','matching room landmarks','같은 공간의 대응 지표']],
 'doppelganger_pair_divergence':[
  ['two matching people','two separate identical figures','matching face and clothing pair','같은 외관의 두 인물'],
  ['different hand gestures','divergent hand actions','서로 다른 손동작'],
  ['separate physical positions','two distinct bodies','서로 다른 실제 위치']],
 'daylight_exposed_threat':[
  ['bright even daylight','fully exposed daylight setting','밝고 균일한 낮빛'],
  ['clearly visible bounded anomaly','unhidden local threat','선명한 국소 이상'],
  ['ordinary bystander tasks','bystanders continue routine','일상 자세를 유지하는 주변인']],
 'safe_boundary_failure':[
  ['mostly intact protective barrier','recognizable protection boundary','대부분 온전한 보호 경계'],
  ['localized protective breach','breach joins protected and threatened zones','보호 구역의 국소 파손']],
 'eerie_expected_absence':[
  ['ready operational equipment','working service area','준비된 서비스 공간'],
  ['expected users absent','vacant active area','예상 이용자의 부재'],
  ['fresh use trace','recent trace in empty room','비어 있는 곳의 새 사용 흔적']],
 'dramatic_irony_unseen_back':[
  ['background presence behind person','threat behind the observer','인물 뒤의 존재'],
  ['gaze directed elsewhere','person looks away','다른 곳을 보는 시선'],
  ['both visible in one frame','same frame foreground and background','한 화면의 두 대상']],
 'tsukumogami_tool_agency':[
  ['worn household tool body','recognizable old tool','낡은 도구 본체'],
  ['eye or limb on the tool','animate tool appendage','도구에서 연결된 눈이나 팔다리'],
  ['original tool function readable','tool structure remains legible','원래 도구 구조의 가독성']],
}

def read(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

cpath=SKILL/'assets/photo_prompt_horror_extension.json'
ppath=SKILL/'assets/photo_prompt_visual_obligations_horror.json'
candidate,profile=read(cpath),read(ppath)
change_log=[]
before={str(p):__import__('hashlib').sha256(p.read_bytes()).hexdigest() for p in [cpath,ppath]}
for slot,rows in candidate['slots'].items():
 for entry in rows:
  slug=entry['id'][3:]
  old=json.loads(json.dumps(entry['affected_properties']))
  effects=[]
  for effect in entry['affected_properties']:
   effect=dict(effect)
   if effect['dimension']=='subject' and effect['property']=='props':
    effect={'dimension':'setting','target':'*','property':'objects'}
   elif effect['dimension']=='subject' and effect['property']=='secondary_people':
    effect={'dimension':'count','target':'scene','property':'people'}
   elif effect['dimension']=='subject' and effect['property']=='recorded_presence':
    effect={'dimension':'count','target':'recorded_scene','property':'entities'}
   elif effect['dimension']=='subject' and effect['property']=='reflected_presence':
    effect={'dimension':'count','target':'mirror_frame','property':'entities'}
   elif effect['dimension']=='subject' and effect['property'] in {'background_presence','apparition'}:
    effect={'dimension':'count','target':'scene','property':'entities'}
   elif slug=='bodily_fusion_shared_junction' and effect['dimension']=='subject' and effect['property']=='hardware':
    # The primary subject remains the same body. The added carrier is part of
    # the declared anatomy/material junction, already covered by those scopes.
    continue
   if effect not in effects:effects.append(effect)
  entry['affected_properties']=effects
  entry['affected_dimensions']=list(dict.fromkeys(e['dimension'] for e in effects))
  if slug in ALIASES:
   alternatives=[a for group in ALIASES[slug] for a in group]
   entry['aliases']=list(dict.fromkeys(entry['aliases']+alternatives))
   entry['paraphrases']=list(dict.fromkeys(entry['paraphrases']+alternatives))
  if old!=effects or slug in ALIASES:
   change_log.append({'candidate_id':entry['id'],'before_effects':old,'after_effects':effects,'alternative_components':ALIASES.get(slug,[])})

by_id={e['id']:(s,e) for s,rows in candidate['slots'].items() for e in rows}
for p in profile['profiles']:
 slug=p['id'][12:]
 e=by_id['hr_'+slug][1]
 p['concept_candidate']['affected_dimensions']=e['affected_dimensions']
 p['concept_candidate']['affected_properties']=e['affected_properties']
 if slug in ALIASES:
  groups=p['authored_components']['components']
  if len(groups)!=len(ALIASES[slug]):raise ValueError('Component arity changed: '+slug)
  for group,aliases in zip(groups,ALIASES[slug]):
   group['match_terms']=list(dict.fromkeys(group['match_terms']+aliases))

with source_update(SKILL,EVIDENCE/'runtime-store'):
 save(cpath,candidate);save(ppath,profile)
 d=read(EVIDENCE/'ADOPTION-MAP.json')
 for row in d['adopted']:row['effects']=by_id[row['candidate_id']][1]['affected_properties']
 save(EVIDENCE/'ADOPTION-MAP.json',d)
save(EVIDENCE/'ADMISSION-REVISION.json',{'reason':'Initial blind retrieval found overbroad primary-subject effects and single-expression component vocabularies. Correct concrete owner scopes and add general relational alternatives; preserve original misses.','before_hashes':before,'changed':change_log,'unchanged':['request envelopes','all three frozen cores','baseline prompts','creative controls','exact hard terms','full adoption evidence requirements','all native gates','retrieval algorithm'],'holdout_boundary':'Initial three scenes were independent before data access. Replays after this repair are development verification, not a fresh held-out sample.'})
print(json.dumps({'changed_entries':len(change_log),'profiles_with_alternative_components':len(ALIASES)}))
