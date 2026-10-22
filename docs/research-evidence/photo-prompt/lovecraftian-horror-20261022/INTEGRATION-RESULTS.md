# 데이터 반영 및 독립 이미지 실험

2026-10-22. 후속 요청에 따라 연구 자료를 실제 후보 source와 격리 설치본에 반영하고, 첨부 인물 사진을 사용하는 독립 서브에이전트 3개 실험을 수행했다. 데이터·봉인·설치 무결성은 통과했지만 **새 데이터의 이미지 기여는 입증하지 못했다.** 실제 생성 호출 3회 중 2장은 반환됐고 두 장 모두 엄격한 전체 조건은 부분 실현, 나머지 1회는 출력 차단으로 평가 불가다. 기본 검색 세대 전환은 HOLD다. 이 문서는 앞선 연구의 `NOT_RUN` 기록과 구분되는 후속 실행 기록이다.

## 실제 반영 범위

| 항목 | 반영 |
|---|---:|
| 한영 완결 시각 후보 | 57개 |
| 비가시·문맥·해결 보류 diagnostic | 27개 |
| 의미 카드와 실제 CID 대응 | 84개 |
| 기존 한영 source 보완 | 6개 |
| 신규 선택형 slot binding | 158개 |
| 원래 용어의 의미 경로 | 185개 |

새 source는 `skills/photo-prompt-image-generator/assets/photo_candidate_lovecraftian_horror_20261022.json`, binding은 `photo_candidate_lovecraftian_horror_bindings_20261022.json`, 의미 registry는 `photo_lovecraftian_horror_semantics_20261022.json`이다. registry의 graph와 키워드 alias는 검색·검토용 metadata이며 native 사실이나 채택 권한을 부여하지 않는다. 27개 diagnostic은 양성 재료 검색에서 제외한다.

초기 연구의 재사용7·정교화28·신규22는 조사 단계의 근접 분류다. 실제 source는 연령·프레이밍·재질·관계 끝점의 추가 조건을 포함하므로 57개 모두 완결된 선택형 변형으로 등록했다. 기존 근접 후보를 동일한 contract로 간주하거나 제거하지 않았다. 이를 57개의 새로운 공포 개념 발견으로 해석하면 안 된다.

기존 C119·C120·C126·C169·C173·C174의 한국어 명제를 완결했다. C173의 인물과 집단 사이 경계, C174의 두 문서 사이 차이에는 두 끝점을 모두 적었다. 기존 CID, intrinsic conditions, effects, provenance는 보존했다. 시작 시점의 다른 19,553개 후보, 13,777개 binding, slot catalog와 policy도 보존했다. 실행 도중 다른 작업이 추가한 medical-horror source는 별도 변경이며 이번 작업량에 포함하지 않는다.

원전의 부조·소상·실제 몸, 불투명 금속 뇌 원통·창작 유리 용기, 원전 가지형 Elder Sign·후대 별/눈 도안, 비늘·접힘·인쇄 무늬, 유사 진균·자실체·살아 있는 원형질을 구분했다. 그림으로 나타낼 수 있는 관계와 의식·기원·광기·우주적 무관심처럼 정지 이미지로 입증할 수 없는 주장은 분리했다. 자세한 사용 주의는 `references/lovecraftian-horror-semantics.md`에 있다.

## 검증의 범위

source 검사 8개와 의미 경계 회귀 21개, literal-text 회귀 24개가 통과했다. source 보존·한영 완결·185개 경로·diagnostic 비양성·기존 guard 보존을 확인했다. 이는 이미지의 예술성이나 픽셀 실현을 입증하지 않는다.

새 검색 세대는 시작 당시의 검증된 설치 커널을 유지하고 이번 데이터와 검토한 기존 6건만 교체하는 격리 successor다. 편집 중인 커널을 설치 커널에 덮어쓰지 않으며, 다른 작업과 기본 검색 설정을 경쟁해서 활성화하지 않는다. 실제 실험은 검증을 마친 특정 generation ID를 명시해 실행한다. 로컬 `google/embeddinggemma-2`를 사용하며 Gemini API 호출은 없다.

## 독립 실험 설계와 한계

사용자가 요청한 3개 서브에이전트는 기록·유물, 비인간 과학, 낯선 존재와의 조우라는 서로 다른 넓은 계열을 맡았다. 각 에이전트가 자체 난수로 세부 상황을 정하고 최신 canonical SKILL과 허용된 precore 자료, 사용자 요청·참고 사진·일반 지식만 사용해 기본 프롬프트와 관찰 항목을 고정했다. 계열과 자체 설정을 사용자 요구의 hard lock으로 만들지 않았다. 다른 실험의 프롬프트·후보·이미지는 공유하지 않는다.

