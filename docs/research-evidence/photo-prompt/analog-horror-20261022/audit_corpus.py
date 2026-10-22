#!/usr/bin/env python3
"""Read-only corpus diagnosis. Writes only this new research package."""
import collections, csv, hashlib, json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
FIELDS = ('en', 'ko', 'definition', 'phrase_en', 'phrase_ko', 'composition_instruction', 'runtime_expression')
FOCUS = ('VHS', 'CRT', 'tracking', 'scanline', 'dropout', 'ghosting', 'analog horror',
         'surveillance', 'color bars', 'teletext', 'timecode', 'spectrogram',
         'head switching', 'mistracking', 'chroma', 'doppelganger', 'redaction',
         'animatronic', 'cursed', 'body imprisonment', 'living architecture')

def sha(b): return hashlib.sha256(b).hexdigest()
def write(n, x): (HERE/n).write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n')
def leaves(v, p):
    if isinstance(v, str): yield p, v
    elif isinstance(v, dict):
        for k, x in v.items(): yield from leaves(x, p+'/'+k)
    elif isinstance(v, list):
        for k, x in enumerate(v): yield from leaves(x, p+'/'+str(k))
def selected(r):
    for k in FIELDS:
        if k in r.get('content', {}): yield from leaves(r['content'][k], '/content/'+k)
    for rid, branch in r.get('realizations', {}).items():
        if not isinstance(branch, dict): continue
        for k in FIELDS:
            for box in ('content', ''):
                obj = branch.get(box, {}) if box else branch
                if isinstance(obj, dict) and k in obj:
                    yield from leaves(obj[k], '/realizations/'+str(rid)+('/content' if box else '')+'/'+k)
def pat(t):
    return re.compile(r'(?<![a-z0-9])'+re.escape(t)+r'(?![a-z0-9])' if t.isascii() else re.escape(t), re.I)

def main():
    raw_manifest = (ASSETS/'photo_candidate_corpus_manifest.json').read_bytes()
    manifest = json.loads(raw_manifest)
    records, owners, bindings, hashes, duplicate = {}, {}, {}, {}, []
    for module in manifest['modules']:
        raw = (ASSETS/module['file']).read_bytes(); hashes[module['file']] = sha(raw)
        data = json.loads(raw)
        for cid, row in data.get('candidates', {}).items():
            if cid in records: duplicate.append(cid)
            records[cid] = row; owners[cid] = module['file']
        bindings.update(data.get('slot_bindings', {}))
    texts = {cid: list(selected(r)) for cid, r in records.items()}
    terms = list(csv.DictReader((HERE/'seeds.tsv').open(), delimiter='\t'))
    results = []
    for term in terms:
        aliases = [x.strip() for x in term['en'].split(' / ') + term['ko'].split('·') if len(x.strip()) >= 3]
        patterns = [(t, pat(t)) for t in aliases]
        hits = []
        for cid, field_texts in texts.items():
            local = [dict(pointer=p, exact_text=s, aliases=[t for t, rg in patterns if rg.search(s)])
                     for p, s in field_texts if any(rg.search(s) for _, rg in patterns)]
            if local: hits.append(dict(cid=cid, module=owners[cid], matches=local))
        results.append(dict(seed_id=int(term['id']), en=term['en'], aliases=aliases, count=len(hits), hits=hits))
    focus_results, picked = [], {}
    for term in FOCUS:
        rg = pat(term); ids = [cid for cid, vals in texts.items() if any(rg.search(s) for _, s in vals)]
        focus_results.append(dict(term=term, count=len(ids), selected=ids[:2]))
        for cid in ids[:2]: picked.setdefault(cid, []).append(term)
    mapping = []
    for cid, terms in picked.items():
        record = records[cid]
        edges = {bid: b for bid, b in bindings.items() if b.get('candidate_id') == cid}
        mapping.append(dict(cid=cid, module=owners[cid], focus_terms=terms, record=record,
                            canonical_sha256=sha(json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()),
                            direct_bindings=edges, recommendation='review_full_meaning_before_reuse_or_refine', native_approval=False))
    drift = [f for f, h in hashes.items() if not (ASSETS/f).exists() or sha((ASSETS/f).read_bytes()) != h]
    audit = dict(schema='analog-horror-lexical-diagnostic/v1', candidate_count=len(records), binding_count=len(bindings),
                 module_count=len(manifest['modules']), manifest_sha256=sha(raw_manifest), module_sha256=hashes,
                 fields=list(FIELDS), selection='exact bounded fields; English word boundaries; first two focus hits in manifest order, not ranking',
                 limitations=['zero lexical hits is not semantic absence', 'no H-F2 retrieval, rank, selection, prompt or pixel test'],
                 duplicate_candidate_ids=duplicate, changes_during_read=drift,
                 manifest_changed_during_read=sha((ASSETS/'photo_candidate_corpus_manifest.json').read_bytes()) != sha(raw_manifest),
                 term_results=results, focus_results=focus_results)
    write('CORPUS-LEXICAL-AUDIT.json', audit); write('existing-source-mapping.json', mapping)
    print(json.dumps(dict(candidates=len(records), bindings=len(bindings), modules=len(manifest['modules']),
                          zero_terms=sum(x['count']==0 for x in results), selected_records=len(mapping),
                          drift=drift, manifest_drift=audit['manifest_changed_during_read'], focus=focus_results), ensure_ascii=False))

if __name__ == '__main__': main()
