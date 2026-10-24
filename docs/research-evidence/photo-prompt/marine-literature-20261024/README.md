# 해병문학 리서치와 데이터 반영 설계

2026-10-24 KST · **소스·인덱스 반영과 독립 이미지3개 검증 완료 · 신규 픽셀 반영 미입증**

현재 실행 상태는 [반영 및 이미지 검증 결과](INTEGRATION-RESULTS.md)를 기준으로 한다. 아래 연구 초안·기준선은 등록 이전의 이력을 보존한다.

- [상세 리서치](RESEARCH.md): 현실 차용·판본·외형·포즈·위계·은어·그래픽·주장 한계.
- [반영 계획](IMPLEMENTATION-PLAN.md): 우선순위, 기존 데이터 재사용, 독립 인덱스, 검색 회귀, 픽셀 검증, 채택 기준.
- [전체 키워드 지도](KEYWORD-ATLAS.md): 크롬에서 확보한 표 23개·247행을 원뜻과 함께 보존.
- [시각 의미 카드](VISUAL-CARDS.md): 96개 카드, 한영 필수 관찰 그룹 288개, 소유자와 방향 관계.
- [후보 초안](candidate-drafts.json): 등록 전 90개 연구용 제안. 후속 실행에서 87개 새 CID와 3개 기존 CID 재사용으로 연결했다.
- [기존 데이터 대조](existing-source-mapping.json) · [반영 분류](DATA-ADOPTION.tsv): 전체 레코드·조건·효과·bindings를 읽은 15개 비교.
- [출처 장부](SOURCES.md): 입력 대화와 외부 출처 19개. 외부 15개 본문/관련 부분, 1개 팬아트 캡션, 2개 검색 추출, 1개 접근 실패를 구분.
- [40개 평가 사례](evaluation-cases.json): 한영 질의 80개와 금지 추론. 실행 전 기대값.
- [픽셀 계획](PIXEL-PLAN.md): 최초 12개 검증군과 장면 제안. 실제 독립 테스트는 후속 요청에서 각 agent가 별도 확정했다.
- [구조 검증](VALIDATION.json) · [기준선](BASELINE.json) · [종료 관찰](SOURCE-OBSERVATIONS.json).

핵심은 ‘해병문학=빨강·근육·최소 복장’이라는 강제 묶음을 만들지 않는 것이다. 실제 군복·팬 설정·일반 포즈를 분리하고, 신체·옷·소품·문자·그려진 장면의 소유와 접점을 명확히 한다. 민감한 은어 30행도 뜻을 삭제하지 않고 문맥 데이터로 보존했다.

96개 카드 중 74개는 정지 형태, 9개는 그래픽, 9개는 대리 표현, 4개는 연속 서사다. 4개 연속 서사와 빈 방 문패·내용물을 가린 메뉴 대리형 2개는 긍정 후보 초안에서 제외했다. `new` 85개는 잠정 새 정의 제안이며 의미 중복 검토가 끝났다는 뜻이 아니다. 기존 데이터 재사용 권고 3개도 실제 검색이나 픽셀 성공과 다르다.

최초 연구 단계는 운영 소스·인덱스를 편집하지 않았다. 이후 사용자의 반영·생성 요청에 따라 새 후보·연결·의미 데이터를 등록하고 실제 검색과 테스트용 설치를 검증했다. 기본 실행본 승격은 보류했다. 이 둘의 기준선·검증 결과를 섞지 않는다. commit/push는 수행하지 않았다.

## 최초 연구 단계 재현

```sh
python3 docs/research-evidence/photo-prompt/marine-literature-20261024/audit_corpus.py
python3 docs/research-evidence/photo-prompt/marine-literature-20261024/build_research.py
python3 docs/research-evidence/photo-prompt/marine-literature-20261024/validate_research.py
```

첫 명령은 현재 운영 파일을 읽어 이 폴더에만 발견 기록을 쓴다. 두 번째는 원본 대화 표와 저술 데이터를 사용해 문서·초안을 다시 만든다. 세 번째는 행 보존·참조·그래프·필수 그룹·기존 레코드 해시를 검증한다. 이 PASS는 사실 전체·실제 검색·픽셀 합격의 대용이 아니다.

후속 등록 이후에는 위 명령의 과거 read-only 기준선 검증을 현재 운영 무변경 증거로 사용하지 않는다. 실제 실행의 재현 스크립트와 기록은 `integration-evidence/`, 독립 프롬프트·생성·판정 기록은 `image-tests/`에 있다.

[최종 원본·정확한 prompt·판정·후속 계획](INTEGRATION-RESULTS.md): 이미지3회 생성, 신규 후보 활용0/3, managed technical qualification 합격0/3. 소스/인덱스 반영과 운영 기본 선택은 별도 상태다.
