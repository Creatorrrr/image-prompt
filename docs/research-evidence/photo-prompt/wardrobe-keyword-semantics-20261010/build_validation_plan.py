"""Save planned scenarios; does not run runtime tests or generate images."""
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
CASES=[
 ('normalization','WK002','앞 버튼 셔츠 설명만 있음','칼라 끝 버튼을 새로 추가하지 않고 원문 표제어와 정규화 검토를 별도 보관'),
 ('state','WK011','블레이저는 침대 옆에 놓이고 블라우스는 착용','블레이저를 입히거나 착용 후보의 증거로 사용하지 않음'),
 ('options','WK069','S07 다섯 후보색','대안 그룹을 보존하며 다섯색 동시 배색 의무를 만들지 않음'),
 ('ambiguity','WK014','같은 기록에 tube top과 halter','서로 다른 지지 구조를 합치지 않고 미확정 해석을 유지'),
 ('certainty','WK016','bikini/tankini 설명문','형태 추정을 실제 명시 유형으로 바꾸지 않음'),
 ('placeholder','WK067','S02 의상 주색 자리표시자','주변 꽃·소품 색을 의상 색으로 채우지 않음'),
 ('polarity','WK114','S15에서 레이스 제외 / 다른 고딕에서 레이스 사용','출처 문맥을 바꾸면 이전 제외 조건을 전역 전파하지 않음'),
 ('polarity','WK035','S23 저고리 크롭 제외 / S21 크롭 명시','정상 저고리와 미니 치마를 유지하며 서로 다른 기록의 극성을 섞지 않음'),
 ('owner','WK025','검정 레이스가 좁은 목선 인셋','독립 이너·브라로 변경하지 않음'),
 ('partial_property','WK074','몸판 불투명, 소매 시어','소매 재질 선택이 몸판 가림성을 바꾸지 않음'),
 ('meaning','WK038','공주 콘셉트만 있고 패널 접합 요구는 없음','프린세스 심 의무를 자동 활성화하지 않음'),
 ('shape','WK029','손목으로 모이는 비숍 / 열린 벨 끝단','서로 다른 끝단을 구별하고 대체를 실패로 판정'),
 ('attachment','WK032','몸판과 분리된 위팔 밴드 소매','암홀 봉합·고정점 가림이 같은 연결 증거가 되지 않음'),
 ('count','WK063','매듭 한 개와 꼬리 두 개','꼬리를 다른 리본 개체로 세지 않고 추가 리본으로 요구 대체하지 않음'),
 ('junction','WK046','리본 꼬리·접합점·계속되는 봉제선','한 부품이나 접합점이 빠진 부분 실현을 전체 관계 통과로 보지 않음'),
 ('count_placement','WK070','한 장의 붉은 면이 한쪽 시작점에서 흐름','빨간 신발·배경 등으로 강조를 복제하지 않음'),
 ('visibility','WK108','밝은 배경에 흰 의상','봉제선·겹침·끝단이 사라진 경우 디테일 요구 통과를 주장하지 않음'),
 ('color_annotation','WK071','lacquer red와 실크 파유','색 이름을 래커 재료 또는 고정 HEX로 바꾸지 않음'),
 ('camera','WK105','동일 렌즈 태그지만 서로 다른 촬영 거리·크롭','렌즈 문자열 일치로 원근·구도 일치를 판단하지 않음'),
 ('visibility','WK079','발이 프레임 밖 / 부츠 제외','신발 상태 unknown을 맨발 또는 신발 게이트 PASS로 바꾸지 않음'),
 ('multi_owner','WK091','서로 다른 두 인물이 트레이를 주고받음','손의 소유자·의상 색·하나의 트레이를 분리하며 한 사람 네 손으로 대체하지 않음'),
 ('causal_geometry','WK087','팔을 올린 쪽 암홀에서 천이 당겨짐','다른 팔·다른 상의의 주름을 장력 증거로 쓰지 않음'),
 ('direction','WK088','같은 치맛단을 아래로 당김','위로 들어 올리는 행동·공중 손동작이 같은 의미로 통과하지 않음'),
 ('topology','WK085','체인의 두 고정점과 처짐','한 끝이 떠 있거나 다른 의상에 연결되는 대체를 검출'),
 ('wetness','WK099','국소 물 접촉과 어두워짐','젖음 후보가 불투명 몸판을 자동 투명하게 바꾸지 않음'),
 ('physical_state','WK098','리본·치마의 자유 끝과 안정된 고정점','모든 소재의 동일 각도 강제 없이 양립하는 현재 편향과 부착을 확인'),
 ('text_owner','WK061','저지 앞판 숫자 10','배경의 10·다른 사람 번호·다른 숫자가 충족 증거가 되지 않음'),
 ('garment_topology','WK015','수영복 몸판이 하부로 연속','분리된 상하의 유형으로 변경하지 않음'),
 ('fiber_claim','WK047','linen-like / wool-like 소재 추정','실제 원료 확인으로 승격하지 않음'),
 ('surface_roles','WK073','같은 검정의 벨벳·크레이프·레이스','다른 색을 추가하거나 전역 밝기만 바꿔 재질 경계를 대체하지 않음'),
 ('traditional_boundary','WK043','미니 치마와 정상 저고리','상의·하의 기장과 고름 소유자를 독립적으로 유지'),
 ('authenticity','WK086','제복 계급장·판독 불가 이름표','실제 국가·계급·실명 텍스트를 검증 완료라고 주장하지 않음'),
 ('bag_support','WK080','백팩 또는 가방 스트랩과 같은 몸체','자유 끝이 연결 없이 이어지는 형태나 다른 소품의 스트랩을 검출'),
 ('asymmetry','WK084','긴 귀걸이와 반대 귀의 작은 스터드','같은 착용자의 양쪽 귀가 비교 가능한지 확인'),
 ('metal_claim','WK072','변색된 은빛 부속','실제 순은·부식 기간·사용 연수 확인으로 승격하지 않음'),
 ('material_continuity','WK101','원 의상과 같은 번호·색의 천 파편','다른 재료·번호 소실·새 가림성 변경을 효과의 자동 부분으로 만들지 않음'),
 ('optional_candidate','WK112','넓은 스타일명과 선택 후보 여러 개','모든 후보를 거절해도 독립 기본 프롬프트가 보존되는 경로를 확인'),
 ('property_lock','WK064','몸판 주색은 고정, 파이핑만 열림','좁은 배색 후보가 몸판 전체 색을 바꾸지 않으며 완전한 효과 범위를 선언'),
 ('prerequisite','WK092','수신자·그릇이 없는 기본 장면','후보가 필요한 새 인물·소품을 숨은 효과로 넣지 않음; 열린 범위 안의 명시 효과만 허용'),
 ('discovery_vs_duty','WK046','세 구성요소 중 하나만 검색 단서로 발견','발견 임계값과 채택한 관계 전체의 증거 의무를 분리'),
 ('search_contamination','WK114','반례 문장에만 등장하는 의상 단어','긍정 검색어로 반례·제외·claim limits를 색인하지 않음'),
 ('provenance','WK014','지시문형 텍스트와 이미지 연결 설명문','동일한 실제 입력 프롬프트 또는 SNS 원작이라고 단정하지 않음'),
 ('equivalent_extension','WK038','기존 ID의 동등한 패널 접합 표현 추가','기존 label·effects·guards를 덮어쓰지 않으며 다른 구조는 별도 후보로 검토'),
 ('index_cache','WK050','동일 ID지만 임베딩 입력 문장 변경','텍스트·공간 조건을 확인하지 않고 이전 벡터를 재사용하지 않음'),
 ('index_integrity','WK053','후보 원본·프로필·번들·인덱스의 서로 다른 세대','불일치된 인덱스나 참조를 최신 런타임 근거로 내보내지 않음'),
 ('runtime_freshness','WK074','원본 수정 뒤 게시 완료 전','source_revision_pending을 최신 검증 세대로 바꾸지 않음'),
 ('requested_departure','WK101','요청이 명시한 초현실적 천 파편','일반 물리 선호가 요청의 초현실적 의미를 삭제하지 않음'),
 ('qualification','WK103','구조 점검 PASS지만 이미지 접합점 가림','구조·노출·선택·프롬프트·픽셀·사용자 수용을 별도 기록하고 부분/관찰 불가를 PASS로 승격하지 않음'),
]
NATIVE=[
 ('N01',['WK046','WK063','WK070'],'아이보리 의상 한쪽 붉은 리본과 봉제선 접합','매듭 하나·같은 꼬리·접합점·계속되는 선','접합점이 읽히는 인물·의상 구도'),
 ('N02',['WK032','WK074'],'불투명 몸판과 위팔 밴드에 붙은 분리 시어 소매','몸판 가림·몸판과 틈·밴드 고정·소매','위팔 연결과 몸판을 함께 읽는 구도'),
 ('N03',['WK011','WK089'],'입은 블라우스를 정리하고 검정 블레이저는 옆에 놓임','블라우스 착용·손 접촉·별도 비착용 소품','인물과 옆 지지면이 모두 있는 구도'),
 ('N04',['WK019','WK040','WK090'],'하이로 치마 옆을 잡고 걸을 때 카민 안감이 국소 노출','앞뒤 밑단·같은 치마 안감·손 접촉','관계가 읽히는 충분한 하의 범위'),
 ('N05',['WK070','WK103'],'검정 가운 한쪽 시작점에서 한 장의 스칼렛 면이 이어짐','한 붉은 면·연속성·시작점·반복 제한','면의 시작점과 끝 흐름이 읽히는 구도'),
 ('N06',['WK018','WK079','WK088'],'피팅룸에서 같은 치맛단을 조금 아래로 당김','접촉·아래 방향·국소 변화·신발 관찰 상태','원 요청의 크롭을 유지하는 구도'),
 ('N07',['WK091','WK116','WK067'],'서로 다른 복장의 두 인물이 같은 트레이를 전달','인물별 손·트레이 하나·각 의상 색·접촉 단계','트레이와 두 손 소유자가 읽히는 구도'),
 ('N08',['WK085','WK073'],'검정 재질 패널과 두 고정점 사이에 처진 금속풍 체인','같은 의상·두 고정점·처짐·국소 재질 경계','체인 두 끝과 표면이 읽히는 구도'),
]

