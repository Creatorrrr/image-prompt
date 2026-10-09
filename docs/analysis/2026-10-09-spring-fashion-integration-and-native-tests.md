# 봄 패션 데이터 반영 및 독립 이미지 테스트

봄 패션 후보 276개, 시각 의미 프로필 276개, 선택용 bundle 276개를 실제 소스·검색 인덱스·런타임에 반영했다. 독립 서브에이전트 3개가 현재 스킬로 서로 다른 복잡한 컨셉과 사전 관찰표를 작성하고, 첨부 사진을 사용하여 실제 `image_gen` 호출을 1회씩 수행했다. 세 PNG를 원본 해상도와 thumbnail에서 에이전트와 coordinator가 각각 검토했다.

신규 요소의 사전 관찰 결과는 A 4/5, B 9/9, C 10/10이다. A는 스커트 허리단이 가려졌고 C는 필수 클립·종이·와이어 접촉이 관찰되지 않았다. B의 선택 주제 및 실제 hard set은 통과했으나 별도 레이스 끝 관찰은 축소 화면에서 실패했다. 세 장의 모든 authorial 세부 요소가 완전히 성공했다고 선언하지 않는다. 사용자 취향·수용 판단은 아직 받지 않았다.

## 반영 범위

[원 리서치](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-09-spring-fashion-visual-semantics-research.md)의 289개 키워드 중 283개 용어와 연결된 가시적 변형 초안 281건을 검토했다. 최종 결정은 신규 276건, 기존 관련 문맥 보강 2건, 기존 의미 재사용 3건이다. 초안과 실제 ID의 전체 대응은 [runtime-integration.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/runtime-integration.json)에 있다.

| 기존 도메인 | 신규 후보 | 신규 프로필 | 신규 bundle |
| --- | ---: | ---: | ---: |
| clothing_structure | 132 | 132 | 132 |
| fashion_fit | 36 | 36 | 36 |
| textile_surface | 24 | 24 | 24 |
| ornament_structure | 10 | 10 | 10 |
| accessory_structure | 25 | 25 | 25 |
| color_relations | 24 | 24 | 24 |
| subculture_appearance | 23 | 23 | 23 |
| portrait_fashion_exposure | 2 | 2 | 2 |
| 합계 | 276 | 276 | 276 |

8개 도메인의 extension/profile 16개 파일에 추가했다. 실제 파일 경로는 [소스 통합 영수증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/PRIMARY-SOURCE-INTEGRATION.json)에 있다. A라인 스커트와 페플럼은 기존 ID에 연결되는 `existing_slot_context_extensions`의 예문·문맥을 보강했다. 기존 후보·프로필 본문 1,535개는 ID별 원형 hash를 유지했다. 슬롯·이 작업의 도메인 등록·스킬 실행 알고리즘을 늘리지 않았다.

소재 성분 4건(cotton, linen, silk, rayon), bias cut 공정 1건, 숨은 속옷 부재(braless) 1건은 이미지의 직접 증거로 승격하지 않았다.

각 후보는 실제 의복·신발·장식의 구성 요소, 소유자, 양끝 노드, 방향 있는 관계, 영향을 주는 속성, 혼동 경계, 출처와 검증 조건으로 묶었다. 조합 스타일은 하나의 관찰 가능한 변형이며 이름 하나로 가족 전체의 특징을 동시에 요구하지 않는다. 한국어·영어 원 용어는 optional 검색에 연결했다. 검색 hit나 bundle의 associated profile은 독립 요청 근거·명시 opt-in을 대신하지 않는다.

실제 lookup 확인에서 `Slingbacks`만 있을 때 단수 `Slingback`의 누락을 발견해 `Mary Jane`, `Slingback` 단수 표현을 optional lookup에 추가했다. hard activation 범위는 넓히지 않았다. [V2 유지보수 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/extension-maintenance/photo_prompt_accessory_structure_extension-spring-lookup-20261009-v2.json)은 V1을 삭제하지 않고 연결하며 현재 소스·후보·bundle·profile hash를 묶는다.

## 중요한 관찰 경계

