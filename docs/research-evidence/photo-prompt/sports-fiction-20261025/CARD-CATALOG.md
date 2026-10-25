# 시각 의미 카드 목록

102개 카드의 선택형 실현 초안이다. 형태·문맥 근거와 직접 검증되지 않은 부분을 각 상태에 표시했다. 모든 카드의 운영 등록·픽셀 검증은 미실행이다.

## B01 농구 트리플 스렛

- 종목/단계: basketball / ball held before first dribble
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 트리플 스렛, Triple threat

선수가 무릎을 굽힌 채 몸통 옆에 공을 잡는다; 같은 선수의 두 손이 하나의 공에 이어진다; 몸은 골대를 향하고 앞에 움직일 공간이 남는다.

the player bends both knees while holding the ball beside the torso; the same player's two hands remain connected to that single ball; the body faces the basket with space available ahead.

혼동 경계: 진행 중 드리블·슛 릴리스와 구분; 세 행동을 동시에 수행하지 않음

가시성: 두 손·공·발 지지를 함께 확인

관계: player → holds → ball; player → faces → basket; player → supported_by → court

출처: [S02 FIBA Basketball Terminology](https://assets.fiba.basketball/image/upload/documents-corporate-regional-offices-europe-programs-fiba-europe-coaching-certificate-fiba-europe-basketball-terminology.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## B02 농구 온볼 스크린

- 종목/단계: basketball / screen set
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 스크린·픽, Screen, Pick

동료 한 명이 볼 핸들러를 수비하는 상대 옆에 선다; 볼 핸들러는 스크리너 몸 바깥에서 공을 다룬다; 수비자의 이동 공간이 스크리너 옆을 지나 볼 핸들러로 이어진다.

a teammate stands beside the ball handler's defender; the ball handler controls a separate ball outside the screener's body; the defender's route passes beside the screener toward the ball handler.

혼동 경계: 단순 밀치기·태클과 구분; 합법성은 발·이동·접촉 시점 자료 별도

가시성: 세 선수의 소속과 공 소유를 한 화면에서 구별

관계: handler → controls → ball; defender → guards → handler; screener → beside → defender

출처: [S02 FIBA Basketball Terminology](https://assets.fiba.basketball/image/upload/documents-corporate-regional-offices-europe-programs-fiba-europe-coaching-certificate-fiba-europe-basketball-terminology.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## B03 농구 롤 단계의 배치

- 종목/단계: basketball / roll snapshot
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 픽앤롤, Pick-and-roll

스크리너가 수비자 옆에서 골대를 향해 몸을 돌린다; 공을 가진 동료는 그 선수의 진로 바깥에 있다; 골대와 열린 통로가 롤하는 선수의 방향을 정한다.

the screener has turned toward the basket beside the defender; the teammate with the ball remains outside that player's path; the basket and the open lane define the roller's direction.

혼동 경계: 스크린 이전과 롤 이후를 한 몸에 겹치지 않음; 이전 스크린은 정지 사진으로 증명 불가

가시성: 공·롤러·수비자·골대의 방향

관계: roller → faces → basket; handler → holds → ball; defender → between → handler

출처: [S02 FIBA Basketball Terminology](https://assets.fiba.basketball/image/upload/documents-corporate-regional-offices-europe-programs-fiba-europe-coaching-certificate-fiba-europe-basketball-terminology.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## B04 농구 점프슛 릴리스

- 종목/단계: basketball / just after release
- 검증 범위: `authored_snapshot_from_term`
- 탐색 단서: 점프슛, Jump shot

슈터의 두 신발이 코트에서 떨어져 있다; 슛 팔이 위로 뻗고 손목은 골대 쪽으로 꺾인다; 공 하나가 릴리스한 손끝에서 떨어져 있다.

both shoes are clear of the court under the shooter; the shooting arm extends upward with the wrist folded toward the basket; one ball is separate from the released fingertips.

혼동 경계: 공을 잡은 채 이미 멀리 날아가는 중복 공 금지; 득점 미확정

가시성: 손목·공 간격·발의 공중 상태

관계: shooter → owns → shooting_hand; shooting_hand → separate_from → ball; shooter → above → court

출처: [S02 FIBA Basketball Terminology](https://assets.fiba.basketball/image/upload/documents-corporate-regional-offices-europe-programs-fiba-europe-coaching-certificate-fiba-europe-basketball-terminology.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## B05 농구 레이업

- 종목/단계: basketball / near rim release
- 검증 범위: `authored_snapshot_from_term`
- 탐색 단서: 레이업, Layup

선수가 백보드 옆에서 한 손을 위로 뻗는다; 뻗은 팔과 같은 쪽 무릎이 올라간다; 이 순간 공은 그 손바닥 위이자 림 높이 아래에 놓인다.

the player reaches one hand up beside the backboard; the same-side knee rises toward the reaching arm; the ball lies above that palm below the rim height in this chosen instant.

혼동 경계: 일부 레이업의 선택된 실현; 모든 레이업의 보편 정의 아님; 덩크와 구분

가시성: 손·무릎·림·백보드 같은 축척

관계: player → owns → reaching_hand; reaching_hand → under → ball; ball → below → rim

출처: [S02 FIBA Basketball Terminology](https://assets.fiba.basketball/image/upload/documents-corporate-regional-offices-europe-programs-fiba-europe-coaching-certificate-fiba-europe-basketball-terminology.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## B06 농구 덩크 접점

- 종목/단계: basketball / ball above rim
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 덩크, Dunk

선수의 손이 림 위의 공을 다룬다; 공이 위에서 림 안쪽 공간과 겹친다; 선수는 어깨에서 공까지 팔이 끊김 없이 이어진 채 공중에 있다.

the athlete's hand controls the ball above the rim; the ball overlaps the hoop opening from above; the athlete hangs in the air with a continuous arm from shoulder to ball.

혼동 경계: 림 아래 레이업·공과 별개인 림 잡기와 구분; 득점 완료는 별도

가시성: 손과 공의 접점·림 높이

관계: athlete → owns → hand; hand → contacts → ball; ball → above → rim

출처: [S02 FIBA Basketball Terminology](https://assets.fiba.basketball/image/upload/documents-corporate-regional-offices-europe-programs-fiba-europe-coaching-certificate-fiba-europe-basketball-terminology.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## V01 배구 포어암 패스 접촉

- 종목/단계: volleyball / forearm contact
- 검증 범위: `authored_geometry_role_boundary_sourced`
- 탐색 단서: 포어암 패스, Forearm pass, 리시브, 디그

선수의 두 팔뚝이 몸 앞에서 하나의 평평한 면으로 모인다; 배구공 하나가 모인 손목 위쪽 팔뚝 면에 닿는다; 굽힌 무릎이 접점 뒤의 몸통을 지지한다.

the player's forearms join into one flat platform in front of the body; one volleyball touches that platform above the joined wrists; bent knees support the torso behind the contact.

혼동 경계: 기술 형태이며 서브 리시브·공격 디그 여부는 선행 타구 맥락 필요

가시성: 공·양팔 연속성·무릎과 지면

관계: player → owns → forearms; ball → contacts → forearms; player → supported_by → feet

출처: [S01 FIVB Official Volleyball Rules](https://www.fivb.com/wp-content/uploads/2025/01/FIVB-Volleyball_Rules2025_2028-EN-v05.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## V02 배구 오버헤드 세트

- 종목/단계: volleyball / fingertip contact
- 검증 범위: `authored_geometry_role_boundary_sourced`
- 탐색 단서: 세트·토스, Set

두 손이 이마 위로 올라가 손가락을 펼친다; 배구공 하나가 팔뚝 대신 펼친 손끝에 만난다; 손목과 팔꿈치가 공 아래의 같은 선수에게 이어진다.

both hands rise above the forehead with fingers open; one volleyball meets the spread fingertips rather than the forearms; the wrists and elbows belong to the same player under the ball.

혼동 경계: 농구 세트 플레이·테니스 세트와 문맥 분리; 모든 세트가 이 형태는 아님

가시성: 손가락 접점이 공 뒤로 모두 숨지 않는 시점

관계: player → owns → hands; hands → contacts → ball; ball → above → forehead

출처: [S01 FIVB Official Volleyball Rules](https://www.fivb.com/wp-content/uploads/2025/01/FIVB-Volleyball_Rules2025_2028-EN-v05.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## V03 배구 스파이크 타격

- 종목/단계: volleyball / overhead strike
- 검증 범위: `authored_geometry_role_boundary_sourced`
- 탐색 단서: 스파이크, Spike

타격자가 네트 한쪽에서 공중에 있다; 편 손 하나가 머리 위 배구공에 닿는다; 타격하는 어깨·팔꿈치·손이 한 선수의 관절 사슬로 이어진다.

the hitter is airborne on one side of the net; one open hand meets the volleyball above the head; the striking shoulder elbow and hand form one owned chain.

혼동 경계: 백스윙과 타격 후 팔로스루 동시 요구 금지; 득점·합법성 미확정

가시성: 네트·공·타격 손·공중 발

관계: hitter → owns → striking_hand; striking_hand → contacts → ball; hitter → beside → net

출처: [S01 FIVB Official Volleyball Rules](https://www.fivb.com/wp-content/uploads/2025/01/FIVB-Volleyball_Rules2025_2028-EN-v05.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## V04 배구 블로킹

- 종목/단계: volleyball / block at net
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 블로킹, Blocking

블로커가 네트 상단 띠 위로 두 팔을 올린다; 편 손바닥이 상대 쪽에서 오는 공을 향한다; 몸통과 두 손이 같은 블로커에게 연결된다.

the blocker lifts both arms above the net tape; open palms face the approaching ball from the opponent's side; the torso and both hands remain traceable to the same blocker.

혼동 경계: 네트 양편 선수·손을 섞지 않음; 리베로 블록은 일반 경기 실현으로 묶지 않음

가시성: 네트 경계와 손 소유를 함께 보기

관계: blocker → owns → hands; hands → above → net; hands → face → ball

출처: [S01 FIVB Official Volleyball Rules](https://www.fivb.com/wp-content/uploads/2025/01/FIVB-Volleyball_Rules2025_2028-EN-v05.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## V05 대비색 리베로 저지

- 종목/단계: volleyball / same team comparison
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 리베로 유니폼, Libero uniform, 리베로

한 선수의 저지 주색이 주변 같은 팀 선수들의 저지와 대비된다; 대비색 저지에도 그 선수의 배번이 보인다; 다른 선수들은 일관된 팀 디자인을 공유한다.

one player's jersey has a dominant colour contrasting with the nearby teammates; the contrasting jersey carries its own visible number; the other players share a consistent team design.

혼동 경계: 다른 팀 선수와 구분; 한 사람만 보이면 대비 관계 검증 불가; 특정 색 고정 금지

가시성: 같은 팀임을 정한 복수 착용자와 배번

관계: libero → wears → contrast_jersey; teammates → wear → team_jerseys; contrast_jersey → contrasts_with → team_jerseys

출처: [S01 FIVB Official Volleyball Rules](https://www.fivb.com/wp-content/uploads/2025/01/FIVB-Volleyball_Rules2025_2028-EN-v05.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## F01 축구 인스텝 킥 접점

- 종목/단계: football / instep contact
- 검증 범위: `geometry_primary_pending`
- 탐색 단서: 인스텝 킥, Instep kick

차는 발의 신발 윗면이 축구공에 닿는다; 지지 발은 공 옆 잔디에 놓인다; 차는 다리가 엉덩이를 거쳐 선수 몸에 연속된다.

the kicking foot meets the football with the top of the shoe; the support foot rests on the turf beside the ball; the kicking leg connects continuously through the bent hip to the player.

혼동 경계: 발 안쪽 패스와 구분; Law4는 장비 출처이며 킥 생체역학 검증 자료 아님

가시성: 발등 접점·지지 발·공

관계: player → owns → kicking_foot; kicking_foot → contacts → ball; support_foot → contacts → turf

출처: [S03 IFAB Law 4 Players Equipment](https://theifab.com/laws/latest/the-players-equipment/)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## F02 축구 바이시클 킥의 한 순간

- 종목/단계: football / airborne overhead contact
- 검증 범위: `geometry_primary_pending`
- 탐색 단서: 오버헤드·바이시클 킥, Bicycle kick

선수의 몸통이 경기장 위에서 뒤로 기울어진다; 올라간 발 하나가 몸통 위의 공에 닿는다; 다른 다리는 차는 다리와 합쳐지지 않고 따로 굽혀진다.

the player's torso tilts backward above the pitch; one raised foot reaches the ball above the torso; the other leg bends separately without fusing into the kicking leg.

혼동 경계: 교차 운동 전체·성공 착지·득점은 정지 사진으로 확정 불가

가시성: 두 다리 관절·공·지면 간격

관계: player → owns → kicking_leg; kicking_leg → contacts → ball; player → above → pitch

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## F03 골키퍼 다이빙 세이브 접점

- 종목/단계: football / glove ball contact
- 검증 범위: `geometry_primary_pending`
- 탐색 단서: 다이빙 세이브, Diving save

골키퍼가 몸통을 잔디에서 띄운 채 옆으로 뻗는다; 패딩 장갑이 뻗은 팔 앞에서 축구공에 닿는다; 같은 골키퍼 뒤로 골대 틀이 별도로 보인다.

the goalkeeper stretches sideways with the torso clear of the turf; a padded glove meets the football in front of the extended arm; the goal frame remains separate behind the same goalkeeper.

혼동 경계: 공에 닿음은 실점 방지 완료와 다름; 두 팔을 하나로 융합하지 않음

가시성: 장갑·공·골대·지면

관계: goalkeeper → wears → glove; glove → contacts → ball; goalkeeper → in_front_of → goal

출처: [S03 IFAB Law 4 Players Equipment](https://theifab.com/laws/latest/the-players-equipment/)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## F04 양말 안의 신가드

- 종목/단계: football / worn equipment
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 신가드, Shin guards

양말이 선수의 무릎 아래 정강이를 덮는다; 양말 아래 정강이에 국소적인 보호구 윤곽이 잡힌다; 발의 신발은 별도 장비로 구분된다.

a sock covers the player's shin below the knee; the covered shin has a localized protective outline under that sock; the shoe remains a separate item at the foot.

혼동 경계: 완전히 가려진 보호구의 실제 재질·인증은 사진으로 미확정; 외부 장착과 구별

가시성: 양말 층과 보호 윤곽; 실제 내부는 unobservable

관계: player → wears → sock; sock → covers → shinguard; shinguard → over → shin

출처: [S03 IFAB Law 4 Players Equipment](https://theifab.com/laws/latest/the-players-equipment/)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## T01 테니스 트로피 포지션

- 종목/단계: tennis / serve preparation
- 검증 범위: `geometry_primary_pending`
- 탐색 단서: 트로피 포지션, Trophy position

한 팔이 토스한 테니스공을 향해 위로 뻗는다; 라켓 팔은 굽혀지고 라켓은 상체 뒤에 놓인다; 선택한 준비 순간 두 발은 베이스라인 뒤에서 서브 선수를 지지한다.

one arm points upward toward the tossed tennis ball; the racket arm is bent with the racket behind the upper body; both feet support the server behind the baseline in this chosen preparation.

혼동 경계: 실제 타격 순간·우승 트로피 소품과 구분; ITF는 세부 포즈 교재 아님

가시성: 토스 팔·라켓 팔·공의 단일 위치

관계: server → owns → toss_arm; server → holds → racket; toss_arm → points_toward → ball

출처: [S06 ITF Tennis Glossary](https://www.itftennis.com/en/about-us/organisation/tennis-glossary/)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## T02 테니스 양손 백핸드

- 종목/단계: tennis / backswing snapshot
- 검증 범위: `authored_snapshot_from_term`
- 탐색 단서: 양손 백핸드, Two-handed backhand

두 손이 같은 라켓 손잡이의 서로 다른 위치를 잡는다; 라켓이 선수 몸통의 백핸드 쪽에 놓인다; 돌린 양어깨가 지면의 두 발 위에서 몸통에 이어진다.

two hands grip different positions on the same racket handle; the racket is held on the backhand side of the player's torso; the turned shoulders remain connected above grounded feet.

혼동 경계: 한손 백핸드·별도 두 라켓과 구분; 좌우는 선수 기준으로 지정

가시성: 두 손과 손잡이 전체 연결

관계: player → owns → hands; hands → grip → handle; handle → part_of → racket

출처: [S06 ITF Tennis Glossary](https://www.itftennis.com/en/about-us/organisation/tennis-glossary/)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## T03 테니스 스플릿 스텝 준비 순간

- 종목/단계: tennis / small airborne hop
- 검증 범위: `geometry_primary_pending`
- 탐색 단서: 스플릿 스텝, Split step

두 신발이 코트에서 조금 떨어져 있다; 무릎은 유연하게 굽히고 라켓은 몸 앞에 든다; 선수는 네트 건너 상대를 향한다.

both shoes lift only slightly above the court; the knees remain soft and the racket is carried in front; the player faces the opponent across the net.

혼동 경계: 순간 모습만으로 착지 타이밍·반응 속도 판정 불가

가시성: 양발·라켓·네트의 방향

관계: player → holds → racket; player → faces → opponent; player → above → court

출처: [S06 ITF Tennis Glossary](https://www.itftennis.com/en/about-us/organisation/tennis-glossary/)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## D01 배드민턴 네트 런지

- 종목/단계: badminton / front court reach
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 네트 런지, Net lunge, 런지

라켓 쪽 발이 네트를 향해 앞으로 디딘다; 낮춘 몸통 뒤로 뒷다리가 뻗는다; 같은 쪽 라켓이 네트 가까이 낮은 셔틀에 닿는 방향으로 뻗는다.

the racket-side foot plants forward toward the net; the rear leg stretches back behind the lowered torso; the racket reaches a low shuttle near the net on that same side.

혼동 경계: 펜싱 런지·일반 스트레칭과 구분; 모든 비상 리턴에 같은 발 강제 금지

가시성: 라켓·셔틀·앞발·뒷발

관계: player → owns → racket_hand; racket_hand → holds → racket; front_foot → contacts → court

출처: [S18 BWF Shuttle Time Teachers Manual](https://www.badminton.lv/faili/shuttletime_skolotaja_rokasgramata_eng.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## D02 배드민턴 오버헤드 스매시

- 종목/단계: badminton / overhead impact
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 오버헤드 스매시, 점프 스매시, Overhead smash, Jump smash

라켓 헤드가 선수 어깨 위의 셔틀 하나에 만난다; 타격 팔꿈치가 같은 라켓 손에 연결된다; 상대 코트가 접점 높이 아래로 네트 너머에 놓인다.

the racket head meets one shuttle above the player's shoulder; the striking elbow connects to the same raised racket hand; the opponent's court lies beyond the net below the contact height.

혼동 경계: 공을 셔틀로 대체; 점프는 별도 선택하며 모든 스매시에 강제하지 않음

가시성: 라켓 면과 셔틀 접점

관계: player → holds → racket; racket → contacts → shuttle; shuttle → above → net

출처: [S18 BWF Shuttle Time Teachers Manual](https://www.badminton.lv/faili/shuttletime_skolotaja_rokasgramata_eng.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## P01 탁구 셰이크핸드 그립

- 종목/단계: table_tennis / grip closeup
- 검증 범위: `primary_fulltext_pending`
- 탐색 단서: 셰이크핸드, Shakehand

손잡이가 선수의 손바닥에 놓인다; 검지가 라켓 면 뒷부분 아래쪽에 뻗는다; 다른 손가락들이 같은 손잡이를 감싼다.

the handle rests in the player's palm; the index finger extends along the lower back of the racket face; the other fingers wrap around the same handle.

혼동 경계: 펜홀드와 구별; 보조장구를 쓰는 선수에 동일 그립 강제 금지

가시성: 손가락·라켓 뒷면의 충분한 크기

관계: hand → grips → handle; index_finger → along → blade; handle → part_of → racket

출처: [S19 ITTF Foundation Smash Down Barriers Manual](https://ittffoundation.org/get-inspired-tt-dream-building?cid=18658&file=files%2Fcms%2Fget-inspired%2Fgi-tt-dreambuilding%2Fsmash-down-barriers_manual_hr.pdf), [S34 ITTF Penhold Article](https://www.ittf.com/2016/08/08/rio-2016-penhold-grip-dying-art/)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## P02 탁구 펜홀드 그립

- 종목/단계: table_tennis / grip closeup
- 검증 범위: `geometry_primary_pending`
- 탐색 단서: 펜홀드, Penhold

엄지와 검지가 손잡이 윗부분을 둘러 굽힌다; 라켓 면이 모아 잡은 손 아래로 이어진다; 선택한 변형에서 나머지 손가락은 반대 라켓 면에 놓인다.

the thumb and index finger curve around the top of the handle; the racket blade continues below that compact grip; the remaining fingers rest on the reverse face in this selected variant.

혼동 경계: 중국식·일본식·후면 타법 변형은 별도; 기사만으로 모든 손가락 형태 확정 금지

가시성: 그립 양면 또는 명시된 단면

관계: thumb → around → handle; index_finger → around → handle; fingers → against → blade

출처: [S34 ITTF Penhold Article](https://www.ittf.com/2016/08/08/rio-2016-penhold-grip-dying-art/)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## A01 육상 크라우칭 스타트

- 종목/단계: athletics / set position
- 검증 범위: `authored_snapshot_rule_version_scoped`
- 탐색 단서: 크라우칭 스타트, Crouch start, 스타팅 블록

두 손이 출발선 뒤 트랙에 놓인다; 두 발이 같은 스타팅 블록의 별도 페달을 누른다; 출발 전 엉덩이가 굽힌 무릎 위로 올라간다.

both hands rest on the track behind the start line; both feet press separate pedals of the same starting block; the hips rise above the bent knees before the launch.

혼동 경계: 수영 출발대·이미 질주 중인 포즈와 구분; 규정 합격은 최신 개정 재확인

가시성: 손·블록·발·출발선

관계: runner → owns → hands; hands → contacts → track; feet → contacts → block_pedals

출처: [S04 World Athletics Competition and Technical Rules](https://worldathletics.org/download/download?filename=acdec6c6-1261-4c7f-96d2-92f712707e99.pdf&urlslug=Competition+and+Technical+Rules+%E2%80%93+2026+Edition), [S05 World Athletics Technical Information](https://worldathletics.org/about-iaaf/documents/technical-information)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## A02 육상 드라이브 단계

- 종목/단계: athletics / after block clearance
- 검증 범위: `geometry_primary_pending`
- 탐색 단서: 드라이브 단계, Drive phase, 전경 자세

단거리 선수가 몸통과 엉덩이의 연속선으로 앞으로 기울어진다; 한 발이 트랙을 밀고 다른 무릎이 앞으로 나간다; 이동하는 선수 뒤에 스타팅 블록이 남아 있다.

the sprinter leans forward from a continuous trunk and hip line; one foot pushes off the track while the other knee drives forward; the starting blocks remain behind the moving athlete.

혼동 경계: 고개만 숙인 달리기와 구분; 가속도 수치·기량 판정 불가

가시성: 전신·지지 발·블록의 상대 위치

관계: runner → owns → support_foot; support_foot → contacts → track; blocks → behind → runner

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## A03 허들 클리어런스

- 종목/단계: athletics / above hurdle
- 검증 범위: `geometry_primary_pending`
- 탐색 단서: 허들 클리어런스, Hurdle clearance

리드 레그가 허들 위에서 앞으로 뻗는다; 뒤따르는 무릎은 엉덩이 뒤에서 옆으로 접힌다; 선수 몸이 허들 가로대 위에서 분리되어 있다.

the lead leg extends forward over the hurdle; the trailing knee bends out to the side behind the hip; the athlete's body stays separate above the hurdle bar.

혼동 경계: 양다리가 같은 모양인 스플릿 리프와 구별; huddle과 무관

가시성: 허들 가로대·양 무릎·엉덩이

관계: athlete → owns → lead_leg; athlete → owns → trail_leg; athlete → above → hurdle

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## A04 계주 배턴 인계 접점

- 종목/단계: athletics / shared contact during transfer
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 배턴 패스, Baton pass, 앵커

두 주자가 같은 레인 방향을 향하고 한 명이 앞선다; 뒤 주자의 손이 배턴 하나의 한쪽을 잡는다; 앞 주자가 뒤로 손을 내밀어 같은 배턴의 다른 부분에 닿는다.

two runners move in the same lane direction with one ahead; the rear runner's hand holds one end of a single baton; the front runner reaches back to contact another part of that baton.

혼동 경계: 완료 후에는 받는 사람만 소유; 앵커 지위·구역 합법성은 별도 자료

가시성: 서로 다른 팔에서 시작한 두 손과 하나의 배턴

관계: giver → owns → giving_hand; receiver → owns → receiving_hand; giving_hand → contacts → baton; receiving_hand → contacts → baton

출처: [S04 World Athletics Competition and Technical Rules](https://worldathletics.org/download/download?filename=acdec6c6-1261-4c7f-96d2-92f712707e99.pdf&urlslug=Competition+and+Technical+Rules+%E2%80%93+2026+Edition), [S05 World Athletics Technical Information](https://worldathletics.org/about-iaaf/documents/technical-information)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## S01 수영 출발대 트랙 스타트

- 종목/단계: swimming / on starting platform
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 트랙 스타트, Track start

수영 선수가 출발대 위에 두 발을 앞뒤로 놓는다; 낮춘 어깨 아래의 두 손이 출발대 앞 가장자리를 잡는다; 수면이 출발대보다 낮은 앞쪽에 놓인다.

the swimmer places the feet front and back on the starting platform; the hands hold the front edge beneath the lowered shoulders; the pool surface lies below and in front of the platform.

혼동 경계: 육상 블록·공중 입수·이미 수중 상태와 혼합 금지

가시성: 플랫폼·네 접점·수면

관계: swimmer → owns → hands; hands → grip → platform_edge; feet → contacts → platform

출처: [S07 US Masters Swimming Track Start](https://www.usms.org/fitness-and-training/articles-and-videos/articles/five-key-elements-of-a-good-track-start?Oldid=3258), [S08 World Aquatics Competition Regulations](https://www.worldaquatics.com/rules/competition-regulations)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## S02 수영 공중 입수 정렬

- 종목/단계: swimming / airborne before entry
- 검증 범위: `authored_snapshot_from_term`
- 탐색 단서: 공중 입수, Dive

두 팔이 수영 선수 머리 앞에서 나란히 뻗는다; 두 발이 출발대에서 떨어져 있다; 손끝이 수면의 한 입수 지점을 향해 아래로 향한다.

both arms stretch together ahead of the swimmer's head; the feet have left the starting platform; the fingertips point down toward one entry point on the water.

혼동 경계: 출발대 손잡기와 수중 스트림라인 동시 요구 금지

가시성: 전신·출발대 간격·입수 지점

관계: swimmer → owns → arms; swimmer → separate_from → platform; fingertips → point_toward → water

출처: [S07 US Masters Swimming Track Start](https://www.usms.org/fitness-and-training/articles-and-videos/articles/five-key-elements-of-a-good-track-start?Oldid=3258)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## S03 수중 스트림라인

- 종목/단계: swimming / underwater glide
- 검증 범위: `geometry_primary_pending`
- 탐색 단서: 스트림라인, Streamline

수영 선수가 보이는 수면 아래에 완전히 잠겨 있다; 편 두 팔이 머리 위에서 만나고 두 손이 포개진다; 몸통과 모은 다리가 길게 정렬된 실루엣을 이룬다.

the swimmer is fully beneath the visible water surface; straight arms meet above the head with hands overlapping; the torso and joined legs form one long aligned silhouette.

혼동 경계: 아르데코 Streamline Moderne·출발대 자세와 구분; 속도·무호흡 확인 아님

가시성: 물 위아래 경계·손·몸통·다리

관계: swimmer → below → water_surface; swimmer → owns → arms; left_hand → overlaps → right_hand; left_hand → part_of → swimmer; right_hand → part_of → swimmer

출처: [S08 World Aquatics Competition Regulations](https://www.worldaquatics.com/rules/competition-regulations)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## S04 접영 리커버리

- 종목/단계: swimming / arms over water
- 검증 범위: `geometry_primary_pending`
- 탐색 단서: 접영 리커버리, Butterfly recovery

두 팔이 수영 선수 양옆에서 수면 위로 뻗는다; 같은 양어깨가 등 위쪽을 거쳐 두 팔에 이어진다; 몸통이 돌아오는 두 팔 사이 수면에 놓인다.

both arms extend outward above the water on opposite sides of the swimmer; the same shoulders connect both arms across the upper back; the torso remains at the water surface between the recovering arms.

혼동 경계: 아이스하키 버터플라이·수중 풀 단계와 구별; 동시성은 영상 필요

가시성: 양팔과 수면 접경

관계: swimmer → owns → arms; arms → above → water; torso → at → water_surface

출처: [S08 World Aquatics Competition Regulations](https://www.worldaquatics.com/rules/competition-regulations)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## G01 공중 턱 형태

- 종목/단계: gymnastics / airborne body shape
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 턱 — Tuck, Tuck

체조 선수가 허벅지를 몸통 쪽으로 접는다; 두 무릎을 굽혀 종아리가 안으로 접힌다; 선택한 형태에서 두 손이 접힌 종아리 쪽에 닿는다.

the gymnast folds the thighs toward the torso; both knees bend so the lower legs tuck inward; the hands reach the folded lower legs in this chosen form.

혼동 경계: 무릎을 편 파이크·전신을 편 레이아웃과 구별; 회전수 미판독

가시성: 엉덩이와 무릎 굴곡을 동시에

관계: gymnast → owns → thighs; gymnast → owns → knees; hands → contacts → lower_legs

출처: [S16 USA Gymnastics Tumbling Code](https://members.usagym.org/PDFs/T%26T/Rules/devcop/2021/tu.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## G02 공중 파이크 형태

- 종목/단계: gymnastics / airborne body shape
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 파이크, Pike

체조 선수가 엉덩이 관절에서 몸을 접는다; 모은 다리를 따라 두 무릎은 펴져 있다; 몸통이 엉덩이 접힘을 사이에 두고 편 다리에 가까워진다.

the gymnast folds sharply at the hips; both knees remain extended along the joined legs; the torso approaches the straight legs across the hip fold.

혼동 경계: 턱과 구별 핵심은 무릎; 모든 종목 채점각 수치 강제 금지

가시성: 엉덩이와 두 무릎의 옆 실루엣

관계: torso → folds_toward → legs; gymnast → owns → knees; legs → joined_with → leg_pair

출처: [S16 USA Gymnastics Tumbling Code](https://members.usagym.org/PDFs/T%26T/Rules/devcop/2021/tu.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## G03 공중 레이아웃 형태

- 종목/단계: gymnastics / airborne straight form
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 레이아웃, Layout

몸통이 엉덩이에서 깊게 접히지 않고 펴진다; 두 다리를 따라 무릎이 펴진다; 몸이 공중에서 길게 펴진 하나의 실루엣을 이룬다.

the torso extends without a deep fold at the hips; the knees extend along both legs; the body forms one elongated airborne silhouette.

혼동 경계: 페이지 layout·스키 tuck과 문맥 분리; 회전·착지 성공 미확정

가시성: 전신 윤곽과 지면의 분리

관계: gymnast → owns → torso; gymnast → owns → legs; gymnast → above → floor

출처: [S16 USA Gymnastics Tumbling Code](https://members.usagym.org/PDFs/T%26T/Rules/devcop/2021/tu.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## G04 링 아이언 크로스

- 종목/단계: gymnastics / rings support
- 검증 범위: `geometry_primary_pending`
- 탐색 단서: 아이언 크로스, Iron cross

두 손이 각각 다른 매달린 링을 잡는다; 편 팔이 어깨에서 좌우 수평으로 뻗는다; 몸통과 모은 다리가 링 사이에 수직으로 매달린다.

each hand grips a different suspended ring; straight arms extend horizontally from the shoulders; the torso and joined legs hang vertically between the rings.

혼동 경계: 바닥 지지·십자가 소품·링 하나 양손과 구분; 기술 안정·지속 시간 미확정

가시성: 양 링·손·팔·몸통 수직

관계: left_hand → grips → left_ring; right_hand → grips → right_ring; gymnast → supported_by → rings

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## G05 핸드스탠드 지지

- 종목/단계: gymnastics / hand support
- 검증 범위: `geometry_primary_pending`
- 탐색 단서: 핸드스탠드, Handstand

두 손바닥이 어깨 아래 같은 바닥에 놓여 몸을 받친다; 팔꿈치를 펴고 몸통이 거꾸로 올라간다; 엉덩이와 다리가 손 위로 이어진다.

both palms bear on the same floor beneath the shoulders; the elbows extend as the torso rises upside down; the hips and legs continue upward above the hands.

혼동 경계: 헤드스탠드·손이 바닥에 닿지 않은 공중 동작과 구분

가시성: 손목·팔꿈치·어깨·바닥 지지

관계: gymnast → owns → palms; palms → contacts → floor; torso → above → palms

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## I01 피겨 카멜 형태

- 종목/단계: figure_skating / spin silhouette
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 카멜 스핀, Camel spin

한 스케이트가 빙판에서 선수를 지지한다; 자유 다리가 뒤로 뻗고 그 무릎이 엉덩이보다 높다; 몸통은 지지 다리 위에서 앞으로 기울어진다.

one skate supports the skater on the ice; the free leg extends backward with its knee above hip level; the torso inclines forward over the supporting leg.

혼동 경계: 스파이럴과 정지 실루엣이 겹침; 회전·레벨은 영상 필요

가시성: 지지 스케이트·자유 무릎·엉덩이

관계: skater → supported_by → support_skate; free_leg → behind → torso; support_skate → contacts → ice

출처: [S17 ISU Figure Skating Sports Rules](https://isu-d8g8b4b7ece7aphs.a03.azurefd.net/isudamcontainer/CMS/Corporate-Site/Governance/Isu-Regulations/2026-FS---Pair-Sports-Rules-FINAL-20260513-1778685370-9916.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## I02 피겨 싯 형태

- 종목/단계: figure_skating / low spin silhouette
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 싯 스핀, Sit spin

지지 무릎이 한 스케이트 위에서 깊게 굽혀진다; 지지 허벅지가 빙판과 수평 이상으로 낮아진다; 선택한 실현에서 자유 다리는 웅크린 몸 앞에 따로 놓인다.

the supporting knee bends deeply above one skate; the supporting thigh reaches at least a horizontal relation to the ice; the free leg stays separate ahead of the crouched torso in this realization.

혼동 경계: 일반 앉기·두 발 스쿼트와 구분; 회전 증거 별도

가시성: 지지 허벅지·스케이트·자유 다리

관계: skater → owns → support_leg; support_skate → contacts → ice; free_leg → in_front_of → torso

출처: [S17 ISU Figure Skating Sports Rules](https://isu-d8g8b4b7ece7aphs.a03.azurefd.net/isudamcontainer/CMS/Corporate-Site/Governance/Isu-Regulations/2026-FS---Pair-Sports-Rules-FINAL-20260513-1778685370-9916.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## I03 피겨 비엘만 형태

- 종목/단계: figure_skating / upright held-foot variation
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 비엘만 스핀, Biellmann spin

한 스케이트가 빙판에서 세운 몸통을 지지한다; 자유 발이 머리 뒤와 위로 올라간다; 선택한 잡기에서 두 손이 올린 스케이트에 눈에 보이게 이어진다.

one skate supports an upright torso on the ice; the free foot rises behind and above the head; the hands connect visibly to the raised skate in this selected hold.

혼동 경계: 카멜로 분류 금지; 스케이트 잡기·어깨 연속성 누락 금지; 회전수 미확정

가시성: 손과 들어 올린 스케이트·지지 발

관계: skater → supported_by → support_skate; hands → grip → free_skate; free_skate → above → head

출처: [S17 ISU Figure Skating Sports Rules](https://isu-d8g8b4b7ece7aphs.a03.azurefd.net/isudamcontainer/CMS/Corporate-Site/Governance/Isu-Regulations/2026-FS---Pair-Sports-Rules-FINAL-20260513-1778685370-9916.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## C01 복싱 오서독스

- 종목/단계: boxing / guard stance
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 오서독스, Orthodox

복서의 해부학적 왼발이 상대에게 더 가까이 선다; 해부학적 왼쪽 글러브도 앞선 글러브가 된다; 오른발과 오른쪽 글러브는 앞선 쪽 뒤에 남는다.

the boxer's anatomical left foot stands closer to the opponent; the anatomical left glove is also the lead glove; the rear right foot and right glove remain behind that lead side.

혼동 경계: 화면 왼쪽을 신체 왼쪽으로 오인 금지; 타고난 우세손 추정 금지

가시성: 상대 방향·양발·어깨-글러브 연결

관계: boxer → owns → left_foot; left_foot → nearer_than → right_foot; left_glove → toward → opponent

출처: [S21 IBA Coach Manual](https://www.iba.sport/documents/iba-coach-manual/)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## C02 복싱 사우스포

- 종목/단계: boxing / guard stance
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 사우스포, Southpaw

복서의 해부학적 오른발이 상대에게 더 가까이 선다; 해부학적 오른쪽 글러브도 앞선 글러브가 된다; 왼발과 왼쪽 글러브는 뒤쪽에 남는다.

the boxer's anatomical right foot stands closer to the opponent; the anatomical right glove is also the lead glove; the left foot and left glove remain on the rear side.

혼동 경계: 좌우 반전·왼손잡이 신분과 구분; 전환 자세는 특정 순간으로 기록

가시성: 상대 방향과 해부학적 좌우

관계: boxer → owns → right_foot; right_foot → nearer_than → left_foot; right_glove → toward → opponent

출처: [S21 IBA Coach Manual](https://www.iba.sport/documents/iba-coach-manual/)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## C03 복싱 하이 가드

- 종목/단계: boxing / guard held
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 하이 가드, High guard

두 글러브가 복서의 뺨과 관자놀이 가까이에 올라간다; 굽힌 팔꿈치는 글러브 아래 몸통 가까이에 놓인다; 각 손목이 추가 손 없이 자기 글러브로 이어진다.

both gloves rise near the boxer's cheeks and temples; bent elbows remain below the gloves near the torso; each wrist continues into its own glove without an extra hand.

혼동 경계: 군중의 주먹 세리머니와 구분; 특정 방어 성공·공포 미확정

가시성: 얼굴과 양 글러브·팔꿈치

관계: boxer → wears → gloves; gloves → near → face; elbows → below → gloves

출처: [S21 IBA Coach Manual](https://www.iba.sport/documents/iba-coach-manual/)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## C04 복싱 클린치 접촉

- 종목/단계: boxing / close torso contact
- 검증 범위: `authored_snapshot_from_term`
- 탐색 단서: 클린치, Clinch

두 복서가 몸통이 가까운 거리에서 마주한다; 글러브를 낀 팔이 상대 상체 사이 또는 주변으로 접힌다; 보이는 글러브마다 한 복서의 어깨까지 이어진다.

two boxers face each other at close torso distance; their gloved arms fold between or around the opposing upper bodies; each visible glove traces to one boxer's shoulder.

혼동 경계: 포옹·MMA 지상 기술·합법성·동의와 동일시 금지

가시성: 두 몸의 경계·팔 소유·발 지지

관계: boxer_a → faces → boxer_b; arm_a → contacts → torso_b; arm_b → contacts → torso_a

출처: [S21 IBA Coach Manual](https://www.iba.sport/documents/iba-coach-manual/)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## E01 펜싱 앙가르드

- 종목/단계: fencing / ready stance
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 앙가르드, En garde

앞 무릎이 피스트를 따라 상대 쪽으로 굽혀진다; 검 손이 가드를 손과 상대 사이에 두고 검 하나를 앞으로 든다; 뒷발이 앞발 뒤에서 몸을 지지한다.

the front knee bends toward the opponent along the piste; the weapon hand holds one blade forward with the guard between hand and opponent; the rear foot supports the body behind the front foot.

혼동 경계: 실제 런지의 길게 뻗은 뒷다리와 구분; 검 손의 좌우 임의 고정 금지

가시성: 검 손·가드·양발·피스트

관계: fencer → holds → weapon; weapon → toward → opponent; feet → contacts → piste

출처: [S09 British Fencing Glossary](https://www.britishfencing.com/glossary-of-terms/)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## E02 펜싱 런지

- 종목/단계: fencing / extended attack
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 런지·팡트, Lunge, Fente

검 팔이 피스트 위 상대를 향해 뻗는다; 앞 무릎이 앞으로 디딘 발 위에서 굽혀진다; 뒷발이 지지한 채 뒷다리가 뒤로 펴져 도달을 받친다.

the weapon arm extends toward the opponent on the piste; the front knee bends over the forward planted foot; the rear leg extends back with the rear foot supporting the reach.

혼동 경계: 배드민턴 네트 런지·스트레칭과 구분; 찌르기 성공과 별개

가시성: 검·상대 방향·두 지지 발

관계: fencer → holds → weapon; front_foot → contacts → piste; rear_foot → contacts → piste

출처: [S09 British Fencing Glossary](https://www.britishfencing.com/glossary-of-terms/)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## E03 플뢰레 라메 겹침

- 종목/단계: fencing_foil / equipment worn
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 라메, Lamé, 플뢰레

금속처럼 보이는 민소매 겉조끼가 펜싱 선수의 몸통을 덮는다; 흰 보호 재킷 소매가 그 바깥층 아래 별도로 남는다; 마스크 목 덮개와 보이는 연결선이 같은 선수에게 이어진다.

a sleeveless metallic-looking over-jacket covers the fencer's torso; the white protective sleeves remain separate below that outer layer; the mask bib and its visible connecting lead stay attached to the same fencer.

혼동 경계: 사브르의 소매 범위·에페와 구분; 광택만으로 전도성·인증 주장 금지

가시성: 겨드랑이·겹침 경계·마스크 연결

관계: fencer → wears → protective_jacket; lame → over → protective_jacket; mask_lead → connects_to → lame

출처: [S10 FIE Material Rules](https://static.fie.org/uploads/40/204156-book%20material%20August%202026%20ang.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## E04 사브르 라메 겹침

- 종목/단계: fencing_sabre / equipment worn
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 라메, Lamé, 사브르

금속처럼 보이는 겉재킷이 몸통과 양팔 손목까지 덮는다; 칼라 위 마스크는 별도 망 면과 목 덮개를 갖는다; 검 손 장갑이 같은 재킷 손목 부위와 겹친다.

the metallic-looking outer jacket covers the torso and both arms to the wrists; the mask has a separate mesh face and bib above the collar; the weapon glove overlaps the wrist area of the same jacket.

혼동 경계: 플뢰레 민소매 조끼와 구분; 하부 보호층은 가려지면 실증 불가

가시성: 소매 전체·손목·마스크

관계: fencer → wears → lame; lame → covers → arms; glove → overlaps → lame_wrist

출처: [S10 FIE Material Rules](https://static.fie.org/uploads/40/204156-book%20material%20August%202026%20ang.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## R01 리커브 풀 드로

- 종목/단계: archery_recurve / before release
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 풀 드로, 앵커링, Full draw, Anchoring

활 손이 중앙 손잡이를 잡고 과녁 쪽으로 활을 뻗는다; 선택한 방식에서 시위 손이 얼굴 쪽 일정한 기준점까지 당긴다; 화살 하나가 활의 받침 위에 놓이고 팽팽한 시위에 걸린다.

the bow hand holds the central grip with the bow extended toward the target; the string hand draws to a consistent face-side anchor in this chosen style; one arrow rests on the bow and nocks onto the taut string.

혼동 경계: 릴리스 후 모습·느슨한 전시용 활·컴파운드 보조기와 구분

가시성: 화살 길이·시위 경로·양손·과녁 방향

관계: archer → owns → bow_hand; bow_hand → holds → bow; string_hand → contacts → string; arrow → nocked_on → string

출처: [S11 World Archery Recurve](https://www.worldarchery.sport/sport/equipment/recurve)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## R02 컴파운드 릴리스 보조기

- 종목/단계: archery_compound / before release
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 풀 드로, 컴파운드, Compound

캠과 케이블이 소형 활 양끝을 잇는다; 당기는 손이 화살의 D루프 부근에 연결된 릴리스 보조기를 다룬다; 화살 하나가 받침에서 과녁 쪽으로 정렬된다.

cams and cables connect the ends of the compact bow; the drawing hand controls a release aid attached near the arrow's D-loop; one arrow aligns from its rest toward the target.

혼동 경계: 손가락으로 시위를 직접 당기는 리커브 형태와 혼합 금지; 모든 파라 변형에 강제 금지

가시성: 보조기·루프·노크·화살 받침

관계: archer → holds → bow; release_aid → connects_to → d_loop; arrow → rests_on → arrow_rest

출처: [S12 World Archery Compound](https://www.worldarchery.sport/sport/equipment/compound)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## R03 양궁 보호구 소유 관계

- 종목/단계: archery_recurve / equipment detail
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 체스트가드, 암가드, 핑거탭

작은 암가드가 활 쪽 팔뚝 위에 놓인다; 핑거탭이 당기는 손가락과 시위 사이에 놓인다; 체스트가드가 활 쪽 의복을 시위 경로 바깥으로 정리한다.

a small arm guard lies on the bow-side forearm; a finger tab separates the drawing fingers from the string; a chest guard contains the bow-side clothing away from the string path.

혼동 경계: 체스트가드와 브라·갑옷, 암가드와 손목밴드를 구분; 좌우는 활 손에 따라

가시성: 두 팔의 역할·시위 경로·착용 경계

관계: arm_guard → on → bow_forearm; finger_tab → contacts → drawing_fingers; finger_tab → contacts → string; chest_guard → over → clothing

출처: [S11 World Archery Recurve](https://www.worldarchery.sport/sport/equipment/recurve)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## H01 하키 골리 버터플라이

- 종목/단계: ice_hockey / low save stance
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 골리 버터플라이, Butterfly

골리의 두 무릎이 모여 빙판 쪽으로 내려간다; 큰 다리 패드가 바깥으로 벌어져 골대 아래 공간을 막는다; 스틱 블레이드가 몸통 앞 빙판에 놓인다.

the goalie's knees descend together toward the ice; the large leg pads flare outward to close the lower goal area; the stick blade remains on the ice ahead of the torso.

혼동 경계: 수영 접영·단순 스플릿과 구분; 패드가 다리와 분리된 장비임

가시성: 무릎·패드 하단·스틱·골대

관계: goalie → wears → pads; pads → near → ice; stick_blade → contacts → ice

출처: [S15 Hockey Canada Butterfly Mechanics](https://cdn.hockeycanada.ca/hockey-canada/Hockey-Programs/Players/Goaltending/Downloads/goaltending-butterfly-e.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## H02 하키 슬랩샷 준비

- 종목/단계: ice_hockey / backswing snapshot
- 검증 범위: `geometry_primary_pending`
- 탐색 단서: 슬랩샷, Slap shot

두 글러브가 같은 하키 스틱의 서로 다른 위치를 잡는다; 선택한 백스윙에서 블레이드가 돌아선 몸통 뒤로 올라간다; 퍽 하나가 선수 앞 빙판에 놓인다.

both gloves grip different locations on the same hockey stick; the blade rises behind the turned torso in this backswing; one puck stays on the ice ahead of the player.

혼동 경계: 백스윙·접촉·팔로스루를 동시에 고정하지 않음

가시성: 두 손·스틱 전체·퍽

관계: player → holds → stick; stick_blade → part_of → stick; puck → on → ice

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## Q01 럭비 유니언 스크럼 부분 대형

- 종목/단계: rugby_union / bound front rows
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 스크럼, Scrum

양 팀의 앞줄이 낮고 정렬된 자세로 마주한다; 보이는 결합 팔마다 동료 또는 상대 저지의 특정 지점을 잡는다; 발들이 결합한 몸 아래 잔디에서 지지한다.

the opposing front rows face each other in low aligned stances; each visible binding arm grips a teammate or opponent's jersey at an identified point; feet support the joined bodies on the turf below.

혼동 경계: 유니언 풀 대형·세븐스·축소 드릴 인원 구분; 가려진 전원 수를 판정하지 않음

가시성: 장면 범위와 선수 수·결합 팔·지지 발

관계: front_row_a → faces → front_row_b; binding_hand → grips → jersey; feet → contacts → turf

출처: [S20 World Rugby Law 19 Scrum](https://passport.world.rugby/laws-of-the-game/laws-by-number/19-scrum/)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## Q02 미식축구 스리포인트 스탠스

- 종목/단계: american_football / before snap
- 검증 범위: `geometry_primary_pending`
- 탐색 단서: 스리포인트 스탠스, Three-point stance

웅크린 선수 아래 두 발이 경기장에 디딘다; 한 손이 세 번째 지지점으로 잔디에 닿는다; 다른 팔은 몸 옆에서 지면에 닿지 않는다.

two feet plant on the field under the crouched athlete; one hand contacts the turf as a third support point; the other arm remains free beside the body.

혼동 경계: 럭비 스크럼·네 점 지지·공을 잡은 센터와 구별

가시성: 두 발과 한 손의 세 접점

관계: athlete → owns → support_hand; support_hand → contacts → turf; feet → contacts → turf

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## Y01 사이클 에어로 자세

- 종목/단계: cycling / seated low torso
- 검증 범위: `geometry_primary_pending`
- 탐색 단서: 에어로 포지션, Aero position

사이클 선수의 몸통이 자전거 상단 튜브 위로 낮아진다; 두 손이 선택한 핸들바 접점에 놓인다; 골반은 안장 위에 놓이고 두 발은 페달에 연결된다.

the rider's torso lowers above the bicycle top tube; the hands rest on the selected handlebar contact points; the pelvis rests on the saddle while both feet connect to pedals.

혼동 경계: 로드 드롭바와 타임트라이얼 에어로바 별도 변형; 항력 수치 미확정

가시성: 손·바·골반·페달·바퀴의 공간

관계: rider → supported_by → saddle; hands → contacts → handlebar; feet → contacts → pedals

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## Y02 사이클 댄싱

- 종목/단계: cycling / standing on pedals
- 검증 범위: `geometry_primary_pending`
- 탐색 단서: 아웃 오브 더 새들, Out of the saddle, 댄싱

선수 골반이 안장에서 눈에 보이게 떨어져 있다; 두 신발이 엉덩이 아래 페달에 이어진다; 두 손이 핸들바에서 앞으로 기운 몸통을 받친다.

the rider's pelvis is visibly clear of the saddle; both shoes connect to the pedals beneath the hips; the hands support the forward torso on the handlebars.

혼동 경계: 안장에 앉은 에어로 자세·음악 춤과 구분

가시성: 안장 간격·두 페달·손 지지

관계: rider → separate_from → saddle; feet → contacts → pedals; hands → contacts → handlebar

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## Y03 사이클 집단과 일렬 배치

- 종목/단계: cycling / riding formation
- 검증 범위: `geometry_primary_pending`
- 탐색 단서: 펠로톤·드래프팅, Peloton, Drafting, 도메스티크

여러 사이클 선수가 도로의 같은 방향을 향한다; 뒤따르는 자전거가 바퀴 겹침 없이 앞 자전거 뒤에 놓인다; 선수마다 별도의 자전거에 연결된다.

multiple cyclists share the same road direction; one trailing bicycle sits behind another without wheel overlap; each rider remains connected to a separate bicycle.

혼동 경계: 바람·항력 절감·도메스티크 임무·승부조작을 배치만으로 확정 금지

가시성: 바퀴 간격과 선수-자전거 대응

관계: trailing_rider → behind → leading_rider; rider_a → rides → bicycle_a; rider_b → rides → bicycle_b

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## N01 스노보드 그랩 접점

- 종목/단계: snowboard / airborne held edge
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 그랩, Grab

두 부츠가 보드 하나의 별도 바인딩에 붙어 있다; 지정한 손 하나가 바인딩 사이 선택한 보드 엣지를 잡는다; 보드가 눈에서 떨어진 채 다른 팔은 별도로 남는다.

both boots stay attached to separate bindings on one board; one identified hand grips a selected board edge between the bindings; the other arm remains separate while the board clears the snow.

혼동 경계: 보드 대신 부츠·무릎 잡기는 같은 그랩으로 통과하지 않음; 회전수 미확정

가시성: 손-엣지 접점·두 바인딩·공중 간격

관계: rider → wears → boots; boots → attached_to → bindings; hand → grips → board_edge

출처: [S30 FIS Snowboard Tricks List](https://www.fis-ski.com/DB/snowboard/park-and-pipe/tricks-list.html?disciplinecode=HP&sectorcode=SB)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## N02 스키 턱 자세

- 종목/단계: alpine_ski / low gliding stance
- 검증 범위: `geometry_primary_pending`
- 탐색 단서: 턱 자세, Tuck position

스키 선수가 굽힌 무릎 위로 몸통을 낮춘다; 두 스키가 각각의 부츠 아래에 따로 놓인다; 선택한 실현에서 손은 앞에 있고 폴은 뒤로 뻗는다.

the skier lowers the torso over bent knees; two separate skis remain under their corresponding boots; the hands stay forward while the poles extend back in this realization.

혼동 경계: 체조 공중 tuck과 구분; 카빙 궤적·속도·엣지각은 별도

가시성: 스키-부츠 대응·무릎·폴

관계: skier → wears → boots; boots → attached_to → skis; skis → contacts → snow

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## W01 훈련 비브 겹침

- 종목/단계: multi_sport / worn over jersey
- 검증 범위: `existing_candidate_reuse`
- 탐색 단서: 훈련 조끼·비브·피니, Training bib, Pinnie

메시 훈련 조끼가 반소매 저지 위에 겹쳐진다; 저지 소매가 조끼 진동 바깥으로 드러난다; 조끼 밑단이 저지 밑단과 구별된다.

a mesh training bib lies over a short-sleeved jersey; the jersey sleeves remain visible outside the bib armholes; the bib's lower edge stays distinct from the jersey hem.

혼동 경계: 레이스 비브·사이클 빕 쇼츠와 구분

가시성: 진동과 밑단의 두 겹 경계

관계: athlete → wears → jersey; bib → over → jersey; bib → has → armholes

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## W02 레이스 비브 부착

- 종목/단계: athletics / number sheet attached
- 검증 범위: `authored_snapshot_from_term`
- 탐색 단서: 배번호판·레이스 비브, Race bib, 배번

별도 직사각형 번호판이 달리기 선수 상의 위에 놓인다; 번호판은 자체 가장자리와 보이는 부착 지점을 갖는다; 번호판 네 변 밖으로 상의가 이어진다.

a separate rectangular number sheet lies over the runner's shirt; the sheet has its own edges and visible fastenings; the underlying shirt continues outside all sides of that sheet.

혼동 경계: 상의에 인쇄한 저지 번호·훈련 조끼와 구분; 참가자 실명 판독 불필요

가시성: 번호판 경계·부착·상의 소유

관계: runner → wears → shirt; number_sheet → attached_to → shirt; number_sheet → has → fastenings

출처: [S04 World Athletics Competition and Technical Rules](https://worldathletics.org/download/download?filename=acdec6c6-1261-4c7f-96d2-92f712707e99.pdf&urlslug=Competition+and+Technical+Rules+%E2%80%93+2026+Edition)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## W03 사이클 빕 쇼츠 구조

- 종목/단계: cycling / garment structure view
- 검증 범위: `existing_candidate_refine`
- 탐색 단서: 빕 쇼츠, Bib shorts

밀착 쇼츠가 위로 이어져 두 어깨 스트랩이 된다; 스트랩은 짧은 바지 부분과 같은 의복에 속한다; 상부 빕 구조가 실제로 보이는 상태로 의복을 제시한다.

fitted shorts continue upward into two shoulder straps; the straps belong to the same garment as the short legs; the garment is displayed so the upper bib construction is actually visible.

혼동 경계: 저지가 완전히 덮으면 스트랩 실증 불가; 내부 패드 노출 강제 금지

가시성: 의복 단독·상의 열린 상태 등 선택한 가시성

관계: straps → part_of → bib_shorts; short_legs → part_of → bib_shorts; bib_shorts → has → upper_bib

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## W04 육상 싱글렛

- 종목/단계: athletics / separate upper garment
- 검증 범위: `authored_structure_primary_pending`
- 탐색 단서: 싱글렛, Singlet

민소매 러닝 상의가 독립된 밑단에서 끝난다; 아래 반바지가 별도 의복으로 시작한다; 진동과 목둘레가 같은 상의에 속한다.

a sleeveless running top ends at a separate lower hem; shorts begin below as a different garment; the armholes and neckline belong to that upper top.

혼동 경계: 레슬링 일체복·유니타드와 구분

가시성: 상하의 분리선·진동

관계: runner → wears → top; top → separate_from → shorts; armholes → part_of → top

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## W05 레슬링 싱글렛

- 종목/단계: wrestling / one piece garment
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 싱글렛, Singlet

밀착 민소매 몸통이 두 짧은 바지 다리로 이어진다; 허리 연결을 끊는 별도 셔츠 밑단이 없다; 어깨끈과 바지 다리 입구가 한 의복에 속한다.

a fitted sleeveless torso continues into two short legs; no separate shirt hem interrupts the waist connection; the straps and leg openings belong to one continuous garment.

혼동 경계: 육상 민소매 상의와 구분; 특정 체형·성별 자동 결합 금지

가시성: 허리 연속성·어깨끈·다리 길이

관계: straps → part_of → singlet; short_legs → part_of → singlet; torso_panel → continuous_with → short_legs

출처: [S36 UWW Uniform Regulations](https://cdn.uww.org/2026-01/uniform_regulations_jan2025_final.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## W06 레오타드와 유니타드 구별

- 종목/단계: gymnastics / garment silhouette
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 레오타드, 유니타드, Leotard, Unitard

선택한 유니타드는 몸통에서 양 다리 부분으로 직접 이어진다; 선택한 체조 형태에서 다리 부분이 엉덩이부터 발목까지 양 다리를 덮는다; 허리에 별도 바지 허리밴드가 없다.

the selected unitard connects its torso directly to both leg sections; the leg sections cover both legs from hips to ankles in this selected gymnastics form; the waist has no separate trouser waistband.

혼동 경계: 레오타드는 다른 다리 입구 형태의 별도 후보로 추가; 이 비교 카드로 모든 길이 고정 금지

가시성: 허리 연결·의복 끝 위치

관계: wearer → wears → unitard; torso_panel → continuous_with → leg_sections; leg_sections → covers → thighs

출처: [S35 Gymnastics NZ Competition Attire](https://www.gymnasticsnz.com/attire/), [S38 World Gymnastics Clothing and Advertising](https://www.worldgymnastics.sport/publicdir/rules/files/en_Advertising%20Rules%20Competition%20Clothing%20-%20valid%20from%20May%202024.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## W07 스코트의 겹친 구조

- 종목/단계: tennis / selected visible construction
- 검증 범위: `existing_candidate_refine`
- 탐색 단서: 스코트, Skort

바깥 치마 패널이 안쪽 반바지를 둘러싼다; 반바지는 분리된 두 다리 입구를 갖는다; 구조를 보여주는 이 장면에서 치마와 쇼츠가 같은 허리에 연결된다.

an outer skirt panel surrounds a separate pair of inner shorts; the shorts have two distinct leg openings; the skirt and shorts connect at the same waist in this construction view.

혼동 경계: 안감·노출 사고·성적 의도로 대체 금지; 닫힌 치마에서는 내부 unobservable

가시성: 제품 구조도 또는 자연스럽게 보이는 옷 경계

관계: skirt_panel → outside → inner_shorts; skirt_panel → attached_to → waist; inner_shorts → attached_to → waist

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## W08 윔블던 화이트 범위

- 종목/단계: tennis_wimbledon / clothing appearance
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 테니스 화이트, Tennis whites

이 대회 설정에서 보이는 테니스 의상이 주로 흰색이다; 상의와 하의는 각각의 봉제선과 가장자리를 유지한다; 선택한 어두운 이너 쇼츠는 치마 아래 별도 층으로 남는다.

the visible tennis clothing is predominantly white in this tournament setting; the shirt and lower garment retain distinct seams and edges; any selected dark inner shorts remain a separate layer beneath the skirt.

혼동 경계: 모든 테니스 흰색·흰색=정숙·이너 노출 강제 금지; 2023 자료 범위

가시성: 겉옷 색 분포와 별도 층; 세부 합법성은 미판정

관계: player → wears → tennis_clothing; inner_shorts → under → skirt; seams → part_of → clothing

출처: [S28 Wimbledon White Clothing Rule](https://www.wimbledon.com/pdf/4.%20Media%20Fact%20Sheet%20-%20White%20Clothing%20Rule%202023.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## W09 수영복 길이와 연결

- 종목/단계: swimming / garment comparison
- 검증 범위: `authored_structure_primary_pending`
- 탐색 단서: 재머, Jammers

선택한 재머가 몸통 아래 허리밴드에서 시작한다; 이 실현에서는 밀착된 두 다리 부분이 허벅지 아래 부근에서 끝난다; 위 몸통은 수영 하의와 연결되지 않는다.

the selected jammer begins at a waistband below the torso; two fitted leg sections end around the lower thighs in this realization; the bare upper torso remains separate from the swimming bottoms.

혼동 경계: 니 스킨은 몸통 연결의 별도 형식; 웻수트·브리프와 구별; 규정 수치 미검증

가시성: 허리 시작점·다리 끝·몸통 연결 유무

관계: swimmer → wears → jammers; jammers → has → waistband; jammers → covers → thighs

출처: [S08 World Aquatics Competition Regulations](https://www.worldaquatics.com/rules/competition-regulations), [S37 USA Swimming Speedo Tech Suit Database](https://www.usaswimming.org/docs/default-source/rules-regulations/tech-suit-restrictions/speedo-120220.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## W10 레이스 수트와 발라클라바

- 종목/단계: motorsport / protective clothing layers
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 레이스 수트·오버올, 발라클라바, Race suit, Balaclava

일체형 겉수트가 몸통에서 양 바지 다리로 이어진다; 별도 밀착 후드가 헬멧 아래 머리와 목을 감싼다; 장갑이 수트 소맷단과 겹치며 손이 따로 떠 있지 않다.

a one-piece outer suit joins the torso to both trouser legs; a separate close hood surrounds the head and neck beneath the helmet; gloves overlap the suit cuffs without exposed floating hands.

혼동 경계: 레이싱 의상 외형과 실제 난연 인증·보호시간은 별개; 카트 규정 자동 적용 금지

가시성: 후드-헬멧·소맷단-장갑 층

관계: driver → wears → suit; balaclava → under → helmet; gloves → overlap → suit_cuffs

출처: [S31 FIA Protective Clothing Safety Guidelines](https://www.fia.com/sites/default/files/guidelines_safety_clothing_to_publish_bd.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## W11 도복의 종목별 구조 비교

- 종목/단계: martial_arts / garment construction
- 검증 범위: `authored_structure_primary_pending`
- 탐색 단서: 도복, Gi, Dobok

선택한 유도 재킷의 깃이 몸통 앞에서 겹친다; 별도 띠가 재킷 허리를 둘러싼다; 재킷 밑단 아래 바지가 별도 의복으로 남는다.

the selected judo jacket has overlapping lapels across the torso; a separate belt wraps around the jacket waist; trousers remain a different garment below the jacket hem.

혼동 경계: 태권도 V넥·가라테 깃·띠 급수는 별도 조사; 모든 도복에 같은 구조 강제 금지

가시성: 앞깃 여밈·띠·상의 밑단

관계: athlete → wears → jacket; belt → around → jacket_waist; jacket → overlaps → trousers

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## W12 역사 체육복 블루머

- 종목/단계: historical_sportswear / 1890s US reference
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 레트로 체육복·부르마, Bloomers

헐렁한 블라우스 아래 풍성하게 나뉜 하의 다리가 놓인다; 하의 다리는 각각 끝단에서 모인다; 허리 장식띠가 블라우스·하의와 별도로 남는다.

a loose blouse sits above voluminous divided lower legs; the lower legs gather at their own cuffs; the waist sash remains separate from both blouse and lower garment.

혼동 경계: 1893–98 미국 유물과 일본 짧은 후기 부르마를 동의어 처리 금지

가시성: 박물관 유물 형태와 시대·지역 표기

관계: blouse → above → bloomers; bloomers → has → gathered_cuffs; sash → around → waist

출처: [S29 Met Museum Gym Suit 2009.300.884a–f](https://www.metmuseum.org/art/collection/search/159463)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## Z01 육상 경주 휠체어

- 종목/단계: para_athletics / race chair structure
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 패러스포츠물, Classification, 휠체어

경주용 휠체어는 긴 프레임 앞에 바퀴 하나를 둔다; 큰 뒷바퀴 두 개가 선수 좌석 양옆에 놓인다; 선수의 두 손이 각각 대응하는 푸시림에 가까이 간다.

the racing chair has a long frame with one front wheel; two large rear wheels flank the athlete's seat; the athlete's hands approach the corresponding push rims.

혼동 경계: 일상 의자·농구 의자와 구분; 등급·진단·장애 원인은 외형 미판정

가시성: 프레임·바퀴 수·손-림·좌석

관계: athlete → seated_in → chair; front_wheel → part_of → chair; rear_wheels → beside → seat; hands → near → push_rims

출처: [S13 IPC Classification](https://www.paralympic.org/classification), [S14 IPC Wheelchairs in Wheelchair Sports](https://www.paralympic.org/news/para-sport-explained-wheelchairs-wheelchair-sports)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## Z02 코트 스포츠 휠체어

- 종목/단계: wheelchair_basketball / court chair structure
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 패러스포츠물, 휠체어 농구

스포츠 의자가 기울어진 큰 바퀴 두 개 사이 낮은 위치에서 선수를 지지한다; 작은 캐스터 바퀴가 바닥 가까이에 별도로 남는다; 선수 몸통이 의자 좌석 위로 이어진다.

the sport chair supports the player low between two cambered large wheels; small caster wheels remain separate near the floor; the player's trunk stays connected above the chair seat.

혼동 경계: 경주용 앞 긴 단일 휠·럭비 범퍼를 자동 결합 금지; 개인 등급 미판정

가시성: 좌석·캠버·캐스터·선수 연결

관계: player → seated_in → chair; large_wheels → part_of → chair; casters → near → floor

출처: [S13 IPC Classification](https://www.paralympic.org/classification), [S14 IPC Wheelchairs in Wheelchair Sports](https://www.paralympic.org/news/para-sport-explained-wheelchairs-wheelchair-sports)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## L01 선수와 코치의 작전판 관계

- 종목/단계: multi_sport / instruction snapshot
- 검증 범위: `authored_relational_proposal`
- 탐색 단서: 감독·코치, 작전판·클립보드, 분석관

한 사람이 코트처럼 보이는 선이 있는 판을 든다; 다른 사람의 시선과 몸통이 그 판을 향한다; 가리키는 손은 판을 든 사람에게 속한다.

one person holds a board with visible court-like lines; another person's gaze and open torso face that board; the pointing hand belongs to the board holder.

혼동 경계: 권한·전술 실효성·고용·멘토 경력은 외형만으로 확인 불가

가시성: 손 소유·판·시선 대상

관계: coach → holds → board; coach_hand → points_to → board; athlete → looks_toward → board

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## L02 팀 원진

- 종목/단계: multi_sport / group gathered
- 검증 범위: `authored_relational_proposal`
- 탐색 단서: 팀 원진, Team huddle

여러 동료가 안쪽을 향해 원을 이룬다; 보이는 팔마다 옆 동료 가까이에서 자기 어깨로 이어진다; 중앙의 빈 공간이 둘러선 몸들과 구별된다.

several teammates form an inward-facing ring; each visible arm links to its own shoulder near the adjacent teammate; a clear central space separates the surrounding bodies.

혼동 경계: hurdle 장애물·원형 관중·자동 단결 증명과 구분

가시성: 머리·몸통·팔 소유·원 안 빈 공간

관계: teammates → face → centre; arm_a → near → teammate_b; teammates → around → centre

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## L03 하이파이브 접점

- 종목/단계: multi_sport / palm contact
- 검증 범위: `authored_relational_proposal`
- 탐색 단서: 하이파이브, High five

두 선수가 팔 하나씩 같은 만남 지점으로 올린다; 그 지점에서 편 손바닥이 만난다; 손목마다 다른 선수에게 이어진다.

two athletes raise one arm each toward the same meeting point; their open palms meet at that point; each wrist traces back to a different athlete.

혼동 경계: 피스트 범프·가까운 두 손의 비접촉과 구분; 우정·우승 미확정

가시성: 손바닥 접촉면과 양팔 소유

관계: athlete_a → owns → hand_a; athlete_b → owns → hand_b; hand_a → contacts → hand_b

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## L04 무릎 위 손의 휴식 자세

- 종목/단계: multi_sport / rest stance
- 검증 범위: `authored_snapshot_claim_limited`
- 탐색 단서: 무릎에 손을 짚기, Hands on knees, 벌어진 입·거친 호흡·처진 어깨

선수가 굽힌 무릎 위로 몸통을 숙인다; 손바닥마다 무릎 위 대응하는 허벅지에 놓인다; 손 접점을 숨기지 않은 채 머리가 어깨 사이로 낮아진다.

the athlete bends the torso over flexed knees; each palm rests on the corresponding thigh above the knee; the head lowers between the shoulders without hiding the hand contacts.

혼동 경계: 패배·입스·번아웃·질환·호흡 소리 단정 금지

가시성: 양 손-허벅지와 발 지지

관계: left_hand → contacts → left_thigh; right_hand → contacts → right_thigh; feet → contacts → floor

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## L05 신발 끈 묶기 접점

- 종목/단계: multi_sport / lace handling
- 검증 범위: `authored_relational_proposal`
- 탐색 단서: 신발 끈 묶기, Tying shoelaces

선수가 지지된 한 발의 신발 쪽으로 몸을 굽힌다; 두 손이 같은 신발의 서로 다른 끈 끝을 잡는다; 끈이 같은 신발 갑피의 구멍에서 나온다.

the athlete bends toward one shoe on a supported foot; two hands each hold a separate lace end of that shoe; the lace emerges through eyelets on that same shoe upper.

혼동 경계: 다른 신발 끈·허공 매듭·매듭 완료와 구분

가시성: 손-끈-아일렛의 연결

관계: athlete → owns → hands; hands → grip → lace_ends; laces → through → shoe_eyelets

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## L06 착용 테이핑 경로

- 종목/단계: multi_sport / visible applied tape
- 검증 범위: `existing_diagnostic_plus_authored_visual`
- 탐색 단서: 테이핑·서포터, Taping, Support

테이프 띠가 같은 손목을 따라 연속된 경로로 감긴다; 테이프 가장자리가 피부·소매와 구별된다; 그 손목 너머로 손가락이 이어진다.

a strip of tape follows a continuous path around the same wrist; its edges remain distinct from the skin and sleeve; the fingers emerge beyond that supported wrist.

혼동 경계: 예방·부상·치료 효과·진단은 외형으로 확정 불가

가시성: 테이프 경로·피부 경계·손목 소유

관계: tape → around → wrist; wrist → part_of → athlete; tape → separate_from → sleeve

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## L07 땀과 젖은 원단의 표면

- 종목/단계: multi_sport / surface state
- 검증 범위: `authored_surface_proposal`
- 탐색 단서: 땀방울·땀광, 웨트 룩·젖은 유니폼, Wet look, Wet uniform

작은 물방울과 반사광이 보이는 피부 위에 남는다; 어두워진 젖은 패치가 같은 저지 패널 일부를 따른다; 저지는 자체 봉제선·주름·불투명 경계를 유지한다.

small droplets and highlights remain on the visible skin; darker damp patches follow parts of the same jersey panel; the jersey retains its own seams folds and opaque boundaries.

혼동 경계: 물·비·땀의 원인·탈수·성적 의도·투명성 자동 추가 금지

가시성: 피부와 원단의 별도 표면

관계: droplets → on → skin; damp_patches → on → jersey; seams → part_of → jersey

출처: [S25 IOC Portrayal Guidelines](https://www.olympics.com/ioc/gender-equality/portrayal-guidelines)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## L08 사용 흔적의 국소 부착

- 종목/단계: multi_sport / visible wear
- 검증 범위: `authored_surface_proposal`
- 탐색 단서: 잔디 얼룩·흙먼지, 마찰 자국·닳은 장비, Scuff marks, Worn gear

흙처럼 보이는 국소 얼룩이 반바지 한쪽 무릎 부근에 남는다; 해당 부위의 원단 봉제선이 구별된다; 별도 신발 앞코에 닳은 패치가 놓인다.

a localized soil-like smear follows one knee area of the shorts; the material seam stays visible through the affected area; a scuffed patch lies on a separate shoe toe.

혼동 경계: 경력·가난·최근 충돌·오염 성분은 흔적만으로 미확정

가시성: 흔적-의복·신발 소유 위치

관계: smear → on → shorts; seam → part_of → shorts; scuff → on → shoe

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## L09 초크와 손·기구의 관계

- 종목/단계: gymnastics / hand preparation
- 검증 범위: `authored_surface_proposal`
- 탐색 단서: 초크 가루·초크 구름, Chalk

흰 가루처럼 보이는 잔여물이 선수 손바닥 일부에 묻는다; 미세 입자가 떨어진 두 손 가까이에 떠 있다; 가까운 기구는 별도 고체 물체로 남는다.

white powder-like residue coats parts of the athlete's palms; fine particles hang close to the separated hands; the nearby apparatus remains a separate solid object.

혼동 경계: 백색 가루의 화학 성분·도핑·연기와 동일시 금지

가시성: 손 표면·입자·기구를 분리

관계: residue → on → palms; particles → near → hands; athlete → near → apparatus

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## L10 스포츠 브라의 기능적 외형

- 종목/단계: training / garment silhouette
- 검증 범위: `authored_surface_boundary_sourced`
- 탐색 단서: 스포츠 브라, Sports bra, 밀착 실루엣

밀착 스포츠 상의가 가슴 아래 경계 있는 하단 밴드를 갖는다; 어깨 스트랩이 같은 상의로 연속된다; 의복이 드러난 팔·복부와 구분된다.

a fitted sports top has a bounded lower band below the chest; shoulder straps connect continuously to that same top; the garment remains distinct from the exposed arms and abdomen.

혼동 경계: 유방 세부·성적 의도·성인 신분은 의복으로 추정하지 않음

가시성: 스트랩·밴드·옷-피부 경계

관계: athlete → wears → sports_top; straps → part_of → sports_top; band → part_of → sports_top

출처: [S25 IOC Portrayal Guidelines](https://www.olympics.com/ioc/gender-equality/portrayal-guidelines)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## X01 패닝의 상대 선명도

- 종목/단계: photography / single exposure appearance
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 모션 블러·패닝, Panning, Motion blur

움직이는 선수의 몸통 부근이 상대적으로 선명하다; 배경의 표식이 일관된 수평 흐름으로 늘어난다; 선수는 중복 팔다리 대신 하나의 몸을 유지한다.

the moving athlete remains comparatively sharp around the torso; background marks extend into a coherent horizontal flow; the athlete retains one body rather than multiple duplicated limbs.

혼동 경계: 슬로모션 시간 재생·무조건 피사체 전체 선명·복제 잔상과 구별

가시성: 주피사체와 배경 흐림의 차이

관계: background_blur → behind → athlete; athlete → separate_from → background; limbs → part_of → athlete

출처: [S32 Canon Panning Effect](https://www.usa.canon.com/learning/training-articles/training-articles-list/how-do-i-get-a-panning-effect)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## X02 그림 매체의 오라 비유

- 종목/단계: illustration / explicit graphic metaphor
- 검증 범위: `authored_medium_gated_proposal`
- 탐색 단서: 오라·동물 비유·잔상, 초인·가상 스포츠물

그려진 선수가 하나의 물리적 인물로 남는다; 별도 반투명 동물 형태 윤곽이 그 인물을 둘러싼다; 그래픽 윤곽 너머로 코트 경계가 보인다.

a drawn athlete remains a single physical figure; a separate translucent animal-shaped contour surrounds that figure; the court boundary stays visible through the graphic contour.

혼동 경계: 실제 동물·초능력 사실·사진 필수 효과로 전환 금지

가시성: 명시된 일러스트 매체와 그래픽 층

관계: graphic_contour → around → athlete; graphic_contour → separate_from → body; court → behind → graphic_contour

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## X03 벤치클리어링의 대치 배치

- 종목/단계: baseball / players entering field
- 검증 범위: `authored_claim_limited_proposal`
- 탐색 단서: 벤치클리어링, Benches clearing

유니폼 선수 여럿이 더그아웃 입구 바깥에 선다; 두 무리가 사이 공간을 두고 마주한다; 일부 인물 사이에서 편 손이 몸을 떼어 놓고 주먹 타격은 필수가 아니다.

several uniformed players stand outside the dugout entrance; two groups face each other with visible space between; open hands separate some adjacent bodies without a required punch.

혼동 경계: 난투·보복 동기·첫 공격자·실제 싸움 자동 추가 금지

가시성: 두 집단·입구·손과 접촉 상태

관계: group_a → faces → group_b; players → outside → dugout; separating_hands → between → players

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## X04 심판의 경기 중지 개입

- 종목/단계: combat_sport / official intervention snapshot
- 검증 범위: `authored_snapshot_result_unobservable`
- 탐색 단서: 닥터 스톱, TKO, 다운, KO, 코너 스톱·타월 투척

공식 진행자가 두 선수 사이에서 팔을 벌린다; 한 선수가 로프 또는 케이지 경계 가까이에 따로 남는다; 다른 선수는 진행자의 편 팔 너머에 멈춰 선다.

an official stands between two competitors with arms spread; one competitor remains separate near the ropes or cage boundary; the other competitor pauses beyond the official's open arm.

혼동 경계: KO·TKO·닥터스톱·다운·실신은 서로 다름; 종목·결과 기록 없는 최종 판정 금지

가시성: 개입자·두 선수·경기장 경계

관계: official → beside → competitor_a; official → beside → competitor_b; official → owns → arms; competitors → inside → venue

출처: [S22 NBA Rule 12 Fouls and Penalties](https://official.nba.com/rule-no-12-fouls-and-penalties/), [S23 ABC Regulatory Guidelines](https://www.abcboxing.com/abc-regulatory-guidelines/)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## X05 탭의 접촉 형태

- 종목/단계: grappling / one contact snapshot
- 검증 범위: `authored_snapshot_result_unobservable`
- 탐색 단서: 서브미션·탭아웃, Submission, Tap out

한 선수의 편 손이 상대 위팔에 닿는다; 닿는 손목이 몸을 제어당하는 선수에게 이어진다; 제어하는 두 팔은 상대 선수 소유로 남는다.

one athlete's open hand touches the opponent's upper arm; the touching wrist traces to the athlete whose body is being controlled; the opponent's controlling arms remain assigned to that opponent.

혼동 경계: 한 번의 손 접촉만으로 반복 탭·항복·동의·서브미션 결과 판정 불가

가시성: 손 소유·대상 위팔·두 몸 경계

관계: athlete_a → owns → touching_hand; touching_hand → contacts → arm_b; athlete_b → owns → controlling_arms

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## X06 비노골적 손상 흔적

- 종목/단계: combat_sport / visible surface mark
- 검증 범위: `authored_snapshot_claim_limited`
- 탐색 단서: 컷·출혈·타박 흔적, 부상·재활 서사

작은 붉은 표면 흔적이 한쪽 뺨에 놓인다; 흔적은 내부 조직 노출 없이 피부 표면을 따른다; 가까운 코너에 별도의 깨끗한 수건이 놓인다.

a small red superficial mark stays on one cheek; the mark follows the skin surface without exposed internal tissue; a separate clean towel rests in the nearby corner.

혼동 경계: 진단·상해 원인·심각도·커리어 종료·가해자·KO 미확정; 연구 범위에 다른 수위도 기록하되 별도 실현

가시성: 흔적 위치와 피부 경계

관계: mark → on → cheek; cheek → part_of → athlete; towel → in → corner

출처: [S26 IOC Safeguarding and Interpersonal Violence](https://www.olympics.com/ioc/news/ioc-publishes-new-consensus-statement-on-safeguarding-and-interpersonal-violence-in-sport)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## X07 검사 장면의 표면 증거

- 종목/단계: sports_integrity / sample station
- 검증 범위: `authored_context_evidence_only`
- 탐색 단서: 도핑, TUE, 치료목적사용면책

봉인된 검체 용기가 선수와 떨어진 탁자 위에 놓인다; 진행자가 그 용기 옆에서 서식을 든다; 선수의 두 손이 따로 보이는 위치에 놓인다.

sealed sample containers sit on a table apart from the athlete; an official holds a form beside those containers; the athlete's hands rest separately in view.

혼동 경계: 검사=위반·약병=금지물질·TUE=편법으로 추정 금지; 실제 검체 절차 재현은 별도 확인

가시성: 용기·폼·사람의 소유 관계

관계: containers → on → table; official → holds → form; athlete → near → table

출처: [S24 WADA World Anti Doping Code](https://www.wada-ama.org/sites/default/files/resources/files/2021_code.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## X08 성인 선수의 친밀한 상호 시선

- 종목/단계: adult_sports_romance / mutual attention snapshot
- 검증 범위: `authored_relational_proposal`
- 탐색 단서: 스포츠 로맨스, 라이벌 로맨스, 팀메이트 로맨스, BL·GL 스포츠 로맨스

명시된 성인 가상 선수 두 명이 가까운 대화 거리에서 마주한다; 각자의 보이는 시선이 상대 얼굴을 향한다; 스포츠 장비 옆에서 각자의 손과 몸이 구별된다.

two explicitly adult fictional athletes face each other at close conversational distance; each person's visible gaze is directed toward the other's face; their separate hands and bodies remain readable beside the sports equipment.

혼동 경계: 시선만으로 연애·성적 지향·동의·라이벌 경력 확정 금지; 성인성은 사용자 설정 근거

가시성: 시선의 양방향·두 사람 경계

관계: adult_a → looks_toward → face_b; adult_b → looks_toward → face_a; equipment → beside → adults

출처: [S25 IOC Portrayal Guidelines](https://www.olympics.com/ioc/gender-equality/portrayal-guidelines), [S26 IOC Safeguarding and Interpersonal Violence](https://www.olympics.com/ioc/news/ioc-publishes-new-consensus-statement-on-safeguarding-and-interpersonal-violence-in-sport)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## X09 프로레슬링 마이크 프로모

- 종목/단계: pro_wrestling / microphone address
- 검증 범위: `primary_specialist_pending`
- 탐색 단서: 프로모, Promo, 프로레슬링물

퍼포머가 링 안에서 입 가까이에 마이크를 든다; 다른 손은 별도 상대를 가리킨다; 상대는 보이는 간격 너머로 말하는 인물을 향한다.

a performer holds a microphone near the mouth inside the ring; the free hand points toward a separate opponent; the opponent faces the speaker across a visible gap.

혼동 경계: 음성·대사·케이페이브·힐·슈트·실제 적대는 표정으로 확정 금지

가시성: 마이크·발언자·가리킨 상대

관계: performer → holds → microphone; free_hand → points_to → opponent; opponent → faces → performer

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## X10 관중석 티포의 구조

- 종목/단계: stadium / coordinated visual display
- 검증 범위: `authored_structure_primary_pending`
- 탐색 단서: 티포, Tifo, 응원가·챈트

분리된 여러 카드가 관중석에서 하나의 큰 색 패턴을 이룬다; 카드들이 구별되는 관중 위에 들려 있다; 표시는 경기장 바깥 관중석 안에 머문다.

many separate cards form one large colour pattern across the stands; the cards remain held above distinct spectators; the display stays inside the seating area beyond the pitch.

혼동 경계: 응원가 가사·집단 신념·훌리거니즘·소리를 모양만으로 확정 금지

가시성: 카드 반복·관중·관중석 경계

관계: spectators → hold → cards; cards → form → pattern; stands → outside → pitch

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## W13 레오타드 다리 입구

- 종목/단계: gymnastics / garment structure
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 레오타드, Leotard

밀착 몸통 의복 하나가 두 다리 입구에서 끝난다; 그 입구 아래로 맨 허벅지가 이어진다; 어깨끈이 같은 몸통 의복에 속한다.

one fitted torso garment ends at two high leg openings; the bare thighs continue below those openings; the shoulder straps remain part of the same torso garment.

혼동 경계: 유니타드·상하 분리 수영복과 구분; 경기복만으로 선정성 미판정

가시성: 다리 입구와 몸통의 연속성

관계: wearer → wears → leotard; leg_openings → part_of → leotard; thighs → below → leg_openings

출처: [S35 Gymnastics NZ Competition Attire](https://www.gymnasticsnz.com/attire/), [S38 World Gymnastics Clothing and Advertising](https://www.worldgymnastics.sport/publicdir/rules/files/en_Advertising%20Rules%20Competition%20Clothing%20-%20valid%20from%20May%202024.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## W14 니 스킨의 몸통 연결

- 종목/단계: swimming / garment structure
- 검증 범위: `authored_structure_primary_pending`
- 탐색 단서: 니 스킨, Kneeskin, 원피스 수영복·니 스킨

수영복 몸통이 밀착된 두 허벅지 부분으로 연속된다; 선택한 형태의 밑단이 무릎 위에서 끝난다; 별도 허리밴드가 몸통과 하부 수영복을 나누지 않는다.

a continuous swimsuit torso joins both fitted thigh sections; the leg hems end above the knees in this chosen version; no separate waistband divides the torso from the lower suit.

혼동 경계: 허리에서 시작하는 재머·일반 원피스와 구분; 경기 허용 범위 수치 미검증

가시성: 몸통-하부 연결과 다리 끝

관계: swimmer → wears → kneeskin; torso_panel → continuous_with → thigh_panels; leg_hems → above → knees

출처: [S08 World Aquatics Competition Regulations](https://www.worldaquatics.com/rules/competition-regulations), [S37 USA Swimming Speedo Tech Suit Database](https://www.usaswimming.org/docs/default-source/rules-regulations/tech-suit-restrictions/speedo-120220.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## M01 포수 보호구와 낮은 자세

- 종목/단계: baseball / crouched behind plate
- 검증 범위: `geometry_primary_pending`
- 탐색 단서: 포수 보호구, 포수 자세, Catcher

포수가 포수석에서 별도의 가슴·정강이 보호구를 입고 낮게 앉는다; 마스크가 별도 케이지 경계로 얼굴을 둘러싼다; 포수에게 이어진 한 손의 미트가 몸 앞에서 열린다.

the catcher crouches behind the plate wearing separate chest and shin guards; a mask surrounds the face with a distinct cage boundary; one mitt opens in front of a hand connected to that catcher.

혼동 경계: 복싱 글러브·타자의 헬멧과 구분; 투수와 포수 소유를 섞지 않음

가시성: 마스크·흉부·다리·미트 소유

관계: catcher → wears → mask; catcher → wears → chest_guard; catcher → wears → shin_guards; catcher → holds → mitt

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## M02 핸드랩과 복싱 글러브의 층

- 종목/단계: boxing / pre-bout equipment
- 검증 범위: `authored_layer_proposal`
- 탐색 단서: 글러브·핸드랩, Gloves, Hand wraps

천 핸드랩이 드러난 한 손의 주먹과 손목을 따라 감긴다; 별도 복싱 글러브가 감긴 손 옆에 놓인다; 글러브는 패딩 주먹 덩어리와 자체 손목 입구를 갖는다.

fabric wraps follow the knuckles and wrist of one exposed hand; a separate boxing glove rests beside that wrapped hand; the glove has one padded fist volume and its own wrist opening.

혼동 경계: 글러브를 완전히 낀 손의 내부 핸드랩까지 보인다고 판정 금지

가시성: 감긴 손·분리 장갑·손목 입구

관계: wraps → around → hand; glove → beside → hand; wrist_opening → part_of → glove

출처: [S21 IBA Coach Manual](https://www.iba.sport/documents/iba-coach-manual/)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## M03 수모와 수경의 부착

- 종목/단계: swimming / head equipment
- 검증 범위: `authored_structure_primary_pending`
- 탐색 단서: 수모·수경, Swim cap, Goggles

밀착 수모가 수영 선수 머리를 덮는다; 수경 한 쌍의 두 아이컵이 눈 위에 놓인다; 수경 스트랩이 수모를 쓴 머리 둘레로 이어진다.

a fitted cap covers the swimmer's head; two eye cups sit over the eyes as parts of one pair of goggles; the goggles strap continues around the capped head.

혼동 경계: 일반 안경·수경을 이마에 올린 상태와 구분; 수모 재질·방수 성능 미판정

가시성: 아이컵·눈·스트랩·수모 경계

관계: cap → covers → head; goggles → over → eyes; strap → part_of → goggles; strap → around → head

출처: [S08 World Aquatics Competition Regulations](https://www.worldaquatics.com/rules/competition-regulations)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## M04 펜싱 플라스트롱 내부층

- 종목/단계: fencing / exposed layer demonstration
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 펜싱 마스크·플라스트롱, Plastron

열린 겉재킷이 별도 내부 보호층을 드러낸다; 선택한 시점에서 내부층이 검 쪽 상체를 덮는다; 겉재킷 가장자리가 내부층 바깥에 보인다.

an opened outer jacket reveals a separate protective under-layer; the under-layer covers the weapon-side upper torso in the selected view; the outer jacket edges remain visibly outside that layer.

혼동 경계: 닫힌 경기 재킷 안 플라스트롱은 unobservable; 라메 겉층과 구별

가시성: 선택한 구조 시연 장면의 여밈과 층

관계: plastron → under → jacket; plastron → covers → weapon_side_torso; jacket → open_at → front

출처: [S10 FIE Material Rules](https://static.fie.org/uploads/40/204156-book%20material%20August%202026%20ang.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## M05 콕핏의 선수·벨트·휠 접점

- 종목/단계: motorsport / seated controls
- 검증 범위: `authored_snapshot_claim_limited`
- 탐색 단서: 콕핏 착좌 자세, Seated cockpit posture

운전자가 좌석 안에 앉아 골반을 지지받는다; 스트랩이 두 어깨 위에서 보이는 중앙 버클로 향한다; 글러브를 낀 두 손이 운전대 하나의 양쪽을 잡는다.

the driver sits within the seat with the pelvis supported; straps run over both shoulders toward a visible central buckle; two gloved hands grip different sides of one steering wheel.

혼동 경계: 레이스 수트만으로 콕핏 고정 확인 불가; 벨트의 모든 점·인증·조작 의도 미판정

가시성: 손-휠·어깨 스트랩·버클·좌석

관계: driver → supported_by → seat; straps → over → shoulders; straps → connect_to → buckle; hands → grip → steering_wheel

출처: [S31 FIA Protective Clothing Safety Guidelines](https://www.fia.com/sites/default/files/guidelines_safety_clothing_to_publish_bd.pdf)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## M06 주장 완장의 착용자

- 종목/단계: football / arm marker
- 검증 범위: `source_supported_boundary`
- 탐색 단서: 주장 완장, Captain’s armband, 주장

별도 띠가 한 선수 위팔을 둘러싼다; 저지 소매 끝이 그 띠와 구분된다; 띠는 가까운 동료 대신 해당 팔에 속한다.

a separate band encircles one player's upper arm; the jersey sleeve edge stays distinct from the band; the band belongs to that same arm rather than a nearby teammate.

혼동 경계: 에이스 기량·전 종목 주장·리더십 성격 자동 결합 금지

가시성: 띠의 둘레·소매·팔 소유

관계: captain → owns → upper_arm; armband → around → upper_arm; sleeve → separate_from → armband

출처: [S03 IFAB Law 4 Players Equipment](https://theifab.com/laws/latest/the-players-equipment/)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## M07 수건의 목·어깨 걸침

- 종목/단계: multi_sport / rest equipment
- 검증 범위: `authored_relational_proposal`
- 탐색 단서: 수건을 목에 걸치기, Towel around neck

수건이 선수 목 뒤를 가로지른다; 양 끝이 가슴 앞에서 따로 내려온다; 수건 원단이 저지 칼라와 구별된다.

a towel crosses behind the athlete's neck; two ends hang separately down the chest; the fabric stays distinct from the jersey collar.

혼동 경계: 스카프·목 자체·피로 진단·경기 결과와 동일시 금지

가시성: 목 뒤 연결과 앞의 두 끝

관계: towel → around → neck; towel_ends → in_front_of → chest; towel → separate_from → jersey

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.

## M08 목표를 향한 시점 숏

- 종목/단계: photography / athlete viewpoint
- 검증 범위: `authored_camera_proposal`
- 탐색 단서: 시점 숏, POV shot

전경 손이 경기 공간 쪽으로 운동 도구를 든다; 도구가 보이는 방향을 따라 앞쪽에 목표가 놓인다; 카메라가 선언된 선수의 시점 위치를 차지한다.

a foreground hand holds the sport implement toward the playing area; the target lies ahead along the implement's visible direction; the camera occupies the declared athlete viewpoint.

혼동 경계: 카메라 시점은 실제 인물 눈으로 촬영했다는 사실 아님; 필요한 손 수·몸 소유 유지

가시성: 전경 도구·목표·방향

관계: hand → holds → implement; implement → toward → target; target → ahead_of → camera

출처: [S00 사용자 지정 스포츠물 용어 정리 대화](https://chatgpt.com/c/6adc0773-1cb0-83ee-b4b5-18e4481cde33)

선택한 세 구성 요소가 함께 보이지 않으면 완전 카드로 통과하지 않는다. 출처는 해당 정의·경계를 지원하며 작성한 장면 전체를 입증하지 않는다.
