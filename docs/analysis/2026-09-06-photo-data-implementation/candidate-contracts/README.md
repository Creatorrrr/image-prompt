# 후보 의미 계약 구현 검증

실제 `generate_once(selection_mode="rule") → build_candidate_pack(v6)` 경로에서
`bundle:clean_beauty_clamshell`을 발견한 pack `5080eed2cbe98b02`를 보존한다.
인덱스·사전·품질 데이터는 현행 정상 로더를 사용했으며 sampler 결과나
후보 목록을 주입하지 않았다. 원자료→102개 병합 묶음→관련 선택 묶음→
축약 뷰→전체 detail→명시 채택→전체 composition audit을 확인했다.

- `pack.json`: 생성된 원본 v6 팩.
- `detail.json`: 원본 팩과 hash로 결합된 선택 묶음의 전체 상세.
- `selection_evidence.json`: 모든 component·relation의 literal evidence.
- `composed.json`, `composed-audit.json`: 완성한 composition과 전체 감사 PASS.
- `composed-audit-initial-missing-fields.json`: 초기 구성의 명시 빈 선택 목록과
  authored slot 선언 누락 오류. 코어·팩을 바꾸지 않고 해당 선언을 보완했다.
- `focused-tests.log`, `full-integration-test.log`: 집중 검사 실행 기록.

source contract를 변조한 뒤 hash까지 다시 계산해도 감사가 동일 skill
snapshot의 사전·품질 데이터에서 admission을 재계산하여 거부한다. 입증되지
않은 외부 role prerequisite를 넣으면 묶음을 노출하지 않는다. 기존 개별
후보의 모든 자격이 충족되거나, 동시 채택된 묶음 내부에서만 필요한 조건이
충족되는 경우를 구분한다. 어느 경우에도 잠긴 차원의 변경, 관리 태그 노출,
연결 profile의 자동 필수화, 묶음 내부 후보의 독립 선택권 추가를 허용하지 않는다.

이 입력은 구현에서 도출한 유지보수 fixture다. 실제 사용자 이미지 요청이나
독립 holdout으로 취급하지 않으며, 생성 이미지·픽셀 성능·사용자 선호를
입증하지 않는다. 별도 5개 과거 요청 실험의 입력·출력은 이 검증에 사용하지 않았다.
