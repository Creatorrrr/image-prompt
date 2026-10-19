# 구 그래프 검증 함수·상수 397행 정리

상태: 구현·검증 완료, 이번 변경만 로컬 커밋 대상으로 확정했다.

## 변경

`skills/photo-prompt-image-generator/scripts/prompt_generator.py`에서 다음 여섯 항목만 제거한다. 소스 diff는 **0행 추가·397행 삭제**다. 주변 빈 줄·import·다른 함수·데이터는 수정하지 않는다.

- 함수: `validate_character_mechanism_graph` 370행, `character_runtime_node_topic_ids` 5행, `character_runtime_node_family_ids` 5행.
- 상수: `CHARACTER_MECHANISM_GRAPH_SCHEMA` 1행, `CHARACTER_RESPONSE_RELATION_FIELDS` 5행, `CHARACTER_CONCEPT_EVIDENCE_ROLES` 11행.

이전 분석에서 현재 호출 부재, 현재 native graph projection 규격과 구 검증 API의 불일치, 설치본·보관 ZIP과 대상 원문 bytes 동등성을 확인했다. 이번에는 실제 source node SHA와 승인 목록을 다시 대조했고 원래 397행만 제외한 AST가 제거본 AST와 같음을 확인했다. private patch 역적용으로 원본 bytes가 정확히 복구된다. 원래 검증 규칙 전체가 다른 검증기에 대체됐다고 추정하는 변경은 아니다. 역사 소스와 실행 세대의 원문은 보존한다.

현재 사용하는 graph 데이터, 축 어휘와 alias, 관계 concept, public/private tag 필터, 원문·owner·permission·guard·RID 계약은 그대로다. `precore/photo_authoring_wire.py`의 동명 관계 상수는 유지한다. 자동 부정어 정책 2필드나 데이터 저장본 통합은 이번 범위가 아니다.

## 검증

작업본의 독립 private 소스에서 운영 관련 48개와 core·관계·재시도 관련 43개 검사가 skip 없이 통과해야 확정한다. BM25F 모듈이 두 그룹에 중복되므로 91개의 서로 다른 테스트로 세지 않는다. 변경 폭이 미참조 AST 삭제로 고정되어 기존 native 전체 70개 suite를 다시 실행하지 않고, 영향 경계와 관련 계약을 검증한다.

추가 smoke는 실제 사용 중인 축 alias, private-tag 제거, concept profile 복사 독립성, precore 관계 상수와 source implementation hash 일치 허용·불일치 거부를 확인한다. 원본·private 제거본·적용본의 algorithm binding은 code hash 외 설정·호출 signature가 같다. 원본 소스 fallback, 원본/cache 쓰기, 네트워크와 torch 읽기를 OS sandbox로 차단한다. 모델·assets는 APFS 독립 clone이며 원본 hardlink를 만들지 않는다.

커밋될 HEAD 기반 소스와 같은 HEAD의 tracked 테스트도 별도로 비교한다. 43개씩 실행해 **정리 전후 모두 41개 통과·같은 기존 실패 2개, 새 실패 0개**여야 한다. 이는 차등 검증 통과이며 HEAD 자체가 전체 green이라는 뜻이 아니다. 기존 contextual 관련 미커밋 수정은 이번 커밋에 포함하지 않는다. traceback 정규화는 project 경로와 완전히 같은 source line의 행 번호 대응에 한정한다.

실제 `photo_workflow.py`의 `view → retrieve → view → compose-audit → deliver`를 원본·private 제거본·원본 적용본에서 각각 수행한다. composition·lighting 목표별 **BM25F 1회·local cosine 1회**, 공통 풀 전체 **18,180 CID·18,182 RID**, 기존 top 8·전체 순서/점수 digest·전달 상태를 유지해야 한다. 기존 실제 query vector와 실행 근거를 재사용하며 새 임베딩·이미지 호출은 없다.

설치 kernel과 원래 발급 H/native 영수증의 점수·전체 순서·composition audit, frozen audit, 별도 파생 native public view, 누락·변조 거부 CLI 4개와 archive 순서 450개·실험 검사 17개를 검증한다. 과거 archive의 품질 **HOLD**는 그대로 유지하며 품질 통과로 바꾸어 해석하지 않는다. 파생 native view를 별도의 과거 원본 실행으로 세지 않는다. 원래 store가 없는 과거 실행을 다른 manifest로 임의 재결속해 성공으로 처리하지 않는다.

## 보존과 커밋

시작 보호 경로 **139,542개**, CURRENT **168개**, root의 기존 dirty/untracked **40,629경로**와 다른 worktree의 **6,161경로**를 고정했다. 직전 분석의 미커밋 17파일도 기존 작업으로 보호하며 이번 stage에서 제외한다. 이전 제거 경로 293개도 계속 부재여야 한다.

변경을 허용한 generator 외에는 bytes·mode·inode·links를 유지한다. generator도 허용 제거 전후 기존 dirty diff payload SHA가 같고, 커밋용 HEAD 기반 patch와 작업본 patch를 별도 검증한다. **generator 전체를 git add하지 않는다.** 실제 index에는 HEAD 기반 397행 삭제 patch만 적용하고 새 evidence 디렉터리만 명시적으로 추가한다. staged 경로·source blob·numstat와 cached diff 검사를 다시 확인한 뒤 로컬 커밋한다.

source/code 해시 변경을 이유로 CURRENT를 재발행하거나 guard를 완화하지 않는다. 구 native CURRENT의 code inventory와 mutable source 차이도 그대로 둔다. installed/frozen 소스·원문·벡터·모델·영수증·후보·binding 데이터와 다른 worktree를 수정하지 않는다. Gemini·새 embedding·이미지 호출, 전수 의미 검토, runtime publish, CURRENT 쓰기와 push는 없다.

`BASELINE-DELTA.json.gz`와 `PREVIOUS-PROTECTION.json.gz`는 직전 committed cleanup before/after 체인에 새로 보호한 분석 파일을 더해 baseline을 재구성한다. `INPUT-REFERENCES.json`, `INPUT-GRAPH-PRESERVED.json`은 이전 분석의 읽기 입력을 이번 evidence 안에 그대로 pin한 사본이다. 기존 분석 파일을 수정하거나 stage하지 않는다. `AFTER-DELTA.json.gz`에는 허용 source 한 개의 before/after stamp만 남긴다. private 디렉터리는 실행 scratch이며 복구의 유일한 자료가 아니다.

최종 판정은 `RESULTS.json`, `SOURCE-operating.json`, `SOURCE-related.json`, `HEAD-COMPARISON.json`, `MANAGED-*.json`, `INSTALLED.json`, `HISTORY-*.json`, `AFTER-PRESERVATION.json`, `STAGED-CHECK.json`에 기록한다. 커밋 뒤에는 실제 commit 경로·blob·parent, 기존 미커밋 상태와 전체 보호 경로/CURRENT를 다시 대조한다.
