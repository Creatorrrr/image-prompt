---
name: reverse-image-prompt
description: Reverse engineer a faithful standalone English text-to-image prompt from a provided or attached image. Use when the user asks to analyze a reference image, extract or reconstruct an image-generation prompt, create a GPT Image 2 prompt, write a negative prompt, or produce recommended generation settings from visible image evidence.
---

# Reverse Image Prompt

## Purpose

Create a text-only image generation prompt from one provided image. The prompt must stand alone without the original image attached and should maximize reproducibility of the source image's visible composition, subject appearance, pose, crop, camera treatment, lighting, background, color, medium, and artifacts.

Preserve the source image, not a corrected, beautified, safer-looking, more modest, more sexualized, more cinematic, more polished, more generic, or more socially normalized version of it.

## Workflow

1. Inspect only the provided image.
   - If the image is attached in the conversation, visually analyze it directly.
   - If the user provides a local path, use `view_image` to inspect it.
   - If no image is available, ask the user to attach or provide the image.
   - If multiple images are provided and the user asks for one prompt, ask which image to use or process each image independently if the request clearly allows multiple outputs.

2. Do not use external identity or metadata assumptions.
   - Do not identify or name real people, celebrities, copyrighted characters, brands, artists, exact cameras, exact lenses, exact film stocks, or exact private identities.
   - Do not rely on external knowledge. Use only visible evidence.
   - If a detail is ambiguous, write `appears`, `suggests`, `visually reads as`, `likely`, `partially obscured`, or `ambiguous`.

3. Silently analyze in this priority order:
   1. Primary visual concept, perceived intent, and perceptual relationships: separately from any object inventory, identify what the image is arranged to make a viewer perceive. Form at least one literal object-level reading and, when visible relationships support it, one relationship/effect-level reading. Decide which reading is dominant and name the visible cues that force it, such as alignment, contour continuation, scale match, overlap, shared line, crop boundary, frame placement, contact point, foreground/background ordering, occlusion, replacement, reflection, screen-within-screen, mixed media, or scale contrast. If the relationship/effect reading is dominant, every object is subordinate to it and should be described by visual role, not only by category.
   2. Composition, aspect ratio, orientation, crop, subject scale, frame placement, and spatial layout.
   3. Human appearance fidelity when people are visible: face, skin tone, broad apparent visual ancestry or race-coded appearance when visually evident, hair, visible body proportions, clothing-shaped silhouette, pose, and occlusion.
   4. Pose mechanics, gesture, limb placement, hand placement, negative space, and crop boundaries.
   5. Camera distance, height, angle, lens impression, perspective distortion, focus target, depth of field, focus clarity, blur, camera shake, and optical behavior.
   6. Lighting direction, atmosphere, color grading, contrast, highlights, visible shadows when relevant, shadow falloff, flash behavior, and lighting-to-volume effects.
   7. Background zoning, objects, depth layers, and environmental details.
   8. Medium, texture, grain, noise, compression, imperfections, and processing artifacts.

4. Use approximate normalized coordinates when useful:
   - `x=0%` is the far left edge; `x=100%` is the far right edge.
   - `y=0%` is the top edge; `y=100%` is the bottom edge.
   - Use coordinates for major anchors such as face center, eye line, head, shoulders, torso, waist, hips, elbows, hands, knees, feet, held objects, important foreground/background objects, horizon line, light sources, highlights, shadow boundaries, receiving surfaces, contact shadows, shadow-hidden contours, focus zones, blur zones, crop edges, and occluding objects.
   - Use coordinates for concept-critical relationships such as shared eye lines, centerlines, contour junctions, screen or frame edges, foreground contact points, overlap boundaries, replacement zones, and scale-reference points.
   - For high-fidelity reconstruction, include a dedicated coordinate-lock passage in `PROMPT:` that covers the dominant foreground subject, the most important background or secondary-layer anchors, frame-edge artifacts, crop boundaries, and any small text/mark locations. Coordinates should describe placement and relative dominance, not only object presence.

4a. Audit the source frame ratio before drafting:
   - If image file dimensions are available in the conversation or from local inspection, compute or preserve the actual width:height relationship in plain terms, such as `aspect about 0.69, taller than 3:4 but wider than 9:16`.
   - When a local source file path is available, check the actual pixel dimensions with a local metadata tool before drafting. If the visible frame is meaningfully narrower, taller, squarer, letterboxed, cropped, or otherwise different from a common ratio, do not normalize it to the common ratio.
   - Keep aspect ratio and output size conceptually separate. Report the measured source pixel dimensions as `width x height`, the decimal width/height ratio, and the nearest plain-language shape.
   - Do not substitute common portrait or landscape labels such as `2:3`, `3:4`, `4:5`, `9:16`, `16:9`, or `1:1` unless that label is close to the measured frame. If no common label is close, say `source-specific portrait crop`, `source-specific landscape crop`, or `source-specific square-adjacent crop` and give the source dimensions or approximate aspect.
   - Do not substitute a generator-preferred size, downscaled preview size, reduced fraction, conversation preview, viewer downscale, model output default, or common 1024-based canvas for the source ratio. If the source file is available, file metadata wins over visible preview dimensions.
   - Put the measured frame treatment in the first sentence of `PROMPT:` before broad labels such as beauty portrait, cosplay portrait, editorial portrait, product shot, screenshot, or landscape.
   - Repeat the measured ratio in `RECOMMENDED SETTINGS:` and list the nearest standard size only as a fallback, clearly saying it is a fallback.
   - Treat aspect-ratio drift as a major fidelity failure because it changes subject scale, edge crops, object placement, and visibility budgets.

