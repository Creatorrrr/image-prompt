# 전체 문맥의 부분 native 검증 배치

이 배치는 현재 연구 source102 전체 18,250개 ID와 149개 catalog, 모든 기존 binding·정책·참조를 유지한다. 루트가 이미 수용한 정확한 77개 proof와 그 162개 역할 관계만 별도로 연결한다. 영구 binding을 추가하지 않는다. 전체 18,250건/pending0 채택 조건을 변경하거나 expected_count=77로 우회하지 않는다. 운영 원본·catalog139·자격0·운영 pointer는 이 배치의 쓰기 대상이 아니다.

소비자는 이미 검증된 `50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839` generation의 정확한 코드 바이트를 사용한다. 모델은 기존 설치된 로컬 EmbeddingGemma2 공간만 사용하며 그 설치 lock과 worker 코드가 generation과 같은지 검사한다. 새 다운로드, 외부 API, Gemini, 외부 의미 심사는 사용하지 않는다.

아래 명령은 저장소 루트에서 실행했다. 산출물은 불변 증거이므로 이미 존재하는 결과를 덮어쓰지 않는다. 재실행은 새로운 배치 디렉터리에서 같은 검토 입력을 명시적으로 고정하여 수행한다.

```bash
R=docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014
env -i HOME=/Users/chasoik PATH=/opt/homebrew/bin:/usr/bin:/bin \
  PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
  PYTHONPATH=/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/.runtime/embedding-python/lib/python3.14/site-packages \
  PHOTO_EMBEDDING_BACKEND=embeddinggemma2-local \
  /usr/bin/sandbox-exec -f "$R/batch-validation-01/deny-network.sb" \
  /opt/homebrew/opt/python@3.14/bin/python3.14 "$R/batch-validation-01/run.py" prepare

env -i HOME=/Users/chasoik PATH=/opt/homebrew/bin:/usr/bin:/bin \
  PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
  PYTHONPATH=/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/.runtime/embedding-python/lib/python3.14/site-packages \
  PHOTO_EMBEDDING_BACKEND=embeddinggemma2-local \
  /usr/bin/sandbox-exec -f "$R/batch-validation-01/deny-network.sb" \
  /opt/homebrew/opt/python@3.14/bin/python3.14 "$R/batch-validation-01/run.py" build

env -i HOME=/Users/chasoik PATH=/opt/homebrew/bin:/usr/bin:/bin \
  PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
  PYTHONPATH=/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/.runtime/embedding-python/lib/python3.14/site-packages \
  PHOTO_EMBEDDING_BACKEND=embeddinggemma2-local \
  PHOTO_RUNTIME_STORE=/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/batch-validation-01/research-runtime-store \
  /usr/bin/sandbox-exec -f "$R/batch-validation-01/deny-network.sb" \
  /opt/homebrew/opt/python@3.14/bin/python3.14 "$R/batch-validation-01/run.py" consume
```

처리 경로는 `native_reviews.verify_batch` → `verify_acceptance` → CID별 전체 after/closure/binding 일치 → 전체 컨테이너 `photo_candidate_corpus.validate` → `offline_vector_map`의 동일 공간/ID/본문/recipe/실행증거 재사용 → 변경 문서만 local `embed_many` → `photo_search_layout.build/verify` → 전용 `SnapshotPublisher.publish` → `RuntimeSnapshotProvider.acquire` → `photo_role_proposals.propose` → `photo_slot_queries.prepare` → `generate_candidate_pack` → 실제 `receipt/from_receipt` → `audit_composed_prompt`다.

후속 CID도 같은 기존 API를 쓴다. 먼저 별도 assignment/batch/note에 대한 직접 의미 심사와 루트 수용을 완료한 뒤, 최신 전체 source/catalog와 각 CID의 after/참조 closure가 일치하는 새 명시 inventory를 만든다. 새 불변 배치에서 그 inventory와 source/catalog hash·예상 승인 수를 정확히 고정하여 동일 경로를 실행한다. 기존 proof·역사 catalog·초안을 최신 승인으로 자동 전환하지 않는다. 승인되지 않은 binding 조건·weight는 만들지 않는다. 최종 전수 완료 후에만 기존 `native_reviews.verify_latest` 및 `native_adoption.build_preview_v2`의 전체 18,250/pending0 경로를 사용한다.

수록한 blue-cup 입력은 기존 동결 평가 fixture다. baseline을 유지하고 optional 후보를 모두 거절하는 구성은 실제 검색·issued receipt·독립 replay·구성 감사 경로의 건전성만 증명한다. 승인77개의 전원 실제 채택, 역할별 의미 정확도, 최종 이미지·시각 품질, 운영 적용 또는 5~8단계 완료를 인증하지 않는다. native 직접 채택 검사는 정확한 기존 P/PR/core/owner 선택을 재사용하거나 루트의 새 구체 판단을 받은 별도 사례에서 수행해야 한다.

이번에는 루트가 `native6220-proposal-04`의 여섯 complete JSON을 직접 읽고, 기존 전체 이미지·image_A 역할/존재/종류·별개 other_A·연속 윤곽/읽을 수 있는 세부 두 보존 조건을 수용한 뒤 한 건의 native 채택도 실행했다. 루트 메시지와 여섯 파일의 정확한 SHA는 그 폴더의 `ROOT-CORE-REVIEW.json`에 있다. `adopt_6220.py`가 기존 연구 generation에서 실제 image_detail hybrid 검색·정식 public pack·실제 issued receipt/replay를 수행했다. 6220은 BM25F 4위/local cosine 1위/RRF 1위로 표준 두 후보 안에 제시됐다. 후보 강제 삽입은 없다.

최초 `native6220-adoption-01` 구성 감사는 전체 이미지 관계의 `relation_evidence` 누락으로 거부했다. `repair_6220_compose.py`는 같은 root-approved 문구를 그 관계의 literal 증거로 추가하여 02에 보존했다. 루트의 후속 전체 읽기에서 부정확하게 재사용한 cup 설명을 발견해, `correct_6220_rationale.py`가 요청한 clarification rationale 한 필드만 수정한 03을 별도로 감사한다. 모든 이전 실패·정정은 보존한다. 최종 prompt/core/pack/receipt/선택/실제 효과·소유자·P·PR는 설명 정정으로 바뀌지 않는다. 최종 근거는 **03의 COMPOSE-AUDIT/VERIFICATION**이며, `status=pass`와 `quality_status=warn`을 구별한다. 시각적 proposition과 uncovered-intent 경고는 이미지·미적 품질 성공을 뜻하지 않는다.

이후 선택된 source24는 이 source102 체크포인트와 다르다. `SOURCE24-INCREMENTAL-PLAN.json`은 실제 14개 kind만 복원된 차이와 기존 18,198개 동일 공간 벡터 재사용·새 문서 14개 local 추론 계획을 기록한다. 해당 증분 index·새 generation은 아직 실행하지 않았다. core/catalog/controls/space/실행증거가 같으면 기존 질의 벡터를 정확히 재검증해 재사용할 수 있지만, 전체 18,212개 positive의 DF/field-length/포스팅·guard를 다시 만들고 새 source에 대한 실제 검색/pack/receipt를 발급해야 한다. source102 receipt를 새 source 증거로 고쳐 부르지 않는다.

파생 전체 index·runtime generation·model cache는 이 폴더 안에 보존하지만 Git에서 제외한다. source 압축본, 승인 역할 대장, 실제 embedding/query 실행증거, 발급 receipt, consumer 결과와 코드 pin은 검토 가능한 증빙이다. 이를 통과했다고 의미 진실성이나 운영 자격을 새로 부여하지 않는다.
