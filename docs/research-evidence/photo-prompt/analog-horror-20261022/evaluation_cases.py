"""Natural queries and expected semantic judgments. ALL execution is NOT_RUN."""
CASES = []
def e(group, ko, en, cards, reject, check):
    CASES.append(dict(id=f'E{len(CASES)+1:03}', split='development' if group=='positive' else 'held_out_proposed',
                      group=group, query_ko=ko, query_en=en, expected_card_ids=cards.split(',') if cards else [],
                      reject_ko=reject, review_ko=check, execution_status='NOT_RUN'))

e('positive','두 릴 창이 있는 VHS 테이프 물체','A physical VHS cassette with two reel windows','A001','VCR 본체·CRT','물리 carrier를 선택하고 화면 잡음은 추가하지 않는다.')
e('positive','TV 화면 안에만 PLAY 표시','PLAY lettering only inside a television playback image','A004','방 벽의 글자','표시의 owner는 playback raster다.')
e('positive','두꺼운 몸체와 유리 반사가 있는 브라운관 TV 사진','A photo of a deep CRT television with glass reflections','A005','직접 영상 전체의 어안 효과','물체 사진과 직접 래스터를 구분한다.')
e('positive','TV 화면 안에만 균일한 가로 주사선','Fine evenly spaced scanlines confined to the displayed image','A006','피부 줄무늬·트래킹 띠','display owner와 범위를 보존한다.')
e('positive','4대3 영상이 더 넓은 프레임 안에 있다','A four-to-three picture inside a wider surrounding frame','A010','전체 파일 비율만 수정','내부 래스터 비율을 측정한다.')
e('positive','방송국을 알리는 허구 로고 화면','A fictional station identification card','A011','실제 방송국·주거 장면 자동 추가','식별 그래픽의 위치를 보존한다.')
e('positive','직사각형 시험 화면을 채운 수직 컬러바','Vertical color bars filling a rectangular test field','A012','무지개 풍경','특정 표준값의 정확성은 별도다.')
e('positive','지역명과 짧은 경보 문구가 분리된 방송 화면','An alert card with separate region and event-message areas','A014','실제 EAS 음성·프로토콜 성공','저술한 레이아웃 외형만 평가한다.')
e('positive','각진 컬러 문자가 격자로 정렬된 텔레텍스트','A teletext page with block letters aligned on a rigid grid','A015','현대 웹 대시보드','Ceefax 고유명 자동 부여를 피한다.')
e('positive','프레임 주소가 화면 하단 안에 겹쳐 있다','A burned-in frame address at the bottom of recorded footage','A016','VCR 경과 카운터·날짜','timecode의 표시층과 형식을 보존한다.')
e('positive','재생 영상을 가리는 넓은 가로 트래킹 잡음 띠','A broad horizontal mistracking noise band across playback','A018','CME 추적·주사선','기록 트랙 오류 sense를 선택한다.')
e('positive','영상 일부만 끊는 가는 흰 가로 드롭아웃','Thin white dropout streaks interrupt local picture information','A019','물리 테이프의 색 띠','조건부 재생 분기를 보존한다.')
e('positive','캡처한 VHS 화면 맨 아래의 가는 잡음 띠','A narrow head-switching strip at the very bottom of a captured raster','A020','중앙 잡음 띠','하단 위치와 화면 경계를 확인한다.')
e('positive','직사각형 영상 속 문틀 상단만 옆으로 휜다','The top of a recorded door jamb bends while the outer frame stays rectangular','A021','실제 휜 건물','영상의 왜곡과 건축 owner를 구분한다.')
e('positive','빨간 방송 글자의 색이 밝기 윤곽 밖으로 번진다','Red broadcast lettering bleeds beyond its luminance edge','A023','채도 저하·Y/C 지연','퍼짐과 위치 차이를 구분한다.')
e('positive','색 윤곽이 또렷한 밝기 경계에서 옆으로 밀린다','A color contour is laterally displaced from a crisp luminance edge','A024','렌즈 프리즘·단순 블러','색-밝기 경계의 상대 위치를 확인한다.')
e('positive','고채도 색 경계의 작은 점 열','A beaded pattern along a saturated composite-video boundary','A025','화면 전체 노이즈','crawl 움직임은 still 평가에서 제외한다.')
e('positive','방송 영상의 같은 윤곽이 가로로 옅게 중복된다','A faint horizontally displaced echo of the same broadcast image contour','A026','렌즈 플레어 원반','transmission ghost sense를 선택한다.')
e('positive','팔 윤곽에만 교차 가로 빗살이 보인다','Alternating horizontal comb teeth confined to a moving arm contour','A028','화면 전체 가로선','필드 시간차는 별도 확인한다.')
e('positive','높은 방 모서리에서 내려다보는 고정 감시 화면','A fixed surveillance view from a high room corner','A039','로봇 세계·비동의 추론','시점과 공간만 보강한다.')
e('positive','벽돌 속에 유기 막이 박히고 가지 능선이 이어진다','An organic membrane embedded in masonry with branching ridges continuing into the wall','A064','방 안의 별도 생물','동일 기존 living architecture 전체 재사용을 우선한다.')
e('positive','기밀 문서에서 일부 단어만 검은 직사각형으로 가렸다','Black opaque rectangles cover selected words while surrounding text remains visible','A073','밈 효과·실제 기밀 판정','정보 가림의 owner와 범위를 본다.')
e('positive','시간과 주파수 축, 강도 범례가 있는 도표','An intensity plot with time and frequency axes and a color key','A074','오디오 파형·SSTV 이미지','시각화와 실제 신호 해독을 분리한다.')
e('positive','수신기 케이블이 컴퓨터의 복원 이미지 화면으로 이어진다','A radio receiver cabled to a computer showing a decoded still image','A075','스펙트로그램만 표시','실제 수신 성공의 별도 로그를 요구한다.')

