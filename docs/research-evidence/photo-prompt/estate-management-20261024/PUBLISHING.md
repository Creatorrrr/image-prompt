# 영지물 원문·실패 보완의 main 반영

이 문서는 이전 연구·이미지 재시험 뒤 별도로 요청된 Git 반영을 기록한다. 이전 완료 기록의 “커밋·푸시 없음”은 그 시점의 사실로 보존한다.

공유 기본 checkout의 다른 작업과 캐시는 그대로 두고, 전용 워크트리에서 이번 자료와 retry 수정만 명시적으로 골랐다. 기존 원문 모듈 109개는 바이트 그대로 보존하고, 영지물 원문/연결 모듈 4개를 등록했다. 신규 후보 86건은 긍정 29건·진단 57건이며, 연결은 총 77건이다. 원래 후보 78건·연결 56건과 보완 후보 8건(긍정 7·보류 1)·연결 21건을 포함한다. 의미 sidecar 2개는 검색 점수나 자격을 만들지 않는다.

공유 SKILL·주제 검색·샘플링 정책·기본 실행 세대 변경은 이 작업의 커밋에 섞지 않았다. 공통 manifest에는 이번의 네 등록만 추가했고, 유지보수 문서에는 영지물 문단만 추가했다. workflow 문서와 retry helper에는 보존 입력의 provenance 재바인딩 및 부모 자신의 봉인 실행본 감사 수정을 포함한다.

통합한 원문에 맞는 인덱스를 pinned local model로 재생성했다. 기존 벡터 20,695개를 재사용하고, 긍정 후보 29개만 로컬에서 계산했다. 원문·인덱스 검증과 retry 검사 46개가 통과했다. 연구 검사는 374행·60개 시각 카드·20개 문맥 카드·37개 출처의 링크/구조를 확인하며, 계획 192개는 실행하지 않았다. 이미지 재시험의 엄격 판정 0/3과 보류 상태는 그대로 보존한다.

- [원문 보존](publication-evidence/source-preservation-initial.json)
- [인덱스 재생성](publication-evidence/index-build-initial.json)
- [retry 회귀 검사](publication-evidence/focused-tests.json)
- [연구 구조 검사](publication-evidence/research-integrity-check.txt)

작업 커밋 `1c9d31bd8762e31ecaf35410afd0768973dcb78f` 뒤 `git pull --no-rebase origin main`을 실행했다. 원격은 시작점 `f41dd84089acce7d87f864630760c428ab3898a7`와 같았다. 그 main을 기준으로 `--no-ff` 머지를 진행했고 충돌은 0개다. 게시 기록을 덧붙이기 전 전체 머지 tree가 검증된 작업 커밋과 정확히 같으므로 원문·코드·인덱스의 재검증 입력도 같다. 관련 빌드 캐시는 실제 원격 푸시 검증 뒤 제거하고, 첨부 원본·요청된 결과 이미지·원장·검증 기록·현재 설치된 실행본은 보존한다.

[양쪽 보존과 pull/merge 기록](publication-evidence/merge-preservation.json) · [스테이징 파일·바이트 대조](publication-evidence/staged-name-and-blob-check-initial.json) · [실제 부모 봉인 실행본 감사](publication-evidence/actual-parent-sealed-audit.json)
