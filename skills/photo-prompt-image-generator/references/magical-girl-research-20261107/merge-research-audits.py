import collections,copy,csv,glob,hashlib,json,os
from pathlib import Path
p=Path('skills/photo-prompt-image-generator/references/magical-girl-research-20261107');a=Path('skills/photo-prompt-image-generator/assets'); f=p/'source-reconciliation.json';d=json.loads(f.read_text()); rows={x['id']:x for x in d['rows']};manifest=json.loads((a/'photo_candidate_corpus_manifest.json').read_text()); module_cache={};binding_by_id={};bindings_for_candidate=collections.defaultdict(set)
for mod in manifest['modules']:
 if mod['kind']=='slot_bindings':
  for bid,b in json.loads((a/mod['file']).read_text())['slot_bindings'].items():
   if bid in binding_by_id: raise ValueError('duplicate binding ID '+bid)
   binding_by_id[bid]=(mod['file'],b);bindings_for_candidate[b['candidate_id']].add(bid)
source_rows=set()
for path in sorted(p.glob('agent-sources-*.json')):
 for item in json.loads(path.read_text()):
  rid=item['id']; assert rid in rows, (path,rid); r=rows[rid];source_rows.add(rid)
  for e in item.get('external_evidence',[]):
   if not e.get('url') or not e.get('support_and_limits'): raise ValueError((path,rid,e))
   es=r.setdefault('external_evidence',[])
   if not any(x['url']==e['url'] and x['support_and_limits']==e['support_and_limits'] for x in es): es.append(e)
  st=item.get('external_evidence_status')
  if r['external_evidence_status'] in ('not_yet_reviewed','unresolved_after_review'):
   r['external_evidence_status']=st if item.get('external_evidence') else 'unresolved_after_review'
  detail={k:copy.deepcopy(v) for k,v in item.items() if k not in ('id','external_evidence','external_evidence_status')}
  detail['review_file']=path.name
  if detail:
   ds=r.setdefault('external_review_details',[])
   # Replace a previous merge from this file with the latest source result.
   ds[:]=[x for x in ds if x.get('review_file')!=path.name];ds.append(detail)

# Preserve the search scope and unresolved explanation for rows with no positive lead.
for path in sorted(p.glob('agent-candidates-empty-*.json')):
 doc=json.loads(path.read_text())
 if not isinstance(doc,dict): continue
 for item in doc.get('unresolved_rows',[]):
  rid=item.get('term_id',item.get('id'))
  if rid not in rows: raise ValueError(('unknown_unresolved_row',path.name,rid))
  notes=rows[rid].setdefault('candidate_search_attempts',[])
  notes[:]=[x for x in notes if x.get('review_file')!=path.name]
  notes.append({'review_file':path.name,**copy.deepcopy(item)})

# Replace earlier overly broad wording after the independent source audit.
corrections={
 ('MG-03-010','https://www.nanoha.com/archive/story/story1.html'): '나노하 공식 제1화 줄거리는 레이징 하트가 강한 빛을 내고 나노하가 상상한 마법 지팡이와 자신을 지키는 의복을 형성하는 해당 작품 사례를 설명한다. 빛 입자들이 모여 의상이나 무기로 실체화되는 구체적인 메커니즘은 이 줄거리만으로 확인되지 않는다.',
 ('MG-18-006','https://exhibitions.fitnyc.edu/fashion-unraveled/'): 'FIT 전시의 해당 구체 사례는 독립 재조회 중 시간 초과였다. 같은 전시의 별도 섹션은 닳은 스타일과 올풀림을 설명하지만 특정 드레스 밑단이나 전투·그을림의 원인은 확인하지 못했다.',
 ('MG-05-016','https://patents.google.com/patent/JP2025142259A/en'): '일본 공개 특허는 사진을 촬영한 후 눈의 기존 반사 영역 위에 하트·별 모양 장식 이미지를 더해 캐치라이트처럼 표현하는 후처리 사례를 설명한다. 실제 별·하트 형태의 빛 반사가 촬영되었다는 증거가 아니며 장르의 유일한 제작 방식이나 감정의 증거도 아니다.'
}
for (rid,url),note in corrections.items():
 es=rows[rid].get('external_evidence',[]); found=[x for x in es if x['url']==url]
 if found:
  first=found[0];first['support_and_limits']=note
  rows[rid]['external_evidence']=[x for x in es if x is first or x['url']!=url]

