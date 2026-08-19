# Held-sword isolated skill arm report

## Outcome

- Arm: `held_sword_retry_isolated_skill_arm`
- Isolation: `cross_arm_inputs_used=false`
- Candidate packs generated: exactly `1`; alternate packs: `0`
- Native image calls: exactly `1` initial call; retries: `0`
- Selected attempt: `1`
- Retry requested: `false`
- Pack: `photo-candidate-pack/v6`, creativity `0.5`, pack ID `dc67bf66d3255f63`
- Composed audit: `PASS`, failures `0`; advisory length/uncovered-intent warnings only
- Runtime request audit: `PASS`, failures `0`
- Generic render-repair review audit: `PASS`, `technical_qualified=true`, failed gates `[]`
- Frozen major retry triggers: none triggered
- Frozen weighted rubric: `87/100`
- Requesting-user preference: pending and not inferred from audit or pixel qualification

The initial saved result satisfies the bounded stop rule: all four generic repair gates and all five frozen major triggers pass, so attempt 1 is selected without a retry.

## Frozen input and skill validation

The original manifest was validated before any project runtime input:

- Original manifest SHA-256: `31c83e8048a1ced8a4d3f754f05250d3a0f0611068e60fd15470154f9adfd5de`
- Request envelope file/canonical SHA-256: `da22b9f9...c77e3c0` / `4eddecb7...14b82`
- Authorial core file/canonical SHA-256: `00cd604b...40487` / `aeb7803b...27e8f`
- Intent-lock SHA-256: `603b5804cb9e68ca62aea77afb376d7b599298512a48e0281cd3c2885b9751ce`
- Request-lineage SHA-256: `88886662b770a7cf5d555ced08c36b203566bb08828c185a4137c28c06f19e16`
- Render-repair contract SHA-256: `d1e3d5c444df830bf91ff42e7c8480d2d83107c7fe146d8aa371fd79037baddb`
- Evaluation protocol SHA-256: `22d01f04cb100264843e1a22e5b12b45ab64426ffaa4cbcfd088b5cc8cf74a72`
- Face-only JPEG SHA-256: `a8aa61ee7f1452e8b155dc557e55aa7bb662e6755617f779e78ffbae6d769022`
- Improved SKILL.md SHA-256: `9b069efb5d7a57472ad8f7c7b2c5466567b28340792cdae3167024f65df88ed6`

The request envelope, v3 core, intent lock, and request lineage were independently re-normalized with the frozen generator and matched their manifest canonical hashes. The core was never revised.

The full `photo-prompt-image-generator` skill and the post-core references required by this returned v6 pack were read: composition, creative augmentation, typed character response, concept routing, viewer experience, and image runtime. The complete native `imagegen` skill and its shared prompting reference were also read before the image call.

## Auditor integrity correction history

The first current-CLI composed audit was blocked only by `authorial_core_integrity`: the then-frozen auditor's v3 integrity helper accepted an old four-field lineage shape while the generator and the same auditor's repair builder required `photo-request-lineage/v2`. There was no prompt, core, pack, or evidence failure, and no image call had occurred.

The coordinator changed only that contradictory integrity validator and updated the manifest's auditor provenance. The existing request, core, protocol, generator, sole pack, and composed prompt remained byte-identical. Revalidated values:

- Updated manifest SHA-256: `45084a25706d02345de27d8964289e778e1f0db77ff6c168c7e873e1e3f5b8f3`
- Corrected composed auditor SHA-256: `174f5f4486171747d5088416164d3a761d9596a5f3059366f6a0761b65667d41`
- Existing pack SHA-256: `7dcf6ad4a55652d8cb89740e0784caa7916f61dc1d4b2c14abe81fee8f30ec93`
- Existing composed prompt SHA-256: `ce38a6e114166a564c0bc8089bda875df32cdb7e291cdbfddc99044c9d2d3584`

The corrected actual CLI invocation with `--pack` returned `PASS`, failures `[]`. Both the original blocked result and corrected PASS are retained.

## Sole candidate-pack generation

Exact argv:

```text
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py --request-envelope-json /Users/chasoik/Projects/image-prompt/artifacts/photo-prompt-held-sword-retry-20260819/input/request_envelope.json --authorial-core-json /Users/chasoik/Projects/image-prompt/artifacts/photo-prompt-held-sword-retry-20260819/input/authorial_core.json --candidate-pack-version v6 --creativity 0.5 --emit-candidate-pack --n 1 --output-file /Users/chasoik/Projects/image-prompt/artifacts/photo-prompt-held-sword-retry-20260819/isolated_skill_arm/candidate_pack.json
```

