#!/usr/bin/env python3
"""Build the additive visual meaning and image-search evidence assets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from moe_meaning_contract import MEANING_FILENAME, contract_sha256, load_meaning_contracts
from moe_visual_contract import (
    IMAGE_EVIDENCE_FILENAME,
    IMAGE_EVIDENCE_SCHEMA,
    VISUAL_MEANING_FILENAME,
    VISUAL_MEANING_SCHEMA,
)


CREATED_AT = "2026-08-18T00:00:00+09:00"


def _profile(
    all_of: list[str],
    topology: list[str],
    camera: list[str],
    *,
    any_of: list[str] | None = None,
    any_minimum: int = 0,
    temporal: list[str] | None = None,
    interaction: list[str] | None = None,
    modes: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "all_of": all_of,
        "any_of": any_of or [],
        "any_minimum": any_minimum,
        "topology": topology,
        "camera": camera,
        "temporal": temporal or [],
        "interaction": interaction or [],
        "modes": modes or ["single_frame", "paired_frame", "sequence"],
    }


VISUAL_PROFILES: dict[str, dict[str, Any]] = {
    "moe_darkening_corruption": _profile(
        [
            "same camera and scale across the earlier and later character states",
            "one unchanged identity anchor visible in every state",
        ],
        [
            "the unchanged identity anchor connects the earlier and later figure while the allegiance marker changes"
        ],
        ["matched full or three-quarter character framing without identity-obscuring crop"],
        any_of=[
            "expression and gaze direction change tied to the state change",
            "palette or lighting delta tied to the state change",
            "former ally reacting to the changed allegiance",
        ],
        any_minimum=1,
        temporal=[
            "baseline state before the catalyst",
            "changed allegiance and visible consequence after the catalyst",
        ],
        modes=["paired_frame", "sequence"],
    ),
    "moe_ntr_relationship_displacement": _profile(
        [
            "three clearly differentiated relationship roles",
            "one repeated bond token changing ownership or placement",
        ],
        ["a prior pair edge is visibly replaced or interrupted by a third-party pair edge"],
        ["wide enough framing to show all three roles and their spatial distance"],
        any_of=[
            "displaced partner isolated from the changed pair",
            "eyelines converging on the changed pair",
            "empty former place or unopened confession visible",
        ],
        any_minimum=1,
        temporal=[
            "prior bond or missed chance",
            "relationship displacement",
            "displaced viewpoint and consequence",
        ],
        modes=["paired_frame", "sequence"],
    ),
    "moe_sensory_deprivation_magic": _profile(
        [
            "channel-specific suppression glyph",
            "conscious subject continuing a visible task inside the effect",
        ],
        ["the field boundary separates information available to the subject from information available to the viewer"],
        ["split-plane or cutaway framing that keeps subject, boundary, and hidden event legible"],
        any_of=[
            "sound-wave path ending at the boundary",
            "unaffected light or motion passing through the field",
            "caster maintaining the selective field",
        ],
        any_minimum=1,
        temporal=["field activation", "maintained asymmetric event", "release and redirected attention"],
    ),
    "moe_virgin_killer_clothing": _profile(
        ["selected garment lineage shown without cross-lineage pieces"],
        ["front and rear garment boundaries agree with the selected construction lineage"],
        ["front and rear three-quarter garment views with the construction boundary visible"],
    ),
    "moe_mesugaki_provocation": _profile(
        ["adult provocateur visibly addressing one specific adult counterpart", "concrete status cue showing the momentary upper hand"],
        ["gaze, gesture, and interpersonal distance all point from provocateur to counterpart"],
        ["two-person framing that keeps the provocation target and consequence visible"],
        any_of=["half-lidded target-locked gaze", "raised chin with asymmetric smile", "forward lean or pointed gesture toward the counterpart"],
        any_minimum=1,
        temporal=["targeted provocation", "counterpart reaction or status reversal"],
    ),
    "moe_i_balance_pose": _profile(
        ["full body visible from grounded foot through raised foot", "pelvis and torso stacked over the single support foot"],
        ["one uninterrupted anatomical chain connects pelvis to the near-vertical free leg"],
        ["uncropped frontal or three-quarter view with the support contact point visible"],
    ),
    "moe_pajama_challenge": _profile(
        ["same oversized garment before and after rear pulling", "rear hand visibly gripping excess fabric"],
        ["fabric tension lines converge from the torso toward the rear grip"],
        ["matched diptych or rear three-quarter framing that reveals the actual grip"],
        temporal=["loose untensioned garment", "same garment pulled taut from behind"],
    ),
    "moe_reverse_bunny_costume": _profile(
        ["adult character with the retained detached bunny accessory set", "classic torso-suit coverage replaced by a deliberate inverse coverage mask"],
        ["retained ear collar cuff and legwear regions surround the absent or displaced classic torso-suit region"],
        ["full adult costume view with enough front and rear information to read the coverage inversion"],
    ),
    "moe_implied_all_ages_staging": _profile(
        ["central event withheld outside the visible action plane", "reaction or displaced prop causally linked to the unseen event"],
        ["eyeline or object displacement connects the occluded area to the reaction"],
        ["two-shot or three-panel context-and-reaction framing without explicit event depiction"],
        temporal=["context before the unseen event", "intentional withholding", "reaction or aftermath while uncertainty remains"],
    ),
    "moe_dolphin_shorts": _profile(
        ["elastic waistband on a loose running shell", "curved bound hem rising into a short side notch"],
        ["contrast piping follows the complete curved hem and side notch without turning into a straight hem"],
        ["front and side garment view that keeps waistband hem and notch visible"],
    ),
    "moe_thermal_bodysuit": _profile(
        ["continuous rib-knit torso ending in two leg openings", "visible gusset or small snap closure with no separate shirt hem"],
        ["neckline sleeve and rib direction continue into one bodysuit construction"],
        ["flat-lay or three-quarter garment view showing torso continuity and lower closure"],
    ),
    "moe_maternal_care": _profile(
        ["specific recipient need visible before the care action", "care prop physically contacting the need rather than floating nearby"],
        ["caregiver action points toward the recipient and produces an immediate visible result"],
        ["two-person medium framing that preserves hands care prop and recipient response"],
        temporal=["visible need", "targeted care action", "immediate relief recovery or boundary result"],
    ),
    "moe_screen_shake_illusion": _profile(
        ["isolated target with controlled spatial-frequency pattern", "stable surrounding reference with a deliberate phase offset"],
        ["target and surround use different phase relationships while sharing one visible grid system"],
        ["front-facing raster composition at a declared output scale without resampling blur"],
        interaction=["explicit viewer instruction naming shake or scroll direction", "effect checked while the display is moved in the declared direction"],
        modes=["optical_interaction"],
    ),
    "moe_bubble_tea_challenge": _profile(
        ["upright cup with horizontal liquid surface and visible contact shadow", "both hands completely inside the frame and separated from the cup"],
        ["continuous straw connects cup opening to mouth while gravity and body contact support the cup"],
        ["adult upper-body or three-quarter view showing cup straw mouth and both hands"],
    ),
    "moe_thigh_gap": _profile(
        ["both feet on the same ground plane and touching or nearly touching", "full inner-thigh contours surrounding true background"],
        ["one continuous background-bounded negative-space patch lies between the medial thighs"],
        ["neutral frontal lower-body view including pelvis knees ankles and both feet"],
    ),
    "moe_quicksand_sinking": _profile(
        ["opaque water-saturated granular slurry with visible grains or broken crust", "clear body-material meniscus with clinging residue"],
        ["surface depression and displaced rim respond to the trapped body's load"],
        ["wide enough hazard view to show material boundary support surface and escape direction"],
        any_of=["rescue board carrying load", "rope or hand tension toward solid ground", "braced arms widening support"],
        any_minimum=1,
        temporal=["surface failure", "partial entrapment", "self-rescue or assisted extraction"],
    ),
    "moe_axilla": _profile(
        ["raised arm causing visible clavicle and shoulder-girdle shift", "continuous anterior and posterior axillary folds around a shallow hollow"],
        ["upper arm shoulder chest side and torso remain one continuous anatomical surface"],
        ["three-quarter torso view with hair and clothing kept outside the axillary reading area"],
    ),
    "moe_stockings": _profile(
        ["two separate footed garments with both toes covered", "support mechanism visibly connected to each upper stocking band"],
        ["fabric opacity seam and band continue consistently from thigh to foot"],
        ["full leg view including both top bands and both covered feet"],
    ),
    "moe_morals_committee": _profile(
        ["committee role marker paired with a concrete school duty object", "student counterpart or school route affected by the duty"],
        ["clipboard rule object and committee action connect to one visible result"],
        ["school-context medium view showing role marker task and counterpart together"],
        temporal=["rule or route issue", "committee action", "practical result or personal reaction gap"],
    ),
    "moe_adult_finger_sucking": _profile(
        ["explicitly adult face and hand", "finger pad crossing the lip boundary with slight contact compression"],
        ["wrist palm finger pad and mouth form one continuous depth chain"],
        ["adult side or three-quarter close portrait showing exact lip-finger overlap"],
    ),
    "moe_classic_bunny_costume": _profile(
        ["structured strapless one-piece with complete detached collar bow and cuffs", "paired ears centered tail hosiery and closed-toe pumps"],
        ["detached accessory set and structured torso suit read as one historical costume system"],
        ["full adult costume view plus rear or three-quarter evidence for the centered tail"],
    ),
    "moe_tsf_transformation": _profile(
        ["same identity carrier visibly preserved or exchanged according to the mechanism", "consistent camera background and costume anchor across transformation states"],
        ["identity markers and body occupancy change along one declared mechanism path"],
        ["matched sequential framing with every body and identity carrier visible"],
        temporal=["pre-change identity state", "visible catalyst or exchange boundary", "post-change recognition state"],
        modes=["paired_frame", "sequence"],
    ),
    "moe_yandere_obsession": _profile(
        ["specific adult affection target established before control evidence", "boundary-crossing action visibly reducing the target's choices"],
        ["the same love-target token links caring baseline surveillance or access control and consequence"],
        ["paired or sequential two-person framing without relying on weapon props"],
        temporal=["ordinary affection or care baseline", "obsessive control action", "target reaction or reduced options"],
        modes=["paired_frame", "sequence"],
    ),
    "moe_glasses": _profile(
        ["two lens rims joined by a bridge resting on the nose", "both temples continuing through perspective toward the ears"],
        ["frame front bridge hinges and temples form one coherent three-dimensional object"],
        ["front or three-quarter face view with low lens glare and both eyes readable"],
    ),
    "moe_ponytail": _profile(
        ["scalp hair converging radially into one visible tie point", "single tail bundle tapering under gravity from that tie point"],
        ["hair flow follows the skull into the tie and continues as one attached bundle"],
        ["side or rear three-quarter head-and-shoulder view showing scalp flow tie and tail root"],
    ),
    "moe_contempt_derision": _profile(
        ["clear target receiving the directed dismissal", "asymmetric brow eyelid or mouth corner combined with raised chin"],
        ["gaze speech or hand-turn vector runs from the dominant figure to the withdrawing target"],
        ["two-person framing that keeps both directed expression and target response visible"],
        any_of=["cold target-locked gaze", "dismissive hand turn", "addressed readable speech balloon"],
        any_minimum=1,
        temporal=["directed dismissal", "target withdrawal recoil or distance change"],
    ),
    "moe_abdomen": _profile(
        ["continuous lower-rib abdomen pelvis surface", "navel and soft-tissue deformation consistent with the chosen pose"],
        ["compression occurs on the shortened torso side while the opposite side stretches"],
        ["torso framing includes lower ribs pelvis and pose-causing limbs rather than an isolated navel crop"],
    ),
    "moe_strategic_occlusion_selfie": _profile(
        ["explicit adult mirror-selfie setup with complete mirror boundary", "direct hand reflected hand and phone occupying distinct projection points"],
        ["camera-to-mirror handedness and every occlusion T-junction remain geometrically consistent"],
        ["full mirror composition showing direct body mirror boundary and reflected body simultaneously"],
    ),
    "moe_ahegao_expression": _profile(
        ["adult face with eye-control loss mouth-control loss and visible tongue combined", "at least one secondary overload marker without replacing the core facial geometry"],
        ["misaligned pupils slack mouth and tongue remain parts of one coherent adult facial expression"],
        ["adult face-and-shoulders crop keeping both eyes mouth tongue and secondary marker visible"],
        any_of=["drool at the mouth edge", "tears or sweat around the eyes", "facial flush", "facial asymmetry"],
        any_minimum=1,
    ),
}


VARIANT_GROUPS: dict[str, dict[str, list[str]]] = {
    "moe_virgin_killer_clothing": {
        "lineage_2015_blouse_skirt": ["vkc_2015_blouse_skirt", "blouse_highwaist_skirt_2015"],
        "lineage_2017_backless_knit": ["vkc_2017_backless_knit", "backless_knit_2017"],
        "coverage_contrast_comparison": ["vkc_generic_coverage_contrast"],
    },
    "moe_i_balance_pose": {
        "assisted_vertical_balance": ["i_balance_assisted_side_split", "i_balance_assisted_front_split", "assisted_vertical_side_split"],
        "unassisted_vertical_balance": ["i_balance_unassisted_split", "unassisted_vertical_side_split"],
    },
    "moe_reverse_bunny_costume": {
        "strict_coverage_inversion": ["rbc_strict_coverage_inversion", "balanced_coverage_inversion", "arm_heavy_coverage_inversion"],
        "layered_or_occluded_analogue": ["rbc_sns_occlusion_variant", "rbc_cosplay_layered_variant"],
    },
    "moe_thermal_bodysuit": {
        "high_neck_rib_body": ["tb_2018_extra_warm_high_body", "high_neck_long_sleeve_rib"],
        "rib_or_smooth_body": ["tb_2018_rib_tank_body", "crew_neck_short_sleeve_smooth"],
        "lace_body_lineage": ["tb_2015_lace_body"],
        "generic_thermal_body": ["tb_generic_thermal_body"],
    },
    "moe_screen_shake_illusion": {
        "vertical_phase_shake": ["vertical_phase_lag", "vertical_shake_alternating_grid"],
        "horizontal_phase_shake": ["horizontal_phase_lag", "horizontal_shake_vertical_phase_bands"],
        "scroll_activation": ["scroll_activated"],
    },
    "moe_quicksand_sinking": {
        "active_partial_entrapment": ["waist_level_active_struggle", "body_material_state", "self_directed_action"],
        "assisted_rescue": ["knee_level_early_rescue", "ensemble_relation"],
        "material_mechanics": ["material_mechanics"],
    },
    "moe_stockings": {
        "garter_supported": ["st_garter_stockings", "garter_supported_seam_back"],
        "self_supporting_holdups": ["st_hold_ups", "self_supporting_sheer_holdups"],
        "surface_or_contrast_study": ["st_surface_style", "st_tights_pantyhose"],
    },
    "moe_adult_finger_sucking": {
        "index_finger_contact": ["finger_sucking_index_pad_shallow", "index_fingertip_three_quarter"],
        "thumb_contact": ["finger_sucking_thumb_pad_shallow", "thumb_side_profile_contact"],
        "side_contact": ["finger_sucking_side_contact"],
    },
    "moe_tsf_transformation": {
        "single_body_transformation": ["same_person_bodily_change", "temporary_reversible_cycle", "permanent_adaptation", "gradual_single_body_magic_transformation"],
        "reciprocal_body_swap": ["reciprocal_body_swap", "instant_reversible_dual_body_swap"],
        "possession_or_transfer": ["possession_occupancy", "mind_or_brain_transfer"],
        "reincarnation_embodiment": ["reincarnation_new_embodiment"],
    },
    "moe_contempt_derision": {
        "verbal_derision": ["addressed_verbal_abuse", "comic_mockery", "dialogue_led_comedic_derision", "public_ridicule"],
        "nonverbal_contempt": ["silent_contempt_display", "dismissive_turn_away", "power_angle_derision", "cold_private_rejection", "nonverbal_cold_dismissal"],
    },
    "moe_abdomen": {
        "stretch_or_neutral_surface": ["abdomen_neutral_soft", "abdomen_overhead_stretch", "abdomen_selective_definition", "abdomen_breathing_relaxed", "standing_stretch_soft_surface"],
        "seated_compression": ["abdomen_seated_compression", "seated_compression_natural_folds"],
        "twist_tension_compression": ["abdomen_twist_tension_compression"],
    },
    "moe_ahegao_expression": {
        "moderate_control_loss_cluster": ["core_face_code", "moderate_cluster_rolled_eyes_tongue_drool"],
        "low_intensity_asymmetric_cluster": ["low_intensity_one_eye_asymmetry"],
        "narrative_or_gesture_cluster": ["terminal_narrative_expression", "gesture_composite"],
    },
}


DEFAULT_VARIANTS = {
    "moe_virgin_killer_clothing": "lineage_2017_backless_knit",
    "moe_i_balance_pose": "assisted_vertical_balance",
    "moe_reverse_bunny_costume": "strict_coverage_inversion",
    "moe_thermal_bodysuit": "high_neck_rib_body",
    "moe_screen_shake_illusion": "vertical_phase_shake",
    "moe_quicksand_sinking": "active_partial_entrapment",
    "moe_stockings": "self_supporting_holdups",
    "moe_adult_finger_sucking": "index_finger_contact",
    "moe_tsf_transformation": "single_body_transformation",
    "moe_contempt_derision": "nonverbal_contempt",
    "moe_abdomen": "stretch_or_neutral_surface",
    "moe_ahegao_expression": "moderate_control_loss_cluster",
}


VARIANT_REQUIREMENT_OVERRIDES: dict[tuple[str, str], dict[str, Any]] = {
    ("moe_virgin_killer_clothing", "lineage_2015_blouse_skirt"): {
        "all_of": ["frilled blouse visibly separate from a structured high-waisted skirt", "blouse volume compressed by a clear skirt waistband"],
        "topology": ["blouse and skirt remain two garments joined only by the visible waist overlap"],
        "camera": ["front and rear three-quarter garment views showing the blouse-skirt boundary"],
    },
    ("moe_virgin_killer_clothing", "lineage_2017_backless_knit"): {
        "all_of": ["continuous high-halter knit minidress", "open back extending to the waist without a separate blouse or skirt"],
        "topology": ["front knit coverage remains continuous while the rear torso coverage opens to the waist"],
        "camera": ["matched front and rear three-quarter views exposing the backless construction"],
    },
    ("moe_virgin_killer_clothing", "coverage_contrast_comparison"): {
        "all_of": ["side-by-side lineage comparison without merging their garment pieces"],
        "topology": ["each figure preserves one internally complete garment lineage"],
        "camera": ["matched front and rear comparison sheet for both lineages"],
        "modes": ["paired_frame", "sequence"],
    },
    ("moe_i_balance_pose", "unassisted_vertical_balance"): {
        "all_of": ["free leg held near vertical without either hand touching the ankle or foot", "arms used only as free counterweights"],
    },
    ("moe_reverse_bunny_costume", "layered_or_occluded_analogue"): {
        "all_of": ["adult-safe layered or occluded coverage analogue", "retained bunny accessory system and clearly inverted classic coverage map"],
    },
    ("moe_screen_shake_illusion", "horizontal_phase_shake"): {
        "interaction": ["explicit left-right display motion instruction", "horizontal-motion effect checked at the declared raster scale"],
    },
    ("moe_screen_shake_illusion", "scroll_activation"): {
        "interaction": ["explicit vertical scroll instruction", "scroll-induced relative-motion effect checked in an interactive viewport"],
    },
    ("moe_quicksand_sinking", "material_mechanics"): {
        "all_of": ["cross-section of water-saturated grains and collapsed load-bearing structure", "surface load connected to subsurface displacement"],
        "camera": ["educational cutaway plus surface view rather than a cropped body-only peril image"],
    },
    ("moe_stockings", "garter_supported"): {
        "all_of": ["two separate footed stockings", "visible garter straps clipped to both upper stocking bands"],
    },
    ("moe_stockings", "self_supporting_holdups"): {
        "all_of": ["two separate footed stockings", "self-supporting top bands without invented garter straps"],
    },
    ("moe_stockings", "surface_or_contrast_study"): {
        "all_of": ["explicit side-by-side distinction between separate stockings and one-piece pantyhose", "feet and waist topology both visible for comparison"],
        "modes": ["paired_frame", "sequence"],
    },
    ("moe_adult_finger_sucking", "thumb_contact"): {
        "all_of": ["adult thumb pad crossing the lip boundary", "thumb wrist and mouth aligned in a side-profile depth chain"],
    },
    ("moe_tsf_transformation", "reciprocal_body_swap"): {
        "all_of": ["two bodies visible before and after the exchange", "identity anchors exchanged between the two bodies without changing body count"],
        "topology": ["each identity edge crosses from its original body to the other body across the exchange boundary"],
    },
    ("moe_tsf_transformation", "possession_or_transfer"): {
        "all_of": ["source and destination embodiment states both visible", "one identity carrier moving into or occupying the destination body"],
    },
    ("moe_tsf_transformation", "reincarnation_embodiment"): {
        "all_of": ["earlier identity anchor echoed in a later new embodiment", "clear temporal break rather than an instantaneous costume change"],
    },
    ("moe_contempt_derision", "verbal_derision"): {
        "any_of": ["addressed readable speech balloon", "speech gesture and mouth direction visibly aimed at the target"],
        "any_minimum": 1,
    },
    ("moe_abdomen", "seated_compression"): {
        "all_of": ["seated forward-flexed torso with lower ribs and pelvis visible", "soft horizontal compression folds caused by the seated posture"],
    },
    ("moe_abdomen", "twist_tension_compression"): {
        "all_of": ["one shortened compressed torso side", "opposite elongated side with continuous oblique tension"],
    },
    ("moe_ahegao_expression", "low_intensity_asymmetric_cluster"): {
        "all_of": ["adult face with one upward-deviated eye and one half-lidded eye", "slack open mouth with a small visible tongue tip"],
    },
}


ALIAS_OVERRIDES: dict[str, tuple[str, str | None]] = {
    "relationship displacement triangle": ("related", None),
    "directed impudent provocation": ("carrier", None),
    "vertical standing split": ("carrier", None),
    "동정을 죽이는 스웨터": ("variant", "lineage_2017_backless_knit"),
    "童貞を殺すセーター": ("variant", "lineage_2017_backless_knit"),
    "virgin-killer sweater": ("variant", "lineage_2017_backless_knit"),
    "occluded suggestion staging": ("carrier", None),
    "dolphin-hem running shorts": ("carrier", None),
    "turtleneck bodysuit": ("related", None),
    "unexpected caregiver": ("carrier", None),
    "fluttering-heart illusion": ("variant", "vertical_phase_shake"),
    "medial-thigh negative space": ("carrier", None),
    "늪에 빠짐": ("related", None),
    "sinking peril": ("related", None),
    "underarm surface": ("carrier", None),
    "separate stockings": ("carrier", None),
    "hold-up stockings": ("variant", "self_supporting_holdups"),
    "finger-to-mouth contact": ("related", None),
    "body-swap transformation": ("variant", "reciprocal_body_swap"),
    "fictional embodiment transformation": ("carrier", None),
    "glasses accessory": ("carrier", None),
    "ponytail hair bundle": ("carrier", None),
    "directed contempt display": ("carrier", None),
    "abdomen surface": ("carrier", None),
    "midriff surface": ("related", None),
    "ahegao expression code": ("carrier", None),
}


SEARCH_DATA: dict[str, dict[str, Any]] = {
    "moe_darkening_corruption": {"confidence": "high", "queries": ["闇落ち character design before after anime illustration"], "urls": ["https://medibang.com/picture/px2205211726182060023699012/"]},
    "moe_ntr_relationship_displacement": {"confidence": "low", "queries": ["NTR relationship displacement anime visual trope non explicit", "relationship displacement triangle visual storytelling illustration"], "urls": []},
    "moe_sensory_deprivation_magic": {"confidence": "medium", "queries": ["sensory deprivation magic field sound wave blocked fantasy illustration"], "urls": ["https://monstersandmagic.ai/08-spells/10-spells-a-z/S/281-silence/"]},
    "moe_virgin_killer_clothing": {"confidence": "high", "queries": ["童貞を殺す服 backless sweater dress blouse high waist skirt illustration comparison"], "urls": ["https://news.gamme.com.tw/1472721"]},
    "moe_mesugaki_provocation": {"confidence": "medium", "queries": ["cheeky smug adult anime character expression chart teasing provocation"], "urls": ["https://note.com/osushi333/n/n80233473f436"]},
    "moe_i_balance_pose": {"confidence": "high", "queries": ["I字バランス ポーズ 片足 垂直 イラスト"], "urls": ["https://illust.daysneo.com/works/4b163cd0b06a3956b3f5b91625c0415f.html"]},
    "moe_pajama_challenge": {"confidence": "high", "queries": ["pajama challenge oversized t-shirt pulled behind back illustration comparison"], "urls": ["https://knowyourmeme.com/memes/t-shirt-pajamas-challenge"]},
    "moe_reverse_bunny_costume": {"confidence": "medium", "queries": ["reverse bunny costume visual design non explicit illustration"], "urls": ["https://knowyourmeme.com/sensitive/memes/reverse-bunny-suit"]},
    "moe_implied_all_ages_staging": {"confidence": "medium", "queries": ["all ages implied scene foreground occlusion reaction aftermath visual storytelling anime"], "urls": ["https://pmc.ncbi.nlm.nih.gov/articles/PMC6822748/"]},
    "moe_dolphin_shorts": {"confidence": "high", "queries": ["dolphin shorts curved hem contrast piping illustration reference"], "urls": ["https://www.thecollegiatelineup.com/products/dolphin-shorts"]},
    "moe_thermal_bodysuit": {"confidence": "high", "queries": ["rib knit bodysuit technical fashion drawing leg openings snap closure"], "urls": ["https://www.gu-global.com/jp/ja/products/E352218-000/00"]},
    "moe_maternal_care": {"confidence": "medium", "queries": ["maternal caring anime character visual trope illustration"], "urls": []},
    "moe_screen_shake_illusion": {"confidence": "high", "queries": ["screen shake optical illusion static grid central heart interaction illusion"], "urls": ["https://www.bu.edu/lite/Project_LITE_Vector/Vectorized_LITE.html"]},
    "moe_bubble_tea_challenge": {"confidence": "high", "queries": ["bubble tea challenge hands free cup straw upper torso meme illustration non explicit"], "urls": ["https://knowyourmeme.com/memes/hands-free-bubble-tea-tapioca-chalenge/photos"]},
    "moe_thigh_gap": {"confidence": "high", "queries": ["thigh gap closed feet silhouette anatomy reference non sexual"], "urls": ["https://pubmed.ncbi.nlm.nih.gov/41332495/"]},
    "moe_quicksand_sinking": {"confidence": "high", "queries": ["quicksand sinking illustration surface depression rescue board granular slurry"], "urls": ["https://www.nature.com/articles/437635a"]},
    "moe_axilla": {"confidence": "high", "queries": ["anime raised arm axilla anatomy pose reference non explicit adult"], "urls": ["https://www.sohu.com/a/532716006_120171660"]},
    "moe_stockings": {"confidence": "high", "queries": ["stockings garment top band garter seam technical fashion illustration"], "urls": ["https://www.moma.org/collection/works/217851"]},
    "moe_morals_committee": {"confidence": "high", "queries": ["風紀委員 character design armband clipboard anime illustration"], "urls": ["https://imas.gamedbs.jp/cg/idol/detail/193?h=1ddf4597ef3f8115948d32bfa920b691"]},
    "moe_adult_finger_sucking": {"confidence": "medium", "queries": ["adult character fingertip crosses lips side profile drawing reference"], "urls": ["https://www.clipstudio.net/oekaki/archives/151365"]},
    "moe_classic_bunny_costume": {"confidence": "high", "queries": ["classic bunny costume structured bodysuit collar cuffs ears tail fashion illustration"], "urls": ["https://www.playboyclothing.com.au/blogs/playboy-blog/the-authentic-bunny-suit"]},
    "moe_tsf_transformation": {"confidence": "high", "queries": ["TSF transformation before after anime character sequence illustration"], "urls": ["https://www.deviantart.com/jumpy-ai/art/tg-TSF-sequence-2-933372234"]},
    "moe_yandere_obsession": {"confidence": "low", "queries": ["yandere character expression chart affection obsession control visual storytelling non graphic"], "urls": []},
    "moe_glasses": {"confidence": "high", "queries": ["anime glasses frame bridge temples character design reference sheet"], "urls": ["https://ichi-up.net/2019/07"]},
    "moe_ponytail": {"confidence": "high", "queries": ["anime ponytail tie point hair bundle gravity character design reference"], "urls": ["https://atam-academy.com/blog/45146/"]},
    "moe_contempt_derision": {"confidence": "high", "queries": ["anime contempt expression drawing tutorial raised chin half lidded eyes asymmetric mouth"], "urls": ["https://animeartmagazine.com/top-tips-for-drawing-expressions-part-9-hate-disgust/"]},
    "moe_abdomen": {"confidence": "high", "queries": ["anime abdomen drawing seated compression folds navel torso reference adult"], "urls": ["https://hj-gihousho.com/book/3703"]},
    "moe_strategic_occlusion_selfie": {"confidence": "low", "queries": ["mirror selfie occlusion geometry phone reflection hands illustration"], "urls": []},
    "moe_ahegao_expression": {"confidence": "high", "queries": ["ahegao facial expression visual components eyes mouth tongue non explicit reference"], "urls": ["https://en.wikipedia.org/wiki/Ahegao"]},
}


def _encoded(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def _variant_groups(element: dict[str, Any]) -> dict[str, list[str]]:
    element_id = element["id"]
    explicit = VARIANT_GROUPS.get(element_id)
    if explicit is not None:
        return explicit
    return {
        "canonical_visual_signature": sorted(
            {candidate["subtype_id"] for candidate in element["candidates"]}
        )
    }


def _variant_payload(
    element_id: str,
    variant_id: str,
    subtype_ids: list[str],
    base_contract: dict[str, Any],
) -> dict[str, Any]:
    profile = dict(VISUAL_PROFILES[element_id])
    profile.update(VARIANT_REQUIREMENT_OVERRIDES.get((element_id, variant_id), {}))
    return {
        "id": variant_id,
        "candidate_subtype_ids": subtype_ids,
        "required_component_group_ids": [
            group["id"] for group in base_contract["component_groups"]
        ],
        "all_of_en": profile["all_of"],
        "any_of": {
            "minimum": profile.get("any_minimum", 0),
            "alternatives_en": profile.get("any_of", []),
        },
        "topology_edges_en": profile["topology"],
        "camera_requirements_en": profile["camera"],
        "temporal_states_en": profile.get("temporal", []),
        "interaction_requirements_en": profile.get("interaction", []),
        "negative_visual_confounds_en": list(base_contract["false_substitutes_en"]),
        "supported_output_modes": profile["modes"],
    }


def build_assets(asset_dir: str | Path) -> tuple[dict[str, Any], dict[str, Any]]:
    root = Path(asset_dir).expanduser().resolve()
    v3 = json.loads((root / "illustration_moe_grammar_v3.json").read_text(encoding="utf-8"))
    expected_ids = [element["id"] for element in v3["elements"]]
    base = load_meaning_contracts(
        root / "research_evidence_moe_elements" / MEANING_FILENAME,
        expected_element_ids=expected_ids,
    )
    evidence_records: list[dict[str, Any]] = []
    contracts: list[dict[str, Any]] = []
    for element in v3["elements"]:
        element_id = element["id"]
        ordinal = int(element["ordinal"])
        base_contract = base.contracts_by_id[element_id]
        profile = VISUAL_PROFILES[element_id]
        search = SEARCH_DATA[element_id]
        evidence_id = f"moe_image_evidence_{ordinal:02d}"
        evidence_records.append(
            {
                "id": evidence_id,
                "element_id": element_id,
                "queries": search["queries"],
                "search_confidence": search["confidence"],
                "recurring_features_en": list(
                    dict.fromkeys(
                        [
                            *profile["all_of"],
                            *profile["topology"],
                            *profile.get("any_of", []),
                        ]
                    )
                ),
                "observed_confounds_en": list(base_contract["false_substitutes_en"]),
                "representative_source_urls": search["urls"],
                "limitations_en": [
                    "Search results are a qualitative, unstable sample and do not measure trope prevalence.",
                    "Explicit or age-ambiguous results were excluded; low-result queries do not imply absent visual semantics.",
                ],
            }
        )
        groups = _variant_groups(element)
        default_variant = DEFAULT_VARIANTS.get(element_id, next(iter(groups)))
        aliases = []
        for alias in element["aliases"]:
            relation, variant_id = ALIAS_OVERRIDES.get(alias, ("exact", None))
            aliases.append(
                {"alias": alias, "relation": relation, "variant_id": variant_id}
            )
        contracts.append(
            {
                "element_id": element_id,
                "ordinal": ordinal,
                "base_contract_sha256": contract_sha256(base_contract),
                "default_variant_id": default_variant,
                "alias_bindings": aliases,
                "visual_variants": [
                    _variant_payload(element_id, variant_id, subtype_ids, base_contract)
                    for variant_id, subtype_ids in groups.items()
                ],
                "image_evidence_id": evidence_id,
            }
        )
    evidence = {
        "schema": IMAGE_EVIDENCE_SCHEMA,
        "created_at": CREATED_AT,
        "methodology": {
            "search_scope": "One or more Korean, Japanese, or English non-explicit image queries for every one of the 29 reviewed elements.",
            "content_filter": "Exclude explicit sexual acts, age-ambiguous body-focus examples, duplicate AI outputs, and unrelated search spillover.",
            "interpretation_limit": "Derived features support contract design only; they are not popularity statistics, copyright templates, or rendered-pixel proof.",
        },
        "record_count": len(evidence_records),
        "records": evidence_records,
    }
    evidence_bytes = _encoded(evidence)
    visual = {
        "schema": VISUAL_MEANING_SCHEMA,
        "created_at": CREATED_AT,
        "base_contract_schema": base.payload["schema"],
        "base_contracts_sha256": base.sha256,
        "image_evidence_schema": IMAGE_EVIDENCE_SCHEMA,
        "image_evidence_sha256": hashlib.sha256(evidence_bytes).hexdigest(),
        "contract_count": len(contracts),
        "contracts": contracts,
    }
    return evidence, visual


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--asset-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets",
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.asset_dir.expanduser().resolve()
    evidence, visual = build_assets(root)
    outputs = {
        root / "research_evidence_moe_elements" / IMAGE_EVIDENCE_FILENAME: _encoded(evidence),
        root / "research_evidence_moe_elements" / VISUAL_MEANING_FILENAME: _encoded(visual),
    }
    if args.check:
        stale = [str(path) for path, encoded in outputs.items() if not path.is_file() or path.read_bytes() != encoded]
        if stale:
            raise SystemExit(f"visual meaning assets are stale: {stale}")
    else:
        for path, encoded in outputs.items():
            path.write_bytes(encoded)
    print(
        json.dumps(
            {
                "check": args.check,
                "contracts": visual["contract_count"],
                "evidence_records": evidence["record_count"],
                "outputs": [str(path) for path in outputs],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
