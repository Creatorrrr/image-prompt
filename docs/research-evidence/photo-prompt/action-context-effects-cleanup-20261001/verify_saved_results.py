"""Recompute saved diagnostics using existing vectors; no credentials or network."""
from pathlib import Path
import copy, gzip, hashlib, json, math, sys, tempfile
ROOT = Path(__file__).resolve().parents[4]
E = Path(__file__).resolve().parent
A = ROOT / 'skills/photo-prompt-image-generator/assets'
sys.path.insert(0, str(A.parent / 'scripts'))
import prompt_generator as g
from bm25f_retrieval import rank_bm25f
F = json.loads((E / 'frozen-inventory-queries.json').read_text())
B = json.loads(gzip.decompress((E / 'baseline-merged-data.json.gz').read_bytes()))
assert g.dictionary_hash(B) == F['baseline_dictionary_hash']
assert hashlib.sha256((E / 'frozen-inventory-queries.json').read_bytes()).hexdigest() == (E / 'frozen-sha256.txt').read_text().split()[0]
with tempfile.NamedTemporaryFile(dir=A, suffix='.json', delete=False) as handle:
    temporary = Path(handle.name)
    handle.write((E / 'baseline-index-manifest.json').read_bytes())
try:
    old = g.load_semantic_index(temporary, B)
finally:
    temporary.unlink()
D = g.load_json(A / 'photo_prompt_tags.json')
final = g.load_semantic_index(A / 'photo_prompt_semantic_index.json', D)
cache = json.loads((E / 'new-vector-cache.json').read_text())
attempts = json.loads((E / 'api-attempts.json').read_text())
assert len(attempts) == len({x['sha256'] for x in attempts}) == 48
assert all(x['status'] == 'completed' for x in attempts)
assert len(final['entries']) == 9887
changed = [k for k in old['entries'] if old['entries'][k]['text'] != final['entries'][k]['text']]
assert len(changed) == 16
for key, row in final['entries'].items():
    if key in changed:
        assert row['vector'] == cache[hashlib.sha256(row['text'].encode()).hexdigest()]['vector']
    else:
        assert row['vector'] == old['entries'][key]['vector']
for attempt in attempts:
    item = cache[attempt['sha256']]
    assert hashlib.sha256(item['text'].encode()).hexdigest() == attempt['sha256']
    assert item['model'] == 'gemini-embedding-2' and item['dimensions'] == 768
    assert len(item['vector']) == 768 and all(math.isfinite(x) for x in item['vector'])

def make_index(data):
    bm = g.build_semantic_bm25f_payload(data)
    entries = {}
    for key, kind, entry, slot in g.iter_semantic_entries(data):
        text = g.semantic_text_for_entry(entry, slot, kind=kind)
        cached = old['entries'][key] if old['entries'][key]['text'] == text else final['entries'][key]
        assert cached['text'] == text
        entries[key] = {'kind':kind, 'slot':slot, 'id':entry['id'], 'text':text, 'vector':cached['vector'], 'bm25f_document':bm['documents'][key]}
    result = {'provider':g.SEMANTIC_PROVIDER, 'dictionary_hash':g.dictionary_hash(data), 'semantic_text_recipe':g.SEMANTIC_TEXT_RECIPE_VERSION, 'embedding_model':g.SEMANTIC_MODEL_ID, 'embedding_dimensions':768, 'bm25f':{k:v for k,v in bm.items() if k != 'documents'}, 'entries':entries}
    g.validate_semantic_index_metadata(result, data)
    return result, bm

def cosine(a, b):
    return sum(x*y for x,y in zip(a,b))/(math.sqrt(sum(x*x for x in a))*math.sqrt(sum(x*x for x in b)))

def verify_snapshot(name, data):
    index, bm = make_index(data)
    dense = json.loads((E/f'dense-{name}.json').read_text())
    lexical = json.loads((E/f'lexical-{name}.json').read_text())
    for q, saved_dense, saved_lexical in zip(F['queries'], dense, lexical):
        vector = cache[hashlib.sha256(q['query'].encode()).hexdigest()]['vector']
        scores = [{'id':k, 'score':round(cosine(vector,e['vector']),12)} for k,e in index['entries'].items() if e['kind']=='slot' and e['slot']==q['slot']]
        scores.sort(key=lambda x:(-x['score'],x['id']))
        rank = next(i for i,x in enumerate(scores,1) if x['id']==q['target'])
        assert rank == saved_dense['rank'] and scores[:5] == saved_dense['top5'], (name,q['id'],'dense')
        assert scores[rank-1]['score'] == saved_dense['target_score']
        ids = ['slot:'+q['slot']+':'+e['id'] for e in data['slots'][q['slot']]]
        ranks = rank_bm25f(bm, {'query':q['query']}, allowed_ids=ids, limit=len(ids))
        rank = next((i for i,x in enumerate(ranks,1) if x['document_id']==q['target']),None)
        assert rank == saved_lexical['rank'] and ranks[:5] == saved_lexical['top5'], (name,q['id'],'lexical')
    print(name+': 32 dense and lexical comparisons match', flush=True)

verify_snapshot('baseline', B)
stage = copy.deepcopy(B)
for number in [1,2,3]:
    ledger = json.loads((E/f'changes-stage{number}.json').read_text())
    for change in ledger['changes']:
        rows = stage['slots'][change['slot']]
        pos = next(i for i,row in enumerate(rows) if row['id']==change['id'])
        assert rows[pos] == change['before']
        rows[pos] = change['after']
    if number == 3:
        stage['candidate_bundles'] = D['candidate_bundles']
    assert g.dictionary_hash(stage) == ledger['after_dictionary_hash']
    verify_snapshot(f'stage{number}', stage)
verify_snapshot('final', D)
print('Verified 48 unique attempts, 16 new vectors, 9871 unchanged vectors, and all 160 paired-query snapshots')