5. Before writing any output, lock the concept:
   - Commit to the dominant reading in one internal sentence of perceived intent.
   - Identify at least one literal object-level reading and one relationship/effect-level reading when the image contains overlaps, occlusion, scale contrast, framing, insertion, replacement, reflection, screen-within-screen, or mixed media.
   - Name the visible cues that make the dominant reading work, such as alignment, contour continuation, scale match, overlap, shared line, crop boundary, frame placement, contact point, or foreground/background ordering.
   - If the image contains an integrated illusion, replacement surface, reflection, screen- or frame-within-frame structure, mixed-media composite, scale-contrast interaction, subject/object completion, or any case where separate elements must read as one effect, build an internal Concept Spec. If the image is ordinary, do not invent a special relationship; use a one-line ordinary premise.
   - In the Concept Spec, name the relationship type, contributing surfaces/elements and their visual roles, join geometry, completion/missing-side logic, coherence or realism ceiling, and the top 1-3 failure modes.
   - Completion/missing-side logic must state what visible features each surface carries, what hidden or counterpart features another surface supplies, whether side references use subject-side or viewer-side perspective when that could be confused, and which shared lines, contours, proportions, or contact points must match.
   - Coherence or realism ceiling must state whether the effect depends on implausibility, uncanniness, mixed-media contrast, low fidelity, or scale incongruity, so the scene is not normalized into a more plausible physical setup.
   - Treat Concept Spec items as required content for `PROMPT:` section 2 and the relevant `RECOMMENDED SETTINGS:` locks. Treat failure modes as the first inputs to the negative prompt.

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

## Visual Evidence Rules

- Never write `same as the image`, `as shown`, `based on the reference`, `like the provided image`, `from the uploaded image`, or any wording that requires the original image to remain attached.
- Do not infer hidden anatomy, hidden objects, hidden clothing structure, hidden context, personality, intent, nationality, exact ethnicity, religion, measurements, sizes, age, weight, height, camera metadata, or private identity.
- Do not correct image imperfections unless the user explicitly asks for an improved version.
- Preserve imperfections when visible: softness, haze, low contrast, grain, digital noise, compression, motion blur, missed focus, underexposure, overexposure, backlight, clipped highlights, crushed shadows, cast shadows, self-shadowing, contact shadows, casual framing, sensor artifacts, flash flattening, or low-resolution texture.
- Calibrate underexposure instead of maximizing it. When the source has dark clothing, hair, night areas, or shadowed interiors, distinguish fully crushed black regions from low-contrast regions that still show folds, edges, face planes, fabric bands, or object silhouettes. Preserve the amount of remaining shadow detail; do not turn visible dark detail into a featureless black mass.
- When the source image is soft, low-resolution, underexposed, compressed, noisy, or hazy, do not use absolute enhancement terms such as `high quality`, `sharp`, `sharpest`, `crisp`, `clean`, or `pristine` to describe focus, highlights, or recommended quality. Use source-faithful relative terms instead, such as `least soft`, `most in focus relative to the rest`, `retains the most detail`, `small dim highlight`, or `weak specular point`.
- Preserve incomplete evidence. If an object, face, body part, text mark, background figure, surface, or environmental element is cropped, hidden, blurred, shadowed, cut off by frame edges, or only partly visible, describe it as incomplete and specify which visible parts remain. Do not let the prompt invite a complete version of that element.
- Preserve frame-boundary evidence. If the source contains pillarboxing, letterboxing, dark side strips, vignetting, clipped edges, awkward headroom, hard crop boundaries, or edge falloff, treat those as composition facts rather than artifacts to remove.
- For screenshots or screen-recorded social-video frames, treat interface overlays as composition-critical image-plane bands. Lock their exact vertical bands, opacity, corner radius, text size, low-legibility level, and absence/presence of common app controls. State which controls are absent as well as which are present, so the generator does not add hearts, home indicators, action buttons, captions, or clean branded UI that were not visible.
- Preserve overlay restraint. If the source has only a simple status bar, one bottom comment/input field, one crop mark, or one small ambiguous control, do not let the prompt invite a complete modern app interface. Name absent control families in the `PROMPT:` itself when they are likely generator defaults.
- Distinguish transparent overlay icons from app chrome bands. If top status icons float directly over the video/background with no black rectangle behind them, say so explicitly and reject a black top status bar, notch area, or header strip. If the bottom has a dark comment area but no home indicator, reject home indicators even when the generated image is phone-shaped.
- Treat hard frame boundaries and crop exclusions as higher priority than object completion. If satisfying object realism would require revealing cropped areas, completing partial body/object/background regions, removing borders, or expanding the scene, preserve the crop and boundary instead.
- Use a visibility budget for partially visible areas. When only a narrow strip, partial band, partial limb, partial object, or small text mark is visible, state that it remains narrow, partial, secondary, or obscured. Do not reveal more of it, enlarge it, clarify it, or move occluders away unless the source visibly does so.
- Clamp bottom-edge and side-edge partial visibility. If a body region, object, garment, sign, or surface appears only as a thin strip at the frame edge, describe its approximate edge band and explicitly keep it at that edge. Do not let it expand inward, become a full object/body area, or become a new visual center.
- Cap generated polish to the source. When the source is casual, degraded, compressed, dim, soft, or awkwardly framed, the prompt must prevent the output from becoming cleaner, brighter, more symmetrical, more complete, more evenly lit, more editorial, or more polished than the source.
- Preserve awkward capture geometry over attractive pose semantics. If the source is a close, low-angle, cropped, accidental, convention-like, mirror-like, screenshot-like, or casual phone capture, describe that awkwardness as a required fidelity trait and prevent fashion-normalized posture, cleaner posing, centered editorial balance, or full-body/waist-up portrait correction.
- For prompt-only reproduction, repeat the most important frame geometry and crop locks in the `PROMPT:` itself near the beginning and again in the critical fidelity locks. Use affirmative wording such as `the composition remains...`, `the closest plane stays...`, and `the edge band remains...` so the prompt does not rely only on negative exclusions.
- Preserve source aesthetics and non-identifying appearance, not a normalized beauty ideal. When a person, product, place, or object has a particular visible mood, styling, attractiveness pattern, roughness, awkwardness, asymmetry, facial softness, makeup level, surface sheen, color cast, or image-era/social-media look, describe that aesthetic calibration and prevent beautification, fashion-editorial upgrading, influencer-like smoothing, glamorization, aging down/up, westernization, or generic model drift.
- For dark, cramped, low-resolution, heavily styled, or socially edited portraits, prevent coordinate precision from becoming permission to rebalance the image. If the source is murky, crowded, shadow-blocked, underexposed, compressed, or visibly stylized, state that the portrait remains visually compressed, dim, low-detail, and source-faithful even when face, prop, garment, or background coordinates are specified. Avoid wording that upgrades the source into a clean centered studio portrait, product portrait, fashion lookbook frame, or polished character reference unless that finish is visibly present.
- When light-created shadows materially affect likeness, composition, occlusion, or surface separation, preserve them instead of brightening, erasing, retouching, or normalizing them. Do not invent contours, body shape, surface detail, or environmental structure hidden by shadow.
- When backlight both hides and reveals the subject, specify which edges and planes remain readable. Do not let `silhouette`, `underexposed`, or `crushed shadows` erase visible face edges, garment fold bands, lace trim, hair outline, object silhouettes, or background detail that the source still shows.
- Do not resolve the image into the nearest plausible or more coherent scene. If the concept depends on illusion, mismatch, uncanny composite structure, mixed-media layering, scale incongruity, low fidelity, or a deliberately awkward capture, preserve that relationship above realism and plausibility. Do not promote a stylized, composited, inserted, reflected, or screen-contained element into a normal physical object unless it visibly is one.
- For non-photographic images, adapt the same fidelity rules to the medium: virtual camera, perspective, stylized proportions, edge quality, linework, brush texture, value structure, cel shading, render quality, material treatment, paper/canvas texture, or game-engine look.

