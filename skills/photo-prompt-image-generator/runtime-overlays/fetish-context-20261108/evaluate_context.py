#!/usr/bin/env python3
"""Evaluate actual local query embeddings and the sealed research search lane."""
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(os.environ.get('FETISH_CONTEXT_OUTPUT', str(ROOT / 'generated/fetish-hf2-integration-20261108'))).resolve()
staged = json.loads((OUT / os.environ.get('FETISH_CONTEXT_STAGED', 'staged.json')).read_bytes())
store = OUT / os.environ.get('FETISH_CONTEXT_STORE', 'code-store')
native = store / 'generations' / staged['native_generation_id']
lock = json.loads((OUT / 'input-lock.json').read_bytes())
encoder_native = Path.home() / '.cache/image-prompt/photo-shared-runtime/h-f2-installed/generations' / lock['native_generation']
sys.path.insert(0, str(native / 'scripts'))
from photo_h_f2_encoder import LocalEncoder
from photo_h_f2_generation import Generation
import photo_h_f2_research_context as research
import photo_recall_first as rf

cases = [
    ('foot-en', 'foot fetish', 'FASHION-CONTEXT-014'),
    ('foot-ko', '발 페티시', 'FASHION-CONTEXT-014'),
    ('foot-ko-sentence', '발에 대한 페티시의 의미', 'FASHION-CONTEXT-014'),
    ('hand-ko-sentence', '손을 좋아하는 페티시', 'FASHION-CONTEXT-015'),
    ('latex-en', 'latex fetish', 'FASHION-CONTEXT-033'),
    ('latex-ko', '라텍스 소재 페티시란', 'FASHION-CONTEXT-033'),
    ('shoes-en', 'What is footwear fetish?', 'FASHION-CONTEXT-028'),
    ('couture-ko', '패션에서 페티시 쿠튀르', 'fashion-pose-context-FVP-10-075'),
    ('hyphen-en', 'fetish-fashion', 'FASHION-CONTEXT-008'),
    ('podophilia', 'podophilia', 'FASHION-CONTEXT-014'),
    ('general-en', 'leather jacket', None),
    ('general-ko', '가죽 재킷', None),
    ('negated-en', 'fashion without fetish', None),
    ('negated-ko', '페티시 제외 가죽 재킷', None),
    ('control-only', 'fetish=3, blue coat', None),
]
g = Generation(store, staged['generation_id'], full=True)
data = research.load(g)
with LocalEncoder(encoder_native) as enc:
    assert enc.binding == g.binding
    embeddings = enc.encode([q for _, q, _ in cases], 'query')
output = []
cache = OUT / 'query-cache'
cache.mkdir(exist_ok=True)
import photo_candidate_corpus as c
from photo_recall_generation import write
for (name, query, wanted), embedding in zip(cases, embeddings, strict=True):
    rf.check_embedding(embedding, g.binding, query, 'query')
    results = research.query(g, data, query, embedding['vector'])
    passed = results[0]['id'] == wanted if wanted else not results
    output.append({'id': name, 'query': query, 'expected': wanted,
                   'passed': passed, 'results': results, 'embedding_execution': embedding['execution']})
    key = c.digest({'text': query, 'binding': g.binding})
    write(cache / (key + '.json'), {'text': query, 'binding': g.binding, 'row': embedding})
result = {'schema': 'photo-h-f2-research-context-eval/v1', 'generation_id': g.id,
          'query_embedding_provider': g.binding['space']['provider'], 'cases': output,
          'passed': sum(item['passed'] for item in output), 'total': len(output)}
path = OUT / os.environ.get('FETISH_CONTEXT_EVAL', 'context-lane-eval.json')
if path.exists():
    raise FileExistsError(path)
path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'passed': result['passed'], 'total': result['total'],
                  'failures': [r for r in output if not r['passed']]}, ensure_ascii=False), flush=True)
