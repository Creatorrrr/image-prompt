"""Authored visual proposals. Source definitions do not prescribe these scenes."""
CARDS = []
def c(seeds, title, layer, slots, components, relations, confusion, limit, sources, mode='still', priority='P1'):
    owners = []
    for line in components.split(';'):
        oid, text = line.split(':', 1); en, ko = text.split('~')
        owners.append(dict(id=oid.strip(), visible_en=en.strip(), visible_ko=ko.strip()))
    graph = []
    for line in relations.split(';'):
        sub, pred, obj, en, ko = line.split('|')
        graph.append(dict(subject=sub, predicate=pred, object=obj, visible_en=en, visible_ko=ko))
    slot_map = {'text_carrier': 'visible_text', 'spatial_relation': 'prop_placement'}
    mapped_slots = list(dict.fromkeys(slot_map.get(s, s) for s in slots.split(',')))
    CARDS.append(dict(id=f'A{len(CARDS)+1:03}', seed_ids=seeds, title_ko=title, layer=layer,
                      proposed_slots=mapped_slots, semantic_axes=slots.split(','), owners=owners, relations=graph,
                      confusion_boundaries_ko=confusion.split(';'), claim_limit_ko=limit,
                      source_ids=sources.split(','), evidence_mode=mode, priority=priority))

c([33], 'VHS 카세트의 물리적 외형', 'carrier', 'prop,object_structure',
  'cassette:a rectangular full-size video cassette with two reel windows~두 릴 창이 있는 직사각형 비디오 카세트;label:a paper title label on its spine~등 부분의 종이 제목 라벨',
  'label|attached_to|cassette|The paper label is attached to the cassette spine|종이 라벨은 카세트 등 부분에 붙어 있다',
  'VCR 본체;CRT TV;손상 영상의 줄을 플라스틱 표면에 그리기', 'VHS·S-VHS 구별은 표시나 세부 규격 대조 필요. 외형이 녹화 내용·진품 연대를 증명하지 않는다.', 'S01', priority='P0')
c([33], '소형 카세트와 어댑터의 크기 관계', 'carrier', 'prop,scale_relation',
  'compact:a small camcorder cassette~소형 캠코더 카세트;adapter:a larger cassette-shaped adapter with an open bay~삽입부가 열린 큰 카세트형 어댑터',
  'compact|inside|adapter|The compact cassette sits inside the larger adapter bay|소형 카세트가 큰 어댑터의 삽입부 안에 있다',
  '모든 소형 카세트를 VHS-C라고 단정;8mm·MiniDV 혼합', 'VHS-C 규격의 진위는 모양만으로 확정하지 않고 참조 사진·표기를 추가 대조한다.', 'S01', mode='proxy')
c([34], 'VCR의 삽입 슬롯', 'playback_device', 'prop,object_structure',
  'deck:a horizontal video deck with a front loading slot~전면 삽입 슬롯이 있는 수평 비디오 데크;cassette:a video cassette partly inserted into that slot~슬롯에 일부 삽입된 비디오 카세트',
  'cassette|inserted_into|deck|The cassette enters the deck slot|카세트가 데크 슬롯 안으로 들어가 있다',
  'CRT 화면;오디오 데크;카세트 자체', '정지 상태는 녹화·재생의 실제 작동을 증명하지 않는다.', 'S01', priority='P0')
c([34,80], '재생 영상 안의 OSD', 'playback_raster', 'image_artifact,text_carrier',
  'raster:one rectangular recorded image~직사각형 기록 영상;osd:small PLAY lettering in one corner~한 모서리의 작은 PLAY 글자',
  'osd|overlaid_on|raster|The PLAY lettering sits inside the recorded image boundary|PLAY 글자는 기록 영상 경계 안에 겹쳐 있다',
  '벽에 투사된 글자;영상 밖 캡션;실제 버튼', 'PLAY 표시는 저술한 정지 그래픽이며 재생 작동이나 촬영자의 행동 증거가 아니다.', 'S01,S11', priority='P0')
c([35], '브라운관을 외부에서 본 사진', 'display', 'prop,object_structure',
  'housing:a deep television housing with a thick bezel~두꺼운 베젤과 깊은 몸체의 TV;glass:a curved glass display surface with a small reflection~작은 반사가 보이는 곡면 유리 화면',
  'glass|bounded_by|housing|The curved glass is enclosed by the thick bezel|곡면 유리는 두꺼운 베젤로 둘러싸인다',
  '영상 전체에 어안 왜곡 적용;모든 CRT를 TV로 분류', '이 카드는 TV 완제품의 한 예다. CRT에는 다른 용도도 있고 곡률만으로 실제 부품을 증명하지 않는다.', 'S37,S01', priority='P0')
c([57,35], '표시 래스터에 한정한 주사선', 'display', 'image_artifact',
  'display:one illuminated rectangular display area~빛나는 직사각형 화면 영역;lines:fine evenly spaced horizontal dark lines~미세하고 균일한 가로 어두운 선',
  'lines|confined_to|display|The fine lines remain within the display area|미세한 선은 화면 영역 안에만 있다',
  '트래킹 잡음 띠;피부의 줄무늬;벽지', '주사선 외형은 테이프 손상·정확한 주사율·실제 CRT 촬영을 증명하지 않는다.', 'S10,S01', priority='P0')
c([36,26], '손에 든 캠코더와 촬영 방향', 'capture', 'apparatus_pov,prop',
  'camera:a compact camcorder held at shoulder height~어깨 높이에서 손에 든 캠코더;subject:an adult facing the camcorder lens~캠코더 렌즈를 향한 성인',
  'camera|aimed_at|subject|The camcorder lens points at the adult|캠코더 렌즈는 성인을 향한다',
  '모든 캠코더를 아날로그로 단정;흔들림을 공포로 단정', '기기 모델·녹화 형식·음성·촬영 동의는 별도 정보다.', 'S01,S31', mode='proxy')
c([37], '오디오 카세트와 녹음기', 'carrier', 'prop,object_structure',
  'cassette:a small audio cassette with two reels~두 릴이 있는 작은 오디오 카세트;recorder:a portable cassette recorder with an open compartment~카세트 삽입부가 열린 휴대용 녹음기',
  'cassette|beside|recorder|The audio cassette lies next to its recorder|오디오 카세트가 녹음기 옆에 놓여 있다',
  'VHS 카세트;테이프 히스를 픽셀로 평가', '목소리·히스·역재생은 보이지 않는다.', 'S21,S22', mode='proxy')
c([37], '오픈릴의 테이프 경로', 'carrier', 'object_structure,prop',
  'left:a left reel holding magnetic tape~자기테이프가 감긴 왼쪽 릴;right:a right take-up reel~오른쪽 감기 릴;path:a thin tape strip crossing a lower head assembly~아래 헤드부를 지나는 가는 테이프 띠',
  'path|connects|left|The tape strip runs from the left reel|테이프 띠는 왼쪽 릴에서 이어진다;path|connects|right|The same strip continues to the right reel|같은 띠가 오른쪽 릴로 이어진다',
  '필름 영사기;릴 회전을 정지 사진으로 통과', '재생·속도 흔들림·소리의 존재는 입증하지 않는다.', 'S09,S21', mode='proxy')
c([39], '4:3 기록 화면의 경계', 'format', 'format',
  'image:a complete image rectangle with visible corners~네 모서리가 보이는 완전한 영상 직사각형;matte:a plain surrounding matte~영상 밖의 단순한 여백',
  'image|inside|matte|The image rectangle has a width-to-height ratio of four to three|영상 직사각형의 가로세로 비율은 4대3이다',
  '시네마 프레임 전체를 4:3이라고 선언;화면비로 시대 확정', '이미지 파일과 화면 속 영상의 비율을 각각 측정한다. 화면비는 아날로그 전용이 아니다.', 'S01,S15', priority='P0')
