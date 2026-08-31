# 죽음 계열 시각 의미 후보팩 연구·5-arm 렌더 검증

## 결론

네크로맨서, 인간 유령, 한국 저승 인도자, 서구 Death 의인화, 허구 인체 유해를 각각 별도 시각 프로필로 구현했다. 5개 프로필, 49개 후보 원자, 9개 승인 연구 근거, 정밀 라우팅·혼동 경계·픽셀 게이트가 추가됐다. 기존 시각 의무 23개와 신규 의미 테스트 7개는 모두 통과했고, 사전 생성된 시각/의미 인덱스도 최신 상태다.

독립 이미지 실험에서는 모든 arm의 합성 프롬프트와 실제 렌더 요청 감사가 통과했다. 목표 프로필만 보면 3/5 arm이 모든 게이트를 통과했고 전체 25개 게이트 중 23개가 통과했다. 그러나 하드 게이트는 평균내지 않으므로 네크로맨서와 서구 Death arm은 실패다. 또한 참조 외모 및 동결된 복합 장면 세부까지 포함하면 5개 모두 최소 하나의 미해결 편차가 있어 대표 승격하지 않았다. 사용자 심미 판단은 5개 모두 미수신이다.

## 데이터화한 의미와 혼동 경계

| 프로필 | 관찰 가능한 필수 의미 | 실패시키는 대표 대체물 |
|---|---|---|
| `necromancer_dead_causality` | 살아 있는 조작자 → 특정 망자 앵커 → 국소 응답 → 물리적 결과 | 해골 소품, 어두운 로브, 일반 마법진, 수동 영매, 퇴마 장면 |
| `human_ghost_identity_breach` | 한 생전 인물의 연속성 → 하나의 일관된 존재론적 위반 → 국소 행동/흔적 | 장노출 블러, 안개, 홀로그램, 보통 거울상, 실체 언데드 |
| `korean_afterlife_guide_escort` | 인도자 + 사망 여행자 + 같은 여행자를 위한 인도 행동 + 통과 경계 | 검은 옷·갓만 있는 인물, 서구 해골 사신, 여행자 없는 문지기 |
| `western_death_personification` | 구현된 Death 행위자 + 종말/죽음 행동 + 변한 대상 | 해골·모래시계 정물, 단순 코스튬, 한국 저승사자, 장례 조문객 |
| `fictional_human_remains_inert_dignity` | 전신 외부 지지 + 비행위 상태 + 인체/영안 맥락 + 비그래픽 존엄 처리 | 잠든 사람, 의식불명 환자, 마네킹, 빈 시신보, 좀비, 실제 사망 진단 |

`죽음` 같은 광범위 추상어는 단독 exact hard activation으로 만들지 않았다. `사체`도 동물/인간 구분 없이 자동 매핑하지 않는다. 반면 문맥이 충분한 `시신`, `시체`, `저승사자`, `necromancer`, `human ghost`, `grim reaper` 등은 각자의 문맥 제한과 혼동 차단 규칙 아래 라우팅된다.

## 연구 근거

- UCL의 네크로맨시 역사 연구: 특정 망자와의 질문·응답 관계를 현대 판타지 코스튬과 분리했다. <https://discovery.ucl.ac.uk/1541259/1/Page.OIHM.book.chapter2.pdf>
- Metropolitan Museum의 Witch of Endor 자료: 특정 망자 현현과 인식 가능한 앵커의 역사적 도상 근거로 사용했다. <https://www.metmuseum.org/art/collection/search/884929>
- WHO 사망 확인 가이드: 정지 이미지로 실제 사망·원인·신원을 판정하지 않는 불확실성 경계를 세웠다. <https://www.who.int/publications/i/item/WHO-HIS-SDS-2017.5>
- INTERPOL DVI: 유해의 존엄한 처리·기록·식별 절차를 비그래픽 후보로 추상화했다. <https://www.interpol.int/en/How-we-work/Forensics/Disaster-Victim-Identification-DVI>
- Metropolitan Museum의 spirit photography 자료: 유령 의미와 장노출/다중노출 캡처 관습을 구분했다. <https://www.metmuseum.org/art/collection/search/294772>
- 한국민족문화대백과의 귀신 및 저승사자 항목: 원귀의 생전 관계·미해결 귀환과 저승 인도자의 역할을 분리했다. <https://encykorea.aks.ac.kr/Article/E0007205>, <https://encykorea.aks.ac.kr/Article/E0072772>
- Metropolitan Museum의 vanitas 자료와 British Museum의 Death 자료: 죽음 상징 정물과 능동적 서구 Death 행위자를 구분했다. <https://www.metmuseum.org/art/collection/search/436485>, <https://www.britishmuseum.org/collection/term/BIOG68251>

연구 근거는 관찰 축과 혼동 경계를 지원할 뿐, 특정 작품의 문구·구도·의식을 복제하는 런타임 지시로 쓰지 않았다.

## 검증

- 사전 검증: 모든 arm의 candidate-pack v6, composed prompt, exact render request PASS
- 인덱스: 87 profiles, 513 exact terms, 6,959 semantic entries, dictionary hash `8c67703a90d5bc91d7eaee2d470957c4f5a44fdb78bb9966b6f0c9519ae303ee`
- 테스트: 기존 visual-obligation 23/23 PASS, 신규 death-semantics 7/7 PASS
- 생성: 내장 image generation, 독립 arm 5개, arm당 1회, 재시도 0회, 로컬 이미지 5개 저장
- 참조: 첨부 사진은 외모 대조군으로 실제 첨부했다. 가시적 성인 외모 연속성만 검토했고 생체인식 동일인 검증이나 유사도 점수는 만들지 않았다.

## 5-arm 결과

| arm | 목표 의미 게이트 | 참조 외모 | 동결 복합 장면 편차 | 대표 승격 |
|---|---:|---|---|---|
| 네크로맨서 천문대 | 4/5 FAIL | PASS | 변한 바늘의 이전 상태와 유령의 가리킴이 연결되지 않음 | 차단 |
| 거울 속 전직 피아니스트 유령 | 5/5 PASS | FAIL/검증 불가 | 눌린 건반이 파손·들림처럼 보임 | 차단 |
| 한국 저승 인도자 지하철-갈대강 | 5/5 PASS | PASS | 별빛으로 변한 발자국이 물 반사와 구분되지 않음 | 차단 |
| 서구 Death 시계 박물관 | 4/5 FAIL | FAIL/검증 불가 | 변해야 할 시계 숫자가 여전히 밝게 켜짐 | 차단 |
| 북극 영안 이송 | 5/5 PASS | PASS | 보조 인물 1명 추가, 들것 발끝 가림 | 차단 |

엄격한 목표 의미 결과는 3/5 arm PASS다. 모든 복합 지시와 참조 외모까지 포함한 완전 결과는 0/5다. 패키지 구현은 완료됐지만 렌더 충실도 결정은 `revise`다. 작은 상태 변화가 복잡한 프레임에서 사라지는 문제와, 넓은 구도에서 참조 얼굴을 검증할 수 없게 되는 문제를 다음 개선 가설로 남긴다.

## 증거 경계

- [루트 교차검수](root_cross_review.json)
- [개선 반복 기록](improvement_iteration.json)
- 각 arm의 `pack`, `composed`, `render_request`, `pixel_review`, `run_manifest`, `image_runs.ndjson`
- `user_judgment.source`는 모두 `not_yet_received`; 기술 검수는 사용자의 선호 판정을 대신하지 않는다.
