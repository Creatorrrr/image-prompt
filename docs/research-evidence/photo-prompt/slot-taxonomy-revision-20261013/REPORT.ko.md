# 슬롯 정비 0~3단계 리포트

사용자가 지정한 「이미지 특징 요소 정리」의 전체 45개 분류를 대조해 역할을 정비했다. 원래 슬롯 112개에서 6개 총칭·중복 역할을 통합/분해하고, 30개 역할을 추가하여 136개 평면 역할 태그로 전환했다. 후보 본문은 공통 풀에서 한 곳에만 존재하고 각 역할은 전체 positive 풀을 독립 BM25F·실제 임베딩으로 검색한다.

| 항목 | 전 | 최종 |
|---|---:|---:|
| canonical 후보 | 18,250 | 18,250 |
| positive 검색 문서 | 18,186 | 18,186 |
| 관리 역할 | 112 | 136 |
| 영속 연결 | 12,020 | 12,089 |
| 연결에 중복된 효과 사본 | 12,020 | 0 |
| 차원이 비어 있던 역할 | 10 | 0 |

## 의미와 조건

모든 역할에 영한 설명, 대상·소유 범위, 구체 속성 경로, 포함·제외 경계, 이웃 역할, core focus와 제시 우선순위를 둔다. 모발 색과 의복 커프, 광원 방향과 빛무늬, 실제 표면과 영상 흔적, 초점면과 심도, 촬영 거리와 shot scale, 물리 움직임과 기록된 blur, 사진 안의 글자와 외부 캡션을 구별한다. 맥락 역할의 원인·정체·사건 해석을 관찰 사실로 자동 승격하지 않는다.

후보 필수 조건과 효과는 canonical 후보에서 한 번 소유한다. 연결은 역할 적용 조건만 가지며 후보 조건을 덮거나 효과 사본을 보유할 수 없다. 조건을 만족하는 후보의 발견과 잠긴 의미를 바꿀 자격을 구별하고, 모든 역할 제시에서 canonical 효과와 속성 잠금을 검사한다. 기존 역할 조건의 실패를 동일 역할의 무연결 제안으로 우회하지 않는다.

## 기존 관계의 완전 대응

BINDING-MIGRATION.jsonl은 기존 연결 12,020개 전부의 후보 ID·새 관계·새 역할·조건 보존 근거를 기록한다. 혼합 슬롯 후보 682개를 대조했고 213개 ID에 명시적인 경계 결정을 기록했다. 복합 의미에 69개 연결을 추가했으며 후보 본문·ID·출처와 positive embedding 본문은 전부 유지한다. 같은 후보와 역할의 중복 관계 및 고아 참조는 없다.

- body_framing·partner_framing은 subject_framing 및 실제 배치 관계로 이관했다. 일반 subject_framing이 객체도 다루면서 기존 인물 연결의 조건은 보존한다.
- material은 surface_material로 통합했다. quality·frame_anchor_medium·distance_narrative의 후보는 실제 영상·피부·배치·간격·광학 역할로 분해했다.
- motion의 물리 운동, 기록된 streak/blur, 카메라 지지를 구별했다. medium의 인쇄/사진 매체와 장르·게시 목적·촬영 구성을 구별했다.
- person_origin은 declared_person_background, costume_style은 attire_context, adult_context는 adult_presentation_context처럼 의미 범위를 명시했다.

quality 후보 57개의 rendering.quality 총칭 효과를 실제 소유 속성으로 정리했다. 최종 대조에서 깃털은 체모로 분류하지 않고, fantasy라는 일반 장르 표현에서 새로운 세계 규칙을 추론하지 않으며, 영상의 선명도·흐림에서 광학 경로나 공기 상태를 단정하지 않게 7개 항목을 보정했다. EFFECT-REFINEMENTS.json과 FINAL-BOUNDARY-CORRECTIONS.json에 근거가 있다.

운영 catalog·소비자·coherence 참조에서 폐지 슬롯을 제거했다. 숨은 슬롯 우선순위·query focus·기본 적용 표도 제거하고 현재 catalog를 읽는다. core.camera.capture_mode, 의미 차원 material/atmosphere, 역사 provenance·본문 키워드는 슬롯 ID가 아니므로 보존한다. native 원본 V2·독립 질의 V2·팩 V9가 운영 계약이며 옛 계약을 fallback으로 수용하지 않는다.

