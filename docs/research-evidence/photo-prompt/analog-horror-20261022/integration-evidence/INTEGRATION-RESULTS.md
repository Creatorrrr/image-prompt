# 아날로그 호러 데이터 반영 및 독립 이미지 테스트 결과

시각 의미 카드 78개와 키워드 경로 200개를 반영하고, 시각 후보 71개·진단 항목 13개·역할 binding 126개를 추가했다. 기존 시각 후보 1개는 전체 의미를 보존해 재사용했으며, 근거가 부족한 6개 카드는 시각 후보 등록을 보류했다. 새 데이터는 설치된 기본 실행 버전에서 사용할 수 있다.

서로 다른 컨셉을 고정한 독립 서브에이전트 3개가 원본 초상 파일을 실제 이미지 입력으로 전달하여 각각 1회 생성했다. 실제 픽셀의 주제 조건은 2개 케이스가 통과했고, 신체·접촉 조건까지 포함한 전체 케이스는 **1개 통과·2개 실패**다. 실패를 통과로 바꾸거나 재생성하지 않았다. 사용자 수락은 pending이다.

## 데이터와 실행 버전

| 반영 항목 | 결과 |
|---|---:|
| 의미 카드 / 키워드 경로 | 78 / 200 |
| 새 시각 후보 / 진단 항목 | 71 / 13 |
| 기존 시각 후보 재사용 | 1 |
| 새 역할 binding | 126 |
| 시각 후보 등록 보류 | 6 |
| 이전 기본 버전의 전체 후보 보존 | 19,958 |
| 이전 후보 레코드 수정 | 0 |

카드에는 가시 성분, 성분의 소유자, 방향 관계, 혼동 경계, 출처·접근 범위, 한 장에서 증명할 수 없는 주장, 실제 이미지 판정 기준이 들어 있다. 기록 매체·표시 화면·방 안의 물체·기관 문서의 층을 분리했다. 장르명만으로 모든 후보를 활성화하지 않으며, 진단 항목 13개는 positive 검색 인덱스에서 제외했다. 출처와 연구 그래프는 native 자격이나 숨은 사실의 증거가 아니다.

보류한 카드는 소형 카세트/어댑터(A002), 컬러바 표준 패턴(A012), 텔레텍스트 격자(A015), 얼굴 유사 배열(A058), 애니매트로닉 기구(A061), 모스 부호 대응(A076)이다. 기존 후보를 재사용한 A064의 source 의미·조건·효과는 변경하지 않았다.

- [시각 의미 레지스트리](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_analog_horror_semantics_20261022.json)
- [시각 후보와 진단 데이터](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_analog_horror_20261022.json)
- [역할 binding](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_analog_horror_bindings_20261022.json)
- [기본 실행 버전 설정](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/retrieval-runtime.json)

이미지 테스트는 새 데이터를 먼저 설치한 고정 버전 `d5aec2788e925fb6e8b27831b0055a2545067372edf87a6d5c7ea233a716ebfa`에서 진행했다. 이후 동시 작업이 추가한 후보를 보존하여 기본 버전을 `489c99a5cbd447eeb0da1ecdfbda407d06d7687ae868e860f95c06447d2799bf`로 갱신했다. 두 버전의 실행 코드 closure는 같고, 이번 84개 레코드의 native snapshot은 작업 데이터와 정확히 일치한다. 최신 canonical SKILL의 해시도 준비 시점과 같다. 기존 정책과 임베딩 공간을 보존했고 CURRENT 파일에는 쓰지 않았다.

원본 연구 파일 34개의 해시를 보존했다. 작업트리 전체의 기존 dictionary/index 검사는 동시 작업의 source/space 불일치로 실패했으며 이를 되돌리지 않았다. 이번에 설치한 봉인 버전은 별도로 source/index·배포 검증을 통과했다. 커밋·푸시는 하지 않았다.

## 검색 및 구조 검증

최신 설치 버전에 한영 질의 160개를 전체 positive pool 19,622개에 실행했다. 긍정 질의 48개 중 등록 대상 44개를 평가했고, 보류 카드를 대상으로 한 4개 질의는 성공률 분모에서 제외했다. 44개 중 43개에서 기대 source가 상위 10개에 나왔다. A064의 한국어 질의는 42위여서 약점으로 남겼다.

경계·일반·비가시 대조 질의 112개 중 54개에서도 새 후보가 상위 10개에 노출됐다. 부정된 tracking, 일반 풍경에 대한 실종 공고, EXIT 표지만으로 막힌 출구를 들이는 사례 등은 저술 검토에서 거절해야 한다. 이 수치는 대조 사례의 의미 선택 통과율이 아니다. 순위·노출이 자동 채택이나 native 자격을 부여하지 않는다.

로컬 모델이 생성한 동일 질의 벡터를 보존해 각 추가 반영 버전에서 전체 순위를 다시 실행했다. 평가 질의는 연구에서 파생한 개발 자료이며 독립 holdout이 아니다. 이전 버전에서 새 CID가 없었다는 사실로 검색 개선량을 계산하지 않았다. 최신 주제 연결/부정 정책 검사 13개와 각 설치본의 배포 검증도 통과했다.

- [최종 검색 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/analog-horror-20261022/integration-evidence/maintenance/rebase-current/retrieval-qualification.json)
- [검색 한계 검토](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/analog-horror-20261022/integration-evidence/maintenance/rebase-current/retrieval-review.json)
- [최종 데이터 및 전달 증거 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/analog-horror-20261022/integration-evidence/FINAL-VALIDATION.json)

## 세 독립 이미지 테스트

