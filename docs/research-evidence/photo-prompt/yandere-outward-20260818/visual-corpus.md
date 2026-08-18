# Outward yandere visual shorthand: 24-image web convenience corpus

Date: 2026-08-18  
Unit of analysis: one search-result image, coded from inspected pixels  
Sample: 24 distinct images, split evenly across three deliberately chosen strata

## Scope and limits

This is a **purposive convenience sample of image-search results**, not a random sample and not evidence of population frequency. Counts below mean only “present in this 24-image sample.” Search ranking, query wording, reposting, tagging, SEO, and the availability of directly inspectable images all shape the sample.

The strata are:

- `C01–C08`: recognizable existing anime/game characters, production frames, or official-art-like game visuals. Several files are on secondary hosts, so this stratum describes recognizable visual content, not authenticated rights provenance.
- `F01–F08`: fan, editorial, playlist/avatar, or platform explanatory imagery. This stratum includes AI-generated platform images where the result page identified them as such.
- `N01–N08`: nurse/syringe variations, deliberately oversampled to test whether medical shorthand carries “yandere” by itself.

Exact duplicate reposts and obvious crops of the same source image were excluded. Each retained image was opened and inspected at pixel level from a temporary directory outside the repository. No copyrighted image file is stored here; only remote URLs and coded observations are recorded.

### Coding legend

- **Gaze:** `viewer` means camera/viewer-directed; `person` means a visible other person; intensity is `high`, `medium`, or `soft`; `closed/off` means no fixed visible gaze.
- **Eyes/lids:** records lid opening and non-natural emphasis such as heart pupils, glow, tiny pupils, slit pupils, blank irises, or extreme scleral exposure.
- **Mouth / blush / shadow:** `asym.` means a visibly crooked or one-sided mouth; shadow is local facial/eye shadow, not merely a dark background.
- **Pose/distance:** `intrusive` means an extreme close crop, a lean into another person's space, low patient-POV looming, contact, or foreground intrusion.
- **Target:** `visible`, `implicit viewer`, or `absent/off`.
- **Target action:** `yes` only when body, hand, or implement crosses into a visible/implicit target's space; merely holding a prop is `no`.
- **Residual:** coder judgment after mentally removing blood, weapon-like implements (including syringes), and text: `Y` still yandere-coded, `A` ambiguous, `N` no. “Yandere-coded” is a visual reading, not a claim about character canon.

## C — recognizable anime/game visual content

