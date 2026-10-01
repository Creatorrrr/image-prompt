# 사진 편집 효과 데이터 반영 및 독립 이미지 검증

2026-10-01. 기준 커밋 `769f005f01fd54e302e0399e44ac1b2b20122c69`에서 작업했다. 원문 표 245행의 88개 의미군을 검토하여 후보 133개, optional bundle 28개, 시각 프로필 22개를 등록했다. 전체 차원 30개를 유지하며 사진 영상면, 피사체 피부, 장면 조명, 사진 속 인쇄물의 적용 대상을 구분한다.

운영 데이터 반영과 독립 에이전트 3개의 복잡한 장면 생성·원본 픽셀 검토를 완료했다. 최종 v2 결과는 원래 효과 **5/9 PASS**, 장면 전체 **1/3 PASS**다. 테스트 대상 신규 후보 **10/10**이 실제 후보팩에 노출되고 선택됐다. 필름 입자·할레이션·무채색 나머지 영역·암부 바닥의 네 실패를 보존했다. [원본 이미지와 9개 판정](qualification/README.md), [통합 검증 원장](qualification/coordinator-review.json).

## 운영 반영

| 항목 | 반영 전 | 반영 후 | 이번 추가 |
|---|---:|---:|---:|
| slot 후보 | 9,012 | 9,145 | 133 |
| optional bundle | 610 | 638 | 28 |
| 시각 프로필 | 1,076 | 1,098 | 22 |
| preset | 706 | 706 | 0 |

- [후보 확장](../../../../skills/photo-prompt-image-generator/assets/photo_prompt_editing_effects_extension.json): 관찰 가능한 성분, 명시적 적용 관계, 영향 차원·속성. 숫자나 공정 이력을 이미지에서 추론하지 않는다.
- [시각 의미 확장](../../../../skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_editing_effects.json): 작성 성분을 검색·문장 근거·구성 지시·픽셀 gate로 한 번만 작성하고 컴파일한다. 선택된 성분은 모두 판정하며 부분 충족은 실패다.
- [245행 이행 원장](implementation-disposition-ledger.json): 의미군별 재사용·추가 후보와 작업·연산 metadata 경로. 같은 그룹의 후보는 선택 가능한 관찰 결과이며 모든 포함 용어에 강제되는 레시피가 아니다.
- [외부 유지보수 원장 v2](../extension-maintenance/photo-editing-effects-20261001-v2.json): 기존 54개 자료와 [추가 3개 자료](source-supplement.json), provenance, 적용 경계. 연구 설명과 URL은 런타임 검색 문장에 넣지 않았다.

필름 입자를 물체 재질로 해석하지 않도록 기존 `texture:fine_grain`의 영상면 소유 범위를 명시했다. `texture:halation`의 기존 복합 의미인 “film halation and soft light bloom”과 ID는 보존하고, 적주황 경계 halo·중립색 확산·국부 bloom을 별도 후보로 추가했다. digicam 복합 후보와 숫자 ISO 후보에도 영상면 scope를 선언했으며, 실제 센서나 ISO를 증명하는 의무로 승격하지 않았다.

하이라이트 롤오프+bloom, 광학 확산+필름형 halation, 패닝+후막 플래시를 무조건 상호 배제하던 세 제외어는 대체 효과만 요청한 경우를 가리키도록 좁혔다. 기존 다른 제외어를 보존했다. 단독·공존·잘못된 대체 문맥을 실제 resolver와 helper에서 검증했다.

작업·진단·출력 정보와 관찰 결과를 분리했다. RAW·ICC·LUT·레이어 상태·frequency separation·복원·생성형 채우기 등은 자동 룩 후보로 등록하지 않았다. 필요한 경우 원본, 선택 영역, 원하는 결과, 편집 및 출력 조건을 별도로 공급해야 하며 한 장의 이미지로 실제 작업 이력을 증명하지 않는다.

## 후보팩과 잠금 경로

`semantic_source`와 후보팩의 공개 surface에 원본 `affected_properties`를 전달한다. 번들 일반 노출과 joint admission 모두 부분 속성 잠금을 확인한다. 일반 후보에도 충돌하는 속성이 있으면 ineligible로 표시한다. 프롬프트 감사는 선택한 속성 선언을 소스에서 다시 계산해 변조나 잠금 우회를 거절한다.

영상면 grain은 피사체 옷 색상 잠금과 공존할 수 있다. 전역 팔레트 조절은 보호된 색을 바꿀 수 있으므로 보수적으로 거절한다. bundle의 프로필 연결은 advisory 상태를 유지하며 선택만으로 자동 hard 의무가 되지 않는다. 별도 요청 근거나 explicit optional visual concept 채택으로 활성화해야 한다.

