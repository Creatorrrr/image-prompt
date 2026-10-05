세 개의 독립 사전 baseline과 실제 image_gen 도구 인수를 보존한다. 장면은 각 에이전트가 무작위 선택 후 작성한 설명이며 사용자가 직접 쓴 장면으로 취급하지 않는다. 첨부 원본은 모든 호출에서 같은 외형 참고 이미지로 전달했다.

참고 이미지 SHA-256: `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`. DATA manifest SHA-256: `b72b757dfa8491fbb56c3cefb1368e463f8209c35b14aa5c5ce1c18aa54ab054`.


**A: 도자기 공방에서 유약 작업 중 잠깐 쉬는 인물**

seed `274842718384169686176098864896653091728` · 키워드 한쪽 뒤꿈치 들기, 보케, 꽃받침, 윙크 · pack `71b9f180a332682f` · 최종 `PASS`

[사전 동결 testcase](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/qualification/arm-a/testcase.json>) · [실제 요청 envelope](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/qualification/arm-a/request_envelope.json>)

**사전 동결 baseline prompt**

```text
A complex staged portrait in a ceramic atelier shows a human portrait subject, a fictional adult woman with the visible face shape and short dark bob of the supplied photograph. The portrait uses the supplied photograph as a visual reference. She pauses after glazing porcelain for a visible playful pose, inviting the camera with quiet warmth. Standing clear of the workbench, she brings both bare hands below her chin, wrists close together and palms facing upward; the heels of both palms lightly touch the underside of her chin while her fingers fan outward beneath both cheeks like petals. Her bent elbows remain beside her ribs, with both wrists and every finger visible. Her left eyelids meet in a complete wink while her right eye remains clearly open toward the camera, above a small relaxed smile. Her weight rests over the flat right foot; the left heel rises off the tiled floor while the left ball and toes remain planted, both shoes entirely visible. She wears an ochre sleeveless knit vest over an ivory shirt with rolled cuffs and a clay-marked indigo waist apron. Behind her, a scarred wooden bench holds damp porcelain cups on a pale plaster bat and a jade-glaze test tile beside a brush. Frosted window light wraps the face and hands; distant warm shelf lamps dissolve into distinct soft circular bokeh. The portrait frame includes her complete body, ample clear floor beneath the lifted heel, and a focused face-and-hands plane against a softly separated workshop. Use eye-level frontal capture with gently compressed natural perspective, skin pores, knit fibers and damp ceramic sheen.
```


**실제 전송 1 / PASS**

[원본 도구 인수 JSON](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/qualification/arm-a/native_tool_arguments.json>) · SHA-256 `6cae3170fb4d706f52e2887be21aa68936426d05f6dc0a3d6c36dcdd05b64369`

```json
{
  "referenced_image_paths": [
    "/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg"
  ],
  "transparent_background": false
}
```

전송한 prompt 문자열을 그대로 표시한다.

```text
A complex staged portrait in a ceramic atelier shows a human portrait subject, a fictional adult woman with the visible face shape and short dark bob of the supplied photograph. The portrait uses the supplied photograph as a visual reference. She pauses after glazing porcelain for a visible playful pose, inviting the camera with quiet warmth. Standing clear of the workbench, she brings both bare hands below her chin, wrists close together and palms facing upward; the heels of both palms lightly touch the underside of her chin while her fingers fan outward beneath both cheeks like petals. Her bent elbows remain beside her ribs, with both wrists and every finger visible. Her left eyelids meet in a complete wink while her right eye remains clearly open toward the camera, above a small relaxed smile. Her weight rests over the flat right foot; the left heel rises off the tiled floor while the left ball and toes remain planted, both shoes entirely visible. She wears an ochre sleeveless knit vest over an ivory shirt with rolled cuffs and a clay-marked indigo waist apron. Behind her, a scarred wooden bench holds damp porcelain cups on a pale plaster bat and a jade-glaze test tile beside a brush. Frosted window light wraps the face and hands; distant warm shelf lamps dissolve into distinct soft circular bokeh. The portrait frame includes her complete body, ample clear floor beneath the lifted heel, and a focused face-and-hands plane against a softly separated workshop. Use eye-level frontal capture with gently compressed natural perspective, skin pores, knit fibers and damp ceramic sheen.

Avoid: 3d render look, awkward animal anatomy, body distortion, broken facial features, broken window geometry, cartoon style, cgi look, digital illustration, distorted fingers, excessive hdr, fake-looking background, flat collage look, illustration look, impossible perspective, inaccurate reflections, inconsistent shadows, low resolution, obvious cutout edges, over-processed retouching, overly smooth fur, plastic-looking food texture, plastic-looking skin, unmatched lighting, unrealistic hands, unrealistic steam, warped product geometry, warped walls
```