The pack contains one v6 object only. All six sampled creative candidates were rejected because they either duplicated frozen quality or weakened the locked mid-thigh, resting-guard, mantle-clasp, face-first hierarchy. Both optional visual concepts were left unselected; the possessive-control concept conflicted with the core, and the cool-reserve profile would have redundantly promoted additional hard geometry beyond the already frozen typed evidence. `chosen_candidate_ids=[]` and `chosen_visual_concept_ids=[]`.

## Exact final composed prompt

```text
Create a contemporary luxury wuxia beauty editorial of an unmistakably adult woman in her mid-twenties, strikingly beautiful and softly charming. Use the portrait only for facial casting: pale skin, tapered oval face, adult-proportioned gray eyes, slim nose, full rose lips, nose-side beauty mark, and ash-blonde loose half-up hair. Frame a vertical mid-thigh portrait with her luminous face as the immediate first read. An ancient ice-sect master restored to youthful adult form, she carries restrained authority through a weathered belt seal and faint frost. In a restrained modern Northern Sea Ice Palace pavilion of clear ice planes and thin silver seams, her same-ranked adult sparring partner has just placed a charcoal training mantle across her shoulders. She keeps a cool unreadable mouth and composed gaze. His adult hand withdraws from the mantle edge; her free left hand fastens the clasp, only her lower eyelids soften toward that same departing hand, and he pauses in visible surprise while the mantle remains secured. Matching plain black training bracers identify equal peers. The adult heroine holds one plain straight double-edged jian by its leather-wrapped grip in her right hand, upright beside her body in a relaxed resting guard. One plain straight double-edged jian shows a short cylindrical pommel, leather-wrapped grip, compact straight guard, and one continuous narrow double-edged steel blade. The whole blade rises beside her inside the frame at supporting scale; her natural principal fingers, hilt, guard, and blade axis share the face's focal plane. Tailored ivory and ice-blue couture, a broad pearl key, restrained cool rim, shallow 85mm depth, realistic adult skin, and contemporary fashion-campaign polish keep beauty dominant across generous clean ice.
```

Exact pack negative bytes:

```text
low resolution, 3D render look, cartoon style, broken window geometry, excessive HDR, impossible perspective, broken facial features, unrealistic hands
```

The prompt is 271 words. The composed audit's `quality_status=warn` reflects the advisory 180-word and evidence-adjusted 253-word ceilings; the absolute 320-word bound passes. The 173 words of frozen literal evidence, the face-only reference role, held-sword geometry, and two open-dimension authorial decisions were retained instead of deleting requester meaning.

## Runtime request and native call

- Runtime request schema: `photo-image-render-request/v2`
- Runtime prompt ID: `2f268c64498cdd51`
- Runtime prompt SHA-256: `2f268c64498cdd51a0ffcdc1fcaf429637176e4da47996d68334122549e886b6`
- Runtime request SHA-256: `3b3fdebf8f6e4f14d0e1c4d2d34c2ecf71bcb97fbef624491a7303e4082c42b5`
- Runtime negative matches pack byte-for-byte: `true`
- Attached reference: `/Users/chasoik/Downloads/4FBED371-F292-4BB7-8800-B33B91190D45.jpeg`
- Reference role: `facial appearance only`
- Native input mechanism: exact `referenced_image_paths`; prior conversation images were not included
- Runtime audit: `PASS`, reference count `1`, failures `[]`
- Native tool: `image_gen.imagegen`
- Initial image calls: `1`; retry calls: `0`

## Saved image

- Returned default file: `/Users/chasoik/.codex/generated_images/01a01929-68ee-7221-9a8a-d48fde094f89/exec-455c31e0-cc2f-45ff-b4a9-10ba6c8e9197.png`
- Arm-local exact copy: `/Users/chasoik/Projects/image-prompt/artifacts/photo-prompt-held-sword-retry-20260819/isolated_skill_arm/generated_images/held-sword-first-attempt.png`
- SHA-256 at both locations: `2bc760621e894d3b783e1030bbd2d52a51858e37b236f3106c242a871bb4d19a`
- Dimensions: `1023×1537`
- Format: PNG

The exact saved pixels were inspected as a 213×320 thumbnail, at native scale, and through native sword-hand and mantle-interaction crops. The original JPEG was viewed only to assess facial appearance, never as composition, expression, personality, or cross-arm input.

## Generic repair gates

