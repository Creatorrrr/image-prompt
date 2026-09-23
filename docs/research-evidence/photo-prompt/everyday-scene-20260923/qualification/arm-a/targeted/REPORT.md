# Arm A targeted cafe pickup wait qualification

- Request envelope file SHA-256: `a8db7511811cd21cf55956cb40c257a29c165ea946eca53a4394f950f4ad132b` (matched coordinator-supplied hash).
- Test case SHA-256: `f7c1ac181b9d5d41b53936796948feb17e1fd897dbe643e3d8149a375ee1e41f`; seed `15511735850014077439` fixed the phone order cue, lidded paper cup, PICKUP sign, menu board, early-evening light, charcoal sweater, and standing eye-level view before rendering.
- V6 pack `4663e3f5a32b4abe` exposed `visual-concept:ed_cafe_pickup_wait` as eligible optional. It was selected; automatic hard activation before selection was absent. The selected opt-in contract activated four relation gates.
- Composed prompt audit: **PASS**. Exact render request audit: **PASS**. The composed audit also reported 4 uncovered-intent warnings because the exact frozen intent evidence was preserved in free prompt text.
- Native image generation: **1 call**, saved as [generated.png](generated.png), SHA-256 `ad98aac3fd6e1615f981a9e4b27e48abe22707573d7a3022f7c80dda7d09faa4`. [review_thumbnail.png](review_thumbnail.png) is a 384x512 review derivative; native size is 1086x1448.
- Strict pixel decision: **PASS** for all four selected cafe relations at both sizes and all five embodiment gates at native size. The white lidded cup remains under barista control behind the PICKUP sign; the customer faces the handoff while holding her phone, with a visible gap to the cup. A second iced drink appears at the far service side but does not obscure the selected cup.
- Review-record audit: `technical_qualified=true`, `failed_hard_gates=[]`. Its command exits 1 because representative qualification awaits direct user judgment; `user_judgment` remains **pending**. The validator checks the record and image hash, not visual truth.
- Reference image use: visible adult appearance only; identity, biometrics, protected traits, and body shape were not inferred.

The original postcard baseline in the parent arm directory remains exploratory and was not rendered.
