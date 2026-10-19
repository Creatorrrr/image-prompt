# 미사용 함수·과거 재현 분리 실행 결과

2026-10-19 · 8단계 처리·단계별 로컬 커밋 · 운영 소스 변경 0 · 삭제 0 / 보류 9

**별도 오프라인 재현·과거 증거 검증 도구를 추가했다. 미사용 함수 9개의 실제
삭제와 운영 provider/공개 routing 변경은 보류했다.** 레거시 제거 전체가 완료된
결과는 아니다. H 단독+F2, 기존 작업과 CURRENT는 유지했다.

## 적용한 변경

- `native_replay.py`: 원래 발행된 native receipt, pack/source binding, 세대
  manifest와 코드 집합을 검증한다. `verify`는 전체 세대 member hash를 확인하고,
  `audit`는 검토한 원래 코드로 receipt 재계산·구성 감사를 실행한다.
- `historical_evidence.py`: 기존 Gemini RESULT와 원시 응답을 원래 source archive의
  검증기로 읽는다. 과거 증거 읽기를 새 원격 요청과 분리한 명시적 유지보수 명령이다.
- 검증·보호 도구와 문서를 추가했다. 현재 검색 경로는 이 도구들을 자동 호출하지 않는다.
  운영 소스의 물리적인 분리와 기존 공개 명령의 routing 교체는 적용하지 않았다.

실행기는 네트워크·원래 프로젝트/공유 runtime 쓰기를 OS sandbox로 차단한다.
재현 감사에서는 현재 scripts/precore 읽기와 새 임베딩 요청도 막는다. 검토한
설치 소스 94개 및 보존된 native 소스 74개의 코드 집합만 실행할 수 있다.
원래 코드 대신 미등록 bytecode·확장 모듈을 읽는 경로도 차단한다. 자체 manifest와
receipt가 일치하더라도 미등록 코드는 실행하지 않는다. 원본/의존성이 없으면
거부/보류하고 현재 소스나 다른 세대로 넘어가지 않는다.

현재 H 세대 `663038595155d8d48bfa20339bbe7a5c3128eea4ce504900c9a8fdadd34c152b`,
native 세대 `9649504ffbcd1ebe7d9aedf9eab821fc18aa0300a8f70b65dbdd145b435ec1da`,
코드 집합 hash `493f1830db1f564c8acfe0218a24c8445990aa3ec968b948e80d187cfa9f7f90`는
동일하다. 새로운 세대 발행·운영 전환·재임베딩은 없다.

## 단계별 처리

| 단계 | 실제 결과 | 로컬 커밋 |
|---|---|---|
| 1 보호 고정 | 139,072경로·CURRENT 168개·함수 9개 baseline | `4968692d7` |
| 2 소비자 분류 | 현재 코드/테스트와 과거 사본/archived 코드 구분 | `731e51d37` |
| 3 재현 경계 | 별도 frozen 감사 도구·실제 원래 run 감사 통과, 공개 routing 보류 | `37dcd3d22` |
| 4 제거 실험 | 세 묶음 및 전체 제거가 기존 지문 검사에 거부됨, 실제 삭제 9개 보류 | `45b9ecf68` |
| 5 과거 책임 | 과거 receipt 검증 도구·문서 추가, live provider 변경 보류 | `a3b49e8d9` |
| 6 공개 명령 | 기존 운영 48개·CLI 5명령·새 CLI 실패 4종 통과 | `271bbbc8c` |
| 7 통합 검증 | native 70개·설치본 대조·archive 재현·실행 코드 허용 목록 보강 | `582043a48` |
| 8 결과/보존 | 이 보고서·함수별 보류·계획 상태·최종 보존/커밋 범위 확인 | 이 보고서의 커밋 |

각 단계는 해당 구현 또는 보류 판정의 검증 후 이번 경로만 stage하여 커밋했다.
기존 미커밋 source 파일 전체를 stage하지 않았다. push는 하지 않았다.

## 함수 9개가 남은 이유

