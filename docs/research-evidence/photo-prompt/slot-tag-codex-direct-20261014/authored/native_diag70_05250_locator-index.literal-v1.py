import json,gzip,hashlib
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');p=R/'authored/native_diag70_05250_read-packet-v1.json';x=json.loads(p.read_text());sp=R/'SOURCE.json.gz';cp=R/'native-inputs/root-lower-lashes-source-plan-16-R02/CURRENT-PROPOSAL.json.gz';s=json.load(gzip.open(sp));c=json.load(gzip.open(cp));order=json.load(open(R/'ORDER.json'));op=Path(x['origin']['file']);orig=json.load(open(op));catp=R/'CATALOG-FINAL-149-V6.json'
def raw(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def loc(ptr,obj):return {'file':str(op),'file_sha256':raw(op),'pointer':ptr,'sha256':sha(obj)}
def pointerget(obj,ptr):
 for k in ptr.strip('/').split('/'):obj=obj[int(k)] if isinstance(obj,list) else obj[k.replace('~1','/').replace('~0','~')]
 return obj
assert sha(s)==x['source_original_sha256'];assert sha(c)==x['source66_sha256'];assert sha(json.load(open(catp)))==x['catalog149_sha256']
byfiles={};packets={};rows=[]
contexts={}
for k in ['schema_version','domain','priority_order','max_support_cues','axis_vocabularies','families','policies','compatibility_edges','guard_rules']:
 v=orig['character_mechanism_graph'][k];assert v==x['origin_graph_context'][k];contexts[k]=loc('/character_mechanism_graph/'+k,v)
for i,v in enumerate(orig['character_mechanism_graph']['concept_profiles']):assert v==x['origin_parent_profiles'][i];contexts['profile_'+v['id']]=loc('/character_mechanism_graph/concept_profiles/'+str(i),v)
review_paths=[R/'authored/native_diag70_05250_000_015.review-v1.json',R/'authored/native_diag70_05250_015_047.review-v1.json',R/'authored/native_diag70_05250_047_070.review-v1.json'];reviews={}
for f in review_paths:
 y=json.load(open(f))
 for i,r in enumerate(y['rows']):assert r['candidate_id'] not in reviews;reviews[r['candidate_id']]={'file':str(f),'file_sha256':raw(f),'item':i+1,'row_sha256':sha(r),'recommendation':r['retain_diagnostic_recommendation']}
assert len(reviews)==70
for r in x['records']:
 cid=r['candidate_id'];o=r['ordinal'];assert order[o]==cid;assert s['candidates'][cid]==r['original']==r['current66']==c['candidates'][cid]
 b=r['original5B'];bp=Path(b['file']);bdoc=byfiles.setdefault(str(bp),json.load(open(bp)));assert raw(bp)==b['file_raw_sha256'];actualrow=bdoc['decisions'][b['item']-1];assert actualrow==b['row'] and sha(actualrow)==b['row_sha256'];assert actualrow['candidate_id']==cid
 pp=R/'packets'/f'{(o//250)*250:05d}-250.json';pk=packets.setdefault(str(pp),json.load(open(pp)));assert cid in pk['ids'];assert pk['records'][cid]==s['candidates'][cid];assert sha(pk)==b['row']['packet_sha256'];assert pk['source_sha256']==sha(s)
 assert not {k:v for k,v in s['slot_bindings'].items() if v['candidate_id']==cid};assert not {k:v for k,v in c['slot_bindings'].items() if v['candidate_id']==cid}
 assert r['own_original_bindings']==r['own_current_bindings']==r['required_original_closure']==r['required_current_closure']=={}
 e=pointerget(orig,r['origin']['pointer']);assert e==r['origin']['record'];assert sha(e)==r['origin']['canonical_sha256']==r['original']['provenance'][0]['sha256']
 parents=[]
 if r['origin']['parent_profile_pointer']:
  ptr=r['origin']['parent_profile_pointer'];parents.append(loc(ptr,pointerget(orig,ptr)))
 else:
  for i,f in enumerate(orig['character_mechanism_graph']['families']):
   if f['id'] in r['original']['content']['family_ids']:parents.append(loc('/character_mechanism_graph/families/'+str(i),f))
  for i,e2 in enumerate(orig['character_mechanism_graph']['compatibility_edges']):
   if e2['topic_id'] in r['original']['content']['topic_ids']:parents.append(loc('/character_mechanism_graph/compatibility_edges/'+str(i),e2))
 rows.append({'ordinal':o,'candidate_id':cid,'original_compiled_locator':{'file':str(bp),'file_sha256':raw(bp),'item':b['item'],'row_sha256':sha(actualrow)},'original_packet':{'file':str(pp),'file_sha256':raw(pp),'sha256':sha(pk),'record_pointer':'/records/'+cid,'record_sha256':sha(pk['records'][cid])},'original_source':{'file':str(sp),'file_sha256':raw(sp),'sha256':sha(s),'pointer':'/candidates/'+cid,'row_sha256':sha(s['candidates'][cid])},'current_source66':{'file':str(cp),'file_sha256':raw(cp),'sha256':sha(c),'pointer':'/candidates/'+cid,'row_sha256':sha(c['candidates'][cid])},'exact_original_entry':{**loc(r['origin']['pointer'],e),'source_provenance':r['original']['provenance'][0],'full_entry':e},'parent_context_locators':parents,'shared_parent_context_keys':['schema_version','domain','priority_order','max_support_cues','axis_vocabularies','families','policies','compatibility_edges','guard_rules'],'original_own_bindings':{},'current_own_bindings':{},'required_closure':{},'independent_semantic_read_locator':reviews[cid],'root_selection':False})
assert len(rows)==70 and len({r['candidate_id'] for r in rows})==70
out={'schema':'diagnostic70-root-input-locator-proposal/v1','task':'/root/review_05250_06250','model':'gpt-6.1-sol','effort':'high','purpose':'Mechanical exact identity/locator extraction from already directly read records and context, for root independent plain INPUT/ASSIGNMENT preparation. No kind approval, semantic inference, source-native BATCH, permission proof or status activation.','item_index_base':1,'ordinal_index_base':0,'file_sha256_definition':'raw file bytes, including compressed bytes for .gz','sha256_definition':'canonical UTF-8 JSON ensure_ascii=False sort_keys=True separators=(comma,colon)','read_packet':{'file':str(p),'file_sha256':raw(p)},'catalog149':{'file':str(catp),'file_sha256':raw(catp),'sha256':sha(json.load(open(catp)))},'shared_parent_context_manifest':contexts,'rows':rows,'actual_direct_read_count':70,'mechanical_locator_checks_passed':70,'independent_recommendations':{'retain_diagnostic':65,'semantic_HOLD':5},'root_selected_diagnostic':0,'formal_native_proofs':0,'operational_changes':0,'bulk8000_addition':0}
q=R/'authored/native_diag70_05250_locator-index-v1.json';assert not q.exists();q.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');n={'task':out['task'],'model':out['model'],'effort':out['effort'],'artifact':str(q),'raw_sha256':raw(q),'canonical_sha256':sha(out),'verified_original_compiled_rows':70,'verified_packet_hashes':len(packets),'verified_origin_entry_hashes':70,'verified_current_original_equal':70,'full_source_5B_ownbindings_closure_provenance_direct_read':70,'semantic_classifier_or_native_verifier_run':0,'root_selected_or_operating':0,'final_read_artifacts':[{'file':str(f),'raw_sha256':raw(f)} for f in review_paths],'five_HOLD_detail':{'file':str(R/'authored/native_diag70_05250_hold5.alternatives-v1.json'),'raw_sha256':raw(R/'authored/native_diag70_05250_hold5.alternatives-v1.json')},'boundary':'Identity/hash checks are not semantic approval. Earlier preparation packet actual_read_count0 remains immutable historical metadata; three review checkpoints attest later actual70. Three separate profile records and20 scene-slot examples are context, never added to candidate/bulk completion counts.'};z=R/'worker-notes/native_diag70_05250_locator-index.worker-note-v1.json';assert not z.exists();z.write_text(json.dumps(n,ensure_ascii=False,indent=2)+'\n');print(json.dumps(n,ensure_ascii=False))
