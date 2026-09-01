# arm-02 katabasis 독립 평가 보고서

## 결론

- 프로필: `katabasis_living_underworld_descent`
- 결과: `revise`
- prompt/composed audit: PASS
- exact runtime request audit: PASS
- 픽셀 기술 자격: FAIL (`vo_myth_katabasis_threshold`)
- 사용자 선호: `pending`
- built-in image call: 1회
- retries: 0
- CLI/API fallback: 사용 안 함
- 다른 arm 입력: 사용 안 함

생성 이미지는 생자성, 지상 기원, 저승 목적지, 목적 표식을 충족했다. 그러나 두 발이 같은 하부 착지면에 고정되어 경계문을 걸쳐 아래로 이동하는 순간이 보이지 않는다. 계단 방향만 보이는 것은 bounded active crossing의 부분 충족이므로 FAIL이다. 다섯 profile gate가 한 이미지에서 모두 PASS하지 않아 qualified로 승격하지 않았다.

## 독립 baseline과 phase boundary

`request_envelope.json`과 지정 참조 JPEG만 확인한 뒤, 프로젝트 후보팩·레지스트리·프로필·기존 실험 자료를 열기 전에 192단어 `photo-authorial-core/v3`를 동결했다. core의 `source_request`는 envelope의 `request_text`와 byte-equal하며 SHA-256은 `ac3d78504fabac5fdbed1c19d51b0e8dcfaf0a5bb0cbb32f92d1893d778813c0`이다.

독립 컨셉은 살아 있는 성인 지도 제작자가 빗물 젖은 현무암 계단을 내려가 사자의 강 뱃사공이 든 익사 도시 지도판을 향해 황동 천문의를 내밀고, 그 빛이 배의 계류 사슬을 끊는 한 정지 프레임이다. actor, action, target, consequence를 잠갔고 `framing`, `lighting`, `camera`, `color`는 열린 차원으로 남겼다.

core 동결 뒤에만 현재 레지스트리를 읽어 post-core `photo-visual-intent/v1`로 다음 다섯 hard component를 활성화했다: 생자성, 지상 기원, 아래 방향의 경계 통과, 별도 저승 목적지, 방문 목적 표식.

## 최종 runtime prompt

```text
Create a photograph of a living adult woman cartographer actively descending a steep, rain-wet basalt stair from a small rectangle of daylight into a cavernous realm of the dead. Image 1 supplies visible face-and-hair cues only: long near-black softly wavy hair with a center part, softly arched brows, almond-shaped brown eyes, and a softly tapered oval face. Show the living traveler visibly descending across an underworld threshold in one continuous full-body frame. One traveler shows breath warm color active grip or another explicit sign of living agency: her flushed skin, condensed breath, and firm astrolabe grip. Daylight vegetation settlement or another human-world cue remains behind the traveler: a taut red cord leads continuously up to the daylight opening. Stairs slope gate or river crossing establishes a directional descent across a boundary: her two boots straddle the carved basalt gate on descending treads. A distinct chthonic realm lies below or beyond the crossed threshold, with skeletal inhabitants, a hooded ferryman, and a black subterranean river. A named objective guide token retrieval object or mission cue travels with the living visitor: her glowing astrolabe points toward the ferryman's drowned-city map tablet. At mid-descent, she reaches a glowing brass astrolabe toward a hooded skeletal ferryman beside a black subterranean river; he visibly holds a cracked ceramic map tablet. The astrolabe light has just split the boat's iron mooring chain, with one opened link falling in sparks as dead passengers turn toward her. Use 24mm deep focus and a lantern beam linking daylight, traveler, threshold, ferryman, and broken chain through mineral haze.
Avoid: unrealistic hands, plastic-looking skin, excessive HDR, cartoon style, illustration look, 3D render look, body distortion, over-processed retouching, broken facial features, fake-looking background
```

`negative_en`은 pack bytes를 그대로 보존했다. profile의 `runtime_forbidden_labels`는 비어 있었고, 선택적 `figura_serpentinata_spiral_pose`, `medium_native_glitch`, 여섯 creative 후보는 모두 거절했다.

## 픽셀 판정

