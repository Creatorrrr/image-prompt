# Source Policy

Use this reference before enabling a source adapter or adding a new platform.

## Allowed Collection Methods

- `local_inbox`: User-supplied files in this repository. This is the safest default.
- `allowed_feed`: RSS, Atom, ActivityPub, or equivalent public feeds that are intentionally exposed for machine reading.
- `official_api`: Platform-published API endpoints used within their documented scopes, permissions, and rate limits.

Any other collection method is blocked by default. Do not implement browser scraping, cookie replay, private mobile/web endpoints, hidden GraphQL endpoints, CAPTCHA bypass, or session automation.

## Platform Notes

- Meta and Threads: use only official Threads APIs or an explicitly allowed feed. Meta's automated collection terms require authorization for automated collection, so the `threads_official` adapter must stay disabled until official access, token scope, and endpoint configuration are present.
- X: use X API search endpoints with developer credentials. X terms prohibit crawling or scraping outside published interfaces without written consent.
- ActivityPub/Mastodon: public endpoints are acceptable only when the instance exposes them for machine access and the adapter respects rate limits.
- RSS/Atom: acceptable when the feed publisher exposes the feed and the registry enables the URL.

## Source Registry Rules

Every adapter must be declared in `assets/source_registry.json`.

- `enabled: false` means skip, never fail the whole run.
- `required_env` lists credentials that must exist before an adapter runs.
- Empty feed/query/url config means skip cleanly.
- `collection_method` must be one of `official_api`, `allowed_feed`, or `local_inbox`.
- Rate limits are per scout run and must be enforced by the adapter.

## Output Rules

- Raw source text, author handles, and media stay under gitignored `data/raw`.
- Reports must not include source handles, raw prompts, raw captions, or source media.
- "Do not repost", "do not steal", watermark, and credit-required signals become `no_raw_reuse` and `no_republish`.
- Private abstraction is allowed; raw reuse or reupload is not.
