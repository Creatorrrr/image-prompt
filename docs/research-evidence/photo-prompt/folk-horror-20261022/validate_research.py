"""Validate research references and evidence boundaries, never runtime quality."""
import collections
import csv
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]


def read(name):
    return json.loads((ROOT/name).read_text())


def main():
    checks=[]
    def check(name, condition):
        checks.append(dict(check=name,passed=bool(condition)))
    seeds=read('seed-keywords.json')['terms']
    routes=read('keyword-routes.json')['routes']
    cards=read('semantic-cards.json')['cards']
    drafts=read('candidate-drafts.json')['drafts']
    sources=read('sources.json')['sources']
    cardmap={x['id']:x for x in cards}; source_ids={x['id'] for x in sources}
    check('150 unique consecutive original seed numbers',[s['number'] for s in seeds]==list(range(1,151)))
    check('150 routes retain exact source titles',len(routes)==150 and all(r['title']==s['title'] and r['seed_number']==s['number'] for r,s in zip(routes,seeds)))
    check('every seed has a valid nonempty route',all(r['card_refs'] and set(r['card_refs'])<=set(cardmap) for r in routes))
    check('route-to-card seed backrefs',all(r['seed_number'] in cardmap[c]['seed_numbers'] for r in routes for c in r['card_refs']))
    check('unique card draft source identifiers',len(cardmap)==len(cards) and len({d['id'] for d in drafts})==len(drafts) and len(source_ids)==len(sources))
    check('all card citations resolve',all(c['source_refs'] and set(c['source_refs'])<=source_ids for c in cards))
    check('all sources retain access and claim limits',all(s['access'] and s['supports'] and s['limit'] and s['url'].startswith('https://') for s in sources))
    visual=[c for c in cards if c['evidence_mode']=='observable_realization']; contextual=[c for c in cards if c['evidence_mode']=='context_only']
    check('complete one-to-one visible draft coverage',{d['card_ref'] for d in drafts}=={c['id'] for c in visual} and len(drafts)==len(visual))
    check('no context record promoted to positive draft',not ({d['card_ref'] for d in drafts}&{c['id'] for c in contextual}) and all(not c['positive_candidate_allowed'] and not c['gates'] for c in contextual))
    check('visible drafts retain exact bilingual meanings',all(d['phrase_en']==cardmap[d['card_ref']]['phrase_en'] and d['phrase_ko']==cardmap[d['card_ref']]['phrase_ko'] for d in drafts))
    check('owner graph endpoints are declared',all(c['relations'] and all(r['source'] in c['owners'] and r['target'] in c['owners'] and r['predicate'] for r in c['relations']) for c in visual))
    check('visible distinction boundaries and gates retained',all(c['distinguishing_observation'] and c['confusion_boundaries'] and c['claim_limit'] and len(c['gates'])>=2 and c['partial_is_fail'] and c['missing_evidence']=='UNOBSERVABLE_NOT_PASS' for c in visual))
    check('drafts claim no operating CID or RID',all(d['cid'] is None and d['rid'] is None and d['native_source_units']=='NOT_AUTHORED' and d['status']=='RESEARCH_DRAFT_ONLY' for d in drafts))
    catalog=json.loads((REPO/'skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json').read_text())['slot_catalog']
    check('proposed navigation roles exist without claiming approval',all(d['proposed_roles'] and set(d['proposed_roles'])<=set(catalog) and not d['unresolved_role_names'] and d['role_approval'].startswith('NOT_REVIEWED') for d in drafts))
    check('source scenes explicitly authored not historical defaults',all(c['historical_status']=='authored_optional_realization_not_attested_practice' for c in visual))
    cases=list(csv.DictReader((ROOT/'EVALUATION-CASES.tsv').open(),delimiter='\t'))
    sets=collections.Counter(x['set'] for x in cases)
    check('52 authored cases and 104 nonempty bilingual queries',len(cases)==52 and all(c['query_ko'] and c['query_en'] for c in cases))
    check('evaluation split',sets==dict(development=24,boundary=16,ordinary_control=8,nonvisual_control=4))
    check('evaluation refs resolve and no runs claimed',all(set(c['card_refs'].split(','))<=set(cardmap) and c['execution_status']=='NOT_RUN' for c in cases))
    check('explicit sealed opaque bottle observability boundary',cardmap['O09']['phrase_en']!=cardmap['O10']['phrase_en'] and '보이지 않음' in cardmap['O09']['claim_limit'])
    check('geumjul and shimenawa retain distinct source meaning',cardmap['K01']['source_refs']!=cardmap['J01']['source_refs'] and cardmap['K01']['phrase_en']!=cardmap['J01']['phrase_en'])
    baseline=read('BASELINE.json'); drift=[];missing=[]
    for f,sha in baseline['source_hashes'].items():
        p=REPO/f
        if not p.exists():missing.append(f)
        elif hashlib.sha256(p.read_bytes()).hexdigest()!=sha:drift.append(f)
    snapshots=read('existing-source-mapping.json')
    check('existing source snapshots preserve canonical record hashes',all(hashlib.sha256(json.dumps(x['record'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()==x['record_sha256'] for x in snapshots))
    report=dict(status='RESEARCH_STRUCTURE_PASS' if all(x['passed'] for x in checks) else 'FAIL',
        counts=dict(seeds=len(seeds),routes=len(routes),sources=len(sources),cards=len(cards),visual_drafts=len(drafts),context_cards=len(contextual),evaluation_cases=len(cases),bilingual_queries=len(cases)*2,existing_source_snapshots=len(snapshots)),
        checks=checks,baseline_source_drift=drift,baseline_sources_missing=missing,
        drift_interpretation='Concurrent source changes are observed, not attributed to this research. Rebaseline before adoption.',
        evidence_limits=dict(runtime_registration='NOT_RUN',hybrid_retrieval='NOT_RUN',source_native_qualification='NOT_RUN',image_generation='NOT_RUN',pixel_review='NOT_RUN',activation='NOT_RUN',commit_push='NOT_RUN',user_acceptance='PENDING'))
    (ROOT/'VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    sums=[]
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and p.name!='SHA256SUMS' and '__pycache__' not in p.parts:
            sums.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(ROOT)))
    (ROOT/'SHA256SUMS').write_text('\n'.join(sums)+'\n')
    print(json.dumps(dict(status=report['status'],counts=report['counts'],checks_passed=sum(x['passed'] for x in checks),checks_total=len(checks),source_drift=len(drift),missing_sources=len(missing)),ensure_ascii=False))
    if not all(x['passed'] for x in checks):
        raise SystemExit(1)


if __name__=='__main__':main()
