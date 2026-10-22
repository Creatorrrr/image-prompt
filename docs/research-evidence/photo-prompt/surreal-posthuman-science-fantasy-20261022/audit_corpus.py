"""Read-only corpus snapshot. Lexical diagnostics, never retrieval or adoption evidence."""
from pathlib import Path
import hashlib, json, re, subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,d):
    p=HERE/name
    if p.exists(): raise SystemExit(f'Refusing to overwrite historical snapshot: {p}')
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

manifest=json.loads((ASSETS/'photo_candidate_corpus_manifest.json').read_text())
records={};owners={};bindings={};module_hashes={}
for module in manifest['modules']:
    path=ASSETS/module['file'];module_hashes[str(path.relative_to(ROOT))]=sha(path)
    d=json.loads(path.read_text())
    for cid,record in d.get('candidates',{}).items():
        if cid in records:raise SystemExit(f'duplicate CID: {cid}')
        records[cid]=record;owners[cid]=str(path.relative_to(ROOT))
    for bid,binding in d.get('slot_bindings',{}).items():bindings.setdefault(binding['candidate_id'],[]).append(binding)

def positive_text(record):
    content=record.get('content',{})
    return '\n'.join(str(content.get(k,'')) for k in ['en','ko','phrase_en','phrase_ko'])
def alias_text(record):
    return json.dumps(record.get('content',{}).get('aliases',[]),ensure_ascii=False)

queries={
'A':['surreal','oneiric','metamorph','juxtaposition','초현실','변형','도자기','porcelain'],
'B':['double image','anamorph','reflection','shadow','왜상','거울','반사','이중 이미지'],
'C':['socket','cable','prosthetic','biomechanical','소켓','접합','인공 팔','생체'],
'D':['memory','archive','hive','upload','기억','인지','서랍','단말'],
'E':['living architecture','mycel','root','membrane','살아 있는 건축','균사','뿌리','주름막'],
'F':['ritual','crank','circuit','bell','의례','크랭크','회로','종'],
'G':['megastructure','pocket universe','vast','거대한','우주','광물','거주'],
'H':['recursive','model','palimpsest','portrait','재귀','모형','초상','겹친'],
'I':['chimera','hybrid','pouch','culture','키메라','혼성','주머니','배양'],
'J':['scar','shell','seam','viscous','흉터','외피','이음','점성'],
'K':['intimacy','glove','adult','touch','친밀','장갑','성인','접촉'],
'L':['ration','worker','repair','display','배급','작업자','수선','진열']}

audit=[];selected=[]
for family,terms in queries.items():
    term_rows=[];scores={}
    for term in terms:
        term_l=term.casefold();positive=[];alias_only=[]
        # A substring diagnostic deliberately records ambiguity and never claims semantic qualification.
        for cid,record in records.items():
            if term_l in positive_text(record).casefold():positive.append(cid);scores[cid]=scores.get(cid,0)+1
            elif term_l in alias_text(record).casefold():alias_only.append(cid)
        term_rows.append(dict(term=term,positive_field_hits=len(positive),alias_only_hits=len(alias_only),positive_sample_ids=positive[:5],match='casefolded substring; not role fit'))
    ordered=sorted(scores,key=lambda cid:(-scores[cid],cid))
    # Prefer topic extensions to inspect close neighbors, then distinct whole-source owners.
    prioritized=[cid for cid in ordered if '_202610' in owners[cid]]+[cid for cid in ordered if '_202610' not in owners[cid]]
    sample=[]
    for cid in prioritized:
        if cid in selected:continue
        sample.append(cid);selected.append(cid)
        if len(sample)==3:break
    audit.append(dict(family=family,terms=term_rows,positive_any_hit_count=len(scores),selected_snapshot_ids=sample))

snapshot=[]
for cid in selected:
    record=records[cid]
    snapshot.append(dict(candidate_id=cid,owner_module=owners[cid],module_sha256=module_hashes[owners[cid]],
                         record_sha256=hashlib.sha256(json.dumps(record,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest(),
                         record=record,bindings=bindings.get(cid,[]),decision='semantic_review_pending',
                         native_approval=False,limit='Whole record snapshot is a neighbor for review, not approval or a candidate-pack result.'))

write('CORPUS-AUDIT.json',dict(schema='research-corpus-lexical-snapshot/v1',date_kst='2026-10-22',
      candidates=len(records),bindings=sum(map(len,bindings.values())),modules=len(module_hashes),
      slots=len(json.loads((ASSETS/'photo_candidate_slot_catalog.json').read_text())['slot_catalog']),
      manifest_sha256=sha(ASSETS/'photo_candidate_corpus_manifest.json'),module_sha256=module_hashes,
      matching_scope='Exact own en/ko/phrase fields. No definitions, research metadata or negative examples are positive evidence. Aliases separately counted.',
      lexical_limit='A hit is not meaning; zero is not corpus absence. No embedding, query pipeline, ranking receipt or native approval ran.',families=audit))
write('existing-source-snapshots.json',dict(schema='research-source-neighbors/v1',snapshots=snapshot))
runtime_paths=['skills/photo-prompt-image-generator/retrieval-runtime.json','skills/photo-prompt-image-generator/assets/photo_candidate_search.json']
runtime={p:{'sha256':sha(ROOT/p),'data':json.loads((ROOT/p).read_text())} for p in runtime_paths}
# Save the runtime declaration, not its potentially huge search bodies.
runtime[runtime_paths[1]]['data']={k:v for k,v in runtime[runtime_paths[1]]['data'].items() if k in ['schema','space','corpus_sha256','index_source_sha256','layout_id','lexical_recipe','routing_recipe','embedding','model','backend','source_fingerprint','source_revision','generation_id','embedding_space','vector_dimensions']}
check=subprocess.run(['python3',str(ROOT/'skills/photo-prompt-image-generator/scripts/photo_installed_h_f2.py'),'--check-runtime'],cwd=ROOT,capture_output=True,text=True)
write('RUNTIME-OBSERVATION.json',dict(schema='research-runtime-observation/v1',declarations=runtime,check_exit_code=check.returncode,installed_check=json.loads(check.stdout),evidence_limit='Dependencies and recorder compatibility only. No source adoption, retrieval or image qualification.'))
print(json.dumps({'candidates':len(records),'modules':len(module_hashes),'whole_record_snapshots':len(snapshot),'runtime_check':check.returncode}))