c([40,6], '방송국 식별 그래픽', 'broadcast_graphics', 'text_carrier,presentation_style',
  'raster:a plain broadcast graphic field~단순한 방송 그래픽 바탕;ident:a large fictional station mark with a smaller channel number~큰 허구 방송국 표시와 작은 채널 번호',
  'ident|centered_in|raster|The station mark is centered within the broadcast field|방송국 표시는 방송 그래픽 바탕 중앙에 있다',
  '실제 방송국의 공식 경보로 주장;모든 후보에 같은 로고 주입', '방송 사이 연결·반복·변조는 시퀀스 증거가 필요하다. 원작 로고 복제는 기본값이 아니다.', 'S11,S27', mode='proxy')
c([42], '시험 화면의 컬러바', 'signal_test', 'image_artifact,presentation_style',
  'frame:a clean rectangular test field~깔끔한 직사각형 시험 화면;bars:a row of broad adjacent vertical color bars~서로 붙은 넓은 수직 색 띠 한 줄',
  'bars|fill|frame|The vertical bars fill the test field without random gaps|수직 색 띠가 임의의 틈 없이 시험 화면을 채운다',
  '무지개 풍경;특정 SMPTE 규격 순서를 임의로 주장', '일반 컬러바 제안이다. 특정 표준명·정확한 색값·보정 기능은 규격별 추가 대조 후 사용한다.', 'S01,S10', mode='proxy', priority='P0')
c([43,17], '이전 시대 비상방송의 문자 화면', 'broadcast_graphics', 'text_carrier,presentation_style',
  'screen:a monochrome instructional television card~단색 지침 TV 화면;notice:a short fictional emergency heading above a simple instruction~짧은 허구 비상 제목과 그 아래 단순한 안내',
  'notice|within|screen|The heading and instruction remain inside the television card|제목과 지침은 TV 화면 내부에 있다',
  '1980년대 EBS와 1997년 이후 EAS 혼합;경보음 자동 추가', 'CONELRAD·EBS의 세부 시대·제도를 동일시하지 않는다. 이 카드는 일반적인 저술 그래픽이며 사료 복원은 아니다.', 'S13,S11', mode='proxy')
c([43,44,23], '지역 경보의 계층적 레이아웃', 'broadcast_graphics', 'text_carrier,narrative_clue',
  'card:a rectangular alert card~직사각형 경보 화면;area:a short fictional area name in a header~머리말에 적힌 짧은 허구 지역명;message:a separate short event message below it~그 아래 분리된 짧은 사건 안내',
  'area|above|message|The area header appears above the event message|지역 머리말이 사건 안내 위에 있다;message|within|card|The message is confined to the alert card|안내 문구는 경보 화면 안에 있다',
  'SAME 데이터와 주의 환기 음을 동일시;모든 EAS가 동일 레이아웃이라는 주장', '화면은 저술한 예다. 실제 경보 기능·음원·전송 프로토콜 성공을 평가하지 않는다.', 'S12,S13', mode='proxy', priority='P0')
c([45], '텔레텍스트의 문자 격자', 'broadcast_graphics', 'text_carrier,presentation_style',
  'page:a black television information page~검은 TV 정보 화면;grid:rows of blocky colored letters aligned in a rigid grid~고정 격자로 정렬된 각진 컬러 글자 행;number:a small three-digit page marker at the top~상단의 작은 세 자리 페이지 표시',
  'grid|within|page|The colored text occupies a rigid grid within the page|컬러 문자는 페이지 안의 고정 격자를 차지한다;number|above|grid|The page marker sits above the text rows|페이지 표시는 문자 행 위에 있다',
  '현대 웹 UI;Ceefax를 모든 텔레텍스트의 보통명으로 사용', '격자 규격과 실제 Ceefax 화면의 정확한 재현은 별도 참고 자료가 필요하다.', 'S14', mode='proxy', priority='P0')
c([46], '화면 안의 프레임 주소', 'playback_raster', 'text_carrier,narrative_clue',
  'raster:a recorded image with a visible lower edge~하단 경계가 보이는 기록 영상;code:a single small timecode in HH:MM:SS:FF form~시·분·초·프레임 형식의 작은 타임코드 하나',
  'code|overlaid_on|raster|The timecode is burned into the lower recorded image|타임코드는 기록 영상 하단 안에 겹쳐 있다',
  '달력 날짜;VCR 경과 카운터;임의 숫자 반복을 시간 역행으로 통과', '표시 예시는 프레임 주소의 외형이다. 실제 타임베이스·순서·시간 역행은 별도 검증한다.', 'S01,S10', mode='proxy', priority='P0')
c([34,46], 'VCR 경과 카운터', 'playback_raster', 'text_carrier,image_artifact',
  'raster:a single playback image~재생 영상 하나;counter:a small 00:12:34 counter beside PLAY~PLAY 옆의 작은 00:12:34 카운터',
  'counter|overlaid_on|raster|The counter belongs to the playback overlay|카운터는 재생 영상의 표시층에 속한다',
  '프레임 주소로 해석;달력 날짜로 해석', '정지 카운터가 실제 경과 시간이나 원본 길이를 증명하지 않는다.', 'S01,S10', mode='proxy')
c([48], '트래킹 오류와 가로 잡음 띠', 'playback_signal', 'image_artifact',
  'raster:a recognizable playback image~대상을 알아볼 수 있는 재생 영상;band:a broad horizontal band of irregular noise~불규칙한 잡음의 넓은 가로 띠',
  'band|occludes|raster|The noise band obscures one horizontal portion of the playback image|잡음 띠가 재생 영상의 한 가로 구간을 가린다',
  '등간격 주사선;카메라 동작 추적;블록 압축', '띠 외형은 묘사할 수 있지만 실제 헤드 정렬 불량이라는 원인은 정지 이미지로 확정하지 않는다.', 'S02,S01', priority='P0')
c([49], '드롭아웃의 짧은 수평 정보 결손', 'playback_signal', 'image_artifact',
  'raster:an otherwise readable recorded image~대체로 읽을 수 있는 기록 영상;streaks:a few short thin white or black horizontal streaks~짧고 가는 흰색 또는 검은색 가로 줄 몇 개',
  'streaks|interrupt|raster|The short streaks interrupt local picture information|짧은 줄이 영상 일부의 정보를 끊는다',
  '화면 전체의 눈보라 잡음;종이 긁힘;물리 테이프의 색 띠', '짧게 나타났다가 사라지는 시간성은 프레임 연속 자료가 필요하다.', 'S03', priority='P0')
c([50], '영상 하단의 헤드 전환 흔적', 'playback_signal', 'image_artifact',
  'raster:a complete captured playback raster including its lower edge~아래 경계까지 담긴 완전한 재생 래스터;noise:a thin irregular distortion strip at the bottom~맨 아래의 가늘고 불규칙한 왜곡 띠',
  'noise|along_bottom_of|raster|The distortion strip stays at the bottom edge of the captured raster|왜곡 띠는 캡처 래스터 맨 아래 경계에 있다',
  '화면 중앙의 두꺼운 잡음 띠;항상 무지개색이라는 의무', '출처는 하단 위치를 지원한다. 실제 헤드 전환·시간 동작은 이 정지 외형만으로 입증하지 않는다.', 'S01,S10', priority='P0')
c([51], '시간축 오차의 수직선 휨', 'playback_signal', 'image_artifact',
  'raster:a recorded doorway with recognizable vertical jambs~수직 문틀을 알아볼 수 있는 기록 영상;edge:one jamb visibly bending sideways near the top~상단 가까이에서 옆으로 꺾이는 문틀 윤곽',
  'edge|distorted_within|raster|The jamb bends within the recorded picture while the outer frame stays rectangular|바깥 프레임은 직사각형인 채 기록 화면 속 문틀이 휜다',
  '실제 휜 문;광각 렌즈;초자연적 건축으로 자동 해석', '저술한 왜곡 예다. 실제 시간축 오류의 원인은 재생·신호 비교로 확인한다.', 'S04', priority='P0')
