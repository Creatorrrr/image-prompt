# 데이터 반영 계획

이 문서는 후속 구현을 위한 실행 설계다. 이번 요청은 리서치와 계획이며 운영 source/index/CURRENT/설치 선택을 바꾸지 않는다. 별도 구현을 시작할 때에는 이 연구의 historical snapshot을 유지하고 구현 당시 기준을 새로 기록한다.

## 1. 우선순위와 완료 산출물

| 단계 | 작업 | 구체 산출물 | 종료 조건 |
|---|---|---|---|
| W0 재기준화 | HEAD·dirty·manifest closure·search·설치 세대 확인 | 구현 단계의 baseline, 선행 변경 포함 목록, 작업 공간 | 동시 작업의 파일과 source 세대를 설명할 수 있음 |
| W1 원문/의미 결정 | 182키워드, 72안, 기존 source 이웃 비교 | 카드별 reuse/refine/new/context/defer ledger | 실제 CID/RID·원문·hash·조건·효과·근거·남은 조사 기록 |
| W2 P0 관계 저술 | 각 군 01/02, 총 24안 우선 검토 | 필요한 신규/정제 source, 정확한 한영 긍정 문장 | 필수 소유·개수·부위·끝점·효과·전제가 직접 근거를 가짐 |
| W3 범위 확장 | 나머지 48안, 16문맥 기록 | P1 차이 근거와 검증 가능한 대안 | 단순 별칭 복제가 없고 기존 기본형과 차이가 있음 |
| W4 별도 index/검색 | staged source에서 필요 벡터만 계산 | 검증된 staging index, 실제 query/rank/receipt | 계약 무결성 및 지정 의미 평가 통과, 일반 요청 오염 없음 |
| W5 실제 이미지 | 우선 12군×3 arm, 필요 시 실패군 재시험 | 동결 입력·exact prompt·원본 이미지·픽셀 판단 | 기술 검사와 모든 필수 관계 PASS, 장면 평가 별도 기록 |
| W6 설치/정리 | 검토한 code/data closure 봉인·설치 검증 | 세대 ID·검증·롤백 경로·마감 상태 | 새 세대 자격 확인 후 별도 활성화, 실패 시 HOLD |

P0는 A01/A02, B01/B02, C01/C02, D01/D02, E01/E02, F01/F02, G01/G02, H01/H02, I01/I02, J01/J02, K01/K02, L01/L02다. 이는 **24개 새 CID를 만들라는 할당량이 아니다**. 기존 완전한 source로 충분하면 재사용한다. W3의 수량 목표보다 실제 관계 다양성과 일반 요청 회귀가 우선한다.

## 2. 코드와 데이터의 반영 위치

예상 경로이며 이번 연구에서는 만들거나 등록하지 않았다.

| 위치 | 역할 |
|---|---|
| `assets/photo_surreal_posthuman_science_fantasy_semantics_20261022.json` | 출처·sense·가시/문맥 경계·채택 결정의 유지보수 registry. native 사실의 두 번째 권위가 아님 |
| `assets/photo_candidate_surreal_posthuman_science_fantasy_20261022.json` | 채택 결정한 신규 V3 후보 소스. 완전한 조건·효과·선택 실현 저술 필요 |
| `assets/photo_candidate_surreal_posthuman_science_fantasy_bindings_20261022.json` | 실제 149 catalog 역할에 적합하다고 검토한 binding만 |
| 기존 CID의 단일 소유 모듈 | refine가 필요한 실제 source만 수정. 임의로 CID 이동/중복 소유 금지 |
| `assets/photo_candidate_corpus_manifest.json` | 검토 완료한 모듈만 명시 등록 |
| `references/surreal-posthuman-science-fantasy-semantics.md` | 조사 범위·혼동·운영 유지보수 주의. 일반 precore의 장면 재료로 노출하지 않음 |
| 영향받은 테스트/평가 fixtures | 소유·락·한영 의미·비가시 승격·일반 요청 회귀 |

`candidate-drafts.json`을 loader에 복사하는 구현은 허용하지 않는다. 현재 초안에는 실제 CID/RID, native facts/proof, intrinsic guards/effects가 없으며 graph와 catalog에서 복사한 descriptor는 연구용이다. 허용되지 않는 새 필드를 loader가 무시할 것이라 가정하지 않는다. 계약 변경이 필요하면 데이터 보강과 별도 문제로 입증하고 범위를 제한한다. 이번 조사 자체로 engine 변경이 필요하다는 증거는 없다.

## 3. W1의 결정 ledger

