# 데이터 반영 계획

이 계획은 조사 후의 구현 순서를 정한다. 이번 요청에서는 연구 폴더만 작성했다. 운영 source·manifest·검색 인덱스·설치 포인터·CURRENT를 수정하거나 모델/이미지를 호출하지 않았다. 아래 명령과 수치는 후속 작업의 계획이며 실행 결과가 아니다.

## 1. 결과와 반영 단위

목표는 장르를 입력하면 수십 가지 장식이 자동으로 붙는 프로파일이 아니라, **이미 결정된 요청의 의미와 장면을 더 정확하게 표현할 수 있는 선택적 후보**다. 한 후보는 실제로 함께 성립해야 하는 소유자·관계·상태를 온전하게 가진다. 서로 배타적인 분리/연결·모형/신체·음식/인체를 한 거대 후보에 합치지 않는다.

|단계|구체적 작업|완료 산출물|중단/보류 조건|
|---|---|---|---|
|P0 재기준화|현재 HEAD·dirty·source/index/installed 세대를 새로 고정|별도 integration-evidence의 baseline·hash·환경|동시 수정/누락 모델/소스 drift가 설명되지 않음|
|P1 원문 심사|86개 초안과 관련 기존 CID를 전체 조건·효과·역할로 대조|초안별 reuse/refine/new/context/defer ledger|이름·출처 링크·태그만으로 지원을 주장|
|P2 1차 관계 저술|우선 24개 카드의 필요한 원자 의미를 보강|한영 원문·owner/guard/effect·role·출처 한계|역할/소유자/진단·동의 경계가 미확정|
|P3 나머지·문맥|나머지 가시 62개와 문맥 22개 검토|중복 없는 선택안, 의미를 보존한 context 경로|미확인 용어를 정본으로 승격해야만 성립|
|P4 격리 검증|별도 source 전체와 인덱스 작성·계약 검사|source/index/code closure와 검증 로그|기존 frozen lock·조건 우회, 모델 공간 불일치|
|P5 검색 실험|80개 한영 사례와 새 독립 holdout으로 A/B 실행|질의·실제 CID/RID·순위·노출·채택·receipt|관계군 누락·오탐 채택·일반 대조 회귀|
|P6 이미지 비교|12개 장면군×3 arm 비교|저장 픽셀·gate·장면 이해·미감 평가|비가시/부분을 통과 처리, 의미 대체|
|P7 선택적 채택|필요 기준을 통과한 exact closure만 봉인·설치|설치 세대·새 run·복구 경로|검색/픽셀 실패군은 HOLD 유지|

P2의 우선 24개는 `A01 A02 B01 B02 B03 B04 C01 C02 C03 C04 D01 D02 D06 F01 F03 F08 G01 G02 G04 G06 G07 G08 G09 G10`이다. 이 숫자는 신규 후보 수량 목표가 아니다. 기존 데이터가 완전히 지원하면 새 CID를 만들지 않는다. G08/H17은 인피라는 재료의 시각 인증이 불가능하다는 문맥 경계를 1차부터 보존하기 위해 포함했다.

## 2. 구현 전에 확인할 현재 상태

[BASELINE](BASELINE.json)은 시작 HEAD와 6,139개 추적 파일 hash·기존 dirty 상태를 보존한다. [corpus 관찰](CORPUS-LEXICAL-AUDIT.json)은 조사 당시 55개 모듈과 manifest hash를 기록한다. [installed 관찰](RUNTIME-OBSERVATION.json)은 기존 설치 세대의 의존성과 recorder를 읽기 전용으로 확인한 결과다. 셋의 캡처 시각과 의미가 다르므로 하나의 설치 완료 증거로 합치지 않는다.

실제 반영 때 현재 HEAD·기존 dirty 목록·manifest가 선언한 **전체** 모듈·slot catalog·`photo_candidate_search.json`·`retrieval-runtime.json`·installed closure를 다시 고정한다. 옛 연구 스냅샷을 새 결과로 덮어쓰지 않는다. 다른 작업의 변경은 reset/stash/revert로 치우지 않는다. 격리 작업 소스에 필요한 선행 변경만 명시해 포함한다.

현재 원본은 `skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json`, 검색은 `photo_candidate_search.json`이 선언한다. 149개 슬롯은 역할 vocabulary이며 검색 공간을 149개로 쪼개는 단위가 아니다. source 게시·native CURRENT·installed generation 선택은 다른 상태다.

