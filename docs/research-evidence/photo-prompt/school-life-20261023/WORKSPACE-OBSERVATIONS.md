# 공유 작업 트리 변동 관찰

연구의 첫 구조 검증에서는 23/23 항목이 통과했고 보호 대상으로 읽은 212개 파일이 baseline과 같았다. 한영 개발 질의와 관계 endpoint를 보완한 뒤의 최종 검사에서는 구조 검증은 다시 23/23 통과했지만, 아래 기존 파일 6개가 baseline과 달랐다. 관찰 시 HEAD는 baseline과 같았고 보호 파일의 삭제는 없었다.

- `skills/photo-prompt-image-generator/assets/photo_candidate_candidates_000.json`
- `skills/photo-prompt-image-generator/assets/photo_candidate_candidates_002.json`
- `skills/photo-prompt-image-generator/assets/photo_candidate_candidates_006.json`
- `skills/photo-prompt-image-generator/assets/photo_candidate_candidates_010.json`
- `skills/photo-prompt-image-generator/assets/photo_candidate_candidates_013.json`
- `skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json`

이 작업의 쓰기는 새 `school-life-20261023` 연구 폴더에 한정했다. 공유 source의 별도 변동을 연구가 보존에 실패한 것으로 숨기거나, 반대로 최종 source가 처음과 같다고 주장하지 않는다. 다른 변경을 되돌리거나 연구 baseline/corpus snapshot을 새 값으로 덮어쓰지 않았다.

`BASELINE.json`은 baseline 시점, `corpus-snapshot.json`은 그때 실제 읽은 모듈과 전체 기존 CID 10건, `VALIDATION.json`은 마지막 검사 시점의 drift 목록이다. 81모듈·20,341 CID·15,120 binding의 관찰과 재사용 triage는 해당 snapshot에만 해당한다. 후속 구현에서는 최신 manifest/module/설치 세대를 별도 단계 evidence에 고정하고 실제 CID·분기·조건·effects·binding을 다시 심사해야 한다.

최종 상태는 `STRUCTURE_PASS_SOURCE_DRIFT_REQUIRES_REBASELINE`이다. 이는 연구 참조 구조의 통과와 통합 전 재기준화 필요를 함께 표시하며, 실행하지 않은 검색·native·픽셀·설치를 승인하지 않는다. 마지막 검사 후의 추가 공유 변경을 이 문서가 지속 감시하는 것은 아니다.
