# 악기 시각 의미·후보팩 강화 및 5개 독립 렌더 검증 보고서

## 결론

- 새 악기 시각 의미 프로필 10개, 후보 67개, 승인 연구 근거 10개를 반영했다.
- 5개 독립 에이전트가 서로 다른 랜덤 복합 콘셉트를 코어 우선으로 동결한 뒤, 참조 이미지를 실제 입력으로 첨부해 각각 정확히 1회 생성했다.
- composed prompt 감사 5/5, render request 감사 5/5, 생성 성공 5/5였다.
- 엄격한 픽셀 게이트는 총 25개 중 23개가 통과했다. 팔 단위 완전 통과는 3/5다.
- 완전 통과: 더블베이스 5/5, 비브라폰 5/5, 테레민 5/5.
- 비승격: 거문고 4/5(고정 괘와 별도 이동식 안족의 공존 불명확), 색소폰 4/5(리가처는 보이나 별도 케인 리드 식별 불명확).
- 참조 이미지는 보이는 성인 얼굴 외형, 헤어스타일, 메이크업/피부 표면에만 사용했다. 동일인·생체 식별·민족성·건강·매력·성격 판단은 하지 않았다.
- 사용자 미감·닮음 판단은 모든 팔에서 별도 `pending`이다.

## 데이터 반영

- `photo_prompt_visual_obligations.json`: 10개 고혼동 악기 프로필 추가. 현재 120개 프로필.
- `photo_prompt_tags.json`: 13개 슬롯에 67개 후보 추가, 버전 `1.33`. 현재 111개 슬롯, 5,283개 후보.
- `research_evidence.jsonl`: 승인 근거 10개 추가.
- `photo_prompt_visual_profile_index.json`: 120개 프로필, exact term 726개, `gemini-embedding-2`, 768차원으로 재생성.
- `photo_prompt_semantic_index.json`: 7,187개 엔트리, 16개 shard로 재생성.
- `tests/test_photo_instrument_semantics.py`: 후보 존재성, 프로필 결속, 5개 구성 그룹/게이트, exact activation, broad/ambiguous negative, 근거 연결, 레지스트리 검증을 포함한 7개 테스트 추가.

추가 프로필은 다음 혼동쌍을 fail-closed로 다룬다.

1. 가야금 ↔ 거문고
2. 색소폰 ↔ 피스톤 트럼펫
3. 첼로 ↔ 더블베이스
4. 비브라폰 ↔ 실로폰
5. 테레민 ↔ MIDI 컨트롤러

## 연구 근거