## 3. 초안별 채택 ledger와 중복 방지

각 행에 `research_card_id`, 관련 기존 CID/RID·정확한 source hash, 긍정 원문 전체, intrinsic 조건/효과, binding 조건, 선택 branch, 소유자 대응, disposition, 이유, 남은 검증을 둔다. 28개 기존 스냅샷의 현재 조사 판단은 reuse 8·refine 17·context 1·부적합 이웃 2다. **현재 태그나 native 자격을 승인한 수치가 아니다.**

다음 순서로 판단한다.

1. 기존 원문의 **같은 원자 의미**가 충분한지 먼저 본다. 벨벳 파일의 반응은 재사용할 수 있어도 human/garment 조건을 가진 후보를 의자 팔걸이에 그대로 적용할 수는 없다.
2. 이름이 맞아도 원문이 관계를 지원하는지 본다. `Evisceration` 명칭이 분리된 신체 부분과 간격만 설명하면 내부 구조·공동·연결 상태까지 지원한 것이 아니다.
3. 본문이 맞아도 intrinsic guard·모든 effect·owner/property lock·role 조건을 평가한다. 범죄 태그를 요구하는 출입 후보를 일상 가정에 쓰려고 guard를 제거하지 않는다.
4. 별도 맥락인 합의·의도·혈연·생사·재료 검사·시간을 긍정 시각 사실에서 분리한다. 이를 삭제하거나 일반 소품이 충족한 것처럼 꾸미지 않는다.
5. source가 부족한 경우에만 신규를 작성한다. 모든 초안이 무조건 새 후보가 되지는 않는다.

실제 데이터 파일명 제안은 `photo_candidate_decadent_domestic_splatter_20261022.json`, `photo_candidate_decadent_domestic_splatter_bindings_20261022.json`, `photo_decadent_domestic_splatter_semantics_20261022.json`, 관련 reference 문서다. 날짜·namespace는 실제 구현 시 확정한다. 기존 대형 shard를 광범위하게 편집하기보다 작은 명시적 모듈을 우선한다.

## 4. source·binding·context 저술 계약

현행 `photo-candidate-module/v3`에서는 후보가 intrinsic 조건과 effect를 한 번 소유하고, `photo-candidate-slot-bindings/v3`는 역할 적용을 소유한다. 연구 JSON을 운영 loader 입력으로 바로 넣거나 연구 graph에서 executable effect/guard를 자동 생성하지 않는다.

|관계 유형|원문에 필요한 사실|영향·권한 검토|
|---|---|---|
|B01/B04 열쇠·돈|서로 다른 손·동일 물건·접촉/거리·구체적 장치|인물 수·손 소유자·action/contact·prop·접근 관계 전체|
|C01/C03 반사·화면|실물·표시 경계·대응 표식·시선|새 인물 복제·camera/composition·반사/장치 시점·가림|
|A01/D01/D02 재질|같은 물건·층/무늬·빛의 반응·연속 경계|의복/가구 조건·material/garment 상태·성분 과잉 주장|
|D06/F02 천·피부|찢긴 소유자·경계·드러난 면의 실제 종류|body/garment 분리·몸의 온전함·기존 anatomy 보존|
|F01/F03/F04 신체|양 끝점·기관/공동·분리/연결·선언된 매체|body geometry·count·소유자·현재 단계·숨은 부분|
|F08 융합|두 구별되는 몸·공통 조직·사지 소유|subject_count/species/anatomy·독립 limb·접합 연속성|
|G01/G06/G07 수집|유리 아래 모발·모형 패널·조각 받침 등|object/skin 매체 혼합·판독 가능한 표기·성적/죽음 추론|
|H 문맥|원 요청의 정확한 관계·동의·생사·검사·시퀀스|문맥 의미 보존·positive visual obligation 자동 추가 금지|

표의 영향 차원은 검토 범위다. 실제 canonical effect는 각 원문과 선택 branch를 기준으로 현행 스키마에 저술한다. 같은 값의 effect도 mutation이며 requester lock을 우회할 수 없다. 역할 direct/contextual, 조건 실패, 선택한 RID의 whole-source closure를 별도로 검토한다. 같은 역할의 실패를 unbound request-local proposal로 우회하지 않는다.

