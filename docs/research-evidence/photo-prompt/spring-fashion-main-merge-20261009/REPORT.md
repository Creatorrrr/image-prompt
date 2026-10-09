# 봄 패션 Git 게시 검토

게시 범위는 봄 패션 신규 후보·프로필·bundle 각 276개, 기존 ID 문맥 2건, 재사용 3건 및 관련 리서치·프롬프트·native 판정·테스트다. 실제 픽셀 실패와 사용자 판단 pending을 유지한다.

기준 main은 f081ac7305210def8348cc76d3a8f9f48393b4de다. 원래 primary에는 다른 계절 작업의 dirty/untracked 경로 10,958개가 있어 별도 게시용 worktree를 사용했다. 원래 inherited 프로필 수정 3개는 이 커밋에서 제외했고, 기준의 authored identity 1,535개를 보존했다. 본 작업의 데이터만 반영한 최초 게시 인덱스는 semantic 11,457개, visual profile 3,210개다. 추가 embedding 호출 없이 정확한 텍스트와 vector space가 같은 벡터만 재사용했다.

초기 dictionary 및 봄 패션 테스트 8개를 통과했다. 첫 커밋 후 origin/main을 pull하고, 들어오는 authored intent를 ID별로 보존하여 통합한다. 달라진 corpus의 인덱스는 재생성하며, 통합 관련 검사·전체 suite와 원격 게시 결과는 후속 영수증에 기록한다.

전체 생성 PNG는 primary의 generated_images/spring-fashion-20261009에 byte-identical 사본으로 보존했다. 원본 사진이나 ignored 환경파일·빌드 checkpoint·대형 인덱스 staging cache를 강제로 Git에 넣지 않았다. 검사용 crop/thumbnail과 exact native ledger·사전 기준은 기존 증거 폴더에 포함했다.

삭제는 push가 정상 완료되고 원격 main을 확인한 다음 수행한다. 모든 원래 primary 작업은 보존하고 이 채팅의 spring integration/publication worktree만 제거한다.
