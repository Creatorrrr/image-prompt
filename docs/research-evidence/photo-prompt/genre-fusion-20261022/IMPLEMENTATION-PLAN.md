# 데이터 반영 계획

이 문서는 후속 구현을 위한 계획이다. 2026-10-22의 연구가 운영 채택을 의미하지 않는다. 현재 작업 트리의 다른 변경을 보존하고 연구 폴더 이외의 source/index/pointer는 이번 작업에서 수정하지 않았다.

## 1. 반영 단위와 우선순위

새 genre 이름 네 개를 조합한 대형 프로파일을 만드는 대신, **완전한 관계를 가진 선택적 실현안**을 기존 shared candidate pool에 보강한다. 장르·비평·시간·권리·동의 설명은 검색 의미와 문맥 구분에 보존한다. 넓은 용어가 모든 카드의 시각 의무를 활성화하지 않게 한다. 각 source의 내용·조건·effect가 권위이며 연구 보고서·tag·출처 링크·카드 ID는 자격 증거가 아니다.

|작업 묶음|검토 대상|목적|종료 조건|
|---|---|---|---|
|W0 재기준화|현재 HEAD·dirty·53개 원본 모듈·catalog·search·installed config|동시 작업과 세대 변경 확인|시작/끝 해시와 실행 환경을 별도 evidence에 보존|
|W1 원문 대조|24개 기존 CID와 84개 초안|완전 재사용/정제/신규/문맥/보류 결정|각 초안에 결정·근거·실제 CID/RID 또는 신규 필요·미확인 사항 기록|
|W2 생활 관계 1차|아래 24개 카드|새 연구의 가장 큰 차별점인 접촉·수선·환대 보강|각 선택 source의 owner/property/guard/효과·한영 의미 검토 완료|
|W3 공간·제도·단서|나머지 60개 긍정 초안 중 W1에서 필요한 항목|특수 몸·시설·기록·정물·공존 확장|겹치는 소스와 차이를 설명한 항목만 추가|
|W4 문맥 경로|150개 seed와 문맥 전용 12개 카드|용어 누락 없이 가시성 한계 보존|긍정 이미지 의무·성적/폭력적 의미의 자동 생성 0건|
|W5 검색·픽셀·설치|자격 확인된 source/index/code closure|의미 회귀와 실제 효과를 검증한 뒤 활성화|독립 증거가 통과한 세대만 설치, 실패 시 HOLD|

W2의 24개는 A02/A03/A04/A08, B01/B02/B03/B05/B12, C01/C02/C03/C04/C05/C06, D01/D02/D03/D05/D06/D12, E01/E03, F02다. 이는 후보 수량 목표가 아니라 우선 의미 검토 범위다. 완전 재사용으로 충족되면 신규 레코드를 만들지 않는다. 84개 초안을 84개 새 CID로 확정하지 않는다.

W3은 일반 음식/수선에서의 회귀가 없고 W2 관계 검색에 실제 효용이 확인된 뒤 진행한다. 해석·권리·동의·시간의 문맥 기록은 W2와 함께 검토하되, 가시성 자격과 분리한다. 논쟁적인 단어를 지우는 대신 무슨 근거가 있어야 그 의미를 채택할 수 있는지 기록한다.

## 2. 구현 전 재기준화

`BASELINE.json`의 당시 HEAD·기존 dirty 경로·추적 파일 해시, `CORPUS-LEXICAL-AUDIT.json`의 manifest와 각 source 모듈 해시, `RUNTIME-OBSERVATION.json`의 installed 세대를 새 스냅샷과 비교한다. 이 증거 파일들을 새 결과로 덮어쓰지 말고 구현 단계의 별도 하위 디렉터리에 보존한다. 연구 도중 바뀐 원본은 타 작업으로 분리해 확인하며 복원·stash·reset으로 없애지 않는다.

현재 source는 `assets/photo_candidate_corpus_manifest.json`, 검색 manifest는 `assets/photo_candidate_search.json`이다. catalog 149개 슬롯은 역할 vocabulary이며 검색 공간을 슬롯별로 분할하지 않는다. `retrieval-runtime.json`이 installed H-F2 세대를 지정한다. 작업 소스 게시, native CURRENT, installed 세대 선택은 서로 다른 상태다. `references/installed-h-f2.md`에 적힌 후보 숫자를 현재 데이터 수로 재사용하지 않는다.

