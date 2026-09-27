"""Write a prospective evaluation population. No tests or renders run here."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

TEXT_CASES = [
    ("bare_y2k", "Y2K 느낌의 성인 인물", "keep family advisory; no mandatory low rise, thin brows, pink, flash or device"),
    ("historical_1999", "1999년 일상 사진을 고증해줘", "exclude original iPod, nano, Razr and original Sidekick; do not ban all digital cameras"),
    ("ipod_early_2001", "2001년 2월 소매점에서 산 첫 iPod", "detect incompatible model/date; preserve issue in audit instead of silently inventing retail availability"),
    ("ipod_late_2001", "2001년 12월 첫 세대 iPod를 든 성인", "allow first-generation player with mechanical wheel; do not substitute nano"),
    ("nano_2005", "2005년 9월 검정 1세대 nano", "match first-generation black model; no pink later model"),
    ("revival_mixed", "현대 Y2K 재해석, 새 스마트폰도 함께", "allow deliberate contemporary mixing; do not apply archival exclusion"),
    ("year_unspecified", "Y2K 음악 플레이어 소품", "do not invent an exact year/model; generic morphology or advisory choices only"),
    ("spiky_not_messy", "spiky bun, 지저분한 풀린 번은 제외", "preserve compact gathered mass and separated projecting ends; enforce negation"),
    ("messy_not_spiky", "messy bun, 뻗친 스파이크는 제외", "do not activate spiky by nearby retrieval"),
    ("zigzag_not_crimp", "zigzag part와 곧은 머리", "zigzag belongs to scalp part, not wave of the lengths"),
    ("chunky_not_balayage", "굵고 경계가 뚜렷한 하이라이트", "defined hair color bands; no soft undelimited gradient substitute"),
    ("butterfly_owner", "나비 핀은 머리에만, 상의는 무지", "bind clip to hair and keep top print absent"),
    ("crop_not_low", "짧은 상의, 하이웨이스트 팬츠", "do not infer low rise from exposed midriff or short tee"),
    ("low_not_ultra", "low-rise, ultra-low는 제외", "preserve requested waist category; no automatic more extreme exposure"),
    ("bootcut_not_flare", "약한 bootcut, 큰 flare는 제외", "slight lower-leg opening rather than dramatic flare"),
    ("cargo_mini", "카고 미니 스커트", "use skirt silhouette with utility pockets, not cargo trousers"),
    ("flare_yoga", "유연한 플레어 요가 팬츠", "do not force denim construction"),
    ("tiny_big_geometry", "작은 상의와 넓은 팬츠, 몸 비율은 유지", "clothing-volume contrast without anatomical body shrinkage"),
    ("velour_not_terry", "짧은 파일의 velour 후디, 타월 루프 제외", "short pile on hoodie owner; loops cannot satisfy"),
    ("terry_not_velour", "루프가 보이는 terry 탑", "uncut visible loops; smooth sheen or cut pile cannot satisfy"),
    ("satin_not_silk", "새틴 같은 광택", "describe surface appearance without certifying silk fiber"),
    ("holo_not_projection", "홀로그램 코팅 가방", "bounded surface diffraction-like bands; no floating holographic figure"),
    ("retroreflective_limit", "플래시에 밝아지는 트림", "source-facing trim behavior; no material certification from one still"),
    ("shield_only", "하나의 shield 렌즈, 거의 평평하게", "single lens structure without forcing wraparound curve"),
    ("wrap_two", "두 렌즈가 얼굴 옆까지 감싸는 안경", "two lens topology and wrap curve can coexist; no shield forced"),
    ("bag_small_longstrap", "작은 숄더백, 긴 스트랩", "small bag size does not force underarm baguette carry"),
    ("hoop_size", "귀에 가까운 작은 huggie 링", "no oversized hoop substitution"),
    ("stone_not_sequin", "각면 스톤 벨트, 스팽글 제외", "three-dimensional faceted stones on belt; flat discs fail"),
    ("bead_phone", "비즈 참이 휴대폰 고리에 연결", "continuous attachment to phone; a separate bracelet is insufficient"),
    ("phone_neck", "휴대폰 목 스트랩", "continuous cord from neck to phone; wrist charm cannot replace"),
    ("graphic_not_object", "상의의 체리 프린트", "flat printed motif on garment; actual cherries are not evidence"),
    ("tattoo_print", "타투풍 프린트 티셔츠, 피부는 무문신", "preserve textile owner and skin exclusion"),
    ("camo_no_identity", "얼룩무늬 캐미솔", "no military job, nationality or affiliation inference"),
    ("blackletter_no_identity", "gothic lettering 상의", "no religion, goth membership or behavior inference"),
    ("text_user_control", "baby tee에 사용자 지정 문자 SUN", "retain SUN and text owner; no universal no-text rule"),
    ("intrinsic_color", "핑크 후디를 중성광으로", "pink belongs to fabric, not global illumination or skin tone"),
    ("lip_regions", "갈색 외곽선과 밝은 중심, gloss", "outline surrounds center on lips; dark full lip fill is not equivalent"),
    ("nail_owner", "손톱 위 입체 별 장식", "raised charm attached to nail plate; a star ring fails"),
    ("flash_optional", "Y2K 착장, 부드러운 창문광", "respect window light and do not promote direct-flash profile"),
    ("flash_not_age", "현대 디지털 직광 사진", "do not infer film capture, archival age, date stamp or indie sleaze"),
    ("gyaru_variation", "성인의 갸루 재해석", "keep requested adult subject and chosen literal styling; no forced tan, school uniform or Japanese nationality"),
    ("teen_pop_label", "Teen Pop 계열 성인 모델", "style label does not lower subject age"),
    ("frutiger_interface", "Frutiger Aero 앱 화면을 배경에만", "bind UI to background screen; do not transfer grass/glass graphics into wardrobe"),
    ("acubi_revival", "Acubi의 현대 층입기", "preserve contemporary scope and avoid claiming authentic 1999 reproduction"),
    ("locked_appearance", "상의·헤어 고정, 조명만 열림", "all appearance-changing bundles remain unavailable even if retrieved"),
    ("prop_scope", "iPod 소품 후보를 보고 싶음", "do not mark an empty-scope prop bundle adopted without declared contextual owner/dimension binding"),
    ("occluded_gate", "바스트 샷으로 낮은 팬츠 허리선은 화면 밖", "waist predicate unscored, not inferred visually or marked passed"),
    ("retrieval_not_obligation", "검토 후보 목록에 spiky bun이 있음", "retrieval/selection alone cannot activate a hard hairstyle profile"),
]

RENDER_PAIRS = [
    ("hair_topology", "spiky_bun tendrils", "messy_bun", "head three-quarter", "same adult subject description and light; only gathered-hair form differs"),
    ("part_vs_length", "zigzag_part straight_hair", "center_part crimp", "head top and front", "scalp path and length texture inspected separately"),
    ("waist_and_hem", "baby_tee low_rise bootcut", "baby_tee flare", "full body with waistband and feet", "control uses an explicitly higher waistband and stronger flare; only clothing boundaries change"),
    ("pile_vs_loop", "velour", "terry", "macro on same hoodie patch", "same garment color lighting scale; compare cut short pile and uncut loops"),
    ("stone_vs_disc", "rhinestones", "sequins", "macro on belt patch", "same belt color; count readable facets versus flat separate discs"),
    ("shield_vs_wrap", "shield", "wraparound", "eyewear front plus separate three-quarter arms", "a four-cell lens-count by curve matrix is required; one frontal image cannot resolve curvature"),
    ("bag_owner", "baguette underarm", "mini_shoulder", "shoulder to hips", "control requests long strap; compare size shape and carry height separately"),
    ("lip_scope", "brown_liner nude_center gloss", "gloss", "lip macro", "control requests uniform brown fill; gloss highlights cannot substitute for center/perimeter relation"),
    ("nail_attachment", "star_nail square_nails", "star_pendant", "hand and a hand-held necklace charm in the same macro frame", "control locates a star pendant on its separate necklace chain beside the hand; wrong-owner icon does not pass nail gate"),
    ("print_vs_scene", "circuit_graphic", "pixel_graphic", "upper garment detail", "requested print stays on cloth; background circuitry alone fails"),
    ("color_cause", "bling_palette velour_hoodie", "velour_hoodie", "torso under neutral light", "control uses a white hoodie under pink illumination; fabric-color role is scored separately"),
    ("lighting_independence", "baby_tee low_rise retro_flash", "baby_tee low_rise", "torso and receiving wall", "same outfit; compare direct flash to soft window light without changing historical label"),
]

OUT = {
    "schema_version": "y2k-prospective-qualification/v1",
    "status": "planned_not_executed",
    "text_cases": [{"id": name, "request_ko": request, "expected_contract": expected} for name, request, expected in TEXT_CASES],
    "render_pair_designs": [{"id": name, "positive_component_ids": positive.split(), "comparison_component_ids": control.split(),
        "minimum_view": view, "control_specification": rationale, "qualification_status": "not_rendered"} for name, positive, control, view, rationale in RENDER_PAIRS],
    "protocol": {
        "freeze_before_exposure": "request meaning, locked dimensions, era mode, tested component IDs, all gates and each arm's exact request",
        "evidence_layers": ["authored source", "generated index", "actual pack exposure", "candidate selection", "literal final prompt evidence", "runtime prompt and image response", "blind owner-scoped pixels", "user acceptance"],
        "comparators": "keep predeclared subject description camera light framing and request fixed except the chosen contrast; before/after qualification also requires a frozen baseline source snapshot",
        "arm_isolation": "one recorded generation per arm; zero retries or fallbacks; no cross-arm prompts images or observations",
        "provenance": ["source and proposed-extension SHA-256", "generator revision", "seed", "model and exact settings", "original candidate pack hash", "selected IDs", "composed and actual runtime prompt hashes", "returned image hashes", "moderation status", "reviewer gate answers"],
        "pixel_rule": "each component's owner, form and boundary gates must all pass; partial_is_fail",
        "unscored_rule": "blocked, inaccessible, cropped-out or too-small evidence is unscored with reason; never count as pass or visual zero",
        "source_limit": "a dated archival caption supports date context; the pixels do not independently prove capture year or cultural membership",
        "publication_rule": "do not claim strengthened operating quality until exposure, selection and declared pixel gates are measured",
        "historical_primary_archive_backlog": ["region-specific hip-hop/skate clothing in 1997–2005", "Nu-metal, Emo and Scene period collections", "gyaru subtype and year-specific silhouettes", "nail-technique earliest-date sources", "textile-museum or manufacturer samples covering pile/loop/weave and fiber variations", "specific phone colors and local retail dates"],
        "human_judgment_pending": True
    }
}

(HERE / "qualification-plan.json").write_text(json.dumps(OUT, ensure_ascii=False, indent=2) + "\n")
print(f"Wrote {len(TEXT_CASES)} prospective text cases and {len(RENDER_PAIRS)} paired render designs; none executed.")
