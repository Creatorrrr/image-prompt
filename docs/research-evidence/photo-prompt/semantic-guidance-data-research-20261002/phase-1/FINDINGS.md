# 시각 의미 데이터 보강 — 첫 조사 묶음 결과

조사일: 2026-10-02. 앞서 정한 **12개 개념군·15개 기존 프로필**의 실제 용례와 구조를 조사하고, **14개 개념 설명 카드·56개 이름 없는 한영 묘사·42개 변형 초안·84개 한영 문맥 사례 쌍**을 작성했다. 이는 출처를 바탕으로 작성한 연구용 데이터이며, 전문가가 승인한 정답 집합이나 생성 결과는 아니다.

현재 데이터에 필요한 보강은 **일반적인 용어 뜻과 프로젝트가 선택한 특정 형상을 연결하되, 서로의 범위를 같다고 만들지 않는 것**이다. 두 번째 목적에서도 이름을 지운 뒤 같은 물체의 부착·층·방향 관계가 남아야 한다. 표현을 바꾸면서 형상까지 바뀌면 다른 변형으로 기록해야 한다.

## 조사 범위와 산출물

새 출발점은 HEAD `0ed2267b91e73f4b4d1493d095287e7795ebf805`, 로더가 읽은 **1,419개 프로필**이다. 앞선 조사안의 1,385개는 이전 스냅샷 수치로 보존했다. 이번에 선택한 15개 프로필은 목적에 따른 표본이며 전체 데이터 품질이나 사용 빈도를 대표하지 않는다. [현재 소스 스냅샷](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/semantic-guidance-data-research-20261002/phase-1/source-snapshot.json)

| 산출물 | 수량·범위 | 읽는 곳 |
| --- | --- | --- |
| 1차 출처 | 20건. 직접 읽은 정의·본문 외에 검색 색인 발췌와 본문 미확인 자료도 포함 | [출처·확인 범위](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/semantic-guidance-data-research-20261002/phase-1/sources.json) |
| 개념 설명 | 12군을 14카드로 분리. sheer/mesh와 broad/short를 각각 나눔 | [사람이 읽는 상세 자료](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/semantic-guidance-data-research-20261002/phase-1/CONCEPTS.md), [구조화 자료](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/semantic-guidance-data-research-20261002/phase-1/concept-cards.json) |
| 이름 없는 묘사 | 카드마다 짧은·상세 문장을 한국어·영어로 각각 작성, 총 56문장 | 개념 카드의 `neutral_descriptions` |
| 변형 | 카드마다 세 가지, 총 42개. 선택 범위를 유지하도록 작성한 초안 | 개념 카드의 `variants` |
| 문맥 사례 | 카드마다 긍정 3쌍·경계 3쌍, 총 84쌍·168문장 | [문맥 사례](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/semantic-guidance-data-research-20261002/phase-1/context-cases.jsonl) |
| 기존 필드 추가안 | 15개 프로필의 재서술·반례·한계에 대한 추가안. 미적용 | [필드별 초안](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/semantic-guidance-data-research-20261002/phase-1/profile-data-proposals.json) |
| 실제 참고 화면 주석 | 박물관 카울 의복과 제작자 셔링 견본 2건 | [관찰과 권리 범위](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/semantic-guidance-data-research-20261002/phase-1/reference-observations.json) |

## 문맥상 뜻을 안내하는 자료에서 발견한 경계

| 개념군 | 조사 결과 | 데이터에 기록한 보강 |
| --- | --- | --- |
| pilot | 항공 조종자 외에 방송·시험·선박·점화 불꽃 의미가 있다. 조종사 직업과 현재 프로필의 운항 중 장면도 범위가 다르다. | 같은 단어의 다른 뜻, 직업은 맞지만 운항 관계를 요청하지 않는 카페 인물 사진을 구별 |
| one piece | 영어의 한 벌 의복은 수영복·바지형 의복에도 쓰인다. 현재 한국어 드레스 문맥보다 넓다. | 한 벌인 드레스와 한 장의 천·상하의 두 벌·수영복·작품명을 구별 |
| corruption | 일반 사전은 부정행위·파일 변질·부패 등을 나눈다. 일본어 창작 용례는 인물 상태 전환을 제공한다. | 현재의 몸 위 미완료 변화 경계를 모든 흑화·서사 변화의 뜻으로 확대하지 않음 |
| kuudere | 1차 원어 발췌는 차분한 외면과 상대를 향한 호의의 결합을 지지한다. 실용적 도움을 항상 해야 한다는 근거는 확보하지 못했다. | 일반 용례와 현재 프로젝트의 구체적인 성인 도움 장면을 구별. 무표정·직무 서비스·큰 감정 반전을 경계 사례로 작성 |
| cowl | 두건·기계 덮개·드레이프 목둘레 등 뜻이 있고, 스카프처럼 생긴 목둘레도 실제 카울 용례다. | 별도 스카프인지 같은 옷의 목둘레인지 부착 관계로 구별. 두꺼운 니트 칼라는 다른 변형으로 기록 |

