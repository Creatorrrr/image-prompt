#!/usr/bin/env python3
"""Exercise the actual staged H-F2 material search and replay its receipt audit."""
import json
import os
import copy
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(os.environ.get('FETISH_CONTEXT_OUTPUT', str(ROOT / 'generated/fetish-hf2-integration-20261108'))).resolve()
staged = json.loads((OUT / os.environ.get('FETISH_CONTEXT_STAGED', 'staged.json')).read_bytes())
store = Path.home() / '.cache/image-prompt/photo-shared-runtime/h-f2-installed'
native = store / 'generations' / staged['native_generation_id']
sys.path.insert(0, str(native / 'scripts'))
import photo_h_f2_workflow as workflow
from photo_h_f2_generation import Generation
from photo_h_f2_receipts import audit_packet
import photo_recall_first as rf

cases = [('foot-en', 'foot fetish', 'FASHION-CONTEXT-014'),
         ('latex-en', 'latex fetish', 'FASHION-CONTEXT-033'),
         ('general-en', 'leather jacket', None),
         ('negated-ko', '페티시 제외 가죽 재킷', None)]
g = Generation(store, staged['generation_id'], full=True)
query_set = {'schema': 'photo-h-f2-research-context-eval-queries/v1',
             'slots': {name: {'text': text, 'text_sha256': rf.sha(text)} for name, text, _ in cases},
             'query_scopes': {name: 'slot' for name, _, _ in cases}}
output = OUT / os.environ.get('FETISH_CONTEXT_SMOKE', 'managed-smoke')
packet = workflow.search_material(g, query_set, OUT / 'query-cache', output,
                                  skill=native, creativity=1, sampling_seed=723192)
audit = audit_packet(g, packet, output)
import photo_h_f2_research_context as research
tampered = copy.deepcopy(packet)
tampered['research_contexts']['foot-en'][0]['term'] = 'altered'
try:
    research.audit(g, tampered)
    raise AssertionError('modified context was accepted')
except ValueError:
    tamper_rejected = True
from unittest.mock import patch
with patch('photo_h_f2_receipts.verify_bound', return_value=packet), \
     patch('photo_h_f2_workflow.value', return_value={'contract_version': 'photo-validation-context/v1'}), \
     patch('compose_pack_view.build_view', return_value={}):
    displayed = workflow.view({})
assert displayed['research_contexts'] == packet['research_contexts']
checks = []
for name, text, expected in cases:
    result = packet['research_contexts'][name]
    matches = result[0]['id'] == expected if expected else not result
    checks.append({'id': name, 'query': text, 'expected': expected,
                   'passed': bool(matches), 'context_results': result,
                   'material_count': len(packet['goals'][name]['candidates']),
                   'lane_calls': packet['goals'][name]['lane_calls']})
summary = {'schema': 'photo-h-f2-research-managed-smoke/v1', 'generation_id': g.id,
           'search_function': 'photo_h_f2_workflow.search_material',
           'receipt_audit': audit, 'context_tampering_rejected': tamper_rejected,
           'view_projection_check': 'passed with receipt and validation-context lookups mocked',
           'passed': sum(c['passed'] for c in checks),
           'total': len(checks), 'cases': checks}
(OUT / (output.name + '-summary.json')).write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(summary, ensure_ascii=False), flush=True)