c([52], '수직 롤의 분할 프레임 외형', 'playback_signal', 'image_artifact',
  'upper:an upper image segment ending abruptly~갑자기 끊긴 위쪽 영상 조각;lower:a displaced continuation of the same picture~위치가 밀린 같은 영상의 연속 부분;gap:a horizontal blank interval between them~두 부분 사이의 가로 빈 구간',
  'gap|separates|upper|A horizontal blank interval borders the upper segment|가로 빈 구간이 위쪽 조각과 맞닿는다;lower|below|gap|The displaced continuation appears below the blank interval|밀린 연속 영상이 빈 구간 아래에 있다',
  '분할 화면 UI;정지 외형을 실제 롤 움직임으로 합격', '움직임·동기 상실은 시퀀스에서만 판정한다.', 'S10', mode='proxy')
c([53], '색 번짐과 밝기 윤곽', 'playback_signal', 'image_artifact',
  'letter:a saturated red block letter against a neutral field~중성 바탕 위의 채도 높은 빨간 각진 글자;bleed:a soft red spread extending beyond its readable luminance edge~읽을 수 있는 밝기 윤곽 밖으로 번진 부드러운 빨간색',
  'bleed|extends_beyond|letter|The red color spreads beyond the letter edge|빨간색이 글자 윤곽 밖으로 번진다',
  '단순 초점 흐림;위치가 일정하게 밀린 Y/C 지연;렌즈 색수차', '색 번짐의 외관과 합성·전송·기록 과정의 원인은 분리한다.', 'S11,S10', priority='P0')
c([54], '색과 밝기 경계의 위치 어긋남', 'playback_signal', 'image_artifact',
  'edge:a crisp high-contrast graphic edge~또렷한 고대비 그래픽 윤곽;color:a colored contour displaced slightly to one side~한쪽으로 조금 밀린 채색 윤곽',
  'color|offset_from|edge|The color contour is laterally offset from the luminance edge|채색 윤곽이 밝기 윤곽에서 옆으로 어긋나 있다',
  '모든 RGB 분리를 Y/C 지연이라 단정;색 번짐;프리즘', '픽셀은 어긋남을 보여 줄 뿐 Y/C 시간 지연 자체의 측정이 아니다.', 'S05', priority='P0')
c([55], '고채도 경계의 도트 크롤 외형', 'composite_signal', 'image_artifact',
  'border:a boundary between two saturated flat color areas~채도 높은 두 단색 영역의 경계;dots:a tight row of alternating bright and dark beads~밝고 어두운 점이 교차하는 촘촘한 열',
  'dots|along|border|The beaded pattern follows the saturated boundary|점 열이 고채도 경계를 따라 놓인다',
  '화면 전체 입자;디지털 사각 블록;움직임 주장', '정지 도트 패턴은 제안 가능하다. crawl 움직임과 합성 신호 원인은 검증하지 않는다.', 'S06', mode='proxy', priority='P0')
c([56], '방송 수신의 좌우 겹상', 'transmission', 'image_artifact',
  'primary:a strong primary doorway contour~선명한 원래 문 윤곽;echo:a fainter copy of that contour shifted horizontally~가로로 밀린 같은 윤곽의 옅은 복제',
  'echo|horizontal_echo_of|primary|The faint copy repeats the same contour at a horizontal offset|옅은 복제가 같은 윤곽을 가로로 어긋나게 반복한다',
  '렌즈 반사 고스트 원반;귀신 형상;카메라 잔광 꼬리', '외형은 겹상이다. 반사 RF 경로·신호 지연은 추가 증거가 필요하다.', 'S07', priority='P0')
c([56,59], '관형 카메라 잔광의 꼬리', 'capture', 'image_artifact,motion_rendering',
  'source:a bright compact light against a darker field~어두운 바탕 위의 작고 밝은 광원;trail:a fading elongated trace extending from the light~광원에서 이어지는 점차 옅어지는 긴 흔적',
  'trail|extends_from|source|The fading trace is attached to the bright source|옅어지는 흔적은 밝은 광원에 이어져 있다',
  '좌우 동일 윤곽 겹상;렌즈 플레어 구슬;지속 시간 주장', '잔광처럼 보이는 형태만 제안한다. 실제 관형 카메라·이동 방향·잔류 시간은 미입증이다.', 'S08', mode='proxy')
c([58], '움직이는 경계의 인터레이스 빗살', 'digitization', 'image_artifact',
  'edge:a diagonal arm silhouette in a recorded frame~기록 프레임 속 대각선 팔 실루엣;teeth:fine alternating horizontal teeth restricted to that edge~그 윤곽에 한정된 교대 가로 빗살',
  'teeth|along|edge|The alternating horizontal teeth interrupt the arm contour|교대 가로 빗살이 팔 윤곽을 끊는다',
  '모든 가로선을 인터레이스라 부름;직물 줄무늬', '정지 프레임은 빗살 외형을 보여 준다. 실제 필드 시간차는 연속 필드 대조가 필요하다.', 'S10', mode='proxy', priority='P0')
c([59], '밝은 부분의 국소 팽창', 'capture_or_display', 'image_artifact',
  'lamp:a small bright lamp in a dark recorded room~어두운 기록 영상 속 작은 밝은 램프;halo:a locally expanded white region around the lamp~램프 주변에서 국소적으로 커진 흰 영역',
  'halo|surrounds|lamp|The expanded bright region stays centered on the lamp|커진 밝은 영역이 램프를 중심으로 둘러싼다',
  '화면 전체 안개;광원 없는 무작위 발광;CRT 원인 확정', '밝기 팽창의 외형이다. 카메라·표시장치·후처리의 어느 원인인지는 확정하지 않는다.', 'S08', mode='proxy')
c([60], '영상 가장자리의 크롭 비교', 'display', 'format,image_artifact',
  'full:a labeled full-frame reference view with corner marks~모서리 표시가 있는 전체 프레임 참고 화면;crop:a second view of the same image with outer marks cut off~바깥 표시가 잘린 같은 영상의 두 번째 화면',
  'crop|cropped_version_of|full|The second view removes only the outer edges of the reference image|두 번째 화면은 참고 영상의 가장자리만 잘라낸다',
  '단독 프레임에서 overscan 단정;비교 없는 숨겨진 정보 복원', '비교 패널의 관계만 평가한다. 실제 TV의 오버스캔 양이나 원본 진위를 증명하지 않는다.', 'S01,S10', mode='proxy')
c([61], '복제 세대 손실의 비교 표본', 'copy_chain', 'presentation_style,image_artifact',
  'first:a relatively sharp reference image~비교적 선명한 참고 영상;later:a second matching composition with softer edges and more noise~같은 구도에 윤곽이 더 무르고 잡음이 많은 두 번째 영상',
  'later|same_composition_as|first|Both panels preserve the same subject and composition|두 패널은 같은 피사체와 구도를 유지한다',
  '어두운 사진이면 복제 손실로 판정;실제 세대 수 추정', '저술한 비교 외형이며 실제 복제 이력은 메타데이터·원본이 필요하다.', 'S01,S06', mode='proxy')
c([62], '수신 눈보라 잡음', 'reception', 'image_artifact',
  'screen:a bounded display raster~경계가 보이는 화면 래스터;noise:dense irregular monochrome speckles~조밀하고 불규칙한 흑백 점무늬',
  'noise|fills|screen|The irregular speckles fill the display raster|불규칙 점무늬가 화면 래스터를 채운다',
  '모든 VHS는 항상 static;필름 입자;피부 점무늬', '잡음의 실제 수신 원인이나 소리는 외형으로 입증하지 않는다.', 'S01', priority='P0')
