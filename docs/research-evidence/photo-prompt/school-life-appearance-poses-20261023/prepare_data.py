"""Assemble explicitly authored proposals; no semantic inference or native approval."""
from pathlib import Path
import csv,json,hashlib,collections
Q=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
source_rows=[
('S01','National Portrait Gallery portrait learning resource','https://www.npg.org.uk/schools-hub/how-to-create-a-photographic-portrait','Pose, gaze, expression, clothing, props and composition are separate photographic choices. Interpretation is not independent verification of inner state.'),
('S02','FIT Uniformity','https://exhibitions.fitnyc.edu/uniformity/','Exhibited school-uniform combinations and sailor-derived collar context; historical examples, not universal present regulations.'),
('S03','FIT Ivy Style','https://sites.fitnyc.edu/depts/museum/Ivy_Style/default.htm','Campus fashion combinations; style category does not establish actual background.'),
('S04','Getty AAT knife pleats','https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=clay&page=1&subjectid=300228444','Same-direction pressed folds; width labels vary across vocabularies.'),
('S05','Getty AAT box pleats','https://www.getty.edu/vow/AATFullDisplay?find=&logic=&note=&subjectid=300228368','Double folds under each side with outward flat face.'),
('S06','Getty AAT inverted pleats','https://www.getty.edu/vow/AATFullDisplay?find=buffet&logic=AND&note=&subjectid=300228436','Flat fold turns inward, distinguished from outward box pleat.'),
('S07','Scottish Register of Tartans FAQ','https://www.tartanregister.gov.uk/FAQ','Repeated stripe arrangement, pattern versus fiber and heritage boundaries.'),
('S08','LOreal Paris Dutch braid tutorial','https://www.lorealparisusa.com/beauty-magazine/hair-style/braid-hairstyles/how-to-dutch-braid-hair','Dutch under-crossing versus French over-crossing; process is not proved by one still.'),
('S09','Hair.com hime cut explanation','https://www.hair.com/hime-cut.html','Length levels of long back, blunt side sections and fringe; no royal-history claim adopted.'),
('S10','LOreal Paris lob haircuts','https://www.lorealparisusa.com/beauty-magazine/hair-style/medium-hairstyles/lob-haircuts','Long-bob length and face-framing variations; geometry in cards is authored.'),
('S11','National Galleries of Scotland contrapposto','https://www.nationalgalleries.org/art-and-artists/glossary-terms/contrapposto','One-leg weight, relaxed opposite leg and balancing torso.'),
('S12','Adobe sitting poses and hand poses','https://www.adobe.com/creativecloud/photography/discover/sitting-poses-and-hand-poses.html','Support, prop handling and perspective planning; exact multi-owner scene geometry is authored.'),
('S13','Adobe over-the-shoulder shot','https://www.adobe.com/in/creativecloud/video/production/cinematography/camera-shots-and-angles/over-the-shoulder-shot.html','Foreground shoulder or head and person beyond; distinct from looking-back pose.'),
('S14','Shueisha Imidas kabedon','https://imidas.jp/ryuko/detail/N-101-2151.html','Wall-banging noise sense and staged wall gesture sense; no automatic consent or romance claim.'),
('S15','Yayoi Museum school uniform exhibition archive','https://www.yayoi-yumeji-museum.jp/yayoi/exhibition/past_detail.html?id=2720','Historical modified-uniform and loose-sock contexts; association does not verify individual behavior.'),
('S16','Academy of Korean Studies gyoryeonbok','https://encykorea.aks.ac.kr/Article/E0079847','Historical Korean training-course clothing; not a present generic uniform.'),
('S17','GH Bass penny loafers','https://www.ghbass.com/collections/mens-penny-loafers','Manufacturer examples of slip-on upper and cutout saddle; marketing and pricing not adopted.'),
('S18','Clarks Mary Jane and T-bar school shoes','https://clarks.com.au/collections/school-girls-mary-jane-t-bar','Manufacturer distinction between transverse strap and added central strap.'),
('S19','Shogakukan Digital Daijisen moesode via Kotobank','https://kotobank.jp/word/%E8%90%8C%E3%81%88%E8%A2%96-2627057','Sleeve covering part of hand; affective etymology is not an age or personality inference.'),
('S20','CELSYS Art Rocket anime eyes','https://www.clipstudio.net/how-to-draw/archives/162395','Illustrated eye construction and stylization; individual cartoon symbols are authored proposals, not literal anatomy.'),
('S21','PSSCIVE Assistant Fashion Designer Class 11','https://psscive.ac.in/storage/uploads/textbooks/pdf/english/assistant-fashion-designer-english-class-11.pdf','Locally downloaded primary textbook verified for weave, pleats, garment parts and plackets. It does not independently verify every proposed school outfit.'),
('S22','Brooks Brothers brand press release','https://corporate.authentic.com/press-releases/brooks-brothers-125th-anniversary-iconic-button-down-collar-shirt','Button-down collar and Oxford-cloth combination; corporate superlatives and historical priority claims not adopted.'),
('S23','Crockett and Jones Oxford guide','https://www.crockettandjones.com/blogs/the-article/definitive-guide-the-english-oxford','Oxford closed lacing below vamp versus Derby above-vamp open construction; no dress-code prescription.'),
('S24','Oxford Learners Dictionaries jumper','https://www.oxfordlearnersdictionaries.com/definition/english/jumper','British sweater and North American sleeveless dress senses.'),
('S25','Adobe Dutch angle shot','https://www.adobe.com/creativecloud/video/production/cinematography/camera-shots-and-angles/dutch-angle-shot.html','Camera rotation tilts architectural or horizon lines; does not imply body lean.')]
sources=[dict(zip(['id','title','url','claim_scope'],r),accessed='2026-10-23',status='primary_publisher_read',whole_scene_geometry='authored proposal, not source quotation') for r in source_rows]
write(Q/'sources.json',{'sources':sources,'source_policy':'Publisher context and limited distinctions; no source proves a complete authored scene. No copied passages.'})
visual=list(csv.DictReader((Q/'visual-authored.tsv').open(),delimiter='\t'))
assert len(visual)==140 and len({r['id'] for r in visual})==140
contexts=list(csv.DictReader((Q/'contexts-authored.tsv').open(),delimiter='\t'))
for r in contexts:
 if r['id']=='N04':r['sources']='S24'
 if r['id']=='N27':r['sources']='S25'
