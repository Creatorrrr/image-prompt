**후보 데이터 무작위 1,000개 의미 품질 감사 — 2026-10-13**

대부분의 후보는 실제 사물·형태·관계 또는 유효한 촬영/서사 맥락을 담고 있다. 다만 의미가 다른 부품·별칭의 혼합, 특정 과학 변형의 과도한 일반화, 잘못된 슬롯과 효과 대상, 후보 의미와 맞지 않는 적용 조건이 확인됐다. 데이터 품질을 충분히 정리된 상태로 보기는 어렵다. 아래의 98%는 내용의 중심 의미가 명료하다는 이번 정성 판정이며, 데이터 전체의 정확도나 검색·생성 성공률은 아니다.

| 검토 축 | 결과 | 분모와 해석 |
|---|---:|---|
| 중심 의미가 명료하고 일관됨 | 980개 / 98.0% | 무작위 표본 1,000개 |
| 의미/시각 단서 보강 필요 | 14개 / 1.4% | 추상적 단서, 모호한 비유, 의미 필드에 섞인 작성 지시 |
| 의미 불일치·정의 범위 문제 | 5개 / 0.5% | 부품·별칭·원전·한영 주체 범위 불일치 |
| 전문 표현 세부 확인 보류 | 1개 / 0.1% | prix seam의 추가적인 맞댄 경계 설명 |
| 기존 슬롯 태그 적합 | 653개 / 94.4% | persistent binding이 있는 692개 |
| 범위가 넓지만 관련 있는 태그 | 30개 / 4.3% | 위 692개; 자동 오류로 계산하지 않음 |
| 기존 슬롯 태그 부적합 | 9개 / 1.3% | 위 692개 |
| persistent binding 없음 | 308개 | 프로필 196, 번들 106, 관계 메커니즘 6; 허용된 구조 |
| ko 필드의 한국어 설명 누락 | 45개 | 영어가 그대로 들어 있는 옵션; 의미 부재와 다름 |
| ko/en 내용·범위 차이 | 23개 | 의도적인 제목/구체 변형 차이도 가능 |

검토 축은 겹친다. 태그가 맞고 문장 의미가 명료한 후보도 적용 조건에 막힐 수 있으므로 각 행을 더해 전체 오류 수로 사용하면 안 된다. 슬롯이 없는 308개를 모두 태그 누락 오류로 처리하지도 않았다. 공통 풀의 profile/bundle/mechanism은 현재 binding 없이 존재할 수 있다. 관련 역할 제안은 판정표에 기록했으며 새 태그를 적용하지 않았다.

실질적인 문제를 대표하는 원본은 다음과 같다.

