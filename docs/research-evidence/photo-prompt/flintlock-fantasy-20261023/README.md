# 플린트록 판타지 리서치와 데이터 반영 설계

2026-10-23. **리서치·초안·반영 계획 작성 완료.** 크롬에서 참조 대화의 17절 전체를 확인하여 도구의 20,000자 제한으로 빠진 후반을 보완했다. 운영 데이터 반영·검색·생성 이미지는 미실행이다.

## 먼저 읽을 문서

- [RESEARCH.md](RESEARCH.md): 조사 결과, 역사·기술 구별, 관찰/비가시 경계, 기존 데이터 진단, 남은 원전 과제.
- [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md): 재기준화 → 원전/한영 검토 → 기존 CID 보정/재사용 → 신규 source/binding → 자격 → 별도 인덱스 → 실제 검색 → 프롬프트/픽셀 → 설치/게시의 입력과 완료 조건.
- [VISUAL-CARDS.md](VISUAL-CARDS.md): 부품·소유자·방향·수량·혼동·출처를 가진 81개 시각 실현과 21개 문맥 카드.
- [SCENE-DIRECTIONS.md](SCENE-DIRECTIONS.md): 원문의 여덟 장르 조합을 장면 관계로 연결하고 아홉 대표작의 접점을 분리.
- [PIXEL-PLAN.md](PIXEL-PLAN.md): 여덟 의미군과 첫 6장 비교 제안, 부분·비가시·차단의 판정 기준.
- [CORPUS-FINDINGS.md](CORPUS-FINDINGS.md), [CORPUS-SUPPLEMENT.md](CORPUS-SUPPLEMENT.md): 기존 후보의 전체 원문/조건/효과/binding 감사와 처리 제안.

## 산출물과 범위

| 항목 | 결과 |
|---|---:|
| 참조 원문 | 17절 전체 확인 |
| 키워드 경로 | 319개: 최초 조각 220 + 크롬 후반 회수 85 + 독립 보충 14 |
| 시각 실현/한영 후보 초안 | 81개 |
| 비가시·제도·정체·작품 문맥 카드 | 21개 |
| 외부 출처 | 57건: 본문 48, 색인만 9 |
| 기존 source 감사 기준 | 20,341 source / 15,120 binding / 149 slot |
| 고유 어휘 일치 source | 83개; 전수 의미 심사 아님 |
| 고유 전체 원문 수동 검토 | 25개 |
| 시각 초안 처리 제안 | new 52 / refine 6 / reuse 1 / defer 22 |
| 평가 설계 | 개발 81 + 경계 32 = 113사례, 한영 226질의; 전부 NOT_RUN |
| 예정 픽셀 gate | 관계 194 + 수량 52; 전부 NOT_RUN |

경로 수는 합성 행의 slash 별칭과 서로 다른 문맥의 다의어를 포함하며 독립된 새 개념/CID 수가 아니다. 처리 제안도 카드 단위이며 81개 신규 등록을 의미하지 않는다. 22개는 정밀 도판·물리 관계·직접 원전을 더 확인해야 한다. 다른 카드도 native/source-image qualification을 통과한 것은 아니다.

`candidate-drafts.json`은 운영 schema의 candidate module이 아니다. CID/RID는 null이며 effects/guards/role 자격의 완성본이 아니다. `semantic-cards.json`의 연구 graph와 role descriptor는 실행 사실이나 소유자 권한을 부여하지 않는다.

## 재현·확인

이 폴더에서 `python3 build_research.py`, `python3 validate_research.py`로 산출물 생성과 참조 무결성을 확인할 수 있다. build는 이 폴더에만 쓴다. `audit_corpus.py`는 최초 기준 snapshot을 만드는 도구이므로 기존 BASELINE을 보존해야 할 때 다시 실행하지 않는다. 추가 감사는 `audit_supplement.py`와 별도 snapshot으로 구분한다.

`VALIDATION.json`의 PASS는 카드/출처/role/owner/count/평가 연결 및 snapshot hash의 연구 무결성 결과다. 실제 검색·native 채택·이미지 의미·사용자 수용의 PASS가 아니다. 검증 대상 manifest·authored modules·runtime pointer/search/SKILL의 변경 여부를 `protected_drift`에 별도로 기록한다. `SHA256SUMS`는 이 폴더 파일만 포함한다.

| 실행 층 | 이번 상태 |
|---|---|
| 참조/외부 조사·원문 감사·계획 | 완료, 제한 명시 |
| 연구 파일 무결성 | VALIDATION.json 참조 |
| 운영 source/manifest/binding 반영 | 미실행 |
| native source 자격·한영 독립 심사 | 미실행 |
| 인덱스 구축·실제 retrieval | 미실행 |
| installed runtime 활성화 | 미실행 |
| 이미지 생성·저장 픽셀 판정 | 미실행 |
| 사용자 수용 | pending |
| commit/push | 미실행 |

외부 자료별 제한과 URL은 `SOURCES.tsv`/`sources.json`에 있다. 처음의 잘린 원문과 크롬 회수 이력은 `reference-excerpt.md`, `reference-chrome-supplement.md`, `REFERENCE-ACCESS.json`에 보존했다.
