#!/usr/bin/env python3
"""Research artifact integrity and scope checks. No runtime qualification claimed."""
import collections,csv,hashlib,json,re
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]

def read(name):return json.loads((HERE/name).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    errors=[]
    def check(test,message):
        if not test:errors.append(message)
    cards=read('semantic-cards.json')['cards'];routes=read('keyword-routes.json')['routes']
    drafts=read('candidate-drafts.json')['drafts'];sources=read('sources.json')
    cm={c['id']:c for c in cards};sm={s['id']:s for s in sources}
    check(len(cards)==len(cm)==72,'72 unique cards required')
    check(len(routes)==len({r['en'] for r in routes})==247,'247 unique routes required')
    check(len(sources)==len(sm)==46,'46 unique sources required')
    check(len(drafts)==68,'68 research drafts required')
    check(not read('semantic-cards.json')['runtime_importable'],'registry must not import into runtime')
    check(not read('candidate-drafts.json')['runtime_importable'],'drafts must not import into runtime')
    for c in cards:
        ids=[o['id'] for o in c['owners']]
        check(len(ids)==len(set(ids)),c['id']+' duplicate owners')
        check(set(c['source_refs'])<=set(sm),c['id']+' missing source')
        check(all(e['subject'] in ids and e['object'] in ids for e in c['relations']),c['id']+' dangling endpoint')
        check(bool(c['phrase_en'] and c['phrase_ko'] and c['claim_limit_ko']),c['id']+' empty bilingual/limit')
        check(len(c['confusion_boundaries'])>=2,c['id']+' needs confusions')
        if c['evidence_mode']!='context':
            check(len(c['gates'])==len(c['owners'])+len(c['relations']),c['id']+' incomplete component/relation gate set')
            check(all(e['subject']!=e['object'] for e in c['relations']),c['id']+' unsupported self relation')
            connected={x for e in c['relations'] for x in (e['subject'],e['object'])}
            check(set(ids)<=connected,c['id']+' disconnected owner')
    for r in routes:check(set(r['optional_cards'])<=set(cm),r['id']+' missing card')
    for d in drafts:
        check(d['native_cid'] is None and d['native_rid'] is None,d['research_id']+' false native identity')
        check(cm[d['research_id']]['evidence_mode']!='context',d['research_id']+' context converted into candidate')
    with (HERE/'EVALUATION-CASES.tsv').open() as f:cases=list(csv.DictReader(f,delimiter='\t'))
    counts=collections.Counter(c['cohort'] for c in cases)
    check(counts==dict(development=24,boundary=16,ordinary_control=12,nonvisual_control=4),'evaluation cohorts differ')
    check(len({c['id'] for c in cases})==56,'duplicate/missing evaluation case')
    check(all(c['status']=='NOT_RUN' for c in cases),'research must not claim evaluation pass')
    check(all(c['query_ko'] and c['query_en'] for c in cases),'missing bilingual query')
    audit=read('CORPUS-LEXICAL-AUDIT.json')
    check(len(audit['term_results'])==247,'incomplete lexical audit')
    check(not audit['duplicate_candidate_ids'],'duplicate candidate owners in audit')
    check(not audit['changes_during_read'] and not audit['manifest_changed_during_read'],'corpus moved during its snapshot')
    mapping=read('existing-source-mapping.json')
    for x in mapping:
        actual=hashlib.sha256(json.dumps(x['record'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        check(actual==x['canonical_record_sha256'],x['cid']+' snapshot hash mismatch')
        check(x['native_approval'] is False,x['cid']+' false approval')
    broken=[]
    for path in HERE.glob('*.md'):
        for dest in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            # These two links point to this validator's own outputs, written below.
            if dest in ('VALIDATION.json','SHA256SUMS'):continue
            if '://' not in dest and not dest.startswith('#') and not (path.parent/dest.split('#')[0]).exists():
                broken.append(path.name+' -> '+dest)
    check(not broken,'broken local links: '+str(broken))
    base=read('BASELINE.json');drift=[];missing=[]
    for path,old in {**base['tracked_sha256'],**base['selected_untracked_sha256']}.items():
        p=ROOT/path
        if not p.exists():missing.append(path)
        elif sha(p)!=old:drift.append(path)
    current_modules={}
    for name,old in audit['module_sha256'].items():
        p=ROOT/'skills/photo-prompt-image-generator/assets'/name
        if not p.exists() or sha(p)!=old:current_modules[name]='differs_from_audit_snapshot'
    runtime=read('RUNTIME-CHECK.json')
    check(runtime['image_calls']==0 and runtime['source_writes']==0,'runtime check must be read-only')
    result=dict(status='pass' if not errors else 'fail',errors=errors,
                counts=dict(terms=247,cards=len(cards),drafts=len(drafts),sources=len(sources),evaluation_cases=len(cases),queries=2*len(cases),captured_basic_sources=len(mapping)),
                card_priority=dict(collections.Counter(c['priority'] for c in cards)),
                scope='all authored writes confined to this new research folder; existing working sources not edited by research scripts',
                baseline_comparison=dict(tracked_files=len(base['tracked_sha256']),changed_since_start=drift,missing_since_start=missing,
                                         interpretation='concurrent workspace drift is reported; global unchanged-file preservation is not claimed when differences exist'),
                corpus_snapshot_vs_current=current_modules,
                runtime_check_status=runtime['status'],
                not_proven=['native source qualification','actual hybrid retrieval exposure','role-specific semantic precision','generated-image fidelity','artistic improvement','user acceptance'],
                model_api_calls=0,index_builds=0,image_calls=0,runtime_registration=False,activation=False)
    (HERE/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    paths=sorted(p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS')
    (HERE/'SHA256SUMS').write_text('\n'.join(sha(p)+'  '+str(p.relative_to(HERE)) for p in paths)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('baseline_comparison','corpus_snapshot_vs_current')},ensure_ascii=False))
    print(json.dumps(dict(changed_since_start=len(drift),missing_since_start=len(missing),audit_modules_changed_since_snapshot=len(current_modules)),ensure_ascii=False))
    if errors:raise SystemExit(1)

if __name__=='__main__':main()
