# 리서치 결과 반영 계획

2026-10-23. **연구·계획 완료 후 실행할 제안**이다. 이 문서의 모듈 이름·평가 수량·목표치는 제안이며 구현 완료 수치가 아니다. 현재 66개 초안을 66개 신규 CID로 일괄 등록하는 계획이 아니다.

## 목표

학원물 요청에서 구체적인 학교 활동과 구조를 더 잘 발견하고 선택할 수 있게 하면서, 사용자가 정한 장면·인원·나이·관계·복식·시대·매체의 의미를 보존한다. 평가할 결과는 다음과 같다.

1. 세일러 칼라/가쿠란/블레이저, 방송/음악/과학 활동, 급식/청소/계주, 하우스/기숙 공간이 실제로 구분된다.
2. 학생회·동아리 모집·짝꿍 공동학습·매니저 지원처럼 학교 공동체의 행동 선택지가 늘어난다.
3. 학원물이라는 라벨만으로 일본·교복·미성년·고백·고딕·폭력·성적 맥락이 자동 강제되지 않는다.
4. 소유자·관계 양끝·가시성·조건·전체 effects와 잠금이 유지된다. 비가시 의미를 원본 픽셀 성공으로 바꾸지 않는다.

## 우선순위와 첫 구현 범위

P0에는 학교 생활의 기본 구분과 오류 방지가 들어간다. S01–S08, S10–S13, S15, W01–W08, A01–A09, A12–A14, A16–A17, R01–R03, R08, H01–H04 및 P0 문맥 카드를 먼저 심사한다. 실제 수량은 semantic-cards.json에서 산출하고, 문맥 카드에는 시각 후보를 만들지 않는다. 후속 P1은 예술·사교육·교외행사·판타지·호러·시간·상징의 선택지를 확장한다.

첫 묶음은 **현실적인 활동과 의복/소유 구조**를 우선한다. 특정 국가·연도의 고증이 필요한 카드와 작품 특유의 공간은 출처 보강 후 별도 묶음으로 채택한다. 비평·성적 피해·권력·자해·시간·음향 범주는 연구에서 유지하면서 그 자체에 자동 visual recipe를 만들지 않는다.

## 단계별 작업과 종료 조건

|단계|작업|완료 증거|멈추거나 다시 심사할 조건|
|---|---|---|---|
|0 기준 고정|최신 HEAD·dirty·source/manifest·현재 인덱스·sealed/installed 세대 확인|정확한 파일/SHA·권위 경계·변경 allowlist|연구 스냅샷과 다른 세대의 소스를 혼합|
|1 의미 심사|210 route·90 카드·66 초안과 기존 CID 전체 의미 검토|reuse/refine/new/context/defer 결정표|키워드 0건·label 유사성만으로 채택 판단|
|2 원문 저술|승인한 한영 전체 분기·owner·조건·효과·의무 작성|검토 가능한 source/binding diff|연구 그래프·태그를 native 사실·permission으로 사용|
|3 source/role 검증|현재 validator와 영향 경로의 focused 회귀 검사|조건·전체 effects·소유·한영·텍스트/매체 경계 확인|약한 age 조건·락 우회·context→direct 승격|
|4 staging 검색 빌드|완전한 별도 source union에서 현재 recipe/space로 build+verify|source/index/vector/coverage/closure의 SHA|기존 벡터 재명명·변경 소스와 옛 텍스트 혼합|
|5 검색·선택 평가|카드 개발 사례·32 경계 사례·독립 holdout 실행|실제 CID/RID/role·순위·노출·선택·거절 이유|노출을 채택이나 시각 품질의 성공으로 보고|
|6 이미지 비교|첫 12사례×3 arms=36장 제안|원본 파일·선택 원문·픽셀 gate·장면 품질의 분리 기록|unobservable/partial/차단을 전체 PASS로 승격|
|7 봉인·설치|현재 native/installed 절차로 봉인·비활성 설치·검증 후 필요한 활성화|세대·포인터·복구 지점·활성 상태|source 수정만으로 설치본 반영을 주장|
|8 발행|사용자가 발행을 요청한 범위의 명시 파일만 커밋/푸시/PR|allowlist·staged blob·원격 SHA 확인|공유 checkout의 다른 변경을 함께 포함|

## 0. 기준과 다른 작업 보존

