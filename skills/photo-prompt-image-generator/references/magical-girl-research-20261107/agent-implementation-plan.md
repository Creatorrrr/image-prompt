# 마법소녀 용어 반영을 위한 실제 자산·검증 계획

조사 기준: 2026-11-07 로컬 작업본. 이 문서는 조사와 향후 실행 계획이다. 후보·바인딩·검색 뷰·인덱스·실행본을 이 작업에서 수정하거나 생성·활성화하지 않았다. 모든 경로는 저장소 루트 기준이다.

## 1. 실제 소스와 권한 경계

- 사진 후보 정본: `skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json`. 이번에 읽은 manifest SHA-256은 `e04e4ef09b3333fecc4eeda5e934386545c9558398fa1eee87fd84e81ce307b0`, 모듈 168개(후보 86, 바인딩 80, slot_catalog 1, policies 1)다. 이 값은 스냅샷이므로 실제 수정·빌드 직전에 다시 계산한다. `photo-candidate-module/v3`의 후보 ID 하나는 정확히 하나의 payload 소유자를 갖고, `photo-candidate-slot-bindings/v3`는 후보에 0개 이상 연결된다. `conditions`/`effects`는 후보 정본에서, 역할별 적용 조건은 바인딩에서 읽는다. 조건부 realization은 하나의 선택된 대안을 전체 명제로 보존한다. 한 용어 검색에 매칭된 모든 명제를 자동 합치지 않는다.
- 유사한 선행 자산은 `assets/photo_cosplay_semantics_20261106.json`, `assets/photo_candidate_cosplay_20261106.json`, `assets/photo_candidate_cosplay_bindings_20261106.json`, `assets/photo_candidate_retrieval_views_cosplay_20261106.json`, `assets/photo_cosplay_research_context_views_20261107.json`이다. 연구 원문 맥락과 실행 가능한 후보의 검색 뷰는 별개다. 예컨대 코스프레 연구 맥락은 `context_only: true`, `native_approval: false`이며 원문 출처 포인터·인용·레지스트리 해시를 기록한다. 이 구조를 참고하되 새 파일이 기존 시스템에 자동 적용된다고 가정하지 않는다.
- 정식 검색 뷰 검증 함수는 `scripts/photo_candidate_retrieval_views.py`다. `whole`, `context`, `relation`을 구분하고, 진단 레코드에 양성 뷰를 허용하지 않으며, 후보/realization의 원본 해시·인용·whole coverage를 검증한다. 원문 용어 맥락 뷰가 후보 검색 뷰와 같은 권한을 가진다는 뜻은 아니다. 신규 뷰에 원본 명제 전체, 조건, 소유자 및 필수 관계를 유지하고 나머지 문장·별칭은 검색 단서로만 취급한다.
- 일러스트 경로는 별도다: `skills/subculture-illustration-image-generator/assets/research_evidence_illustration/character_world.jsonl`의 `transformation_fx_causal_grammar`, `assets/illustration_universal_scene_candidates_v1.json`, `assets/illustration_universal_semantic_bindings_v1.json`, `assets/illustration_topic_crosswalk_v1.json`, `assets/research_evidence_universal_scene/manifest.json` 및 `scripts/universal_scene_runtime.py`. 사진 후보 스키마를 그대로 복사하거나 인덱스 포함을 추론하면 안 된다. 이 런타임은 별도 후보·semantic bindings·research manifest 해시와 선택 재생을 검증한다. 해당 경로를 전수 비교하기 전 일러스트 커버리지는 미확인이다.

## 2. 301개 행에서 실행 가능한 의미까지

