"""Read-only lexical baseline. Matches are leads, never source/retrieval approval."""
from pathlib import Path
import collections, hashlib, json, re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
TERMS = ['아이돌', 'idol', '연습생', 'trainee', '팬사인', 'fansign', '직캠', 'fancam',
         '엔딩 요정', 'ending fairy', '인이어', 'in-ear', '헤드셋', 'headset', '군무',
         'formation', '응원봉', 'light stick', '포토카드', 'photocard', '체키', 'cheki',
         '모션 캡처', 'motion capture', '바디 롤', 'body roll', '손가락 하트',
         'finger heart', '가터', 'garter', '하네스', 'harness', '스팽글', 'sequin']

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def run():
    manifest = ASSETS / 'photo_candidate_corpus_manifest.json'
    data = json.loads(manifest.read_text())
    hashes = {'photo_candidate_corpus_manifest.json': sha(manifest)}
    records, owners, bindings = [], {}, collections.defaultdict(list)
    for module in data['modules']:
        p = ASSETS / module['file']
        hashes[module['file']] = sha(p)
        d = json.loads(p.read_text())
        if module['kind'] == 'candidates':
            for cid, r in d['candidates'].items():
                assert cid not in owners, cid
                owners[cid] = module['file']
                records.append((module['file'], cid, r))
        elif module['kind'] == 'slot_bindings':
            for bid, r in d['slot_bindings'].items():
                bindings[r['candidate_id']].append({'id': bid, 'slot_id': r['slot_id']})
    hits = []
    counts = collections.Counter()
    for owner, cid, r in records:
        content = r.get('content', {})
        raw = json.dumps(content, ensure_ascii=False).lower()
        found = [t for t in TERMS if (re.search(r'(?<![a-z])'+re.escape(t)+r'(?![a-z])', raw) if t.isascii() else t in raw)]
        if not found:
            continue
        counts.update(found)
        hits.append({'candidate_id': cid, 'file': owner, 'record_kind': r.get('record_kind'),
                     'matched_terms': found, 'en': content.get('en'), 'ko': content.get('ko'),
                     'conditions': r.get('conditions'), 'bindings': bindings[cid],
                     'triage': 'manual_review_required_not_reuse_approval'})
    changes = [n for n, h in hashes.items() if sha(ASSETS/n) != h]
    result = {'schema': 'idol-research-corpus-lexical-audit/v1', 'scope': 'working_source_manifest_only',
              'manifest_schema': data['schema'], 'module_count': len(data['modules']),
              'candidate_count': len(records), 'matching_records': len(hits),
              'term_match_counts': dict(counts), 'source_hashes': hashes,
              'source_changed_during_read': changes, 'hits': hits,
              'limitations': ['Lexical occurrence does not prove semantic precision, completeness, native qualification or installed retrieval.',
                             'English terms use letter boundaries to exclude pareidolia and information. Nonhuman idol senses remain lexical false positives.',
                             'Unregistered files and installed sealed-release content are outside this baseline.']}
    (HERE/'CORPUS-AUDIT.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['hits','source_hashes']}, ensure_ascii=False))
    for h in hits:
        if any(t in h['matched_terms'] for t in ['idol','아이돌','팬사인','엔딩 요정','손가락 하트','인이어','fancam']):
            print(h['candidate_id'], h['file'], h['ko'] or h['en'], [b['slot_id'] for b in h['bindings']])

if __name__ == '__main__':
    run()
