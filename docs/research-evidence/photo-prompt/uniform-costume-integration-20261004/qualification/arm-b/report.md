Arm B는 첫 결과에서 활성 gate 6/7(85.7%), 최초 비행복 keyword 4/5(80%)였고, 허리의 원단 연결이 가려 UNOBSERVABLE이었다. 허용된 가시성 수정 1회 후 같은 gate 7/7(100%), 같은 keyword 5/5(100%)가 PASS다. 첫 실패·원본·판정 기준을 보존했으며 추가 생성은 하지 않았다. 반대편 벨트 고리 전체의 지지는 별도 UNOBSERVABLE 한계로 남았다.

독립 랜덤 컨셉은 비가 그친 격납고 유리 통로에서 성인 가상 모델이 서비스 카트의 흰 리넨 모서리를 고르는 일반 비행복 사진이다. keyword는 비행복, random seed는 792606917928791112다. 일체형 천 의복의 허리 연결, 주머니, 앞지퍼와 서비스 카트의 손동작을 함께 보기 적합해 선택했다. sage 원단, 흰 리넨, brushed metal, 젖은 유리의 재질과 cool window light / warm wall lamp의 관계를 독립 작성했다. 선택은 agent authored 열린 차원이며 user definition이나 required semantic assertion으로 추가하지 않았다. 첨부는 실제 관찰한 dark eyes, wispy fringe, jaw-length dark bob의 얼굴·헤어 참고다.

같은 frozen core/envelope/controls/embodiment review와 최초 pack seed 4123720042059685325로 두 스냅샷을 비교했다. round-1 pack bfd7588a534a725e에서는 새 slot:garment_detail:unif_continuous_coverall_front_closure를 선택했지만 uniform opt-in profile이 노출되지 않아 관련 compiled gate가 0개였다. 노출된 slot:garment_detail:unif_front_belt_rear_dress_zip는 색/의복/뒤여밈 관계가 컨셉에 맞지 않아 거절했다. 최초 연결 실패와 embodiment gate 5개 목록은 round-1에 보존했다.

snapshot-2 pack d441ffa1f2b93970에서는 실제 새 후보 slot:garment_detail:unif_continuous_coverall_front_closure와 visual-concept:uniform_continuous_coverall_front_closure가 반환됐다. 동일 의미를 판단해 선택했으며 profile uniform_continuous_coverall_front_closure의 native gates 2개가 prompt 증거와 함께 실제 컴파일됐다. effective contract SHA256은 33a613f26b3dd537e42485cf2739f66e5eb55c84dedaf247a94d11d7247cff7c다. 기존 데이터 보강 후보의 선택 교집합은 0개다. 비행복 관련 unif_fabric_flight_coverall_zips는 반환되지 않았으므로 그 후보/프로필은 테스트하지 않았다. 전체 66개 변경 후보의 이미지 성공을 이 한 컨셉으로 주장하지 않는다.

| 동일 활성 gate | 첫 native 이미지 | 가시성 수정 이미지 |
|---|---|---|
| embodiment_body_ownership | PASS | PASS |
| embodiment_joint_chain_and_reach | PASS | PASS |
| embodiment_support_and_balance | PASS | PASS |
| embodiment_contact_and_space | PASS | PASS |
| embodiment_visibility_and_projection | PASS | PASS |
| vo_uniform_continuous_coverall_front_closure_1 | UNOBSERVABLE | PASS |
| vo_uniform_continuous_coverall_front_closure_2 | PASS | PASS |

새 후보 → 선택 → opt-in profile → prompt의 서로 다른 component 증거 → compiled native gate 경로가 snapshot-2에서 연결됐다. 첫 prompt는 round-1과 동일한 283단어 bytes였고 구성/runtime 감사는 PASS였다. 첫 이미지에서 벨트와 팔이 허리 연결을 가린 것은 audit 통과로 덮지 않았다. 수정에서는 열린 wardrobe.belt.closure_state / wardrobe.details.waist_visibility만 whitelist로 허용했다. 앞 벨트 끝 사이의 작은 틈으로 중앙 원단과 지퍼가 바지 앞판까지 이어져 같은 의복의 연결이 읽혔다. 수정의 구성/runtime 감사도 PASS이며 362단어 advisory budget 경고가 남아 있다.