1. **원문·분해·출처를 고정한다.** `source-reconciliation.json`의 301개 행 ID와 원문 셀을 보존한다. 추가 별도 연구 레지스트리(가칭 `photo_magical_girl_semantics_YYYYMMDD.json`)에 원문 행→원자 개념 1:N 및 개념 ID를 둔다. 같은 행의 서로 다른 개념(오프숄더/스트랩리스, 카보숑/패싯, 각 고유 지팡이)을 분리하고 행을 삭제하지 않는다. 각 개념에 실제 출처 URL·본문 위치·직접 지지 명제·시대/작품/매체·해석 및 미확인 사항을 기록한다. 18절 창작 조합은 원문 예시로 보존하고 구성요소 근거와 창작 조합을 구별한다.
2. **발견을 전수 검토와 분리한다.** `candidate-discovery-all.jsonl`은 해당 manifest 86개 후보 모듈에서 제한된 필드와 표면어로 찾은 행–후보 단서다. 각 단서에 `(row_id, module, candidate_id, realization_id)`를 부여하여 중복 조회를 줄이되 행마다 별도 의미 판정을 남긴다. 한 후보를 한 번 전체로 읽은 후 모든 관련 행과 비교한다. 어휘 오탐을 관련 없음으로 명시하고, 표면어에 없는 한·영·일 변형, 전체 content·조건·효과·바인딩, 일러스트 자산과 실제 검색 뷰를 별도 확대한다. 이것까지 하기 전 `11,134`는 전체 관련 후보의 수가 아니다.
3. **각 비교의 재현 가능한 증거를 남긴다.** 후보 원본 모듈·ID·전체 정규화 SHA-256, `record_kind`, 모든 선택 가능한 realization, 명제의 en/ko, 내장 조건/활성화/제외/잠금/효과, 연결된 각 바인딩의 역할·조건·효과 권한, 대상 소유자·수·관계·매체를 기록한다. 분류는 `조건부 정확`, `일부 사례`, `대조 개념`, `연구/진단`, `맥락만`, `미해결`로 나누고 이유와 누락된 명제를 필수화한다. `visual_profile`의 활성화나 가시 게이트를 양성 이미지 지시로, 연구 메타데이터를 native 승인으로 취급하지 않는다. 강한 성인 조건 및 성적 맥락은 해당 후보의 실제 조건 그대로 둔다.
4. **각 원자의 처리 결정을 남긴다.** 전제·효과까지 동등한 경우에만 기존 후보 재사용으로 표시하고 추가 의복·색·소유자·행위가 있으면 선택적 부분 사례로 남긴다. 명시적 서사(비밀, 계약, 시간 반복)는 원문·출처 범위의 맥락으로만 유지하고, 관찰 가능한 결과 예시는 별도의 선택적 후보로 제안한다. 후보 부재가 충분히 검토된 경우에만 추가 후보를 작성한다. 출처 한계나 스키마 문제로 결론을 못 내리면 원자 ID·원인·필요 증거와 함께 보류한다.

## 3. 시각 데이터·후보·뷰 설계

- 시각 명제는 `매체/개체와 소유자 → 부위/파츠 → 개수·배치 → 접점·방향·경계 → 상태·가시 조건`을 유지한다. 재질과 가시 광택, 물체 방패와 공간 결계, 개별 프레임과 시퀀스/뱅크, 사실과 원인·기능을 별도 필드로 구분한다. 예를 들어 한 사람의 어깨 갑옷을 보여주는 후보에 팔뚝 갑옷이나 종교적 의복이 추가돼 있으면 전체 후보는 그 추가 조건이 요청 범위에서 허용된 경우에만 선택한다.
- 기존 corpus와 충돌하지 않는 ID, 한영 전체 문장, 개체·관계·비관찰 게이트, `conditions` 및 실제로 바뀌는 전체 `effects`를 가진 선택적 후보만 `photo-candidate-module/v3`로 작성한다. 진단과 맥락은 별도 레코드/뷰로 유지하고 양성으로 변환하지 않는다. 슬롯 바인딩은 후보 선택·효과·나이·소유자 권한을 새로 만들지 않는다. 사용자가 명시하지 않은 색·의복·연령·작품 고유명·노출을 기본값으로 추가하지 않는다.
- 각 후보의 각 realization에 대해 원본 포인터·완전한 문자 인용·원본 해시를 가진 whole 뷰를 만들고 추가 context/relation은 검색용으로 구분한다. 원문 행 중심의 연구 맥락 뷰에는 행 ID·원문 인용·독립 근거의 지원 범위·상충/미결 사유와 링크를 남기되 `context_only`를 명시한다. 본문의 시각 제안을 외부 출처의 사실처럼 인용하지 않는다. 뷰가 있다고 native 선택 자격, 실행 인덱스 노출, 픽셀 성공이 자동으로 생기지 않는다.
- 사진과 일러스트를 연결할 경우 먼저 각 런타임의 실제 필드·해시·소유자 계약을 검토하고 별도 crosswalk 제안서를 작성한다. 일러스트의 사건·연속 프레임 관계를 사진 단일 프레임의 사실로 강제하거나 반대로 누락하지 않는다.

