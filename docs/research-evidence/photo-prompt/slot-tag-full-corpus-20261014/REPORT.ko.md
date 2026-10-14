# 전체 슬롯 태그 보강 — 5단계 선행 구현 및 외부 한도 중단

> 2026-10-14 현재 안내: 아래는 최초 중단 당시의 역사 리포트다. 이후 저장된 1차 응답은 639개 파일/7,666개 ID, `qualified-reviews` 결과 파일은 5,341개이며 이 수들은 직접 검토 승인을 의미하지 않는다. 사용자가 이후 작업을 중지했고 이번에는 계획만 수정했다. **Gemini 재개·원격 cache 생성·provider 한도 확인은 수행하지 않는다.** 남은 의미·태그 판정은 Codex 직접 검토, 임베딩은 로컬 EmbeddingGemma 2로 전환한다. 아래의 옛 재개 안내 대신 [수정 계획](../../../analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md)과 [현황](../slot-taxonomy-revision-20261013/PROGRESS.ko.md)을 따른다. 과거 수치·본문·응답은 역사 증빙으로 보존한다.

요청한 5~8단계 전체는 완료하지 못했다. 5단계의 원전 보정·조건부 실현 계약을 구현하고 검증했지만, 전수 의미 심사 중 Gemini 프로젝트의 **월 지출 한도 초과(429 RESOURCE_EXHAUSTED)**가 발생했다. 추가 요청을 중단했고 한도를 올리거나 다른 유료 공급자로 우회하지 않았다. **미검토 항목·검증 실패 응답을 확정 태그로 적용하지 않았다.**

## 병합과 보호 범위

`git pull --no-rebase origin main`은 `Already up to date`를 반환했다. 시작 HEAD는 `e76a650e8d7fe4f20338247107df4ffc50e14382`, 확인한 `origin/main`은 `3f9a31a9e898a0604b1a0b07e8a76ea252ca8634`다. 로컬이 7개 커밋 앞서 있었고 원격의 신규 변경·충돌은 없었다.

기존 미커밋 문서 두 개는 BASELINE.json에 hash를 기록하고 그대로 보존했다. 다른 작업의 미추적 자료·옛 파생 layout도 정리하거나 포함하지 않았다. 이번 요청은 커밋까지이며 푸시는 실행하지 않았다.

## 적용한 선행 변경

4단계 CORRECTION-PROPOSALS.json의 11개 원전을 적용했다. 관련 의복 구성원 두 개의 효과 소유 범위까지 함께 정비해 변경된 canonical 레코드는 **13개**다.

- 중성적 표현을 boyish와 동의어로 취급하던 한국어·alias·keyword를 보정했다.
- 물리 테이프 지지체와 재생 영상의 dropout을 분리했다. 재생 영상 분기는 동결 core에 이미 선언된 긍정 재생 맥락이 있어야 사용할 수 있고 새 장치를 발명하지 않는다.
- 잔이 이미 정지 지지된 상태와 아직 내려오는 상태를 동시에 요구하던 묶음·연결 프로필을 접촉 시작 시점으로 정렬했다. 더 넓은 의미의 일반 lowering/rest 구성원은 바꾸지 않았다.
- 분홍 안층의 드레스와 누드색 저지 안층의 버스티에를 각각 완전한 대안으로 보존했다. 선택한 분기의 구성원·문구·효과만 사용한다.
- 구체 시각 값 없는 작성 규칙 6개는 diagnostic으로 전환했다. 원래 ID·본문·출처·graph/policy 참조는 유지하고 긍정 검색에서 제외했다.

V3 원본·V3 역할 제안·V4 슬롯 검색·V10 팩·V2 묶음 계약으로 관련 reader/제시/재검산/구성 경로를 함께 전환했다. 이전 V2 corpus 및 V9 pack을 받아주는 호환 경로는 추가하지 않았다. query recipe V2·runtime/receipt V3는 변경하지 않았다.

조건부 효과는 공통 효과와 명시적인 `one` 또는 `optional` 실현 분기로 구성한다. 분기 조건은 canonical 조건과 AND로 검사하고, 서로 다른 대안의 구성원·색·효과를 합치지 않는다. 조건부 후보 채택에는 제시된 `realization_id`가 필요하다. 묶음 공동 채택에도 전체 풀 검색과 동일한 동결 주체·성인 표현 허용 맥락을 사용한다. 성인 나이 선언만으로 성적 표현 권한이 생기지 않는다.

