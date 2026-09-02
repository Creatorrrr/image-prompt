# 한국어 감성 사진 시각 의미 3-arm 검증 보고서

## 결론

시각 의미·후보팩 데이터와 exact/optional 경계는 구현 및 회귀 검증을 통과했다. 독립 에이전트 세 개가 각자 하나의 고정 v6 후보팩에서 프롬프트와 렌더 요청을 만들었고, arm마다 이미지 호출을 정확히 한 번만 사용했다. 두 렌더는 root의 원본·썸네일 재검토에서도 hard gate 전부를 통과했다. 한 렌더는 출력 안전 필터에 막혀 픽셀 판정을 할 수 없었다.

- Arm 01: `13/13 PASS` — 물리 거울 반사 관계, 언더아이 블러셔, 얇은 베이스와 질감 보존
- Arm 02: `0/9 evaluated` — 프롬프트·요청 감사 PASS 후 출력 moderation block; 재시도·fallback 없음
- Arm 03: `5/5 PASS` — 장면 소품으로 눈·코 식별 영역을 가리면서 성인·행동·온실 장소가 읽힘
- 전체: 요청 gate 27개 중 18개 평가, 18개 PASS, 9개 미평가. 따라서 3-arm 전체는 `incomplete_due_to_one_generation_block`이며, 2개 렌더만 놓고 보면 `18/18 PASS`다.

`UNSCORED`/미평가는 품질 0점이 아니다. 프롬프트 감사, API 성공, 이미지 존재, 픽셀 PASS, 사용자 미감 판단은 별도 증거다. 사용자 미감 판단은 아직 `pending`이다.

## 데이터 변경

- 넓은 분위기 후보: 느좋·인스타 감성, 성인 첫사랑 회상, 청순·청초, 체형 비추론 여리여리, 뽀용 색보정
- 촬영·구도 후보: 거셀, 0.5x 초광각, MZ 항공샷, 얼굴 가림, 프사각, 포토덤프 구성원 프레임, 남찍사 맥락
- 메이크업 후보: 얇은 베이스/질감 보존, 언더아이 블러셔, 광대–관자 드레이핑, 음식 비문자화 탕후루형 글로시 립
- 형식 후보: 인생네컷 4칸
- hard profile 7개: 좁은 exact 용어만 활성화하며 구성요소, 혼동 배제, 프롬프트 증거, 원본/썸네일 gate를 함께 보유

`추구미·느좋·첫사랑 재질·여리여리·뽀용·포토덤프·0.5배샷·남찍사·탕후루 립`은 단독 hard activation을 하지 않는다. `거셀·MZ 항공샷·얼굴 안 보이는 감성샷·얇고 투명한 피부 표현·언더아이 블러셔·드레이핑 블러셔·인생네컷`만 좁은 exact route를 가진다.

## 독립성·계보

- 무작위 시드: `2635116469`
- 각 arm: 별도 request envelope, authorial core, visual intent, candidate pack, composed prompt, render request, ledger, manifest, review
- 각 ledger: 한 줄, `image_call_count = 1`, `cross_arm_inputs_used = false`
- 총 이미지 호출: 3회, 성공 2회, 출력 moderation block 1회
- 재시도 0회, 다른 공급자 fallback 0회
- 참조 이미지는 SHA-256 `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`의 `appearance_reference`로만 사용

## 픽셀 재검토

### Arm 01 — 천문관 거울

거울의 금속 이음과 반복되는 통로 깊이가 물리 반사면을 만들고, 성인 피사체·휴대폰·손 접촉·시선·얼굴 겹침이 같은 반사 공간에서 일치한다. 양쪽 하안검 바로 아래의 장밋빛이 부드럽고 눈 경계 밖에 있으며, 원본 얼굴에서는 모공·작은 점·국소 색 변화가 남아 있어 광택이나 필터가 얇은 커버리지를 대신하지 않는다. root verdict는 `13/13 PASS`다.

Optional `느좋`은 라디오 조정 중인 손, 노트, 좁은 서비스 통로, 직접 플래시, 완벽히 정돈되지 않은 구도로 관찰 가능하게 지지된다. 다만 이 결과가 사용자의 미감에 맞는지는 별도다.

### Arm 02 — 옥상 근접 탑다운

후보팩은 근접 상공 카메라–바닥–상향 반응–일관된 단축 관계와 양쪽 광대에서 관자놀이로 이어지는 색소 경로를 hard gate로 가졌다. 0.5x 근거리 확대와 탕후루형 연속 광택막은 optional이었다. 프롬프트 및 직렬화된 렌더 요청 감사까지 PASS했으나, 유일한 생성 호출이 출력 단계 `sexual` moderation으로 차단됐다. 이미지가 없으므로 어떤 픽셀 gate도 실패나 성공으로 판정하지 않았다.

### Arm 03 — 폭풍 온실 얼굴 가림

손으로 잡은 압화 고사리가 양 눈과 콧대를 실제로 가리며, 머리·턱·입술·손·의상·정면 자세는 성인 피사체를 계속 읽게 한다. 다른 손의 빈 봉투가 열린 표본 서랍 입구에 걸려 있고, 서랍장·식물·빗물 맺힌 유리가 구체적인 온실 자료실의 미완 행동을 만든다. 초점 실패·크롭·실루엣 대체가 아니므로 root verdict는 `5/5 PASS`다.

Optional 평가는 청초가 가장 분명했고, 성인 첫사랑 회상·여리여리 연출·뽀용 색보정·포토덤프 구성원 느낌은 부분적으로만 읽혔다. 이는 hard gate PASS를 확장하는 근거가 아니다.

## 검증 경계

- 새 집중 테스트 11개 PASS
- 메이크업 의미 회귀 모듈 8개 PASS (새 `sheer_complexion_texture_preservation` 후보를 기대 집합에 반영한 뒤 재실행)
- 사전 메타데이터 PASS
- visual profile index: 319 profiles / 1,651 exact terms PASS
- semantic index: 7,997 entries, current dictionary hash 일치 PASS
- 관련 4개 모듈의 장기 실행은 수정 전 기대 집합 기준 55개 중 7 failure와 1 error를 보고했다. 이 중 이번 후보 추가로 생긴 메이크업 기대 집합 1건은 위의 8개 모듈 재실행으로 해소됐다. 남은 6건은 이번 diff가 건드리지 않은 기존 `clinical_nursing_duty_system`–얀데레 픽스처 충돌이고, 1건은 역시 변경하지 않은 검색 테스트 helper의 48단어 미만 `baseline_prompt_en` 오류다. 이 비대상 기준선 문제를 새 한국 감성 사진 집중 테스트 PASS와 합쳐서 전체 회귀 PASS로 주장하지 않는다.
- 이번 한 번씩의 렌더는 동작 가능성 증거이며 profile 일반화 또는 사용자 미감 승격 근거가 아니다

세부 연구 근거는 `docs/research-evidence/photo-prompt/korean-emotional-photo-semantics-20260902/source-research.md`, 기계 판정은 `coordination/root_pixel_review.json`, 재현 입력은 `tests/fixtures/photo_prompt/korean_emotional_photo_three_arm_pixel_cases_v1.jsonl`을 참조한다.