runtime의 별도 negative 원문:

```text
3d render look, awkward animal anatomy, body distortion, broken facial features, broken window geometry, cartoon style, cgi look, digital illustration, distorted fingers, excessive hdr, fake-looking background, flat collage look, illustration look, impossible perspective, inaccurate reflections, inconsistent shadows, low resolution, obvious cutout edges, over-processed retouching, overly smooth fur, plastic-looking food texture, plastic-looking skin, unmatched lighting, unrealistic hands, unrealistic steam, warped product geometry, warped walls
```

[최종 원본 이미지](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/qualification/arm-a/attempt-1-original.png>)

[전체 결과와 원본·감사·ledger 경로](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/qualification/arm-a/RESULT.json>)


**B: 비 온 뒤 계단과 음료 수레가 있는 작은 등불 축제**

seed `7582531431900127391` · 키워드 보케, 고양이 앞발, 윙크, 눈물 고임과 미소, 모에소데 · pack `2239561234f2d260` · 최종 `BLOCKED_UNSCORED`

[사전 동결 testcase](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/qualification/arm-b/testcase.json>) · [실제 요청 envelope](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/qualification/arm-b/request_envelope.json>)

**사전 동결 baseline prompt**

```text
One complex photographic scene presents a reference-guided fictional adult woman in a single visible moment at a tiny neighborhood lantern festival after a brief shower. Use the reference image for the visible face and short dark hair: the softly tapered jaw, dark eyes, broad facial proportions, short dark bob and airy fringe remain recognizable. She sits upright on a broad wet stone step beside a small drink cart, meeting the viewer with a playful, intimate presence. Her elbows are bent close to her ribs and both forearms rise toward her chest; both wrists droop downward and the fingertips curl loosely inward as small human cat-paw gestures. A rust-colored ribbed-knit cardigan over a charcoal scoop-neck top gives her relaxed adult bearing; both long cuffs extend over the bases of the fingers, with curled fingertips emerging clearly. She gives a soft, unmistakable smile, her right eye visibly winking closed while her left eye remains open; a distinct small pool of clear tears visibly gathers along the lower lid of her open left eye. The expression reads as a tender moment of celebration. Behind her, paper lanterns and distant stall lights dissolve into round bokeh while the face and both hands remain sharply readable. A pale cloth canopy slopes above the cart and a thin plume of steam rises beside a metal kettle; wet stone catches warm lantern reflections against cool evening air. A vertical, mid-thigh-up photograph at conversational distance keeps both hands separate from the face, every fingertip contact with its cuff clear, and enough layered festival space around her to connect the close moment to its setting. Warm soft light brushes her cheeks and knit fibers; natural skin texture and quiet color retain the feeling of a real photograph.
```


**실제 전송 1 / BLOCKED_UNSCORED; 원본 이미지 반환 없음**

[원본 도구 인수 JSON](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/qualification/arm-b/native_tool_args.attempt-1.json>) · SHA-256 `26b941564ab60d66de4239b8c159b59d0d5303f4f4dc6964afad57053536dd93`

```json
{
  "referenced_image_paths": [
    "/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg"
  ],
  "transparent_background": false
}
```

전송한 prompt 문자열을 그대로 표시한다.

```text
One complex photographic scene presents a reference-guided fictional adult woman in a single visible moment at a tiny neighborhood lantern festival after a brief shower. Use the reference image for the visible face and short dark hair: the softly tapered jaw, dark eyes, broad facial proportions, short dark bob and airy fringe remain recognizable. She sits upright on a broad wet stone step beside a small drink cart, meeting the viewer with a playful, intimate presence. Her elbows are bent close to her ribs and both forearms rise toward her chest; both wrists droop downward and the fingertips curl loosely inward as small human cat-paw gestures. A rust-colored ribbed-knit cardigan over a charcoal scoop-neck top gives her relaxed adult bearing; both long cuffs extend over the bases of the fingers, with curled fingertips emerging clearly. She gives a soft, unmistakable smile, her right eye visibly winking closed while her left eye remains open; a distinct small pool of clear tears visibly gathers along the lower lid of her open left eye. The expression reads as a tender moment of celebration. Behind her, paper lanterns and distant stall lights dissolve into round bokeh while the face and both hands remain sharply readable. A pale cloth canopy slopes above the cart and a thin plume of steam rises beside a metal kettle; wet stone catches warm lantern reflections against cool evening air. A vertical, mid-thigh-up photograph at conversational distance keeps both hands separate from the face, every fingertip contact with its cuff clear, and enough layered festival space around her to connect the close moment to its setting. Warm soft light brushes her cheeks and knit fibers; natural skin texture and quiet color retain the feeling of a real photograph.

Avoid: 3d render look, awkward animal anatomy, body distortion, broken facial features, broken window geometry, cartoon style, cgi look, digital illustration, distorted fingers, excessive hdr, fake-looking background, flat collage look, illustration look, impossible perspective, inaccurate reflections, inconsistent shadows, low resolution, obvious cutout edges, over-processed retouching, overly smooth fur, plastic-looking food texture, plastic-looking skin, unmatched lighting, unrealistic hands, unrealistic steam, warped product geometry, warped walls
```

