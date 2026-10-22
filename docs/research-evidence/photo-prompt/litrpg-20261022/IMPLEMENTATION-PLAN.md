# 운영 반영 계획

이 문서는 실행 순서와 완료 조건을 정한다. 이번 작업은 연구 자료·초안·계획까지만 작성했다. 아래 운영 파일과 설치 상태는 아직 변경하지 않았다. 60개 초안은 검토 대상이며 등록 목표량이 아니다.

## 1. 기존 소스 대조와 정확한 범위 확정

최신 manifest와 각 모듈 hash를 다시 고정한다. 조사 스냅샷은 69개 모듈·19,813개 레코드·14,287개 바인딩이다. 검사 중 manifest와 다른 운영 파일의 동시 변경을 실제 관찰했으므로 이 스냅샷을 최신 상태로 재사용하지 않는다. `WORKSPACE-DRIFT.json`을 확인하고 최신 소스를 다시 대조한다. `CORPUS-AUDIT.json`과 `reviewed-litrpg-sources.json`의 원문·조건·효과·기존 바인딩을 기준으로 초안마다 다음 중 하나를 기록한다.

- **reuse_exact**: 기존 전체 원문의 인원·개수·재료·행동·관계·조건을 그대로 만족하는 대안으로 재사용.
- **new_variant_review**: 의미 있는 관계·표시 기능·매체 차이가 있으므로 독립 실현 후보로 검토.
- **context_only**: 원인·의도·시간·동의 등의 문맥. 양성 시각 효과로 승격하지 않음.
- **defer**: 출처 또는 전체 원문 의미 심사가 부족함. 등록·활성화를 진행하지 않음.

기존 후보의 adult 조건·필수 표식·물리 소품을 제거해 새 일반 개념으로 사용하지 않는다. 이미 등록된 D01–D08과 새로운 U/I/Q/R 번호는 서로 다른 연구 namespace다. 운영 ID는 `litrpg_system_*` 같은 고유 namespace로 변환하고 원래 ID를 참조 링크로 남긴다. 8개 상세 비교는 [CORPUS-FINDINGS.md](CORPUS-FINDINGS.md)에 있다. 전체 코퍼스 중복 제거 완료로 해석하지 않는다.

## 2. 데이터 모델과 제안 파일

| 파일 또는 위치 | 제안 변경 | 지켜야 할 경계 |
|---|---|---|
| `skills/photo-prompt-image-generator/assets/photo_litrpg_system_semantics_20261022.json` | 심사한 의미 카드·어휘 경로·출처·해석 한계의 별도 자료 | 장르 별칭을 자동 profile 의무로 바꾸지 않음 |
| `skills/photo-prompt-image-generator/assets/photo_candidate_litrpg_system_20261022.json` | 승인된 전체 양언어 시각 실현과 contextual diagnostic | `owners/relations` 연구 그래프를 native scalar fact로 복사하지 않음 |
| `skills/photo-prompt-image-generator/assets/photo_candidate_litrpg_system_bindings_20261022.json` | 실제 catalog 슬롯에 맞춘 개별 바인딩·조건·effects | 슬롯명·tag·연구 source만으로 역할 적격성을 만들지 않음 |
| `skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json` | 심사한 모듈만 추가 | 다른 미완성 모듈을 우연히 함께 등록하지 않음 |
| `skills/photo-prompt-image-generator/references/litrpg-system-semantics.md` | 매체·표시값·인지 범위·시간 증거 가이드 | 최초 요청 의미를 keyword glossary로 대체하지 않음 |
| `skills/photo-prompt-image-generator/references/maintenance.md` | 소유 자료와 변경 범위 연결 | 연구 수·코퍼스 수와 runtime qualification을 구별 |
| 관련 `tests/`의 focused maintenance tests | bilingual source, wrong-owner, text context, sequence boundary 검증 | 연구 JSON을 그대로 assert하는 테스트 대신 실제 오수용 경계 검증 |

이름은 제안이며 기존 모듈과 중복되지 않는지 구현 시 다시 확인한다. 연구 스키마를 그대로 운영에 복사하는 변환은 하지 않는다. 완전한 양언어 긍정 단위와 조건을 작성하고, 실제 schema validator가 허용하는 필드에만 넣는다. 원전 인용·설명·출처 정보가 검색 가중치나 추가 권한으로 둔갑하지 않게 한다.

표시 정보와 시각 구조를 분리한다. 예컨대 `HP 100`은 해당 화면에 그 라벨·수가 표시된다는 의미이며 몸의 건강이나 시스템의 진실성을 보증하지 않는다. 내용이 정확히 읽혀야 할 요청에는 짧은 핵심 문자열과 소유 화면을 함께 지정한다. 글자가 중요하지 않은 장면에 긴 능력표를 자동 추가하지 않는다.

## 3. 적용 우선순위

| 순서 | 검토 카드 | 이유·출하 조건 |
|---|---|---|
| P0: 핵심 24개 | U01–U07, I01–I06, Q01/Q04–Q08, C01–C04, E01 | 표시 매체·자원·스킬 분기·물증·장착·지원의 기본 관계. 기존 D 소스와 먼저 대조하고 전체 소유자·끝점 검토 통과 |
| P1: 확장 24개 | U08, I07–I08, Q02–Q03/Q09–Q12, C05–C08, W01–W06, E02–E06 | 진화·덱·제작·거점·범위·지도·정보 위계. 일반 공방·재고·광고·파티 오염 통제 통과 |
| P2: 관계·이력 12개 | D01–D03, H01–H04, R01–R05 | 사망 이력·변형·관계·권한. 표시와 실제 사실 구분, 비시각 주장 경계 통과 |
| 각 단계 공통 | X01–X18 | 문맥 14개·연속 증거 4개. 자동 강제 소품을 만들지 않고 해당 의미의 한계를 유지 |