c([63], '필름 입자와 비디오 잡음의 분리', 'film_capture', 'grain_profile,image_artifact',
  'image:a continuous-tone photographed image~연속 계조의 촬영 영상;grain:fine irregular non-grid grain over its tones~계조 위에 퍼진 미세하고 격자가 아닌 입자',
  'grain|distributed_over|image|The fine grain follows the image tones without block-grid organization|미세한 입자가 블록 격자 없이 영상 계조에 분포한다',
  '자기테이프 가로 드롭아웃;픽셀 블록;모든 장르에 강제', '필름 유래라는 실제 인과·현상 조건은 입증하지 않는다. 필름→방송→테이프 경로가 선언된 경우 다른 흔적과 공존 가능하다.', 'S10', mode='proxy')
c([63], '필름 흠집의 방향성', 'film_carrier', 'image_artifact',
  'image:a recorded photographic image~기록된 사진 영상;scratch:a narrow vertical irregular pale scratch~가늘고 불규칙한 세로 밝은 흠집',
  'scratch|crosses|image|The vertical scratch crosses the recorded image|세로 흠집이 기록 영상을 가로지른다',
  '헤드 전환 하단 띠;균일 CRT 주사선', '손상 원인과 매체가 반드시 필름이었다는 사실은 외형만으로 확정하지 않는다.', 'S10', mode='proxy')
c([64], '암부 디테일 손실', 'tone_transfer', 'exposure,image_artifact',
  'room:a room with midtone furniture still readable~중간 밝기의 가구는 읽을 수 있는 방;shadow:a localized dark region losing internal texture~내부 질감이 사라진 국소 어두운 영역',
  'shadow|within|room|The dark region loses detail while adjacent midtones remain readable|이웃 중간 계조는 읽히는 채 어두운 영역의 디테일이 사라진다',
  '단순 밤;검은 괴물 존재를 통과;모든 것을 불가시로 처리', '손실 영역 속 물체·생물은 통과시키지 않는다. 핵심 성분이 가려지면 UNOBSERVABLE_NOT_PASS다.', 'S10', priority='P0')
c([64], '하이라이트 디테일 손실', 'tone_transfer', 'exposure,image_artifact',
  'scene:a scene with readable surrounding midtones~주변 중간 계조가 읽히는 장면;window:a bright window reduced to a flat white patch~평평한 흰 영역이 된 밝은 창',
  'window|within|scene|The window loses internal detail while the surrounding scene remains legible|주변 장면은 읽히는 채 창 내부 디테일이 사라진다',
  '국소 blooming과 같은 개념;흰 존재의 정체를 입증', '밝은 부분의 정보 손실을 평가할 뿐 그 뒤 내용은 추정하지 않는다.', 'S10', priority='P0')
c([65], '디지털 블록 압축의 경계', 'digital_codec', 'image_artifact',
  'raster:a digitally transferred picture~디지털로 옮긴 영상;blocks:rectangular blocks of uneven color across a local region~국소 영역의 불균일한 직사각형 색 블록',
  'blocks|partition|raster|The local picture region breaks into rectangular blocks|영상 일부가 직사각형 블록들로 나뉜다',
  'VHS 고유 손상;도트 크롤;datamoshing 시간 동작', '디지털 재압축 경로가 선언된 장면에만 제안한다. 정확한 코덱·손상 기법은 미입증이다.', 'S10', mode='proxy', priority='P0')
c([26], '일상 홈비디오의 촬영 프레임', 'capture_context', 'capture_context,composition',
  'room:an ordinary domestic living room~평범한 가정의 거실;adults:two adults loosely framed beside a table~탁자 옆에서 느슨하게 프레이밍된 성인 두 명',
  'adults|within|room|The adults remain embedded in the ordinary living room|성인들이 평범한 거실 안에 자리한다',
  '자동 괴물·피해·가족관계;VHS 장르 전체를 같은 방으로 고정', '느슨한 프레임은 창작 제안이다. 가족관계·촬영 날짜·촬영 동의는 별도 맥락이다.', 'S31', mode='proxy')
c([27], '고정 감시카메라의 높은 시야', 'capture_context', 'apparatus_pov,capture_configuration',
  'room:a complete room seen from a high corner~높은 모서리에서 보이는 방;adult:one adult small within the fixed wide view~고정 광각 구도 안에서 작게 보이는 성인 하나',
  'adult|within|room|The high corner view contains the adult and surrounding empty floor|높은 모서리 시야가 성인과 주변 빈 바닥을 함께 담는다',
  '전지적 움직이는 카메라;감시만으로 비동의·관음 확정', '고정 시점의 외형이다. 실제 카메라의 고정 지속·동의·감시 의도는 미입증이다.', 'S31', mode='proxy', priority='P0')
c([16,18,20], '공익·절차 안내의 시각 문법', 'instructional_format', 'presentation_style,text_carrier',
  'card:a plain instructional card~단순한 지침 화면;icons:two simple action pictograms~단순한 행동 그림 두 개;steps:two short numbered instructions below the pictograms~그림 아래의 짧은 번호 지침 두 개',
  'icons|above|steps|The pictograms sit above the matching numbered instructions|그림이 대응하는 번호 지침 위에 있다;steps|within|card|Both instructions belong to the same card|두 지침은 같은 화면에 속한다',
  '공식 기관 보증;안내가 실제 안전하다는 주장', '교육 목적·권위·신뢰·실제 안전성은 그래픽의 외형과 다르다.', 'S11,S24', mode='proxy')
c([19,20,127], '사내 교육물의 장비-절차 관계', 'instructional_format', 'presentation_style,procedure_step',
  'equipment:a generic industrial console~일반 산업 제어반;diagram:a small numbered diagram of the same console~같은 제어반의 작은 번호 도해;card:a plain training panel~단순한 교육 패널',
  'diagram|depicts|equipment|The diagram visibly matches the console beside it|도해가 옆의 제어반과 시각적으로 대응한다;diagram|within|card|The numbered diagram is printed on the training panel|번호 도해는 교육 패널 안에 인쇄되어 있다',
  '기업 존재만으로 악행·사고 은폐 확정;원작 회사 로고 자동 복제', '교육물의 용도 외형이다. 기업의 의도·책임은 기록·서사로 남긴다.', 'S25,S23', mode='proxy')
c([21,24], '교육 방송의 친근한 마스코트 도해', 'instructional_format', 'presentation_style,text_carrier',
  'card:a simple classroom broadcast card~단순한 교실 방송 화면;mascot:a cheerful original cartoon mascot~밝은 표정의 독자적인 만화 마스코트;diagram:a plain labeled learning diagram~단순한 라벨 학습 도해',
  'mascot|beside|diagram|The mascot is placed next to the learning diagram|마스코트가 학습 도해 옆에 있다;diagram|within|card|The diagram belongs to the broadcast card|도해가 방송 화면 안에 있다',
  '어린이 프로그램에 실제 아이·학대 자동 추가;고유 캐릭터 복제', '대상의 연령·학대·세뇌·발화 내용은 외형으로 확정하지 않는다.', 'S23,S11', mode='proxy')
c([22,138], '자연사 도해와 서식지의 연결', 'instructional_format', 'presentation_style,narrative_clue',
  'specimen:an invented nonhuman organism in profile~옆모습의 독자적인 비인간 생물;habitat:a small habitat inset showing the same organism~같은 생물이 담긴 작은 서식지 삽화;sheet:a plain natural-history plate~단순한 자연사 도판',
  'habitat|depicts|specimen|The habitat inset depicts the same organism as the main study|서식지 삽화가 주 도해와 같은 생물을 그린다;specimen|within|sheet|The organism is framed as a study on the plate|생물이 도판 안의 관찰 대상으로 놓인다',
  '실제 종 분류;모든 생물을 Woodcrawler로 통칭;먹이사슬 인과 자동 판정', '허구 생물의 저술 도해다. 실제 생물학·침입·전염·생활사는 미입증이다.', 'S23', mode='proxy')
