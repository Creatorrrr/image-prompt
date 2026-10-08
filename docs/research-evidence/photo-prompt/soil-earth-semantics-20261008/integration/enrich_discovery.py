"""Add owned short paraphrases only to optional component discovery."""
from pathlib import Path
import hashlib,json,sys
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[4]
SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
from photo_runtime_sources import source_update
from visual_profile_contracts import validate_visual_profile_source,compile_visual_profile

ROWS='''
e002|coarse sand grains/모래알|shadows between grains/알갱이 사이 그림자|granular sand bed/모래 바탕
e004|rounded pebbles/둥근 자갈|pebble edges/자갈 가장자리|fine sediment matrix/고운 기질
e005|crumb aggregates/부스러기형 입단|aggregate boundaries/입단 경계|interaggregate pores/입단 사이 틈
e007|dry soil surface/마른 흙 표면|dust plume at contact/접촉점의 먼지|wheel touching ground/지면에 닿는 바퀴
e008|cohesive mud bed/진흙 바닥|turbid standing water/고인 흙탕물|mud water boundary/진흙과 물의 경계
e009|damp soil patch/촉촉한 흙|local water film/국소 수막|moisture boundary/수분 경계
e010|boot pressing into mud/진흙을 누르는 부츠|tread depression/밑창 압흔|raised mud ridge/밀려 올라온 진흙
e011|parallel wheel ruts/나란한 차륜 홈|soil ridges beside ruts/홈 옆 흙 능선|aligned tread marks/나란한 타이어 자국
e014|fingertips pressing clay/점토를 누르는 손가락|retained finger grooves/남은 손가락 홈|folded clay edge/접힌 점토 가장자리
e016|vertical soil exposure/수직 흙 단면|soil band boundaries/흙층 경계|continuous cut face/연속 절개면
e017|leaf litter/낙엽 조각|dark topsoil layer/어두운 표토|roots crossing litter/낙엽을 가로지르는 뿌리
e019|weathered rock fragments/풍화 암편|continuous bedrock/연속 기반암|soil rock contact/흙과 암반 경계
e025|plant fibres in peat/이탄의 식물 섬유|compressed organic layers/눌린 유기층|wet cut edge/젖은 절단면
e028|crystalline soil crust/결정 피막|soil beneath crust/피막 아래 흙|raised crystal grains/도톰한 결정
e036|shallow erosion channels/얕은 침식 홈|downhill branching grooves/내리막 분기 홈|sediment below channel/물길 아래 퇴적물
e038|undercut riverbank/파인 하안|exposed bank roots/노출된 하안 뿌리|fallen soil clods/떨어진 흙덩이
e050|alluvial fan deposit/선상 퇴적체|mountain channel outlet/산지 물길 출구|receiving plain/퇴적체를 받는 평원
e057|wet sediment flat/젖은 퇴적 평면|branching drainage grooves/분기 배수 홈|receding waterline/물러난 수면
e059|crescent dune ridge/초승달 사구|steep dune face/급한 사구 면|gentle dune slope/완만한 사구 면
e060|sand ripple ridges/모래 사련 능선|sandy troughs/모래 골|continuous sand patch/연속 모래 바탕
e064|cave entrance/동굴 입구|bedrock passage walls/암반 통로벽|continuous entrance floor/이어진 입구 바닥
e065|ceiling stalactite/천장 종유석|floor stalagmite/바닥 석순|continuous cave column/이어진 동굴 기둥
e070|folded rock layers/휘어진 암석층|shared fold hinge/함께 휜 중심|coherent rock face/연속 암면
e077|segmented earthworm/마디 지렁이|burrow opening/굴 입구|coiled soil casts/구불구불한 분변토
e080|partly decomposed leaves/분해 중 낙엽|broken organic fragments/부서진 유기물|common forest floor/같은 숲바닥
e081|branching exposed roots/노출된 가지 뿌리|soil around roots/뿌리 주위 흙|plant connected to roots/뿌리와 연결된 식물
e083|crop residue cover/작물 잔재 피복|seedlings through residues/잔재 사이의 싹|uncovered soil patches/드러난 흙 부분
e086|unfired earthen blocks/흙벽돌|earthen mortar joints/흙 줄눈|broken fibrous block/섬유가 보이는 벽돌 파단
e087|continuous cob wall/연속 콥 벽|fibres at damaged edge/손상부의 섬유|continuous earthen material/이어진 흙 재료
e088|horizontal rammed earth lifts/수평 판축층|formwork impressions/거푸집 자국|continuous compacted wall/연속 다짐 벽
e089|woven rods/엮은 나뭇가지|daub adhering to rods/나뭇가지에 붙은 흙|bounding timber frame/둘러싼 목재 틀
e091|open excavation trench/열린 굴착 도랑|adjoining spoil pile/옆의 파낸 흙더미|continuous trench cut/연속 도랑 절개면
e093|hands shaping clay/점토를 빚는 손|clay vessel on wheel/물레 위 점토 그릇|clay slurry on fingers/손가락의 점토액
e094|clay coil junction/점토 코일 접합|lower vessel coils/그릇 아래 코일|finger smoothing junction/접합부를 다듬는 손가락
e096|unglazed terracotta foot/유약 없는 적색 굽|glaze ending above foot/굽 위에서 끝나는 유약|glaze body boundary/유약과 몸체 경계
e097|earth pigment powder/흙 안료 분말|bound paint swatch/바인더 색 견본|separate binder container/별도 바인더 용기
e099|stratified excavation face/층진 발굴면|embedded pottery fragment/박힌 도자기 조각|scale at layer contact/층 경계의 눈금
e100|rounded earth mound/둥근 흙 봉분|mound base boundary/봉분 바닥 경계|adjoining surrounding ground/이어진 주변 지면
e107|earthen golem body/흙 골렘 몸체|articulated earthen joints/이어진 흙 관절|crumbs at acting hand/작용하는 손의 흙 부스러기
e108|floating layered earth/떠 있는 지층|hanging exposed roots/매달린 노출 뿌리|continuous air gap/연속 공기 틈
e109|skin beside mud/진흙 옆 피부|thick adhering mud/두께 있는 부착 진흙|fingertip track at edge/경계의 손가락 자국
e110|garment seams and folds/의복 봉제선과 주름|mud clumps at hem/밑단의 진흙덩이|mud clean fabric boundary/진흙과 깨끗한 천 경계
e115|granular regolith surface/입자성 레골리스|sharp tread impression/선명한 밑창 자국|angular rock fragments/각진 암편
'''

