"""Validate research structure and record source drift; this is not runtime qualification."""
import ast
import collections
import csv
import hashlib
import json
import pathlib
import re
import subprocess

ROOT=pathlib.Path(__file__).resolve().parent
REPO=ROOT.parents[3]

def read(name):return json.loads((ROOT/name).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    cards=read('semantic-cards.json')['cards']
    routes=read('keyword-routes.json')['routes']
    drafts=read('candidate-drafts.json')['drafts']
    sources=read('sources.json')['sources']
    snap=read('corpus-snapshot.json')
    baseline=read('BASELINE.json')
    checks=[]
    def check(name,condition):
        checks.append({'name':name,'pass':bool(condition)})
    ids={c['id'] for c in cards};sids={s['id'] for s in sources}
    check('210 exact numbered seeds',len(routes)==210 and [r['n'] for r in routes]==list(range(1,211)))
    check('14 groups of 15 seeds',collections.Counter(r['category'] for r in routes)=={i:15 for i in range(1,15)})
    check('unique card and source IDs',len(ids)==len(cards) and len(sids)==len(sources))
    check('complete seed routing',all(r['optional_visual_card_ids'] or r['context_card_ids'] for r in routes))
    check('all route references exist',all(set(r['optional_visual_card_ids']+r['context_card_ids'])<=ids for r in routes))
    check('routes remain advisory',all(r['activation']=='advisory_only' for r in routes))
    check('card seed references and inverse routing agree',all(c['id'] in routes[n-1]['optional_visual_card_ids']+routes[n-1]['context_card_ids'] for c in cards for n in c['source_keyword_ids']))
    check('all sources exist',all(set(c['source_ids'])<=sids for c in cards))
    unavailable={s['id'] for s in sources if s['access']=='unavailable'}
    check('inaccessible sources are never evidence anchors',not any(set(c['source_ids'])&unavailable for c in cards))
    visual=[c for c in cards if c['mode'] in {'visible','proxy'}]
    context=[c for c in cards if c['mode'] not in {'visible','proxy'}]
    check('visual fragments have bilingual text, boundary, gates and graph',all(c['positive_en'] and c['positive_ko'] and c['confusion_boundary'] and c['observable_gate'] and c['research_relations'] for c in visual))
    check('every graph endpoint belongs to its own card',all(e['from'] in c['research_owner_nodes'] and e['to'] in c['research_owner_nodes'] for c in visual for e in c['research_relations']))
    check('context/audio/sequence has no positive realization or owner authority',all(c['positive_en'] is None and c['positive_ko'] is None and not c['research_relations'] and not c['suggested_slots'] for c in context))
    check('suggested slots exist in observed catalog',all(set(c['suggested_slots'])<=set(snap['catalog_slots']) for c in cards))
    check('research drafts are exact visual-card subset',len(drafts)==len(visual) and {d['card_id'] for d in drafts}=={c['id'] for c in visual})
    check('drafts remain inert and unqualified',all(not d['runtime_importable'] and not d['native_approval'] for d in drafts))
    check('all research cards remain unqualified',all(c['native_approval'] is False for c in cards))
    check('10 existing CIDs include full source and bindings',len(snap['existing_source_triage'])==10 and all(x['candidate_id']==x['source_record']['id'] and x['bindings'] for x in snap['existing_source_triage']))
    check('corpus snapshot read consistency',snap['read_consistency']['manifest_stable'] and not snap['read_consistency']['changed_modules'])
    with (ROOT/'BOUNDARY-CASES.tsv').open() as f:boundary=list(csv.DictReader(f,delimiter='\t'))
    check('32 bilingual boundary cases have card references and expected results',len(boundary)==32 and all(r['query_ko'] and r['query_en'] and r['expected'] and set(r['cards'].split(','))<=ids for r in boundary))
    dev=read('development-cases.json')['cases']
    check('development scaffolds are not passed off as holdout or execution',len(dev)==len(cards) and all(not r['independent_holdout'] and r['result']=='NOT_RUN' for r in dev))
    check('24 nonvisual development queries are fully bilingual',sum(bool(r['language_status']=='full_bilingual_context_development_query' and r['input_ko'] and r['input_en']) for r in dev)==24)
    for p in ROOT.glob('*.py'):ast.parse(p.read_text())
    check('research Python syntax',True)
    missing_links=[]
    for p in ROOT.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if '://' in target or target.startswith('#'):continue
            if not (p.parent/target.split('#',1)[0]).exists():missing_links.append([p.name,target])
    # VALIDATION and SHA256SUMS are outputs of this command, so their pre-write absence is expected.
    missing_links=[x for x in missing_links if x[1] not in {'VALIDATION.json','SHA256SUMS'}]
    check('package local links resolve',not missing_links)
    changed=[];missing=[]
    for name,h in baseline['protected_sha256'].items():
        p=REPO/name
        if not p.exists():missing.append(name)
        elif sha(p)!=h:changed.append(name)
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
    module_drift=[n for n,h in snap['module_sha256'].items() if sha(REPO/'skills/photo-prompt-image-generator/assets'/n)!=h]
    passed=all(c['pass'] for c in checks)
    drift=bool(changed or missing or module_drift or head!=baseline['head'])
    status='STRUCTURE_PASS_SOURCE_DRIFT_REQUIRES_REBASELINE' if passed and drift else ('STRUCTURE_PASS_PROTECTED_FILES_STABLE' if passed else 'STRUCTURE_FAIL')
    out={'schema':'school-life-research-validation/v1','status':status,'checks':checks,
         'counts':{'keywords':len(routes),'cards':len(cards),'modes':dict(collections.Counter(c['mode'] for c in cards)),
                   'candidate_drafts':len(drafts),'external_source_records':len(sources)-1,
                   'external_access':dict(collections.Counter(s['access'] for s in sources if s['id']!='S00')),
                   'boundary_cases':len(boundary),'bilingual_boundary_queries':len(boundary)*2,'development_scaffolds':len(dev)},
         'baseline_head':baseline['head'],'observed_head':head,
         'protected_state':{'count':len(baseline['protected_sha256']),'changed':changed,'missing':missing,'module_drift':module_drift,
              'interpretation':'Observed drift in shared checkout is separate from research validity; no reset/revert performed.'},
         'missing_links':missing_links,'runtime_source_mutations_by_this_task':0,
         'evidence_limits':['Structure is not factual validation of all definitions.','Geometry is authored, not proven by contextual citations.',
                           'Native qualification, index closure, retrieval, image generation, pixels, installation and user acceptance NOT_RUN.'],
         'commit':'NOT_RUN','push':'NOT_RUN'}
    (ROOT/'VALIDATION.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    members=sorted(p for p in ROOT.rglob('*') if p.is_file() and p.name!='SHA256SUMS' and '__pycache__' not in p.parts)
    (ROOT/'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p.relative_to(ROOT)}\n' for p in members))
    print(json.dumps({'status':status,'checks_passed':sum(c['pass'] for c in checks),'checks_total':len(checks),'counts':out['counts'],
                     'protected_changed':changed,'protected_missing':missing,'head_changed':head!=baseline['head']},ensure_ascii=False))
    if not passed:raise SystemExit(1)

if __name__=='__main__':main()