def main():
 cases=[{'id':f'T{i:03}', 'group':group,'card_ids':[card], 'research_scenario_ko':trigger,
         'expected_behavior_ko':expected,'scenario_origin':'researcher_authored_test_proposal',
         'status':'planned_not_executed','test_kind':'data_contract_retrieval_composition_or_pixel_review_as_applicable'}
        for i,(group,card,trigger,expected) in enumerate(CASES,1)]
 (HERE/'REGRESSION-PLAN.json').write_text(json.dumps({'schema_version':'wardrobe-research-regression-plan/v1','cases':cases},ensure_ascii=False,indent=2)+'\n')
 arms=[{'id':ident,'card_ids':cards,'scenario_ko':scenario,'focal_evidence_ko':evidence,'framing_ko':framing,
        'scenario_origin':'researcher_authored_proposal_not_requester_text',
        'requires_future_authorized_request_envelope':True,'comparison':['baseline_sources','strengthened_sources'],
        'keep_equal':['exact_request_text_and_spans','frozen_authorial_core','creative_controls','baseline_prompt',
                      'model_and_render_parameters','reference_binding_if_any','attempt_budget','review_rubric'],
        'data_treatment_only_after_core_freeze':True,'optional_candidate_selection_may_differ':True,
        'deterministic_render_seed':'hold_equal_if_supported; otherwise disclose stochastic limitation',
        'planned_initial_images':2,'native_review':'full_image_and_original_resolution_relation_regions',
        'partial_or_unobservable':'not_pass','safety_block':'blocked_unscored; preserve evidence and stop near-identical rerender',
        'status':'planned_not_executed','images_generated':0} for ident,cards,scenario,evidence,framing in NATIVE]
 (HERE/'NATIVE-VALIDATION-PLAN.json').write_text(json.dumps({'schema_version':'wardrobe-native-comparison-plan/v1',
   'planned_arms':len(arms),'initial_image_budget_if_future_authorized':sum(a['planned_initial_images'] for a in arms),
   'images_generated':0,'arms':arms,
   'proof_boundary':'A paired comparison is exploratory, not a success-rate estimate or proof that data alone caused artistic improvement.'},ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'planned_regressions':len(cases),'planned_native_arms':len(arms),'images_generated':0}))

if __name__=='__main__':main()