runtime의 별도 negative 원문:

```text
3d render look, awkward animal anatomy, body distortion, broken facial features, broken window geometry, cartoon style, cgi look, digital illustration, distorted fingers, excessive hdr, fake-looking background, flat collage look, illustration look, impossible perspective, inaccurate reflections, inconsistent shadows, low resolution, obvious cutout edges, over-processed retouching, overly smooth fur, plastic-looking food texture, plastic-looking skin, unmatched lighting, unrealistic hands, unrealistic steam, warped product geometry, warped walls
```


**실제 전송 2 / BLOCKED_UNSCORED; 원본 이미지 반환 없음**

[원본 도구 인수 JSON](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/qualification/arm-b/native_tool_args.attempt-2.json>) · SHA-256 `26b941564ab60d66de4239b8c159b59d0d5303f4f4dc6964afad57053536dd93`

```json
{
  "referenced_image_paths": [
    "/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg"
  ],
  "transparent_background": false
}
```

전송한 prompt 문자열을 그대로 표시한다.

```text
One complex photographic scene presents a reference-guided fictional adult woman in a single visible moment at a tiny neighborhood lantern festival after a brief shower. Use the reference image for the visible face and short dark hair: the softly tapered jaw, dark eyes, broad facial proportions, short dark bob and airy fringe remain recognizable. She sits upright on a broad wet stone step beside a small drink cart, meeting the viewer with a playful, intimate presence. Her elbows are bent close to her ribs and both forearms rise toward her chest; both wrists droop downward and the fingertips curl loosely inward as small human cat-paw gestures. A rust-colored ribbed-knit cardigan over a charcoal scoop-neck top gives her relaxed adult bearing; both long cuffs extend over the bases of the fingers, with curled fingertips emerging clearly. She gives a soft, unmistakable smile, her right eye visibly winking closed while her left eye remains open; a distinct small pool of clear tears visibly gathers along the lower lid of her open left eye. The expression reads as a tender moment of celebration. Behind her, paper lanterns and distant stall lights dissolve into round bokeh while the face and both hands remain sharply readable. A pale cloth canopy slopes above the cart and a thin plume of steam rises beside a metal kettle; wet stone catches warm lantern reflections against cool evening air. A vertical, mid-thigh-up photograph at conversational distance keeps both hands separate from the face, every fingertip contact with its cuff clear, and enough layered festival space around her to connect the close moment to its setting. Warm soft light brushes her cheeks and knit fibers; natural skin texture and quiet color retain the feeling of a real photograph.

Avoid: 3d render look, awkward animal anatomy, body distortion, broken facial features, broken window geometry, cartoon style, cgi look, digital illustration, distorted fingers, excessive hdr, fake-looking background, flat collage look, illustration look, impossible perspective, inaccurate reflections, inconsistent shadows, low resolution, obvious cutout edges, over-processed retouching, overly smooth fur, plastic-looking food texture, plastic-looking skin, unmatched lighting, unrealistic hands, unrealistic steam, warped product geometry, warped walls
```

runtime의 별도 negative 원문:

```text
3d render look, awkward animal anatomy, body distortion, broken facial features, broken window geometry, cartoon style, cgi look, digital illustration, distorted fingers, excessive hdr, fake-looking background, flat collage look, illustration look, impossible perspective, inaccurate reflections, inconsistent shadows, low resolution, obvious cutout edges, over-processed retouching, overly smooth fur, plastic-looking food texture, plastic-looking skin, unmatched lighting, unrealistic hands, unrealistic steam, warped product geometry, warped walls
```

[전체 결과와 원본·감사·ledger 경로](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/qualification/arm-b/qualification_result.json>)