실제 구현에는 별도 작업 소스 또는 격리된 전체 skill 복사본을 사용한다. 현재 checkout에 다른 수정이 많으므로 W0에서 선행 변경의 포함 범위를 명시한다. 새로운 코드·데이터를 원래 작업의 산출물인 것처럼 포함하지 않는다.

## 3. 원문 대조와 데이터 저술

W1 ledger의 각 행에는 `card_id`, 기존 후보의 전체 CID/RID·hash, 전체 원문, intrinsic conditions/effects, role bindings/conditions, 선택한 branch, 판단 근거, 최종 disposition을 둔다. `existing-source-mapping.json`의 24행은 원문 이웃 스냅샷이지 역할 승인이다. 원문을 생략한 레이블 대조로 reuse를 확정하지 않는다.

|결정|적용 조건|예|
|---|---|---|
|reuse|모든 소유자·부분·재료·관계·조건·효과가 정확히 맞음|기존 티포트 자체의 부품 관계만 필요할 때|
|refine|더 구체적인 관계가 필요하며 기존 의미를 보존할 수 있음|일반 생활품 수선에서 소매·패치·접점을 분리|
|new|기존 후보로 완전한 관계가 성립하지 않음|주인–동일 그릇–손님의 전달, 화덕에 박힌 재사용 부재|
|context|서사·비평·시간·정치·동의의 의미이며 이미지에서 확정 불가|열적 죽음·시민권·혈통·원리적 불가지|
|defer|판본·한영 의미·관계·효과가 아직 불확정|밴스식 마법의 판본별 준비·망각 규칙|

신규가 필요하면 날짜가 붙은 별도 module·binding·semantic reference를 저술하고 기존 거대 shard를 무작정 편집하지 않는다. 파일명 예시는 `photo_candidate_genre_fusion_20261022.json`, `photo_candidate_genre_fusion_bindings_20261022.json`, `photo_genre_fusion_semantics_20261022.json`이다. 실제 namespace와 날짜는 구현 시점에 결정한다. manifest 등록은 검토한 source 범위만 포함한다.

`photo-candidate-module/v3`의 후보가 intrinsic 조건·효과를 한 번만 소유하고 `photo-candidate-slot-bindings/v3`는 역할 적용만 소유하도록 한다. 연구 graph를 effect schema로 자동 변환하지 않는다. direct/contextual은 해당 역할별로 검토한다. 같은 CID의 다른 역할이나 request-local proposal로 원래 조건 실패를 우회하지 않는다. diagnostic을 긍정 pool로 넣지 않는다.

한영 원문은 같은 소유자·수량·재료·도구·접점·현재 단계를 보존해야 한다. 현재 초안은 저술자의 한영 초안이며 독립 번역 검토가 남아 있다. “그릇을 내민다”를 “돌봄으로 안심시킨다”로, “붉은 원반”을 “늙은 태양”으로 번역하면 주장 범위가 바뀐다. 문맥·출처·오탐 경계가 positive text의 사실 근거를 대신하지 않도록 한다.

## 4. 관계·소유자·효과·자격

|실현 유형|명시할 소유자/영향|검토할 경계|
|---|---|---|
|D01/D03 전달|제공자 손·수신자 손/부속지·동일 그릇·지지 면, relational action/contact/gaze 등 실제 변동 전체|손이 각기 다른 컵을 잡음, 도구·그릇·신체 융합, 동의/연애 추론|
|D06 수선|착용자·소매·찢어진 부분·패치·돕는 손, garment state/detail/contact|인체 상처로 바뀜, 다른 사람 소매를 수선, 천 대신 피부에 접촉|
|E01 보수|동일 관·틈·클램프 양 접점·작업 손, object structure/contact/environment|다른 관을 수리, 가린 접점을 존재한다고 판정, 성공 효능 추가|
|B01/B02 재사용|옛 부재·새 구조·고정 부품/모르타르·새 용도|인접 배치만으로 재사용 확정, 원재료를 새 사물의 소유자로 혼합|
|C03/C04/C05 몸 돌봄|주민 몸·분리된 외피·천/쟁반·돌봄 손·기존 해부 구조|빈 외피/옷/시신, 부속지 수, 피부 당김, 의도치 않은 성적/상해 의미|
|C01/C02 생태/빛|기질·균사·별도 호스·용기·발광처럼 보이는 면·수광면|기억·지능·상리·생물발광 원인·효능을 외형으로 확정|
|E04/E06 제도|창구·문서·민원인·담당자·구획·빛의 소유자|시민권·강제·계급을 외모·조도·물건 하나로 판정|
|G03/G04/G07 불일치|실물·반사/기록·각 경계·비교 부분·전체 연결|가림을 부재로 처리, 다른 대상 비교, 프레임 밖 연결을 발명|

