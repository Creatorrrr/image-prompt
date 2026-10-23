이 문서는 통합시험 시점의 결과다. 공용 runtime 선택은 이후 다른 작업으로 바뀔 수 있으며, 이번 Git 발행은 현재 runtime 선택을 변경하지 않는다.

# 군대물 데이터 반영과 독립 이미지 검증

2026-10-24 KST. 군대물 시각 카드 104개를 운영 후보와 연결했다. 신규 시각 후보는 103개이며 기존 완결 후보 1개를 재사용했다. 독립된 세 이미지에서는 군대물 맥락이 모두 읽혔고, 미리 정한 전체 장면 기준을 완전히 충족한 이미지는 0개였다. 새 군대물 후보의 최종 프롬프트 사용도 0개여서 이번 데이터의 이미지 개선 효과는 확인되지 않았다.

## 반영한 데이터

| 항목 | 반영 범위 |
|---|---|
| 시각 의미 레지스트리 | 원문 용어 393행의 검토용 연결, 시각 카드 104개, 소유자·연결 관계·관찰 조건·혼동 경계 |
| 신규 시각 후보 | 완결된 한국어·영어 선택지 103개 |
| 검색 양성 집합에서 제외한 진단 | 문맥 구분 52개와 보류 주제 18개, 합계 70개 |
| 신규 선택적 binding | 203개 |
| 기존 후보 재사용 | V20 트렌치코트의 완결 출처 1개 |
| 기존 후보 수정 | 경례 한국어의 손·팔 관계 보완, aircraft flight deck의 조종실 번역·별칭 구분 2개 |

레지스트리는 계급·임무·동의·진단·법적 상태 같은 문맥과 복장·장비·몸의 가시적 상태를 구분한다. 장비의 소유자, 끈·케이블의 양 끝, 지지 표면, 착용·분리 상태, 그림·화면과 실물의 경계를 후보 전체 원문에 보존했다. 연구 그래프는 검토용 메타데이터이며, 개별 후보의 조건·효과·출처와 별도로 유지한다. 신규 출처에 native approval을 부여하지 않았다.

운영 파일은 [시각 의미 레지스트리](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_military_fiction_semantics_20261024.json), [후보 모듈](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_military_fiction_20261024.json), [binding 모듈](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_military_fiction_bindings_20261024.json), [의미 검토 지침](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/military-fiction-semantics.md)이다. corpus manifest와 유지보수·설치 문서에 진입점을 등록했다.

[원본 대조](./integration-evidence/final-source-validation.json)는 검토한 신규 173개·기존 수정 2개와의 일치를 확인했다. 작업 시작 당시의 다른 후보 21,881개와 binding 16,698개, slot catalog·정책도 보존됐다. 다른 작업의 추가 데이터는 이번 반영 건수에 합산하지 않았다. 기존 후보 수정에서도 원래의 조건·효과·출처를 유지했다.

## 설치와 검색 검증

테스트용 설치본은 전체 배포 검증과 기록 도구 의존성 검사를 통과했다. 세 실행은 공식 `--runtime-store`·`--generation-id` 옵션으로 같은 설치본에 고정됐다. 설치본은 자체 코드·후보·색인·벡터를 보유하며 연구 폴더를 읽지 않는다.

| 대상 | 상태와 범위 |
|---|---|
| 테스트용 H-F2 | `b89c136eaf8d05128cc10f5d4c01cbfe313a73aad7ecdedae9fc983177b6760a` |
| 테스트용 native | `64d0831bea3f21d4a2ab0e9b8b6a8a11718c34332aca0ea69b6a1943056785a8` |
| 테스트용 설치 검증 | PASS, 양성 CID 20,726개·RID 20,728개, CURRENT 쓰기 0 |
| 공용 기본 H-F2 | `3cc98eb359d1faf61ff99c75d7370cb03615dd6a019407c88c6935e767a900f9` · 배포·선택 완료 |
| 공용 기본 native | `19c79b683df6c234b05941b137dd968ff07f9fb389872fa790b3577c2a9ef5ce` |
| 공용 기본 설치 검증 | PASS, 양성 CID 21,031개·RID 21,033개, CURRENT 쓰기 0, 환경·기록 도구 PASS |
| 기존 집중 테스트 | 48개 PASS, 실패·오류·skip 0 |

작업 중 공용 기본 검색본이 여러 차례 갱신됐다. 각 설치 검사에서 기준 변경을 확인해 이전 병합본의 선택을 중단하고 최신 설치본에 군대물 변경만 다시 합쳤다. 실행 코드는 검증된 설치 커널을 유지했다. 최신 스킬 본문 SHA-256은 `f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089`이다.

최종 기본 설치본은 직전 설치본의 후보 22,087개 중 수정 대상 2개를 제외한 22,085개와 기존 binding·catalog·정책을 그대로 보존하고 신규 173개를 추가했다. 총 후보는 22,260개다. 검증된 벡터와 원래 실행 증거를 재사용했으며 실행 커널과 모든 배포 검증을 유지했다. [기본 설치 결과](./integration-evidence/rebase-selected/install-active.json), [설치 원본 보존 검사](./integration-evidence/rebase-selected/canonical-source-validation.json), [기본 환경 검사](./integration-evidence/runtime-check-default.json)에 최종 선택과 범위가 기록됐다.

