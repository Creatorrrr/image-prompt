# Visual search audit: kuudere outward conventions

Audit date: 2026-08-19  
Purpose: identify recurring outward shorthand and its failure modes before translating the researched meaning into prompt data. No source image is copied into the repository.

## Method

Convenience image-search queries:

- `クーデレ キャラクター 一覧 アニメ`
- `kuudere anime characters calm expression`
- `クーデレ 無表情 凛とした キャラ`

The review compared search-result thumbnails and the examples described by the source pages in `source-research.md`. It deliberately separated **visible pixels** from character-canon knowledge. The search was qualitative: there is no claim that the sample is representative, independent, or large enough for frequency estimates.

Representative result pages included:

- https://gamerant.com/anime-best-kuudere-female-characters/
- https://moemee.jp/post/12259/3/
- https://www.animatetimes.com/news/details.php?id=1268627121
- https://www.animatetimes.com/news/details.php?id=1477372541
- https://www.animatetimes.com/news/details.php?id=1769993073

## Observed outward shorthand

### Recurrent but non-defining

- neutral, serious, or minimally smiling face;
- relatively still brows and low-amplitude mouth changes;
- upright, stable, or economical posture;
- tidy silhouette and visually restrained styling;
- muted, cool, or neutral color treatment in many editorial thumbnails;
- sparse staging that keeps the face readable.

### Attributes that varied

Examples spanned different genders, hair colors, hair lengths, eye colors, uniforms, fantasy clothes, contemporary clothes, roles, and body presentation. This variation is enough to reject a fixed silver/blue hair recipe, fixed red/blue eyes, a school uniform, or femininity as a required visual feature.

### Search artifacts

- Silver-haired female close-ups were heavily overrepresented in generic web results.
- Many thumbnails were selected because they already looked calm or beautiful, not because the pixels showed a relationship-specific “dere” response.
- Ranking and reposting favored familiar franchise images and listicles.
- Centered portrait composition hid the relationship target and turned a behavioral archetype into an appearance tag.
- Search snippets sometimes described a character's canon while the isolated image itself showed only a neutral face.

The search therefore supports optional outward conventions only. It does not validate hair, eye, costume, palette, or a neutral expression as proof.

## Pixel-only failure test

Mentally remove the character name, franchise knowledge, listicle title, and the word “kuudere.” Ask whether the frame still shows:

1. a stable low-expression baseline;
2. one identifiable trusted target;
3. a quiet practical act toward that target;
4. one localized warmth cue;
5. a visible helpful consequence for the same target.

Most isolated search portraits fail items 2–5. They are useful appearance references but weak semantic references.

## Drawn-to-photographic mapping

| Drawn/editorial shorthand | Photographic translation | Residual ambiguity |
|---|---|---|
| Flat or neutral anime mouth | Natural closed or slightly parted mouth with a fractional one-corner release | Reads as ordinary seriousness without target/action context. |
| Minimal eyelid change | Slight lower-lid easing while brows and head remain stable | Can read as fatigue or softness without a visible trigger. |
| Upright, still pose | Balanced stance, economical gesture, no theatrical recoil or broad embrace | Can read as professional formality. |
| Cool/muted palette | Restrained wardrobe or grade that preserves skin and eye realism | Mood only; cannot establish personality. |
| Small “dere” smile | Localized mouth or cheek softening caused by the target's visible relief | Generic beauty smile if the target/result is absent. |
| Quiet gift/help object | Show the handoff or repair plus the target using or receiving it | Prop-only portrait if the action and consequence are not visible. |

## Recommended single-frame bundles

### Bundle A: shared shelter

- calm adult subject remains upright and minimally expressive;
- the same trusted adult counterpart is visibly caught by rain;
- subject quietly angles or offers spare shelter toward that person;
- the counterpart's shoulder or clothing is now sheltered;
- only the near-target hand tension or mouth corner softens.

### Bundle B: task rescue

- composed adult coworker watches a shared task rather than posing for camera;
- one identifiable trusted coworker lacks a needed tool or has a small practical problem;
- subject places the exact tool within reach or repairs the item without ceremony;
- coworker visibly resumes the task;
- lower lids or one brow region relax by a small amount.

### Bundle C: comfort adjustment

- low-expression adult subject remains calm and close enough for a practical gesture;
- trusted counterpart has a wet sleeve, loose collar, slipping strap, or cold hands;
- subject quietly adjusts or supplies what is needed;
- target's posture visibly becomes more comfortable;
- only the hand nearest the target or one mouth corner loses tension.

## Reject as insufficient

- an attractive neutral face with silver or blue hair;
- cool lighting, blue-gray grading, or minimalist clothing;
- a competent scientist, soldier, maid, nurse, student, or office worker;
- crossed arms, direct gaze, averted gaze, or perfect posture;
- coffee, umbrella, handkerchief, charger, book, or repaired object held as a static prop;
- a small smile or blush with no trusted target;
- broad open happiness that erases the restrained baseline;
- hostility, flustered denial, anxious avoidance, surveillance, possession, or boundary control.

## Implementation consequence

The runtime profile requires the five relationship/behavior components. Low-amplitude face, economical posture, restrained styling, and cool-neutral color are optional support groups. Fixed hair, eyes, costume, gender, role, gaze, camera, and prop are explicitly forbidden as personality proof.
