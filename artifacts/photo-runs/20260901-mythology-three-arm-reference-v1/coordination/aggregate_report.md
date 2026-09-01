# 신화 시각 의미 3-arm 독립 렌더 테스트

## 결론

세 candidate pack과 세 runtime request는 모두 감사에 통과했고, built-in image generation은 arm별 정확히 1회씩 성공해 세 이미지가 저장되었다. 그러나 사전 고정한 15개 프로필 하드 게이트 중 11개만 픽셀에서 통과했으며, `partial_is_fail` 규칙에 따라 기술적으로 자격을 얻은 arm은 0/3이다. 세 결과 모두 `revise`이며 요청자의 미적 선호 판정은 별도로 pending이다.

데이터 회귀층은 `.venv/bin/python -m unittest tests.test_photo_mythology_visual_semantics`에서 8/8 통과했다. 이 결과는 소스 데이터와 라우팅이 정상임을 증명하지만 이미지 픽셀 성공을 증명하지 않는다.

## 독립성 및 재현성

- 랜덤 시드: `351826943`
- 추출 프로필: `chaoskampf_cosmogonic_ordering`, `katabasis_living_underworld_descent`, `moirai_fate_thread_life_allocation`
- 참조 이미지 SHA-256: `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`
- 참조 범위: 보이는 성인 얼굴과 머리 외형 참고만 사용. 동일인, 생체 신원, 민감 특성 판단 없음.
- arm별 image call: 1
- 전체 retries: 0
- cross-arm input: 없음
- 공통 candidate pack: v6

## Arm 01 — Chaoskampf

이미지: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-01-chaoskampf/render-attempt-01.png`

SHA-256: `f881178191337c11a6d0711e883411b069f93797b4bc6edc38bd9786123277bb`, 1024×1535

최종 프롬프트:

```text
Photorealistic: cosmogonic combat visibly producing ordered realms, a battle that visibly turns primordial disorder into a measured world. At a flooded salt quarry, one adult woman storm-bearer wears four-river bronze regalia; one tradition-bound champion remains distinct from the adversary and leads the ordering side as the adult woman storm-bearer. Opposing her, one primordial sea storm serpent or chaos adversary is visually distinct and tradition-bound, embodied as a single colossal rain-dark serpent resisting at the strike point. She drives a bronze axis-spear down across the armored jaw of one colossal abyssal sea serpent onto a basalt meridian stone. Weapon force counterforce and contact geometry make the central combat readable as both of her hands drive the spear against the serpent's jaw. Lightning links spear, contact, and coil. The adversary visibly passes from active resistance into a defeated or partitioned state because the spear pins its jaw and its resisting coil is splitting at the same impact. New boundaries world matter stable realms or sovereign placement visibly result from that defeat as four straight rivers and concentric terraces emerge from the pinned flood. Her clearly visible face and long center-parted dark wavy hair follow only the supplied portrait's visible facial and hair appearance. Image 1 solely guides appearance continuity; preserve eye aperture and spacing, face length, jaw width, brows, nose, lips, cheekbones, asymmetry, and hairline. Low 35mm framing keeps face, hands, contact, coil, rivers, and terraces legible together. Deep focus, cobalt backlight, bronze return, wet salt, scales, spray: documentary texture.
Avoid: cartoon style, 3D render look, illustration look, distorted fingers, low resolution, excessive HDR, unrealistic hands, body distortion
```

판정: champion PASS, adversary PASS, combat PASS, defeat FAIL, defeat-caused order FAIL. 3/5, `revise`. 전경의 머리와 코일이 여전히 능동적으로 온전하고, 원경 파편은 타격과 한 몸으로 이어지는 패배 상태가 불명확하다. 방사형 수로와 계단식 지형도 새로 생긴 질서보다 기존 채석장 지형처럼 읽힌다. 외형 통제도 눈·얼굴 길이·턱 폭 변화로 실패했다.

## Arm 02 — Katabasis

이미지: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-02-katabasis/render-attempt-01.png`

SHA-256: `0eb511d354d819c161c93120551bbdf5f76a23e3122589486c04faf9533bfff4`, 1122×1402

최종 프롬프트:

```text
Create a photograph of a living adult woman cartographer actively descending a steep, rain-wet basalt stair from a small rectangle of daylight into a cavernous realm of the dead. Image 1 supplies visible face-and-hair cues only: long near-black softly wavy hair with a center part, softly arched brows, almond-shaped brown eyes, and a softly tapered oval face. Show the living traveler visibly descending across an underworld threshold in one continuous full-body frame. One traveler shows breath warm color active grip or another explicit sign of living agency: her flushed skin, condensed breath, and firm astrolabe grip. Daylight vegetation settlement or another human-world cue remains behind the traveler: a taut red cord leads continuously up to the daylight opening. Stairs slope gate or river crossing establishes a directional descent across a boundary: her two boots straddle the carved basalt gate on descending treads. A distinct chthonic realm lies below or beyond the crossed threshold, with skeletal inhabitants, a hooded ferryman, and a black subterranean river. A named objective guide token retrieval object or mission cue travels with the living visitor: her glowing astrolabe points toward the ferryman's drowned-city map tablet. At mid-descent, she reaches a glowing brass astrolabe toward a hooded skeletal ferryman beside a black subterranean river; he visibly holds a cracked ceramic map tablet. The astrolabe light has just split the boat's iron mooring chain, with one opened link falling in sparks as dead passengers turn toward her. Use 24mm deep focus and a lantern beam linking daylight, traveler, threshold, ferryman, and broken chain through mineral haze.
Avoid: unrealistic hands, plastic-looking skin, excessive HDR, cartoon style, illustration look, 3D render look, body distortion, over-processed retouching, broken facial features, fake-looking background
```