c([25], '광고의 약속과 작은 각주', 'commercial_format', 'text_carrier,presentation_style',
  'product:a generic boxed product~일반 상자 제품;headline:a short large promise beside the product~제품 옆의 짧고 큰 약속 문구;footnote:a small separate disclaimer underneath~그 아래 분리된 작은 각주',
  'headline|beside|product|The large promise sits beside the product|큰 약속 문구가 제품 옆에 있다;footnote|below|headline|The smaller disclaimer sits below the promise|작은 각주가 약속 문구 아래에 있다',
  '각주가 작으면 실제 기만으로 판정;광고=호러 자동 연결', '기만·위험·부작용은 내용과 서사의 문제이며 크기 차이만으로 확정하지 않는다.', 'S25,S23', mode='proxy')
c([28,5], '증거물 번호와 기록 매체', 'archive_format', 'prop_placement,text_carrier',
  'tape:a sealed generic tape carrier~봉인된 일반 테이프 지지체;tag:a short evidence number on a custody tag~보관 탭의 짧은 증거물 번호;file:a nearby incident folder repeating that number~같은 번호가 적힌 옆의 사건 문서철',
  'tag|attached_to|tape|The numbered tag is attached to the sealed carrier|번호 탭이 봉인된 지지체에 붙어 있다;file|matches_id_of|tag|The folder repeats the same evidence number|문서철이 같은 증거물 번호를 반복한다',
  '공식 조사 진위;기밀과 실제 사건을 외형만으로 확정', '보관 관계의 시각 제안이다. 진짜 증거·사건 책임·원본성은 입증하지 않는다.', 'S21,S31', mode='proxy')
c([29], '의료 기록의 피험자-관찰 화면', 'clinical_format', 'capture_context,narrative_clue',
  'adult:a fully clothed adult seated beside an examination table~진찰대 옆에 앉은 옷을 입은 성인;chart:a neutral observation chart with a subject number~피험자 번호가 적힌 중립 관찰표',
  'chart|beside|adult|The neutral observation chart is visible beside the adult|중립 관찰표가 성인 옆에 보인다',
  '의료 장비만으로 비윤리성·동의·임신·진단 확정', '기록 형식의 외형만 제안한다. 의료 상태·생사·동의는 추론하지 않는다.', 'S30', mode='proxy')
c([30], '인터뷰의 인물과 녹음 장치', 'interview_format', 'capture_context,prop_placement',
  'adult:one seated adult seen in a medium interview view~중간 거리 인터뷰 구도의 앉은 성인;microphone:a small microphone on the table~탁자 위의 작은 마이크',
  'microphone|in_front_of|adult|The microphone sits in front of the seated adult|마이크가 앉은 성인 앞에 있다',
  '표정으로 진술 진위 판정;녹음 목소리의 존재를 통과', '증언 내용·불일치·침묵은 별도의 음성·텍스트·시퀀스 증거가 필요하다.', 'S21', mode='proxy')
c([31], '실종 공고의 사진-정보 묶음', 'bulletin_format', 'text_carrier,narrative_clue',
  'poster:a plain fictional missing-person bulletin~단순한 허구 실종 공고;portrait:a generic adult headshot~일반 성인 얼굴 사진;details:a short identifying block next to the portrait~사진 옆의 짧은 식별 정보 묶음',
  'portrait|within|poster|The adult portrait is printed within the bulletin|성인 사진이 공고 안에 인쇄되어 있다;details|beside|portrait|The identifying block sits beside the portrait|식별 정보가 사진 옆에 있다',
  '실제 실종 상태·정체성 입증;자세한 개인정보 자동 생성', '허구 공고 레이아웃이다. 신원·실종·범죄 사실은 주장하지 않는다.', 'S31', mode='proxy')
c([80,81], '방 안에서 재생되는 극중 매체', 'diegetic_relation', 'composition,prop_placement',
  'tv:a television with a visible enclosing bezel~둘러싼 베젤이 보이는 TV;picture:a smaller recorded room shown inside its screen~TV 화면 안에 보이는 더 작은 기록된 방;viewer:an adult seated outside the television image~TV 영상 바깥에 앉은 성인 시청자',
  'picture|within|tv|The recorded room is contained inside the television screen|기록된 방은 TV 화면 안에 들어 있다;viewer|outside|picture|The viewer remains in the room outside the recorded image|시청자는 기록 영상 바깥의 방에 있다',
  '글로벌 오버레이와 극중 TV 혼합;TV 내부 인물과 실제 시청자 소유자 합침', '두 공간의 가시 관계만 제안하며 액자 서사의 시간 순서까지 입증하지 않는다.', 'S31,S21', priority='P0')
c([82,129], '서로 다른 보관 표기', 'archive_relation', 'text_carrier,narrative_clue',
  'tape:a tape sleeve with a short date label~짧은 날짜 라벨이 있는 테이프 케이스;file:a matching catalogue card with a different date~다른 날짜가 적힌 대응 목록 카드',
  'file|contradicts_label_of|tape|The two visible date labels disagree|두 곳에 보이는 날짜 표기가 다르다',
  '오타를 자동 은폐·거짓말로 판정;역사 위조 확정', '불일치만 가시화한다. 누가 왜 바꿨는지·어느 기록이 참인지는 정하지 않는다.', 'S21', mode='proxy')
c([83,85], '기록 번호의 빈 자리', 'archive_relation', 'prop_placement,narrative_clue',
  'shelf:a row of labeled tape slots~라벨이 붙은 테이프 보관 칸의 줄;gap:one empty slot between occupied neighboring slots~양옆이 채워진 칸 사이의 빈 칸 하나',
  'gap|within|shelf|The empty slot interrupts the otherwise occupied row|빈 칸이 대체로 채워진 보관 줄을 끊는다',
  '빈 칸만으로 삭제·유실·범인 확정;시간 생략 통과', '기록의 빈 자리라는 정황이다. 존재했던 영상·삭제 행위·유실 원인은 미입증이다.', 'S21', mode='proxy')
c([86,93], '반응이 향하는 빈 출입구', 'spatial_attention', 'composition,gaze_target',
  'adult:an adult turning toward a doorway~출입구를 향해 고개를 돌린 성인;doorway:a visible empty doorway occupying a large quiet area~넓고 고요한 영역을 차지한 눈에 보이는 빈 출입구',
  'adult|looks_toward|doorway|The adult looks toward the empty doorway|성인이 빈 출입구를 바라본다',
  '반드시 괴물 추가;오프스크린 존재를 픽셀 합격;소리의 원인 확정', '보이는 것은 빈 공간과 시선이다. 공포 반응·소리·화면 밖 존재는 별도 맥락이다.', 'S23,S24', priority='P0')
c([87], '서로 충돌하는 방송 그래픽 층', 'broadcast_relation', 'image_artifact,text_carrier',
  'base:a recognizable original station graphic~알아볼 수 있는 원래 방송국 그래픽;intrusion:a different abrupt rectangular graphic overlapping part of it~일부에 겹친 갑작스러운 별도 직사각형 그래픽',
  'intrusion|overlaps|base|The distinct graphic covers only part of the station image|다른 그래픽이 방송국 영상 일부만 덮는다',
  '단순 PIP를 실제 탈취로 판정;자막·부서진 화면과 동일시', '정지 합성은 충돌하는 층을 보인다. 실제 신호 탈취·원래 방송·침입 주체는 시퀀스와 설정이 필요하다.', 'S11,S27', mode='proxy', priority='P0')