최종 기본 설치본에서는 기존 개발 질의 6개를 재사용해 별도 동작 검사를 했다. 시각 카드 4개의 지정 후보가 모두 1위였고, 일반 장면 2개에는 새 군대물 후보가 상위 10위에 없었다. 전체 양성 CID 21,031개를 검색했고 추가 embedding 호출은 0회였다. 이 [6개 동작 검사](./integration-evidence/runtime-smoke.json)는 아래 262개 평가의 반복이나 새 holdout 결과가 아니다.

raw working native 색인은 여러 원본 변경으로 `source/space mismatch` 상태였으며 그 검사를 통과로 처리하지 않았다. 실제 테스트에는 별도로 완성·검증한 sealed 설치본을 사용했다. [설치 결과](./integration-evidence/install.json), [기록 도구 검사](./integration-evidence/runtime-check-pinned.json), [48개 테스트 결과](./integration-evidence/focused-tests.json)에 범위가 구분돼 있다.

같은 테스트 설치본에서 전체 양성 공용 집합을 대상으로 262개 개발 질의를 실행했다. 각 질의는 같은 문장으로 BM25F 1회와 로컬 cosine 1회를 실행했고, 주제별 사전 필터를 사용하지 않았다.

| 질의 종류 | 수 | 결과 |
|---|---:|---|
| 카드 원문 한국어·영어 | 208 | 지정 후보 상위 8위 208개 |
| 작성한 자연어 개발 질의 | 48 | 지정 후보 상위 8위 46개 |
| 일반 장면 대조 질의 | 6 | 새 군대물 후보 상위 10위 노출 0개 |

군대물 목표 질의 전체로는 254/256개가 상위 8위에 들었다. 두 미달 질의는 “두 사람 중 한 사람만 오른손 경례”의 한국어·영어 표현이며 지정 V49 후보는 각각 60위·129위였다. 진단 70개는 양성 집합에서 제외됐다. 이 질의들은 작성한 개발용 사례이며 독립 holdout이나 전후 비교가 아니다. 순위는 실제 관리 검색의 표본 노출·후보 적합성·최종 사용·이미지 실현을 대신하지 않는다. [질의별 결과](./integration-evidence/retrieval-qualification.json)에 정확한 순위와 설치 세대를 기록했다.

## 독립된 세 이미지 테스트

세 서브에이전트는 서로의 대화 이력을 받지 않고 시작했다. 각자 주제에 맞는 후보 콘셉트를 비교해 seed로 선정하고, 후보 접근 전에 콘셉트·테스트 기준·기본 프롬프트·core를 확정했다. 구체적 장면 선택은 작성자 소유로 기록했으며 요청자 제약으로 바꾸지 않았다. 실제 사용자 요청과 앞선 사용자 문구 “군대물”을 연결한 공통 topic context를 사용했다.

첨부 사진은 직접 관찰한 얼굴·머리 외형에 사용했다. 참고 파일 SHA-256은 `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`이다. 실제 신원·나이·군 경력은 판단 범위에 포함하지 않았다. 세 실행은 같은 최신 스킬을 읽었고, 각자 전체 후보 원문과 모든 질의별 occurrence를 검토한 후 대안과 기본안을 비교했다.

| 실행과 seed | 독립 콘셉트 | 검토 occurrence / 고유 출처 | 새 군대물 출처 노출 / 최종 사용 |
|---|---|---:|---:|
| A · `2526402208739747887` | 정렬 직전 동료의 금색 의전 견장끈 정돈 | 24 / 24 | 0 / 0 |
| B · `2026102402` | 새벽 항공기 바퀴 쐐기 점검과 동료의 인수 기록 | 24 / 23 | 2 / 0 |
| C · `202610240303` | 출발 전 쉘터에서 야전 무전기 배터리 교체 | 40 / 33 | 0 / 0 |

B에 노출된 신규 출처는 V75 격납고의 열린 동선과 V83 노즈아트 경계다. 전체 출처의 장소·행위·표현 경계를 비교한 뒤 최종 사용하지 않았다. A와 B의 최종 프롬프트는 독립 기본안과 동일하다. C는 기존 일반 재질 후보의 손잡이 국소 마모만 작성자 표현에 참고했으며 새 군대물 후보의 사용은 없었다. 세 실행 모두 native chosen 목록은 비어 있다. [프롬프트 사용 대조](./integration-evidence/material-use-audit.json)는 신규 CID 집합과 실제 반환·사용 CID의 교집합 및 정확한 프롬프트 해시를 확인한다.

