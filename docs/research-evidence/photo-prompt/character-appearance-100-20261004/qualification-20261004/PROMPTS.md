# 실제 생성에 사용한 프롬프트 3개

모두 내장 image_gen 도구를 사용했다. 참조 입력은 같은 첨부 사진 1개이며 얼굴의 시각적 특징만 안내한다. 아래 positive prompt와 negative는 각각 검증된 composed object의 문자열을 그대로 복사했다. 실제 도구에는 positive 뒤에 정확한 `\n\nAvoid: <negative>`를 붙여 전달했다.

## arm-1

Positive prompt

```text
A photographic qualification scene with a fictional adult subject during a visible working moment. She is an adult woman in her thirties, a conservator paused beside a small brass star-projector lamp in the timber projection booth of a closed seaside planetarium at blue hour. The supplied portrait guides only her visible facial features. Her dark chin-length blunt bob has straight brow-length bangs, with the hair on her right side tucked behind her ear. A soft burgundy beret with a round flattened crown and narrow fitted band sits above the bangs, tilted toward her left. Thin round gold wire eyeglasses sit over her eyes. A small silver ear cuff encircles the exposed upper cartilage of her right ear, and a separate dangling teardrop earring hangs from that same earlobe. She wears a matte charcoal blouse with an open collar; the warm light traces her neck and relaxed shoulders with subtle intimate appeal. Her right hand rests lightly on the lamp housing while her left palm rests on the bench edge, elbows comfortably bent and both arms connected to her shoulders. The small brass lamp glows through its perforated domed housing, scattering crisp star-shaped points onto the timber wall behind her. Her eyes meet the camera during the calibration pause, lips relaxed and quietly amused. Frame a waist-up environmental portrait from slightly to her right at eye level, keeping the complete beret, bob outline, exposed right ear, eyeglasses and both hands legible. Gentle amber practical light on her face meets the cool harbour dusk through the booth window; worn wood and brass remain subordinate to her presence.
```

Negative

```text
3d render look, awkward animal anatomy, body distortion, broken facial features, broken window geometry, cartoon style, cgi look, digital illustration, distorted fingers, excessive hdr, fake-looking background, flat collage look, illustration look, impossible perspective, inaccurate reflections, inconsistent shadows, low resolution, obvious cutout edges, over-processed retouching, overly smooth fur, plastic-looking food texture, plastic-looking skin, unmatched lighting, unrealistic hands, unrealistic steam, warped product geometry, warped walls
```

## arm-2

Positive prompt

```text
Create one photographic test image of a fictional adult woman in a single held moment inside a used-book kiosk in an old railway concourse at dawn. The attached portrait supplies visible facial proportions for this invented adult subject. She stands comfortably with both feet on the floor, her right hand holding a slim paper-wrapped book upright against her right hip, thumb resting on its front cover and fingers supporting its back. Her left arm rests loosely beside her body. Her torso is turned slightly toward the book counter while her face turns toward the camera with a small, warm, closed-mouth smile. A dark chin-length bob with wispy strands frames her face. She wears a cropped graphite-and-ivory houndstooth jacket, its woven surface covered in small jagged broken checks, open over an ivory blouse. The blouse has a softly gathered ruffled collar standing around her neck, with a separate lower tier of scalloped lace fanning outward over the jacket neckline. The lace has small openwork holes and distinct rounded scallops along its outer edge. A narrow striped silk neck scarf sits beneath the raised ruffle and is tied in a small knot to one side; two short striped tails lie over that jacket lapel, leaving the layered collar readable. Soft window light from the cool concourse shapes her face, with a warm kiosk lamp catching the raised collar folds and matte woven jacket. Book spines and a worn wooden counter remain quiet background context. Photograph her from eye level in a vertical head-to-upper-thigh frame, including both hands and the jacket hem. Her face leads attention, then the nested collar textures and scarf, then the book, with natural skin detail and crisp garment surfaces in a restrained editorial photograph.
```

Negative

```text
3d render look, awkward animal anatomy, body distortion, broken facial features, broken window geometry, cartoon style, cgi look, digital illustration, distorted fingers, excessive hdr, fake-looking background, flat collage look, illustration look, impossible perspective, inaccurate reflections, inconsistent shadows, low resolution, obvious cutout edges, over-processed retouching, overly smooth fur, plastic-looking food texture, plastic-looking skin, unmatched lighting, unrealistic hands, unrealistic steam, warped product geometry, warped walls
```

## arm-3

Positive prompt

```text
A reference-guided photographic portrait of a fictional adult woman who pauses for the portrait in a converted greenhouse rehearsal corner. Use the supplied image as visible facial appearance guidance. She stands in a comfortable three-quarter stance after a quiet rehearsal, with an easy, composed gaze toward the camera and softly parted lips. Her dark navy sleeveless rehearsal dress is cinched by a black leather belt. The belt has a rectangular brass buckle, with its prong seated through a punched hole and its leather tail passing through a keeper loop. A pale ivory gauze scarf wraps across both shoulders; two overlapped fabric edges meet under a small round silver clasp at her upper chest, with gentle woven folds descending over the dress. A rigid geometric brass cuff encircles her left upper arm over the visible bare arm, its faceted band separated from her skin by a clean inner rim and small cast shadow. Her left arm hangs slightly away from her torso so the cuff and its enclosing shape stay visible. A slender strip of greenhouse background remains visible between her left upper arm and torso, continued by her gently bent elbow and relaxed wrist below. Her right elbow bends naturally beside her waist, and her right thumb and forefinger rest on the loose belt tail beside the closed buckle. The hands belong to her own connected arms. A middle-thigh-up frame includes the whole face, shoulders, cuff, belt and both hands. Tall glazed greenhouse panels and a simple wooden rehearsal barre sit behind her, softly out of focus. Diffuse late-afternoon daylight catches the gauze weave and metal edges, giving her quiet presence a subtle warmth. The photograph has natural skin texture, restrained contrast and a calm editorial rhythm.
```

Negative

```text
3d render look, awkward animal anatomy, body distortion, broken facial features, broken window geometry, cartoon style, cgi look, digital illustration, distorted fingers, excessive hdr, fake-looking background, flat collage look, illustration look, impossible perspective, inaccurate reflections, inconsistent shadows, low resolution, obvious cutout edges, over-processed retouching, overly smooth fur, plastic-looking food texture, plastic-looking skin, unmatched lighting, unrealistic hands, unrealistic steam, warped product geometry, warped walls
```