실제 선정 컨셉은 기록 보존가의 발굴 탁본과 화석 비교, 관찰창 너머 뇌 모양 표본과 감각 장치, 온실에서 눈 없는 방사형 생물에게 꽃을 건네는 순간이다. 각각 자연스러운 slot query로 전체 후보군을 검색하고, 완전한 source와 조건을 읽어 적합한 후보를 선택하거나 거절한다. 특정 신규 CID를 강제 노출하거나 순위를 조작하지 않는다. 새 후보가 검색되지 않거나 채택되지 않으면 그대로 기록한다.

한 에이전트당 참고 이미지가 실제 첨부되는 native 이미지 생성 1회를 실행했다. 실제 호출은 총 3회이며 2장은 반환됐고 기록·유물 arm 1회는 output moderation으로 차단됐다. coordinator는 비성적 직업복 구도로 추가 시도를 제안했으나, 최신 관리형 retry 계약을 확인하고 실행 전에 중단했다. 추가 이미지 호출은 없다. provider/API fallback도 사용하지 않았다.

프롬프트·transport·참고 파일 hash·실제 출력 파일·픽셀 판정을 연결한다. 관계의 필수 구성요소가 일부 숨겨지면 해당 whole-case는 통과시키지 않는다. 기원·의식·동의·심리 같은 비가시 명제에는 `UNOBSERVABLE_NOT_PASS`를 사용한다. 생성기가 출력하지 않으면 `BLOCKED_UNSCORED`이며 데이터의 픽셀 실패로 간주하지 않는다.

**절차 편차:** byte-exact coordinator envelope는 서브에이전트 생성 후, 세 에이전트 모두 core 작성·후보 접근을 멈춘 상태에서 작성해 전달했다. 따라서 '위임 이전 envelope 생성'의 엄격한 시간 순서는 충족하지 못했다. core 고정 이전에는 모든 에이전트가 동일한 실제 사용자 요청과 별도의 request ID를 사용했다. 일부 중립 slot 준비 명령은 범위를 바꿀 수 없어 동일 입력 hash의 새 run으로 기술적으로 재바인딩했다. 과학 실험은 후보 접근 전에 계열을 사용자 lock으로 오해한 문구를 수정하고 최종 run에서 다시 고정했다. 조우 실험은 의미 해석 후, 전체 컨셉 결정과 control brief 읽기 전에 허용된 중립 분류명 catalog를 읽었다. 후보·예시 접근은 없었지만 이 중립 단계의 권장 시간 순서도 엄격히 충족했다고 주장하지 않는다. 이 기록을 완벽한 절차 준수로 표기하지 않는다.

이 실험은 source에서 나온 개발 query와 native 생성 시도 3회(실제 반환 2장)를 이용하는 탐색적 검증이다. 독립 holdout, 반복 성공률, 기존 데이터만 쓴 대조 이미지, 신규 데이터의 인과적 개선, 사용자 수용을 입증하지 않는다. 원래 제안했던 36장 전체 비교와도 다르다.

과학 실험의 추가 provenance 점검에서는 최종 composition 작성 후 보완된 기존 CID를 대조하려고 파일을 넓게 출력해, 발급되지 않은 source 본문 일부도 읽었다. 에이전트는 해당 읽기의 시점과 범위를 별도로 기록했고, 그 상세를 query·프롬프트·채택 판단에 사용하지 않았다고 보고했다. 최종 prompt는 기본 prompt를 그대로 유지했으며 hash와 실행 transport를 대조한다. 이 추가 접근도 절차 편차로 남긴다.

coordinator는 에이전트의 점수를 읽기 전에 실제 출력 파일을 먼저 보고 별도 관찰을 저장했다. 조우 실험에서는 그 첫 관찰 후 coordinator가 같은 arm에 줄기 접촉의 불명확성을 전달했고, 에이전트의 공식 기록은 그 메시지 후 완성됐다. 에이전트의 첫 관찰은 메시지 전이었으나 최종 post-render review가 완전히 blind였다고 주장하지 않는다. 다른 arm의 prompt·후보·출력은 공유하지 않았다.

## 실행 결과