각 조합은 서로 다른 슬롯의 후보로 구성하고, 동시에 필요한 각 성분은 별도 component로 보존했다. 현재 컴포넌트의 one-of 계약을 이용해 두 관찰 성분 중 하나만 충족하고 통과하는 문제가 생기지 않게 했다.

## 1차 이미지에서 발견한 검색 공백과 v2 보완

1차 세 후보팩에서 A의 grain·halation·rolloff와 C의 selective color·lifted blacks·skin finish가 일반 후보 슬롯에 노출되지 않았다. B의 compact flash·shutter trace는 노출됐으나 luma/chroma 세부 후보는 빠졌다. 슬롯 샘플링 trace만 후보팩에 투영하고, 전체 장면 검색에서 효과 설명이 희석되는 경로를 확인했다. 해당 1차 이미지와 실패 판정은 보존했다.

v2는 소스에서 `core_assertion_discovery`를 명시한 후보·프로필만 동결된 typed assertion의 설명과 축별로 검색한다. 적용 속성·차원을 먼저 검토하고, per-assertion BM25F로 제한된 선택지를 기존 예약 여부와 무관하게 제공한다. 코드에 편집 키워드별 라우터나 특정 테스트 ID를 넣지 않았다. 새 슬롯을 포함해 전체 일반 후보 64개 제한, 슬롯별 제한, 샘플러 선택, 강제 pool과 문맥 guard를 유지한다. 이미 관련된 후보는 후속 후보 추가 때문에 밀려나지 않는다.

새 발견은 모두 optional이며 사용자 요구나 hard gate가 되지 않는다. 선택한 visual concept의 완전한 구성 의무만 기존 opt-in 계약으로 승격한다. source-authored 영향 속성은 공개 후보에도 전달하며 부분 잠금을 통과해야 한다. bundle에 연결된 프로필은 별도 선택 없이는 활성화하지 않는다. 세 동결 코어를 이용한 슬롯 노출·예산 검사와 advisory/닫힌 차원/부분 속성/제외·강제 pool 검사를 통과했다.

동결 v2 dictionary SHA-256: `70379562ac6e618750d724a51659049174aec2e4cb95f3226e3bf6a1036f4ed4`. registry SHA-256: `103e10149bcda2a0ba846b215c309d07ed3f0102d49d5b0a25741f5483e6d45c`. [운영 반영 상태](qualification/implementation-ready-v2.json), [v1 소스](qualification/source-snapshot-v1/source-manifest.json), [v2 소스 95개 해시](qualification/source-snapshot-v2/source-manifest.json)를 보존했다. 각 런에서 성공적으로 발행한 pack은 버전별 한 개다.

## 인덱스와 코드 검사

두 Gemini `gemini-embedding-2` 768차원 인덱스를 갱신했다. 기존 호환 벡터를 재사용하고 새 후보 133개·프로필 22개의 검색 문장을 추가했다. semantic index는 9,887개 항목, visual profile index는 1,098개 프로필·2,731개 exact term이다. 원본과 인덱스의 hash 검사가 통과했다. 기존 shard 세대는 보존했다.

- 변경 전 관련 테스트: **44 PASS** ([로그](baseline-focused-tests.log)).
- 최종 데이터·잠금·후보 노출·공존·변조 검사: **14 PASS** ([로그](editing-effects-v2-tests.log)).
- v2 확장 후 기존 후보 의미·촬영·조명·프로필 검색: **44 PASS** ([로그](post-v2-focused-tests.log)).
- v2 요청·구성·scope·attempt 관련 검사: **39 PASS** ([로그](post-v2-contract-tests.log)).
- v1 요청·구성·팩 전달·attempt 계약: **73 PASS** ([로그](post-integration-contract-tests.log)).
- v1 확장 검사: **60 tests, 라우팅 fixture 한 method의 8개 subcase FAIL** ([로그](post-integration-visual-contract-tests.log)). 지정 HEAD와 불변 v1 소스에서 해당 8건의 direct hard/optional 호출 결과가 모두 같았다. hard lane은 기대값을 충족했고 기존 추가 optional 후보 때문에 fixture 기대값이 맞지 않는다. 전체 HEAD suite를 실행한 결과로 확대하지 않았다. [비교 결과](baseline-routing-comparison.json).

## 독립 3개 이미지 테스트

