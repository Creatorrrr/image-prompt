# Camera owner fallback — first implementation failure

Recorded 2026-10-03 UTC before retry. Runtime commit: `dee90820`.

The first focused run executed 42 methods and recorded one failure and one
error. Frozen original006 still lacked a correct upward candidate because the
fallback rejected the entire baseline whenever a sentence contained both
`background` and `camera`, even when the background was a separate scene clause.
The correct camera-owned sentence remained available in the unchanged baseline.
The fix must restrict the exclusion to a description of the camera itself;
whole-scene text must not enter the query. Keep the frozen original and property
arms and their expected meanings unchanged.

The additional error was a test's incorrect assumption that projected public V6
slots contain `selected`. The public optional-adoption binding is the appropriate
contract check. This is a test API error, not permission to force adoption.

The parent's first independent 14-scene set was evaluated on this same runtime
before further implementation changes: 0/6 affirmative cases found and 8/8
negative cases abstained. These positives exceed the initial bounded clause
grammar, including passive/embedded capture-camera descriptions and raw Korean
prose. The English-baseline production probe reports Korean prompt-budget
normalization failures separately; raw extraction remains measured for all 14.
Do not rewrite those scenes or call this set a final blind holdout after tuning.
A fresh set is required after the implementation is fixed.

Raw focused log, evaluator error, corrected evaluator report, and source hashes
are preserved in the follow-on evidence archive. No provider calls or DATA edits
were made.