c([88,90], '동일 상황에 대한 반대 지침', 'instruction_relation', 'text_carrier,concept_tension',
  'left:a fictional notice headed KEEP THE DOOR CLOSED~KEEP THE DOOR CLOSED라는 허구 안내;right:a matching notice headed OPEN THE DOOR~OPEN THE DOOR라는 대응 안내;door:a single closed door between the notices~두 안내 사이의 닫힌 문 하나',
  'left|beside|door|The closed-door notice is attached beside the same door|닫힌 문 지침이 같은 문 옆에 붙어 있다;right|beside|door|The open-door notice addresses the same door|열린 문 지침도 같은 문을 대상으로 한다',
  '서로 다른 조건부 안내를 모순으로 오판;판독 불가 텍스트 합격', '문구의 논리적 충돌은 보이는 텍스트를 읽어 확인한다. 어느 지침이 참인지는 별도 서사다.', 'S24,S11', mode='proxy', priority='P0')
c([89,130], '안전 표식과 막힌 출구', 'instruction_relation', 'narrative_clue,concept_tension',
  'sign:a short fictional EXIT arrow~짧은 허구 EXIT 화살표;door:a door visibly blocked by a rigid barrier~단단한 장벽으로 막힌 문',
  'sign|points_to|door|The EXIT arrow points directly toward the blocked door|EXIT 화살표가 막힌 문을 직접 가리킨다',
  '모순만으로 살해 의도 확정;격리 실패 사건을 자동 판정', '안내와 가시 상태의 불일치다. 지침의 거짓·고의성·실제 피해는 미입증이다.', 'S24', mode='proxy')
c([96,117], 'TV 화면 경계 밖으로 이어진 형태', 'diegetic_boundary', 'object_structure,spatial_relation',
  'tv:a television with a complete visible bezel~베젤 전체가 보이는 TV;shape:one continuous nonhuman ribbon-like form crossing its screen edge~화면 경계를 가로지르는 연속된 비인간 띠 모양 형태',
  'shape|crosses_boundary_of|tv|The continuous form crosses from inside the screen over its bezel into the room|연속된 형태가 화면 안에서 베젤을 넘어 방으로 이어진다',
  '단순 화면 속 전신 사진;시청자 반응으로 실제 저주 입증', '경계 침범의 저술 형상이다. 실제 저주·시청자 인식·미래 예측은 입증하지 않는다.', 'S31', priority='P0')
c([97,98], '인간형 인형의 국소 불일치', 'subject_appearance', 'facial_geometry,object_structure',
  'head:a humanlike mannequin head with ordinary face proportions~일반 얼굴 비율의 인간형 마네킹 머리;eyes:two rigid glass eyes set into that face~얼굴 안의 단단한 유리 눈 두 개;joint:a narrow mechanical seam below one cheek~한쪽 뺨 아래의 가는 기계 이음매',
  'eyes|embedded_in|head|The glass eyes remain set in the humanlike face|유리 눈이 인간형 얼굴 안에 자리한다;joint|within|head|The cheek seam interrupts an otherwise familiar face surface|뺨 이음매가 익숙한 얼굴 표면 일부를 끊는다',
  '모든 괴물 얼굴=uncanny valley;인간 외모를 비인간으로 판정', '인공물의 외형을 제안한다. 관객의 불쾌감·보편적 반응은 별도 평가다.', 'S20', mode='proxy')
c([100], '얼굴처럼 읽히는 물체 배열', 'perceptual_proxy', 'composition,object_structure',
  'wall:a worn wall surface~낡은 벽 표면;marks:two small upper marks~위쪽 작은 얼룩 두 개;lower:a single curved lower stain~아래쪽의 휜 얼룩 하나',
  'marks|on|wall|The two small marks sit on the wall surface|작은 얼룩 두 개가 벽 표면에 있다;lower|on|wall|The curved stain also lies on the wall|휜 얼룩도 같은 벽 표면에 있다;lower|below|marks|The curved stain lies below the two marks in a face-like arrangement|휜 얼룩이 두 얼룩 아래에 있어 얼굴 같은 배열을 이룬다',
  '실제 얼굴·괴물 의무;형상 지각의 보편성 확정', '배열만 저술한다. 지각 현상의 보편성·실제 생명체는 입증하지 않는다. 독립 심리 원전 대조는 후속이다.', 'S20', mode='proxy')
c([110,111,112], '서로 다른 두 인물의 외형 대응', 'subject_relation', 'character_contrast,composition',
  'first:one adult on the left with a distinct jacket and haircut~특정 재킷과 머리 모양의 왼쪽 성인;second:a second adult on the right matching those visible features~같은 가시 특징을 지닌 오른쪽의 별도 성인',
  'second|visually_matches|first|The two separate adults visibly share the same jacket and haircut|별개의 두 성인이 같은 재킷과 머리 모양을 보인다',
  '거울상을 두 인물로 통과;쌍둥이·사칭·대체 사건 자동 확정', '외형 유사성만 평가한다. 혈연·정체·교체·모방 능력은 설정이다.', 'S24', mode='proxy', priority='P0')
c([113], '외피와 그 아래 지지 구조', 'subject_structure', 'object_structure,material_form',
  'shell:a human-shaped synthetic face shell~인간 얼굴 모양의 합성 외피;support:a visibly different rigid support under a lifted shell edge~들린 외피 가장자리 아래 보이는 다른 재질의 단단한 지지 구조',
  'support|under_edge_of|shell|The rigid support is visible beneath the lifted synthetic shell|들린 합성 외피 아래로 단단한 지지 구조가 보인다',
  '실제 사람의 피부와 학대 자동 연결;단순 가면을 교체 인간으로 판정', '인공 외피의 가시 구조다. 실제 인체·생명·교체 사건은 주장하지 않는다.', 'S30,S24', mode='proxy')
c([114,115], '애니매트로닉의 외피와 기구', 'subject_structure', 'object_structure,subject',
  'mascot:an original large mascot shell on a stage~무대 위의 독자적인 큰 마스코트 외피;panel:an open access panel in its side~옆면에 열린 점검 패널;linkage:a visible metal linkage inside the opening~개구부 안에 보이는 금속 연결 기구',
  'panel|within|mascot|The access panel opens within the mascot shell|점검 패널이 마스코트 외피 안에서 열린다;linkage|inside|panel|The linkage is visible through the access opening|점검 개구부를 통해 연결 기구가 보인다',
  '단순 천 인형;항상 살인·빙의·시체 포함;특정 작품 캐릭터 자동 복제', '기계 구조는 보이지만 실제 운동·자율성·내부의 생사는 미입증이다.', 'S38,S20', mode='proxy', priority='P0')
c([118,119,139,141], '숙주와 부착 생물의 접점', 'biological_relation', 'anatomical_connection,contact_point',
  'host:a fictional nonhuman host organism~허구의 비인간 숙주 생물;growth:a distinct small growth attached at one visible junction~한 가시 접점에 붙은 별개의 작은 생장체',
  'growth|attached_to|host|The growth remains visibly joined to the host at one junction|생장체가 한 접점에서 숙주에 이어져 있다',
  '옆에 놓인 생물을 기생으로 판정;실제 감염·생활사·동화 확정', '접점의 외형이다. 기생·전염·의식 흡수의 기능은 생물학 기록·서사가 필요하다.', 'S23,S30', mode='proxy')
c([120], '여러 개체의 같은 자세', 'group_relation', 'body_pose,composition',
  'left:a standing adult on the left with arms held in an unusual position~특이한 팔 자세로 왼쪽에 선 성인;right:a separate adult on the right holding the same arm position~같은 팔 자세로 오른쪽에 선 별개 성인',
  'right|pose_matches|left|The two separate adults show a clearly matching arm posture|별개의 두 성인이 분명히 같은 팔 자세를 보인다',
  '군체 의식 입증;동시성·반복 동작을 한 장으로 통과', '군체 의식·동기화·명령의 존재는 미입증이다.', 'S23', mode='proxy')