## 4. 준비 및 검증 명령과 실질적 한계

아래는 **향후 변경을 수행할 때**의 명령이다. 현재 산출물에 실행되었다는 뜻이 아니다. 기존 뷰/데이터·실행본을 입력 경로로 덮어쓰지 않는다.

```sh
# 새 사진 검색 뷰에 기존 검토 뷰와 전환을 재생·검증해 별도 파일로 준비
python3 skills/photo-prompt-image-generator/scripts/photo_prepare_reviewed_views.py \
  --input /absolute/new-magical-girl-views.json \
  --output /absolute/prepared-magical-girl-views.json

# 소스 형식·기존 뷰 계약의 변경 범위 검증
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python skills/photo-prompt-image-generator/tests/test_candidate_retrieval_views.py
.venv/bin/python skills/photo-prompt-image-generator/tests/test_prepare_reviewed_views.py

# 활성 인덱스를 덮지 않는 별도 후보 원본 인덱스 빌드
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_shared_candidate_index.py \
  --backend embeddinggemma2-local --output-assets /absolute/staged-assets \
  --cache /absolute/staged-cache --batch-size 32

# 실제 선택된 설치본과 recorder 검증: 읽기 전용
python3 skills/photo-prompt-image-generator/scripts/photo_installed_h_f2.py --check-runtime
```

`photo_prepare_reviewed_views.py` 기본 current 모드는 고정된 과거 오버레이와 전환 및 현재 후보 인용·해시를 확인하며 충돌 시 중단한다. `--release-mode historical` 출력은 완전한 당시 코퍼스 스냅샷도 현재 검색본도 아니다. `validate_photo_prompt_dictionary.py` 및 테스트의 성공은 문장 뜻이 진실이거나 검색 순위·이미지 품질이 좋다는 증거가 아니다. 실제 변경이 있을 때 검증 결과를 보관해야 한다.

**중요한 빌드 제약:** `build_shared_candidate_index.py`는 후보 원본의 별도 인덱스이며 H-only+F2의 다중 뷰 검색본 전체를 생성하지 않는다. `references/tobe-data-maintenance.md`는 임의의 새 후보에서 H-only+F2까지 한 번에 만드는 통합 명령이 현재 없다고 명시한다. 기존 TO-BE runtime/source 번들 설치기는 고정 원본에 맞는 검증본을 복원할 뿐, 새 후보를 재임베딩하거나 새로운 뷰를 포함하지 않는다. 따라서 다중 뷰 임베딩·H-F2 세대 빌드/봉인 절차를 별도 규명하고 구현·검증하기 전에는 위 빌더 성공만으로 사용자 검색에 새 데이터가 노출된다고 보고하지 않는다.

별도의 실제 H-F2 빌드·qualification이 성공했을 때에만, `scripts/install_photo_h_f2_runtime.py --source-store STORE --generation-id ID --no-activate`로 이미 적격 판정된 세대를 **비활성** 설치해 실세대 질의·무결성·회귀를 확인한다. 이 명령은 빌드기가 아니다. 활성화는 소스 manifest와 빌드 입력의 해시가 여전히 일치하고, 이전 선택본·복구 경로를 보존한 뒤 별도 릴리스 단계에서 수행한다.

이번 읽기 전용 `--check-runtime`은 통과했으며, 선택된 H-F2 세대 `40ca5236a557a29fd14113fcf830a6a96f8a077f41ebd8c8283fb9d96a1a5a8f`와 native 세대 `c23afd2de882fd075d91e1fec9bf96ed59ab823fd26efa414ac0a715a56f3be2`의 NumPy/recorder 결합만 확인했다. 설치된 소스와 작업 manifest의 완전 일치, 마법소녀 항목 포함 여부, 검색 성능 또는 픽셀은 이 확인만으로 증명되지 않는다.

## 5. 회귀·관찰·동시 변경 관리

