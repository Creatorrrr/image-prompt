C 이미지의 기록 검증은 통과했지만 전체 픽셀 조건은 실패했습니다. 지지 손의 손목에서 전완·소매까지 이어지는 경로 일부가 로봇 프레임 뒤에 가려져 `UNOBSERVABLE_NOT_PASS`로 남았습니다. 숨은 변형으로 진단하지 않았고 추가 생성은 하지 않았습니다.

원본 1536×1024에서 로봇의 팔꿈치–노출 프레임–별도 손목, bare mid-frame 지지 접점, 드라이버 끝의 체결점, 받침 접촉은 각각 확인했습니다. 실제 이미지 호출은 built-in imagegen 1회입니다.

- [이미지](/Users/chasoik/Projects/image-prompt/generated/photo-runs/mecha-20261024-repair2-anchored-c/output/mecha-repair2-c.png) — SHA256 `d9290ae4b637e694a8382bfcfc177499425e00b8ae12d62d9834cb36a4d617b8`
- [최종 영문 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/mecha-20261024-repair2-anchored-c/final-prompt.txt) — runtime payload SHA256 `7f47e066ee9ac70723f78562f3647a5ddf51ed3fd644210852a7946c4ac8ef70`; 텍스트 파일은 마지막 줄바꿈이 있어 파일 해시가 별도입니다.
- [생성 전 고정 기준](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/mecha-robot-20261024/repair-round-2/arm-c/pre-generation-testcase.json) — SHA256 `be37fd9f2a2155b4e78ff332b31840370b978b956b9d2c0edc34d661b8cc704e`, 생성 후 변경 없음.
- [직접 픽셀 관찰](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/mecha-robot-20261024/repair-round-2/arm-c/pixel-observations.json)
- [검증 결과](/Users/chasoik/Projects/image-prompt/generated/photo-runs/mecha-20261024-repair2-anchored-c/revisions/9865a210531d4a158240b3f8c3451aa9/review_audit.json) — `record_valid=true`, `technical_qualification=fail`, 사용자 판단 pending.

수정 후 ordinary retrieval 1회에서 4질문×8건=32 occurrence, 중복 제외31개 출처 전체를 읽었습니다. 신규 C08/A12가 실제 노출되었고, A12의 전체 착용 연결 경로를 공존시키는 대안을 포함한 5개 완전한 대안을 원 초안과 비교했습니다. 최종은 원 독립 초안이며 native 선택·신규 출처 픽셀 자격은0입니다. [비교 근거](/Users/chasoik/Projects/image-prompt/generated/photo-runs/mecha-20261024-repair2-anchored-c/composition-comparison.md), [노출 기록](/Users/chasoik/Projects/image-prompt/generated/photo-runs/mecha-20261024-repair2-anchored-c/exposure-report.json).

기존 per-arm ledger의 4341바이트/기존1행은 해시까지 보존했고 정확히1행만 추가했습니다. 새 ledger run은 `b3aef6415cb0d7bc`, 원래 시도 연결은 `921cba5da2392e6d`입니다. [보존 감사](/Users/chasoik/Projects/image-prompt/generated/photo-runs/mecha-20261024-repair2-anchored-c/ledger-prefix.after-audit.json). HEAD는 저장소 문맥일 뿐 dirty skill/kernel 전체를 대표하지 않으며, exact SKILL SHA와 tested data392/native578을 [별도 출처 문맥](/Users/chasoik/Projects/image-prompt/generated/photo-runs/mecha-20261024-repair2-anchored-c/manifest-source-context.json)에 남겼습니다.