def main():
 path=SKILL/'assets/photo_prompt_visual_obligations_soil_earth.json'
 data=json.loads(path.read_text()); before=hashlib.sha256(path.read_bytes()).hexdigest()
 profiles={p['id']:p for p in data['profiles']}; changed=[]
 for line in ROWS.strip().splitlines():
  key,*groups=line.split('|'); p=profiles['soil_rel_'+key]
  for component,terms in zip(p['authored_components']['components'],groups):
   for term in terms.split('/'):
    if term not in component['match_terms']: component['match_terms'].append(term)
  validate_visual_profile_source(p); changed.append(p['id'])
 for p in data['profiles']:
  exact={term.casefold() for term in p['activation']['exact_terms']}
  p['semantics']['paraphrase_examples']=[s for s in p['semantics']['paraphrase_examples'] if s.casefold() not in exact]
  old=p['authored_components']
  if old['contract_version']!='photo-authored-visual-components/v1': continue
  compiled=compile_visual_profile(p)
  components=old['components']
  p['authored_components']={
   'contract_version':'photo-authored-visual-components/v2',
   'components':[{'id':c['id'],'match_terms':c['match_terms']} for c in components],
   'discovery':{'minimum_component_groups':2,'required_group_ids':[components[0]['id']]},
   'obligations':[{'component_ids':[c['id'] for c in components],
    'evidence':[{'field':c['evidence_field'],'requirement':{'min_content_words':c['min_content_words'],'must_mention_any':c['evidence_terms']}} for c in components],
    'instruction':' '.join(c['instruction'] for c in components),
    'render_gates':[c['render_gate'] for c in components]}]}
  validate_visual_profile_source(p)
  after=compile_visual_profile(p)
  for field in ['required_evidence_fields','evidence_requirements','render_gates','composition_instruction']:
   assert compiled[field]==after[field],(p['id'],field)
 with source_update(SKILL):
  if hashlib.sha256(path.read_bytes()).hexdigest()!=before: raise RuntimeError('owned profile source changed during authoring')
  path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 (OUT/'optional-discovery-enrichment.json').write_text(json.dumps({'before_sha256':before,'after_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'profile_ids':changed,'collective_obligations':len(data['profiles']),'authority':'Optional discovery uses two groups including the principal material form; complete exact proposition and all opt-in evidence, instructions and gates are unchanged.'},ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'optional_component_lexicons_enriched':len(changed)},ensure_ascii=False))

if __name__=='__main__': main()
