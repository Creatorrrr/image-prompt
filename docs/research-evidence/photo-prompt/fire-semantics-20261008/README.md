# 불 관련 시각 의미·후보팩 강화 리서치

2026-10-08 작성. 참조 대화의 조회 가능한 278개 키워드와 보충 조사를 바탕으로 연구·데이터 초안·반영 계획을 작성했다.

- [리서치 보고서](RESEARCH.md): 주요 발견, 과학·시각 경계, 현재 데이터와의 차이, 근거 한계.
- [구현·반영 계획](IMPLEMENTATION-PLAN.md): 우선순위, 실제 source 위치, owner/property 검토, 인덱스·runtime·픽셀 완료 조건.
- [의미 카드 전체](SEMANTIC-CARDS.md): 20개 영역, 155개 카드.
- [후보 초안](CANDIDATE-DRAFTS.json): 131개 연구용 후보.
- [프로필 예시](PROFILE-PROTOTYPES.json): V2 관계 프로토타입 18개.
- [출처](SOURCES.md): 42개 1차·기관 출처와 접근 범위.
- [검증 결과](VALIDATION.json): 연구 정합성과 제한된 compiler shape 검증.
- [원문 조회 범위](SOURCE-CONVERSATION.json): 20,000자 제한과 잘린 위치.
- [키워드 연결](SEED-COVERAGE.json): 조회한 278개 표 행의 누락 방지 기록.
- [공동 채택 관계](BUNDLE-DRAFTS.json): 7개 연구용 묶음.
- [회귀 계획](REGRESSION-PLAN.json): 44쌍.
- [픽셀 검증 계획](PIXEL-QUALIFICATION-PLAN.json): 10개 사례와 통제 비교.
- [원본 보존 점검](PRESERVATION-CHECK.json): active assets JSON과 기존 dirty 파일의 비교.
- [조사 중 관찰된 저장소 변경](LIVE-DRIFT-NOTE.md): VEL 커밋과 semantic index 변경의 별도 기록.
- [산출물 manifest](ARTIFACT-MANIFEST.json): 파일별 SHA-256.

상태: **리서치·초안·계획 완료**. active source 등록·인덱스 재생성·runtime 발행·이미지 생성은 수행하지 않았다.

원 대화 본문이 16절 중간에서 잘려 후반의 세부 키워드 전체는 조회되지 않았다. 후반 관련 문화·광학·신체·폭력·관능·비유는 보충 조사로 표시했다. 278개 연결은 연구 누락 방지이며 모든 원 정의·runtime·이미지의 검증을 뜻하지 않는다.

재생성: `python3 docs/research-evidence/photo-prompt/fire-semantics-20261008/build_research.py`. 이 스크립트는 이 연구 폴더에만 출력한다. active asset이나 runtime store를 수정하지 않는다.
