# 궁중물 전체 참조 대화 재검토·2차 반영·재생성 시험

## Chrome 전체 대화 확인

로그인된 Chrome에서 [궁중물 용어 조사](https://chatgpt.com/c/6adb17fb-6238-83e8-a54e-d5e467110649)의 사용자 발화 2개와 답변 2개, 번호가 붙은 대단원 34개, 표 41개를 확인했다. 렌더링된 본문 표의 실제 데이터 행은 621개다. term/definition에서 공백과 인용 링크 라벨을 제거한 순서 보존 해시 `092b14607f44ede41291be7e818e4a97da6b23cdf893268739d640ed3d3eba06`이 이전 추출의 동일 정규화 해시와 일치했다. 새로 발견한 누락 답변은 없다.

이전 622개 표 행 집계 중 `품계 / 정품 / 종품`은 열 머리글이었다. 잘못 만든 R0059 경로 한 개만 제거했다. 따라서 표 본문 621개 + 표 밖 초야권 문맥 1개 = 현재 원 항목 경로 622개다. 기존 결과의 623은 당시 추출 수치로 보존한다. 참조 대화의 문장은 조사 자료이며 현재 사용자의 추가 지시로 실행하지 않았다.

근거: [Chrome 검증](chrome-full-conversation-proof.json), [본문 행 재검증 데이터](reference-body-rows-verified.json).

## 연구와 데이터 반영

이번에는 18개 공식 기관/박물관 본문 근거를 읽었고, 그중 14 URL은 기존 40개 출처 목록에 없던 주소다. Chrome에서 유물·재현 착장 7점/8뷰를 직접 보았다. 접근 실패/본문 미확인 페이지는 출처 판정에서 제외했다. 박물관 사진은 검토에만 사용했으며 생성 참조는 사용자가 첨부한 인물 사진 한 장이다.

- 새 시각 대안 18개, diagnostic 6개, optional binding 35개를 추가했다.
- 기존 88개와 합쳐 의미 카드 112개다. 기존 33개 시각 대안과 새 18개는 총 51개이며 기존 55개와 새 6개 diagnostic은 총 61개다.
- 거들지 접힘, 노리개 지지 경로, 몸판의 사각 쌍학 흉배, 신 바닥 중앙 받침, 가리기누 접합, 손과 샤쿠 접촉, 폴로네즈 세 덩이, 맨투아 구성, 포맨더 분할 덮개, 빗살과 장식, 스너프박스 이음선, 게이블 윤곽, 브레이드와 술, 개혁기 오스만 복식, 친타마니 특정 변형, 산수 없는 요질, 시타가사네 출현점, 가리마 두 겹을 각각 완전한 bounded realization으로 작성했다.
- 현재 원 항목 19개 경로에 수동 검토한 구성 요소 연결을 추가했다. 기존 고증 보류 복합 카드 40개는 그대로 보류한다. 부품 하나의 근거로 일습 전체를 승인하지 않았다.
- 실제 품계, 가려진 쓰개 철사, 숨은 폴로네즈 고정 장치, 향기/의학적 효능, 빗 하나로 파뤼르 전체 충족, 한 장으로 퇴장 순서 확정은 별도 diagnostic이다.

각 카드에는 부품, 주인, 연결 관계, 혼동 경계, 출처 범위와 픽셀 gate가 있다. 모두 native_approval=false이며 자동 hard activation을 허용하지 않는다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`을 유지한다. 실제 고증·native typed-fact 승인·사용자 수락과는 별개다.

근거: [출처와 사진 판독](source-read-log.json), [관측 요소별 상세 조사](RESEARCH-CATALOG.md), [새 의미 카드](semantic-cards.json), [작성 결과](authoring-result.json), [데이터 구조 검증](data-integrity.json).

## 실행 데이터와 검증

작성용 전체 union 인덱스는 후보 21,531개·positive 20,609개와 source closure 검증을 통과했다. 이번 24개 외에 동시에 바뀐 4개 기존 파일을 관찰·보존했다. 원본과 설치용 canonical snapshot의 구조가 다르므로 raw 작성용 총수와 설치 총수를 동일하게 취급하지 않는다.

고정 이미지 시험 버전 H2는 `265a75945bda1a1aea3b26ca88e13ab0dcb3139d22ae85197ed2d478ee3f2978`, native는 `eeaafc1952af220bd23823e72fcd1b1fadca8048f8ac334e08e7edbb25705d9a`다. 설치와 deployed validators PASS, positive 20,406 CID / 20,408 RID, CURRENT 쓰기 0이다. 기존 21,240개 원본을 모두 보존하고 24개를 추가했다. 실행 kernel SHA `ec29f441dbfc26930e7f4fb71ced759bf5ae271e672176110b21d2a7f6c846ef`, skill SHA `f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089`를 유지했다.

처음 오프라인 빌드가 CPython 3.12로 시작된 오류를 발견했다. 그 중간 release는 설치하지 않았다. 실제 배포 환경 CPython 3.14.3/Unicode16에서 complete native index verification을 다시 실행하고 F2 필드를 재계산한 뒤 최종 native/H2를 다시 봉인했다. 재계산한 F2 필드의 내용은 정확히 동일했다. 모든 원래 검증을 실행했으며 allocation scheduling용 GC helper 외에 kernel/검증/인자를 바꾸지 않았다. [환경 검증](environment-seal-validation.json), [검색 필드 검증](exact-environment-tokenizer-verify.json).

source-derived 한영 개발 질의 36개 중 36개가 해당 새 후보를 top10에 반환했다. 24개 boundary/ordinary control의 이전 top10 평균 중복은 9.708/10이었다. 새 diagnostic6개는 positive index에 없고 새 visual18개의 native snapshot은 원본과 정확히 일치했다. 이는 독립 holdout 성능이나 이미지 개선의 증거가 아니다. [60개 검색 검증](retrieval-qualification.json).

일반 장면 검색에서는 A 5query/40occurrence/34distinct, B 4/32/32, C 4/32/31을 검토했다. 새 24개 모듈의 자연 노출은 0/3이다. 기존 88개 궁중 모듈에서는 B에 F06만 노출됐다. 다른 공통풀의 기존 궁정 관련 후보는 이 모듈 집계와 별개다. 각 arm이 별도 direct-postcore 원본 검토를 통해 선택한 R2V01/R2V13/R2V15를 시험했고, 이를 자연 노출이나 native adoption으로 집계하지 않았다. native chosen arrays는 모두 []/[]다.

실제 발행한 13개 query와 query vector를 그대로 사용한 별도 whole-pool 진단에서 선택한 새 표현의 최고 순위는 A 664, B 1,539, C 1,212였다. 모두 creativity1의 rank32 창 밖이다. 새 managed retrieve·sampling·pack 변경 없이 원인을 확인했다. 즉 우연히 8개 표본에 뽑히지 않은 문제만은 아니다. [실제 질의 진단](pinned-actual-query-ranks.json).

검증 중 기본 버전이 다른 주제의 새 release로 여러 차례 바뀌어 덮어쓰지 않았다. 테스트 arm은 공식 dispatcher의 generation/store 명시 pin으로 위 설치본에 고정했다. 각 시점의 부모를 보존한 `union-final/`, `union-latest/`는 검증을 통과했지만 기본 포인터가 다시 앞서가 선택하지 않았다. 최신 부모를 기준으로 만든 `union-current/`의 데이터 전용 successor 검증과 기본 버전 선택을 완료했다. 앞선 버전으로 되돌리지 않았다. 최종 기본 포인터와 보존 검증은 아래에 기록한다.

<!-- final-union-result -->
### 최종 기본 버전 반영

- H2: `8421c8b02c7c23b4557898bc1c463d1991533e95e3ceb4ef9758890909217e8c`
- Native: `792a73564665b875c976619e712a77d92ee071f51347d9d1f9726600791f9a8c`
- 보존한 직전 기본 H2: `6d1d1389408abd7ddecd1da9e50ed007c4a87ce04f9fe547a49154127b7c6738`
- 기존 canonical 후보 21,682개와 모든 기존 source module·binding·catalog·policy를 보존했다. 커널 코드와 CPython 3.14.3/Unicode16 환경도 동일하다.
- 이미지 시험 버전과 최종 기본 버전의 신규 후보 module 및 binding module은 **byte-identical**이다. 원본 snapshot 24개, binding 35개가 모두 동일하다. 이미지 생성은 앞서 명시한 시험 pin에서 했다. 최종 글로벌 검색·표본이 그때와 동일하다고 주장하지 않는다.
- 최종 기본 검색은 positive 20,623 CID다. source-derived 개발 질의 36/36 top10, 24개 control의 이전 top10 평균 중복 9.750/10이다. 모든 배포 검증을 통과했고 CURRENT 쓰기는 0이다. 기본 선택용 설정 파일만 의도대로 바꿨다.
- 보호한 기존 파일 221개가 그대로이며 HEAD `264a5ab9f15a689f22b2984d917711940f90bf17`도 동일하다. 다른 dirty 파일을 되돌리거나 stage하지 않았다. 커밋·푸시·PR은 수행하지 않았다.

근거: [최종 통합본 대조](final-union-verification.json), [최종 60개 검색 검증](union-current/retrieval-qualification.json), [기본 선택 결과](union-current/install-active.json), [통합 결과](TEST-RESULTS.json).

## 세 독립 실행의 범위

세 새 에이전트는 이번 연구 데이터 접근 전에 각각 다른 장면의 core와 baseline을 고정했다. 기존 이미지의 repair나 짝지어진 before/after 실험이 아니다. 원 실행의 결과와 실패 판정을 보존한다. controls는 sensual=1, fetish=0, creativity=1, surreal=0이다. 사용자 요청/첨부 파일 hash와 coordinator가 미리 만든 envelope를 그대로 사용한다.

A: 조선 궁중 부엌에서 청자 그릇을 살피는 여성. B: 관객 도착으로 중단되는 유럽 궁정 하프시코드 리허설. C: 오스만 궁정에서 중단된 청원서 전달.

C는 자료 접근 전에 event anchor 과고정을 발견하고 원 freeze를 보존한 채 own-root 안 corrected-run을 새로 준비했다. envelope는 byte-identical이다. B는 모든 사전 고정 후 상태 조회 도구에서 이전 시험 결과 요약이 비의도적으로 노출됐다. 따라서 사전 창작 고정 독립성은 유지하나 postcore까지 완전 미노출이었다고 주장하지 않는다. 신규 장면을 고정한 뒤 다른 실행 결과에 맞춰 core를 바꾸지 않았다.

생성 파일, prompt literal, reference attachment, native attempt ledger, 일반 gate와 source-specific gate는 각각 검증한다. 검색 노출, 별도 직접 검토, prompt 반영, 픽셀 충족은 따로 집계한다. 가림은 성공이 아니며 생성이 차단되면 BLOCKED_UNSCORED다. 실제 모델명은 도구가 보고한 경우에만 확정한다.

## 재생성 결과

최신 로컬 스킬을 사용한 새 에이전트 세 개에서 첨부 사진 한 장을 실제 참조로 사용해 각각 한 번 생성했다. 총 실제 image_gen 호출 3회, 재시도 0회다. 세 run 모두 compose/runtime/일반 픽셀 리뷰 기록 검증을 통과했으며 일반 신체·접촉·지지·가시성 gate는 각각 5/5다. 실제 도구가 모델명을 반환하지 않아 모델명은 미확정이다. 설정의 gpt-image-2와 실제 관측 모델을 구분했다.

| 실행 | 장면과 이번 시험 구조 | 원본 픽셀 gate | 완전한 저술 장면 판정 |
|---|---|---|---|
| A | 조선풍 궁중 부엌, 색 소매 위로 흰 안감이 되접히는 경계·두께·연속성 | R2V01 3/3, PASS | 그릇 검사 의도와 달리 카메라를 보는 시선이며, 뜰만으로 왕실 부엌임은 증명되지 않아 NOT_FULLY_QUALIFIED |
| B | 유럽 궁정 음악실, 왼쪽 악보 소매의 브레이드→술 머리→낱실 | R2V13 3/4, FAIL | 구조 연결은 보이지만 오른쪽 건반 소매에 나타났다. 미리 지정한 주인/좌우 관계를 사후 완화하지 않았다. |
| C | 오스만풍 청원서 전달, 자홍색 몸판에 반복된 노란 세 원의 삼각 군집 | R2V15 4/4, PASS | 종이가 펼쳐져 있고 끈이 받는 쟁반으로 이어지지 않아 PARTIAL_NOT_PASS |

따라서 **이번 새 시각 구조는 2/3 통과**, **저술한 전체 장면은 0/3 완전 충족**이다. 장면의 문화적 분위기나 비슷한 장식만으로 합격시키지 않았다. A/C의 구조 통과는 일습 고증이나 숨은 봉제·직조 방식, 신분·정체성의 증명이 아니다. 기준을 이미지 생성 뒤에 바꾸지 않았으며, 부모 에이전트도 저장 원본 3개를 직접 보고 같은 한계를 기록했다.

- A: [실제 프롬프트](prompts/A.txt), [이미지](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-a/result.png), [arm 보고서](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-a/REPORT.md).
- B: [실제 프롬프트](prompts/B.txt), [이미지](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-b/images/royal-music-salon-r2-b.png), [arm 보고서](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-b/REPORT.md).
- C: [실제 프롬프트](prompts/C.txt), [이미지](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-c/corrected-run/images/court-ottoman-c-r2.png), [arm 보고서](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-c/corrected-run/REPORT.md).

[제공 원본과 저장 이미지 동일성](provider-original-equality.json), [부모 픽셀 판독](parent-pixel-reviews/)과 [파일·실제 호출·프롬프트 대조 검증](image-evidence-verification.json)을 보존했다. 후자는 세 run의 workflow가 묶은 28개 파일씩, A의 추가 manifest 89개 파일, predata core/baseline 고정 hash, 실제 호출 payload/ledger/composed/runtime의 동일한 프롬프트, 참조 사진 hash, PNG 전체 chunk CRC/IEND 및 이미지 hash를 확인했다. 각 arm은 새 모듈 원본 24개를 별도 직접 검토했으나 일반 검색의 자연 노출은 0/3이다. 따라서 2/3은 **직접 연구 자료를 검토한 뒤 프롬프트에 반영했을 때의 구조 시험**이며 자동 검색 제안 기능의 성공률이 아니다.

사용자 미적 수락은 pending이다. 생성하지 않은 baseline과 비교한 개선 효과는 주장하지 않는다. B의 사후 자료 미노출 독립성 한계도 위에 명시했다.

## 반영 범위와 재현

새 source modules는 `photo_candidate_court_palace_full_review_20261023.json`, `photo_candidate_court_palace_full_review_bindings_20261023.json`, 의미 sidecar는 `photo_court_palace_full_review_semantics_20261023.json`이다. 기존 의미 sidecar에는 잘못 센 표 머리글 제거와 구성 요소 연결만 추가했다. 저장소의 다른 dirty/concurrent 파일은 복구·삭제·staging하지 않는다. commit/push는 요청하지 않아 수행하지 않는다.

프렌치 후드 경로에는 게이블 쓰개와의 차이만 안내하는 contrast-only 연결 1개를 둔다. 프렌치 후드 검색어는 인접 대안 발견을 위한 lookup cue이며 각진 게이블을 동일 형태로 승인하지 않는다.


## 보강 적용 계획과 남은 검증 범위

1. 전체 대화의 본문 행/정의 검증과 머리글 오분류 수정은 완료했다. 출처를 읽고 named component, owner, 연결, 혼동 경계, 픽셀 gate로 변환해 실제 source modules와 optional bindings에 반영했다.
2. 정확한 환경에서 인덱스/봉인/설치/한영 검색을 검증했다. 동시 기본 release는 보존하며 최종 union에 같은 후보 원문·조건·효과·binding을 유지한다. 이미지 시험은 고정된 설치 버전에서만 시행하며, 최종 union의 글로벌 검색 결과와 동일한 실행이었다고 주장하지 않는다.
3. 선택한 3개 구조의 source-specific gate와 일반 기술 gate를 모두 실제 저장 파일에서 판독한다. 어느 한 연결이나 수가 가려지면 partial/unobservable로 전체 구조를 fail 처리한다. 미적 인상과 사용자 수락은 별도다. 이전 시험의 실패를 이번 결과로 덮거나 paired improvement로 해석하지 않는다.
4. 넓은 장면 질의에서 새 표현을 제안하는 성능은 이번 자연 검색 0/3으로 확인된 미해결 한계다. 후속 보강은 기능·사용 장면·주체 관계를 직접 뒷받침하는 근거를 확보하고, 연구를 보기 전에 고정한 자연 질의에서 재평가하는 방식이 적절하다. 단순 장르 단어 반복, 현재 3개 질의에 맞춘 과적합, 강제 hard activation으로 메우지 않는다.
5. 기존 보류40개 복합 일습은 부품의 일부 근거로 해제하지 않는다. 새 부품의 완전성, 전체 일습의 고증, native typed-fact 승인, 이미지 픽셀, 사용자 판단은 각각 별도다.


## 후속 적용 계획: 이번 실패에 연결된 구체적 작업 (미수행)

| 과제 | 이번 근거 | 반영 방식 | 다음 검증에서 구분할 결과 |
|---|---|---|---|
| 넓은 장면에서의 후보 발견 | 새 모듈 자연 노출 0/3, 선택 후보 최고 순위 664/1539/1212 | 기능·착용 위치·사용 장면을 직접 뒷받침하는 공식 출처를 더 확보한 뒤 해당 literal과 optional 연결만 추가한다. 현재 세 prompt의 문구를 복사해 검색어를 늘리지 않는다. | 연구 자료를 보기 전에 고정한 새로운 자연 질의에서 적합 후보가 rank32 안에 드는지, 실제 표본에 노출되는지, 검토 뒤 선택되는지를 따로 집계한다. |
| 좌우와 주체 연결 보존 | B는 왼쪽 악보 소매 대신 오른쪽 건반 소매에 구조가 생겼다. | 표현 원문과 구성 요소 그래프는 유지한다. 저술한 장면의 주체·좌우·손의 역할·장식 끝점이 연결된 상태를 preimage plan에 고정하고 실제 결과와 대조한다. | 연결 자체의 가시성과 선택한 소매 주인의 일치를 별도 기록하며 어느 하나라도 틀리면 전체 선택 표현은 실패다. |
| 장면 행동의 정확성 | A의 시선, C의 종이 열림과 끈 방향은 의도와 다르다. | source 후보 합격을 장면 행동 합격으로 재사용하지 않는다. 시선 대상, 종이 상태, 끈 시작·끝·받는 물체를 각 장면의 관측 항목으로 구체화한다. | source 구조, 일반 신체·접촉, 전체 장면 행동을 각각 판정한다. 보이지 않는 의도와 전후 순서는 판정하지 않는다. |
| 검색 변경의 부작용 | source-derived 36/36은 자연 질의 검증과 성격이 다르다. | 다음 변경 전 질의를 고정한다. 한영·문화권·구조·평범한 현대 장면을 분리하고, 새 source를 읽기 전에 정한 질의와 source 표현에서 만든 개발 질의를 혼합 집계하지 않는다. | target@10/32, 실제 노출, 부적합 일반 장면 침입, 이전 top10 보존을 각각 비교한다. 단일 종합 점수로 픽셀·고증까지 성공 처리하지 않는다. |
| 보류 일습 해제 | 이번에 추가한 것은 구성 요소 18개다. | 기존 보류40개는 독립된 일습 전체 자료를 확보할 때만 별도로 검토한다. | 부분적 닮음이나 새 부품 하나만으로 기존 복합 카드의 고증 합격을 선언하지 않는다. |

다음 이미지 시험을 하게 되면 이번 세 장의 사후 수정 재생성과 새로운 독립 장면 시험을 분리해야 한다. 이번 결과는 생성한 baseline이 없어 인과적 개선 실험이 아니며, 이전 실패를 대체하지 않는다. B의 postcore 노출 한계가 없는 새 실행이라야 완전 미노출 비교로 분류할 수 있다.
