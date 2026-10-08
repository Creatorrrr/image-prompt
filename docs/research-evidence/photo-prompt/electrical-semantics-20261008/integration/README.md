# 전기 시각 의미 데이터 반영 및 독립 이미지 평가

2026-10-08. 연구 카드의 실제 채택, 최신 런타임 정합성, 후보 노출·선택,
프롬프트 증거와 원본 이미지 평가를 구별해 기록한다.

## 실제 데이터 반영

- 연구 116개 카드 중 91개 채택: P0 24개 전부, P1 47개, P2 20개.
- 후보 98개, 새 시각 의미 프로필 97개, 20개 기존 슬롯 사용.
- 오로라의 horizon/arc/curtain/rays는 기존 `auroral_arc_curtain_atmosphere`
  프로필과 전체 의무를 재사용한다. 기존 후보·프로필은 덮어쓰지 않았다.
- 전압/전류 계기, 창/검/채찍, 외부 방벽/표면 갑옷, 채널 색, 왕관/제단/피부
  표식처럼 소유·연결이 다른 family는 별도 원자로 나눴다.
- 25개는 보류했다. 시간 연속 기록, 보고된 구상 발광의 물리적 정체,
  전문 도해·임상 설정 및 목적·비유·음성만으로 뜻이 정해지는 항목을
  generic 전기 형상으로 대체하지 않는다. 전체 처분은
  [ADOPTION-LEDGER.json](ADOPTION-LEDGER.json)에 있다.
- 채택 카드가 연결된 원문 seed는 184개다. 원문 435개 각각의 의미를 전부
  독립적으로 검증하거나 런타임에 승격했다는 뜻은 아니다.

원본은 `skills/photo-prompt-image-generator/assets/`의
`photo_prompt_electrical_relations_extension.json`과
`photo_prompt_visual_obligations_electrical_relations.json`이다.
두 파일을 중앙 source manifest에 required extension으로 등록했다.
기존 manifest 행과 등록 순서는 그대로 보존했다.

Runtime source에는 긍정 시각 요소, directed owner relations, 명시적 effects,
전체 opt-in evidence와 native gates를 넣었다. 연구 URL·출처 ID·보류 상태는
별도 evidence ledger에 남겼다. Broad electricity/번개/색/비유는 특정
방전 subtype의 hard duty를 자동 생성하지 않는다. Approximate discovery도
선택 가능한 제안이며, 선택한 프로필의 전체 의무를 생략할 수 없다.

## Effects 검토와 수정

첫 실제 pack 조회에서 `target: * / property: *` 조합은 모든 얼굴·헤어
property anchor와 교차 충돌했다. 조합 및 이미지 호출 전에 그 pack을
superseded pre-render로 보존하고 원본 source를 수정했다.

현재는 아직 해소되지 않은 instance owner에 wildcard target을 유지하면서
emission/light_source, apparatus/topology/object_inventory, hair/hairstyle,
skin/marking, surface/damage 등의 검토한 property domain을 선언한다.
전극·장치·매질을 도입할 수 있는 후보에는 setting 등 간접 effects도 넣었다.
얼굴·헤어를 바꾸지 않는 방전은 참조 appearance lock과 양립하고,
머리카락 geometry 변경이나 같은 피부 marking 변경은 해당 lock을 우회하지
못한다. Carrier dimension을 옮겨도 동일 property 충돌은 보존한다.

현재 consumer는 문자열 path overlap을 검사하며 자연어 역할을 실제 object
ID에 해소하는 엔진이 아니다. 이 선언의 구조적 검증과 현재 회귀 결과를
의미적 진실의 증명으로 확장하지 않는다. 실제 선택 시 final scene의 같은
전극·구름·유리·표면에 관계가 붙었는지는 author가 별도로 검토한다.

