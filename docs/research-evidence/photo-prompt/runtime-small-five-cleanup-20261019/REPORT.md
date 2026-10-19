# 미사용 함수 5개와 중복 import 2개 정리

상태: 구현·검증 완료. 이번 변경만 부분 커밋 대상으로 확정했다. push와 운영 generation 전환은 수행하지 않는다.

## 변경 범위

| 파일 | 제거한 함수 | 함수 본문 행 수 |
|---|---|---:|
| `prompt_generator.py` | `character_axis_value_classes` | 2 |
| `prompt_generator.py` | `cosine_similarity` | 9 |
| `prompt_generator.py` | `core_focal_hit_supported` | 6 |
| `prompt_generator.py` | `filter_authorial_negative_entries` | 21 |
| `audit_composed_prompt.py` | `english_prompt_word_count` | 3 |

`photo_runtime_sources.py`에서는 `import photo_shared_views`와 `SearchReader` import 바인딩만 제거했다. `LazyRuntimeData`, `identity`, 실제 검색 reader 및 shared view 모듈은 보존한다. 함수 41행과 import 변경을 합친 소스 diff는 1행 추가·43행 삭제다. 함수 밖의 나머지 AST가 같은지 별도로 검증했다.

직전 참조 조사에서 고정한 범위를 사용했다. 작업 소스·테스트 187개, 다른 보존 Python 9,676개, 유지보수 Python 48개, archive Python 114개를 조사한 결과를 SCOPE.json에 추출했다. 이 다섯 함수에는 현재 작업 소스의 named load/import/직접 문자열 소비자가 없다. 임의의 외부 동적 호출까지 부재를 증명한 것은 아니다. 과거 frozen 구현과 source ZIP에는 손대지 않는다.

## 기존 작업 보존과 부분 커밋

출발 HEAD는 `729365bfeadddc02740148eba1c33901c3aae9d4`다. 시작 시 루트의 변경·미추적 경로는 40,537개, 다른 작업 트리는 6,161개였다. CURRENT 168개를 포함해 139,289개 경로의 바이트·모드·inode·링크 상태를 BASELINE.json.gz에 저장했다.

`prompt_generator.py`와 `audit_composed_prompt.py`에는 원래 미커밋 변경이 있다. 두 파일 전체를 stage하지 않는다. 현재 작업본에 적용할 WORKING.patch와 HEAD에서 만들 INDEX.patch를 따로 고정했다. 각각에 동일한 함수 삭제만 적용하고, 삭제 전후의 기존 미커밋 변경 내용이 정확히 같은지 위치를 제외한 diff payload 해시로 검증했다. 원래 변경의 본문은 이 증거에 복사하지 않는다.

실제 index에 적용하기 전, 별도 임시 index에서 INDEX.patch를 적용해 정확한 3개 소스 blob과 1/43행 범위를 확인했다. 다른 신규 stage 대상은 이번 전용 helper와 증거 디렉터리뿐이다. 직전 분석의 미추적 파일도 기존 작업으로 취급해 stage하지 않는다. 이번 요청에서는 push하지 않는다.

## 검증 범위와 한계