BOUNDARIES = [
 ('트래킹 오류가 아니라 밤하늘 물체를 따라가는 카메라','A camera tracking a moving object in the night sky','','A018','tracking 다의어를 차단한다.'),
 ('낮은 채도의 팔레트, 색 번짐은 없음','A low-chroma palette without video color bleed','','A023,A024','색채 관계와 비디오 신호를 분리한다.'),
 ('광원-렌즈 축을 따라 생긴 플레어 고스트','Lens-reflection ghosts aligned with a bright light and lens axis','','A026','기존 lens ghosting source의 고유 의미를 유지한다.'),
 ('사람의 피부에 빛나는 스캔라인 무늬','Glowing scanline patterns on skin','','A006','피부와 표시 래스터 owner를 분리한다.'),
 ('짧은 드롭아웃과 화면 전체의 수신 잡음','Local dropout streaks versus full-screen reception static','A019,A032','둘을 동일 후보로 병합','서로 다른 현상을 독립 제안한다.'),
 ('아래쪽 헤드 전환 띠와 중앙 트래킹 띠','A bottom head-switch strip versus a central tracking band','A020,A018','위치 조건 삭제','각 위치를 따로 심사한다.'),
 ('색 퍼짐과 일정하게 밀린 색 윤곽','Color spreading versus a consistently displaced color contour','A023,A024','색수차 하나로 대체','확산과 위치 차이를 구별한다.'),
 ('방송 수신 겹상과 밝은 광원의 잔광 꼬리','A received image echo versus a camera-tube light trail','A026,A027','동일 ghost 후보','복제 윤곽과 광원 연결 흔적을 구별한다.'),
 ('주사선과 움직임 윤곽의 빗살','Display scanlines versus interlace combing at a moving contour','A006,A028','전체 가로선 하나로 대체','영역·밀도·윤곽 결합을 보존한다.'),
 ('원본과 가장자리 잘림 비교','A full reference picture and its edge-cropped version','A030','단일 프레임으로 overscan 원인 확정','패널 대응과 제거된 모서리를 확인한다.'),
 ('필름을 VHS로 옮긴 뒤 디지털 재압축한 영상','Film transferred to VHS and later digitally recompressed','A033,A034,A037','경로 없이 흔적 전부 강제','요청에 명시한 전송 경로에만 복합 효과를 허용한다.'),
 ('VHS 고유 손상만, 디지털 블록은 요청하지 않음','VHS playback defects only, with no digital compression request','A018,A019','A037','디지털 처리 분기 추가를 막는다.'),
 ('평범한 VHS 가족 영상, 공포 없음','An ordinary VHS family video with no horror','A038','괴물·경보·유혈 자동 추가','장르 문맥이 없는 요청을 보존한다.'),
 ('방송 종료 카드 한 장','A single sign-off card','','종료 사건·끝없는 반복 성공','정지 카드가 순서를 입증하지 않는다.'),
 ('1983년 미국 EBS 자료풍','A fictional US EBS-style card set in 1983','A013','현대 EAS/SAME 레이아웃 강제','역사적 경로를 분리한다.'),
 ('텔레텍스트 일반 화면, BBC 고유명 없음','A generic teletext page without BBC branding','A015','Ceefax 로고 강제','기술 방식과 고유 서비스명을 구분한다.'),
 ('화면 밖 자막과 TV 화면 속 PLAY','An external caption and PLAY inside a television picture','A004,A049','같은 텍스트 owner','극중/극외 텍스트 경계를 유지한다.'),
 ('VCR 경과 표시와 프레임 주소','A VCR elapsed counter versus a frame address','A016,A017','두 값을 같은 timecode로 판단','날짜·counter·frame code를 분리한다.'),
 ('CCTV가 있으나 촬영 동의는 명시하지 않음','CCTV footage with no statement about recording consent','A039','비동의 촬영·관음 확정','가시 시점과 동의를 분리한다.'),
 ('거울에 비친 한 사람','One person reflected in a mirror','','A059','서로 다른 두 인물의 조건이 없다.'),
 ('둘이 닮았지만 정체는 설명하지 않음','Two similar-looking adults with no identity explanation','A059','대체 인간·쌍둥이 확정','외형 대응만 평가한다.'),
 ('원작 미지정 모방 괴물','An original mimic with no named franchise','','Alternate·Woodcrawler 자동 추가','고유 설정과 일반 능력을 분리한다.'),
 ('애니매트로닉 점검구만, 내부 시체는 없음','An animatronic access hatch with no corpse inside','A061','시체·빙의 자동 추가','가시 기구와 서사 생사를 구분한다.'),
 ('SCP의 mimetic과 memetic을 비교','Distinguish mimetic from memetic in SCP','','동일 키워드·괴물 외형','허구 메커니즘을 context로 각각 유지한다.'),
 ('정보를 가린 문서이지만 항밈이라고 하지 않음','A redacted document with no antimemetic claim','A073','항밈 효과 합격','가림과 기억 억제를 분리한다.'),
 ('시간-주파수 도표와 수신한 정지 이미지','A time-frequency plot versus a radio-received still image','A074,A075','같은 decoding 의미','표현 종류와 실제 처리 증거를 따로 본다.'),
 ('모스 부호 자체를 암호라고 부르지 않음','Morse code as encoding rather than encryption','A076','암호화 성공 주장','부호 대응은 별도 검증한다.'),
 ('빈 쇼핑몰 복도, 폐업 여부 불명','An empty mall corridor with unknown operating status','A068','폐업·Backrooms 확정','보이는 상태와 역사·판본을 분리한다.'),
 ('단일 영상의 같은 이미지를 여러 플랫폼에 게시','The same video image reposted across several platforms','','트랜스미디어 성공','각 매체의 추가 정보가 필요하다.'),
 ('부검과 생체 해부를 구분','Distinguish autopsy from vivisection','','의료 테이블로 생사 확정','생사·행위는 context로 분리한다.'),
 ('근친 금기와 가족 내 성적 학대를 구분','Distinguish an incest motif from intrafamilial sexual abuse','','혈연·비동의·성적 의도를 외형으로 확정','관련 항목을 제외하지 않고 관계별로 보존한다.'),
 ('고문 중심 호러라는 비평 용어','The critical phrase torture porn applied to horror','','성적 장르·성적 흥분 자동 판정','porn이라는 어휘의 오탐을 막는다.')
]
for ko,en,cards,reject,check in BOUNDARIES: e('boundary',ko,en,cards,reject,check)