## Primary Visual Concept and Perceptual Relationship Fidelity

Before listing visible objects, identify the primary visible concept that makes the image recognizable. Treat this as the highest-priority fidelity target. The primary concept may be an illusion, a mixed-media relationship, a frame-within-frame structure, a scale contrast, an interaction, a deliberately imperfect capture mode, or another visible relationship between elements.

Separate intent from inventory: an inventory lists what objects are present, while intent states what those objects are arranged to make the viewer perceive. When the two diverge, intent governs. Never let a complete object inventory substitute for the perceptual relationship; an image where every object is named but the intended relationship is absent has failed, even if no object is missing.

Describe each concept-critical element by its visual role, not only by its object category. Examples of roles include replacement surface, continuation plane, occluder, scale anchor, foreground interaction target, UI frame, reflection, inserted image, stylized overlay, physical prop, or medium-contrast anchor.

If two visible elements are meant to read as one continuous subject, preserve the alignment, scale, contour continuation, crop boundary, and feature proportions that create that perception. If one visible element replaces part of another subject, describe exactly which part is replaced, how the replacement aligns, and what would break the illusion.

When a replacement, reflection, screen, frame, overlay, occluder, or continuation plane completes another element, write it as a construction recipe rather than a prop list. State what content each surface carries, what hidden or counterpart features the completing surface supplies, and how the union avoids duplicated or missing features across the seam. Preserve shared eye lines, centerlines, contact points, contour junctions, feature scale, crop boundaries, and medium contrast that make the surfaces fuse or interact.

For handheld-screen or phone-screen replacement portraits, the screen is not merely a prop. Lock the screen as the active replacement surface with its approximate corner coordinates, diagonal or rotation angle, border thickness, image-plane area, and overlap boundary over the real subject. State which real face features remain visible outside the screen, which real features are hidden by the screen, and which screen-contained features visually substitute for the hidden side. If the source has only one real eye or a narrow facial sliver visible, make that visibility budget explicit and reject a fuller real face. If the screen is steeply diagonal, prevent the generator from flattening it into a generic horizontal selfie-phone pose or upright product-like phone.

If a handheld screen covers the lower center of a face or torso, state the screen's lower and inner overlap as mandatory, not optional. Name hidden mouth, chin, nose, cheek, jaw, neckline, garment, or torso zones as absent in the real layer when supported by visible evidence, and repeat that those hidden features should not reappear around the screen edges. When the source screen sits low enough to cover a face boundary or upper-torso boundary, do not let the screen drift upward, outward, smaller, or to the side in a way that exposes a conventional portrait or fashion subject.

For any screen-replacement portrait or frame-replacement composition, draft an explicit replacement-overlap polygon before describing beauty, cosplay, character, fashion, product, or scenic cues. The polygon should include the containing surface corners, the edge that crosses the real subject, the lower or inner edge that hides visible features when present, and the maximum reveal outside that polygon. Use this polygon to constrain face visibility, hand placement, object scale, and screen/frame scale. If satisfying a prettier or more plausible scene would require moving the replacement surface away from the occluded zone, preserve the overlap and accept the awkward crop.

When an opaque rectangular occluder such as a phone, screen, card, sign, book, mirror panel, sticker, window frame, or foreground prop blocks a face, body, garment, product, or background region and defines the visible concept, prioritize the occluder's image-plane footprint, corners, lower and inner edges, and hidden-feature coverage before face attractiveness, garment readability, object completeness, or portrait symmetry. This is a general source-evidence rule: the occluder footprint outranks beauty, fashion, product clarity, and scene completion when the source visibly depends on that occlusion.