각 실행은 compose·runtime 검사를 통과한 정확한 요청과 첨부 사진으로 built-in `image_gen`을 1회 호출했다. 총 3회 모두 이미지를 반환했고, 저장 이미지와 프롬프트·참고 사진의 연결을 기록했다. 추가 이미지 호출이나 API·CLI fallback은 사용하지 않았다. prompt 사전 검사에는 작성자 원문으로 보존한 의미에 대한 `uncovered_intent` 경고가 A/B/C 각각 5/5/6개 있었으며, 이미지 픽셀 판정은 별도로 수행했다.

| 이미지 | 직접 확인한 주제·행위 | 미리 정한 기준에서 부족한 점 | 전체 장면 |
|---|---|---|---|
| [A 의전 정돈](/Users/chasoik/Projects/image-prompt/generated/photo-runs/military-20261024-a/image.png) | 의전복·대기 대형·동료 끈 정리·참고 얼굴/단발 | 오른손 집기가 견장 옆에서 가슴 쪽 매듭으로 이동. 구도도 기본안의 knee-up보다 좁음 | 부분 충족, strict FAIL |
| [B 항공 정비](/Users/chasoik/Projects/image-prompt/generated/photo-runs/military-20261024-b/military-b-dawn-maintenance.png) | 수송기·정비복·손–쐐기–타이어 접점·연필–종이 접점·참고 외형 | 함께 보여야 할 바퀴 전체가 왼쪽 경계에서 잘림 | 부분 충족, strict FAIL |
| [C 무전기 교체](/Users/chasoik/Projects/image-prompt/generated/photo-runs/military-20261024-c/image.png) | 군복·쉘터·무전기 정비·분리 배터리·출발 장비 | 왼손 바닥 지지가 벤치 지지로 변경. 정확한 반 삽입·뒤 레일 접점과 눈/얼굴 비교는 부분 관찰 | 부분 충족, strict FAIL |

각 서브에이전트의 저장 픽셀 검토 후 주 에이전트도 원래 해상도의 세 저장본을 직접 확인했다. 군대물 맥락은 3/3, 전체 strict 통과는 0/3이다. 관리 도구의 일반 embodiment 기술 gate는 B가 5/5 통과했고 A/C는 실패했다. B의 바퀴 전체 가시성은 별도의 사전 testcase에서 미충족이므로 전체 장면 통과로 올리지 않았다. 이 결과는 신체 기형을 진단하는 판정이 아니라 정해 둔 지지·접촉·가시성 관계의 충족 여부다. 신규 후보 최종 사용이 0/3이므로 새 데이터의 픽셀 효과는 미확립이다. 비교용 기본 이미지와 사용자 수용 판단도 없다. [주 에이전트의 픽셀 기록](./integration-evidence/parent-pixel-review.json)에 관찰 항목과 이미지 해시가 있다. [세 실행의 바이트 연결 대조](./integration-evidence/three-arm-binding-audit.json)는 동결 testcase·core·최신 스킬·프롬프트·참고 사진·저장 이미지와 세 review record의 구조 검증을 확인한다.

세부 보고서와 정확한 프롬프트는 [A 보고서](image-test-evidence/a/RESULTS.md)·[A 프롬프트](image-test-evidence/a/final-prompt.txt), [B 보고서](image-test-evidence/b/RESULTS.md)·[B 프롬프트](image-test-evidence/b/prompt_en.txt), [C 보고서](image-test-evidence/c/RESULTS.md)·[C 프롬프트](image-test-evidence/c/final-prompt.txt)에 보존했다.

## 후속 검증 계획

1. 이번 세 장면과 판정 기준을 회귀 사례로 보존한다. 보완 이후의 일반화 판단에는 새로 확정한 독립 holdout을 사용한다.
2. 새 출처 노출이 A/C 0개인 원인을 질의 목적·순위 창·표본·전체 출처 적합성으로 나눠 분석한다. 경례 개발 질의 두 건도 함께 검토한다. 개별 실패 사례를 그대로 별칭에 넣어 결과를 강제하지 않는다.
3. 새 출처와 독립 core가 완전히 양립하는 경우에 한해 기본안과 출처를 참고한 완결 대안을 같은 참고 사진·controls로 비교 생성한다. 후보 선택과 native qualification은 별도로 검토하고, 전후 픽셀 차이가 있을 때만 데이터 효과를 판단한다.
4. 의전의 높은 집기 위치, 바퀴 전체의 화면 여유, 무전기를 받치는 왼손과 삽입 레일을 한 뷰에서 읽을 수 있도록 작성자 구도를 보완한다. 동일 기준의 재검사와 새 독립 장면 검사를 구분한다.

이번 요청의 원본 데이터·설치·독립 세 생성 테스트 결과를 보존했다. 통합시험 종료 시에는 commit·push를 수행하지 않았다. 후속 발행 검증은 [PUBLISHING.md](PUBLISHING.md)에 기록한다. 최초 연구와 40개 근거 출처의 범위는 [RESEARCH.md](./RESEARCH.md), 반영 전 계획은 [IMPLEMENTATION-PLAN.md](./IMPLEMENTATION-PLAN.md)에 있다.
