"""Read authored sources only; emit a dated lexical-neighbor research snapshot."""
from pathlib import Path
import collections, datetime, hashlib, json, re, sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
sys.path.insert(0, str(ROOT))
from photo_source_manifest import SourceInventory
from tools.photo_data_maintenance.corpus import raw_entities

def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

assets = SKILL / 'assets'
inventory = SourceInventory.load(assets)
kinds = {'photo_prompt_tags.json': 'candidate', 'photo_prompt_visual_obligations.json': 'visual_profile'}
for name, kind, required, order in inventory.rows:
    if kind in {'candidate', 'visual_profile'}:
        kinds[name] = kind
blobs = {name: (assets/name).read_bytes() for name in kinds}
values = {name: json.loads(blob) for name, blob in blobs.items()}
findings = []
entities, pointers = raw_entities(values, kinds, findings)

def normalize(text):
    return re.sub(r'[\s_\-–—]+', ' ', str(text).lower()).strip()

def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for v in value:
            yield from strings(v)
    elif isinstance(value, dict):
        for v in value.values():
            yield from strings(v)

def positive(record, kind):
    if kind == 'profile':
        sem = record.get('semantics', {})
        act = record.get('activation', {})
        return list(strings([record.get('id'), act.get('exact_terms'), sem.get('definition'),
            sem.get('paraphrase_examples'), sem.get('visual_components'), record.get('concept_candidate')]))
    keys = ('id', 'ko', 'en', 'label', 'aliases', 'keywords', 'embedding_text', 'concept_units',
            'relations', 'concept_terms', 'visual_profile_id', 'visual_profile_ids')
    return list(strings([record.get(k) for k in keys]))

positive_fields = {key: '\n'.join(normalize(v) for v in positive(node['record'], node['kind']))
                   for key, node in entities.items()}
terms = [r for r in json.loads((OUT/'thread-rows.json').read_text()) if r['section'] <= 15]
neighbors = []
for term in terms:
    label = term['label'].replace('†', '')
    chunks = re.split(r' — | / |·', label)
    needles = sorted({normalize(c) for c in chunks if len(normalize(c)) >= 3})
    patterns = {q: re.compile(r'(?<![a-z0-9])'+re.escape(q)+r'(?![a-z0-9])') for q in needles if re.search(r'[a-z]',q)}
    matches = []
    for key, fields in positive_fields.items():
        hits = [q for q in needles if (patterns[q].search(fields) if q in patterns else q in fields)]
        if hits:
            matches.append({'entity_id':key, 'kind':entities[key]['kind'],
                'matched_queries':hits, 'source_locations':pointers[key],
                'record_sha256':hashlib.sha256(json.dumps(entities[key]['record'],ensure_ascii=False,sort_keys=True).encode()).hexdigest()})
    matches.sort(key=lambda m:(-len(m['matched_queries']),m['entity_id']))
    neighbors.append({'term_id':term['term_id'], 'label':term['label'], 'queries':needles,
        'positive_lexical_hit_count':len(matches), 'review_neighbors':matches[:12],
        'meaning_support':'not_inferred', 'runtime_exposure':'not_tested'})

loader = {}
try:
    import prompt_generator as pg
    data = pg.load_json(assets/'photo_prompt_tags.json', inventory=inventory)
    registry = pg.load_visual_obligation_registry(assets/'photo_prompt_visual_obligations.json', inventory=inventory)
    loader = {'status':'PASS', 'slots':len(data.get('slots',{})),
        'candidates':sum(len(rows) for rows in data.get('slots',{}).values()),
        'profiles':len(registry.get('profiles',[])), 'bundles':len(data.get('candidate_bundles',[])),
        'scope':'Authored-source loader validation at this snapshot; no retrieval, index freshness or runtime publication claim'}
except Exception as error:
    loader = {'status':'FAIL', 'error_type':type(error).__name__, 'error':str(error),
        'scope':'Raw-source lexical snapshot is retained; loader failure is not repaired by research'}
summary = {'observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'source_root':str(SKILL), 'manifest_rows':len(inventory.rows), 'source_files_scanned':len(blobs),
    'entity_counts':dict(collections.Counter(n['kind'] for n in entities.values())),
    'source_sha256':{name:hashlib.sha256(blob).hexdigest() for name,blob in blobs.items()},
    'source_manifest_sha256':hashlib.sha256((assets/'photo_prompt_source_manifest.json').read_bytes()).hexdigest(),
    'raw_structural_findings':findings, 'authored_loader':loader,
    'terms_with_lexical_neighbors':sum(bool(n['positive_lexical_hit_count']) for n in neighbors),
    'terms_without_lexical_neighbors':sum(not n['positive_lexical_hit_count'] for n in neighbors),
    'embedding_calls':0, 'image_calls':0, 'runtime_dispatch_calls':0,
    'warning':'A positive text hit is a review lead, not proof of equivalent meaning, retrieval quality, hard activation, selection or pixels.'}
write('current-inventory.json',summary)
write('current-positive-neighbors.json',neighbors)
selected = {m['entity_id'] for n in neighbors for m in n['review_neighbors']}
write('current-authored-entities.json',{'entities':{k:entities[k] for k in sorted(selected)},
    'locations':{k:pointers[k] for k in sorted(selected)},'scope':'Lexical review neighbors only; full corpus counts are in current-inventory.json'})
print(json.dumps({k:summary[k] for k in ['entity_counts','authored_loader','terms_with_lexical_neighbors','terms_without_lexical_neighbors']},ensure_ascii=False,indent=2))
