"""Serialize explicit per-pair authored inverse findings only; offline, no tagging."""
import sys,json,hashlib,datetime,collections,runpy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import inverse_11870_047_094 as q
def ptr(v,p):
 for k in p.strip('/').split('/'):v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
def bindings(v):
 out=set()
 if isinstance(v,dict):
  for k,x in v.items():
   if k=='binding_id' and isinstance(x,str):out.add(x)
   else:out.update(bindings(x))
 elif isinstance(v,list):
  for x in v:out.update(bindings(x))
 return sorted(out)
def write(literal_path):
 a=runpy.run_path(str(literal_path));start,stop=a['RANGE'];J=a['J'];R=q.R;h=q.dr.c.digest
 stem=f'inverse_11870_{start:03d}_{stop:03d}';out=R/f'authored/{stem}.json';snap=R/f'authored/{stem}_blind_sources.json';note=R/f'worker-notes/inverse-11870-{start:03d}-{stop:03d}.json'
 assert not any(x.exists() for x in [out,snap,note])
 inputs={str(p.relative_to(R)):{'bytes_sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [q.PLAN,q.RESULT,R/'SOURCE.json.gz',R/'CATALOG.json',R/'CATALOG-CORRECTED-PROPOSAL-01.json',Path(q.__file__),Path(__file__),literal_path]}
 inputs.update(source_canonical_sha256=h(q.d),catalog139_canonical_sha256=h(q.d['slot_catalog']),proposed141_catalog_canonical_sha256=h(q.proposal['catalog']))
 slots=[];logs=[];sources={};seen={}
 for i in range(start,stop):
  slot=q.p['queries'][i]['slot_id'];lanes,union=q.discovery(i);rows=[x for x in J if x[0]==i];assert [x[1] for x in rows]==union,(i,'coverage')
  reviewed=[]
  for _,cid,status,pointer,quote,meaning,owner,prop,dim,scope,reason,issue in rows:
   row=q.d['candidates'][cid];refs=q.dr.closure(q.d,cid);rids=q.pr.ids(row);bids=bindings([row,*refs.values()])
   assert status in {'fit','nonfit','pending'};assert quote in ptr(row,pointer),(cid,pointer);assert cid in a['FULL_READ_IDS'];assert set(refs)<=set(a.get('FULL_READ_CLOSURE_IDS',[])),(cid,'unread closure')
   sources[cid]={'source_sha256':h(row),'source':q.blind(row),'closure':{k:{'source_sha256':h(v),'source':q.blind(v)} for k,v in refs.items()},'frozen_bindings':{k:{'source_sha256':h(q.d['slot_bindings'][k]),'source':q.blind(q.d['slot_bindings'][k])} for k in bids}}
   logid=f'{stem}-slot{i}-{cid}';logs.append({'read_id':logid,'slot_index':i,'slot_id':slot,'candidate_id':cid,'source_sha256':h(row),'full_semantic_source_conditions_effects_alternatives_read':True,'complete_required_closure_read':True,'closure_ids':list(refs),'closure_sha256':{k:h(v) for k,v in refs.items()},'frozen_binding_ids':bids,'realization_ids':rids,'duplicate_record_equal_to':seen.get(cid)});seen.setdefault(cid,logid)
   anchor={'candidate_id':cid,'source_sha256':h(row),'pointer':pointer,'quote':quote}
   reviewed.append({'candidate_id':cid,'authored_status':status,'actual_record_kind':row['record_kind'],'meaning':meaning,'source_anchor':anchor,'positive_slot_evidence':[anchor] if status=='fit' else [],'owner':owner,'asserted_property':prop,'asserted_dimension':dim,'actual_realization_ids':rids,'role_scope_and_prerequisites':scope,'reason_and_neighbor_boundary':reason,'specific_qualification_or_uncertainty':issue,'conditions_exact':row.get('conditions',{}),'effects_exact':row.get('effects',{}),'full_source_read_id':logid,'automatic_tag_confirmation':False,'current_binding_comparison':'Root owns later comparison; existing tags/reviews hidden.','source_corrections':[]})
  old=q.d['slot_catalog'][slot];new=q.proposal['catalog'].get(slot)
  diff={k:{'frozen139':old.get(k),'proposed141':new.get(k)} for k in sorted(set(old)|set(new)) if old.get(k)!=new.get(k)}
  slots.append({'sorted139_slot_index':i,'slot_id':slot,'spec139':old,'spec139_sha256':h(old),'query_fields':q.p['queries'][i]['fields'],'proposal141_spec':new,'proposal141_spec_sha256':h(new),'proposal141_spec_exact_equal_to139':old==new,'proposed141_field_changes':diff,'proposal141_change_impact':a['SPEC_IMPACT'][i],'discovery_top3_by_lane':lanes,'discovery_union':union,'individual_judgments':reviewed})
 now=datetime.datetime.now(datetime.timezone.utc).isoformat();counts=dict(collections.Counter(x[2] for x in J))
 proof='Frozen139 top3 discovery only; manually authored fit/nonfit/pending, no automatic tag confirmation or existing-binding comparison. Proposed141 specification differences are separately recorded; no141 retrieval, runtime-core, pixels, full-recall or overall-quality completion claim.'
 body={'schema':'photo-inverse-direct-semantic-investigation/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','recorded_at':now,'parent_assigned_sorted139_range':[52,94],'completed_contiguous_sorted139_range':[start,stop],'input_hashes':inputs,'blinding':['content.tags','content.facets','all role_evidence','all semantic_review','source slot_id/semantic_role annotations','provenance.source tag routes'],'proof_boundary':proof,'slot_reviews':slots,'direct_read_log':logs,'read_commands':a['READ_COMMANDS'],'related_full_specs':{k:q.d['slot_catalog'][k] for k in a['RELATED_FULL_SPECS']}}
 out.write_text(json.dumps(body,ensure_ascii=False,indent=2)+'\n');snap.write_text(json.dumps({'source_sha256':h(q.d),'candidates':sources},ensure_ascii=False,indent=2)+'\n')
 n={'task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','recorded_at':now,'completed_contiguous_sorted139_range':[start,stop],'complete_source_and_closure_read_for_this_checkpoint':True,'directly_reviewed_slot_count':stop-start,'directly_reviewed_candidate_slot_pair_count':len(J),'unique_discovery_candidate_count':len(sources),'counts':counts,'pending_pairs':[[x[0],x[1]] for x in J if x[2]=='pending'],'next_unread_slot_index':stop,'next_unread_slot_id':q.p['queries'][stop]['slot_id'] if stop<94 else None,'remaining_assigned_range':[stop,94] if stop<94 else None,'input_hashes':inputs,'authored_paths':[str(out),str(snap),str(literal_path),str(Path(__file__).resolve())],'output_bytes_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [out,snap]},'direct_read_log':logs,'read_commands':a['READ_COMMANDS'],'specific_qualification_issues':a['ISSUES'],'mechanical_checks':['Exact per-slot top3 union coverage/order','Every manual quote contained at exact source pointer','Fixed original source/catalog canonical hashes','Actual native realization IDs retained without base-only assumptions','Every required closure ID explicitly included in directly read IDs','139/141 differences recorded separately'],'proof_boundary':proof,'no_model_or_network_calls':True,'no_registration_canonical_git_changes':True}
 note.write_text(json.dumps(n,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'range':[start,stop],'pair_count':len(J),'counts':counts,'json':str(out),'json_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'note':str(note)},ensure_ascii=False))
if __name__=='__main__':write(Path(sys.argv[1]).resolve())
