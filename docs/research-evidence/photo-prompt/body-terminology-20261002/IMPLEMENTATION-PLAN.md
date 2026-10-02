# 신체 시각 의미·후보 데이터 반영 계획

2026-10-02 작성. 이번 작업은 조사와 계획이며 아래 반영·테스트·렌더는 **미실행**이다. 실행 순서는 `기존 의미/소유자 대조 → 작은 배치의 저작 데이터 → 회귀 → 인덱스 → frozen-core 평가 → 필요 시 픽셀 평가`다. 연구용 파일을 런타임으로 직접 복사하지 않는다.

## 1. 목표와 완료 기준

최종 목표는 구체 신체 표현의 의미를 잘 찾으면서 인물·부위·속성의 혼동과 요청하지 않은 변경을 줄이는 것이다. 키워드 수나 프로필 수 증가는 완료 기준으로 삼지 않는다.

- 새 의미마다 부위 소유자·독립 속성·3개 이상의 관찰 구성요소·보기/상태·가까운 반례·주장 한계·증거 필드·픽셀 게이트를 갖춘다.
- 후보는 기존 슬롯의 실제 허용 차원과 **완전한 효과**를 선언하고, core의 대상과 canonical property에 바인딩한다. 슬롯을 바꿔 잠금을 우회하지 않는다.
- 사용자가 정의한 뜻이 프로젝트 별칭보다 우선한다. 요청에 없는 체형·가림·표현 강도를 후보가 추가할 때는 실제 열린 속성 범위 안에서만 선택 가능하다.
- Exact 활성화와 BM25F/embedding 탐색을 구분한다. 간접 검색 결과는 선택 전까지 선택 후보이며 의무·증거·렌더 게이트를 만들지 않는다.
- source/index hash·현재 스키마·보존해야 할 기존 의미·회귀가 모두 맞아야 배치를 완료한다. 소스 검증과 이미지 품질 검증은 별도로 기록한다.

## 2. 작성안과 소유권

| 파일/산출물 | 이번 산출물 | 후속 반영의 역할 |
|---|---|---|
| `TERM-INVENTORY.json` | 415개 표현 그룹 | 보존·다의성·라우팅의 입력. 자동 별칭 목록이 아님 |
| `SEMANTIC-PROPOSALS.json` | 구체 축 91개 + 문맥/지식 11개 | runtime profile 작성 시 검토할 정의·구성요소·관계·반례·게이트 |
| `CANDIDATE-PROPOSALS.json` | 후보 초안 91개 | 슬롯·positive text·완전한 효과·eligibility 검토의 시작점 |
| `REGRESSION-CASES.jsonl` | 제안 70사례 | 요청 정의·동음어·근접 반례·잠금·픽셀 판정 테스트의 요구사항 |
| `EXISTING-OWNER-MAP.json` | 15개 기존 프로필의 실제 파일 | 기존 ID를 유지하며 보강할 위치 |
| `CURRENT-DATA-AUDIT.json` | 현재 코퍼스와 소스 69건 해시 | 후속 작업 시작 시 바뀐 소스·인덱스를 식별할 기준 |

기존 15개 프로필 중 13개는 `assets/photo_prompt_visual_obligations.json`, 측면·하부 가슴 노출 2개는 `assets/photo_prompt_visual_obligations_portrait_fashion_exposure.json`에 있다. 보강은 실제 소유 파일에 한다. 다른 확장에 같은 ID나 같은 의미를 중복 추가하지 않는다.

기존 후보는 `photo_prompt_tags.json`과 이미 등록된 확장 전체를 로더로 조회해 소유 파일을 찾는다. 기본 사전 원문만 확인하면 확장 후보를 누락한다. `compact_adult_frame`, `willowy_long_limb_proportion`, `long_torso_shorter_leg_relation`, `short_torso_longer_leg_relation`, `shoulder_to_waist_taper`, `waist_to_hip_flare`, `hip_to_outer_thigh_transition`, `back_to_waist_curve`, `waist_to_glute_transition` 및 국소 피부·체모 후보를 우선 대조한다.

신규 축을 담을 파일이 필요하면 `photo_prompt_visual_obligations_body_morphology.json`와 `photo_prompt_body_morphology_extension.json` 같은 **제안 이름**의 저작 확장을 검토한다. 현재는 만들지 않았다. 분리 파일을 채택할 때만 로더의 visual/candidate extension 등록 목록과 사전의 required extension 계약을 함께 갱신한다. 실측 지식·분류 체계·출처 URL을 별도 런타임 의미 저장소로 만들지 않는다.

