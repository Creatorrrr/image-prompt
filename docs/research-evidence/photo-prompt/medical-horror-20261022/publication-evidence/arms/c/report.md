# Medical horror C arm 결과

**전체 판정: PARTIAL.** 실제 이미지 1회 생성·저장과 원본 픽셀 검토를 완료했다. 표본/용기/액면/서리 대비와 참조 외형은 구현되었으나, 저자가 지정한 좌우 손 동작이 반전되었다. 새 A08 자료는 현미경·라벨 슬라이드 랙·별도 표본 용기로 운반되었지만 현미경의 작업대 지지점이 가려져 완전 관계는 부분 실현이다. 사용자 수용은 pending이다.

- Run: /Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-c-image-v2
- Image: /Users/chasoik/Projects/image-prompt/generated/photo-runs/medical-horror-20261022-arm-c-image-v2/rendered/cryobank-thaw-anomaly.png
- Image SHA256: a12f026f0e52f71c85188ba0e56cac884f74805def9a965e1cc4ee7a212e7c46
- 크기: 1237 × 1272
- Tool: built-in image_gen.imagegen, 실제 호출 1회, 자동 재생성/다른 provider/CLI 호출 0회. 도구가 반환한 구체 로컬 파일을 복사했고 원본과 바이트 동일하다. 실제 이미지 모델명은 도구가 제공하지 않아 unknown이다.
- Final prompt: final-prompt.txt; audited composition: composed-corrected.json.

## 동결 및 실행 증거

- 독립 무작위 콘셉트: 다른 표본은 서리로 덮인 트레이에서 한 앰풀만 맑은 액체를 드러내는 동결보관실 검사 중단. 신규 데이터를 보기 전에 core를 동결했다.
- 원본 사용자 요청을 그대로 보존했고, 얼굴 비율·짧은 단발만 참조했다. 가상 연구원 역할, 의상, 연령, 자세, 동결보관실과 표본 현상은 사용자 처방이나 실제 인물의 병력/내면이 아니다.
- v1 prompt_only run은 보존하고 coordinator가 공식 init한 image-v2에서 같은 seed/context/저자입력으로 controls→freeze→3슬롯 seal을 재현했다. exact-replay-proof.json의 모든 비교 파일 바이트와 envelope/controls/core/intent-lock 해시가 동일하다.
- Core canonical: 556ece7af758c8c849ea276a1662ac56cf904c1661ff3fcb32ab42d47df66636
- Controls canonical: 3f25c8fa05be207ce67eeaabddd187519484c6f624d065b6f287aeffb017cdac; sensual 1, fetish 0, surreal 0, creativity 1, auto→sensual_led.
- 최초 검색 pinned H-F2 generation: 3ed7d4cd1bacbf4bea873116a5ff51b113e6f9ed5b983889d85f84933fd533b5; 실제 h_f2_binding 동일. native source generation c92dfffe22c45949e950a62e6ad923ccca8816a40f404ef27ad16e8dabe53088.
- 최초 compose 감사는 clarification evidence의 list/string wire 차이로 실패했다. composed-wire-correction.json에 실패와 보정을 보존했고 최종 사진 prompt 바이트는 동일하다. 보정 후 compose PASS, runtime request PASS, authorize limit 1, native plan/started PASS, native-result ledger 기록 완료.
- Ledger: image_runs.ndjson, ledger_run_id b6a702e574df27f0; independent manifest: run_manifest.json.
- Managed visual review는 visual-review.json과 review-audit.output.json에 보존한다. review-audit는 status=pass, record_valid=true, technical_qualification=fail로 실패 기록의 유효성을 확인했다. body/관절/지지/가시성은 pass이고 contact의 좌우 동작 일치는 fail이다. phase=review_record_validated이며 실패를 성공으로 바꾸는 재생성은 하지 않았다.

## 검색 노출과 새 자료 기여

- 5개 검색에서 각각 BM25F 1회와 local_cosine 1회가 실행되었다. concept_tension은 agent query의 “no added impossible physics under surreal 0”를 exclusion-only 제한으로 읽은 projection 때문에 0개를 반환했다. 데이터 부재로 설명하지 않으며 계획 수정·재검색은 하지 않았다. retrieval-exposure-qualification.json 참조.
- 나머지 4개 검색은 각 8개, 총 32회 query/CID/RID 발생과 30개 고유 원본을 반환했다. 전원본과 모든 발생별 판단은 issued-full-source-reading.json, issued-occurrences.json, source-decisions.full.json, composed h_f2_material_decisions에 있다.
- 신규 photo-medical-horror-visual-semantics/v1 원본 6개가 노출되었다. 12개 완성 대안과 독립 baseline을 같은 creativity 1에서 비교했고 신규 원본 1개를 inspiration_only로 사용했다. qualified native adoption은 0이며 모든 native_approval=false를 보존했다.

