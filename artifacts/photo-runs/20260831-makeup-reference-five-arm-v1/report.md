# 첨부 메이크업 시각 의미 데이터화 및 5-arm 픽셀 검증

## 결과 요약

첨부 이미지는 신원 소스가 아니라 메이크업의 배치·색 분포·표면 마감만을 위한 참조로 사용했다. 이를 `restrained_polished_natural_makeup_balance`라는 8요소 시각 의무 프로필과 `restrained_polished_natural_makeup_closeup` 후보 프리셋으로 일반화했다.

- 실제 이미지 저장: 5/5
- built-in 이미지 호출: arm당 1회, 총 5회, 재시도 0회
- 합성 프롬프트 감사: 5/5 PASS
- 런타임 입력 감사: 5/5 PASS
- 메이크업 프로필 기술 PASS: 4/5 arm, 개별 게이트 39/40
- 복합 콘셉트 게이트까지 포함한 엄격 PASS: 3/5 arm
- 사용자 선호/수용 판단: 5/5 pending

개별 게이트를 평균으로 상쇄하지 않았다. B의 치크 게이트 하나가 실패했으므로 B의 메이크업 기술 판정은 FAIL이며, E는 메이크업 8/8이지만 별도 복합 장면 게이트가 실패해 엄격 종합 FAIL이다.

## 데이터 반영

### 시각 의미 프로필

`restrained_polished_natural_makeup_balance`는 다음 요소가 같은 얼굴에서 동시에 보여야 한다.

1. 피부 결과 자연 색 변화가 남는 시어-라이트 새틴 보정
2. 개별 털이 남는 낮은 아치 눈썹
3. 위 속눈썹선에서 가장 진하고 크리즈로 퍼지는 뉴트럴 타우프
4. 아주 짧은 바깥 테이퍼로 끝나는 얇은 인터래시 라인
5. 절제된 볼륨의 분리된 속눈썹
6. 환경광과 구분되는 저채도 양측 로즈 치크
7. 안쪽 중심이 진하고 부드러운 경계·낮은 새틴 광택을 가진 로지 코랄 립
8. 눈·볼·입술이 서로 절제되어 피부가 위계를 주도하는 전체 균형

런타임 모드는 `definition_only`다. 좁은 활성 라벨은 검색에만 쓰고 최종 프롬프트에는 구성요소 문장만 남긴다. bare face, opaque glam, 디지털 스무딩, 환경 색조, 단일 강조 부위를 대체물로 거부한다.

### 후보팩

사전 프리셋은 기존 독립 슬롯의 좁은 조합으로 구성했다: 시어/라이트 커버리지, 로우 아치 브로, 모노크롬 디퓨즈드 아이 워시, 인터래시 타이트라인, 분리 속눈썹, 뮤트 치크, 중심 그라데이션 립, 새틴/밤 립 마감, fresh wear state. 특정 인물·인종·건강·매력 규범은 인코딩하지 않았다.

최종 인덱스는 visual profile 82개/483 exact term, semantic entry 6,910개다.

## 독립 테스트 결과

| Arm | 랜덤 복합 콘셉트 | 메이크업 | 장면 | 엄격 종합 | 실패 경계 |
|---|---|---:|---:|---:|---|
| A | 궤도 식물 검역관 + 서리 씨앗 캡슐 검사 | 8/8 PASS | PASS | PASS | 없음 |
| B | 사막 태양 관측소 복원가 + 균열 헬리오스타트 정렬 | 7/8 FAIL | PASS | FAIL | 로즈 치크와 앰버 반사광을 분리할 수 없음 |
| C | 침수 도서관 보존가 + 젖은 성도 건조 프레임 | 8/8 PASS | PASS | PASS | 없음 |
| D | 야간 수분 기록가 + 생물발광 나방 가루 표본 | 8/8 PASS | PASS | PASS | 없음 |
| E | 지하 세라믹 음향 연구자 + 공명 타일 매핑 | 8/8 PASS | FAIL | FAIL | 분필 진동 표시가 줄눈/스크래치와 구분되지 않음 |

### 산출물

- A: `arms/arm-a/result.png`, `arms/arm-a/composed_prompt.json`, `arms/arm-a/pixel_review.json`
- B: `arms/arm-b/result.png`, `arms/arm-b/composed_prompt.json`, `arms/arm-b/pixel_review.json`
- C: `arms/arm-c/result.png`, `arms/arm-c/composed_prompt.json`, `arms/arm-c/pixel_review.json`
- D: `arms/arm-d/result.png`, `arms/arm-d/composed_prompt.json`, `arms/arm-d/pixel_review.json`
- E: `arms/arm-e/result.png`, `arms/arm-e/composed_prompt.json`, `arms/arm-e/pixel_review.json`

각 arm에는 v6 candidate pack, composed/runtime audit, 단일 ledger row, v2 independent manifest, 결과 해시, 사용자 판단 pending 상태가 함께 보존돼 있다.

## 사전 계약 결함과 수정

최초 profile revision에서 짧은 고정 바인딩 두 개의 형식적 내용어 하한이 실제 문구보다 1단어씩 높았다. 이미지 호출 전에 fail-closed 되었고, `lash_phrase` 하한 5→4, `cheek_phrase` 7→6만 수정했다. 의미·프롬프트·픽셀 게이트는 바꾸지 않았다. 각 최초 pack은 `candidate_pack.preflight-invalid.json`으로 보존했으며 렌더에는 사용하지 않았다.

## 검증과 해석 경계

- dictionary validation PASS
- visual-profile index check PASS: 82 profiles, 483 exact terms
- 최종 메이크업 집중 테스트 22/22 PASS
- visual-obligation/retrieval/authorial-core 관련 회귀 53/53 PASS
- 모든 결과는 로컬 workspace에 저장되고 SHA-256으로 원장과 연결됨

이 결과는 프롬프트/런타임 계약과 5개 단일 샘플의 픽셀 결과를 증명한다. 반복 생성 안정성, 모든 조명에서의 일반화, 신원 일치, 또는 사용자의 미적 선호를 증명하지 않는다. 특히 B는 저채도 치크가 유사색 환경광에 취약하다는 실제 혼동 경계를 드러냈다. 따라서 현재 상태는 구현 완료이지만 render-fidelity 보편 승격은 보류하고 `revise`로 기록한다.