pilot와 corruption은 사전의 편집된 정의를 사용했다. 자동 수집된 최신 뉴스 예문이나 독자 리뷰를 개념 근거로 삼지 않았다. [Merriam-Webster pilot](https://www.merriam-webster.com/dictionary/pilot), [corruption](https://www.merriam-webster.com/dictionary/corruption)

영어 one-piece의 범위는 사전에서 확인했지만, 국립국어원 개별 항목의 직접 확인은 완료하지 못했다. 따라서 한국어 원피스의 범위를 외부 사전으로 검증했다고 기록하지 않고 **현재 프로젝트가 선택한 드레스 의미**로 한정했다. [Collins one-piece](https://www.collinsdictionary.com/us/dictionary/english/one-piece)

쿠데레의 두 1차 자료는 발췌·저자 페이지까지 확인했다. PDF 전체 또는 정확한 발췌 위치의 직접 확인은 남아 있다. 성별·나이·외양·특정 상대 설정을 한 제품이나 작품에서 가져와 보편 조건으로 만들지 않았다. [FLIGHT 공식 자료](https://www.flight.co.jp/uploaded_files/c_news/106_detail.pdf), [Togashi 저자 자료](https://www2.ic.daito.ac.jp/jtogashi/t09a.html)

## 이름 없이 형상을 묘사하는 자료에서 발견한 경계

| 개념군 | 보존해야 하는 형상 | 이름만 바꾸면서 손실하기 쉬운 부분 |
| --- | --- | --- |
| cowl | 같은 옷 목둘레의 부착점 사이에서 천이 처지고 연속된 가장자리·겹 그림자를 가짐 | 별도 스카프나 평평한 V자 선으로 치환 |
| one-shoulder | 같은 상의가 한 어깨 위에서 지지되고 반대 어깨는 같은 비대칭 목둘레 밖에 있음 | 끈 수를 어깨 수로 착각하거나 숨겨진 두 번째 지지점을 무시 |
| ruching | 지정한 한 패널의 봉제선·고정점으로 작은 주름이 모이고 주변 천과 연속됨 | 무관한 구김·플리츠·장식 띠를 같은 뜻으로 처리 |
| sheer / mesh | sheer는 빛 투과와 층 관계, mesh는 실 사이의 실제 열린 공간 | 투과와 구멍을 동의어로 처리하거나 격자 프린트로 치환 |
| corset 구조 | 현재 변형은 좌우 앞판의 고리·돌기 쌍이 맞물리는 앞면 잠금 | 내부의 단단한 버스크, 뒤 끈, 잘록한 윤곽으로 앞면 잠금을 대체 |
| split diopter | 현재 변형은 동시에 선명한 근·원거리 대상, 더 부드러운 사이 깊이·전환, 연속된 공간 관계 | 모든 깊은 초점이나 화면 분할을 같은 효과로 처리 |
| halation | 현재 변형은 매우 밝은 경계 바로 밖의 얇고 따뜻한 국소 번짐과 세부 유지 | 전역 붉은 색 보정·안개·색수차로 치환 |
| broad / short | 카메라에 넓게·좁게 보이는 얼굴 면 중 어느 면이 주광을 받는지 | 고정 좌우만 적거나 그림자 때문에 얼굴 방향 단서를 지움 |

섬유 산업 자료는 메시의 실제 열린 공간을 설명한다. 사전의 sheer는 직물의 얇고 투명한 성질을 구별한다. 두 자료는 실제 아래층·셀 모양·재료별 투과량까지 정하지 않는다. 이 초안의 안감 예시는 **불투명한 천 아래층을 선택한 변형**이며, 아래층이 다른 원래 요청을 그대로 보존했다고 기록하지 않는다. [CottonWorks mesh](https://cottonworks.com/encyclopedia-item/mesh/), [Merriam-Webster sheer](https://www.merriam-webster.com/dictionary/sheer)

실용적 제작 자료와 박물관 사례는 명칭의 범위가 현재 프로필보다 넓을 수 있음을 보여줬다. 기계 셔링과 자수 스모킹, 내부 버스크와 분할 앞면 잠금, 스카프 같은 카울과 실제 독립 스카프를 각각 구별했다. [Seamwork shirring](https://www.seamwork.com/sewing-tutorials/a-guide-to-elastic-shirring), [V&A corsets](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear), [Met 카울 사례](https://www.metmuseum.org/art/collection/search/155680)

광학 출처가 설명하는 일반 현상과 현재 선택 조건도 같지 않다. 반쪽 보조 렌즈의 모든 사용이 중앙에 흐린 띠를 남기는 것은 아니며, Kodak의 일반 할레이션 설명은 모든 결과가 붉어야 한다고 정하지 않는다. 초안에서는 현재 프로필의 부드러운 사이 영역과 따뜻한 번짐을 유지하면서 그 한계를 기록했다. [Schneider-Kreuznach](https://schneiderkreuznach.com/application/files/5717/0142/0920/Fact_Sheet_Diopter_Split_GEN2_Schneider-Kreuznach.pdf), [Kodak](https://www.kodak.com/content/products-brochures/Film/kodak-essential-reference-guide-for-filmmakers.pdf)

브로드·쇼트는 머리 회전과 카메라에 보이는 얼굴 면을 기준으로 작성했다. 사진 제작자의 설명은 두 관계를 직접 구별하지만 얼굴이 더 아름답다는 평가나 실제 성격을 데이터 조건으로 가져오지 않았다. 본문은 검색 색인의 원문 텍스트로 확인했으며 참고 사진 자체는 관찰하지 않았다. [Profoto / John Russo](https://www.profoto.com/lv/en/still-photography/profoto-stories/character-portraits-with-john-russo-and-profoto-d2)

## 기존 데이터에 연결하는 방식

`profile-data-proposals.json`은 기존 `semantics.paraphrase_examples`, `semantics.contrast_examples`, `semantics.claim_limits`에 넣을 수 있는 **추가 문장**만 담는다. 정의·정확 활성어·표현 모드·컴포넌트·증거 조건·픽셀 게이트는 수정하지 않았다. 변형과 출처는 외부 개념 카드에 보관했다.

작성 자료의 짧은·상세 묘사는 각 개념의 이름을 사용하지 않고 대상과 관계를 기술한다. 이 문자열 검사는 이름이 빠졌음을 확인하는 것이며, 모든 문장이 모델에서 무난하게 받아들여지거나 같은 픽셀을 만든다는 검사와 다르다. 기존 증거 필드의 문자 조건은 그대로이므로 **재서술 문장을 늘렸다는 사실만으로 현재 실행 경로가 그 문장을 채택하거나 통과한다고 주장할 수 없다.**

특히 `pfe_cowl`과 `clothing_ct037_v1`은 뜻이 겹쳐 한 조사 카드에 연결했지만, 전자의 상세 관찰 조건을 후자의 보편 필수 조건으로 자동 승격하지 않았다. 변형 세 가지를 동시에 만족할 조건으로 합치지도 않았다.

## 검증한 범위

- 14카드·20출처·84사례의 고유 ID, 출처·프로필 연결, 한영 문장 누락 여부를 확인했다.
- 15개 프로필의 추가안은 세 가지 기존 의미 필드만 가리키며, 동결한 원본 프로필 해시에 연결된다.
- 56개 이름 없는 묘사에서 해당 개념 이름이 빠져 있음을 확인했다.
- 조사 시작 때 기록한 **기존 `skills` 추적 파일 429개와 대상 프로필 15개가 동일**했다. 로더 결과도 1,419개였다.
- 생성·모델 해석·검색 활성화·검열 통과율·픽셀 형상 충족은 실행하지 않았다. 84쌍의 사례는 작성용 자료이며 독립 검증용 홀드아웃이 아니다.

[검사 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/semantic-guidance-data-research-20261002/phase-1/validation-results.json), [검사 코드](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/semantic-guidance-data-research-20261002/phase-1/verify_research.py), [출력과 코드를 함께 보는 노트북](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/semantic-guidance-data-research-20261002/phase-1/research-checks.ipynb). 노트북 셀은 표준 라이브러리 Python으로 순서대로 실행해 출력을 보존했으며 Jupyter 커널 실행은 아니다.

참고 이미지는 정상 페이지의 화면으로 카울 의복과 셔링 견본 두 건만 직접 봤다. 카울 페이지의 확대·다운로드 제한과 셔링 튜토리얼의 미확인 재사용 권리를 기록했고, 원격 이미지 파일을 수집·재게시하지 않았다. 픽셀에서 본 천의 처짐·주름과 소장품·제작 설명의 사실을 별도 항목에 적었다. 내부 봉제·탄성·재단은 사진 관찰만으로 확인하지 않았다.

## 다음 데이터 조사에서 먼저 채울 공백

| 우선순위 | 남은 공백 | 확보할 구체적인 자료 |
| --- | --- | --- |
| P0 | 쿠데레 원어의 의미 범위와 한국어 원피스의 번역 범위 | 두 원어 PDF의 정확한 본문 위치, 국어사전 개별 항목, 독립 원어 검토 기록 |
| P0 | 작은 부착·잠금·셀의 실제 참고 형상 | 앞뒤 연결이 보이는 현대 one-shoulder 도해, 버스크 대응 부품의 제작자 접사, 튤 셀 구조 도해와 권리 확인 사진 |
| P1 | 일반 개념과 현재 효과 변형의 시각적 경계 | 두 초점 면과 깊은 초점 비교, 국소 할레이션과 블룸·색수차 비교, 같은 얼굴의 broad/short 비교 |
| P1 | 작성 문장의 독립적인 의미 보존 | 이 84쌍을 재사용하지 않고 새 문맥을 따로 작성하여 대상·부착·층·방향의 복원 여부를 검토 |

모델이 어떤 개념을 실제로 모르거나 어떤 단어를 차단하는지는 현재 메타데이터와 문서 조사만으로 알 수 없다. 이번 묶음은 그 측정을 했다는 주장 없이, 두 목적에 필요한 구체적인 의미 자료와 구조 묘사의 초안을 확보한 결과다.
