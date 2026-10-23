# 궁중물 데이터 반영·독립 이미지 테스트

2026-10-23 실행 완료. 데이터 반영·설치·한영 질의 272개·독립 참조 이미지 생성 3회를 수행했다. 신규 source의 완전한 시각 관계는 1/3, generic 신체 gate는 1/3이 통과했고 두 기준을 함께 충족한 arm은 0/3이다. 생성 성공과 엄격한 의미 충족을 분리한 결과다.

## 반영한 데이터

| 대상 | 실제 반영 |
| --- | --- |
| 시각 의미 | 카드 88개, 원문 항목 경로 623개, 출처 40개를 operational sidecar로 보존 |
| 새 후보 | 완전한 한영 시각 대안 33개; 고증 보류 40개와 비가시 문맥 15개는 positive 검색에서 제외하는 진단 55개 |
| 역할 연결 | 시각 대안에 선택적 binding 72개 추가 |
| 기존 후보 | 당의 3개 CID의 한영 대응, 빈 왕좌 1개 CID의 검색 의미를 보정 |
| 보존 | 기존 조건·효과·provenance·다른 후보·기존 binding·149개 catalog·policy 보존 |

새 시각 대안은 당의 자락·옆트임·거들지, 조포의 분리된 옷 부위, 겹옷, 유럽 치마 지지 구조, 손과 부채·옷자락·상자의 관계, 문턱 전후 인물 배치 등을 다룬다. 각 카드에 보이는 구성 요소, 관계의 양 끝과 연결, 혼동 경계, 관찰 gate, 출처 범위를 기록했다. 직함·혈통·승계권·의도·동의·사건 원인 같은 비가시 의미를 외형으로 확정하지 않는다.

파일:

- [시각 의미 sidecar](../../../../skills/photo-prompt-image-generator/assets/photo_court_palace_semantics_20261023.json)
- [후보 88개](../../../../skills/photo-prompt-image-generator/assets/photo_candidate_court_palace_20261023.json)
- [선택적 binding 72개](../../../../skills/photo-prompt-image-generator/assets/photo_candidate_court_palace_bindings_20261023.json)
- [카드→실제 CID·역할·반영 상태](integration-evidence/data-integration.json)
- [기존 4개 CID의 수정 전후](integration-evidence/existing-source-patches.json)
- [실행용 의미 경계 안내](../../../../skills/photo-prompt-image-generator/references/court-palace-semantics.md)

