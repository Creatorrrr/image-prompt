# C 테스트케이스: 비 뒤 첫 배를 기다리는 접힌 항로

독립 난수 seed는 `7825148642666662853`이다. 첨부 참조의 보이는 얼굴·짧은 검은 머리만 사용하여, 비 뒤 선착장에서 시간표의 종이 모서리를 다시 고정하는 현재 순간을 구성했다. 장면, 의상, 소품, 카메라와 구체 기하는 authorial 선택이며 사용자 lock이 아니다. 원문 envelope와 frozen core는 그대로 유지했다.

| 검증 층 | 결과 |
| --- | --- |
| Immutable READY generation/receipt | 정확히 일치 |
| Composed / native runtime 감사 | PASS / PASS |
| Native image_gen 실제 호출 / ledger 행 | 1 / 1 |
| 기존 선택 원피스 계약 | 5/5 관찰 PASS |
| Embodiment 계약 | 3/5 PASS, 2 FAIL |
| 정확한 effective hard union | 8/10, 기술 자격 FAIL |
| 신규 bundle 보충 all-of | 10/10 관찰 PASS |
| 신규 spring 프로필 hard activation | 미노출·미검증, 승격 없음 |
| 원래 사용자 의미 4 anchor | 4/4 관찰 PASS |
| 기존 authorial 보충 관찰 | 4/9 PASS |
| 사용자 판단 | not_yet_received |

신규 선택은 `bundle:spf_sf071_1_bundle`(원본 슬롯 `spf_sf071_1`)과 `bundle:spf_sf107_02_bundle`(원본 슬롯 `spf_sf107_02`)이다. 앞판의 두 어깨끈 연결과 별도 블라우스 앞에 놓이는 층, 각 신발의 발등 스트랩 및 자기 신발의 반대편 두 끝 고정을 생성 전에 4 component + 6 directed relation 표로 고정했다. 양쪽 신발을 따로 관찰했고 partial/unobservable은 실패로 처리했다. 이 10개 보충 항목은 runtime `hard_gates`에 넣지 않았다. `spring_sf071_1`, `spring_sf107_02` 프로필은 별도 opt-in이 노출되지 않아 hard activation을 주장하지 않는다.

별도로 실제 노출된 기존 `visual-concept:one_piece_dress_construction`을 opt-in했다. Sage 앞판·허리 연결·사선 앞판·플리츠 밑단이 한 벌로 읽히며 원피스의 5개 native/thumbnail 게이트가 통과했다. 실제 exact union은 `exact-hard-gate-checklist.json`에 그대로 기록했다.

실패한 hard gate는 `embodiment_contact_and_space`, `embodiment_visibility_and_projection`이다. 손가락이 종이 모서리의 나무 클립을 잡지만, 같은 클립 턱이 와이어까지 잡는 관계와 그 끝점은 보이지 않는다. 단순히 손과 종이가 보인다는 이유로 전체 접촉을 통과시키지 않았다. 보충 관찰에서 꽃은 블라우스보다 sage 어깨끈에 붙고, 블라우스 대각선 드레이프와 신발에서 발등 X를 거쳐 발목 매듭으로 이어지는 리본 경로도 완전하게 나타나지 않았다.

전체 인상은 조용하고 따뜻한 봄 선착장 사진으로 설득력 있다. 실제 이미지는 보는 사람 쪽으로 향하는 얼굴과 게시판에 붙은 종이로 표현되어, 원래의 돌아오는 배를 향한 반응과 종이·와이어 수선 관계는 약해졌다. 예술적 인상은 기술 자격이나 사용자 수용을 대체하지 않는다.

생성 이미지: [image.png](/Users/chasoik/Projects/image-prompt/generated_images/spring-fashion-ornament-shoe-20261008T213050Z-3d55c278/image.png) — 1024×1536, SHA256 `7f2b1b4c8903a27342d51f49c510b43bd67fc76d6a17f5d03c2cd98adf1e527d`. 도구가 실제 반환한 로컬 파일에서 byte-identical 복사했고 원본은 남겼다.

프롬프트: [prompt.en.txt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/ornament_shoe/prompt.en.txt). 감사된 객체: [composed.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/ornament_shoe/run/revisions/d0d1a653579b46f4acf93bc335afc6b0/composed.json). 최종 결과: [stage2-result.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/ornament_shoe/stage2-result.json). Ledger: [image_runs.ndjson](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/ornament_shoe/image_runs.ndjson). 독립 manifest: [independent-run-manifest.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/ornament_shoe/independent-run-manifest.json). 정식 리뷰: [visual-pixel-review.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/ornament_shoe/visual-pixel-review.json). 신규 topic 리뷰: [new-topic-pixel-review.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/ornament_shoe/new-topic-pixel-review.json).

Runtime generation은 `a7fd58162695c7c23a9257ac89b13434e94e6899fc3891858b837636ad1ced6c`, source fingerprint는 `6d92970bf0f1f1acb3cf20b2ac5262a357f61f89b4dd03b1ede39945b77d1b8a`이다. 추가 재생성, API/CLI fallback, 다른 arm 입력, shared asset/index 수정은 수행하지 않았다. 이미지 검토용 crop/thumbnail은 arm 안에 별도로 두었고 최종 원본 픽셀은 변경하지 않았다.