판정: living PASS, origin PASS, threshold FAIL, destination PASS, purpose PASS. 4/5, `revise`. 여행자는 이미 하부 착지면에 두 발을 모아 서 있어 살아 있는 사람이 경계를 실제로 내려가는 순간은 부분 충족에 그친다. 지도판의 요청하지 않은 의사문자도 추가 결함이다. 보이는 얼굴·머리 외형 연속성은 통과했으며 동일인 판정은 하지 않았다.

## Arm 03 — Moirai

이미지: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-03-moirai/render-attempt-01.png`

SHA-256: `054ec31dbff7a446e317de6aa4ab8bf93056e6139564e04869893160baeb0395`, 1448×1086

최종 프롬프트:

```text
Photorealistic editorial photograph in a storm-battered tidal observatory at blue hour. Moirai visibly spinning measuring and cutting one life thread is expressed through this scene. Three unmistakably adult women stand around a circular stone worktable, performing a three-stage allocation of one human life by a spun, measured, and cut thread. The left woman spins a fresh luminous red thread from a wooden spindle; the central woman draws that same continuous thread taut against a graduated bronze measuring rule; the right woman closes open iron shears through its far end. Simultaneously, three distinct fate figures occupy separate readable work roles around one shared mortal allocation table; the first figure visibly spins or draws the beginning of the thread from a loaded wooden spindle into a bright origin coil; the second figure visibly measures an allotted section of that same thread against a graduated bronze rule with marked endpoints; the third figure visibly cuts the endpoint of that same thread with open iron shears at the marked terminal point; one continuous mortal life thread physically connects the spin measure and cut roles from origin across the rule to the recipient's hourglass token. One adult lighthouse keeper in a wet yellow oilskin holds a clear hourglass below the cut point; the severed measured length falls inside, igniting finite amber sand-light while the unused filament is dark. The central measuring woman carries only the reference image's visible facial appearance and loose, long, center-parted dark hair. Image 1 guides observed realistic-adult facial geometry: eye aperture and spacing, brows, nose, lips, face length, lower-face and jaw width, cheek contours, hairline, and natural asymmetry; the figure is fictional and no identity claim is made. A medium-wide three-quarter tableau keeps every face, six worker hands, tools, complete thread path, recipient, and consequence legible. Cool blue-hour lightning contrasts localized red-thread and amber-hourglass glow on flooded mosaics beneath a brass astrolabe.
Avoid: cartoon style, 3D render look, unrealistic hands, broken facial features, body distortion, over-processed retouching, low resolution, plastic-looking skin
```

판정: three roles PASS, spin PASS, measure PASS, cut FAIL, continuity PASS. 4/5, `revise`. 가위는 열려 있고 한 가닥이 끊김 없이 굽어 지나가므로 잘린 틈과 분리된 끝이 보이지 않는다. 중앙 인물의 아래쪽 시선 때문에 참조에서 보이는 눈 개구·간격을 완전히 비교할 수 없어 외형 통제도 엄격 규칙상 실패했다.

## 테스트 유래 후보팩 보강점

1. `chaoskampf`: 패배 변화와 질서 형성이 같은 타격 지점에서 시작하고, 파편이 같은 적의 몸에서 이어지는 것을 의무화한다. 기존 질서 지형이나 분리된 원경 파편을 대체물로 명시한다.
2. `katabasis`: 뒤쪽 발은 인간 세계 쪽, 앞쪽 발은 경계 아래 또는 너머에 두고 무게중심이 아래로 이동하는 교차 토폴로지를 추가한다. 두 발이 한 착지면에 정착한 상태를 실패 대체물로 둔다.
3. `moirai`: 연속성을 “실패 없이 한 가닥”이 아니라 “물레→측정→단 하나의 절단점까지 추적 가능한 같은 실”로 정의하고, 닫힌 날·작은 절단 간격·분리된 끝을 동시에 요구한다.
4. 참조 외형 통제: 복잡 장면에서도 얼굴 크기와 시선 방향이 눈 개구, 얼굴 길이, 아래 얼굴 폭을 실제로 비교할 수 있을 만큼 확보되도록 한다.

## 증거 위치

- 사전 랜덤 할당: `coordination/random_assignment.json`
- 사전 픽셀 기준: `coordination/precommitted_pixel_rubric.json`
- 루트 독립 재검토: `coordination/root_independent_pixel_review.json`
- 각 arm의 pack, prompt, runtime request, audits, test case, self review, manifest, ledger, crops, report는 해당 arm 디렉터리에 보존되어 있다.

스킬 영향: `image-prompt-skill-improver`가 baseline/core를 후보 노출 전에 고정하고 partial을 fail로 유지했다. `photo-prompt-image-generator`가 v6 pack, visual obligation, composed/runtime audits와 manifest lineage를 만들었다. `imagegen`은 각 arm에 참조 이미지를 실제 첨부한 built-in 호출을 1회씩 실행하고 반환 파일을 프로젝트에 보존했다.