각 에이전트는 새 대화 문맥에서 실제 요청 envelope와 같은 참조 이미지만 전달받았다. 다른 에이전트의 장면·초안·후보 선택·이미지를 보지 않고 무작위 장면을 선택한다. 프롬프트 초안과 core를 먼저 동결하고, 이후 정확히 한 번 후보팩을 만들고, 선택 근거·프롬프트·렌더 요청을 감사한 뒤 실제 이미지를 생성한다.

각 장면은 원래 코어·seed·controls를 유지해 v2에서 재시험했다. 초기 실패를 숨기거나 새로운 코어로 바꿔 성공률을 집계하지 않았다. v2에서는 신규 source candidate/profile의 노출과 실제 선택을 확인하고 모든 선택 성분을 원본 픽셀로 검토했다. seed는 장면·후보 선택의 재현 값이며 builtin 이미지 모델의 샘플링 seed를 통제하지 않는다.

| arm | 독립 무작위 컨셉 | 원래 3개 효과의 v1 엄격 결과 | 최종 v2 원본 픽셀 결과 |
|---|---|---|---|
| A | 비 오는 항구 수선 부스에서 수리된 컵을 고객에게 공개 | 1/3 PASS; grain FAIL·halo PARTIAL→FAIL | **1/3 PASS, 장면 FAIL**. 롤오프 통과. 표면 얼룩·도장 박락은 영상면 입자가 아니며, 전구 대부분이 밝은 벽 앞에 있어 지정한 밝음-어둠 경계 halo 관계 불충족 |
| B | 심야 롤러장에서 반납대로 이동하다 카메라를 바라보는 순간 | 2/3 PASS; 노이즈 분포 PARTIAL→FAIL | **3/3 PASS, 장면 PASS**. 직접 플래시, 선명한 인물에 연결된 짧은 움직임 궤적, 벽과 재킷 암부의 미세 밝기·색 노이즈 동시 충족 |
| C | 공연 후 소품 수선실에서 빨간 문진으로 말린 도면을 펴는 작업 | 1/3 PASS; 무채색·암부 바닥 PARTIAL→FAIL | **1/3 PASS, 장면 FAIL**. 피부 톤·미세 질감 통과. 빨간 문진 외의 따뜻한 색 기운과 깊게 남은 머리·선반 암부 때문에 두 효과 실패 |

v1의 실제 성공 이미지 3장에서는 효과 합산 4/9 PASS, 세 장면 all-of 0/3이었다. 세 장면 모두 손·물체·지지·접촉 등 물리 관계 5개와 참조 외관 범위는 통과했다. C의 첫 builtin 호출은 출력 안전 차단으로 이미지가 없어 평가 제외했으며, 같은 코어·팩의 평범한 작업복·중립적인 표정으로 재시도한 원본이 평가 대상이다. 차단 원문과 두 시도는 각각 보존했다.

최종 v2에서는 선택한 시각 프로필 7개의 필수 성분 **10/14 PASS**(A 0/2, B 6/6, C 4/6), 물리 관계 **15/15 PASS**, 참조 외관 범위 **3/3 PASS**다. 이 성분 검사와 원래 효과 9개는 겹치므로 독립 시행으로 합산하지 않는다. A는 선택한 film bundle의 6성분 중 3개만 통과했으며, 관련 halation·rolloff 프로필은 별도 선택되지 않아 자동 활성화하지 않았다. B는 기술 자격 통과·사용자 판단 대기이고, A/C는 기술 필수 gate 실패다. 모든 이미지의 사용자 수용은 미확인이다.

실제 builtin 이미지 호출은 v1 4회와 v2 3회, 합계 **7회**다. 성공 원본 6장과 평가 제외 안전 차단 1건을 run ID로 중복 없이 기록했다. 성공적으로 발행한 pack은 arm·버전별 하나씩 총 6개다. B의 v2 첫 generator 실행은 snapshot의 semantic shard symlink가 경로 containment 검사를 통과하지 않아 팩·이미지 없이 종료했다. 이후 운영 소스 95개와 shard 해시가 동결 snapshot과 같음을 확인하고 live generator로 단일 팩을 발행했다. 해당 generator 오류는 이미지 호출이나 픽셀 실패가 아니다.

코디네이터도 각 원본을 따로 보고 독립 에이전트의 판정에 동의했다. C의 읽기 전용 RGB 진단은 빨간 문진 밖에서 채널 차이 중위값 7/255를 확인해 따뜻한 색 기운을 뒷받침했다. 이 숫자는 사후 측정 근거이며 새로운 허용 오차나 요청자 잠금이 아니다. 암부의 약 45/255 지침 역시 에이전트가 작성한 표현 가이드로, 별도 숫자 gate로 승격하지 않았다.