검색 generation은 `fc8ae54d09d76258d0e77b8ab52037869fc9362fcb8331d847b8ea438f667196`, native generation은 `002465b20d8d6b3b27e078d0f3a4c7dbadd7bd99dd05181c7907062d656c321c`다. source/D/F2 통계·실행 증명·벡터 coverage의 봉인 검증이 통과했다. 새 문서 벡터 63개를 로컬 실행했고, 기존 문서 벡터 19,252개를 그대로 재사용했다.

최초 배포 준비 검사가 확인한 범위는 dependency와 installed recorder였다. coordinator가 정식 설치 전 staging store를 전달해 세 첫 검색 모두 `local_model_missing_or_unsafe: 1_Pooling/config.json`로 후보 검색 전에 중단됐다. core·query scope·후보 순위를 바꾸지 않고 `install_photo_h_f2_runtime.py --no-activate`로 로컬 모델 파일을 배치한 후 같은 generation으로 재시도했다. 정식 설치는 deployed `Generation(full=True)`와 native `RuntimeSnapshotProvider.load_generation` 검증까지 통과했다. 설치본은 `/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed`이며 positive CID 19,313개/RID 19,315개다. dependency/recorder 검사 통과가 native 모델 로딩까지 입증하지는 않았다는 점을 구분한다.

큰 JSON의 Python 3.14 cyclic-GC 병목으로 최초 빌드 프로세스를 중단하고, 이미 완료된 native publication의 모든 member hash와 stage 동일성을 재검증해 재사용했다. 이후 source/D/F2 봉인 검증은 그대로 수행했다. kernel·validator를 고치거나 검사 항목을 생략하지 않았다. 자세한 기록은 `resume-execution.json`에 있다.

개발용 한영 query 160개를 전체 positive CID 19,313개에 각각 실행했다. 양성 query 60개 중 59개는 지정 신규 CID가 top10, 나머지 영어 faceless-head query는 R30이 138위였다. 이 질문의 실제 1위는 기존 L129 `cand_9e033cb1ac945925b3c1563ad84a3605`였고, 원문에서 매끈한 정면 얼굴과 머리 사이 경계를 요구함을 확인했다. R30은 두 뿔·목·막날개 뿌리까지 포함하는 구체 변형이므로, 이를 더 넓은 faceless 의미의 검색 실패율로 일반화하지 않는다. baseline에는 신규 CID가 없으므로 before rank를 개선율로 계산하지 않았다.

경계·일반·비가시 query 100개 중 50개에 신규 시각 후보가 top10으로 나왔다(경계32·일반10·비가시8). 이는 raw whole-pool exposure이며 eligibility나 채택 통과율이 아니다. 대표적으로 '모퉁이 하나가 안개 뒤' 질문에 전체 네 모퉁이 관찰을 요구하는 계단 후보가 1위, '사건 번호도 다름' 질문에 동일 번호를 요구하는 두 기록 후보가 1위였다. 후대 별/눈 Elder Sign 질문에서는 원전 가지형 표식 및 Elder Thing 몸 후보가 노출됐다. 이들은 각각 가림, 명시적 차이, 버전/대상 충돌 때문에 그 질문의 실현으로 선택하면 안 된다. 은빛 열쇠 상품 사진의 열쇠 후보 노출처럼 소재만 겹치는 경우도 있어 50개를 모두 false positive로 집계하지 않는다. 비가시 의식·우주적 무관심 질문의 장치·방향 proxy 역시 원래 주장의 증명이 될 수 없다.

160개 raw probe는 native compatibility qualification이 아니며 control 100개 전체에 대한 관리형 선택 검증은 수행하지 않았다. 기본 runtime 선택은 전환하지 않고, 이미지 실험만 위 새 generation을 명시해 수행한다. 편집 source의 전역 index는 병행 작업으로 계속 달라져 기존 dictionary 검사의 `layout source/space mismatch`를 PASS로 바꾸지 않았다. 이번 격리 검증본 자체의 source/index closure는 별도로 통과했다.

### 실제 관리형 검색과 채택

| 독립 arm | 제출 query | distinct source / occurrence | 신규 CID 노출 | 보완한 기존 CID 노출 | 이번 반영 source 채택 |
|---|---:|---:|---:|---:|---:|
| 기록·유물 비교 | 4 | 29 / 32 | 1 (R06) | 0 | 0 |
| 비인간 과학 | 5 | 31 / 32 | 1 (R41) | 0 | 0 |
| 온실의 낯선 조우 | 5 | 28 / 34 | 0 | 0 | 0 |