- 누락 검사: 301행→원자→출처 또는 구체 보류→기존 후보 비교/새 후보/맥락 결정→바인딩→뷰→해시가 이어져야 한다. `미검토`와 실제 관련 없음, 직접 근거/부분 근거/접근 실패, 맥락/양성/진단을 각기 다른 상태로 유지한다. 연구 조사의 완료와 구현·배포 완료는 따로 집계한다.
- 고정된 독립 한영 질의로 포함·제외·다의어·명시 금지·복수 인물·각 realization·짧은 동의어를 평가한다. 특히 양쪽 홍채색/한쪽 홍채 내부색, 견갑/견장, 케이지/속치마, 가터/허리 벨트, 원작 고유 카드/일반 카드, 실제 상해/분장, 타임루프/한 프레임, 부유/도약을 대조한다. 미리 개발자가 작성한 정답 질의와 나중에 만든 독립 평가 질의를 분리하고 낮은 순위·미반환·오탐을 전부 기록한다.
- 평가 단계는 `소스·뷰 무결성 → 검색 반환/순위 → 선택·효과·전체 명제 보존 → 프롬프트 감사 → 저장된 실제 이미지의 각 관계와 가림 → 사용자 수용`을 따로 기록한다. 가려진 접점·내부 후프·섬유 조성·원인·시간 경과는 미관찰이다. 이미지 생성이 성공했다는 사실은 해당 이미지가 구성요소를 충족했거나 개선됐다는 증거가 아니다.
- 다른 작업의 신규 코스프레·간호복 데이터와 현 manifest를 덮어쓰지 않도록 빌드 직전과 설치 직전에 manifest/모듈/뷰 SHA를 재검사한다. 입력이 바뀌면 멈추고 전체 변경을 병합한 후 준비·재임베딩·검증을 다시 수행한다. 실행본 포인터와 Git 밖 모델·인덱스는 Git 상태와 별도로 확인한다. 장기간 수행될 경우 보호할 활성 closure·이전 세대·진행 중 작성물을 식별한 뒤에만 정리한다.

## 6. 산출물 명세와 현재 스키마의 실제 차이

아래 연구용 산출물 이름과 필드는 **구현 제안**이며, 현재 코퍼스 validator가 이미 지원하는 새 스키마라는 뜻이 아니다. 원문의 행을 재작성하거나 별칭을 표준 정의로 승격하지 않도록 연구 산출물과 배포 산출물을 나눈다.

| 산출물 | 제안하는 최소 필드 | 필수 검증 및 이후 단계 |
|---|---|---|
| 원자 개념 레지스트리 | `atom_id`, `row_id`, 원문 `source_cell_pointer`, 원문 표제·설명에 대한 정확 인용, 한정된 `sense`, `concept_kind`, `scope`, `unresolved` | 각 행에 하나 이상 원자가 있어야 하고 모든 참조가 301개 원문 행에 되돌아가야 한다. 원자의 의미가 원문에 없으면 `authored_inference`로 별도 표시한다. |
| 근거 원장 | `evidence_id`, `atom_id`, URL, 확인 방식·날짜, 자료 유형, 정확한 주장/적용 범위, 미지원 명제, 접근 상태 | 창작 예시·시각 제안과 독립 근거를 분리한다. 직접 열기와 검색 발췌를 구분한다. 원문 정의 전체에 대한 지지로 잘못 올리지 않는다. |
| 후보 비교 원장 | `atom_id`, corpus manifest SHA-256, 모듈·CID·RID, canonical record SHA-256, 전체 조건/효과·바인딩 참조, 의미 판정과 남는 차이, 심사 상태 | 후보 하나가 여러 행에 걸치면 원본 검토를 재사용하되 원자별 판정은 따로 둔다. 조회되지 않은 레코드는 `not_reviewed`, 검색 누락 가능성이 있는 표면어 0건은 `not_discovered`로 남긴다. |
| 라우팅 결정 | `atom_id`, `visual`/`context`/`diagnostic`/`hold` 중 하나 이상, 근거와 CID/RID 또는 보류 사유 | 복수 라우팅 가능. 연구 맥락이 양성 후보를 자동 생성하지 않고, 시간·인과나 원인 같은 비가시 명제를 정지 이미지의 증명으로 올리지 않는다. |
| 후보·바인딩·검색 뷰 | 기존 `photo-candidate-module/v3`, `photo-candidate-slot-bindings/v3`, `photo-candidate-retrieval-views/v1` 계약을 따르는 별도 신규 파일 | manifest를 갱신하기 전 staging copy에서 전체 corpus와 뷰를 검증한다. 새 연구 필드만 만들면 운영 코드가 소비한다고 가정하지 않는다. |
| 연구 맥락 뷰 | 원문 registry 및 원문 원자 포인터/인용, 출처 범위, 검토 원장·해시, `context_only: true`, `native_approval: false` | 선행 nurse/cosplay 연구 맥락 뷰는 도메인별 제안 구조다. 새 마법소녀 맥락 뷰를 검색에 연결하려면 소비자와 계약을 별도로 구현·검증해야 한다. |
| 비교·검증 보고 | 총 원문 행/원자/열린 항목·관련/무관/보류, 후보 고유 ID·행별 비교·RID 검토 수, 소스/뷰/인덱스 해시·검증 일시 | 301행 모두에 값이 있다는 사실을 상세 근거/후보 전수 검증 완료로 오인하지 않는다. 각 분모의 의미를 별도로 적는다. |

