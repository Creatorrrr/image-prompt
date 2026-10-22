# A arm 결과: PARTIAL

독립 랜덤 콘셉트는 **퇴원은 처리됐지만 나갈 수 없는 기록 창구**다. 빈 봉투를 돌려받은 인물과 유리 너머 남겨진 차트, 빗장으로 닫힌 출구를 한 화면에서 시험했다.

![A arm 이미지](/Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-a-image-v2/generated-image.png)

| 구분 | 결과 | 확인한 범위 |
| --- | --- | --- |
| 독립 코어·설정 보존 | PASS | 공식 image-v2 전환 뒤 envelope/core/controls/intent-lock 해시 동일 |
| 검색 세대 고정 | PASS | H-F2 `3ed7d4cd1bacbf4bea873116a5ff51b113e6f9ed5b983889d85f84933fd533b5` |
| 원본 자료 검토 | PASS | 5질의, 29고유 자료, 32발생별 결정; 새 메디컬 호러 자료 7개 노출 |
| 새 데이터의 이미지 운반 | NOT_ADOPTED | 새 자료 0개 채택; 최종 literal·픽셀 기여 없음 |
| 프롬프트·전송 감사 | PASS | 실패 없음; authored 의미 보존 관련 품질 경고 3개 |
| 생성·보존 | PASS | built-in image_gen.imagegen 정확히 1회; 1536×1024; 복사본과 원본 바이트 동일 |
| managed 픽셀 검토 | VALID / qualification FAIL | 5 hard gate 중 3 pass, 2 fail; record_valid=true |
| 사전 관계·외형 기준 | 5 PASS | 얼굴·단발 참고, 임상 공간, 봉투/유리/차트, 출구 빗장, 실제 손 연결 |
| 장르·미감 | PARTIAL | 임상적·제도적 서스펜스는 읽히나 강한 호러 인상은 덜함 |
| 사용자 수용 | PENDING | 실제 사용자 평가를 받지 않음 |

실제 실패는 봉투 아래쪽이 카운터에 닿지 않고 손에 들린 채 떠 있다는 점이다. 예정한 지지·접촉 관계가 빠졌으므로 hard gate 2개를 실패로 기록했다. 팔과 손 자체의 연결·도달 범위는 자연스럽다. 좌우 손 배치는 최종 프롬프트와 뒤바뀐 것으로 보이며 별도 지시 충실도 결함으로 남겼다. 고정 사전 기준은 변경하지 않았다.

키워드를 제외하고 장면을 읽으면, 짧은 머리의 인물이 빈 투명 봉투를 들고 병원 기록 창구로 몸을 기울인다. 유리 너머에는 비슷한 얼굴 사진이 붙은 파일이 있으며, 바로 뒤 EXIT에는 문 이음새를 가로지르는 빗장이 보인다. 밝은 병원 조명과 큰 얼굴 비중 때문에 공포보다 행정적 장벽과 불안이 먼저 읽힌다. 이는 프롬프트를 작성했던 저자의 질적 관찰이며 독립 블라인드 실험이나 사용자 선호 판정은 아니다.

새 자료의 전체 조건을 읽고 7개의 완전한 비교안을 작성했다. 치과 기구·병리 작업대·배양 플라스크·두 문 전실은 별도 처치나 공간 체계를 추가해 기록 교환의 초점을 흐렸다. 성인 팔뚝 전용 프레임·대형 화면의 얼굴 가림·침상 난간과 호출기는 성인 전제 또는 이 장면의 참조·가시성 범위와 맞지 않았다. 출처를 부분 차용하거나 native_approval=false 자료를 qualified 채택으로 보고하지 않았다. 채택하지 않았으므로 이 이미지는 새 데이터가 이미지 품질을 높였다는 인과 증거가 아니다.

재현·검토 파일은 모두 이 보고서와 같은 폴더에 있다.

- 최종 프롬프트: `composed.json`의 정확한 prompt_en, 읽기용 `final-prompt.txt`
- 자료 결정: `full-source-review.json`, `composition-comparison.md`, `new-data-exposure.occurrences.json`
- 픽셀 판정: `pixel-testcase.result.json`, `visual-review.json`, `review-audit.stdout.json`
- 장르·미감·컨트롤 관찰: `supplemental-artistic-review.json`
- 보존·독립 실행: `native-image-save-proof.json`, `image_runs.ndjson`, `run_manifest.json`
- 전체 요약: `arm-a-result-summary.json`

이미지 SHA-256: `e1b9524e088e2d4e944f0ae0c5a3eb32cde4644d3f00e38f1d8af8b5f94d59f6`. 원장 run ID: `6194cfd695c234ed`. 대체 provider·자동 재생성·공유 소스 수정·커밋·푸시는 하지 않았다. 원본 사진의 실제 병력·내면·동의·나이는 추정하지 않았으며 얼굴과 짧은 머리만 외형 단서로 사용했다.
