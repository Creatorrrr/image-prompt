# Preflight schema correction

The coordinator froze the semantic meaning before any project-local retrieval. The first JSON serialization had file SHA-256 `5d320b32c814bd920d1790a7c29001a698373cdf67d1938e7e1d5b196cb8d233`, but a post-freeze schema check found unsupported field names and shapes.

Before any candidate-pack or image-generation call, only the mechanical representation was corrected: `identity_reference_scope` became the supported `reference_use` dimension; unsupported `wardrobe` was removed from open dimensions; the assertion uses `dimension`/`polarity`/`affected_dimensions`; the leak channel is a one-item list; and relations use the supported operator shapes. The requester text, interpreted meaning, baseline prompt, anchors, evidence phrases, and visual event were not revised.
