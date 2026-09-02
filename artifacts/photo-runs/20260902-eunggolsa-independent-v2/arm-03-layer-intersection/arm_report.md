# Arm 03 — Layer Intersection

Status: completed, but not technically qualified. The built-in image generator returned one image from exactly one call; no retry or fallback was used.

Concept: a late-night boutique editorial portrait in which one unmistakably adult woman lifts the exact left-front waist corner of a navy tailored jacket. The hand-controlled diagonal edge opens a bounded waist interval while a constructed opaque ivory satin foundation remains visibly separate; a transparent acrylic screen carries one ceiling-strip reflection.

Final image: `final.png` (`941 × 1672`, SHA-256 `f792c4d4026c857585c884c6ae0dc50edad9e67b91e154d306f906f4584fe75f`). Thumbnail: `thumbnail.png` (`216 × 384`).

The prompt audit passed with only a non-blocking 487-word advisory warning, and the exact runtime-input audit passed. Those results are preflight evidence only. Native and thumbnail pixel review scored 12/14 hard gates:

- `adult_everyday_controlled_reveal_moment`: 8/9.
- `underwear_as_outerwear_layer_system`: 4/5.
- Combined: 12 pass, 2 fail.

Failed gates:

- `vo_everyday_reveal_thumbnail_dual_salience`: at 216 × 384, the face reads first, but the large bright ivory chest panel reads before the smaller hand-altered lower boundary.
- `vo_outerwear_layer_intersections`: native pixels show layer order, hems, lapels, button, overlap, and contact shadow, but the required camisole straps are completely hidden or absent; partial evidence is FAIL.

The generated pixels therefore remain retained failure evidence and are not representative-qualified. Requesting-user judgment has not been received.