## 검증

전체 사진 테스트 370개는 3단계 이관 checkpoint에서 통과했다. 마지막 7개 원본 의미 보정과 미사용 guard_role 조회 제거 후, 최종 원본에서 관련 회귀 123개가 통과했다. 전체 370개를 그 뒤 다시 실행했다고 보고하지 않는다. 최종 원본의 모든 ID·본문·조건·관계·소유 경계와 새/옛 슬롯 거절을 전수 비교한다. 이전 실패·중간 source/build 및 중단된 실험은 최종 성공으로 바꾸지 않고 보존한다.

18,186개 본문과 recipe가 모두 동일해 벡터를 모두 재사용했다. 최종 문서 embedding provider 호출은 0개다. 전체 payload·posting·float64 vector·routing closure를 검증한 native generation을 발행했다.

최종 source `fbc108f6fa97380a56a6f26542931ec18e1f7ef2888ea0e1e00350cf1bc3dc29`와 generation `46ee782459a942b211aa6f9260a784e5ab91a308e61ceeee0485721f30e41d3e`에서 다음을 통과했다. 상세 수치·순위·실제 provider trace·캐시 경위는 STAGE03-HYBRID-VERIFICATION.json과 각각의 contexts/retrieval 파일에 있다.

- 객체 문맥 136개 역할과 인물 문맥 136개 역할의 독립 영어 검색, 의미 경계가 중요한 인물 한국어 검색 14개: **실제 질의 286개**. 전체 positive 문서 18,186개에서 후보 필수 조건을 적용한 후 검색하며 슬롯 태그로 검색 대상을 나누지 않는다.
- 모든 질의의 BM25F·exact cosine·RRF가 offline 전체 스캔과 동일했고, 각 cosine skip certificate도 재검산했다. 태그가 없는 후보나 다른 태그만 있던 후보의 제시 경로를 유지한다.
- cold acquire 시 payload·posting·vector 본문 읽기 0. 각 질의의 vector leaf 읽기는 2006~2614/3850개이며 필요한 범위의 bytes를 읽는다. cache peak 67,108,863 bytes는 64MiB 이내이고 vector descriptor 61개는 64개 한계 이내다. 정확도를 증명할 수 없는 영역을 임의로 생략하지 않는다.
- 대표 네 역할의 실제 V9 팩 발행·영수증 재검산·선택 후보를 모두 거절하는 합성 감사가 통과했다. 전체 역할 검색 및 64개 unique presentation allocation은 별도의 전체 검색 record에서 검증한다.
- 이 최종 실행은 query provider 150개와 정확히 바인딩된 캐시 136개를 사용했다. 중간 실행까지 포함한 durable 성공 요청은 2단계 8개와 3단계 286개이며 모두 성공 상태다. 문서 embedding 신규 호출과 이미지 생성은 0개다.

이 결과는 고정 유지보수 객체/인물 문맥의 검색·조건·순위·I/O 검증이다. 모든 사용자 질의의 의미 정확도나 이미지 픽셀 품질을 일반화하지 않는다.

## 남은 범위

이번 실행은 슬롯 체계 정비와 기존 관계 이관인 0~3단계다. 전체 18,250개에 적합한 신규 다중 태그를 심사·추가하는 4~8단계는 남아 있다. 새 역할 18개에는 아직 영속 연결이 없고 연결 없이도 전체 풀을 검색한다. 이를 채우려고 후보를 복제하거나 최소 태그 수를 강제하지 않았다. 다음은 정비된 catalog를 기준으로 500~800개 pilot을 심사하는 4단계다.

코드·원본·검색 무결성 검증과 모든 후보의 의미 심사, 전문가 검증, 생성 이미지 품질은 별개다. 구체 효과·소유 근거가 부족한 후보는 review_required이며 검증된 직접 역할로 보고하지 않는다. 이번 작업으로 전체 데이터의 의미 품질이나 생성 이미지 품질을 인증하지 않는다.
