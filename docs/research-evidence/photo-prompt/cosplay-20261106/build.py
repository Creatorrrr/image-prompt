from pathlib import Path
import hashlib,json,sys,uuid
R=Path('/Users/chasoik/Projects/image-prompt'); A=R/'skills/photo-prompt-image-generator/assets';O=Path(__file__).parent
config=json.loads((R/'skills/photo-prompt-image-generator/retrieval-runtime.json').read_text())
N=Path.home()/'.cache/image-prompt/photo-shared-runtime/h-f2-installed/generations'/config['native_generation_id'];sys.path.insert(0,str(N/'scripts'))
import photo_candidate_retrieval_views as rv
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
plan=R/'docs/research/cosplay-visual-semantics-research-plan-20261106.md';planhash=sha(plan)
rows=[line.split('\t') for line in (O/'visual-options.tsv').read_text().splitlines() if line.strip()]
assert all(len(r)==6 for r in rows)
diags=[
('D01','바디수트와 캣수트','Bodysuit, catsuit, unitard and zentai differ in garment continuity and coverage; face, hand and foot coverage require their own evidence.','바디수트·캣수트·유니타드·젠타이는 의복의 연결과 덮는 범위가 다르며 얼굴·손·발 덮임은 별도의 근거가 필요하다.'),
('D02','가터와 가터벨트','A thigh garter is a band; a garter belt connects a waist belt and stocking tops with separate straps.','허벅지 가터는 띠이며 가터벨트는 허리 벨트와 스타킹 윗단을 별도 끈으로 연결한다.'),
('D03','패션과 코스프레','Lolita fashion is a fashion culture; recreating a character wearing that fashion can also be cosplay.','로리타 패션은 패션 문화이며 그 옷을 입은 캐릭터를 재현하면 코스프레와 겹칠 수 있다.'),
('D04','크로스플레이와 젠더벤드','Crossplay concerns the performer and character relationship; genderbend concerns reinterpretation of character gender or presentation.','크로스플레이는 연기자와 캐릭터의 관계에, 젠더벤드는 캐릭터의 성별이나 표현의 재해석에 관한 말이다.'),
('D05','레이스의 여러 의미','Lace fabric, lace-up fastening and lace-front wig construction are different concepts.','레이스 원단, 레이스업 끈 여밈, 레이스 프런트 가발 구조는 서로 다른 개념이다.'),
('D06','재료와 외형','A glossy surface alone does not establish whether an outfit is latex, PVC, satin or another material.','광택이 보인다는 사실만으로 의상이 라텍스·PVC·새틴 또는 다른 재질이라고 확정하지 않는다.'),
('D07','가발 기술과 결과','Wig ventilation, wefts, teasing and crimping describe construction or process; observable hair shape is a separate property.','가발 식모·웨프트·백코밍·크림핑은 구조나 과정이며 보이는 헤어 형태는 별도 속성이다.'),
('D08','상처와 의상 손상','Skin injury effects, torn clothing, stains and the cause of a depicted event are separate observations.','피부 상처 분장, 찢어진 의복, 얼룩과 묘사된 사건의 원인은 서로 다른 관찰이다.'),
('D09','인물 신체와 착용 파츠','Costume ears, masks, prosthetics and a character’s anatomy are distinct; hidden attachment edges are unobserved.','귀 착용품·가면·프로스테틱과 캐릭터의 신체는 구별하며 보이지 않는 부착 경계는 미관찰이다.'),
('D10','촬영 시점과 자세','Framing, camera height, subject pose and lighting are independent properties.','프레이밍, 카메라 높이, 인물 자세와 조명은 서로 독립적인 속성이다.'),
('D11','나이와 의도','Clothing, styling or an adult product label alone does not establish a person’s age, sexual intent or consent.','의복·스타일이나 성인 상품 표지만으로 사람의 나이·성적 의도·동의를 확정하지 않는다.'),
('D12','판타지 성격과 외형','A villain, demon or angel role does not require a fixed color, pose, outfit or facial expression.','빌런·악마·천사 역할이 특정 색·자세·의상·표정을 필수로 만들지는 않는다.'),
('D13','촬영 포즈와 실제 기술','A staged weapon pose does not establish a real martial technique, attack or historical combat practice.','촬영용 무기 포즈는 실제 무술 기술, 공격 또는 역사적 전투 관행을 입증하지 않는다.'),
('D14','캐넌과 창작 버전','Canon, alternate universe, fan art and original design describe source relationships rather than a single visible costume.','캐넌·대체 세계관·팬아트·오리지널 디자인은 단일 외형이 아니라 원작과의 관계를 뜻한다.'),
('D15','후반 효과와 원인','Compositing, visual effects and cel-shaded appearance describe different processes or looks and need independent evidence.','합성, 시각 효과, 셀 셰이딩 외형은 서로 다른 과정 또는 외관으로 별도 근거가 필요하다.'),
]
ns=uuid.UUID('a14f7d7a-0552-43ac-930c-2de3086b4158')
ident=lambda prefix,s:prefix+uuid.uuid5(ns,s).hex
contract='Apply only as a complete optional visual realization to independently identified owners and permitted changes. Preserve each stated owner, object, garment, count, contact and spatial relation. No age, identity, intent, consent, material composition, cause or event history follows solely from appearance. Research metadata and search views grant no native qualification or effect permission. Hidden required parts are unobservable, not a pass.'
candidates={};bindings={};cards=[]
for code,name,alias,slot,en,ko in rows:
 cid=ident('cand_',code)
 card={'id':code,'name_ko':name,'candidate_id':cid,'positive_en':en,'positive_ko':ko,'suggested_slot':slot,'source':'cosplay-visual-semantics-research-plan-20261106.md','source_evidence_scope':'Named domain and boundaries researched in the plan; this particular complete proposition is independently authored, not a universal definition.','observable_gate':en+' All stated parts and endpoints must be visible; hidden parts are unobservable.','confusion_boundary':'Context is not proof of identity, age, intent, material composition or cause.','native_approval':False,'pixel_status':'NOT_RUN'}
 dims={'contact_point':['appearance','pose','action','relationship','count'],'body_pose':['pose','relationship'],'hand_pose':['pose','relationship'],'expression':['expression'],'object_structure':['appearance'],'lighting':['lighting']}.get(slot,['appearance'])
 rec={'id':cid,'record_kind':'visual_option','content':{'en':en,'ko':ko,'definition':'Complete optional cosplay visual realization: '+en,'aliases':[name,alias],'application_contract':contract,'research_semantics':card},'conditions':{},'effects':{'dimensions':dims,'properties':[]},'provenance':[{'source':'authored-research:photo-prompt/cosplay-20261106/'+code,'sha256':planhash}]}
 candidates[cid]=rec;bid=ident('bind_',code+':'+slot);bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional','semantic_role':'direct','conditions':{'subject_applicability':{}},'weight':1.0};cards.append(card)
