# 다섯 독립 프롬프트와 검증 결과

2026-10-07 · 합성 무작위 주제. 다섯 사례의 실제 프롬프트 감사·요청 의미·양방향 연결·현재성 검사와 최종 도구 검증 모두 PASS. 작품 판단은 텍스트 수준의 PARTIAL이며 이미지 픽셀·사용자 수용은 미검증이다. 실제 케이스는 lexical 검색으로 실행했다.

각 에이전트는 독립 venv·skill·runtime·출력 폴더에서 DATA 접근 전 baseline/core를 동결했다. 초기 실패와 기술적 schema 사본을 보존했으며 같은 의미로 수정 세대에서 재실행했다. 마지막 관리 도구 방어 수정은 별도 복사본으로 재검증했다.

| 사례 | 무작위 요청 | 감사 | 의미 | 연결 | 현재성 | 최종 도구 |
|---|---|---|---|---|---|---|
| 01 | 야외 공연을 앞두고 바닷바람 속에서 활을 확인하는 성인 첼리스트의 사진. | PASS | PASS | PASS | PASS | PASS |
| 02 | 오래된 구리 주전자와 접힌 리넨을 이른 아침 자연광으로 찍은 사진. 사람은 없음. | PASS | PASS | PASS | PASS | PASS |
| 03 | 숲속 폭포의 물보라를 뒤에서 비추는 아침 햇빛의 사진. 사람은 없음. | PASS | PASS | PASS | PASS | PASS |
| 04 | 겨울 저녁 작은 기차역 플랫폼의 지붕과 빗물 자국을 찍은 사진. 사람은 없음. | PASS | PASS | PASS | PASS | PASS |
| 05 | 마른 솔방울의 비늘 틈과 거친 표면을 낮은 옆빛으로 찍은 접사 사진. 사람은 없음. | PASS | PASS | PASS | PASS | PASS |

모든 사례는 전체 2,971개 명시적 edge를 원본에서 독립 재계산했다. 정상 현재 조회는 성공하고 손상 보고서·다른 root는 거부됐다. 최초 첼리스트 감사는 잘못 적용된 연주 의무 4개로 FAIL이었으며 동일한 baseline을 보존한 정비 후 PASS다.

일부 기존 advisory에는 인물 전제나 열린 차원 밖 제안이 남아 있고 모두 미채택이다. 관리 기능의 정확성과 전체 후보의 의미 품질을 구분한다. 주전자 문장에는 반사광/확산광 소유의 모호함이 남아 작품 판단을 부분 검토로 기록했다.

## 사례 01

야외 공연을 앞두고 바닷바람 속에서 활을 확인하는 성인 첼리스트의 사진.

Pack `59035d64155e621b` · [평가](qa/case-01/final/QA-REPORT.md) · [기계 결과](qa/case-01/final/QA-RESULT.json) · [최종 도구 검증](qa/case-01/final/FINAL-TOOL-VERIFICATION.json)

```text
A photograph of an adult cellist checking a cello bow before an outdoor performance on a small wooden stage beside the sea. The cellist is seated on a plain chair, with both feet set apart on the deck. The cello rests upright between their knees, its endpin planted in a rubber stop. They hold the bow horizontally at waist height in front of the cello. Their right thumb and forefinger pause at the frog's adjustment screw while the left hand supports the wooden stick near its balance point; their gaze follows the narrow, evenly stretched ribbon of hair beneath the stick. The sea breeze lifts loose hair at their temple and pulls a dark shirt cuff away from the wrist, while their shoulders stay settled and their mouth is softly set in concentration. Two waiting chairs and a music stand with clipped sheet music sit farther along the stage, making this small preparation feel close to the first note. Soft coastal daylight grazes the cheek and open collar, with a gentle glint along the bow hair and warm amber reflections in the cello. Compose a quiet environmental portrait that keeps the seated figure, both hands, the entire bow, and the instrument's point of support readable, with the pale water receding behind them. The fine, steady line of the bow carries attention against the moving hair and cloth.
```

## 사례 02

오래된 구리 주전자와 접힌 리넨을 이른 아침 자연광으로 찍은 사진. 사람은 없음.

