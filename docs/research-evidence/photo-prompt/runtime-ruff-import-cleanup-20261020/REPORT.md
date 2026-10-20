# 사진 스킬 Ruff 도입 및 미사용 import 일괄 정리

기준 main: `87ab455fc3d5cd7493a370e6899990e9e2d48ef7`. 현행 스킬 소스의 미사용 import를 한 번에 관리하고 새 위반을 CI에서 차단한다. 임시 qualification 코드는 저장소 밖에 보관하며 이 요약과 검증 결과만 함께 커밋한다.

`ruff.toml`은 사진 스킬의 scripts/precore Python 76파일에 `F401`만 적용한다. Ruff는 0.15.1로 고정했고 formatter·import 정렬·unsafe fix는 켜지 않았다. 새 GitHub Actions workflow는 PR/main push/수동 실행에서 같은 명령을 실행하며 읽기 권한만 가진다. 두 Actions는 확인한 v6 commit SHA로 고정했다. Actions 자체는 아직 원격 실행하지 않았고 로컬에서 동일 명령과 workflow 구조를 검증했다.

초기 28건 중 23개는 공개 재노출을 `name as name`으로 명시했다. native qualifier의 로딩 순서를 보존하는 `qualify_local_hybrid.c`는 줄 단위 noqa 1개로 고정했다. 설치 H-F2의 worker_sha256에 묶인 photo_local_embedding.py는 단일 파일 설정 예외로 보존했고 바이트를 바꾸지 않았다. 나머지 `qualify_local_embeddings.c`, `qualify_local_hybrid.slots` 2개는 Ruff가 제거했다. 포괄적인 generator/규칙 무시는 추가하지 않았다. 각 수정 파일에 새 위반을 넣은 네 가지 검사에서 F401을 검출했고 재수정 diff는 비어 있었다.

수정 전후 작업본 각각 관련 검사 71개가 PASS했다. 공개 재노출 객체 identity·다른 namespace 타입·import 외 AST·implementation 일치/불일치 guard도 보존했다. HEAD-only 대조 각 50개에서는 이전부터 존재한 source-effects 실패 2개가 양쪽에 동일했고 새 실패는 0개였다. 기존 미커밋 수정에 의존하는 이 두 건을 해결하려고 사용자 작업을 함께 stage하거나 평가를 완화하지 않았다. 커밋할 HEAD-only 소스도 Ruff를 통과했다.

실제 설치된 H-only+F2를 사용하는 private/applied managed 경로에서 각각 issued-view→retrieve→view→compose-audit→deliver 5명령을 검증했다. 기존 로컬 query vector를 재사용했고 positive 공통 풀 18,180 CID/18,182 RID와 슬롯당 BM25F 1회·local cosine 1회를 유지했다. 이전 설치 kernel의 두 목표에서도 전체 점수 배열·순위와 원래 receipt/native 구성 감사가 같았다. 과거 450개 전체 순위·17개 테스트를 재현했으며 원래 품질 HOLD를 보존했다. derived native public view는 control/combined/applied가 같았다. 이것은 선택한 운영·재현 경계 검증이며 모든 과거 실행이나 전체 테스트의 전수 검증은 아니다.

원래 159,309경로와 CURRENT 168개를 bytes/mode/inode/link까지 대조했다. 의도한 소스 4파일과 유지보수 README의 기존 dirty payload를 정확히 보존했다. 159,308경로의 원래 값 또는 명시한 변경 값 비교와 별도로, 범위 밖 기존 미추적 검토 문서 1개에는 동시 작업의 내용 추가가 있었다. 그 문서의 최초 2,856 bytes가 원래 SHA 그대로인 append-only임을 확인했고 현재 문서를 변경하거나 stage하지 않았다. 최초 strict FAIL과 별도 검토 PASS를 모두 보존했다. 설치 선택, 봉인 release, 후보 데이터, shard, 로컬 worker와 다른 worktree는 유지했다. 새 의미 판정·Gemini·새 임베딩 추론·이미지 API·운영 publish·원래 CURRENT 쓰기·push는 없다. 동시 추가 미추적 파일은 원래 파일의 변경과 구별해 손대지 않았다.

stage는 HEAD에서 만든 별도 source/README 패치와 새 설정·CI·이 요약 두 파일만 허용한다. 사용자 dirty 본문이나 이전 분석 산출물은 포함하지 않는다. 자세한 범위·수치·raw evidence 해시는 `VALIDATION.json`에 있다. 운영/유지보수 사용법은 `tools/photo_runtime_maintenance/README.md`의 미사용 import 절을 따른다.