**C: 유리 돔·황동 기계·구름 섬유가 있는 구름 제조 박물관**

seed `17340368523501746970` · 키워드 고개 갸웃, 꽃받침, 하이키, 복슬복슬, 캐치라이트 · pack `6510a34a03bc8482` · 최종 `FAIL`

[사전 동결 testcase](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/qualification/arm-c/testcase.json>) · [실제 요청 envelope](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/qualification/arm-c/request_envelope.json>)

**사전 동결 baseline prompt**

```text
A layered photographic tableau inside an eccentric museum of cloud-making contraptions. A fictional adult woman stands behind a pale terrazzo exhibit counter, her visible facial structure and short black bob guided by the attached reference. She pauses a demonstration to pose playfully for the viewer, wearing a smooth ivory satin blouse with a relaxed open collar beneath a fluffy cream vest whose long soft fibers visibly fringe its edges. Both elbows rest on the low counter; each forearm rises naturally to its own hand. Both open palms face the camera and cup the lower cheeks, the palm heels lightly touching the underside of the jaw. Her wrists meet in a small V below the chin and all ten fingers fan outward, separately visible beside her cheeks. Her head tilts toward screen right by about fifteen degrees while her shoulders stay nearly level; the two palms follow the tilted jaw at slightly different heights. Her amused closed-lip smile and warm direct gaze give the staged moment a gentle intimate charm. Both eyes are open and each pupil contains a distinct small bright rectangular catchlight. Behind her, three glass bell jars on brass stands hold shaggy white fiber cloud sculptures paired with small copper weather gauges. Tiny fabric kites hang on visible threads deeper in the gallery, in front of pale blue walls displaying fine line drawings of balloon devices. The polished counter, transparent glass, warm metal and soft pile remain visibly distinct. Bright diffused skylight and a large frontal white reflector create high-key illumination across the frame, pale luminous backgrounds, gently filled facial shadows and retained skin detail. An eye-level frontal waist-up photograph gives the face, complete hands and their contact points clear focus; the layered exhibits remain readable farther behind them. The face and open hands carry the first impression, followed by the fluffy surfaces, then the curious museum machinery. Natural skin texture, fine black hair strands and believable glass reflections preserve photographic presence.
```


**실제 전송 1 / FAIL**

[원본 도구 인수 JSON](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/qualification/arm-c/imagegen_tool_args.json>) · SHA-256 `afd925aa9e0119443fbef60fd71b66049937e47e153fc87d263ce10bf471f6c2`

```json
{
  "referenced_image_paths": [
    "/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg"
  ],
  "transparent_background": false
}
```

전송한 prompt 문자열을 그대로 표시한다.

```text
A layered photographic tableau inside an eccentric museum of cloud-making contraptions. A fictional adult woman stands behind a pale terrazzo exhibit counter, her visible facial structure and short black bob guided by the attached reference. She pauses a demonstration to pose playfully for the viewer, wearing a smooth ivory satin blouse with a relaxed open collar beneath a fluffy cream vest whose long soft fibers visibly fringe its edges. Both elbows rest on the low counter; each forearm rises naturally to its own hand. Both open palms face the camera and cup the lower cheeks, the palm heels lightly touching the underside of the jaw. Her wrists meet in a small V below the chin and all ten fingers fan outward, separately visible beside her cheeks. Her head tilts toward screen right by about fifteen degrees while her shoulders stay nearly level; the two palms follow the tilted jaw at slightly different heights. Her amused closed-lip smile and warm direct gaze give the staged moment a gentle intimate charm. Both eyes are open and each pupil contains a distinct small bright rectangular catchlight. Behind her, three glass bell jars on brass stands hold shaggy white fiber cloud sculptures paired with small copper weather gauges. Tiny fabric kites hang on visible threads deeper in the gallery, in front of pale blue walls displaying fine line drawings of balloon devices. The polished counter, transparent glass, warm metal and soft pile remain visibly distinct. Bright diffused skylight and a large frontal white reflector create high-key illumination across the frame, pale luminous backgrounds, gently filled facial shadows and retained skin detail. An eye-level frontal waist-up photograph gives the face, complete hands and their contact points clear focus; the layered exhibits remain readable farther behind them. The face and open hands carry the first impression, followed by the fluffy surfaces, then the curious museum machinery. Natural skin texture, fine black hair strands and believable glass reflections preserve photographic presence. The black bob and fine pupil rims supply compact dark landmarks within the bright cream-and-blue gallery.

Avoid: 3d render look, awkward animal anatomy, body distortion, broken facial features, broken window geometry, cartoon style, cgi look, digital illustration, distorted fingers, excessive hdr, fake-looking background, flat collage look, illustration look, impossible perspective, inaccurate reflections, inconsistent shadows, low resolution, obvious cutout edges, over-processed retouching, overly smooth fur, plastic-looking food texture, plastic-looking skin, unmatched lighting, unrealistic hands, unrealistic steam, warped product geometry, warped walls
```