Pack `5439f63faea1192b` · [평가](qa/case-02/final/QA-REPORT.md) · [기계 결과](qa/case-02/final/QA-RESULT.json) · [최종 도구 검증](qa/case-02/final/FINAL-TOOL-VERIFICATION.json)

```text
An object-only still-life photograph of an old copper kettle beside a length of linen that lies folded, lit by natural light in the early morning. Both rest on a pale stone windowsill. The kettle's curved flank carries small rubbed patches and darkened seams; the linen's stacked folds reveal a coarse, dry weave. A soft window reflection runs along the copper curve and falls across the upper fold, making the metal's rounded volume answer the fabric's flat layers. The kettle holds the visual center, with a small interval of stone separating it from the linen. Cool, quiet shadows remain readable against a plain, dim interior background, while the warm copper and off-white cloth retain their natural colors.
```

## 사례 03

숲속 폭포의 물보라를 뒤에서 비추는 아침 햇빛의 사진. 사람은 없음.

Pack `498635d44f1e8731` · [평가](qa/case-03/final/QA-REPORT.md) · [기계 결과](qa/case-03/final/QA-RESULT.json) · [최종 도구 검증](qa/case-03/final/FINAL-TOOL-VERIFICATION.json)

```text
A photograph of the spray at a forest waterfall, illuminated by morning sunlight shining from behind the spray. Falling water breaks against the pool, sending a drifting veil of fine droplets into the air. Light catches the airborne droplets, giving their edges a pale gold brightness against deep green woodland shadow. The cascade remains clearly visible beside this luminous cloud, with ripples spreading from its impact across the darker pool. Enclosing trees establish the forest around the water, their trunks and leaves receding into shade. Dark, water-polished rock and small patches of moss sit close to the falling water. A balanced landscape frame gives the illuminated spray the strongest visual presence while retaining its connection to the cascade and pool. The water has crisp, irregular detail, and brightness rolls gently into the surrounding natural shadows.
```

## 사례 04

겨울 저녁 작은 기차역 플랫폼의 지붕과 빗물 자국을 찍은 사진. 사람은 없음.

Pack `a997327a635ba1dd` · [평가](qa/case-04/final/QA-REPORT.md) · [기계 결과](qa/case-04/final/QA-RESULT.json) · [최종 도구 검증](qa/case-04/final/FINAL-TOOL-VERIFICATION.json)

```text
An architectural photograph of the roof canopy of a small railway station platform on a winter evening. The roof and its rainwater stains are the main subject: dark, uneven runoff streaks descend along the fascia and spread beneath the roof seams, with pale dried tide lines edging the dampened patches. The canopy occupies most of the frame, while a narrow strip of platform paving, one supporting post, and the parallel rails establish its modest station setting. A single warm platform lamp draws out the overlapping stain edges and the slight roughness of the roof surface against the cold blue-gray dusk. The platform is empty, its paving carrying a subdued wet glimmer. Preserve the quiet difference between a working shelter's straight structure and the irregular water traces that have accumulated on it. Natural tonal transitions and legible surface texture make the photograph feel observed and still, with the surrounding station kept subordinate to the stained roof.
```

## 사례 05

마른 솔방울의 비늘 틈과 거친 표면을 낮은 옆빛으로 찍은 접사 사진. 사람은 없음.

Pack `fa51ab9b7be0e977` · [평가](qa/case-05/final/QA-REPORT.md) · [기계 결과](qa/case-05/final/QA-RESULT.json) · [최종 도구 검증](qa/case-05/final/FINAL-TOOL-VERIFICATION.json)

```text
A macro photograph of a pine cone centers on the gaps between its scales and their rough woody surfaces. The scales are dry, with fibrous ridges and slightly chipped edges interrupting their repeated pattern. Low side light grazes across the scale relief, bringing raised ridges into brightness while the crevices hold narrow shadows. A close crop lets the overlapping scales form an irregular layered rhythm. The central cluster is crisply resolved; neighboring layers soften gently enough to retain their shapes. The cone rests against a plain charcoal-brown background. Muted russet and umber tones keep attention on the transition from illuminated surface to shaded gap.
```
