# 불 데이터 반영 및 독립 이미지 검증

2026-10-08. 앞선 연구 산출물은 조사 당시의 상태로 보존했다. 이 디렉터리는 이후 실제 구현과 검증 증거다.

## 실제 반영

- 신규 후보 **127개**, 기존 후보 **4개**의 동일 의미 맥락·paraphrase 보강.
- `authored_components/v2` 시각 프로필 **131개**, 활성화 후 적용할 원본·관계 gate **521개**.
- 시각화하지 않는 맥락 **24개**는 활성 후보/프로필에서 제외.
- 원본 후보는 **20개 슬롯**에 등록. 후보팩 V6, core V3 및 최신 스킬 절차는 변경하지 않았다.
- 광학 플레어 3개와 코로나그래프 CME 1개는 기존 candidate ID를 재사용했다. 기존 carrier와 effects를 바꾸지 않았다.

활성 소스:

- [후보 원본](../../../../../skills/photo-prompt-image-generator/assets/photo_prompt_fire_relations_extension.json)
- [시각 의미 원본](../../../../../skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_fire_relations.json)
- [등록 manifest](../../../../../skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json)
- [채택·소유·출처 ledger](ADOPTION-LEDGER.json)
- [회귀 검증](../../../../../tests/test_photo_fire_relations.py)
- [최종 이미지·검증 보고서](FINAL-REPORT.md)

각 카드의 전체 3요소는 연구자가 설계한 **선택적 실현**이다. 해당 용어의 유일한 과학적 정의나 모든 이미지의 필수 연출로 해석하지 않는다. 긴 complete proposition만 좁은 exact activation에 등록했고, 자연 문장·유사 검색은 선택 가능한 discovery다. 선택한 프로필의 전체 duty는 composition/runtime/pixel 감사에 연결된다.

화염, 발광하는 고체, 분리 입자, 공중 연기, 표면 검댕, 수광면, 수면 반사, 광학 영상면을 구별했다. 촛농·머리·의복 효과는 기존 `main_subject`의 실제 property 경로에 선언했다. 의복 손상은 coverage 변경까지 선언하여 다른 carrier로 잠금을 우회할 수 없도록 했다. 선언의 문법과 property 소비는 코드로 검사하며, 실제 물리 소유 관계의 진실은 literal composition과 원본 픽셀에서 따로 판단한다.

화원 위치, EUV 채널, 관측 방식 같은 메타데이터는 보이지 않는 정보를 입증하는 native gate로 만들지 않았다. 온도·원인·화학 물질·임상 진단·동기·안전 성능·특정 의례 판본은 픽셀로 추론하지 않는다. 42개 외부 출처의 접근 한계는 원래 연구의 `SOURCES.json`에 유지했다. 창작 형태와 출처가 지원한 현상 경계를 구별한다.

## 인덱스와 보존

[VECTOR-REUSE.json](VECTOR-REUSE.json)은 의미 인덱스가 10,567 → 10,694개, 시각 프로필 인덱스가 2,321 → 2,452개로 바뀌었음을 기록한다. 기존 의미 10,563개와 기존 프로필 2,321개의 동일 텍스트 벡터는 값이 모두 동일하다. 새 후보 127개, 보강된 기존 후보 4개, 새 프로필 131개만 새 입력으로 임베딩했다. provider/model/dimensions는 Gemini / gemini-embedding-2 / 768이다. 배치는 1이었다. primary 적용에는 검증된 동일 입력·동일 공간 캐시를 사용하여 동일 벡터를 재호출하지 않았다.

두 인덱스를 canonical builder로 생성하고 사전·프로필 인덱스를 검증한 뒤 immutable runtime generation을 실제 발행했다. `RUNTIME-READY.json`은 격리 checkout의 실험 소스 준비 상태이고, [primary-runtime-publication.log](primary-runtime-publication.log)는 활성 primary의 별도 발행 결과다. 스킬과 중립 definitions/catalog는 두 checkout에서 동일하다.

이미지 시험 중 발견한 F097의 `forge` endpoint를 설명과 일치하는 `declared_fire_bed`로 수정했다. [수정 기록](BELLOWS-OWNER-CORRECTION.json)은 이전 maintenance record를 보존한다. [마지막 vector 비교](VECTOR-REUSE-AFTER-BELLOWS.json)에서 의미 vector 한 개만 새 입력이며, 나머지 의미 10,693개와 profile 2,452개 전체는 첫 통합 상태와 동일하다. 이 후보는 이미지에 선택되지 않았으므로 수정 후 pixel 성공은 미판정이다. [최종 primary 런타임](primary-runtime-final.log)을 별도로 발행했고, 세 이미지가 사용한 최초 immutable generation은 그대로 보존했다.