[BASELINE.json](BASELINE.json)에 조사 도중의 HEAD·dirty/untracked 목록과 운영 관련 212개 파일의 해시를 기록했다. baseline 이전에 수행한 탐색 읽기는 별도이며, baseline이 작업 시작부터 모든 저장소 바이트를 고정했다는 뜻은 아니다. [corpus-snapshot.json](corpus-snapshot.json)의 manifest/module read consistency도 별도로 확인했다.

공유 checkout에는 다수의 다른 변경이 있었다. 이번 작업은 이 연구 폴더만 작성한다. 후속 구현 때도 stash/reset/restore로 다른 작업을 치우지 않는다. 적절한 기존 작업 공간을 재사용하거나 필요할 때 격리 작업 공간을 만들고, 변경 대상 allowlist를 먼저 고정한다. 현행 source·runtime·sealed/installed 세대는 구현 직전에 다시 읽는다.

현재 snapshot은 81개 모듈·20,341개 CID·15,120개 binding·149개 슬롯이다. 이것은 source inventory 수다. positive/diagnostic 투영, 검색 manifest의 metadata 수, 설치 세대의 문서 수는 서로 다른 관측이므로 같다고 가정하지 않는다. 연구 작업에서는 index closure나 설치본 검증을 실행하지 않았다.

## 1. 재사용·보완·신규·문맥·보류 결정

각 결정에는 `card_id`, 실제 기존 CID, 모듈/record/binding SHA, 실제 선택 분기/RID가 있으면 그 값, 전체 조건·effects·의무, slot 의미, source 범위와 한계, 차이를 기록한다.

|결정|충족 조건|이번 연구의 적용 예|
|---|---|---|
|reuse|기존 전체 원문·조건·효과·선택 분기·role가 요구에 부합|일반 교실·오크 도서관·백팩의 정확한 기존 의미|
|refine|기존 의미를 지키면서 한영·관계·고증·발견성을 국소 개선 가능|정독 전체 관계와 짧은 한글 label의 차이; 시대 교실의 실물 근거|
|new|기존 complete source로 필요한 구체 구조/현재 상태를 충족할 수 없음|심사 후 확정할 학생회 안건 공유·모집 접점·배식·계주·방송 장비 관계|
|context|외형·정지사진으로 직접 증명할 수 없는 의미|반복 괴롭힘·성격·지향·동의·그루밍 의도·성적 소재 비평·회귀·소리|
|defer|실물·판본·권한·native 표현을 현재 확정하기 어려움|세부 학교 고증·팬덤 문화사·미확보 비평 문헌·미검증 작품 고유 외형|

`CORPUS-FINDINGS.md`의 10개 기존 CID 판단은 이 심사의 초안이다. 예컨대 `quiet classroom`은 S01의 책상/통로 구조 전체를 이미 갖췄다는 뜻이 아니다. `coordinated school uniform`의 contextual binding을 교복의 모든 디테일에 대한 direct 승인으로 바꾸지 않는다. 학생회 검색 0건은 새 CID가 반드시 필요하다는 증거가 아니다.

성인 코스프레·성인 갸루의 기존 나이/용도/조건을 보존한다. adult라는 라벨이 실제 조건·해당 source의 native 제약에 반영되는지도 직접 심사한다. 조건이 부족하면 기존 후보를 학생 쪽으로 재분류하거나 조용히 수리하지 않고 별도 변경 범위로 다룬다.

## 2. 제안 파일과 실제 등록 경로

아래는 모두 후속 제안 경로다. 현재 만들거나 등록하지 않았다.

|`skills/photo-prompt-image-generator/` 기준 경로|역할|
|---|---|
|`assets/photo_school_life_semantics_20261023.json`|키워드·출처·카드·채택 결정의 추적용 registry; native 조건/효과의 별도 권위가 아님|
|`assets/photo_candidate_school_life_20261023.json`|심사한 신규 V3 source만 등록; 연구 draft ID는 CID가 아님|
|`assets/photo_candidate_school_life_bindings_20261023.json`|현재 catalog의 정확한 의미에 맞는 검토된 binding|
|기존 CID의 소유 모듈|refine 결정한 전체 원문만 국소 변경; shard 전체 재저술 금지|
|`assets/photo_candidate_corpus_manifest.json`|검증한 실제 source/binding 모듈의 명시 등록|
|`references/school-life-semantics.md`|문화/판본/혼동/비가시 경계의 유지보수 지침|
|실제 영향받은 tests/fixtures|owner·락·문맥·매체·한영·age·선택 분기의 의미 있는 회귀|

