#!/usr/bin/env python3
"""Read-only, bounded lexical diagnostic. This is NOT H-F2 retrieval/qualification."""
import hashlib,json,re,collections
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'

def digest(b):return hashlib.sha256(b).hexdigest()
def write(name,data):(HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def main():
    manifest_bytes=(ASSETS/'photo_candidate_corpus_manifest.json').read_bytes()
    manifest=json.loads(manifest_bytes); hashes={};candidates={};owners={};bindings={}
    duplicate_ids=[]
    for mod in manifest['modules']:
        path=ASSETS/mod['file'];raw=path.read_bytes();hashes[mod['file']]=digest(raw);data=json.loads(raw)
        for cid,record in data.get('candidates',{}).items():
            if cid in candidates:duplicate_ids.append(cid)
            candidates[cid]=record;owners[cid]=mod['file']
        bindings.update(data.get('slot_bindings',{}))
    # Fixed named fields only. Unknown, negative, metadata and commentary fields
    # are deliberately excluded. Each selected realization is recorded separately.
    fields=('en','ko','definition','phrase_en','phrase_ko','composition_instruction','runtime_expression')
    def strings(value,pointer):
        if isinstance(value,str):yield pointer,value
        elif isinstance(value,dict):
            for k,v in value.items():yield from strings(v,pointer+'/'+k)
        elif isinstance(value,list):
            for i,v in enumerate(value):yield from strings(v,pointer+'/'+str(i))
    def selected_text(record):
        content=record.get('content',{})
        for k in fields:
            if k in content:yield from strings(content[k],'/content/'+k)
        realizations=record.get('realizations',{})
        if isinstance(realizations,dict):
            for rid,branch in realizations.items():
                if not isinstance(branch,dict):continue
                for k in fields:
                    for box in ('content',''):
                        obj=branch.get(box,{}) if box else branch
                        if isinstance(obj,dict) and k in obj:
                            yield from strings(obj[k],'/realizations/'+str(rid)+('/content' if box else '')+'/'+k)
    texts={cid:list(selected_text(c)) for cid,c in candidates.items()}
    routes=json.loads((HERE/'keyword-routes.json').read_text())['routes']
    patterns={}
    for r in routes:
        english=r['en'].split(' / ')
        korean=r['ko'].split('·') if r['ko'] else []
        terms=[t.strip() for t in english+korean if len(t.strip())>=3]
        patterns[r['id']]=[(t,re.compile((r'(?<![a-z])'+re.escape(t)+r'(?![a-z])') if t.isascii() else re.escape(t),re.I)) for t in terms]
    findings=[];by_term=[]
    for route in routes:
        hits=[]
        for cid,values in texts.items():
            local=[]
            for pointer,value in values:
                matches=[t for t,pat in patterns[route['id']] if pat.search(value)]
                if matches:local.append(dict(pointer=pointer,terms=matches,exact_field_text=value))
            if local:hits.append(dict(cid=cid,module=owners[cid],field_matches=local))
        by_term.append(dict(term_id=route['id'],en=route['en'],patterns=[t for t,_ in patterns[route['id']]],count=len(hits),hits=hits))
    focus=['reliquary','gargoyle','necromanc','chiaroscuro','tenebrism','memento mori','ossuary','catacomb','living armor','living architecture','body fusion','shadow','gothic','ritual','crypt','grimoire','fallen paladin','death knight']
    selected={}
    for term in focus:
        found=[cid for cid,values in texts.items() if any(term in v.casefold() for _,v in values)]
        # A bounded diagnostic shortlist only, with deterministic corpus order.
        for cid in found[:2]:
            selected.setdefault(cid,[]).append(term)
        findings.append(dict(pattern=term,count=len(found),selected_cids=found[:2],selection='first_two_in_manifest_order_not_relevance_rank'))
    mapping=[]
    for cid,reasons in selected.items():
        b=[dict(id=bid,record=v) for bid,v in bindings.items() if cid in json.dumps(v,ensure_ascii=False)]
        raw=json.dumps(candidates[cid],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
        mapping.append(dict(cid=cid,module=owners[cid],canonical_record_sha256=digest(raw),matched_focus=reasons,
                            record=candidates[cid],bindings=b,decision='review_required',
                            review_scope='full record captured; selected findings are discussed in CORPUS-FINDINGS.md; not all captured bindings semantically approved',
                            integration_options=['reuse_complete_source','refine_with_explicit_diff','new_only_for_missing_relation','context_or_defer'],
                            native_approval=False))
    changed=[f for f,h in hashes.items() if digest((ASSETS/f).read_bytes())!=h]
    manifest_changed=digest((ASSETS/'photo_candidate_corpus_manifest.json').read_bytes())!=digest(manifest_bytes)
    snapshot=dict(schema='dark-fantasy-corpus-lexical-audit/v1',candidate_count=len(candidates),binding_count=len(bindings),
                  module_count=len(manifest['modules']),manifest_sha256=digest(manifest_bytes),module_sha256=hashes,
                  selected_fields=list(fields),duplicate_candidate_ids=duplicate_ids,
                  changes_during_read=changed,manifest_changed_during_read=manifest_changed,
                  limitation='bounded exact-field lexical diagnostic; 0 does not prove semantic absence; counts are neither exposure, rank nor native qualification',
                  term_results=by_term,focus_results=findings)
    write('CORPUS-LEXICAL-AUDIT.json',snapshot);write('existing-source-mapping.json',mapping)
    print(json.dumps(dict(candidates=len(candidates),bindings=len(bindings),modules=len(manifest['modules']),
                          zero_lexical_terms=sum(x['count']==0 for x in by_term),mapping_records=len(mapping),
                          changes_during_read=changed,manifest_changed=manifest_changed,focus=findings),ensure_ascii=False))

if __name__=='__main__':main()