원본 이미지, keyword 검사와 평가 문구는 각 attempt에 별도 보존했다. 최초 keyword 5개는 일체형 연결·앞지퍼·utility pockets·waist belt·원단/색 경계다. 장면/참고 검사는 두 이미지 각각 4/4 PASS다. 수정 fidelity는 3/4 PASS이고 반대편 belt-loop 전체 지지는 팔 뒤에 가려 UNOBSERVABLE이다. 실제 identity, 원본 사람의 나이, 공식 항공사/기관 복장, 사용자 취향이나 대표 결과 수용은 평가하지 않았다. requesting-user judgment는 pending이다.

native built-in 생성은 첫 호출과 수정 1회, 총 2회이며 CLI/API fallback은 없었다. [첫 원본 이미지 1237×1271](/Users/chasoik/Projects/image-prompt/outputs/uniform-costume-qualification-20261004/arm-b/round-2/image-1.png), [수정 원본 이미지 1237×1272](/Users/chasoik/Projects/image-prompt/outputs/uniform-costume-qualification-20261004/arm-b/repair-1/image-2.png)를 byte-identical로 보존했다. 첫 SHA256은 0d831f789e2fefe90b0409de842fd0dbdc38e87babb4fb282d307a8489dd9330, 수정 SHA256은 80baedf8cdbf7d88253d8f473603fddead1ab53a32c25c21ff3ac0b9a4f45e91다. 첫 run_id는 4dbe4bbcfc679a89, 수정 run_id는 cbd5375991338575다.

source snapshot SHA256은 round-1 02e5df6ed3c5b322e57465a94e08bacd90819d2ae557e287abe33eef91d2e607, round-2 96a091df35acbb54aac8faf95c56f073325d5dba899c0bef6dbb0489adb85df4다. final preservation audit에서 frozen precore 9개, 첫 증거 13개, snapshot-2 source 141개 및 최초 testcase의 해시가 모두 일치했다. 다른 arm의 결과를 읽거나 공유 데이터/코드/공용 ledger를 수정하지 않았다.

상세 기록: [최초 결과 보고](/Users/chasoik/Projects/image-prompt/outputs/uniform-costume-qualification-20261004/arm-b/round-2/report.md), [수정 결과 보고](/Users/chasoik/Projects/image-prompt/outputs/uniform-costume-qualification-20261004/arm-b/repair-1/report.md), [후보 propagation](/Users/chasoik/Projects/image-prompt/outputs/uniform-costume-qualification-20261004/arm-b/round-2/retrieval-propagation.json), [최초 pixel review](/Users/chasoik/Projects/image-prompt/outputs/uniform-costume-qualification-20261004/arm-b/round-2/pixel-review.json), [수정 pixel review](/Users/chasoik/Projects/image-prompt/outputs/uniform-costume-qualification-20261004/arm-b/repair-1/pixel-review.json), [최초 prompt](/Users/chasoik/Projects/image-prompt/outputs/uniform-costume-qualification-20261004/arm-b/round-2/prompt_en.txt), [수정 prompt](/Users/chasoik/Projects/image-prompt/outputs/uniform-costume-qualification-20261004/arm-b/repair-1/prompt_en.txt), [arm-local image_runs.ndjson](/Users/chasoik/Projects/image-prompt/outputs/uniform-costume-qualification-20261004/arm-b/image_runs.ndjson), [검증 범위 ledger](/Users/chasoik/Projects/image-prompt/outputs/uniform-costume-qualification-20261004/arm-b/run_verification.ndjson), [보존 감사](/Users/chasoik/Projects/image-prompt/outputs/uniform-costume-qualification-20261004/arm-b/final-preservation-audit.json).
