---
id: subject.human
version: 3
priority: 82
type: subject
tier: 2
facet: subject
facet_values:
  - human
  - person
  - portrait
  - face
  - body
  - human-like
triggers:
  - visible person
  - visible human face, hair, skin, body silhouette, or portrait/body crop
avoid_when:
  - no human subject or human-like figure
dependencies:
  - core.visual-evidence
  - core.frame-coordinates
  - core.fidelity-discipline
conflicts: []
provides_anchors:
  - face_fidelity
  - aesthetic_upgrade
  - symmetric_large_body_lock
  - symmetric_moderate_body_lock
  - face_exposure_budget
---

# Subject: human fidelity

## When to load

Load when a real or fictional person is visible. For stylized miniatures, use this only for visible human-like construction cues and combine with miniature modules when applicable.

## Face and non-identifying appearance

Describe a fictional person with similar visible non-identifying appearance. Include only visible evidence:

- apparent age range and gender presentation when visually relevant
- broad apparent visual ancestry or race-coded appearance only when visually evident and useful for preventing drift
- skin tone depth and undertone; pores, shine, matte texture, freckles, moles, blemishes, redness, under-eye shadows, scars, wrinkles, facial hair, makeup level
- face shape and silhouette; forehead, hairline, cheeks, cheekbones, jaw width, jaw softness/sharpness, chin size/shape
- eye size, spacing, shape, eyelid structure, eyelid fold visibility, brow shape/thickness/arch, catchlights, gaze direction
- nose bridge, width, length, tip shape, nostril visibility, frontal/profile/three-quarter impression
- mouth width, lip fullness, cupid's bow, teeth visibility, parted/closed lips, smile/tension
- ears, neck, visible asymmetry, dimples, facial marks, and other non-identifying anchors
- hair color, texture, density, length, parting, bangs, flyaways, volume, curl/wave pattern, and how hair frames or occludes the face

Do not identify the person. Do not upgrade the face into a more symmetrical, generic model-like, influencer-like, westernized, airbrushed, stylized, sanitized, brighter, or differently lit face.

For edge-adjacent or partially cropped faces, describe visible feature status separately from hair, head outline, clothing, props, and frame-edge crop. State whether each important feature group is fully inside frame, partly hidden by hair/hand/shadow/object, or actually cut by the frame: eyes, brows, nose, mouth/lips, cheek edge, chin, jawline, ear, and neck when visible. If only hair or the outer head mass is cropped, prevent the generated face from being sliced through the eyes, nose, mouth, cheek, or chin.

## Body and silhouette

Describe only visible image-plane proportions shaped by clothing, pose, crop, lens, focus, blur, lighting, shadow, and occlusion. Do not infer hidden anatomy under clothing, props, hands, arms, hair, shadow, blur, or crop.

If the subject is not clearly adult or age is ambiguous, use neutral non-sexual clothing, posture, and upper-torso silhouette language only. Do not emphasize sexualized body traits.

For clearly adult subjects, use the weakest accurate visible calibration:

- `hidden or not visible`
- `visible but mostly obscured`
- `slight`
- `moderate`
- `moderate-to-full`
- `full`
- `large`
- `very large`
- `broad but low-detail`
- `visually dominant because of crop/camera/pose/lighting/clothing`
- `visually secondary despite being visible`

State whether visible volume is silhouette-defined, clothing-shaped, shadow-defined, self-shadowed, cast-shadow-obscured, contact-shadowed, highlight-defined, rim-defined, flat-lit, backlit, underexposed, overexposed, dark-fabric-obscured, bright-fabric-softened, haze-softened, low-contrast, low-detail, or partially obscured.

Use symmetric calibration locks: preserve large visible features against reduction, and preserve moderate/secondary/soft/obscured features against enlargement, extra projection, tighter clothing, stronger contouring, or increased dominance.

## Prompt additions

- Put face/hair/skin details after crop, primary concept, and coordinates.
- For partial/occluded faces, create a face exposure budget: visible features, hidden features, frame area, occluders, shadows, blur, and tempting features that must remain absent or ambiguous.
- For partial side-profile or profile-glimpse faces, describe visible geometry and ambiguity before attractive trait lists: nose/lip/chin contour, cheek plane, partial eyelid or hidden eye, softness, crop, and occlusion. Do not enumerate enough features to turn a small or secondary face fragment into a clean beauty portrait.
- For windblown, motion-soft, or heavily occluding hair, describe mass groups, directional clumps, flyaway silhouettes, blur, and occlusion before strand-level texture. Do not repeat shine, gloss, volume, density, salon, or texture wording in ways that enlarges, sharpens, smooths, or glamorizes the hair beyond the source.
- Preserve aesthetic face treatment: expression tension, mouth relaxation, gaze intensity, eye openness, eyelid shadow, skin sheen/matte quality, cosmetic strength, retouching level, candid/ordinary/glamorous/polished/uncanny/unfiltered reading.
- For edge-adjacent faces, add a feature-visibility lock that distinguishes frame crop from occlusion: which facial features stay inside the image, which are blocked by hair/hand/shadow/object, and which are truly outside the frame.
- For body silhouette, describe image-plane proportions and clothing-shaped silhouette without inventing hidden anatomy.

## Negative additions

Reject wrong apparent age range, race-coded appearance when visible, skin tone, face shape, eyelid structure, eye spacing, nose structure, lips, jawline, chin, hair texture, hairline, facial texture, makeup level, face-defining light/shadow, body type, shoulder width, torso/waist/hip silhouette, limb thickness, occlusion drift, beauty drift, influencer face, airbrushed skin, generic model face, hidden anatomy invention, and lighting-caused proportion drift. For edge-adjacent faces, reject confusing hair/head crop with facial-feature crop, slicing through eyes/nose/mouth/cheek/chin when those features are visible in the source, or revealing facial areas hidden by hair, hand, shadow, object, or crop.

## Settings additions

- Face fidelity locks:
- Aesthetic and non-identifying appearance locks:
- Body-proportion calibration locks:
- Adult chest/upper-torso/waist/hip silhouette locks when relevant:

---

# Legacy monolith fidelity rules preserved verbatim

These excerpts are normative. They preserve detailed anti-drift behavior from `legacy/SKILL.monolith.original.md`; do not weaken them when applying this module.


## Legacy Human Subject Fidelity

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


## Legacy human body and silhouette calibration excerpt

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