| ID | Remote image URL | Gaze | Eyes/lids | Mouth / blush / facial shadow | Pose and distance | Target | Target action | Prop/horror shorthand | Residual |
|---|---|---|---|---|---|---|---|---|---|
| C01 | [URL](https://secure.static.tumblr.com/15c8c48a0996cd224753501426f9c8d6/9i8ej7k/SE5n6o8n1/tumblr_static_45rwfwds1iw44co0kkgc8sssc_1280_v2.jpg) | viewer, high | wide; luminous/highlighted irises | parted, near-symmetric; diffuse blush; no local shadow | frontal tight close-up; both hands press cheeks; intrusive | implicit viewer | no; self-framing | no weapon/blood/text; purple monochrome wash | `Y` — fixed luminous gaze + flush + cheek-clutch already reads obsessive/lovestruck |
| C02 | [URL](https://vignette.wikia.nocookie.net/yandere-simulator/images/8/8f/AyanoOficialPage2.png/revision/latest?cb=20161009181544&path-prefix=es) | viewer, medium | normal opening and pupils | neutral symmetric mouth; blush; no shadow | upright full body; hand at collar; non-intrusive | implicit viewer | no | school uniform only | `N` — ordinary shy/neutral school portrait |
| C03 | [URL](https://n.sinaimg.cn/sinacn/w1600h900/20180123/b05f-fyqwiqi8941165.jpg) | viewer, high | half-lidded/narrow | small asym. smirk; no blush; heavy eye/face shadow | head lowered and tilted; forward lean; saw dominates foreground; intrusive | implicit viewer | yes; saw crosses viewer axis | bloodied saw, night rooftop, hard glint | `A` — still ominous, but love/possession is no longer visible |
| C04 | [URL](https://i0.wp.com/www.animefeminist.com/wp-content/uploads/2023/05/Higurashi-No-Naku-Koro-Ni-Anime-Shion-Sonozaki-laughing.png?ssl=1) | viewer, high | extreme scleral exposure; tiny pupils | very wide open mouth; no blush; deep under-eye shadow | extreme face close-up; intrusive | implicit viewer | no | facial blood, black background | `N` — manic horror remains, not love-specific obsession |
| C05 | [URL](https://cdn.gaminggorilla.com/wp-content/uploads/2023/02/Best-Yandere-Anime-Characters-Anna-Nishikinomiya.jpg-768x434.jpg) | viewer, high | wide; sparkling pink irises | slightly asym. parted/drooling mouth; heavy blush; no shadow | forward tight close-up; both hands cup face; intrusive | implicit viewer | no; self-framing | no weapon/blood/text | `A` — intense desire is visible, but possessive danger is not |
| C06 | [URL](https://ogre.natalie.mu/media/news/comic/2018/0621/HS01_088_t3_0001.jpg?imdensity=1&imwidth=750) | viewer, soft | normal glossy eyes | small symmetric smile; blush; no shadow | tilted close portrait; non-intrusive | implicit viewer | no | none | `N` — gentle affection only |
| C07 | [URL](https://image.kddi-video.com/3b4/3b4d17efa943ffe6ef0d55321057454e/fit-background-transparent/1463773941/1080x608.png) | person, high | narrowed/intent toward the other person | parted speech mouth; no blush; no shadow | torso crosses table; hand planted near other person; intrusive | visible | yes; leans into his space | no horror prop | `N` — a forceful conversation without the story context |
| C08 | [URL](https://staticg.sportskeeda.com/editor/2022/08/0d978-16598123106554-1920.jpg) | closed; attention oriented to person | closed lids | small symmetric smile; no clear blush; no shadow | face-to-face contact; hand encloses target's head; intrusive | visible | yes; face hold/kiss | no horror prop | `N` — dominant/intimate romance, not visually possessive danger |

## F — fan/editorial/explanatory imagery

| ID | Remote image URL | Gaze | Eyes/lids | Mouth / blush / facial shadow | Pose and distance | Target | Target action | Prop/horror shorthand | Residual |
|---|---|---|---|---|---|---|---|---|---|
| F01 | [URL](https://img.youtube.com/vi_webp/EBmhxfZAl8A/maxresdefault.webp) | viewer, high | heart pupils; slightly lowered upper lids | asym. toothy grin; no clear blush; no shadow | tilted extreme close-up; knife spans foreground; intrusive | implicit viewer | no; weapon displayed laterally, not aimed | hearts, flowers/ribbons, bloodied knife, facial blood | `Y` — heart-fixed gaze + predatory smile survives removal |
| F02 | [URL](https://i1.sndcdn.com/artworks-vaK6t7AnhwdgRJyz-IwNczA-t1080x1080.jpg) | viewer, high | one eye hidden; other narrow/glowing red | asym. smirk; no clear blush; dark face shadow | close frontal portrait; heart-sealed letter pressed to cheek; intrusive | implicit viewer | no; symbolic display only | heart letter, bloody hand, knife, red/black field | `A` — targeted affection remains, but danger becomes uncertain |
| F03 | [URL](https://dthezntil550i.cloudfront.net/yo/latest/yo1807252031490620005842325/1280_960/332f9829-be91-48df-8341-55c86e31d1a7.png) | viewer, high | extreme wide heart pupils | broad near-symmetric fanged grin; heavy blush; no shadow | frontal tight crop; hand frames eye; cleaver in foreground; intrusive | implicit viewer | no; weapon displayed, not aimed | heart doodles, bloodied cleaver | `Y` — heart pupils + fixed stare + blush/grin remain |
| F04 | [URL](https://dthezntil550i.cloudfront.net/hi/latest/hi1809301809096110001677968/1280_960/5d6a5bb5-abff-4baf-b55f-bc5d6dadbecf.png) | viewer, high | half-lidded pale irises | asym. drooling/trembling smile; blush; dark eye-band shadow | frontal medium portrait; non-intrusive | implicit viewer | no; knife held down at side | heart doodles, sweat, bloody knife | `Y` — affection graphics + fixed shaded eyes + unstable smile remain |
| F05 | [URL](https://dthezntil550i.cloudfront.net/vd/latest/vd1803300420075540005274181/1280_960/7bd38675-a08f-4e0b-a001-33c2ffa2911d.png) | viewer, medium | one eye hidden; visible eye otherwise normal | small symmetric smile; blush; no shadow | tilted full-body pose; non-intrusive | implicit viewer | no; knife rests at shoulder | knife, blood, handwritten love/death text | `N` — shy schoolgirl pose after removing the explicit labels |
| F06 | [URL](https://dthezntil550i.cloudfront.net/rv/latest/rv2410010604482440008703509/64bf5a92-b7d2-414b-bef4-85e3ddc03ade.jpg) | viewer, high | wide heart pupils; one eye framed by fingers | huge asym. fanged grin; mild blush; no shadow | low-angle extreme close-up; blade fills foreground; intrusive | implicit viewer | no; blade is lateral display rather than an aimed act | hearts, pills, bandages, teddy/flowers, serrated knife | `Y` — heart-fixed gaze + exaggerated private grin remain |
| F07 | [URL](https://cdn.polyspeak.ai/speakmaster/a5c33233f94292b339900307517d1d5a.webp) | viewer, high | ultra-wide heart pupils | broad near-symmetric grin; heavy blush; no shadow | close frontal crop; both fists under cheeks; intrusive | implicit viewer | no; knife stays behind head | floating hearts, knife, small blood marks | `Y` — fixed heart eyes + blush + cheek-clutch/grin remain |
| F08 | [URL](https://shapes.inc/api/public/avatar/yanderegirlsakura) | viewer, high | wide heart pupils; tears/highlights | mouth hidden by gloved hands; blush obscured/uncertain; dark eye surrounds | tight frontal avatar; hands cover lower face; intrusive | implicit viewer | no; pencil remains beside own cheek | facial blood, bandages, bloodied pencil, horns, hearts | `A` — obsessive affect remains, but danger becomes uncertain |

## N — nurse/syringe variations

| ID | Remote image URL | Gaze | Eyes/lids | Mouth / blush / facial shadow | Pose and distance | Target | Target action | Prop/horror shorthand | Residual |
|---|---|---|---|---|---|---|---|---|---|
| N01 | [URL](https://upload-os-bbs.hoyolab.com/upload/2024/02/05/98387867/0c59922001b97da26c0baac729073985_1861698490863666894.png?x-oss-process=image%2Fauto-orient%2C0%2Finterlace%2C1%2Fformat%2Cwebp%2Fquality%2Cq_80) | viewer, medium | normal wide glossy eyes | open symmetric smile; strong blush; no shadow | low patient-POV; torso leans over viewer; intrusive | implicit viewer | yes; syringe readied above patient/viewer | syringe, clipboard, blood-stained curtains, clinical room | `N` — cheerful leaning nurse after removing medical/horror cues |
| N02 | [URL](https://i.imgur.com/68gXxun.jpeg) | viewer, high | one heart pupil; other eye obscured | asym. tongue-out grin; blush; one side visually occluded | tilted three-quarter medium shot; non-intrusive | implicit viewer | no; syringe displayed to side | syringe, vials/tray, red cross, blood, bandages/eye cover | `Y` — heart-fixed eye + blush + unstable grin remain |
| N03 | [URL](https://images-ng.pixai.art/images/orig/f6d74311-520b-45f0-9c76-b6ce60d70c28) | viewer, high | wide heart pupils inside flat gray irises | tiny pout/flat mouth; blush; no shadow | close frontal portrait; non-intrusive | implicit viewer | no; syringe held beside cheek | syringe, bandages, heart cap, tiny blood spot | `A` — obsessive/lovestruck, but threat/possession is weak |
| N04 | [URL](https://image.cdn2.seaart.me/2025-06-20/d1aaao5e878c73b7gnpg/fe4badf3874ed124d3724ccf22984a530a91e732_high.webp) | viewer, high | luminous slit-like pink pupils | asym. fanged smile; blush; low-key face shadow | close frontal portrait in dark corridor; non-intrusive | implicit viewer | no; syringe vertical against own torso | syringe, fangs, dark corridor | `N` — generic predatory/monster nurse, not love-specific |
| N05 | [URL](https://animextra.net/cdn/shop/files/mikan11x17noblood.png?v=1689907058&width=1445) | viewer, medium | normal purple irises | asym. toothy smile; no clear blush; hair/upper-face shadow | three-quarter medium/full pose; non-intrusive | implicit viewer | no; syringe held near own head | syringe, claw-like second arm, hospital, ambiguous purple stains | `N` — eccentric nurse/horror styling without possessive relation |
| N06 | [URL](https://66.media.tumblr.com/eca001d4273b50eb5c03979e74df6006/tumblr_p29z43BjDM1u8gax7o2_r2_400.jpg) | viewer, high | wide glowing pink eyes | open mouth; no blush; dramatic green top/eye shadow | low patient-POV; forward lean; hand planted in foreground; intrusive | implicit viewer | yes; syringe readied while looming over patient/viewer | syringe, hard clinical spotlight, dark room | `N` — monster/medical horror, not affection or possession |
| N07 | [URL](https://ih1.redbubble.net/image.992370904.1944/flat%2C750x%2C075%2Cf-pad%2C750x1000%2Cf8f8f8.u1.jpg) | off/upward, medium | normal half-lidded eyes | small asym. fang smile; blush; under-eye shadow | kneeling full-body pose; non-intrusive | absent/off | no | giant syringe silhouette, heart specks, bandages, pink pool | `N` — fragile/shy nurse styling after removal |
| N08 | [URL](https://merch.kawaentertainment.com/cdn/shop/files/cohposter2.png?v=1690602014&width=1445) | viewer, high | half-lidded; pink slit pupils | mouth hidden/flat; no blush; mild eye shadow | frontal medium/full portrait; non-intrusive | implicit viewer | no; syringe held horizontally across own face | syringe, monster-filled clinical backdrop | `N` — stern horror nurse, no affection marker |

## Within-sample counts

These are descriptive audit counts, **not estimates of how often a cue occurs in yandere imagery generally**.

| Coded feature | C (n=8) | F (n=8) | N (n=8) | Total (n=24) |
|---|---:|---:|---:|---:|
| Gaze aimed at viewer or visible person | 7 | 8 | 7 | 22 |
| High-intensity fixed gaze | 5 | 7 | 5 | 17 |
| Non-natural/high-emphasis eye treatment | 3 | 6 | 5 | 14 |
| Clear blush | 4 | 5 | 5 | 14 |
| Explicit heart/love graphic motif | 0 | 8 | 3 | 11 |
| Clear mouth asymmetry/crookedness | 2 | 4 | 4 | 10 |
| Local eye/face shadow | 2 | 3 | 4 | 9 |
| Intrusive close/contact/POV composition | 6 | 6 | 2 | 14 |
| Another target visibly present | 2 | 0 | 0 | 2 |
| Strict target-directed action | 3 | 0 | 2 | 5 |
| Cutting/weapon-like implement or syringe | 1 | 8 | 8 | 17 |
| Explicit blood/blood-like mark | 2 | 7 | 3 explicit + 1 ambiguous | 12 explicit + 1 ambiguous |
| Affection marker (blush or heart motif) | 4 | 8 | 5 | 17 |
| High fixed gaze + affection marker + threat shorthand | 0 | 7 | 3 | 10 |
| Residual `Y / A / N` | 1 / 2 / 5 | 5 / 2 / 1 | 1 / 1 / 6 | 7 / 5 / 12 |

The near-universal viewer/person gaze (`22/24`) is partly a portrait-search artifact. More diagnostic in this sample is **co-occurrence**, not gaze alone: `10/24` combine high fixed attention, an affection surface, and a threat cue. Seven of those ten are in the deliberately trope-dense fan/editorial stratum. Only `5/24` depict a strict action entering a target's space, and only two show the target at all.

## Recurring cue bundles

1. **Affection surface + fixed attention + threat.** Fan/explanatory images compress blush or hearts, viewer-locked eyes, and a knife/blood cue into one frame. The affect says “love,” the gaze says “you specifically,” and the implement says “unsafe.” Any one component alone is weak.
2. **Affection surface + fixed attention + self-framing.** Hands pressing cheeks, fingers framing an eye, a head tilt, and a private smile make attention feel absorbed even without action. C01 and the strongest residual fan images retain the reading after weapon removal.
3. **Fixed attention + distance violation/contact.** Leaning across a table, looming from patient POV, holding a target's face, or occupying an extreme close crop supplies relational pressure. It works better when paired with affection; without it, the result is often ordinary confrontation, romance, or medical horror.
4. **Expression mismatch.** A warm blush or smile paired with very wide/flat/heart eyes, a shaded eye band, a crooked mouth, or an unusually steady gaze creates the “pleasant surface / unsafe commitment” contrast. Blood is not required for this mismatch.
5. **Medical variant.** Nurse clothes and a syringe efficiently establish role and vulnerability, but they do not establish yandere. In this nurse stratum, six of eight become generic cute, sensual, monster, or medical-horror nurses after the syringe/blood is removed. N02 is the only clear residual `Y`; it retains heart-focused attention, blush, and an unstable smile.

## Fixed attributes versus relational evidence

Hair color, hairstyle, school uniform, nurse uniform, red/pink palette, body type, and character identity are **fixed or genre-level attributes**, not recurring yandere evidence. The corpus includes pink, black, green, white, blue, and brown hair; no hair color carries a stable reading. Uniforms mostly index “school” or “clinic.”

The repeatable outward shorthand is relational and multi-cue:

> apparent affection + unusually fixed attention on one target + reduced interpersonal distance or target-linked action

Threat props can intensify that bundle, but cannot substitute for it. Blood/weapon without affection reads slasher or horror; hearts/blush without pressure reads ordinary infatuation; direct gaze without either is common portrait grammar. This also explains why a known canonical character can look completely non-yandere in a neutral official portrait or a tender isolated frame.

## Confounders

- **Search conditioning:** queries containing “yandere,” “nurse,” and “syringe” directly favor tagged heart, blade, blood, and medical-prop images.
- **Ranking/reposting:** a few iconic stills recur heavily across hosts. Exact duplicates were removed, but search prominence still affects which visual vocabulary was available.
- **Portrait bias:** image search favors centered faces looking at the camera, inflating viewer-directed gaze and hiding the loved/controlled target offscreen.
- **Fan/AI compression:** fan, avatar, playlist, and AI-platform images are designed for instant tag legibility and therefore stack signs more aggressively than narrative animation frames.
- **Character-knowledge leakage:** recognizing a canonical character can make a neutral frame feel diagnostic. Residual coding therefore used only visible pixels, with C02 retained as a useful identity-without-shorthand negative case.
- **Single-frame loss:** yandere is often established by sequence—monitoring, exclusivity, jealousy, coercion, or harm on behalf of attachment. A still cannot recover those causal relations.
- **Generic horror and sensuality:** blood, fangs, glowing eyes, a syringe, a dark clinic, forward cleavage, blush, or drool can code slasher horror, monster nurse, erotic invitation, or simple lovesickness rather than yandere.
- **Source provenance:** several canonical-looking frames are secondary-host copies. The analysis concerns visible shorthand, not ownership or official-source authentication.
- **Single coder:** judgments, especially `Residual A`, are interpretive. This is an audit sample, not an inter-rater validated annotation set.

## Photorealistic translation

Literal heart pupils, glowing irises, anime blush hatching, or a flat purple eye band are likely to look synthetic in a photograph. Translate their function instead:

- **Fixed attention:** use sustained, target-specific eye contact; restrained blinking; slightly too-still head alignment; normal pupils and catchlights; either subtly raised lids or a deliberate half-lidded stare.
- **Affection surface:** use a restrained flush, moist eyes, a small private smile, gently parted lips, or careful grooming of the target. Keep it plausible and let one mouth corner or the jaw remain tense.
- **Mismatch:** pair a tender mouth with unbroken eye contact, or relaxed words with a hand that grips a little too firmly. Small asymmetry is more photographic than a giant manic grin.
- **Distance/ownership:** show the subject leaning inside normal conversational distance, blocking an exit, holding the target's face/shoulder, keeping a hand on the chair, or orienting the whole torso toward one person while ignoring the room.
- **Make the target legible:** include the loved person's face, shoulder, reflection, reaction, or a clear patient POV. A lone portrait with a knife says “dangerous person”; a target-linked gesture says “dangerous attachment.”
- **Clinical version:** combine credible bedside care with target-specific attention and a syringe or medication that is actually poised in relation to the patient. A clean syringe held beside the face is merely “nurse”; a looming patient POV without affection is merely “medical horror.”
- **Lighting:** use under-brow or one-sided facial shadow, slight catchlight imbalance, and controlled background falloff. Avoid making the entire room horror-coded if the goal is relational obsession rather than a monster/slasher scene.
- **Props:** prefer one believable object and a clear action over blood spectacle. The strongest non-gore translation is warm care + unwavering target focus + a small boundary violation; the prop should clarify the relationship, not carry the concept by itself.

## Practical takeaway

For a single photoreal frame, do not lock the archetype to hair color, schoolwear, nursewear, red eyes, blood, or a weapon. Build at least one cue from each of three functional groups:

1. **Affection:** blush, private warmth, cherished token, careful touch.
2. **Fixation:** gaze or whole-body attention anchored to one target.
3. **Pressure:** too-close distance, controlling contact, blocked movement, or a target-directed act.

Then add horror shorthand only if the intended scene needs explicit danger. In this convenience sample, removing blood/weapon/text leaves only `7/24` clearly yandere-coded and `5/24` ambiguous; the lost cases show why relational cue bundles matter more than decorative threat markers.
