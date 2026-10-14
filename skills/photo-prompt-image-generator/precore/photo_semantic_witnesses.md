# Frozen semantic witnesses

Read this candidate-free contract when authoring `semantic_assertions` before
retrieval. It describes addresses and exact facts, without candidate examples or
automatic anatomy, age, material, or ownership inference. Author only facts
grounded in the active requester spans and already expressed in the independent
baseline. An open authorial choice is not a required frozen fact.

Use the normal assertion fields with `polarity: required`, active
`source_span_ids`, literal baseline `evidence`, and these exact `axes` shapes:

| kind | axes in addition to `native_schema` and `kind` |
| --- | --- |
| `owner` | `owner`, `owner_kind` |
| `role` | `role`, `owner` |
| `fact` | `owner`, `property`, `value_type`, `value` |
| `equivalent` | `left`, `right` |
| `part_of` | `left`, `right` |
| `disjoint` | `left`, `right` |
| `scope_inventory` | `owner`, `scope_kind`, `inventory` |

Every row uses `native_schema: photo-frozen-semantics/v1`. Owner, role and
relationship rows use `dimension: subject` and `affected_dimensions: [subject]`.
Fact rows use their actual dimension and that same one-item affected-dimension
list. Required facts need a whole-dimension lock or protection by an existing
requester property anchor covering the same actual owner and exact property or
its ancestor. A narrower anchor cannot protect a broader fact. Keep a partially
specified dimension open; declaring a fact does not broaden the request's locks.

`scope_inventory` rows also use required subject assertions and the subject
lock. Their `scope_kind` is `reference_appearance` or `requester_identity`.
Author these before retrieval only when grounded in the actual request. The
`inventory` is a canonical JSON string: sorted keys, compact separators,
unescaped Unicode and no duplicate keys or nonfinite numbers.

For these scopes, supply `--input-inventory FILE` at run initialization. Its
exact object is `{schema: "photo-request-input-inventory/v1", complete: true,
items: [...]}`. Each item contains exactly `id`, `kind`, and `sha256`; hashes
are the actual input bytes' lowercase SHA-256. List the exact request once as
`request_text`, plus every other supplied input. Other allowed kinds are
`text`, `reference_image`, `identity_reference`, and `other`. There are at most
32 distinct IDs. Completeness is the caller's explicit assertion, not an
independently observed fact. An omitted inventory stays omitted. Text can
establish identity or appearance without an image file.

The decoded scope inventory has exactly `schema`, `complete`, `input_binding`,
`reviewed_input_ids`, `state`, and `items`, with schema
`photo-frozen-scope-inventory/v1`. Bind the actual request, request envelope and
input inventory hashes as `request_sha256`, `request_envelope_sha256` and
`input_inventory_sha256`. Review every listed input ID. Use `known_present`
with a nonempty complete item list, `known_absent` with no items, or `unknown`
when the information is unresolved. Missing inputs, incomplete review, a stale
binding or a conflicting scoped fact cannot support a known-absent assertion.

Each item repeats one scoped frozen fact's exact `assertion_id`, `dimension`,
`target` (actual owner), `property`, and typed `value` (`type`, `value`). A
scoped fact adds both `scope_kinds` and `source_input_ids` to its usual axes;
these are explicit provenance declarations. Include all scoped facts belonging
to the owner or its explicitly grounded owned parts. Do not create an owner,
part relationship or protected fact merely to complete this inventory. A fact
without scope provenance cannot silently become a scoped item. Final delivery
checks literal evidence of preservation for the same actual owners and values;
literal binding does not establish image pixels or semantic entailment.

Declare each actual owner once. A role maps a common protocol address to that
owner's run-local ID. The available addresses are `main_subject`,
`secondary_subject`, `scene`, `image`, `recording_camera`, `primary_face`,
`secondary_face`, `primary_hair`, `secondary_hair`, `primary_hands`,
`secondary_hands`, `primary_garment`, `secondary_garment`, `primary_prop`,
`secondary_prop`, `foreground_surface`, `background_surface`, `light_source`,
`light_receiver`, and `relationship_target`. Declare only applicable grounded
roles; there is no first-owner or automatic primary assignment. A depicted
camera is distinct from the capture camera. A role name is an address and does
not establish anatomy or a property's value.

Equivalence identifies one entity under two explicit names. `part_of` connects a
part to its owner without making them the same entity. `disjoint` explicitly
separates entities; different spellings alone do not establish separation.
Declare all endpoints. Contradictory facts, dangling endpoints and cycles fail.

Facts use one nonblank string or a list of 1–8 distinct nonblank strings as their
value. The namespace and value are compared exactly. For common presence and age
facts, use these shared neutral spellings when they express the actual request:

| dimension | property | value_type | value |
| --- | --- | --- | --- |
| `subject` | `entity.presence` | `entity.presence/v1` | `present` |
| `subject` | `anatomy.face.presence` | `anatomy.face.presence/v1` | `present` |
| `subject` | `anatomy.hair.presence` | `anatomy.hair.presence/v1` | `present` |
| `subject` | `anatomy.nails.presence` | `anatomy.nails.presence/v1` | `present` |
| `age` | `age.declared` | `age.declared/v1` | `adult` for explicitly declared adulthood |

These are authoring conventions, not entailment rules or default facts. Use the
actual owner of the asserted property. A human category, material label, role
address, adult-treatment permission or newly introduced candidate does not
witness any row. Exact numeric age, another body part, a depicted face, and a
separate actor require their own actual source-grounded meanings. For other
properties, declare a precise namespace and exact value independently; the
validator does not translate synonyms or infer a value from the property name.
Dimension, property, actual owner, value type and value are one exact protocol
tuple. A different presence spelling or dimension does not match this tuple.
Keep several required parts as independently grounded atomic facts when their
meaning is minimum presence; an exact whole-set anatomy value does not become
a subset query. Extra unrelated atomic facts do not establish a missing part.

For example, these fragments describe an already requester-specified red cup.
They assume an active span `topic`, the literal baseline phrase `red ceramic
cup`, and an existing color property anchor with target `cup_01` and property
`surface.color`. They are not a complete core or instructions to add a cup:

```json
[
  {
    "assertion_id": "cup_owner", "dimension": "subject", "polarity": "required",
    "source_span_ids": ["topic"], "affected_dimensions": ["subject"],
    "axes": {"native_schema": "photo-frozen-semantics/v1", "kind": "owner", "owner": "cup_01", "owner_kind": "object"},
    "evidence": {"subject_phrase": "red ceramic cup"}
  },
  {
    "assertion_id": "cup_role", "dimension": "subject", "polarity": "required",
    "source_span_ids": ["topic"], "affected_dimensions": ["subject"],
    "axes": {"native_schema": "photo-frozen-semantics/v1", "kind": "role", "role": "main_subject", "owner": "cup_01"},
    "evidence": {"subject_phrase": "red ceramic cup"}
  },
  {
    "assertion_id": "cup_color", "dimension": "color", "polarity": "required",
    "source_span_ids": ["topic"], "affected_dimensions": ["color"],
    "axes": {"native_schema": "photo-frozen-semantics/v1", "kind": "fact", "owner": "cup_01", "property": "surface.color", "value_type": "surface.color/v1", "value": "red"},
    "evidence": {"color_phrase": "red ceramic cup"}
  }
]
```

The complete core permits at most 64 assertion rows in total and 32 actual
owners. Keep only grounded necessary facts and relationships; do not merge
owners, drop required meanings or broaden locks to fit. The neutral helper
`photo_semantic_witnesses.py` validates shape, exact bindings and graph
consistency. It cannot prove the author's interpretation or rendered pixels.

Freeze these witnesses with the independent core. Missing facts remain missing
after retrieval. Do not inspect candidate requirements and then retrofit an
owner, age, anatomy or preservation fact to make that candidate pass.