def candidate_inputs(path):
 doc=json.loads(path.read_text())
 if isinstance(doc,list):
  for row in doc:
   for c in row.get('reviewed_candidates',[]):yield row['id'],c
 else:
  for c in doc.get('reviewed',doc.get('reviewed_candidates',[])):
   yield c['term_id'],c

invalid=[];added=0;seen_reviews=set()
for path in sorted(p.glob('agent-candidates-*.json')):
 if 'depth-upgrade' in path.name or '-relevant-depth' in path.name or '-arrow-deep' in path.name: continue
 for rid,c in candidate_inputs(path):
  cid,mod=c['candidate_id'],c['module']; assert rid in rows
  if mod not in module_cache: module_cache[mod]=json.loads((a/mod).read_text())['candidates']
  rec=module_cache[mod][cid]; canon=json.dumps(rec,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode(); h=hashlib.sha256(canon).hexdigest()
  errors=[]
  if c.get('whole_record_sha256')!=h: errors.append('hash')
  if c.get('conditions',{})!=rec.get('conditions',{}): errors.append('conditions')
  if c.get('effects',{})!=rec.get('effects',{}): errors.append('effects')
  for snap in ('original_record','entire_source_record'):
   if snap in c and c[snap]!=rec:errors.append(snap)
  if 'native_content' in c and c['native_content']!=rec.get('content',{}):errors.append('native_content')
  captured_binding_ids={b.get('record',b).get('id') for b in c.get('bindings',[])}
  if captured_binding_ids!=bindings_for_candidate[cid]: errors.append('binding_set_incomplete')
  for b in c.get('bindings',[]):
   br=b.get('record',b); bid=br.get('id')
   if bid not in binding_by_id: errors.append('binding_missing:'+str(bid));continue
   actualmod,actual=binding_by_id[bid]; br={k:v for k,v in br.items() if k!='module'}
   if br!=actual: errors.append('binding_changed:'+str(bid))
   if b.get('module') and b['module']!=actualmod: errors.append('binding_module:'+str(bid))
  if errors: invalid.append({'row':rid,'candidate_id':cid,'file':path.name,'errors':errors});continue
  arr=rows[rid].setdefault('reviewed_candidates',[])
  prev=next((x for x in arr if x['candidate_id']==cid and x['module']==mod),None)
  if prev:
   if prev.get('review_source_file')==path.name:
    for name in ('classification','comparison','conditions','effects','bindings','review_depth','deep_review','full_record_review','deep_review_findings','deep_review_fields','detailed_contract_review'):
     if name in c: prev[name]=copy.deepcopy(c[name])
   if 'review_depth' in c:
    prev.setdefault('review_depth_by_file',{})[path.name]=c['review_depth']
   # Preserve prior decision as well as the full agent review file.
   refs=prev.setdefault('additional_review_files',[])
   if path.name!=prev.get('review_source_file') and path.name not in refs:refs.append(path.name)
  else:
   v={k:copy.deepcopy(val) for k,val in c.items() if k not in ('term_id','original_record','entire_source_record','native_content')}
   v['review_source_file']=path.name
   if 'review_depth' in c: v['review_depth_by_file']={path.name:c['review_depth']}
   arr.append(v);added+=1
  rows[rid]['existing_candidate_status']='limited_review_other_candidates_open'
  seen_reviews.add((rid,mod,cid))
for path in sorted(p.glob('agent-candidates-*.json')):
 if 'depth-upgrade' not in path.name and '-relevant-depth' not in path.name and '-arrow-deep' not in path.name: continue
 doc=json.loads(path.read_text())
 for u in doc.get('upgrades',doc.get('reviewed',[])):
  rid,cid,mod=u['term_id'],u['candidate_id'],u['module']
  matches=[x for x in rows[rid].get('reviewed_candidates',[]) if x['candidate_id']==cid and x['module']==mod]
  if len(matches)!=1:
   invalid.append({'row':rid,'candidate_id':cid,'file':path.name,'errors':['upgrade_without_prior_review']});continue
  sha=u.get('original_sha256',u.get('whole_record_sha256'))
  if sha!=matches[0]['whole_record_sha256']:
   invalid.append({'row':rid,'candidate_id':cid,'file':path.name,'errors':['upgrade_hash_mismatch']});continue
  matches[0].setdefault('review_depth_by_file',{})[path.name]=u['review_depth']
  if u.get('review_note'):
   notes=matches[0].setdefault('depth_review_notes',{})
   notes[path.name]=u['review_note']
  if cid=='cand_85046694df0a5659bf4b6acfdd303962':
   matches[0]['comparison']='사람 조건의 착용자 한쪽 손목에 금색 커프 팔찌가 놓이는 사례다. 원문에 폭의 수치나 넓다는 조건은 없다. 마법 발동 기능도 명시되지 않는다.'
  matches[0].setdefault('additional_review_files',[])
  if path.name not in matches[0]['additional_review_files']:matches[0]['additional_review_files'].append(path.name)

for c in rows['MG-06-019'].get('reviewed_candidates',[]):
 if c['candidate_id']=='cand_7437f298cb7e5b9f89ef06eba19fed68':
  c['bindings']=[copy.deepcopy(binding_by_id[bid][1]) for bid in sorted(bindings_for_candidate[c['candidate_id']])]
for r in rows.values():
 if r['id'] in ('MG-03-011',) and r['external_evidence_status']=='official_search_result_only_direct_page_unavailable': r['external_evidence_status']='search_result_only_direct_page_unavailable'
rows['MG-02-012']['external_evidence_status']='partial_or_example_not_full_definition'
for e in rows['MG-02-012'].get('external_evidence',[]):
 if e['url']=='https://kakuyomu.jp/works/1177354054893145794/episodes/1177354054893855864':
  e['support_and_limits']='작가가 공개한 소설 본문은 변신 가능 시간을 소진하고 변신하지 않는 동안 회복하는 해당 작품의 설정을 기술한다. 본문을 직접 열어 확인했으며 모든 마법소녀의 보편적 시간 제한은 아니다.'
d['external_source_assignment_count']=sum(bool(x.get('external_evidence')) for x in rows.values());d['candidate_comparison_count']=sum(len(x.get('reviewed_candidates',[])) for x in rows.values());d['method_notes'].append('2026-11-07 병렬 검토 결과를 행별로 병합했다. 각 후보의 원본 해시, conditions, effects, 저장된 바인딩 원본이 일치한 경우만 기록하며 추가 데이터에는 리뷰 파일 포인터를 남긴다.') if not any('병렬 검토' in x for x in d['method_notes']) else None
f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
leads={x['term_id']:x for x in map(json.loads,(p/'candidate-discovery-all.jsonl').read_text().splitlines())}
fields=['term_id','source_label','source_definition','external_status','external_sources','candidate_review_status','reviewed_candidate_ids','reviewed_classifications','unreviewed_lexical_match_count','lexical_without_full_record_review','full_record_comparisons','core_only_comparisons','review_depth_unreported']
with (p/'review-progress.csv').open('w',encoding='utf-8',newline='') as o:
 w=csv.DictWriter(o,fieldnames=fields);w.writeheader()
 for r in d['rows']:
  cs=r.get('reviewed_candidates',[]); done={(c['module'],c['candidate_id']) for c in cs};remaining=sum((h['module'],h['candidate_id']) not in done for h in leads[r['id']]['hits'])
  def depth(c):
   values=set(c.get('review_depth_by_file',{}).values())
   if c.get('review_depth'): values.add(c['review_depth'])
   return 'full_record' if 'full_record' in values else ('core_proposition_only' if 'core_proposition_only' in values else 'not_reported')
  cm={(c['module'],c['candidate_id']):c for c in cs}
  full_pending=sum((h['module'],h['candidate_id']) not in cm or depth(cm[(h['module'],h['candidate_id'])])!='full_record' for h in leads[r['id']]['hits'])
  ndepth=collections.Counter(depth(c) for c in cs)
  w.writerow({'term_id':r['id'],'source_label':r['source_cells'][0],'source_definition':r['source_cells'][1] if len(r['source_cells'])>1 else '', 'external_status':r['external_evidence_status'],'external_sources':' | '.join(dict.fromkeys(e['url'] for e in r.get('external_evidence',[]))),'candidate_review_status':r['existing_candidate_status'],'reviewed_candidate_ids':' | '.join(c['candidate_id'] for c in cs),'reviewed_classifications':' | '.join(c['classification'] for c in cs),'unreviewed_lexical_match_count':remaining,'lexical_without_full_record_review':full_pending,'full_record_comparisons':ndepth['full_record'],'core_only_comparisons':ndepth['core_proposition_only'],'review_depth_unreported':ndepth['not_reported']})
for row in d['rows']:
 for c in row.get('reviewed_candidates',[]):
  if 'additional_review_files' in c:
   c['additional_review_files']=[x for x in dict.fromkeys(c['additional_review_files']) if x!=c.get('review_source_file')]
# Save normalized references, including older merge versions that repeated the same file.
f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
depth_counts=collections.Counter()
for row in d['rows']:
 for c in row.get('reviewed_candidates',[]):
  depths=set(c.get('review_depth_by_file',{}).values())
  if c.get('review_depth'): depths.add(c['review_depth'])
  depth_counts['full_record' if 'full_record' in depths else ('core_proposition_only' if 'core_proposition_only' in depths else 'not_reported')]+=1
report={'review_depth_counts':dict(depth_counts),'source_rows_in_agent_files':len(source_rows),'source_assignment_count':d['external_source_assignment_count'],'source_statuses':dict(collections.Counter(x['external_evidence_status'] for x in d['rows'])),'candidate_comparisons':d['candidate_comparison_count'],'candidate_rows':sum(bool(x.get('reviewed_candidates')) for x in d['rows']),'new_candidate_comparisons_added_this_run':added,'invalid_candidate_reviews':invalid}
(p/'audit-merge-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
progress=list(csv.DictReader((p/'review-progress.csv').open()))
remaining=sum(int(x['unreviewed_lexical_match_count']) for x in progress)
not_full=sum(int(x['lexical_without_full_record_review']) for x in progress)
status='''# 검토 현황 스냅샷\n\n이 문서는 `merge-research-audits.py`로 산출한 현재 기록의 집계다. 사용자 지시에 따라 이미 세 번 검토한 원문 항목과 동일 행–후보는 다시 검토하지 않는다. 기존 작업에 모든 반복 횟수가 기록되어 있지는 않으므로 정확한 전 기간 횟수를 사후 복원했다고 주장하지 않는다.\n\n- 원문 301행 중 관련 출처가 하나라도 연결된 행: {source}/301. 단, 대부분은 하위 명제·특정 작품·유비의 부분 근거이고 직접 페이지를 못 연 출처도 있다.\n- 사진 후보의 행–후보 비교: {total}건, {rowcount}행. 전체 중첩 계약까지 직접 해석한 `full_record` {full}건, 핵심 명제 위주 `core_proposition_only` {core}건, 검토 깊이를 명시하지 못한 이전 기록 {unknown}건. 원본 복사와 해시는 전체 의미 검토가 아니다.\n- 기존 표제 문자열 검색 11,134건 중 아직 핵심 명제조차 대조하지 않은 단서: {remaining}건. 이 중 다의어·낱말 내부 일치가 많다. 전체 계약 검토가 없는 단서: {not_full}건. 반면 검색에 누락된 의미상 후보는 이 수에 포함되지 않는다.\n- `agent-illustration-audit.md`, `agent-illustration-comparisons.md`와 일러스트 별도 JSON은 사진과 별도 범위다. 일러스트 301행에 연결한 일반 가드·정체성 앵커를 해당 의미 구현이나 전수 의미 검토로 계산하지 않는다.\n- `agent-source-quality-audit.md`는 각 행의 첫 기재 출처에 대한 독립 감사 상태 301행을 기록한다. 이 감사자의 상태는 직접 확인 198행·부분 확인 19행·직접 재확인 불가 또는 검색 발췌 84행이다. 재확인 불가는 자료가 틀렸다는 뜻이 아니며 다른 조사자가 과거 본문을 확인했을 수 있다. 각 행의 모든 출처·하위 명제를 검증했다는 뜻도 아니다. 이전 세 번 제한과 접근 불가를 지킨다.\n- 전체 후보 의미·조건 검증, 검색/런타임 노출, 픽셀 품질은 아직 완성으로 표시할 수 없다. 현재 실행 데이터와 인덱스를 수정하지 않았다.\n\n각 행은 [review-progress.csv](review-progress.csv), 근거·한계·개별 후보는 [source-reconciliation.json](source-reconciliation.json), 원본 자산·명령·수용 기준은 [구현 계획](agent-implementation-plan.md)에 있다. `agent-candidates-*`에는 개별 원본과 검토 사항이, `candidate-corpus-audit-index.jsonl.gz`에는 28,026개 후보의 해시·조건·효과·바인딩 포인터가 있다. 색인은 검토 결과가 아니다.\n'''.format(source=report['source_assignment_count'],total=report['candidate_comparisons'],rowcount=report['candidate_rows'],full=depth_counts['full_record'],core=depth_counts['core_proposition_only'],unknown=depth_counts['not_reported'],remaining=remaining,not_full=not_full)
(p/'research-progress.md').write_text(status)
print(json.dumps(report,ensure_ascii=False,indent=2))
