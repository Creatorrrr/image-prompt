# 궁중물 독립 재테스트 A

**결과: 일반 신체 gate 5/5 PASS, R2V01 소매 안감의 제한된 시각 구현 PASS. 장면 전체는 NOT_FULLY_QUALIFIED. 사용자 수용 여부는 pending.**

독립 추첨한 콘셉트는 궁중 부엌 마당에서 상에 올리기 전 청자 그릇을 살피는 여성이다. 기존 이미지의 수리나 개선 전후 비교가 아닌 fresh test다. 사전 baseline은 312단어였고 후보 접근 전에 core/중립 feature 8개/embodiment를 고정했다. 최종 문구는 381단어다. 기본 controls는 sensual 1, fetish 0, creativity 1, surreal 0이다.

## 실제 결과와 경계

- 이미지: [result.png](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-a/result.png) — 1237×1272, SHA `eca7aa5208fe0711e320b01bbeaf9ebf2c3ae29178049ab246b12af18b85c169`
- 생성: builtin image_gen 실제 **1회**, 성공 반환·저장, 재시도 0회. 모델명은 도구 응답에 없어 미관측으로 둔다.
- 실제 첨부: [원본 reference](/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg), 얼굴·머리 외형 guidance. SHA `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`. 텍스트 경로만 적은 참조가 아니다.
- [최종 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-a/final-prompt.txt), [완전한 대안 비교](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-a/composition-comparison.md), [상세 JSON](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-a/arm-report.json).

원본과 리샘플링하지 않은 crop에서 양 소매의 흰 천/색 소매 경계, 되돌아가는 두께 있는 가장자리, 같은 소매에서 안쪽 흰 면이 바깥으로 이어지는 국소 전환을 관찰했다. 이는 **R2V01의 local visible realization**만 통과한다. 전체 내부 봉제 경로, 역사적 복식 전체, 시대·신분·실존 인물은 입증하지 않는다. [소매 pixel 기록](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-a/source-specific-pixel-review.json)과 [crop provenance](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-a/crop-provenance.json)에 좌표와 해시를 남겼다.

두 손과 그릇의 지지는 일관되고 참조의 짧은 보브·가느다란 앞머리·얼굴 인상이 보인다. 다만 눈은 그릇보다 카메라를 향하는 인상이 강해 '몰입한 유약 검사'보다는 그릇을 보여 주는 장면에 가깝다. 전통 마당·격자 문·상차림만으로 궁궐임을 독립 확정할 수는 없다. 그래서 소매 한정 통과를 장면 전체·역사적 진정성·사용자 선호의 통과로 확장하지 않았다. [전체 이미지 관찰](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-a/whole-image-observation.json).

## 데이터 경로와 실행

고정 H2 generation은 `265a75945bda1a1aea3b26ca88e13ab0dcb3139d22ae85197ed2d478ee3f2978`, native generation은 `eeaafc1952af220bd23823e72fcd1b1fadca8048f8ac334e08e7edbb25705d9a`다. 세 slot과 요청 주제/전체 baseline의 **5질의, 40 발생, 34개 원본**을 모두 검토했다. 새 24개 모듈 CID의 **자연 H2 노출은 0회**였다. 최종 소매는 별도로 허용된 **직접 postcore authoritative-source 검토**에서 선택한 R2V01이며, H2 노출 성공으로 보고하지 않는다. 신규 모듈 정확 파일 SHA는 `404aaa211a707f016ff4c066e19f2b34fb331b01df21512468131efe93d1ac4f`다. 두 native chosen 배열은 모두 `[]`, `native_approval=false`를 유지했다.

[직접 검토](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-a/direct-postcore-source-review.json)에서 새 24개 원본을 읽고 소매·노리개·쌍학 흉배의 완전한 대안을 비교했다. [일반 검색 원본 검토](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-a/ordinary-source-reviews.json)는 34개 원본별 실제 조건/효과/비사용 이유를 기록하고, 40개 발생별 결정은 모두 skip이다. 일반 후보의 gallery/service/glaze/glass 완전 대안도 비교했으나 유지하지 않았다.

precore feature 검사, compose audit, runtime audit, managed pixel review audit가 통과했다. compose의 세 경고는 후보가 대신 제공하지 않은 원래 court/woman/palace-life 의미를 작성된 literal evidence로 보존했다는 내용이다. 차단 실패는 없다. native manifest 기록은 처음 누락된 provenance 인자로 거절되어, 실제 skill SHA와 현재 HEAD를 넣어 같은 이미지/operation을 기록했다. 추가 이미지 호출은 없었다.

## 파일과 문자열 해시

- Core canonical: `49fd82452520ef2743ba09776afb85b70baba150a32f8cc98ba1c54ae2726646`
- Core normalized JSON **파일**: `add7f12aa72f26ba62e5314161e7cba1200787ea0e2e5397fafba183479c3a47`
- Frozen baseline **텍스트**: `3070dfd73869ba96345f2e99afe6e6b7436d2bb08f5f39228c865b34faca870b`
- 최종 prompt.txt **파일**: `a7ec068e1cae863d7aa1b354e74181c8eaa4299f03623aa31b0f477e878bb811`
- 줄바꿈을 제외한 최종 **텍스트** 및 정확 runtime prompt: `f275d54e3f555c537bfb528693126fc17e35ed8c3008fa53f94bd8d394b47bf2`
- Ledger: [image_runs.ndjson](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-a/image_runs.ndjson), 1행, run ID `c5cdb5576fa439e0`. [native manifest](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-a/native-manifest.json).
- 모든 안정된 run 파일의 실제 파일 해시: [artifact-file-manifest.json](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-a/artifact-file-manifest.json). 정규화 객체·문자열 해시는 [arm-report.json](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-a/arm-report.json)에 별도 이름으로 보존했다.

사진 비교 baseline 없음. 이전 arm/이전 결과를 이용하지 않았으며, 데이터 변경 전후의 우열이나 전체 궁중 데이터 품질 향상은 이 한 장으로 주장하지 않는다.