현재 scripts/precore/tests 188파일에는 대상 함수의 정적 호출이 없었다. 보호된
과거 소스 9,706파일과 archive Python 114파일까지 확장하면 예전 사본 안에는
호출이 있다. 같은 함수가 과거 사본에 있다는 이유로 그 사본을 지우지 않았다.
기존 authored literals 원문 1개는 파싱되지 않았지만 대상 함수명의 직접 텍스트는
없었고, 원문을 수정하거나 조사 성공으로 재분류하지 않았다.

8개가 있는 `prompt_generator.py`는 원래 미커밋 변경 중이지만 후보 함수 AST는
HEAD와 같았다. HEAD 기준 제거 patch를 원래 작업 소스의 private 복사본에
적용한 결과가 함수 삭제만 수행한 결과와 같고, 역적용하면 원래 bytes가 정확히
복원됐다. 따라서 기존 변경과 patch를 구분할 수 없어서만 보류한 것은 아니다.

주된 문제는 **함수 호출 여부와 별개로 Python 파일 전체가 source/algorithm
지문에 들어가는 계약**이다. 원래 CURRENT 세대의 소스 74개를 그대로 복사한
대조군은 실제 `_require_implementation()` 검사와 알고리즘 일치 검사를 통과했다.
아래 소스 변경을 가한 복사본은 모두 `runtime_restart_required`로 거부됐다.

- camera 1개 제거
- Gemini 보조 4개 제거
- 검색/후보 보조 4개 제거
- 9개 전체 제거
- scripts에 작은 재현 경계 모듈 추가
- provider transport 본문을 바꾸거나 설정 누락 시 Gemini 기본값을 없애는 probe

마지막 provider probe는 지문 영향만 확인한 실험이며, 기능 검증을 통과한 provider
리팩터링은 아니다. 검사 예외나 지문 제외 규칙을 추가하지 않았다. CURRENT와
기존 공개 native 계약을 바꾸지 않는 조건에 따라 실제 소스 변경을 보류했다.

추가로, 현재 작업 소스 77개는 이미 CURRENT의 74개와 다르다. 시작 전부터 있던
차이는 `build_photo_slot_intents.py`, `install_photo_h_f2_runtime.py`,
`photo_installed_h_f2.py` 추가와 `photo_workflow.py` 변경이다. 이번 변경으로 생긴
문제로 보고하지 않으며 이를 고치기 위해 CURRENT를 전환하지 않았다. 맞춘
대조군과 변경군을 따로 실행해 기존 불일치와 제거의 영향을 구분했다.

| 함수 | 최종 처리 |
|---|---|
| `legacy_camera_clauses` | DEFER_CURRENT_IMPLEMENTATION_BINDING |
| `get_gemini_api_key` | 위와 같음 |
| `cached_gemini_client` | 위와 같음 |
| `extract_embedding_values` | 위와 같음 |
| `round_embedding_vector` | 위와 같음 |
| `_bm25f_lexicon_from_documents` | 위와 같음 |
| `candidate_pack_float` | 위와 같음 |
| `candidate_pack_assertion_discovery` | 위와 같음 |
| `authorial_core_bm25f_query_fields` | 위와 같음 |

`ACTION-LIST.json`에 함수별 원문/AST hash와 이유가 있다. `PROPOSED-REMOVALS.patch.gz`는
미적용 proposal이다. 압축을 푼 bytes의 hash와 private 적용/역적용 증거는
`PATCH-PROOF.json`에 있다. 봉인된 설치본과 기존 source archive는 원문 그대로다.

## 검증 결과와 증거 범위

| 검사 | 결과 |
|---|---|
| 기존 operating 회귀 | 48개 통과 |
| 기존 native 회귀 | 70개 통과, skip 0 |
| 새 재현 도구의 receipt·코드·실행 경계 | 최종 16개 통과 |
| 실제 설치된 H-F2 | 기존 2목표의 BM25F·cosine 점수와 전체 순서 완전 일치 |
| 일반 H-F2 CLI | 기존 run view, 새 retrieve/view/compose-audit/deliver 5명령 통과 |
| 검색 예산 | 목표마다 BM25F 1회·local cosine 1회, 기존 query vector 재사용 |
| 과거 평가 archive | 저장 순서 225+225=450개, 전용 검사 17개 통과 |
| 실제 원래 native receipt·구성 감사 | 설치 run 1건, 최종 실행 코드 정책으로 재실행 통과 |
| 새 재현 CLI 실패 경로 | 원본 run/issued receipt 누락·receipt/manifest 변조 4종 거부 |
| 과거 Gemini 증거 | 기존 RESULT/원시 응답 3건 일치, 원래 검증기로 손상 증거 4종 거부 |
| 원본 보존 | 139,072경로 및 추가 과거 증거 6개 전수 stamp 대조 통과 |

