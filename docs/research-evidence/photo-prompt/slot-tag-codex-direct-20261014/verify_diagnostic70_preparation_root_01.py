"""Read-only sparse preparation checks followed by exact research-only staging."""
import ast
import gzip
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path.cwd()
R = ROOT / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'


def read(p):
    raw = p.read_bytes()
    return json.loads(gzip.decompress(raw) if p.suffix == '.gz' else raw)


def digest(v):
    return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


cache = {}


def raw(p):
    if p not in cache:
        cache[p] = (hashlib.sha256(p.read_bytes()).hexdigest(), read(p) if p.suffix in ('.json', '.gz') else None)
    return cache[p]


def refs(v):
    if isinstance(v, dict):
        if 'file' in v and 'file_sha256' in v:
            p = ROOT / v['file']
            assert p.resolve().is_relative_to(ROOT.resolve())
            assert raw(p)[0] == v['file_sha256']
            if set(v) == {'file', 'file_sha256', 'sha256'}:
                assert digest(raw(p)[1]) == v['sha256']
        for x in v.values():
            refs(x)
    elif isinstance(v, list):
        for x in v:
            refs(x)


D = R / 'native-inputs/root-diagnostic-kind-source-plan-18'
P = R / 'native-inputs/prepared/review05250-diagnostic70-149-01'
original = read(R / 'SOURCE.json.gz')
parent = read(R / 'native-inputs/root-lower-lashes-source-plan-16-R02/CURRENT-PROPOSAL.json.gz')
current = read(D / 'CURRENT-PROPOSAL.json.gz')
assert digest(current) == '08c699d25b3b6117c26f1ab6f05175b7db013ad17c69e44a9d2fd7acbcb5ea9c'
memo = read(D / 'ROOT-SOURCE-SELECTION.json')
chosen = memo['selected']
changed = {k for k in current['candidates'] if current['candidates'][k] != parent['candidates'][k]}
assert changed == {r['candidate_id'] for r in chosen} and len(changed) == 5
for row in chosen:
    cid = row['candidate_id']; a = current['candidates'][cid]; b = parent['candidates'][cid]
    assert a == row['after'] and b == row['before'] and b['record_kind'] == 'diagnostic' and a['record_kind'] == 'visual_option'
    assert {k:v for k,v in a.items() if k != 'record_kind'} == {k:v for k,v in b.items() if k != 'record_kind'}
    assert row['native_proof'] is None and row['complete_positive_contract_selected'] is False
assert all(current[k] == parent[k] for k in ('slot_catalog', 'slot_bindings', 'policies'))
assert Counter(r['record_kind'] for r in current['candidates'].values())['diagnostic'] == 65
approval = read(D / 'SOURCE-APPROVAL.json')
assert len(approval['changes']) == 71 and approval['current_source_sha256'] == digest(current)
assignment = read(P / 'ASSIGNMENT.json'); inp = read(P / 'INPUT.json'); packet = read(P / 'PREPARED-PACKET.json'); receipt = read(P / 'PREPARATION.json')
order = raw(ROOT / inp['order']['file'])[1]
assert len(assignment['ids']) == len(set(assignment['ids'])) == 70
assert [order[o] for o in assignment['ordinals']] == assignment['ids'] == inp['ids'] == packet['ids']
assert assignment['task_name'] == '/root/review_05250_06250' and assignment['model'] == 'gpt-6.1-sol' and assignment['reasoning_effort'] == 'high'
assert packet['actual_read_count'] == receipt['actual_read_count'] == 0
assert packet['prepared_count'] == receipt['prepared_count'] == 70
assert receipt['native_proofs_created'] == receipt['operating_changes'] == receipt['Gemini_calls'] == 0
assert not receipt['contiguous_helper_modified']
assert {cid for cid,r in original['candidates'].items() if r['record_kind'] == 'diagnostic'} == set(assignment['ids'])
for cid in assignment['ids']:
    assert packet['original_records'][cid] == original['candidates'][cid]
    assert packet['current_records'][cid] == current['candidates'][cid]
    assert packet['references'][cid] == packet['reference_bindings'][cid] == {}
    loc = inp['original_decisions'][cid]; doc = raw(ROOT / loc['file'])[1]
    row = doc['decisions'][loc['item']-1]
    assert row == packet['historical_compiled_rows'][cid] and digest(row) == loc['row_sha256'] and row['candidate_id'] == cid
    req = inp['required_revisions'][cid]
    assert req['prior_review']['pointer'] == '/decisions/' + str(loc['item']-1) and req['prior_review']['sha256'] == digest(row)
protected = {'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md':'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359',
             'docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md':'0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b'}
for name, h in protected.items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == h
assert not subprocess.check_output(['git','diff','--cached','--name-only'], text=True).strip()
paths = [R/'prepare_diagnostic70_root_01.py', Path(__file__), *sorted(D.iterdir()), *sorted(P.iterdir()),
         ROOT/'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md',
         *sorted((R/'authored').glob('native_diag70_*')), *sorted((R/'worker-notes').glob('native_diag70_*'))]
pins = {}
for p in paths:
    if p.suffix in ('.json', '.gz'):
        refs(read(p))
    elif p.suffix == '.py':
        ast.parse(p.read_bytes())
    pins[str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
report = R / 'ROOT-DIAGNOSTIC70-PREPARATION-01.json'
value = dict(schema='photo-root-sparse-preparation-verification/v1', actor='/root', source_changes_total=71, sparse_prepared=70,
             root_source_kind_restorations=5, remaining_diagnostic=65, positive_contracts_selected=0, native_proofs_created=0,
             operating_changes=0, Gemini_calls=0, source_body_effect_conditions_provenance_preserved=True,
             catalog_bindings_policies_unchanged=True, strict_contiguous_helper_unchanged=True,
             meaning_review_boundary='Root source-kind decision and frozen fresh input only. Worker recommendations are not native approvals. All70 source bodies and all5 detailed contexts were read by root in the ongoing task; full70 historical/parent reading is independently credited to the worker.',
             files=pins, protected_files=protected)
with report.open('xb') as f:
    f.write(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode() + b'\n')
names = sorted(set(pins) | {str(report.relative_to(ROOT))})
subprocess.run(['git','add','--',*names], check=True)
subprocess.run(['git','diff','--cached','--check'], check=True)
assert set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines()) == set(names)
for name in names:
    assert subprocess.check_output(['git','show',':'+name]) == (ROOT/name).read_bytes()
print(json.dumps(dict(files=len(names), sparse_prepared=70, kind_restorations=5, native_proofs_created=0, operating_changes=0, Gemini_calls=0)))