- 스위트하트는 두 곡선과 중앙 딥의 직물 경계로 판정하며 스트랩 유무와 분리한다.
- 포인텔은 작은 구멍을 둘러싸는 실제 니트 실·루프와 같은 연속 면의 기하학 반복으로 판정한다. 프린트 점·펀칭 직물·별도 네트는 대체 증거가 아니다.
- 밑단 길이와 허리단 위치는 각각 다른 의복 경계와 같은 착용자의 기준점에 묶는다.
- 메리제인 앞등 스트랩과 슬링백 뒤꿈치 스트랩은 각각 양끝 고정점과 실제 경로를 확인한다.
- 실루엣·공정 명칭·숨은 보강·섬유 성분은 보이는 겉면에서 자동 추론하지 않는다.

## 독립 검증 방식

3개 persistent subagent가 원문 요청을 byte-exact envelope로 묶고 RAG 전에 각 core를 먼저 고정했다. 컨셉·의상·구도·소품은 에이전트의 독립적인 난수 기반 authorial 선택으로 기록했다. 다른 arm 자료를 사용하지 않았다는 선언은 독립 manifest에 있다. 마지막 검증에서 arm마다 frozen 파일 12개, 최종 managed artifact 24개 hash와 동일 generation/receipt, 서로 다른 core/prompt, 실제 1행 ledger 및 PNG bytes를 확인했다.

현재 저장소의 `photo-prompt-image-generator` 스킬 SHA256은 세 arm 모두 `9e9b87e6f0b2c1ec1c36bd8e9d55f90950d53529a0b873722b546924dfc7043b`다. 원문 참조 파일 SHA256은 `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`이다. 실제 파일을 `referenced_image_paths`에 첨부했으며 보이는 얼굴 형태·짧고 어두운 bob·가느다란 앞머리만 안내로 사용했다.

| arm / 컨셉 | 새 데이터 사전 all-of 관찰 | 실제 hard set | 실패·관찰 한계 |
| --- | --- | --- | --- |
| A / 강변 인쇄 공방의 첫 도판과 봄바람 | 4/5, FAIL | 11/11, PASS | 스커트 허리단 가림 |
| B / 옥상 건조줄의 마지막 청사진 | 9/9, PASS | 8/8, PASS | 별도 레이스 끝 thumbnail 관찰 실패 |
| C / 비 뒤 첫 배를 기다리는 접힌 항로 | 10/10, PASS | 8/10, FAIL | 같은 clip jaw의 종이·와이어 접점과 가시성 부족 |

신규 all-of 관찰표와 실제 effective hard set은 다른 집합이다. hard 집합은 검증된 generation의 pack과 audited composed selection에서 파생한다. 같은 이미지에서 같은 owner의 지정 구성 요소·관계·필요 scale을 평가했고 부분 충족·가림·불확실은 실패로 처리했다. 다른 이미지의 성공으로 빠진 부분을 보충하거나 평균내지 않았다. 감사기는 기록의 유효성을 검증하며 픽셀 관찰은 에이전트와 coordinator가 직접 수행했다.

A는 신규 `visual-concept:spring_sf057_02`에 실제 opt-in했고 연속 실이 진짜 열린 셀을 둘러싸며 불투명한 실과 안쪽 면이 구별되는 것을 native에서 확인했다. 기존 sheer profile 5개와 embodiment 5개도 통과했다. 색 bundle `spf_sf104_2`의 같은 착용자와 가까운 warm palette는 보이지만 사전에 지정한 스커트 허리단 끝점은 가려졌다. associated 색 프로필은 hard 활성화하지 않았다. 작은 구멍의 `spring_sf057_01`까지 native 검증됐다는 뜻은 아니다.

![A 강변 인쇄 공방](/Users/chasoik/Projects/image-prompt/generated_images/spring-fashion-20261009/knit-layer.png)

[A 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/knit_layer/prompt_en.txt) · [A 테스트케이스](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/knit_layer/TESTCASE.md) · [A 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/knit_layer/stage2-result.json)

B는 스퀘어 목둘레 `spf_sf004_01`과 인접 warm palette `spf_sf104_2` bundle을 선택했다. 목둘레의 가로 하단·양쪽 모서리 연결, 같은 착용자, 페플럼 끝과 아래 스커트 면이 native 및 thumbnail에서 나타났다. B의 사전 색 기준은 페플럼 끝과 아래 면이므로 A의 허리단 기준을 사후 추가하지 않았다. 오른손이 파란 종이를 누르고 왼손이 떨어진 클립을 드는 사건, 얼굴·손·옥상 단서가 읽힌다. Spring opt-in은 pack에서 미노출되어 associated 신규 프로필의 hard activation을 주장하지 않는다. 별도 scallop 끝 실패는 남겼다.

