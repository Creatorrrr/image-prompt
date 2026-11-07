import json,hashlib
from pathlib import Path
R=Path('/Users/chasoik/Projects/image-prompt');A=R/'skills/photo-prompt-image-generator/assets';prior=A/'photo_nurse_uniform_external_review_20261107.json';p=json.loads(prior.read_text());old={x['source_row_id']:x for x in p['rows']};s1=A/'photo_nurse_uniform_external_source_supplement_20261107.json';covered={x['source_row_id'] for x in json.loads(s1.read_text())['rows']};a={}
def add(ids,url,name,scope):
 for n in ids:
  rid='NURSE-ROW-%03d'%n;assert rid in old and not old[rid]['new_external_sources'] and rid not in covered;a.setdefault(rid,[]).append({'url':url,'source':name,'supported_scope_ko':scope,'evidence_level':'partial'})
add([152],'https://alledascrubs.com/products/women-ultraflex-4-way-stretch-8-pocket-v-neck-scrub-set-pastel-pink','Alleda 파스텔 핑크 스크럽','한 제품의 파스텔 핑크 스크럽 상하의 사례다. 색상 표현은 조명과 표시 장치에 따라 달라진다.')
add([162],'https://www.ideastage.com/OvertheKnee-Socks-Custom-536714028','IdeaStage 오버니 양말','무릎 위까지 오는 양말 상품 범주의 사례다. 상단 길이와 착용자의 실제 활동은 따로 관찰한다.')
add([173],'https://www.nike.com/ca/a/best-work-sneakers/','Nike 작업용 스니커즈 구매 가이드','작업용 운동화라는 판매 범주를 기술한다. 의료용 안전 적합성이나 발의 편안함을 사진에서 판정하지 않는다.')
add([191],'https://www.hse.ie/eng/services/publications/hospitals/nho-code-of-practice-for-healthcare-records-management-version-2-0.pdf','아일랜드 HSE 의료기록 관리 지침','의료기록 차트와 종이 문서를 보관하는 실제 폴더의 사례다. 표지에 드러나지 않은 내용이나 환자 정보는 추론하지 않는다.')
add([322],'https://www.hse.ie/eng/services/publications/hospitals/nho-code-of-practice-for-healthcare-records-management-version-2-0.pdf','아일랜드 HSE 의료기록 관리 지침','의료기록 차트 폴더의 부분 요소를 보여 준다. 이 출처는 가슴 앞에서 안는 특정 포즈를 입증하지 않는다.')
add([256],'https://yomorio.com/products/feisty-nurse-cosplay-costume-cyberpunk-pu-leather-dress-outfit-latex-rave-outfits','YOMORIO 사이버풍 간호 코스튬','사이버풍 간호 코스튬이라고 이름 붙인 특정 상품이다. 의료복의 보편적 정의, 화면에 보이지 않는 소재나 기능을 증명하지 않는다.')
add([192,324],'https://www.leedsth.nhs.uk/about/trust/strategy/investing-in-technologies/about-ppm/','Leeds NHS 전자기록 시스템','태블릿에서 병원 전자기록을 사용하는 한 시스템과 간호 기록 기능의 사례다. 화면이 보이지 않는 사진에서 실제 기록이나 열람 행위를 확정하지 않는다.')
add([299,300,301,302],'https://www.wbstudiotour.co.uk/es/schools/resource-hub/costume-distressing/','Warner Bros. 의상 디스트레싱 교육자료','제작진이 의복에 먼지·오염·찢긴 듯한 낡음 효과를 만드는 사례다. 실제 오염, 오래된 시간, 특정 밑단 형태를 입증하지 않는다.')
add([318],'https://collection.sciencemuseumgroup.org.uk/objects/co8064498/canvas-straitjacket-for-adults-london-england-1930-1960-restraint-suit','Science Museum Group 성인용 구속복','1930–1960년대 환자에게 사용된 별도 구속복 소장품이다. 간호사 제복과 구별하며 이미지에서 실제 구속 또는 동의를 추론하지 않는다.')
add([321],'https://www.adobe.com/creativecloud/photography/hub/guides/best-lens-for-family-portraits.html','Adobe 정면 서기 사진 가이드','서서 카메라를 바라보는 단체 인물사진이라는 부분적 포즈 사례다. 1인 독립 포즈 전체를 정의하지 않는다.')
add([345],'https://spencerart-temp.ku.edu/art/collection-highlights/highlight/9141','Spencer Museum 침묵 손짓 자화상','손가락을 입술에 대어 침묵을 나타낸 회화 사례다. 실제 발성, 감정, 사진 속 인물의 의도는 확정하지 않는다.')
add([352],'https://www.adobe.com/nl/express/discover/ideas/picture/senior','Adobe 인물 포즈 사례','앉아서 한쪽 다리를 구부리는 포즈를 소개한다. 정확한 무릎 높이와 대상 장면의 연령은 별도다.')
add([372],'https://mainweb.awsprod.nlm.nih.gov/exhibition/picturesofnursing/exhibition3s1.html','미국 국립의학도서관 간호 이미지 전시','제1차 세계대전 군 병동의 특정 역사적 사진 사례다. 모든 시대·나라의 병동 구성에 일반화하지 않는다.')
add([373],'https://www.stevenboss.com/fairfield-hills-hospital','Steven Boss 병원 사진','사진가가 폐병원으로 설명한 특정 장소 사례다. 건물의 폐쇄 여부는 사진의 분위기만으로 확정하지 않는다.')
add([381],'https://www.adobe.com/creativecloud/video/hub/ideas/what-is-medium-wide-shot.html','Adobe 미디엄 와이드 쇼트','인물 머리부터 무릎 부근까지 보이는 영상 구도 정의다. 무릎의 정확한 절단 지점은 촬영에 따라 다르다.')
add([112],'https://designmuseum.org/asset/download?id=9b552e92-a967-49a5-9014-4cd46bc146cc','Design Museum Azzedine Alaïa 교육 자료','체형의 윤곽을 드러내는 bodycon 스타일을 한 디자이너 전시 맥락에서 설명한다. 직업·정확한 신축률은 추론하지 않는다.')
add([144],'https://maisoncatanzaro.com/en/sales/1805-11092-mme-poussycat-robe-wetlook-92-polyester-8-elasthanne.html','Patrice Catanzaro wetlook 드레스','제조사가 광택이 있는 wet-look 소재라고 설명한 개별 제품이다. 실제로 젖었는지 또는 사진만으로 소재 조성을 추정하지 않는다.')
add([268],'https://mallbg.com/en/cottelli-collection-black-wet-look-mesh-bodysuit-with-front-zipper-m-1775387.html','전면 지퍼 의상 상품','전면 지퍼가 있는 의상이라는 부분 요소의 사례다. 지퍼가 부분적으로 내려간 상태를 이 출처가 확정하지 않는다.')
add([280],'https://rave-nation.com/products/contagious-naughty-nurse-halloween-costume','간호 테마 비키니형 코스튬 상품','판매자가 간호사 테마의 비키니 상의와 모자 등을 제시한 개별 코스튬이다. 실제 의료복이나 직업을 뜻하지 않는다.')
add([283],'https://en.obsessive.com/en/products/wet-look-bodysuit-11089.html?selected_size=S','개방형 의상 상품 설명','한 상품의 개방형 구성 용례다. 실제 사람의 연령이나 사진에서 가려진 신체와 의복 상태는 알 수 없다.')
add([315],'https://www.mehron.com/stage-blood/','Mehron 공연용 혈액 효과 제품','공연·영화에 쓰이는 가짜 혈액 효과의 일부 사례다. 고어 전체의 정의나 실제 상해·물질의 존재를 증명하지 않는다.')
add([337],'https://www.npg.org.uk/collections/search/portraitExtended/mw00319/Sir-Squire-Bancroft-n-Butterfield','National Portrait Gallery 허리에 손을 둔 인물화','서서 양손을 허리에 둔 인물화를 설명한다. 인물의 직업·감정이나 사진 장르 자체를 일반화하지 않는다.')
add([348],'https://www.pexels.com/photo/woman-sitting-with-knees-up-and-ankles-crossed-11689458/','Pexels 발목을 교차한 사진','앉은 인물의 발목 교차를 설명한 특정 사진 사례다. 다른 자세나 인물의 의도를 증명하지 않는다.')
add([267],'https://www.metmuseum.org/art/collection/search/451160','The Met 앞이 열린 엔타리','앞이 열린 별도 겉옷을 속옷과 바지 위에 착용한 역사적 소장품이다. 간호복이나 현대 코스튬의 형태를 일반화하지 않는다.')
reviewsha=hashlib.sha256(prior.read_bytes()).hexdigest();rows=[]
for rid,sources in sorted(a.items()):
 row=old[rid];rows.append({'source_row_id':rid,'prior_review_file':prior.name,'prior_review_sha256':reviewsha,'previous_status':row['source_status'],'additional_sources':sources,'source_meaning_boundary':row['unresolved_ko'],'context_only':True,'native_approval':False})
q=A/'photo_nurse_uniform_external_source_supplement2_20261107.json';assert not q.exists();q.write_text(json.dumps({'schema':'nurse-uniform-external-source-supplement/v1','scope':'Additional source-supported portions of previously unsupported rows, not proof of full semantics.','rows':rows,'native_approval':False},ensure_ascii=False,indent=2)+'\n');print('additional rows',len(rows),'remaining',86-len(covered)-len(rows))