코퍼스 validator `scripts/photo_candidate_corpus.py`를 직접 확인한 제약은 다음과 같다.

- manifest는 `photo-candidate-corpus-source/v3`이며 각 모듈은 `schema`와 해당 kind 하나만 가진다. 파일은 assets 바로 아래 `.json`, 동일 모듈 중복이나 assets 밖 경로는 실패한다. 같은 후보·바인딩 ID의 소유자 중복도 실패한다.
- 후보 원본은 정확히 `id`, `record_kind`, `content`, `conditions`, `effects`, `provenance` 필드를 가진다. ID는 `cand_`와 소문자 16진수 32자리다. `content` 안에 별도 `id` 또는 최상위 효과·조건의 중복 소유 필드를 넣지 않는다. provenance는 적어도 하나의 출처 문자열과 SHA-256이 필요하다.
- 효과는 `dimensions`, `properties`, 선택적 `realizations`이고 각 property는 정확히 dimension/target/property와 소유자를 갖는다. 분기 모드는 `one` 또는 `optional`이고 분기 ID·조건·효과가 독립적이다. `optional`만 base가 존재하며 다른 대안의 구성요소나 소유자를 합치지 않는다. 기존 candidate ID와 동일하다는 이유만으로 다른 RID를 하나의 명제로 취급하지 않는다.
- 바인딩은 정확히 `id`, `candidate_id`, `slot_id`, `role`, `semantic_role`, `conditions`, `weight`를 갖고 정본 슬롯의 semantic role과 일치해야 한다. 바인딩 조건은 `subject_applicability`, 선택적으로 `native_guards`를 사용하며 candidate의 intrinsic 조건이나 효과를 재정의할 수 없다. 효과의 충돌 또는 소유자 허가를 슬롯에 넣어 우회할 수 없다.
- ID와 record digest는 다르다. `photo_candidate_retrieval_views.digest()`는 JSON 객체를 `ensure_ascii=False`, `sort_keys=True`, `separators=(',', ':')`, `allow_nan=False`로 정규화한 UTF-8 바이트의 SHA-256이다. 파일의 원시 바이트 SHA-256과 구별해 기록한다. 본문 해시만 일치해도 자연어 번역과 용어 의미의 정확성이 자동 입증되지는 않는다.

## 7. 뷰 생성·검증의 상세 연결

현재 `photo_candidate_retrieval_views.py`는 저자가 만든 뷰를 검증하고 임베딩 입력을 구성하는 라이브러리다. `photo_prepare_reviewed_views.py`는 새 뷰 **작성기**가 아니라 입력으로 받은 뷰에 과거 검토 뷰·오버레이를 재생하고 버전 전환을 검증하는 도구다. 현재 이 둘이 원자 레지스트리에서 자동으로 한영 뷰를 창작·검증해 준다는 근거는 없다. 별도 저작 또는 신설 작성기와 사람/에이전트의 의미 검토가 필요하다.

검색 뷰의 각 행은 `id=view_id(cid,rid,key)`, `candidate_id`, 실제 `realization_id`, 비어 있지 않은 `key`, `kind` (`whole`, `context`, `relation`), `source_record_sha256`, 비어 있지 않은 `text_en`/`text_ko`, 적어도 하나의 `source_quotes`를 갖는다. 인용 pointer는 원본 `/content/` 아래 실제 문자열이어야 하고 인용은 그 문자열의 부분 문자열이어야 한다. `/content/realization_content/<RID>/...` 인용은 동일 RID에서만 가져온다. 진단에는 양성 뷰를 붙일 수 없고, 실제 양성 `(CID,RID)`별 whole 뷰는 정확히 하나여야 한다. 여기서 검사하는 것은 연결과 문구 일치이며 원문의 전체 사실성이나 native 승인, 성인 조건·효과 허가에 대한 심사는 아니다.