## 3. 단계 0 — 415개 표현을 개별 검토하고 기존 의미와 대조

먼저 `COVERAGE-MAP.json`의 장별 탐색 연결을 **표현별 검토 매핑**으로 바꾼다. 지금의 연결은 같은 장에 속하는 관련 축 안내이며 동의어 확정이 아니다.

각 표현에 `의미/다의성`, `부위·대상`, `관찰 축`, `기존 owner ID`, `출처 수준`, `문맥별 긍정 사례`, `가까운 반례`, `결정`을 기록한다. 결정은 `기존 보강`, `새 독립 축`, `복합 조합`, `지식/문맥 유지`, `근거 보류` 중 하나다. 415개를 415개 프로필로 만들지 않는다.

문자열 프로브가 비었다고 의미 부재로 판정하지 않는다. 기존 정의·의역·component·concept unit·directed relation을 조회하고 형태가 같으면 ID를 재사용한다. 표현만 같은데 소유자나 물성이 다르면 합치지 않는다. 피부의 패임과 퀼팅, 몸의 허리와 하의 허리선이 예다.

한국어 압축어와 일부 커뮤니티 은어는 신뢰할 수 있는 원어 사전/용례를 추가 확보하기 전까지 broad exact alias 승격을 보류한다. 그동안 원 대화의 표현과 문맥은 연구 목록에 유지한다. Root-height·발 아치·눈꺼풀·귀 부착 등 세부 자료의 부족한 근거도 해당 레코드 단위로 보강한다.

완료 조건: 모든 표현에 처분 결정이 있고, 신규 축은 전체 1,419개 프로필과 전체 후보 코퍼스의 중복 검토를 거쳤으며, 보류는 이유·필요 근거를 갖는다.

## 4. 단계 1 — P1의 24개 축: 혼동 위험이 큰 기본 형상

P1은 신장/프레임/폭·길이 관계, slender·stocky·wiry·soft volume·curvilinear, 근육 부피/윤곽, 어깨 폭/경사, 흉곽 폭/깊이, 몸통/다리·허리 위치, 가슴 prominence/root width/projection, 허리 폭/깊이, 골반 폭/엉덩이 projection, hip dip, thigh gap이다.

처음부터 24개를 한 번에 활성화하지 않고 다음 네 묶음으로 반영한다.

1. **전신 기본 축:** stature·frame·width/length·soft volume. Petite와 skinny의 비동의성, 작은 키+두툼한 몸, 큰 키+가는 몸을 유지한다.
2. **근육·상체:** volume과 definition, 어깨 폭과 경사, ribcage와 breasts의 owner를 분리한다.
3. **국소 가슴·골반:** root width/projection/spacing, hip width/gluteal projection의 독립 조합을 지원한다.
4. **기존 계약의 범위:** `글래머 체형`, hip dip의 국소 의미, thigh gap의 공간·자세 계약을 검토한다.

기존 `curvilinear_figure_relation`, `bust_prominence_relation`, `toned_muscular_build`의 ID와 authored 의미를 유지한다. 애매한 별칭 변경은 definition/source/version을 기록하고 현재 동작과 제안 동작의 차이를 보여 준다. `글래머=가슴만` 같은 명시적 요청 정의는 즉시 전신 곡선 의무의 근거가 되어서는 안 된다. 반면 역사적 pack을 새 의미로 재해석하지 않는다.

Hip dip는 국소 indentation과 전체 waist→hip transition의 관계를 모델링한다. 기존 프로필의 필수 그룹을 무조건 약화하지 않는다. 국소 계약이 별도로 필요하면 exact 충돌·의미 중복·복합 관계를 검토한 뒤 정의한다.

Thigh gap는 현재 profile의 close-foot stance·inner boundaries·real background 계약을 보존한다. 후보화 시 `body_pose`에 body geometry 효과를 숨기지 않는다. 형상 관계 후보와 이미 요청된 자세의 지원 후보로 분리하거나 소유권 계약을 검토한다.

완료 조건: P1 각 묶음의 positive·paraphrase·near-miss·negation·requester-definition·lock 사례가 통과하고, 기존 shape/aesthetic 계약이 보존된다. broad alias는 이 조건을 통과한 좁은 문맥만 추가한다.

## 5. 단계 2 — P2의 35개 축: 국소 형상과 상태

