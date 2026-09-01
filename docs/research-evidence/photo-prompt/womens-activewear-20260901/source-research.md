# 여성 액티브웨어 시각 의미·후보팩 강화 리서치

- 조사일: 2026-09-01
- 참조 대화: `여성 운동복 용어 조사` (`6a964451-f18c-83ee-bfae-ea1c2b92db13`)
- 대상: `photo-prompt-image-generator`의 시각 의미 프로필과 후보팩 데이터
- 결정 상태: `proposed`
- 적용 상태: 연구 산출물만 작성했으며 런타임 자산, 의미 인덱스, 테스트에는 아직 반영하지 않음
- 검증 경계: 출처·현행 데이터·제안 스키마를 확인했지만 생성 이미지의 픽셀 충족과 사용자 선호는 검증하지 않음

## 1. 핵심 결론

참조 대화의 용어 목록은 폭은 충분하지만, 그대로 후보팩에 넣으면 다음 네 종류의 의미가 섞인다.

1. **의복 객체와 토폴로지**: 스포츠브라, 레깅스, 스코트, 유니타드처럼 사진에서 형태를 확인할 수 있는 것
2. **구조·핏·표면 속성**: 레이서백, 크로스백, 7/8 길이, 스크런치 중심봉, 립 니트처럼 특정 부위에서 확인할 수 있는 것
3. **사용 목적·성능 주장**: high support, compression, moisture-wicking, quick-dry, four-way stretch, UPF처럼 정지 사진만으로 성능을 입증할 수 없는 것
4. **마케팅·스타일 합성어**: buttery-soft, sculpting, gym girl aesthetic, tenniscore처럼 브랜드·시대·코디에 따라 의미가 달라지는 것

후보팩 강화의 올바른 단위는 `용어 -> 동의어`가 아니라 다음과 같다.

```text
사용자 용어
-> 기본 의복 객체
-> 몸에 대한 덮임과 연결 구조
-> 국소 부품·봉제·길이·표면
-> 보이는 사용 맥락
-> 정지 이미지로 검증 불가능한 성능 메타데이터
-> 혼동 대체물
-> 구도 요구와 픽셀 게이트
```

ICOM Costume의 기록 원칙도 유행성 이름보다 기본 객체명을 먼저 두고 기능을 별도 항목으로 다룬다. Fashionpedia 역시 의복 범주, 부품, 세부 속성과 위치를 분리한다. 따라서 `activewear`, `sportswear`, `performance wear`, `athleisure`는 하드 시각 프로필이 아니라 상위 맥락 또는 검색용 소프트 후보로 두고, 하드 프로필은 연결 구조가 안정적인 세부 용어에만 허용해야 한다.

## 2. 현재 저장소 기준선

현행 `photo_prompt_tags.json`에는 운동복과 직접 관련된 일반 후보로 `gym_athleisure_mirror_fit`, `covered_track_jacket_training_set`, `skort_outer_panel_inner_shorts` 등이 있으나 다음 공백이 확인되었다.

- 전용 스포츠브라 구조 프로필이 없다.
- 레깅스 길이·허리·밑단·중심봉 구조를 소유하는 전용 후보군이 없다.
- `seamless`, `compression`, `high support`를 시각 증거와 성능 주장으로 분리하는 정책이 없다.
- 2-in-1 쇼츠, brief-lined 쇼츠, split 쇼츠의 서로 다른 내부·외부 구조가 없다.
- exercise dress, cycling bib shorts, unitard의 연결 토폴로지가 없다.
- `scrunch`, `contour`, `sculpting`, `butt-lifting`을 신체 평가가 아닌 의복 봉제·음영 구조로 제한하는 경계가 없다.

현행 시각 의무 레지스트리에는 위 운동복 계열 전용 하드 프로필이 검색되지 않았다. 이 연구는 기존 사용자 변경을 건드리지 않고 별도 제안 파일에만 신규 데이터를 설계한다.

## 3. 근거가 지지하는 데이터 모델

### 3.1 기본 객체, 세부 속성, 기능을 분리한다

ICOM Costume는 의복을 몸의 어느 부위를 어떤 방식으로 덮는지에 따라 기본 객체부터 기록하고, 일시적인 패션명과 기능은 별도 층으로 다룬다. Fashionpedia는 주 의복, 의복 부품, 세부 속성, 속성 위치를 분리한 온톨로지와 마스크를 사용한다.

