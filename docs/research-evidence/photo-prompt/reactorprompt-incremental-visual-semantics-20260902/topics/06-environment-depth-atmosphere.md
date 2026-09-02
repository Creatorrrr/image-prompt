# 06. 환경·배경 구조·깊이·대기·날씨

- 조사일: 2026-09-02
- 상태: **proposed — 설계·리서치만 완료, 런타임 미구현, 렌더 자격 미평가, 사용자 판단 미평가**
- 기준 리비전: `8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab`
- 코퍼스: `generated/reactorprompt-export-20260902-incremental/manifest.json`
- 범위: 환경/배경 구조, 전경·중경·배경 깊이, 대기 원근, 날씨의 가시 결과, 피사체-환경 균형
- 비범위: 인물 정체성·인구통계 추론, 건축물만으로 문화권/국적 단정, 보이지 않는 기후·역사·생태 기능 추론

## 1. 결론

새 ReactorPrompt 코퍼스에서 환경이 잘 읽히는 이미지는 장소 명사나 배경 흐림이 많은 이미지가 아니었다. **피사체, 행동, 장소 구조, 접촉 표면, 구도**가 한 프레임에서 인과적으로 연결되고, 깊이나 날씨를 서로 다른 두 종류 이상의 단서가 지지하는 이미지였다.

이번 조사에서 확인한 핵심 간극은 다음과 같다.

1. 기존 데이터는 장소 후보 576개, 구도 후보 249개, 표면 재질 후보 137개, 날씨 후보 37개와 다수의 깊이 후보를 이미 보유한다. 환경 명사를 더 늘리는 것이 우선 과제가 아니다.
2. 프롬프트에서는 `background`, 얕은 심도, 안개·비·바람 표현이 흔하지만, 명시적인 **중경**, **상대 크기**, **선원근**, **대기 대비 감소**는 드물다. 선언된 깊이가 실제 3평면 구조로 이어진다고 볼 수 없다.
3. 픽셀에서 강한 사례는 실내 작업면-피사체-후면 설비, 유리 경계-빗물-젖은 외부, 근거리 사물-피사체-수평선처럼 관계를 추적할 수 있었다. 반대로 꽃다발 전경, 두 사람의 앞뒤 배치, 균일한 Gaussian-like blur, 청회색 색보정은 환경 깊이나 물리적 대기의 대체물이 되지 못했다.
4. 따라서 보강점은 새 장소 사전이 아니라 다음 두 축이다.
   - 일반 인물/사물 장면의 `subject_environment_role`과 독립적인 `depth_cue` 묶음
   - `phenomenon_process → visibility/light → surface_material → subject/prop response`의 날씨·대기 결과 사슬
5. 두 축 모두 광범위 자동 활성화가 아니라, 일반 표현에는 자문 후보로 작동하고 정확한 관계 구문에만 하드 시각 의무를 부여해야 한다.

최종 판단은 `proposed`다. 코퍼스 관찰은 소유권과 테스트 설계를 제안하기에 충분하지만, 이 보고서에서 후보 데이터·프로필·런타임·테스트를 수정하거나 새 이미지를 생성하지 않았다. 새 후보의 프롬프트 통과, 렌더 픽셀 통과, 사용자 미감 판단은 모두 `UNSCORED`다.

## 2. 조사 범위와 표본 방법

### 2.1 고정 입력

공유 브리프의 고정 입력을 그대로 사용했다.

| 항목 | 값 |
|---|---:|
| 게시물 | 1,182개, ID 1565–2746 |
| 이미지 | 4,908개 |
| 비어 있지 않은 프롬프트 | 924개 |
| 고유 프롬프트 본문 | 904개 |
| 프롬프트 누락 | 258개 |
| manifest SHA-256 | `0f4cdd97730a3009071c853b6006fbbf00e14cfe8541935663f35cf6a38f7732` |
| gallery SHA-256 | `35142b192966bd01eefa7c7cfdc05e7ca83a2f1c2ac43a7e34e6e693689cc64f` |
| translation SHA-256 | `d2483fc1eefc941ddf2a51137ac2114cea0de61e8be3c152c00d49cfe5ce6586` |
| visual-obligation source SHA-256 | `64e73c97f12da099b18cb7be4e0086f0c51c66d63380c297ec7632709b4805bc` |
| tag/candidate source SHA-256 | `5ae9ae8311f418875a011d7fd887804c9b974f26941689679af55a1499406b00` |
| quality source SHA-256 | `99597926d0f136bfabaf5f8be28597aae82f15bdbe8e3bfcfbbb774b3ac0541f` |
| generated profile index SHA-256 | `4d674dc00cfa05897f837a7b53410d18766edb8556b1378190523e6e4d1b6626` |

### 2.2 프롬프트 전수 스캔

비어 있지 않은 924개 프롬프트 전부를 대소문자 무시 정규식으로 스캔했다. 넓은 의미군 집계에서는 문장/개행 단위 절을 나눈 뒤 `no`, `without`, `avoid`, `exclude`, `absent`, `never`, `not`가 있는 절을 부정 선언으로 따로 셌다. 이 휴리스틱은 자연어 파서가 아니므로 중첩 부정과 인용문을 완전히 해결하지 못한다. 아래 수치는 **코퍼스의 프롬프트 표현량**이지 픽셀 성공률이 아니다.

### 2.3 픽셀 표본

환경·깊이·대기·날씨 표현이 상대적으로 풍부한 게시물을 초기/중기/후기로 나누어 16개 선정했다. 각 게시물의 첫 이미지와 마지막 이미지를 보되, 이미지가 한 장뿐인 1852는 중복 계산하지 않았다. 각 양성 게시물마다 가장 가까운 ID의 비어 있지 않은 프롬프트 중 주제 점수 1 이하인 게시물을 결정론적 근접 대조군으로 붙였다.

- 썸네일 판독: **47개 고유 이미지 파일 / 32개 게시물**
- 네이티브 판독: 위 47개 중 **16개 파일**
- 게시물 범위: 초기 5개, 중기 5개, 후기 6개 양성 + 각 1개 근접 대조군
- 표본 성격: 목적 표본이며 무작위 대표 표본이 아니다. 따라서 `47/4,908`의 관찰을 코퍼스 전체 빈도로 일반화하지 않는다.
- 한 프레임 원칙: 같은 게시물의 서로 다른 이미지에 흩어진 증거를 한 이미지의 통과 근거로 합치지 않았다.

### 2.4 증거 층 분리