Separate canvas orientation from object orientation. A vertical source image may contain a landscape-oriented phone, screen, frame, card, book, sign, panel, label, package, window, or tabletop object rotated diagonally. For each major rectangular object, identify its own long edge, short edge, corner order, and rotation in the image plane before using labels like portrait, landscape, vertical, or horizontal. If the object's long edge runs lower-left to upper-right or upper-left to lower-right, say that directly and avoid shorthand that could rotate the object upright.

When a screen-contained face, poster face, reflection face, printed face, illustrated insert, UI panel, or framed secondary image supplies only a partial counterpart, describe it as partial content inside its containing surface. Name the visible eye, mouth, hair, highlight, object, text, or crop fragments and the absent counterpart fragments. Do not let the prompt invite a full in-world person, complete object, separate sticker outside the containing surface, or clean second subject unless those are visibly present.

If side, direction, or mirrored/counterpart logic matters, state whether the description uses subject-side or viewer-side perspective and keep that perspective consistent. Do not let the generated result swap which side is visible, duplicate features on both sides, omit required counterpart features, or disconnect matching contours.

If the intended relationship depends on implausibility, uncanniness, low fidelity, mixed rendering styles, a screen-within-screen structure, or scale contrast, preserve that coherence ceiling. Do not turn the relationship into a cleaner, more physically plausible, more realistic, or more unified scene when that would erase the visual premise.

If the image does not contain a special illusion or relationship, do not invent one. In that case, use this section to identify the ordinary main visual premise, such as a specific portrait crop, product arrangement, gesture, environmental mood, or rendering style.

When a background, reflection, poster, screen, printed surface, mirror, window, or other secondary layer contains partial human features, object fragments, text, or environmental details, write the visible fragments as fragments. State which counterpart features are absent, cropped away, obscured, or outside the frame so the generated image does not complete the layer into a fuller scene.

For secondary layers, prevent completion aggressively. A printed, reflected, screen-contained, blurred, or background-only face/object should not gain a complete body, missing eyes, missing limbs, readable full text, extra surroundings, or physical interaction unless those features are visibly present. Put these completion risks into the negative prompt.

For large secondary layers, distinguish dominant visible fragments from tempting but absent counterpart fragments. The prompt should name the 1-3 fragments that visually matter most, their approximate coordinates, and any counterpart details that should stay cropped, hidden, blurred, or absent.

For partial secondary-layer faces, preserve expression evidence conservatively. If mouth openness, teeth, eyes, gaze, or expression are cropped, blurred, ambiguous, or only partly visible, say so and prevent the generator from making them clearer, wider open, more expressive, more centered, or more complete than the source.

When useful, use normalized coordinates for concept-critical relationships: shared eye lines, centerlines, contour junctions, screen or frame edges, foreground contact points, overlap boundaries, replacement zones, and scale-reference points.

Appearance, body, clothing, and object fidelity serve the primary visual concept and must not outrank it. When descriptive detail competes with the perceptual relationship that makes the image recognizable, preserve the relationship first.

## Human Subject Fidelity

When people are visible, describe a fictional person with similar visible non-identifying appearance. Include:

- Apparent age range, gender presentation if visually relevant, and broad apparent visual ancestry or race-coded appearance only when visually evident and useful for preventing drift.
- Skin tone depth and undertone; pores, shine, matte texture, freckles, moles, blemishes, redness, under-eye shadows, scars, wrinkles, facial hair, makeup level, and other visible non-identifying anchors.
- Face shape and silhouette; forehead, hairline, cheeks, cheekbones, jaw width, jaw softness or sharpness, chin size and shape.
- Eye size, spacing, shape, eyelid structure, eyelid fold visibility, brow shape/thickness/arch, catchlights, and gaze direction.
- Nose bridge, width, length, tip shape, nostril visibility, and frontal/profile/three-quarter impression.
- Mouth width, upper/lower lip fullness, cupid's bow, teeth visibility, parted or closed lips, and smile/tension.
- Ears, neck, visible asymmetry, dimples, facial marks, and other visible anchors.
- Hair color, texture, density, length, parting, bangs, flyaways, volume, curl/wave pattern, and how hair frames or occludes the face.

Prevent the generated person from drifting into a different face type, skin tone, apparent ancestry, age range, eyelid structure, nose structure, jawline, chin, lip fullness, hair texture, hairline, makeup level, facial texture, or a more generic model-like, influencer-like, symmetrical, westernized, airbrushed, stylized, sanitized, or differently lit face.

Also preserve the source's aesthetic face treatment: expression tension, mouth relaxation, gaze intensity, eye openness, eyelid shadow, skin sheen or matte quality, cosmetic strength, retouching level, facial softness or angularity, and whether the face reads as candid, ordinary, glamorous, polished, uncanny, doll-like, influencer-like, or unfiltered. Do not let the generator improve attractiveness by changing these visible cues.

Before finalizing portrait prompts, check for aesthetic-upgrade risks: more symmetrical face, cleaner skin, rounder or sharper idealized features, glossier lips, brighter eyes, smoother makeup, more frontal beauty lighting, or influencer-style polish. Add source-specific counterweights when these would drift from the visible source.

## Body Proportion and Clothing-Silhouette Fidelity

For every visible person, describe only visible image-plane proportions shaped by clothing, pose, crop, lens, focus, blur, lighting, shadow, and occlusion. Do not infer hidden anatomy under clothing, props, hands, arms, hair, shadow, blur, or crop.

If the subject is not clearly adult or age is ambiguous:

- Use neutral non-sexual clothing, posture, and upper-torso silhouette language only.
- Do not emphasize chest, bust, cleavage, hips, or other sexualized body traits.

For clearly adult subjects:

