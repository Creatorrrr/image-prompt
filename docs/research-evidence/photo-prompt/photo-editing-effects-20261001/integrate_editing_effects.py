#!/usr/bin/env python3
"""Reviewed editing-effect source authoring. Research provenance stays external.

Rows below are authored observable projections, not vendor recipes or empirical
frequency estimates. Re-running writes the same extension and maintenance data.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
MAINTENANCE = ROOT / "docs/research-evidence/photo-prompt/extension-maintenance"


def read(name):
    return json.loads((OUT / name).read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


# group | slot | ID suffix | Korean label | English label | simultaneous units.
# The final field deliberately keeps complete phrases, rather than bags of words.
SPEC = """
01|quality|natural_detail|자연스럽게 남은 피부·사물 세부|natural photographic surface detail with restrained processing|fine subject surface detail remains readable;tonal transitions remain gentle
01|quality|clean_edges|깔끔하고 연속적인 사진 경계|clean continuous photographic edges|object contours remain continuous;small surface details remain readable
04|color_grading|cool_shadow_warm_skin|차가운 배경 암부와 따뜻한 피부 계조|cool background shadows with restrained warm skin tones|background shadow regions carry a cool tint;skin midtones retain restrained warmth
05|quality|painterly_photo_finish|사진 구조를 유지하는 회화적 세부 단순화|painterly photographic finish with simplified fine detail|fine image detail is simplified into soft tonal masses;subject geometry and photographic light remain legible
06|color_grading|airy_tones|열린 암부와 밝은 공기감|bright airy image tones with open shadows|shadow image regions remain luminous and readable;bright regions retain gradual tonal transitions
06|color_grading|moody_density|국부 밝은 부분과 짙은 암부|dark moody tonal density with selective bright regions|most image regions sit in deep shadow tones;a small lit region remains visibly separated
07|color_grading|muted_chroma|명암 형태를 유지한 절제된 색|restrained image chroma with readable tonal structure|image colors have visibly reduced chroma;light-dark structure remains readable
07|color_grading|faded_black_floor|올라간 암부와 약해진 색|faded image tones with lifted blacks and reduced chroma|dark image tones stop above dense black;image colors remain restrained rather than fully achromatic
07|color_grading|washed_tones|옅은 색과 줄어든 명암 간격|washed-out image tones with pale color and compressed contrast|image colors look pale;bright and dark image tones have a reduced separation
08|quality|coarse_lofi_detail|거친 저해상도형 사진 세부|coarse low-fidelity photographic detail|small image details look coarse;large subject contours remain recognizable
08|quality|polished_specular_detail|정돈된 사진 세부와 분명한 반사 하이라이트|polished photographic detail with crisp specular accents|subject surface details remain clean and legible;small reflected highlights remain distinct
09|color_grading|expanded_tonal_separation|밝고 어두운 영역의 넓은 계조 간격|expanded light-dark tonal separation|bright image regions stand well above dark regions;intermediate subject tones remain continuous
09|color_grading|compressed_tonal_separation|계조를 남기는 낮은 명암 분리|compressed light-dark tonal separation with retained detail|bright and dark regions have a reduced brightness difference;subject surface detail remains visible
10|color_grading|open_shadow_detail|암부의 읽히는 세부|readable detail within dark image regions|shadow regions retain visible surface variation;shadow regions remain darker than lit regions
10|color_grading|contained_white_detail|밝은 영역의 남은 형태와 세부|contained bright image tones with retained surface detail|bright subject regions retain shape and texture;small specular points may remain brighter than diffuse whites
11|color_grading|s_shaped_separation|끝 계조를 유지한 중간톤 대비|strong midtone separation with gentler tonal endpoints|midtone brightness differences are pronounced;dark and bright endpoint transitions remain gradual
13|color_grading|high_key_tones|어두운 기준을 조금 남긴 하이키 계조|high-key image tones with a small dark reference|most image regions are bright;a small darker contour or feature preserves readable form
13|lighting|low_key_island|어두운 장면의 국부 조명|selective illumination within a predominantly dark scene|one bounded subject region receives visible light;the surrounding scene remains substantially darker
14|color_grading|lifted_black_floor|세부를 남긴 올라간 검정 바닥|lifted black floor with readable dark image tones|dark image tones are lifted to visible gray;dark subject information remains readable
14|color_grading|crushed_black_regions|일부 암부가 검정 덩어리로 닫힌 계조|selected dark image regions collapse into dense black|selected shadow regions lose internal tonal variation;lit subject regions remain readable
15|color_grading|gentle_rolloff|밝은 계조의 점진적 전이|gradual bright tonal transition into highlights|bright image tones approach white gradually;highlight form remains readable without requiring a spatial halo
15|color_grading|compressed_highlight_range|밝은 영역 간격을 압축한 계조|compressed highlight brightness range with retained shape|bright tonal differences are reduced;highlight surfaces remain distinguishable from each other
16|color_grading|neutral_balance|중립 물체가 중립적으로 보이는 색 균형|neutral object colors under balanced image color|a declared neutral surface remains near neutral;other object colors remain distinguishable
16|color_grading|warm_cast|영상 전체의 따뜻한 색 기운|warm image-wide color cast|neutral image regions carry a warm tint;subject color differences remain readable
16|color_grading|cool_cast|영상 전체의 차가운 색 기운|cool image-wide color cast|neutral image regions carry a cool tint;subject color differences remain readable
16|color_grading|green_cast|영상 중립 영역의 녹색 기운|green tint in nominally neutral image regions|nominally neutral regions carry a green tint;light-dark structure remains intact
16|color_grading|magenta_cast|영상 중립 영역의 자홍색 기운|magenta tint in nominally neutral image regions|nominally neutral regions carry a magenta tint;light-dark structure remains intact
17|color_grading|restrained_red_family|붉은 물체의 절제된 채도|restrained saturation in the red object color family|red object regions have visibly restrained saturation;non-red color regions remain distinguishable
17|color_grading|bright_blue_family|푸른 물체의 밝은 계조|brighter tonal values within blue object regions|blue object regions appear relatively luminous;the blue family remains visibly distinct from neutral regions
19|color_grading|warm_highlight_cool_shadow|따뜻한 밝은 부분과 차가운 암부|warm highlight tint and cool shadow tint in separate tonal regions|bright tonal regions carry a warm tint;shadow tonal regions carry a cool tint
19|color_grading|teal_shadow_orange_midtones|청록 암부와 주황 중간톤|teal shadow tint with restrained orange midtones|shadow tonal regions carry a teal tint;selected midtones carry a restrained orange tint
20|color|pastel_palette|밝고 약한 파스텔 물체 색|light low-chroma pastel object palette|major object colors are pale and low in chroma;different object color families remain distinguishable
20|color|earth_palette|흙빛 물체와 배경 색 조합|earth-toned object and background palette|major objects use brown ochre or muted green colors;tonal structure separates adjacent surfaces
21|color_grading|achromatic_tones|색상 없이 읽히는 흑백 계조|achromatic image with readable gray tonal differences|the picture contains gray tonal variation;object color hue is absent from the picture area
21|color_grading|sepia_tones|갈색 계열로 제한된 계조|brown sepia tonal image|the picture uses a restrained brown tonal family;subject form is preserved by brightness differences
22|color|cobalt_cream_mapping|코발트·크림의 두 색 계조 매핑|cobalt-to-cream two-color tonal mapping|dark image tones map to cobalt;bright image tones map to cream
22|color|burgundy_peach_mapping|버건디·복숭아색 계조 매핑|burgundy-to-peach tonal color mapping|dark image tones map to burgundy;bright image tones map to pale peach
23|color_grading|red_object_splash|지정한 붉은 물체만 남긴 색|selected red object remains colored in an otherwise achromatic image|one declared red object retains its red color;the rest of the picture is achromatic
24|lighting|soft_shadow_edges|넓은 전이를 갖는 부드러운 그림자|soft illumination with broad shadow-edge transitions|cast shadow boundaries have broad gradual transitions;the lit subject remains in readable focus
24|lighting|hard_shadow_edges|짧고 분명한 그림자 전이|hard illumination with short sharp shadow-edge transitions|cast shadow boundaries have short sharp transitions;shadow direction agrees with the declared source position
25|lighting|frontal_flash_falloff|정면 플래시와 어두워지는 배경|near-axis direct flash with darker distant background|the near subject receives frontal flash illumination;distant background regions receive substantially less flash light
25|lighting|ceiling_bounce|천장 쪽 넓은 반사광|broad ceiling-bounced illumination|upper-facing subject surfaces receive broad illumination;shadow transitions are softer than a small direct flash source
26|light_direction|rear_rim|뒤쪽 광원의 경계 림|rear light outlining selected subject contours|a declared rear source lights selected subject edges;front-facing surfaces remain comparatively darker
26|light_direction|side_modeling|옆 광원의 밝고 어두운 면|side light separating lit and shadow-facing surfaces|one side of the subject receives stronger illumination;the opposite side carries coherent shadow
26|light_direction|top_modeling|상부 광원의 아래 방향 그림자|overhead light with downward cast shadows|upper-facing surfaces are illuminated;cast shadows extend downward from raised forms
26|light_direction|under_modeling|하부 광원의 위 방향 그림자|low light with upward cast shadows|lower-facing surfaces receive stronger illumination;cast shadows extend upward from raised forms
27|lighting|cheek_triangle|그림자 볼에 남는 작은 삼각광|small lit triangle on the shadow-side cheek|one cheek is predominantly shadowed;a small bounded light triangle remains beneath its eye
27|lighting|silhouette_outline|밝은 배경 앞의 어두운 윤곽|dark subject silhouette against a bright background|subject interior is predominantly dark;subject outline is legible against the brighter background
28|quality|local_bloom|밝은 영역 주위의 국부 블룸|localized luminous bloom around bright image regions|luminous spread extends just beyond bright source edges;darker non-highlight subject detail remains readable
28|quality|soft_glow_layer|사진 세부 위의 부드러운 밝은 광막|soft luminous image glow over readable detail|a soft luminous layer occupies the image plane;some underlying subject detail remains readable
29|film_emulation|red_edge_halation|밝고 어두운 경계의 적주황 필름형 번짐|film-like red-orange halo confined to bright contrast edges|red-orange halo hugs bright-dark image boundaries;unrelated dark edges remain free of the colored halo
30|lens_artifact|veiling_flare|광원 쪽 영상의 베일형 대비 감소|light-facing veiling flare contrast loss|a luminous veil reduces contrast toward the declared light source;the veil has no required discrete polygonal ghost
30|lens_artifact|aligned_ghosts|광원과 정렬된 분리형 플레어 고스트|discrete optical flare ghosts aligned with a bright source|separate optical ghost shapes align with the bright source;the shapes overlay the scene rather than occupy it as objects
31|film_emulation|edge_light_leak|장면 광원과 독립된 가장자리 빛샘|irregular warm light-leak patch entering the picture edge|an irregular warm patch enters the picture edge;the patch overlays scene detail without requiring a scene lamp at its origin
32|lens_artifact|point_starburst|점광원 중심의 다방향 별빛 선|starburst rays centered on a small bright point light|multiple thin rays meet at the bright point light;rays remain image-plane optical marks
32|lens_artifact|horizontal_anamorphic_streak|밝은 광원 중심의 긴 수평 플레어|long horizontal optical flare streak through a bright source|a thin luminous streak passes horizontally through a bright source;unrelated scene lines remain ordinary objects
33|lens_artifact|dark_periphery|영상 가장자리의 점진적 어두움|gradual darkening toward the picture periphery|outer image regions become progressively darker;central subject information remains legible
34|lens_artifact|edge_color_fringe|고대비 경계에 붙은 얇은 색 테두리|thin chromatic fringes along high-contrast image edges|thin differently colored fringes hug high-contrast boundaries;large interior object regions retain their own colors
35|quality|neutral_diffusion|세부를 남긴 색중립 하이라이트 확산|neutral-colored optical-diffusion-like highlight spread|bright edges spread into a neutral-colored soft halo;selected subject details remain recognizable through the softening
36|focus|shallow_falloff|선명한 대상과 깊이에 따른 흐림|selected subject sharpness with depth-dependent focus falloff|the selected subject plane is visibly sharp;nearer or farther regions become gradually defocused
36|focus|deep_readability|근경부터 원경까지 읽히는 세부|readable near-to-far scene detail|near subject details remain legible;far scene details remain legible
37|focus|background_bokeh|초점 밖 배경의 부드러운 광원 원반|soft out-of-focus background light discs|small background lights form soft discs;the selected subject plane remains sharper than those discs
37|focus|soft_focus_core|광막 속에서 읽히는 부드러운 초점|soft-focus photographic detail under a mild luminous veil|fine subject edges are softly spread;larger facial or object forms remain recognizable
38|quality|uniform_image_blur|깊이와 독립된 균일한 영상 흐림|depth-independent soft image-plane blur|fine image edges are evenly softened;softness does not track scene distance from a focus plane
39|focus|miniature_focus_band|좁은 띠 선명도와 점진적 주변 흐림|miniature-like narrow focus band across a distant scene|one narrow scene band remains sharp;regions above and below the band become progressively defocused
40|quality|orton_overlap|선명한 세부와 넓은 연성 광막의 중첩|Orton-like sharp detail beneath broad soft luminosity|fine subject detail remains sharp in selected regions;broad soft luminous masses overlay that detail
41|motion|moving_subject_streak|움직이는 대상의 방향성 흔적|directional moving-subject image streak|the moving subject leaves a continuous directional trace;stationary scene anchors remain comparatively stable
41|motion|light_trails|움직이는 광원의 연속된 궤적|continuous light trails from moving luminous sources|a moving luminous source leaves a continuous path;stationary objects remain distinguishable from that path
42|motion|tracked_subject_background_trace|읽히는 추적 대상과 방향성 배경|tracked moving subject against directional background streaks|the tracked moving subject remains recognizable;background streaks follow a coherent tracking direction
43|motion|camera_sweep|장면 여러 물체의 같은 방향 흔들림|intentional camera sweep across stationary scene forms|multiple stationary scene edges share a coherent sweep direction;their traces lie on the image plane
43|motion|radial_zoom|중심에서 바깥으로 뻗는 줌 흔적|radial zoom streaks extending from an image center|image streaks radiate from a shared center;central subject form remains more readable than outer traces
43|motion|rotation_arc|공통 중심을 도는 회전 흔적|curved image traces around a common rotation center|multiple scene edges form curved arcs;the arcs share a common image rotation center
44|motion|flash_core_shutter_trace|읽히는 플래시 핵과 주변광 흔적|readable flash-lit subject core with ambient slow-shutter traces|the flash-lit subject core remains recognizable;ambient moving lights leave visible elongated traces
45|film_emulation|scan_picture_area|종이 테두리 없이 읽히는 필름 스캔형 영상|film-scan-like picture area with soft tonal transitions|the picture area has soft tonal transitions;fine image-plane grain remains visible within tones
46|film_emulation|instant_picture_area|순간 필름형 사진 영역의 제한된 계조|instant-film-inspired picture area with restrained tonal range|the picture area has restrained tonal separation;color transitions remain soft within the picture area
46|film_emulation|disposable_picture_area|단순 정면광과 거친 일회용 카메라형 영상|disposable-camera-inspired frontal flash and coarse picture grain|near objects show simple frontal flash illumination;coarse image-plane grain overlays the picture area
47|camera_type|compact_flash_noisy_finish|직접 플래시·노이즈의 소형 디지털형 영상|compact-digital-style direct flash and noisy shadow finish|near subjects receive direct frontal flash;dark image regions carry digital noise
48|color_grading|cross_process_cast|중립색 이탈과 강한 공정 모사 색|cross-process-inspired nonneutral color and contrast|neutral object regions carry a conspicuous color cast;tonal separation remains pronounced
49|color_grading|bleach_bypass_tones|색을 줄이고 암부 밀도를 높인 룩|bleach-bypass-inspired reduced chroma and dense shadows|image chroma is visibly reduced;dark image tones remain dense and strongly separated
50|quality|readable_microdetail|과한 링 없이 읽히는 미세 세부|readable fine image detail without exaggerated edge halos|fine subject surface details remain readable;high-contrast contours avoid broad artificial rings
51|quality|local_midcontrast|중간톤 이웃 영역의 분명한 세부|pronounced local midtone detail separation|neighboring midtone details show visible brightness separation;global bright and dark regions remain coherent
52|quality|fabric_detail|영상에서 읽히는 직물의 미세 세부|readable fine fabric detail within the photograph|fine woven or knitted fabric details are legible;fabric contours and folds remain continuous
53|quality|reduced_veil|원경 형태를 남긴 옅은 베일|reduced atmospheric veil with readable distant contours|distant scene contours remain distinguishable;a slight depth-related atmospheric veil remains visible
54|quality|sharpening_edge_halo|고대비 경계의 밝고 어두운 선명화 링|paired bright and dark sharpening-like edge halos|bright and dark narrow bands straddle high-contrast edges;the bands are image artifacts rather than emitted light
55|grain_profile|fine_midtonal_grain|중간톤의 미세한 필름형 입자|fine film-like image-plane grain in midtones|fine irregular image-plane grain is visible in midtones;subject material details remain distinct from the grain
55|grain_profile|coarse_film_grain|영상면의 굵은 필름형 입자|coarse irregular film-like image-plane grain|coarse irregular grain overlays the picture area;the grain does not become physical object damage
56|grain_profile|digital_luma_noise|암부의 밝기 성분 노이즈|brightness-only digital noise in dark image regions|dark image regions contain irregular brightness speckle;speckle remains an image-plane artifact
56|grain_profile|digital_chroma_noise|암부의 색 성분 노이즈|colored digital noise speckles in dark image regions|small colored speckles appear within dark image regions;speckles remain separate from large object colors
56|quality|denoised_detail|노이즈가 절제되고 남은 세부|restrained image noise with retained fine subject detail|smooth image regions show little irregular speckle;fine subject surface details remain readable
57|film_emulation|scan_dust_specks|스캔 영상면의 불규칙 먼지 점|irregular dust-like marks on the scanned picture plane|small irregular marks overlay the picture area;the marks remain separate from dust on depicted objects
57|film_emulation|scan_scratches|스캔 영상면의 길고 얇은 긁힘|long thin scratch-like marks on the scanned picture plane|long thin marks traverse picture tones;marks overlay the image rather than cut depicted object surfaces
58|quality|jpeg_edge_blocks|고대비 영상 경계의 JPEG형 블록|JPEG-like block artifacts near high-contrast image edges|small block-pattern artifacts cluster around contrast boundaries;the blocks remain image marks rather than scene objects
58|quality|gradient_banding|부드러운 계조 영역의 띠 경계|visible tonal bands within an otherwise smooth image gradient|a smooth image gradient breaks into discrete tonal bands;band boundaries remain separate from object contours
58|quality|moire_on_pattern|촘촘한 반복 무늬에 겹친 간섭 물결|moire-like interference across a fine repeated surface pattern|a fine repeated pattern carries larger wavy interference bands;interference remains localized to the patterned region
60|quality|local_form_tones|대상 형태를 따라 나뉜 국부 명암|local light-dark shaping along subject form|selected raised surfaces carry gently brighter tones;adjacent recesses carry gently deeper tones
62|skin_finish|texture_preserving_tone_evening|미세 피부결을 남긴 국부 톤 정리|local skin-tone evening with readable fine skin texture|skin color transitions remain locally even;fine skin texture remains visible without facial-geometry alteration
62|skin_finish|mild_skin_softening|국부 피부 세부의 약한 연성 처리|mild local skin-detail softening with retained contours|very fine skin detail is mildly softened;larger facial contours remain unchanged and readable
64|composition|level_horizon|정돈된 수평 기준선|level scene horizon within the photograph|a declared horizontal scene reference appears level;subject framing remains coherent around that reference
65|lens|parallel_verticals|수직 건축선이 나란한 투영|parallel architectural verticals within the image projection|declared vertical architectural lines remain parallel;subject geometry remains continuous beside those lines
65|lens|barrel_projection|중심 밖 직선의 바깥쪽 휨|outward bowing of off-center straight scene lines|off-center straight scene lines bow outward;central scene contours remain comparatively straight
65|lens|pincushion_projection|중심 밖 직선의 안쪽 휨|inward bowing of off-center straight scene lines|off-center straight scene lines bow inward;central scene contours remain comparatively straight
67|composition|integrated_composite|경계·그림자가 일관된 배경 결합|subject and destination scene with coherent composite boundaries|subject boundaries meet the background continuously;subject contact shadows agree with destination illumination
68|quality|double_exposure_overlap|읽히는 두 장면 영상의 중첩|two recognizable scene layers overlapping within one picture|one scene layer remains recognizable;a second scene layer visibly overlaps the first in the same picture area
69|color_grading|wide_tonal_detail|밝고 어두운 부분에 함께 남은 세부|readable bright and dark scene detail within one image|bright scene surfaces retain visible detail;dark scene surfaces retain visible detail without edge halos
70|focus|extended_near_far_focus|가까운 부분과 먼 부분의 연속 선명도|extended near-to-far subject detail with continuous geometry|near subject regions remain in readable focus;far subject regions remain in readable focus with continuous geometry
71|composition|continuous_wide_view|연결 경계가 연속적인 넓은 장면|continuous wide scene with aligned overlapping contours|scene contours remain continuous across the wide picture;repeated edges do not jump at internal boundaries
72|composition|photographic_fragments|경계가 드러나는 사진 조각 구성|photographic fragments with deliberate visible boundaries|multiple photographic fragments remain separately readable;their distinct boundaries remain visible in the composition
74|quality|posterized_tones|적은 계조 단계의 포스터화|few discrete tonal steps across the picture area|continuous surfaces reduce to a few flat tonal steps;subject outline remains recognizable
74|quality|binary_threshold|검정·흰색 두 값의 영상면|black-and-white binary threshold picture|picture regions use only black or white values;subject shape remains readable through binary boundaries
74|quality|negative_tones|명암 순서가 뒤집힌 네거티브형 영상|negative-like reversal of picture brightness relationships|normally bright reference surfaces appear dark;normally dark reference surfaces appear bright
74|quality|solarized_contours|일부 명암 역전 경계가 남은 영상|partial tonal reversal with visible solarized boundaries|selected tonal regions reverse brightness ordering;transition boundaries form visible contour bands
75|quality|halftone_picture_plane|영상면의 규칙적인 망점|regular halftone dots within the picture plane|regular dots form the picture tones;dot density or size varies with the depicted brightness
75|quality|photocopy_picture_plane|입자와 검정 덩어리의 복사형 영상|photocopy-like coarse marks and dense dark regions|coarse reproduction marks overlay picture tones;dark subject regions form dense black masses
75|quality|emboss_picture_plane|그림 내부 경계의 얕은 양각형 명암|shallow emboss-like light-dark edge pairs within the picture|image contours carry paired light and dark edges;the relief-like marks belong to the picture plane
75|quality|edge_outline_picture_plane|사진 경계를 선으로 단순화한 영상|contour outlines extracted across the picture plane|major picture contours appear as distinct lines;interior tonal masses are simplified
76|surface_material|watercolor_print|사진 속 종이에 그려진 수채 표현|watercolor washes on a depicted paper artifact|transparent color washes occupy the paper surface;paper boundaries and surrounding scene remain photographic
76|surface_material|charcoal_print|사진 속 종이의 목탄선|charcoal marks on a depicted paper artifact|dark powdery charcoal marks occupy the paper surface;the surrounding scene retains ordinary photographic detail
76|surface_material|pencil_print|사진 속 종이의 연필선|pencil linework on a depicted paper artifact|fine graphite-like linework occupies the paper surface;paper boundaries remain visible within the photograph
76|surface_material|torn_paper_edge|사진 속 인쇄물의 찢어진 경계|torn edge of a depicted photographic paper artifact|irregular fibers remain visible along the paper edge;the tear belongs to the paper rather than the image frame
77|quality|rgb_split_picture_plane|영상 경계의 RGB 채널 어긋남|offset red green and blue image-channel contours|high-contrast picture contours split into offset color channels;the offsets remain image marks rather than extra scene objects
77|quality|scanline_picture_plane|영상면을 가로지르는 반복 주사선|repeated horizontal scan lines across the picture plane|fine horizontal lines repeat across picture tones;subject contours remain recognizable underneath
77|quality|pixelated_picture_plane|영상면의 굵은 사각 샘플|coarse square sampling across the picture plane|picture tones are grouped into visible square cells;large subject shape remains readable across those cells
77|quality|displaced_picture_strip|어긋난 영상 조각의 변위|displaced picture strips with broken image continuity|selected image strips shift relative to neighboring strips;the discontinuity belongs to reproduction rather than body anatomy
77|quality|vhs_picture_plane|영상면의 수평 노이즈와 색 번짐|VHS-inspired horizontal noise and picture color bleed|horizontal noise bands traverse the picture area;color spreads slightly across picture contours
78|surface_material|cyanotype_paper|종이 위 청색 감광형 인쇄물|Prussian-blue cyanotype-inspired image on depicted paper|blue image areas occupy a visible paper surface;pale image shapes retain readable paper-tone contrast
79|surface_material|silver_print_paper|종이 위 흑백 은염형 계조|gelatin-silver-inspired gray image on depicted paper|gray photographic tones occupy a visible paper surface;surface sheen and paper boundary remain legible
79|surface_material|platinum_print_paper|종이 위 섬세한 무광 흑백 계조|platinum-print-inspired matte tonal image on paper|a matte monochrome image occupies the paper surface;gentle midtone differences remain visible
79|surface_material|wet_plate_artifact|판면의 불균일한 감광형 계조|wet-plate-inspired uneven monochrome image on a depicted plate|a monochrome image occupies a visible plate surface;uneven edge coating remains confined to the plate
79|surface_material|daguerreotype_plate|반사 금속 판면의 흑백 영상|reflective metal plate carrying a monochrome photographic image|a monochrome image occupies a reflective metal surface;the plate boundary and reflection remain visible
79|surface_material|photogravure_paper|종이 위 잉크형 사진 계조|photogravure-inspired ink tones on depicted paper|ink-like tonal marks occupy a visible paper surface;fine printed tonal structure remains readable
80|surface_material|photogram_paper|종이 위 물체 접촉·반투명 실루엣|contact-shadow and translucent silhouettes on a light-sensitive paper artifact|object-contact silhouettes occupy a visible paper surface;opaque and translucent shapes have different tonal densities
80|surface_material|luminogram_paper|종이 위 빛의 경로형 추상 영상|abstract light-path image on a depicted paper artifact|continuous abstract light-path marks occupy the paper surface;the surrounding scene remains ordinary photography
84|lighting|coherent_relighting|그림자·반사와 일치하는 대상 조명|subject illumination coherent with cast shadows and reflections|subject shading agrees with the declared light direction;cast shadows and reflections agree with that same direction
"""

groups = {g["id"]: g for g in read("concept-proposals.json")["groups"]}
slots, by_suffix, provenance = {}, {}, []


def scope_for(slot, suffix):
    if suffix == "compact_flash_noisy_finish":
        return ["lighting", "style"], [
            {"dimension": "lighting", "target": "*", "property": "*"},
            {"dimension": "style", "target": "image_plane", "property": "rendering.noise"}]
    if slot in {"color", "color_grading"}:
        # Changing a rendered global palette can change any protected color.
        return ["color"], [{"dimension": "color", "target": "*", "property": "*"}]
    if slot == "skin_finish":
        dimensions = ["appearance"]
        effects = [{"dimension": "appearance", "target": "main_subject", "property": "skin.texture"}]
        if suffix == "texture_preserving_tone_evening":
            dimensions.append("color")
            effects.append({"dimension": "color", "target": "main_subject", "property": "skin.color"})
        return dimensions, effects
    if slot == "surface_material":
        return ["material"], [{"dimension": "material", "target": "depicted_artifact", "property": "surface.finish"}]
    if slot in {"lighting", "light_direction"}:
        return ["lighting"], [{"dimension": "lighting", "target": "*", "property": "*"}]
    if slot == "composition":
        return ["composition"], [{"dimension": "composition", "target": "image_plane", "property": "layout"}]
    if slot in {"camera_type", "motion", "focus", "lens", "lens_artifact"}:
        if suffix == "flash_core_shutter_trace":
            return ["camera", "lighting"], [
                {"dimension": "camera", "target": "image_plane", "property": "optical.motion"},
                {"dimension": "lighting", "target": "*", "property": "*"}]
        return ["camera"], [{"dimension": "camera", "target": "image_plane", "property": "optical." + slot}]
    dimensions = ["style"]
    effects = [{"dimension": "style", "target": "image_plane", "property": "rendering." + slot}]
    if suffix in {"digital_chroma_noise", "red_edge_halation", "edge_light_leak", "rgb_split_picture_plane", "vhs_picture_plane",
                  "scan_picture_area", "instant_picture_area", "posterized_tones", "binary_threshold", "negative_tones",
                  "solarized_contours", "halftone_picture_plane", "photocopy_picture_plane", "gradient_banding"}:
        dimensions.append("color")
        effects.append({"dimension": "color", "target": "*", "property": "*"})
    if suffix == "disposable_picture_area":
        dimensions.append("lighting")
        effects.append({"dimension": "lighting", "target": "*", "property": "*"})
    if suffix == "double_exposure_overlap":
        dimensions.append("composition")
        effects.append({"dimension": "composition", "target": "image_plane", "property": "layout"})
    return dimensions, effects


for line in SPEC.strip().splitlines():
    number, slot, suffix, ko, en, units_text = line.split("|")
    group_id = "edit_" + number
    units = units_text.split(";")
    dimensions, effects = scope_for(slot, suffix)
    entry = {"id": "pe_" + suffix, "ko": ko, "en": en, "weight": 0.72,
             "core_assertion_discovery": True,
             "aliases": [ko, en], "keywords": [en], "concept_units": units,
             "affected_dimensions": dimensions, "affected_properties": effects,
             "embedding_text": en + "; " + "; ".join(units),
             "relations": [{"id": "effect_owner", "type": "applies_to",
                            "subject": en, "object": groups[group_id]["owner_scope"]}]}
    slots.setdefault(slot, []).append(entry)
    by_suffix[suffix] = (slot, entry)
    provenance.append({"candidate_id": f"slot:{slot}:pe_{suffix}", "proposal_group_id": group_id,
                       "owner_scope": groups[group_id]["owner_scope"], "source_ids": groups[group_id]["source_ids"],
                       "claim_limit": groups[group_id]["confusion_boundary"],
                       "weight_status": "authored_neutral_not_frequency_or_quality_estimate",
                       "native_pixel_status": "not_qualified_by_data_or_schema_checks"})

# This is the same compound effect described in ordinary photographic words;
# it does not create a hardware claim or route a particular test/keyword ID.
by_suffix["flash_core_shutter_trace"][1]["paraphrases"] = [
    "a sharp flash-lit subject with a continuous moving-light exposure trail"
]

supplement = read("source-supplement.json")
for source in supplement["sources"]:
    for suffix in source["candidate_suffixes"]:
        for row in provenance:
            if row["candidate_id"].endswith(":pe_" + suffix):
                row["source_ids"] = [*row["source_ids"], source["id"]]

# Profile source components are the single owner for discovery, literal evidence,
# composition instruction and all-of native pixel gates. Labels are qualified.
PROFILE_SPECS = [
    ("local_bloom", "localized highlight bloom relation", "국부 하이라이트 블룸 관계", "both"),
    ("fine_midtonal_grain", "fine image-plane film grain", "영상면 미세 필름 입자", "native"),
    ("coarse_film_grain", "coarse image-plane film grain", "영상면 굵은 필름 입자", "native"),
    ("digital_luma_noise", "dark-region digital luminance noise", "암부 디지털 밝기 노이즈", "native"),
    ("digital_chroma_noise", "dark-region digital chroma noise", "암부 디지털 색 노이즈", "native"),
    ("jpeg_edge_blocks", "image-edge JPEG-like block artifact relation", "영상 경계 JPEG형 블록 관계", "native"),
    ("gradient_banding", "smooth-gradient tonal banding relation", "매끈한 계조의 밴딩 관계", "native"),
    ("moire_on_pattern", "repeated-pattern moire interference relation", "반복 무늬 모아레 간섭 관계", "native"),
    ("texture_preserving_tone_evening", "texture-preserving local skin-tone evening", "피부결 보존 국부 피부 톤 정리", "native"),
    ("red_object_splash", "selected red object color-splash relation", "선택한 붉은 물체 컬러 스플래시 관계", "both"),
    ("lifted_black_floor", "readable lifted-black tonal floor", "세부를 남긴 상승 검정 계조", "both"),
    ("crushed_black_regions", "selected-region crushed-black tonal floor", "선택 영역 닫힌 검정 계조", "both"),
    ("orton_overlap", "sharp-detail soft-luminosity Orton relation", "선명 세부와 연성 광막 오르톤 관계", "both"),
    ("edge_light_leak", "picture-edge independent light-leak relation", "영상 경계 독립 빛샘 관계", "both"),
    ("sharpening_edge_halo", "image-edge sharpening halo relation", "영상 경계 선명화 링 관계", "native"),
    ("posterized_tones", "picture-plane posterized tonal steps", "영상면 포스터화 계조 단계", "both"),
    ("binary_threshold", "picture-plane binary threshold relation", "영상면 이진 임계 계조 관계", "both"),
    ("rgb_split_picture_plane", "picture-plane offset RGB channel contours", "영상면 RGB 채널 경계 어긋남", "native"),
    ("halftone_picture_plane", "picture-plane halftone dot-density relation", "영상면 망점 밀도 관계", "native"),
    ("compact_flash_noisy_finish", "compact-digital frontal-flash noisy-shadow relation", "소형 디지털 정면 플래시와 암부 노이즈 관계", "both"),
    ("double_exposure_overlap", "recognizable two-scene exposure overlap relation", "읽히는 두 장면 노출 중첩 관계", "both"),
    ("scan_dust_specks", "scanned-picture-plane dust-mark relation", "스캔 영상면 먼지 흔적 관계", "native"),
]
profiles, profile_for_suffix = [], {}
for suffix, label, ko, scale in PROFILE_SPECS:
    slot, entry = by_suffix[suffix]
    profile_id = "pe_" + suffix + "_relation"
    profile_for_suffix[suffix] = profile_id
    units = entry["concept_units"]
    boundary = groups[next(p["proposal_group_id"] for p in provenance if p["candidate_id"].endswith(":" + entry["id"]))]["confusion_boundary"]
    components = []
    for i, unit in enumerate(units, 1):
        components.append({"id": f"component_{i}", "match_terms": [unit],
                           "evidence_field": f"component_{i}_phrase", "evidence_terms": [unit],
                           "min_content_words": 3,
                           "instruction": "Realize this visible property on its declared owner: " + unit,
                           "render_gate": {"id": f"vo_{profile_id}_{i}", "review_scale": scale,
                                           "description": unit + ". Inspect its declared owner in the native image; partial or substituted evidence fails."}})
    profiles.append({"id": profile_id, "category": "scoped_photographic_editing_effect",
                     "activation": {"exact_terms": [label, ko], "requires_adult_character": False,
                                    "semantic_discovery_requires_component_evidence": False},
                     "semantics": {"definition": "; ".join(units), "paraphrase_examples": [entry["en"], entry["ko"]],
                                   "visual_components": units, "contrast_examples": [boundary],
                                   "claim_limits": ["This is a depicted effect; it does not establish capture hardware, editing software, source layers or processing history.",
                                                    "Every component belongs to the declared owner and must pass independently; partial evidence fails.", boundary]},
                     "concept_candidate": {"concept_terms": [label, ko, *units],
                                           "core_assertion_discovery": True,
                                           "affected_dimensions": entry["affected_dimensions"],
                                           "affected_properties": entry["affected_properties"]},
                     "runtime_expression": {"default_mode": "definition_with_optional_label", "prompt_label_terms": [],
                                            "forbidden_prompt_terms": [], "runtime_forbidden_labels": []},
                     "reject_substitutes": [boundary],
                     "authored_components": {"contract_version": "photo-authored-visual-components/v1", "components": components}})

BUNDLE_SPECS = [
    ("film_edge_grain_rolloff", ["red_edge_halation", "fine_midtonal_grain", "gentle_rolloff"], ["film_halation_highlight_edge_relation", "highlight_rolloff_tone_response"]),
    ("bright_local_bloom", ["local_bloom", "airy_tones"], ["highlight_rolloff_tone_response"]),
    ("neutral_diffusion_skin", ["neutral_diffusion", "texture_preserving_tone_evening"], ["diffusion_filter_highlight_halation"]),
    ("digital_flash_trace", ["digital_luma_noise", "flash_core_shutter_trace", "jpeg_edge_blocks"], ["rear_curtain_flash_motion_trace"]),
    ("compact_direct_flash", ["compact_flash_noisy_finish", "digital_chroma_noise"], []),
    ("muted_grain_finish", ["muted_chroma", "fine_midtonal_grain"], []),
    ("faded_scan_finish", ["faded_black_floor", "scan_picture_area"], []),
    ("duotone_detail", ["cobalt_cream_mapping", "readable_microdetail"], ["cr_duotone", "cr_gradient_mapping"]),
    ("red_splash_detail", ["red_object_splash", "readable_microdetail"], []),
    ("tracked_flash_motion", ["tracked_subject_background_trace", "frontal_flash_falloff"], ["panning_subject_tracking_motion_relation"]),
    ("dark_rim_shape", ["rear_rim", "moody_density"], []),
    ("warm_luminous_skin", ["local_bloom", "warm_highlight_cool_shadow", "texture_preserving_tone_evening"], ["cr_split_toning"]),
    ("light_leak_grain", ["edge_light_leak", "coarse_film_grain"], []),
    ("dust_scan_detail", ["scan_dust_specks", "readable_microdetail"], []),
    ("depth_bokeh_skin", ["background_bokeh", "texture_preserving_tone_evening"], ["shallow_depth_focus_falloff_relation"]),
    ("extended_detail_view", ["extended_near_far_focus", "readable_microdetail"], ["focus_stacked_extended_depth_composite"]),
    ("wide_tone_detail", ["wide_tonal_detail", "readable_microdetail"], []),
    ("bleach_grain_finish", ["bleach_bypass_tones", "coarse_film_grain"], []),
    ("cross_process_grain", ["cross_process_cast", "fine_midtonal_grain"], []),
    ("frontal_lofi_snapshot", ["frontal_flash_falloff", "coarse_lofi_detail"], []),
    ("soft_shadow_sharp_detail", ["soft_shadow_edges", "readable_microdetail"], ["soft_light_shadow_edge_relation"]),
    ("hard_shadow_dark_floor", ["hard_shadow_edges", "crushed_black_regions"], ["hard_light_shadow_edge_relation"]),
    ("luma_noise_muted_palette", ["digital_luma_noise", "muted_chroma"], []),
    ("orton_midtonal_grain", ["orton_overlap", "fine_midtonal_grain"], []),
    ("vignette_sharp_plane", ["dark_periphery", "shallow_falloff"], []),
    ("cyanotype_artifact_detail", ["cyanotype_paper", "readable_microdetail"], ["cyanotype_contact_print_prussian_blue_relation"]),
    ("torn_artifact_fragments", ["torn_paper_edge", "photographic_fragments"], []),
    ("parallel_scene_deep_focus", ["parallel_verticals", "deep_readability"], []),
]
bundles = []
for suffix, member_suffixes, existing_profiles in BUNDLE_SPECS:
    members = [by_suffix[s] for s in member_suffixes]
    assert len({slot for slot, _ in members}) == len(members), suffix
    associated = list(dict.fromkeys([*existing_profiles, *(profile_for_suffix[s] for s in member_suffixes if s in profile_for_suffix)]))
    units = [unit for _, entry in members for unit in entry["concept_units"]]
    bundles.append({"id": "pe_bundle_" + suffix, "primary_visual_proposition": "; ".join(entry["en"] for _, entry in members),
                    "candidate_only": True, "candidate_ids": [entry["id"] for _, entry in members],
                    "candidate_slots": {entry["id"]: slot for slot, entry in members},
                    "component_groups": [{"id": f"component_{i}", "visible_evidence": [unit]} for i, unit in enumerate(units, 1)],
                    "hard_profile_ids": associated, "source_keywords": [entry["en"] for _, entry in members],
                    "confusion_boundaries": ["This optional combination preserves each component's spatial owner; its associated profiles require separate activation.",
                                             "A style label or processing name alone does not establish these observable components."],
                    "relations": []})

by_group = {gid: [row["candidate_id"] for row in provenance if row["proposal_group_id"] == gid] for gid in groups}
workflow_groups = {12, 59, 61, 63, 66, 73, 81, 82, 83, 85, 86, 87, 88}
purpose_groups = {2, 3}
dispositions = []
for row in read("keyword-matrix.json")["rows"]:
    group = groups[row["proposal_group_id"]]
    number = int(group["id"].split("_")[1])
    route = ("workflow_or_operator_metadata_no_automatic_visual_projection" if number in workflow_groups else
             "photographic_purpose_or_approach_requires_authored_scene" if number in purpose_groups else
             "scoped_optional_observable_projection")
    dispositions.append({"reference_row": row["reference_row"], "label": row["label"], "proposal_group_id": group["id"],
                         "route": route, "owner_scope": group["owner_scope"], "source_ids": group["source_ids"],
                         "candidate_ids": by_group[group["id"]], "reuse_profile_ids": group["reuse_profile_ids"],
                         "mapping_scope": "group-level reviewed projections; members are alternatives, never a mandatory recipe for every keyword",
                         "workflow_contract": ("Supply source, selected target, desired result and output/workflow metadata separately; pixels cannot prove the operation." if number in workflow_groups else None),
                         "native_pixel_qualification": "pending_selected_test_arms; not implied by catalog inclusion"})
record = {"schema_version": "photo-editing-effect-maintenance/v1", "maintenance_only": True,
          "record_id": "photo-editing-effects-20261001-v2", "research_directory": str(OUT.relative_to(ROOT)),
          "source_ledger_sha256": digest(read("source-ledger.json")), "source_count": len(read("source-ledger.json")["sources"]),
          "source_supplement_sha256": digest(supplement), "supplement_source_count": len(supplement["sources"]),
          "candidates": provenance, "keyword_dispositions": dispositions,
          "new_profile_ids": [p["id"] for p in profiles], "new_bundle_ids": [b["id"] for b in bundles],
          "judgment_boundary": "Data/schema/retrieval success does not qualify generated pixels or requester acceptance.",
          "discovery_revision": "v2 permits bounded per-frozen-assertion discovery on source-opted-in candidates and profiles; all matches remain optional and respect authored dimensions and property locks.",
          "legacy_migration": "Existing compound IDs preserve their original meaning; declare image-plane ownership and add separate optional atomic entries.",
          "operator_boundary": "Numeric sliders, RAW, ICC, LUT, layer state and editing history are not inferred from a rendered photograph."}
save(MAINTENANCE / (record["record_id"] + ".json"), record)
save(ASSETS / "photo_prompt_editing_effects_extension.json", {
    "schema_version": "photo-prompt-research-extension/v1", "auto_optional_policy": "authored_filters_only",
    "maintenance_ref": {"contract_version": "photo-extension-maintenance-ref/v1", "record_id": record["record_id"], "sha256": digest(record)},
    "slots": slots, "visual_semantics": bundles})
save(ASSETS / "photo_prompt_visual_obligations_editing_effects.json", {
    "schema_version": "photo-visual-obligation-registry-extension/v1", "relation_contract_version": "photo-visual-relation/v1",
    "description": "Owner-scoped visible editing-effect projections; processing history and hardware are not pixel claims.", "profiles": profiles})
save(OUT / "implementation-disposition-ledger.json", {"schema_version": "photo-editing-implementation-disposition/v1",
     "reference_rows": len(dispositions), "proposal_groups": len(groups), "candidates_added": len(provenance),
     "bundles_added": len(bundles), "profiles_added": len(profiles), "rows": dispositions})
print(json.dumps({"candidates": len(provenance), "bundles": len(bundles), "profiles": len(profiles), "rows": len(dispositions)}))