| 층 | 이번 보고서에서 답하는 것 | 답하지 않는 것 |
|---|---|---|
| 프롬프트 선언 | 작성자가 어떤 환경·깊이·날씨를 요구했는가 | 이미지가 실제로 구현했는가 |
| 코퍼스 픽셀 | 기존 이미지 한 장에서 무엇이 읽히는가 | 새 후보가 생성 모델에서 재현되는가 |
| 후보/프로필 설계 | 어느 레이어가 무엇을 소유해야 하는가 | 런타임이 실제로 선택·합성하는가 |
| 생성 자격 | 이번 조사에서는 수행하지 않음 | 프롬프트 PASS, 픽셀 PASS 모두 `UNSCORED` |
| 사용자 판단 | 이번 조사에서는 수행하지 않음 | 미감·유사도·선호를 자동 판정하지 않음 |

## 3. 프롬프트 측 전수 조사

### 3.1 넓은 의미군

의미군끼리 중복되며 합계는 924가 아니다.

| 의미군 | 원시 일치 게시물 | 긍정 절 일치 | 부정 절에만 일치 | 해석 경계 |
|---|---:|---:|---:|---|
| 명시적 배경/장면 구조 | 588 | 546 | 42 | `background`, `backdrop`, `scene`, 배경 구조 표현을 포함한 넓은 군 |
| 전경 | 99 | 94 | 5 | 프레임 가장자리 사물과 인물 앞 사물을 모두 포함 |
| 깊이 구조 | 504 | 462 | 42 | depth, perspective, focus falloff, bokeh 등을 포괄 |
| 대기/공중 매질 | 336 | 313 | 23 | haze, mist, fog, smoke, particles, volumetric 등 |
| 날씨 | 200 | 192 | 8 | rain, snow, wind, storm, overcast 등 |
| 자연 장소 | 367 | 334 | 33 | forest, coast, garden, mountain, field 등 |
| 건조 환경/실내 장소 | 590 | 552 | 38 | room, street, rooftop, studio, shop 등 |
| 배경 억제 | 288 | 225 | 63 | plain/clean/uncluttered/blurred/no background를 넓게 포함 |
| 환경의 프레임 점유·우선순위 | 6 | 5 | 1 | 환경이 주역/대부분의 프레임이라고 직접 말한 경우 |
| 표면 결과 | 42 | 35 | 7 | wet pavement, runoff, condensation, puddle 등 직접적인 결과 표현 |

주요 공기·공간 공출현은 `depth_structure + atmosphere` 202개, `natural_setting + weather` 116개, `built_setting + weather` 111개, `weather + surface_consequence` 25개였다. `explicit_background + background_suppression`도 196개여서 “배경을 말함”과 “배경을 구조적으로 보여 줌”이 같은 개념이 아님을 확인했다.

### 3.2 정확 단서 감사

넓은 의미군과 별도로, 실제 깊이 판독에 가까운 구문을 더 좁게 셌다.

| 정확/협소 구문 | 일치 게시물 | 의미 |
|---|---:|---|
| `foreground` | 93 | 전경을 직접 지칭 |
| `midground` 또는 `middle-distance` | 2 | 게시물 2553, 2610뿐 |
| `background` 또는 `backdrop` | 503 | 배경 직접 지칭 |
| 세 평면을 모두 직접 지칭 | 1 | 게시물 2610 |
| occlusion | 9 | 상대적 앞뒤 순서를 암시 |
| linear perspective | 7 | 수렴선/직선 원근을 직접 지칭 |
| relative scale | 4 | 크기 감소를 직접 지칭 |
| texture gradient | 0 | 명시 구문 없음 |
| atmospheric depth/aerial perspective | 7 | 거리별 대비·색 변화에 가까운 표현 |
| focus falloff/shallow/deep/bokeh | 292 | 광학적 흐림·초점 표현 |
| environmental portrait | 6 | 장르/관계 직접 지칭 |
| 환경/피사체 프레임 점유율 직접 지시 | 8 | 하늘 비율, 넓은 환경, 작은 인물 등 |
| 날씨 방향/공통 변형 관계 | 69 | 바람 방향, 휘는 머리·옷·식생 등 |
| 날씨-표면 반응 | 61 | 젖음, 반사, 물방울, 퇴적, 유출 등 |