![B 옥상 청사진](/Users/chasoik/Projects/image-prompt/generated_images/spring-fashion-20261009/bodice-hem.png)

[B 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/bodice_hem/final-prompt.txt) · [B 테스트케이스](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/bodice_hem/TESTCASE.md) · [B 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/bodice_hem/stage2-result.json)

C는 에이프런형 원피스 `spf_sf071_1`과 메리제인 발등 스트랩 `spf_sf107_02` bundle을 선택했다. 앞판 양쪽 끈 연결과 별도 블라우스 앞의 층, 양쪽 신발 각각의 발등 스트랩 및 그 신발 양끝 연결을 확인했다. 기존 원피스 계약도 5개 통과했다. 그러나 같은 클립 턱이 와이어까지 잡는 끝점이 없어 `embodiment_contact_and_space`, `embodiment_visibility_and_projection`이 실패했다. 별도 꽃의 부착 소유자, 블라우스 대각선 주름, 리본의 완전한 경로 및 배를 향한 반응도 일부 사전 의미와 달랐다. 신규 Spring hard activation은 미노출·미검증이다.

![C 비 뒤 선착장](/Users/chasoik/Projects/image-prompt/generated_images/spring-fashion-20261009/ornament-shoe.png)

[C 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/ornament_shoe/prompt.en.txt) · [C 테스트케이스](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/ornament_shoe/TESTCASE.md) · [C 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/ornament_shoe/stage2-result.json)

모든 결과는 1024×1536 PNG이고 실제 반환 파일과 배달 경로의 bytes/hash가 같다. native 호출은 총 3회다. 재생성·API/CLI 대체 호출은 수행하지 않았다. 도구가 모델명을 반환하지 않아 observed model은 unknown이다. 참조 사진은 평가된 generated baseline이 아니며 실제 사용자 판단도 없다.

## 인덱스·런타임 및 소프트웨어 검증

공식 빌더로 semantic/profile index 및 BM25F 런타임을 재생성하고 깊은 검증 후 immutable generation을 발행했다. Gemini `embedding-2`, 768차원으로 텍스트·provider·model·dimensions가 모두 같은 기존 벡터만 재사용했다. 새 벡터는 실제 embedding 호출로 만들었고 파생 인덱스를 손으로 수정하지 않았다. 이전 shard와 generation은 남겼다.

| 스냅샷 | 후보 | 프로필 | bundle | source 등록 | semantic entry |
| --- | ---: | ---: | ---: | ---: | ---: |
| 세 독립 이미지 테스트 공통 | 11,738 | 3,527 | 1,897 | 120 | 11,774 |
| primary 최종 반영 | 11,897 | 3,686 | 2,056 | 134 | 11,933 |

이미지 검증 generation은 `a7fd58162695c7c23a9257ac89b13434e94e6899fc3891858b837636ad1ced6c`, fingerprint는 `6d92970bf0f1f1acb3cf20b2ac5262a357f61f89b4dd03b1ede39945b77d1b8a`다. primary에는 동시에 추가된 다른 계절 데이터 159개와 14개 등록도 포함했다. primary generation은 `b980b1d3f880f799b6a262bed44fc7562efeec0a5ad9841fa47ebb025c3557a8`, fingerprint는 `3f056e6b7788b63a4c74494c7ae7663b5d79a21c608fea86c757fe80d6967bd9`다. 서로 다른 세대를 같은 이미지 증거로 취급하지 않는다.

마지막 확인은 기존 primary CURRENT에 대해 `acquire(bootstrap=False)`로 수행했고 현재 소스와 generation의 정확한 일치를 통과했다. [최종 freshness 영수증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/FINAL-RUNTIME-FRESHNESS.json)에 기록했다.

신규 [봄 패션 테스트](/Users/chasoik/Projects/image-prompt/tests/test_photo_spring_fashion_semantics.py)는 격리 worktree와 primary에서 각각 8개 모두 통과했다. 소유자/관계, optional/hard 경계, 숨은 성분·공정 주장 배제, partial/owner 대체 실패, pointelle 실 경계, 유지보수 이력, index coverage, 실제 BM25F 원 키워드·단수 lookup 및 stale 거부를 검사한다.