- Treat visible body proportions as ordinary visual facts.
- Describe relevant visible build, shoulder width, ribcage or upper-torso width, calibrated chest/bust/upper-torso silhouette, waist position and taper, abdomen or midsection if visible, hip width if visible, torso-to-leg ratio, limb scale, and clothing-shaped silhouette.
- Use the weakest accurate calibration supported by the image: `hidden or not visible`, `visible but mostly obscured`, `slight`, `moderate`, `moderate-to-full`, `full`, `large`, `very large`, `broad but low-detail`, `visually dominant because of crop/camera/pose/lighting/clothing`, or `visually secondary despite being visible`.
- State whether visible volume is silhouette-defined, clothing-shaped, shadow-defined, self-shadowed, cast-shadow-obscured, contact-shadowed, highlight-defined, rim-defined, flat-lit, backlit, underexposed, overexposed, dark-fabric-obscured, bright-fabric-softened, haze-softened, low-contrast, low-detail, or partially obscured.

Use symmetric calibration locks:

- If a visible adult body feature is large or very large, preserve it against reduction, flattening, averaging, hiding, or modesty/safety correction.
- If it is moderate, moderate-to-full, slight, flat, broad, secondary, softened, low-detail, or obscured, preserve that calibration against enlargement, extra projection, deeper neckline, tighter clothing, added cleavage shadows, added under-bust shadows, stronger highlights, sharper contouring, or increased dominance.
- If hands, phone, arms, hair, fabric, props, another person, cast shadow, self-shadowing, contact shadow, blur, crop, or frame edge partially hide contours, preserve that occlusion instead of revealing or clarifying hidden shape.
- If a feature is visible but not central, describe it as visible but secondary, not as dominant.
- If a feature is visually dominant because of crop, camera angle, lens, pose, lighting, or clothing, state the visible cause rather than inventing hidden anatomy.
- Avoid words that over-sculpt a covered or shadow-obscured body area. If the visible area reads mainly as a dark near-camera garment mass, say `covered near-field torso mass`, `clothing-shaped foreground area`, or `dark fabric plane` instead of repeated anatomy labels such as `chest`, `bust`, `abdomen`, `midriff`, or `waist`, unless those anatomical regions are visibly distinct and central.

Avoid repetition that over-weights body features. Mention a body feature in the body-proportion section, and repeat it in locks or negative prompt only when it is genuinely important to fidelity.

For crop-sensitive, near-frame, or garment/prop-dominant human images, lock relative image-plane widths and areas instead of relying on broad body or fashion labels. Compare visible shoulder/torso width, waist or closure-band width, garment-panel width, prop/accessory width, and nearby fixed anchors such as rails, furniture edges, mirrors, doors, horizons, or frame edges. State whether a visible body or garment region is actually dominant, or only appears prominent because of crop, camera distance, lens perspective, pose, lighting, or occlusion. Prefer visible construction anchors such as seams, pockets, straps, hems, closures, folds, coverage bands, narrow gaps, and cropped edges over repeated anatomy labels when the source is a clothing/crop composition. Prevent the generator from widening, narrowing, sculpting, glamour-posing, flattening, completing, or modestly hiding that silhouette unless those changes are visible in the source.

For close portrait or product-adjacent crops where a held foreground object, package, cup, phone, toy, bouquet, charm, ornament, or other small prop overlaps the torso or face, treat the prop as a measured foreground anchor rather than a category label. Lock its bounding box, top edge, bottom edge, hand overlap, rotation, visibility budget, and scale relative to the face, shoulders, nearby body regions, and crop. If tiny decorative figures or attachments sit on the prop, describe them as small attached ornaments with their actual count, silhouette height, and low-detail material treatment; do not let the wording promote them into full separate subjects. Put these locks in `PROMPT:` affirmative language, because downstream generation may ignore `NEGATIVE PROMPT:` and `RECOMMENDED SETTINGS:`.

When a foreground prop is important but not larger than the face or head mass, calibrate its image-plane dominance explicitly. Compare prop width to face width, prop height to head height, prop area to visible torso or surface area, and prop top edge to chin, neckline, chest, hand, or nearby object anchors. If the prop is secondary or co-dominant, say so; do not make it sound like a product hero. Avoid phrases such as `dominates`, `large foreground product`, or repeated ornate material detail unless the prop truly dominates the source. If the prop has a label, bow, charm, small attachment, or miniature figure, keep those details subordinate to the prop's measured size instead of allowing them to enlarge the whole prop.

If a prop contains many small details, do not let detail count imply larger scale. Write the prop's measured footprint once, then group fine details as small low-legibility surface, edge, or attachment details unless they are individually central. Repeating miniature attachments, labels, bows, filigree, charms, text, patterns, and material terms can overweight the prop and cause a product-shot result; keep detailed props subordinate to the source's face, crop, or primary-concept hierarchy.

For shoulder-and-upper-torso portrait crops, audit side-specific skin and fabric visibility separately. Record viewer-left and viewer-right shoulder edge positions, strap positions, neckline or collar-band height, hair coverage, shadow coverage, and whether exposed skin is secondary to face, prop, accessory, or crop anchors. When one shoulder or upper-torso area is visible but not the subject, say it remains a cropped, partially shadowed side plane; avoid broad wording that could expand it into a cleaner fashion neckline, wider torso reveal, symmetrical exposed shoulders, or glamour pose.

For side-edge shoulders and upper arms, distinguish a shoulder cap, a narrow upper-arm strip, and a full visible arm. If the source shows only a cropped shoulder plane or partial upper-arm edge, lock it as a side-edge visibility budget with coordinates and shadow, strap, hair, prop, or crop interruptions. Do not use generic `bare arm`, `exposed arm`, or `off-shoulder` language unless the arm is actually a full subject element; those labels often expand the side edge into a clean portrait arm.