runtime의 별도 negative 원문:

```text
3d render look, awkward animal anatomy, body distortion, broken facial features, broken window geometry, cartoon style, cgi look, digital illustration, distorted fingers, excessive hdr, fake-looking background, flat collage look, illustration look, impossible perspective, inaccurate reflections, inconsistent shadows, low resolution, obvious cutout edges, over-processed retouching, overly smooth fur, plastic-looking food texture, plastic-looking skin, unmatched lighting, unrealistic hands, unrealistic steam, warped product geometry, warped walls
```


**실제 전송 2 / FAIL**

[원본 도구 인수 JSON](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/qualification/arm-c/imagegen_tool_args_attempt2.json>) · SHA-256 `861a0de96fb8de493a9712b21e2b46057d35d38c48a12d03b84eed8fcb3b11ad`

```json
{
  "referenced_image_paths": [
    "/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg"
  ],
  "transparent_background": false
}
```

전송한 prompt 문자열을 그대로 표시한다.

```text
A layered photographic tableau inside an eccentric museum of cloud-making contraptions. A fictional adult woman stands behind a pale terrazzo exhibit counter, her visible facial structure and short black bob guided by the attached reference. She pauses a demonstration to pose playfully for the viewer, wearing a smooth ivory satin blouse with a relaxed open collar beneath a fluffy cream vest whose long soft fibers visibly fringe its edges. Both elbows rest on the low counter; each forearm rises naturally to its own hand. Both open palms face the camera, their heels lightly touching the underside of her jaw in a flower-cup pose. Her wrists meet in a small V below the chin. Each visible palm has one clearly separated thumb and four extended fingers spreading as a broad fan diagonally outward beside the cheeks; all ten fingertips and the gaps between them remain individually visible in open space. The top of her head tips toward the right edge of the image, her screen-right ear lowering toward her screen-right shoulder. Her eye line slopes downward toward screen right by about fifteen degrees while her shoulders stay nearly level; the screen-right palm sits slightly lower to follow the tilted jaw. Her amused closed-lip smile and warm direct gaze give the staged moment a gentle intimate charm. Both eyes are open and each pupil contains a distinct small bright rectangular catchlight. Behind her, three glass bell jars on brass stands hold shaggy white fiber cloud sculptures paired with small copper weather gauges. Tiny fabric kites hang on visible threads deeper in the gallery, in front of pale blue walls displaying fine line drawings of balloon devices. Bright diffused skylight and a large frontal white reflector create high-key illumination across the frame, pale luminous backgrounds, gently filled facial shadows and retained skin detail. An eye-level frontal waist-up photograph gives the face, complete hands and their contact points clear focus; the layered exhibits remain readable farther behind them. Natural skin texture, fine black hair strands and believable glass reflections preserve photographic presence. The black bob and fine pupil rims supply compact dark landmarks within the bright cream-and-blue gallery.

Avoid: 3d render look, awkward animal anatomy, body distortion, broken facial features, broken window geometry, cartoon style, cgi look, digital illustration, distorted fingers, excessive hdr, fake-looking background, flat collage look, illustration look, impossible perspective, inaccurate reflections, inconsistent shadows, low resolution, obvious cutout edges, over-processed retouching, overly smooth fur, plastic-looking food texture, plastic-looking skin, unmatched lighting, unrealistic hands, unrealistic steam, warped product geometry, warped walls
```

runtime의 별도 negative 원문:

```text
3d render look, awkward animal anatomy, body distortion, broken facial features, broken window geometry, cartoon style, cgi look, digital illustration, distorted fingers, excessive hdr, fake-looking background, flat collage look, illustration look, impossible perspective, inaccurate reflections, inconsistent shadows, low resolution, obvious cutout edges, over-processed retouching, overly smooth fur, plastic-looking food texture, plastic-looking skin, unmatched lighting, unrealistic hands, unrealistic steam, warped product geometry, warped walls
```

[최종 원본 이미지](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/qualification/arm-c/attempt2_original.png>)

[전체 결과와 원본·감사·ledger 경로](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/qualification/arm-c/ARM-C-RESULT.json>)