for code,name,en,ko in diags:
 cid=ident('cand_',code);card={'id':code,'name_ko':name,'candidate_id':cid,'mode':'context_only','context_en':en,'context_ko':ko,'native_approval':False,'pixel_status':'NOT_RUN'}
 candidates[cid]={'id':cid,'record_kind':'diagnostic','content':{'en':en,'ko':ko,'definition':'Context and evidence boundary only; excluded from positive image material retrieval. '+en,'aliases':[name],'application_contract':'Context and proof limits only. No positive still-image prescription, native authority or automatic selection.','research_semantics':card},'conditions':{},'effects':{'dimensions':[],'properties':[]},'provenance':[{'source':'authored-research:photo-prompt/cosplay-20261106/'+code,'sha256':planhash}]};cards.append(card)
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
cf=A/'photo_candidate_cosplay_20261106.json';bf=A/'photo_candidate_cosplay_bindings_20261106.json';sf=A/'photo_cosplay_semantics_20261106.json';vf=A/'photo_candidate_retrieval_views_cosplay_20261106.json'
assert not any(p.exists() for p in (cf,bf,sf,vf))
save(cf,{'schema':'photo-candidate-module/v3','candidates':candidates});save(bf,{'schema':'photo-candidate-slot-bindings/v3','slot_bindings':bindings});save(sf,{'schema':'photo-cosplay-semantic-registry/v1','cards':cards,'native_approval':False,'pixel_qualification':'NOT_RUN','research_plan_sha256':planhash,'coverage_note':'Selected examples across the topic; not an exhaustive per-keyword implementation. Existing candidates and concepts still require full semantic deduplication.'})
views=[]
for cid,rec in sorted(candidates.items()):
 if rec['record_kind']!='visual_option':continue
 en=rec['content']['en'];ko=rec['content']['ko'];rh=rv.digest(rec)
 for kind in ['whole','context']:
  key=cid+':base:'+kind;ctx=kind=='context';prefix='Complete optional cosplay visual realization: '
  views.append({'id':rv.view_id(cid,'base',key),'candidate_id':cid,'realization_id':'base','key':key,'kind':kind,'source_record_sha256':rh,'text_en':('Cosplay visual option: ' if ctx else '')+en,'text_ko':('코스프레 시각 선택지: ' if ctx else '')+ko,'source_quotes':([{'pointer':'/content/definition','quote':prefix}] if ctx else [])+[{'pointer':'/content/en','quote':en},{'pointer':'/content/ko','quote':ko}],'context_ko':'원본에서 명시한 코스프레 맥락과 한영 명제만 보존한다.' if ctx else '원본 한영 전체 문장을 보존한다.','difference_ko':'코스프레 맥락의 전체 명제' if ctx else '한영 전체 의미 뷰','native_approval':False})
module={'schema':rv.SCHEMA,'recipe':rv.RECIPE,'source_inventory_id':'cosplay-20261106','coverage':{'positive_realizations':len(rows),'diagnostics_excluded':len(diags),'source_module_sha256':sha(cf),'context_views':len(rows)},'native_approval':False,'views':views};rv.validate(module,candidates);save(vf,module)
manifest=A/'photo_candidate_corpus_manifest.json';m=json.loads(manifest.read_text());assert not any(x['file'] in (cf.name,bf.name) for x in m['modules']);m['modules'] += [{'file':cf.name,'kind':'candidates'},{'file':bf.name,'kind':'slot_bindings'}];save(manifest,m)
print(json.dumps({'positive':len(rows),'diagnostics':len(diags),'bindings':len(bindings),'views':len(views),'source_sha256':sha(cf)}))