For layered clothing, exposed/covered gaps, or repeated visual bands, preserve band height as carefully as width. State the y-position and height of garment edges, material transitions, visible gaps, fasteners, prop bands, lower or side-edge bands, and frame crop boundaries as separate image-plane bands when they affect likeness. Compare each band against adjacent fixed anchors such as surface lines, horizons, rails, tables, mirrors, furniture seams, or frame edges. Do not describe narrow or secondary bands as broad regions unless they visibly occupy that much of the frame. Treat band-height drift as a major fidelity failure.

## Pose, Occlusion, and Clothing

For each visible person, describe precise mechanics rather than only generic pose labels:

- Body crop and visible body parts.
- Head direction, head tilt, chin angle, gaze, neck visibility, shoulder line angle, torso orientation, twist, lean, posture, and spine/action line.
- Shoulder height difference, hip height difference, weight distribution, arm direction, elbow bend, forearm angle, wrist angle, hand placement, finger visibility, object grip, leg placement, knee bend, ankle/foot placement, and negative space.
- Occlusion relationships between limbs, clothing, body, face, objects, cast shadows, self-shadowing, contact shadows, blur, and crop.
- Approximate pose landmark coordinates when helpful.

Describe clothing as it affects visible silhouette:

- Fit, fabric type and thickness, opacity/transparency, stiffness/looseness, fabric tension, wrinkles, folds, neckline depth and width, strap position, sleeve position, seam placement, waist seam, under-bust seam if visible, buttons, lace, pattern scale, garment layers, and interaction with body shape and pose.
- Prefer visible garment geometry over broad fashion-category labels when fidelity matters. If a category label such as dress, crop top, off-shoulder, uniform, robe, jacket, or swimsuit would cause the generator to normalize the garment, describe the exact visible edges, coverage bands, straps, sleeve openings, crop boundaries, fabric opacity, and occlusions first, and use the category label only as secondary shorthand.
- Do not let a broad garment or portrait label dominate the first sentence when the source depends on awkward crop, low camera angle, partial visibility, or non-editorial styling. Put the visible coverage geometry and camera crop first, then use the category label only after those constraints are established.
- Create a coverage map for exposed skin, fabric, and occluded regions when clothing placement is important. State which image regions are skin, which are fabric, which are shadow-hidden, and which must remain outside the crop. Reject expanding exposed skin or completing hidden garment/body regions beyond the source.
- Do not make clothing tighter, looser, more structured, more corseted, more revealing, more transparent, more padded, more lifted, more sculpted, more modest, more fashion-editorial, more lingerie-like, more body-hugging, or more generic than the source.

For close upper-torso crops with scoop necklines, collars, straps, hems, shirt openings, jackets, or layered garment edges, treat the visible edge as a measured boundary band rather than a fashion label. Lock the neckline or garment-edge width, lowest y-position, visible skin or underlayer area above and below it, sleeve or shoulder fabric area, and bottom crop. If the source is covered or only mildly open, avoid words that can deepen the neckline, lower a garment edge, or recenter the torso; phrase the region as an opaque garment boundary, covered torso plane, or interrupted edge band when that is what the source shows. Reject deeper neckline drift, larger exposed skin bands, tighter fabric, added contour emphasis, and any attempt to make the torso a cleaner fashion subject when it is secondary to another visual concept.

When a neckline, collar, or garment opening is dark, shadowed, cropped, low-contrast, or interrupted by hair, prop, jewelry, accessory, hand, or blur, describe it as an interrupted covered band before using any fashion category. Avoid `low neckline`, `off-shoulder`, `camisole`, `dress`, `lingerie`, or similar labels if they would invite a wider, clearer, deeper, or more centered exposed region than the source. The positive prompt should state the visible covered band and occluders, not only negative exclusions.

For chokers, collars, necklaces, straps, lace trim, bows, and shoulder accessories in tight portraits, describe only the visible silhouette and approximate density. If the source accessory is dark, low-contrast, partly hidden by hair, shadow, blur, or foreground objects, do not upgrade it into a crisp ornate necklace, symmetrical pendant system, decorative collar set, or clean fashion accessory. Lock whether the accessory is a narrow band, scalloped edge, bead cluster, dangling center detail, loose tie, or shadowed texture, and preserve its incompleteness and low legibility.

When a foreground object, hair mass, arm, hand, prop, shadow, blur, or crop hides part of a neckline, shirt opening, garment hem, or upper torso, make that occlusion part of the clothing map. State which garment edges are interrupted, softened, shadowed, cropped, or blocked, and prevent the generator from lowering, widening, clarifying, or completing the garment edge in a way that shows a larger uninterrupted skin or fabric area than the source.

For flat graphic accessories, stickers, printed marks, cel-shaded overlays, decals, patches, or stylized props attached to or overlapping a photoreal subject, describe their graphic flatness, simplified shape, outline style, color patches, limited shading, and medium contrast before giving the object category. Prevent the generator from converting them into realistic physical props, botanical objects, jewelry, polished 3D accessories, or clean product graphics unless the source visibly has that material realism.

When a graphic accessory or stylized overlay overlaps a real subject, put its medium constraints in the first mention. Lock the accessory's simplified contour, outline, shape count or part count if visible, color-block treatment, low-realism shading, and exact overlap with the real subject. If related stems, leaves, labels, marks, or secondary shapes share the same graphic treatment, lock them as part of the same flat overlay rather than separate realistic objects.

Preserve occluding elements and their shadows. Do not move hands, phones, arms, hair, bags, props, shadows, blur, another person, clothing folds, or crop edges in a way that reveals more body, hides different areas, or clarifies hidden anatomy. Preserve shadows from clothing folds, hair, arms, hands, props, and background structures as separate visible evidence from the occluding objects that create them.

For crop boundaries, state the visible absence. If hands, feet, waist, hips, lower body, object ends, background details, or text are outside the frame or only barely visible, say so directly and keep them cropped, narrow, or secondary. Do not use wording that would encourage the generator to reveal, center, enlarge, complete, or beautify the missing or partial area.