| Gate | Result | Direct pixel evidence |
| --- | --- | --- |
| `rr_held_martial_prop_object_class_legible` | PASS | At thumbnail and native scale the prop is recognizably one straight double-edged sword with pointed blade, guard, wrapped grip, and pommel. |
| `rr_held_martial_prop_gross_structure_coherent` | PASS | Native pixels show one continuous aligned blade–guard–grip–pommel structure; extra guard ornament is minor. |
| `rr_held_martial_prop_intended_interaction_matches` | PASS | The heroine herself encloses the grip and keeps the complete sword upright beside her; it is not transferred, hidden, relocated, or wall-mounted. |
| `rr_held_martial_prop_contact_anatomy_coherent` | PASS | Thumb, four curled fingers, palm, knuckles, and wrist form a coherent grip without severe fusion or impossible articulation. |

The exact `photo-image-render-review/v1` record and current auditor both pass; `failed_gate_ids=[]`.

## Frozen evaluation protocol

| Category | Score | Review |
| --- | ---: | --- |
| 미소녀 | 38/40 | The large luminous adult face is the immediate thumbnail read and remains structurally coherent at native scale. |
| 쿨데레 | 18/25 | Her stable cool expression coexists with fastening the same peer's mantle and matching peer bracers. The intended lower-lid direction and his surprise are subtle. |
| 반로환동 | 8/10 | Youthful adult beauty coexists with controlled sword posture, a weathered belt seal, and restrained authority. |
| 북해빙궁 | 7/8 | Clear ice planes, frosted glazing, pale seams, and cool atmosphere support the portrait. |
| 검 상호작용 명료도 | 7/7 | The heroine visibly holds one complete recognizable sword with coherent contact. |
| 현대적 균형 | 4/5 | Minimal translucent architecture and fashion lighting dominate over mild classical costume/guard detail. |
| 화보 및 주요 해부 완성도 | 5/5 | Campaign polish and all event-critical hands are coherent. |

Total: `87/100`.

All five frozen major retry triggers are false:

1. Adult beauty remains the first read; no severe face failure.
2. Cool surface plus same-peer-specific acceptance remains present and does not read as maternal care.
3. No frozen sword repair gate fails.
4. Classical decoration does not overwhelm the heroine.
5. No event-critical principal hand has severe fusion, impossible articulation, or missing contact.

Non-retry observations: the guard and belt are more ornate than the plain wording; the small reference beauty mark is not clearly visible; the peer's surprise and eye-direction microcue are understated. These lower the character-response score but do not meet a frozen major retry trigger. No retry was made.

## Ledger and manifest

- Recorder SHA-256: `83c0b8575b80309f5fad501b55b5a2a639c49a0eea564e81df3311c17f8d902c`
- Ledger run ID: `5a7ce8670aab7be0`
- Ledger prompt ID: `2f268c64498cdd51`
- Arm-local ledger: `/Users/chasoik/Projects/image-prompt/artifacts/photo-prompt-held-sword-retry-20260819/isolated_skill_arm/runs/image_runs.ndjson`
- Manifest: `photo-independent-run-manifest/v2`
- Manifest path: `/Users/chasoik/Projects/image-prompt/artifacts/photo-prompt-held-sword-retry-20260819/isolated_skill_arm/run_manifest.json`
- Manifest image call count: `1`
- Manifest render-repair contract SHA-256: `d1e3d5c444df830bf91ff42e7c8480d2d83107c7fe146d8aa371fd79037baddb`
- Failed repair gate provenance: none; the exact review audit records `failed_gate_ids=[]`
- `cross_arm_inputs_used=false`

## Preserved artifacts

- `input_validation.json`: manifest, file, canonical, skill, and script hash checks
- `candidate_pack_generation.json`: exact sole-generation argv and pack provenance
- `candidate_pack.json`: exact generated one-item v6 pack
- `composed_prompt.json`: exact agent composition and byte-identical hard evidence maps
- `composed_audit_blocked.json`: original contradictory-validator failure
- `composed_audit_corrected.json`: corrected current-CLI PASS
- `composed_audit_history.json`: immutable linkage between the two auditor states
- `runtime_render_request.json`: exact serialized native inputs
- `runtime_render_audit.json`: exact runtime preflight PASS
- `image_call_evidence.json`: one-call evidence, returned path, copy identity, hashes, and dimensions
- `render_review.json`: exact four-gate pixel review
- `render_review_audit.json`: repair-review qualification PASS
- `evaluation_review.json`: all frozen rubric categories, first-attempt requirements, and major triggers
- `reviews/`: thumbnail and native review crops
- `runs/image_runs.ndjson` and `run_manifest.json`: recorder outputs
- `generated_images/held-sword-first-attempt.png`: selected exact pixels

No source skill or test file was edited by this arm. Prompt/runtime audit PASS is treated as preflight only; the 87/100 score and gate results come from the exact saved pixels, and the requesting user's preference remains pending.