목·쇄골·견갑·등, 머리/몸 비율, 가슴 fullness/root height/spacing/vertical relation/asymmetry, 복부/배꼽/근육 구획, 엉덩이 분포/접힘, 사지·손·발, 얼굴 국소 특징, 자세에 따른 표면 변화를 다룬다.

작성 중 중요한 구분은 `고정된 형상`, `현재 자세/하중`, `조명에서 읽히는 표면`, `옷의 지지/압박`이다. 각 레코드의 필요 조건으로 따로 선언한다. 비교 보기의 자세·조명이 다르면 수치나 본래 형태를 판정한 결과로 사용하지 않는다.

`face_shape_relation`의 11개 기존 얼굴형을 유지하고 eyes/nose/lips/ears의 국소 소유자를 추가 검토한다. 인중은 기존 `upper_lip_philtral_contour`를 보강한다. Anatomy 문서의 일반적 위치만 확인된 세부 축은 추가 공개 근거가 확보된 뒤 exact 활성화를 검토한다.

`pose_surface_change`는 pose와 표면·형상에 걸친 효과를 가진다. 현재 `body_pose`의 차원만으로는 완전한 효과를 선언할 수 없다. 자세가 이미 core에 있는 경우의 표면 지원과 실제 자세 변경을 분리한다. 전체 효과를 선언할 수 없다면 후보 추가를 보류한다.

완료 조건: 동일 속성을 조명·의복·표정으로 흉내 낸 사례가 통과하지 않고, 필요한 보기와 잠긴 framing이 충돌하면 부적합으로 처리한다. 작은 표면 특징은 native 크기 게이트를 갖는다.

## 6. 단계 3 — P3의 19개 축: 피부·체모·옷 경계

피부색·색소·microrelief·striae·cellulite·scar-like relief·wrinkles, 털 굵기/색·분포/길이·상태, nail geometry, neckline·side/lower chest·cleavage·midriff, opaque outline·sheer layering, band compression을 다룬다.

기존 `skin_finish`, `skin_condition`, `body_marking`, `facial_hair`, `garment_detail` 후보를 우선 보강한다. 같은 용어가 있다고 skin_finish에 모든 피부 현상을 넣지 않는다. 색소 패턴·표면 부조·소재 광학·해부 형상은 다른 효과다.

`pfe_lateral_chest`, `pfe_lower_chest`, `decolletage_neckline_exposure`, `sheer_garment_optical_layering`는 기존 소유자와 필수 구성요소를 재사용한다. 좁은 same-garment 경계 계약을 유지한다. 외측 가슴을 겨드랑이로, 하부 가슴을 복부로, 비침을 타이트핏으로 바꾸면 원래 의미의 실패다.

`compression_contour`는 appearance+body_geometry의 연동 효과, `nail_shape`는 자연 판의 geometry와 색/연장의 appearance를 분리한다. 현재 슬롯 차원과 다르면 slot 지원을 분리하거나 ownership 정책을 먼저 검토한다. 새로운 슬롯부터 만드는 방안은 우선하지 않는다.

완료 조건: 색소↔그림자, striae↔cellulite, skin↔fabric, body hair region↔whole body, opaque↔sheer, underboob↔midriff의 가까운 반례를 통과한다. 원래 garment coverage와 body shape 잠금이 유지된다.

## 7. 단계 4 — P4의 13개 축와 11개 문맥/지식 레코드

명시적 중립 해부 문맥의 nipple/areola, gluteal cleft, vulvar/penile/scrotal/perineal 관계, 성인 의복 문맥의 under-gluteal boundary/bulge/central crease, 요청된 limb difference/prosthesis/mobility support를 검토한다. P4는 앞 배치가 완료되었다는 이유만으로 자동 등록하지 않는다. 레코드마다 근거·소유자·문맥을 확인한다.

기관의 이름은 고정 노출·성적 행위·치수·흥분·개인 이력의 추가 근거가 아니다. 의복 표면의 projection/crease와 실제 기관 형상을 분리한다. 해부 구성은 명시된 요청과 가림 조건을 보존한다. 차단된 렌더는 원래 의미의 성공 또는 품질 실패 점수로 전환하지 않는다.

11개 문맥/지식 레코드에는 body composition/measurements, 업계 사이즈, 스타일 분류, 평가어, 한국어 압축어, 성인 다의어, 커뮤니티 명칭, 브라 사이즈, 해부 이력/내부 구조, 3D workflow, 예술적 비율을 남긴다. 연구 내용을 긍정 검색 prototype으로 일괄 투입하지 않는다. 시각적으로 동일한 의미가 검토된 의역만 existing-slot context extension으로 추가한다.