For every boundary-sensitive crop, include both positive and negative wording: the positive prompt states exactly what remains visible and how much frame area it occupies, while the negative prompt rejects expanded visibility, recentered missing parts, completed limbs, completed bodies, extra exposed bands, extra readable text, and moved occluders.

For partial turned-face portraits, including over-shoulder, mirror, profile-glimpse, reflection, screen, or occluded-face views, distinguish the actual face evidence from a generic clean portrait. State whether the visible face is frontal, strict profile, partial three-quarter, small cheek-and-eye glimpse, mostly hidden by hair/objects/shadow, or only a narrow facial sliver. Lock face size relative to the head, hair, body, frame, or containing surface; visible gaze direction; nose/lip/chin/eye visibility; occlusion; and whether the head turn reads candid, posed, reflected, screened, or interrupted. Reject turning a small obscured glance into a cleaner, larger, more frontal, brighter, or more complete face than the source supports.

For small, partial, or occluded faces in portraits, reflections, screens, mirrors, background layers, or over-shoulder views, create a face exposure budget. State which facial features are visible, hidden, cropped, shadowed, blurred, or obscured; how much frame area the face occupies relative to the head, hair, body, containing surface, or nearby anchors; and which tempting features must remain absent or ambiguous. If the source supports only a small glance or facial fragment, avoid enough feature enumeration to invite a larger clean portrait, clearer far eye, more exposed cheek or jaw, brighter beauty lighting, or a more readable expression than the source supports.

For over-shoulder glances, separate head turn from facial exposure. State whether the viewer sees a cheek-and-nose sliver, a partial three-quarter face, or a nearly frontal face. If the source only shows a small side-leaning glimpse, reject direct eye-contact glamour, a large centered face, two fully clear eyes, fully lit cheeks, and a portrait-style head angle.

For small side-profile or over-shoulder faces, lock the gaze geometry as image-plane evidence. State whether the nose points left or right, how much of each eye is visible, whether the far eye is hidden by hair/shadow/profile angle, and whether the mouth reads as a small side contour. Reject turning this into a clearer direct-gaze portrait even when the source appears to look toward the camera.

If the source face reads closer to a side profile than a portrait glance, lead with the profile evidence before any gaze wording. A tiny visible eye or cheek highlight should not be enough to request direct eye contact. Prefer `small side-profile facial sliver`, `near eye barely readable`, and `gaze ambiguous through shadow` over `looking at camera` when the camera-facing evidence is weak.

For contact gestures where a hand, limb, hair, clothing, tool, prop, or other occluder touches or grips another visible element, describe the contact as a spatial relationship, not just as a generic gesture. Lock approximate size, angle, visible fingers or endpoints, contact point, compression, overlap, hidden portions, loose or displaced material, and where the interacting element begins and ends. If the source bounds length, volume, or reach by crop or occlusion, state those limits and prevent a longer, smoother, cleaner, heavier, more complete, or more stylized replacement.

When a body area or garment gap is only a thin bottom-edge or side-edge sliver, avoid making it sound like a subject. Prefer wording such as `a narrow edge band/gap remains at the crop boundary`, `a thin skin-toned edge strip`, or `a barely visible cropped gap` over labels such as `visible abdomen`, `visible midriff`, or `visible waist` unless that area is actually central and materially visible. If a prompt uses a body-part label for a sliver, immediately qualify that it is not a subject region and should not expand inward.

If the source garment is cropped near the bottom and a broad clothing category such as `crop top` would invite a fashion-style exposed abdomen composition, describe the visible hem and frame cut first, and use the category label only as secondary shorthand or omit it when the hem/crop is the important evidence. Never let bottom-edge garment wording imply that the lower body should be completed or that a larger skin band should be centered.

For small text marks, logos, labels, signatures, UI text, or incidental lettering, preserve location, size, contrast, and readability level over exact transcription unless the exact readable text is central to the image. If it is small, partial, distorted, or low confidence, describe it as an indistinct mark and prevent the generator from enlarging it or turning it into prominent clean typography.

For watermarks, product labels, package labels, background signs, reflected marks, engraved marks, and decorative monograms in photographic scenes, distinguish text-plane role from exact text content. If the mark is secondary, soft, transparent, curved, reflected, low-resolution, or partially legible, write it as a faint graphic or label artifact with approximate placement and legibility ceiling. Do not over-transcribe low-confidence letters in `PROMPT:` unless exact readability is central; over-transcription often makes generators create a crisp logo, clean sign, or new prominent text object.

For incidental text that is visible but compressed or small, lock it as low-legibility. Do not request crisp typography unless the source clearly centers readable text as the subject.

When incidental UI text is clearly readable despite being small, preserve the exact visible characters and their low-legibility rendering together. Do not let the generator substitute a plausible different time, placeholder, number, brand, or label. Exact text locks should still emphasize small size, soft edges, and secondary priority, not clean typography.

When incidental text is near a garment or object edge, describe it as a small, soft mark anchored to that edge. Avoid repeating the exact text in ways that make the model prioritize clean lettering over edge placement, size, softness, and low contrast.

For incidental interface overlays, screenshot controls, camera controls, reaction marks, low-confidence symbols, small badges, or cropped graphic marks, preserve them as low-legibility artifacts unless their exact symbol is central and clearly readable. Describe approximate shape, size, opacity, edge distance, internal contrast, and ambiguity. If the internal mark is unclear, call it an abstract mark rather than a named icon, arrow, logo, or app control. Reject conversion into clean readable typography, a brand mark, a watermark, a caption, or an enlarged interface element.

