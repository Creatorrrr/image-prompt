# 수사물 데이터 반영 계획

2026-10-25 KST. 목표는 **요청한 조사 행위와 단서를 올바른 소유자·매체·현재 상태로 검색하고 표현하는 것**이다. 연구의 76개 대안을 모두 신규 CID로 등록하는 계획이 아니다. 중복·근거·원뜻·실제 허용 효과를 검토해 재사용, 좁은 수정, 독립 신규, 문맥, 보류로 결정한다.

이번 요청에서 실행한 범위는 조사·초안·계획·연구 자료 검증이다. 아래 운영 변경, 검색 비교, native qualification, 실제 생성, 설치 선택 전환은 미실행이다.

## 1. 구현 순서와 완료 조건

|단계|구체 작업|완료 조건|
|---|---|---|
|0. 기준 확보|현재 HEAD·dirty 상태·manifest closure·설치 선택과 실제 설치본을 재확인. 적합 checkout/worktree에서 정확한 변경 allowlist와 해시를 동결|관련 없는 수정·삭제를 포함하지 않고 baseline/stage의 source·코드·모델 공간을 설명할 수 있음|
|1. 의미 판정|321개 용어와 40개 context 경계에서 구현할 의미를 확정. 사진/서사 proxy/다이어그램/보류를 유지|동의·권한·시간·사후성·재질·분석 결과를 외형으로 승격하지 않음. 원 요청의 의미를 약화시키지 않음|
|2. 기존 source 재사용|28개 비교부터 시작해 전체 corpus의 다른 실현·한영·조건·효과·선택 branch를 확인|CID 복제 없이 reuse/refine/separate/context/defer 결정과 실제 바뀔 원문·효과·조건이 확정됨|
|3. 완결 시각 대안 작성|A/F/D/I 우선. 각 후보의 owner·도구·접점·기록·매체 경계와 actual effects를 분리|한영 전체 뜻이 같고 단일 실현에 필요한 끝점이 함께 관찰 가능. 후보별 실제 조건과 모든 영향이 설명됨|
|4. 원천 및 native 심사|현행 V3 source/binding 규약과 field-local positive anchors로 실제 CID/RID를 심사|연구 graph·gate·출처를 typed native fact나 허가로 재사용하지 않음. 실패·보류가 보존됨|
|5. 별도 전체 index|확정된 전체 공통 source union으로 비활성 경로에서 build·vector/manifest closure 검증|source/text recipe/provider/model/dimension/hash 일치. 토픽 전용 index나 tag 선필터가 없음|
|6. 검색·선택·compose 비교|258개 노출된 개발 요청으로 정비 후 별도 독립 요청으로 비교|양성·혼동을 함께 평가하고 실제 노출·sample·조건·효과·채택·프롬프트 보존을 구분해 보고|
|7. 픽셀 비교|우선 3쌍, 이어 필요한 나머지 11장면. 동일 사용자 의미로 baseline/stage 실행|실제 전송·저장 이미지·의미/물리 관계 판정 연결. 보이지 않음·부분·거절을 성공으로 계산하지 않음|
|8. 설치·출판|검증된 별도 sealed generation을 비활성 설치로 확인하고 설치 선택 변경. 요청된 출판 범위가 있을 때 정확한 파일만 commit/push|이전 선택과 복구 경로, 최종 source·installed generation·remote SHA가 구분됨. 기존 실패 기록 보존|

## 2. 우선 구현할 데이터

### P0 — 기존 원뜻의 손실과 범위 혼동 정리

- 표지 소품·표지 검사 행위·감식 매크로·감식요원·실험실 탁자의 영어 복제 번역과 구문을 검토한다. **표지 검사→흔적 검사**는 다른 행위이므로 번역 수정으로 위장하지 않는다.
- 마법 붉은 실 보드를 현실 source로 덮어쓰지 않는다. N05의 고정 핀·느슨한 실·자료 경계를 가진 현실 대안의 중복 여부를 확인한다.
- 전체→중경→근접의 두 sequence source는 현재 한 촬영 순간과 분리한다. 명시적 다중 사진/영상과 한 사진을 다른 결과로 평가한다.
- 괴이 보관 세계 장비의 `requires_primary_any_tags`를 삭제해 일반 수사 자료로 쓰지 않는다. 디지털 장면의 독립 source를 작성한다.
- 성인 성폭력·구금 고문·인신매매 묶음의 선언 문맥과 실제 행위/소유자/시간을 `style` 한 효과로 승인하지 않는다. 기존 narrow case와 범죄 개념 전체를 구별한다.

