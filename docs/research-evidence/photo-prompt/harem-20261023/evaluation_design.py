from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
# Authored minimal contrasts for development. Neither side is a new runtime fact.
PAIRS=r'''
하렘/앙상블|성인 B와 C가 각자 A에게 구애하는 장면|Adults B and C separately court A.|세 성인이 같은 탁자에서 각자 식사하는 장면|Three adults independently eat at the same table.|집단 인원수만으로 구애를 추가하지 않음
경쟁/비경쟁|B와 C가 A 옆의 빈자리 하나를 두고 다툰다|B and C compete for the one empty seat beside A.|B와 C가 서로 다른 의자에 앉아 A와 대화한다|B and C sit in separate chairs while talking to A.|한정 선택은 경쟁 요청에만 유지
역하렘/혼성|성인 여성 A에게 성인 남성 B와 C가 각각 구애한다|Adult men B and C each court adult woman A.|성인 A에게 서로 다른 성별의 성인 B와 C가 각각 구애한다|Adults B and C of different genders each court adult A.|명시한 인물별 성별과 관계 방향 보존; 외형 추론 금지
백합/여성 집단|성인 여성 B와 C가 성인 여성 A에게 각각 연애 관심을 보인다|Adult women B and C each show romantic interest in adult woman A.|성인 여성 셋이 업무 회의를 한다|Three adult women hold a work meeting.|여성만 있다는 사실로 연애를 추가하지 않음
why-choose/선택|마지막에도 복수 상대와 관계를 유지하는 이야기의 표지|A cover for a story whose protagonist keeps several partners at the end.|결말에 한 상대를 선택하는 이야기의 표지|A cover for a story whose protagonist chooses one partner at the end.|결말은 선언된 문맥; 표지로 독립 증명하지 않음
CNM/외도|관련된 모든 성인이 알고 동의한 복수 연애|Multiple romantic relationships known and agreed to by every adult involved.|독점 약속을 어긴 비밀 외도|A secret affair violating an exclusivity agreement.|포옹·반지·인원수로 동의나 약속을 만들어내지 않음
츤데레/홍조|도시락을 건네며 시선을 피하는 츤데레 성인|A tsundere adult offers a lunchbox while averting the gaze.|운동 후 뺨이 붉은 성인|An adult has flushed cheeks after exercise.|홍조를 숨긴 애정으로 고정하지 않음
얀데레/도구|상대와 경쟁자의 접근을 통제하는 얀데레 성인|A yandere adult controls access to the beloved and a rival.|성인 요리사가 주방에서 칼을 든다|An adult chef holds a knife in a kitchen.|칼 소유를 집착·살인으로 바꾸지 않음
카베돈 다의성|성인 A가 B 머리 옆 벽에 손을 짚고 마주 선다|Adult A plants a hand on the wall beside B's head while facing B.|성인 A가 옆방 소음에 항의해 벽을 두드린다|Adult A knocks on a wall to protest noise next door.|동일 표제의 다른 의미·상대·소리 구별
팔짱 다의성|B가 A의 팔에 자기 팔을 건다|B links an arm through A's arm.|A가 자기 가슴 앞에서 두 팔을 교차한다|A folds both arms across A's own chest.|상대/자기 팔 owner 보존
소매/손목|B가 A의 소매 천을 집는다|B pinches the fabric of A's sleeve.|B가 A의 맨 손목을 붙잡는다|B grips A's bare wrist.|천 접점과 피부 접점을 바꾸지 않음
깍지 owner|A와 B가 서로 손가락을 엇갈려 손을 잡는다|A and B hold hands with their fingers interlaced.|A가 자기 두 손 손가락을 엇갈려 모은다|A interlaces the fingers of A's own two hands.|기존 자기 손 후보를 타인 손에 그대로 bind하지 않음
무릎베개/어깨|A 머리가 B 허벅지 위에 놓이고 몸통은 벤치가 받친다|A's head rests on B's thighs while a bench supports A's torso.|A 머리가 앉은 B 어깨에 기댄다|A's head rests on seated B's shoulder.|머리 지지 target 보존
안기/업기|A가 B의 등과 무릎 아래를 받쳐 가로로 안는다|A carries B horizontally with support beneath B's back and knees.|A가 B를 등에 업는다|A carries B on A's back.|같은 carrying 표제로 지지 구조를 합치지 않음
키스 전/접촉|A와 B 입술 사이에 보이는 틈이 있다|A visible gap remains between A's and B's lips.|A와 B 입술이 서로 닿아 있다|A's and B's lips touch.|gap와 contact는 반대 상태
거울/실물|B 실제 몸과 거울 속 B 반사상이 보인다|B's physical body and B's mirror reflection are visible.|B와 C라는 서로 다른 두 사람이 나란히 있다|Two distinct people B and C stand side by side.|반사상을 새 인물로 세지 않음
유사 하렘/복수 캐스트|한 성인 배우의 여러 표정을 패널로 보여준다|Panels show several expressions of one adult performer.|서로 다른 세 성인 배우가 각각 다른 표정을 짓는다|Three distinct adult performers show different expressions.|매체 속 반복과 실제 인원수 보존
루트/동시 관계|게임 화면 안의 세 개별 루트 패널|Three separate route panels within a game screen.|방 안에서 실제로 함께 있는 성인 세 사람|Three adults physically share one room.|screen boundary를 실물로 넘기지 않음
실크/새틴|실크 섬유로 만든 무광 직물|A matte fabric made from silk fibres.|합성섬유로 만든 광택 새틴|Glossy satin made from synthetic fibres.|섬유와 조직·광택 별도, 성분은 문맥
슬립/슬립드레스|겉드레스 아래 별도 슬립이 보인다|A separate slip is visible under an outer dress.|슬립드레스 한 벌을 겉옷으로 입었다|One slip dress is worn as outerwear.|레이어 수와 용도 경계
슬릿/컷아웃|밑단까지 이어지는 치마 트임|A skirt slit opens to the hem.|천으로 사방이 둘러싸인 옆구리 개구|A side cutout is enclosed by fabric on every side.|개구의 topology 보존
가터/허벅지 링|허리벨트 끈의 클립이 스타킹 윗단에 붙는다|A clip on a waist-belt strap attaches to a stocking top.|허벅지 장식 링 하나가 독립적으로 있다|A decorative thigh ring sits independently.|벨트→끈→클립→스타킹 연결을 생략하지 않음
레이스/투명|레이스 아래 불투명 안감이 있다|Opaque lining lies beneath lace.|레이스 구멍 뒤로 피부가 보인다|Skin is visible behind the lace openings.|레이스 명칭으로 노출을 증가시키지 않음
하네스/장비|옷 위에 장식 스트랩 하네스가 있다|Decorative harness straps lie over clothing.|선언된 등반 장비 하네스를 착용했다|A declared climbing harness is worn.|기능·구속·역할·동의를 모양만으로 전환하지 않음
제복/직업|무대용 집사 의상을 입은 성인 배우|An adult actor wears a butler stage costume.|실제 집사라는 설정의 성인|An adult is declared to work as a butler.|착용과 직업·주종·애정 구별
역사/회화|오스만 궁전의 사적 생활 구역|A private domestic quarter in an Ottoman palace.|19세기 유럽 오리엔탈리즘 회화의 스튜디오 재연|A studio restaging of a nineteenth-century European Orientalist painting.|시대·지역·가공 세트·실제 주거 구분
멘헤라/진단|멘헤라라는 팬덤 표제의 성인 인물|An adult character carries the fandom label menhera.|슬픈 표정을 짓는 성인|An adult has a sad expression.|둘 다 외형에서 정신질환 진단 금지
OT3/세 커플|세 명이 한 관계를 이루는 OT3 구상|An OT3 concept involving three people in one relationship.|서로 다른 세 커플의 여섯 사람|Six people form three separate couples.|약어 정확한 외부 검증 전까지 문맥 유지; 사람/관계 수 분리
NTR/허용|기존 파트너 A가 B와 C의 관계를 모르고 있는 문맥|Existing partner A is unaware of B's relationship with C.|A가 B와 C의 관계를 허용한 문맥|A permits B's relationship with C.|관점·인지·허용은 문맥; B/C 동의 별도
본디지/동의|상호 합의를 명시한 성인 역할극의 장식적 구속|Decorative restraint in explicitly agreed adult roleplay.|강제로 이동을 제한한다는 비성적 위기 문맥|Nonsexual danger context explicitly states forced restriction of movement.|끈·옷·미소로 동의의 진위를 판단하지 않음
강제 근접/강압|폭우로 같은 대합실에 머무는 성인 둘|Two adults stay in the same waiting room because of heavy rain.|상대를 떠나지 못하게 위협하는 문맥|Context states threats preventing another person from leaving.|forced proximity 장르와 의지 침해는 별도
한 침대/성적 사건|빈 침대 하나를 두고 떨어져 서 있는 성인 둘|Two adults stand apart beside one empty bed.|성적 사건이 있었다는 이야기 문맥|Story context states that a sexual event occurred.|한 침대나 가까운 거리에서 성적 사건 추론 금지
정신 지배/눈 모양|외부 마법이 판단을 바꾼다는 문맥|Context states that external magic alters judgment.|단순한 나선 무늬 눈의 성인 캐릭터|An adult character merely has spiral-pattern eyes.|미학적 표면과 의지 변화·동의 구별
히메컷/보브|일자 앞머리·뺨 길이 옆머리·긴 뒷머리|Straight fringe, cheek-length sidelocks and long back hair.|뒷머리까지 턱선에서 끝나는 보브|A bob also ends at the jawline at the back.|독립 모발 구간과 길이 관계 보존
손등/볼 키스|A 입술이 B 손등에 닿는다|A's lips touch the back of B's hand.|A 입술이 B 뺨에 닿는다|A's lips touch B's cheek.|접촉 target를 낭만 유사성으로 대체하지 않음
카메라/상대 시선|B가 전경 A의 얼굴을 본다|B looks at A's foreground face.|B가 렌즈를 똑바로 본다|B looks directly into the lens.|화면상 대략 방향이 같아도 target를 분리
'''

def build():
 out=[]
 for i,line in enumerate(PAIRS.strip().splitlines(),1):
  label,ako,aen,bko,ben,expected=line.split('|')
  out.append(dict(id=f'B{i:02d}',contrast=label,a=dict(ko=ako,en=aen),b=dict(ko=bko,en=ben),
                  acceptance=expected,status='DESIGNED_NOT_RUN',independent_holdout=False))
 assert len(out)==36
 (HERE/'boundary-cases.json').write_text(json.dumps(dict(schema='harem-boundary-design/v1',pairs=out,
     pair_count=36,case_count=72,query_count=144,independent_holdout=False),ensure_ascii=False,indent=2)+'\n')
 text=['pair\tside\tquery_ko\tquery_en\tacceptance']
 for p in out:
  for side in ['a','b']: text.append('\t'.join([p['id'],side,p[side]['ko'],p[side]['en'],p['acceptance']]))
 (HERE/'BOUNDARY-CASES.tsv').write_text('\n'.join(text)+'\n')

if __name__=='__main__':build()
