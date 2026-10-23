#!/usr/bin/env python3
"""Check research evidence integrity, not retrieval success or rendered fidelity."""
import collections,hashlib,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
def read(n):return json.loads((HERE/n).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    issues=[]
    def check(ok,msg):
        if not ok:issues.append(msg)
    ks=read('keyword-routes.json');cards=read('semantic-cards.json');sources=read('sources.json');drafts=read('candidate-drafts.json');contexts=read('context-records.json');cases=read('evaluation-cases.json');matrix=read('adoption-matrix.json')
    for name,rows,key in [('keywords',ks,'seed_id'),('cards',cards,'card_id'),('sources',sources,'id'),('drafts',drafts,'draft_id'),('contexts',contexts,'context_id'),('cases',cases,'case_id')]:check(len(rows)==len({r[key] for r in rows}),f'duplicate {name} id')
    kid={k['seed_id'] for k in ks};cid={c['card_id'] for c in cards};sid={s['id'] for s in sources};did={d['context_id'] for d in contexts}
    check(len(ks)==291,'keyword coverage');check(len(cards)==72,'card count');check(len(contexts)==26,'context distinctions');check(len(drafts)==65,'draft count')
    check(collections.Counter(k['provenance'] for k in ks)=={'connector_body':171,'browser_rendered_table_recovered':120},'connector/browser coverage')
    for k in ks:
        check(set(k['card_ids'])<=cid,f"unknown card {k['seed_id']}");check(bool(k['context_record_ids']) and set(k['context_record_ids'])<=did,f"unrouted context {k['seed_id']}")
        check(k['individually_source_verified'] is False,f"overclaimed keyword verification {k['seed_id']}")
    for c in cards:
        ident=c['card_id'];check(bool(c['proposal_en']) and bool(c['proposal_ko']),f'empty bilingual {ident}')
        check(set(c['seed_ids'])<=kid and bool(c['seed_ids']),f'bad seeds {ident}');check(set(c['source_ids'])<=sid,f'bad source {ident}')
        check(c['native_approval'] is False and c['registration_status']=='research_only',f'activation {ident}')
        for e in c['directed_relations']:
            check(e['from'] in c['owners'] and e['to'] in c['owners'],f'unresolved owner {ident} {e}')
            check(e['from']!=e['to'],f'self relation requires explicit review {ident}')
        check(len(c['review_gates'])==len(c['directed_relations']),f'missing gate {ident}')
        check(all(g['status']=='NOT_RUN' and g['partial_is_fail'] and not g['unobservable_is_pass'] for g in c['review_gates']),f'gate overclaim {ident}')
        check(bool(c['claim_limit']) and bool(c['nearest_confusion']),f'missing distinction {ident}')
    for d in drafts:
        c=next(c for c in cards if c['card_id']==d['card_id'])
        check(c['proposed_action'] not in ['context','defer'],f'deferred draft {d["draft_id"]}')
        check(d['en']==c['proposal_en'] and d['ko']==c['proposal_ko'],f'partial proposition {d["draft_id"]}')
        check(d['runtime_id'] is None and d['native_source_review']=='NOT_RUN',f'draft activation {d["draft_id"]}')
    for d in contexts:check(set(d['source_ids'])<=sid and set(d['seed_ids'])<=kid,f'context references {d["context_id"]}')
    check({m['card_id'] for m in matrix}==cid,'adoption coverage');check(all(x['retrieval']=='NOT_RUN' and x['pixels']=='NOT_RUN' for x in matrix),'adoption evidence overclaim')
    check(collections.Counter(c['group'] for c in cases)=={'development':65,'boundary':20,'general_control':12},'case group coverage');check(all(c['status']=='NOT_RUN' for c in cases),'unrun evaluation claim')
    check(collections.Counter(s['access'] for s in sources)=={'body':41,'search_excerpt':3,'failed':1},'source access count')
    for s in sources:check(all(s.get(k) for k in ['title','url','read_scope','supports','limits']),f'source missing scope {s["id"]}')
    for fname in ['existing-source-snapshots.json','topology-neighbors.json']:
        for r in read(fname):check(sha(json.dumps(r['record'],sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())==r['canonical_sha256'],f'original record checksum {r["cid"]}')
    links=[]
    for f in HERE.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',f.read_text()):
            if '://' in target or target.startswith('#') or target.startswith('/'):continue
            local=target.split('#')[0]
            if local and local not in ['VALIDATION.json','SHA256SUMS']:check((f.parent/local).exists(),f'broken link {f.name}: {target}')
            links.append(target)
    report=dict(schema='space-opera-research-validation/v1',status='PASS' if not issues else 'FAIL',issues=issues,counts=read('COUNTS.json'),checks=['unique IDs','291 original rows and connector/browser split','all keyword context routes','graph endpoints and nonreflexive relations','source/seed references','complete bilingual drafts','deferred/context exclusion','NOT_RUN boundaries','source access scope','original source-record checksums','local Markdown links'],proof_limit='research structure and evidence integrity only; not native qualification, retrieval, generation, pixels or user acceptance',source_review='sequential self-review after two bounded source investigations',runtime_registration='NOT_RUN',retrieval='NOT_RUN',image_calls=0,installation='NOT_RUN',commit_push='NOT_RUN')
    (HERE/'VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    files=sorted(p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS')
    (HERE/'SHA256SUMS').write_text(''.join(f'{sha(p.read_bytes())}  {p.relative_to(HERE)}\n' for p in files))
    print(json.dumps(dict(status=report['status'],issues=issues,hashed_files=len(files)),ensure_ascii=False))
    if issues:raise SystemExit(1)
if __name__=='__main__':main()