효과의 소유자를 기술적으로 다른 이름으로 표현해서 `main_subject/wardrobe` 잠금을 우회하지 않도록 기존 착용자의 보수적인 wardrobe 범위를 보존했다. 전체 태그안의 정확한 효과·역할 조건 자격화는 여전히 5단계에 남아 있다. 기존 source의 성인/주체/역할 제한을 의미 심사 없이 느슨하게 만들지 않았다.

## 원본·벡터·실행 검증

NATIVE-VERIFICATION.json은 기존 커밋의 모든 source module과 현재 원본을 대조한다.

| 항목 | 확인 결과 |
|---|---:|
| canonical ID 및 payload owner | 18,250개, 각 1개 owner, 유실·복제 없음 |
| 긍정 검색 / 진단 | 18,180 / 70 |
| 슬롯 / 기존 연결 | 139 / 12,089 |
| 연결·catalog·policy 변경 | 없음; binding ID·조건·weight 보존 |
| intrinsic 조건·출처 | 18,250개 전부 기존 값 보존 |
| 중복 후보/슬롯 관계·고아 참조 | 0 |
| 새 긍정 본문 | 5개 |
| document embedding 신규 호출 | 최초 보정 build에서 5개 |
| 기존 벡터 재사용 | 최초 build 18,175개; 최종 metadata build 18,180개 |
| 현재 query/image 신규 호출 | 0 / 0 |

최종 source SHA는 `125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b`, layout은 `89b2a0e79319da13e1f8b0b798273b66838b380b13ba1d2045f795e9c9b2d8a3`다. active closure 721개 파일의 존재·hash·coverage를 검증한 새 V3 generation을 발행하고 실제 기본 acquire 경로에서도 확인했다. 최종 generation은 `3cac944a550748d87939317c7a93827e7973ee7fd266f633873625eccbeccf9f`다.

변경 영향에 맞춰 corpus/조건·owner fit/분기/슬롯 lane/영수증/실행 연결 회귀를 수행했다. 마지막 계약 회귀 **56회**, 분기·재검산·영수증 회귀 **39회**가 통과했고, 앞선 runtime/source-race/workflow 검사 **34회**도 통과했다. 재실행 및 import된 fixture 테스트가 포함된 실행 수이며 고유 테스트 수·전체 suite 완료 수로 계산하지 않는다. 처음 존재하지 않는 테스트 모듈 이름을 지정한 loader 실패와 공개 분기 테스트의 fixture 잠금·문구 불일치 실패는 통과로 계산하지 않았다. 실제 요청에 묶인 조명 속성 잠금을 제거하지 않고 채택하려던 fixture를, 조명이 열린 단위 상황과 정확한 source cue로 수정해 재검증했다.

기존 실제 provider query 응답 3개의 core·controls·slot spec·본문·recipe·space를 현재 명세에 다시 대조했다. `light_quality`, `surface_material`, `visual_hierarchy`의 BM25F·exact cosine·RRF는 현재 전체 허용 풀의 offline full-scan과 일치했고 skip certificate·issued receipt replay·구성 감사가 통과했다. query를 새로 호출하지 않았다.

이 세 슬롯의 구현 smoke에서는 cold payload/posting/vector read가 모두 0이었다. 검색·재검산·구성 검사를 포함한 전체 실행의 cache peak는 67,108,831 bytes로 64MiB 한도 이내였고 descriptor는 61개였다. reader의 cache 한도와 전체 프로세스 메모리·원본 offline materialization은 별개다. 이 결과는 새 태그 적용 후 모든 슬롯을 검증할 7단계의 완료 증거가 아니다.

## 전수 심사 진행과 한도 오류

전체 18,250개 ID를 고정하고 4단계 609개와 연결 프로필 1개를 앞에 배치했다. 실제 원본·조건·효과·참조와 139개 의미 명세를 읽는 **Gemini 3.8 Flash 텍스트 모델**로 후보 중심 심사 초안을 받았다. 기존 binding 목록은 입력에서 숨겼다. 태그·facet은 의미 증거가 아니라 적용 정보로 다루도록 지시했다. 이것은 외부 모델의 의미 판정이며 독립적인 사람의 검토가 아니다.

한도 오류 이후 이미 진행 중이던 응답까지 포함해 **1,786개 / 149배치**의 원본 심사 응답과 재심사 응답 3개를 저장했다. **16,464개는 심사 응답이 없다.** 전체 심사 완료라고 표시하지 않는다.