c([124], '건축과 유기 구조의 연속', 'architectural_relation', 'location,anatomical_connection',
  'wall:a recognizable masonry wall~알아볼 수 있는 석조 벽;membrane:a layered organic opening embedded in the wall~벽 안에 박힌 층상 유기 개구부;conduit:branching ridges continuing into the masonry~석조로 이어지는 가지 모양 능선',
  'membrane|embedded_in|wall|The organic opening is embedded in the wall plane|유기 개구부가 벽면 안에 박혀 있다;conduit|continues_into|wall|The branching ridges continue into the masonry|가지 모양 능선이 석조로 이어진다',
  '덩굴로 덮인 건물;방 안의 별도 고깃덩어리;소화 기능 확정', '기존 living architecture와 같은 가시 의미면 완전 재사용한다. 생명·의식·수축은 미입증이다.', 'S25,S30', priority='P0')
c([126,129], '삭제선이 남은 접수 문서', 'bureaucratic_relation', 'text_carrier,narrative_clue',
  'form:a plain incident form with a short incident number~짧은 사건 번호가 적힌 단순 접수 양식;stamp:a large CLOSED stamp across a body paragraph~본문 단락에 가로놓인 큰 CLOSED 도장',
  'stamp|overlaps|form|The CLOSED stamp crosses the form body without hiding its incident number|CLOSED 도장이 사건 번호는 남긴 채 양식 본문을 가로지른다',
  '접수 문서만으로 은폐·책임·사망 확정;권위가 실제임을 주장', '문서 상태만 가시화한다. 사건 처리의 정당성·악행은 서사다.', 'S25,S24', mode='proxy')
c([130], '격리 경계와 열린 개구부', 'spatial_relation', 'object_structure,narrative_clue',
  'barrier:a solid partition with a short containment sign~짧은 격리 표시가 붙은 단단한 칸막이;opening:a visible torn opening across the partition~칸막이를 가로질러 난 가시 개구부',
  'opening|breaks|barrier|The opening visibly interrupts the marked partition|개구부가 표시된 칸막이를 끊는다',
  '단순 열린 문으로 탈출 사건 확정;SCP 개체 자동 추가', '경계 손상의 외형이다. 탈출·격리 실패의 시간·원인·주체는 미입증이다.', 'S28,S25', mode='proxy')
c([135,158,159], '가림 뒤에서 본 사적 실내', 'apparatus_relation', 'apparatus_pov,composition',
  'occluder:a dark narrow foreground obstruction~어둡고 좁은 전경 가림물;room:a private domestic room beyond the obstruction~가림물 너머 사적 가정 실내;adult:a fully clothed adult small in the room~실내에 작게 보이는 옷을 입은 성인',
  'occluder|partially_occludes|room|The foreground obstruction partly masks the domestic view|전경 가림물이 가정 실내 시야를 일부 가린다;adult|within|room|The adult remains visible inside the room|성인이 방 안에 보인다',
  '은밀한 시점=비동의·성적 관음 확정;피해자의 몸 노출 자동 추가', '가려진 관찰 시점만 제안한다. 촬영 동의·관찰자의 목적·성적 의미는 추정하지 않는다.', 'S31,S32', mode='proxy', priority='P0')
c([136,102], '기능이 멈춘 실내의 운영 흔적', 'environment', 'location,environment_detail',
  'hall:a mall corridor with closed storefront shutters~가게 셔터가 닫힌 쇼핑몰 복도;directory:a lit directory kiosk in the empty corridor~빈 복도에서 켜진 안내 키오스크',
  'directory|within|hall|The lit directory remains in the corridor between closed storefronts|켜진 안내판이 닫힌 점포 사이의 복도 안에 있다',
  '빈 복도만으로 폐시설·위험·아날로그 호러 판정;백룸 판본 자동 활성화', '운영 흔적과 인적 부재의 외형이다. 실제 폐업·시간 경과·공포 반응은 미입증이다.', 'S21', mode='proxy')
c([137], '연결이 모순되는 공간의 비교 도면', 'spatial_proxy', 'object_structure,spatial_relation',
  'plan:a simple plan of one rectangular room~직사각형 방 하나의 단순 평면도;view:a room view showing an additional doorway absent from the plan~도면에 없는 추가 문이 보이는 방의 시점 화면',
  'view|conflicts_with|plan|The view shows one extra doorway relative to the plan|시점 화면이 도면보다 문 하나를 더 보인다',
  '문 수 불일치를 수학적 비유클리드 공간으로 통과;광각 복도를 무한 공간으로 단정', '도면·영상 불일치만 가시화한다. 수학적 공간 성질·무한성은 입증하지 않는다.', 'S21', mode='proxy')
c([138,22], '생태 분포 지도의 이상 영역', 'ecological_proxy', 'text_carrier,narrative_clue',
  'map:a simple fictional regional map~단순한 허구 지역 지도;zone:a dense branching organic zone over one part of the map~지도 일부에 걸친 조밀한 가지 모양 유기 영역;inset:a specimen inset matching that zone pattern~그 영역 무늬에 대응하는 표본 삽화',
  'zone|within|map|The organic zone occupies one mapped region|유기 영역이 지도 안 한 지역을 차지한다;inset|visually_matches|zone|The specimen inset repeats the branching pattern of the zone|표본 삽화가 영역의 가지 무늬를 반복한다',
  '지도만으로 실제 확산·인체 위험·감염 확정', '허구 도해의 관계다. 시간적 확산·인과·실제 생태 침입은 별도 자료가 필요하다.', 'S23', mode='proxy')
c([139,141,142], '복합 신체의 연결 접점', 'subject_structure', 'anatomical_connection,body_form',
  'torso:a fictional nonhuman central body~허구의 비인간 중심 몸체;limbs:two visibly different limb structures joined to it~몸체에 이어진 서로 다른 두 팔다리 구조',
  'limbs|joined_to|torso|The distinct limb structures share visible junctions with the central body|서로 다른 팔다리 구조가 중심 몸체와 가시 접점을 공유한다',
  '단순 군중 겹침;실제 사람의 변이·유전 질환으로 판정;유혈 필수화', '연결된 허구 외형이다. 변형 과정·여러 인격의 흡수·의학 원인은 입증하지 않는다.', 'S30', mode='proxy')
c([151,114], '장치 내부 인체형 실루엣의 한계', 'enclosure_relation', 'object_structure,prop_placement',
  'cabinet:a fictional upright machine cabinet~허구의 세로 기계 캐비닛;window:a small inspection window in its front~전면의 작은 점검 창;figure:a clothed adult-shaped mannequin visible behind the window~창 뒤로 보이는 옷을 입은 성인형 마네킹',
  'window|within|cabinet|The inspection window belongs to the machine cabinet|점검 창이 기계 캐비닛 안에 있다;figure|behind|window|The adult-shaped mannequin stands behind the window|성인형 마네킹이 창 뒤에 있다',
  '실제 생존자·시체·의식·감금·시체 조종 자동 확정', '가시 실현은 인체형 모형과 외함의 위치 관계다. 원 용어의 감금·생사·조종을 대체하거나 통과시키지 않는다.', 'S30,S38', mode='proxy')
c([168,169,170,171,179], '가려진 정보와 남은 주변 문장', 'document_surface', 'text_carrier,narrative_clue',
  'page:a plain fictional document with several short text lines~짧은 글 여러 줄이 있는 단순 허구 문서;bars:opaque black rectangles covering selected words~일부 단어를 가리는 불투명 검은 직사각형',
  'bars|occlude_words_on|page|The black rectangles cover selected words while surrounding text remains visible|검은 직사각형이 일부 단어만 가리고 주변 문장은 남긴다',
  '검은 가림=인지·밈·항밈 효과 입증;하이라이트 마커와 혼동', '가림의 외형은 정보재해의 효과가 아니다. 네 허구 메커니즘은 문맥에 보존하고 픽셀 사실로 승격하지 않는다.', 'S28', priority='P0')