설치본 대조는 공통 positive 풀 18,180 CID / 18,182 RID를 고려했다. 슬롯 태그나
native admission으로 material 검색 대상을 줄이지 않았고, H 단독+F2·RRF10·top8·
CID 중복 제거와 원래 receipt/구성 감사 결과를 유지했다. 실제 설치 코드 검사와
현재 작업 소스 검사는 별도 실행이며 서로 대체하지 않았다.

기존 검사에 모델·transport를 대체하는 오프라인 fixture가 있다. 원본 runtime에서
새 Gemini/임베딩/이미지 요청을 실행한 결과가 아니다. native 테스트가 만드는
generation/CURRENT와 run 변경도 private fixture 안에서만 일어난다.

원래 store가 없는 과거 실행 41건은 실제 재현 성공으로 세지 않았다. 해당 원본,
대체 세대 manifest 7개, 고유 입력/출력·receipt는 보존했다. 모든 과거 실행이나
이미지 품질을 전수 검증한 결과는 아니다. 검색 품질을 새로 개선했다고 주장하지 않는다.

## 기존 작업·CURRENT·운영 보존

전체 보호 검사는 `VERIFY-07.json`, 단계별 source/config/cache·pointer·Git 상태 검사는
`CHECKPOINT-03`부터 `CHECKPOINT-08.json`까지 확인한다. main의 원래 변경/미추적
40,478경로와 별도 작업 트리의 6,161경로 상태를 유지했다. 다른 작업 트리의 HEAD/index,
원래 staged 상태, 운영 source 77개와 설정, 원래 CURRENT 168개도 같다.
운영 Python 원문·후보 데이터·모델·설치 선택·세대·원래 run에는 이번 diff가 없다.

bytecode 21개, root shard 5세대와 기존 보류 store는 이동·삭제하지 않았다.
Gemini 호출·새 임베딩 추론·새 의미 판정·CURRENT 전환은 0회다. 커밋의 경로는
이 작업의 도구·문서·증거 allowlist에 속하는지 별도로 확인했다.

## 재사용 방법과 남은 일

원래 run의 자료가 있는 경우 프로젝트 루트에서 다음을 사용할 수 있다.

```sh
python3 -B tools/photo_runtime_maintenance/native_replay.py inspect --run RUN
python3 -B tools/photo_runtime_maintenance/native_replay.py verify --run RUN
python3 -B tools/photo_runtime_maintenance/native_replay.py audit --run RUN
python3 -B tools/photo_runtime_maintenance/historical_evidence.py --result RESULT_JSON --output /tmp/new-history-check.json
```

기존 `SOURCE-LOCK.json`과 source/실험 archive를 재사용한다. 같은 원문 전체를
새 archive에 복제하지 않았다. 자세한 실행 경계는
`docs/research-archives/photo-prompt/REPLAY.md`에 있다.

`NATIVE-final-progress.json`의 private 로그 경로는 실행 중 진척 확인용이다.
해당 임시 경로가 사라져도 전체 stderr·70개 결과는 `NATIVE-final.json`에 남는다.
이 임시 경로를 새로운 재현 의존성이나 유일한 원본으로 취급하지 않는다.

향후 실제 함수 제거와 provider 분리를 적용하려면 코드 지문·과거 실행 소유 경계를
어떻게 승계할지 먼저 해결해야 한다. 현재의 CURRENT/봉인/공개 native 계약 보존
조건을 유지한 채 통과하지 못한 변경을 이번 작업에서 강제 적용하지 않았다.