문맥 경로를 보강하려면 현재 전용 context 레코드 방식을 먼저 검토한다. diagnostic을 긍정 pool에 넣거나 `No still-image recipe`라는 문자열만으로 의미 검토를 대체하지 않는다. 요청에서 명시된 사건을 소품·일상·분장으로 바꾸는 것은 context 보존이 아니다.

한영 대조는 소유자·수량·재료와 직조·매체·끝점·연결·현재 단계·부정 범위를 항목별로 확인한다. 특히 `red liquid/blood`, `hair locket/mourning jewellery`, `silk/satin`, `flayed figure/ecorche sculpture`, `externalized/removed`, `coercion/consensual exchange`를 대조한다. 현 초안은 독립 번역 검토 전이다.

## 5. source 자격과 구조 검사

native source qualification은 exact CID/RID의 긍정 필드에서 실제 인용 구간·fact·owner·role witness를 직접 심사한다. 참고문헌 URL·연구 카드·gate·태그가 source의 빠진 사실을 메울 수 없다. source/version/recipe가 바뀌면 과거 proof의 재사용 가능성을 다시 검토한다.

격리된 전체 skill 복사본에서 현행 dictionary validator를 실행하고 변경한 invariants와 관련된 테스트만 고른다. 시작 후보는 `test_h_f2_semantic_boundaries.py`, `test_h_f2_source_context.py`, `test_h_f2_primary_proof_boundaries.py`, `test_h_f2_literal_text.py`, `test_h_f2_whole_scene.py`, `test_h_f2_sampling.py`다. 구현 시 파일 존재와 관련 사례를 다시 확인한다.

```sh
"$RUNTIME_PYTHON" "$STAGED_SKILL/scripts/validate_photo_prompt_dictionary.py"
```

위 변수는 후속 작업의 실제 경로를 뜻한다. 이 연구에서 dictionary validator나 repository 테스트를 실행한 기록은 아니다. 지금 실행한 연구 validator는 자체 JSON·graph·참조·표·hash 검사만 한다.

## 6. 격리 인덱스와 세대 생성

현행 `photo_candidate_search.json`의 provider/model/dimensions/recipe와 pinned local model 파일을 재확인한다. 현재 로컬 EmbeddingGemma 계열 공간을 임의의 원격 Gemini/OpenAI 임베딩으로 바꾸지 않는다. 모델/API 호출은 이번 연구에서 0회다.

정확한 CID·텍스트 hash·recipe·모델 공간·vector integrity가 맞는 벡터만 재사용한다. 후보 본문/의미 텍스트를 바꾸면 새 문서 임베딩이 필요할 수 있다. source metadata만 바꿨다고 추론 0회라고 단정하지 않는다. build 명령의 기본 출력 경로·publish/activation 부작용을 먼저 확인한 후 **격리된 전체 corpus**를 대상으로 생성한다.

완료 기준은 전체 긍정 레코드의 coverage, global BM25F 통계, payload/posting/vector extent와 routing bound의 closure, source/index identity, 실제 재사용/추론 수량 기록이다. 일부 신규 후보만으로 corpus를 대체하거나 현재 운영 포인터를 빌드 중간에 움직이지 않는다. 소스가 바뀌면 새 baseline으로 다시 고정한다.

## 7. 검색 비교와 종료 기준

현재 평가 파일은 개발 36·경계 26·일반 12·비가시 14, 총 88사례/한영 176질의이며 모두 `NOT_RUN`이다. 같은 연구자가 저술한 개발 코호트이므로 독립 holdout이라고 부르지 않는다. 후보 튜닝 전에 사용자 또는 별도 독립 작성자가 실제 자연어 holdout 24개 이상을 작성·고정하고 정답은 실제 CID/RID로 심사한다.

동일한 candidate-free request/core·creative controls·slot plan에서 기존 세대 A와 데이터만 반영한 staged 세대 B를 비교한다. 이미지의 독립 baseline도 검색 전에 작성한다. 연구 문장을 그대로 옮겨 독립 baseline이라고 주장하지 않는다.

현행 managed 흐름에서 슬롯마다 질의를 독립 작성·봉인하고 검색한다. `__request_topic__`와 `__baseline_prompt__`의 두 whole-scene 검색도 각각 남긴다. 세 결과를 하나로 합쳐 슬롯 검색을 대체하거나 중복 ranking vote를 만들지 않는다. 실제 BM25F·cosine·RRF 순위, CID 중복 제거 창, 노출 표본, 의미 적합성, 조건상 eligible/adoptable, 최종 채택, 거절 이유, receipt를 구분한다.