| Gate | 판정 | 이미지 근거 |
|---|---|---|
| `vo_myth_katabasis_living` | PASS | 따뜻한 피부색, 응결된 숨, 천문의를 향한 능동적 손 동작이 주변 해골과 분명히 구별된다. |
| `vo_myth_katabasis_origin` | PASS | thumbnail에서 밝은 야외 입구, 위쪽 젖은 계단, 붉은 줄이 인물 뒤와 위에 남는다. |
| `vo_myth_katabasis_threshold` | FAIL | 계단 방향은 보이지만 두 발이 같은 하부 착지면에 서 있고, 경계를 걸쳐 아래로 통과하는 동작은 없다. 부분은 FAIL이다. |
| `vo_myth_katabasis_destination` | PASS | native에서 검은 지하 수로, 배, 후드 쓴 해골 뱃사공, 다수의 사자가 별도 저승 영역을 만든다. |
| `vo_myth_katabasis_purpose` | PASS | 빛나는 황동 천문의가 뱃사공의 금이 간 지도판과 배 사슬을 향해 있어 방문 목적이 읽힌다. |

추가 관찰:

- actor/action/target/consequence: 천문의 동작, 뱃사공/지도판 target, 불꽃이 튀는 사슬 consequence는 보이나 active downward step이 빠져 conjunction은 FAIL이다.
- 외형 참고 연속성: 긴 거의 검은 중앙 가르마의 부드러운 웨이브, 완만한 아치형 눈썹, 갈색 아몬드형 눈, 끝이 부드럽게 좁아지는 성인 타원형 얼굴이 이어진다. 이는 보이는 외형 비교일 뿐 동일인·신원 판정이 아니다.
- anatomy/contact: native에서 중대한 여분 팔다리, 손·발·관절 붕괴, 그립 또는 지면 접촉 붕괴는 발견하지 못했다.
- text artifact: 지도판에 요청하지 않은 큰 의사 라틴 문자가 나타나 추가 quality FAIL로 기록했다.
- 결과 PNG: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-mythology-three-arm-reference-v1/arm-02-katabasis/render-attempt-01.png`
- 결과 SHA-256: `0eb511d354d819c161c93120551bbdf5f76a23e3122589486c04faf9533bfff4`
- 참조 SHA-256: `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`

## 스킬 사용과 영향

- `photo-prompt-image-generator`: pre-core 격리, byte-bound envelope/core, v6 후보팩, post-core visual intent, open-dimension 제한, pack negative 보존, composed/runtime fail-closed audit를 적용했다.
- `imagegen`: built-in 모드를 사용하고 local reference path를 실제 첨부했다. 반환된 concrete local path에서 arm 폴더로 비파괴 복사했으며 재시도와 CLI/API fallback은 하지 않았다.
- `image-prompt-skill-improver`: package/prompt/generation/pixel/user evidence를 분리했다. prompt PASS를 pixel PASS로 승격하지 않았고, 한 motivating render만으로 skill 변경이나 일반화를 하지 않은 채 `iteration_record.json`을 `revise`로 남겼다.

## 실행한 감사와 기록 명령

1. `generate_photo_prompt.py ... --candidate-pack-version v6 --reference-edit-mode identity --creativity 0.5 --emit-candidate-pack --n 1`: 최종 exit 0, pack `ce021c982f366a85`. 사전 구조 검증에서 허용되지 않은 `color_palette`와 불충분한 profile anchor가 각각 차단되어, baseline 의미를 바꾸지 않고 `color` 및 literal profile anchor로 교정했다. 이미지 호출은 발생하지 않았다.
2. `audit_composed_prompt.py --pack candidate_pack.json --composed composed_prompt.json`: exit 0, `status=pass`, failures 0, prompt 258 words, advisory warning만 존재.
3. `audit_image_render_request.py --pack ... --composed ... --request render_request.json`: exit 0, `status=pass`, reference count 1, negative match true.
4. built-in `image_gen` + 지정 local reference: 정확히 1회 성공, concrete local path 반환, retries 0.
5. `audit_moe_render_review.py --pack ... --composed ... --review self_review.json`: exit 1은 예상된 non-promotion 결과이며, `qualification_status=failed_technical_hard_gates`, schema failures 0, failed gate는 `vo_myth_katabasis_threshold` 하나다.
6. `validate_iteration_record.py iteration_record.json`: exit 0, `status=ok`, errors 0.
7. `record_image_run.py ... --image-call-count 1 --independent-no-cross-arm-inputs`: exit 0, run ID `b58daf1580f7d306`, prompt ID `6b36f8a9594aa525`.

`run_manifest.json`은 `image_call_count=1`, `retries=0`, `independent_no_cross_arm_inputs=true`, `cross_arm_inputs_used=false`, `pixel_qualification=revise`, `user_judgment=pending`을 기록한다.
