#!/usr/bin/env python3
"""Provisional per-card implementation disposition; never source adoption permission."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
cards=json.loads((HERE/'semantic-cards.json').read_text())['cards']
overrides={
 'V14':('reuse',['cand_7b74028598cd503abdcd5256886084e5'],'정상 연결 EVA는 기존 전체 압력복·배낭·안전줄 의미를 우선 재사용한다. 끝점/역할의 추가 의무는 따로 검토한다.'),
 'V15':('new',['cand_7b74028598cd503abdcd5256886084e5'],'이웃은 부착 안전줄이다. 자유 끝이라는 반대 상태를 기존 소스 의미에 덧씌우지 않는다.'),
 'V16':('reuse',['cand_49652d62206e522fb28ad2b5d4c2bc43'],'기존 네 성분과 전체 authored-components 의무를 비교한다. 단순 제목/동의어 신규 등록은 피한다.'),
 'V18':('refine',['cand_7e3a0e42226b591c9deeffb66b6e3f34'],'기존 노후 공간은 우주선 외피·도킹 구조가 아니다. 보완은 명시적 diff 또는 독립 실현으로 한다.'),
 'V19':('new',['cand_33e0096e59a5582a8844388034c8833a'],'기존 유령선의 물/항적/rigging/유령 단절과 빈 자동 우주선은 다르다. 해당 이웃은 재사용 권한이 아니다.'),
 'V22':('context',[],'키 눈금·사진은 세대 계승/혈연의 정황이다. generic habitat 흔적 후보를 검토하되 세대 항해의 입증으로 등록하지 않는다.'),
 'V26':('refine',['cand_7b6ccb0fb8095db38c6337a0ac3df0d4'],'거대구조물 이웃은 회전·거주·조립 의미를 가진다. 이를 삭제하지 않고 척도 관계의 독립 필요를 검토한다.'),
 'V28':('refine',['cand_8ed5a9486be65af9b7a3e3d39ca477fb'],'기존 벽/막/도관과 우주선의 지지 아치 통합을 비교한다. 단순 명칭 변경으로 생명 기능을 추가하지 않는다.'),
 'V31':('reuse',['cand_4c2a218da12358c2ab9e8ae53951adc4'],'기존 숙주/부착체/접점을 우선 비교하고 영양·피해·편익의 비가시 한계를 유지한다.'),
 'V36':('new',['cand_e86ead0041ee5c1787e0259e037a2b94'],'기존 다른 세계 귀환 격리실의 primary guard를 지우지 않는다. 실제 표본 귀환 경로와 독립 컨텍스트가 필요하다.'),
 'V41':('context',[],'검사 배치가 생체 해부·비동의를 입증하지 않는다. 양성 초안 보류를 유지한다.'),
 'V44':('reuse',['cand_ee6b62e77e9357b69cd2ae19b63a3677'],'기존 배태 실루엣과 비교하고 원인·성별·동의의 미확정을 보존한다.'),
 'V45':('defer',['cand_313088e0690a56688ea5e89ee2577058'],'성적 생체기계와 vagina dentata는 동일하지 않다. 실제 원전/도판 검토 전 도상 후보 등록을 보류한다.'),
 'V47':('context',[],'접근 거부/할당 칸만으로 생식 강압·우생학이 성립하지 않는다. 양성 초안 보류를 유지한다.'),
 'V48':('refine',['cand_ffd66c197f525d9393ccf212a2785e2e'],'기존 서비스 안드로이드와 외피/손 연속 부품의 추가 관계를 검토한다. 의식/악의 의무를 만들지 않는다.'),
 'V53':('new',['cand_a7f1e74071375d87a59a7181fe761301'],'기존 정보/인지 위험 진단은 문맥으로 유지한다. 새로 제안한 화면/독자 관계도 위해의 입증이 아닌 선택 재료다.'),
 'V55':('reuse',['cand_d1d1920147855b41a40559368ae95ea0'],'기존 그림자/원반/렌즈상 전체 실현을 비교한다. 전경 우주선은 열린 저술 선택이며 모든 블랙홀의 의무가 아니다.'),
 'V56':('defer',[],'조석력의 물리 정확도를 필요한 구체 설정과 시각화 자료로 추가 검토한다. 늘어난 선체만으로 물리 기제를 승인하지 않는다.'),
 'V57':('defer',[],'연속 기하의 투영 모순과 정상 곡률/렌즈를 구분할 도식·정밀 예시가 필요하다. broad impossible이라는 라벨을 native 사실로 만들지 않는다.'),
 'V59':('context',[],'조립 배치는 자기복제·절멸 목표·나노 증식의 단서만 된다. 일반 제조 재료의 기존 원문을 먼저 확인한다.'),
 'V61':('context',['cand_16a369703de2528fbf8ceee0faa7539e','cand_2e56b944d56f50e3af7ac1a4adf95eaa'],'유해/처리/음식의 동시 배치는 식인의 종·기원·경로를 증명하지 않는다. 진단을 보존하고 양성 초안은 보류한다.'),
}
matrix=[]
for c in cards:
    decision,neighbors,reason=overrides.get(c['card_id'],('new',[],'이 카드의 구체적인 소유/경계/기능 관계는 신규 작성 검토 대상으로 제안한다. 기존 전체 의미의 동등 관계가 확인되면 reuse/refine으로 바꾼다. 현재 정확 어휘 미검출은 신규 필요의 증거가 아니다.'))
    matrix.append(dict(card_id=c['card_id'],title=c['title'],proposed_decision=decision,status='research_recommendation_not_final_source_adoption',neighbor_cids=neighbors,reason=reason,mandatory_before_registration=['rebaseline current corpus and installed generation','inspect full existing positive fields, selected realization, conditions, bindings and effects','record exact reuse/refine/new decision and source hashes','validate proposed role and owner/property effect compatibility'],native_approval=False))
(HERE/'adoption-matrix.json').write_text(json.dumps(dict(schema='space-horror-adoption-plan/v1',records=matrix),ensure_ascii=False,indent=2)+'\n')
