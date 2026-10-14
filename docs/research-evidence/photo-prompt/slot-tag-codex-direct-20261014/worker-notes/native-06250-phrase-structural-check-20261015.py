"""Read-only structural comparison. Writes only its uniquely named research report.

No semantic classification, corpus validation, embedding, runtime build or approval.
"""
import ast
import copy
import difflib
import gzip
import hashlib
import json
from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parents[5]
SCRIPTS = ROOT/'skills/photo-prompt-image-generator/scripts'
sys.path.insert(0, str(SCRIPTS))
import photo_candidate_corpus as c
import photo_candidate_realizations as r
import photo_semantic_evidence as e
import photo_global_index as g
import photo_native_pack as pack
import photo_search_layout as layout

HERE = Path(__file__).resolve().parent
R = HERE.parent
BASELINE = HERE/'native-06250-phrase-consumer-before-20261015.json'
OUT = HERE/'native-06250-phrase-structural-report-20261015.json'
PATCH = HERE/'native-06250-phrase-consumer-20261015.patch'
assert not OUT.exists() and not PATCH.exists()
sha = lambda value: hashlib.sha256(value).hexdigest()
baseline = json.loads(BASELINE.read_text())
old_modules = {}
patches = []
for name in ('photo_semantic_evidence', 'photo_global_index'):
    path = SCRIPTS/(name+'.py')
    before = baseline[str(path.relative_to(ROOT))]
    assert sha(before['source'].encode()) == before['raw_sha256']
    module = types.ModuleType('_before_'+name)
    module.__file__ = str(path)
    exec(compile(before['source'], str(path)+' [captured before]', 'exec'), module.__dict__)
    old_modules[name] = module
    patches.extend(difflib.unified_diff(before['source'].splitlines(True), path.read_text().splitlines(True),
        fromfile=str(path.relative_to(ROOT))+' before', tofile=str(path.relative_to(ROOT))+' after'))
old_e, old_g = old_modules['photo_semantic_evidence'], old_modules['photo_global_index']
assert e.POSITIVE_FIELDS - old_e.POSITIVE_FIELDS == {'phrase_en', 'phrase_ko'}
assert old_e.POSITIVE_FIELDS <= e.POSITIVE_FIELDS

def without_positive_fields(source):
    tree = ast.parse(source)
    tree.body = [node for node in tree.body if not (isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == 'POSITIVE_FIELDS' for target in node.targets))]
    return ast.dump(tree, include_attributes=False)
assert without_positive_fields(baseline[str((SCRIPTS/'photo_semantic_evidence.py').relative_to(ROOT))]['source']) == without_positive_fields((SCRIPTS/'photo_semantic_evidence.py').read_text())

def load(path):
    raw = path.read_bytes()
    data = json.loads(gzip.decompress(raw) if path.suffix == '.gz' else raw)
    return data, {'file': str(path.relative_to(ROOT)), 'raw_sha256': sha(raw), 'canonical_sha256': c.digest(data)}

source, source_locator = load(R/'SOURCE.json.gz')
inventory, inventory_locator = load(HERE/'native-08250-phrase-fields-inventory-20261015.json')
assert len(source['candidates']) == 18250
assert source_locator['canonical_sha256'] == inventory['source_canonical_sha256']
expected = {row['candidate_id'] for row in inventory['rows']}
rows = []
unchanged = []
all_record_hashes = {cid: c.digest(record) for cid, record in source['candidates'].items()}
for cid, record in source['candidates'].items():
    before_fields, after_fields = old_g.fields(record), g.fields(record)
    before_recipe, before_text = old_g.text(record)
    after_recipe, after_text = g.text(record)
    paths = {}
    for rid in r.ids(record):
        before_paths, after_paths = old_e.primary_paths(record, rid), e.primary_paths(record, rid)
        assert before_paths <= after_paths
        if before_paths != after_paths:
            paths[rid] = sorted(after_paths-before_paths)
    changed = before_fields != after_fields or (before_recipe, before_text) != (after_recipe, after_text) or bool(paths)
    if changed:
        assert cid in expected and r.ids(record) == ['base'] and record['record_kind'] == 'visual_option'
        assert paths == {'base': ['/content/phrase_en', '/content/phrase_ko']}
        assert before_fields.keys() == after_fields.keys()
        assert {k:v for k,v in before_fields.items() if k!='labels'} == {k:v for k,v in after_fields.items() if k!='labels'}
        assert after_fields['labels'] == before_fields['labels']+[record['content']['phrase_en'], record['content']['phrase_ko']]
        assert before_recipe == old_g.RECIPE and after_recipe == g.PHRASE_RECIPE
        rows.append({'candidate_id': cid, 'actual_rids': r.ids(record), 'added_primary_paths': paths,
            'source_record_sha256': c.digest(record), 'changed_field_names': ['labels'],
            'before_fields_sha256': c.digest(before_fields), 'after_fields_sha256': c.digest(after_fields),
            'before_recipe': before_recipe, 'after_recipe': after_recipe,
            'before_text_sha256': sha(before_text.encode()), 'after_text_sha256': sha(after_text.encode()),
            'text_bytes_changed': before_text.encode()!=after_text.encode()})
    else:
        assert c.canonical_bytes(before_fields) == c.canonical_bytes(after_fields)
        assert before_text.encode() == after_text.encode() and before_recipe.encode() == after_recipe.encode()
        unchanged.append({'candidate_id': cid, 'fields_sha256': c.digest(after_fields),
                          'recipe': after_recipe, 'text_sha256': sha(after_text.encode())})
