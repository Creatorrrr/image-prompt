# Generator 미사용 바인딩 정리

상태: 검증 완료 후 확정한다.

- `prompt_generator.py`의 미사용 from-import 바인딩 3개와 상수 1개만 제거했다(추가 0행, 삭제 4행). 계약 공급 모듈의 정의와 활성 소비자는 유지했다.
- 대상 외 AST가 동일하며 HEAD 기반 커밋 패치와 현재 작업 파일 패치를 분리했다. 기존 generator 수정의 diff 내용은 동일하다.
- 운영 관련 48건과 계약·문맥·재시도 관련 43건 통과(그룹 간 BM25F 테스트 중복 포함). HEAD 대조는 양쪽 각각 43건 중 41건 통과, 기존 실패 2건 동일, 신규 실패 0건.
- 실제 관리 CLI 5개 명령을 변경 전·격리 변경본·실제 적용본에서 실행하고 top8, 전체 순서·점수가 동일함을 검증했다. 공통 풀 전체 H 단독+F2 검색 및 슬롯당 BM25F 1회·로컬 cosine 1회 계약을 유지했다.
- 설치된 실행·발급 receipt/frozen audit·파생 native view·보존 archive 450개 순서/17개 테스트·잘못된 입력 거부를 검증했다. 과거 품질 HOLD 판정은 유지했다.
- 이번 작업 시작 시점의 미커밋·미추적 파일, 다른 worktree, 설치된 세대, 데이터·모델, CURRENT를 보호했다. 이전 분석 뒤 별도 작업에서 변경된 문서는 이번 시작 상태로 기록했으며 과거 버전으로 되돌리지 않았다. 상세 경로 수와 해시는 RESULTS.json 및 BASELINE-DELTA.json.gz 참조.
- 네트워크 차단 상태에서 검증했다. Gemini·새 임베딩 추론·이미지 생성·publish·CURRENT 전환·push는 수행하지 않았다.

재현: `python3 -B run.py <command>`와 `head_check.py`, `finalize.py`를 사용한다. 과거 커밋의 공통 검증 도구를 재사용한다. 실행 scratch 경로는 유일한 복구 자료가 아니며 패치·원본 지문·실행 출력은 이 디렉터리에 남긴다.

동시 작업: 검증 중 `candidate-baseline-20261020/`에 추가된 미추적 파일은 보호 목록 시작 시점의 변경이 아닌 신규 동시 작업으로 분리했다. 최초 엄격한 상태 비교 실패는 그대로 보존하고 `BEFORE-APPLICATION-REVIEWED.json`에서 기존 파일·상태·index·HEAD·CURRENT 불변과 추가 파일 미포함을 별도 판정했다.
