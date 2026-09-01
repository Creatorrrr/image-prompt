# Three-arm boundary and transition render qualification

## Independence contract

- Three separate subagents receive one assigned profile, one immutable request envelope, the same source snapshot, the same portrait reference, and one arm-local rubric.
- Before freezing `photo-authorial-core/v3`, an arm may read only the skill entrypoint, its request envelope, the assignment, the portrait, and use general visual reasoning. It must not inspect the registry, candidate extension, index, tests, sibling directories, or another arm's output.
- After the core is frozen, the arm may load the current project data, bind its assigned profile through `agent_postcore_interpretation`, generate one candidate pack, compose and audit one prompt, and audit one render request.
- Each arm makes exactly one built-in image-generation call and performs no retry. A safety or tool block is `blocked_generation` and receives no pixel score.
- An arm must not read or use sibling prompts, packs, messages, images, or reviews. Visual diversity is not evidence of independence; the manifests and agent boundaries are.

## Reference boundary

The portrait is evidence only for visible adult appearance: adult impression, long center-parted dark wavy hair, dark eyes, softly arched brows, face proportions, and the visible black blouse when the arm chooses to preserve it. It is not evidence of identity, same-person status, protected traits, health, attractiveness, ethnicity, nationality, personality, occupation, power, awakening, transcendence, victim status, or narrative alignment.

## Per-arm authoring task

Using the assigned random seed, independently invent one complex but single-frame photorealistic concept in which the assigned event remains the dominant falsifiable relation. Complexity may vary setting, era, weather, practical role, materials, secondary action, camera, and lighting. It may not replace any profile-owned component or make the portrait reference the sole proof of the concept.

## Evidence layers

1. envelope/core/intent provenance;
2. candidate-pack and composed-prompt audit;
3. exact render-request/reference audit;
4. generation delivery and saved image hash;
5. thumbnail and native pixel review under the frozen rubric;
6. requesting-user judgment, left pending.

`partial_is_fail`: every profile and common gate must pass in the same saved image. Prompt presence, candidate retrieval, an attractive result, or a sum score cannot substitute for pixel evidence.
