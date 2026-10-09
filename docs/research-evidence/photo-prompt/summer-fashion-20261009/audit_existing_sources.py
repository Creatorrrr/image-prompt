"""Read authored source overlays only; no runtime publisher, index build or API calls."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import json, hashlib, sys, subprocess, re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    paths = list((SKILL / 'assets').glob('*.json')) + list((SKILL / 'scripts').glob('*.py'))
    before = {str(p.relative_to(ROOT)): sha(p) for p in paths}
    started = datetime.now(timezone(timedelta(hours=9))).isoformat()
    data = pg.load_json(SKILL / 'assets/photo_prompt_tags.json')
    registry = pg.load_visual_obligation_registry(SKILL / 'assets/photo_prompt_visual_obligations.json')
    records = []
    for slot, entries in data['slots'].items():
        for e in entries:
            records.append({'kind':'slot_candidate','slot':slot,'id':e['id'],
                            'positive_text':pg.semantic_text_for_entry(e, slot), 'entry':e})
    for p in registry['profiles']:
        records.append({'kind':'visual_profile','id':p['id'],
                        'positive_text':pg.visual_profile_semantic_text(p), 'entry':p})
    # These seeds contain Korean/Latin only. Their lexicon cannot segment Han
    # or Japanese text, so caching the shared tokenizer is exactly equivalent
    # to semantic_text_contains_authored_term for this inventory.
    record_tokens = [set(pg.tokenize_bm25f_text(r['positive_text'])) for r in records]
    terms = []; group = ''
    for line in (HERE/'seed-terms.txt').read_text().splitlines():
        if line.startswith('#'): group = line[2:]; continue
        if not line.strip(): continue
        ko, _, en = line.partition(' — ')
        aliases = [ko, en, *ko.split('·'), *en.split(' / ')]
        aliases = list(dict.fromkeys(x.strip() for x in aliases if len(x.strip()) >= 2))
        assert not any(re.search(r'[\u3400-\u9fff\u3040-\u30ff]',x) for x in aliases)
        alias_tokens = {x:set(pg.tokenize_bm25f_text(x,lexicon=[x])) for x in aliases}
        hits = []
        for r, tokens in zip(records,record_tokens):
            found = [x for x in aliases if alias_tokens[x] and alias_tokens[x].issubset(tokens)]
            if found: hits.append({'kind':r['kind'],'slot':r.get('slot'),'id':r['id'],'matched_terms':found})
        terms.append({'id':f'ST{len(terms)+1:03d}','group':group,'term':line,'aliases':aliases,'lexical_neighbors':hits})
    matched_ids = {r['id'] for t in terms for r in t['lexical_neighbors']}
    selected = [r for r in records if r['id'] in matched_ids]
    (HERE/'current-positive-records.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2)+'\n')
    (HERE/'term-inventory.json').write_text(json.dumps(terms,ensure_ascii=False,indent=2)+'\n')
    after = {str(p.relative_to(ROOT)): sha(p) for p in paths}
    changed = [p for p in before if before[p] != after[p]]
    slots = data['slots']
    summary = {'captured_at':started,'finished_at':datetime.now(timezone(timedelta(hours=9))).isoformat(),
               'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
               'counts':{'seed_terms':len(terms),'slots':len(slots),'slot_candidates':sum(len(x) for x in slots.values()),
                         'profiles':len(registry['profiles']),'bundles':len(data.get('candidate_bundles',[])),
                         'terms_with_candidate_surface':sum(any(x['kind']=='slot_candidate' for x in t['lexical_neighbors']) for t in terms),
                         'terms_with_profile_surface':sum(any(x['kind']=='visual_profile' for x in t['lexical_neighbors']) for t in terms),
                         'terms_with_either_surface':sum(bool(t['lexical_neighbors']) for t in terms)},
               'candidate_property_paths':sorted({x['property'] for r in records if r['kind']=='slot_candidate'
                                                  for x in r['entry'].get('affected_properties',[]) if isinstance(x,dict) and 'property' in x}),
               'proof_boundary':'Shared tokenizer membership in positive fields; tokens may occur apart. Not contiguous phrase coverage, semantic equivalence, retrieval rank, live dispatch, adoption or pixels.',
               'read_stability':{'files_checked':len(paths),'changed_files':changed,'status':'stable' if not changed else 'concurrent_drift'},
               'source_sha256':before,'runtime_dispatch':False,'embedding_calls':0,'image_calls':0}
    (HERE/'current-source-audit.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ['head','counts','read_stability','runtime_dispatch','embedding_calls','image_calls']},ensure_ascii=False))

if __name__ == '__main__': main()
