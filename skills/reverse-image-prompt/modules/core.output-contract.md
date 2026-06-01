---
id: core.output-contract
version: 2
priority: 98
type: core
tier: 0
facet: core
facet_values:
  - output-contract
  - prompt-negative-settings
triggers:
  - any image
avoid_when: []
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
  - concept.primary-relationship
  - core.pre-emit-gate
conflicts: []
provides_anchors:
  - output_sections
  - prompt_contract_16
  - negative_primary_concept
  - recommended_settings_aspect
---

# Core: output contract

## When to load

Always. Load this before drafting any final answer.

Write the final answer in English. Output only these sections.

## PROMPT:

Write a polished, detailed standalone image-generation prompt in this order:

1. Overall image type, measured/source-specific aspect ratio, orientation, realism level, medium/rendering type, mood, and the primary visible concept in the first sentence.
2. Concept-critical relationships: elements, roles, construction recipe, alignment, overlap, scale relationship, continuity, replacement, completion/missing-side logic, seam or join geometry, feature-scale matching, interaction, medium contrast, coherence/realism ceiling, and what must remain true.
3. Exact composition, crop, subject size, frame placement, bounding box, and approximate coordinates.
4. Subject face and human appearance fidelity when people are visible.
5. Subject visible body proportions and physique fidelity when people are visible, including safe adult calibration locks only when relevant.
6. Exact pose, body orientation, head angle, gaze, shoulder line, torso lean, arms, elbows, wrists, hands, fingers, object grip, legs, stance, weight distribution, occlusion, negative space, crop boundaries, and pose landmark coordinates.
7. Clothing, accessories, and held objects, including how they reveal, obscure, flatten, soften, follow, compress, stretch over, widen, narrow, or visually define the body or pose.
8. Background by screen zones: left, right, top, bottom, foreground, midground, and background.
9. Lighting, atmosphere, color grading, contrast, highlights, notable shadow placement, falloff, receiving surfaces, visible cast shadows, self-shadowing, contact shadows when relevant, shadow edge quality and density only when they materially affect likeness, composition, or occlusion.
10. Camera position, distance, height, angle, rotation, lens impression, perspective distortion, subject-to-camera relationship, and perspective effects on apparent proportions.
11. Focus target, focus accuracy, depth of field, focus clarity, bokeh, foreground blur, background blur, low-detail areas, and relative focus hierarchy.
12. Motion blur, camera shake, shutter behavior, ghosting, smear direction, low-light exposure, haze, rolling-shutter or slow-shutter effects if visible.
13. Film/camera/sensor or rendering look: grain, noise, compression, sharpening, halation, vignetting, light leaks, scan texture, dust, scratches, flash snapshot look, smartphone HDR, dynamic range, black-level handling, bright-fabric bloom, dark-fabric absorption, shadow response, highlight rolloff, or non-photographic medium artifacts.
14. Boundary and visibility-budget locks: incomplete features, cropped-away counterpart features, frame-edge artifacts, pillarboxing/letterboxing/vignetting, narrow visible strips, secondary text marks, and occluders that must not move.
15. Coordinate and anchor locks: foreground subject anchors, background/secondary-layer anchors, frame-edge/border thickness and side placement, small text/mark coordinates, and dominant overlap boundaries.
16. Critical fidelity locks: primary visual concept, perceptual relationships, composition, crop, subject scale, face, body proportions when relevant, occlusion, clothing fit, neckline/seams, lighting-to-volume, pose, camera/focus/blur, lighting, color, background, objects, UI/text if relevant, and medium/rendering.

## NEGATIVE PROMPT:

Write concise, image-specific exclusions. Include only relevant drift risks:

- primary-concept drift and concept-lock failure modes
- wrong crop, subject scale, placement, headroom, body crop, object placement, or layer order
- cropped/partial features completed into full features
- missing counterpart features invented
- narrow visible bands expanded
- edge artifacts erased
- occluders moved to reveal hidden areas
- wrong background, extra subjects, duplicated objects, over-detailed blurred background, wrong location type
- wrong style or medium drift
- random text, subtitles, captions, logos, UI icons, watermarks, readable brand marks unless truly central and visible
- malformed hands, extra/missing fingers, broken limbs, warped face, impossible clothing folds, fused objects
- face, body, clothing, pose, lighting, camera/focus, and medium-specific drift only when those categories are present

