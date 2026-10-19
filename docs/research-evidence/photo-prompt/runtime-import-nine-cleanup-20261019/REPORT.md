# 미사용 import 9개와 지역 변수 1행 정리

상태: 구현·검증 완료. 검증한 소스 10행 삭제와 이번 helper/증거만 로컬 커밋 대상으로 확정했다. push와 CURRENT 전환은 수행하지 않는다.

## 구현 범위

| 소스 파일 | 제거 대상 | 삭제 행 수 |
|---|---|---:|
| `photo_contracts.py` | `hashlib`, `json`, `Any` import | 3 |
| `photo_embodiment.py` | `copy`, `hashlib`, `json`, `Any` import | 4 |
| `photo_shared_views.py` | `Path`, `photo_global_index as index` import | 2 |
| `photo_runtime_sources.py` | `algorithm_binding()` 안의 미사용 `get = ...` 할당 | 1 |

네 파일은 `skills/photo-prompt-image-generator/scripts/` 아래 있다. 합계는 소스 0행 추가·10행 삭제다. 함수 signature, 정책·환경·검색 recipe와 실제 계약 함수는 그대로다. 제거한 지역 변수는 생성한 뒤 읽거나 반환하지 않는 closure였다. generator module·dict·None 입력의 algorithm binding은 같고, 정리 전후 code 항목을 제외한 metadata도 같다. code 목록의 해시는 소스가 바뀌므로 달라지는 것이 정상이다.

각 소스는 정리 전에 깨끗했고 초기 HEAD `c212466cd97b5781d6c654b3a9617353f97811be`와 바이트가 같았다. AST에서 승인한 import 문과 할당만 제거했을 때의 나머지 AST와 실제 수정본이 같다. private patch를 역적용하면 원본 bytes로 정확히 돌아오는 것도 확인했다.

직전 분석의 권고 범위만 적용한다. 그 분석에서 현재 source/test 187개, 다른 보호 Python 9,681개, tools Python 49개, 검증한 archive Python 114멤버를 조사했고 해당 import 바인딩 9개의 named 소비자는 0개였다. 문서·shell·설정 3,155개에서도 이 바인딩의 qualified 사용은 없었다. 임의 외부 소비자나 일반적인 module object escape까지 부재를 증명한 것은 아니다. 모듈 자체와 실제 reexport 소비자가 있는 `photo_contextual_appeal.compile_context`는 보존한다.

## 검증

현재 작업본을 복사한 독립 private 프로젝트에서 운영 검색 48개와 native 70개 회귀를 실행한다. 모델·assets는 원본과 다른 APFS clone이고 hardlink를 만들지 않는다. 필요한 precore JSON 등 비 Python 입력도 복사한다. 고정 Python과 `-I -B`를 사용하고 원본 scripts/precore 읽기 fallback, 원본과 cache 쓰기, 네트워크와 torch 읽기를 차단한다. 실제 로딩한 네 소스 경로와 SHA가 정리한 수정본과 맞고 skip이 없어야 통과한다.

정리 전·private 수정본·원본 적용본에서 실제 `photo_workflow.py`의 `view → retrieve → view → compose-audit → deliver`를 실행한다. 기존 발급 run을 임시 복제하고 실제 query vector를 재사용하며 composition·lighting 두 목표 각각 BM25F 1회·local cosine 1회를 유지하는지 확인한다. top 8과 전체 CID 순서·점수 digest 및 전달 완료 상태를 비교한다. 공통 후보풀 전체 검색을 유지하며 새 임베딩 추론은 하지 않는다.

원래 설치된 kernel·발급 영수증·frozen native audit, archive에서 과거 225개와 최신 225개 검색 순서 및 평가 검사 17개, 누락/변조 거부 CLI 4개도 별도로 검증한다. archive의 기존 품질 HOLD는 그대로 재현해야 한다. 검증 PASS를 과거 실험의 품질 통과로 해석하지 않는다. 공개 native view는 원래 실행에서 파생한 임시 workflow의 비교이며 새로운 과거 원본 실행으로 세지 않는다.

