# Concept and Format Routing

## Choose the Narrowest Input

- Natural request: `--concept`.
- Exact research route: `--route <topic_id>`.
- Exact output variant: `--format <variant_id>`.
- Reproducible bundle: `--seed`.
- Creative development: defaults to `--creativity 0.85` for every illustration request.
- Separate safety report: `--safety-evaluation` only when the user requests it.

The runtime is local and deterministic. It uses NFKC-normalized scoped aliases and never sends intent or research text to an embedding provider.

## Route the Output Medium First

Use this skill for non-photographic illustration, artwork, key visual, cover, card, vertical webtoon, character sheet, sticker, SD/chibi merchandise, or campaign-board requests. Use `$photo-prompt-image-generator` for photographs, photographic editorials, documentary frames, product photography, or image edits that must remain photographic.

The six canonical format families are:

- `single_frame`: `single_illustration`
- `key_art`: `key_art`, `ensemble_key_art`, `responsive_key_art`
- `cover`: `light_novel_cover`
- `card`: `collectible_card`
- `vertical_sequence`: `vertical_scroll_sequence`
- `adaptation_board`: `character_design_board`, `merch_adaptation_board`, `campaign_art_board`

An explicit format wins. Otherwise use the longest scoped format phrase, then the route default. An incompatible explicit route and format must fail with allowed variants; do not silently add a ratio suffix.

## Resolve Topics Without Overfitting

Use short, unique mechanism phrases rather than frozen full sentences. Broad terms such as `anime`, `illustration`, `artwork`, `character`, `서브컬처`, or `그림` cannot activate a specialty topic alone.

Resolution priority:

1. explicit `--route`;
2. exact scoped phrase;
3. all required terms;
4. unique supporting terms;
5. format-family default.

If equal top-tier rules point to different topics, fail as ambiguous and show candidate route IDs. Determinism is not permission to choose a silent wrong route.

## Route Creative Intent

High creative development is the default even when the request contains no creativity keyword. It requires alternative proposals, one selected changed rule, visible consequences, and a repeatable authorial decision system rather than extra decoration.

Lower creativity below `0.75` only for an explicit restrained, literal, or utilitarian request. Creative, original, ingenious, surprising, or authorially distinctive intent must keep high development enabled. Korean cues include `창의적`, `독창적`, `기발한`, `참신한`, `작가적`, and `작가의 터치`; interpret meaning rather than exact keywords. High creativity does not require an impossible premise.

## Preserve Boundaries

- Artist, studio, work, franchise, and character names are provenance or exclusion data, never positive style tokens.
- CJK market terms and audience-literacy labels are routers, not visible evidence.
- Negative phrases such as `without text`, `no logo`, `not a poster`, or `인물 없이` remain constraints.
- A color, shape, costume, ethnicity, or market label cannot prove emotion, personality, nationality, or relationship.
