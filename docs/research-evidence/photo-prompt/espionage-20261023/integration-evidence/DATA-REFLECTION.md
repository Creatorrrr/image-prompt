# 첩보물 데이터 반영 결과

2026-10-23 후속 구현 기록. 초기 연구의 README/RESEARCH/NOT_RUN/0장 표시는 연구 완료 시점의 스냅샷이며 그대로 보존했다. 후속 이미지 결과는 별도 통합 결과 문서에서 판정한다.

연구의 138개 시각 카드 가운데 111개를 완전한 한영 선택 후보로 추가하고, 17개는 기존 원문·조건·효과·연결을 바꾸지 않고 재사용했다. 세부 표본 동등성을 확인해야 하는 10개는 보류했다. 원문에서 복원한 160개 문맥 구분과 보충 12개, 보류 10개를 합한 182개는 diagnostic으로 등록해 positive 검색에서 제외했다. 선택 연결은 158개 추가했다. 키워드 경로 340개 중 아직 독립적인 원문 검토·매핑이 없는 외형 용어 65개는 그대로 남았다. 138개 카드와 같은 카드의 한영 초안을 서로 다른 항목으로 합산하지 않는다.

작성 소스:

- `skills/photo-prompt-image-generator/assets/photo_candidate_espionage_20261023.json`
- `skills/photo-prompt-image-generator/assets/photo_candidate_espionage_bindings_20261023.json`
- `skills/photo-prompt-image-generator/assets/photo_espionage_semantics_20261023.json`
- `skills/photo-prompt-image-generator/references/espionage-semantics.md`
- `skills/photo-prompt-image-generator/tests/test_espionage_semantics.py`

기존 corpus manifest에는 두 모듈만 추가했다. 직접 전달과 접촉 전 전달, 자기 커프와 타인의 넥타이, 귀에 착용한 장치와 손에 든 수화기, 배우의 뒤돌아보기와 카메라 위치, 실제 인물과 사진/거울 속 표현을 분리했다. 물건·옷·표정은 의도·동의·신분·소속·실제 통신/녹음 성공을 증명하지 않는다. 연구 그래프와 역할 표시는 native 사실이나 소유자 선택 권한, qualification, 자동 profile/hard activation을 만들지 않는다.

보호한 원본 128개 중 126개는 바이트가 같고, 바뀐 두 파일은 허용된 corpus manifest와 파생 검색 layout이다. 기존 후보·연결·catalog·policy 보존 검사를 통과했다. 초기 연구 SHA256SUMS의 34개 멤버도 모두 같은 바이트다. 이는 지정한 보호 범위의 증거이며 다른 동시 작업 전체의 무변경을 주장하지 않는다.

관련 경계 검사 11개와 사전 검증을 통과했다. 원래 사전 검증 한 번은 소스 편집 후 낡은 인덱스 때문에 실패했고 그 증거도 남겼다. 정확한 소스에서 인덱스를 다시 만든 뒤 검증을 통과했다. 작성 코퍼스는 후보 21,252개, 연결 16,069개다. 작업 중 다른 설치 갱신을 확인해 기존 설치본으로 되돌리지 않고 최신 기준에 이번 기록 293개를 재기반했다. 직전 설치본의 후보 20,782개를 모두 보존했다. native 커널 코드는 변경하지 않았다.

실제 기본 설치:

- H-F2 `587f77950e648994525a9066e8757e9fbaa55b38c3d9312f0b5ef517fdaece28`
- native `489839d65a789793d41a60e11d83965132f2030d23f69032ff35e7d8a5ab51f4`
- 전체 21,075 CID, positive 20,268 CID / 20,270 RID
- 새 positive 111개 전부 존재, diagnostic 182개 전부 제외, 재사용 17개 전부 존재
- 기존 검증된 문서 벡터 20,159개 재사용, 신규 문서 111개만 같은 pinned local embedding binding에서 계산
- 실제 배포 코드의 source/embedding/seal/native 검증 통과, CURRENT.json 쓰기 0

작성 코퍼스와 기본 설치본의 총량 차이는 아직 별도로 설치되지 않은 다른 작업의 작성 데이터 때문이며, 이번 주제의 누락 수가 아니다. 작업 소스를 한꺼번에 배포해 다른 작업의 범위를 확대하지 않았다.

최종 기본 설치본에서 연구 사례 412개 한영 질의를 다시 실행했다. literal smoke는 276개 중 positive gold가 있는 256개를 채점하여 top8 251, top32 254였다. 자연어 48개는 top8 39(한국어 18/24, 영어 21/24), top32 45였다. 경계/일반/비시각 대조 88개는 exact-CID gold가 없어 성공률을 매기지 않았다. 기존 설치본에서도 대조 88개를 실행했다. 연구자가 원문을 알고 작성한 질의이므로 독립 holdout, 일반 정확도나 인과적 개선 수치로 사용할 수 없다. 한국어 신발 여밈/스타킹 지지 등의 회수 약점이 남아 있다.

세 이미지 실행은 독립 초안 고정 뒤 별도로 검증·설치한 동일 테스트 release `3300bd369483c394610b29a53b8421934dacba4a9039e6cdd017deec7c4c26b7`에 고정한다. 이후 기본 설치본과 주제 모듈 두 개의 바이트가 같은 것을 확인했다. 그러나 후보 전체 집합은 다르므로 그 이미지의 검색·픽셀 관찰을 최종 기본 설치본에서 실행한 것으로 바꾸어 부르지 않는다. 검색 노출, 소스 채택, 최종 프롬프트, 실제 참조 첨부, native 결과, 픽셀 관계, 사용자 선호를 각각 기록한다.

`final-active-config.json`, `final-install-active.json`, `final-canonical-source-validation.json`, `final-positive-closure.json`, `final-active-retrieval-summary.json`, `test-source-rebase-equivalence.json`에 검증 증거가 있다. 구체적인 검색 결과는 generated maintenance의 각 `probe-after.json`/`probe-before.json`/`retrieval-qualification.json`에 있다. 커밋·푸시는 수행하지 않았다.
