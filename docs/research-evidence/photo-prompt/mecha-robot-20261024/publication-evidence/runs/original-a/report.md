# Arm A — 착용형 로봇 장비 / 옥상 온실 수리

생성·저장·검토를 완료했다. **일반 메카 주제는 보이지만, 새 데이터의 실제 노출/반영 증명과 전체 기계 연결 경로 검사는 통과하지 못했다.**

| 단계 | 결과 | 근거 |
|---|---|---|
| 독립 기본 작성 | 고정 완료, 작성 한계 있음 | seed `41ca8a5e5e26bf3515fe6ced64bd0e62`; 다른 arm 입력 없음. 두 앵커의 착용형/현장 작업 단어는 agent staging을 과도하게 고정한 한계로 별도 기록. |
| 새 데이터 노출 | FAIL | 4개 질의, 32 반환 항목 / 28 고유 소스 중 새 CID 0. 기본 프롬프트 질의의 상위 32개 창에 G01이 있었지만 고정 8개 표본에서 빠짐. 재검색/재표본 없음. |
| 새 데이터 채택 | 입증 불가 | 새 소스 CID/RID 없음. 28개 전체 소스와 4개 완성형 대안 비교 후 기본 장면 유지, 32개 material decision 모두 skip. |
| 구성·전송 | PASS | 프롬프트·참고 이미지 해시 감사 통과. 후보가 덮지 않은 의미 5개는 작성된 문구로 보존된다는 품질 경고만 있음. |
| 생성 | SUCCESS | 내장 image_gen 1회, 원본 참고 JPEG 실제 첨부. PNG 1024×1536, 작업 폴더 복사본·원장·매니페스트 생성. 관측 모델명 없음. |
| 일반 메카 주제 | 가시 | 흰색 상완 커프, 원형 팔꿈치, 전완 하우징, 하네스와 작업용 문손잡이 접촉. |
| 전체 연결 경로 | FAIL / partial | 어깨 하네스 뿌리부터 상완 장치까지의 연결 경로가 어깨·옷·팔 윤곽에 가림. 양 끝이 따로 보이는 것만으로 연결을 통과시키지 않음. |
| 관리형 픽셀 검토 | 유효 기록 / 기술 FAIL | 5개 embodiment gate 중 4 pass, visibility_and_projection fail. 기록 감사 PASS와 픽셀 기술 판정 FAIL은 별개. |
| 사용자 수락 | pending | 직접 요청자의 수락/거절을 아직 받지 않음. |

프롬프트: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/mecha-20261024-arm-a/prompt_en.txt`

이미지: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/mecha-20261024-arm-a/result.png`

이미지 SHA256: `5dbe0d6625d36a39438a63674a1b5287117fd396fa7fb9c5a6a0f63ab8ab0b2c`

프롬프트/런타임 SHA256: `dc956e16b2febc9f89d9120fce415eb56fada780d0d4e9403924e04da7e0a8c5`

원장 run ID `23686135e6dc0d04`, pack `cd2146acdf77c2c9`. H-F2 `e1a3d0cb7623488dfbfff9f0b8337200cef8c0142248414c0a0f4b890faecc71`, native `e51d43e44abad75550a4213b3de14028697c1470dc1c42a31b895029886b32ea`에 고정했다.

참고 사진의 어두운 단발, 앞머리, 어두운 눈과 부드러운 얼굴 외형은 유사하게 남았지만, 근접 원본과 전신 결과의 차이가 있고 개인의 신원이나 성격을 검증하지 않는다. 출력은 밝은 온실의 작업 인물사진으로 읽힌다. 피부·천·기계 표면과 두 손의 작업 접점은 구체적이다. 시선은 카메라를 향해 실제 힌지 점검 순간보다 작업 인물사진의 인상이 강하고, 폭풍으로 휘어진 문이라는 전후 사정도 픽셀만으로 강하게 확정하지 못한다.

세부 판정은 `pixel-test.json`, `visual-review.json`, `review-audit-output.json`; 노출은 `new-source-exposure.json`; 전체 비교는 `composition-comparison.md`와 `source-comparisons.json`; 작성 한계는 `authoring-limitation.json`; 실행 독립성은 `run_manifest.json`에 남겼다. 실제 토크·동력·하중 성능, 특정 폭풍의 시간 순서, 새 데이터가 이미지를 야기했다는 인과는 주장하지 않는다. commit/push는 하지 않았다.