For progress lines, scrub bars, separators, or edge slivers, preserve the observed length and discontinuity. If the source shows only a tiny partial line at an edge or a short pale segment, do not describe it as a full progress bar; explicitly reject full-width bars, timeline tracks, knobs, home indicators, or completed app controls unless they are visible.

For ambiguous tiny UI edge marks that are not central to recognition, do not over-promote them in `PROMPT:`. It is safer to say that no full progress bar or timeline is visible than to positively request a mark that may expand into a complete control. Mention the tiny mark only as a cropped edge artifact when it is visually clear and bounded.

For secondary objects such as bags, straps, jewelry, tools, handheld items, furniture fragments, signs, UI controls, props, or cropped products, create a secondary-object budget. Lock edge distance, bounding box, overlap with the primary subject or containing surface, visible crop, occlusion, and relative size against nearby body, object, frame, or background anchors. If the object is secondary or edge-adjacent in the source, describe it as partial, tucked, compressed, low-priority, obscured, or low-detail as supported by evidence; prevent it from becoming larger, cleaner, front-facing, product-like, fully readable, or more central than the source.

Identify completion-prone regions before drafting: partially cropped bodies, partial garments, partial faces, partial text, partial posters/screens/reflections, cut-off limbs, and border-adjacent areas. In `PROMPT:`, lock each such region as partial or cropped; in `NEGATIVE PROMPT:`, reject completing, recentering, expanding, or clarifying those regions.

## Camera, Focus, Lighting, and Medium

For photographic images, describe how the camera captured the scene:

- Camera distance, camera height, camera angle/rotation, lens impression, perspective distortion, subject-to-camera relationship, and how perspective affects apparent face/body/object/background proportions.
- Wide-angle or close-camera foreground enlargement, edge stretching, foreshortening, barrel-like distortion, or minimal distortion only when visible.
- Telephoto compression only when visible.
- Low-angle elongation or high-angle compression only when visible.
- For close low-angle or high-angle captures, state the image-plane scale hierarchy explicitly: which plane is nearest, which body/object region dominates the lower or upper frame, whether the face is relatively smaller/larger than expected, and which cropped regions must stay outside the frame. Preserve this hierarchy before any conventional portrait or product-photo balance.
- If the source has extreme perspective but not an extreme body-feature emphasis, separate `near-camera scale` from `anatomical size`. Describe the nearest covered surface as large in the image plane because of lens and crop, while preventing rounded, sculpted, exposed, or glamorized anatomy from replacing the flatter source evidence.
- Focus target, focus accuracy, depth of field, focus clarity, bokeh, foreground blur, background blur, low-resolution softness, digital sharpening, compression, noise reduction, bloom, haze, and which planes are relatively most in focus or blurred.
- Motion blur, camera shake, shutter behavior, ghosting, smear direction, rolling-shutter artifacts, or stable no-blur capture.
- Camera/sensor/medium impression: smartphone rear-camera snapshot, front-camera selfie, compact camera, disposable-camera-like, 35mm-like film, instant-film-like, webcam, CCTV, low-light phone image, social-media compression, professional digital camera, documentary photo, clean digital photo, or other visible look.

Describe lighting-to-volume:

- Main light direction, intensity, softness, temperature, fill, bounce, rim light, backlight, flash, practical light, window light, screen light, neon, daylight, or ambient light when visible.
- Highlight placement, shadow falloff, black-level handling, bright-fabric bloom, dark-fabric absorption, local contrast, haze, clipped highlights, lifted shadows, crushed shadows, underexposure, or overexposure.
- For visible shadows that materially affect likeness, composition, occlusion, or surface separation, note the apparent caster, receiving surface, shadow shape, edge softness or hardness, density, direction, falloff, and color cast when supported by visible evidence.
- When useful, distinguish self-shadowing on visible surfaces such as faces, hair, clothing, body contours, and objects from cast shadows made by clothing, folds, hair, arms, hands, props, architecture, background structures, or the frame boundary.
- State how shadows affect visible edges, detail, separation, and occlusion without inferring new structure from shadowed areas.
- How lighting affects face structure, skin texture, clothing texture, object shape, visible body contour, and perceived body volume.
- Do not relight the scene into cleaner, brighter, more commercial, more frontal, more beauty-oriented, more contrasty, more cinematic, more sculpted, more exposed, or more evenly lit lighting if that changes apparent proportions or face structure.

## Background and Color

Describe the background by zones:

- Left side, right side, top, bottom, foreground, midground, and background.
- Include only visible location type, architecture, nature, furniture, props, street details, interior details, weather, time of day, practical lights, reflections, shadows, background figures, vehicles, plants, signs, windows, doors, textiles, surfaces, and objects.
- If background objects are blurred, minor, or indistinct, say they remain blurred, minor, indistinct, soft silhouettes, or heavily defocused. Do not over-specify barely visible objects.
- Describe whether the background separates from or blends with the subject silhouette.

For soft, distant, degraded, or low-legibility background layers, preserve massing before category. Describe blurry blocks, horizon bands, rhythm of repeated shapes, silhouette layers, transition lines, absent object classes, and softness level before asking for a generic scenic or realistic version of the location. If people, vehicles, signs, readable windows, landmarks, lights, or distinct small objects are not visible, explicitly keep them absent, indistinct, cropped, or low-priority. Prevent the generator from replacing a soft blocky background with a sharper postcard-like panorama, cleaner room, clearer street, or more complete environment.

Describe color and mood:

- Dominant palette, color grading, white balance, saturation, contrast, global cast, skin tone rendering, color imperfections, mixed lighting, film color shift, digital color noise, and emotional tone.
- Preserve whether the image reads as warm, cool, neutral, muted, pastel, high-contrast, low-contrast, faded, nostalgic, candid, raw, ordinary, elegant, dramatic, mysterious, intimate, documentary, chaotic, surreal, polished, accidental, quiet, glamorous, or understated.

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