c([173,174], '축이 있는 스펙트로그램 도해', 'data_visualization', 'text_carrier,presentation_style',
  'plot:a rectangular intensity map with a visible color scale~색 범례가 보이는 직사각형 강도 지도;axes:one time axis and one frequency axis~시간 축 하나와 주파수 축 하나',
  'axes|bound|plot|The plot is bounded by distinct time and frequency axes|도표가 서로 다른 시간 축과 주파수 축으로 둘러싸인다',
  '오디오 파형;SSTV 수신 사진;가짜 그림을 실제 해독으로 통과', '도해의 표현만 평가한다. 숨긴 음성·신호·실제 메시지 복원은 입력 파일과 분석 재현이 필요하다.', 'S16', mode='proxy', priority='P0')
c([175], '수신기와 SSTV 복원 화면', 'radio_image_relation', 'prop_placement,presentation_style',
  'radio:a radio receiver connected by a cable~케이블이 연결된 무선 수신기;computer:a computer showing a single decoded image panel~복원된 정지 영상 패널 하나를 표시하는 컴퓨터;cable:a visible cable between receiver and computer~수신기와 컴퓨터 사이에 보이는 케이블',
  'cable|connects|radio|The cable visibly reaches the radio receiver|케이블이 무선 수신기에 닿아 있다;cable|connects|computer|The same cable reaches the computer input|같은 케이블이 컴퓨터 입력부에 닿아 있다',
  '스펙트로그램=SSTV;케이블 그림=실제 수신 성공', '장비·화면의 가시 구성이다. 실제 SSTV 해독 성공은 오디오 입력과 복원 결과 대조로 검증한다.', 'S17,S18', mode='proxy', priority='P0')
c([176], '모스 부호와 대응 표', 'code_surface', 'text_carrier,narrative_clue',
  'strip:a strip containing separated dots and dashes~구분된 점과 선이 적힌 띠;key:a small neighboring letter-to-code key~옆의 작은 문자-부호 대응표',
  'key|beside|strip|The visible key maps letters to the dot-dash groups|보이는 대응표가 문자를 점·선 묶음에 연결한다',
  '모스는 곧 암호라는 주장;무작위 점선=해독 가능한 메시지', '생성 단계의 정확한 부호는 별도 문자열 검증 대상이다. 암호성·전송·해독은 자동 통과하지 않는다.', 'S18', mode='proxy')
c([177,172], '타임라인에서 분리된 단일 프레임', 'editing_proxy', 'text_carrier,presentation_style',
  'timeline:a row of small video thumbnails~작은 영상 썸네일의 줄;selected:one visibly different thumbnail outlined in the row~줄 안에서 테두리로 표시된 다른 썸네일 하나;preview:a larger preview repeating that thumbnail~그 썸네일을 반복하는 큰 미리보기',
  'selected|within|timeline|The different thumbnail occupies one position in the timeline|다른 썸네일이 타임라인 한 자리를 차지한다;preview|depicts|selected|The enlarged preview repeats the selected thumbnail|큰 미리보기가 선택된 썸네일과 대응한다',
  '정지 화면만으로 역하 인지·노출 시간 판정;정신 통제 효과', '편집 화면의 관계만 제안한다. 한 프레임 삽입·실제 지속 시간은 영상 파일을 검사한다.', 'S21', mode='proxy')
c([178,182], '파일 정보와 영상 날짜의 차이', 'paratext_relation', 'text_carrier,narrative_clue',
  'image:a recorded frame with a short visible date~짧은 날짜가 보이는 기록 프레임;panel:a separate file information panel with another date~다른 날짜가 적힌 별도 파일 정보 패널',
  'panel|beside|image|The file panel sits outside the recorded image|파일 정보 패널이 기록 영상 바깥에 있다',
  '업로드 날짜=촬영 날짜;가짜 메타데이터를 실제 파일 정보로 인정;본문과 주변 텍스트 혼합', '두 날짜의 시각적 차이다. 원본 파일의 실제 메타데이터는 파일 검사로 확인한다.', 'S29,S21', mode='proxy')

# Exactly these records received a full source/binding snapshot during this turn.
# The recommendations below are source review decisions, not native approval.
EXISTING_DECISIONS = {
 'cand_87585d0a3333587a811818ca4e402216': ('reuse_if_compatible', '홈비디오 거실 설정으로만 재사용. VHS 물체·손상 신호 전체의 의미를 맡기지 않는다.'),
 'cand_09dc4590c0f654729757916a5a3501a7': ('refine', 'VHS scanlines and color bleed를 표시 주사선/색 번짐의 독립 실현과 명시적 carrier로 분리한다.'),
 'cand_40412df852a1502d9eefc44e366601a5': ('context_only', '보존 표면 복합 후보다. CRT TV의 가시 구조 전체를 재사용했다고 볼 수 없다.'),
 'cand_50c34ab35e5a59a6ba557d1476ff78d8': ('do_not_broaden', 'text_persistent_world_recovery_scene의 primary 조건을 장르 라벨로 해제하지 않는다.'),
 'cand_99862b5e0d11592dadf9860ad7ca36f5': ('reject_polysemy', 'CME 팽창 추적은 테이프 트래킹 오류와 다른 의미다.'),
 'cand_4bc100634382539f95a82e78e0324be9': ('reject_polysemy', 'VTuber 모션 추적 마커는 비디오 헤드 트랙 추적과 다르다.'),
 'cand_f5a02e6e7c965c508b537b95f8f0fda7': ('do_not_broaden', '홀로그램 표면의 선을 CRT 표시 래스터와 동일시하지 않는다.'),
 'cand_b98c83caa6d45d3699c2a6101f760e28': ('do_not_broaden', '피부 표면의 선은 CRT 화면 owner와 다르다.'),
 'cand_aceaa5a1d9465f5a9e9ded075cefeac0': ('reuse_branch_review', '물리 매체+선택적 재생 영상 dropout 분기다. 전체를 보존하며 선택한 분기의 carrier 조건을 검토한다.'),
 'cand_13d8065131ae521183055d14318faa36': ('reject_polysemy', '광원과 렌즈 축에 정렬된 내부 반사 고스트다. 방송 신호의 수평 윤곽 겹상으로 재태깅하지 않는다.'),
 'cand_d1c18ed396a658ce8b79571391acb58a': ('context_only', '장르 라벨 노출을 화면 구성요소·공포 성공의 증거로 보지 않는다.'),
 'cand_1ef1f3cd1ec75dc5af21ee54752d5561': ('do_not_broaden', 'surveillance-state robot world 설정이다. 일반 CCTV 시점으로 robot world를 불러오지 않는다.'),
 'cand_7943af3de7a658c19ce18178e146322e': ('context_only', '감시 업무와 애정 부재의 설명이다. 고정 CCTV 프레임의 시각 후보를 대체하지 않는다.'),
 'cand_a33a937063c758f6b7d84dd735def7f2': ('do_not_broaden', '제작 도구의 timecode 메모는 화면에 삽입된 타임코드가 아니다.'),
 'cand_f318eda868e45d9cbd49f77d5bd00a98': ('reject_polysemy', 'Low-Chroma Palette는 선택 색 영역의 낮은 채도 관계다. 비디오 색 신호 지연과 다른 의미다.'),
 'cand_43b61efd4d2b578496555d6ee7af9130': ('reject_polysemy', 'Vivid-on-Muted는 피사체와 주변의 채도 차이다. 비디오 색 번짐과 다른 의미다.'),
 'cand_44b6a2aecbdc5a0cb7dffbcde8aa809c': ('reuse_if_compatible', '테마파크 애니매트로닉 subject는 재사용 가능. 기구 접점은 별도 보완한다.'),
 'cand_2d5565650bda5cfbb88d9d9a5876a5c9': ('reuse_if_compatible', '무대 설정은 재사용 후보이며 인형 내부·빙의·가해 사건을 뜻하지 않는다.'),
 'cand_8ed5a9486be65af9b7a3e3d39ca477fb': ('reuse_complete_source', '벽-막-능선의 기존 전체 관계를 우선 재사용. 감축·재태깅·새 동일 후보 등록은 피한다.')
}
