"""Translate reviewed research into narrow authored runtime DATA; never prompt routing.

Run with --root pointing at a task-owned source checkout. Research, source URLs,
coverage decisions and historical claims stay in docs, outside runtime assets.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


# Each row is an independently reviewed observable relation, not a copied glossary.
# card, suffix, slot, Korean narrow label, English narrow label, components,
# effects (dimension, target, property), positive owner context.
ROWS = [
 ("EG05", "gold_ground_sparse_botanical_screen", "prop", "금빛 패널의 회화 꽃가지와 여백", "painted sparse floral motifs on a bounded gold-ground panel",
  ["painted floral motifs lie on one bounded gold-colored panel", "exposed gold-colored intervals separate the painted motif groups"],
  [("appearance","depicted_artifact","surface.pattern"),("material","depicted_artifact","surface.material")], ["panel","screen","backdrop","패널","병풍"]),
 ("EG07", "neutral_lowered_upper_lids", "expression", "이완된 얼굴의 부분적으로 낮은 윗눈꺼풀", "partly lowered upper lids with relaxed brows and mouth",
  ["the upper lid margins partly cover the visible irises of the same face", "the visible brow and mouth contours remain relaxed"],
  [("expression","main_subject","eyes.aperture"),("expression","main_subject","brows.tension"),("expression","main_subject","mouth.tension")], ["face","portrait","woman","man","얼굴","초상"]),
 ("EG08", "off_camera_upward_eyeline", "expression", "머리 방향과 구분한 위쪽 카메라 밖 시선", "upward off-camera eyeline separate from head orientation",
  ["both visible eyes aim toward the same point above and beside the capture lens", "the eye direction remains readable independently of the head tilt"],
  [("expression","main_subject","eyes.gaze_direction")], ["eyes","face","portrait","시선","얼굴"]),
 ("EG09", "head_torso_orientation_axes", "body_orientation", "어깨 회전과 다른 머리 방향", "head direction distinct from the shoulder plane",
  ["the visible nose direction differs from the orientation of the same shoulder plane", "a continuous neck joins that head to those shoulders"],
  [("pose","main_subject","head.orientation"),("body_geometry","main_subject","head_neck_shoulders.orientation")], ["portrait","head","shoulder","초상","어깨"]),
 ("EG10", "relaxed_lip_separation", "expression", "이완된 입술 사이의 작은 틈", "small relaxed separation between the lip margins",
  ["the upper and lower lip margins enclose a small readable gap", "the mouth corners remain relaxed around that gap"],
  [("expression","main_subject","mouth.aperture"),("expression","main_subject","mouth.tension")], ["face","lips","portrait","얼굴","입술"]),
 ("EG11", "closed_eyes_composed_repose", "eye_detail", "안정된 머리 자세의 닫힌 양눈", "closed eye apertures with a supported composed head",
  ["both eye apertures on the same face are visibly closed", "the head remains aligned with its visibly supported shoulder posture"],
  [("expression","main_subject","eyes.aperture"),("pose","main_subject","head.support")], ["face","portrait","eyes","얼굴","초상"]),
 ("EG13", "central_vertical_bust_axis", "composition", "중앙 세로 배경 요소와 흉상 배치", "bust portrait aligned with an existing central vertical backdrop element",
  ["the bust crop retains the same face and neck as readable primary forms", "the existing vertical background element lies in the central region behind that bust"],
  [("framing","image_plane","crop"),("composition","main_subject","layout.position"),("composition","background_element","layout.position")], ["portrait","bust","초상","흉상"]),
 ("EG14", "arcing_branch_frame", "composition", "얼굴을 둘러싸되 가리지 않는 실제 곡선 가지", "physical arcing branches framing a readable portrait opening",
  ["continuous woody branch paths curve around the portrait region", "the branch opening leaves the selected facial features readable"],
  [("composition","scene_branches","layout.path"),("composition","main_subject","layout.occlusion")], ["branch","branches","flower","가지","꽃"]),
 ("EG15", "dark_lateral_negative_space", "composition", "장식과 얼굴 사이의 어두운 측면 여백", "dark low-detail lateral intervals separating face and ornament",
  ["low-detail dark intervals remain beside the primary face", "those intervals separate that face from the existing peripheral ornament"],
  [("composition","image_plane","layout.negative_space")], ["portrait","face","ornament","초상","장식"]),
 ("EG16", "asymmetric_botanical_balance", "composition", "얼굴 주변 꽃 그룹의 비대칭 분포", "unequal existing floral groups around a primary face",
  ["the two existing floral groups occupy visibly unequal extents or heights", "their distribution retains the face as the primary region"],
  [("composition","scene_flowers","layout.distribution"),("composition","image_plane","layout.focal_hierarchy")], ["flower","flowers","floral","꽃"]),
 ("EG17", "portrait_focus_plane_order", "focus", "선명한 눈과 더 먼 부드러운 꽃 평면", "readable near eye and softer farther physical flowers",
  ["the selected near eye retains readable iris and eyelid detail", "the farther physical flower plane has visibly softer petal boundaries"],
  [("camera","camera","focus.depth_of_field"),("composition","scene_flowers","layout.depth")], ["portrait","flower","flowers","초상","꽃"]),
 ("EG18", "nape_coiled_bun", "hair_style", "목덜미에 연결된 낮은 코일 번", "compact coiled hair bun connected at the nape",
  ["gathered scalp hair continues into a compact coiled mass at the nape", "the bun remains attached to the same head at its gathering point"],
  [("appearance","main_subject","hair.style")], ["hair","head","portrait","머리","초상"]),
 ("EG19", "brow_level_blunt_fringe", "hair_style", "눈썹 높이의 일자 앞머리", "blunt fringe edge at the eyebrow level",
  ["the front hair descends across the forehead into a blunt transverse edge", "that fringe edge ends at the same face's eyebrow level"],
  [("appearance","main_subject","hair.fringe")], ["hair","face","portrait","앞머리","초상"]),
 ("EG20", "separate_cheek_tendrils", "hair_style", "뿌리가 이어지는 볼 옆 가는 머리 가닥", "root-connected fine hair tendrils beside the cheek",
  ["fine strands descend beside the cheek from continuous hair roots", "those strands retain filament edges distinct from flat fabric ribbon"],
  [("appearance","main_subject","hair.side_strands")], ["hair","portrait","머리","초상"]),
 ("EG21", "attached_trailing_hair_ribbon", "hair_style", "머리 매듭에 연결된 늘어진 리본", "trailing fabric ribbon ends attached to a hair fastening",
  ["flat fabric ribbon ends continue from a readable fastening in the hair", "the attached ribbon tails hang with coherent gravity beside the same head"],
  [("appearance","main_subject","hair.accessories"),("material","main_subject","hair.accessories.material")], ["ribbon","hair","리본","머리"]),
 ("EG24", "cool_skin_warm_reflected_edge", "color", "차가운 얼굴 바탕과 국부 따뜻한 윤곽광", "cool facial base with a bounded warm source-facing contour",
  ["the central facial surface retains a relatively cool base color", "warm illumination stays on bounded source-facing skin contours"],
  [("color","main_subject","skin.apparent_color"),("lighting","main_subject","contour_light.color_distribution")], ["face","portrait","skin","얼굴","초상"]),
 ("EG27", "high_collar_lace_structure", "garment_detail", "목 주위를 세워 감싸는 레이스 칼라", "standing lace collar attached around the lower neck",
  ["a standing garment collar forms a boundary around the lower neck", "the lace pattern and scalloped upper edge belong to that attached collar"],
  [("appearance","main_subject","wardrobe.collar"),("material","main_subject","wardrobe.collar.material")], ["collar","lace","garment","칼라","레이스","의상"]),
 ("EG30", "shoulder_bound_flower_corsage", "garment_detail", "옷 어깨에 고정된 꽃 코르사주", "compact flower corsage attached at the garment shoulder",
  ["a compact flower group attaches at the selected garment shoulder", "its petal forms remain localized around that same attachment"],
  [("appearance","main_subject","wardrobe.shoulder_decoration")], ["garment","shoulder","corsage","의상","어깨"]),
 ("EG31", "fabric_rosette_vs_living_flower", "garment_detail", "직물 로제트와 별도 실제 꽃의 재질 구분", "folded fabric rosette distinct from an existing botanical flower",
  ["the garment rosette consists of gathered or folded fabric with cloth edges", "the separate existing flower retains botanical petals connected to its own stem"],
  [("appearance","main_subject","wardrobe.rosette"),("material","main_subject","wardrobe.rosette.material"),("appearance","scene_flower","surface.structure")], ["rosette","garment","flower","로제트","의상","꽃"]),
 ("EG34", "micropleated_tulle_panel", "garment_detail", "반복 가는 주름과 망이 함께 읽히는 튈", "micropleated tulle panel with readable mesh cells",
  ["narrow repeated pleat folds traverse one selected tulle panel", "fine open mesh cells remain readable on that same pleated panel"],
  [("appearance","main_subject","wardrobe.panel.folds"),("material","main_subject","wardrobe.panel.structure")], ["tulle","garment","mesh","튈","의상"]),
 ("EG37", "matte_mourning_crape", "surface_material", "광택을 억제한 검은 크레이프형 직물", "dark low-sheen cloth with a fine irregular crape-like surface",
  ["the selected dark cloth has a finely irregular low-sheen surface", "the same cloth folds retain restrained highlights and readable fabric edges"],
  [("material","main_subject","wardrobe.material"),("appearance","main_subject","wardrobe.surface_finish")], ["cloth","garment","crape","직물","의상"]),
 ("EG41", "mume_on_leafless_woody_branches", "prop", "성긴 작은 꽃이 달린 잎 적은 매화형 목질 가지", "small pale blossoms spaced along a sparse-leaf woody mume-like branch",
  ["small pale blossoms attach at separated intervals along one continuous woody branch", "that flowering branch has sparse or absent leaves and readable woody gaps"],
  [("appearance","scene_branch","botanical.structure")], ["branch","blossom","flower","가지","꽃","매화"]),
 ("EG42", "camellia_flower_leaf_system", "prop", "동백형 꽃과 같은 가지의 윤기 있는 넓은 잎", "camellia-like flowers connected with broad glossy leaves",
  ["the larger layered flowers connect to a traceable branching stem", "broad glossy leaves have distinct leaf boundaries on that same branch"],
  [("appearance","scene_branch","botanical.structure"),("material","scene_branch","leaf.surface_finish")], ["flower","camellia","branch","꽃","동백","가지"]),
 ("EG43", "magnolia_large_petals", "prop", "목련형 큰 꽃잎의 열린 컵 형태", "open cup-shaped magnolia-like flower with large floral segments",
  ["large distinct floral segments form an open cup-shaped bloom", "the bloom remains attached to its own woody stem"],
  [("appearance","scene_flower","botanical.structure")], ["flower","magnolia","branch","꽃","목련","가지"]),
 ("EG45", "near_black_layered_rose", "prop", "빛받는 주름에서 암적색이 읽히는 거의 검은 장미", "near-black layered rose with dark red-purple illuminated folds",
  ["layered rose petals retain separate folds and overlapping edges", "illuminated portions of those near-black petals retain a dark red-purple tendency"],
  [("appearance","scene_flower","botanical.structure"),("color","scene_flower","surface.local_color")], ["rose","flower","장미","꽃"]),
 ("EG46", "airy_small_flower_spray", "prop", "가는 줄기의 작은 꽃과 열린 간격", "airy branching spray of separated tiny flowers",
  ["fine branching stems carry many small individually separated flowers", "open intervals remain visible between those flower groups"],
  [("appearance","scene_flower","botanical.structure"),("composition","scene_flower","layout.spacing")], ["flower","spray","branch","꽃","가지"]),
 ("EG48", "frost_on_petals", "texture", "꽃잎에 붙은 작은 서리 결정", "small pale frost-like crystals attached to petal surfaces",
  ["small pale ice-like crystals cling to the selected petal surfaces", "the underlying petal folds and edges remain readable beneath the crystals"],
  [("material","scene_flower","surface.deposit"),("appearance","scene_flower","surface.texture")], ["petal","flower","꽃잎","꽃"]),
 ("EG48", "dew_on_petals", "texture", "꽃잎 가장자리의 분리된 투명 물방울", "separate clear droplets resting on petal edges",
  ["discrete clear droplets rest along the selected petal edges", "each droplet has a bounded contour separate from image-plane grain"],
  [("material","scene_flower","surface.deposit"),("appearance","scene_flower","surface.texture")], ["petal","flower","꽃잎","꽃"]),
 ("EG48", "dried_curled_petals", "texture", "퇴색한 마른 꽃잎의 국부 말린 가장자리", "localized curled edges on faded dry petals",
  ["the selected dry petals have localized curled edges", "uneven faded surface tones remain on those same dry petals"],
  [("appearance","scene_flower","surface.texture"),("color","scene_flower","surface.local_color")], ["petal","flower","꽃잎","꽃"]),
 ("EG53", "gold_leaf_like_bounded_panel", "surface_material", "한 패널에 한정한 불균일 금박형 반사", "bounded panel with uneven gold-leaf-like reflective patches",
  ["subtly uneven gold-colored reflective patches remain on one bounded panel", "highlight variation follows those panel patches while its outer boundary stays readable"],
  [("material","depicted_artifact","surface.reflectance"),("appearance","depicted_artifact","surface.texture"),("color","depicted_artifact","surface.local_color")], ["panel","screen","surface","패널","병풍","표면"]),
 ("EG54", "gold_mosaic_tesserae", "surface_material", "금빛 모자이크 조각과 반복 경계", "gold-colored mosaic pieces retaining adjacent tile boundaries",
  ["small adjacent gold-colored pieces retain repeated tile boundaries on one panel", "neighboring pieces show separate light responses within those boundaries"],
  [("material","depicted_artifact","surface.structure"),("appearance","depicted_artifact","surface.texture"),("color","depicted_artifact","surface.local_color")], ["panel","mosaic","tile","패널","모자이크"]),
 ("EG55", "localized_flaking_gilding", "texture", "금빛 표층의 국부 손실과 드러난 바탕", "localized gold-colored layer loss revealing a separate substrate",
  ["irregular local losses interrupt the reflective surface layer", "a distinguishable lower substrate occupies only the bounded loss regions"],
  [("appearance","depicted_artifact","surface.damage"),("material","depicted_artifact","surface.layering")], ["panel","gilding","surface","패널","금박","표면"]),
 ("EG56", "gilded_artifact_branch", "prop", "목질 가지와 구분한 금빛 가지형 공예물", "solid branch-shaped artifact with bounded metallic reflection",
  ["the branch-shaped artifact has a continuous solid object boundary", "metallic-looking reflections remain on that same branch-shaped member"],
  [("appearance","depicted_artifact","form.structure"),("material","depicted_artifact","surface.reflectance")], ["artifact","branch","sculpture","공예물","가지","조각"]),
 ("EG57", "charcoal_backdrop_dark_material", "location", "암회색 배경과 분리되는 피사체 외곽", "charcoal low-detail backdrop preserving the subject boundary",
  ["the existing backdrop is predominantly charcoal-dark with restrained surface detail", "small lightness differences keep the primary subject boundary readable against it"],
  [("appearance","background","surface.detail"),("color","background","surface.local_color"),("composition","image_plane","layout.figure_ground")], ["backdrop","background","portrait","배경","초상"]),
 ("EG60", "occluded_vertical_emissive_slit", "light_shape", "신체 뒤에서 가려지는 가늘고 긴 세로 발광 틈", "narrow vertical luminous aperture occluded behind the subject",
  ["a narrow vertically extended luminous aperture lies behind the subject", "the subject silhouette occludes the aperture wherever they overlap", "the remaining visible aperture segments belong to the same aligned opening"],
  [("lighting","rear_aperture","source.shape"),("composition","rear_aperture","layout.position"),("composition","main_subject","layout.occlusion")], ["subject","portrait","figure","인물","초상"]),
 ("EG63", "low_key_lifted_black_floor", "lighting", "어두운 장면과 잔존 세부가 있는 매트 암부", "dark-dominated scene with a separately lifted matte shadow floor",
  ["large low-luminance scene regions dominate the composition", "the output's matte shadow regions retain faint surface information above solid black"],
  [("lighting","scene","light.distribution"),("style","image_plane","rendering.black_floor")], ["scene","portrait","dark","장면","초상","어두운"]),
 ("EG65", "restrained_diffusion_detail", "quality", "부드러운 밝은 톤 전환과 남아 있는 피사체 세부", "gently softened bright transitions with retained focal detail",
  ["selected bright tonal transitions are gently softened", "the chosen focal eye or material detail remains readable through that softening"],
  [("style","image_plane","rendering.quality")], ["portrait","image","detail","초상","사진","세부"]),
 ("EG70", "localized_haze_depth", "ambient_particle", "선택한 깊이 영역에 한정된 엷은 안개", "thin haze confined to a declared scene depth region",
  ["thin haze occupies the selected depth region between existing scene owners", "clearer neighboring regions retain distinguishable object boundaries"],
  [("atmosphere","scene","medium.haze_distribution")], ["scene","room","space","장면","공간"]),
 ("EG70", "localized_suspended_particles", "ambient_particle", "선택한 조명 부피 안의 분리된 부유 입자", "separate suspended particles in a bounded lit scene volume",
  ["separate airborne particles occupy one bounded illuminated scene volume", "the particles sit at varying scene depths rather than covering the image plane uniformly"],
  [("atmosphere","scene","medium.particle_distribution")], ["scene","light","beam","장면","조명"]),
 ("EG70", "still_air_hanging_elements", "ambient_particle", "정지한 공기의 수직 매달림", "hanging flexible elements resting vertically in still air",
  ["the existing flexible hanging elements rest with a coherent downward gravity direction", "those elements show settled contours rather than wind-driven lateral deflection"],
  [("atmosphere","scene","air.motion_state"),("appearance","hanging_element","form.deflection")], ["ribbon","cloth","hanging","리본","직물"]),
]

LIMITS = [
 "Bind all components to the same declared owners; existing owners or compatible explicit authorial development are prerequisites.",
 "Broad mood, style, material or botanical labels alone do not require this narrow relation.",
 "Depicted appearance establishes no fabrication method, physical species identification, measured setting, historical identity, age, ethnicity, memory or mental state.",
 "Reference facial and hair appearance, requested wardrobe, exposure, count and events remain separately governed; this relation supplies none of them.",
 "All adopted components require native visible evidence; partial evidence fails and occlusion is unobservable.",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    assets = root / "skills/photo-prompt-image-generator/assets"
    research = root / "docs/research-evidence/photo-prompt/ethereal-gothic-research-20261007"
    evidence = root / "docs/research-evidence/photo-prompt/ethereal-gothic-integration-20261007"
    cards = {c["id"]: c for c in json.loads((research / "SEMANTIC-CARDS.json").read_text())["cards"]}
    slots, profiles, bundles, mapping = {}, [], [], []

    def add(card_id, suffix, slot, ko, label, units, effect_rows, owners, paraphrases=None, profile_override=None):
        cid = "egr_" + suffix
        pid = "egr_profile_" + suffix
        effects = [dict(dimension=d, target=t, property=p) for d,t,p in effect_rows]
        dimensions = list(dict.fromkeys(x["dimension"] for x in effects))
        definition = "; ".join(units)
        relation = dict(id="declared_owner_relation", type="has_bounded_visible_relation", subject="the declared existing owners", object=definition)
        examples = paraphrases or ["The selected owners show " + definition + ".", ko + "의 각 요소가 같은 대상에 연결되어 읽힌다."]
        entry = dict(id=cid, ko=ko, en=definition, weight=0.42,
                     tags=list(dict.fromkeys([slot, *owners[:2]])),
                     aliases=[ko, label], keywords=[ko, label], paraphrases=examples,
                     concept_units=units, relations=[relation], core_assertion_discovery=True,
                     affected_dimensions=dimensions, affected_properties=effects,
                     requires_primary_any_tags=owners,
                     embedding_text="; ".join([ko, label, *units, *examples]))
        slots.setdefault(slot, []).append(entry)
        if profile_override is None:
            components = [dict(id=f"component_{i}", match_terms=[unit], evidence_field=f"component_{i}_phrase",
                               evidence_terms=[unit], min_content_words=3,
                               instruction="Realize this selected relation on its declared owners: " + unit + ".",
                               render_gate=dict(id=f"vo_{pid}_{i}", review_scale="native",
                                  description=unit + ". Inspect original pixels on the declared owners; partial evidence fails and occlusion is unobservable."))
                          for i,unit in enumerate(units,1)]
            profiles.append(dict(id=pid, category="owner_bound_portrait_material_relation",
                activation=dict(exact_terms=[ko, label], requires_adult_character=False,
                    semantic_discovery_requires_component_evidence=False,
                    hard_activation=dict(contract_version="photo-visual-hard-activation/v1",
                        required_any_groups=[dict(id="declared_owner_context", any_terms=owners)])),
                semantics=dict(definition=definition, paraphrase_examples=examples, visual_components=units,
                    contrast_examples=cards[card_id]["confusion_boundaries"], claim_limits=LIMITS),
                concept_candidate=dict(concept_terms=[ko,label,*units,*examples],core_assertion_discovery=True,
                    affected_dimensions=dimensions,affected_properties=effects),
                runtime_expression=dict(default_mode="definition_with_optional_label",prompt_label_terms=[],forbidden_prompt_terms=[],runtime_forbidden_labels=[]),
                reject_substitutes=cards[card_id]["confusion_boundaries"],
                authored_components=dict(contract_version="photo-authored-visual-components/v1",components=components)))
        else:
            pid=profile_override
        bundles.append(dict(id=cid+"_bundle",candidate_only=True,primary_visual_proposition=definition,
            candidate_ids=[cid],candidate_slots={cid:slot},hard_profile_ids=[pid],
            component_groups=[dict(id=f"component_{i}",visible_evidence=[unit]) for i,unit in enumerate(units,1)],
            source_keywords=[ko,label],confusion_boundaries=cards[card_id]["confusion_boundaries"],relations=[relation]))
        mapping.append(dict(card_id=card_id,candidate_id=cid,slot=slot,profile_id=pid,
            source_ids=cards[card_id]["source_ids"],actual_components=units,
            transformation="reviewed_narrow_observable_relation"))
        return entry

    for row in ROWS:
        add(*row)

    # Twenty palettes are alternative local-color assignments, not material,
    # ethnicity, skin, light-source or object-creation recipes.
    palette_units=["three declared existing owners retain separate bounded color regions",
                   "the first color is the dominant field, the second is a separate secondary region, and the third remains a smaller bounded accent",
                   "the selected local color families remain distinguishable through their own surface or light boundaries"]
    effects=[("color","*","surface.local_color"),("color","*","wardrobe.color"),
             ("color","*","background.local_color"),("color","*","light.color")]
    palette_pid="egr_profile_three_owner_palette_roles"
    # Shared relation authored once; each palette candidate additionally binds its hues.
    add("EG69","three_owner_palette_roles","color","기존 세 대상에 분리한 주색·보조색·작은 강조색",
        "three-owner dominant secondary and bounded accent palette",palette_units,effects,
        ["palette","color","surface","light","색","표면","조명"])
    common=slots['color'].pop()
    common_bundle=bundles.pop()
    mapping.pop()
    palette_rows=json.loads((research/"PALETTE-ROLE-DRAFTS.json").read_text())["items"]
    for row in palette_rows:
        color_terms=row["color_terms"]
        units=[f"the declared dominant owner carries {color_terms[0]} local color",
               f"a separate declared secondary owner carries {color_terms[1]} local color",
               f"the smaller declared accent owner carries {color_terms[2]} local color"]
        entry=add("EG69","palette_"+row['seed_id'].lower(),"color",row['phrase']+"의 대상별 색 역할",
            "owner-bound palette "+row['phrase'],units,effects,
            ["palette","color","surface","light","색","표면","조명"],profile_override=palette_pid)
        entry['contextual_usage']={'contexts':[dict(id=entry['id']+'_premises',application_conditions=[
            'Declare three compatible existing color owners in the final scene and bind the dominant, secondary and accent roles to them.',
            'A color name containing metal, porcelain, rose, pearl or moon does not create that object or alter skin; it names a selected apparent hue family.'],
            limits=['Color words alone establish neither material identity nor exact spectral, numerical or HEX values.'])]}
        # Candidate hues and shared owner-role duties must both survive a joint choice.
        bundles[-1]['component_groups'] += [dict(id=f"role_{i}",visible_evidence=[u]) for i,u in enumerate(palette_units,1)]

    # Reviewed contextual enrichment is append-only. Narrow variants above are
    # NOT aliases for broader old entries (coiling and brow level add duties).
    contexts={
      'hair_style':{
        'low_bun_hair':dict(paraphrases=['hair gathered into a bun low on the head'],contexts=[dict(id='egr_low_bun_boundary',limits=['Low position alone does not establish coiling, nape attachment visibility, ribbons or a fringe.'])])},
      'color':{},
      'quality':{},
    }
    # Find reviewed existing entries by identity in the authored corpus rather
    # than silently assigning them to a guessed slot.
    raw_entries={}
    for path in [assets/'photo_prompt_tags.json',*assets.glob('*_extension.json')]:
        data=json.loads(path.read_text())
        for slot,entries in data.get('slots',{}).items():
            for e in entries: raw_entries.setdefault(e['id'],(slot,e))
    enrich={
      'cr_candidate_cool_subject':('a relatively cool subject color against relatively warm surrounding colors across their visible boundary','Cool relative tendency is not a fixed skin lightness, ethnicity, HEX value or warm-rim duty.'),
      'cr_candidate_dark_on_dark':('readable subject boundaries and surface detail separate dark local surfaces from a dark surrounding field','Dark local material, background light and output black-floor grading remain different properties.'),
      'pe_neutral_diffusion':('bright edges spread into a neutral soft halo while selected subject details stay recognizable','This existing variant requires neutral highlight halos; it does not require orange-red halation, all-over defocus or mist. Generic diffusion variants have separate contracts.'),
      'cr_candidate_low_chroma':('restrained chroma across the principal hue families with faint hue differences that remain visible','Restrained chroma does not name a fixed palette or create three color carriers.'),
    }
    for cid,(phrase,limit) in enrich.items():
        if cid not in raw_entries: raise ValueError('Missing reviewed enrichment target '+cid)
        slot,entry=raw_entries[cid]
        contexts.setdefault(slot,{})[cid]=dict(paraphrases=[phrase],contexts=[dict(id='egr_'+cid+'_boundary',limits=[limit])])
    contexts={k:v for k,v in contexts.items() if v}

    # Eight optional arrangements compose already-authored members. They cannot
    # turn aesthetic labels into duties or invent absent prerequisite owners.
    recipe_members={
      'central_rear_aperture':['egr_central_vertical_bust_axis','egr_occluded_vertical_emissive_slit','pe_rear_rim'],
      'quiet_face_axes':['egr_neutral_lowered_upper_lids','egr_off_camera_upward_eyeline','egr_relaxed_lip_separation'],
      'attached_hair_structure':['egr_nape_coiled_bun','egr_brow_level_blunt_fringe','egr_attached_trailing_hair_ribbon'],
      'lace_tulle_layers':['egr_high_collar_lace_structure','egr_micropleated_tulle_panel','clt_ct079_v1'],
      'physical_mume_portrait':['egr_arcing_branch_frame','egr_dark_lateral_negative_space','egr_mume_on_leafless_woody_branches'],
      'painted_reflective_panel':['egr_gold_ground_sparse_botanical_screen','egr_gold_leaf_like_bounded_panel'],
      'dark_material_separation':['egr_matte_mourning_crape','egr_high_collar_lace_structure','clt_ct089_v2'],
      'restrained_picture_finish':['pe_neutral_diffusion','pe_fine_midtonal_grain','pe_gentle_rolloff','pe_lifted_black_floor'],
    }
    candidates={e['id']:(slot,e) for slot,entries in slots.items() for e in entries}
    candidates.update(raw_entries)
    for name,members in recipe_members.items():
        items=[]
        for mid in members:
            if mid not in candidates: raise ValueError('Missing recipe member '+mid)
            slot,e=candidates[mid];items.append((mid,slot,e))
        units=list(dict.fromkeys(u for _,_,e in items for u in e.get('concept_units',[e['en']])))
        related=[m['profile_id'] for m in mapping if m['candidate_id'] in members]
        if not related:
            related=['diffusion_filter_highlight_halation','pe_fine_midtonal_grain_relation','highlight_rolloff_tone_response','pe_lifted_black_floor_relation']
        bundles.append(dict(id='egr_arrangement_'+name,candidate_only=True,
            primary_visual_proposition='; '.join(units),candidate_ids=members,
            candidate_slots={mid:slot for mid,slot,_ in items},hard_profile_ids=list(dict.fromkeys(related)),
            component_groups=[dict(id=f'component_{i}',visible_evidence=[u]) for i,u in enumerate(units,1)],
            source_keywords=[name.replace('_',' ')],
            confusion_boundaries=['The arrangement is an optional joint selection over already declared compatible owners; each member keeps its entire effects and premises.',
                'An aesthetic label, candidate exposure or associated profile ID supplies no automatic hard authority.'],
            relations=[]))

    record=dict(schema_version='photo-extension-maintenance/v1',record_id='ethereal-gothic-20261007-v2',maintenance_only=True,
        research_package='docs/research-evidence/photo-prompt/ethereal-gothic-research-20261007',
        curated_relation_count=len(profiles),candidate_count=sum(len(v) for v in slots.values()),
        optional_bundle_count=len(bundles),enriched_entry_count=sum(len(v) for v in contexts.values()),
        source_mapping=mapping,claim_boundary='Authored observable relations derived from cited research; no render qualification or user preference asserted by this record.',
        planned_to_actual=['Narrow bun, fringe, facial color and charcoal variants are separate opt-ins because their extra properties are not equivalent broad aliases.',
           'Atmosphere is split into haze, scene particles and settled hanging elements; no dust is inferred from grain.',
           'Magnolia variant is explicitly open cup form; no universal petal count.',
           'Palette hues have existing owners; no porcelain skin, metals or objects are implied.',
           'Ordinary appearance is not proof of optical hardware, species, historical process or unseen feelings.'])
    record_hash=hashlib.sha256(canonical(record)).hexdigest()
    extension=dict(schema_version='photo-prompt-research-extension/v1',slots=slots,
        existing_slot_context_extensions=contexts,visual_semantics=bundles,
        maintenance_ref=dict(contract_version='photo-extension-maintenance-ref/v1',record_id=record['record_id'],sha256=record_hash))
    profile_ext=dict(schema_version='photo-visual-obligation-registry-extension/v1',relation_contract_version='photo-visual-relation/v1',profiles=profiles)
    candidate_name='photo_prompt_ethereal_gothic_scene_extension.json'
    profile_name='photo_prompt_visual_obligations_ethereal_gothic_scene.json'
    write(assets/candidate_name,extension);write(assets/profile_name,profile_ext)
    manifest_path=assets/'photo_prompt_source_manifest.json'
    manifest=json.loads(manifest_path.read_text())
    for filename,kind in [(candidate_name,'candidate'),(profile_name,'visual_profile')]:
        if any(row['file']==filename for row in manifest['sources']): continue
        order=max(row['load_order'] for row in manifest['sources'] if row['kind']==kind)+1
        manifest['sources'].append(dict(file=filename,kind=kind,required=True,load_order=order))
    write(manifest_path,manifest)
    write(root/'docs/research-evidence/photo-prompt/extension-maintenance'/(record['record_id']+'.json'),record)
    # Complete seventy-card review disposition, including reuse and deferred items.
    all_mapping=[]
    for card in cards.values():
        authored=[m for m in mapping if m['card_id']==card['id']]
        actual='INTEGRATED_NEW_RELATION' if authored else ('REUSE_EXISTING' if card['integration']['treatment'] in {'REUSE','REUSE_EXISTING'} else card['integration']['treatment'])
        if card['id']=='EG65':actual='INTEGRATED_NEW_RELATION_AND_EXISTING_ENRICHMENT'
        all_mapping.append(dict(card_id=card['id'],planned_treatment=card['integration']['treatment'],actual_disposition=actual,
            candidate_ids=[m['candidate_id'] for m in authored],profile_ids=list(dict.fromkeys(m['profile_id'] for m in authored)),
            existing_references=card['existing_references'],source_ids=card['source_ids']))
    write(evidence/'INTEGRATION-MAP.json',dict(schema_version='ethereal-gothic-integration-map/v1',cards=all_mapping))
    write(evidence/'DATA-SUMMARY.json',dict(candidate_count=record['candidate_count'],profile_count=len(profiles),bundle_count=len(bundles),
        enrichment_count=record['enriched_entry_count'],maintenance_record_sha256=record_hash,
        added_asset_files=[candidate_name,profile_name],manifest_added_rows=[r for r in manifest['sources'] if r['file'] in [candidate_name,profile_name]],
        status='AUTHORED_NOT_YET_VALIDATED'))
    print(json.dumps({k:record[k] for k in ['curated_relation_count','candidate_count','optional_bundle_count','enriched_entry_count']},ensure_ascii=False))


if __name__=='__main__':main()