assert {row['candidate_id'] for row in rows} == expected and len(rows) == 381
assert sum(len(paths) for row in rows for paths in row['added_primary_paths'].values()) == 762
assert all_record_hashes == {cid:c.digest(record) for cid,record in source['candidates'].items()}

current, current_locator = load(R/'native-inputs/11870-01250-01300-plan-04/CURRENT-PROPOSAL.json.gz')
assert current_locator['canonical_sha256'] == '88614a52f5e4148efc57806c641717107c2b045acfc205e934f96246af8a81d8'
assert len(current['candidates']) == 18250

def application_inventory(data):
    result=[]
    for cid, record in data['candidates'].items():
        if 'application_contract' not in record['content']:
            continue
        value = record['content']['application_contract']
        result.append({'candidate_id':cid, 'value_type':type(value).__name__,
            'value':value, 'source_record_sha256':c.digest(record),
            'primary_path_present_by_rid':{rid:'/content/application_contract' in e.primary_paths(record,rid)
                                         for rid in r.ids(record)}})
    return result

base_app, current_app = application_inventory(source), application_inventory(current)
formal_paths = [R/'native_batches/review11870-01250-01300-03/BATCH.json'] + [
    R/('native_batches/review11870-01250-01300-04/CHECKPOINT-'+span+'.json')
    for span in ('01250-01255','01255-01260','01260-01265','01265-01270')]
formal_reports = []
for path in formal_paths:
    batch, locator = load(path)
    records = batch['records']
    audits = []
    for number, row in enumerate(records):
        assert {'candidate_id','source_after','proof','status','ordinal'} <= row.keys()
        cid, record, proof = row['candidate_id'], row['source_after'], row['proof']
        assert record['id'] == cid and isinstance(record['content'],dict)
        assert proof is None or isinstance(proof,dict)
        app = record['content'].get('application_contract')
        matches_current = c.canonical_bytes(record) == c.canonical_bytes(current['candidates'][cid])
        units = [] if proof is None else [u for u in proof['source_units'] if u['pointer']=='/content/application_contract']
        facts = [] if proof is None else [f for f in proof['facts'] if f['pointer']=='/content/application_contract']
        exact_normal = [u for u in units if u['disposition'] in {'semantic','nonsemantic'} and u['quote']==app]
        audits.append({'candidate_id':cid,'ordinal':row['ordinal'],'pointer':'/records/'+str(number),
            'row_keys':sorted(row), 'row_sha256':c.digest(row), 'source_after_sha256':c.digest(record),
            'source_after_exact_current':matches_current,'status_as_authored':row['status'],
            'proof_present':proof is not None, 'proof_sha256':c.digest(proof) if proof is not None else None,
            'application_contract_present':app is not None,
            'application_primary_by_rid':{rid:'/content/application_contract' in e.primary_paths(record,rid) for rid in r.ids(record)},
            'exact_ordinary_application_units':len(exact_normal),
            'application_unit_dispositions':[u['disposition'] for u in units],
            'application_fact_count':len(facts),
            'current_source_proof_pair':matches_current and proof is not None,
            'semantic_approval_inferred':False})
    formal_reports.append({'artifact':locator,'record_count':len(records),'rows':audits})
