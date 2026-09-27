# Reflection Rubric

Use this rubric when reviewing generated candidates.

## Recommendation Values

- `adopt`: Repeated across multiple sanitized examples, low source risk, not already covered, and maps cleanly to a photo-prompt slot, facet, recipe, or coherence rule.
- `trial`: Promising but based on a small sample, partially overlapping with existing tags, or useful only for a narrow concept family.
- `reject`: Too generic, already covered, too close to source wording, not photographic, or not actionable for `photo-prompt-image-generator`.
- `needs_human`: Any IP, brand, real-person, minor-coding, explicit sexual, graphic violence, medical-risk, legal, or source-policy ambiguity.

## Candidate Quality Gates

- Prefer visual grammar over vibe labels.
- Prefer reusable prompt structure over one-off scene nouns.
- Prefer slot/facet/coherence changes over long prose additions.
- Do not copy source prompts into `SKILL.md`, `photo_prompt_tags.json`, or reports.
- If a trend is mainly a creator signature, watermark, hashtag, or branded workflow, reject it.

## Mapping Priorities

1. Existing `photo_prompt_tags.json` slot ids and `facet_vocab`.
2. Existing `concept_recipes.json` roles and mixins.
3. New tag or facet candidate only when existing coverage is weak.
4. Drift gate or coherence rule when the issue is selection quality rather than a missing tag.

## Review Checklist

- Does the candidate still make sense if the source URL and author are removed?
- Is the proposed wording abstract enough that it is not a copy of a source prompt?
- Would this improve generated photo prompts rather than just describe a social trend?
- Is there a testable validation path after applying it?