연구 JSON을 importer에 바로 넣지 않는다. 현재 V3 원문과 V10 pack, 현행 source-unit·owner 선택·qualified role 계약을 확인한 뒤 자연스러운 한영 **전체 source**를 저술한다. 사용자가 선언하지 않은 국가·인물·직함·나이를 연구자의 판단으로 core에 고정하지 않는다. 출처 설명·금지 추론·비평 주석을 positive embedding 문장에 섞어 그 개념을 역유입시키지 않는다.

## 3. owner·조건·effects·role 심사

연구 노드 이름은 실제 인물·물건을 생성하거나 permission을 주지 않는다. 실제 요청의 독립적으로 고정된 core에서 owner를 선택한다. source/binding은 전제와 intrinsic effects, 실제 변경 receiver, 선택한 완전 분기의 의무를 보존해야 한다. 같은 값으로 다시 쓰는 effect도 변경으로 심사한다. binding은 source의 guard/effect를 덮거나 deferred role의 실패를 우회하지 않는다.

|묶음|특히 확인할 관계와 실제 영향|
|---|---|
|S02 창가 뒷자리|동일 책상·창·뒷벽·앞 방향; 위치 효과와 기존 구도/인원 잠금|
|S03 방송실|조작자 손·페이더·마이크·케이블 양끝; 장비/빛/행위 추가 영향|
|W01–W05 의복|같은 착용자·소매·깃·레이어·부착점; 몸/나이/성별 변경과 의복 변경 분리|
|W06 앨범|책·페이지·인쇄 얼굴·빈칸; 실제 subject_count 증가 방지|
|W07–W08 전달/우산|각 인물 손과 소품 소유·수·지지; 관계 감정·동의 추론 금지|
|A04/A12 공동 작업|동일 공책/모형/공동 기록지·손 역할·시선; 새 인물 추가를 사소한 소품 변경으로 처리 금지|
|A05–A09 행사|국자→그릇→쟁반, 바통→두 손, 증서 양끝; 전체 현재 동작과 단계|
|R03–R04 음악|각 손-악기, 지휘 방향, 케이블 양끝; 소리라는 비가시 효과와 구분|
|H01–H04 갈등/봉쇄|행위자/대상·통로·출구·현재 접촉·지지; 의도/반복/감염 원인과 분리|
|F03–F05 창작 기구|손·측정판·케이블·표시; 물체·곡면·국소 빛; 능력/통치 효능을 만들지 않음|
|H05/H07 반사/감시|실물·매체 경계·대응 형상; 추가 실물 인물·원인·감시 권한의 오인 방지|

`location`, `action`, `relational_action`, `contact_point`, `garment_detail`, `occasion_context`, `participant_role`, `visible_text` 등은 제안 role다. catalog에서 이름 존재를 확인한 것은 의미 적합성 승인과 다르다. 같은 source의 문맥 해석을 direct geometry나 신원 사실로 승격하지 않는다. 모든 role를 달거나 149개 슬롯 모두에 `school-life`를 질의어로 넣지 않는다.

## 4. 검증과 staging 검색 빌드

후속 변경에서 영향받은 source validator·native unit·조건/락·선택 분기·한영 투영·role 경로를 검사한다. 연구 validator는 참조·범위·파일 보존만 확인하므로 runtime 의미 검증이나 실제 검색을 대신하지 않는다.

별도의 완전한 staged skill에 승인한 source union을 만든 뒤, **현재** search manifest가 선언한 backend·model/revision·dimensions·recipe·vector integrity를 읽는다. ID·전체 text bytes/hash·recipe·embedding space·벡터 검증이 모두 일치하는 것만 재사용한다. 모델이나 레이아웃의 이름만 바꾸어 재활용하지 않는다. 변경 텍스트는 그 공간의 provider로 계산하고 실패/불명 요청은 별도 기록한다. 다른 원격 provider로 조용히 우회하지 않는다.

현재 스크립트의 실행 방식을 재확인한 뒤 사용할 미실행 예시:

```sh
"$TASK_RUNTIME_PYTHON" "$TASK_STAGED_SKILL/scripts/validate_photo_prompt_dictionary.py"
"$TASK_RUNTIME_PYTHON" "$TASK_STAGED_SKILL/scripts/build_shared_candidate_index.py" \
  --assets "$TASK_STAGED_SKILL/assets" --backend "$TASK_VERIFIED_BACKEND" \
  --cache "$TASK_BUILD_CACHE" --batch-size 32
"$TASK_RUNTIME_PYTHON" "$TASK_STAGED_SKILL/scripts/build_shared_candidate_index.py" \
  --assets "$TASK_STAGED_SKILL/assets" --backend "$TASK_VERIFIED_BACKEND" --verify
```