reopen_path = R/'native_batches/review11870-01250-01300-04/REOPEN-01257-QUOTE-v1.json'
reopen, reopen_locator = load(reopen_path)
prior_locator = reopen['before_checkpoint']
prior_batch = next(b for b in formal_reports if b['artifact']['file']==prior_locator['file'])
assert prior_batch['artifact']['canonical_sha256']==prior_locator['sha256']
row_index = int(prior_locator['pointer'].split('/')[-1])
assert prior_batch['rows'][row_index]['row_sha256']==prior_locator['row_sha256']
assert reopen['record']['ordinal']==1257 and reopen['record']['proof'] is None and reopen['record']['status']=='pending'
effective04 = {row['ordinal']:copy.deepcopy(row) for batch in formal_reports[1:] for row in batch['rows']}
effective04[1257].update(status_as_authored='pending',proof_present=False,proof_sha256=None,
    exact_ordinary_application_units=0,application_unit_dispositions=[],application_fact_count=0,
    current_source_proof_pair=False, override=reopen_locator)
assert len(effective04)==20

modules = {module.__name__:{'path':module.__file__,'raw_sha256':sha(Path(module.__file__).read_bytes())}
           for module in (c,r,e,g,pack,layout)}
report = {'schema':'photo-named-phrase-structural-comparison/v1','task_name':'/root/review_06250_07250',
    'model':'gpt-6.1-sol','reasoning_effort':'high','source':source_locator,'inventory':inventory_locator,
    'source_candidate_count':18250,'phrase_candidate_count':381,'added_positive_string_count':762,
    'changed_fields_count':sum(row['before_fields_sha256']!=row['after_fields_sha256'] for row in rows),
    'changed_text_count':sum(row['text_bytes_changed'] for row in rows), 'changed_recipe_count':len(rows),
    'unaffected_count':len(unchanged),'unaffected_byte_identity':True,
    'unaffected_exact_projection_manifest_sha256':c.digest(unchanged), 'unaffected_projection_manifest':unchanged,
    'changed_rows':rows,'source_unmodified_in_memory':True,'source_raw_file_unchanged':sha((R/'SOURCE.json.gz').read_bytes())==source_locator['raw_sha256'],
    'actual_loaded_modules':modules, 'semantic_evidence_ast_except_positive_fields_unchanged':True,
    'query_recipe_unchanged':g.QUERY_RECIPE==old_g.QUERY_RECIPE,'embedding_space_unchanged':g.SPACE==old_g.SPACE,
    'same_space_projection_reuse_identity_counts':{'exact_cid_recipe_text_sha_preserved':len(unchanged),
                                                  'changed_recipe_requires_new_vector':len(rows)},
    'application_contract_read_only_audit':{'original_count':len(base_app),'original_rows':base_app,
        'current_source':current_locator,'current_count':len(current_app),'current_rows':current_app,
        'explicit_formal_artifacts':formal_reports,'reopen_override':reopen_locator,
        'effective04_record_count':len(effective04),'effective04_rows':list(effective04.values()),
        'scope':'Structural exact source/proof pairing only; no native validity or meaning approval inferred. Historical rows remain historical.'},
    'new_semantic_direct_review_count':0,'native_approvals':0,'model_calls':0,'network_calls':0,
    'runtime_or_asset_builds':0,'semantic_reference_contract_changed':False}
PATCH.write_text(''.join(patches))
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ('source_candidate_count','phrase_candidate_count','added_positive_string_count','changed_fields_count','changed_text_count','changed_recipe_count','unaffected_count')},indent=2))
print('application original/current',len(base_app),len(current_app))
for batch in formal_reports:
    print(batch['artifact']['file'], 'rows',len(batch['rows']), 'current source matches',sum(row['source_after_exact_current'] for row in batch['rows']), 'proofs',sum(row['proof_present'] for row in batch['rows']), 'exact app ordinary units',sum(row['exact_ordinary_application_units'] for row in batch['rows']))
print('effective04',len(effective04),'proofs',sum(row['proof_present'] for row in effective04.values()),'app units',sum(row['exact_ordinary_application_units'] for row in effective04.values()))
print('report',OUT,'rawsha',sha(OUT.read_bytes()))