범위는 의미와 기존 재사용 판단으로 줄거나 나뉠 수 있다. 특정 숫자를 채우려고 약한 변형·동의어를 추가하지 않는다. 후속 의미 리뷰에서 동치인 실현은 병합하지만 서로 다른 매체·대상·인원·관계를 하나의 느슨한 후보로 합치지 않는다.

## 4. 의미와 조건 검증

각 실제 후보에 대해 전체 en/ko 동치, 원문 모든 필수 요소, exact owner/part, 서로 다른 인물·개체의 개수, 양쪽 관계 끝점, 비교 기준을 심사한다. 효과가 여러 차원에 걸치면 슬롯 하나만 보고 판단하지 않는다. 그룹형 연구 노드(`others`, `choices`)는 실제 개체 수와 각 연결을 운영 원문에 확정해야 한다.

P0에서는 기존 손·물리 카드·트리·소켓 소스의 조건을 보존하면서 다음 실패를 거부하는지 확인한다: 일반 dashboard에서 RPG 규칙 추론, 대상 이름표의 owner 교환, 시전·쿨다운·효과 지속시간 혼합, 예비 진화 도식의 실제 개체 추가, 미소/수치로 동의 단정, 숨긴 필수 끝점을 합격 처리. profile·guard·typed native fact 또는 새로운 역할 view가 필요하다면 기존 독립 전체-source 심사를 거친다. 연구 단계의 citation·관계 그래프·검토 flag가 그 심사를 대체하지 않는다.

## 5. 인덱스 발행과 설치 경계

반영한 semantic text는 인덱스 갱신 대상이다. 현재 소스의 유지보수 문서에 있는 dictionary validation과 shared-index verify/build/publish 경로를 사용한다. 먼저 `photo_installed_h_f2.py --check-runtime`으로 실제 설치 release·실행 Python을 확인한다. 이번 연구에서는 이를 실행하거나 설치 release를 변경하지 않았다.

빌드 전 활성 세대와 closure·source hash를 보존하고 별도 staging 경로에서 작업한다. 변경되지 않은 전체 텍스트·provider/model/dimensions/vector space와 checksum이 맞는 벡터만 재사용한다. 변경된 텍스트의 임베딩이 실제로 필요하면 그 실행·비용·오류를 별도 기록한다. alias만 추가했는지, 본문이 바뀌었는지에 따라 실제 text recipe를 확인하며 비용 0을 미리 보장하지 않는다.

source/index 전체 검증과 승인된 allowlist 검토가 끝난 뒤에만 현재 문서가 규정하는 publish 및 설치 qualification 절차를 진행한다. 코퍼스 source 등록, index publication, sealed generation, 설치 activation, 자연 질의 노출은 각각 별도 결과다. 과거 candidate-pack v6 증거를 현재 H-F2 실행 증거로 재사용하지 않는다.

## 6. 의미 검색과 이미지 검증

[48개 평가 입력](evaluation-cases.json)으로 양성·근접 음성·무키워드 양언어·평범한 장면·비시각 주장 경계를 확인한다. 개발 이후 새 검증 세트를 먼저 고정한다. 질의·실제 예산·반환 CID/RID·전체 출처 hash·표본 seed·adoption disposition을 남기고 원문 호환성을 사람이 확인한다. 운영 검색 성공이 실제 채택·픽셀 의미 충족을 대신하지 않는다.

[EVALUATION-PLAN.md](EVALUATION-PLAN.md)의 6개 장면은 후속 이미지 검증 제안이다. 이미지 실행을 요청받으면 현재 스킬의 독립 baseline/core 동결→retrieval→전체 비교→감사→render 경로를 따른다. 연구 초안을 최초 core의 요청 의미로 미리 주입하지 않는다. 사용자 고정 요구와 현재 창작 제어를 보존하고, 선택 가능한 staging만 비교·변경한다. 기술 합격, 장면 의미, 미학적 선호, 사용자 승인을 구분한다.

## 7. 반영 완료와 보류 기준

완료 보고에는 채택·재사용·보류한 정확한 목록, 변경 파일과 source hash, 관련 검사 결과, 인덱스·설치의 실제 상태, 검색 결과, 이미지가 있으면 전체 게이트와 미충족 관계를 적는다. `partial_is_fail`/`UNOBSERVABLE_NOT_PASS`를 유지한다. 이번 연구의 `native_approval:false`는 구현만으로 자동 반전하지 않는다.

부족한 출처는 해당 주장을 좁히거나 검증 대기로 남긴다. 예컨대 SAO의 403이나 Solo Leveling의 지역 제한을 근거로 작품 고유 색·동작을 지어내지 않는다. 전체 권한·조건 심사를 할 수 없는 후보는 보류하되 나머지 승인 범위는 진행할 수 있다.

commit/push를 나중에 요청받으면 명시 allowlist와 별도 검토 가능한 작업 공간을 이용한다. 현재 dirty 작업을 통째로 stage하지 않고 source·index 관련 closure만 재구성한다. 원격 SHA 확인과 복구 상태 검증은 발행 후 별도 단계다.