### P1 — 완결 관계가 부족한 분기

|우선 가족|연구 카드|실제 구현에서 확인할 전체 변화|
|---|---|---|
|현장 기록·채취|A01–A10|통제 경계·물건·손·도구·대상·텍스트 식별자·인원·위치·현재 절차 단계|
|표본/분석 매체|F01–F08|표면 소유·표본 분리·실물/화면/인쇄물·그래프가 표현하는 명제·미확정 결론|
|디지털·금융|D01–D08|원본/복제·케이블·포장·노드/선·비교 행·짧은 허구 텍스트·소유/거래의 다른 관계|
|면담·관찰|I01–I08|기존 인물들의 시선·눈높이·손과 도구·탁자·창의 양쪽·차량 안/밖·도움의 대상|
|단서와 서로 다른 관심|N03–N06|두 기록의 차이·반복되는 장소 특징·실의 두 끝·각 손의 다른 지시 대상|

`prop` 또는 `composition` binding이 있다고 실제 물건·인원·텍스트·관계 변화를 허용하는 것은 아니다. 같은 값으로 덮어쓰는 변화도 효과 검토에서 제외하지 않는다. 관찰 가능한 채취 접점이 없으면 ‘sampling’이라는 단어만 넣어 통과시키지 않는다.

### P2 — 재사용·정밀 분기·잔여 근거

트렌치 부품 W01, 빗장 N01, 봉투/관 A08의 이웃, 수갑 V05, 인터뷰 기록 I04는 기존 전체 source와 비교해 재사용을 우선한다. 기존 source의 ‘앉음·성인·단독 인물·좁은 crop’ 등을 없애는 것은 재사용이 아니다. 변형이 필요하면 선택권과 효과를 가진 별도 완결 대안으로 심사한다.

W03/W04/W16/W17/W18/V03 여섯 보류는 실물 도판·형태·임상 근거를 확보하기 전 긍정 운영 pool에 넣지 않는다. F09/F10은 유골/교육 모형이라는 지정 매체를 유지한다. 실제 시신·상해의 대체 성공으로 세지 않는다. V06은 세 패널 교육도 경로로만 다룬다.

## 3. 예상 파일과 등록 단위

구현을 시작할 때 현행 schema와 유지보수 코드를 다시 확인한 뒤 다음 단위를 검토한다.

- `skills/photo-prompt-image-generator/assets/photo_investigative_fiction_semantics_20261025.json`: 원 용어·표기 지위·source 범위·context/proxy/defer·카드 대응. 원문이 영어 검색용 조합어인지 정식 용어인지 구별.
- `skills/photo-prompt-image-generator/assets/photo_candidate_investigative_fiction_20261025.json`: 실제 중복 검토·한영·조건·효과·native 심사를 마친 완결 visual source만.
- `skills/photo-prompt-image-generator/assets/photo_candidate_investigative_fiction_bindings_20261025.json`: 각 슬롯의 전체 정의·소유자·이웃 경계를 확인한 optional binding만.
- 기존 `photo_candidate_candidates_*.json` 중 확정된 소수 CID의 번역/범위 수정: 실제 수정할 필드별 before/after와 이유를 함께 보존.
- `skills/photo-prompt-image-generator/references/investigative-fiction-visual-semantics.md`: 실제 등록 범위·재사용/수정 이유·미확인 의미·검색/이미지의 실제 결과.
- `photo_candidate_corpus_manifest.json`: 승인된 실제 모듈만 등록. 검색 index는 확정 union에서 별도로 재생성.

연구의 `candidate-drafts.json`은 운영 source schema가 아니고 CID도 없다. 그대로 import하지 않는다. `relations`, `owner_nodes`, `observable_gate`는 심사를 돕는 메타데이터이며 prerequisite·native fact·효과 권한의 근거로 승격하지 않는다. source용 한영 문장을 확정한 뒤 실제 field-local 인용과 typed values를 별도로 심사한다.

