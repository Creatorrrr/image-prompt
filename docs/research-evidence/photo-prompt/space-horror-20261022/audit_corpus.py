#!/usr/bin/env python3
"""Read source fields and capture research-only evidence. Never searches/rebuilds runtime."""
import collections, hashlib, json, re, subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(n,v): (HERE/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT).decode().strip()
def protected():
    names=git('ls-files','-z').split('\0')
    names += [str(p.relative_to(ROOT)) for p in ASSETS.glob('*2026102*.json')]
    return {n:sha((ROOT/n).read_bytes()) for n in sorted(set(names)) if n and (ROOT/n).is_file() and not n.startswith(str(HERE.relative_to(ROOT))+'/')}

def baseline():
    dump('BASELINE.json',dict(head=git('rev-parse','HEAD'),status=git('status','--short'),protected_sha256=protected(),scope='tracked files plus dated asset neighbors; excludes untracked runs and generated search shards'))

def audit():
    raw=(ASSETS/'photo_candidate_corpus_manifest.json').read_bytes();m=json.loads(raw)
    cand={};modules={};bind={};hashes={};duplicates=[]
    for mod in m['modules']:
        p=ASSETS/mod['file'];data=p.read_bytes();hashes[mod['file']]=sha(data);j=json.loads(data)
        for cid,r in j.get('candidates',{}).items():
            if cid in cand: duplicates.append(cid)
            cand[cid]=r;modules[cid]=mod['file']
        bind.update(j.get('slot_bindings',{}))
    fields=['en','ko','definition','phrase_en','phrase_ko','composition_instruction','runtime_expression']
    def strings(v,p):
        if isinstance(v,str): yield p,v
        elif isinstance(v,dict):
            for k,w in v.items(): yield from strings(w,p+'/'+k)
        elif isinstance(v,list):
            for k,w in enumerate(v): yield from strings(w,p+'/'+str(k))
    def texts(r):
        for f in fields:
            if f in r.get('content',{}): yield from strings(r['content'][f],'/content/'+f)
        for rid,rr in (r.get('realizations',{}) if isinstance(r.get('realizations',{}),dict) else {}).items():
            for box in ['', 'content']:
                ob=rr.get(box,{}) if box else rr
                for f in fields:
                    if isinstance(ob,dict) and f in ob: yield from strings(ob[f],'/realizations/'+rid+('/content' if box else '')+'/'+f)
    tt={c:list(texts(r)) for c,r in cand.items()}
    terms=['space horror','cosmic horror','airlock','depressurization','microgravity','tether','scrubber','life support','hull breach','derelict','ghost ship','generation ship','cryopod','stasis','bioship','living architecture','alien ocean','parasitoid','parasitic','symbiosis','ovipositor','artificial womb','quarantine','biomechanical','flesh fusion','hive mind','swarm','doppelganger','android','cognitohazard','information hazard','basilisk','event horizon','wormhole','impossible geometry','time loop','cassette','CRT','industrial decay','blood droplets','식인','생식','시신','진공','우주선']
    results=[];selected={}
    for term in terms:
        pattern=re.compile(r'(?<![a-z])'+re.escape(term)+r'(?![a-z])',re.I) if term.isascii() else re.compile(re.escape(term))
        hits=[]
        for cid,tx in tt.items():
            matches=[dict(pointer=p,text=t) for p,t in tx if pattern.search(t)]
            if matches: hits.append(dict(cid=cid,module=modules[cid],fields=matches))
        # Two complete records per focus, in deterministic source order; not rank.
        for h in hits[:2]: selected.setdefault(h['cid'],[]).append(term)
        results.append(dict(term=term,count=len(hits),hits=hits))
    snapshots=[]
    for cid,terms0 in selected.items():
        record=cand[cid]
        snapshots.append(dict(cid=cid,module=modules[cid],matched_terms=terms0,record=record,canonical_sha256=sha(json.dumps(record,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()),bindings=[dict(id=k,record=v) for k,v in bind.items() if v.get('candidate_id')==cid],decision='review_required',native_approval=False))
    changed=[f for f,h in hashes.items() if sha((ASSETS/f).read_bytes())!=h]
    summary=dict(schema='space-horror-corpus-audit/v1',head=git('rev-parse','HEAD'),candidates=len(cand),bindings=len(bind),modules=len(m['modules']),manifest_sha256=sha(raw),module_sha256=hashes,duplicate_candidate_ids=duplicates,fields=fields,selection='first_two_per_focus_in_manifest_order_not_rank',changes_during_read=changed,manifest_changed=sha((ASSETS/'photo_candidate_corpus_manifest.json').read_bytes())!=sha(raw),limitation='lexical evidence only; no match does not prove absent meaning; no embedding, material exposure, source qualification or pixel proof',results=results)
    dump('CORPUS-AUDIT.json',summary);dump('existing-source-snapshots.json',snapshots)
    print(json.dumps({k:summary[k] for k in ['candidates','bindings','modules','changes_during_read','manifest_changed']}));print(json.dumps([dict(term=r['term'],count=r['count']) for r in results],ensure_ascii=False))

def preservation():
    base=json.loads((HERE/'BASELINE.json').read_text());now=protected()
    changes=[dict(path=p,before=h,after=now.get(p)) for p,h in base['protected_sha256'].items() if now.get(p)!=h]
    dump('PRESERVATION.json',dict(head_before=base['head'],head_after=git('rev-parse','HEAD'),changes=changes,protected_count=len(base['protected_sha256']),attribution='observed drift is not automatically attributable to this research; only new files in this research folder were authored by this task'))
    print('protected drift',len(changes))

if __name__=='__main__':
    import sys
    {'baseline':baseline,'audit':audit,'preservation':preservation}[sys.argv[1]]()