각 행에 `card_id`, `seed_ids`, 기존 candidate/RID·owner module·전체 원문·hash, intrinsic conditions/effects, 전체 binding/role conditions, 채택 branch, source 열람 범위, 새 장면과의 차이, disposition, 근거, 미해결 사항을 남긴다. 그래프가 같아 보여도 추가 색·재료·인물·행동 의무가 있으면 함께 검토한다.

원전이 부족한 철학·정신분석·종교·금기 개념을 정식 의미 registry에 확정하기 전에는 해당 원전/학술 사전·공식 소개의 실제 범위를 보강한다. 현재 `family_background_only_term_specific_verification_pending` 상태를 `verified`로 일괄 바꾸지 않는다. ‘설정어’는 학술어로 승격하지 않는다. 작품은 공식 시놉시스·개발자 설명·실제 장면 독해를 구분한다.

긍정 가시 문장에는 해당 실현의 물체·재료·관계만 넣는다. 혼동 예·부정적 주장·원전 설명·동의/신성/기억 성공 같은 claim limit는 source 의미를 오염시키는 긍정 embedding text로 합치지 않는다. 문맥 후보를 만들 때에도 실제 요청 문맥의 역할과 조건을 검토하고 강제 가시 효과를 부여하지 않는다. 기존 negative의 소유와 승인 경로는 보존한다.

## 4. 소유자·효과·한영 검토

| 대표안 | native 저술 전에 확정할 사항 |
|---|---|
| A03 물–사슬 | 주전자 소유 주둥이, 액체 시작점, 전이 위치, 고리와 컵의 끝점. 투명 재질·개수·물리적 연속성 구분 |
| B01 기둥–얼굴 | 실제 두 기둥·아치 void와 독해된 얼굴을 구분. 별도 얼굴 생물/인격을 생성하지 않음 |
| B02 손–거울상 | 같은 오른손인지, 실제 손과 상의 자세, 거울 경계. 다른 손·다른 인물로 대체하지 않음 |
| C01/C03 관 | 실제 기존 신체 owner·소켓·착용 의복·구멍·관·기계 단자. 구멍 통과와 피부/옷 부착을 구분 |
| D02 Y 케이블 | 두 실제 단말의 포트와 한 Y자 선의 두 갈래. 정보/의식 공유는 별도 문맥 |
| E02 벽 밸브 | 밸브가 벽 안에 박힌 관계와 벽 주름의 연속성. 실제 살아 있는 조직이라는 사실은 추가하지 않음 |
| F03 도선 문자 | 문자처럼 보이는 무늬·실제 읽을 수 있는 문자·도선 경로를 구분. 문화권이나 주문 효과를 추론하지 않음 |
| H01 모형 | 실제 방/미니어처 방의 owner를 분리. 구성 대응과 무한/층위 침범은 다른 판단 |
| I04 공유 막 | 두 개체 각각의 외피와 막의 양쪽 edge. 가림·단순 겹침은 접합 PASS가 아님 |
| J04 모형 | 실제 인체와 전시 모형의 ontology·재료·매체 구분. 모형을 인체 훼손의 대체 후보로 승인하지 않음 |
| K01/K03/K05 | 두 성인·각자의 손·장갑/원판의 소유. 같은 물체인지와 접점. 성적 의미·합의는 명시 문맥만 보존 |
| L02/L04/L05 | 인공 손과 실제 조직, 접촉과 출입 성공, 기록함과 내용 기억, 전달 자세와 소유권 변화를 구분 |

초안의 복수 owner(`seats`, `hands`, `platforms` 등)는 native 저술 때 실제 cardinality와 각 부품의 pairing을 정한다. 연구 graph의 set-valued endpoint를 곧바로 native each-member selector로 쓰지 않는다. 기존 owner에 영향을 주는 모든 속성과 actual receiver를 검토하고 equal-value mutation도 변경 footprint에서 제외하지 않는다. ‘관계만 바뀜’이라는 설명으로 인물 수·신체·의복·재질·동작의 변경을 빠뜨리지 않는다.

한영 대조에서는 주어·소유·수·같은/다른·안/밖·연속/분리·접촉/가까움·시작/끝을 별도 체크한다. 영어에만 접점이 있고 한국어에는 제목/한계만 있는 source는 검색 레이블 추가로 해결됐다고 하지 않는다. 직접 사실을 뒷받침하는 정확한 긍정 필드의 literal anchor가 있어야 하며 alias와 research graph가 이를 대신하지 않는다.