이 표는 검토 범위이며 실제 effect/guard 계약은 현행 스키마로 개별 저술한다. 독립 동작·소유자를 새로 도입하는 후보는 count·subject·species·anatomy·action·contact 등 모든 영향을 평가한다. frozen core가 허용하지 않은 인물·사지·관계·공간·사물을 추가하지 않는다. 요청이 이미 고정한 것과 같은 값의 effect도 mutation이다.

native qualification을 후속 범위에 포함할 때는 exact CID/RID/source closure에 대해 positive field의 실제 인용 구간과 fact·owner·role witness를 직접 검토한다. 출처 페이지·메타데이터·연구 gate가 빠진 source fact를 대신 지원할 수 없다. source/version/recipe가 바뀐 과거 proof는 재사용 가능성을 다시 검증한다. 단순 JSON 구조 PASS·태그 등록·검색 노출을 native 승인이라고 보고하지 않는다.

## 5. 구조 검사와 필요한 회귀

먼저 별도 staged skill에서 현행 dictionary validator를 실행한다. 실제 손댄 invariants에 맞춰 존재하는 아래 파일의 관련 사례를 선택하고, 데이터로 해결 가능한 문제 때문에 engine을 확장하지 않는다.

```sh
"$RUNTIME_PYTHON" "$STAGED_SKILL/scripts/validate_photo_prompt_dictionary.py"
```

관련 테스트: `test_h_f2_semantic_boundaries.py`, `test_h_f2_source_context.py`, `test_h_f2_primary_proof_boundaries.py`, `test_h_f2_literal_text.py`, `test_h_f2_whole_scene.py`, `test_h_f2_sampling.py`. 변수는 후속 구현의 실제 전체 skill·bound Python 경로로 확정한다. 여기서 이 명령이나 repository 테스트를 실행했다는 뜻이 아니다.

새 의미 회귀는 연구 평가 TSV의 16개 경계 사례를 중심으로 작성한다. 특히 molten/molting, calibration/ration, 조석 수선/의복 수선, 다른 그릇·다른 관·다른 신체의 접촉, 장식과 재사용, 반사에서 가려진 손, 판독 불가 계약 문서, 붉은 수프의 식인 오인, 일반 카페에 비인간을 강제하는 실패를 구별한다. 행동·접점이 명시되지 않은 광범위 라벨은 보완 후보일 수 있으나 완전 충족으로 채점하지 않는다.

## 6. 인덱스와 isolated generation

실행 시점의 `photo_candidate_search.json`이 선언하는 provider/model/dimensions/recipe를 재확인한다. 현재 프로젝트의 local EmbeddingGemma 계열 운용을 임의의 Gemini/원격 provider로 우회하지 않는다. 정확한 ID·텍스트 hash·recipe·모델 공간·vector integrity가 일치하는 벡터만 재사용한다. 의미 텍스트가 바뀌면 새 로컬 문서 임베딩이 필요할 수 있다. 태그만 고쳤으니 추론 0회라고 단정하지 않는다.

staging에서 전체 source snapshot을 사용해 인덱스를 만든다. 일부 새 후보만으로 corpus를 대체하면 안 된다. 후속 구현에서 현행 `build_shared_candidate_index.py --help`와 local-embeddings 지침을 다시 확인한 후 실제 경로로 실행한다. 기본 출력이 활성 assets를 움직이는지 먼저 확인하며 현재 checkout의 manifest·CURRENT·installed config를 직접 갱신하는 빌드 명령을 연구 검증으로 실행하지 않는다.

완료 조건은 source identity, global BM25F 통계, payload/posting/vector extent, 모델 공간, routing bounds, 전체 closure 검증과 사용/재사용/추론 수량의 기록이다. code/source drift가 나면 새 세대로 재기준화한다. stale source의 proof·receipt·벡터를 묵시적으로 재사용하지 않는다. 이 단계 통과도 검색 의미 품질이나 이미지 품질의 증거는 아니다.

## 7. 실제 검색 비교

개발 32·경계 16·일반 12·비가시 8의 68개 한영 사례를 제공했다. 모두 연구를 보며 만든 **개발 코호트**다. 사용자 또는 독립 작성자가 새로 쓴 자연어 holdout을 후보 저술·질의 튜닝 전에 고정한다. 카드 ID를 gold CID로 세지 말고 구현된 실제 CID/RID와 적합 branch의 수동 정답 집합을 확정한다.