사진용 출처·CID·binding을 일러스트 경로로 자동 복사하지 않는다. 일러스트에서 사건 보드·교육도·패널 표현을 추가하려면 해당 corpus/schema/매체 계약을 먼저 읽고 별도 변경으로 검증한다. 이번 리서치는 사진 경로를 주 대상으로 현재 source를 대조했다.

## 4. source·slot 심사 기준

각 후보에 대해 다음 질문에 구체적으로 답한다.

1. 주체·각 손/팔·물건·표본·기록·표현 매체는 누구에게 귀속되는가?
2. 도구가 무엇에 닿고, 무엇은 닿지 않으며, 실제 지지·거리·문/창 경계는 무엇인가?
3. 필요한 인원·개수·성인 맥락·모형/실물·정지/연속 정보는 source 전체에서 일관적인가?
4. 한영 문장·정의·별칭·embedding 텍스트의 강도가 같고, 숨은 마법·권한·성적/폭력적 행위·시간 이력이 추가되지 않는가?
5. 실제 변하는 모든 속성과 canonical effects가 requester의 open 범위에 맞는가? 기존 owner가 없으면 임의로 추가하고 있지 않은가?
6. 서로 다른 선택 branch를 union하거나, 짧은 요약에 없는 qualifier를 연구 graph에서 빌려 오지 않는가?

`anatomical_connection`은 선언된 생물/해부학 묘사의 연속·소유·분리 관계다. 가터·벨트·케이블·문 빗장의 물체 접합에는 `object_structure` 등 실제 역할을 검토한다. 수갑은 두 손목과 장비의 접점이지 수갑 자체가 해부학인 것은 아니다. `procedure_step`과 `participant_role`은 현재 catalog에서 contextual 역할이므로 관찰된 한 형태를 곧 절차 완료·직업 진실로 승격하지 않는다.

## 5. 원천·설치·index의 별도 검증

현재 읽은 [maintenance.md](../../../../skills/photo-prompt-image-generator/references/maintenance.md)와 [installed-h-f2.md](../../../../skills/photo-prompt-image-generator/references/installed-h-f2.md)를 구현 시점 기준으로 확인한다. 조사 시점에 다음 entrypoint와 별도 출력 옵션이 존재했다. 아래 운영 검사는 이번 조사에서 실행하지 않았다.

```sh
python3 skills/photo-prompt-image-generator/scripts/photo_installed_h_f2.py --check-runtime
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_shared_candidate_index.py --verify
```

별도 build에는 `build_shared_candidate_index.py`의 `--assets`, `--output-assets`, `--runtime-store` 경계를 확인한다. `--output-assets`와 `--publish`는 현재 함께 사용할 수 없다. 변경 source를 반영할 staging skill root를 만든 뒤 그 전체 source union으로 build한다. 기존 working assets에 대고 명령부터 실행하지 않는다.

벡터는 CID·정확한 텍스트·recipe·provider/model·차원·vector integrity가 모두 맞을 때만 재사용한다. 일부 새 수사물만 모은 작은 pool로 성능을 평가하지 않는다. source가 build 중 바뀌면 이전 해시와 결과를 보존하고 다시 기준화한다. 설치된 H-F2는 sealed snapshot을 읽으므로 working-tree JSON 변경만으로 운영 검색이 바뀌지 않는다.

## 6. 검색·선택·프롬프트 평가

현재 [개발 요청](development-cases.json)은 시각 초안의 한영 138개와 혼동쌍 30개×두 방향×한영 120개, 총 258개다. 작성자와 자료 문구에 노출되어 있으므로 독립 평가셋이라고 부르지 않는다. 검색을 실행한 결과도 아직 없다.

개발 평가에서는 직접 같은 문구를 찾는지보다 B01–B30의 실제 의미 차이를 우선 점검한다. 이후 별도 작성자가 카드·후보 문구를 보지 않고 **16개 가족×양성/혼동×한영=64개 자연어 요청**을 작성하고, 기대 관계/배제 이유를 먼저 동결하는 독립 확인을 제안한다. 현재 독립 작성자는 배정하지 않았다. 같은 작성자가 만든 추가 바꿔 쓰기는 개발셋으로만 분류한다.