| 원본 | 문제 | 필요한 정리 |
|---|---|---|
| [#83](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/candidate-quality-random-1000-20261013/samples.jsonl:83) | 뒷밴드 훅앤아이 여밈이 재표현·속성에서는 브라 어깨끈 조절로 바뀜 | 실제 부품의 소유자와 변경 속성을 일치시키기 |
| [#503](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/candidate-quality-random-1000-20261013/samples.jsonl:503) | EL 와이어에 가스 방전 유리관이 aliases로 붙어 있음 | 다른 방식의 물체를 별칭으로 연결하지 않기 |
| [#123](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/candidate-quality-random-1000-20261013/samples.jsonl:123) | 강착원반 시각화에 시점 의존적인 밝기 비대칭을 보편 조건으로 요구 | 선택된 관측 시점을 명시하기 |
| [#642](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/candidate-quality-random-1000-20261013/samples.jsonl:642) | 피부의 바디페인트가 garment_detail이고 효과 대상도 wardrobe | body_marking 및 피부 소유자로 정리하기 |
| [#396](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/candidate-quality-random-1000-20261013/samples.jsonl:396) | 나뭇잎의 얼룩빛이 light_direction에 들어 있음 | 패턴과 방향을 분리하기 |
| [#302](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/candidate-quality-random-1000-20261013/samples.jsonl:302) | TikTok 표현 감성이 world/setting 변경으로 등록됨 | 플랫폼·스타일의 역할을 구분하기 |

EL 와이어의 형광체 코팅 구조는 [Adafruit 기술 문서](https://learn.adafruit.com/el-wire/)로 확인했다. 원반 밝기 비대칭의 시점 의존성은 [NASA 시각화 설명](https://svs.gsfc.nasa.gov/13326)으로 확인했다. 나머지 의미 불일치 2개와 슬롯 부적합 9개 전체, 보강 대상 14개 및 한영 차이 23개는 [상세 발견 목록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/candidate-quality-random-1000-20261013/FINDINGS.ko.md)에 원본 링크와 함께 기록했다.

적용 조건에서는 의복 소재 후보 12개가 사람을 설명하면서 기본 subject_categories에서는 human을 제외하고 있었다. 현재 정책 함수를 인물·패션 계약으로 호출했을 때 12개 모두 거부됐으며, CJK 세계관 도메인의 override 조건에서는 허용됐다. 따라서 후보가 항상 검색 불가한 것은 아니지만 일반 패션 용도와 적용 범위가 충돌한다. 상품 매크로 촬영 후보 #995도 object/product 계약에서 거부됐다. [조건별 함수 입력과 반환값](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/candidate-quality-random-1000-20261013/GUARD-PROBES.json)은 실제 함수로 재현한 근거다. 이 검사는 합성 계약의 정책 판정이며 전체 검색 순위·회수율 검사는 아니다.

중복 검사는 표본 안에서 identity/provenance를 제외한 content+effects 완전 일치 0그룹, 실제 양성 인덱스 recipe+text 완전 일치 0그룹이었다. 핵심 의미 문장이 겹치는 것은 17그룹, 34개 후보였다. 전부 서로 다른 종류의 옵션·프로필·번들 사이의 반복이며 각자의 사용 계약이 다르다. 이를 무조건 같은 canonical ID로 합치면 활성화·증거·구성 계약을 잃을 수 있다. 이번 결과로 전 데이터의 의미 중복이 없거나 검색 순위에 반복 편향이 없다고 판단할 수는 없다. 비교 방식과 그룹은 [REPETITION-CHECKS.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/candidate-quality-random-1000-20261013/REPETITION-CHECKS.json)에 보존했다.

정상적인 좁은 변형도 구분했다. 크리놀렛의 평평한 앞과 뒤쪽 구조는 [V&A](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)가 뒷받침한다. 선택된 헤바즈라의 손·컵·배우자 특징은 [Himalayan Art의 해당 작품](https://www.himalayanart.org/items/90531), 테필린의 머리·위팔 착용은 [Chabad의 구성 설명](https://www.chabad.org/library/article_cdo/aid/1921512/jewish/Purchasing-Tefillin-A-Buyers-Guide.htm)과 대조했다. 혜성 꼬리의 넓은 의미에서의 태양 반대 방향은 [NASA 설명](https://spaceplace.nasa.gov/comets/en/)에 맞아 초기 의심을 해제했다. 장르·의도·신화·문화의 선택된 표현을 그 전체의 유일한 정의로 취급하지 않았다.

표본은 canonical 후보 18,250개 전체에서 단순 무작위 비복원으로 1,000개를 추출한 것이다. 종류·슬롯 quota와 재추출은 없었다. 난수 seed는 `168994301657083962123452681460976404683`이고, 정렬된 전체 ID 목록에 Python Random.sample을 적용했다. 표본 종류는 옵션 692, 프로필 196, 번들 106, 관계 메커니즘 6개이며 112개 catalog 슬롯 중 88개가 기존 binding으로 나타났다. diagnostic 및 relationship_concept는 이번 난수 표본에 없었다. 희소 종류나 모든 슬롯의 의미 품질을 별도로 보장하는 검사 결과는 아니다.

모든 표본의 핵심 의미·한영 표현·관계·효과·binding을 중복 문구를 줄인 카드로 개별 읽고, 의심 사례는 원본 필드와 공통 적용 조건 및 제한을 추가 대조했다. 단순 문자열 규칙이나 schema 통과로 의미 판정을 자동 생성하지 않았다. 처음 판정과 재확인 후 변경은 [ADJUDICATIONS.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/candidate-quality-random-1000-20261013/ADJUDICATIONS.json)에 남겼다. 한글 설명과 영어 구체 변형의 차이가 최초 작성 의도인지 이관 오류인지까지는 이 감사만으로 확정하지 않는다. 문화·과학 전문 항목도 선택된 근거를 대조한 범위이며 모든 세부의 전문가 인증은 아니다.

검증에서는 고정 seed로 동일한 1,000개와 동일 순서를 재현했고, 모든 판정의 ID·원본 SHA·binding을 대조했다. 후보·정책·catalog·manifest를 포함한 원본 파일 35개의 SHA가 일치했고 참조 후보 224개도 현재 원본과 일치했다. native 구조 검사는 18,250개 후보와 12,020개 binding에서 통과했다. HEAD `3f9a31a9e898a0604b1a0b07e8a76ea252ca8634`, runtime generation `6028917cf30299b9996122cbfdc1d49ea925e66fa6331c3b777c06f87beb1d12`, source fingerprint가 유지됐다. 기존 수정 중인 문서 2개도 바뀌지 않았다. [검증 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/candidate-quality-random-1000-20261013/VERIFICATION.json)에 비교값과 결과를 저장했다.

우선 수정 방향은 다음과 같다.

1. 실제 부품·장치 의미가 바뀌는 정의·별칭·원전 차이 5개와 피부/의복/그림자처럼 효과 대상이 다른 항목을 정리한다.
2. 소재 및 촬영 후보의 적용 조건을 실제 용도와 맞춘다. 사람·패션과 오브젝트·상품의 대표 계약을 함께 검증한다.
3. 부적합 태그 9개를 바로잡고 넓은 관련 태그 30개에는 필요한 추가 역할을 검토한다. binding 없는 프로필·번들은 역할 계약을 고려해 태그를 보강한다.
4. ko/en을 제목과 구체 변형으로 명시적으로 구분하고, 영어가 그대로 있는 ko 45개와 내용·범위 차이 23개를 정리한다. 작성 지시를 시각 의미 필드에서 분리한다.
5. 데이터 수정 뒤에는 그 변경의 영향을 받는 검색 텍스트·임베딩을 갱신하고 소유자·방향·부품 경계 검색을 검증한다. 이번 감사는 기존 벡터의 의미 품질이나 이미지 결과를 검증한 작업이 아니다.

전체 결과는 [1,000행 판정표](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/candidate-quality-random-1000-20261013/SAMPLE-RESULTS.csv), [개별 판정 JSONL](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/candidate-quality-random-1000-20261013/reviews.jsonl), [집계 JSON](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/candidate-quality-random-1000-20261013/RESULTS.json)에서 확인할 수 있다. 완전한 원본은 [samples.jsonl](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/candidate-quality-random-1000-20261013/samples.jsonl), 추출 및 원본 고정값은 [SAMPLE-MANIFEST.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/candidate-quality-random-1000-20261013/SAMPLE-MANIFEST.json), 평가 기준은 [METHOD.ko.md](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/candidate-quality-random-1000-20261013/METHOD.ko.md)에 있다.

이번 작업은 감사 자료만 새로 저장했다. 후보 데이터·binding·임베딩·runtime는 수정하지 않았고 이미지 또는 임베딩 API 호출, 커밋, 푸시는 하지 않았다. Codex의 정성적 텍스트 판정이며 독립 전문가 합의·실서비스 요청·생성 이미지 및 실제 픽셀 검증을 대체하지 않는다.