## RECOMMENDED SETTINGS:

Fill every field with source-specific values:

- Aspect ratio:
- Size:
- Source frame treatment:
- Quality/Fidelity:
- Style/rendering target:
- Camera/film/rendering target:
- Lighting/rendering target:
- Primary visual concept locks:
- Perceptual relationship locks:
- Completion/seam continuity locks:
- Scale/interaction anchor locks:
- Coherence/realism ceiling locks:
- Most important fidelity locks:
- Face fidelity locks:
- Aesthetic and non-identifying appearance locks:
- Body-proportion calibration locks:
- Adult chest/upper-torso/waist/hip silhouette locks when relevant:
- Occlusion fidelity locks:
- Clothing-fit, neckline, and seam locks:
- Boundary and visibility-budget locks:
- Coordinate and anchor locks:
- Lighting-to-volume fidelity locks:
- Pose fidelity locks:
- Focus and depth-of-field locks:
- Motion blur and camera-shake locks:
- Film/camera/sensor or medium artifact locks:
- UI/text/label locks when relevant:
- Category-specific locks:

## Output gate

Before emitting, re-read `PROMPT:` as if the original image is gone. If it would recreate only the object inventory, not the relationship, crop, boundary, medium, and fidelity ceiling, revise. Any non-negotiable rule must appear in `PROMPT:` itself in affirmative language.

---

# Legacy monolith fidelity rules preserved verbatim

These excerpts are normative. They preserve detailed anti-drift behavior from `legacy/SKILL.monolith.original.md`; do not weaken them when applying this module.


## Legacy output gates and required output policy

6. Output gate before finalizing:
   - Re-read the drafted `PROMPT:` as if the image is no longer available. If the text would recreate only the object inventory, but not the relationship/effect, revise it before emitting.
   - If any Concept Spec item is missing from `PROMPT:` section 2 or the settings locks, revise before emitting.
   - For portraits, compare the drafted face and aesthetic description against the source. If it could generate a more symmetrical, cleaner, more glamorous, more influencer-like, brighter, or more idealized face than the source, add source-specific counterweights before emitting.
   - For clothing, compare the drafted garment description against the source geometry. If a broad garment label could reveal more skin, smooth awkward coverage, recenter the outfit, or turn it into a cleaner fashion garment, revise toward explicit visible edges and coverage maps.
   - For adjacent visual-band compositions, audit normalized vertical and horizontal bands before emitting. Check visible edges such as garment hems, material transitions, exposed or covered gaps, fasteners, prop boundaries, surface lines, horizons, rails, table edges, mirror seams, and crop boundaries. Do not let category labels, pose labels, garment-length labels, crop labels, or body-region labels shift those bands lower, higher, wider, narrower, taller, shorter, cleaner, or more centered than the source. When a broad label conflicts with a coordinate, bounding box, edge-band, or coverage-map lock, omit or weaken the broad label and keep the visible coordinate or band lock.
   - Weaken broad portrait, fashion, garment, product, genre, and body-region labels whenever they compete with source-specific visibility budgets. Labels such as `upper-body portrait`, `bare shoulder`, `off-shoulder`, `dress`, `corset`, `camisole`, `beauty portrait`, `product`, `fantasy`, or `character portrait` can pull the generator toward a conventional clean composition. Use them only as secondary shorthand after measured crop, occlusion, darkness, and edge-band locks; omit them if they cause a cleaner, more centered, more complete, or more revealing layout than the source.
   - For coordinate-heavy prompts, audit internal contradictions before emitting. If face center, head mass, eye line, shoulder span, prop box, hand box, text mark, watermark, label, or background seam coordinates disagree with descriptive phrases such as `centered`, `slightly right`, `lower-left`, `near the face`, `below the cheek`, `wide`, `small`, `dominant`, or `secondary`, revise so the coordinates and plain-language placement describe the same image-plane layout. Do not include multiple approximate ratio labels or centerline descriptions that could pull the generator toward a common crop or a more balanced portrait, fashion, or product composition.
   - For tight portraits, audit vertical face placement against frame budget. If the source face sits high, with substantial torso, prop, garment, or background detail below it, say that the face remains high and prevent the head from drifting downward to a balanced head-and-shoulders portrait. If the source face sits low or has unusual headroom, lock that instead. The face vertical anchor should agree with eye line, chin, top-of-head, shoulder, prop, and bottom-crop coordinates.
   - When estimating coordinates, trust the inspected source file and full image over a downscaled preview, crop-transformed viewer, or generator-friendly normalized composition. If coordinates are uncertain, use wider approximate ranges and relative anchors rather than overconfident exact centers that could shift the subject. Avoid letting a single coordinate estimate override the visible balance of face, foreground objects, shoulders, crop boundaries, and background.
   - For screenshots, screen recordings, app captures, camera previews, or social-video frames, audit the exact UI/content split before emitting. If a bottom input band, player control, crop bar, status overlay, or app overlay is present, state its measured y-start, height, opacity, and image-plane role.
   - For screenshot-like sources, explicitly reject common controls that are not visible, such as home indicators, heart/reaction buttons, share buttons, profile avatars, side action stacks, progress bars, captions, top app chrome, branded headers, or enlarged UI controls.
   - Assume downstream image generation may use only the `PROMPT:` body. Any non-negotiable crop, camera, boundary, appearance, garment, occlusion, and medium-fidelity constraints must appear inside `PROMPT:` in affirmative visual language, not only in `NEGATIVE PROMPT:` or `RECOMMENDED SETTINGS:`.
   - Before finalizing, check whether any secondary prop, garment edge, accessory, text mark, label, watermark, or background object receives more words than its visible importance supports. If a secondary element has become over-described, compress it into one measured sentence plus one drift-prevention sentence. Spend the prompt's detail budget in the same hierarchy as the source image: dominant concept and composition first, primary subject and key occluders next, then secondary marks and background fragments.
   - If the source is a casual, awkward, low-angle, close-camera, screenshot-like, or otherwise non-editorial capture, the opening sentence should lead with frame geometry, camera height/angle, crop, subject scale, and fidelity ceiling before broad fashion, beauty, or genre labels that could normalize the image.