현재 코드에서 확인한 창/표본 상한은 creativity 0=`8/4`, 1=`32/8`, 2=`96/12`, 3=`256/16`이다. 기본 비교는 creativity1에서 고정 평가 seed 네 개로 A/B를 짝짓고 0/2/3은 경계 subset으로 검사한다. 새 사용자 run의 fresh 128-bit seed 정책은 유지한다. resume/view는 발행된 receipt를 재사용하고 순위를 재현하려고 질의를 재임베딩하지 않는다.

제안 종료 기준은 다음과 같다. **측정 전 기준이며 달성치가 아니다.**

- 양 언어·각 관계군의 적합 목표 후보 `Recall@32 ≥ 90%`. 정답 전체 inventory가 없으면 Recall 대신 **심사한 목표 후보의 창 진입률**이라고 쓴다.
- owner·guard·effect lock 위반 채택 0건. 문맥/진단/성적 의미의 무근거 자동 추가 0건. 검색 노출 자체는 오류가 아니고 부적합 후보를 거절할 수 있어야 한다.
- 일반 대조의 심사된 채택 precision 악화가 2%p 이내. 12개 일반 사례만으로 2%p 차이를 신뢰성 있게 추정할 수 없으므로 실제 정밀 비교에는 표본을 늘리고 건수·구간을 함께 보고한다. 12개에서는 구체적인 오탐 발생 여부를 우선 확인한다.
- 평균뿐 아니라 언어별·개념군별·seed별 창 진입·표본 노출·채택을 제시한다. 특정 군이 모두 실패하면 그 군은 HOLD다.

실패를 후보 수 부족으로 곧바로 해석하지 않는다. 원문 부재, 질의의 의미 노출 부족, vector/BM25F 랭크, 표본 노출, 역할 조건, 최종 저술 중 어디에서 끊겼는지 분리한다. 길어진 프롬프트 자체도 개선의 증거가 아니다.

## 8. 픽셀 비교·설치·복구

[PIXEL-PLAN.md](PIXEL-PLAN.md)의 12장면군×3 arm, 총 36장 제안부터 평가한다. 비용은 도구/해상도·실행 조건이 정해지지 않아 견적을 발명하지 않는다. 생성 호출은 이번 연구에 포함되지 않았다.

gate별 fidelity·화면만으로 읽히는 상황·전체 미감/장르 균형·사용자 선호를 별개로 평가한다. 소품을 보고 장기 학대·동의·식인·진단을 이해했다고 채점하지 않는다. 반대로 실제 신체 결과를 요청한 arm을 단순 붉은 얼룩·무대 분장으로 바꿔 통과시키지 않는다. 정책 차단은 `BLOCKED_UNSCORED`, 미반환 픽셀은 `NOT_OBSERVED`다.

필요한 source 자격·검색·픽셀 기준을 통과한 exact code/source/index closure만 봉인·설치한다. 이전 installed config·native CURRENT·복구 가능한 세대를 보존한다. 활성화 후 새 요청에서 세대·receipt·저장 결과를 확인하고, 실패군은 HOLD로 분리한다. runtime 선택 변경과 source commit을 같은 것으로 보고하지 않는다.

커밋/푸시가 후속 범위에 포함되면 검토한 경로 allowlist만 stage하고 cached diff·제외 dirty hash·local/tracking/remote SHA를 확인한다. 이번 연구에서는 commit/push를 수행하지 않았다.

## 9. 추가 조사 우선순위

1. 브라우저로 복원한 40개 추가 행과 보완한 149번을 포함한 189행의 독립 의미 대조를 진행한다. 기존 bounded snapshot과 보완 provenance는 보존한다.
2. Williams 본문, 스플래터펑크·그랑담 기뇰의 제안자/핵심 연구, 개별 건축 용어를 원전으로 대조한다. 현재 확인한 publisher/abstract 범위를 확대한다.
3. 86개 한영 초안의 독립 의미 대조를 시행한다. 특히 매체·생사·원인·동의의 번역 차이를 점검한다.
4. 우선 24개에서 reuse/refine/new/context/defer를 확정한 뒤 P2 데이터 저술을 시작한다. 검증되지 않은 문헌 사실은 필요한 부분만 defer하고 관계 연구 전체를 폐기하지 않는다.
