# 아톰펑크 발행 범위와 검증 근거

사용자가 아톰펑크 작업의 커밋, 최신 origin/main pull, 양쪽 의도 보존 병합, main push 및 작업용 worktree 정리를 요청했다. 기존 main 체크아웃의 다른 미커밋 작업을 보존하기 위해 별도 worktree에서 발행 변경을 구성했다.

## 포함한 변경

- 101개 의미 카드/191개 키워드 경로를 보존하는 registry, 완전한 EN/KO 시각 후보 88개와 positive 검색 제외 진단 13개, 선택적 binding 176개.
- corpus manifest의 해당 후보/binding 모듈 2개 등록, Atompunk 참고 문서와 maintenance의 해당 연결만 추가.
- 후보 source의 의미/소유자/관계/진단 제외/비승격 경계를 확인하는 회귀 테스트 8개.
- 연구 원본 및 이미지 테스트의 텍스트 증거, exact prompt export, 성공/실패 판정. 세 이미지의 주제 및 얼굴/헤어 guidance는 관찰되며 엄격 세부 검사는 0/3 전체 통과(각 4/5)다. 실패를 성공으로 바꾸지 않았다.
- 발행할 source만 포함한 공유 검색 인덱스를 로컬 모델로 재생성하고 전체 검증했다. 미발행 다른 작업의 source나 index는 이 발행에 섞지 않았다.

## 보존 범위

기존 원격 source 모듈 77개는 아톰펑크 추가로 수정하지 않았다. 초기 scoped tree는 후보 19,963개(새 101개 포함), binding 14,553개이며 `publication/SCOPED-SOURCE.json`에 원본 보존과 corpus hash를 기록했다. 이후 origin/main에서 새 변경이 들어오면 그 의도를 병합 결과에 유지하고 필요 시 합쳐진 source로 인덱스를 다시 만든다.

primary 체크아웃의 다른 dirty/untracked 작업, SKILL/엔진 수정, 로컬 설치 runtime 선택, CURRENT 및 새 모델 설치 상태는 이 발행의 변경 대상이 아니다. 생성 이미지와 사용자 사진은 저장소의 기존 generated/user-data ignore 정책을 유지하며 원래 로컬 경로에 보존한다. 새 .runtime 모델 복제는 검증용 재생성 가능한 worktree 의존성이고 커밋하지 않는다.

## 기록 해석

연구/통합 보고서의 corpus 수치와 설치 generation은 각 실험 당시의 고정 snapshot이다. 이번 scoped Git tree의 수치는 별도 publication 기록을 따른다. 이전 보고서의 “commit/push 수행 안 함” 역시 이미지 실험 종료 시점의 기록이며, 후속 발행 절차는 이 문서와 Git history를 따른다.

세 native 이미지와 managed review의 원본은 primary의 generated 경로에 있다. 공개 저장소에 사용자 원본 이미지나 generated media를 강제로 추가하지 않았다. `integration-evidence/RESULTS.md`, `PROMPTS.md`, `three-arm-completion.json`과 각 run ledger에서 실험 provenance를 확인할 수 있다.

실제 push 이후 로컬/추적/원격 SHA와 원본 보존 및 worktree 삭제 결과는 primary의 `publication-evidence`에 별도로 기록한다. 이 운영 증거 디렉터리의 model/cache/store 복제나 다른 작업 hash inventory는 커밋 범위에서 제외한다.

## 원격 main 병합

최신 origin/main에서 Clockpunk 커밋 `2ce3aca853b4c4e909d1c0a614d32ed2112d30e2`을 가져왔다. corpus manifest, maintenance 문서와 파생 index manifest의 3개 충돌은 양쪽 주제의 추가 내용을 유지해 해결했다. incoming main의 기존 모듈 목록을 유지하고 아톰펑크 2개 모듈만 추가했으며, 81개 source 모듈 및 두 의미 registry가 각 소유 부모 커밋과 바이트 단위로 일치한다. 파생 인덱스는 합친 source로 재생성했다. 최종 검증은 `publication/MERGED-VALIDATION.json`과 `publication/MERGED-INDEX-BUILD.json`에 기록한다.
