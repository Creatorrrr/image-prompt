# Camera owner blind V2: preserved positive misses

Date: 2026-10-03 UTC. Frozen runtime: `6665684fd5c3a73591b4c5b4508c4cc5f5d3da1f`.
The independent author saw no repository, implementation, or prior holdouts.

All six positive English baselines failed literal camera owner extraction both before
and after the patch. All eight negative raw extraction controls abstained in both
arms. Expected owners/predicate spans and 59–66-word baselines remain unchanged.
No runtime or expected-outcome tuning followed evaluation.

Embedded capture-purpose camera modifiers and lens handoffs are outside the bounded
legacy grammar. KO_LOW also contains a local upward negation that conservatively
suppresses the entire sentence. This does not demonstrate general camera-ownership
recall improvement; original frozen 006 is a narrower direct-camera command success.

KO_TWO was rejected by the existing blanket-negative baseline contract in both arms:
`No single capture direction can be selected from this scene`. Its baseline was not
rewritten. The other 13 normalized synthetic callers have unchanged camera queries
and candidate IDs. Generic optional camera exposure continues in both arms, including
wrong-direction options, so extractor abstention is not candidate precision evidence.

Original V1 first-pass 0/6 and post-seen development 1/6 remain separately preserved.
Provider calls and rendered images: zero. Details and fixture hash are in
[the final report](../research-evidence/photo-prompt/upward-camera-owner-20261003/README.md).