slots={1:['wardrobe_style','wardrobe_layering'],2:['garment_detail'],3:['garment_detail','silhouette_proportion'],4:['surface_pattern','texture'],5:['wardrobe_style','wardrobe_layering'],6:['wearable_accessory'],7:['hair_style'],8:['wearable_accessory'],9:['wardrobe_style'],10:['body_pose'],11:['body_pose','contact_point'],12:['relational_action','contact_point'],13:['body_pose','contact_point'],14:['expression'],15:['garment_state'],16:['composition']}
confusions={1:'garment construction versus person age or actual enrollment',2:'whole garment versus collar, opening or attached part',3:'outline versus fold construction versus leg tubes',4:'pattern versus weave versus unverified fiber composition',5:'outfit function versus demonstrated activity or identity',6:'strap and upper construction versus generic shoe/bag name',7:'cut, length, part, tie points, crossing and current state are independent',8:'surface or accessory versus diagnosis, age or personality',9:'visible combination versus inferred cultural identity or character',10:'weight, support, rotation, target and camera axes are independent',11:'hand owner, contact and support must all remain visible',12:'two participants and both relation endpoints; no inferred consent or emotion',13:'static stance versus event outcome, intention, speed or injury cause',14:'facial geometry or drawn sign versus inner state or literal anatomy',15:'wearing state versus cut, cause, chronology or medical proof',16:'camera framing and rotation versus body posture'}
cards=[]
for r in visual:
 sec=int(r['section']);ss=r['sources'].split(',')
 if r['id']=='C04':ss=['S25']
 if r['id']=='U06':ss=['S24','S21']
 chosen=slots[sec]
 if r['id'].startswith('B0') and int(r['id'][1:])<=5:chosen=['footwear']
 if r['id']=='I02':chosen=['wearable_accessory','contact_point']
 if r['id'] in {'I03','I05'}:chosen=['skin_condition']
 if r['id']=='I04':chosen=['lip_finish','lip_color_placement']
 if r['id']=='I06':chosen=['garment_fit']
 if r['id']=='Q03':chosen=['body_orientation','gaze_target']
 if r['id']=='Q06':chosen=['camera_height']
 if r['id']=='R01':chosen=['gaze_target','proxemics']
 cards.append({'id':r['id'],'name_ko':r['name_ko'],'section':sec,'mode':'visible','priority':'P0','source_ids':ss,'suggested_slots':chosen,'evidence_status':'authored_optional_realization_with_limited_publisher_context','positive_en':r['en'],'positive_ko':r['ko'],'observable_components':[{'id':r['id']+'.'+str(i+1),'requirement_ko':s,'visibility_gate':'UNOBSERVABLE_NOT_PASS'} for i,s in enumerate(r['components'].split(';'))],'owner_relation_contract':{'complete_proposition_en':r['en'],'complete_proposition_ko':r['ko'],'owner_rule':'Every stated limb, garment, prop and target retains its stated owner and count; no endpoint transfer.','hidden_contact':'not observable, never assumed'},'confusion_boundary':confusions[sec],'pixel_gate':'All distinguishing components and both endpoints jointly observable; partial_is_fail.','scope':'optional depiction, not person classification','native_approval':False})