| 신규 CID | 원본 주제 | 노출 검색 | 결정 |
|---|---|---|---|
| cand_27f2134beb0d57fb8a2b24c11547a494 | L05 닫힌 생물안전 구역의 장갑 경계 | prop_state | skip |
| cand_120d83e19c8b5b28ad998007bba7d7dc | L06 가상 생물과 숙주 사이의 단일 접점 | __request_topic__ | skip |
| cand_b02903be03575c7bab86382c46a2b667 | A03 격리 경계의 문·유리·전실 | __request_topic__ | skip |
| cand_c0dde54a6cbf589785dbcafbd284fcac | A08 현미경 작업대와 슬라이드 트레이 | __request_topic__, __baseline_prompt__ | inspiration_only |
| cand_6ec311e081c256239949646a57a6b768 | L09 서로 다른 코드가 붙은 같은 외형의 시료 | __baseline_prompt__ | skip |
| cand_6eb1553fb8385fed86246f53255bac35 | D13 슬라이드·커버글라스·조직 절편 | __baseline_prompt__ | skip |

반영된 최종 literal:

> On the right side of the same laboratory bench, a compact microscope stands beside a rack of glass slides with small paper end labels; the sealed specimen ampoule is a separate container in front of them.

선택의 의미: 보조 현미경과 라벨 슬라이드 랙을 통해 검사실 맥락을 구체화했다. 표본 앰풀과 슬라이드는 별개 소유자로 유지되며 병리 진단, 사람 조직 기원, 유전적 상태를 주장하지 않는다.

**실제 픽셀 운반: PARTIAL.** 현미경의 접안부·대물렌즈·스테이지, 라벨이 있는 유리 슬라이드를 담은 랙, 독립적인 중앙 앰풀은 보인다. 현미경의 받침/발과 작업대 지지점은 우측 가장자리 및 슬라이드 랙 뒤에 가려졌다. 따라서 full source의 모든 지지 endpoint가 보이는 것으로 처리하지 않고 source complete gate를 fail/observability=partial로 남겼다. source-contribution-gates.review.json 참조.

## 동결 사전 픽셀 기준

| 기준 | 판정 | 주요 관찰 |
|---|---|---|
| C_REFERENCE | PASS | 얼굴 비율·짧은 검은 단발·성긴 앞머리의 외형 연속성 |
| C_SPECIMEN_CONTAINER | PASS | 닫힌 유리 앰풀 안의 옅은 접힌 표본과 앰버 액체 |
| C_LIQUID_SURFACE | PASS | 수평 액면과 headspace, 그 아래의 표본 |
| C_SINGLE_ANOMALY | PASS | 맑은 앰풀 하나와 여러 서리 이웃의 같은 프레임 대비 |
| C_BOUNDED_MOISTURE | PASS | 액체 내부와 구분되는 유리 어깨의 방울 및 젖은 바닥 흔적 |
| C_HUMAN_SAMPLE_RELATION | FAIL | 손-팔 연결·공극·지지는 보이나 actor 좌우 동작 반전 |
| C_CLINICAL_UNEASE | PASS | 동결보관실 질서·단일 표본 이상·멈춘 검사 관계 |

6 PASS / 1 FAIL이며 전체 gate conjunction은 FAIL, 실험 결과 요약은 PARTIAL이다. 판독 불가나 일부 가시성을 PASS로 올리지 않았다. 자세 실패는 실제 해부학적 기형 판정이 아니라 작성된 좌우 동작과의 불일치다. 원래 사전 7개 기준 파일은 수정하지 않았다.

## 장르·미감·한계

첫 픽셀 독해는 first-pixel-reading.md, 전체 미감/controls 검토는 artistic-review.md에 있다. 얼굴→멈춘 장갑→앰플의 시각 흐름과 차가운 서리/앰버 액체의 대비는 강하다. 메디컬 맥락과 조용한 임상적 불안은 읽히지만, 강렬한 호러보다 정제된 검사실 서스펜스에 가깝다. 도구 metadata나 prompt의 장르 라벨을 실제 공포 강도의 증거로 삼지 않았다.

스틸 이미지는 실제 온도, 해동 이력, 배양 생존, 병원체, 감염, 진단, 유전적 기원, 실제 인물의 신원·내면을 입증하지 않는다. 생성된 -80°C 디스플레이와 슬라이드 식별자는 원본 데이터의 측정값이 아니다. 거절한 D13의 조직 절편/커버글라스 계약은 보라색 slide 무늬가 나타났다는 이유로 사후 채택하지 않았다.

이 run은 새 자료 등록 전체의 품질, 모든 의료 호러 검색의 recall, 반복 생성의 성공률 또는 사용자 선호를 일반화하지 않는다. 원본/스킬/다른 arm/공유 runtime pointer는 수정하지 않았고 commit/push도 하지 않았다.
