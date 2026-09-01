# 희얼사·희연사 시각 의미 및 후보팩 적용 근거

## 결론

희얼사와 희연사는 단일 hard visual profile이 아니다. 두 표현에는 희소성, 촬영자, 유통 경로, 인물 신분, 촬영 시기처럼 한 장의 픽셀로 확인할 수 없는 의미가 포함된다. 런타임에서는 bare shorthand를 복수의 선택 가능한 후보 경로로만 사용하고, 좁은 시각 표현만 exact hard profile을 활성화한다.

이번 적용은 다음 세 층을 분리한다.

1. 비시각 메타 의미: 희귀, 미공개, 삭제, 과거, 프리데뷔, 실제 연예인, 팬 촬영자, B컷 또는 outtake 상태
2. 관찰 가능한 촬영 관계: 공개 행사 관객 측 망원, 카메라 LCD 재촬영, 가까운 동행자 시점, 테이크 사이 제작 현장, 물리 인화지 스캔, 초기 디카 재압축, 컨택트 시트 선택 과정
3. 독립 처리 흔적: 직광 플래시, CCD 프린징, JPEG 블로킹, 모아레, 물리 인화지 마모

실제 촬영자, 연예인 여부, 희소성, 촬영 연도, 공개 여부를 추론하지 않는다. 첨부 인물사진은 신원이나 보호 특성의 근거가 아니며 보이는 성인 외형만 참조한다.

## 근거와 데이터 소유권

- 팬 촬영 연구는 공항, 공연, 팬사인회, 공개 일정과 빠른 프리뷰/후편집본의 구분을 설명한다. 픽셀 계약은 공개 행사, 관객 측 경계, 망원 압축에 한정한다: https://acr.comm.or.kr/_common/do.php?a=full&aidx=43195&b=&bidx=3839
- 아카이브의 연대와 출처는 맥락·생성자·메타데이터가 필요하다. 세피아나 먼지는 provenance를 증명하지 않는다: https://www.archives.gov/research/catalog/lcdrg/archival-materials 및 https://www.archives.gov/records-mgmt/initiatives/digital-photo-records.html
- JPEG는 고대비 경계에 blocking과 mosquito noise를 만들 수 있다: https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=908515
- 직광 플래시는 평평한 정면광, 반사광, 가까운 배경 그림자와 빠른 falloff를 만들 수 있다: https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/the-basics-of-flash-photography
- 가까운 셀피 거리는 원근 왜곡을 키우므로 동행자 시점의 촬영 거리와 구분해야 한다: https://pmc.ncbi.nlm.nih.gov/articles/PMC5876805/
- 비하인드 사진은 실제 카메라 운용, 조명, 연출, 녹음, 스태프 행동이 보일 때 제작 과정으로 판정한다: https://www.loc.gov/item/98518451/
- 컨택트 시트는 연속 촬영과 선택 과정을 보이지만, outtake 상태 자체는 최종 편집 메타데이터다: https://www.magnumphotos.com/theory-and-practice/contact-sheet-mother-child-elliott-erwitt-portrait/ 및 http://vocab.getty.edu/page/aat/300263849

## 런타임 적용

- hard profiles: `fan_side_public_event_telephoto`, `camera_display_rephotographed_preview`, `companion_viewpoint_everyday_candid`, `production_gap_behind_scenes`, `physical_print_scan_material_context`, `early_2000s_compact_digicam_social_repost`, `contact_sheet_selection_context`
- optional capture candidates: 대응하는 `capture_context` 7개 원자
- `희얼사`는 동행자·스캔·디카 후보에, `희연사`는 팬 행사·LCD 프리뷰·제작 비하인드 후보에 복수 alias로 연결한다.
- `과사`, `B컷`, `미공개컷`은 후보 탐색을 도울 수 있지만 hard evidence나 역사·유통 사실을 만들지 않는다.

## 렌더 판정

세 arm은 별도 요청 envelope, authorial core, candidate pack, composed prompt, runtime request, 이미지, 해시, 픽셀 리뷰를 갖는다. 다른 arm의 프롬프트·후보팩·이미지를 입력으로 사용하지 않는다. 각 profile의 다섯 hard gate 중 partial 또는 누락은 실패다. 프롬프트 및 런타임 audit PASS, 이미지 전달, 픽셀 PASS, 사용자 판단은 각각 별도 증거 층이다.
