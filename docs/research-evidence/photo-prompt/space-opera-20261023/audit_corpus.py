#!/usr/bin/env python3
"""Read-only corpus inspection; writes evidence only beside this script."""
import collections, hashlib, json, re, subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(name,data): (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT).decode().strip()
def protected():
    paths=git('ls-files','-z').split('\0')
    paths += [str(p.relative_to(ROOT)) for p in ASSETS.glob('*2026102*.json')]
    return {p:sha((ROOT/p).read_bytes()) for p in sorted(set(paths)) if p and (ROOT/p).is_file() and not p.startswith(str(HERE.relative_to(ROOT))+'/')}
def baseline():
    dump('BASELINE.json',dict(head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),dirty=git('status','--short'),protected_sha256=protected(),scope='tracked files and dated neighbor assets; excludes untracked runs/search shards'))
def audit():
    raw=(ASSETS/'photo_candidate_corpus_manifest.json').read_bytes(); manifest=json.loads(raw)
    candidates={};bindings={};modules={};hashes={};duplicates=[]
    for m in manifest['modules']:
        b=(ASSETS/m['file']).read_bytes();hashes[m['file']]=sha(b);j=json.loads(b)
        for cid,c in j.get('candidates',{}).items():
            if cid in candidates: duplicates.append(cid)
            candidates[cid]=c;modules[cid]=m['file']
        bindings.update(j.get('slot_bindings',{}))
    # Positive authored fields only. Research title/aliases/negative metadata excluded.
    fields=['en','ko','definition','phrase_en','phrase_ko','composition_instruction','runtime_expression']
    def flatten(v,p):
        if isinstance(v,str): yield p,v
        elif isinstance(v,dict):
            for k,w in v.items(): yield from flatten(w,p+'/'+k)
        elif isinstance(v,list):
            for i,w in enumerate(v): yield from flatten(w,p+'/'+str(i))
    def texts(c):
        for f in fields:
            if f in c.get('content',{}): yield from flatten(c['content'][f],'/content/'+f)
        rr=c.get('realizations',{})
        if isinstance(rr,dict):
            for rid,r in rr.items():
                for box in ['', 'content']:
                    ob=r.get(box,{}) if box else r
                    for f in fields:
                        if isinstance(ob,dict) and f in ob: yield from flatten(ob[f],'/realizations/'+rid+('/content' if box else '')+'/'+f)
    txt={cid:list(texts(c)) for cid,c in candidates.items()}
    terms=['space opera','galactic empire','federation','senate','heraldry','dynastic','customs','freighter','smuggling','resource monopoly','jump gate','wormhole','hyperspace','warp drive','ion thruster','solar sail','radiator','generation ship','cryopod','bioship','airlock','tether','torus','cylinder','ringworld','dyson','shipyard','carrier','capital ship','point defense','railgun','blockade','first contact','translator','hive mind','symbiosis','android','cyborg','shipmind','mind fork','artificial womb','reproductive','consent','slavery','glassing','refugee','used future','cassette','greeble','holographic','tactical table','space bikini','pressure suit','기밀실','우주선','행성']
    results=[];picked={}
    for term in terms:
        pat=re.compile((r'(?<![a-z])'+re.escape(term)+r'(?![a-z])') if term.isascii() else re.escape(term),re.I)
        hits=[]
        for cid,tx in txt.items():
            mt=[dict(pointer=p,text=t) for p,t in tx if pat.search(t)]
            if mt: hits.append(dict(cid=cid,module=modules[cid],matches=mt))
        for h in hits[:2]: picked.setdefault(h['cid'],[]).append(term)
        results.append(dict(term=term,count=len(hits),hits=hits))
    snaps=[dict(cid=cid,module=modules[cid],matched_terms=ts,record=candidates[cid],canonical_sha256=sha(json.dumps(candidates[cid],sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()),bindings=[dict(id=k,record=v) for k,v in bindings.items() if v.get('candidate_id')==cid]) for cid,ts in picked.items()]
    dump('CORPUS-AUDIT.json',dict(schema='space-opera-corpus-lexical-audit/v1',head=git('rev-parse','HEAD'),candidates=len(candidates),bindings=len(bindings),modules=len(manifest['modules']),manifest_sha256=sha(raw),module_sha256=hashes,duplicates=duplicates,fields=fields,results=results,selection='first two matches per term in manifest order; not relevance ranking',changes_during_read=[f for f,h in hashes.items() if sha((ASSETS/f).read_bytes())!=h],manifest_changed=sha((ASSETS/'photo_candidate_corpus_manifest.json').read_bytes())!=sha(raw),proof_limit='lexical coverage only; zero does not establish semantic absence; no query embedding/retrieval/qualification/pixels'))
    dump('existing-source-snapshots.json',snaps)
    print(json.dumps(dict(candidates=len(candidates),bindings=len(bindings),modules=len(manifest['modules']),snapshots=len(snaps),hits={r['term']:r['count'] for r in results}),ensure_ascii=False))
def preservation():
    b=json.loads((HERE/'BASELINE.json').read_text());now=protected()
    changes=[dict(path=p,before=h,after=now.get(p)) for p,h in b['protected_sha256'].items() if now.get(p)!=h]
    dump('PRESERVATION.json',dict(head_before=b['head'],head_after=git('rev-parse','HEAD'),changes=changes,protected_files=len(b['protected_sha256']),attribution='observed concurrent drift is not attributed automatically; task writes are restricted to this research directory'))
    print(json.dumps(dict(protected_files=len(b['protected_sha256']),drift=len(changes))))
if __name__=='__main__':
    import sys
    {'baseline':baseline,'audit':audit,'preservation':preservation}[sys.argv[1]]()
