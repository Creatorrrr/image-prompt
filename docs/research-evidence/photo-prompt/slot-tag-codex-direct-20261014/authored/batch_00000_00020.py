"""Individually authored after reading all twenty complete source records.

This file encodes decisions, not a classifier. Tuple roles, properties, quotes,
rejections and meanings below were chosen by Codex for each named packet row.
The writer only expands that explicit judgement into the review wire format.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
packet = json.loads((RUN / 'packets/00000-020.json').read_text())
catalog = json.loads((RUN / 'CATALOG.json').read_text())

# ordinal, explicit status, meaning, explicit role/fact tuples, rejected boundary
# Role tuple: role, dimension, owner, property, exact English quote, rationale.
DECISIONS = [
 (0, 'approved', '네온 조명을 지칭한다. 색·방향·밝기나 간판 글자는 정해져 있지 않다.', [
  ('light_type','lighting','illuminating_light','lighting.source.neon','neon',
   '조명 맥락의 네온 광원 명칭이다.')],
  '네온이라는 명칭만으로 분홍색·문자 간판·도시 배경을 만들지 않는다.'),
 (1, 'approved', 'LED 광원을 지칭하는 짧은 조명 후보다. lab은 특정 파장·장치 형상·조도를 확정하지 않는다.', [
  ('light_type','lighting','illuminating_light','lighting.source.led','led',
   '본문의 LED 명칭이 광원의 종류를 직접 제공한다.')],
  'lab이라는 수식만으로 실험실 배경·연구원·의료 기능이나 특정 색온도를 추가하지 않는다.'),
 (2, 'approved', '소프트박스를 사용하는 광원/확산 장치 선택이다. 화면의 실제 그림자 경계는 따로 명시되지 않았다.', [
  ('light_type','lighting','illuminating_light','lighting.source.modifier','softbox',
   '광원 측 소프트박스 장치를 명시한다.')],
  '소프트박스라는 장치 이름만으로 거리·각크기·화면 전체의 부드러운 그림자나 빛 방향을 확정하지 않는다.'),
 (3, 'approved', '사진을 판타지 장르로 읽도록 하는 표현 맥락이다. 개별 세계 법칙·종·마법 사건은 없다.', [
  ('genre','style','image','genre.fantasy','fantasy',
   '판타지는 이 후보가 직접 선언한 장르 맥락이다.')],
  '장르 이름만으로 초현실 법칙·생물·서사 사건·특정 시대를 생성하지 않는다.'),
 (4, 'approved', '파인아트 사진의 작업 장르를 선언한다. 전시 장소나 특정 재료·화풍은 정하지 않는다.', [
  ('genre','style','image','genre.fine_art','fine art',
   '파인아트는 사진 작업의 장르/표현 목적 범주다.')],
  'art/gallery metadata를 화랑 장소·인쇄 매체·특정 미술 운동의 긍정 근거로 쓰지 않는다.'),
 (5, 'approved', '영상 면에 기록된 움직임 번짐이다. 어떤 대상이 어떤 방향으로 움직였는지는 없다.', [
  ('motion_rendering','camera','image','image.motion.blur','motion blur',
   '모션 블러는 물리 행위가 아닌 기록된 영상의 움직임 표현이다.')],
  '물리 동작·카메라 흔들림·패닝·주체의 이동 방향이나 속도를 블러만으로 추론하지 않는다.'),
 (6, 'approved', '플래시 광원과 경질 광질을 함께 명시한다. 방향·밝기·색·피사체는 없다.', [
  ('light_type','lighting','illuminating_light','lighting.source.flash','hard flash',
   'flash가 광원의 종류를 명시한다.'),
  ('light_quality','lighting','illuminating_light','lighting.quality.hard','hard flash',
   'hard가 플래시의 경질 광질을 명시한다.')],
  '플래시를 카메라 정면·고출력·특정 색으로 자동 보충하지 않고 완결된 다광원 구성으로 분류하지 않는다.'),
 (7, 'approved', '형광 광원을 가리키는 조명 후보다. 물체 고유색이나 발광 도료를 지정하지 않는다.', [
  ('light_type','lighting','illuminating_light','lighting.source.fluorescent','fluorescent',
   '현재 조명 의미의 fluorescent는 광원 발생 계열을 나타낸다.')],
  '형광이라는 말만으로 녹색 색편이·깜빡임·병원·실험실이나 물체의 형광색을 확정하지 않는다.'),
 (8, 'approved', '여행 사진이라는 사진 장르다. 실제 이동 경로·나라·배경·촬영 장치는 없다.', [
  ('genre','style','image','genre.travel','travel photograph',
   '물리 매체가 아닌 여행 사진의 장르를 선언한다.')],
  '기존 medium 소속을 의미 근거로 유지하지 않고 실제 여행 이력·국적·장소·카메라를 추정하지 않는다.'),
 (9, 'approved', '50mm로 명시된 표준 계열 렌즈 선택이다. 촬영 거리·조리개·센서 크기는 없다.', [
  ('lens','camera','camera','lens.focal_length','50mm',
   '본문에 초점거리 50mm가 명시되어 있다.')],
  '명명된 표준 렌즈 분류와 모든 센서에서의 실제 화각을 동일시하지 않고 거리·심도·초점면을 추론하지 않는다.'),
 (10, 'approved', '반려동물을 다루는 사진 장르를 선언한다. 구체 종·마릿수·동반 동물 관계는 없다.', [
  ('genre','style','image','genre.pet','pet photography',
   '반려동물 사진이라는 장르가 본문의 완결된 의미다.')],
  '장르의 주제어를 독립 동물 추가나 동반 동물 역할로 확대하지 않고 종·수·인간 주인을 발명하지 않는다.'),
 (11, 'approved', '골든 아워라는 자연광 주기의 시간 맥락이다. 특정 광원 장치의 종류가 아니다.', [
  ('time_of_day','timing','scene','timing.time_of_day.golden_hour','golden hour',
   '하루의 자연광 주기 중 시점을 명시한다.')],
  'golden hour를 광원 장치 종류로 유지하지 않으며 일출/일몰 중 하나·정확한 시각·맑은 날씨·특정 색 수치를 추정하지 않는다.'),
 (12, 'approved', '창을 통한 빛과 그 부드러운 광질을 함께 선택하는 조명 후보다.', [
  ('light_type','lighting','illuminating_light','lighting.source.window_light','soft window',
   '조명 본문의 window가 창을 통한 광원의 통로를 나타낸다.'),
  ('light_quality','lighting','illuminating_light','lighting.quality.soft','soft window',
   'soft가 실제 선언된 광질이므로 장치 이름만으로 추정한 경우와 구별한다.')],
  '창이라는 조명 통로만으로 실내 장소·커튼·구체 창 위치·입사 방향을 추가하지 않는다.'),
 (13, 'approved', '음식 사진 장르다. 특정 음식·그릇·조리 동작은 정해지지 않았다.', [
  ('genre','style','image','genre.food','food photography',
   '음식 사진이라는 장르를 본문이 명시한다.')],
  'genre의 주제명만으로 새 음식·소품을 생성하거나 모든 음식 사진을 정물로 제한하지 않는다.'),
 (14, 'approved', '디젤펑크라는 복고 기술 계열의 미적 표현 맥락이다. 구체 세계 제도나 연료 장치는 없다.', [
  ('aesthetic_trend','style','image','style.aesthetic.dieselpunk','dieselpunk mood',
   'mood를 포함한 문구는 미감의 이름이며 지속적 세계 규칙을 선언하지 않는다.')],
  '복고 태그에서 역사적 사실·산업시설·디젤 기관·세계 규칙이나 특정 감정을 자동 도출하지 않는다.'),
 (15, 'approved', '거리 사진의 장르를 선언한다. 구체 장소·도시·행위자·비연출 여부는 없다.', [
  ('genre','style','image','genre.street','street photography',
   '거리 사진은 사진의 장르/관습 범주다.')],
  '거리 장르만으로 도시 장소를 교체하거나 사람·군중을 추가하고 비연출 촬영이라고 확정하지 않는다.'),
 (16, 'approved', '집중감 있는 장면 분위기의 제안이다. 한국어가 렌즈 초점이나 개인의 실제 마음과 구별한다.', [
  ('mood','atmosphere','scene','mood.focused','집중한 분위기',
   '한국어 본문이 집중한 분위기라는 정서 해석을 명시한다.')],
  'focused를 광학 focus 슬롯·특정 표정·직업·실제 인물의 마음 상태로 바꾸지 않는다.'),
 (17, 'approved', '24mm 광각 렌즈의 선택이다. 촬영 거리·카메라 높이·주체 형태는 없다.', [
  ('lens','camera','camera','lens.focal_length','24mm',
   '명시된 초점거리 24mm를 렌즈 속성으로 기록한다.')],
  '광각 렌즈만으로 카메라 접근·로우앵글·신체 과장·배럴 왜곡 정도를 확정하지 않는다.'),
 (18, 'approved', '실험실이라는 장소의 종류다. 특정 실험·장비·안전등급·종사자는 없다.', [
  ('location','setting','environment','setting.location.laboratory','a laboratory',
   '물리 장소의 종류가 직접 명시되어 있다.')],
  '과학 metadata에서 연구원·실험 행위·의료 목적·멸균·광원·구체 장비를 추가하지 않는다.'),
 (19, 'approved', '실내 공간을 대상으로 하는 인테리어 사진 장르다. 특정 방·가구·렌즈는 없다.', [
  ('genre','style','image','genre.interior','interior photography',
   '인테리어 사진은 공간 자체의 지정이 아닌 사진 작업의 장르다.')],
  '장르를 물리 장소·건축 구조로 대체하거나 가구·생활 흔적·광각 렌즈를 자동 보충하지 않는다.'),
]

rows = []
for ordinal, status, meaning, selected, rejection in DECISIONS:
    cid = packet['ids'][ordinal]
    record = packet['records'][cid]
    roles, facts = [], []
    for tag, dimension, target, prop, quote, rationale in selected:
        text = record['content']
        field = 'ko' if quote in text['ko'] and quote not in text['en'] else 'en'
        fact = {'pointer': '/content/' + field, 'quote': quote, 'dimension': dimension,
            'target': target, 'property': prop}
        roles.append({'slot_id': tag, 'semantic_role': catalog[tag]['semantic_role'],
            'scope': 'whole_record', 'realization_ids': ['base'], 'rationale': rationale,
            'evidence': [fact]})
        facts.append({**fact, 'realization_id': 'base'})
    rows.append({'candidate_id': cid, 'meaning_summary': meaning,
        'recommended_kind': 'visual_option', 'corrections': [], 'roles': roles, 'facts': facts,
        'rejected_boundaries': [rejection], 'uncertainties': [], 'status': status,
        'all_roles_considered': True})
assert len(rows) == 20 and len({r['candidate_id'] for r in rows}) == 20
(HERE / 'batch_00000_00020.json').write_text(json.dumps({'decisions': rows},
    ensure_ascii=False, indent=2) + '\n')