baseline과 stage에서 동일한 사용자 의미·소유자·열린 속성·슬롯 의도·모델 공간·검색 예산을 유지한다. 현행 H-F2의 슬롯 질의와 두 whole-scene 질의를 각각 전체 공통 pool에 실행하고 BM25F·실제 query embedding·cosine·RRF를 보존한다. tag 선필터나 수사물 가산점으로 정답을 만들지 않는다.

정렬 순위와 실제 material sample 노출을 별도로 보고한다. 현재 creativity 0/1/2/3의 rank window/sample limit은 8/4, 32/8, 96/12, 256/16이다. 첫 eligible anchor와 저장 seed를 포함한 실제 표본이 있어야 ‘후보가 사용자에게 노출됐다’고 평가한다. 비교 시 통제 가능한 동일 seed·동일 계약을 사용하고, 새 source가 창 크기에 미치는 영향도 기록한다.

|평가 층|지표|판정|
|---|---|---|
|검색|가족/언어별 적합 source의 원 rank·실제 sample 포함률|정답 후보가 원래 없는 요청은 no-valid-source로 분리. metadata나 diagnostic 적중을 성공으로 세지 않음|
|채택 가능성|실제 CID/RID·source hash·guard·owner·effect 허용|노출과 구분. 원뜻을 부분 채택하거나 guard를 우회하면 실패|
|오선택|표지/흔적·실물/화면·천/신체·정지/시간·마법/현실 치환|중대한 소유/의미/허용 범위 위반은 0건 목표. 양성 전부 차단으로 개선했다고 주장하지 않음|
|최종 프롬프트|필수 대상·연결·현재 상태·참조 외형의 보존|실제 compose와 감사 evidence. 카드 exposure만으로 성공 판정하지 않음|
|사진 판독|상황·조사 목적·연결·가시성·개연성|픽셀 평가와 기술 감사 별도. 장면을 읽을 수 있는지도 확인|

연구 문서에는 후보 rank·채택률·품질 수치를 만들지 않는다. 효과 크기·성능 임계치는 비교 전에 기준 데이터와 사용 목적에 맞춰 동결하고 결과를 보고 낮추지 않는다. 기존 무관 가족에서도 작은 회귀 표본을 두어 누아르·범죄·성적 의미가 보통 인물 사진으로 누출되는지 확인한다.

## 7. 픽셀·활성화·복구

[PIXEL-PLAN.md](PIXEL-PLAN.md)는 14장면×baseline/stage의 28장을 제안한다. 먼저 채취·면담·CCTV 비교의 3쌍으로 비교 계약이 작동하는지 확인한 후 나머지를 진행한다. 생성 비용·모델·출력 방식은 후속 구현 시 실제 조건에 맞춘다. 이번 연구가 생성을 예약하거나 승인 기록을 만드는 것은 아니다.

필수 연결의 한쪽이 가려지거나 너무 작으면 `UNOBSERVABLE_NOT_PASS`, 일부만 구현되면 전체 사례 실패다. 도구 출력 차단은 `BLOCKED_UNSCORED`로 기록하고 생성되지 않은 픽셀을 채점하지 않는다. 모형·분장·덮인 포장으로 바꾸었다면 실제 손상·시신·사건의 충족과 합산하지 않는다. 실패와 수정 계보를 보존한다.

source 등록, native qualification, index 검증, sealed release 노출, 실제 source 채택, 실제 전송, 저장 픽셀, 사용자의 수용을 각각 보고한다. 소수 비교 쌍과 모델 비결정성만으로 데이터의 인과적 품질 향상을 단정하지 않는다. 확인된 별도 generation을 비활성 설치에서 점검한 뒤 선택을 전환하고 이전 generation/selector를 복구 가능하게 보존한다.

현재 보고서와 계획의 저장을 제외한 위 단계는 미실행이다. 후속 구현에서는 이 폴더의 초안을 출발점으로 삼고, 현재 변경된 source·설치 계약을 다시 확인해야 한다.
