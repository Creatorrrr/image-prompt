import json,pathlib,hashlib,copy
r=pathlib.Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');pp=r/'authored/native_05250_peer05.01285_01295.read-packet-v1.json';x=json.loads(pp.read_text())
def canon(a):return hashlib.sha256(json.dumps(a,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def point(x,p):
 for s in p.strip('/').split('/'):
  s=s.replace('~1','/').replace('~0','~');x=x[int(s)] if isinstance(x,list) else x[s]
 return x
rows=[]
for a in x['records']:
 errors=[];cp=a['checkpoint_record'];p=cp['proof'];cid=a['candidate_id'];old=a['original_5B']; assert a['original_packet_record']==a['original']; assert a['own_current_bindings']==a['own_original_bindings'];assert not cp['dependency_records'] and not cp['reference_bindings'];assert canon(old)==cp['original_compiled']['row_sha256']
 after=copy.deepcopy(a['original'])
 for co in old['corrections']:
  container=after;parts=co['pointer'].strip('/').split('/')
  for s in parts[:-1]:container=container[s]
  assert container[parts[-1]]==co['before'];container[parts[-1]]=co['after']
 for group in ['facts','source_units','guard_supports']:
  for f in p.get(group,[]):
   field=point(a['current'],f['pointer'])
   if not isinstance(field,str) or f['quote'] not in field:errors.append({'group':group,'id':f.get('id'),'pointer':f['pointer'],'quote':f['quote'],'field':field})
 for v in p.get('manual_role_views',[]):
  for anchor in v['normal_anchors']:
   field=point(a['current'],anchor['pointer'])
   if field[anchor['start']:anchor['stop']]!=anchor['facet_quote']:errors.append({'view':v['id'],'anchor_error':anchor})
 rows.append({'ordinal':a['ordinal'],'candidate_id':cid,'checkpoint_record_sha256':canon(cp),'original_record_sha256':canon(a['original']),'exact5B_after_sha256':canon(after),'current_record_sha256':canon(a['current']),'original_compiled':cp['original_compiled'],'fact_count':len(p['facts']),'source_unit_count':len(p['source_units']),'RID_count':len(p['effect_sets']),'manual_role_view_count':len(p.get('manual_role_views',[])),'quote_errors':errors,'full_original_and_current_ownbinding_equal':True,'reference_closure_empty':True,'exact5Bafter':after if after!=a['original'] else {'exact_equal':'original'}})
y={'schema':'independent-peer-literal-audit/v1','task':'/root/review_05250_06250','model':'gpt-6.1-sol','effort':'high','prepared':10,'semantic_approval_automated':False,'consumer_rerun':False,'boundary':'Only byte/hash/pointer/quote/closure mechanical checks. Manual semantic decisions separately authored.','packet_raw_sha256':hashlib.sha256(pp.read_bytes()).hexdigest(),'records':rows}
p=r/'authored/native_05250_peer05.01285_01295.literal-audit-v1.json';assert not p.exists();p.write_text(json.dumps(y,ensure_ascii=False,indent=2)+'\n');print('AUDIT',hashlib.sha256(p.read_bytes()).hexdigest());print('ERRORS',json.dumps([q for q in rows if q['quote_errors']],ensure_ascii=False));print('TOTALS',{k:sum(q[k] for q in rows) for k in ['fact_count','source_unit_count','RID_count','manual_role_view_count']});print('CHANGED5B',json.dumps([{'ordinal':q['ordinal'],'5B_after':q['exact5Bafter']} for q in rows if 'exact_equal' not in q['exact5Bafter']],ensure_ascii=False))