CONTROLS = [
 ('맑은 여행 사진','A clear travel photograph'),('신제품 LCD 모니터','A new LCD monitor'),
 ('조용한 병원 대기실 사진','A quiet hospital waiting-room photograph'),('밝은 사무실의 안내판','An information board in a bright office'),
 ('일반적인 가족 초상','An ordinary family portrait'),('숲 자연 다큐의 선명한 스틸','A clean still from a forest nature documentary'),
 ('평범한 마이크 제품 사진','A standard microphone product photo'),('새 카세트의 제품 사진','A product photo of a new audio cassette'),
 ('대낮의 쇼핑몰 안내도','A daytime shopping-mall directory'),('인터뷰 중인 성인','An adult being interviewed'),
 ('명확한 흑백 사진','A clean black-and-white photograph'),('일반 4대3 풍경 사진','An ordinary four-to-three landscape photograph'),
 ('저채도 가구 광고','A low-chroma furniture advertisement'),('적색 EXIT 안내 표지','A red EXIT information sign'),
 ('아무 소리 없는 정지 JPEG','A still JPEG with no sound track'),('곡면 유리 진열장','A curved-glass display cabinet')
]
for ko,en in CONTROLS: e('ordinary_control',ko,en,'','장르·노이즈·괴물·피해·성적 의미의 자동 추가','요청에 없는 아날로그 호러 bundle을 노출·선택하지 않는다. 매체/소품 자체의 관련 후보는 허용한다.')

NONVISUAL = [
 ('낡은 테이프에서 느린 음높이 흔들림','Slow pitch fluctuations from an old tape'),
 ('방송 침묵이 오래 이어진다','A long stretch of dead air'),
 ('입 움직임보다 늦게 들리는 음성','A voice arriving after the lip movement'),
 ('숫자 방송의 반복되는 목소리','A repeating spoken numbers-station transmission'),
 ('점차 악화되는 세 단계 지침','Three instructions that become progressively worse'),
 ('녹화된 인물이 현재 시청자의 기억을 안다','A recorded person knows the present viewer’s memories'),
 ('읽으면 잊게 되는 항밈 문서','An antimemetic document forgotten after reading'),
 ('촬영 동의가 없었던 기록','A recording made without consent')
]
for ko,en in NONVISUAL: e('unobservable_control',ko,en,'','정지 이미지로 원래 의미 전체 합격','맥락은 보존하되 still proxy가 음성·시간·동의·초자연 인과를 통과시키지 않는다.')