33개는 선택 가능한 source 등록이다. 연구 메타데이터나 선택적 binding을 native typed-fact 승인으로 취급하지 않는다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`을 유지한다.

## 데이터·런타임 검증

[데이터 검증 15개](integration-evidence/VALIDATION.json)가 통과했다. [원본 index 검증](integration-evidence/raw-dictionary-validation.json)은 이 작업의 빌드 시점 후보 20,959개·binding 15,911개에서 오류가 없었다. 이후 공유 폴더에 별도 espionage 데이터가 추가됐다. 그 추가분을 보존했으며 이 작업이 그 데이터의 현재 raw index 상태까지 검증했다고 주장하지 않는다.

실제 테스트와 설치는 검증된 이전 canonical source 20,694개에 이번 후보 88개와 기존 4개 보정만 더한 20,782개 source를 사용한다. 기존에 raw에만 있던 다른 주제 데이터와 이후 동시 작업을 임의로 설치하지 않는다. source kernel·policy·embedding space는 보존하고 source에서 index를 다시 만들었다. 기존 H-F2 문서 벡터 20,122개를 동일하게 재사용하고 변경·신규 문서 37개의 벡터를 계산했다.

- H-F2 generation: `5bb0e4da6498ef7d0f2727421c0b032338293f69b4a5dfb6b893db8f599f11aa`
- native generation: `6d15d4026ce11757a9697a10cb907f9fc9238ae8cf258213738823c3c07833d9`
- 검색 대상: positive CID 20,157개, RID 20,159개
- [canonical source 보존 검사](integration-evidence/maintenance/canonical-source-validation.json)
- [sealed 빌드 기록](integration-evidence/maintenance/successor.json)
- [독립 설치와 deployed 전체 validator 결과](integration-evidence/maintenance/install.json)

[기본 포인터 활성화](integration-evidence/maintenance/install-active.json)도 통과했다. 활성화 후 다른 동시 작업이 궁중물+espionage 통합 successor를 설치했다. 최종 기본 generation은 `587f77950e648994525a9066e8757e9fbaa55b38c3d9312f0b5ef517fdaece28`, native는 `489839d65a789793d41a60e11d83965132f2030d23f69032ff35e7d8a5ab51f4`다. [최종 기본 버전 보존 검사](integration-evidence/maintenance/active-successor-preservation.json)에서 이번 88개 source·72개 binding·4개 보정 모듈의 byte hash가 테스트 버전과 일치함을 확인했다. 새 positive 33개가 모두 검색 index에 있고 diagnostic 55개는 제외된다. 이 통합 pointer를 되돌리지 않았다. 테스트 receipt는 원래의 검증된 generation에 계속 고정되어 있다. native `CURRENT`는 이 작업이 변경하지 않았다. 설치 검증은 이미지 의미 충족이나 사용자 수용을 증명하지 않는다.

## 실제 검색 확인

[272개 한영 질의의 실행 기록](integration-evidence/maintenance/retrieval-qualification.json)을 남겼다. 개발 질의 146개, 비가시 문맥 경계 30개, 혼동 대비 질의 96개다. 새 positive 후보 33개에 대응하는 개발 질의 66개는 모두 해당 CID를 상위 10개에서 찾았다. 고증 보류 후보를 위한 개발 질의 80개는 positive 정답 후보를 등록하지 않은 상태로 구분했다. 진단 55개가 positive index에 들어가지 않았다는 [설치 index 멤버십 검사](integration-evidence/maintenance/positive-membership-validation.json)도 통과했다.

혼동 대비 96개는 이전 generation과도 비교했다. 상위 10개 집합의 평균 공통 항목은 9.4375개였고, 새 후보가 상위 10개에 등장한 질의는 45개다. 유사한 시각 대안이 검색되는 것 자체를 오답이나 채택으로 계산하지 않는다. 이 검사는 출처에서 만든 개발/경계 질의이며 독립 holdout, 모든 후보의 고증 승인, native 의미 승인 또는 이미지 개선의 인과 증명이 아니다.

## 독립 테스트 방법

coordinator가 실제 사용자 원문·주제 문맥·첨부 이미지 hash를 묶은 요청 envelope를 만들고 fresh-context 서브에이전트 3개에 전달했다. 각 에이전트는 최신 스킬 문서와 neutral precore로 데이터 접근 전에 core/baseline을 확정했다. 문화권 범위만 분배하고 구체적인 컨셉은 각 에이전트가 선택했다. 세 arm은 상대의 prompt·pack·이미지를 읽지 않는다.

스킬 문서 SHA256: `f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089`. 별도 사용자 수치가 없어 기본 creativity=1, sensual=1, fetish=0, surreal=0을 사용한다. 참조 사진은 보이는 얼굴·짧은 검은 머리의 외형 참고이며 역사 속 신원·품계·성격의 근거가 아니다.

각 arm의 실제 이미지 호출 예산은 1회다. 이미지 호출 전 감사 오류는 고치되, 도구 차단이나 실패를 성공으로 바꾸지 않는다. source 노출, 실제 선택, literal prompt, 실제 호출, 생성 파일, 픽셀, 사용자 수용을 따로 기록한다.

| arm | 독립 컨셉 | 주요 관찰 대상 |
| --- | --- | --- |
| A | 비 갠 조선 회랑에서 닫힌 붉은 격자문 곁에 문서 쟁반을 들고 대기 | 당의 구성과 의복 부위, 문서 지지, 문·문턱·인물의 관계 |
| B | 18세기 후반 유럽 궁정 대기실에서 안내를 받아 접견실 문턱을 넘는 장면 | 열린 문, 안내자, 들어가는 인물, 뒤에 남는 대기자, 치마 구조 |
| C | 청대 복식 재현에서 붉은 문턱 곁에 문서첩을 받치는 장면 | 옷 부위의 같은 착용자 소유, 손·문서첩 지지 관계, 참조 bob 유지 |

실제 선택과 gate는 각 arm의 frozen testcase와 최종 review를 기준으로 판정한다. 한 장에서 가려진 부위를 충족으로 보충하지 않는다. 사용자 수용은 피드백 전 pending이다.

## 실제 생성·픽셀 결과

세 arm은 서로의 입력 없이 독립적으로 완성했고, [데이터 접근 전 core 파일 hash가 생성 후에도 유지됨](integration-evidence/core-freeze-preservation.json)을 확인했다. 원문 요청 envelope와 참조 파일 hash도 모두 같다. A/B/C는 각각 4/4/3개 실제 질의를 한 번씩 실행했다. 발급된 검색을 다시 샘플링하거나 케이스에 맞게 고쳐 성공을 만들지 않았다.

| arm | 신규 CID 자연 노출 | 실제 자료 전달 경로 | 신규 source 전체 픽셀 | generic 신체 gate | 전체 기준 |
| --- | --- | --- | --- | --- | --- |
| A 조선 | 0개; 실패 | B04 당의 전체 source를 postcore에서 직접 읽은 별도 전달 시험 | 부분 실패: 뒤 자락·트임 경계 불명확; 흰 거들지 연결은 보임 | 5/5 관찰 통과 | FAIL |
| B 유럽 | 2개; I04·A08 | 반환 I04를 전체 의미 그대로 inspiration_only로 사용; A08은 거절 | 통과: 문축·첫 경계의 안내자·바깥 대기자·안쪽 인물 관계 5/5 | 4/5; 드레스 아래 양 신발의 지지가 관찰되지 않음 | FAIL |
| C 청대 | 0개; 실패 | D02 길복 전체 source를 postcore에서 직접 읽은 별도 전달 시험 | 부분 실패: 완전한 용·봉황 공통 원형은 소매에 있고 몸판 원형은 잘림 | 2/5; 수평 바닥 받침 대신 모서리 그립 | FAIL |

A/C의 직접 자료 전달은 자연 검색의 성공이나 native 채택으로 계산하지 않는다. 세 arm 모두 native chosen 목록은 비어 있고 `native_approval:false`를 유지한다. B도 실제 출입 권한·직위·역사적 사건을 인증한 것이 아니라 시각적으로 연출된 공간 관계를 통과한 것이다.

A는 긴 둥근 앞 자락과 흰 커프가 보이지만, 가는 붉은 옆 자락만으로 뒤 패널 전체와 양쪽 트임 경계를 확정할 수 없다. B는 주요 공간 관계가 보이되 카메라 응시가 안내자 응시를 대신하고 가장 가까운 문틀 상단이 잘렸다. C는 소매의 용·봉황 도상이 매우 선명하지만 같은 도상이 요구된 **몸판**에 완전히 드러났다는 증거가 부족하다. 몸판/소매를 다른 carrier로 구별하는 검사가 실제 실패를 잡았다.

모든 managed review는 `record_valid:true`다. 이는 검토 기록의 유효성이다. `technical_qualification`은 A=pass, B=fail, C=fail이며 신규 source별 수동 gate는 A=fail, B=pass, C=fail이다. 완전한 신규 source와 generic body gate를 모두 요구한 결합 기준은 0/3이다. 세 이미지의 분위기가 궁중물로 읽힌다는 관찰을 전체 구조 PASS로 올리지 않았다.

| arm | 프롬프트·개별 기록 | 이미지 |
| --- | --- | --- |
| A | [최종 프롬프트](../../../../generated/photo-runs/court-palace-20261023-a/final_prompt.txt), [arm 보고서](../../../../generated/photo-runs/court-palace-20261023-a/arm-report.json), [source 픽셀](../../../../generated/photo-runs/court-palace-20261023-a/targeted-pixel-review.json), [부모 독립 검토](integration-evidence/parent-review-a.json) | [PNG](../../../../generated/photo-runs/court-palace-20261023-a/outputs/court-a-attempt-1.png) |
| B | [최종 프롬프트](../../../../generated/photo-runs/court-palace-20261023-b/authoring/final_prompt_en.txt), [arm 보고서](../../../../generated/photo-runs/court-palace-20261023-b/authoring/arm-summary.json), [source 픽셀](../../../../generated/photo-runs/court-palace-20261023-b/authoring/source-transfer-test.json), [부모 독립 검토](integration-evidence/parent-review-b.json) | [PNG](../../../../generated/photo-runs/court-palace-20261023-b/images/european-court-admission.png) |
| C | [최종 프롬프트](../../../../generated/photo-runs/court-palace-20261023-c/final_prompt_en.txt), [arm 보고서](../../../../generated/photo-runs/court-palace-20261023-c/arm-report.json), [source 픽셀](../../../../generated/photo-runs/court-palace-20261023-c/supplemental-pixel-review.json), [부모 독립 검토](integration-evidence/parent-review-c.json) | [PNG](../../../../generated/photo-runs/court-palace-20261023-c/court-c-qing-jifu-threshold.png) |

[집계 JSON](integration-evidence/TEST-RESULTS.json)은 각 arm의 baseline/core/final prompt·이미지·manifest·ledger ID·hash를 연결한다. 세 이미지 모두 1024×1536 PNG이며 [독립 파일 검증](integration-evidence/image-file-integrity.json)에서 PIL 검사, 모든 PNG chunk CRC, IEND와 trailing byte 검사를 통과했다. 각 arm은 첨부 사진을 실제 reference payload에 연결한 builtin `image_gen.imagegen`을 1회 호출했다. 총 3회, 재시도 0회, 차단/도구 실패 0회다. 도구가 실제 모델명을 제공하지 않아 관측 모델명은 미상으로 기록한다.

A/C의 저장 프롬프트 파일에는 끝 공백이 있고 runtime은 `strip`된 텍스트를 사용한다. 파일 SHA와 audited/runtime 텍스트 SHA를 구분해 보존했고, 정규화 후 실제 전달 텍스트가 일치함을 세 arm 모두 확인했다. 원본 파일·프롬프트·픽셀을 성공 판정을 위해 다시 쓰지 않았다.

호출 전 일부 감사 기록에서 빈 선택 배열이나 clarification key의 형식 오류가 나와 기록만 보정하고 재감사했다. core·최종 프롬프트와 이미지 예산은 유지했다. 큰 source 검증의 allocation 비용 때문에 이후 일부 CLI 호출은 [GC scheduling helper](../../../../generated/photo-runs/court-palace-20261023-coordinator/gc_photo_cli.py)를 사용했다. 원래 공개 entry와 sealed code·모든 validator·원래 arguments/return code는 유지하며 순환 GC의 allocation scheduling만 조정했다. 개별 사용/중단 기록은 arm execution-helper 또는 execution-notes에 있다.

참조 사진과 비교한 검은 단발·앞머리·얼굴 외형의 유사성은 보이지만 정확한 신원, 나이, 실제 품계, 역사적 진위, 사건의 전후·동기·허가를 인증하지 않는다. 참조 bob을 유지하는 재현이므로 완전한 시대 고증을 통과했다는 뜻도 아니다. baseline 이미지를 생성하지 않아 이전 버전보다 좋아졌다는 인과·우열 비교는 하지 않는다. 사용자 수용은 pending이다.

## 발견한 한계의 다음 반영 계획 — 미실행

1. 자연 질의 세트를 데이터 열람 전에 별도로 고정하고 한국·중국 궁정 장면을 추가 평가한다. 이번 정확한 source 문장 기반 66개 질의의 상위 10개 성공과 실제 sampled discovery 1/3을 다른 수치로 유지한다. 현재 테스트를 튜닝에 재사용할 경우 독립 holdout으로 부르지 않는다. source 부위·owner·역할 의미를 보강한 뒤 새로운 질의와 기존 회귀 질의를 모두 실행한다.
2. 당의는 측사면 거리와 몸 방향을 조정하여 옆구리 트임과 앞뒤 자락의 각 밑단을 동시에 드러내는 별도 케이스를 설계한다. 길복은 몸판과 소매 carrier를 구별하고, 문서첩을 낮춰 몸판 원형의 경계·두 도상이 프레임 안에 완전히 남는 구도를 검증한다. 현재 source의 경계를 완화해 실패를 없애지 않는다.
3. 유럽 장면은 카메라 거리와 의상 길이/발 위치를 조정해 양발·문턱·첫 문틀 전체를 함께 관찰할 수 있게 설계한다. 청대 문서첩은 양손 바닥 받침과 모서리 그립을 별개 동작으로 다룬다. 실제 사용자 의미와 새로 잠근 조건을 보존한 수정 케이스만 준비한다.
4. 현재 40개 고증 보류 항목은 개별 유물·시대·착용자 근거를 더 모은 뒤 분할/승격을 판단한다. source 메타데이터를 자동 native typed fact로 승격하지 않는다. 현 3장 결과는 보존하고 추가 생성은 수행하지 않았다.

## 저장·공유 상태

이번 작업은 데이터·로컬 설치와 테스트 결과를 남겼다. HEAD는 시작과 같은 `264a5ab9f15a689f22b2984d917711940f90bf17`이다. 이 작업에서 commit·push·PR은 수행하지 않았다. 기존 dirty/deleted 파일과 동시 추가 데이터는 되돌리지 않았다. 연구 단계 원본 증거는 [당시 README](integration-evidence/research-stage-README.md), [당시 검증](integration-evidence/research-stage-VALIDATION.json), [당시 checksum](integration-evidence/research-stage-SHA256SUMS)에 따로 보존했다. 현재 결과의 checksum 범위는 `INTEGRATION-SHA256SUMS`로 기록한다.