이는 일반 검색의 top10 개발 probe와 다른 결과다. 각 에이전트가 자체적으로 쓴 slot/whole-scene query, 실제 발급 material, 완전한 source를 검토한 결과를 센 것이다. 신규 R06은 점토 부조+종이 스케치·갈라진 머리·비대칭 세 돌기를 함께 요구하고 count 효과를 포함한다. 기록 실험은 count가 열리지 않아 이를 잘라 채택하지 않았다. 과학 실험에서 나온 R41은 '덮인 허구 성인 표본의 노출된 팔과 별도 종이 해부 도식'이며 뇌 원통 후보가 아니므로 전체를 거절했다. 조우 실험은 신규 CID 자체가 발급되지 않았다. 세 arm 모두 보완된 기존 6개 CID와의 교집합도 0이었다.

제출 query 수는 실제 색인 호출 수와 다를 수 있다. 과학 실험의 occurrence는 object_structure 8, prop 0, situation_context 8, request_topic 8, baseline 8이었다. prop projection은 `nonpositive_scope_without_requested_change` / `no_independently_requested_positive_change`를 기록했다. 에이전트가 독립적으로 작성한 용기·감각 장치의 의도가 이 경로에서 발급 재료로 이어지지 않았다는 구체적 관찰이며, scope 규칙의 오류 여부까지 확정한 것은 아니다. query나 순위를 사후 수정해 재실행하지 않았다.

따라서 **이번 세 실험의 신규/수정 source 기여는 입증하지 못했다.** 화면에서 주제가 잘 드러나더라도 source→채택→prompt→pixel의 연결이 없는 상태다. 강제 CID나 조건 완화로 이 실패를 감추지 않았다. 과학·기록 실험은 비교 후 기본 prompt를 그대로 유지했고, 조우 실험은 후보 접근 전에 적어둔 기하 문제의 국소 staging을 개선했다.

### 실제 픽셀 관찰

| arm | 화면에서 확인된 내용 | 전체 사례 판정 | 이번 source 기여 |
|---|---|---|---|
| 기록·유물 최초 호출 | output moderation으로 파일 미반환 | BLOCKED_UNSCORED | NOT_DEMONSTRATED |
| 비인간 과학 | 관찰창 너머 뇌 모양 표본·곡선형 감각 장치·관찰자, 참고 외형의 대체적 유사성 | PARTIAL_NOT_FULL_PASS: 원통 상단/우측 잘림, 오른손 받침 요구와 반대인 왼손 접촉 | NOT_DEMONSTRATED |
| 온실 조우 | 눈 없는 꽃/절지형 생물과 인물, 같은 꽃의 교환, 가까운 팔의 몸통→관절→집게 연결 | PARTIAL_NOT_FULL_PASS: 집게는 꽃 머리/꽃받침 부근을 가려, 반대 줄기 끝의 직접 접촉 불명 | NOT_DEMONSTRATED |

과학 장면의 SF/과학 공포 모티프는 읽히지만 의식·장치의 효력·외계 기원을 증명하지 않는다. 조우 장면은 비인간 해부와 조심스러운 교환이 읽히지만, 특정한 우주적 무관심·탈인간중심 공포는 온화한 호기심 장면과 구별하기 어렵다. 세부 필수 조건의 일부가 가려지거나 바뀌면 whole-case를 PASS로 세지 않는다. 참고 사진과의 대체적 외형 유사성은 실제 인물의 동일성·나이·성격·동의 판정이 아니다. 사용자 수용은 미확인이다.

coordinator는 과학 이미지를 먼저 보고 모티프·공간·대체적 외형을 평가한 뒤, 실제 전송 prompt와 에이전트 판정을 읽어 전체 원통/손 좌우 불일치를 추가 검증했다. 두 단계의 범위를 `coordinator-pixels-science.json`에 구분했다.

기록·유물 최초 차단은 request ID `51de86ec-94ec-4fc8-90ac-8d39031af489`, HTTP 400, `moderation_blocked`, `moderation_stage=output`, `categories=[sexual]`로 기록됐다. 요청한 보존가 장면이나 참고 인물의 실제 속성이 해당 범주라는 뜻으로 해석하지 않는다. 반환되지 않은 픽셀은 볼 수 없었다. coordinator가 비성적 직업복 구도의 대안을 제안했으나, 실제 지원 route `provider_blocked`는 `allowed_changes`, `local_axes`, 양수 `additional_invocation_limit`를 금지하며 `failure_route_cannot_rerender`를 반환하도록 구현돼 있었다. [SKILL.md](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/SKILL.md:38)의 “An unrepresentable lineage-v2 scope stays blocked; do not open composition for convenience.” 규칙에 따라 추가 생성은 실행하지 않았다. route를 `artistic_revision`으로 바꾸거나 guard를 고쳐 진행하지 않았다.