for r in contexts:
 cards.append({'id':r['id'],'name_ko':r['name_ko'],'mode':'context_diagnostic','priority':'P0','source_ids':r['sources'].split(','),'suggested_slots':[],'handling':r['handling'],'proof_limits':r['limits'].split(';'),'query_en':r['query_en'],'native_approval':False,'pixel_gate':'Context does not create positive visual qualification.'})
write(Q/'semantic-cards.json',{'schema':'school-life-appearance-pose-semantic-cards/v1','cards':cards,'native_approval':False})
write(Q/'candidate-drafts.json',{'drafts':[{'card_id':r['id'],'prompt_fragment_en':r['en'],'prompt_fragment_ko':r['ko']} for r in visual]})
write(Q/'contexts-development.json',{'rows':contexts})
# Manual component routes, in source-row order. A route is not an alias or an equivalence.
mapping={
1:'U01|U02|~|U01|U03|U04|U05|U06|U07|U08|U02|X02,U09|U11|U12|U10,U12',
2:'D01|D02|U08|D03|D04|U04|U03|D05|D06|D07|D08|D09,D10|D11|D12|D12,U03|D13|~|D14',
3:'P01,P02,P03|P01|P02|P03|P04|P04|P05|~|P06,P07|P05|P05,M07|P08|~',
4:'M01|M01|M02|M03|M04|M05,M06|M07|M10|M08|~|M09|~',
5:'X07|X06|X06|X05|X03|X01|X04|X10,X12|X08|X08|~|~|X09|X10,U09|X11|X11|~|V03,P08|X11',
6:'B01|B02,B03|B04,B05|~|B10|B06|B06|B07|~|B08|~|~|B09|B09|~',
7:'H01,H02|~|H01|H02|H05|H05|H04|H04|H06|H07|H11|H09,H10|H08|H08|~|H03|~|H13|H13|~|H14|H02,H03|~|H12|H06,H07',
8:'I01|I01|~|~|I03|~|~|V02|I04|~|I06|H14',
9:'U01|V01|V01|X05|~|X07|V02|V02|V03|V03|~',
10:'Q01,Q05|C01|C01|Q01|Q02|Q01|Q03|R01|R01|~',
11:'A01|A02|A03,Q03|A04|A03|R07|Q03|A05|A05|I02|~|A06|Q02|Q03|Q02|A08',
12:'R07|~|R01|~|R02|~|~|~|R05|R10|R06|R08|~|~|~|R09|~|~',
13:'F02|F01|F01|~|Q05|F03|F03|F04|A05|~|F05|Q05|~|F06|F05',
14:'~|E01|E01|E01|~|~|~|E02|E02|E04|I04|E03|E03|E03|~|H14',
15:'I06|U01|T02|T01|T03|T04|F04|~|T05|T07|T07|T06|T08|~|~',
16:'C02,C05,C06|Q06|C03|R01,R08|C04|C06|R01|V04'}
extra={1:['N01','N02','N03','N04'],2:['N02','N05'],3:['N06','N07'],4:['N08','N09'],5:['N02','N10'],6:['N09','N01'],7:['N11'],8:['N01','N12','N24'],9:['N10','N12'],10:['N13','N14','N25'],11:['N14','N15'],12:['N15','N16','N17','N18'],13:['N19','N20','N21'],14:['N23','N24'],15:['N03','N21','N22'],16:['N25','N26','N27']}
terms=read(Q/'additional-terms.json')['terms'];routes=[];valid={r['id'] for r in cards}
for sec,line in mapping.items():
 rows=[r for r in terms if r['section']==sec];parts=line.split('|');assert len(parts)==len(rows),(sec,len(parts),len(rows))
 for r,part in zip(rows,parts):
  ids=[] if part=='~' else part.split(',');assert all(i in valid for i in ids)
  routes.append({'keyword_id':r['id'],'term':r['term'],'seed_description':r['description'],'seed_status':'untrusted vocabulary seed retained for review, not verified claim','optional_visual_card_ids':ids,'context_card_ids':extra[sec]+['N28'],'route_type':'authored_component_alternative_not_equivalence' if ids else 'context_only_no_new_positive_candidate','coverage_limit':'Compound alternatives and all variants are not implied by this route. Inspect complete source; no term-level alias broadening.','native_approval':False})
assert len(routes)==238
write(Q/'keyword-routes.json',{'routes':routes,'counts':dict(collections.Counter(r['route_type'] for r in routes)),'combination_examples':{'rows':read(Q/'additional-terms.json')['combination_examples'],'status':'advisory composites, not requester locks or automatically combined candidates'}})
print(json.dumps({'cards':len(cards),'visual':len(visual),'diagnostic':len(contexts),'routes':len(routes),'route_counts':dict(collections.Counter(r['route_type'] for r in routes))},ensure_ascii=False))
if __name__=='__main__':pass