격리 focused suite 113개 실행에서 최초 111개 통과·2개 실패·error 0이었다. 새 변형이 기존 `fit_ff` cohort 수를 늘리는 검사 범위를 수정한 후 fashion-fit 모듈 10개 전체 재실행이 통과했다. 남은 실패 1개는 시작 전에도 실패하던 `PortraitFashionExposureTests.test_added_projection_preserves_initial_profiles_candidates_and_source_links`이며 기존 `pfe_one_shoulder` 누적 의미와 오래된 initial fixture의 차이다. 해당 소스 원형은 보존했고 fixture를 바꿔 실패를 숨기지 않았다. 113개 전체 suite를 수정 후 다시 실행하거나 전체 저장소 suite를 실행한 것은 아니다.

원 데이터 사전 검사·유지보수 검사·실제 인덱스 깊은 검증은 통과했다. 기존 테스트 중 4개 파일은 additive 데이터와 인증된 유지보수 successor 이력을 읽도록 좁게 조정했다. [TEST-SUMMARY.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/TEST-SUMMARY.json)에 baseline·후속 실행·미실행 경계가 있다. 소프트웨어 검증을 native 픽셀 성공으로 대신하지 않는다.

## 기존 작업 보존

[보존 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/FINAL-PRESERVATION.json)는 이전 authored record 1,535개, 기존 asset 1,816개 및 tracked 파일 24,611개의 존재·변경 범위를 확인했다. 기존 120개 source 등록은 유지되고 concurrent 14개 등록을 포함했다. 과거 replay의 live symlink 10개는 link bytes를 유지했다.

원래 untracked 경로 8,690개 중 8,689개가 남으며 다른 겨울 작업의 임시 `primary-semantic-cache.partial` 하나가 사라진 상태는 별도 delta로 남겼다. 이 작업은 그 파일 삭제를 수행하지 않았다. 위 소스·이미지 검증 단계에서는 HEAD를 유지했고 commit·push·PR을 만들지 않았다. 이후 Git 게시 상태는 별도의 봄 패션 게시 보고서와 영수증에서 확인한다.

## 후속 적용 계획

데이터·검색 반영은 완료했다. 픽셀 실패 때문에 가시성 기준을 완화하거나 원래 의무를 삭제하지 않는다. 다음 개선은 실패한 관계의 끝점을 같은 프레임에서 드러내는 작업으로 좁힌다.

| 대상 | 다음 작업 | 통과 조건 |
| --- | --- | --- |
| A 허리 경계 | 기존 장면 의미를 유지하며 블라우스 아래 스커트 허리단을 드러내는 가시성 수선 | 니트·블라우스·허리단의 지정 경계를 같은 PNG에서 관찰 |
| B/C 신규 프로필 | 가시적 기하가 있는 독립 요청을 먼저 고정하고 정식 retrieve에서 실제 opt-in 노출 검사 | 노출된 profile만 명시 선택하고 exact hard set의 native 판정 완료 |
| C 접촉·꽃·리본 | 같은 clip jaw 안의 종이·와이어, 블라우스 부착점, 각 신발 리본의 시작·교차·매듭을 보이는 수선 | 올바른 소유자와 모든 지정 끝점이 같은 이미지에서 보이고 부분/가림 없음 |
| 전체 변형 coverage | 미렌더 목둘레·밑단·작은 pointelle·슬링백 정밀 사례를 순차 추가 | owner/관계·혼동 반례·요구 scale을 사전 고정하고 개별 native qualification |

이 계획은 이번 3회 결과를 바꾸거나 추가 호출을 예약한 상태가 아니다. 새 호출은 지원되는 repair/독립 freeze 절차와 별도 기록을 따른다. 사용자 선호는 직접 판단을 받은 후에만 채우고 image qualification과 source validation을 계속 분리한다.

## 증거 경계와 산출물

소스 데이터, 인덱스, 검색, 후보 선택, 프롬프트 감사, 실제 도구 호출, 저장 이미지의 픽셀, 사용자 평가는 각각 기록한다. 3개의 이미지는 반영 가능성 사례를 검사하며 통계적 효과나 모든 276개 변형의 렌더 성공을 증명하지 않는다.

전체 결과는 [증거 인덱스](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/README.md), [세 native 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/FINAL-NATIVE-TESTS.json), [coordinator 직접 관찰](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/COORDINATOR-PIXEL-REVIEW.json)에서 확인할 수 있다.