1. 기존 세대 A, 데이터만 바꾼 staged 세대 B를 같은 candidate-free core·controls·slot plan에서 비교한다. 연구 문장을 독립 baseline으로 재포장하지 않는다.
2. 현행 managed `prepare-slot-intents → seal-slot-intents → retrieve → view` 흐름으로 관련 슬롯을 저술한다. requester lock과 owner/property 권한은 고정한다.
3. 한국어·영어를 각각 실행한다. 각 slot query, `__request_topic__`, `__baseline_prompt__`의 두 독립 whole-scene query를 보존한다. 결과를 합쳐 슬롯별 검색을 대체하거나 중복 vote를 만들지 않는다.
4. BM25F·cosine·RRF의 실제 순위, CID 중복 제거 창, 노출 표본, eligible/adoptable 판단, 최종 채택을 따로 기록한다. discovery는 승인이 아니다.
5. creativity 1에서 paired evaluation seed 네 개를 고정해 세대 간 창·표본 노출을 비교한다. 실제 사용자 새 run은 현행 fresh 128-bit seed 정책을 따른다. 0/2/3은 필수 경계 subset에서 별도 회귀 검사한다. resume/view는 재검색·재표본·임의 재임베딩 없이 issued receipt를 사용한다.

|creativity|쿼리별 CID 중복 제거 창|표본 상한|
|---:|---:|---:|
|0|8|4|
|1|32|8|
|2|96|12|
|3|256|16|

첫 통과 목표 제안: 관계 질의의 양 언어 완전 적합 CID/RID `Recall@32 ≥ 90%`, owner·필수 조건·requester lock 위반 채택 0건, 일반 대조군의 리뷰 precision 악화가 2%p 이내. 이는 측정 전 제안 기준이며 달성치가 아니다. 정답 inventory가 불완전하면 Recall 대신 **목표 후보 창 진입률**로 부른다. seed별 실제 표본 노출률·최악 사례·개념군별 결과를 함께 보고한다. 평균이 높아도 탈피/환대처럼 한 군이 전부 실패하면 그 군은 HOLD다.

일반 대조에서 관련 후보가 노출된 것 자체는 오류가 아니다. 부적합 후보를 거절하는 것은 정상이다. 넓은 장르 의미를 강제하거나 source 조건을 어겨 채택한 경우에 실패로 기록한다. 후보를 전부 거절할 수 있어야 한다. 검색 개선 때문에 프롬프트 길이·정보량만 증가한 경우도 별도 관찰한다.

## 8. 이미지 평가와 전환

[PIXEL-PLAN.md](PIXEL-PLAN.md)의 첫 12군×3 arm, 총 36장 제안부터 비교한다. 생성 도구·비용·실험 범위가 정해진 후의 작업이며 이번 연구에서는 생성 호출 0회다. 장면별 gate·서사 이해·화면 완성도·장르 균형·사용자 선호를 분리한다. unobservable/partial은 완전 gate 통과가 아니고 정책 차단은 `BLOCKED_UNSCORED`다.

검색·데이터·픽셀·출처 자격에서 필요한 기준이 통과한 exact source/index/code closure만 봉인한다. 이전 installed config·CURRENT와 복구 가능한 세대를 보존한 뒤 선택된 설치 포인터를 바꾼다. 실제 새 요청의 generation·receipt·저장 이미지를 확인하고, 실패한 군은 HOLD로 남긴다. 연구 폴더의 존재·구조 PASS·published source commit으로 운영 활성화를 추정하지 않는다.

커밋/푸시가 후속 요청에 포함되면 검토한 경로 allowlist만 stage하고 staged diff·제외한 dirty 파일 hash·local/tracking/remote SHA를 대조한다. 조사, 데이터 반영, 인덱스, installed 채택, source qualification, 검색, 픽셀, 사용자 수용, commit/push를 별도 상태로 보고한다.

## 남은 원전·독립 검토

Polder·Thinning의 직접 원전, Fisher의 상세 존재/부재 논증, 밴스식 마법의 판본별 규칙, 150개 개별 정의의 독립 사전 대조, 한영 번역의 독립 검토가 남아 있다. 현재 자료의 접근 실패·개요/요약만 읽은 범위는 `sources.json`에서 보존한다. 이 미완료를 이유로 이미 확인한 관계 초안을 버리지 않되, 정본 정의·승인된 source로 승격하지 않는다.