각 서브에이전트는 다른 arm의 입력을 보지 않고 로컬 난수로 세부 컨셉을 선택했다. 후보 접근 전에 컨셉·기준 프롬프트·코어·신체 검토·주제 픽셀 조건을 고정했다. 공통 원본 초상은 얼굴·머리 모양의 외형 안내로 사용했다. 저장된 제어값은 sensual 1 / fetish 0 / creativity 1 / surreal 0을 유지했다.

| 컨셉 | 신규 자료 노출과 반영 | 주제 조건 | 신체·접촉 조건 | 전체 케이스 |
|---|---|---|---|---|
| 빈 의자에 앉아 있는 녹화 속 얼굴 | A038·A049 노출. A038 거절, A049의 일반 베젤 경계만 독립 구도에 보강 | 7/7 통과 | 5/5 통과 | **통과** |
| 냉동창고 입고대장의 사람 모양 화물 | A001 노출. 두 릴 창과 등 라벨이 보이도록 VHS 외형을 보강 | 5/5 통과 | 4/5 통과 | **실패** |
| 끝나지 않는 방송 종료 멘트 | 이번 시각 source 노출 0. 독립 baseline 유지 | 4/5 통과 | 5/5 통과 | **실패** |

첫 케이스에서는 CRT 속 점유된 의자와 실제 빈 의자, 공통 대각선 수선 자국, 화면 한정 잡음, 빈 의자로 향한 시선이 함께 보인다. 화면 인물의 낯선 정체나 실제 녹화 이력은 입증하지 않는다.

두 번째 케이스에서는 종이의 `23 / CRATE`와 화면 속 사람 모양 포장물의 `23`을 읽어 모순을 비교할 수 있다. 새 A001의 구조·라벨 조건 3개도 보인다. 그러나 검지가 23번 행 위쪽을 가리키고 펜촉이 별도 빈 영역에 닿아, 같은 행을 가리키며 그 위에서 멈춘다는 사전 접촉 조건이 실패했다.

세 번째 케이스에서는 CRT, 방송 부스, ON AIR/GOOD NIGHT, 서로 다른 입 모양이 보인다. 현실 인물의 입도 약간 벌어져 있으므로, 사전에 정한 닫힌 입 대 크게 열린 입 조건은 부분 충족이다. 전체 케이스는 실패이며, 새 데이터가 프롬프트를 개선했다고 주장할 수도 없다.

세 케이스 모두 managed review 기록은 유효하다. 두 번째의 신체 technical qualification은 fail이고, 세 번째는 신체 검토가 통과해도 별도 주제 조건에서 실패한다. 기록 유효성과 이미지 성공은 다른 판정이다. `partial_is_fail`과 `UNOBSERVABLE_NOT_PASS`를 유지했다. native source 전체 채택은 모두 비어 있고, 이 테스트로 전체 데이터의 native 자격을 승인하지 않았다. 비교용 baseline 이미지가 없어 전후 개선이나 선호도는 판정하지 않았다.

| 케이스 | 프롬프트 | 생성 이미지 | 상세 결과 |
|---|---|---|---|
| 1 | [프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/analog-horror-20261022-arm1/final-prompt.txt) | [이미지](/Users/chasoik/Projects/image-prompt/generated/photo-runs/analog-horror-20261022-arm1/generated-image.png) | [보고서](/Users/chasoik/Projects/image-prompt/generated/photo-runs/analog-horror-20261022-arm1/result-report.md) |
| 2 | [프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/analog-horror-20261022-arm2/final_prompt_en.txt) | [이미지](/Users/chasoik/Projects/image-prompt/generated/photo-runs/analog-horror-20261022-arm2/generated_image.png) | [결과 및 증거](/Users/chasoik/Projects/image-prompt/generated/photo-runs/analog-horror-20261022-arm2/arm-result.json) |
| 3 | [프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/analog-horror-20261022-arm3/final_prompt.txt) | [이미지](/Users/chasoik/Projects/image-prompt/generated/photo-runs/analog-horror-20261022-arm3/generated_image.png) | [보고서](/Users/chasoik/Projects/image-prompt/generated/photo-runs/analog-horror-20261022-arm3/arm3-report.md) |

[별도 coordinator 픽셀 검토](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/analog-horror-20261022/integration-evidence/coordinator-pixel-review.json)는 각 원본 이미지 SHA와 관찰을 보존한다. 세 arm의 모든 bound artifact 해시, 원본 참조 경로·해시, 정확한 프롬프트, 1회 operation/attempt, 1행 ledger, PNG 무결성도 확인했다. 실제 사용한 이미지 모델의 식별자는 도구에서 제공되지 않았다.

## 다음 보강 순서

1. 접촉 실패는 입고대장의 23번 행과 손가락·펜 사이 공간을 단순화한 scoped retry로 확인한다. 새 감사와 한 장의 실제 결과가 필요하며 이번 결과를 통과로 재분류하지 않는다.
2. 방송 부스는 닫힌 입의 가시 조건을 더 분명하게 저술한 scoped retry가 필요하다. 새 데이터 미노출은 별도의 역할·자연어 질의 coverage 문제로 조사하며 CID 강제 주입이나 장르 태그 일괄 증폭으로 해결하지 않는다.
3. A064의 한국어 검색 약점은 기존 완전 의미와 한영 표현의 충실도를 검토하고, 이번 평가 문구와 다른 holdout 질의로 재확인한다. 대조 노출은 실제 저술 결정의 거절 여부까지 확인한다.
4. 보류 6개는 세부 외형·표준·코드의 1차 자료와 픽셀 기준을 확보한 뒤 따로 등록한다. 나머지 카드도 실제 장면별 검증 전에는 native 자격이나 사용자 수락을 부여하지 않는다.
