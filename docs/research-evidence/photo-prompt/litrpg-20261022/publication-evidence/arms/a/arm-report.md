A 검증을 완료했습니다. 새 설치 세대에 명시적으로 고정하고 독립 난수 콘셉트(seed 10685162680402208503)로 공원 관리원의 개인 체력·기술 재사용 대기 상태가 일상 작업에 개입하는 장면을 구성했습니다. 참고 이미지는 얼굴·머리 외형 가이드로 실제 첨부했습니다.

- built-in image_gen 1회 성공. image.png (1312×1199), 원본 복사 해시 일치. 재시도·대체 API 없음.
- compose/runtime 감사 PASS. 사전 whole-scene 테스트 6개 중 5개 PASS. 개인 level·stamina·skill, 소유 wrist 연결, 시선, 휴식, grounded tool, 미완 뿌리 관계는 같은 장면에서 확인됩니다.
- exact staging FAIL: 본인 기준 오른손이 도구를 잡고 왼팔이 무릎 위에 있습니다. 사전 프롬프트·게이트의 왼손 tool/오른팔 knee와 반대입니다. 해부학 결함으로 진단하지 않으며, 명시된 장면 충실도 실패로 기록합니다. 정규 review audit는 record_valid=true, technical_qualification=fail입니다.
- 반환 30개 distinct source/32 occurrences 전체를 검토하고 6개 완성 대안과 baseline을 비교했습니다. 신규 CID는 노출0/사용0, 오래된 generic depth 자료만 배경 초점 결정에 inspiration_only로 남겼습니다.
- 신규 데이터의 품질 개선 인과는 미입증입니다. 비교 렌더가 없으며 LitRPG 시스템 의미는 검색 전 독립 baseline에 이미 있었습니다. 사용자 수락은 pending입니다.

릴리스: ef02180fc06f390a079ecb7727ece11c2dd30e54394f9e1ae8b9112217bd29ac
최종 프롬프트: final-prompt.txt / 구조화 composed: final.json
사전 게이트: testcase-preimage-final.json
픽셀 판단: litrpg-pixel-review.json / visual-review.json / review-audit-output.json
실행 증거: run_manifest.json / image-runs.ndjson / exposure-and-use.json