`photo_candidate_retrieval_views.documents()`는 명시된 문서 집합을 실제 양성 CID/RID 집합과 정확히 비교하고 `English: ...`와 `Korean: ...`를 임베딩한다. 그 후 `canonical_bindings()`는 별도 generation의 검증된 canonical API로 source snapshot·같은 RID의 primary literal과 출처 인용을 다시 결합한다. 연결 실패를 ID 재해싱으로 숨기지 않는다. view별 점수는 CID/RID별 최대값으로 합쳐지지만 뷰 수가 많은 항목이 선택될 기회가 많다는 편향은 남는다.

향후 staged 후보·뷰가 완성됐을 때 전체 모집단 기준으로 실행할 수 있는 실제 검증 호출 예시는 다음과 같다. 경로는 staged 파일을 가리키도록 바꾸며, **실행하지 않은 예시**다.

```sh
# 준비된 뷰의 모든 positive CID/RID가 정확히 whole 뷰 하나를 갖는지 확인
STAGED_ASSETS=/absolute/staged-assets PREPARED_VIEWS=/absolute/prepared-views.json python3 - <<'PY'
import json, os, sys
sys.path.insert(0, 'skills/photo-prompt-image-generator/scripts')
import photo_candidate_corpus as corpus
import photo_candidate_retrieval_views as views
records = corpus.load(os.environ['STAGED_ASSETS'])['candidates']
with open(os.environ['PREPARED_VIEWS'], encoding='utf-8') as f:
    module = json.load(f)
views.validate(module, records, require_complete=True)
docs = sorted(cid + '|' + rid for cid, rec in records.items()
              if rec['record_kind'] != 'diagnostic'
              for rid in views.realization_ids(rec))
print('positive_realizations', len(docs), 'dense_view_rows', len(views.documents(module, records, docs)))
PY

# 별도 일러스트 네 자산을 실제 런타임 로더로 확인(읽기 전용)
python3 - <<'PY'
import sys
sys.path.insert(0, 'skills/subculture-illustration-image-generator/scripts')
import universal_scene_runtime as u
assets = u.load_universal_scene_assets()
print('candidate_count', len(assets.candidate_by_id))
print('asset_hashes', dict(assets.asset_hashes))
PY
```

첫 예시는 **전체 staged corpus가 전체 뷰 범위인 경우에만** 유효하다. 개별 주제 부분 모듈은 `require_complete=False`로 자체 참조를 확인할 수 있지만, 이 성공은 전체 인덱스 coverage를 뜻하지 않는다. 최종 릴리스에서는 실제 인덱스 모집단·뷰와 사전 검토된 원본 집합을 정확히 일치시켜야 한다. `--output`은 신규 경로여야 하며 기존 파일은 덮어쓰지 않는다.

일러스트 loader는 `illustration_universal_scene_candidates_v1.json`, `illustration_universal_compatibility_graph_v1.json`, `illustration_universal_semantic_bindings_v1.json`, `research_evidence_universal_scene/manifest.json`의 실제 파일 바이트 해시와 상호 참조를 검증한다. 2026-11-07 이 읽기 전용 loader는 현재 파일에서 통과했고 후보 127개를 반환했다. 마법소녀 원자별 적용성이나 픽셀 적합성을 검증한 것은 아니다. `illustration_topic_crosswalk_v1.json`은 `illustration_runtime.py`의 별도 로더·계약이므로 네 파일 loader 성공에 포함되지 않는다.

## 8. 단계별 중단 조건

