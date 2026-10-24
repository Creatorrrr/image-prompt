# 기존 source 읽기 전용 진단

조사 snapshot HEAD: `52128de98276e8987abe28ded90292affaaf7768`. manifest 모듈 105개, 전체 candidate 21,883개, binding 16,698개, catalog slot 149개를 JSON으로 읽었다. 전체 candidate 수에는 문맥/진단 record도 포함한다. corpus native validator, actual retrieval, index closure 검증을 수행한 수치가 아니다.

## 좁힌 어휘 탐색

positive content의 en/ko/phrase_en/phrase_ko와 제한된 realization 하위 필드만 탐색했다. alias·정의·주석·research metadata는 제외했다. 아래 수치는 검색엔진 결과나 의미의 유무를 뜻하지 않는다.

| 패턴 | record 수 |
|---|---:|
| campus | 6 |
| varsity | 2 |
| lecture | 0 |
| critique | 53 |
| laboratory | 19 |
| library | 9 |
| umbrella | 24 |
| garment_transfer | 19 |
| laptop | 6 |
| contact | 85 |
| graduation | 5 |
| dormitory | 0 |
| dark_academia | 7 |
| aftermath | 104 |

`dormitory` 0건이어도 기존 `cand_ff15b8efa40558cc903aaea6d86f0f4c`는 침대와 책상이 한 방에 있는 가시 구조를 이미 가진다. `lecture` 0건도 모든 강의실 관련 의미의 부재가 아니다. `critique` 패턴의 architectural은 비캠퍼스 건축에도 맞고 `aftermath`의 멍은 구멍에도 맞는다. 자동 집계로 의미 적합성이나 신규 필요성을 확정하지 않는다.

## 14개 기존 후보의 원문·조건·effects·모든 binding 대조

아래는 반영 전 제안이다. 원문 전체는 existing-records.json에 보존했으며 기존 provenance/qualification을 이번 조사에서 새로 인증하지 않았다.

- **cand_0956755753b254979d3fb0d24d7ac3fb → reuse** (W01). 배색 소매·골지·스냅의 구조는 재사용 우선. 허리단과 원문 전체 차이는 추가 심사. 과잠의 소속·대여·글자를 자동 부여하지 않는다. 원문 모듈: `photo_candidate_school_appearance_poses_20261023.json`; binding 2개.
- **cand_c253a08a2be6512db4f682e535209347 → refine** (W23). 기존은 열린 가운과 교복. UCSD 작업 홍보촬영용 닫힌 가운·손목 경계의 요구를 충족하지 않는다. 기존 의미는 보존하고 별도 조건/후보를 제안한다. 원문 모듈: `photo_candidate_school_appearance_poses_20261023.json`; binding 2개.
- **cand_ff15b8efa40558cc903aaea6d86f0f4c → refine** (S11). 기존 침대·책상 생활실은 이미 존재한다. 2인실 두 생활구역은 새 개수 계약이므로 기존을 둘로 바꾸지 않는다. 원문 모듈: `photo_candidate_school_life_20261023.json`; binding 2개.
- **cand_4cf75c08dd1a5b0da1a6e4990145df32 → reuse** (A22). 단일 대·천·두 사람의 구조 재사용 검토. 기존 문구의 걷기·젖은 길도 effects/동결 core와 함께 검토한다. 특정 손 주인은 별도 해소한다. 원문 모듈: `photo_candidate_school_life_20261023.json`; binding 3개.
- **cand_ba5f64034a9b5cb1b5dbece356a147d1 → refine** (A13, A14). 기존은 공책·연필·두 학생이다. 공동 노트북이나 건축 도면으로 조용히 치환하지 말고 별도 실현을 작성한다. 원문 모듈: `photo_candidate_school_life_20261023.json`; binding 2개.
- **cand_63f48b07d7825d42a4c2ea7de4a0e463 → reuse** (W27). 긴 가운·정장·후드의 층 재사용 우선. 학사모와 sub fusc는 기존 문구에 없으므로 추가 의무로 취급하지 않는다. 원문 모듈: `photo_candidate_school_appearance_poses_20261023.json`; binding 2개.
- **cand_e88cd98b3bce5a3f938e3043f720708e → reuse** (A25). 교대 손가락·두 엄지·손목의 기존 계약 재사용. 성인·관계·동의를 이 CID가 대신 증명하지 않는다. 원문 모듈: `photo_candidate_harem_20261023.json`; binding 1개.
- **cand_1f4978cf591554b39621a86500cf98b5 → context** (P07). 기존은 SCP 특정 세계/별명·답글 화면과 고유 한글 제약을 포함한다. 일반 대학 커뮤니티로 세계관 없이 재태깅하지 말고 중립 realization 분리를 심사한다. 원문 모듈: `photo_candidate_scp_20261022.json`; binding 2개.
- **cand_e90885a8cc4d5198b145a3f56349ce25 → refine** (C07, W01, W06). 산뜻한 대학생 스타일은 visible components가 부족하다. 실제 옷·핏·소품을 선택적 카드로 보충하고 외형을 대학생 신원으로 승격하지 않는다. 원문 모듈: `photo_candidate_candidates_006.json`; binding 1개.
- **cand_b58a94e7a3295198887306113167e2ae → reuse** (W04, W06, W07, W09). 셔츠·니트 베스트·주름 하의·로퍼의 기존 조합 재사용. 각 부품을 단독 후보로 분해할 때 새로운 native 근거와 effects 심사가 필요하다. 원문 모듈: `photo_candidate_school_appearance_poses_20261023.json`; binding 1개.
- **cand_455838fef14a5caba8aa45911dc42aae → context** (S06, C01). 오크 서가를 선택한 경우만 위치 재사용 검토. 모든 캠퍼스·dark academia를 오크 도서관으로 고정하지 않는다. 원문 모듈: `photo_candidate_candidates_009.json`; binding 1개.
- **cand_19ad7efe62325ab69d71591fc152c76e → refine** (A26). 관자-어깨 접촉과 받치는 사람 손 위치는 재사용 가치가 있다. 기존 classmates 역할을 일반 성인 관계로 자동 변경하지 않는다. 원문 모듈: `photo_candidate_school_appearance_poses_20261023.json`; binding 2개.
- **cand_d7bfcc8602f45d34832f1e3b8642997b → refine** (A03). 원문은 볼이 손바닥에 닿는다. 한국어 턱 괴기라는 표제만 보고 chin 접촉을 충족한다고 판정하지 않는다. 원문 모듈: `photo_candidate_school_appearance_poses_20261023.json`; binding 2개.
- **cand_2685b1123b8c5a47a96da576ec80f7e3 → reuse** (A42). 풀린 실·구멍·온전한 봉제선 경계는 의복 상태로 재사용. 붕대·멍·폭력 원인은 따로 심사한다. 원문 모듈: `photo_candidate_school_appearance_poses_20261023.json`; binding 1개.

기존 native 검증·현행 installed runtime·source와 index 일치는 재검증하지 않았다. 연구 validator가 관찰한 이후 변동은 VALIDATION.json에서 확인한다. 실제 반영 직전 최신 상태로 다시 심사한다.
