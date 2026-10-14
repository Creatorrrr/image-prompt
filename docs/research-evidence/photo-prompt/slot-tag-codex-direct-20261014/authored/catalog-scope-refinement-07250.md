# 카탈로그 범위 명료화 제안 — 07250

운영에 적용하지 않은 직접 심사 제안이다. 제안 141의 실제 정의와 SOURCE 원문 28개(필수 참조 4개 포함), source binding 2개, 관련 명세 32개를 읽었다. 원래 후보의 조건·효과·가시성 gate·참조 소유자를 유지한다. 동결된 기존 5B/역검색 판정이나 native pilot은 수정하지 않았다.

| 역할 | 권고 | 실제 근거와 경계 |
|---|---|---|
| body_hair | 열거된 속성 범위를 제한적으로 추가 | 같은 성인 피부 부위의 털 부착·굵기·색소가 실제 profile의 필수 본문이다. 밀도·길이·분포도 유지한다. 두피에서 목으로 이어지는 모발은 hair_style이며 피부 마감·수염·눈썹을 체모로 흡수하지 않는다. |
| body_marking | 인간 전용 applicability를 제한적으로 확장 | 비인간 몸 표면의 닫힌 색 고리와 같은 바탕색 중심이 실제 필수 본문이다. human-only 필터와 wildlife 거부만 제거하고 product/jewelry/food 거부는 유지하는 안이다. 원문의 nonhuman-only 및 인간 참조 변환 금지는 그대로다. 팔찌·의복·투사 그림자·빛 방출을 표식으로 대체하지 않는다. |
| footwear | 명시된 국소 맨발 상태와 소유자 분기를 추가 | 실제 두 원문은 지정 발등·발가락의 신발·양말 없는 상태와 자기 발목 연결을 요구한다. 신발이 있을 때는 신발 object, 명시적 부재 상태는 착용자의 지정 발 부위에 결속한다. 보이지 않는 신발을 부재로 간주하거나 존재하지 않는 신발 owner를 만들지 않는다. 피부색·오픈토 신발은 음성 witness다. |
| brow_style / expression | 범위 확장 없이 경계를 명료화 | 눈썹의 미간 수축·하강·내측 상승·눈 기준점 대비 상승은 현재 expression의 눈 주위 반응에 해당한다. 보류 4건은 brow_style에서 not_fit으로 재심사할 근거가 있다. 털을 위로 빗은 상태와 아치형 grooming은 brow_style에 남는다. 사적 감정이나 숨은 근육 작동은 입증하지 않는다. |
| golden hour 및 조명·시간 이웃 | 5개 역할의 경계 유지·명료화 | 실제 본문은 golden hour뿐이고 원효과는 lighting이다. 실제 하루 시점·광원 device·광질·색·방향·완결된 조명 구성을 새로 만들 수 없다. 기존 timing-only 보정의 lighting 삭제는 철회 상태를 유지한다. |

역할의 context fact와 전체 실제 effects inventory는 다르다. 따라서 golden hour의 하루 주기 명칭을 context로 설명하면서 기존 lighting 효과를 유지하는 최소 영·한 본문 명료화안을 별도로 제안했다. 수정 후 전체 복사본을 다시 읽었다. 이 안도 실제 scene-time 변경을 허용하거나 v3 자격화를 완료하지 않는다. 기존 coarse lighting 효과를 실제로 보호할 typed inventory가 추가 직접 심사를 기다린다. 표시된 lighting 역할이 없다는 이유로 해당 효과를 삭제하거나 no-op으로 바꾸면 안 된다.

새 역할은 제안하지 않는다. 본문·조건으로 구분할 수 있는 사례를 모두 포함하려고 카탈로그를 무차별 확장하지 않았다. JSON의 exact_field_changes와 complete_spec_before/after에 10개 역할의 정확한 변경값, 긍정 witness 23개와 음성 guard witness 5개, 직접 영향 CID를 기록했다. 기존 proof/catalog/native hash는 갱신하지 않았다.

제안 채택 후에는 영향 후보와 참조 parent를 개별 재심사해야 한다. 구조적 CID 참조로 찾은 parent 5개 중 inner-brow bundle만 이번에 전체를 읽었고, 나머지 4개는 재심사 대기다. 이 목록은 새 의미 판정이나 전체 corpus 영향 검토의 완료 증거가 아니다. 같은 제안을 채택하더라도 기존 native proof의 자동 이관은 허용하지 않는다.

정확한 근거·보정안은 `catalog-scope-refinement-07250.proposal.json`, 원문·명세 고정 복사본은 `catalog-scope-refinement-07250.sources.json`에 있다. 운영 native 자격화 수는 0이다.