- [MIMO Consortium의 Hornbostel–Sachs 분류](https://mimo-international.com/documents/Hornbostel%20Sachs.pdf)는 상위 악기 분류 경계에만 사용했다.
- 국립국악원 [가야금](https://www.gugak.go.kr/ency/topic/view/364)·[거문고](https://www.gugak.go.kr/ency/topic/view/88) 항목은 줄, 안족/괘, 연주법의 관찰 가능한 차이에 사용했다.
- Yamaha [색소폰](https://www.yamaha.com/en/musical_instrument_guide/saxophone/mechanism/mechanism002.html)·[트럼펫](https://www.yamaha.com/en/musical_instrument_guide/trumpet/mechanism/mechanism002.html) 구조 자료는 리드/리가처/키워크와 컵 마우스피스/3피스톤 경계를 만드는 데 사용했다.
- Philharmonia [첼로](https://philharmonia.co.uk/resources/instruments/cello/)·[더블베이스](https://philharmonia.co.uk/resources/instruments/double-bass/)·[타악기](https://philharmonia.co.uk/resources/instruments/percussion/) 자료는 사람 대비 스케일, 바닥 지지, 금속/목재 바와 공명관 경계에 사용했다.
- [Moog Etherwave 매뉴얼](https://api.moogmusic.com/sites/default/files/2018-06/Etherwave_Theremin_Manual.pdf)은 직선 피치 안테나, 루프 볼륨 안테나, 비접촉 양손 제어를 정의하는 데 사용했다.
- [MIDI Association 자료](https://midi.org/mixing-with-virtual-instruments-the-basics)는 컨트롤러와 외부 음원의 기능 경계를 정의하는 데 사용했다.

근거는 별칭 확대가 아니라 관찰 가능한 구성 요소, 혼동 대체물, 렌더 게이트와 후보 ID에 연결했다.

## 독립성·생성 프로토콜

- 각 팔은 스킬, 공통 요청 봉투, 참조 범위, 배정 프로필만 읽고 32-bit 랜덤 seed와 `authorial_core.json`을 먼저 동결했다.
- 코어 동결 전에는 후보팩, 시각 프로필 레지스트리, 테스트, 과거 산출물, 다른 팔 산출물을 읽지 않았다.
- 각 팔은 최소 두 개의 저자적 차원을 open으로 남겼다.
- 후보팩은 모두 v6이며 서로 다른 pack ID를 갖는다.
- 각 팔은 참조 SHA-256 `e3e010b75a48da02f914d7e8202690b3353450a78832daaefea0bbbc234aa5b3`을 결속했다.
- 각 팔은 built-in `image_gen`을 정확히 1회 호출했고 재시도하지 않았다.
- 모든 manifest의 `cross_arm_inputs_used`는 `false`다.

## 결과 요약

| 팔 | Seed | Pack ID | 랜덤 복합 콘셉트 | 감사 | 픽셀 | 판정 |
|---|---:|---|---|---|---:|---|
| 거문고 | 322530066 | `619617f9572536a4` | 해무 낀 등대실, 바람에 휘는 오일램프, 인디고+회전 백색광, 낮은 55mm | 2/2 PASS | 4/5 | FAIL |
| 색소폰 | 940818821 | `7d68d3781f23c3d2` | 블루아워 식물 연구 온실, 자동 미스트, 청색+호박색, 50mm 세로 | 2/2 PASS | 4/5 | FAIL |
| 더블베이스 | 1711376315 | `d048a78f1c0121cd` | 해무 유입 해안 펌프 홀, 청록+텅스텐, 저시점 35mm 전신 | 2/2 PASS | 5/5 | PASS |
| 비브라폰 | 2834404087 | `d4dfb14d53653495` | 야간 플라네타륨 보정, 첫 모터 다운비트, 별자리 투사+호박 스폿 | 2/2 PASS | 5/5 | PASS |
| 테레민 | 926806901 | `5448188d9b2753cc` | 폭우·번개 속 야간 온실 라이브 녹음, sodium-orange+cyan | 2/2 PASS | 5/5 | PASS |

## 팔 1 — 거문고

![거문고 렌더](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-instrument-semantics-five-agent-v1/arm-01-geomungo/result.png)

정확한 positive prompt:

```text
Create a photorealistic environmental portrait inside a coastal lighthouse keeper room during dense sea fog. An original adult performer sits cross-legged behind a full-scale Korean geomungo. It is a long horizontal wooden zither with a small set of strings, specifically six thick strings; prominent fixed gwae frets coexist with movable bridges on the playing surface. The fretted zither rests horizontally before the seated performer at a plausible full instrument scale, spanning the lower frame with both endpoints visible. Her left hand presses a string firmly over a fixed fret; the right hand uses a short suldae stick on the strings, with its tip in visible contact, the suldae tip visibly contacting a string in a precise accented stroke. Bare-finger plucking across many individual bridges does not substitute for the visible fixed-fret and suldae system. Freeze the instant when a draft bends the oil-lamp flame. Deep indigo ambient light fills the room while a hard white sweep from the lighthouse optic grazes the fret row; warm lamp bounce joins performer, hands, and wood in one believable exposure. Use a low seated 55 mm three-quarter viewpoint: the zither forms a strong horizontal band, the face occupies the upper third, and both hand contacts stay unobstructed and sharp. Image 1 is only a scoped visible-appearance reference for this original adult performer: use its visible adult facial appearance, long dark wavy center-parted hair, softly defined eye makeup, muted rose lips, and natural luminous skin-surface finish.
```

Negative: `body distortion, plastic-looking skin, unrealistic hands, 3D render look, excessive HDR, over-processed retouching, distorted fingers, fake-looking background`

통과: 수평 현악기, 술대 접촉, 좌식 지지, 가야금 비대체. 실패: 고정 괘형 구조는 보이나 별도 이동식 안족의 공존을 식별할 수 없음.

핵심 파일: [agent_result.json](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-instrument-semantics-five-agent-v1/arm-01-geomungo/agent_result.json), [pixel_review.json](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-instrument-semantics-five-agent-v1/arm-01-geomungo/pixel_review.json), [run_manifest.json](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-instrument-semantics-five-agent-v1/arm-01-geomungo/run_manifest.json)

## 팔 2 — 알토 색소폰

![색소폰 렌더](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-instrument-semantics-five-agent-v1/arm-02-saxophone/result.png)

정확한 positive prompt:

```text
Create a complex independent saxophone-semantics test photograph in a botanical research glasshouse at blue hour. An original adult saxophonist plays a sustained phrase while the automated misting system activates in blue skylight and amber grow light. Show an alto or tenor saxophone. The curved conical metal body ends in a flared bell beside her knee at realistic alto-saxophone scale. A single reed and ligature sit on the mouthpiece, with their tan cane and metal edges clearly visible. Dense keywork runs along the metal body, with linked rods, pads, key cups, and pearl touches remaining legible. The lips seal the reed mouthpiece while both hands operate keys, left on the upper stack and right on the lower stack. A cup mouthpiece and three piston valves do not substitute for the visible reed, ligature, curved conical body, and dense side keywork. Use Image 1 only as a scoped visible-appearance reference for this original adult performer: long dark center-parted wavy hair, softly defined eyes, muted rose lips, and a luminous natural skin-surface finish. A natural 50 mm f/4 vertical mid-to-knee frame contains her face, reed contact, both hands, keyed body, and bell; condensation and controlled reflections preserve humid depth.
```

Negative: `excessive HDR, impossible perspective, illustration look, low resolution, cartoon style, warped product geometry, broken window geometry, 3D render look, warped walls`

통과: 곡선 원추형 몸체, 조밀한 키워크, 입술+양손 연주 접촉, 트럼펫 비대체. 실패: 리가처는 보이나 tan cane reed를 독립적으로 식별할 수 없음.

핵심 파일: [agent_result.json](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-instrument-semantics-five-agent-v1/arm-02-saxophone/agent_result.json), [pixel_review.json](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-instrument-semantics-five-agent-v1/arm-02-saxophone/pixel_review.json), [run_manifest.json](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-instrument-semantics-five-agent-v1/arm-02-saxophone/run_manifest.json)

## 팔 3 — 더블베이스

![더블베이스 렌더](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-instrument-semantics-five-agent-v1/arm-03-double-bass/result.png)

정확한 positive prompt:

```text
Create one photorealistic vertical environmental photograph. An original adult double-bass performer stands in a decommissioned coastal pump hall at blue hour, on wet concrete as a partly open rolling service door admits a narrow ribbon of sea mist. A full-sized upright double bass rises nearly to the standing performer's head: a human-scale waisted wooden body stands upright nearly as tall as the adult performer, and the long neck rises near or above the player's head, with pegbox and scroll fully visible. A load-bearing endpin anchors the large body to the floor at a clearly visible contact point. The standing or high-stool performer bows or plucks the strings; here the standing adult fingers the neck while the bow contacts the strings, and the right hand draws a bow in clear contact across the strings. The relationship is explicit because human-scale upright-bass geometry beside a standing adult makes clear that a medium cello held between conventionally seated knees does not substitute. Cyan window light crosses one warm tungsten maintenance lamp, revealing wet reflections, varnished wood, matte charcoal wool clothing, and sparse rust-red pipe accents. Use a low eye-level 35mm full-body composition that keeps the performer, scroll, broad lower bouts, hands, bow contact, endpin, and floor junction simultaneously legible, with the mist held as a narrow backlit layer behind the scroll. Image 1 contributes only observable visible adult facial appearance, long dark wavy hairstyle, understated eye makeup, and softly luminous natural skin-surface finish. Realize those surface cues in a newly designed original adult performer whose identity, origin, health, attractiveness, personality, and protected traits remain unspecified.
```

Negative: `excessive HDR, plastic-looking skin, 3D render look, over-processed retouching, fake-looking background, distorted fingers, low resolution, body distortion, illustration look`

5개 게이트 모두 통과: 사람 대비 스케일, 긴 넥/스크롤, 바닥 엔드핀, 활+지판 접촉, 첼로 비대체.

핵심 파일: [agent_result.json](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-instrument-semantics-five-agent-v1/arm-03-double-bass/agent_result.json), [pixel_review.json](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-instrument-semantics-five-agent-v1/arm-03-double-bass/pixel_review.json), [run_manifest.json](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-instrument-semantics-five-agent-v1/arm-03-double-bass/run_manifest.json)

## 팔 4 — 비브라폰

![비브라폰 렌더](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-instrument-semantics-five-agent-v1/arm-04-vibraphone/result.png)

정확한 positive prompt:

```text
Use case: photorealistic-natural. A photorealistic editorial photograph on an empty planetarium's circular stage during overnight projector calibration. Depict one newly invented adult performer at an unmistakable motor-equipped pedal vibraphone built around two rows of silvery metal bars. On the instrument, two rows of graduated metal bars form the keyboard, their silvery alloy surfaces catching clean highlights. Beneath them, vertical resonator tubes show fan or rotor assemblies beneath the bars, with circular disks visibly aligned inside multiple open tube mouths. At floor level, a damper pedal connects to the wheeled frame and sits visibly under the performer's pressing right foot. Freeze the first motor-on downbeat: her two yarn-wrapped mallets make real playing contact with separate metal bars while her right foot visibly depresses the full-width damper pedal; mallets contact the metal bars while one foot controls the pedal in a single physically playable downbeat. The positive construction stays unmistakable: wooden bars without motor fans and a pedal do not substitute; the pictured instrument reads through positive metal-bar, rotor, and damping-hardware evidence. Use Image 1 only for the original adult performer's visible facial appearance, long dark wavy hairstyle, restrained warm eye makeup, natural rose lips, and luminous skin-surface finish. Image 1 is a scoped visible-appearance reference for this original performer, with identity and personal-trait claims outside its role. A narrow amber follow spot intersects cool moving constellation projections and dim red aisle lights, while the projections stay off the reflective bar tops. A low 35 mm three-quarter view from the audience aisle keeps her face in the upper third and runs the bars diagonally through the frame; keep one unobstructed depth line from face to mallet contact, rotating fan disks, resonator ranks, connected pedal, and pressing foot. Preserve realistic adult anatomy, instrument scale, optical texture, and readable physical contact.
```

Negative: `body distortion, illustration look, plastic-looking skin, over-processed retouching, distorted fingers, 3D render look, broken window geometry, low resolution, excessive HDR`

5개 게이트 모두 통과: 금속 바, 공명관 팬/로터, 연결된 댐퍼 페달, 말렛+발 동시 접촉, 실로폰 비대체.

핵심 파일: [agent_result.json](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-instrument-semantics-five-agent-v1/arm-04-vibraphone/agent_result.json), [pixel_review.json](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-instrument-semantics-five-agent-v1/arm-04-vibraphone/pixel_review.json), [run_manifest.json](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-instrument-semantics-five-agent-v1/arm-04-vibraphone/run_manifest.json)

## 팔 5 — 테레민

![테레민 렌더](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-instrument-semantics-five-agent-v1/arm-05-theremin/result.png)

정확한 runtime prompt:

```text
Create a photorealistic editorial photo in a rain-streaked glass botanical conservatory at night. An original adult performer stands at a powered wooden theremin cabinet during a live recording as lightning silhouettes tropical leaves. A powered theremin cabinet connects to an audible output system through one visible output cable and a lit amplifier. One straight pitch antenna and one loop-shaped volume antenna stand unobstructed at opposite sides of the cabinet. The two hands occupy separate pitch and volume fields, the right hand near the straight rod and the left above the loop. Both hands remain visibly suspended without touching the antennas or cabinet, with clean air gaps around every fingertip. Keys, pads, a single sensor, or touching gestures do not substitute; the performer controls only the two antenna fields. Use an eye-level 35 mm head-to-mid-thigh environmental portrait, cabinet low-center, keeping both antenna fields and the performer's face clear. Sodium-orange rain light contrasts with cyan instrument glow and a neutral bounced key. Image 1 guides only visible adult facial appearance, long dark wavy hair, warm eye-makeup placement, natural lip color, and luminous skin-surface finish for this original adult character.

Avoid: illustration look, low resolution, unrealistic hands, fake-looking background, 3D render look, plastic-looking skin, cartoon style, excessive HDR, over-processed retouching
```

5개 게이트 모두 통과: 전원/출력 캐비닛, 직선+루프 안테나, 분리된 양손 필드, 명확한 비접촉, MIDI 컨트롤러 비대체.

핵심 파일: [agent_result.json](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-instrument-semantics-five-agent-v1/arm-05-theremin/agent_result.json), [pixel_review.json](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-instrument-semantics-five-agent-v1/arm-05-theremin/pixel_review.json), [run_manifest.json](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-instrument-semantics-five-agent-v1/arm-05-theremin/run_manifest.json)

## 루트 재검증

- 5개 result 이미지와 참조 이미지 SHA-256을 재계산해 manifest와 일치함을 확인했다.
- 5개 manifest 모두 `candidate_pack_version=v6`, `image_call_count=1`, `cross_arm_inputs_used=false`, 동일한 reference/skill SHA를 기록했다.
- composed prompt와 render request를 루트에서 재감사해 5/5 PASS, failure 0, reference count 1, negative byte match를 확인했다.
- 원본 5개 이미지를 루트에서 직접 재검토했으며 에이전트의 23/25 게이트 집계와 일치했다.
- 프롬프트 감사 PASS는 픽셀 PASS를 대신하지 않았고, partial은 FAIL로 처리했다.

## 다음 개선 표적

- 거문고: `고정 괘`와 `별도 이동식 안족`을 같은 각도에서 서로 다른 형태·위치로 분리해 읽을 수 있도록, 상판 사선 시점과 두 시스템의 공간적 분리를 더 강하게 요구해야 한다.
- 색소폰: 연주 접촉을 유지하면서도 마우스피스 아래쪽의 케인 리드가 리가처와 분리되어 보이도록, 하부 3/4 시점·리드 가장자리·색 대비·최소 픽셀 크기를 추가해야 한다.
- 이 두 실패는 데이터/감사 실패가 아니라 생성 픽셀의 미세 구조 가시성 실패다. 따라서 현재 결과는 비승격 상태로 보존하고, 향후 재시도는 실패 차원만 수정한 별도 lineage로 실행해야 한다.