슬롯은 역할이고 검색 공간 분할이나 의미 승인 수단이 아니다. 예를 들어 body_form이 맞는 후보를 mood·genre·surreal_concept의 direct 효과로 자동 승격하지 않는다. 역할 거부를 unbound proposal로 우회하지 않고 원본 전제와 모든 잠금을 적용한다. `viewer_position`처럼 contextual 역할이 있는 슬롯은 가시 정렬과 관객 위치 설명을 구분한다.

## 5. 인덱스와 검색 검증

구현 단계에서 source manifest·search manifest·recipe·provider/model/차원·설치 세대를 다시 확인한다. 모델 이름을 문서의 과거 관찰에서 고정하지 않는다. 현재 환경의 실행 Python은 `photo_installed_h_f2.py --check-runtime`의 반환값을 사용한다. 이번 검사에서는 recorder 호환성을 확인했고 이미지 호출과 source 쓰기는 0건이었다.

전체 skill의 격리된 staging 복사본에서 빌드한다. 기존 source의 ID·text·recipe·모델 공간·벡터 무결성이 전부 맞는 것만 재사용하고 바뀐 문장은 필요한 만큼만 새로 계산한다. source 변경 중에는 빌드/활성화를 막고, 원격 모델로 임의 우회하지 않는다. `--publish`나 CURRENT 변경은 staging verify와 별도 단계다. 현재 작업 source와 설치된 sealed code/data가 다를 수 있다.

먼저 실제 변경한 source/role/lock 계약의 필수 검증만 실행한다. dictionary 검증, source/native proof 검증, 실제 영향받은 semantic boundary·source context·query·owner resolution 회귀가 대상이다. 통과 후 이유 없이 전체 평가를 반복하지 않는다. 의미 실패는 데이터·번역·질의·기존 corpus 문제를 분리하고, 검색 실패를 장르별 강제 routing으로 덮지 않는다.

`EVALUATION-CASES.tsv`는 카드 저술과 함께 만든 **개발 코호트**다. 72개 긍정, 16개 혼동 경계, 12개 일반, 12개 비가시 사례의 각 한영 질의 224개를 실행한다. 별도의 독립 holdout 최소 24사례를 신규로 작성하고 카드 문장을 그대로 복제하지 않는다. 짧은 키워드, 전체 문장, 순서 변화, 동의어, 키워드가 없는 의미 요청을 섞되 동일 요청 의미를 유지한다.

각 query에는 실제 텍스트·언어·독립 core와 controls hash·각 슬롯 문맥·검색 lane·model/space·top 후보 CID/RID·노출·선택·거절 이유·팩/receipt를 보존한다. target draft ID가 검색된 것처럼 보고하지 않는다. 기존 후보가 더 잘 맞으면 그것을 선택할 수 있다. top-k에 보였다는 사실과 native 채택 자격은 별도다.

종료 기준은 (a) 가시 관계가 필요한 모든 지정 개발 사례에서 적합한 기존/신규 완전 후보를 찾거나 명시적 abstention, (b) 경계/일반/비가시 사례에서 잘못된 의무·성적 의미·폭력·인물·기억/동의/기적 성공의 자동 추가 0건, (c) 한영에서 소유·수·방향 손실 0건, (d) 독립 holdout 결과와 실패 분모 공개다. 긍정 사례에서 abstention은 안전한 거절 기록이지만 coverage 미달로 남으며 ‘보강 완료’의 합격으로 세지 않는다. recall@k·precision@k·nDCG를 쓸 경우 k·관련성 기준·코호트·분모를 사전 고정하며, 수치 하나로 장면 품질을 승인하지 않는다. 실패가 있으면 해당 source/역할은 HOLD 또는 보류한다.

## 6. 픽셀·설치 종료 조건

세부 비교는 `PIXEL-PLAN.md`를 따른다. 원본 이미지의 필수 owner·관계가 전부 보일 때만 기술적 관계 PASS다. 실제 소리·연대·동의·인격·주술 작동은 해당 이미지의 성공 기준에 넣지 않는다. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`를 유지한다.

픽셀 실패와 별개로 전체 장면의 의미·구성·사진 매체·초현실적 긴장을 평가한다. source 도입 arm이 나아졌다는 증거가 없으면 후보 수 증가를 성공으로 보고하지 않는다. 설치는 검토한 파일 allowlist로 봉인한 새 세대에서 검증하고, 원래 CURRENT/설치 세대의 복구 경로를 유지한다. 게시·설치·활성화·사용자 수용·커밋/푸시 상태를 각각 보고한다.
