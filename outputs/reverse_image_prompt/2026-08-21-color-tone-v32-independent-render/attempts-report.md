# Generation attempts

- Frozen prompt: `frozen-prompt.txt`
- Frozen SHA-256: `20fa18f4c340129ad20f2eebcccd7e926f0a512b77c48288b11899ef5ae63841`
- Frozen byte count: `4181`
- Retry policy: built-in image generation only; exact same prompt bytes; stop at first returned image; maximum 3 actual generation calls.

## Attempt 1

- Prompt SHA-256 verified immediately before call: `20fa18f4c340129ad20f2eebcccd7e926f0a512b77c48288b11899ef5ae63841`
- Prompt bytes passed: `4181`
- Image returned: no
- Status: `moderation_blocked`
- Stage: `output`
- Category: `sexual`
- Request ID: `2e5e676e-1c3c-4d8c-a360-7a7e9d7106bc`
- Generated image path: none

## Pre-call transport notes

- Two local transport preflights stopped before invoking image generation because the JavaScript isolate lacked base64 and UTF-8 helper globals. They are not generation attempts and did not modify the frozen prompt.

## Attempt 2

- Prompt SHA-256 verified immediately before call: `20fa18f4c340129ad20f2eebcccd7e926f0a512b77c48288b11899ef5ae63841`
- Prompt bytes passed: `4181`
- Image returned: no
- Status: `moderation_blocked`
- Stage: `output`
- Category: `sexual`
- Request ID: `193a0d44-0a43-4321-b48d-1e0c1c1f8061`
- Generated image path: none

## Attempt 3

- Prompt SHA-256 verified immediately before call: `20fa18f4c340129ad20f2eebcccd7e926f0a512b77c48288b11899ef5ae63841`
- Prompt bytes passed: `4181`
- Image returned: no
- Status: `moderation_blocked`
- Stage: `output`
- Category: `sexual`
- Request ID: `c6ddeb6e-48ce-4085-a6f5-1076a6972fca`
- Generated image path: none

## Final outcome

- Actual built-in generation calls: `3`
- Successful image calls: `0`
- First successful image/path: none
- Final category/stage: `moderation_blocked` at `output` moderation, category `sexual`
- Prompt mutations after freeze: none
- CLI/API fallback: not used

## Reconstruction route

- Mode: `faithful`
- Dominant fidelity axis: appearance-led with composition and crop as co-primary controls
- Source frame: `853 x 1280` JPEG, approximately `2:3` portrait
- Color/Tone Contract: applied from visible evidence; representative wall, skin, matte black fabric, washed charcoal denim, and glossy black leather regions were probed diagnostically. Raw measurements were not placed in the production prompt.
- Tier 0: `core.visual-evidence`, `core.frame-coordinates`, `concept.primary-relationship`, `core.fidelity-discipline`, `core.background-color`, `core.pre-emit-gate`, `core.output-contract`
- Routed non-core: `subject.human`, `medium.photographic-capture`, `detail.human-body-form`, `detail.color-tone-fidelity`, `detail.clothing-fashion`, `detail.pose-hands-gesture`
- Model adapter resource: `references/model-adapters.md`; prompt-level built-in/GPT Image compatible guidance only, with no unsupported settings invented
- Built-in image generation resources: `imagegen/SKILL.md`, `references/prompting.md`, `references/sample-prompts.md`