- [ICOM Costume terminology](https://costume.mini.icom.museum/publications-2/terminology/)
- [Fashionpedia: Ontology, Segmentation, and an Attribute Localization Dataset](https://arxiv.org/abs/2004.12276)

데이터 영향:

- `wardrobe_style`: 완성 코디 또는 하나의 주 의복
- `garment_detail`: 스트랩 경로, 컵 분리, 안감, 허리밴드, 봉제선, 포켓, 고리
- `silhouette_proportion`: rise와 길이를 몸 랜드마크에 상대적으로 표현
- `surface_material`: 사진에서 보이는 니트 골, 메시 구멍, 립스톱 격자, 저광택 표면
- `occasion_context`·`action`·`location`: 운동 종목과 실제 사용 장면
- 비시각 메타데이터: 시험이 필요한 성능 주장

### 3.2 스포츠웨어와 패션 스포츠웨어는 같은 픽셀 계약이 아니다

Museum at FIT는 실제 운동용 의복과 그 구조·기술에서 영감을 받은 일상 패션을 나란히 다룬다. 그러므로 `sportswear`는 실제 운동 중인 기능복일 수도 있고, 패션 업계의 캐주얼 의복일 수도 있다. `athleisure`도 스포츠브라·레깅스만으로 자동 판정하면 안 된다.

- [Museum at FIT, Sporting Life](https://sites.fitnyc.edu/depts/museum/sporting_life/home.html)

후보팩 규칙:

- `activewear`, `sportswear`, `athletic wear`, `workout wear`, `gymwear`, `training wear`, `performance wear`는 하드 프로필을 활성화하지 않는다.
- 사용자가 종목을 명시하면 종목 맥락을 잠그되, 의복 세부는 그 종목에서 가능한 후보로만 제안한다.
- `athleisure`는 운동복 요소와 일상 레이어·신발·가방·장소가 함께 읽히는 코디 축이며, 실제 운동 성능을 뜻하지 않는다.
- `tenniscore`, `balletcore`, `gorpcore`, `Y2K activewear`, `luxury activewear`는 `aesthetic_trend` 또는 `wardrobe_style`의 소프트 후보로만 둔다.

## 4. 스포츠브라 시각 의미

Nike와 lululemon은 현재 상품 분류에서 support level과 racerback, longline, strappy, high-neck, zip-front, neckline 등을 별도 축으로 사용한다. 이 분류는 현재 리테일 용례를 보여 주지만 보편 규격은 아니다.

- [Nike sports-bra fit guide](https://www.nike.com/gb/size-fit/womens-sports-bra-fit-guide)
- [Nike sports-bra category and cup-style guide](https://www.nike.com/gb/w/womens-sports-bras-40qgmz5e1x6/)
- [lululemon sports-bra category](https://www.eu.lululemon.com/en-dk/c/womens/bras-and-underwear/sports-bras)

| 용어 | 사진에서 소유해야 할 구조 | 혼동 경계 | 데이터 처리 |
| --- | --- | --- | --- |
| Racerback | 좌우 어깨 스트랩이 견갑 사이 중앙 또는 Y형 등판으로 수렴 | 평행 스트랩, 한 번 교차하는 X-back, 홀터넥 | 하드 프로필 후보 |
| Crossback / X-back | 두 스트랩이 등에서 교차해 반대편 하부에 연결 | 중앙 한 줄 레이서백, 여러 가는 장식 스트랩 | 하드 프로필 후보 |
| Strappy | 셋 이상의 가는 스트랩이 등에서 별도 경로를 유지 | 메시 패널의 선, 프린트, 레이서백 가장자리 | 소프트 후보; 정확한 개수는 요청 시만 잠금 |
| Longline sports bra | 컵·브라 본체 아래의 넓은 연장 밴드가 하부 갈비뼈까지 이어짐 | 단순히 짧은 crop tank, 높은 허리 레깅스가 밴드를 가림 | 하드 프로필 후보 |
| High-neck | 앞 목선이 쇄골 가까이 올라오고 암홀과 연결됨 | mock-neck top, 일반 탱크 위에 브라를 겹침 | 소프트 또는 조합 프로필 |
| Zip-front | 앞 중심 지퍼가 목선에서 하부 밴드 방향으로 실제 개폐 경로를 형성 | 장식 지퍼, 재킷 안쪽 브라, 프린트 선 | 하드 프로필 후보 |
| Encapsulation | 좌우 컵 경계와 중심 브리지가 분리되고 각 컵이 개별 볼륨을 가짐 | 평평한 한 장 압박 패널, 단순 패드 윤곽 | 하드 프로필 후보 |
| Compression bra | 넓은 전면 패널이 가슴을 흉곽 쪽으로 밀착시키는 설계 | 일반적인 타이트한 브라 사진만으로 실제 압박량 추정 | 외형 후보만; 성능 하드 게이트 금지 |
| Hybrid | 분리 컵과 외부 압박 패널·밴드가 동시에 보임 | 컵 봉제만 있는 브라, 패턴 음영 | 복합 후보; 운동 성능은 별도 |
| Light / medium / high support | 정지 외형이 아니라 활동 중 이동량·밴드 안정성·착용 적합성과 관련 | 넓은 스트랩이나 높은 넥만 보고 등급 추정 | 비시각 메타데이터 |

스포츠브라 연구는 support를 정지 외형이 아닌 착용 상태, 보행·달리기 속도, 이동과 불편감 측정으로 평가한다. 따라서 생성 이미지에서 넓은 스트랩, 몰드 컵, 높은 커버리지를 보여 줄 수는 있지만 이를 곧바로 `high support PASS`로 부르면 안 된다.

- [McGhee & Steele, breast elevation and compression study](https://pubmed.ncbi.nlm.nih.gov/20019639/)
- [Chen et al., encapsulation versus compression under gait-speed changes](https://pubmed.ncbi.nlm.nih.gov/26256619/)

## 5. 상의와 내장 지지 구조

| 용어군 | 관찰 가능한 의미 | 혼동 경계 |
| --- | --- | --- |
| Tank / racerback tank / muscle tank | 몸통 한 장 상의, 어깨 폭·암홀 깊이·등판 연결이 서로 다름 | 스포츠브라를 탱크로, 넓은 암홀을 찢어진 옷으로 대체하지 않음 |
| Crop tank / longline tank | 밑단을 허리·배꼽·골반 랜드마크에 상대적으로 기록 | 카메라 크롭이나 레깅스 허리밴드가 길이를 위조하지 않음 |
| Bra tank | 외부 탱크 실루엣과 브라 수준의 상부 밀착·내부 구조가 한 벌에 결합 | 스포츠브라 위에 별도 탱크를 겹친 두 벌 |
| Shelf-bra tank | 탱크 안쪽의 별도 언더밴드·라이너가 보이는 구조 | 외부 프린트 선, 몸 그림자, 단순 이중 천 |
| Half-zip / quarter-zip | 앞 중심 지퍼가 목에서 흉부 일부까지만 내려옴 | full-zip jacket, 장식 파이핑 |
| Base layer / compression top | 밀착된 긴팔 또는 반팔 기저층 | 외형만으로 보온·압박 성능을 증명하지 않음 |
| Thumbholes | 소매 커프가 손등 위로 연장되고 엄지가 전용 구멍을 통과 | 손가락 없는 장갑, 소매를 손에 걸친 포즈 |

## 6. 레깅스·타이츠 시각 의미

Nike의 현행 가이드는 rise, fit, length, fabric을 별도 축으로 둔다. 7/8은 발목 바로 위라는 상대 길이로 설명한다. 따라서 길이와 rise는 절대 치수 대신 보이는 몸 랜드마크와 양쪽 밑단 일관성으로 기록한다.

- [Nike workout-legging guide](https://www.nike.com/ca/a/best-leggings-tights)

### 6.1 길이와 실루엣

| 용어 | 관찰 가능한 계약 | 주요 혼동 |
| --- | --- | --- |
| Full length | 양쪽 밑단이 발목 부근까지 도달 | 긴 양말, 부츠, 카메라 크롭 |
| 7/8 | 양쪽 밑단이 발목뼈보다 약간 위에서 끝남 | 키 차이로 우연히 짧아진 full length, capri |
| Capri | 양쪽 밑단이 종아리 중간 부근 | 무릎 길이 타이츠, 7/8 |
| Biker shorts | 허벅지 중간에서 무릎 위까지의 밀착된 두 바지통 | 짧은 hot pants, 패드가 있는 cycling shorts |
| Flared leggings | 허벅지·무릎까지 밀착되고 무릎 아래부터 두 밑단이 확장 | 허벅지부터 넓은 wide-leg pants, bootcut의 약한 확장 |
| Split-hem leggings | 밀착 또는 플레어 밑단에 실제 세로 절개가 열림 | 대비 파이핑, 접힌 주름, 그림자 |
| Stirrup leggings | 각 밑단에서 발바닥 아래로 이어지는 스트랩·고리 | 양말, 신발 스트랩, footed tights |
| Footed tights | 천이 발등·발가락까지 연속적으로 덮음 | 레깅스와 같은 색 양말 |

### 6.2 허리와 중심 구조

| 용어 | 관찰 가능한 계약 | 주요 혼동 |
| --- | --- | --- |
| High-rise / high-waisted | 허리밴드 상단이 배꼽 부근 또는 위에 위치 | 상의를 넣어 입은 효과, 카메라 원근 |
| Mid-rise / low-rise | 허리밴드와 배꼽·골반의 상대 위치 | 몸 비율이나 포즈만으로 판정하지 않음 |
| Crossover waist | 앞 중심에서 좌우 허리밴드 가장자리가 교차해 겹침 | 한 줄 V 프린트, 대각 봉제 하나 |
| V-back waist | 뒤 중심 허리밴드 상단이 V로 낮아짐 | 요크 봉제나 색 블록만 있는 경우 |
| Foldover waist | 뒤집어 접은 외부 밴드와 접힘선·이중층이 읽힘 | 넓은 단일 허리밴드 |
| No front seam | 앞 중심 세로 봉제가 없어야 함 | `seamless` 제조법 전체와 동일시하지 않음; 부재 증거이므로 정면 native 검토 필요 |
| Scrunch / ruched back seam | 뒤 중심 세로 채널을 따라 반복된 모임과 짧아진 중심선이 있음 | 신체 그림자, 프린트 컨투어, 단순 뒤 중심봉 |
| Glute contour seam | 좌우를 감싸는 곡선 봉제가 의복 표면에 실제로 존재 | 몸 윤곽, 조명, 색 그라데이션 |
| Contour shading | 니트 또는 염색의 명도·텍스처 구역이 의복 좌우에서 재현됨 | 환경광, 피부 그림자, 한쪽만 보이는 얼룩 |

`scrunch`, `booty-contouring`, `butt-lifting`, `sculpting`은 몸의 가치나 효과를 판정하는 프로필이 아니다. 후보 데이터는 `center-back gathered channel`, `curved seam`, `knit shading zone`처럼 의복이 소유한 원인만 표현한다. 생성된 신체 실루엣만으로 제품의 리프팅 효과를 주장하지 않는다.

## 7. 쇼츠 시각 의미

Brooks는 2-in-1 쇼츠를 외부 shell과 더 긴 밀착 liner의 두 층으로 기술한다. Nike의 split running shorts는 외부 side split과 별도 brief liner를 함께 사용한다. 두 구조는 서로 대체되지 않는다.

- [Brooks Dash 2-in-1 Shorts](https://www.brooksrunning.com/en_us/womens/apparel/bottoms/dash-2-in-1-short/221754368.020.html)
- [Nike AeroSwift brief-lined split running shorts](https://www.nike.com/t/aeroswift-womens-dri-fit-adv-mid-rise-3-brief-lined-running-shorts-SsbNQGKt/FN2328-570)

| 용어 | 관찰 가능한 구조 | 혼동 경계 | 프로필 우선순위 |
| --- | --- | --- | --- |
| 2-in-1 shorts | 루즈한 외부 shell과 별도 밀착 inner shorts, 두 개의 밑단 | brief liner만 있는 쇼츠, 한 겹 색 블록 | P0 |
| Brief-lined shorts | 외부 쇼츠 안에 팬티형 라이너가 부분적으로 보임 | 더 긴 inner shorts, 속옷 노출 | P1 |
| Split shorts | 옆선 일부가 실제로 열려 앞·뒤 패널이 움직임에 따라 분리 | 대비 옆줄, 곡선 밑단만 있는 dolphin shorts | P0 |
| Dolphin shorts | 둥근 옆밑단과 대비 바인딩이 앞뒤 곡선을 이음 | 깊은 side split, 일반 체육 쇼츠 | P1 |
| Compression shorts | 허리에서 두 허벅지로 이어지는 밀착 바지 | biker shorts와 외형 중첩; 실제 압박량은 비시각 | 후보만 |
| Cycling shorts | 밀착된 두 바지통에 안장용 패드·그리퍼·사이클 맥락이 결합 | 일반 biker shorts | P1; 패드가 안 보이면 맥락 필요 |
| Booty shorts / hot pants | 매우 짧은 패션·운동 쇼츠 | 기능 카테고리가 불안정하고 성적 인상과 혼동 | 하드 프로필 금지; 요청 시 중립 길이 후보 |

## 8. 스코트·액티브 드레스

REI의 스코트는 바깥 스커트와 내장 라이너 쇼츠를, Outdoor Voices의 exercise dress는 A-line 외부 드레스와 built-in shorts liner를 별도 구조로 기술한다.

- [REI Active Pursuits Skort](https://www.rei.com/product/202455/rei-co-op-active-pursuits-skort)
- [Outdoor Voices The Exercise Dress](https://www.outdoorvoices.com/products/w-the-exercise-dress-black)

| 용어 | 필수 구조 | 혼동 경계 |
| --- | --- | --- |
| Skort | 공유 허리밴드, 외부 스커트 패널, 별도 inner shorts, 자연스러운 보폭·옆열림에서 두 층 확인 | 일반 스커트, 쇼츠 위에 임의로 두른 천, 플리츠 그림자 |
| Exercise / active dress with shorts | 상·허리·스커트가 한 드레스로 이어지고 내부 shorts liner의 별도 두 바지통이 보임 | 일반 스포츠 드레스, 별도 biker shorts를 나중에 입은 코디 |
| Built-in bra dress | 외부 드레스와 내부 언더밴드·라이너 연결 | 스포츠브라를 별도로 레이어링한 모습 |
| Tennis / golf / court dress | 드레스 구조 외에 종목 맥락이 필요 | 흰색, 플리츠, 바이저만으로 종목 판정하지 않음 |

내장 쇼츠는 정면 정지 포즈에서 가려질 수 있다. 하드 프로필 평가에는 자연스러운 한 걸음, 3/4 측면, 라켓 준비 자세처럼 외부 스커트와 안쪽 쇼츠를 동시에 보이는 구도가 필요하다. 노출을 목적으로 과도한 포즈를 만들 필요는 없다.

## 9. 원피스형 운동복

Nike는 현재 bodysuit를 short와 7/8 길이로도 판매하지만, 리테일 명명은 브랜드마다 `bodysuit`, `unitard`, `short unitard`를 다르게 쓸 수 있다. 후보팩은 이름보다 몸 덮임과 다리 길이를 우선한다.

- [Nike bodysuits category](https://www.nike.com/w/bodysuits-2a768z63edxz8ukqp)

| 용어 | 관찰 가능한 구조 | 혼동 경계 |
| --- | --- | --- |
| Bodysuit | 상체가 골반·가랑이까지 한 벌로 이어지고 다리 덮임은 없거나 매우 짧음 | 탑을 레깅스 안에 넣어 입은 두 벌 |
| Short unitard | 상체부터 가랑이와 두 허벅지 바지통까지 한 벌로 연속 | bodysuit + separate biker shorts, romper의 루즈한 다리 |
| Long unitard | 상체부터 가랑이와 두 긴 다리까지 한 벌로 연속 | matching top + leggings, jumpsuit의 루즈·테일러드 구조 |
| Leotard | 상체와 골반을 덮는 밀착 일체형이며 다리 개구가 분리 | 수영복, bodysuit와 외형 중첩; 체조·댄스 맥락이 없으면 이름 단정 금지 |
| Workout romper | 한 벌 상체와 짧은 두 바지통, 보통 unitard보다 디자인 여유가 큼 | dress, matching set |
| Athletic jumpsuit | 한 벌 상체와 긴 두 바지통 | 현행 일반 점프수트 프로필을 재사용하고 스포츠 맥락만 별도 |
| Cycling bib shorts | 밀착 쇼츠에서 어깨 스트랩·상부 메시까지 연속되고 안장 패드 또는 사이클 맥락이 결합 | 멜빵을 단 일반 쇼츠, unitard, overalls |

Rapha의 bib-shorts 자료는 shoulder straps, chamois pad, leg grippers, on-bike fit을 서로 다른 설계 부품으로 다룬다. 패드 성능과 편안함은 wear test·pressure mapping의 영역이므로 사진에서는 스트랩 연결·패드 외형·그리퍼·사이클 맥락만 확인한다.

- [Rapha women’s bib-shorts/chamois design](https://content.rapha.cc/nl/en/a/story/new-womens-chamois)

## 10. 루즈 팬츠·아우터·신발·액세서리·종목 맥락

참조 대화의 조거, 트랙 팬츠, 윈드 팬츠, 카고·패러슈트 팬츠, 재킷, 신발, 양말·장비 용어는 액티브웨어 장면을 풍부하게 하지만, 핵심 의복 구조와 보조 맥락을 분리해야 한다.

### 10.1 루즈 팬츠와 아우터

| 용어 | 관찰 가능한 구조 | 혼동 경계와 데이터 처리 |
| --- | --- | --- |
| Joggers | 허리밴드, 여유 있는 허벅지, 아래로 좁아지는 두 바지통, 발목 커프 | 단순 sweatpants나 straight-leg pants와 구분; `silhouette_proportion` 후보 |
| Track pants | 운동용 긴 바지 실루엣과 옆선·지퍼·스냅·커프 같은 구조 | side stripe 하나만으로 트랙 팬츠 판정 금지 |
| Woven training / wind pants | 얇은 직조 표면, 패널 봉제, 탄성·드로코드 개구, 바람에 반응하는 낮은 질량감 | 실제 windproof 성능은 비시각 메타데이터 |
| Ripstop pants | 같은 직조 바탕을 통과하는 보강 격자 | 프린트 체크와 구분; 찢김 강도는 시험 필요 |
| Cargo training pants | 기능 포켓 몸판·플랩·입구·부착 봉제, 움직임 여유 | 장식 사각 프린트나 작은 지퍼 하나로 대체하지 않음 |
| Parachute pants | 큰 디자인 여유, 무릎·밑단의 볼륨, 드로코드 또는 탄성 개구 | 실제 낙하산 소재나 운동 성능을 뜻하지 않음 |
| Track jacket | 앞 중심 전장 지퍼, 스탠드 칼라 또는 운동 재킷 넥, 커프·밑단 | side stripe·로고만으로 판정 금지 |
| Windbreaker / running shell | 얇은 외피, 폐쇄 가능한 앞여밈·후드·커프·밑단, 패널 구조 | water-/wind-resistant 수치는 픽셀로 검증 금지 |
| Packable jacket | 의복과 연결된 주머니·파우치로 실제 접혀 들어가는 상태 | 단순히 작은 재킷이나 파우치 옆에 놓인 재킷은 부족 |
| Insulated / puffer / fleece layer | 충전 구획 또는 기모·파일과 레이어 연결 | 보온 수치·섬유 조성은 비시각 |

`jogger`, `track pants`, `wind pants`, `cargo`, `parachute`는 서로 배타적인 이름이 아닐 수 있다. 후보팩은 기본 바지 토폴로지를 하나 고른 뒤 taper, cuff, pocket, surface, weather function을 독립 축으로 조합해야 한다.

### 10.2 신발과 액세서리

- running shoes, training shoes, court shoes, cycling shoes, hiking shoes는 의복 프로필이 아니라 `footwear` 후보다. 종목을 하드하게 잠그려면 밑창, 클릿, 발목 지지, 코트·트레일 접지 같은 구조와 실제 장면이 함께 필요하다.
- grip socks는 발바닥의 실리콘·고무 그립 패턴이 보일 때만 구조 후보가 된다. 스튜디오 장소나 발목 양말만으로 grip을 추정하지 않는다.
- hydration vest는 몸통 전면 플라스크·포켓, 어깨 하네스, 측면 조절끈이 하나의 착용 시스템으로 연결되어야 한다. 일반 러닝 베스트나 백팩과 구분한다.
- lifting belt, wrist wraps, lifting straps, knee sleeves는 서로 다른 `wearable_accessory`다. 웨이트 장면만으로 자동 선택하지 않는다.
- visor, running cap, headband, crew socks, leg warmers, belt bag은 스타일 보조 후보이며 주 의복 의미를 대신하지 않는다.
- reflective trim은 직접광에서 보이는 국소 효과 후보일 뿐, 안전장비 적합성이나 역반사 성능의 증거가 아니다.

### 10.3 종목별 장면은 의복과 별도 소유권을 가진다

| 종목 | 의복 외에 필요한 장면 증거 | 의복만으로 생기는 오탐 |
| --- | --- | --- |
| Yoga / Pilates / barre | 매트·리포머·바·그립 양말, 통제된 동작, 스튜디오 관계 | 레깅스와 브라탱크만으로 종목 확정 |
| Running / trail running | 보행 주기, 러닝화, 트랙·도로·트레일, 러닝 장비 | split shorts만으로 러너 역할 확정 |
| Tennis / padel | 라켓 종류, 코트선·네트, 공과 동작 | 흰 스코트·바이저만으로 테니스 확정 |
| Golf | 클럽·그립·볼·티·코스 관계 | 폴로와 스코트만으로 골프 확정 |
| Cycling | 자전거·페달·안장·전경 자세, 빕/저지 관계 | biker shorts만으로 사이클링 확정 |
| Hiking / climbing | 지형·장비·접촉점·움직임, 마찰·레이어 맥락 | 카고 팬츠나 스포츠브라만으로 종목 확정 |
| Boxing / weight training | 글러브·링 또는 바벨·랙과 실제 접촉 동작 | 스포츠브라와 쇼츠만으로 역할 확정 |

`matching set`, `monochrome set`, `tonal set`, `color block`, `contrast piping`, `side stripe`, `gradient`, `marl`은 코디·색·표면 축이다. 이 축은 사용자 색상 잠금을 보존하면서 의복 구조 뒤에 적용해야 하며, 같은 색이라는 이유로 상하의가 한 벌 원피스가 되거나 종목이 자동 결정되면 안 된다.

## 11. 심리스·봉제·표면

### 11.1 `seamless`는 무봉제와 동의어가 아니다

원형 심리스 니팅 연구와 브랜드 설명은 몸 크기의 튜브형 니트를 만들고 허리밴드·언더밴드·메시·립·압박 구역을 통합하며, 절단·봉제를 줄이는 방식으로 설명한다. 완성 과정의 일부 봉제는 남을 수 있다.

- [Computational design for seamless circular knitting](https://www.sciencedirect.com/science/article/abs/pii/S001044852200015X)
- [Gymshark seamless-legging construction guide](https://www.gymshark.com/blog/article/gymshark-seamless-leggings)

후보팩 규칙:

- `seamless` 정확어만으로 `zero seams`를 프롬프트에 쓰지 않는다.
- 하드하게 보일 수 있는 것은 `continuous tubular knit appearance`, `minimal panel seams`, `integrated rib/mesh/contour zones`, `no center-front seam when separately requested`이다.
- 사진만으로 제조기계나 실제 원형 니팅 공정을 확정하지 않는다.
- `no front seam`은 하나의 부재 속성이고 `seamless construction` 전체와 별도다.

### 11.2 봉제 후보

ISO 4915와 ASTM D6193는 stitch type과 seam type을 표준화된 별도 구조로 다룬다. 겉보기 선 하나로 flatlock, coverstitch, bonded, welded를 섞으면 안 된다.

- [ISO 4915 stitch types](https://www.iso.org/standard/10932.html)
- [ASTM D6193 stitches and seams](https://store.astm.org/d6193-16r25.html)

| 용어 | 보이는 단서 | 제한 |
| --- | --- | --- |
| Flatlock / flat seam | 낮게 눕는 넓은 다중 실 사다리 또는 맞댄 연결 | native-scale에서 실 경로가 없으면 단정 금지 |
| Coverstitch | 평행한 겉면 봉제선과 안쪽 루퍼 구조 | 겉면만 보이면 일반 twin-needle과 혼동 가능 |
| Bonded / welded seam | 실이 거의 없고 낮은 접합선·테이프·매끈한 가장자리 | 접착과 열용착을 사진만으로 구분하지 않음 |
| Laser-cut / raw-cut edge | 접힌 시접 없이 얇고 깨끗한 절단 가장자리 | 실제 절단 공정은 단정하지 않고 low-profile cut edge로 표현 |
| Gusset | 가랑이 또는 겨드랑이에 별도 다각형 패널이 연결 | 그림자나 주름을 패널로 오인하지 않음 |

### 11.3 표면 후보

픽셀에서 비교적 안정적인 표면은 다음과 같다.

- 립 니트: 반복되는 세로 웨일과 국소 늘어남에 따른 간격 변화
- 메시: 실제 구멍 또는 투과 구조와 가장자리 연결
- perforated panel: 일정한 천공 배열과 패널 경계
- ripstop: 직조 격자 보강선이 같은 천 표면을 가로지름
- smooth interlock: 조밀하고 균일한 저광택 니트 표면
- brushed / peached: native close-up에서만 보이는 짧은 기모와 부드러운 난반사
- marl / mélange: 서로 다른 색 실이 표면 전체에서 섞이는 구조

섬유 조성 `polyester`, `nylon`, `spandex`, `merino wool`은 이미지에서 안전하게 판정할 수 없다. 후보팩은 사용자가 조성을 지정했을 때 텍스트 메타데이터로 보존하되, 픽셀 게이트는 표면·드레이프·광택·두께로 제한한다.

## 12. 기능·마케팅 용어의 하드 금지 경계

AATCC는 moisture management, wicking, drying, water-vapor transmission, odor reduction 등을 각각 시험법으로 다룬다. ASTM도 stretch, growth, recovery를 하중과 연장 조건 아래 측정한다. 압박 의류 연구는 센서 또는 직물 파라미터로 interface pressure를 측정하며, 자세와 사이즈에 따라 압력이 달라진다고 보고한다.

- [AATCC TM195 liquid-moisture management](https://members.aatcc.org/store/tm195/591/)
- [AATCC test-method index](https://www.aatcc.org/testing/standards)
- [ASTM D3107 stretch, growth and recovery](https://store.astm.org/d3107-26.html)
- [Sports compression pressure and posture study](https://pubmed.ncbi.nlm.nih.gov/25530213/)
- [Compression-hosiery pressure measurement](https://pubmed.ncbi.nlm.nih.gov/32538901/)

| 용어 | 정지 이미지에서 가능한 표현 | 금지되는 결론 | 실제 검증 층 |
| --- | --- | --- | --- |
| Moisture-/sweat-wicking | 건조한 표면 또는 땀 분포 장면 | 섬유의 수분 이동 성능 PASS | AATCC TM195/TM197/TM198 |
| Quick-dry / fast-dry | 시간 경과 전후의 별도 실험 장면 | 한 장으로 건조 속도 PASS | AATCC TM199/TM200/TM201 |
| Breathable / high-airflow | 메시·천공·개방 구조 | 실제 공기 투과량 PASS | 공기·수증기 투과 시험 |
| Four-way stretch | 두 축 변형을 보여 주는 동작 또는 재료 샘플 | 복원률·방향별 신율 PASS | ASTM/ISO 인장·회복 시험 |
| Compression | 밀착 실루엣, 니트 밀도 구역 | 실제 interface pressure 또는 등급 PASS | 센서·압력 측정 |
| High support | 넓은 밴드·컵·스트랩·클로저 | 운동 중 지지력 PASS | 착용·동작·운동학 시험 |
| Squat-proof / opaque | 특정 자세와 조명에서 불투명해 보임 | 모든 하중·색·사이즈에서 불투명 | 표준화된 신장·투과 시험 |
| UPF / UV protection | 아무 픽셀 대체물도 없음 | UPF 수치·차단 성능 PASS | 분광 투과 시험 |
| Water-resistant / repellent | 물방울이 맺힌 한 순간 | 내수압·세탁 후 성능 PASS | 발수·내수압 시험 |
| Wind-resistant / windproof | 셸 구조, 조여진 개구, 바람 장면 | 공기 투과 성능 PASS | 공기 투과 시험 |
| Odor control / anti-odor | 아무 픽셀 대체물도 없음 | 항균·탈취 성능 PASS | AATCC TM211/TM216 등 |
| Thermal | 기모·레이어·추운 맥락 | 열저항·보온 등급 PASS | 열저항 시험 |
| Reflective | 직접광에서 밝아진 트림 | 역반사 계수·PPE 적합성 PASS | 규정된 기하의 역반사 시험 |
| Packable | 의복이 자신의 주머니·파우치 안에 접혀 들어감 | 무게·부피·내구성 PASS | 제품 측정·사용 시험 |
| Buttery-soft / silky / second-skin | 저광택·미세결·밀착·주름 반응 | 촉감이나 편안함의 보편적 사실 | 사용자 촉각 평가 |
| Sculpting / butt-lifting / shape-retention | 봉제·니트·음영 구역 | 신체 개선·매력·건강 효과 | 제품·착용 시험 및 사용자 판단 |

## 13. 후보팩 데이터 우선순위

### P0: 하드 프로필까지 연구 근거가 충분한 구조

1. `racerback_sports_bra_strap_convergence`
2. `longline_sports_bra_extended_underband`
3. `encapsulated_sports_bra_separate_cups`
4. `two_in_one_running_shorts_dual_layer`
5. `split_running_shorts_side_opening`
6. `active_skort_outer_skirt_inner_shorts` — 기존 `skort_outer_panel_inner_shorts` 재사용 우선
7. `exercise_dress_integrated_short_liner`
8. `cycling_bib_shorts_strap_pad_continuity`
9. `unitard_upper_crotch_leg_continuity`
10. `stirrup_leggings_underfoot_loop`

### P1: 후보 원자는 유용하지만 바로 하드 의무로 만들면 위험한 구조

- crossback, strappy, high-neck, zip-front, shelf-bra tank
- 7/8, capri, biker length, flare, split hem
- crossover waist, V-back waist, foldover waist, no-front-seam
- scrunch channel, contour seam, contour shading
- brief liner, gusset, thigh phone pocket, thumbhole
- flatlock-like seam, bonded low-profile edge, mesh/perforated panel
- integrated rib/mesh body-mapped knit zones

위 항목은 작은 부품, 부재 증거, 정면·후면 의존, 조명·신체 그림자 혼동이 있어 native-scale 또는 특정 구도를 요구한다. 별도 렌더 캘리브레이션 전에는 소프트 후보로 두는 편이 안전하다.

### P2: 상위 맥락·코디 후보

- yoga / Pilates / barre studio set
- running / trail-running ensemble
- tennis / padel / golf court ensemble
- cycling bib-and-jersey ensemble
- hiking base-layer and shell system
- athleisure, tenniscore, balletcore, gorpcore, retro track, Y2K activewear

이들은 하나의 의복을 정의하지 않고 장소·행동·신발·소도구·레이어 조합을 제안한다. 사용자 `intent_lock`이 이미 정한 의복, 종목, 노출, 길이, 색을 덮어쓰면 안 된다.

## 14. 제안하는 활성화 정책

```text
exact stable structural term
  -> component evidence present
  -> one hard profile eligible

broad category or activity term
  -> advisory candidate families only

BM25F or embedding-only similarity
  -> optional candidate only

performance or marketing term
  -> preserve as requested metadata
  -> never create pixel PASS by itself
```

- `women's`는 의복 구조 프로필의 필수 성별 조건이 아니다. 사용자가 여성 피사체를 요청하면 `subject`가 이를 소유한다.
- 운동복의 밀착도, 스크런치, 짧은 길이를 신체 가치·건강·매력·성격·연령·정체성 판단으로 확장하지 않는다.
- generic `seamless`, `compression`, `high support`, `squat-proof`, `sculpting`, `buttery-soft`는 하드 프로필 exact term에서 제외한다.
- exact term이더라도 프롬프트에는 라벨 한 번과 즉시 이어지는 구조 설명 한 번만 둔다. 동의어를 반복해 과가중하지 않는다.

## 15. 회귀 테스트 설계

### 15.1 정적·라우팅 테스트

- 모든 후보 ID는 한 슬롯만 소유한다.
- P0 exact term은 목표 프로필 하나만 활성화한다.
- broad category와 성능 용어는 하드 프로필을 활성화하지 않는다.
- embedding-only 적중은 `optional_eligible=true`, `hard_eligible=false`를 유지한다.
- 기존 `skort_outer_panel_inner_shorts`를 중복 생성하지 않는다.
- `seamless`와 `no front seam`, `compression`과 `tight fit`, `sportswear`와 `athleisure`가 서로 자동 동치가 되지 않는다.

### 15.2 인과·혼동 쌍

| 목표 | 양성 케이스 | 음성 케이스 |
| --- | --- | --- |
| Racerback | 두 스트랩이 중앙 Y 등판으로 수렴 | 평행 스트랩, X 교차 |
| Longline bra | 컵 아래 연장 밴드가 갈비뼈까지 이어짐 | 높은 허리 레깅스가 짧은 브라 밑단을 가림 |
| Encapsulation | 좌우 개별 컵과 중심 브리지 | 평평한 한 장 압박 패널 |
| 2-in-1 shorts | 외부 shell + 더 긴 inner shorts | brief liner만 있는 외부 쇼츠 |
| Split shorts | 실제 열린 옆선과 움직이는 앞뒤 패널 | 대비 옆줄·둥근 dolphin hem |
| Skort | 외부 스커트 + inner shorts | 플리츠 스커트·쇼츠 단독 |
| Exercise dress | 한 벌 드레스 + 연결된 inner shorts | 일반 드레스 + 별도 biker shorts |
| Unitard | 상체부터 가랑이와 두 다리까지 연속 | matching top + leggings |
| Stirrup | 밑단에서 발바닥 아래로 이어지는 고리 | 같은 색 양말·신발 스트랩 |
| Scrunch | 뒤 중심 모임 채널과 반복 주름 | 그림자·프린트·일반 중심봉 |

### 15.3 픽셀 게이트

공통 규칙:

- `one_saved_image`에서 모든 목표 게이트가 보여야 한다.
- 일부만 보이거나 가림·포즈·렌즈·그림자로 해석이 갈리면 `fail`이다.
- 렌더가 없거나 moderation으로 차단되면 `unscored`다.
- 프롬프트·후보팩·런타임 감사 PASS는 픽셀 PASS가 아니다.
- 제품 성능과 촉감은 생성 픽셀로 자격을 부여하지 않는다.
- 사용자 판단은 별도 `pending` 상태로 남긴다.

권장 구도:

- 등 스트랩: 등 중심이 보이는 상반신 3/4 후면
- 컵 구조: 정면 또는 제한된 3/4 상반신
- 레깅스 길이·밑단: 발목·발까지 포함한 전신
- 허리·스크런치: 허리부터 허벅지까지의 정면 또는 후면, native 확인
- 2-in-1·스코트·드레스 라이너: 자연스러운 한 걸음의 3/4 측면
- unitard·bib shorts: 어깨부터 양쪽 밑단까지 연결 경로가 한 프레임에 보이는 전신

## 16. 구현 시 권장 순서

1. 제안 JSON에서 P0 프로필 10개와 후보 원자를 검토한다.
2. 기존 태그와 의미 인덱스의 중복 ID·별칭 충돌을 다시 검색한다.
3. `photo_prompt_tags.json`에 후보를 한 슬롯 소유권으로 추가한다.
4. `photo_prompt_visual_obligations.json`에는 P0 중 실제 렌더 구도가 가능한 항목만 추가한다.
5. 정확어·혼동어·embedding-only 회귀 테스트를 먼저 만든다.
6. 의미 인덱스를 재생성하고 source/generated parity를 확인한다.
7. 무참조 holdout과 혼동 쌍으로 프롬프트 행동을 확인한다.
8. 그 뒤에만 독립 렌더를 만들고 thumbnail/native 픽셀 게이트를 적용한다.

이 조사만으로는 어떤 프로필도 `promote`할 수 없다. 현재 결정은 데이터·테스트를 구현할 수 있는 연구 기반을 마련한 `proposed`이며, 실제 후보팩 행동과 생성 픽셀은 아직 미검증이다.