전압/전류 family의 parallel/series 구별은 원 연구 S40과
[Fluke 계기 설명서의 제조사 공개 텍스트](https://media.fluke.com/e76c91b6-f364-48ea-9c09-b10800bed531_original%20file.pdf)
로 보강했다. 이번 추가 확인 범위는 검색에 노출된 제조사 문서 텍스트이며,
해당 PDF 전체 그림을 별도 검토했다는 뜻은 아니다. 데이터는 관측 연결과
표시 단위의 일치를 기술하고, 작업 절차나 측정값의 사실성을 주장하지 않는다.

## 인덱스와 검증

- Gemini `gemini-embedding-2`, 768 dimensions, batch size 1.
- Semantic index: 10,888 entries, 16 shards. 최종 effects 수정 때
  10,888개 동일-text vector를 재사용했고 전체 BM25F/source binding을 재생성했다.
- Visual index: 2,645 profiles, 5,261 exact terms. 원본 registry에 맞게 갱신.
- Dictionary validator와 visual deep check PASS. Publisher가 semantic/visual
  deep validation과 slot BM25F를 검증한 후 immutable generation을 활성화했다.
- 최종 generation:
  `2834651af2b0ea5161d8a8cc743ff23525b6479a89a30bcda7ee6af05b632da6`
- Source fingerprint:
  `4ab1a58fdb72b9bcad7e3a934410acc9c555202f7942f62c8a7b2b6dae68674c`
- 전기 owner/혼동/선택/lock 회귀 11개 PASS. 인접 candidate/profile/runtime/
  prepack/feature 계약 83개, controls 관련 검증 실행 48개, index 8개 PASS.
  일부 실행은 같은 검사를 포함하므로 이 수를 합산한 unique test 수로 보고하지 않는다.
- 전체 테스트 discovery는 실행하지 않았다. 실제 native 평가 및 사용자
  수락은 위 source/index/audit 성공으로 대신할 수 없다.

로그: `electrical-tests-final.log`, `focused-tests.log`,
`final-scope-tests.log`, `index-tests.log`, `dictionary-check-final.log`,
`visual-check-final.log`, `runtime-publication-final.json`.

## 독립 테스트 구성

사용자가 요구한 세 subagent는 fresh context로 시작했다. Coordinator가
실제 requester bytes와 active spans를 동결한 뒤 전달했다. 각 agent는
SKILL/허용 neutral 파일·대화 문맥·일반 지식·같은 원본 reference pixels만으로
랜덤 seed, 서로 다른 복잡한 scene, baseline/core, feature selection,
embodiment review와 자체 native criterion을 먼저 작성·동결했다.
후보·연구·다른 arm의 결과는 그 전에 읽지 않았다.

SKILL SHA-256:
`9e9b87e6f0b2c1ec1c36bd8e9d55f90950d53529a0b873722b546924dfc7043b`.
Saved controls는 세 arm 모두 sensual 1, fetish 0, creativity 1, surreal 0,
reference_edit_mode off를 유지했다. 원본 얼굴·헤어의 appearance reference로
첨부 이미지를 실제 전송한다. 원본 의상·구도나 가상의 줄거리를 사용자
세부 조건으로 승격하지 않았다.

| Arm | 독립 선택한 scene | 동결한 전기 관측 |
|---|---|---|
| 1 | 이동 박물관 고전압 시연기 복원 qualification | 두 구형 단자 사이 spark / 별도 glass tube 내부 gas glow |
| 2 | 폭풍 속 선박 조타실의 기록과 창 닫기 | 가까운 mast-tip corona / 먼 cloud 내부 lateral lightning |
| 3 | 마지막 등대 기록실의 장치 종료 | 두 전극 tip 사이 spark / comb-tip local corona / coil-to-lamp 연결 |

각 arm의 첫 generation 조회와 준비 실패는 삭제하지 않았다. Effects 수정
후 원본 request/envelope/controls/core/baseline/selection/review bytes를
그대로 새 managed subrun에서 replay해 최신 generation으로 재조회한다.
이는 새로운 scene을 사후 작성하거나 새 user text를 만드는 절차가 아니다.
이미지 호출 전에 source receipt·composition·runtime request audits를 완료한다.

원본은
`/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg`,
SHA-256 `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`.
원본이 갖는 특정 인물의 실제 나이·성격·과거·동의·직업은 사진으로 추정하지 않는다.

## 보존과 제출 상태

`PRIMARY-PRESERVATION-FINAL.json`의 최종 sweep은 보호 대상 23,998개 중 이번에
의도적으로 갱신한 manifest/semantic-index/visual-index 3개를 제외한
23,995개 파일 SHA가 모두 유지됐고 삭제가 없음을 확인했다. HEAD도
시작과 끝이 같다. 이번 변경은 새 두 source, 중앙 manifest의 두 등록,
파생 indexes 및 scoped 새 test/evidence 파일이다. 기존 dirty authored
source와 테스트를 덮어쓰지 않았다. Commit/push/PR은 이번 요청 범위에 없다.

이미지 결과와 각 gate의 원본 해상도 판정은
[FINAL-REPORT.md](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/electrical-semantics-20261008/integration/FINAL-REPORT.md)에
저장했다. 실제 native 호출은 arm마다 1회, 총 3회다. 세 장 모두 주요 전기
형상은 보이지만 전체 필수 장면은 arm 2만 PASS다. Arm 1은 지정한 콘솔
접촉, arm 3은 두 번째 램프 배선 끝점 확인이 실패했다. 가려진 필수 관계,
부분 실현, preview-only/blocked/unknown
결과는 PASS로 계산하지 않는다. 세 장의 결과만으로 통계적·인과적 개선이나
사용자 수락을 입증하지 않는다.