Limb difference와 보조 장치는 입력에 명시된 구성과 실제 연결을 보존한다. 원인·능력을 추정하거나 일반 신체 구성으로 자동 보정하지 않는다. 가능한 장치 형상도 실제 요청 범위 안에서 정한다.

## 8. 저작 데이터에 옮길 필드

| 대상 | 보강 필드 | 검토 규칙 |
|---|---|---|
| Visual profile | definition, paraphrase_examples, component_semantics, concept_terms | 부위/속성과 관찰 관계의 긍정 텍스트. provenance·taxonomy 설명을 넣지 않음 |
| Activation | exact_terms, project_glossary_aliases, context/exclusion guards | whole-request 의미와 단어 경계 검증. 다의어 broad exact 보류 |
| Evidence | required_evidence_fields, evidence_requirements | prompt에 들어갈 실제 구절과 같은 owner·관계 |
| Evaluation | render_gates, reject_substitutes, claim_limits | required components 전부 확인. 혼동·불가시·비수치 한계 분리 |
| Candidate | ko/en, aliases, keywords, embedding_text, concept_units, relations | 검토된 시각 의역·독립 단위·방향 관계. 출처/반례/금지 설명은 positive text에 넣지 않음 |
| Ownership/eligibility | slot dimensions, affected_properties, facets/guards | 실제 core target/property로 binding. 상태·보기·조건은 다른 후보가 만들어 주었다고 간주하지 않음 |

연구 후보의 `research.*` 경로는 설명용이다. 실제 canonical target/property를 확인한 뒤 옮긴다. broad wildcard로 몸 전체를 잠금 해제하지 않는다. 미지정 property는 eligible로 간주하지 않는다. default weight는 기존 동등 후보의 범위에서 검토하고 높은 값으로 노출을 강제하지 않는다.

## 9. 검증 순서와 실제 도구