| 단계 | 중단하고 수정·보류해야 하는 조건 |
|---|---|
| 원문·원자 분해 | 301개 행/순서/ID 충돌, 원문 인용 불일치, 묶음의 한 의미 누락, 근거 없이 확정된 번역·연상·창작 구성 |
| 외부 근거 | 원문에 대한 직접 지지 범위가 불명확, 접근 실패를 본문 확인으로 표기, 작품 한 사례를 보편 정의로 확대, 다중 개념 중 한쪽만 확인하고 전체를 완료 처리 |
| 후보 대조 | 후보 모듈/record SHA 변경, 읽지 않은 RID·activation·guard·소유자·효과·바인딩을 미기록, 검색 0건을 부재로 판정, 11,134개 문자열 단서를 의미상 전수 후보로 간주 |
| 연구·양성 분류 | 서사·시간을 정지 이미지 사실로 강제, 진단을 양성 검색으로 변환, 고유명에서 일반 범주로 무단 전파, 원문이 요구하지 않은 성인·색·소유자·옷·폭력을 추가 |
| 신규 corpus | 후보/바인딩 ID 중복, provenance 누락, 유효하지 않은 intrinsic condition·효과 또는 미존재 슬롯·참조, 기존 조건을 바인딩으로 약화, 동일 ID 서로 다른 원문 |
| 뷰·인덱스 | 원본 해시·인용·RID 또는 한영 문장 누락, 양성 realization whole 뷰 부재/중복, 연구 전용 뷰가 native 권한을 갖는 것으로 처리, 소스 변경 또는 모집단/embedding recipe 불일치 |
| 릴리스 | 다중 뷰 빌드 경로 미구현, 변경된 manifest와 봉인 입력 불일치, 병행 작업 누락, 비활성 세대 검증 실패, 현재 포인터/이전 복구 세대 미확인 |
| 결과 판정 | 검색 단독 성공을 이미지 개선으로 기재, 숨은 접점·재질·시간을 가시적 성공으로 판정, 일부 검토를 전체 완료로 표기, 사용자 수용을 추론 |

## 9. 검토 중 확인된 수정 경계와 반영 순서

다음 항목은 **수정 제안과 검증 과제**다. 원문·기존 후보를 지금 자동 변경했다는 뜻이 아니다.

1. `MG-08-014`의 트레인은 복식의 길게 이어지는 부분이라는 역할과 부착 위치를 분리한다. 어깨에 부착된 Watteau train도 있으므로 ‘어깨에서 내려오면 망토이고 트레인이 아니다’라는 배타 규칙은 만들지 않는다. `MG-11-011`도 타로 내부의 슈트와 일반 놀이패의 무늬가 겹칠 수 있어 판본·무늬 체계로 구분한다. `MG-13-3-005`는 파손된 소품의 가시 상태와 기능 상실을 별도 사실로 기록한다. 상세 출처·적용 범위는 행별 원장에 있다.
2. `MG-16-014` 관련 `cand_674574747ce55333965815e6471e7853`의 `for_any: [human, adult]`를 `human AND adult`로 읽지 않는다. 후보의 조건·검색 태그·바인딩 조건과 별도 프로필/상위 런타임 가드를 각각 확인하며, 이 후보의 현행 런타임 노출이나 최종 가드 통과는 미검증이다. 특정 맥락에 성인 조건이 필수라면 태그나 OR 조건으로 대체하지 말고 현재 계약에서 검증 가능한 별도 명시 요구로 다룬다.
3. `cand_4c3d7e3dbd2d5d11afe8ad78202bb529`는 검토 기록상 본문이 일반 주름치마인데 효과에는 knife pleats가 기재되어 있다. 구현 전 실제 정본·적용 경로를 다시 대조하되 사용자 지시의 **동일 대상 최대 3회**를 넘기지 않는다. 요청이 일반 주름이라면 더 좁은 주름 종류를 묵시적으로 추가하지 않는 테스트를 둔다. 비교 기록은 해당 후보를 찾은 에이전트 파일과 행별 원장에 보존한다.
4. 후보별 `full_record`는 개별 기록자가 원문·중첩 활성화·계약·바인딩을 직접 비교했다는 뜻으로만 쓴다. `core_proposition_only`는 핵심 명제 기반의 부분 판정이며, 원본 전체 복사·정규화 해시·기계적 바인딩 일치만으로 승격하지 않는다. 과거 검토 횟수를 정확히 복원할 수 없는 항목은 3회 미만이라고 가정하지 않고 기존 자료로 판단하거나 보류한다.
5. 소스–후보 판정이 끝난 원자만 데이터 패치로 묶는다. 우선 의미의 관계·소유·가림과 조건·효과의 불일치를 해소하고, 그다음 독립된 선택 후보, 연구 맥락 뷰와 진단을 각각 작성한다. 각 원자에서 **해당 없음 / 정확 범위의 기존 후보 / 부분 사례 / 신규 제안 / 맥락 전용 / 검증 보류** 중 하나와 이유를 남기며, 미검토는 어느 결과에도 포함하지 않는다.
