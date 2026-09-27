---
name: prompt-trend-scout
description: Periodically and read-only collect AI-image and image-prompt examples shared on SNS or local inboxes through official APIs, allowed feeds, or user-provided files; sanitize signatures, handles, watermarks, and promotional boilerplate; abstract examples into visual grammar, tag, recipe, and drift-gate candidates; and emit a human-review reflection report for photo-prompt-image-generator without applying changes. Use when the user or an automation asks to scout prompt trends, crawl/collect SNS prompt examples, or prepare a reflection plan. Never like, reply, repost, follow, bookmark, DM, publish, or auto-mutate photo-prompt-image-generator.
---

# Prompt Trend Scout

## Overview

Use this skill to run a read-only trend scout that turns outside prompt examples into private research records and abstract reflection candidates. The scout never uploads, republishes, socially interacts, or edits `photo-prompt-image-generator` by itself.

## Non-Negotiable Contract

- Use only official APIs, explicitly allowed feeds, or local files supplied by the user.
- Do not use browser scraping, private endpoints, cookies, session replay, or any workaround that bypasses platform controls.
- Do not call or implement social actions such as liking, replying, reposting, following, bookmarking, messaging, or publishing.
- Keep raw source text and media only under this skill's gitignored `data/` cache.
- Strip author signatures, handles, watermarks, tool signatures, credit boilerplate, and promotional calls to action before analysis.
- Treat "do not repost", "do not steal", watermark, or credit-required signals as `no_raw_reuse` and `no_republish`; still allow private abstraction into visual grammar.
- Emit reports and candidates only as abstract visual grammar, tag candidates, recipe candidates, drift gates, and review notes.
- Never write to `skills/photo-prompt-image-generator/assets/*` during the automated scout. Use `apply_reflection.py` only after explicit user approval.

## Default Workflow

Run the weekly scout pipeline:

```bash
python3 skills/prompt-trend-scout/scripts/run_scout.py --cadence weekly
```

The pipeline is:

1. `collect_sources.py`: fetch enabled read-only sources from `assets/source_registry.json`.
2. `sanitize_examples.py`: remove signatures/promos and attach reuse flags.
3. `analyze_corpus.py`: convert sanitized examples into abstract candidates.
4. `diff_against_photo_prompt.py`: compare candidates against `photo_prompt_tags.json` and `concept_recipes.json` in read-only mode.
5. `build_reflection_report.py`: write `data/reports/<report_id>.md` and `.json`.
6. `validate_harvest_schema.py`: validate every emitted record and leakage gate.

The default enabled source family is multi-SNS, but collection is fail-closed:

- `local_inbox`: enabled by default and safest. Put user-supplied JSON files under `data/raw/inbox/`.
- `rss_atom` and `activitypub_public`: enabled but produce no output until feeds/URLs are configured.
- `x_api`: enabled only when `X_BEARER_TOKEN` and a query are configured.
- `threads_official`: disabled until official Threads API access and endpoint configuration are present.

## Local Inbox Format

Use local inbox JSON for manual or ToS-safe inputs:

```json
{
  "source_url": "https://example.invalid/thread/123",
  "platform": "local",
  "raw_text": "Prompt text or caption...",
  "image_description": "Optional private visual note for analysis",
  "media_paths": ["optional-local-image.png"]
}
```

Arrays of these objects are also accepted.

## Human Approval Path

Reports are proposals only. To inspect an approved subset:

```bash
python3 skills/prompt-trend-scout/scripts/apply_reflection.py \
  --report skills/prompt-trend-scout/data/reports/<report_id>.json \
  --select <candidate_id>,<candidate_id> \
  --approved-by "<reviewer>" \
  --dry-run
```

Only after reviewing the dry-run should a user rerun with `--no-dry-run`. After any approved dictionary change, validate through the target skill:

```bash
python3 skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
python3 skills/photo-prompt-image-generator/scripts/build_semantic_index.py --progress
```

## References

- Read `references/sources_policy.md` before enabling or adding any source adapter.
- Read `references/reflection_rubric.md` before accepting, rejecting, or applying candidates.
- Use schemas under `assets/*.schema.json` as the machine contract for runtime records.