7. Write only the required output sections:
   - `PROMPT:`
   - `NEGATIVE PROMPT:`
   - `RECOMMENDED SETTINGS:`

8. Do not compress or summarize the output contract.
   - The `PROMPT:` section must include the full ordered fidelity coverage, not a short caption plus a few locks.
   - The `RECOMMENDED SETTINGS:` section must preserve the field labels listed in this skill. Do not collapse them into a paragraph or omit fields because they seem redundant.
   - If a source contains people, partial elements, occlusion, frame-edge artifacts, degraded fidelity, or mixed media, those facts must appear in `PROMPT:`, drift prevention in `NEGATIVE PROMPT:`, and explicit locks in `RECOMMENDED SETTINGS:`.

9. Report prompt-only limits honestly.
   - If prompt-only reproduction appears intrinsically capped below a requested similarity threshold, keep improving the prompt extraction skill, but state the cap clearly.
   - Recommend reference-conditioned generation, image editing, control/seed support, or a tool with image-fidelity controls when exact crop, pose, appearance aesthetics, and background fragment placement cannot be achieved reliably from text alone.

Do not include hidden analysis, checklist text, caveats, explanations, or references to the source image still being attached.


## Legacy Output Contract

## Output Contract

Write the final answer in English and output only these sections.

### PROMPT:

Write a polished, detailed standalone image-generation prompt in this order:

1. Overall image type, aspect ratio, orientation, realism level, medium/rendering type, mood, and the primary visible concept in the first sentence.
2. Concept-critical relationships: which elements create the main visual idea, their roles, construction recipe, alignment, overlap, scale relationship, continuity, replacement, completion/missing-side logic, seam or join geometry, feature-scale matching, interaction, medium contrast, coherence or realism ceiling, and what must remain true for the image to read correctly.
3. Exact composition, crop, subject size, frame placement, bounding box, and approximate coordinates.
4. Subject face and human appearance fidelity when people are visible.
5. Subject visible body proportions and physique fidelity when people are visible, including adult calibration locks when relevant and safe.
6. Exact pose, body orientation, head angle, gaze, shoulder line, torso lean, arms, elbows, wrists, hands, fingers, object grip, legs, stance, weight distribution, occlusion, negative space, crop boundaries, and pose landmark coordinates.
7. Clothing, accessories, and held objects, including how they reveal, obscure, flatten, soften, follow, compress, stretch over, widen, narrow, or visually define the body or pose.
8. Background by screen zones: left, right, top, bottom, foreground, midground, and background.
9. Lighting, atmosphere, color grading, contrast, highlights, notable shadow placement, falloff, receiving surfaces, visible cast shadows, self-shadowing, contact shadows when relevant, shadow edge quality and density only when they materially affect likeness, composition, or occlusion, flash behavior if present, and how shadows affect visible edges, separation, occlusion, and lighting-to-volume effects without inferring new structure.
10. Camera position, distance, height, angle, rotation, lens impression, perspective distortion, subject-to-camera relationship, and perspective effects on apparent proportions.
11. Focus target, focus accuracy, depth of field, focus clarity, bokeh, foreground blur, background blur, low-detail areas, and which planes are relatively most in focus or blurred.
12. Motion blur, camera shake, shutter behavior, ghosting, smear direction, low-light exposure, haze, rolling-shutter or slow-shutter effects if visible, and whether blur should be preserved or avoided.
13. Film/camera/sensor or rendering look: grain, noise, compression, sharpening, halation, vignetting, light leaks, scan texture, dust, scratches, flash snapshot look, smartphone HDR, dynamic range, black-level handling, bright-fabric bloom, dark-fabric absorption, shadow response, highlight rolloff, or non-photographic medium artifacts.
14. Boundary and visibility-budget locks: incomplete features, cropped-away counterpart features, frame-edge artifacts, pillarboxing/letterboxing/vignetting when visible, narrow visible strips, secondary text marks, and occluders that must not move to reveal more detail.
15. Coordinate and anchor locks: foreground subject anchors, background/secondary-layer anchors, frame-edge/border thickness and side placement when visible, small text/mark coordinates, and dominant overlap boundaries.
16. Critical fidelity locks: primary visual concept, perceptual relationships, composition, crop, subject scale, face, calibrated body proportions when relevant, adult chest/upper-torso/waist/hip silhouette when relevant, occlusion, clothing fit, neckline/seams, lighting-to-volume, pose, camera/focus/blur, lighting, color, background, objects, and medium/rendering.

### NEGATIVE PROMPT:

Write concise, image-specific exclusions tailored to the actual image. Include only relevant drift risks, covering:

- Primary-concept drift and concept-lock failure modes: all objects present but their visual relationship is wrong, concept-critical object treated as a generic prop, intended effect collapsed into separate unrelated objects, replacement/continuation/scale/interactions broken, fused surfaces rendered as separate stacked objects, completion seam misaligned, counterpart or missing-side logic swapped, duplicated, or omitted, feature proportions mismatched across a join, frame-within-frame lost, mixed-media contrast lost, intended implausibility or uncanniness normalized into a plausible realistic scene, stylized/composited/screen-contained element promoted into a normal physical object, ordinary scene replacing the intended visual premise, or a visually separate collage replacing a single integrated illusion.
- Wrong crop, subject scale, placement, headroom, body crop, object placement, or foreground/midground/background order.
- Crop-boundary drift: cropped or partial features completed into full features, missing counterpart features invented, narrow visible bands expanded, edge artifacts removed, pillarboxing/letterboxing/vignetting erased, or occluders moved to reveal hidden areas.
- Wrong background, extra people, extra objects, duplicated objects, over-detailed blurred background, or wrong location type.
- Wrong style or medium drift: cartoon, anime, illustration, 3D render, painting, sketch, vector art, glossy commercial look, fake cinematic look, fake vintage look when absent, overprocessed HDR, plastic skin, excessive retouching, AI-smoothed face or body.
- Text, watermark, logos, UI icons, subtitles, captions, random letters, readable brand marks unless truly central and generic.
- Distorted hands, extra fingers, missing fingers, malformed grip, broken limbs, warped face, mismatched eyes, duplicated people, fused objects, impossible clothing folds, impossible anatomy.
- For portraits: wrong apparent ancestry/race-coded appearance, skin tone, face shape, eyelid structure, eye spacing, nose bridge/width/length, lip fullness, jawline, chin, cheekbones, age range, hair texture, hairline, facial texture, makeup level, face-defining light/shadow, and non-identifying facial anchors.
- Aesthetic drift: beautified face, influencer face, fashion-editorial styling, glamour retouching, changed expression mood, changed gaze intensity, changed skin sheen, changed makeup level, more symmetrical or model-like features, more polished styling, or sanitized social-media look when the source is rougher, softer, dimmer, more ordinary, more awkward, or differently styled.
- For visible adult bodies: different body type, shoulder width, upper-torso/chest/bust silhouette, waist position/taper, hip width, torso-to-leg ratio, limb thickness, clothing-shaped silhouette, hidden anatomy invention, body-feature erasure, body-feature exaggeration, lighting-caused volume drift, occlusion drift, and camera/lens distortion drift.
- If a visible adult chest/bust/upper-torso silhouette is large or very large, prevent it from becoming moderate, average, small, flat, athletic, narrower, less projected, less rounded, less dominant, more generic, hidden by excessive shadow, flattened by frontal light, or reduced by modesty/anti-sexualization defaults.
- If it is moderate, moderate-to-full, partial, secondary, softened, low-detail, or obscured, prevent it from becoming large, very large, more projected, more rounded, more exposed, more centered, more lifted, more sculpted, more visible, more dominant, more tightly clothed, more cleavage-emphasized, more sharply shadowed, more strongly highlighted, or exaggerated by prompt overcorrection.
- Occlusion drift: phones, hands, arms, hair, clothing, bags, props, shadows, blur, another person, or crop edges moving in a way that reveals more body, hides different body areas, removes partial coverage, or clarifies hidden anatomy.
- Clothing drift: wrong neckline depth/width, strap placement, sleeve placement, seam placement, fabric tightness/looseness/thickness, folds, opacity, transparency, lace, buttons, corset-like structure when absent, lingerie-like structure when absent, tighter/looser/more revealing/more modest clothing, or changed silhouette.
- Lighting drift: wrong light direction, highlight placement, shadow falloff, exposure, contrast, black-level handling, bloom, dark-fabric absorption, rim light, frontal flattening, contour lighting, missing cast shadows, wrong contact shadows, removed self-shadowing, shadow direction mismatch, shadow caster/receiver mismatch, over-brightened shadow areas, shadow-hidden contours becoming invented detail, haze-softened contours becoming sharp, low-contrast contours becoming high-contrast, or lighting that changes visible proportions.
- Pose drift: mirrored pose, changed head tilt/gaze/shoulder angle/torso lean/arm placement/elbow bend/hand position/finger pose/leg stance/weight distribution/crop, added or removed hands, generic standing/seated/fashion/action pose, or changed occlusion.
- Camera/focus drift: wrong camera distance/height/angle/lens perspective/focus target/depth of field, background too sharp, foreground too sharp, missed focus becoming perfect, soft photo becoming overly sharp, sharp photo becoming blurry, added or removed camera shake, wrong blur direction, wrong grain/sharpening/flash/color cast/camera type/dynamic range/highlight rolloff, or polished studio quality when the source is casual or imperfect.

### RECOMMENDED SETTINGS:

Fill every field with source-specific values:

- Aspect ratio:
- Size:
- Source frame treatment:
- Quality/Fidelity: match the source fidelity; if the source is degraded, soft, compressed, noisy, hazy, or underexposed, state that directly and do not default to high quality.
- Style/rendering target:
- Camera/film/rendering target:
- Lighting/rendering target:
- Primary visual concept locks:
- Perceptual relationship locks:
- Completion/seam continuity locks:
- Scale/interaction anchor locks:
- Coherence/realism ceiling locks:
- Most important fidelity locks:
- Face fidelity locks:
- Aesthetic and non-identifying appearance locks:
- Body-proportion calibration locks:
- Adult chest/upper-torso/waist/hip silhouette locks when relevant:
- Occlusion fidelity locks:
- Clothing-fit, neckline, and seam locks:
- Boundary and visibility-budget locks:
- Coordinate and anchor locks:
- Lighting-to-volume fidelity locks: include source-specific light direction plus only source-specific shadow details that materially affect likeness, composition, occlusion, or surface separation; avoid over-specifying minor shadows or inferring hidden structure from shadowed areas.
- Pose fidelity locks:
- Focus and depth-of-field locks: describe the relative focus hierarchy rather than absolute sharpness; for degraded sources, use phrasing like `eyes and face are the least soft area, still low-resolution and compression-softened`.
- Motion blur and camera-shake locks:
- Film/camera/sensor or medium artifact locks:
