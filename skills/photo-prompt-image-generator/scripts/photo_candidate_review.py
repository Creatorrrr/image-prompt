"""Grounded source-only review contract. Structural checks are not truth proofs."""
from photo_candidate_authoring import digest, canonical

SCHEMA = 'photo-candidate-source-review/v1'
DECISIONS = {'enrich', 'retain', 'needs_semantic_edit', 'defer', 'diagnostic'}
KINDS = {'entity', 'action', 'relation', 'attribute', 'context', 'condition'}
FIELDS = {'schema', 'candidate_id', 'source_sha256', 'decision', 'rationale', 'realizations', 'slot_tags', 'review'}
RID_FIELDS = {'summary_en', 'summary_ko', 'anchors', 'facets', 'search_aliases', 'unknowns'}


def require(value, reason):
    if not value:
        raise ValueError(reason)


def text(value, maximum=1000, *, empty=False):
    require(isinstance(value, str) and len(value) <= maximum and (empty or bool(value.strip())), 'invalid review text')
    require(not any(ord(c) < 32 and c not in '\n\t' for c in value), 'control character in review')


def anchors(items, record, rid):
    require(isinstance(items, list) and 1 <= len(items) <= 12, 'grounded source anchors required')
    units = record['meaning']['primary'][rid]
    seen = set()
    for item in items:
        require(isinstance(item, dict) and set(item) == {'pointer', 'quote'}, 'exact source pointer/quote required')
        pointer = item['pointer']
        require(pointer in units and record['meaning']['literals'][units[pointer]] == item['quote'], 'anchor is not an exact primary source unit on this RID')
        require(pointer not in seen, 'duplicate source anchor')
        seen.add(pointer)


def validate(row, record, catalog):
    require(isinstance(row, dict) and set(row) == FIELDS, 'complete source-review fields required')
    require(row['schema'] == SCHEMA and row['candidate_id'] == record['id'] and row['source_sha256'] == digest(record), 'review source identity changed')
    require(row['decision'] in DECISIONS, 'unknown source review decision')
    text(row['rationale'], 1600)
    require(row['review'] == {'author': 'gpt-6-luna', 'effort': 'max', 'source_only': True, 'native_approval': False}, 'review provenance or authority changed')
    require(isinstance(row['realizations'], dict) and set(row['realizations']) == set(record['meaning']['primary']), 'actual RID coverage required')
    for rid, value in row['realizations'].items():
        require(isinstance(value, dict) and set(value) == RID_FIELDS, 'complete realization review required')
        text(value['summary_en'], 900, empty=row['decision'] in {'defer', 'needs_semantic_edit'})
        text(value['summary_ko'], 600, empty=row['decision'] in {'defer', 'needs_semantic_edit'})
        require(len(value['summary_en'].split()) <= 80, 'summary exceeds80 words')
        anchors(value['anchors'], record, rid)
        require(isinstance(value['facets'], list) and len(value['facets']) <= 12, 'facet budget exceeded')
        for facet in value['facets']:
            require(isinstance(facet, dict) and set(facet) == {'kind', 'text_en', 'anchors'} and facet['kind'] in KINDS, 'typed grounded facet required')
            text(facet['text_en'], 400);anchors(facet['anchors'], record, rid)
        require(isinstance(value['search_aliases'], list) and len(value['search_aliases']) <= 6, 'alias budget exceeded')
        for alias in value['search_aliases']:
            require(isinstance(alias, dict) and set(alias) == {'text', 'anchors'}, 'grounded alias required')
            text(alias['text'], 160);anchors(alias['anchors'], record, rid)
        require(isinstance(value['unknowns'], list) and len(value['unknowns']) <= 8, 'unknown budget exceeded')
        for unknown in value['unknowns']:
            text(unknown, 500)
    require(isinstance(row['slot_tags'], list) and len(row['slot_tags']) <= 6, 'slot tag budget exceeded')
    seen = set()
    for tag in row['slot_tags']:
        require(isinstance(tag, dict) and set(tag) == {'slot_id', 'realization_id', 'rationale', 'anchors'}, 'grounded slot tag required')
        require(tag['slot_id'] in catalog and tag['realization_id'] in row['realizations'], 'unknown slot or realization')
        key = (tag['slot_id'], tag['realization_id'])
        require(key not in seen, 'duplicate slot tag');seen.add(key)
        text(tag['rationale'], 700);anchors(tag['anchors'], record, tag['realization_id'])
    if record['meaning']['retrieval_class'] == 'diagnostic':
        require(row['decision'] == 'diagnostic', 'diagnostic source is not positive material')
    require(len(canonical(row)) <= 65536, 'review payload exceeds64KiB')
    return row
