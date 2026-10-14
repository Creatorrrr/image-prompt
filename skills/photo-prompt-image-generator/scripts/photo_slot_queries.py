"""Post-freeze, candidate-free role queries and immutable provider contexts."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import photo_candidate_corpus as c
from photo_embedding_provider import embed, embed_many, SPACE, default_space, validate_vector, validate_execution
import re
HASH=re.compile(r'[0-9a-f]{64}\Z')

RECIPE = 'photo-independent-slot-query/v2'
SCHEMA = 'photo-slot-query-set/v2'
CONTEXT_SCHEMA = 'photo-slot-query-vector/v2'


def specification(catalog, slot):
    if slot not in catalog:
        raise ValueError('unknown managed slot: ' + slot)
    row = catalog[slot]
    return {'recipe': RECIPE, 'slot_id': slot, 'focus_en': row['description'],
            'focus_ko': row['description_ko'], 'dimensions': row['dimensions'],
            'semantic_role': row['semantic_role'], 'owners': row['owners'],
            'property_prefixes': row['property_prefixes'], 'includes': row['includes'],
            'excludes': row['excludes'], 'neighbors': row['neighbors'],
            'core_fields': row['core_fields'], 'applicability': row['applicability'],
            'search_scope': 'whole_shared_positive_corpus'}


def inputs(core, controls, catalog, slot, language='en'):
    import prompt_generator as g
    if language not in {'en', 'ko'}:
        raise ValueError('unsupported slot query language')
    spec = specification(catalog, slot)
    global_text, _ = g.authorial_core_retrieval_text(core)
    projection, fields = g.candidate_pack_slot_focus_text(core, slot, catalog)
    focus = spec['focus_' + language] + (': ' + projection if projection else '')
    lexical = {'global_context': global_text, 'slot_focus': focus}
    text = global_text + '\nPhotographic role: ' + focus
    binding = {'recipe': RECIPE, 'slot_id': slot, 'slot_spec_sha256': c.digest(spec),
               'core_sha256': core['canonical_sha256'], 'controls_sha256': controls['canonical_sha256'],
               'language': language, 'query_fields': lexical, 'focus_fields': fields}
    if not global_text.strip() or any(not HASH.fullmatch(v) for v in (core['canonical_sha256'], controls['canonical_sha256'])):
        raise ValueError('slot queries require frozen core and controls')
    return text, lexical, binding


def context(core, controls, catalog, slot, cache, language='en', *, space=None, result=None):
    space=space or default_space()
    text, fields, binding = inputs(core, controls, catalog, slot, language)
    row = result or embed(text, binding, cache,space=space)
    value = {'schema': CONTEXT_SCHEMA, 'text': text, 'text_sha256': hashlib.sha256(text.encode()).hexdigest(),
             'binding': binding, 'space': space, 'vector': row['vector'], 'vector_sha256': row['vector_sha256'],
             'execution': row['execution'], 'cache_hit': row['cache_hit']}
    value['canonical_sha256'] = c.digest(value)
    return value


def validate(row, core, controls, catalog, slot, *, space=SPACE):
    language = (row.get('binding') or {}).get('language') if isinstance(row, dict) else None
    text, fields, binding = inputs(core, controls, catalog, slot, language)
    if (row.get('schema') != CONTEXT_SCHEMA or row.get('binding') != binding
            or row.get('space') != space or row.get('text') != text
            or row.get('text_sha256') != hashlib.sha256(text.encode()).hexdigest()
            or row.get('vector_sha256') != c.digest(row.get('vector'))
            or row.get('canonical_sha256') != c.digest({k:v for k,v in row.items() if k != 'canonical_sha256'})):
        raise ValueError('foreign or modified independent slot query')
    validate_vector(row.get('vector'))
    trace = row.get('execution') or {}
    validate_execution(trace,space,text,row['vector'])
    return fields


def prepare(core, controls, catalog, slots, cache, *, workers=4, language='en',space=None):
    slots = sorted(set(slots))
    space=space or default_space()
    if space['provider']=='embeddinggemma2-local':
        items=[inputs(core,controls,catalog,slot,language) for slot in slots]
        results=embed_many([x[0] for x in items],[x[2] for x in items],cache,space=space)
        rows=[context(core,controls,catalog,slot,cache,language,space=space,result=row) for slot,row in zip(slots,results,strict=True)]
    else:
        with ThreadPoolExecutor(max_workers=max(1, min(8, workers))) as pool:
            rows = list(pool.map(lambda slot: context(core, controls, catalog, slot, cache, language,space=space), slots))
    value = {'schema': SCHEMA, 'slots': dict(zip(slots, rows))}
    value['canonical_sha256'] = c.digest(value)
    return value


def validate_set(value, core, controls, catalog, slots, *, space=SPACE):
    if not isinstance(value, dict) or value.get('schema') != SCHEMA or set(value.get('slots', {})) != set(slots):
        raise ValueError('exact independent slot query set required')
    if value.get('canonical_sha256') != c.digest({k:v for k,v in value.items() if k != 'canonical_sha256'}):
        raise ValueError('slot query set checksum mismatch')
    return {slot: validate(value['slots'][slot], core, controls, catalog, slot,space=space) for slot in sorted(slots)}