이 명령은 실행하지 않았다. 현재 옵션과 Python·backend 경로를 구현 시 확인한다. 별도 build/verify는 publish·봉인·설치·활성화가 아니다. source가 빌드 도중 바뀌면 이전 source와 union·CID/RID/binding closure를 다시 맞춰 재검증한다.

## 5. 검색·선택·문장 평가

[development-cases.json](development-cases.json)은 카드에서 파생한 90개 **한영 개발 scaffold**, 총 180질의다. 66개 가시/대리 문장은 초안에서 파생했고 24개 비가시 문맥 질의도 한영으로 저술했다. 이를 독립 자연어 holdout이나 실제 평가 성과로 세지 않는다. [BOUNDARY-CASES.tsv](BOUNDARY-CASES.tsv)의 32개 한영 경계/일반 사례는 개발 회귀용 64질의이며 아직 실행하지 않았다.

실행 전 별도의 작성 단계에서 자연어 holdout **30사례/60질의**를 고정한다: 가시 양성 18, 일반 학교 4, 다의어/판본 4, 비가시/민감 경계 4. 카드 문장의 단순 번역이나 재서술을 독립 holdout이라 부르지 않는다. 저술과 같은 카드에서 만든 개발 자료와 분리하며 데이터 수정 전에 동결한다.

평가마다 requester text·frozen core·변경 허용 범위·나이/국가/매체의 선언값·slot·언어·query bytes·source/index/code SHA·실제 RID·qualified role·현재 resolver의 실제 순위 창/표본 규칙·receipt를 기록한다. `rank → offered → selected → composed`를 각각 보존한다. 정답 ID는 연구 카드가 아니라 실제 심사한 CID/RID/role다.

실행 전에 확정할 **제안 gate**:

- holdout 양성 18개 각각의 언어에서 최소 16개(88.9%)에 의미가 맞고 eligible한 source가 실제 노출된다. 최종 합격 기준은 baseline과 함께 사전 확정하며 결과를 본 뒤 낮추지 않는다.
- 32개 경계 사례의 양 언어에서 잘못된 자동 의무, 인물/나이/관계 추론, 권한 확대, 매체 혼합, 성적 맥락 오염, 비가시 사실의 PASS, 락 우회는 **0건**이어야 한다.
- 사용자 선택 source의 한영 owner·endpoint·전제·의무·effects 의미 불일치는 0건이어야 한다. 문자열 유사도만으로 통과시키지 않는다.
- 일반 학교 control에서 고정 인원·주체·국가·복식·매체의 의도치 않은 변경은 0건이어야 한다. 관련 후보가 선택지 목록에 있는 것과 자동 채택은 구별한다.
- current/proposed corpus를 같은 code/settings로 비교한다. family 하나의 실패를 평균 개선으로 덮지 않는다. 양성 baseline이 이미 높으면 노출률을 억지로 높이기보다 새 형태의 실제 선택 가능성과 잘못된 대체 감소를 평가한다.

## 6. 픽셀·설치·발행과 복구

[PIXEL-PLAN.md](PIXEL-PLAN.md)의 첫 36장은 후보 없는 frozen core, current corpus 보강, proposed corpus 보강을 비교한다. 완전한 가시 구조, 전체 장면의 가독성/자연스러움, 사용자 수용을 별도로 기록한다. 한 장의 성공이나 노출률 개선은 전체 장르의 성공이 아니다. blocked 출력은 이미지가 없으므로 미채점이다.

검증한 source/index를 현행 세대 절차로 봉인하고 비활성 설치→검증→필요한 활성화 순서로 진행한다. 기존 CURRENT·installed/sealed 세대·receipt·과거 run을 복구 가능하게 보존한다. 실패 family는 HOLD하고 수정 source revision에서 다시 심사하며 과거 proof를 덮어쓰지 않는다.

커밋·푸시·PR·발행이 요청되면 연구/구현 파일의 명시 allowlist, staged-name·blob hash, 보호 상태, 로컬·tracking·원격 SHA를 확인한다. 다른 dirty/untracked 작업을 포함하거나 `git add -A`로 일괄 stage하지 않는다. 현재 요청에서는 연구 산출물 작성과 구조 검증까지 수행하며 운영 반영·검색 빌드·이미지 생성·설치·커밋·푸시는 실행하지 않는다.