중요한 비대칭은 **초점·bokeh 계열 292개 대 중경 2개**다. 이 코퍼스에서 “depth”는 쉽게 “배경을 흐리게 한다”로 축약될 수 있다. 그러나 흐림은 단일 단서일 뿐이고, 깊이의 양이나 장소 구조를 혼자 증명하지 못한다. 시각 연구에서도 가림, 상대 크기, 선원근, 질감 변화, 대기 원근, 음영, 흐림은 서로 다른 그림 단서이며 서로 충돌할 수 있다고 정리한다. 특히 가림은 앞뒤 순서는 알려도 거리의 양 자체를 알려 주지는 않는다. [Stereoscopy and the Human Visual System](https://pmc.ncbi.nlm.nih.gov/articles/PMC3490636/)

## 4. 픽셀 측 관찰

### 4.1 높은 정합 사례

| 게시물 | 실제 픽셀에서 읽힌 관계 | 프롬프트 선언과의 경계 |
|---|---|---|
| 1651 | 모래/인물/수평선·등대·작은 해변 인물이 단계적으로 읽히고 머리카락이 바람 방향을 보임 | 배경이 다소 흐려도 해안 장소와 바람의 공통 원인이 남음 |
| 1933 | 인물 전경, 물·수영객 중거리, 먼 건물과 수평선이 이어짐; 머리카락 바람과 일상 활동이 장소에 결합 | Dutch tilt/저가 카메라 흔적은 깊이와 별도 속성 |
| 1940 | 근거리 병·싱크·접시·물 접촉, 인물의 행동면, 뒤쪽 선반·가전의 세 평면이 연결 | “주방” 명사보다 작업면과 행동이 장소를 증명 |
| 2076 | 곤돌라 내부/창·반사/인물/눈 덮인 산 배경이 분리되고 깊은 초점 선언이 대부분 유지 | 유리 경계와 원경이 함께 남아 단순 산 배경보다 강함 |
| 2422 | 유리 대피 구조, 유리 물방울, 젖은 선로·지면, 우산의 물방울이 한 날씨 상태로 연결 | 빗줄기 자체보다 경계·표면·도구의 결과 사슬이 강함 |
| 2686 | 빗줄기·처마 유출, 젖은 중정, 웅덩이·반사, 젖은 머리카락이 같은 시간 상태를 지지 | 건축만으로 문화적 정체성을 추론하지 않고 “built courtyard”로만 판독 |

### 4.2 부분 정합과 프레임 균형 손실

| 게시물 | 읽힌 것 | 손실/모호성 |
|---|---|---|
| 1634 | 전경 촛불, 실내 인물, 창밖 눈 덮인 정원과 온·냉 색 대비 | `volumetric` 대기 자체는 뚜렷하지 않음 |
| 2105 | 옥상 난간·하늘과 바람에 움직인 머리카락 | 피사체가 커서 장소의 구조적 깊이는 얕음 |
| 2188 | 전경 잎 흐림, 선명한 인물, 배경 초점 이탈 | “dreamy blur”는 보이지만 장소 고유성은 약함 |
| 2316 | 전경 유리잔, 인물, 갑판 난간 대각선, 바다 수평선 | 근접 크롭으로 선박·바다는 지원 맥락에 머묾 |
| 2610 | 전경 꽃, 인물, 후경 식생의 순서는 읽힘 | 프롬프트가 직접 요구한 중경의 다리 주변 꽃과 전신이 상반신 크롭에서 탈락; `partial_is_fail` 대상 |
| 2627 | 바람 부는 해안 구릉, 풀·나무·바다·하늘과 움직이는 머리카락 | 요청은 가로 16:9와 하늘 우세인데 결과는 세로형·큰 인물; 장소는 있으나 역할/점유율 의무 실패 |
| 2745 | 바람 머리카락, 옥상 난간, 바다·하늘 | 안개와 얕은 심도 흐림을 픽셀만으로 분리하기 어렵고 환경은 보조적 |

### 4.3 거짓 양성·매체/결합 불확실성

| 게시물 | 관찰 | 왜 환경 증거가 아닌가 |
|---|---|---|
| 2236 | 검은 스튜디오에서 앞쪽 남성, 뒤쪽 여성 | 다중 인물의 앞뒤 배치이며 장소 구조가 아니다. `layered depth`라는 선언만으로 환경 깊이가 되지 않음 |
| 2587 | 꽃다발 전경, 인물, 특징 없는 실내 배경 | 꽃은 소품 깊이일 뿐 꽃밭/환경으로 승격할 수 없음. 캡션의 flower field와 프롬프트의 interior bouquet도 분리해야 함 |
| 1852 | 안개 속 군중, 크기 감소와 대비 저하가 보이는 한 스틸 | 프롬프트는 19초 8쇼트 영상이다. 한 이미지로 전체 시간 시퀀스를 검증할 수 없음 |
| 대조군 2628 | 캐주얼한 실내 인물 이미지 | 프롬프트는 사회 분석 글에 가까워 일부 행의 프롬프트-이미지 결합 자체가 불확실함 |

양성 목적 표본 16개를 보수적으로 나누면 6개는 강한 정합, 7개는 부분 정합, 3개는 환경 메커니즘의 거짓 양성 또는 매체 불일치였다. 이 분류는 코퍼스 통계가 아니라 후보 설계용 사례 코딩이다.

### 4.4 근접 대조군이 드러낸 키워드 집계의 한계

- 1653의 편의점 통로는 주제 정규식 점수가 낮아도 선반 반복, 통로 수렴, 사람의 크기 감소로 강한 선원근과 장소가 읽힌다.
- 2432의 테라스/카페/정형 정원은 테이블 행동, 난간 경계, 후방 정원 축이 환경 관계를 만든다.
- 2733의 욕실 거울 셀피는 반사면과 욕실 재질이 공간 깊이를 만든다.
- 1632, 1851, 1939, 2077, 2186, 2313, 2598, 2685는 평면 배경·스튜디오·그래픽 장면 대조군으로 유용하다.

즉 정확 키워드의 희소성은 구조의 부재와 같지 않다. BM25/embedding/정규식 적중은 **자문 검색 신호**로만 쓰고, 하드 의무는 작성자 코어의 정확한 관계 구문으로 활성화해야 한다.

## 5. 프롬프트 선언과 픽셀 판독의 분리

| 선언 | 픽셀에서 요구할 최소 증거 | 거절해야 할 대체물 |
|---|---|---|
| “foreground, midground, background” | 같은 한 프레임의 세 개 식별 가능한 평면과 연속된 앞뒤 순서 | 꽃다발+벽, 두 사람 앞뒤 배치, 여러 패널에 나뉜 증거 |
| “deep environmental depth” | 최소 두 종류의 독립 깊이 단서와 장소 고유 앵커 | 균일 blur, vignette, `cinematic depth`라는 형용사 |
| “atmospheric perspective” | 거리에 따라 대비·채도·에지 선명도가 점진적으로 감소 | 화면 전체에 같은 농도의 안개 필터, 얕은 심도만 존재 |
| “fog” 또는 “mist” | 지표 부근 시정 감소는 판독 가능하나 정확 분류는 거리 앵커 필요 | 흰색 컬러 그레이드, 배경 bokeh, 연막만으로 기상 분류 |
| “rain” | 낙하 입자 또는 비 이후 퇴적/젖음의 시간 일관성과 물질 반응 | 렌즈에 붙인 물방울, 마른 바닥 위 젖은 피부, 원형 bokeh |
| “wind” | 머리·옷·식생·강수 중 둘 이상의 방향 일치 | 한 요소만 임의 방향, 서로 반대인 변형 |
| “environmental portrait” | 요청 역할에 맞는 피사체 크기와 최소 두 장소 앵커 | 큰 인물 뒤의 식별 불가 색면 |
| “environment dominates” | 썸네일에서 환경 구조가 먼저/공동으로 읽히고 피사체가 규모 앵커 역할 | 세로 크롭으로 인물이 프레임 대부분을 점유 |

WMO는 fog를 지표의 수평 시정 1 km 미만, mist를 그 이상으로 구분한다. 알려진 거리나 규모 앵커가 없는 정지 이미지에서 둘을 확정적으로 구분하지 않는 것이 안전하다. [WMO, Fog compared with Mist](https://cloudatlas.wmo.int/fog-compared-with-mist.html)

WMO의 hydrometeor 분류는 물 입자가 공중에 떠 있음, 낙하함, 바람에 들림, 지면/물체에 퇴적됨을 구분한다. 따라서 `rain/snow/fog`라는 하나의 날씨 태그보다 **과정 상태와 물질 결과를 분리**해야 한다. 지면의 눈이나 물 자체는 같은 분류에서 공중 입자와 구별된다. [WMO, Hydrometeors](https://cloudatlas.wmo.int/en/general-classification-of-meteors-hydrometeors.html)

대기 흐림은 먼 구조의 대비와 질감을 약화시키므로, 대기 원근은 균일 blur가 아니라 거리별 대비·에지 변화로 판정해야 한다. [WMO, Luminance and haze](https://cloudatlas.wmo.int/en/appearance-of-clouds-luminance.html)

## 6. 현재 데이터와 소유권 경계

### 6.1 이미 존재하는 자산

기준 리비전의 `skills/photo-prompt-image-generator/assets/photo_prompt_tags.json`에는 다음이 이미 있다.

- `location` 576, `composition` 249, `surface_material` 137, `weather` 37, `ambient_particle` 12, `focus` 20 후보
- `facet_vocab.place_type`: `urban`, `street`, `interior`, `nature`, `studio`, `commercial`, `transport`, `home` 등
- `facet_vocab.weather`: `clear`, `rain`, `snow`, `fog`, `storm`, `heat`, `haze`, `dust`, `wind`, `flood`, `underwater`, `none`
- `facet_vocab.placement`: `layered_depth`, `foreground_frame`, `negative_space`, `frame_filling` 등
- `facet_vocab.weather_effect`: `visibility_loss`, `surface_wetness`, `airborne_particles`, `wind_deformation`, `heat_distortion`, `frost_accumulation`, `flooding`, `none`
- 구도 후보: `wide_establishing`, `extreme_wide_environmental`, `leading_lines_depth`, `through_doorway_deep_frame`, `scale_contrast_tiny_human`, `stage_haze_layers`, `leaf_foreground_bokeh`, `layered_reflection_depth`, `layered_foreground_midground_background`, `three_plane_depth_chain` 등

`photo_prompt_natural_environment_extension.json`은 이미 7개 슬롯 75개 후보를 가진다.

| 슬롯 | 현재 후보 수 |
|---|---:|
| `aesthetic_trend` | 12 |
| `subject` | 12 |
| `action` | 12 |
| `location` | 12 |
| `surface_material` | 11 |
| `composition` | 12 |
| `weather` | 4 |

이 확장은 `authored_filters_only`이고, `photo_prompt_visual_obligations.json`에는 노령림, 습지, 조간대, 카르스트, 활동 빙하, 풍성사구, 적란운, 고산 수목한계의 좁은 8개 하드 프로필이 있다. 기존 자연환경 렌더 자격 결과는 대상 환경 게이트 25/25였지만 공유 게이트 24/25, 엄격 전체 시나리오 3/5로 분리되어 있다. 즉 자연환경 키워드 픽셀 성공을 전체 시나리오 성공으로 바꾸어 말하면 안 된다. 근거는 `docs/research-evidence/photo-prompt/natural_environment_visual_semantics_20260901.md`와 `artifacts/photo-runs/20260901-natural-environment-five-arm-v1/coordinator/qualification_summary.json`이다.

`photo_prompt_quality_layers.json`에는 이미 다음 소유자가 있다.

- `photographic_integration.axes`: `interior_environment`, `performance_stage_environment`, `wet_or_weather_trace`, `longitudinal_place_evidence`, `close_camera_depth` 등
- `photographic_integration.categories`: `environment_binding`, `optical_depth`, `material_trace` 등
- `photographic_craft.dimensions`: `shot_intent`, `frame_hierarchy`, `environment_consequence` 등

`photo_prompt_research_extension.json`에는 `atmospheric_class = hydrometeor/lithometeor/photometeor`, `phenomenon_process = suspended_particles/falling_particles/wind_raised_particles/deposited_particles/optical_interaction`가 이미 있다. 새 대기 분류를 중복 생성해서는 안 된다.

### 6.2 제안 소유권

| 의미 | 단일 소유 레이어 | 하지 말아야 할 일 |
|---|---|---|
| 장소의 의미적 종류와 구조 앵커 | `location` | `focus`나 `weather`가 장소를 소유하지 않음 |
| 접촉면·젖음·퇴적·반사·유출 | `surface_material` | `rain` 태그 하나로 재질 결과를 암시하지 않음 |
| 평면 순서, 프레임 점유, 피사체-환경 역할 | `composition` + 새 관계 facet | `location` 후보에 카메라 점유율을 중복 저장하지 않음 |
| 흐림·초점면·광학적 falloff | `focus` | `shallow_depth` 하나를 환경 깊이 통과로 사용하지 않음 |
| 기상 상태 | `weather` | 대기 입자 과정과 물질 결과를 한 문자열에 뭉치지 않음 |
| 입자/광학 과정의 분류 | 기존 research extension의 `atmospheric_class`, `phenomenon_process` | 같은 값을 일반 tags에 재정의하지 않음 |
| 교차 슬롯 인과성과 픽셀 게이트 | `photo_prompt_quality_layers.json` | 후보 문구만으로 하드 통과 처리하지 않음 |
| 정확한 좁은 관계 구문의 하드 의무 | `photo_prompt_visual_obligations.json` | `background`, `rainy`, `cinematic`, `bokeh`로 자동 활성화하지 않음 |
| 생태·지형의 특정 자연 시스템 | 기존 natural-environment extension | 일반 인물 환경 관계를 생태 시스템 팩에 섞지 않음 |

## 7. 제안 시각 의미 문법

### 7.1 관찰 가능한 구성요소

환경 후보는 다음 5개 기본 슬롯과 1개 조건부 상태를 결합해야 한다.

| 구성요소 | 반드시 관찰 가능한 내용 | 예 | 거짓 대체물 |
|---|---|---|---|
| `subject` | 피사체의 환경 역할, 상대 크기, 프레임 점유 | 작은 사람이 큰 해안을 스케일링; 주방 행동의 주체 | 인물 뒤에 임의 배경 합성 |
| `action` | 장소 안에서/표면에 행하는 동작 또는 날씨가 피사체에 가한 결과 | 싱크에서 물을 다룸; 우산 아래 이동; 바람에 머리·옷이 움직임 | 장소와 무관한 정적 포즈 |
| `location` | 식별 가능한 구조 앵커 최소 2개와 경로/경계/수평선 중 하나 | 작업면+후면 선반; 유리 경계+선로; 난간+바다 수평선 | 장소 명사와 소품 목록 |
| `surface_material` | 접촉, 하중, 젖음, 반사, 먼지, 응결, 퇴적 등 상태 결과 | 젖어 어두워진 포장, 물방울 맺힌 유리, 처마 유출 | 전체 화면 gloss 필터 |
| `composition` | 전경/중간면/배경 순서, 읽기 경로, 역할별 점유율 | 전경 프레임→인물→원경, 작은 인물+넓은 환경 | bokeh 색면, 다중 패널 |
| 조건부 `weather/atmosphere` | 과정과 방향/시정/광학 결과 | 낙하 비→젖은 바닥→우산 물방울; 거리별 대비 감소 | `moody`, blue-gray grade, 연무 이름만 |

핵심 불변식은 다음과 같다.

1. `location`은 최소 두 개의 진단적 앵커로 읽혀야 한다.
2. 3평면을 요청했다면 세 평면이 같은 한 이미지에 있어야 한다.
3. 깊이는 서로 다른 두 종류 이상의 단서가 필요하다. blur는 보조 단서일 수 있지만 유일한 단서가 될 수 없다.
4. 날씨/대기는 가시성·광선·표면·피사체/소품 중 최소 두 영역에 일관된 결과를 남겨야 한다.
5. 피사체-환경 역할은 썸네일의 첫 읽기와 프레임 점유에서 확인해야 한다.
6. 정확히 요구되지 않은 소품 종류·세부 크롭·정확한 날씨 분류는 유연할 수 있지만, 역할과 인과 사슬은 유연하지 않다.

### 7.2 새 facet 제안

`photo_prompt_tags.json`의 `facet_vocab`에 다음 두 축을 추가하는 안을 제안한다. 전역 기본값을 두지 않고, 작성자 코어·정확 별칭·후보 자체 facet으로만 선택한다.

```json
{
  "subject_environment_role": [
    "supportive_context",
    "co_primary_relation",
    "environment_primary_scale_anchor"
  ],
  "depth_cue": [
    "occlusion_order",
    "relative_scale_recession",
    "linear_perspective",
    "texture_gradient",
    "aerial_contrast_loss",
    "focus_falloff"
  ]
}
```

- `supportive_context`: 환경은 분명하지만 피사체가 첫 읽기다.
- `co_primary_relation`: 피사체와 장소 구조가 함께 장면 명제를 만든다.
- `environment_primary_scale_anchor`: 환경 구조가 첫 읽기이고 피사체/알려진 물체가 규모 앵커다.
- `depth_cue`는 중복 선택 가능하되 하드 프로필에서는 서로 다른 두 값 이상을 요구한다.
- `focus_falloff` 단독은 하드 프로필을 만족하지 않는다.

### 7.3 일반 후보팩 제안

아래 후보는 단독 장소 명사가 아니라 관계 구문이다. 일반적인 자연어에는 자문 검색·선택 후보로만 작동한다.

| 제안 ID | 슬롯 | 핵심 문구/필수 관계 | 반대 예 |
|---|---|---|---|
| `co_primary_subject_place_relation_frame` | `composition` | 피사체 면 + 서로 다른 장소 앵커 2개, 썸네일에서 둘 다 소실되지 않음 | 큰 얼굴+정체불명 blur |
| `environment_primary_scale_anchor_frame` | `composition` | 환경 구조가 우세하고 작은 피사체/알려진 물체가 상대 크기를 제공 | 단지 wide lens 왜곡 |
| `weather_boundary_three_plane_frame` | `composition` | 전경 물방울/유리/처마, 보호된 피사체 면, 젖은 외부 경로/배경 | 렌즈 물방울 오버레이 |
| `multi_cue_environment_depth_frame` | `composition` | 전경·중간면·배경의 순서 + 서로 다른 깊이 단서 2개 | 전경 소품+평면 벽 |
| `atmospheric_contrast_recession` | `composition` | 거리에 따라 대비·채도·에지가 감소하고 가까운 앵커는 유지 | 화면 전체 균일 blur |
| `transparent_weather_threshold_location` | `location` | 유리/개구부/처마 경계가 피사체와 외부 날씨를 연결 | 임의 창문 배경 |
| `lived_in_action_bay_location` | `location` | 근접 작업면, 행동 공간, 후면 저장/설비 앵커가 연결 | 소품을 나열한 스튜디오 셋 |
| `open_horizon_scale_location` | `location` | 근거리 지형/표면, 중거리 피사체/물체, 원거리 수평선 | 하늘색 배경막 |
| `post_rain_deposit_runoff_surface` | `surface_material` | 재질별 젖음·물방울·웅덩이·유출 중 둘 이상이 같은 시간 상태 | 마른 바닥+젖은 피부 |
| `directionally_coupled_wind_material_state` | `surface_material` | 머리/옷/식생/모래/강수 중 둘 이상이 같은 바람 방향을 보임 | 요소마다 방향이 다름 |

기존 `after_rain_wet_pavement`, `sea_fog_coast`, `stage_haze_layers`처럼 겹치는 후보가 있으면 새 ID를 늘리지 말고 `facets`, `embedding_text`, `for_any`를 보강해 위 관계를 소유하게 해야 한다. 후보 ID 추가 전에 의미적 중복 검사를 필수화한다.

### 7.4 품질 레이어 제안

`photo_prompt_quality_layers.json`에서 교차 슬롯 관계를 다음처럼 소유한다.

1. `photographic_integration.axes.environment_relation` 제안
   - trigger: `subject_environment_role`, 환경 관계형 composition, 날씨 경계 location
   - required categories: `environment_binding`, `optical_depth`; 날씨가 있으면 `material_trace` 추가
   - 요구 문장: `subject role + diagnostic place anchors + contact/route relation`
2. `photographic_craft.dimensions.frame_hierarchy`에 `depth_cue_bundle` refinement 추가
   - 3평면 요청 시 세 앵커를 명명
   - 최소 두 개의 서로 다른 깊이 단서 명시
   - blur-only와 multi-person-only를 금지
3. `photographic_craft.dimensions.environment_consequence`에 `weather_state_chain` refinement 추가
   - `phenomenon_process → visibility/light → surface response → subject/prop response`
   - 비가 이미 그친 장면은 낙하 입자를 강제하지 않고 퇴적·유출·반사·재질 변화의 시간 일관성으로 통과 가능
4. `photographic_craft.dimensions.shot_intent`에 `subject_environment_balance` refinement 추가
   - `supportive_context`: 피사체 우세를 허용하되 장소 앵커 2개 유지
   - `co_primary_relation`: 썸네일에서 양쪽이 공동 명제를 형성
   - `environment_primary_scale_anchor`: 환경이 첫 읽기, 피사체는 규모 앵커

## 8. 좁은 하드 프로필 제안

### 8.1 `foreground_midground_background_environmental_depth_chain`

**정확 활성화 예**

- “foreground-midground-background environmental depth”
- “three-plane environmental composition with a readable foreground, middle plane, and location background”
- 한국어 동등 구문: “전경·중경·배경이 모두 읽히는 3평면 환경 깊이”

`depth`, `cinematic depth`, `bokeh`, `background`, `layered`, `environmental portrait` 단독으로는 활성화하지 않는다. BM25/embedding 적중도 자문 신호일 뿐 하드 활성화가 아니다.

**필수 구성요소/증거 필드**

| 그룹 | 필수 증거 필드 | 픽셀 의무 |
|---|---|---|
| 전경 | `foreground_anchor_phrase` | 프레임 가장자리/피사체 앞에서 부분 가림 또는 크기 기준 제공 |
| 중간면 | `middle_plane_phrase` | 주 피사체 또는 행동면이 전·후경과 분리 |
| 배경 | `background_location_anchor_phrase` | 장소를 식별하는 구조 앵커 최소 1개 |
| 독립 깊이 단서 | `independent_depth_cues_phrase` | `depth_cue` 중 서로 다른 2개 이상 |
| 연속성 | `relation_continuity_phrase` | 세 평면이 같은 카메라 공간과 앞뒤 순서를 공유 |

**픽셀 게이트**

1. 썸네일에서 전경/중간면/배경의 순서가 첫 읽기로 분리된다.
2. 중간면과 배경이 각각 이름 붙일 수 있는 앵커를 가진다.
3. 네이티브에서 독립 깊이 단서가 2종 이상이고, 모두 blur의 다른 표현이 아니다.
4. 가림·크기·선원근 중 사용된 단서가 공간 순서와 충돌하지 않는다.
5. 요청한 `subject_environment_role`이 썸네일 점유율과 읽기 순서에서 유지된다.

**거절 대체물**

- 꽃다발/컵 같은 전경 소품 + 특징 없는 벽
- 두 인물의 앞뒤 배치만 있는 스튜디오
- collage/multi-panel의 서로 다른 칸에 흩어진 세 평면
- 장소 명사/소품을 반복한 목록
- 화면 전체 균일 blur, vignette, haze overlay
- 세 평면 중 하나가 크롭되어도 나머지가 예쁜 경우; `partial_is_fail`

### 8.2 `weather_atmosphere_material_subject_consequence_chain`

**정확 활성화 예**

- “weather visibly affects both the subject and the environment”
- “post-rain environmental portrait with visible surface consequences”
- “directionally consistent wind across subject, clothing, and vegetation”
- 한국어 동등 구문: “날씨가 피사체와 환경 재질에 함께 결과를 남기는 장면”

`rainy`, `misty`, `storm mood`, `windy hair`, `wet`, `moody atmosphere` 단독으로는 활성화하지 않는다.

**필수 구성요소/증거 필드**

| 그룹 | 필수 증거 필드 | 픽셀 의무 |
|---|---|---|
| 현상/과정 | `phenomenon_process_phrase` | 기존 `phenomenon_process` 중 하나 또는 명확한 사후 상태 |
| 광학/시정 | `visibility_or_light_response_phrase` | 거리 대비, 확산광, 입자 궤적 등 |
| 접촉 표면 | `surface_material_response_phrase` | 젖음, 응결, 퇴적, 반사, 유출, 풍변형 등 |
| 피사체/소품 | `subject_or_prop_response_phrase` | 머리·옷·우산·신발·도구의 물리적 반응 |
| 일관성 | `direction_timing_continuity_phrase` | 방향과 사건 시간이 서로 충돌하지 않음 |

**픽셀 게이트**

1. 썸네일에서 날씨/대기의 주된 결과가 읽힌다.
2. 네이티브에서 입자·퇴적·시정 중 선언된 과정 증거가 확인된다.
3. 표면 반응이 재질에 맞고 장면의 같은 시간 상태를 공유한다.
4. 피사체/소품 반응이 날씨 방향 또는 사후 상태와 일치한다.
5. 색보정·렌즈 오버레이·bokeh만으로 결과 사슬을 대체하지 않는다.

**거절 대체물**

- 청회색 grade만으로 비/추위 주장
- 원형 bokeh를 빗방울로 주장
- 유리/렌즈에 붙인 물방울과 마른 장면
- 젖은 피부/머리와 마른 옷·바닥·가구
- 머리카락만 흔들리고 옷·식생은 반대 방향
- 거리/시정 앵커 없이 fog와 mist를 정확 분류
- active rain과 post-rain을 같은 게이트로 강제

## 9. 혼동 경계와 비추론 규칙

1. **배경 명사 목록 ≠ 환경 결합**: `kitchen, shelf, window, plant`가 있어도 행동면·경계·접촉이 없으면 장소 소품 목록이다.
2. **얕은 심도 ≠ 공간 깊이**: blur는 앞뒤 분리를 도울 뿐 3평면 구조나 거리량을 증명하지 않는다.
3. **전경 소품 ≠ 환경 전경**: 꽃다발·컵·카메라 가림은 장소 구조와 연결되어야 한다.
4. **다중 인물 배치 ≠ 환경 깊이**: 앞사람/뒷사람만으로 `environmental depth`를 통과시키지 않는다.
5. **색보정 ≠ 대기 현상**: 청회색, 저채도, bloom은 물리적 입자/시정/표면 반응과 별도다.
6. **현재 강수 ≠ 강수 이후 상태**: 빗줄기가 없어도 젖음·유출·웅덩이의 일관성으로 post-rain은 통과할 수 있다.
7. **날씨 단어 ≠ 물리 결과**: `windy`, `stormy`, `foggy`라는 선언은 방향·시정·재질 결과를 대신하지 않는다.
8. **풍경 명사 ≠ 환경 우세**: 큰 인물 뒤의 바다/산은 프레임 점유와 스케일 관계가 없으면 지원 맥락이다.
9. **multi-shot ≠ 한 프레임 증거**: 8쇼트 영상 프롬프트의 증거를 한 스틸에서 모두 충족했다고 판정하지 않는다.
10. **프롬프트-이미지 결합 불확실성**: 설명문/캡션/프롬프트가 서로 다르면 이미지가 어느 텍스트를 구현했는지 확정하지 않는다.
11. **건축 스타일 ≠ 문화·국적·정체성**: 관찰 가능한 공간 재질과 구조만 기록한다.
12. **환경 우세 ≠ 미적 선호**: 점유율과 첫 읽기는 판정할 수 있으나 “더 좋은 구도”인지는 사용자 판단이다.

## 10. 회귀·홀드아웃 설계

### 10.1 정적 라우팅 테스트

| 입력/사례 | 기대 결과 |
|---|---|
| 2610 계열의 정확한 “foreground, midground, background” 관계 구문 | 3평면 하드 프로필 활성화 |
| 2587 계열의 bouquet foreground + plain wall | 일반 전경 후보 가능, 환경 3평면 하드 프로필 비활성/픽셀 실패 |
| 2236 계열의 foreground man + background woman + black studio | 다중 인물 배치 후보 가능, 환경 깊이 하드 프로필 비활성 |
| 2422/2686 계열의 날씨-표면-피사체 정확 관계 구문 | 날씨 결과 사슬 하드 프로필 활성화 |
| “rainy portrait”, “windy hair”, “cinematic fog” | 날씨/분위기 자문 후보만; 하드 프로필 비활성 |
| 1940 계열의 작업면-행동-후면 설비 | `lived_in_action_bay_location` 및 co-primary 관계 검색 가능 |
| 1653 계열의 선반 통로, 그러나 깊이 키워드 없음 | 후보 검색은 가능하되 하드 프로필 자동 활성화 금지 |
| embedding이 정확 프로필 ID와 유사하나 코어에 좁은 구문이 없음 | advisory-only, required profile 미부착 |

### 10.2 최소 대조쌍

각 쌍은 다른 변수를 고정하고 한 관계만 제거한다.

1. 같은 장소에서 인물 크롭만 `co_primary` → `frame_filling`으로 변경
2. 같은 전경/배경에서 중간면 앵커만 제거
3. 같은 안개 농도에서 거리별 대비 구배 → 화면 전체 균일 blur로 변경
4. 같은 비 상태에서 젖은 바닥·유출·머리 반응을 함께 유지/제거
5. 같은 바람 장면에서 머리·옷·식생 방향을 일치/충돌시킴
6. 같은 창 장면에서 유리 물방울과 외부 젖은 표면을 연결/분리
7. 같은 해안에서 작은 인물 스케일 앵커를 유지/크게 확대
8. 같은 3개 앵커를 한 프레임/세 패널로 분리

### 10.3 홀드아웃 장면

동기 사례의 명사에 과적합하지 않도록 다음을 홀드아웃으로 둔다.

- 사람이 없는 건축 중정의 깊이
- 비 오는 창가의 제품/정물
- 동물과 서식 환경의 상대 크기
- 안개 낀 산맥의 거리별 대기 원근
- 연막을 사용한 스튜디오 인물
- 눈이 그친 뒤 퇴적·융해·발자국만 남은 장면
- 사막의 모래 이동과 인물/천/사구 방향 관계
- 야간 도시의 젖은 포장과 네온 반사

### 10.4 렌더 자격 게이트

후속 구현이 있을 때 각 arm은 독립 입력·독립 후보팩·한 번의 기록된 생성을 사용하고 다른 arm의 결과를 입력으로 쓰지 않는다.

| 게이트 | 배율 | 통과 조건 |
|---|---|---|
| `plane_order_thumbnail` | 썸네일 | 요청된 전·중·후경 또는 상대 역할이 첫 읽기로 분리 |
| `diagnostic_location_anchors` | 썸네일+네이티브 | 서로 다른 장소 앵커 2개 이상 |
| `independent_depth_cues` | 네이티브 | 서로 다른 깊이 단서 2개 이상, blur-only 금지 |
| `weather_process_or_aftermath` | 네이티브 | 현상 또는 사후 상태가 프롬프트 시간과 일치 |
| `surface_material_response` | 네이티브 | 재질별 젖음/퇴적/변형/반사 일관성 |
| `direction_timing_continuity` | 썸네일+네이티브 | 피사체·소품·환경의 방향/시간 충돌 없음 |
| `subject_environment_balance` | 썸네일 | 요청 역할과 점유율/첫 읽기 일치 |
| `single_frame_completeness` | 둘 다 | 다른 이미지/패널 증거를 합치지 않고 모든 필수 관계 충족 |

어느 하드 게이트든 하나가 실패하면 전체는 실패다. 프롬프트 감사 PASS는 픽셀 PASS가 아니며, `UNSCORED`를 0점이나 성공으로 처리하지 않는다.

## 11. bounded decision

### 제안: `proposed`

이 조사로 제안할 수 있는 것은 다음까지다.

- 일반 인물/사물 장면을 위한 `subject_environment_role`과 `depth_cue` facet
- 관계형 composition/location/surface 후보의 제한적 추가 또는 기존 후보 보강
- 두 개의 exact-only 하드 시각 프로필
- quality layer의 깊이 단서 묶음과 날씨 결과 사슬
- 최소 대조쌍, 홀드아웃, 썸네일/네이티브 픽셀 게이트

아직 주장할 수 없는 것은 다음이다.

- 제안 후보가 런타임에서 선택·합성된다는 주장
- 작성된 프롬프트가 모든 의무를 보존한다는 주장
- 생성 이미지가 깊이·날씨·환경 균형을 재현한다는 주장
- ReactorPrompt 목적 표본의 비율을 전체 4,908개 이미지의 비율로 일반화
- 사용자 미감, 유사도, 선호 통과

따라서 다음 단계는 소유권 중복 검사 → fixture/activation 테스트 → 독립 렌더 arm → 썸네일/네이티브 `partial_is_fail` 검토 순서다. 기존 자연환경 자격 결과는 참고선일 뿐 새 일반 환경 관계 후보의 렌더 자격을 대신하지 않는다.

## 12. 증거 부록

### 12.1 양성 표본과 실제 이미지 경로

모든 경로는 `generated/reactorprompt-export-20260902-incremental/` 기준이다.

| 양성 ID | 확인 이미지 | 근접 대조군 ID | 대조 이미지 |
|---:|---|---:|---|
| 1634 | `images/1634_DY7OAMTGkmz_01.jpg`, `images/1634_DY7OAMTGkmz_04.jpg` | 1632 | `images/1632_DY7OzfUmhAw_01.jpg` |
| 1651 | `images/1651_DY9bUzwGlaP_01.jpg`, `images/1651_DY9bUzwGlaP_05.jpg` | 1653 | `images/1653_DY9dbPGmltJ_01.jpg` |
| 1852 | `images/1852_DZkOvc2gcs__01.jpg` | 1851 | `images/1851_DZkO9i_mjuq_01.jpg` |
| 1933 | `images/1933_DZ3wPRtGsTh_01.jpg`, `images/1933_DZ3wPRtGsTh_04.jpg` | 1935 | `images/1935_DZ4YqqBmhAi_01.jpg` |
| 1940 | `images/1940_DZ4HfCHmsLF_01.jpg`, `images/1940_DZ4HfCHmsLF_04.jpg` | 1939 | `images/1939_DZ4LHOXGgno_01.jpg` |
| 2076 | `images/2076_DaZc8egGuUe_01.jpg`, `images/2076_DaZc8egGuUe_06.jpg` | 2077 | `images/2077_DaaYKTUGp4p_01.jpg` |
| 2105 | `images/2105_DaffUVZGt7_01.jpg`, `images/2105_DaffUVZGt7_05.jpg` | 2102 | `images/2102_DaffrQFGkl8_01.jpg` |
| 2188 | `images/2188_Da7FY-cGiOz_01.jpg`, `images/2188_Da7FY-cGiOz_06.jpg` | 2186 | `images/2186_Da5GLHrmtHO_01.jpg` |
| 2236 | `images/2236_DbDDsQumrpD_01.jpg`, `images/2236_DbDDsQumrpD_04.jpg` | 2235 | `images/2235_DbDENmfGjcH_01.jpg` |
| 2316 | `images/2316_Dbia_gPmsjf_01.jpg`, `images/2316_Dbia_gPmsjf_04.jpg` | 2313 | `images/2313_Dbc5UPhAbGl_01.jpg` |
| 2422 | `images/2422_Db0XqjAmnZ_01.jpg`, `images/2422_Db0XqjAmnZ_04.jpg` | 2432 | `images/2432_Dbzg9SQGhCh_01.jpg` |
| 2587 | `images/2587_DcYcT2DGsYm_01.jpg`, `images/2587_DcYcT2DGsYm_04.jpg` | 2598 | `images/2598_DcbWhFqmhZ2_01.jpg` |
| 2610 | `images/2610_DcdxSkHGtaR_01.jpg`, `images/2610_DcdxSkHGtaR_04.jpg` | 2611 | `images/2611_DcdzVommlj4_01.jpg` |
| 2627 | `images/2627_DcgT1OEGvWI_01.jpg`, `images/2627_DcgT1OEGvWI_04.jpg` | 2628 | `images/2628_DcgPtJoGg_S_01.jpg` |
| 2686 | `images/2686_Dcn1s_EGlJT_01.jpg`, `images/2686_Dcn1s_EGlJT_04.jpg` | 2685 | `images/2685_Dcn2ZfkGjA__01.jpg` |
| 2745 | `images/2745_Dcxz4LZGrtY_01.jpg`, `images/2745_Dcxz4LZGrtY_04.jpg` | 2733 | `images/2733_DcsnmkZGqa8_01.jpg` |

### 12.2 네이티브 확인 파일

- 양성: 1634 `_01`, 1651 `_01`, 1852 `_01`, 1933 `_01`, 1940 `_01`, 2076 `_01`, 2422 `_01`, 2587 `_01`, 2610 `_01`, 2627 `_01`, 2686 `_01`, 2745 `_01`
- 대조: 1653 `_01`, 2432 `_01`, 2628 `_01`, 2733 `_01`

### 12.3 재현 명령

프롬프트 수와 ID 범위:

```bash
jq '{posts:length, min_id:(map(.id)|min), max_id:(map(.id)|max), nonempty_prompts:(map(select((.prompt // "")|length>0))|length), images:(map(.images|length)|add)}' generated/reactorprompt-export-20260902-incremental/manifest.json
```

기준 리비전 후보 수와 facet:

```bash
git show 8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab:skills/photo-prompt-image-generator/assets/photo_prompt_tags.json \
  | jq '{slot_counts:(.slots|map_values(length)), place_type:.facet_vocab.place_type, placement:.facet_vocab.placement, weather:.facet_vocab.weather, weather_effect:.facet_vocab.weather_effect}'
```

자연환경 확장 수:

```bash
git show 8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab:skills/photo-prompt-image-generator/assets/photo_prompt_natural_environment_extension.json \
  | jq '{slot_counts:(.slots|with_entries(.value |= length)), total:([.slots[][]]|length), auto_optional_policy}'
```

정규식 감사에서 사용한 핵심 협소 토큰은 `foreground`, `midground|middle-distance`, `background|backdrop`, `occlusion`, `linear perspective`, `relative scale`, `texture gradient`, `aerial|atmospheric perspective`, `shallow|deep focus|bokeh`, 날씨 방향 표현, 젖음·응결·웅덩이·유출 표현이다. 넓은 의미군은 이 토큰에 장소·장면·입자·날씨 동의어를 추가했고, 절 단위 부정어를 별도 집계했다.

### 12.4 외부 출처

- [WMO International Cloud Atlas — Fog compared with Mist](https://cloudatlas.wmo.int/fog-compared-with-mist.html): 알려진 시정 거리 없이 fog/mist를 과도하게 판정하지 않는 경계
- [WMO International Cloud Atlas — Hydrometeors](https://cloudatlas.wmo.int/en/general-classification-of-meteors-hydrometeors.html): 부유·낙하·비산·퇴적 과정 분리
- [WMO International Cloud Atlas — Luminance and haze](https://cloudatlas.wmo.int/en/appearance-of-clouds-luminance.html): 대기 입자가 거리 구조의 대비·질감 판독에 미치는 영향
- [Stereoscopy and the Human Visual System](https://pmc.ncbi.nlm.nih.gov/articles/PMC3490636/): 가림, 상대 크기, 선원근, 질감 구배, 대기 원근, 흐림 등 그림 깊이 단서와 충돌 가능성

### 12.5 한계

- 픽셀 표본은 47개 고유 파일로 4,908개 전체를 대표하지 않는다.
- 썸네일 47개 중 네이티브 확인은 16개다. 미세 입자·재질 판정은 네이티브 확인 사례에 한정했다.
- 정규식은 선언을 찾았을 뿐 문법적 의미, 텍스트-이미지 결합, 생성 성공을 자동 검증하지 않는다.
- 코퍼스는 영상 프롬프트, 캡션/설명문, 이미지 결합이 섞여 있어 정지 이미지 한 장과 직접 비교할 수 없는 행이 있다.
- 이 보고서는 후보/프로필을 설계했지만 구현하지 않았고, 새 후보를 생성 이미지로 검증하지 않았다.