아래 명령은 **후속 데이터 반영 단계의 예시**이며 이번 조사에서 실행한 체크가 아니다. 경로는 현재 저장소에서 확인했다. 배치별 새 사례를 현재 테스트 구조에 구현하고 기존 테스트의 기대 의미를 약화하지 않는다.

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python -m unittest tests.test_photo_body_shape_semantics tests.test_photo_body_aesthetic_semantics tests.test_photo_visual_profile_retrieval tests.test_photo_core_retrieval tests.test_photo_control_span_ownership tests.test_photo_embodiment
.venv/bin/python -m unittest discover -s tests
git diff --check
```

이미 source를 바꿨으면 stale index 검사가 실패하는 것은 정상이다. 저작 데이터 자체 검증과 인덱스 검증의 실패 원인을 구별하고, stale 검사를 끄지 않는다. 인덱스를 갱신한 뒤 최종 dictionary validator와 전체 discovery를 완료한다.

인덱스는 `build_visual_profile_index.py`와 `build_semantic_index.py`의 현행 CLI로 재생성한다. Visual builder의 `--cache-index`, semantic builder의 기본 호환 캐시·checkpoint를 사용하되 **동일 텍스트·동일 vector space**만 재사용한다. 배치 크기 기본값 1을 유지하고 현재 provider/model/dimensions 및 source hashes를 기록한다. 새 embedding 호출과 해당 비용은 후속 데이터 반영 작업 범위에 속한다. 이미지 API는 일반 사전/회귀 검증에 사용하지 않는다.

`photo_prompt_visual_profile_index.json`와 `photo_prompt_semantic_index.json` 및 semantic shards는 파생 결과다. 직접 손으로 의미를 편집하지 않는다. 새 manifest가 완성되어 검증된 뒤 그 결과가 대체하는 구체 obsolete shard만 정리한다. 다른 작업의 소스나 캐시를 삭제하지 않는다.

## 10. Frozen-core 비교 평가

현재 SHA 기준선과 반영 후 SHA를 고정한다. 입력 envelope·core·requester definitions·intent/property locks·creative controls·embodiment review를 동일하게 유지하고, query/index recipe와 hash를 기록한다. 같은 core에 소스 변경만 비교하는 평가와 writer가 독립적으로 core를 작성하는 평가를 분리한다.

1. 70개 제안 사례를 의미·활성화·ownership 테스트로 구현한다. `R004/R005`의 요청 정의 우선, `R017/R018`의 root/spacing 구별, `R040–R046`의 의복 경계를 포함한다.
2. 동일 용어라도 부위·owner·물성이 다른 근접 반례와 부정 범위를 포함한다. `lean/wiry/cleavage/thicc/well-endowed/베이글/V-line/S-line`의 동음어 사례를 유지한다.
3. 한국어·영어의 긍정 사례와 자연스러운 의역을 별도로 둔다. Exact 긍정 사례와 의역의 후보 노출을 구분한다. 의역이 노출되었다고 hard 의무 생성이 정당화되지 않는다.
4. 테스트 문장을 positive prototype에 그대로 복사하지 않는다. 신규 authored 사례와 **동결된 별도 holdout**을 나누고 결과를 따로 보고한다.
5. Ground-truth 의미·원하는 owner·관련 property·부적합 후보를 agent가 명시적으로 검토한다. 문자열 일치 점수만으로 정답을 정의하지 않는다.

측정은 `target profile/candidate exposure`, `wrong-owner/axis exposure`, `hard activation precision`, `negated-scope leakage`, `locked-property interference`, `source/index validity`, `literal evidence preservation`으로 나눈다. Exposure와 실제 채택을 구분한다. 선택하지 않은 optional 후보 0개 채택도 유효하다.

합격 기준은 회귀의 요청 의미·잠금·부정 범위 침범 **0건**이며, 목표 의미가 완전히 노출·보존되는지 사례별로 보고한다. 검색 수치에는 분모·K·eligibility를 적고 source-passing만으로 개선을 주장하지 않는다. 현행 core slot당 최대 4개, support slot당 최대 2개, 전체 최대 64개의 후보 제한은 검색 부하 제약이며 내용 추가 quota가 아니다.

## 11. 픽셀 평가가 필요할 때의 별도 실행 설계

첫 픽셀 파일럿은 외관·의복 경계가 중요한 P1/P3 대표 사례 중 8개 정도를 고정하는 방안을 제안한다. 정확한 사례·의복·시점은 평가 목적에 맞춰 정하며, 원래 개념을 더 쉬운 대체물로 바꾸지 않는다. 비교는 `기존 데이터`, `보강 데이터에서 optional 후보 0개 채택`, `명시적으로 채택한 적합 후보`의 3조건으로 나눌 수 있다. 단순한 단어 추가 효과와 candidate opt-in 효과를 섞지 않기 위한 제안이다.

Core와 원래 요청 의미를 고정하고 모델·날짜·개수·seed 지원 여부·reference·prompt/negative 원문·hash·attempt·이미지 artifact를 기록한다. 공통 seed가 지원되지 않으면 이를 적고 완전히 같은 확률조건을 통제했다고 주장하지 않는다. 예산과 반복 수는 별도 평가 작업에서 정한다.

각 이미지의 required component별 native/thumbnail 판정을 남기고 `PASS/FAIL/PARTIAL/UNASSESSABLE`을 구분한다. PARTIAL은 전체 통과가 아니다. 가려진 필수 경계·프레임 밖의 부위는 성공으로 세지 않는다. 차단 호출은 unscored attempt다. Sideboob를 midriff로, hip width를 gluteal projection으로 바꾸는 대체는 원래 의미의 성공이 아니다.

Prompt literal audit → runtime binding audit → 실제 픽셀 → 사용자 수용은 별도 열이다. Prompt와 runtime이 통과해도 피부 요철이나 옷 경계의 이미지 표현은 실패할 수 있다. 대표 파일럿 통과를 91개 축 전체의 픽셀 보장으로 확대하지 않는다.

## 12. 배치 종료 기록과 적용 판단

각 배치에서 기존/신규 ID, 변경 별칭, 변경 source와 index hash, 소유권 검토, 추가/보류 표현, 긍정 사례·반례·holdout 결과, 실제 실행/미실행 항목을 저장한다. 신규 데이터로 다시 조회한 merged counts를 기록하고 임의 프로필 개수를 목표로 맞추지 않는다.

필요한 회귀가 실패하면 해당 배치의 exact 승격·후보 채택을 멈추고 author data/guard/property 선언의 원인을 수정한다. 회귀를 느슨하게 바꾸거나 별칭을 더 넣어 실패를 감추지 않는다. 이미 검증된 다른 독립 배치는 유지할 수 있지만 전체 적용 완료로 표시하지 않는다.

이번 리서치의 재현 검사는 `validate_research_artifacts.py`와 `VALIDATION.json`에 남긴다. 그것이 검증하는 것은 JSON/TSV 참조·출처·초안 내부 구조·baseline source 보존이며, 위 단계의 런타임·검색·렌더 성공은 아니다.