- 임시 수정본은 현재 작업 소스 76개와 필요한 비 Python 메타데이터를 복사했다. 모델·assets는 독립 APFS clone이며 원본 hardlink를 사용하지 않는다. 원본 소스 읽기 fallback, 원본 쓰기, 네트워크와 torch 읽기를 차단하고 고정 Python으로 실행한다.
- 운영 검색 48개와 native 70개 회귀를 각각 별도 임시 프로젝트에서 실행한다. 결과 파일의 실제 로딩 경로와 세 소스 SHA가 수정본과 일치해야 통과한다. skip을 허용하지 않는다.
- 실제 H 단독+F2 CLI의 `view → retrieve → view → compose-audit → deliver`를 정리 전/후와 실제 적용본에서 검증한다. composition·lighting 두 목표 각각 BM25F 1회와 local cosine 1회, top 8 및 전체 CID 순서·점수 digest, 전달 완료 상태를 비교한다. 기존 query vector를 재사용하므로 새 임베딩 추론을 수행하지 않는다.
- 원래 설치된 검색 kernel·영수증과 frozen native 실행을 별도로 검사한다. 원래 설치 구현은 변경된 작업 소스로 대체하지 않는다. 공개 native view는 원래 실행에서 파생한 임시 workflow로 비교하며, 이를 새로운 과거 원본 실행으로 세지 않는다.
- archive에서 과거 225개와 최신 225개 검색 순서, 평가 테스트 17개를 재생한다. 과거 품질 판정 HOLD도 그대로 재현해야 한다. 검증 PASS는 과거 실험의 품질 통과를 뜻하지 않는다.
- 누락 실행, checksum 불일치, 발급 영수증 누락, generation 변조의 실제 CLI 부정 사례 4개는 기존 거부 결과를 유지해야 한다.

### HEAD 기반 별도 검사에서 확인한 기존 실패

현재 작업본의 회귀와 별개로, 커밋할 HEAD 기반 소스도 검증했다. 첫 시도는 HEAD 소스와 현재 테스트를 결합했고 contextual footprint 테스트 2개가 실패했다. 이후 초기 HEAD의 테스트까지 맞춰 검사해도 같은 두 실패가 있었다. 따라서 테스트 입력의 시점 차이만으로 생긴 실패가 아니라, 출발 HEAD 자체의 기존 실패다. 각 시도의 원문은 HEAD-SOURCE-ATTEMPT01/02.json에 남겼다.

초기 HEAD 소스·테스트와 이번 삭제만 적용한 소스·동일 테스트를 각각 실행한 결과, 각 15개 중 13개 통과·2개 실패였다. 실패 test ID와 경로만 정규화한 traceback·assertion 전체가 정확히 같고 새 오류/실패가 없었다. HEAD-SOURCE.json의 PASS는 이 차등 비교를 뜻하며, 15개 전체 통과를 뜻하지 않는다. 실제 작업본에는 이 동작과 관련된 기존 미커밋 수정이 있으며, 해당 수정은 이번 커밋에 포함하지 않는다.

## 이번에 보류하는 항목

`validate_character_mechanism_graph` 370행과 그 내부에서 참조하는 `character_runtime_node_topic_ids`, `character_runtime_node_family_ids` 각 5행은 함께 후속 검토해야 하므로 유지한다. 수동 source 검증기, provider/과거 Gemini trace 처리, bytecode 21개, 구 shard 5세대, 과거 미존재 store 41개와 대체 manifest 7개도 범위를 넓혀 제거하지 않는다.

작업 소스의 구현 해시가 바뀌어도 CURRENT를 새 구현으로 전환하지 않는다. 기존 루트 native CURRENT의 74개 코드와 현재 소스 76개 사이의 차이도 이번에 해소하거나 해시 검증을 약화하지 않는다. Gemini·새 임베딩·이미지 생성 호출, 전수 의미 검토, 운영 generation 발행은 수행하지 않는다.

## 최종 결과

현재 작업본 기준 운영 검색 48개·native 70개, 합계 118개가 skip 없이 통과했다. HEAD 기반 별도 차등 비교는 각 13개 통과·기존 2개 실패를 동일하게 유지했다. 실제 CLI 3개 arm × 5개 명령, 설치 kernel·frozen audit·파생 native view 비교, archive 검색 순서 450개와 테스트 17개, 부정 CLI 4개도 요구한 결과를 유지했다.

적용 후 원본 139,289개 보호 경로를 전수 대조했다. 허용한 세 소스의 정확한 수정본 외에는 바이트·메타데이터가 같고, CURRENT 168개와 기존 삭제 cache의 부재도 보존됐다. 원래 두 소스 파일의 미커밋 diff payload는 그대로다. 적용 후 결과의 SHA와 근거는 RESULTS.json과 AFTER-PRESERVATION.json에 있다.
