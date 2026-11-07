# 코스프레 시각 의미와 구현 상태

조사와 적용 범위는 로컬 연구 문서 `docs/research/cosplay-visual-semantics-research-plan-20261106.md` 및 `docs/research-evidence/photo-prompt/cosplay-20261106/`에 기록한다. 해당 `docs/`는 Git 무시 경로여서 다른 체크아웃에 없을 수 있다.

이번 모듈은 의상·갑옷·헤어·분장·착용 파츠·소품 접점·포즈·표정에 대한 선택적 시각 명제 48개와 별도 진단 15개를 제공한다. `photo_cosplay_semantics_20261106.json`, `photo_candidate_cosplay_20261106.json`, `photo_candidate_cosplay_bindings_20261106.json`, `photo_candidate_retrieval_views_cosplay_20261106.json`으로 구분한다. 각 후보는 하나의 완전한 선택적 명제이며 한영 뷰는 원본 문장·해시·출처 포인터를 보존한다. 진단은 양성 검색 물질이 아니다. 슬롯이나 뷰는 선택 권한, 신체·의복 소유자, 효과 허가 또는 픽셀 적합성을 보장하지 않는다.

문서의 356개 원문 행은 조사 인벤토리의 범위이지 신규 후보 356개가 아니다. 모든 행을 제한된 후보 대조로 검토했지만 이는 코퍼스 전체의 완전한 중복 제거를 뜻하지 않는다. 추가 출처 검증은 미완료다. 특히 원작 관계·제작 공정·팬덤 활동과 같은 비시각적 의미를 시각 후보로 자동 변환하지 않는다.

코스프레, 패션, 촬영 장르, 성인용 표시, 고어, 재질·제작 방식, 배역·인물·성별은 구별한다. 외형만으로 실제 나이·정체성·동의·의도·재료 조성·사건 원인을 확정하지 않는다. 필요한 접점이나 부분이 가려지면 관찰되지 않은 상태로 기록한다. 검색 노출, 실제 프롬프트 반영, 이미지 관찰과 인과적 개선은 서로 다른 단계다.
# Follow-up comparison and review (2026-11-07)

`photo_cosplay_semantics_20261106.json` preserves the 356 rows and Korean
descriptions from the referenced ChatGPT conversation. These are secondary
research, not independently authenticated definitions. The inventory records
which examples are related. Three independent reviews cover all 356 rows:
57 have an existing realization, 192 a partial example, 63 diagnostic context,
and 44 insufficient evidence. These are bounded judgments, not exhaustive
corpus-wide equivalence; a lexical hit is not semantic equivalence.

`photo_cosplay_existing_review_20261107.json` records inspected existing
candidate examples with their own conditions, effects and bindings. A candidate
can illustrate only part of a term and may require a specific subject or scene;
the original source contract remains authoritative. The supplementary module
adds authored, optional visual examples and corresponding source-quoted context
views. It is not a definition or exhaustive realization for each source term.
The companion semantic registry records deliberately excluded overlaps. The
supplement adds 56 positive optional examples and 44 unverified glossary
diagnostics; diagnostics never enter positive retrieval. Full review snapshots
are retained separately from the current source hashes and bindings. The 356
`photo_cosplay_research_context_views_20261107.json` views quote the source
registry for research use; they are not H-F2 positive retrieval views or native
candidate selectors.

For further refinement of partial and insufficient rows, inspect the exact source definition and
every plausible multilingual search lead rather than approving lexical matches.
Record the candidate's full proposition, applicability, effects and slot
binding; distinguish a reusable complete candidate from an example, a partial
diagnostic boundary, and no established match. Where a term denotes production
history, identity, material composition or community context, preserve it as
context unless an independently specified observable realization is justified.
Only then add or reuse positive candidates and quote-preserving views, rebuild
the complete installed index, and run regression retrieval and pixel reviews.
The current count of related examples is not a count of fully deduplicated terms.

Managed pixel reviews of the three existing images were recovered using
self-reported source paths and exact image hashes, with the old preview-only
observations preserved. These audits do not authenticate provider responses or
establish that new data caused an improvement. See `photo-workflow.md` for the
reconciliation boundary.
