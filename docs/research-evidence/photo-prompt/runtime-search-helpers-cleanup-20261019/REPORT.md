# 미사용 import 바인딩 6개와 구 검색 함수 4개 정리

상태: 승인 범위 구현·검증 완료. RESULTS.json과 적용 후 검증이 모두 PASS이며 이번 변경만 로컬 커밋 대상으로 확정했다. push와 CURRENT 전환은 수행하지 않는다.

## 구현 범위

소스 6파일에서 import 바인딩 6개와 구 검색 helper 4개·131행을 제거한다. Git 기준 4행 추가·136행 삭제, 순감소 132행이다. 경로는 `skills/photo-prompt-image-generator/` 기준이다.

| 파일 | 제거한 항목 |
|---|---|
| `scripts/photo_global_index.py` | `atomic` import |
| `scripts/photo_retry_projection.py` | `digest`, `encode` import |
| `scripts/prepare_retry_context.py` | `save_state` import |
| `precore/prepare_photo_run.py` | `bound_path` import |
| `precore/photo_authoring_wire.py` | `SUBJECT_CATEGORIES` import |
| `scripts/prompt_generator.py` | `_bm25f_lexicon_from_documents`, `candidate_pack_float`, `candidate_pack_assertion_discovery`, `authorial_core_bm25f_query_fields` |

공급 모듈의 다른 import를 같은 문장에 유지하므로 provider의 eager import와 실제 함수·상수·오류 타입은 그대로다. 같은 이름의 원래 provider 정의를 삭제하지 않는다. 현재 H 단독+F2의 query·index·BM25F/local cosine 경로와 공통 풀 전체 검색을 유지한다.

원본에서 승인한 import·함수만 제외한 AST와 제거본 AST가 같고, private patch 역적용 시 원본 bytes가 정확히 복원된다. 직전 분석에서 고정한 HEAD/작업본 제거본 SHA와 이번 후보 SHA가 일치한다. 해당 분석의 current/preserved/archive 참조 조사와 43개×4조건 제한 검사 결과는 입력 근거이며 이번 전체 검사를 대신하지 않는다. 원본 분석 파일은 기존 미커밋 작업으로 보호하고 stage하지 않는다.

## 검증

현재 작업본의 독립 private 소스에서 운영 회귀 48개, native 회귀 70개, closed retry context 8개, 총 126개가 skip 없이 통과해야 확정한다. 모델·assets는 APFS 독립 clone이며 hardlink하지 않는다. 고정 Python과 `-I -B`를 사용하고, 원본 scripts/precore 읽기 fallback·원본과 cache 쓰기·네트워크·torch 읽기를 OS sandbox로 차단한다. 실제 로딩 경로·SHA와 제거 대상 부재, 코드 76개 및 일치 구현 허용·불일치 구현 거부를 확인한다.

원본·private 제거본·원본 적용본에서 실제 `photo_workflow.py`의 `view → retrieve → view → compose-audit → deliver`를 각각 실행한다. composition·lighting 목표별 BM25F 1회·local cosine 1회와 top 8·전체 순서/점수 digest·전달 완료 상태가 동일해야 한다. 기존 query vector를 재사용하며 새 임베딩 추론은 없다. `prepare_photo_run`과 `prepare_retry_context`의 `--help`도 원본/제거본 출력이 동일해야 한다.

원래 설치된 kernel과 발급 영수증은 전체 CID 18,180개·RID 18,182개 검색의 점수·전체 순서가 같다. frozen audit·별도 파생 native public view·archive 검색 순서 450개와 평가 검사 17개, 누락/변조 거부 CLI 4개를 확인한다. archive의 기존 품질 HOLD를 그대로 재현하며 품질 통과로 바꾸어 해석하지 않는다. 파생 native view는 새 과거 원본 실행으로 세지 않는다.

커밋될 HEAD 기반 소스와 같은 시점의 tracked 테스트로 43개를 별도 비교한다. 정리 전후 각각 41개 통과·기존 실패 2개이며 실패 ID·내용이 같고 새 실패/오류가 없어야 한다. 현재 작업본의 contextual 관련 미커밋 수정은 이번 커밋에 포함하지 않는다. traceback 정규화는 프로젝트 경로와 정확히 같은 source line의 행 번호 대응에 한정한다.

## 보존과 커밋

보호 경로 139,480개와 CURRENT 168개를 원본 적용 전후 대조한다. 허용한 6소스 수정본 외에는 bytes·mode·inode·links를 유지한다. 루트의 기존 변경/미추적 40,612경로와 다른 worktree 6,161경로를 보호하며, 직전 분석의 미추적 26파일도 이번 stage에서 제외한다. 이전 제거 경로 293개도 계속 부재여야 한다.

generator의 기존 미커밋 변경은 HEAD 기반 index patch와 작업본 patch로 분리한다. 변환 전후 기존 dirty diff payload SHA가 같고, private index의 staged source blob이 HEAD 기반 후보와 정확히 같으며 소스 diff가 4행 추가·136행 삭제임을 확인한다. 실제 stage도 그 index patch와 이번 helper·증거만 허용한다. 파일 전체를 stage하지 않는다.

이번 소스와 검증 자료만 로컬 커밋한다. 기존 후보 데이터·installed/frozen source·영수증·모델·archive·다른 미커밋 수정은 함께 커밋하지 않는다. source 해시 변경을 이유로 CURRENT를 재발행하거나 구현 불일치 거부를 약화하지 않는다. 기존 native CURRENT의 코드 74파일과 작업 소스 76파일 차이는 그대로 둔다.

구 그래프 3함수·상수 3개, 수동 `validate_visual_profile_source`, 실제 사용하는 `compile_context` 재export, qualifier import 3개·오류 타입 reexport 2개, bytecode 21개, root shard 5세대, 원래 store가 없는 과거 실행 41건과 대체 manifest 7개는 이번 제거 범위가 아니다. Gemini·새 임베딩·이미지 생성 호출, 전수 의미 검토, 운영 generation 발행, CURRENT 쓰기와 push는 없다.

`BASELINE-DELTA.json.gz`와 pinned `PREVIOUS-PROTECTION.json.gz`는 직전 cleanup의 committed 보호 체인에 추가 26경로를 더해 시작 상태를 재구성한다. `AFTER-DELTA.json.gz`는 허용 소스 6개의 before/after stamp만 기록한다. private 폴더는 실행 scratch이며 복구의 유일한 자료가 아니다. 완료 evidence는 덮어쓰지 않는다. 최종 상태는 RESULTS.json, SOURCE-*.json, RETRY.json, HEAD-COMPARISON.json, MANAGED-*.json, HISTORY-*.json, AFTER-PRESERVATION.json, STAGED-CHECK.json으로 확인한다.

## 최종 결과

현재 작업본 126개가 skip 없이 통과했다. 원본·private 제거본·원본 적용본의 CLI 15명령, installed/frozen·archive 검색 순서 450개·평가 검사 17개·부정 CLI 4개가 요구 결과를 유지했다. HEAD 비교는 각 41개 통과·동일한 기존 실패 2개와 새 실패 0개다. 원본 적용 후 보호 139,480경로와 CURRENT 168개 대조가 통과했고, generator의 기존 dirty diff payload도 보존했다. 이번 소스 diff는 정확히 4행 추가·136행 삭제다.