[PRESERVATION-AFTER-INTEGRATION.json](PRESERVATION-AFTER-INTEGRATION.json)은 데이터 반영 직후의 보존 기록이다. 이후 두 runtime transport 수정과 고정 capture test scope 수정을 포함한 [최종 보존 기록](PRESERVATION-FINAL.json)은 기존 스킬 파일·재귀 vector shard·텍스트 테스트 4,016개를 비교했다. 변경한 기존 파일은 manifest 1개, index manifest 2개, runtime script 2개, 고정 test 1개로 6개이며, 다른 비교 대상 변경·삭제는 0개다. 기존 manifest row는 순서와 내용 그대로 보존하고 두 row만 추가했다. Git HEAD는 바꾸지 않았고 commit/push/reset/stash는 수행하지 않았다. 저장소 전체 파일에 대한 보존 주장으로 확장하지 않는다.

## 검증 경계

최종 사전 검증, profile index 2,452개/5,068 exact terms 검사 및 관련 테스트 **35개**가 통과했다. 새 fire 테스트 10개, candidate semantics 13개, transport 4개, 고정 capture scope 8개다. 전체 proposition과 negation, broad keyword의 hard activation 금지, 자연 문장의 optional discovery, 화염/광학/고체 발광의 혼동, owner/property 잠금, metadata gate 분리, context-only 제외, F097 소유 관계 및 기존 후보 전체의 의미 보존을 포함했다. 별도 managed workflow/transport 검사 12개도 통과했다.

시험에서 발견한 `effective_visual_contract_sha256` 누락은 바인딩된 composition 감사 hash만 전달하도록 수정했다. native bridge는 exec session의 완료까지 출력 조각을 모아 exit code/JSON을 검사하도록 수정했다. 고정 capture 테스트는 10월 1일의 원래 exact 비교를 유지하고 후속 fire context overlay만 그 historical inventory에서 제외했다. 현재 네 ID 맥락 추가와 모든 기존 candidate 의미는 별도 새 fire 테스트로 검사했다.

인덱스 생성 도중 시작한 이전 테스트는 stale source/index 때문에 실패했고 전체 발견 실행은 중단했다. 그 로그도 보존하며 완료 후 결과와 합산하지 않는다. 이후 완료된 전체 실행은 225개 모듈, 발견 2,038개/실제 보고 1,954개, 모듈 199개 통과/26개 실패였다. class setup 중단으로 84개 발견 사례는 실행되지 않았다. 기존 산출물 overlay와 고정 capture scope의 제한된 재검증으로 실패 4개 모듈이 통과했고 **22개 모듈은 미해결**이다. F097 마지막 수정 후 균일한 전체 재실행은 하지 않았다. 원인과 검증 한계는 [전체 실패 분류](FULL-REGRESSION-CLASSIFICATION.md)에 있다.

이미지 arm은 공통 사용자 원문과 각 envelope를 사용하며, 별도의 fresh context에서 시작했다. 기본 프롬프트·controls·feature selection·embodiment·core를 먼저 freeze한 다음 새 source generation을 조회한다. 실제 데이터 노출, 선택, baseline 대비 prompt 추가, 감사 통과, 이미지 생성, 원본 픽셀 판정, 사용자 수락을 각각 기록한다. 521개 gate의 존재는 521개를 렌더 검증했다는 뜻이 아니다. 세 장면은 이번 선택 사례의 실용 시험이며, 데이터의 인과 효과를 입증하는 무작위 통제 비교는 아니다.

실제 native 호출은 **3회**, arm마다 1회이며 이미지 재생성/API fallback/baseline 비교 렌더는 0회다. 기록된 필수 gate **19/19**(embodiment 15개 + 새 F002 profile 4개)는 통과했다. arm 1의 추가 검사 6/6, arm 2는 7/9, arm 3은 6/7이다. 해안 장면의 얼굴빛 화원 귀속·가로 석호 연출과 실내 화구 연기 경로의 실패를 유지한다. arm 1/3은 새 profile 노출 0개라 후보 기여만 확인했다. 원본과 축소본을 coordinator도 직접 검사했다. 사용자 수락은 세 arm 모두 pending이다.