### 기존 미커밋 코드와 HEAD 검사 구분

기존 작업을 포함한 현재 source의 회귀와, 커밋될 HEAD 기반 소스를 따로 비교했다. HEAD 소스·동일 시점의 tracked 테스트로 검사 35개를 실행한 결과 정리 전후 각각 33개 통과·기존 실패 2개였다. 실패 test ID와 project 경로만 정규화한 traceback·assertion 내용이 정확히 같고 새 실패/오류는 없다. `HEAD-COMPARISON.json`의 PASS는 이 차등 검증을 의미하며 35개 전체 통과를 뜻하지 않는다. 현재 작업본에 있는 contextual 동작 관련 미커밋 수정은 이번 커밋에 포함하지 않는다.

## 보존과 커밋 범위

보호 기준은 139,351개 경로와 CURRENT 168개다. 루트의 기존 변경·미추적 40,561경로, 다른 worktree의 6,161경로를 보존한다. 직전 분석 디렉터리의 미추적 24개 파일도 기존 작업으로 취급하며 이번 stage 대상에서 제외한다.

stage allowlist는 깨끗했던 소스 4개, 이번 helper `tools/photo_runtime_maintenance/imports_cleanup.py`, 이번 증거 디렉터리뿐이다. 기존 generator/audit 파일을 stage하지 않는다. 커밋 직전에 네 source blob이 검증한 SHA와 같고, 소스 diff가 정확히 0/10행인지 검사한다. 새 증거를 제외한 원래 Git 상태와 CURRENT는 대조하고 이전에 지운 camera 모듈·bytecode도 다시 생기지 않아야 한다. 이번 요청에서는 로컬 커밋만 수행하고 push하지 않는다.

원본 적용 후 source 네 파일의 정확한 수정본을 제외한 보호 경로 전체를 다시 대조한다. 운영 설치본·frozen source·source archive·영수증·모델과 실제 후보 데이터는 그대로 둔다. 소스 구현 해시 변경을 이유로 CURRENT를 바꾸거나 코드 불일치 거부를 약화하지 않는다. 기존 루트 native CURRENT의 코드 74개와 현재 작업 소스 76개 차이도 이번에 해소하지 않는다.

남은 함수 후보 11개·549행, 추가 상수·import 후보, 수동 시각 프로필 원본 검증기, provider와 과거 Gemini 응답/공간 검증·명시적 transport, bytecode 21개, root shard 5세대, 원래 store가 없는 과거 실행 41건과 대체 manifest 7개는 이번 제거 범위가 아니다.

Gemini·새 임베딩·이미지 생성 호출, 전수 의미 검토, 운영 generation 발행과 CURRENT 쓰기는 수행하지 않는다. `BASELINE-DELTA.json.gz`는 커밋된 small-five baseline/AFTER-DELTA에 추가 경로 62개의 stamp와 기존 Git 상태를 더해 보호 기준을 재구성한다. private 실행 폴더는 진행용 scratch이며 복구의 유일한 자료가 아니다.

## 최종 결과

현재 작업본의 운영 검색 48개·native 70개, 총 118개가 skip 없이 통과했다. 실제 CLI는 세 조건 × 각 5개 명령 모두 통과했고, 공통 후보풀 전체와 슬롯당 BM25F/local cosine 1회 및 기존 점수·순서를 유지했다. installed/frozen·파생 native view·archive 검색 순서 450개와 검사 17개·부정 CLI 4개도 요구한 결과를 유지했다. HEAD 기반 35개 비교는 각 33개 통과와 동일한 기존 실패 2개를 유지했다.

원본 적용 후 139,351개 보호 경로 전수 대조가 통과했다. 허용한 네 source 수정본 외에는 바이트·메타데이터가 그대로이며 CURRENT 168개와 기존 미커밋 작업도 보존됐다. 상세 결과는 RESULTS.json과 AFTER-PRESERVATION.json에 기록했다.
