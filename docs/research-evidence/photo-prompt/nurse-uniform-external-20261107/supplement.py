import json,hashlib
from pathlib import Path
R=Path('/Users/chasoik/Projects/image-prompt');A=R/'skills/photo-prompt-image-generator/assets';prior=A/'photo_nurse_uniform_external_review_20261107.json'; p=json.loads(prior.read_text()); old={x['source_row_id']:x for x in p['rows']};a={}
def add(ids,url,name,scope):
 for n in ids:
  rid='NURSE-ROW-%03d'%n;assert rid in old and not old[rid]['new_external_sources'];a.setdefault(rid,[]).append({'url':url,'source':name,'supported_scope_ko':scope,'evidence_level':'partial'})
add([49],'https://cnh.omeka.net/exhibits/show/uniforming/caps','Northeastern Pennsylvania 간호사 캡 전시','학교별 winged cap과 cupcake 스타일을 구분한다. 정확한 형태와 학교별 용례는 추가 확인이 필요하다.')
add([59],'https://luckydollstore.com/nurse-roleplay-costume-accessory-set/','간호 코스튬 액세서리','간호 역할놀이용 머리띠 캡의 상품 예다. 실제 의료복이나 특정 크기를 보장하지 않는다.')
add([60],'https://amarisfmcgsolutions.com/product/hair-nets/','의료·위생용 헤어넷','헤어넷을 머리 덮개와 별도 상품으로 분류한 예다. 소재나 실제 위생 상태는 사진으로 확정하지 않는다.')
add([72],'https://www.sscamh.com/public/backend-assets/js/ckfinder/files/Fashion%20Designer_V4_0_ENG_PHB-compressed.pdf','패션 디자인 교육 안내','캡 소매를 어깨를 짧게 덮는 소매 유형으로 보여 준다. 모든 소매에 같은 길이를 강제하지 않는다.')
add([89],'https://www.interweavetextiles.com/wp-content/uploads/2023/07/Catalogue-Interweave-2023-July.pdf','Interweave 의료복 카탈로그','특정 스크럽 상의에 비대칭 지퍼를 명시한다. 모든 비대칭 여밈이 지퍼인 것은 아니다.')
add([107,242],'https://www.maskworld.com/english/p/sexy-pin-up-nurse-plus-size-costume--203458','핀업 간호사 코스튬 상품','한 성인 상품의 미니 앞치마·드레스·모자 조합이다. 전체 장르의 보편적 정의나 실제 인물의 연령을 뜻하지 않는다.')
add([108],'https://www.etsy.com/listing/874887562/retro-nurse-costume-ruffled-apron-hat','레트로 간호사 의상 상품 제목','상품 제목에서 주름 앞치마와 모자 조합을 확인한다. 판매 종료 상태이며 실제 상품 구성과 보편성은 별도다.')
add([153],'https://www.ballinacostumecompany.ie/?product=nurse','Ballina 간호 코스튬','흰 드레스에 빨간 단추·테두리를 쓰는 한 제품 사례다. 의료 직무나 실제 소속을 뜻하지 않는다.')
add([154],'https://dictionary.archivists.org/entry/monochrome.html','Society of American Archivists monochrome','단색과 흑백의 범위를 구분하는 용어 설명이다. 특정 의복이나 빛의 물리적 원인을 뜻하지 않는다.')
add([167],'https://www.impulse.com.tw/product_en.php?id=14','IMPULSE 레이스 톱 스타킹','레이스 톱과 허벅지 길이를 결합한 제조사 상품 범주다. 보이지 않는 연결장치를 추론하지 않는다.')
add([197],'https://www.elliottsfancydress.co.uk/giant-syringe-accessory','대형 주사기 코스튬 소품','크기가 큰 주사기 모양 소품을 간호·의사 코스튬과 결합하는 특정 상품이다. 실제 주사행위나 기구 안전성을 뜻하지 않는다.')
add([225],'https://www.allure.com/story/keke-palmer-pinned-back-bangs','Allure 핀으로 고정한 앞머리','앞머리를 뒤로 고정한 헤어 스타일의 개별 기사다. 숨은 핀의 정확한 개수는 보이지 않으면 미관찰이다.')
add([229],'https://veeandell.blogspot.com/2014/04/pin-up-makeup-tutorial.html','메이크업 아티스트 핀업 튜토리얼','한 작성자가 빨간 입술과 윙드 라이너를 조합한 핀업 사례다. 모든 핀업의 필수 요소가 아니다.')
add([233],'https://vioda.makeup/looks/soft-goth/','메이크업 아티스트 soft goth','어두운 입술·스모키 눈가와 밝은 피부를 조합하는 한 고딕 메이크업 예다. 실제 인물의 건강이나 성격을 뜻하지 않는다.')
add([244],'https://temple-of-love.org/products/dreamgirl-triage-trixie-nurse-costume','간호 모티프 란제리 상품','간호캡과 가터 슬립을 조합한 특정 성인 상품이다. 다른 상품이나 착용자의 실제 직업과 동의는 추정하지 않는다.')
add([257],'https://bodylinetokyo.co.jp/en-int/collections/cosplay_college_students/products/75671','BODYLINE 메이드풍 간호 코스튬','한 제조사의 메이드풍 간호 코스튬 사례다. 실제 간호복이나 특정 프릴의 필수성을 뜻하지 않는다.')
add([316],'https://academicinformation.arts.columbia.edu/theatre/prop-weapons','Columbia 무기형 소품 지침','공연에서 무기형 소품을 별도로 다루는 실제 제작 맥락이다. 이미지로 실제 무기 여부·위험성·의도를 판정하지 않는다.')
add([330],'https://dlg.usg.edu/record/geusc_170msbcck2-cor_201bk3jb8v-cor','Digital Library of Georgia 트레이 사진','병원 복도에서 트레이를 든 간호사로 기술된 특정 사진이다. 손의 정확한 위치와 내용물은 보이는 범위에서 판정한다.')
add([331],'https://jknjohor.moh.gov.my/hsajb/phocadownload/HSA/OSHA/2024/Code%20Blue%20System%20HSAJB%20Second%20Edition%202021.pdf','병원 응급 카트 절차','한 병원의 문서가 간호사가 응급 카트를 미는 상황을 기술한다. 정지 이미지로 실제 이동 이력이나 응급 상황을 입증하지 않는다.')
add([350],'https://www.theclickcommunity.com/blog/creating-multiple-photographs-out-of-one-pose-by-emily-potts/','인물사진 포즈 사례','한 사진가가 앉은 인물의 무릎을 모아 촬영한 사례다. 인물 감정이나 연령은 포즈로 추정하지 않는다.')
add([375],'https://www.energy.gov/sites/default/files/2016/09/f33/2016_gateway-acc.pdf','미국 에너지부 실내 조명 사례','간호 스테이션 인접 복도의 형광등 조명 사례를 기록한다. 이미지 색온도만으로 실제 광원 종류를 확정하지 않는다.')
reviewsha=hashlib.sha256(prior.read_bytes()).hexdigest();rows=[]
for rid,sources in sorted(a.items()):
 row=old[rid];rows.append({'source_row_id':rid,'prior_review_file':prior.name,'prior_review_sha256':reviewsha,'previous_status':row['source_status'],'additional_sources':sources,'source_meaning_boundary':row['unresolved_ko'],'context_only':True,'native_approval':False})
q=A/'photo_nurse_uniform_external_source_supplement_20261107.json';assert not q.exists();q.write_text(json.dumps({'schema':'nurse-uniform-external-source-supplement/v1','scope':'Additional source-supported portions of previously unsupported rows, not proof of full semantics.','rows':rows,'native_approval':False},ensure_ascii=False,indent=2)+'\n');print('additional sourced rows',len(rows),'remaining without new source',86-len(rows))