REVIEW-PROGRESS.json 기준으로 1,529개 초안이 인용 위치·정확한 문자열·종류·차원·역할·속성 경로의 기계 검사를 통과했다. 257개는 추가 계약/인용 재심사가 필요하고, 의미 모호성 주석 66개·외부 사실 미확인 주석 45개도 남아 있다. 이 숫자는 서로 겹칠 수 있다. **기계 검사 통과는 의미 승인·정확도·native 자격화 완료가 아니다.** 파일럿 1,444개 metadata 사전 작업과 1,527개 의미 승인에 대한 최종 자격화도 끝나지 않았다.

같은 정확한 인용의 포인터 이동·catalog가 정한 차원/직접·맥락 표기 보정은 별도 representation repair로 기록한다. 이것을 독립 재심사로 계산하지 않는다. 존재하지 않는 인용·부적절한 owner/property·태그/facet만의 의미 추정은 적용하지 않고 큐에 둔다. 단순 keyword 점수나 embedding 순위를 의미 심사로 대체하지 않는다.

PROVIDER-BLOCK.json에 실제 `monthly spending cap` 오류와 미검토 ID를 기록했다. 저장된 성공 응답의 token 합계는 완전한 청구 대장이 아니다. 중단된 요청 중 응답을 저장하지 못한 호출의 과금·결과를 0으로 주장하지 않는다. 이후 재개 도구에는 durable attempt, 월 한도 오류 시 신규 요청 차단과 대기 큐 취소를 추가했다. 작업용 원격 prompt cache는 삭제해 중단 기간에 유지하지 않는다. 원본·명세·응답은 로컬에 보존했으며 재개하면 같은 prefix로 새 cache를 만들 수 있다.

## 남은 작업과 재개

- **5단계 진행 중:** 미검토 16,464개, 인용/계약 실패 및 의미 모호성 재심사, 전체 조건·효과 자격화, 필요한 source 의미 보정, 검증된 250~500개 단위 심사 대장·커밋.
- **6단계 미진행:** 확정된 전체 다대다 태그·안정 binding 적용과 참조 이관. 미검증 초안을 영속 관계로 쓰지 않는다.
- **7단계 미진행:** 적용 후 모든 슬롯의 실제 독립 BM25F/embedding/RRF·lazy extent·worst-case streaming·새 receipt/runtime 검증.
- **8단계 미진행:** 별도 seed 1,000개와 희소 경계의 최종 의미 평가, 결함 보정, 레거시 잔존/정확한 미참조 파생물 확인, 완료 리포트.

Gemini 프로젝트 한도 조정 후 기존 모델 방식으로 이어가거나, 외부 API 없는 직접 심사로 이어갈 방법을 사용자에게 문의했다. 어느 경우에도 현재 초안을 검사하지 않고 확정 태그로 가져오지 않는다. 외부 한도는 자동으로 변경하지 않는다.

source 의미·intrinsic 조건·실현 분기가 바뀌면 해당 후보를 다시 심사해야 한다. 이번 owner 범위 보정처럼 본문·조건·분기는 같고 metadata 효과만 바뀐 경우, 고정된 원본 심사 입력과 현재 metadata의 차이를 REVIEW-CURRENT-SOURCE-COMPARISON.json에 기록해 동일 입력 심사를 재개할 수 있다. 이전 모델 캐시가 삭제·만료되면 동일 prefix를 새로 생성한다.

이미지·픽셀 검사는 실행하지 않았다. source/index/실행 검증과 의미 심사 초안, 전문가의 외부 사실 확인, 실제 생성 이미지 품질은 서로 다른 증거다.

## 주요 증빙

- BASELINE.json, PILOT-CORRECTIONS.json, OWNER-SCOPE-CORRECTION.json
- NATIVE-VERIFICATION.json, FIRST-CONTRACT-INDEX.log, FINAL-CONTRACT-INDEX.log
- FINAL-CONTRACT-TESTS.log, FINAL-REPLAY-TESTS.log, RUNTIME-TESTS.log
- CACHED-HYBRID-VERIFICATION.json, CACHED-HYBRID-PACK.json, CACHED-HYBRID-COMPOSITION-AUDIT.json
- REVIEW-SOURCE-MANIFEST.json, REVIEW-ORDER.json, model-reviews/, normalized-reviews/, adjudicated-reviews/
- REVIEW-PROGRESS.json, ADJUDICATION-QUEUE.json, PROVIDER-BLOCK.json, CACHE-CLEANUP.json

텍스트 모델 설정 확인에는 [Gemini 공식 문서](https://ai.google.dev/gemini-api/docs/thinking)를 참고했다. 심사·provider 호출·한도 오류에 대한 결론은 위의 실제 로컬 실행 증빙을 기준으로 한다.
