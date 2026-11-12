# 츤데레 조사 맥락 조회

대화 원문의 24개 표 346행은 `assets/photo_tsundere_semantics_20261112.json`과 `assets/photo_tsundere_research_context_views_20261112.json`에 보존한다. 별도 의미 레지스트리의 행별 의미, 구체적 가시성, 시간과 매체 한계 및 좁은 후보 연결을 확인한다. 사용자 제공 대화의 진술과 관련 검색 예시는 독립 출처 검증이나 동의어 승인이 아니다. 복합 68행의 210개 구성요소는 `assets/photo_tsundere_compound_senses_20261112.json`에 별도 보존한다. 현재 작업 원본 후보·조건·효과·바인딩과의 제한적 행별 대조 및 미해결 상태는 `assets/photo_tsundere_candidate_reconciliation_20261112.json`에 보존한다. 이 분해는 동의어 확정이나 개별 외부 근거 및 후보 전수 대조를 뜻하지 않는다.

독립적 초안과 core 동결 후 연구가 필요할 때만 별도 조회할 수 있다.

```sh
.venv/bin/python skills/photo-prompt-image-generator/scripts/photo_tsundere_context_search.py 'ツンしゅん'
.venv/bin/python skills/photo-prompt-image-generator/scripts/photo_tsundere_context_search.py '브랫' --adult-context
.venv/bin/python skills/photo-prompt-image-generator/scripts/photo_tsundere_context_search.py '勘違いしないで' --include-prose
```

표 밖 본문 70개 문단·제목과 명시적으로 추출한 표현은 `assets/photo_tsundere_prose_context_20261112.json`에 보존하며 `--include-prose`로 별도 검색한다. 표현 추출이 본문의 모든 개별 의미를 검증했다는 뜻은 아니다.

위 명령은 관리형 검색과 별개의 메모리 내 BM25F다. 통합 H-F2 세대는 원문 표 346행과 본문·추출 표현 91행을 관리형 `research_contexts`의 출처 결합 어휘 인덱스로 제공한다. 기존 페티시 맥락 28행도 복구했으며 두 맥락은 후보 순위나 채택 자격을 변경하지 않는다. 새 맥락은 명시적 츤데레 표지 또는 인정된 원문 표현이 있을 때만 반환하므로 관련 자유문 질의를 놓칠 수 있다. 성인·부정 표현의 인식도 규칙 기반으로 모든 문장을 포괄하지 않는다. 일반 복식이나 모호한 단어에서 성인 취향을 유추하지 않기 위해 별도 표시된 성인 맥락은 명시적인 성인 맥락 질의 또는 `--adult-context`에서만 제공한다. 이 제한된 인식은 모든 문맥을 이해한다는 뜻이 아니다. 결과는 후보 발행, 프롬프트 채택, 이미지 요구, native 자격 또는 픽셀 성공을 부여하지 않는다. Core에 확정된 사용자 의미와 소유자/차원 제한을 우선하고, 이름이나 표정·의상에서 나이·성별·관계·성적 취향·동의를 추정하지 않는다. 한 프레임으로 장기적 성격이나 숨은 의도와 과거를 증명하지 않는다.

원문 보존·조회 시험 및 최신 인덱스 반영 상태는 이번 조사 기록 `docs/research-evidence/photo-prompt/tsundere-20261112/`을 참조한다. `docs/`는 Git에서 제외될 수 있다. 자산에 포함된 모든 원문 셀과 source hash는 자료의 출처를 기록하며 원문에서 제시된 주장 자체가 사실임을 보증하지 않는다.


## 109행 후속 검토

`assets/photo_tsundere_109_reviewed_proposals_20261112.json`은 기존 후보 미연결 109행의 원문, 의미, 매체 요구 및 관찰 한계를 행별로 기록한다. 그중 15개는 선택적 부분 정지 이미지 후보로 작성했고 나머지 94개는 연구용 검토 항목으로 유지한다. 언어·시간·내면을 단일 이미지 후보가 증명한다고 취급하지 않는다. 각 맥락 뷰는 검토 항목의 해시와 경계를 포함하며 검색 결과 역시 참고 정보에 한정된다.

## 로컬 검색본 복원

후보·뷰·맥락 원본은 Git에 포함되지만 임베딩 모델과 봉인된 검색본은 포함되지 않는다. 2026-11-12에 검증한 H-F2 세대 `4a36bb7f8085e17e446c29c8dea60c74330556033c933a8f58720f309bf8c45c`와 대응 native 세대 `7eaddf7a06bfb7239f6373e1076a7bdcd29c6c08a825b1904ad966a40e913cde`의 로컬 복원 사본은 저장소 상위의 `../image-prompt-runtime-backups/tsundere-20261112/store/`에 보관한다. 이 사본은 별도로 전달해야 하며 같은 디스크에 있으므로 장애 대비 백업이 아니다. [로컬 임베딩 설치](local-embeddings.md) 후 저장소 루트에서 아래 명령으로 검증·설치한다. `--no-activate`를 더하면 활성 선택자는 바꾸지 않는다.

```sh
python3 skills/photo-prompt-image-generator/scripts/install_photo_h_f2_runtime.py \
  --source-store ../image-prompt-runtime-backups/tsundere-20261112/store \
  --generation-id 4a36bb7f8085e17e446c29c8dea60c74330556033c933a8f58720f309bf8c45c
```

이 세대의 검색·맥락 검증은 이미지 개선의 증거가 아니다. Git을 내려받는 것만으로 별도 저장소의 인덱스와 모델이 자동 설치되지는 않는다.
