# Model adapters

Read only the adapter for the named downstream generator. If no generator is named, keep settings generator-agnostic and do not invent unsupported controls.

## GPT Image 2

Official references:

- https://developers.openai.com/api/docs/guides/image-generation#customize-image-output
- https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide#2-prompting-fundamentals

### Prompt

- Keep the core output contract's P0/P1 and causal dependency order. Use skimmable blocks within that order; scene/background leads only when it carries the source signature.
- Use short labeled segments or line breaks for complex prompts.
- Describe framing, viewpoint, placement, interaction, medium, lighting, and only the quality cues that matter.
- Treat detailed camera specifications as high-level visual cues, not exact physical simulation.
- Put essential exclusions and invariants in the main prompt. The official Image API output controls do not document a separate negative-prompt field.
- For material color fidelity, keep intrinsic value, chroma, and hue in separate short controls. A current-source aggregate color/finish descriptor may lead them once through source-evidence qualification; treat its generator effectiveness as unverified unless response evidence matches the exact model version.

### Visual color conditioning

- When the active image tool accepts referenced images and the request permits reference-conditioned generation, pass the source or an analyst-built color reference through the tool input; keep the standalone production prompt free of references to an absent image.
- When the user asks for text-only generation, do not silently add reference conditioning.
- Do not assume that natural-language color terms map to stable Lab movement across model versions. Use a version-matched response evaluation when available, otherwise report the control as uncalibrated and rely on delivered-pixel evaluation.

### Settings

Use only documented controls that are relevant:

- `model: gpt-image-2`
- `size: auto` or a valid custom size
- `quality: low | medium | high | auto`
- `output_format: png | jpeg | webp`
- `output_compression: 0-100` for JPEG or WebP
- `background: auto | opaque`

Do not request a transparent background for GPT Image 2.

### Custom-size constraints

A custom size is valid only when:

- both edges are multiples of 16 pixels
- the maximum edge is at most 3840 pixels
- long-edge to short-edge ratio is at most 3:1
- total pixels are between 655,360 and 8,294,400 inclusive

Keep `Source frame` and `Target size` separate. When source dimensions are invalid, run:

```bash
python3 tools/size_adapter.py WIDTH HEIGHT
```

Use its target size or choose `auto`. State that the target is a ratio-preserving adapter size, not the source file dimensions.

For actual generation or source/render evaluation, also record how the size reached the tool. Use one of `explicitly-applied`, `auto`, `unsupported`, or `unbound`. After delivery, add the actual frame:

```bash
python3 tools/size_adapter.py WIDTH HEIGHT \
  --binding-status explicitly-applied \
  --delivered-width OUTPUT_WIDTH --delivered-height OUTPUT_HEIGHT
```

Only an explicitly applied target delivered at that exact size passes the frame-setting layer. An explicit mismatch fails; `auto`, unsupported, unbound, or missing delivered dimensions remain unscored, with continuous ratio errors reported when available. This setting evidence does not replace rendered-pixel composition review. Do not try to repair an unavailable size control by repeating aspect-ratio or framing adjectives in the prompt.

## Other generators

- Emit `NEGATIVE PROMPT:` only when the downstream tool exposes a separate negative-prompt input or the user explicitly requests a reusable negative list.
- Use natural-language zones by default. Emit numeric coordinates only if the tool has a compatible layout/control surface or the concept depends on a small number of boundaries.
- Do not name sampler, scheduler, guidance, seed, steps, or control inputs unless the named tool actually supports them.
- Use image, palette, or edit conditioning only when the downstream tool exposes that capability and the request permits it. Keep tool-level reference handling separate from the standalone prompt text.
- Treat any descriptor-response table as model-and-version-specific evaluation evidence, not as a universal color dictionary.
