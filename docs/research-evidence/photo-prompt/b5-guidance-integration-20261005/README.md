# V20: exact guidance source binding, zero frozen-pack delta

V20 qualifies source commit `b5f2e8924be1daa02a99f9661b99796129400e23`
(tree `2862e8d0dd250bf72dc43ca4f5584bfe2fc452d4`), the direct child of
`9105a63d9b261f91219875e15f346d6d52e477bc`. The 131-file source inventory
is unchanged. Exactly three bound files have new bytes: the photo `SKILL.md`,
`references/composition-contract.md`, and `references/retrieval-contract.md`.
Every other bound source, DATA file, index, active semantic shard, and frozen
pack field remains sealed to the prior value. No predecessor proof, baseline,
pack, or validator acceptance condition is replaced or relaxed.

The actual CLI completed with exit code 0 using the already-frozen current
boundary core, envelope, controls, and review, under a network-denying guard.
Its 207,140-byte pack is byte-identical to V19, SHA256
`4eb43e4068ef99765793b68aadbc705a62f02f29fa69954d1de36697356519a2`.
`QUALIFICATION.json` records that observation. This establishes deterministic
runtime and DATA preservation for those inputs. It does not establish the new
guidance's effect on future independent authoring, output equivalence for new
authored inputs, or image quality. Earlier qualification counts and findings
are historical evidence, not new-source results.

V19 tests use `V19-PARENT-SOURCE.json` to reconstruct the original 9105 source
and validator without Git, network access, or live guidance substitution.
The fixture reuses 146 of 149 source members and adds three immutable snapshots
totaling 576,631 bytes: the V19 photo skill, validator, and universal descriptor.
The 199 enumerated dependencies reuse existing repository bytes. SHA256,
Git blob IDs, sizes, paths, source pin, and modes are checked before copying.
The validator's three local imports remain the previously sealed support
modules. V1–V18 fixtures and validator functions remain unchanged.

V20's universal descriptor differs from V19 only in the validator SHA256.
The upstream analysis plan and unbound helper remain untouched; they are not
new acceptance dependencies of this minimal boundary successor.