최신 오류 수집 예시의 tool/environment 표기와 봉인된 recorder의 표기가 달라, 최초 raw-string 증거는 그대로 두고 recorder가 요구하는 `image_gen` / `native_imagegen` 별칭의 관리형 증거를 별도 작성했다. 원래 오류 문자열·request ID·prompt·status는 변경하지 않았다. 조우 arm의 끝나지 않은 read-only review 명령에는 봉인 release를 full 검증한 후 같은 native entrypoint에 cyclic-GC scheduling wrapper를 사용했다. validator·source·prompt·image 호출 수를 바꾸지 않았다.

### 후속 보완 순서

1. 이번 14개 제출 query와 실제 수행/미수행 기록을 고정하고, scope projection·전체 순위·발급된 material을 연결해 관련 source가 검색되기 전에 제외됐는지, 순위에서 밀렸는지, 발급 과정에서 빠졌는지 구분한다. 별도 source-derived 질문 160개의 높은 노출을 실장면 성능으로 대체하지 않는다.
2. 기존 인물 수와 새 소품/신체 부품의 수를 구분할 수 있는 owner 단위 조건·효과를 검토한다. 원문에 필요한 count를 지우거나 고정된 core를 사후에 열지 않는다. native qualification이 필요한 관계는 metadata graph만으로 허용하지 않는다.
3. 장치·매체·생물의 본체와 부분 구조를 함께 보존하는 후보를 장면 용도별로 검토하고, 부적합한 과학 표본이나 전체 해부 bundle로 대체되는 경로를 개선한다. alias를 늘릴 때 원전/후대/창작 판본을 섞지 않는다.
4. 현재 이미지·source·query를 본 적 없는 새 독립 authoring에서 다시 검증하고, 실제 선택된 source의 전체 clause가 prompt와 pixel까지 이어지는지 확인한다. 기본 그림과 보강 그림의 차이를 주장하려면 별도 대조 생성과 반복이 필요하다.
5. 일반·부정·비가시 query의 관리형 eligibility 검증을 보완한 뒤 기본 검색 세대 전환을 판단한다. 현재는 격리 설치·명시 generation 실험까지 완료 대상으로 삼고, 전역 activation은 HOLD다.

### 전달 파일과 보존 상태

| arm | 프롬프트 | 실행 증거 | 실제 이미지 |
|---|---|---|---|
| 기록·유물 | [final-prompt.txt](integration-evidence/archive/final-prompt.txt) | [execution-summary.json](integration-evidence/archive/execution-summary.json) | 반환 없음; [원문 오류](integration-evidence/archive/native-tool-error-1.json) |
| 비인간 과학 | [final-prompt.txt](integration-evidence/science/final-prompt.txt) | [run-summary.json](integration-evidence/science/run-summary.json) | [science.png](test-images/science.png) |
| 온실 조우 | [final-prompt.txt](integration-evidence/encounter/final-prompt.txt) | [test-report.json](integration-evidence/encounter/test-report.json) | [encounter.png](test-images/encounter.png) |

[IMAGE-TEST-RESULTS.json](IMAGE-TEST-RESULTS.json)은 원장 3행·호출 3회·반환 2장·차단 1건·전체 pixel PASS 0건과 실제 파일 hash를 묶는다. 이미지 복사본은 native 저장 파일과 SHA256이 같다. [INTEGRATION-SHA256SUMS](INTEGRATION-SHA256SUMS)는 이 후속 증거 묶음의 무결성 목록이다. 초기 연구 파일 30개는 기존 `SHA256SUMS`와 모두 일치하도록 보존했다.

이 작업의 커밋·푸시는 없다. CURRENT 쓰기와 기본 runtime 설정 전환도 수행하지 않았다. 병행 작업의 dirty/untracked source를 되돌리지 않았다. 실제 설치본은 명시 generation으로 재사용 가능하며, 나머지 제약은 새 데이터 미채택, 반환 이미지의 부분 실현, 출력 차단 1건, 관리형 control qualification 미완료, 사용자 수용 미확인이다.

원시 증거와 빌더: `generated/maintenance/lovecraftian-horror-20261022/`.
각 프롬프트·후보 receipt·이미지·독립 평가는 `generated/photo-runs/lovecraftian-*/`.
