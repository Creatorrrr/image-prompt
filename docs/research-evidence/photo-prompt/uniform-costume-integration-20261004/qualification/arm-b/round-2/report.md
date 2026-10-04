첫 native 결과는 완전 통과하지 않았다. 활성 gate 6/7(85.7%), 최초 비행복 검사 4/5(80%)가 PASS이고, 허리에서 바지통으로 이어지는 원단 연결은 벨트와 팔에 가려 UNOBSERVABLE이다. strict audit는 이를 fail로 처리한다.

독립 컨셉은 비가 그친 격납고 유리 통로에서 성인 가상 모델이 서비스 카트의 흰 리넨 모서리를 고르는 일반 비행복 사진이다. 무작위 시드 792606917928791112에서 비행복을 선택했다. 의복·장소·작은 행동·빛은 agent authored 선택이며 사용자 정의나 required assertion을 만들지 않았다. 첨부는 얼굴과 단발머리의 관찰 가능한 특징에만 사용했다.

같은 frozen core와 최초 pack seed 4123720042059685325로 비교했다. round-1에서 새 후보 unif_continuous_coverall_front_closure는 선택됐으나 uniform opt-in profile이 노출되지 않아 제복 gate는 0개였다. snapshot-2에서는 같은 후보와 visual-concept:uniform_continuous_coverall_front_closure가 반환됐고, 이 프로필을 선택하자 native gate 2개가 실제 컴파일됐다. 원래 컨셉과 영어 prompt bytes는 그대로였다. 비행복용 unif_fabric_flight_coverall_zips는 반환되지 않았으며 해당 프로필의 성공을 주장하지 않는다.

| 실제 활성 gate | 첫 이미지 판정 |
|---|---|
| embodiment_body_ownership | PASS |
| embodiment_joint_chain_and_reach | PASS |
| embodiment_support_and_balance | PASS |
| embodiment_contact_and_space | PASS |
| embodiment_visibility_and_projection | PASS |
| vo_uniform_continuous_coverall_front_closure_1 | UNOBSERVABLE |
| vo_uniform_continuous_coverall_front_closure_2 | PASS |

숨은 연결은 변형이 있다고 진단한 것이 아니다. 넓은 허리벨트가 가운데 연결 구간을 덮고 양팔도 측면을 가리므로, 같은 색의 상의와 하의가 보인다는 사실만으로 원단의 물리적 연속을 증명할 수 없다. 중앙 앞지퍼는 별도 경계와 슬라이더가 읽히고 모델의 바깥 의복 앞판에 속한다. 오른손은 리넨 모서리를 집고 다른 손은 카트 난간에 닿으며, 두 발과 카트 바퀴의 지지가 같은 프레임에 남아 있다.

최초 supplemental keyword 검사는 일체형 연결 UNOBSERVABLE, 앞지퍼 PASS, 독립 주머니 PASS, 허리벨트 PASS, 원단·색 경계 PASS였다. 참고 얼굴/단발머리, 리넨 접촉, 카트 접촉, 비·혼합광·재질 관계의 scene 검사는 4/4 PASS다. 얼굴 특징 대응은 실제 신원이나 첨부 인물의 연령을 증명하지 않는다. 일반 비행복 스타일은 읽히지만 공식 항공사/기관 복장이나 실제 항공기 조작 역할을 입증하지 않는다.

이미지 생성은 built-in image_gen.imagegen 1회였다. [원본 1237×1271 PNG](/Users/chasoik/Projects/image-prompt/outputs/uniform-costume-qualification-20261004/arm-b/round-2/image-1.png)의 SHA256은 0d831f789e2fefe90b0409de842fd0dbdc38e87babb4fb282d307a8489dd9330이며 native 파일을 byte-identical로 복사했다. CLI/API fallback, 이미지 크기 변경, 픽셀 편집은 하지 않았다.

구성 감사와 실제 runtime 입력 감사는 PASS였다. 이는 prompt/참조/hash binding의 통과이고 pixel 성공이 아니다. pixel-review audit는 schema failure 없이 required gate 1개 미통과로 failed_technical_hard_gates다. 원본 이미지와 최초 검사 기준을 바꾸지 않았고 사용자 취향/수용 판단은 아직 받지 않았다.

기록은 [pixel-review.json](/Users/chasoik/Projects/image-prompt/outputs/uniform-costume-qualification-20261004/arm-b/round-2/pixel-review.json), [pixel-review-audit.json](/Users/chasoik/Projects/image-prompt/outputs/uniform-costume-qualification-20261004/arm-b/round-2/pixel-review-audit.json), [영어 프롬프트](/Users/chasoik/Projects/image-prompt/outputs/uniform-costume-qualification-20261004/arm-b/round-2/prompt_en.txt), [propagation 기록](/Users/chasoik/Projects/image-prompt/outputs/uniform-costume-qualification-20261004/arm-b/round-2/retrieval-propagation.json), [arm-local ledger](/Users/chasoik/Projects/image-prompt/outputs/uniform-costume-qualification-20261004/arm-b/image_runs.ndjson)에 보존했다.
