#!/usr/bin/env python3
"""Research integrity only; no claim of semantic, retrieval, or pixel qualification."""
import argparse, collections, hashlib, json, re, subprocess, sys
from pathlib import Path
from urllib.parse import urlparse, unquote

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
def read(p): return json.loads(p.read_text())
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(n,x): (HERE/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def files(): return sorted(p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS')
def seal():
    (HERE/'SHA256SUMS').write_text(''.join(f'{sha(p.read_bytes())}  {p.relative_to(HERE)}\n' for p in files()))
def sealed():
    errors=[]
    expected={}
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        h,n=line.split('  ',1);expected[n]=h
        p=HERE/n
        if not p.is_file() or sha(p.read_bytes())!=h:errors.append(n)
    actual={str(p.relative_to(HERE)) for p in files()}
    errors.extend(sorted(actual-set(expected)))
    if errors:raise ValueError('checksum failure: '+str(errors))
    print(json.dumps({'checksum':'pass','files':len(expected)}));return

def main():
    src=read(HERE/'sources.json')['sources'];sid={s['id'] for s in src}
    cards=read(HERE/'semantic-cards.json')['cards'];cid={c['id'] for c in cards}
    route=read(HERE/'keyword-routes.json')['routes'];rids={r['seed_id'] for r in route}
    draft=read(HERE/'candidate-drafts.json');cases=read(HERE/'evaluation-cases.json')['cases']
    summary=read(HERE/'SUMMARY.json');mapping=read(HERE/'existing-source-mapping.json')
    slots=read(ASSETS/'photo_candidate_slot_catalog.json')['slot_catalog']
    errors=[];checks=[]
    def check(ok,msg):
        checks.append(msg)
        if not ok:errors.append(msg)
    check(len(route)==200 and rids==set(range(1,201)), 'all 200 original seed numbers covered once')
    check(len(cards)==78 and len(cid)==78, '78 unique semantic cards')
    check(len(src)==38 and len(sid)==38 and len({s['url'] for s in src})==38, '38 unique bounded source records')
    check(all(urlparse(s['url']).scheme=='https' and s['read_scope'] and s['access'] for s in src),'source URLs and access scopes explicit')
    for r in route:
        check(set(r['source_ids'])<=sid and set(r['card_ids'])<=cid and bool(r['note_ko']),r['id']+' route references and limitation')
        check(r['native_approval'] is False,r['id']+' no native promotion')
        if r['seed_id']>=183:check(bool(r['version_scope']) and bool(r['canon_review_ko']),r['id']+' work/version scope explicit')
    for c in cards:
        owners={o['id'] for o in c['owners']}
        check(len(owners)==len(c['owners']) and len(owners)>=2,c['id']+' distinct owners')
        check(set(c['source_ids'])<=sid and set(c['seed_ids'])<=rids,c['id']+' sources and seed references')
        check(set(c['proposed_slots'])<=set(slots),c['id']+' current slot names')
        linked=set()
        for r in c['relations']:
            check(r['subject'] in owners and r['object'] in owners and r['subject']!=r['object'],c['id']+' directed relation endpoints')
            linked.update([r['subject'],r['object']])
            check(r['visible_en'] in c['positive_en'] and r['visible_ko'] in c['positive_ko'],c['id']+' relation text transport in EN/KO')
        check(linked==owners,c['id']+' no disconnected owner')
        check(all(o['visible_en'] in c['positive_en'] and o['visible_ko'] in c['positive_ko'] for o in c['owners']),c['id']+' complete EN/KO component transport')
        check(len(c['render_gate_proposals'])==len(owners)+len(c['relations']),c['id']+' all component and relation gates present')
        check(c['native_approval'] is False and c['runtime_importable'] is False and c['requester_acceptance']=='pending',c['id']+' research proof boundary')
        check('partial_is_fail' in c['whole_case_rule'] and 'UNOBSERVABLE_NOT_PASS' in c['whole_case_rule'],c['id']+' partial/unobservable policy')
    dids={d['id'] for d in draft['drafts']}
    check(len(dids)==len(draft['drafts'])==72 and len(draft['held_cards'])==6,'72 drafts and 6 held cards')
    check({d['card_id'] for d in draft['drafts']}|set(draft['held_cards'])==cid,'all cards drafted or explicitly held')
    check(not ({d['card_id'] for d in draft['drafts']}&set(draft['held_cards'])),'held cards not silently drafted')
    for d in draft['drafts']:
        c=next(c for c in cards if c['id']==d['card_id'])
        check(d['positive_en']==c['positive_en'] and d['positive_ko']==c['positive_ko'] and d['relations']==c['relations'],d['id']+' full meaning transferred')
        check(not d['native_approval'] and not d['runtime_importable'] and d['registration_status']=='not_in_operating_manifest',d['id']+' not an operating source')
    check(len(cases)==80 and len({c['id'] for c in cases})==80,'80 unique evaluation cases')
    check(collections.Counter(c['group'] for c in cases)=={'positive':24,'boundary':32,'ordinary_control':16,'unobservable_control':8},'evaluation split counts')
    check(all(c['query_en'] and c['query_ko'] and set(c['expected_card_ids'])<=cid and c['execution_status']=='NOT_RUN' for c in cases),'160 bilingual queries planned, none reported executed')
    for row in mapping:
        h=sha(json.dumps(row['record'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
        check(h==row['canonical_sha256'],row['cid']+' captured source content hash')
        check(bool(row['research_decision']['reason_ko']) and row['native_approval'] is False,row['cid']+' bounded decision without native approval')
    runtime=read(HERE/'RUNTIME-CHECK.json')
    check(runtime['status']=='pass' and runtime['image_calls']==0 and runtime['source_writes']==0,'read-only installed recorder probe')
    manifest=read(ASSETS/'photo_candidate_corpus_manifest.json')
    check(not any('analog_horror' in m['file'] for m in manifest['modules']),'analog research absent from operating manifest')
    check(all(summary[k]=='NOT_RUN' for k in ('runtime_adoption','retrieval_evaluation','image_generation','pixel_evaluation')),'no fabricated runtime/retrieval/image/pixel results')
    broken=[]
    for p in HERE.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if re.match(r'^[a-z]+:',target) or target.startswith('#'):continue
            name=unquote(target.split('#')[0])
            if name and not (p.parent/name).exists() and name not in ('VALIDATION.json','BASELINE-DRIFT.json','SHA256SUMS'):broken.append([p.name,target])
    check(not broken,'local Markdown links resolve')
    baseline=read(HERE/'BASELINE.json');missing=[];changed=[]
    for f,h in baseline['tracked_file_sha256'].items():
        p=ROOT/f
        if not p.is_file():missing.append(f)
        elif sha(p.read_bytes())!=h:changed.append(f)
    audit=read(HERE/'CORPUS-LEXICAL-AUDIT.json');source_changed=[]
    for f,h in audit['module_sha256'].items():
        p=ASSETS/f
        if not p.is_file() or sha(p.read_bytes())!=h:source_changed.append(f)
    current_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
    manifest_changed=sha((ASSETS/'photo_candidate_corpus_manifest.json').read_bytes())!=audit['manifest_sha256']
    drift=dict(schema='analog-research-source-drift/v1',baseline_head=baseline['head'],current_head=current_head,
               tracked_files_changed_since_baseline=changed,tracked_files_missing_since_baseline=missing,
               audited_source_modules_changed=source_changed,manifest_changed=manifest_changed,
               audit_read_drift=audit['changes_during_read'],audit_manifest_read_drift=audit['manifest_changed_during_read'],
               attribution='concurrent workspace changes observed, not attributed or reverted by this research',
               adoption_requirement='always rebaseline before implementation; do not overwrite historical research with new operational evidence')
    dump('BASELINE-DRIFT.json',drift)
    has_drift=bool(changed or missing or source_changed or manifest_changed or current_head!=baseline['head'])
    status='FAIL' if errors else 'STRUCTURE_PASS_SOURCE_DRIFT_REQUIRES_REBASELINE' if has_drift else 'STRUCTURE_PASS_REBASELINE_BEFORE_IMPLEMENTATION'
    result=dict(schema='analog-horror-research-validation/v1',status=status,structure_status='fail' if errors else 'pass',
                check_count=len(checks),errors=errors,broken_links=broken,
                summary=summary,source_drift_observed=has_drift,
                manual_review='technical confusion table; 19 captured records; all authored owner/endpoint relations; selected EN/KO consistency; source access boundaries',
                not_proven=['all 200 independent definitions','all corpus source meanings','hybrid retrieval exposure or rank','candidate selection','prompt audit','image generation','native pixels','artistic improvement','requester acceptance'])
    dump('VALIDATION.json',result);seal()
    print(json.dumps({'status':status,'checks':len(checks),'errors':errors,'tracked_drift':len(changed),'source_module_drift':len(source_changed),'manifest_drift':manifest_changed,'head_changed':current_head!=baseline['head']},ensure_ascii=False))
    if errors:sys.exit(1)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check-sealed',action='store_true');a=p.parse_args()
    if a.check_sealed:sealed()
    else:main()
