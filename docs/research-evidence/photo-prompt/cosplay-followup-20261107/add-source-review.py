from pathlib import Path
import hashlib,json,sys
R=Path('/Users/chasoik/Projects/image-prompt'); A=R/'skills/photo-prompt-image-generator/assets'; D=R/'skills/photo-prompt-image-generator/references/cosplay-followup-20261107.md'
load=lambda p:json.loads(p.read_text()); save=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n'); sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
reviews={
'COS-T1-013':('https://www.cosplayreal.com/blogs/anime-exhibition/closet-cosplay-guide-everyday-clothes-tiktok-trends-2026','판매자의 가이드는 일상복을 조합하는 사례를 설명한다. 이미 소유했는지와 원 캐릭터와의 대응은 사진 한 장으로 입증할 수 없다.'),
'COS-T1-014':('https://keele-repository.worktribe.com/preview/465466/SkentelberyPhD2023.pdf','학위 연구는 캐릭터를 환기하는 일상복으로 설명한다. 옷의 기존 소유 여부를 필수 조건으로 추가하지 않는다.'),
'COS-T1-018':('https://www.tc.columbia.edu/digitalfuturesinstitute/media/pop-and-play/episodes/season-four/episode-6-cosplay/','코스플레이 참가자의 인터뷰는 비인간을 사람형 캐릭터로 해석하는 사례를 설명한다. 귀 장식만으로 원 대상 및 대응 관계는 검증되지 않는다.'),
'COS-T3-019':('https://www.getty.edu/vow/AATFullDisplay?find=tow&logic=AND&note=&subjectid=300210567','Getty AAT는 상체 부분과 팬티가 연결된 한 벌의 속옷으로 구분한다. 동명의 플리스 소재나 모자는 같은 근거가 아니다.'),
'COS-T8-2-011':('https://www.maybelline.com.au/makeup-tips/lips/how-to-overline-lips','브랜드 메이크업 가이드는 실제 입술선 바깥에 라인을 그리는 기법을 제시한다. 입술과 외곽 관계가 숨겨지면 이미지에서 확인 불가다.'),
'COS-T11-2-012':('https://www.mehron.com/mehron-blog/special-effects-zombie-halloween-makeups-trending-this-halloween/','브랜드 튜토리얼은 얼굴 페인트 또는 돌출된 표면을 이용한 각기 다른 좀비 분장 사례를 제시한다. 특정 재료를 결과 사진에서 추론하지 않는다.'),
'COS-T12-011':('https://andi-bagus.com/products/best-mate-micro-bikini','제작자의 특정 상품은 작은 크기와 적은 커버리지를 명시한다. 상품 한 사례를 보편적 고정 치수나 특정 착용자 특성으로 확장하지 않는다.')}
with D.open('a') as f:
 f.write('\n## 추가 용어별 직접 출처와 판단 범위\n\n')
 for tid,(url,note) in reviews.items(): f.write(f'- {tid}: {note} {url}\n')
refsha=sha(D); cf=A/'photo_candidate_cosplay_followup_20261107.json'; c=load(cf)
for record in c['candidates'].values():
 for source in record['provenance']: source['sha256']=refsha
save(cf,c)
config=load(R/'skills/photo-prompt-image-generator/retrieval-runtime.json'); sys.path.insert(0,str(Path.home()/'.cache/image-prompt/photo-shared-runtime/h-f2-installed/generations'/config['native_generation_id']/'scripts')); import photo_candidate_retrieval_views as rv
vf=A/'photo_candidate_retrieval_views_cosplay_followup_20261107.json'; views=load(vf)
views['coverage']['source_module_sha256']=sha(cf)
for v in views['views']:v['source_record_sha256']=rv.digest(c['candidates'][v['candidate_id']])
rv.validate(views,c['candidates']); save(vf,views)
sf=A/'photo_cosplay_followup_semantics_20261107.json'; reg=load(sf);reg['sources_reference_sha256']=refsha
for row in reg['term_reviews']:
 if row['term_id'] in reviews:
  url,note=reviews[row['term_id']];row['direct_external_sources'].append(url);row['followup_evidence_note_ko']=note;row['external_source_scope']='The cited source supports the stated example or boundary only; it does not establish every visual realization or the hidden history.'
save(sf,reg)
xf=A/'photo_cosplay_followup_context_views_20261107.json';x=load(xf);x['source_registry_sha256']=sha(sf)
for i,v in enumerate(x['views']):
 row=reg['term_reviews'][i]
 if row['term_id'] in reviews:
  v['external_sources']=row['direct_external_sources'];v['followup_evidence_note_ko']=row['followup_evidence_note_ko'];v['source_quotes'].append({'pointer':f'/term_reviews/{i}/followup_evidence_note_ko','quote':row['followup_evidence_note_ko']})
save(xf,x)
print('updated',len(reviews),'source-supported terms; source-backed total',sum(bool(r['direct_external_sources']) for r in reg['term_reviews']))
