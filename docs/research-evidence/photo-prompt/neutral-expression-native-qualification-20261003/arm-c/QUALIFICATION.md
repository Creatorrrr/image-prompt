# Arm C native qualification

독립 SystemRandom 추첨으로 **도심 시장 위 옥상 판화 작업실**의 종이등 상승 사건을 선택했다. 인물은 명시적 29세 성인으로 작성했으며, 첨부 사진은 보이는 얼굴·머리 외관 참고로만 사용했다. 키워드의 뜻은 arm C가 만든 합성 시험 조건이며 실제 사용자가 표정·감정·피부·체형을 정의했다고 기록하지 않았다.

최종 프롬프트 316단어, normal V6 pack `01a784154620dc0e`, 실제 `image_gen.imagegen` 호출 **1회**로 1237×1272 이미지 한 장을 저장했다. 초기 동결 파일 16개의 해시는 끝까지 유지했고 다른 arm의 출력은 읽지 않았다.

- [Standalone prompt](prompt_en.txt), [negative](negative_en.txt), [saved image](generated_image.png)
- [Candidate pack](candidate_pack.json), [composition](composed_prompt.json), [choices/provenance](choices_and_provenance.json)
- [Runtime request](native_render_request.json), [runtime audit](native_request_audit.json)
- [Frozen 6-gate pixel review](independent_pixel_review.json), [native crops](native_inspection_crops.json)
- [Hard-gate review](render_review.json), [hard-gate audit](render_review_audit.json)
- [Per-arm ledger](image_runs.ndjson), [independent V2 run manifest](run_manifest.json)

| 동결 시험 기준 | native 관찰 | 판정 |
| --- | --- | --- |
| 얼굴·머리 및 원래 비율 | dark bob/wispy fringe와 참고 얼굴 외관을 유지하며 눈·입술의 임의 확대 없이 충분한 얼굴 디테일을 보인다. | PASS |
| side-eye의 현재 방향 | 두 눈은 거의 정면인 얼굴을 기준으로 인물 왼쪽/화면 오른쪽 위의 종이등으로 향한다. 내면 판단은 추론하지 않는다. | PASS |
| pouty lips의 현재 동작 | 위·아래 입술의 작은 둥근 전방 돌출과 중앙으로 모인 입 양끝이 함께 보인다. 원래 볼륨으로 대체하지 않는다. | PASS |
| smooth의 피부 대상 | 뺨의 국부 표면이 균일한 빛 전이를 이루며 native crop에 미세 피부결이 남아 있다. | PASS |
| supple의 가죽 대상 | 왼손 엄지가 가죽 입구에 닿아 안쪽으로 굽힌 현재 상태와 넓은 부드러운 주름을 보인다. | PASS |
| smooth의 도자기 대상 | 오른손의 단단한 타원형 도자기는 연속 유약 표면과 반사광을 보이며 피부결·가죽 주름과 구별된다. | PASS |

`partial_is_fail=true`로 판정했다. 선택한 `ne_current_lip_protrusion`의 2개 gate, `pe_texture_preserving_tone_evening_relation`의 2개 gate, 5개 embodiment gate도 같은 저장 이미지에서 모두 PASS다. ordinary `pv_side_eye` 후보는 인물의 현재 눈 방향으로 채택했다. `supple`을 사람의 피부나 신체 부위로 잘못 연결하지 않았으며, 사진 한 장으로 복원성·반복 탄성·전체 재료 거동을 검증했다고 주장하지 않는다.

Feature validator는 warning 없이 통과했고 composed/runtime audit는 PASS다. render review audit는 `technical_qualified=true`, `failed_hard_gates=[]`, `schema_failures=[]`이다. 해당 audit의 exit 1은 사용자 미적 판단이 아직 pending이라 대표 사례 승격을 허용하지 않는다는 뜻이다. 사용자 수락은 요청하지도 대신 판정하지도 않았다.

전체 장면의 미적 관찰은 촉각적인 비교 순간과 종이등·판화·시장 환경이 연결된 가까운 초상이다. 저장 결과는 작성한 vertical 방향보다 정사각형에 가깝고, 도자기는 열린 손바닥 아래 지지보다 앞·아래를 감싼 grip으로 보인다. 가죽 아랫면은 낡고 비교적 두껍게 읽히지만 윗 입구의 굽힘은 관찰된다. 이 관찰은 별도 supplemental 기록이며 새 보편 gate나 사용자 선호로 승격하지 않았다.

이미지 SHA-256: `b8b891274df9caab05ae5bfbb5501d85dfbb58f78617736f1675d7a5f42b02c7`

소스 snapshot은 operational manifest `b328c2ef332fd71978d320f1e9a77bd863428c0eaa51ba97fad9c0d38878b17e`에 연결했다. 92개 운영 입력 해시가 일치했으며 source dictionary는 `0620af2ed2904452df6cf761e1f1825a527777f08720dc82bd760f92e501d83e`, registry는 `c97a2c827498fa299a9b5d8ea0d2ade31143e3084cc858d8183491fe9f6ab834`이다. Normal V6 retrieval provenance는 `core_bm25f`다. Native image model 명칭은 도구가 반환하지 않아 unknown으로 보존했다.