[무결성 검증 스크립트](verify_qualification_artifacts.py)는 **169 PASS**다. 동결된 v1/v2 코어·controls·요청 envelope의 바이트 일치, 운영 소스와 snapshot 95개 해시, 실제 선택한 후보, 프롬프트·negative·런타임 전달값, 원본과 보존 사본의 동일 해시, 7개 attempt의 중복 없는 집계를 검사한다. 이 스크립트는 기록을 검증하며 픽셀을 자동 판정하지 않는다. 픽셀 판정은 에이전트와 코디네이터가 원본을 보고 별도로 기록했다.

[실제 요청 envelope](qualification/request-envelope.json)와 [참조 hash](qualification/reference-manifest.json)를 동결했다. 참조는 보이는 성인 얼굴·헤어 외관을 가이드하며 신원·몸 형태·인격 정보를 뜻하지 않는다. 필수 성분의 PARTIAL은 실패, 차단·생성 오류는 attempt로 보존하고 픽셀 점수에는 포함하지 않는다. 프롬프트 감사 통과, 실제 픽셀 충족, 사용자 수용을 별도 상태로 기록한다.

이 3개 조합 이미지는 선택된 효과의 실제 노출과 구현을 검사한다. 133개 후보 전체의 시각 자격, 모든 혼동쌍, 변경 전후 인과 효과 또는 사용자 선호를 검증하는 실험은 아니다.

## 결과를 후속 데이터 검증에 반영하는 계획

검색 공백은 이번 작업에서 해결했다. 다음 표의 네 항목은 렌더 표현에 남은 혼동이며, 실패를 성공으로 바꾸거나 문서·후보 가중치에 성공 빈도로 넣지 않았다. 기존 판정을 유지한 채 새 실험 버전으로 검증한다.

| 우선순위·대상 | 다음 검증 구성 | 데이터 반영 조건 |
|---|---|---|
| P0 영상면 grain / 물체 표면 얼룩 | 매끈한 벽·도색 면·천의 서로 다른 owner에 같은 미세 grain을 요구하고, 도장 박락·직물 조직만 있는 혼동 사례와 비교 | image-plane owner와 재질 분리의 두 성분을 같은 원본에서 모두 확인해야 해당 후보의 픽셀 자격 부여 |
| P0 edge halation / 따뜻한 발광·bloom | 광원의 밝은 윤곽 바로 뒤에 충분한 어두운 면이 보이는 구도를 먼저 고정하고, 넓은 따뜻한 glow와 비발광 금속 테두리를 혼동 사례로 유지 | 적주황 경계 halo와 무관한 어두운 경계의 정상 상태를 모두 확인. 현재 프로필 성분을 약화하지 않음 |
| P0 selective color / sepia desaturation | 색을 유지할 물체 하나와 피부·종이·배경의 무채색 나머지를 명시한 최소 장면에서 검증한 뒤 복잡한 장면에 복귀 | 지정 carrier와 나머지 무채색 영역의 동시 충족. RGB 진단은 보조 근거로 사용하고 사후 관측값으로 합격 기준을 만들지 않음 |
| P1 lifted floor / 깊은 검정 유지 | 머리 뿌리·선반 안쪽 등 최암부 owner를 고정하고, 일반적인 노출 상승·저대비·detail-only와 구분 | 전체의 눈에 보이는 회색 하한과 암부 세부를 모두 요구. 숫자 노출값이나 실제 편집 이력을 추론하지 않음 |

각 항목에 관찰 가능한 긍정 사례 3개와 혼동 경계 사례 3개, 총 24개 독립 원본 판정 사례를 후속 최소 범위로 제안한다. 먼저 단순 장면에서 한 요인씩 바꾸고, 그다음 복잡한 장면에 결합한다. 새로운 코어·팩·프롬프트·attempt를 별도 버전으로 동결하고 원본과 all-of 결과를 보존한다. 현재의 6장을 이 24개 완료 수에 포함하지 않는다.

데이터 추가·검색 가능·픽셀 검증 완료·사용자 수용을 각각 유지보수 원장에 기록한다. 후보 자격은 실제 선택된 ID와 그 적용 owner/문맥에만 붙이며, 한 조합의 결과를 전체 133개나 프리셋 빈도로 확대하지 않는다. [이번 픽셀 자격 유지보수 기록](../extension-maintenance/photo-editing-effects-20261001-v2-qualification.json).
