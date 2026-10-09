# 봄 패션 main 게시 검토

봄 패션 신규 후보·프로필·optional bundle 각 276개, 기존 ID 문맥 2건, 재사용 3건 및 리서치·독립 프롬프트·native 판정·관련 테스트를 게시한다. 픽셀 실패와 사용자 판단 pending은 기존 기록대로 유지한다.

기준 main은 `f081ac7305210def8348cc76d3a8f9f48393b4de`이며, 첫 구현 커밋은 `555a592f5c4360d0aa6502c7432b6118494aaa36`이다. 첫 커밋 후 `git pull --no-rebase --no-commit origin main`은 Already up to date였고, 마지막 원격 조회도 같은 기준 커밋을 확인했다. 들어오는 별도 변경이 없어 fast-forward로 main을 반영한다.

기존 authored identity 1,535개를 유지했다. 원래 primary의 다른 작업 수정 3개는 게시 범위에서 제외했으며, 모든 원래 작업 파일 35,544개와 dirty/untracked 경로 10,958개를 외부 보존 manifest/사본으로 보호한다. source manifest와 알고리즘은 바꾸지 않았다. 게시용 순수 corpus는 semantic 11,457개·visual profile 3,210개이며, 같은 텍스트·provider·model·차원인 벡터만 정확히 재사용해 추가 embedding 호출은 없었다.

Dictionary 검사와 semantic/visual 인덱스 deep 검증 및 봄 패션 테스트 8개를 통과했다. 변경 관련 121개 검사는 120개 통과·기존 portrait fixture 실패 1개다. 전체 discovery 2,097개를 빠짐없이 수집해 실제 2,013개를 실행했으며 실패 이벤트 25개·오류 이벤트 15개·skip 0개가 발생했다. 클래스 준비 단계 오류로 실행하지 못한 멤버 검사는 실제 실행 수에 포함하지 않는다. 전체 suite는 green이 아니다. 모든 최종 실패·오류 이벤트는 테스트 코드를 수정하지 않은 깨끗한 origin/main `f081ac7305210def8348cc76d3a8f9f48393b4de`에서 같은 ID로 재현됐다. 과거 동결 fixture/source 경계, local-only 이미지 증거 누락, 기존 부분 inventory 의존성 등이 포함된다. 자세한 ID와 baseline 로그는 `BASELINE-COMPARISON.json`에 있다.

전체 검사를 나눠 실행한 초기 worker 1에는 동일한 모듈명 충돌과 Python 경로 누락이 있었다. 해당 오류 결과와 미수집 242개를 분리 보존했고, 올바른 root/test 경로 및 전체 import 순서를 사용해 누락·오류 검사만 재확인했다. 다시 나누기 전에 완료한 24개 성공 ID도 보존했다. 최종 discovery ID 합집합은 원래 2,097개와 정확히 일치하며 누락·중복이 없다. 잘못된 실행 및 중단한 serial 실행은 완료된 검사로 계산하지 않았다. 테스트 코드나 성공 조건을 바꾸지 않았다.

전체 PNG 3장은 primary의 `generated_images/spring-fashion-20261009`에 byte-identical 사본으로 남긴다. 원본 사진·환경파일·대형 staging/build cache는 강제로 Git에 넣지 않았다. 검사용 crop/thumbnail·hash·native ledger와 사전 기준은 원래 evidence 폴더에 유지한다.

main 반영은 원래 primary 파일 바이트·링크 대상·mode를 보존하면서 기준 HEAD와 index의 동시 변경을 검사하는 fast-forward로 수행한다. 정상 push 뒤 local main·origin/main·원격 refs/heads/main 일치를 확인하고, 이번 integration/publication worktree를 복구 가능한 snapshot으로 archive한다. 임시 baseline worktree도 제거하며 다른 계절 worktree는 유지한다. 실제 push·제거·최종 보존 영수증은 primary의 같은 evidence 폴더에 `DELIVERY.json`으로 후속 기록한다.
