"""Source ledger: paraphrased findings, bounded access, no copied articles."""
ROWS = '''S01|Canadian Conservation Institute: The Digitization of VHS Videotapes, TB31|https://www.canada.ca/en/conservation-institute/services/conservation-preservation-publications/technical-bulletins/digitization-vhs-video-tapes.html|body_selected|VHS/VCR; artifact descriptions and causes|기록 형식·재생 장비·재생 영상의 결함을 구분한다. 트래킹은 띠, 드롭아웃은 짧은 정보 탈락, 헤드 전환 흔적은 영상 아래쪽이라는 위치 차이가 있다.
S02|AVAA: Tracking Error|https://www.avartifactatlas.com/artifacts/tracking_error.html|body|definition and playback adjustment|기록 트랙을 재생 헤드가 따라가지 못하는 오류. 영상의 왜곡과 실제 장치의 원인 진단은 다른 증거다.
S03|AVAA: Video Dropout|https://www.avartifactatlas.com/artifacts/video_dropout.html|body|definition and appearance|짧은 RF 손실이 영상의 밝거나 어두운 선으로 드러날 수 있다. 물리 테이프 표면에 영상 줄을 그리는 뜻이 아니다.
S04|AVAA: Time Base Error|https://www.avartifactatlas.com/artifacts/time_base_error.html|body|timing; flagging/skew/tearing|시간 불안정은 상단 휨·기울기·가로 찢김으로 나타날 수 있다. 모든 가로줄이 같은 오류는 아니다.
S05|AVAA: Y/C Delay Error|https://www.avartifactatlas.com/artifacts/yc_delay_error.html|body|luminance/chrominance alignment|색·밝기 정보의 불일치가 채색 경계의 위치 어긋남으로 보인다. 광학 색수차와 원인이 다르다.
S06|AVAA: Dot Crawl|https://www.avartifactatlas.com/artifacts/dot_crawl.html|body|composite-video boundary artifact|합성 신호의 밝기·색 분리 문제로 고채도 경계에 움직이는 점 열이 생긴다. 정지 점무늬만으로 움직임은 입증하지 못한다.
S07|AVAA: Ghost|https://www.avartifactatlas.com/artifacts/ghost.html|body|offset received image; distinction from image lag|수신 영상의 좌우 겹상은 반사·지연 신호와 관련된다. 같은 낱말의 렌즈 플레어와 카메라 잔상을 분리해야 한다.
S08|AVAA: Image Lag|https://www.avartifactatlas.com/artifacts/image_lag.html|body|camera tube persistence; blooming|관형 카메라의 잔류 영상과 밝은 영역의 팽창을 설명한다. 정지 화면의 꼬리·발광이 지속 시간이나 특정 카메라를 증명하지 않는다.
S09|AVAA: Wow and Flutter|https://www.avartifactatlas.com/artifacts/wow_and_flutter.html|body|slow/fast speed variation|재생 속도 변화가 느리거나 빠른 음높이 흔들림을 만든다. 단순 저음 처리나 정지 이미지의 테이프 모양과 구분한다.
S10|Seattle Municipal Archives: QCTools Manual|https://mediaarea.net/QCTools/Seattle_Municipal_Archives_Manual|body_selected|artifact taxonomy and glossary; interlace/frame|영상 손상을 장치·신호·매체·처리 문맥에서 진단한다. 프레임과 필드를 구분하며, 비슷한 외관의 원인은 재생 비교가 필요하다.
S11|Kris Straub: New horror! Contingency on Local 58|https://www.patreon.com/krisstraub/posts/new-horror-on-58-4114380|creator_body|2016-01-13 production account|창작자는 iMovie·Photoshop·Flash로 방송 그래픽과 번짐을 만들었다고 설명한다. 실제 아날로그 촬영이 장르의 필수 조건은 아니다.
S12|NOAA NWS: EAS Description|https://www.weather.gov/nwr/eas_description|body_selected|purpose and identical EAS/NWR digital protocol|EAS와 NWR는 디지털 프로토콜을 공유한다. EAS를 아날로그 전용 질감이나 단순 경보음으로 취급하면 부정확하다.
S13|NOAA NWS: SAME Technology|https://www.weather.gov/sgf/nwr_same|body|EBS to EAS chronology; county encoding|1997년 1월 1일 EAS가 EBS를 대체했다. 경보의 지역 부호와 사람의 주의를 끄는 소리는 기능이 다르다.
S14|BBC: The BBC Story, 1970s|https://downloads.bbc.co.uk/historyofthebbc/1970s.pdf|body_selected|page 1 Ceefax introduction|1974년 Ceefax 텔레텍스트 도입을 확인했다. 정밀 문자 격자 사양과 종료 시점까지 이 문서로 검증한 것은 아니다.
S15|ITU-R BT.470: Conventional analogue television systems|https://www.itu.int/rec/R-REC-BT.470/en|landing_only|standard title and edition list|아날로그 TV 신호 규격의 명칭·판본만 확인했다. 국가별 세부 규격·수치·파형은 원문 표를 추가 대조해야 한다.
S16|USGS: About the Spectrograms|https://earthquake.usgs.gov/monitoring/spectrograms/about.php|body|frequency/time/amplitude encoding|시간에 따른 주파수 성분을 색으로 표시하는 그래프다. 파형·이미지 전송·실제 해독된 메시지를 같은 것으로 취급하지 않는다.
S17|ARISS: Fram2Ham Tips and Techniques|https://www.ariss.org/tips-and-techniques.html|body_selected|SSTV signal/image reception|SSTV 신호를 받아 정지 이미지를 복원하는 운용을 설명한다. 주파수 분석 그래프 그 자체를 SSTV라 부르면 안 된다.
S18|ARISS SPARKI Radio Experimenters Kit, June 2023|https://ariss-usa.org/wp-content/uploads/2023/06/ARISS-Radio-Kit-Handbook-Current-Version.pdf|body_selected|SSTV activity and radio reception sections|라디오 신호를 받아 SSTV Decode로 이미지를 표시하는 실험이다. 그림만 생성해서 실제 수신·복원 성공으로 평가할 수 없다.
S19|Night Mind Index: project interaction categories|https://www.nightmind.info/index|body_selected|ARG/Interactive Project/Immersive Narrative|운영자가 관객 상호작용의 필요 정도로 프로젝트를 구분한다. 암호가 보인다는 이유만으로 ARG로 판정하지 않는다.
S20|Masahiro Mori: The Uncanny Valley, authorized translation|https://spectrum.ieee.org/the-uncanny-valley|body_selected|original essay introduction and hypothesis|인간 유사성과 친밀감의 관계에 관한 가설이다. 무서운 얼굴 하나로 관객 반응이나 보편적인 불쾌한 골짜기 효과를 입증할 수 없다.
S21|Tam Lines: Isolated Together, Sonic Scope|https://www.sonicscope.org/pub/uooqf9rf/release/3|body_selected|abstract; introduction; hauntology sections|매체를 소비하는 행위와 소리·영상의 질감이 인터넷 호러에서 중요함을 논한다. 모든 작품의 단일 정의나 생성 성공률 근거는 아니다.
S22|Marco Malvestio: The Ghost in the Tape Recorder|https://ojs.unica.it/index.php/between/article/view/6366|abstract_search_only|2025 abstract; body fetch failed|팟캐스트가 라디오·녹음기를 재매개하는 논의의 초록을 확인했다. 65~83쪽 전체 논지·세부 장면은 미독이다.
S23|Remy Abode interview, F Newsmagazine|https://fnewsmagazine.com/2022/02/ghosts-in-the-machine-archiving-the-end-of-the-world-with-gemini-home-entertainment/|creator_interview|2022-02-15; answer paragraphs on creatures, tools and suspense|창작자는 생물학적 재해석·교육 비디오 형식·여운을 남기는 긴장을 설명한다. 기자의 줄거리 요약과 창작자의 직접 답변을 구분했다.
S24|Alex Kister interview, F Newsmagazine|https://fnewsmagazine.com/2022/01/ghosts-in-the-machine-the-fearful-symmetry-of-alex-kisters-the-mandela-catalogue/|creator_interview|2022-01-16; production, religious premises, predictability|창작자의 발견된 영상 감각·권위·종교 모티프·예측 가능성 회피를 읽었다. 작중 진단 M.A.D.의 상세 정의나 모든 후속 판본을 검증하지 않았다.
S25|Trevor Roberts: Mystery Flesh Pit FAQ|https://www.mysteryfleshpitnationalpark.com/about|creator_body|project description and setting paragraphs|허구 그림·글의 멀티미디어 기록물이며, Anodyne이 생물 내부를 관광 시설로 개발했다는 전제를 확인했다. 시설 외형을 실제 생명 기능의 증거로 간주하지 않는다.
S26|Alpine Arts: Lethal Omen|https://alpine-arts.itch.io/lethal-omen|creator_landing|developer page; description; download availability|실제 배포된 연계 게임의 존재를 확인했다. 다운로드·플레이·엔딩 검증은 하지 않았다.
S27|LOCAL58TV: cached community television homepage|https://local58.tv/web20210624dgtl/|creator_body|in-world digital transition notice|작중 WCLV-TV의 디지털 전환 공지를 확인했다. 작품 안의 날짜·기관을 현실 방송 이력으로 읽지 않는다.
S28|SCP Wiki: Glossary of Terms|https://scp-wiki.wikidot.com/glossary-of-terms|body_selected|cognitohazard/infohazard/antimemetic/mimetic entries|지각·간접 정보·전파 억제·모방은 다른 허구적 메커니즘이다. 일반 아날로그 호러의 필수 규칙이나 현실 의학 현상으로 전환하지 않는다.
S29|Henry Jenkins: Transmedia Storytelling 101|https://henryjenkins.org/blog/2007/03/transmedia_storytelling_101.html|author_body|2007 essay; unique contribution across channels|각 매체가 고유한 내용을 제공하는 체계를 설명한다. 같은 이미지를 여러 기기에서 보는 구도는 트랜스미디어의 증거가 아니다.
S30|BFI: 10 great body horror films|https://www.bfi.org.uk/lists/10-great-body-horror-films|critical_body_selected|opening definition; bodily integrity/autonomy|몸의 변형과 통제 상실을 유혈의 양과 구분한다. 세부 신체 변화의 인과·생사·의학 진단은 정지 이미지 밖의 주장이다.
S31|BFI: When videotapes were sinister, Ring|https://www.bfi.org.uk/features/ringu-hideo-nakata-videotapes-lynch-haneke|critical_body_selected|VHS materiality; media crossing; domestic surveillance|매체의 물성과 사적 공간 침입을 연결하는 비평이다. 저주·기록의 동의 여부는 표면 외형만으로 판정할 수 없다.
S32|BFI: 10 great erotic horror films|https://www.bfi.org.uk/lists/10-great-erotic-horror-films|critical_body_selected|opening; Cat People discussion|성적 욕망과 공포가 결합하는 장르적 맥락을 확인했다. 피부 노출·불안한 표정을 동의나 성폭력의 증거로 사용하지 않는다.
S33|BBFC: The Video Recordings Act|https://www.bbfc.co.uk/film-media-resources/legislation/the-video-recordings-act|institution_body_selected|historical video nasties section|Video nasty는 영국의 비디오 유통·검열 논쟁 맥락이다. VHS 괴물의 종류나 자동 시각 스타일로 등록할 개념이 아니다.
S34|ACOG: Reproductive and Sexual Coercion|https://www.acog.org/clinical/clinical-guidance/committee-opinion/articles/2013/02/reproductive-and-sexual-coercion|search_only_body_402|search metadata; body unavailable|문헌 존재만 확인했으며 원문 정의는 미독이다. 생식 강압의 개별 정의 검증은 후속으로 남긴다.
S35|WHO: Child maltreatment|https://www.who.int/news-room/fact-sheets/detail/child-maltreatment|institution_body_selected|definition paragraph only|책임·신뢰·권력 관계에서의 학대와 방임을 구분하는 정의를 확인했다. 상처 사진만으로 관계·가해자·사건을 확정하지 않는다.
S36|SCP Wiki: Guide for Reading|https://scp-wiki.wikidot.com/guide-for-reading|body_selected|no single canon; multiple canons paragraphs|SCP에는 전체를 통괄하는 하나의 캐넌이 없으며 개별 캐넌들이 있다. 다른 설정집도 판본을 구분해서 읽어야 한다는 설계 원칙의 참고 사례다.
S37|Science Museum Group: Cathode ray tube|https://collection.sciencemuseumgroup.org.uk/objects/co8406906/cathode-ray-tube|institution_body|CRT display and computer-memory description|CRT는 표시장치 등 여러 용도의 부품이다. 해당 소장품은 TV 완제품이 아닌 컴퓨터 메모리용 관으로, 모든 CRT를 TV와 동일시하면 안 된다.
S38|Martin Walls interview, Know Your Meme|https://knowyourmeme.com/editorials/interviews/the-walten-files-creator-martin-walls-talks-about-the-viral-series-animatronic-horror-and-the-most-emotional-scene-he-ever-animated|search_and_partial_body|search excerpt; body mostly navigation; later fetch failed|인터뷰 존재와 애니매트로닉 호러 문맥만 확인했다. 원작의 세부 사건·인물·관계 검증은 완료하지 않았다.'''

def sources():
    out = []
    for line in ROWS.splitlines():
        sid, title, url, access, scope, finding = line.split('|')
        out.append(dict(id=sid, title=title, url=url, access=access, read_scope=scope,
                        finding_ko=finding, accessed_date='2026-10-22',
                        supports='bounded definitions/context only; exact candidate staging is locally authored',
                        pixel_reference_reviewed=False))
    return out
