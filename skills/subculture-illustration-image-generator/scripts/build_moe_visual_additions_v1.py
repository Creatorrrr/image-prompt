#!/usr/bin/env python3
"""Build researched visual-semantics additions without mutating v1-v4 assets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from moe_meaning_contract import contract_sha256
from moe_visual_addition import ADDITION_FILENAME, ADDITION_SCHEMA
from moe_visual_contract import visual_contract_sha256


CREATED_AT = "2026-08-19T00:00:00+09:00"


SOURCES: list[dict[str, str]] = [
    {
        "id": "add_src_ntr_jsscc_2024",
        "kind": "academic",
        "title": "2024 JSSCC conference abstracts: NTR genre study",
        "url": "https://www.jsscc.net/wp/wp-content/uploads/2024_jsscc_23th_abstracts.pdf",
        "publisher": "Japan Society for Studies in Cartoons and Comics",
        "claim_scope": "NTR as a cultural genre derived from netorare and organized around the displaced protagonist viewpoint.",
    },
    {
        "id": "add_src_panchira_kotobank",
        "kind": "dictionary",
        "title": "ぱんちら",
        "url": "https://kotobank.jp/word/%E3%81%B1%E3%82%93%E3%81%A1%E3%82%89-682325",
        "publisher": "Kotobank / Digital Daijisen",
        "claim_scope": "Lexical definition as a brief glimpse of underwear beneath a skirt.",
    },
    {
        "id": "add_src_chirarism_kci",
        "kind": "academic",
        "title": "Chirarism and the aesthetics of a partial glimpse",
        "url": "https://www.kci.or.jp/articles/files/B_FT02_INOUE_Chirarism_JP.pdf",
        "publisher": "Kyoto Costume Institute",
        "claim_scope": "Distinguishes momentary partial visibility from sustained or complete display and discusses the word lineage.",
    },
    {
        "id": "add_src_glasses_imidas",
        "kind": "editorial",
        "title": "Megane moe",
        "url": "https://imidas.jp/ryuko/detail/N-05-2-730-07.html",
        "publisher": "imidas",
        "claim_scope": "Glasses as the identity-salient appeal point of the archetype rather than an incidental prop.",
    },
    {
        "id": "add_src_meganekko_wdic",
        "kind": "community_reference",
        "title": "メガネっ娘",
        "url": "https://www.wdic.org/w/MOE/%E3%83%A1%E3%82%AC%E3%83%8D%E3%81%A3%E5%A8%98",
        "publisher": "通信用語の基礎知識",
        "claim_scope": "Term lineage and the literal glasses-wearing feminine-character core.",
    },
    {
        "id": "add_src_literary_kotobank",
        "kind": "dictionary",
        "title": "文学少女",
        "url": "https://kotobank.jp/word/%E6%96%87%E5%AD%A6%E5%B0%91%E5%A5%B3-1711853",
        "publisher": "Kotobank / Digital Daijisen / Nihon Kokugo Daijiten",
        "claim_scope": "A woman devoted to literature, with literary atmosphere and sometimes literary creation as an aspiration.",
    },
    {
        "id": "add_src_leopard_animate",
        "kind": "editorial",
        "title": "Female leopard pose event report",
        "url": "https://www.animatetimes.com/news/details.php?id=1301984401",
        "publisher": "Animate Times",
        "claim_scope": "Recognizes the named pose as an all-fours or quadrupedal pose convention.",
    },
    {
        "id": "add_src_leopard_crea",
        "kind": "editorial",
        "title": "Gravure pose vocabulary: female leopard pose",
        "url": "https://crea.bunshun.jp/articles/-/48735",
        "publisher": "CREA / Bungeishunju",
        "claim_scope": "Describes kneeling support, arms extended forward, and the upward gaze used in the pose convention.",
    },
    {
        "id": "add_src_cat_yoga_journal",
        "kind": "instructional",
        "title": "Cat Pose (Marjaryasana)",
        "url": "https://yogajournal.jp/pose/62",
        "publisher": "Yoga Journal Online Japan",
        "claim_scope": "Yoga sense: wrists below shoulders, knees below hips, and a rounded spinal phase coordinated with breathing.",
    },
    {
        "id": "add_src_cat_fitpalette",
        "kind": "instructional",
        "title": "Cat pose fitness glossary",
        "url": "https://fitpalette.lotte.co.jp/topics/243",
        "publisher": "Lotte FIT PALETTE",
        "claim_scope": "Confirms cat pose and cat-cow as a quadrupedal exercise sense distinct from portrait posing.",
    },
    {
        "id": "add_src_cat_paw_community",
        "kind": "community_reference",
        "title": "Cat-paw photo pose convention",
        "url": "https://www.lemon8-app.com/user23015580641/7147599909137547781?region=jp",
        "publisher": "Lemon8 community post",
        "claim_scope": "Low-confidence evidence for the separate portrait convention of curled hands held near the cheeks like paws.",
    },
    {
        "id": "add_src_goldsun_everymemes",
        "kind": "community_reference",
        "title": "금태양 slang summary",
        "url": "https://everymemes.tistory.com/322",
        "publisher": "Everymemes",
        "claim_scope": "Community explanation of the abbreviation from blond hair, tanning, and delinquent-coded styling, including its frequent but non-essential NTR association.",
    },
    {
        "id": "add_src_goldsun_ssadic",
        "kind": "community_reference",
        "title": "금태양 user slang dictionary entry",
        "url": "https://ssadic.com/%EB%9C%BB/%EA%B8%88%ED%83%9C%EC%96%91/",
        "publisher": "SSADIC",
        "claim_scope": "Secondary community record of the same abbreviation; not evidence of prevalence or a fixed personality.",
    },
    {
        "id": "add_src_gumiho_krdict",
        "kind": "dictionary",
        "title": "구미호",
        "url": "https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=35014",
        "publisher": "National Institute of Korean Language",
        "claim_scope": "Korean lexical core: a nine-tailed fox of old stories that can beguile or deceive people.",
    },
    {
        "id": "add_src_gumiho_kocis",
        "kind": "editorial",
        "title": "K-story: Gumiho, the nine-tailed fox",
        "url": "https://www.mcst.go.kr/english/policy/kocis/newsView.jsp?pSeq=102",
        "publisher": "Ministry of Culture, Sports and Tourism / KOCIS",
        "claim_scope": "Folklore lineage, human shapeshifting, and the optional fox-bead motif in Korean retellings.",
    },
    {
        "id": "add_src_gumiho_heritage",
        "kind": "editorial",
        "title": "Nine-tailed foxes in Korean folklore",
        "url": "https://www.kh.or.kr/brd/board/741/l/menu/740?bbIdx=112290&brdType=R&searchField=&searchText=&thisPage=1",
        "publisher": "Korea Heritage Agency",
        "claim_scope": "Older-fox spirit lineage and variation across tales; literal tail count is a strong identifier but not every human-form scene exposes all nine.",
    },
    {
        "id": "add_src_dragon_nmok",
        "kind": "editorial",
        "title": "Dragon among clouds and water",
        "url": "https://www.museum.go.kr/JPN/contents/E0403000000.do?relicId=883&schM=view&searchId=search",
        "publisher": "National Museum of Korea",
        "claim_scope": "Korean dragon imagery as a long coiling cloud-and-water being associated with auspicious and royal symbolism.",
    },
    {
        "id": "add_src_dragon_getty",
        "kind": "editorial",
        "title": "Dragons in medieval manuscripts",
        "url": "https://www.getty.edu/art/mobile/center/beasts/stop.php?id=952689",
        "publisher": "J. Paul Getty Museum",
        "claim_scope": "European manuscript dragons commonly combine scales, claws, long tails, and batlike wings, with leg count and fire-breathing varying.",
    },
    {
        "id": "add_src_dokkaebi_aks",
        "kind": "academic",
        "title": "도깨비",
        "url": "https://encykorea.aks.ac.kr/Article/E0015527",
        "publisher": "Academy of Korean Studies",
        "claim_scope": "Dokkaebi are not dead-person ghosts, have no single fixed appearance, and can arise from old objects or natural matter in varied tales.",
    },
    {
        "id": "add_src_dokkaebi_korea_net",
        "kind": "editorial",
        "title": "K-story: Dokkaebi",
        "url": "https://www.korea.net/Events/Overseas/view?articleId=9497",
        "publisher": "Korea.net",
        "claim_scope": "Playful trickster behavior and the treasure-producing club motif, without reducing dokkaebi to a uniformly evil monster.",
    },
    {
        "id": "add_src_ghost_cambridge",
        "kind": "dictionary",
        "title": "ghost",
        "url": "https://dictionary.cambridge.org/us/dictionary/english/ghost",
        "publisher": "Cambridge University Press",
        "claim_scope": "A spirit of a dead person, often represented as a pale or nearly transparent human image.",
    },
    {
        "id": "add_src_ghost_va",
        "kind": "editorial",
        "title": "A brief history of ghosts and spirit photography",
        "url": "https://www.vam.ac.uk/articles/a-brief-history-of-ghosts-and-spirit-photography",
        "publisher": "Victoria and Albert Museum",
        "claim_scope": "Historical visual conventions for apparitions, including translucent overlays and bodily likeness rather than one mandatory costume.",
    },
    {
        "id": "add_src_robot_iso",
        "kind": "instructional",
        "title": "ISO 8373:2021 Robotics vocabulary",
        "url": "https://www.iso.org/standard/75539.html?browse=tc",
        "publisher": "International Organization for Standardization",
        "claim_scope": "Robot as a programmed actuated mechanism with a degree of autonomy for movement, manipulation, or positioning.",
    },
    {
        "id": "add_src_robot_ifr",
        "kind": "instructional",
        "title": "World Robotics 2025 sources and methods",
        "url": "https://ifr.org/img/worldrobotics/Sources___Methods_WR_2025_Industrial_Robots.pdf",
        "publisher": "International Federation of Robotics",
        "claim_scope": "Operational adoption of ISO robot vocabulary and the distinction between industrial and service-robot embodiments.",
    },
    {
        "id": "add_src_assassin_mw",
        "kind": "dictionary",
        "title": "assassin",
        "url": "https://www.merriam-webster.com/dictionary/assassin",
        "publisher": "Merriam-Webster",
        "claim_scope": "A person who deliberately murders a prominent target, often for money or a cause; the role has no necessary costume.",
    },
    {
        "id": "add_src_soldier_cambridge",
        "kind": "dictionary",
        "title": "soldier",
        "url": "https://dictionary.cambridge.org/us/dictionary/english/soldier",
        "publisher": "Cambridge University Press",
        "claim_scope": "A member of an army, commonly distinguished by military uniform.",
    },
    {
        "id": "add_src_soldier_icrc",
        "kind": "instructional",
        "title": "Uniform glossary",
        "url": "https://casebook.icrc.org/a_to_z/glossary/uniform",
        "publisher": "International Committee of the Red Cross",
        "claim_scope": "Uniforms identify membership in the same military unit through shared design, color, and insignia; camouflage remains a uniform.",
    },
    {
        "id": "add_src_pilot_cambridge",
        "kind": "dictionary",
        "title": "pilot",
        "url": "https://dictionary.cambridge.org/us/dictionary/english/pilot",
        "publisher": "Cambridge University Press",
        "claim_scope": "The aircraft sense is a person who flies an aircraft, distinct from maritime and trial-program senses.",
    },
    {
        "id": "add_src_pilot_faa",
        "kind": "instructional",
        "title": "Pilot's Handbook of Aeronautical Knowledge",
        "url": "https://www.faa.gov/sites/faa.gov/files/pilots/pilot_handbook.pdf",
        "publisher": "Federal Aviation Administration",
        "claim_scope": "Flight-control contact, primary flight displays, navigation displays, and cockpit instrument relationships that visually evidence aircraft operation.",
    },
    {
        "id": "add_src_tights_cambridge",
        "kind": "dictionary",
        "title": "tights",
        "url": "https://dictionary.cambridge.org/us/dictionary/english/tights",
        "publisher": "Cambridge University Press",
        "claim_scope": "A close-fitting garment covering the body from the waist through both legs, often to the feet; British usage overlaps pantyhose.",
    },
    {
        "id": "add_src_tights_va",
        "kind": "editorial",
        "title": "Knitted underwear and tights",
        "url": "https://www.vam.ac.uk/articles/knitted-underwear",
        "publisher": "Victoria and Albert Museum",
        "claim_scope": "Historical construction of joined waist-high legwear and the smooth close fit enabled by elastic fibers.",
    },
    {
        "id": "add_src_bandage_cambridge",
        "kind": "dictionary",
        "title": "bandage",
        "url": "https://dictionary.cambridge.org/us/dictionary/english/bandage",
        "publisher": "Cambridge University Press",
        "claim_scope": "A long narrow piece of cloth wrapped around an injured body part for protection or support.",
    },
    {
        "id": "add_src_bandage_redcross",
        "kind": "instructional",
        "title": "First Aid/CPR/AED Participant's Manual",
        "url": "https://www.redcross.org/content/dam/redcross/training-services/no-index/First%20Aid-CPR-AED-Participant%27s-Manual.pdf",
        "publisher": "American Red Cross",
        "claim_scope": "A roller bandage secures a dressing through overlapping turns and a visible fastened end while remaining snug rather than excessively tight.",
    },
]


def _alias(alias: str, relation: str = "exact", variant_id: str | None = None) -> dict[str, Any]:
    return {"alias": alias, "relation": relation, "variant_id": variant_id}


def _axis(axis_id: str, description: str, values: list[tuple[str, list[str]]]) -> dict[str, Any]:
    return {
        "id": axis_id,
        "description": description,
        "values": [
            {"id": value_id, "label": value_id, "request_cues": cues}
            for value_id, cues in values
        ],
    }


def _meaning(
    *,
    element_id: str,
    ordinal: int,
    definition: str,
    essential: list[str],
    non_equivalents: list[str],
    axes: list[str],
    label_policy: str,
    forbidden_labels: list[str],
    fidelity: str,
    groups: list[tuple[str, int, list[str]]],
    optional: list[str],
    false_substitutes: list[str],
    do_not_infer: list[str],
    adult_requirement: str,
    single_frame: str = "exact",
    sequence: str = "not_required",
) -> dict[str, Any]:
    return {
        "element_id": element_id,
        "ordinal": ordinal,
        "source_dossier": "visual_additions",
        "canonical_definition_ko": definition,
        "essential_semantics_ko": essential,
        "non_equivalents_ko": non_equivalents,
        "semantic_axes": axes,
        "runtime_label_policy": label_policy,
        "runtime_forbidden_labels": forbidden_labels,
        "semantic_fidelity": fidelity,
        "component_groups": [
            {"id": group_id, "minimum": minimum, "alternatives_en": alternatives}
            for group_id, minimum, alternatives in groups
        ],
        "optional_components_en": optional,
        "false_substitutes_en": false_substitutes,
        "do_not_infer_en": do_not_infer,
        "adult_requirement": adult_requirement,
        "capability": {
            "single_frame": single_frame,
            "sequence": sequence,
            "interaction": "not_required",
        },
    }


def _candidate(
    *,
    element_id: str,
    slug: str,
    subtype_id: str,
    novelty: int,
    canonical: bool,
    representation_mode: str,
    integration_role: str,
    cues: list[str],
    preference_profile: dict[str, str],
    prompt: str,
    evidence: list[str],
    claim_ids: list[str],
    limitation: str,
    tags: list[str],
) -> dict[str, Any]:
    candidate_id = f"moe_candidate_{element_id.removeprefix('moe_')}_{slug}"
    supports = [
        {
            "id": f"moe_atom_{element_id.removeprefix('moe_')}_{slug}_support_{index}",
            "prompt_fragment_en": f"Keep this literal visual fact: {item}.",
            "observable_evidence": [item],
        }
        for index, item in enumerate(evidence[:3], 1)
    ]
    return {
        "id": candidate_id,
        "label_en": slug.replace("_", " "),
        "subtype_id": subtype_id,
        "novelty_level": novelty,
        "canonical_default": canonical,
        "intent_keys": [f"visual_addition.{element_id}.{subtype_id}"],
        "representation_mode": representation_mode,
        "integration_role": integration_role,
        "selection_cues": cues,
        "preference_profile": preference_profile,
        "primary_atom": {
            "id": f"moe_atom_{element_id.removeprefix('moe_')}_{slug}_primary",
            "prompt_fragment_en": prompt,
            "observable_evidence": evidence,
        },
        "support_atoms": supports,
        "resource_claims": ["focal_primary|scene|1|exclusive", "event_peak|scene|1|shared"],
        "compatibility_tags": tags,
        "source_claim_ids": claim_ids,
        "limitation": limitation,
    }


def _variant(
    *,
    variant_id: str,
    subtype_ids: list[str],
    group_ids: list[str],
    all_of: list[str],
    any_of: list[str],
    any_minimum: int,
    topology: list[str],
    camera: list[str],
    temporal: list[str],
    interaction: list[str],
    confounds: list[str],
    modes: list[str],
) -> dict[str, Any]:
    return {
        "id": variant_id,
        "candidate_subtype_ids": subtype_ids,
        "required_component_group_ids": group_ids,
        "all_of_en": all_of,
        "any_of": {"minimum": any_minimum, "alternatives_en": any_of},
        "topology_edges_en": topology,
        "camera_requirements_en": camera,
        "temporal_states_en": temporal,
        "interaction_requirements_en": interaction,
        "negative_visual_confounds_en": confounds,
        "supported_output_modes": modes,
    }


def _compatibility(
    element_id: str,
    *,
    frame: str,
    camera: str,
    mechanisms: list[str],
    tags: list[str],
) -> dict[str, Any]:
    return {
        "element_id": element_id,
        "frame_requirement_id": frame,
        "camera_profile_id": camera,
        "mechanism_node_ids": mechanisms,
        "resource_claims": [["focal_primary", "scene", 1, "exclusive"], ["event_peak", "scene", 1, "shared"]],
        "capability_requirements": [],
        "rule_tags": tags,
        "fallback_rule_ids": ["fallback_camera_widen", "fallback_demote_support"],
    }


def _claims(*rows: tuple[str, str, list[str], str]) -> list[dict[str, Any]]:
    return [
        {"id": claim_id, "claim_ko": claim, "source_ids": source_ids, "confidence": confidence}
        for claim_id, claim, source_ids, confidence in rows
    ]


def _evidence(
    evidence_id: str,
    *,
    queries: list[str],
    confidence: str,
    recurring: list[str],
    confounds: list[str],
    urls: list[str],
    limitations: list[str],
) -> dict[str, Any]:
    return {
        "id": evidence_id,
        "queries": queries,
        "search_confidence": confidence,
        "recurring_features_en": recurring,
        "observed_confounds_en": confounds,
        "representative_source_urls": urls,
        "limitations_en": limitations,
    }


def _new_profile(
    *,
    element_id: str,
    ordinal: int,
    category: str,
    label_ko: str,
    label_en: str,
    aliases: list[dict[str, Any]],
    summary: str,
    claims: list[dict[str, Any]],
    evidence: dict[str, Any],
    meaning: dict[str, Any],
    axes: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    default_variant_id: str,
    variants: list[dict[str, Any]],
    compatibility: dict[str, Any],
) -> dict[str, Any]:
    visual = {
        "element_id": element_id,
        "ordinal": ordinal,
        "base_contract_sha256": contract_sha256(meaning),
        "default_variant_id": default_variant_id,
        "alias_bindings": aliases,
        "visual_variants": variants,
        "image_evidence_id": evidence["id"],
    }
    return {
        "element_id": element_id,
        "ordinal": ordinal,
        "mode": "new_element",
        "category": category,
        "label_ko": label_ko,
        "label_en": label_en,
        "aliases": aliases,
        "research_summary_ko": summary,
        "claims": claims,
        "research_evidence": evidence,
        "meaning_contract": meaning,
        "meaning_contract_sha256": contract_sha256(meaning),
        "preference_axes": axes,
        "candidates": candidates,
        "visual_meaning_contract": visual,
        "visual_meaning_contract_sha256": visual_contract_sha256(visual),
        "compatibility_profile": compatibility,
    }


def _ntr_refinement(base_element: dict[str, Any]) -> dict[str, Any]:
    element_id = "moe_ntr_relationship_displacement"
    aliases = [
        _alias("NTR"),
        _alias("네토라레", "variant", "established_bond_displaced_view"),
        _alias("寝取られ", "variant", "established_bond_displaced_view"),
        _alias("relationship displacement triangle", "related"),
        _alias("네토리", "variant", "initiator_capture_view"),
        _alias("寝取り", "variant", "initiator_capture_view"),
        _alias("네토라세", "variant", "arranged_handoff_view"),
        _alias("寝取らせ", "variant", "arranged_handoff_view"),
        _alias("BSS", "variant", "unrealized_missed_chance_view"),
        _alias("내가 먼저 좋아했는데", "variant", "unrealized_missed_chance_view"),
    ]
    groups = [group["id"] for group in base_element["meaning_contract"]["component_groups"]]
    confounds = list(base_element["meaning_contract"]["false_substitutes_en"])
    variants = [
        _variant(
            variant_id="established_bond_displaced_view",
            subtype_ids=["netorare_displaced_partner"],
            group_ids=groups,
            all_of=["three clearly differentiated adult relationship roles", "one repeated bond token linking the original pair before the shift"],
            any_of=["displaced partner isolated from the changed pair", "the repeated bond token now placed with the changed pair"],
            any_minimum=1,
            topology=["an established pair edge is interrupted by a new third-party pair edge while the displaced adult remains visible"],
            camera=["wide relational framing that keeps all three adult roles and their distances readable"],
            temporal=["established prior bond", "changed pair", "loss consequence from the displaced viewpoint"],
            interaction=[],
            confounds=confounds,
            modes=["paired_frame", "sequence"],
        ),
        _variant(
            variant_id="initiator_capture_view",
            subtype_ids=["netori_initiator"],
            group_ids=groups,
            all_of=["three clearly differentiated adult relationship roles", "the initiating third party actively redirects the previously bonded partner's attention"],
            any_of=["the initiator owns the dominant approach vector", "the displaced partner sees the attention shift"],
            any_minimum=1,
            topology=["the initiating adult creates a new pair edge without erasing the visible prior-bond evidence"],
            camera=["relational medium-wide framing centered on the initiating action and both affected adults"],
            temporal=["prior pair", "initiating attention capture", "new pair alignment"],
            interaction=[],
            confounds=confounds,
            modes=["paired_frame", "sequence"],
        ),
        _variant(
            variant_id="arranged_handoff_view",
            subtype_ids=["netorase_arranged"],
            group_ids=groups,
            all_of=["three clearly differentiated adult relationship roles", "an explicit arrangement cue visible before the relationship handoff"],
            any_of=["a prior agreement token shared by the original pair", "the arranging partner visibly initiates the handoff"],
            any_minimum=1,
            topology=["the original pair edge remains acknowledged while one partner is deliberately connected to the third adult"],
            camera=["wide framing that keeps the arrangement cue and all three adult roles visible"],
            temporal=["explicit arrangement", "relationship handoff", "resulting role positions"],
            interaction=[],
            confounds=confounds,
            modes=["paired_frame", "sequence"],
        ),
        _variant(
            variant_id="unrealized_missed_chance_view",
            subtype_ids=["bss_missed_chance_witness", "bss_unrealized_love"],
            group_ids=groups,
            all_of=["three adult roles with no established-couple token for the late witness", "an unopened confession or private keepsake proving the unrealized bond"],
            any_of=["the too-late witness arrives after the new pair forms", "the unopened confession remains physically separated from the new pair"],
            any_minimum=1,
            topology=["an unrealized one-way bond ends at the late witness while a mutually visible new pair edge connects the other two adults"],
            camera=["wide enough framing to separate the late witness, unrealized-bond token, and new pair"],
            temporal=["unspoken attachment", "missed timing", "new pair witnessed too late"],
            interaction=[],
            confounds=confounds,
            modes=["paired_frame", "sequence"],
        ),
        _variant(
            variant_id="shift_or_discovery_view",
            subtype_ids=["gradual_bond_displacement", "discovery_and_aftershock"],
            group_ids=groups,
            all_of=["three clearly differentiated adult relationship roles", "the same bond token changes placement or use across the sequence"],
            any_of=["attention progressively shifts toward the third adult", "the displaced partner discovers the changed pair through concrete evidence"],
            any_minimum=1,
            topology=["the prior pair edge visibly weakens or breaks as the third-party edge becomes dominant"],
            camera=["matched relational framing across the shift or discovery states"],
            temporal=["prior bond", "observable attention shift or discovery evidence", "aftermath for the displaced adult"],
            interaction=[],
            confounds=confounds,
            modes=["paired_frame", "sequence"],
        ),
    ]
    evidence = _evidence(
        "moe_add_image_evidence_ntr",
        queries=["NTR netorare relationship viewpoint visual storytelling non explicit", "netori netorase BSS relationship topology illustration"],
        confidence="medium",
        recurring=["three differentiated adult roles", "prior-bond or unrealized-bond token", "changed pair topology", "displaced or late-witness viewpoint"],
        confounds=confounds,
        urls=["https://www.jsscc.net/wp/wp-content/uploads/2024_jsscc_23th_abstracts.pdf"],
        limitations=["The academic source supports genre lineage and viewpoint, not a universal fixed costume or character design.", "Visual topology is a design synthesis and still needs rendered-pixel review."],
    )
    visual = {
        "element_id": element_id,
        "ordinal": int(base_element["ordinal"]),
        "base_contract_sha256": base_element["meaning_contract_sha256"],
        "default_variant_id": "established_bond_displaced_view",
        "alias_bindings": aliases,
        "visual_variants": variants,
        "image_evidence_id": evidence["id"],
    }
    return {
        "element_id": element_id,
        "ordinal": int(base_element["ordinal"]),
        "mode": "existing_refinement",
        "category": base_element["category"],
        "label_ko": base_element["label_ko"],
        "label_en": "NTR relationship displacement",
        "aliases": aliases,
        "research_summary_ko": "NTR은 고정 외형이 아니라 기존·기대 관계, 제3자, 관점과 상실 결과로 성립한다. 네토라레·네토리·네토라세·BSS를 동의나 기존 관계가 같은 것으로 합치지 않는다.",
        "claims": _claims(("moe_add_claim_ntr_viewpoint", "NTR은 네토라레에서 파생된 장르 계열이며 빼앗긴 쪽의 무력한 관점이 중요한 계보다.", ["add_src_ntr_jsscc_2024"], "medium")),
        "research_evidence": evidence,
        "meaning_contract": None,
        "meaning_contract_sha256": base_element["meaning_contract_sha256"],
        "preference_axes": [],
        "candidates": [],
        "visual_meaning_contract": visual,
        "visual_meaning_contract_sha256": visual_contract_sha256(visual),
        "compatibility_profile": None,
    }


def _female_leopard_profile() -> dict[str, Any]:
    element_id = "moe_female_leopard_pose"
    aliases = [_alias("암표범 자세"), _alias("여표범 포즈"), _alias("女豹のポーズ"), _alias("female leopard pose"), _alias("일반 네발 자세", "related")]
    false = ["ordinary crawling", "neutral tabletop yoga pose", "animal transformation", "cropped torso without support limbs"]
    meaning = _meaning(
        element_id=element_id,
        ordinal=30,
        definition="암표범 자세·여표범 포즈는 성인 여성이 손 또는 팔뚝과 무릎으로 몸을 지지하면서 상체를 낮추고 골반을 더 높게 두며, 등허리 곡선과 들어 올린 머리·시선으로 감각적인 네발 실루엣을 만드는 포즈 관습이다.",
        essential=["성인 여성의 네발 지지", "상체보다 높은 골반", "이어지는 등허리 곡선", "들린 머리와 카메라 방향 시선"],
        non_equivalents=["이동 중인 일반 기어가기", "손목과 무릎이 수직인 중립 요가 테이블탑", "고양이나 표범으로 변신한 인물", "지지 팔다리가 잘린 엎드린 상반신"],
        axes=["forelimb_support", "torso_pelvis_height_delta", "spinal_curve", "gaze_direction"],
        label_policy="omit",
        forbidden_labels=["암표범 자세", "여표범 포즈", "女豹のポーズ", "female leopard pose"],
        fidelity="exact_componentized",
        groups=[("four_point_support", 2, ["both knees supporting the body", "both hands supporting the body", "both forearms supporting the lowered upper body"]), ("lowered_front_high_pelvis", 2, ["upper torso lower than the pelvis", "pelvis visibly higher than the shoulders", "continuous arched lower-back curve"]), ("lifted_head_gaze", 1, ["head lifted from the lowered torso", "eyes directed toward the camera"])],
        optional=["extended forearms", "three-quarter silhouette", "controlled confident expression"],
        false_substitutes=false,
        do_not_infer=["sexual activity", "animal identity", "submissive role", "pain or restraint"],
        adult_requirement="explicit_adult_always",
    )
    claims = _claims(
        ("moe_add_claim_leopard_support", "일본 연예·그라비아 용례에서 이 포즈는 네발 지지로 인식된다.", ["add_src_leopard_animate", "add_src_leopard_crea"], "medium"),
        ("moe_add_claim_leopard_geometry", "대표 설명에는 무릎을 대고 팔을 앞으로 뻗으며 얼굴과 시선을 드는 구성이 반복된다.", ["add_src_leopard_crea"], "medium"),
    )
    candidates = [
        _candidate(element_id=element_id, slug="canonical_lowered_forequarters", subtype_id="lowered_forequarters_high_pelvis", novelty=1, canonical=True, representation_mode="single_frame", integration_role="pose", cues=["정면", "상체를 낮춘", "시선"], preference_profile={"forelimb_support": "hands", "viewpoint": "front_three_quarter"}, prompt="Pose one clearly adult woman on both hands and both knees, lowering her upper torso below a visibly higher pelvis while preserving one continuous arched lower-back curve and lifting her head toward the camera.", evidence=["both hands supporting the body", "both knees supporting the body", "upper torso lower than the pelvis", "eyes directed toward the camera"], claim_ids=["moe_add_claim_leopard_support", "moe_add_claim_leopard_geometry"], limitation="A generic quadrupedal pose without the height delta, curve, and lifted gaze is insufficient.", tags=["full_body_pose", "adult_only", "single_frame_geometry"]),
        _candidate(element_id=element_id, slug="forearm_supported_silhouette", subtype_id="forearm_supported_high_pelvis", novelty=0, canonical=False, representation_mode="single_frame", integration_role="pose", cues=["팔뚝 지지", "더 낮은 상체", "측면"], preference_profile={"forelimb_support": "forearms", "viewpoint": "side_three_quarter"}, prompt="Show one clearly adult woman supported by both forearms and both knees, with her chest lowered, pelvis higher than the shoulders, a continuous back curve, and her head lifted enough to keep the gaze readable.", evidence=["both forearms supporting the lowered upper body", "both knees supporting the body", "pelvis visibly higher than the shoulders", "head lifted from the lowered torso"], claim_ids=["moe_add_claim_leopard_support", "moe_add_claim_leopard_geometry"], limitation="Do not crop away the forearms, knees, or pelvis-to-shoulder height relationship.", tags=["full_body_pose", "adult_only", "silhouette_continuity"]),
        _candidate(element_id=element_id, slug="diagonal_full_body_pose", subtype_id="diagonal_full_body_high_pelvis", novelty=2, canonical=False, representation_mode="single_frame", integration_role="pose", cues=["대각선", "전신", "드라마틱"], preference_profile={"forelimb_support": "hands", "viewpoint": "diagonal_full_body"}, prompt="Frame one clearly adult woman diagonally in full body on both hands and both knees; keep the lowered front, higher pelvis, uninterrupted S-like back line, and lifted camera-facing gaze simultaneously legible.", evidence=["both hands supporting the body", "both knees supporting the body", "continuous arched lower-back curve", "head lifted from the lowered torso"], claim_ids=["moe_add_claim_leopard_support", "moe_add_claim_leopard_geometry"], limitation="Dramatic perspective may not hide or anatomically break any support limb.", tags=["full_body_pose", "adult_only", "camera_diagonal"]),
    ]
    variant = _variant(variant_id="lowered_forequarters_high_pelvis", subtype_ids=[candidate["subtype_id"] for candidate in candidates], group_ids=[group["id"] for group in meaning["component_groups"]], all_of=["one clearly adult woman supported by both knees and by both hands or both forearms", "upper torso visibly lower than the pelvis", "continuous arched lower-back line", "head lifted with readable camera-directed eyes"], any_of=["extended forearms lengthening the front silhouette", "three-quarter view preserving the pelvis-to-shoulder height delta"], any_minimum=1, topology=["support runs continuously from each foreground hand or forearm through the shoulders and spine to both grounded knees"], camera=["uncropped full-body or near-full-body framing with all support points visible"], temporal=[], interaction=[], confounds=false, modes=["single_frame", "paired_frame", "sequence"])
    return _new_profile(element_id=element_id, ordinal=30, category="body_pose", label_ko="암표범 자세·여표범 포즈", label_en="female leopard pose", aliases=aliases, summary="정의 자료와 연예·그라비아 용례를 교차해 네발 지지, 낮은 상체, 높은 골반, 등허리 곡선, 들린 시선을 핵심으로 삼았다. 일반 기어가기·요가 자세와 구분한다.", claims=claims, evidence=_evidence("moe_add_image_evidence_leopard", queries=["女豹のポーズ 四つん這い 腕 前 視線", "female leopard pose all fours full body non explicit"], confidence="medium", recurring=["hands or forearms plus knees support", "upper torso lower than pelvis", "arched lower-back silhouette", "lifted gaze"], confounds=false, urls=["https://www.animatetimes.com/news/details.php?id=1301984401", "https://crea.bunshun.jp/articles/-/48735"], limitations=["Entertainment examples describe a convention rather than a biomechanical standard.", "All runtime realizations are restricted to clearly adult, non-explicit fictional subjects."]), meaning=meaning, axes=[_axis("forelimb_support", "front support geometry", [("hands", ["손으로 지지", "손바닥" ]), ("forearms", ["팔뚝 지지", "전완"]) ]), _axis("viewpoint", "camera relationship", [("front_three_quarter", ["정면", "시선"]), ("side_three_quarter", ["측면", "실루엣"]), ("diagonal_full_body", ["대각선", "전신"])])], candidates=candidates, default_variant_id="lowered_forequarters_high_pelvis", variants=[variant], compatibility=_compatibility(element_id, frame="single_frame", camera="camera_full_body_three_quarter", mechanisms=["pose_invariant_landmarks", "thumbnail_outer_contour"], tags=["full_body_pose", "adult_only", "primary_composition_owner"]))


def _cat_pose_profile() -> dict[str, Any]:
    element_id = "moe_cat_pose_family"
    aliases = [_alias("고양이 자세", "ambiguous"), _alias("cat pose", "ambiguous"), _alias("고양이 네발 자세", "variant", "catlike_all_fours"), _alias("고양이 발 포즈", "variant", "cat_paw_portrait"), _alias("냥냥 포즈", "variant", "cat_paw_portrait"), _alias("고양이 요가 자세", "variant", "yoga_cat_pose"), _alias("마르자리아사나", "variant", "yoga_cat_pose"), _alias("Marjaryasana", "variant", "yoga_cat_pose"), _alias("cat-cow pose", "variant", "yoga_cat_pose")]
    false = ["using the ambiguous label without choosing a sense", "animal ears alone", "ordinary standing portrait", "female leopard height-delta silhouette substituted for yoga"]
    meaning = _meaning(element_id=element_id, ordinal=31, definition="고양이 자세는 문맥에 따라 성인의 고양이 같은 네발 포즈, 얼굴 옆에서 손가락을 둥글게 말아 앞발을 흉내 내는 인물 포즈, 또는 네발 기초자세에서 척추를 둥글게 만드는 요가 자세를 가리키는 모호한 표현이다. 세 계보의 신체 구조를 섞지 않는다.", essential=["세 계보 중 하나의 명시적 선택", "선택 계보에 맞는 지지점 또는 손 모양", "고양이를 연상시키는 구체적 동작"], non_equivalents=["고양이 귀만 단 정면 인물", "암표범 자세의 감각적 높이차를 요가로 부르는 것", "아무 네발 자세", "고양이 동물 자체"], axes=["pose_lineage", "support_geometry", "hand_shape", "spinal_phase"], label_policy="allow", forbidden_labels=[], fidelity="exact_componentized", groups=[("lineage_specific_geometry", 1, ["hands and knees in a neutral quadruped base", "both hands curled beside the face like front paws", "wrists under shoulders and knees under hips on an exercise mat"]), ("cat_reference_action", 1, ["supple catlike spine and alert lifted head", "rounded fingers visibly imitating paws", "rounded spinal phase with the navel-facing gaze"])], optional=["playful expression", "exercise mat", "neutral tail-like clothing rhythm"], false_substitutes=false, do_not_infer=["animal identity", "sexual intent from a quadruped pose", "yoga from the words cat pose alone", "youth from the Korean or Japanese archetype label"], adult_requirement="explicit_adult_if_suggestive")
    claims = _claims(("moe_add_claim_cat_yoga", "요가의 고양이 자세는 손목을 어깨 아래, 무릎을 골반 아래에 두고 척추를 둥글게 하는 네발 운동 계보다.", ["add_src_cat_yoga_journal", "add_src_cat_fitpalette"], "high"), ("moe_add_claim_cat_paw", "인물 사진의 고양이 발 포즈는 얼굴 옆에서 손가락을 말아 앞발을 흉내 내는 별도 관습으로 쓰인다.", ["add_src_cat_paw_community"], "low"), ("moe_add_claim_cat_ambiguity", "같은 cat pose 표현이 요가와 인물 포즈에 모두 쓰이므로 문맥 없는 단독어는 한 의미로 확정하기 어렵다.", ["add_src_cat_yoga_journal", "add_src_cat_paw_community"], "medium"))
    candidates = [
        _candidate(element_id=element_id, slug="catlike_all_fours", subtype_id="catlike_all_fours", novelty=1, canonical=True, representation_mode="single_frame", integration_role="pose", cues=["네발", "기민한", "등을 부드럽게"], preference_profile={"pose_lineage": "all_fours", "spinal_phase": "supple"}, prompt="Show one clearly adult character on both hands and both knees in a neutral quadruped base, with a supple catlike spine and alert lifted head; keep the pose playful and non-explicit without the lowered-front, high-pelvis silhouette of the separate sensual pose.", evidence=["hands and knees in a neutral quadruped base", "supple catlike spine and alert lifted head", "four support points visible"], claim_ids=["moe_add_claim_cat_ambiguity"], limitation="This lineage must not silently become yoga or the separate high-pelvis sensual pose.", tags=["full_body_pose", "lineage_selected", "adult_subject"]),
        _candidate(element_id=element_id, slug="cat_paw_portrait", subtype_id="cat_paw_portrait", novelty=0, canonical=False, representation_mode="single_frame", integration_role="pose", cues=["냥냥", "발 포즈", "얼굴 옆"], preference_profile={"pose_lineage": "paw_portrait", "hand_shape": "curled"}, prompt="Frame one clearly adult character in a portrait with both hands curled beside the face like front paws, making the rounded fingers visibly imitate paws while keeping both wrists, fingertips, and the face unobscured.", evidence=["both hands curled beside the face like front paws", "rounded fingers visibly imitating paws", "face and fingertips simultaneously visible"], claim_ids=["moe_add_claim_cat_paw", "moe_add_claim_cat_ambiguity"], limitation="Cat ears, filters, or a smile alone do not establish the hand-pose lineage.", tags=["portrait_pose", "lineage_selected", "adult_subject"]),
        _candidate(element_id=element_id, slug="yoga_cat_pose", subtype_id="yoga_cat_pose", novelty=2, canonical=False, representation_mode="paired_or_sequence", integration_role="pose", cues=["요가", "마르자리아사나", "호흡", "등을 둥글게"], preference_profile={"pose_lineage": "yoga", "spinal_phase": "rounded"}, prompt="Place one clearly adult exerciser on a mat with wrists under shoulders and knees under hips, then show the rounded spinal phase with the navel-facing gaze and a neutral return state synchronized to breathing.", evidence=["wrists under shoulders and knees under hips on an exercise mat", "rounded spinal phase with the navel-facing gaze", "neutral quadruped return state"], claim_ids=["moe_add_claim_cat_yoga", "moe_add_claim_cat_ambiguity"], limitation="Do not replace the exercise alignment with a glamour pose or high-pelvis silhouette.", tags=["exercise_pose", "lineage_selected", "paired_motion"]),
    ]
    groups = [group["id"] for group in meaning["component_groups"]]
    variants = [
        _variant(variant_id="catlike_all_fours", subtype_ids=["catlike_all_fours"], group_ids=groups, all_of=["one clearly adult character with both hands and both knees grounded", "neutral quadruped support with a supple catlike spine and alert lifted head"], any_of=["playful forward gaze", "one shoulder or hip subtly advanced like a poised cat"], any_minimum=1, topology=["each hand connects through its arm and shoulder to one continuous torso ending at two grounded knees"], camera=["full-body or three-quarter framing that shows all four support points"], temporal=[], interaction=[], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
        _variant(variant_id="cat_paw_portrait", subtype_ids=["cat_paw_portrait"], group_ids=groups, all_of=["one clearly adult face and both hands visible", "both hands curled beside the cheeks with rounded fingers imitating front paws"], any_of=["playful smile", "slightly asymmetric paw heights"], any_minimum=1, topology=["the two curled hands flank rather than cover the face"], camera=["head-and-hands portrait with every fingertip inside frame"], temporal=[], interaction=[], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
        _variant(variant_id="yoga_cat_pose", subtype_ids=["yoga_cat_pose"], group_ids=groups, all_of=["one clearly adult exerciser with wrists vertically below shoulders and knees below hips", "rounded spine with pelvis tucked and gaze directed toward the navel"], any_of=["neutral tabletop comparison state", "breathing phase cue"], any_minimum=1, topology=["a stable four-point base supports a continuous rounded spinal arc"], camera=["side three-quarter exercise view showing wrists, shoulders, hips, knees, and spinal curve"], temporal=["neutral tabletop", "exhaled rounded-spine phase"], interaction=[], confounds=false, modes=["paired_frame", "sequence"]),
    ]
    return _new_profile(element_id=element_id, ordinal=31, category="body_pose", label_ko="고양이 자세 계열", label_en="cat pose family", aliases=aliases, summary="단독어가 요가·네발 인물 포즈·고양이 발 흉내를 모두 가리키므로 모호어로 저장하고, 변형 별칭 또는 canonical ID를 통해 계보를 선택하게 했다.", claims=claims, evidence=_evidence("moe_add_image_evidence_cat_pose", queries=["고양이 자세 인물 포즈", "猫の手 ポーズ 顔", "猫のポーズ マルジャリャーサナ 四つん這い"], confidence="medium", recurring=["quadruped all-fours support in body-pose senses", "curled hands beside the face in portrait sense", "wrists-under-shoulders alignment in yoga sense"], confounds=false, urls=["https://yogajournal.jp/pose/62", "https://fitpalette.lotte.co.jp/topics/243", "https://www.lemon8-app.com/user23015580641/7147599909137547781?region=jp"], limitations=["The portrait convention is supported by community material and has low confidence.", "The bare Korean or English label remains ambiguous and is intentionally non-activating."]), meaning=meaning, axes=[_axis("pose_lineage", "which homonymous pose family is intended", [("all_fours", ["네발", "기민한"]), ("paw_portrait", ["냥냥", "고양이 발", "얼굴 옆"]), ("yoga", ["요가", "마르자리아사나", "호흡"])]), _axis("spinal_phase", "spine treatment", [("supple", ["부드러운 등선", "기민한"]), ("rounded", ["등을 둥글게", "배꼽을 보는"])])], candidates=candidates, default_variant_id="catlike_all_fours", variants=variants, compatibility=_compatibility(element_id, frame="single_frame", camera="camera_full_body_three_quarter", mechanisms=["pose_invariant_landmarks", "identity_face_feature_anchor"], tags=["ambiguous_alias_fail_closed", "variant_lineage", "adult_if_suggestive"]))


def _brief_glimpse_profile() -> dict[str, Any]:
    element_id = "moe_brief_underwear_glimpse"
    aliases = [_alias("판치라"), _alias("パンチラ"), _alias("panchira"), _alias("바람에 치마가 순간 들린 장면", "variant", "instantaneous_partial_glimpse"), _alias("속옷 노출", "related"), _alias("업스커트", "related")]
    false = ["full underwear display", "deliberately held-up skirt", "swimsuit or shorts mistaken for underwear", "camera placed beneath the subject", "age-ambiguous subject"]
    meaning = _meaning(element_id=element_id, ordinal=32, definition="판치라는 치마 아래 속옷이 완전히 전시되는 장면이 아니라, 움직임·바람·순간적인 시점 때문에 일부가 잠깐 보이는 연출을 뜻한다. 시각 계약은 명백한 성인, 부분 가림, 짧은 지속과 비노골적 맥락을 동시에 요구한다.", essential=["명백한 성인 대상", "치마 밑단이 남기는 부분 가림", "속옷의 작은 일부만 보임", "바람·동작·전후 상태가 보여 주는 순간성"], non_equivalents=["속옷 전체를 지속적으로 전시", "치마를 손으로 들어 올린 고정 노출", "수영복이나 돌핀 팬츠", "아래에서 올려다보는 침해적 카메라", "미성년 또는 나이 불명 인물"], axes=["visibility_fraction", "occlusion", "transient_cause", "camera_ethics"], label_policy="omit", forbidden_labels=["판치라", "パンチラ", "panchira"], fidelity="partial_evidence", groups=[("partial_occluded_visibility", 2, ["only a small opaque underwear edge visible", "skirt hem still occluding most of the underwear", "visibility confined to a narrow gap under the moving hem"]), ("transient_cause", 1, ["wind visibly moving the skirt hem", "a turning step creating the momentary gap", "before-and-after states returning the hem to coverage"])], optional=["wind lines", "turning fabric folds", "paired covered state"], false_substitutes=false, do_not_infer=["consent to voyeurism", "sexual activity", "youth or school status", "complete exposure outside the visible crop"], adult_requirement="explicit_adult_always", single_frame="partial", sequence="recommended")
    claims = _claims(("moe_add_claim_glimpse_definition", "사전적 중심은 치마 아래 속옷이 흘끗 보이는 순간이다.", ["add_src_panchira_kotobank"], "high"), ("moe_add_claim_glimpse_partiality", "치라리즘의 미학은 지속적·완전한 노출이 아니라 짧고 부분적인 보임을 구분한다.", ["add_src_chirarism_kci"], "high"))
    candidates = [
        _candidate(element_id=element_id, slug="wind_timed_partial", subtype_id="wind_timed_partial_glimpse", novelty=1, canonical=True, representation_mode="single_frame", integration_role="composition", cues=["바람", "순간", "치마 자락"], preference_profile={"transient_cause": "wind", "proof_mode": "single"}, prompt="Show one clearly adult woman in a non-explicit fashion moment as wind visibly moves the skirt hem: keep only a small opaque underwear edge visible while the skirt hem still occludes most of it, with a level three-quarter camera rather than a view from below.", evidence=["only a small opaque underwear edge visible", "skirt hem still occluding most of the underwear", "wind visibly moving the skirt hem", "level three-quarter camera"], claim_ids=["moe_add_claim_glimpse_definition", "moe_add_claim_glimpse_partiality"], limitation="A still image can suggest but cannot fully prove duration; the hem and motion cause must remain visible.", tags=["adult_only", "non_explicit", "partial_occlusion"]),
        _candidate(element_id=element_id, slug="turning_step_partial", subtype_id="movement_timed_partial_glimpse", novelty=0, canonical=False, representation_mode="single_frame", integration_role="composition", cues=["돌아서는", "걸음", "회전"], preference_profile={"transient_cause": "movement", "proof_mode": "single"}, prompt="Depict one clearly adult woman mid-turn in a non-explicit fashion scene, with a turning step creating the momentary gap, visibility confined to a narrow gap under the moving hem, and the skirt still covering nearly everything from a level side view.", evidence=["a turning step creating the momentary gap", "visibility confined to a narrow gap under the moving hem", "skirt hem still occluding most of the underwear", "level side camera"], claim_ids=["moe_add_claim_glimpse_definition", "moe_add_claim_glimpse_partiality"], limitation="Do not substitute a static lifted skirt or a low camera angle for transient movement.", tags=["adult_only", "non_explicit", "motion_cue"]),
        _candidate(element_id=element_id, slug="covered_glimpse_covered_sequence", subtype_id="before_after_transient_glimpse", novelty=2, canonical=False, representation_mode="paired_or_sequence", integration_role="composition", cues=["전후", "연속", "잠깐"], preference_profile={"transient_cause": "wind", "proof_mode": "sequence"}, prompt="Use a short sequence with the same clearly adult woman: a covered skirt state, one wind-driven frame where only a small opaque underwear edge is visible behind the hem, and a final state where the hem has returned to coverage.", evidence=["before-and-after states returning the hem to coverage", "only a small opaque underwear edge visible", "skirt hem still occluding most of the underwear", "same adult identity across all states"], claim_ids=["moe_add_claim_glimpse_definition", "moe_add_claim_glimpse_partiality"], limitation="The middle state remains partial and non-explicit; neither surrounding frame may become a display pose.", tags=["adult_only", "non_explicit", "temporal_proof"]),
    ]
    groups = [group["id"] for group in meaning["component_groups"]]
    variants = [_variant(variant_id="instantaneous_partial_glimpse", subtype_ids=["wind_timed_partial_glimpse", "movement_timed_partial_glimpse"], group_ids=groups, all_of=["one clearly adult woman in an ordinary non-explicit fashion context", "only a small opaque underwear edge visible while the skirt hem occludes most of it", "a visible wind or turning-motion cause"], any_of=["wind-deformed hem and fabric folds", "turning-step fabric lag"], any_minimum=1, topology=["the moving skirt hem remains between the camera and most of the underwear surface"], camera=["level side or three-quarter camera with no view from beneath the subject"], temporal=["momentary movement cue within one still"], interaction=[], confounds=false, modes=["single_frame", "paired_frame", "sequence"]), _variant(variant_id="covered_glimpse_covered_sequence", subtype_ids=["before_after_transient_glimpse"], group_ids=groups, all_of=["the same clearly adult woman across every state", "covered state before and after one narrowly partial middle glimpse"], any_of=["wind cue peaks only in the middle frame", "the hem visibly settles back into place"], any_minimum=1, topology=["the skirt hem occludes the underwear in the first and final states and still occludes most of it in the middle"], camera=["matched level camera and scale across the covered and partial states"], temporal=["covered baseline", "brief partial visibility", "coverage restored"], interaction=[], confounds=false, modes=["paired_frame", "sequence"])]
    return _new_profile(element_id=element_id, ordinal=32, category="staging_social", label_ko="판치라·순간적 부분 노출", label_en="brief partial underwear glimpse", aliases=aliases, summary="사전과 의복문화 연구를 근거로 핵심을 '속옷' 자체가 아니라 순간성·부분성·치마 밑단의 가림으로 잡았다. 성인만 허용하고 아래 시점이나 전체 전시는 거부한다.", claims=claims, evidence=_evidence("moe_add_image_evidence_brief_glimpse", queries=["ぱんちら 一瞬 スカート ちらり 定義", "chirarism partial glimpse skirt fashion history"], confidence="high", recurring=["small partial underwear edge", "skirt hem remains an occluder", "wind or movement cause", "brief rather than sustained visibility"], confounds=false, urls=["https://kotobank.jp/word/%E3%81%B1%E3%82%93%E3%81%A1%E3%82%89-682325", "https://www.kci.or.jp/articles/files/B_FT02_INOUE_Chirarism_JP.pdf"], limitations=["Search results frequently contain age-ambiguous or explicit material and were excluded from positive evidence.", "A single frame proves geometry and motion cues, not literal duration; paired output is stronger."]), meaning=meaning, axes=[_axis("transient_cause", "what creates the brief opening", [("wind", ["바람", "돌풍"]), ("movement", ["회전", "걸음", "돌아서는"])]), _axis("proof_mode", "how transience is evidenced", [("single", ["한 컷", "순간"]), ("sequence", ["전후", "연속", "세 장면"])])], candidates=candidates, default_variant_id="instantaneous_partial_glimpse", variants=variants, compatibility=_compatibility(element_id, frame="single_frame", camera="camera_full_body_three_quarter", mechanisms=["garment_action_deformation", "secondary_discovery_node"], tags=["adult_only", "partial_occlusion", "non_explicit"]))


def _goldsun_profile() -> dict[str, Any]:
    element_id = "moe_blond_tanned_delinq_archetype"
    aliases = [_alias("금태양"), _alias("금발 태닝 양아치"), _alias("goldsun archetype"), _alias("blond tanned delinquent archetype", "carrier"), _alias("NTR 남성", "related")]
    false = ["blond hair alone", "tanned skin alone", "mapping tan skin to ethnicity", "generic muscular man", "relationship antagonist without displacement evidence"]
    meaning = _meaning(element_id=element_id, ordinal=33, definition="금태양은 '금발·태닝·양아치'를 줄인 한국 서브컬처 은어로, 탈색한 금발과 짙게 그을린 피부, 화려하거나 불량배로 코딩된 옷차림·태도를 결합한 성인 남성 아키타입이다. NTR 작품에 자주 결합되지만 외형 아키타입 자체가 NTR 관계를 증명하지는 않는다.", essential=["명백한 성인 남성", "탈색 또는 인공적으로 밝은 금발", "햇볕에 그을린 갈색 피부", "화려하거나 불량배로 코딩된 스타일 표지"], non_equivalents=["자연 금발만 있는 남성", "그을린 피부만 있는 운동선수", "특정 인종 또는 민족", "근육질 남성 일반", "관계 이동 증거 없는 NTR 악역"], axes=["hair_treatment", "tan_visibility", "styling_code", "relationship_independence"], label_policy="omit", forbidden_labels=["금태양", "금발 태닝 양아치", "goldsun"], fidelity="exact_componentized", groups=[("bleached_blond_hair", 1, ["clearly bleached blond hair with darker roots", "artificially bright blond hair"]), ("visible_tan", 1, ["visibly sun-tanned bronze skin", "clear tan contrast at the collar line"]), ("flashy_delinq_styling", 1, ["open-collar streetwear with a chain accessory", "small earrings and deliberately flashy casual styling", "confident loose-limbed street posture"])], optional=["undercut", "chain necklace", "small earrings", "athletic build"], false_substitutes=false, do_not_infer=["ethnicity from skin color", "criminal behavior", "sexual aggression", "relationship displacement", "consent or coercion"], adult_requirement="explicit_adult_always")
    claims = _claims(("moe_add_claim_goldsun_term", "금태양은 금발·태닝·양아치의 축약형으로 설명되는 한국 커뮤니티 은어다.", ["add_src_goldsun_everymemes", "add_src_goldsun_ssadic"], "medium-low"), ("moe_add_claim_goldsun_ntr_boundary", "NTR 맥락에 자주 쓰인다는 커뮤니티 설명은 있으나 관계 서사는 외형에서 자동 추론할 수 없다.", ["add_src_goldsun_everymemes"], "low"))
    common_claims = ["moe_add_claim_goldsun_term", "moe_add_claim_goldsun_ntr_boundary"]
    candidates = [
        _candidate(element_id=element_id, slug="flashy_street", subtype_id="flashy_street_styling", novelty=1, canonical=True, representation_mode="single_frame", integration_role="character_state", cues=["스트리트", "체인", "화려한"], preference_profile={"styling_code": "street", "hair_treatment": "roots_visible"}, prompt="Design one clearly adult man with clearly bleached blond hair and darker roots, visibly sun-tanned bronze skin, and open-collar streetwear with a chain accessory; use a confident loose-limbed street posture without implying any relationship plot.", evidence=["clearly bleached blond hair with darker roots", "visibly sun-tanned bronze skin", "open-collar streetwear with a chain accessory", "confident loose-limbed street posture"], claim_ids=common_claims, limitation="Hair and skin alone are insufficient; the styling is coded, while ethnicity and criminality remain unspecified.", tags=["adult_male_archetype", "appearance_only", "relationship_independent"]),
        _candidate(element_id=element_id, slug="casual_open_collar", subtype_id="casual_open_collar_styling", novelty=0, canonical=False, representation_mode="single_frame", integration_role="character_state", cues=["캐주얼", "오픈 칼라", "귀걸이"], preference_profile={"styling_code": "casual", "hair_treatment": "bright_blond"}, prompt="Show one clearly adult man with artificially bright blond hair, clear tan contrast at the collar line, a relaxed open shirt over a dark tee, and small earrings with deliberately flashy casual styling; keep the design original and relationship-neutral.", evidence=["artificially bright blond hair", "clear tan contrast at the collar line", "small earrings and deliberately flashy casual styling", "relaxed open shirt"], claim_ids=common_claims, limitation="A resort tan or ordinary blond character does not qualify without the combined styling code.", tags=["adult_male_archetype", "appearance_only", "relationship_independent"]),
        _candidate(element_id=element_id, slug="sporty_flashy", subtype_id="sporty_flashy_styling", novelty=2, canonical=False, representation_mode="single_frame", integration_role="character_state", cues=["스포티", "운동형", "민소매"], preference_profile={"styling_code": "sporty", "hair_treatment": "roots_visible"}, prompt="Create one clearly adult athletic man with clearly bleached blond hair and darker roots, visibly sun-tanned bronze skin, a flashy sleeveless street layer, one small earring, and a self-assured stance; do not add a relationship triangle unless separately requested.", evidence=["clearly bleached blond hair with darker roots", "visibly sun-tanned bronze skin", "small earrings and deliberately flashy casual styling", "self-assured athletic stance"], claim_ids=common_claims, limitation="Muscularity, tattoos, aggression, and any relationship role are optional and must not be inferred.", tags=["adult_male_archetype", "appearance_only", "relationship_independent"]),
    ]
    variant = _variant(variant_id="combined_blond_tan_styling", subtype_ids=[candidate["subtype_id"] for candidate in candidates], group_ids=[group["id"] for group in meaning["component_groups"]], all_of=["one clearly adult man", "bleached or artificially bright blond hair", "visibly sun-tanned bronze skin", "at least one concrete flashy street-style marker"], any_of=["darker hair roots", "open collar with chain", "small earrings", "confident loose-limbed posture"], any_minimum=1, topology=["hair, face, collar-line tan contrast, and styling marker remain visible on the same adult character"], camera=["waist-up or three-quarter character view with hair, skin, collar, and accessory readable"], temporal=[], interaction=[], confounds=false, modes=["single_frame", "paired_frame", "sequence"])
    return _new_profile(element_id=element_id, ordinal=33, category="character_archetype", label_ko="금태양 아키타입", label_en="blond tanned delinquent-coded adult archetype", aliases=aliases, summary="낮은 신뢰도의 한국 커뮤니티 어원 자료 두 개가 공통으로 가리키는 금발·태닝·양아치 스타일 결합만 채택했다. 인종·범죄성·성격·NTR 관계는 외형에서 추론하지 않는다.", claims=claims, evidence=_evidence("moe_add_image_evidence_goldsun", queries=["금태양 금발 태닝 양아치 뜻", "금태양 캐릭터 외형 금발 태닝"], confidence="low", recurring=["bleached blond hair", "deep visible tan", "flashy casual or street styling"], confounds=false, urls=["https://everymemes.tistory.com/322", "https://ssadic.com/%EB%9C%BB/%EA%B8%88%ED%83%9C%EC%96%91/"], limitations=["Available definition sources are community-maintained and do not establish prevalence.", "The NTR association is contextual and never activates relationship displacement by itself.", "Tan describes visible styling, not race or ethnicity."]), meaning=meaning, axes=[_axis("styling_code", "visible styling family", [("street", ["스트리트", "체인"]), ("casual", ["캐주얼", "오픈 칼라"]), ("sporty", ["스포티", "운동형"]) ]), _axis("hair_treatment", "how bleaching is shown", [("roots_visible", ["뿌리", "탈색"]), ("bright_blond", ["밝은 금발", "플래티넘"])])], candidates=candidates, default_variant_id="combined_blond_tan_styling", variants=[variant], compatibility=_compatibility(element_id, frame="single_frame", camera="camera_torso_three_quarter", mechanisms=["identity_face_feature_anchor", "first_fixation_contrast"], tags=["adult_male_archetype", "appearance_only", "no_relationship_inference"]))


def _glasses_woman_profile() -> dict[str, Any]:
    element_id = "moe_glasses_woman_archetype"
    aliases = [_alias("안경소녀"), _alias("안경 여성"), _alias("메가네코"), _alias("眼鏡っ娘"), _alias("meganekko"), _alias("glasses girl"), _alias("안경 고쳐쓰는 여성", "variant", "adjustment_gesture")]
    false = ["glasses floating without a wearer", "frames that hide the eyes with opaque glare", "generic woman holding glasses", "assuming intelligence or bookishness", "age-ambiguous girl"]
    meaning = _meaning(element_id=element_id, ordinal=34, definition="안경소녀·메가네코 계열은 안경을 지속적으로 착용하는 여성 캐릭터에서 안경이 얼굴 정체성과 매력의 핵심 표지가 되는 아키타입이다. 이 데이터에서는 연령 혼동을 막기 위해 명백한 성인 여성으로 구현하며, 지성·직업·문학 취향·성격은 안경만으로 추론하지 않는다.", essential=["명백한 성인 여성", "두 렌즈·브리지·양쪽 템플이 연결된 안경", "안경을 쓴 상태에서 읽히는 눈", "안경이 얼굴 정체성의 반복 표지"], non_equivalents=["손에 안경만 든 여성", "불투명 반사로 눈을 가린 프레임", "안경 소품 단독", "문학소녀·우등생·사서로 자동 분류", "나이 불명 인물"], axes=["frame_construction", "wearer_continuity", "eye_visibility", "identity_salience"], label_policy="allow", forbidden_labels=[], fidelity="exact_componentized", groups=[("adult_feminine_wearer", 1, ["one clearly adult woman wearing the glasses", "the same adult woman's face repeated with the same frames"]), ("complete_glasses_geometry", 3, ["two visible lenses", "one bridge joining the lenses", "two temples continuing toward the ears"]), ("identity_salience", 1, ["both eyes readable through controlled lens reflections", "the same frame shape repeated as a face-identity anchor", "one hand adjusting the worn frame without removing it"])], optional=["small controlled lens highlight", "frame-adjustment gesture", "full-rim or half-rim lineage"], false_substitutes=false, do_not_infer=["intelligence", "occupation", "literary taste", "shyness", "youth"], adult_requirement="explicit_adult_always")
    claims = _claims(("moe_add_claim_glasses_identity", "메가네 계열에서는 안경이 부정적 결함이 아니라 캐릭터 매력과 정체성의 핵심 표지로 다뤄진다.", ["add_src_glasses_imidas"], "medium"), ("moe_add_claim_meganekko_term", "메가네코·안경소녀의 문자적 중심은 안경을 쓴 여성 캐릭터다.", ["add_src_meganekko_wdic"], "medium"))
    common = ["moe_add_claim_glasses_identity", "moe_add_claim_meganekko_term"]
    candidates = [
        _candidate(element_id=element_id, slug="full_rim_identity", subtype_id="full_rim_identity", novelty=1, canonical=True, representation_mode="single_frame", integration_role="character_state", cues=["풀림", "두꺼운 테", "정면"], preference_profile={"frame_construction": "full_rim", "gesture": "neutral"}, prompt="Design one clearly adult woman wearing complete full-rim glasses with two visible lenses, one bridge joining the lenses, two temples continuing toward the ears, and both eyes readable through controlled lens reflections; make the frame shape a stable face-identity anchor.", evidence=["one clearly adult woman wearing the glasses", "two visible lenses", "one bridge joining the lenses", "two temples continuing toward the ears", "both eyes readable through controlled lens reflections"], claim_ids=common, limitation="Frames do not imply intelligence, occupation, personality, or literary interests.", tags=["adult_woman_archetype", "face_identity_anchor", "complete_glasses_geometry"]),
        _candidate(element_id=element_id, slug="half_rim_subtle", subtype_id="half_rim_identity", novelty=0, canonical=False, representation_mode="single_frame", integration_role="character_state", cues=["하프림", "얇은 테", "은은한"], preference_profile={"frame_construction": "half_rim", "gesture": "neutral"}, prompt="Show one clearly adult woman wearing delicate half-rim glasses: keep two visible lenses, one bridge joining the lenses, two temples continuing toward the ears, and both eyes readable with only a small controlled lens highlight; repeat the same frame geometry as her identity marker.", evidence=["one clearly adult woman wearing the glasses", "two visible lenses", "one bridge joining the lenses", "two temples continuing toward the ears", "the same frame shape repeated as a face-identity anchor"], claim_ids=common, limitation="Thin frames must remain structurally complete and cannot disappear into hair or glare.", tags=["adult_woman_archetype", "face_identity_anchor", "complete_glasses_geometry"]),
        _candidate(element_id=element_id, slug="adjustment_gesture", subtype_id="adjustment_gesture", novelty=2, canonical=False, representation_mode="single_frame", integration_role="character_state", cues=["고쳐쓰는", "브리지", "손가락"], preference_profile={"frame_construction": "full_rim", "gesture": "adjusting"}, prompt="Frame one clearly adult woman using one fingertip to adjust the bridge of her worn glasses without removing them; preserve two visible lenses, one connecting bridge, both temples toward the ears, and both eyes readable through controlled reflections.", evidence=["one clearly adult woman wearing the glasses", "one hand adjusting the worn frame without removing it", "two visible lenses", "one bridge joining the lenses", "two temples continuing toward the ears"], claim_ids=common, limitation="The adjustment hand may not hide the bridge, either eye, or both frame temples.", tags=["adult_woman_archetype", "face_identity_anchor", "hand_face_interaction"]),
    ]
    groups = [group["id"] for group in meaning["component_groups"]]
    variants = [_variant(variant_id="full_rim_identity", subtype_ids=["full_rim_identity"], group_ids=groups, all_of=["one clearly adult woman wearing complete full-rim glasses", "two lenses joined by one bridge with two temples continuing toward the ears", "both eyes readable through controlled reflections"], any_of=["the same frame shape repeated as an identity anchor", "small asymmetric lens highlight"], any_minimum=1, topology=["each lens connects through the bridge and outer hinge to a temple ending near the corresponding ear"], camera=["front or three-quarter head-and-shoulders framing with both ears or temple directions readable"], temporal=[], interaction=[], confounds=false, modes=["single_frame", "paired_frame", "sequence"]), _variant(variant_id="half_rim_identity", subtype_ids=["half_rim_identity"], group_ids=groups, all_of=["one clearly adult woman wearing structurally complete half-rim glasses", "two lens boundaries, one bridge, and both temples remain visible", "both eyes readable through the lenses"], any_of=["thin upper rims", "small controlled lens highlight"], any_minimum=1, topology=["the half-rim support still forms one continuous wearable frame across both eyes and ears"], camera=["close enough head-and-shoulders view to preserve thin frame lines"], temporal=[], interaction=[], confounds=false, modes=["single_frame", "paired_frame", "sequence"]), _variant(variant_id="adjustment_gesture", subtype_ids=["adjustment_gesture"], group_ids=groups, all_of=["one clearly adult woman still wearing the complete glasses", "one fingertip contacts the bridge while both lenses, both temples, and both eyes remain visible"], any_of=["slight bridge pressure", "small frame tilt being corrected"], any_minimum=1, topology=["the adjusting finger touches the bridge but does not break the visible lens-to-temple continuity"], camera=["tight head-and-hand framing that does not crop fingertips or temples"], temporal=[], interaction=["one hand adjusts the worn frame without removing it"], confounds=false, modes=["single_frame", "paired_frame", "sequence"])]
    return _new_profile(element_id=element_id, ordinal=34, category="character_archetype", label_ko="안경소녀·안경여성", label_en="glasses-woman archetype", aliases=aliases, summary="기존 '안경' 요소의 물체 구조를 보존하면서, 새 아키타입은 명백한 성인 여성과 얼굴 정체성의 반복 표지를 추가한다. 안경에서 지성·직업·문학 취향을 추론하지 않는다.", claims=claims, evidence=_evidence("moe_add_image_evidence_glasses_woman", queries=["メガネっ娘 キャラクター 眼鏡 魅力 定義", "meganekko glasses identity character design"], confidence="medium", recurring=["glasses worn rather than merely held", "complete two-lens bridge-and-temple structure", "eyes visible behind lenses", "frames treated as identity-salient"], confounds=false, urls=["https://imidas.jp/ryuko/detail/N-05-2-730-07.html", "https://www.wdic.org/w/MOE/%E3%83%A1%E3%82%AC%E3%83%8D%E3%81%A3%E5%A8%98"], limitations=["Community descriptions include subjective personality stereotypes that were excluded.", "The Korean and Japanese labels can imply youth colloquially; runtime subjects are explicitly adult."]), meaning=meaning, axes=[_axis("frame_construction", "frame lineage", [("full_rim", ["풀림", "두꺼운 테"]), ("half_rim", ["하프림", "얇은 테"]) ]), _axis("gesture", "wearer action", [("neutral", ["정면", "차분히"]), ("adjusting", ["고쳐쓰는", "브리지", "손가락"])])], candidates=candidates, default_variant_id="full_rim_identity", variants=variants, compatibility=_compatibility(element_id, frame="single_frame", camera="camera_face_close", mechanisms=["identity_face_feature_anchor", "internal_part_boundary"], tags=["adult_woman_archetype", "face_identity_anchor", "no_personality_inference"]))


def _literary_woman_profile() -> dict[str, Any]:
    element_id = "moe_literary_woman_archetype"
    aliases = [_alias("문학소녀"), _alias("文学少女"), _alias("literary girl"), _alias("문학 여성"), _alias("문학을 쓰는 여성", "variant", "active_literary_writing"), _alias("bookish girl", "related"), _alias("사서", "related")]
    false = ["woman merely holding a closed book", "generic library background", "glasses substituted for literary activity", "librarian occupation", "protected franchise costume or character"]
    meaning = _meaning(element_id=element_id, ordinal=35, definition="문학소녀는 문학을 좋아하고 문학적 분위기나 창작 지향을 지닌 여성 아키타입이다. 시각적으로는 단순히 책을 소품으로 드는 것이 아니라 성인 여성이 문학 작품을 읽고 표시하거나, 문장을 쓰고 고치는 구체 행동과 페이지 연속성으로 구현한다.", essential=["명백한 성인 여성", "문학 작품을 읽거나 쓰는 진행 중 행동", "열린 페이지·주석·원고 등 문학적 작업의 물질적 증거", "행동과 시선이 같은 텍스트를 향함"], non_equivalents=["닫힌 책을 든 정면 인물", "도서관 배경만 있는 장면", "안경을 썼다는 이유만으로 문학적이라고 추정", "사서 직업", "특정 작품의 의상·캐릭터 복제"], axes=["literary_activity", "text_material", "attention_relation", "creation_vs_reading"], label_policy="allow", forbidden_labels=[], fidelity="exact_componentized", groups=[("adult_feminine_reader_writer", 1, ["one clearly adult woman actively reading", "one clearly adult woman actively writing and revising"]), ("literary_work_evidence", 2, ["open prose or poetry pages", "handwritten marginal notes tied to the open passage", "a manuscript page with visible revisions", "a bookmark preserving continuity between passages"]), ("attention_to_text", 1, ["eyes and pointing finger aligned to the same passage", "pen tip contacting the sentence being revised", "page-turning hand and gaze following the next passage"])], optional=["quiet room", "muted practical clothing", "stack of currently referenced books", "soft absorbed expression"], false_substitutes=false, do_not_infer=["glasses", "school enrollment", "librarian occupation", "introversion", "a protected title or franchise identity"], adult_requirement="explicit_adult_always")
    claims = _claims(("moe_add_claim_literary_definition", "사전은 문학을 좋아하고 문학적 분위기나 꿈을 지닌 여성을 문학소녀로 설명한다.", ["add_src_literary_kotobank"], "high"), ("moe_add_claim_literary_creation", "일부 사전 계보에는 문학 창작을 지향하는 의미도 포함된다.", ["add_src_literary_kotobank"], "medium"))
    common = ["moe_add_claim_literary_definition", "moe_add_claim_literary_creation"]
    candidates = [
        _candidate(element_id=element_id, slug="annotated_reading", subtype_id="annotated_literary_reading", novelty=1, canonical=True, representation_mode="single_frame", integration_role="character_state", cues=["읽는", "주석", "시집", "소설"], preference_profile={"literary_activity": "reading", "text_material": "annotations"}, prompt="Show one clearly adult woman actively reading open prose or poetry pages, with handwritten marginal notes tied to the open passage and her eyes and pointing finger aligned to the same passage; keep the character and materials original.", evidence=["one clearly adult woman actively reading", "open prose or poetry pages", "handwritten marginal notes tied to the open passage", "eyes and pointing finger aligned to the same passage"], claim_ids=common, limitation="A closed book, library shelf, glasses, or quiet expression alone does not prove literary engagement.", tags=["adult_woman_archetype", "active_text_engagement", "original_generic_design"]),
        _candidate(element_id=element_id, slug="page_turn_continuity", subtype_id="page_turn_literary_reading", novelty=0, canonical=False, representation_mode="single_frame", integration_role="character_state", cues=["페이지를 넘기는", "책갈피", "독서"], preference_profile={"literary_activity": "reading", "text_material": "bookmark"}, prompt="Depict one clearly adult woman turning an open prose page, with a bookmark preserving continuity between passages and her page-turning hand and gaze following the next passage; avoid any recognizable franchise design.", evidence=["one clearly adult woman actively reading", "open prose or poetry pages", "a bookmark preserving continuity between passages", "page-turning hand and gaze following the next passage"], claim_ids=common, limitation="Book ownership or a library location is not a substitute for an active reading relation.", tags=["adult_woman_archetype", "active_text_engagement", "original_generic_design"]),
        _candidate(element_id=element_id, slug="active_literary_writing", subtype_id="active_literary_writing", novelty=2, canonical=False, representation_mode="single_frame", integration_role="character_state", cues=["쓰는", "원고", "퇴고", "수정"], preference_profile={"literary_activity": "writing", "text_material": "manuscript"}, prompt="Frame one clearly adult woman actively writing and revising a manuscript page with visible revisions, her pen tip contacting the sentence being revised, and an open literary volume beside the draft as a concrete reference.", evidence=["one clearly adult woman actively writing and revising", "a manuscript page with visible revisions", "pen tip contacting the sentence being revised", "open prose or poetry pages"], claim_ids=common, limitation="Generic journaling, homework, or office paperwork is not automatically literary creation.", tags=["adult_woman_archetype", "active_text_creation", "original_generic_design"]),
    ]
    groups = [group["id"] for group in meaning["component_groups"]]
    variants = [_variant(variant_id="active_literary_reading", subtype_ids=["annotated_literary_reading", "page_turn_literary_reading"], group_ids=groups, all_of=["one clearly adult woman actively reading an open literary work", "open prose or poetry pages plus a linked note or bookmark", "eyes and one hand physically aligned to the current passage"], any_of=["handwritten marginal notes", "page-turning action", "bookmark preserving passage continuity"], any_minimum=1, topology=["the woman's gaze and active hand both terminate at the same open passage"], camera=["medium or three-quarter view close enough to read page state, hand action, and gaze direction"], temporal=[], interaction=["one hand reads, points to, annotates, or turns the same open text followed by the eyes"], confounds=false, modes=["single_frame", "paired_frame", "sequence"]), _variant(variant_id="active_literary_writing", subtype_ids=["active_literary_writing"], group_ids=groups, all_of=["one clearly adult woman actively writing and revising", "a manuscript page with visible revisions and an open literary reference", "pen tip contacting the exact sentence under revision"], any_of=["crossed-out phrase with a replacement", "margin revision marks", "open reference passage beside the draft"], any_minimum=1, topology=["the pen, revised sentence, gaze, and open reference form one continuous work relation"], camera=["desk-level medium view showing face, writing hand, manuscript, and open reference without page-obscuring crop"], temporal=[], interaction=["the writing hand physically revises the manuscript while the eyes track the same sentence"], confounds=false, modes=["single_frame", "paired_frame", "sequence"])]
    return _new_profile(element_id=element_id, ordinal=35, category="character_archetype", label_ko="문학소녀·문학여성", label_en="literary-woman archetype", aliases=aliases, summary="사전 정의의 문학 애호·문학적 분위기·창작 지향을 보존하되, 런타임은 열린 문학 텍스트와 읽기·주석·퇴고 행동으로 증명한다. 안경·도서관·사서·특정 프랜차이즈를 대체물로 쓰지 않는다.", claims=claims, evidence=_evidence("moe_add_image_evidence_literary_woman", queries=["文学少女 意味 文学 好き 創作", "literary woman reading annotating manuscript visual archetype"], confidence="medium", recurring=["open literary pages", "active reading or writing posture", "notes, bookmark, or manuscript revisions", "gaze and hand aligned to text"], confounds=false, urls=["https://kotobank.jp/word/%E6%96%87%E5%AD%A6%E5%B0%91%E5%A5%B3-1711853"], limitations=["The dictionary supports meaning, while the exact visual construction is a design inference.", "The generic term overlaps a protected title; runtime must use an original, non-franchise design.", "Glasses, long dark hair, uniforms, and libraries are optional conventions rather than required evidence."]), meaning=meaning, axes=[_axis("literary_activity", "reader or creator emphasis", [("reading", ["읽는", "독서", "시집", "소설"]), ("writing", ["쓰는", "원고", "퇴고", "수정"]) ]), _axis("text_material", "physical evidence of work", [("annotations", ["주석", "밑줄", "메모"]), ("bookmark", ["책갈피", "페이지"]), ("manuscript", ["원고", "수정 흔적"])])], candidates=candidates, default_variant_id="active_literary_reading", variants=variants, compatibility=_compatibility(element_id, frame="single_frame", camera="camera_torso_three_quarter", mechanisms=["actor_action_target_triangle", "identity_face_feature_anchor"], tags=["adult_woman_archetype", "active_text_engagement", "protected_title_exclusion"]))


def _gumiho_profile() -> dict[str, Any]:
    element_id = "moe_gumiho"
    aliases = [
        _alias("구미호"),
        _alias("gumiho"),
        _alias("kumiho"),
        _alias("nine-tailed fox", "carrier"),
        _alias("구미호 인간형", "variant", "human_form_fox_state"),
        _alias("kitsune", "related"),
        _alias("huli jing", "related"),
    ]
    false = [
        "an ordinary fox with one tail",
        "a generic human wearing detachable fox accessories",
        "Japanese shrine-maiden or torii imagery used as the only identifier",
        "a generic seductive woman without fox-state evidence",
    ]
    meaning = _meaning(
        element_id=element_id,
        ordinal=36,
        definition="구미호는 한국 설화의 오래 산 여우 계열 존재로, 아홉 꼬리가 가장 강한 식별 표지이며 인간 모습으로 변신하는 전승도 있다. 인간형 장면에서는 꼬리·여우 그림자·변신 연속성 같은 여우 상태 증거가 필요하다.",
        essential=["한국 여우 정령 계보", "아홉 꼬리 또는 그에 준하는 변신 상태 증거", "여우 몸과 인간형 사이의 동일 존재 관계"],
        non_equivalents=["꼬리 하나인 일반 여우", "여우 귀 액세서리만 단 인간", "일본 키츠네 도상만으로 대체", "유혹적 분위기만 있는 여성"],
        axes=["embodiment", "tail_evidence", "transformation_state"],
        label_policy="allow",
        forbidden_labels=[],
        fidelity="exact_componentized",
        groups=[
            ("fox_lineage", 1, ["one fox-bodied supernatural being", "one adult human form physically linked to a fox state"]),
            ("nine_tail_evidence", 1, ["nine individually readable tails converging at one tail root", "one matched fox shadow with nine individually readable tails"]),
            ("identity_continuity", 1, ["the same eye color and ornament repeated across fox and human states", "one transformation seam joining the human silhouette to the fox-tail fan", "one fox bead physically tied to the same transforming figure"]),
        ],
        optional=["fox bead", "moonlit Korean landscape", "subtle aged-fox dignity", "partial transformation seam"],
        false_substitutes=false,
        do_not_infer=["female gender", "evil alignment", "sexual seduction", "human predation", "Japanese or Chinese cultural identity"],
        adult_requirement="none",
    )
    claims = _claims(
        ("moe_add_claim_gumiho_core", "국립국어원 사전은 구미호를 사람을 홀리거나 속인다고 전하는 아홉 꼬리 여우로 풀이한다.", ["add_src_gumiho_krdict"], "high"),
        ("moe_add_claim_gumiho_shapeshift", "한국 문화 소개 자료에는 인간 변신과 여우구슬 모티프가 나타나지만 모든 장면의 필수 소품은 아니다.", ["add_src_gumiho_kocis", "add_src_gumiho_heritage"], "medium"),
    )
    common = ["moe_add_claim_gumiho_core", "moe_add_claim_gumiho_shapeshift"]
    candidates = [
        _candidate(element_id=element_id, slug="nine_tail_fox", subtype_id="full_nine_tailed_fox", novelty=1, canonical=True, representation_mode="single_frame", integration_role="character_state", cues=["여우형", "아홉 꼬리", "전신"], preference_profile={"embodiment": "fox", "reveal": "direct"}, prompt="Show one supernatural fox-bodied being with nine individually readable tails converging at one anatomical tail root, repeating one distinctive eye color and neck ornament as identity anchors, in an original Korean-folklore setting.", evidence=["one fox-bodied supernatural being", "nine individually readable tails converging at one tail root", "the same eye color and ornament repeated as identity anchors"], claim_ids=common, limitation="A single tail, an arbitrary tail cloud, or Japanese shrine iconography alone cannot establish this Korean folklore identity.", tags=["korean_folklore", "nine_tail_count", "nonhuman_character"]),
        _candidate(element_id=element_id, slug="human_tail_leak", subtype_id="adult_human_tail_reveal", novelty=0, canonical=False, representation_mode="single_frame", integration_role="character_state", cues=["인간형", "변신", "꼬리"], preference_profile={"embodiment": "human", "reveal": "tail_fan"}, prompt="Depict one clearly adult human form physically linked to a fan of nine individually readable fox tails, with a single transformation seam at the lower back and the same eye color repeated in a nearby fox reflection.", evidence=["one adult human form physically linked to a fox state", "nine individually readable tails", "one transformation seam joining the human silhouette to the fox-tail fan"], claim_ids=common, limitation="Fox ears or a detachable costume tail without anatomical or reflective continuity are insufficient.", tags=["korean_folklore", "adult_human_shapeshift", "identity_continuity"]),
        _candidate(element_id=element_id, slug="shadow_reveal", subtype_id="human_fox_shadow_reveal", novelty=2, canonical=False, representation_mode="paired_or_sequence", integration_role="character_state", cues=["그림자", "정체 드러남", "여우구슬"], preference_profile={"embodiment": "human", "reveal": "shadow"}, prompt="Stage one clearly adult human figure holding one small luminous fox bead while a matched light casts one fox-shaped shadow with nine individually readable tails; repeat the figure's eye color and wrist ornament in the shadow-state inset.", evidence=["one adult human form physically linked to a fox state", "one matched fox shadow with nine individually readable tails", "one fox bead physically tied to the same transforming figure"], claim_ids=common, limitation="The shadow must be causally matched to the person and cannot be a decorative unrelated fox mural.", tags=["korean_folklore", "shadow_identity_reveal", "paired_state"]),
    ]
    groups = [group["id"] for group in meaning["component_groups"]]
    variants = [
        _variant(variant_id="full_fox_nine_tails", subtype_ids=["full_nine_tailed_fox"], group_ids=groups, all_of=["one supernatural fox body with exactly nine individually readable tails", "all nine tails converge at one anatomical tail root", "one repeated eye or ornament anchor identifies the same being"], any_of=["subtle fox bead nearby", "cloud or moon backlight separating all tail silhouettes"], any_minimum=1, topology=["nine separate tail paths radiate from one pelvis-level root without merging into an uncountable plume"], camera=["full-body three-quarter framing wide enough to count every tail and retain the fox face"], temporal=[], interaction=[], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
        _variant(variant_id="human_form_fox_state", subtype_ids=["adult_human_tail_reveal", "human_fox_shadow_reveal"], group_ids=groups, all_of=["one clearly adult human form physically linked to a fox state", "exactly nine readable fox tails in the body, reflection, or matched shadow", "one repeated eye, ornament, or bead anchor ties both states to the same identity"], any_of=["a visible human-to-tail transformation seam", "a causally matched nine-tailed fox shadow", "one fox bead held by the transforming figure"], any_minimum=1, topology=["the human body and nine-tail evidence share one root, reflection axis, or light-cast shadow relation rather than appearing as separate characters"], camera=["full-body or matched-state framing that keeps the adult human, all nine tails, and identity anchor simultaneously readable"], temporal=[], interaction=[], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
    ]
    return _new_profile(element_id=element_id, ordinal=36, category="folklore_entity", label_ko="구미호", label_en="gumiho", aliases=aliases, summary="한국 설화의 아홉 꼬리 여우와 인간 변신 계보를 분리해 모델링했다. 여우형은 꼬리 수와 꼬리뿌리를, 인간형은 꼬리·그림자·변신 연속성을 증거로 요구하며 여성·악·유혹은 자동 추론하지 않는다.", claims=claims, evidence=_evidence("moe_add_image_evidence_gumiho", queries=["구미호 아홉 꼬리 인간 변신 여우구슬", "Korean gumiho nine tailed fox shapeshift visual"], confidence="high", recurring=["nine-tail fan", "fox body or human transformation", "identity continuity between fox and human states", "optional fox bead"], confounds=false, urls=["https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=35014", "https://www.mcst.go.kr/english/policy/kocis/newsView.jsp?pSeq=102", "https://www.kh.or.kr/brd/board/741/l/menu/740?bbIdx=112290&brdType=R&searchField=&searchText=&thisPage=1"], limitations=["Folklore varies by tale and period; there is no single mandatory costume, gender, morality, or scene.", "Exactly nine visible tails is the strongest single-frame disambiguator, but some narrative human forms conceal them.", "The runtime design must remain culturally Korean without copying a protected character."]), meaning=meaning, axes=[_axis("embodiment", "fox or transformed-human state", [("fox", ["여우형", "전신 여우"]), ("human", ["인간형", "변신한"]) ]), _axis("reveal", "how fox identity becomes visible", [("direct", ["아홉 꼬리", "직접 보이는"]), ("tail_fan", ["꼬리가 드러난"]), ("shadow", ["그림자", "정체 드러남"])])], candidates=candidates, default_variant_id="full_fox_nine_tails", variants=variants, compatibility=_compatibility(element_id, frame="single_frame", camera="camera_full_body_three_quarter", mechanisms=["pose_invariant_landmarks", "thumbnail_outer_contour"], tags=["korean_folklore", "nine_tail_count", "identity_continuity"]))


def _dragon_profile() -> dict[str, Any]:
    element_id = "moe_dragon"
    aliases = [_alias("드래곤"), _alias("dragon"), _alias("용", "variant", "east_asian_cloud_water_dragon"), _alias("동양 용", "variant", "east_asian_cloud_water_dragon"), _alias("Korean dragon", "variant", "east_asian_cloud_water_dragon"), _alias("wyvern", "variant", "western_wyvern"), _alias("와이번", "variant", "western_wyvern"), _alias("드래곤족", "related"), _alias("dragonkin", "related")]
    false = ["a human with decorative horns and wings", "a generic large lizard", "a winged horse or bird", "one culture's dragon anatomy forced onto every lineage"]
    meaning = _meaning(element_id=element_id, ordinal=37, definition="드래곤은 여러 문화권에서 서로 다른 해부와 상징을 지닌 대형 신화적 파충류 계열이다. 무지정 '드래곤'은 서양형 날개 달린 계보를 기본으로 하되, 한국·동아시아의 용은 길고 굽이치는 몸, 구름·물 관계, 뿔과 발톱을 지닌 별도 변형으로 유지한다.", essential=["신화적 비인간 파충류 몸", "사람이나 환경보다 큰 종 규모", "선택한 문화·해부 계보 안에서 일관된 날개·다리·몸통 구조"], non_equivalents=["뿔과 날개 액세서리를 단 인간", "단순 대형 도마뱀", "와이번과 네발 드래곤의 다리 수 혼합", "동아시아 용에 서양 박쥐날개를 필수화"], axes=["dragon_lineage", "limb_plan", "environment_relation"], label_policy="allow", forbidden_labels=[], fidelity="exact_componentized", groups=[("mythic_reptile_body", 2, ["one clearly nonhuman reptilian head and torso", "one long scaled tail continuous with the torso", "one serpentine scaled body with a horned head"]), ("coherent_limb_plan", 1, ["four weight-bearing legs plus a separate wing pair", "two hind legs with the forelimbs transformed into wings", "four clawed legs on a wingless serpentine body"]), ("species_scale_relation", 1, ["the creature spans multiple trees or architectural bays", "clouds and waves wrap around the creature's long body", "one distant human-scale landmark establishes giant size"])], optional=["fire breath for a requested Western subtype", "whiskers and antler-like horns for an East Asian subtype", "clouds", "water", "weather response"], false_substitutes=false, do_not_infer=["evil alignment", "fire breathing", "treasure hoarding", "four legs for every subtype", "wings for East Asian dragons", "humanoid dragonkin"], adult_requirement="none")
    claims = _claims(("moe_add_claim_dragon_east", "국립중앙박물관 자료의 한국 용은 구름과 물 사이를 굽이치며 길게 이어지는 몸과 상서·왕권의 상징성을 보인다.", ["add_src_dragon_nmok"], "high"), ("moe_add_claim_dragon_west", "게티의 중세 자료는 서양 드래곤의 비늘·발톱·긴 꼬리·박쥐형 날개를 반복적으로 보여 주지만 다리 수와 불은 가변적이라고 설명한다.", ["add_src_dragon_getty"], "high"))
    common = ["moe_add_claim_dragon_east", "moe_add_claim_dragon_west"]
    candidates = [
        _candidate(element_id=element_id, slug="western_four_leg", subtype_id="western_four_leg_winged", novelty=1, canonical=True, representation_mode="single_frame", integration_role="character_state", cues=["서양형", "네 다리", "날개"], preference_profile={"dragon_lineage": "western", "limb_plan": "four_plus_wings"}, prompt="Design one giant nonhuman reptilian creature with one scaled torso, four weight-bearing clawed legs, one separate pair of batlike wings, and one long tail continuous with the torso; place a distant tower for scale without requiring fire.", evidence=["one clearly nonhuman reptilian head and torso", "four weight-bearing legs plus a separate wing pair", "one distant human-scale landmark establishes giant size"], claim_ids=common, limitation="Do not merge forelimbs into the wings in this four-legged lineage, and do not infer fire or villainy.", tags=["western_dragon", "four_leg_wing_plan", "giant_scale"]),
        _candidate(element_id=element_id, slug="east_asian_cloud_water", subtype_id="east_asian_serpentine", novelty=0, canonical=False, representation_mode="single_frame", integration_role="character_state", cues=["용", "동양", "구름", "물"], preference_profile={"dragon_lineage": "east_asian", "limb_plan": "serpentine_four_claw"}, prompt="Show one immense wingless serpentine scaled creature with a horned whiskered head, four small clawed legs, and one continuous body coiling through clouds above water; let clouds and waves wrap around its turns to establish scale.", evidence=["one serpentine scaled body with a horned head", "four clawed legs on a wingless serpentine body", "clouds and waves wrap around the creature's long body"], claim_ids=common, limitation="Batlike wings and a squat Western torso are not required for the Korean and East Asian lineage.", tags=["east_asian_dragon", "cloud_water_relation", "wingless_serpentine"]),
        _candidate(element_id=element_id, slug="western_wyvern", subtype_id="western_two_leg_wyvern", novelty=2, canonical=False, representation_mode="single_frame", integration_role="character_state", cues=["와이번", "두 다리", "날개 앞다리"], preference_profile={"dragon_lineage": "western", "limb_plan": "two_wing_forelimbs"}, prompt="Construct one giant nonhuman reptilian creature with two clawed hind legs, forelimbs transformed into one pair of batlike wings, a scaled torso, and one long balancing tail, with trees beneath it establishing species scale.", evidence=["one clearly nonhuman reptilian head and torso", "two hind legs with the forelimbs transformed into wings", "the creature spans multiple trees or architectural bays"], claim_ids=common, limitation="A wyvern's wing pair replaces the forelimbs; adding a second arm pair changes the requested limb plan.", tags=["western_wyvern", "two_leg_wing_plan", "giant_scale"]),
    ]
    groups = [group["id"] for group in meaning["component_groups"]]
    variants = [
        _variant(variant_id="western_four_leg_dragon", subtype_ids=["western_four_leg_winged"], group_ids=groups, all_of=["one giant nonhuman scaled reptile with four weight-bearing legs", "one separate pair of batlike wings attached behind the forelimbs", "one long tail continuous with the torso"], any_of=["a tower or trees establishing giant scale", "weather displaced by the wing span"], any_minimum=1, topology=["four leg attachments and two separate wing attachments remain countable around one continuous torso"], camera=["wide full-body three-quarter view retaining head, all four legs, both wings, tail, and one scale landmark"], temporal=[], interaction=[], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
        _variant(variant_id="east_asian_cloud_water_dragon", subtype_ids=["east_asian_serpentine"], group_ids=groups, all_of=["one wingless serpentine scaled body with a horned whiskered head", "four small clawed legs distributed along the long body", "clouds and water visibly wrap around multiple body turns"], any_of=["antler-like horns", "flowing whiskers", "one claw emerging through cloud"], any_minimum=1, topology=["the head, long coiling torso, four claws, and tail form one uninterrupted path through cloud and water"], camera=["wide landscape framing that preserves several complete body coils, the head, claws, and environmental scale"], temporal=[], interaction=[], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
        _variant(variant_id="western_wyvern", subtype_ids=["western_two_leg_wyvern"], group_ids=groups, all_of=["one giant nonhuman scaled reptile with exactly two weight-bearing hind legs", "the only forelimb pair is transformed into batlike wings", "one long balancing tail continuous with the torso"], any_of=["trees or architecture establishing giant scale", "wing-driven air disturbance"], any_minimum=1, topology=["two hind-leg attachments and two wing-forelimb attachments remain countable around one continuous torso"], camera=["wide side or three-quarter view that makes the two-leg wing-forelimb plan unambiguous"], temporal=[], interaction=[], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
    ]
    return _new_profile(element_id=element_id, ordinal=37, category="mythic_creature", label_ko="드래곤·용", label_en="dragon", aliases=aliases, summary="서양형 네발 드래곤, 서양형 와이번, 한국·동아시아의 구름·물 용을 해부 계보로 분리했다. 날개·다리 수·불·선악을 모든 드래곤에 공통으로 강제하지 않는다.", claims=claims, evidence=_evidence("moe_add_image_evidence_dragon", queries=["Korean dragon cloud water National Museum", "medieval Western dragon wings claws leg count"], confidence="high", recurring=["large mythic reptilian body", "lineage-specific limb plan", "long tail or serpentine body", "environmental scale relation"], confounds=false, urls=["https://www.museum.go.kr/JPN/contents/E0403000000.do?relicId=883&schM=view&searchId=search", "https://www.getty.edu/art/mobile/center/beasts/stop.php?id=952689"], limitations=["Dragon anatomy varies widely by culture and period; the three runtime variants are explicit design families, not a universal taxonomy.", "Fire, treasure, and morality are narrative options rather than defining visual evidence.", "Humanoid dragonkin remains a related but separate concept."]), meaning=meaning, axes=[_axis("dragon_lineage", "cultural and anatomical family", [("western", ["서양형", "드래곤"]), ("east_asian", ["용", "동양 용", "한국 용"]) ]), _axis("limb_plan", "countable limb construction", [("four_plus_wings", ["네 다리", "날개 한 쌍"]), ("two_wing_forelimbs", ["와이번", "두 다리"]), ("serpentine_four_claw", ["긴 몸", "구름 속 발톱"])])], candidates=candidates, default_variant_id="western_four_leg_dragon", variants=variants, compatibility=_compatibility(element_id, frame="single_frame", camera="camera_full_body_three_quarter", mechanisms=["pose_invariant_landmarks", "thumbnail_outer_contour"], tags=["mythic_creature", "lineage_specific_anatomy", "giant_scale_relation"]))


def _dokkaebi_profile() -> dict[str, Any]:
    element_id = "moe_dokkaebi"
    aliases = [_alias("도깨비"), _alias("dokkaebi"), _alias("Korean dokkaebi", "carrier"), _alias("도깨비 방망이", "variant", "magic_club_benefactor"), _alias("씨름 도깨비", "variant", "wrestling_challenger"), _alias("Korean goblin", "related"), _alias("goblin", "related"), _alias("oni", "related"), _alias("도깨비불", "related")]
    false = ["a Japanese oni palette and horns used as the entire definition", "a Western goblin", "the ghost of a dead person", "a generic horned monster without behavior or object lineage"]
    meaning = _meaning(element_id=element_id, ordinal=38, definition="도깨비는 한국 민간신앙과 설화의 비인간적 초자연 존재로, 죽은 사람의 혼인 유령과 다르며 오래된 물건·자연물에서 생기거나 밤길에서 장난·씨름·보상 행동을 하는 등 형상과 성격이 다양하다. 고정된 뿔·피부색은 필수가 아니다.", essential=["한국 설화 계보의 유형적 초자연 행위자", "물건·씨름·장난·보상 중 하나와 연결된 구체 행동", "사람 유령이나 일본 오니가 아닌 독립 정체"], non_equivalents=["죽은 사람의 혼령", "일본 오니의 뿔과 적청 피부", "서양 고블린", "도깨비불만 단독으로 그린 장면"], axes=["tale_role", "manifestation", "magic_object_relation"], label_policy="allow", forbidden_labels=[], fidelity="exact_componentized", groups=[("korean_otherworldly_agent", 1, ["one tangible Korean-folklore otherworldly figure", "one old household object visibly transforming into an otherworldly figure"]), ("tale_action", 1, ["the figure initiates a playful night-road trick", "the figure takes a formal wrestling stance opposite an adult traveler", "the figure uses one marked club to produce a visible gift"]), ("identity_context", 1, ["one worn Korean household object remains attached as its origin trace", "one Korean wrestling ring or satba relation", "one marked club connects the figure's swing to a newly appeared gift"] )], optional=["dokkaebi hat", "one-legged gait from a selected tale", "night road", "thatched-roof village edge", "warmly comic expression"], false_substitutes=false, do_not_infer=["fixed horns", "red or blue skin", "evil alignment", "dead human identity", "Japanese oni identity", "one universal body shape"], adult_requirement="none")
    claims = _claims(("moe_add_claim_dokkaebi_variety", "한국민족문화대백과는 도깨비를 죽은 이의 혼과 구분하고 물건·자연물 기원과 다양한 형상·행동을 기록한다.", ["add_src_dokkaebi_aks"], "high"), ("moe_add_claim_dokkaebi_play", "Korea.net 자료는 도깨비의 장난기와 보물을 내는 방망이 모티프를 소개하며 일률적 악귀로 보지 않는다.", ["add_src_dokkaebi_korea_net"], "medium"))
    common = ["moe_add_claim_dokkaebi_variety", "moe_add_claim_dokkaebi_play"]
    candidates = [
        _candidate(element_id=element_id, slug="object_born_trickster", subtype_id="old_object_night_trickster", novelty=1, canonical=True, representation_mode="single_frame", integration_role="participatory_action", cues=["낡은 물건", "장난", "밤길"], preference_profile={"tale_role": "trickster", "manifestation": "object_born"}, prompt="Stage one tangible Korean-folklore otherworldly figure emerging from one worn household object, leaving that object visibly attached as an origin trace while it playfully rearranges an adult traveler's straw sandals on a moonlit village road.", evidence=["one old household object visibly transforming into an otherworldly figure", "the figure initiates a playful night-road trick", "one worn Korean household object remains attached as its origin trace"], claim_ids=common, limitation="No fixed horn count, skin color, or Japanese oni costume is required; the object origin and action carry the identity.", tags=["korean_folklore", "object_origin", "playful_trickster"]),
        _candidate(element_id=element_id, slug="wrestling_challenger", subtype_id="night_wrestling_challenger", novelty=0, canonical=False, representation_mode="single_frame", integration_role="participatory_action", cues=["씨름", "밤", "도전"], preference_profile={"tale_role": "wrestler", "manifestation": "tangible_figure"}, prompt="Show one tangible Korean-folklore otherworldly figure taking a formal wrestling stance opposite one clearly adult traveler, with both gripping one visible satba relation inside a simple night wrestling ring.", evidence=["one tangible Korean-folklore otherworldly figure", "the figure takes a formal wrestling stance opposite an adult traveler", "one Korean wrestling ring or satba relation"], claim_ids=common, limitation="A generic fight pose without the mutual wrestling grip and Korean tale setting is insufficient.", tags=["korean_folklore", "wrestling_relation", "night_encounter"]),
        _candidate(element_id=element_id, slug="magic_club_gift", subtype_id="magic_club_gift_event", novelty=2, canonical=False, representation_mode="single_frame", integration_role="participatory_action", cues=["방망이", "보물", "선물"], preference_profile={"tale_role": "benefactor", "manifestation": "tangible_figure"}, prompt="Depict one tangible Korean-folklore otherworldly figure swinging one visibly marked wooden club, with a clear motion path ending at a newly appeared pile of food and coins offered to an adult traveler.", evidence=["one tangible Korean-folklore otherworldly figure", "the figure uses one marked club to produce a visible gift", "one marked club connects the figure's swing to a newly appeared gift"], claim_ids=common, limitation="A club held without a visible cause-and-effect gift event does not establish this tale variant.", tags=["korean_folklore", "magic_club", "cause_effect_gift"]),
    ]
    groups = [group["id"] for group in meaning["component_groups"]]
    variants = [
        _variant(variant_id="object_born_night_trickster", subtype_ids=["old_object_night_trickster"], group_ids=groups, all_of=["one tangible Korean-folklore otherworldly figure emerging from one worn household object", "the origin object remains visibly attached to the figure", "one playful night-road trick has a readable human target and consequence"], any_of=["rearranged straw sandals", "a hat or pack shifted to an impossible place", "a trail of misplaced household objects"], any_minimum=1, topology=["the worn object's material continues into the figure while the figure's hand-action connects to the moved item and adult traveler"], camera=["relational medium-wide framing retaining the figure, origin object, adult traveler, and trick consequence"], temporal=[], interaction=["the figure actively changes one travel item while the adult traveler reacts"], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
        _variant(variant_id="wrestling_challenger", subtype_ids=["night_wrestling_challenger"], group_ids=groups, all_of=["one tangible Korean-folklore otherworldly figure and one clearly adult traveler", "both occupy a formal Korean wrestling stance", "one mutual grip or satba relation joins the pair"], any_of=["simple night wrestling ring", "moonlit village clearing", "wrestling footwork trace"], any_minimum=1, topology=["both bodies lean through one shared grip axis rather than striking or standing independently"], camera=["full-body relational framing with both feet, shared grip, and night setting visible"], temporal=[], interaction=["both participants engage in the same wrestling hold"], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
        _variant(variant_id="magic_club_benefactor", subtype_ids=["magic_club_gift_event"], group_ids=groups, all_of=["one tangible Korean-folklore otherworldly figure holding one marked wooden club", "one club swing has a visible motion path", "a newly appeared gift sits at the end of that path for an adult recipient"], any_of=["food appearing", "coins appearing", "useful household goods appearing"], any_minimum=1, topology=["the club, motion path, appeared gift, and adult recipient form one readable cause-and-effect chain"], camera=["medium-wide event framing that retains the club, full motion path, gift, and recipient"], temporal=[], interaction=["the figure produces and offers the visible gift rather than merely posing with a club"], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
    ]
    return _new_profile(element_id=element_id, ordinal=38, category="folklore_entity", label_ko="도깨비", label_en="dokkaebi", aliases=aliases, summary="도깨비는 고정 외형 대신 한국 설화 계보와 물건 기원·장난·씨름·방망이 사건으로 식별한다. 죽은 이의 유령, 일본 오니, 서양 고블린을 동의어로 처리하지 않고 뿔과 적청 피부도 필수화하지 않는다.", claims=claims, evidence=_evidence("moe_add_image_evidence_dokkaebi", queries=["한국민족문화대백과 도깨비 물건 씨름 형상", "Korean dokkaebi playful magic club folklore"], confidence="high", recurring=["variable tangible form", "old-object or material trace", "playful human interaction", "wrestling or magic-club event"], confounds=false, urls=["https://encykorea.aks.ac.kr/Article/E0015527", "https://www.korea.net/Events/Overseas/view?articleId=9497"], limitations=["Dokkaebi have no universal fixed anatomy, costume, horn count, or skin color.", "The visual contracts use tale actions and object relations as stronger evidence than a stereotype silhouette.", "Dokkaebi fire is related folklore imagery but does not by itself depict the agent."]), meaning=meaning, axes=[_axis("tale_role", "observable tale action", [("trickster", ["장난", "밤길"]), ("wrestler", ["씨름", "도전"]), ("benefactor", ["방망이", "보물"]) ]), _axis("manifestation", "how the being becomes tangible", [("object_born", ["낡은 물건", "물건에서 나온"]), ("tangible_figure", ["인물형", "실체 있는"])])], candidates=candidates, default_variant_id="object_born_night_trickster", variants=variants, compatibility=_compatibility(element_id, frame="single_frame", camera="camera_relational_medium", mechanisms=["actor_action_target_triangle", "consequence_trace"], tags=["korean_folklore", "variable_anatomy", "action_based_identity"]))


def _ghost_profile() -> dict[str, Any]:
    element_id = "moe_ghost"
    aliases = [_alias("유령"), _alias("ghost"), _alias("apparition", "carrier"), _alias("phantom", "carrier"), _alias("specter", "carrier"), _alias("투명 유령", "variant", "translucent_apparition"), _alias("wraith", "related"), _alias("zombie", "related"), _alias("demon", "related")]
    false = ["a living pale person", "a white sheet costume", "a zombie or skeleton", "a demon", "a hologram without deceased-person context"]
    meaning = _meaning(element_id=element_id, ordinal=39, definition="유령은 죽은 사람의 육체에서 분리된 영혼이나 그 출현으로 이해되는 존재다. 시각적으로는 생전의 인간 형상을 유지하면서 투명도·바닥 접촉 부재·반사나 그림자의 모순·등장 전후 상태 중 하나가 육체 부재를 드러내야 한다.", essential=["죽은 사람과 연결된 인간 형상", "육체가 없다는 관찰 가능한 모순", "특정 장소·물건·생전 흔적과의 관계"], non_equivalents=["창백한 산 사람", "흰 천을 쓴 코스튬", "좀비·해골", "악마", "맥락 없는 홀로그램"], axes=["apparition_visibility", "disembodiment_cue", "evidence_mode"], label_policy="allow", forbidden_labels=[], fidelity="partial_evidence", groups=[("deceased_human_likeness", 1, ["one pale human likeness matched to a memorial portrait", "one lifelike human apparition matched to a named keepsake"]), ("disembodiment_evidence", 1, ["background lines remain visible through the figure", "the figure casts no floor contact shadow while nearby objects do", "a mirror omits the figure while reflecting the room", "the same camera view changes from empty to occupied without a physical entrance"]), ("haunting_relation", 1, ["the figure and memorial portrait share one face and garment anchor", "the figure reaches toward one keepsake tied to the deceased person", "the apparition occupies the exact location marked in the empty state"] )], optional=["desaturated edge light", "soft translucency", "temperature haze", "subtle floating hem", "matched before-and-after frame"], false_substitutes=false, do_not_infer=["evil intent", "cause of death", "gender", "culture", "white sheet costume", "visible gore"], adult_requirement="none", single_frame="partial", sequence="recommended")
    claims = _claims(("moe_add_claim_ghost_definition", "Cambridge는 ghost를 죽은 사람의 영으로 정의하고 창백하거나 거의 투명한 인간 형상이라는 대표 표현을 함께 제시한다.", ["add_src_ghost_cambridge"], "high"), ("moe_add_claim_ghost_visual_history", "V&A의 영혼 사진사는 투명 중첩과 생전의 신체 닮음을 유령 시각화의 역사적 관습으로 보여 준다.", ["add_src_ghost_va"], "medium"))
    common = ["moe_add_claim_ghost_definition", "moe_add_claim_ghost_visual_history"]
    candidates = [
        _candidate(element_id=element_id, slug="translucent_memorial", subtype_id="translucent_memorial_apparition", novelty=1, canonical=True, representation_mode="single_frame", integration_role="character_state", cues=["반투명", "추모 사진", "떠 있는"], preference_profile={"apparition_visibility": "translucent", "evidence_mode": "single"}, prompt="Show one pale human likeness matched by face and garment to one nearby memorial portrait, with background wall lines remaining visible through the figure and no floor contact shadow while surrounding objects cast shadows.", evidence=["one pale human likeness matched to a memorial portrait", "background lines remain visible through the figure", "the figure and memorial portrait share one face and garment anchor"], claim_ids=common, limitation="Pale skin or transparency alone can also describe a living person or hologram; the memorial match supplies the deceased-person relation.", tags=["apparition", "translucent_body", "memorial_identity_match"]),
        _candidate(element_id=element_id, slug="mirror_omission", subtype_id="lifelike_mirror_omission", novelty=0, canonical=False, representation_mode="single_frame", integration_role="character_state", cues=["거울", "반사되지 않는", "생전 모습"], preference_profile={"apparition_visibility": "lifelike", "evidence_mode": "mirror"}, prompt="Frame one lifelike human apparition reaching toward a named keepsake, with the room and keepsake reflected in a large mirror while the person's position is absent from that reflection; repeat the keepsake beside a memorial portrait.", evidence=["one lifelike human apparition matched to a named keepsake", "a mirror omits the figure while reflecting the room", "the figure reaches toward one keepsake tied to the deceased person"], claim_ids=common, limitation="The mirror geometry must make the missing reflection legible and cannot merely crop the figure out.", tags=["apparition", "reflection_contradiction", "keepsake_relation"]),
        _candidate(element_id=element_id, slug="matched_presence", subtype_id="matched_empty_to_presence", novelty=2, canonical=False, representation_mode="paired_or_sequence", integration_role="character_state", cues=["등장 전후", "같은 구도", "빈 방"], preference_profile={"apparition_visibility": "pale", "evidence_mode": "matched_state"}, prompt="Use two matched camera states of the same locked room: first empty, then occupied at the exact floor mark by one pale human likeness matching a memorial portrait, with no opened door, footprint, or physical entrance between states.", evidence=["one pale human likeness matched to a memorial portrait", "the same camera view changes from empty to occupied without a physical entrance", "the apparition occupies the exact location marked in the empty state"], claim_ids=common, limitation="This evidence needs paired or sequential presentation; a single isolated occupied frame is not equivalent.", tags=["apparition", "matched_state", "presence_absence_change"]),
    ]
    groups = [group["id"] for group in meaning["component_groups"]]
    variants = [
        _variant(variant_id="translucent_apparition", subtype_ids=["translucent_memorial_apparition"], group_ids=groups, all_of=["one pale human likeness matched to one memorial portrait", "background geometry remains visible through the body", "the figure lacks a floor contact shadow while nearby objects retain theirs"], any_of=["desaturated edge light", "slightly floating hem", "soft translucency gradient"], any_minimum=1, topology=["the portrait and apparition share one face anchor while background lines continue through the apparition's body"], camera=["medium full-figure view keeping the portrait, translucent body, feet, floor shadows, and background lines visible"], temporal=[], interaction=[], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
        _variant(variant_id="lifelike_physical_contradiction", subtype_ids=["lifelike_mirror_omission"], group_ids=groups, all_of=["one lifelike human apparition tied to one named keepsake", "a mirror reflects the room and keepsake but omits the figure", "a memorial portrait repeats the apparition's face or garment anchor"], any_of=["hand reaching toward the keepsake", "room objects visible through the expected reflection position"], any_minimum=1, topology=["the direct figure, mirror plane, expected reflected position, keepsake, and portrait remain geometrically comparable"], camera=["three-quarter room view preserving both the direct figure and the full relevant mirror area"], temporal=[], interaction=["the apparition reaches toward the deceased person's keepsake without moving it"], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
        _variant(variant_id="matched_presence_absence", subtype_ids=["matched_empty_to_presence"], group_ids=groups, all_of=["two locked-camera states of the same room", "the first state is empty and the second contains one portrait-matched pale human likeness", "no door, footprint, or physical entrance changes between states"], any_of=["one fixed floor mark under the later figure", "one unmoved keepsake beside the later figure"], any_minimum=1, topology=["the apparition occupies the same marked room coordinates that were visibly empty in the first state"], camera=["identical camera position, lens, crop, room geometry, and object placement across both states"], temporal=["empty locked room", "unexplained portrait-matched presence in the same coordinates"], interaction=[], confounds=false, modes=["paired_frame", "sequence"]),
    ]
    return _new_profile(element_id=element_id, ordinal=39, category="supernatural_entity", label_ko="유령", label_en="ghost", aliases=aliases, summary="죽은 사람의 인간 형상과 육체 부재 증거를 함께 요구한다. 반투명형, 거울 반사 모순형, 동일 구도 등장 전후형을 분리하고 흰 천·좀비·악마·맥락 없는 홀로그램은 대체물에서 제외했다.", claims=claims, evidence=_evidence("moe_add_image_evidence_ghost", queries=["ghost definition pale transparent human image", "spirit photography translucent apparition visual history"], confidence="high", recurring=["human likeness", "pale or translucent rendering", "physical contradiction such as missing shadow or reflection", "memorial or keepsake identity relation"], confounds=false, urls=["https://dictionary.cambridge.org/us/dictionary/english/ghost", "https://www.vam.ac.uk/articles/a-brief-history-of-ghosts-and-spirit-photography"], limitations=["Transparency is a visual convention, not a universal metaphysical property.", "A static image cannot prove death or disembodiment by appearance alone; memorial and physical-contradiction cues are design evidence.", "The matched-state candidate remains prompt preflight until both rendered frames are reviewed."]), meaning=meaning, axes=[_axis("apparition_visibility", "bodily rendering", [("translucent", ["반투명", "비치는"]), ("lifelike", ["생전 모습", "선명한"]), ("pale", ["창백한", "희미한"]) ]), _axis("evidence_mode", "visible disembodiment proof", [("single", ["그림자 없는", "반투명"]), ("mirror", ["거울", "반사되지 않는"]), ("matched_state", ["전후", "같은 구도"])])], candidates=candidates, default_variant_id="translucent_apparition", variants=variants, compatibility=_compatibility(element_id, frame="paired_or_sequence", camera="camera_matched_state", mechanisms=["state_ledger_before_after", "contrast_isolation"], tags=["deceased_likeness", "physical_contradiction", "partial_static_evidence"]))


def _robot_profile() -> dict[str, Any]:
    element_id = "moe_robot"
    aliases = [_alias("로봇"), _alias("robot"), _alias("안드로이드", "variant", "humanoid_service_robot"), _alias("android", "variant", "humanoid_service_robot"), _alias("산업용 로봇", "variant", "industrial_manipulator"), _alias("industrial robot", "variant", "industrial_manipulator"), _alias("service robot", "variant", "mobile_service_robot"), _alias("cyborg", "related"), _alias("사이보그", "related"), _alias("mecha", "related")]
    false = ["a human in rigid armor", "a static mannequin", "a remote-control toy with no task relation", "a cyborg whose defining body remains biological", "a giant piloted mecha"]
    meaning = _meaning(element_id=element_id, ordinal=40, definition="로봇은 프로그램된 구동 기구가 일정한 자율성 아래 이동·조작·위치 결정을 수행하는 기계다. 사람 모양은 필수가 아니며, 제조된 구동 구조·감지 장치·행동 결과의 연결이 시각적 핵심이다.", essential=["제조된 구동 기구", "환경을 감지하는 센서 또는 제어 상태", "이동·조작·위치 결정 중 하나의 과업 결과"], non_equivalents=["갑옷 입은 인간", "정지 마네킹", "생물 신체가 핵심인 사이보그", "조종사가 안에 타는 거대 메카", "과업 관계가 없는 장난감"], axes=["body_plan", "mobility", "task_type"], label_policy="allow", forbidden_labels=[], fidelity="partial_evidence", groups=[("manufactured_actuated_body", 2, ["rigid manufactured shell panels joined by visible actuated joints", "one articulated industrial arm anchored to a machine base", "one mobile chassis with powered wheels or tracks"]), ("sensing_control", 1, ["a sensor array aimed at the active work area", "a status display linking perception to the current task", "calibration markers aligned to the end effector"]), ("task_effect", 1, ["the end effector grips and relocates one workpiece", "the mobile machine scans and updates one mapped route", "the machine presents one requested item at a service station"] )], optional=["battery or charging port", "diagnostic lights", "cable routing", "soft exterior panels", "human-readable status display"], false_substitutes=false, do_not_infer=["sentience", "human gender", "moral alignment", "combat purpose", "humanoid form", "full autonomy from one still image"], adult_requirement="none", single_frame="partial", sequence="recommended")
    claims = _claims(("moe_add_claim_robot_definition", "ISO 8373 계열 정의는 로봇을 이동·조작·위치 결정을 위해 일정한 자율성을 지닌 프로그램된 구동 기구로 규정한다.", ["add_src_robot_iso", "add_src_robot_ifr"], "high"), ("moe_add_claim_robot_forms", "국제로봇연맹 자료는 산업용과 서비스용 로봇이 서로 다른 몸체와 과업 형태를 가질 수 있음을 전제로 한다.", ["add_src_robot_ifr"], "high"))
    common = ["moe_add_claim_robot_definition", "moe_add_claim_robot_forms"]
    candidates = [
        _candidate(element_id=element_id, slug="humanoid_service", subtype_id="humanoid_service_assistant", novelty=1, canonical=True, representation_mode="single_frame", integration_role="participatory_action", cues=["인간형", "서비스", "안드로이드"], preference_profile={"body_plan": "humanoid", "task_type": "service"}, prompt="Design one manufactured humanoid machine with rigid shell panels joined by visible actuated joints, a face-level sensor array aimed at a service tray, and articulated hands presenting one requested item while a chest status display names the task state.", evidence=["rigid manufactured shell panels joined by visible actuated joints", "a sensor array aimed at the active work area", "the machine presents one requested item at a service station"], claim_ids=common, limitation="A smooth human costume or mannequin without joint, sensor, and task evidence is insufficient.", tags=["humanoid_robot", "service_task", "sensor_action_relation"]),
        _candidate(element_id=element_id, slug="industrial_pick_place", subtype_id="industrial_pick_and_place", novelty=0, canonical=False, representation_mode="single_frame", integration_role="participatory_action", cues=["산업용", "로봇팔", "픽앤플레이스"], preference_profile={"body_plan": "fixed_arm", "task_type": "manipulation"}, prompt="Show one articulated industrial arm anchored to a machine base, with calibration markers aligned to its gripper as the end effector lifts one workpiece from a marked input tray toward a separate output tray.", evidence=["one articulated industrial arm anchored to a machine base", "calibration markers aligned to the end effector", "the end effector grips and relocates one workpiece"], claim_ids=common, limitation="A static crane or unjointed prop without controlled end-effector alignment is not enough.", tags=["industrial_robot", "fixed_manipulator", "pick_place_task"]),
        _candidate(element_id=element_id, slug="mobile_inspection", subtype_id="mobile_inspection_mapper", novelty=2, canonical=False, representation_mode="paired_or_sequence", integration_role="participatory_action", cues=["이동형", "점검", "맵핑"], preference_profile={"body_plan": "mobile_chassis", "task_type": "inspection"}, prompt="Depict one mobile machine with a powered wheeled chassis, articulated sensor mast, and forward sensor array scanning aisle markers while its status display updates one mapped route from unchecked to checked segments.", evidence=["one mobile chassis with powered wheels or tracks", "a sensor array aimed at the active work area", "the mobile machine scans and updates one mapped route"], claim_ids=common, limitation="The map update suggests controlled autonomy but a single frame cannot prove the full control policy.", tags=["mobile_robot", "inspection_task", "map_state_change"]),
    ]
    groups = [group["id"] for group in meaning["component_groups"]]
    variants = [
        _variant(variant_id="humanoid_service_robot", subtype_ids=["humanoid_service_assistant"], group_ids=groups, all_of=["one manufactured humanoid body with rigid shell panels and visible actuated joints", "one sensor array points at the current service work area", "articulated hands and a task display jointly evidence one service action"], any_of=["battery or charging indicator", "service tray", "diagnostic joint lights"], any_minimum=1, topology=["sensor gaze, status display, articulated arm, held item, and service station form one perception-to-action chain"], camera=["three-quarter full-body view retaining the sensors, joint construction, both hands, task item, and status display"], temporal=[], interaction=["the machine presents one requested item to a service point"], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
        _variant(variant_id="industrial_manipulator", subtype_ids=["industrial_pick_and_place"], group_ids=groups, all_of=["one base-anchored articulated industrial arm", "one calibrated end effector grips a workpiece", "separate marked input and output positions reveal the manipulation task"], any_of=["joint-axis markings", "machine-guard boundary", "task status light"], any_minimum=1, topology=["base, serial joints, end effector, gripped workpiece, and destination tray remain one continuous kinematic chain"], camera=["wide machine-cell view that retains the arm base, every joint, gripper, source tray, and destination tray"], temporal=[], interaction=["the end effector physically relocates one workpiece between marked positions"], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
        _variant(variant_id="mobile_service_robot", subtype_ids=["mobile_inspection_mapper"], group_ids=groups, all_of=["one powered mobile chassis with a manufactured sensor mast", "the forward sensor array points at marked environmental features", "one route display distinguishes unchecked and checked path segments"], any_of=["wheel encoder markers", "charging port", "inspection light cone"], any_minimum=1, topology=["mobile chassis, sensor direction, inspected marker, and route-display update form one navigation-task relation"], camera=["medium-wide aisle view retaining the whole chassis, sensor cone, route markers, and status display"], temporal=["unchecked route segment", "sensor traversal", "checked route segment"], interaction=[], confounds=false, modes=["paired_frame", "sequence"]),
    ]
    return _new_profile(element_id=element_id, ordinal=40, category="machine_entity", label_ko="로봇", label_en="robot", aliases=aliases, summary="ISO 계열의 기능 정의를 시각화해 인간형 외모 대신 제조된 구동 구조, 센서·제어 상태, 실제 과업 결과를 묶었다. 안드로이드·산업용 팔·이동형 서비스 로봇을 변형으로 두고 사이보그·메카·갑옷 인간과 구분한다.", claims=claims, evidence=_evidence("moe_add_image_evidence_robot", queries=["ISO 8373 robot programmed actuated mechanism autonomy", "industrial service robot sensors actuators task visual"], confidence="high", recurring=["manufactured articulated structure", "sensor or status interface", "movement or manipulation task", "observable perception-action relation"], confounds=false, urls=["https://www.iso.org/standard/75539.html?browse=tc", "https://ifr.org/img/worldrobotics/Sources___Methods_WR_2025_Industrial_Robots.pdf"], limitations=["A still image can evidence actuation and task structure but cannot prove software, autonomy level, or sentience.", "Robot bodies vary from industrial arms to mobile and humanoid systems.", "Cyborg and piloted mecha remain related but non-equivalent concepts."]), meaning=meaning, axes=[_axis("body_plan", "manufactured embodiment", [("humanoid", ["인간형", "안드로이드"]), ("fixed_arm", ["산업용", "로봇팔"]), ("mobile_chassis", ["이동형", "바퀴"]) ]), _axis("task_type", "observable machine task", [("service", ["서비스", "전달"]), ("manipulation", ["집는", "옮기는"]), ("inspection", ["점검", "스캔"])])], candidates=candidates, default_variant_id="humanoid_service_robot", variants=variants, compatibility=_compatibility(element_id, frame="single_frame", camera="camera_full_body_three_quarter", mechanisms=["internal_part_boundary", "actor_action_target_triangle"], tags=["manufactured_actuation", "sensor_action_relation", "no_sentience_inference"]))


def _assassin_profile() -> dict[str, Any]:
    element_id = "moe_assassin"
    aliases = [
        _alias("암살자"),
        _alias("assassin"),
        _alias("청부살인자", "variant", "contract_targeting"),
        _alias("hitman", "variant", "contract_targeting"),
        _alias("contract killer", "variant", "contract_targeting"),
        _alias("ninja", "related"),
        _alias("sniper", "related"),
        _alias("killer", "related"),
    ]
    false = [
        "black clothing alone",
        "a hood or face covering alone",
        "a visible weapon without a deliberate target relation",
        "a ninja, sniper, thief, or generic killer inferred only from equipment",
    ]
    meaning = _meaning(
        element_id=element_id,
        ordinal=41,
        definition="암살자는 특정 표적을 의도적으로 살해하는 역할이며, 대가나 대의가 동기가 될 수 있다. 고정 복장은 없으므로 비노골적 시각화에서는 성인 실행자, 특정 표적 자료, 은밀한 접근·감시·이탈 계획의 결합으로 역할을 증거화한다.",
        essential=["명백한 성인 실행자", "의도적으로 지정된 특정 표적", "발각을 피하는 접근·감시·이탈 계획"],
        non_equivalents=["검은 옷만 입은 사람", "무기만 든 사람", "닌자·저격수·도둑", "표적 관계 없는 일반 범죄자"],
        axes=["operation_phase", "cover_method", "target_evidence"],
        label_policy="omit",
        forbidden_labels=["암살자", "assassin", "청부살인자", "hitman", "contract killer"],
        fidelity="partial_evidence",
        groups=[
            ("adult_covert_operator", 1, ["one clearly adult covert operative using a plausible cover identity", "one clearly adult covert operative positioned in a concealed observation point"]),
            ("specific_target_relation", 2, ["one dossier portrait matched to a distant adult target", "one marked timetable tied to the target's route", "one payment or mission token linked to the same portrait"]),
            ("covert_plan_evidence", 2, ["a concealed approach route marked separately from public access", "one timed observation aligned to the target's movement", "one unobtrusive exit route marked beyond the target location", "cover clothing and access badge matched to the infiltration setting"]),
        ],
        optional=["concealed communication earpiece", "folded floor plan", "non-graphic tool case", "cover-identity badge", "clock synchronization"],
        false_substitutes=false,
        do_not_infer=["ninja identity", "sniper specialization", "political motive", "nationality", "moral alignment", "successful violence", "graphic injury"],
        adult_requirement="explicit_adult_always",
        single_frame="partial",
        sequence="recommended",
    )
    claims = _claims(
        ("moe_add_claim_assassin_role", "Merriam-Webster는 암살 역할을 특정 인물에 대한 의도적 살해와 대가·대의 동기의 가능성으로 정의하지만 고정 복장을 제시하지 않는다.", ["add_src_assassin_mw"], "high"),
        ("moe_add_claim_assassin_visual_inference", "특정 표적 자료와 은밀한 접근·감시·이탈의 결합은 사전 정의를 비노골적 장면으로 번역한 설계 추론이다.", ["add_src_assassin_mw"], "medium"),
    )
    common = ["moe_add_claim_assassin_role", "moe_add_claim_assassin_visual_inference"]
    candidates = [
        _candidate(element_id=element_id, slug="cover_infiltration", subtype_id="cover_identity_infiltration", novelty=1, canonical=True, representation_mode="single_frame", integration_role="participatory_action", cues=["잠입", "위장 신분", "표적 동선"], preference_profile={"operation_phase": "approach", "cover_method": "identity"}, prompt="Show one clearly adult covert operative using a plausible service-worker cover identity, comparing one dossier portrait to the same distant adult target while a floor plan marks a concealed approach and a separate unobtrusive exit; keep the scene pre-action and non-graphic.", evidence=["one clearly adult covert operative using a plausible cover identity", "one dossier portrait matched to a distant adult target", "a concealed approach route marked separately from public access"], claim_ids=common, limitation="Cover clothing, a hood, or a tool alone does not establish the deliberate target relation.", tags=["adult_only", "covert_target_relation", "non_graphic_pre_action"]),
        _candidate(element_id=element_id, slug="contract_route_survey", subtype_id="contract_route_surveillance", novelty=0, canonical=False, representation_mode="single_frame", integration_role="participatory_action", cues=["청부", "감시", "시간표"], preference_profile={"operation_phase": "surveillance", "cover_method": "concealed_position"}, prompt="Frame one clearly adult covert operative at a concealed observation point, with one payment token clipped to a dossier portrait, a marked timetable aligned to the same adult target's route, and a separate exit path beyond the observation site; show no attack or injury.", evidence=["one clearly adult covert operative positioned in a concealed observation point", "one payment or mission token linked to the same portrait", "one timed observation aligned to the target's movement"], claim_ids=common, limitation="Money and surveillance are contextual evidence only when both are linked to the same specifically matched target.", tags=["adult_only", "contract_target_relation", "non_graphic_surveillance"]),
        _candidate(element_id=element_id, slug="overwatch_decision", subtype_id="concealed_overwatch_decision", novelty=2, canonical=False, representation_mode="paired_or_sequence", integration_role="participatory_action", cues=["오버워치", "관찰", "이탈 경로"], preference_profile={"operation_phase": "decision", "cover_method": "concealed_position"}, prompt="Depict one clearly adult covert operative in a concealed observation room, matching one dossier portrait and timetable to the same adult target below while a route board separates approach and exit paths; use a second matched state showing the operative aborting and leaving, with no violence depicted.", evidence=["one clearly adult covert operative positioned in a concealed observation point", "one dossier portrait matched to a distant adult target", "one unobtrusive exit route marked beyond the target location"], claim_ids=common, limitation="This candidate evidences preparation and target specificity, not that a killing occurred or succeeded.", tags=["adult_only", "target_specific_planning", "non_graphic_sequence"]),
    ]
    groups = [group["id"] for group in meaning["component_groups"]]
    variants = [
        _variant(variant_id="covert_infiltration", subtype_ids=["cover_identity_infiltration"], group_ids=groups, all_of=["one clearly adult covert operative using a setting-appropriate cover identity", "one dossier portrait visibly matches the same distant adult target", "one floor plan separates concealed approach and unobtrusive exit routes"], any_of=["cover access badge", "timed service schedule", "concealed communication earpiece"], any_minimum=1, topology=["operative, cover credential, dossier portrait, distant target, approach path, and exit path form one deliberate infiltration plan"], camera=["relational medium-wide framing that retains the adult operative, target match, credential, and both route markings"], temporal=[], interaction=["the operative compares the dossier to the same visible target before any attack"], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
        _variant(variant_id="contract_targeting", subtype_ids=["contract_route_surveillance", "concealed_overwatch_decision"], group_ids=groups, all_of=["one clearly adult covert operative at a concealed observation point", "one dossier portrait and timetable match the same distant adult target", "one mission or payment token and one exit route attach to that target plan"], any_of=["clock synchronized to the timetable", "approach and exit paths in different markings", "an abort state with the operative departing"], any_minimum=1, topology=["operative, token, portrait, timetable, visible target, and exit route remain one specifically linked planning chain"], camera=["over-shoulder or split-depth framing that keeps the planning materials and matched distant target legible"], temporal=[], interaction=["the operative observes and verifies the target while no attack or injury is shown"], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
    ]
    return _new_profile(element_id=element_id, ordinal=41, category="role_archetype", label_ko="암살자", label_en="assassin", aliases=aliases, summary="암살자는 외형 직업이 아니라 특정 표적과 은밀한 의도의 관계다. 고정된 검은 복장·후드·무기를 필수화하지 않고, 성인 실행자와 표적 일치 자료, 접근·감시·이탈 계획을 비노골적 사전행동으로 결합한다.", claims=claims, evidence=_evidence("moe_add_image_evidence_assassin", queries=["assassin definition deliberate target fixed appearance", "visual storytelling covert target dossier route surveillance"], confidence="medium", recurring=["specific target dossier", "concealed approach or observation", "timing and exit plan", "cover identity linked to access"], confounds=false, urls=["https://www.merriam-webster.com/dictionary/assassin"], limitations=["The dictionary supports the role meaning, not a universal costume; all visible planning details are design inference.", "A still scene can support target-specific covert intent but cannot prove a later act or outcome.", "Runtime wording omits sensitive role labels while preserving the canonical meaning and non-graphic target relationship."]), meaning=meaning, axes=[_axis("operation_phase", "non-graphic operational phase", [("approach", ["잠입", "접근"]), ("surveillance", ["감시", "관찰"]), ("decision", ["판단", "중단", "이탈"]) ]), _axis("cover_method", "how concealment is evidenced", [("identity", ["위장 신분", "출입증"]), ("concealed_position", ["은폐 위치", "오버워치"])])], candidates=candidates, default_variant_id="covert_infiltration", variants=variants, compatibility=_compatibility(element_id, frame="paired_or_sequence", camera="camera_relational_medium", mechanisms=["actor_action_target_triangle", "negative_space_window"], tags=["adult_only", "target_specific_relation", "runtime_label_omission", "non_graphic_pre_action"]))


def _soldier_profile() -> dict[str, Any]:
    element_id = "moe_soldier"
    aliases = [
        _alias("군인"),
        _alias("병사"),
        _alias("soldier"),
        _alias("military personnel", "carrier"),
        _alias("군장교", "variant", "service_dress_member"),
        _alias("military officer", "variant", "service_dress_member"),
        _alias("보병", "variant", "field_unit_member"),
        _alias("infantry soldier", "variant", "field_unit_member"),
        _alias("mercenary", "related"),
        _alias("police", "related"),
        _alias("warrior", "related"),
    ]
    false = ["generic camouflage fashion", "a firearm alone", "police or private-security uniform", "a mercenary with no military unit evidence", "tactical cosplay"]
    meaning = _meaning(element_id=element_id, ordinal=42, definition="군인은 군 조직의 구성원이며 영어 soldier는 보통 육군 구성원을 더 좁게 가리킨다. 시각적으로는 성인 인물, 일관된 군복과 가상의 부대·계급 표지, 편제·훈련·야전 과업 중 하나가 함께 보여야 한다.", essential=["명백한 성인 군 조직 구성원", "일관된 군복과 가상 부대·계급 표지", "편제·훈련·야전·의식 과업의 구체 관계"], non_equivalents=["위장무늬 패션", "총기만 든 사람", "경찰·민간경비", "부대 증거 없는 용병", "택티컬 코스프레"], axes=["duty_context", "uniform_mode", "unit_relation"], label_policy="allow", forbidden_labels=[], fidelity="exact_componentized", groups=[("adult_military_member", 1, ["one clearly adult member wearing one coherent fictional military uniform", "multiple clearly adult members wearing the same fictional unit uniform"]), ("unit_identity", 2, ["one repeated fictional unit patch", "one readable fictional rank structure", "the same uniform cut and color system across unit members"]), ("military_task_relation", 1, ["the member checks a field map with assigned formation markers", "the unit responds to one formation signal", "the member stands in an organized service ceremony with unit standards"] )], optional=["load-bearing equipment", "protective helmet", "slung non-firing weapon", "radio", "field pack", "medic or chaplain role marking"], false_substitutes=false, do_not_infer=["nationality", "real-world faction", "moral alignment", "combat experience", "current war", "weapon use", "combatant status from uniform alone"], adult_requirement="explicit_adult_always")
    claims = _claims(("moe_add_claim_soldier_definition", "Cambridge는 soldier를 육군 구성원으로 정의하고 군복을 대표적 구분 표지로 든다.", ["add_src_soldier_cambridge"], "high"), ("moe_add_claim_soldier_uniform", "ICRC 자료는 같은 군 부대의 군복이 디자인·색·휘장으로 구성원을 식별하며 위장복도 군복에 포함된다고 설명한다.", ["add_src_soldier_icrc"], "high"))
    common = ["moe_add_claim_soldier_definition", "moe_add_claim_soldier_uniform"]
    candidates = [
        _candidate(element_id=element_id, slug="field_map_member", subtype_id="field_map_unit_member", novelty=1, canonical=True, representation_mode="single_frame", integration_role="participatory_action", cues=["야전", "지도", "부대 패치"], preference_profile={"duty_context": "field", "uniform_mode": "utility"}, prompt="Show one clearly adult member wearing one coherent fictional military utility uniform, with a repeated fictional unit patch and readable rank tab, checking a field map whose markers correspond to the positions of two similarly uniformed adult teammates; keep any weapon slung and inactive.", evidence=["one clearly adult member wearing one coherent fictional military uniform", "one repeated fictional unit patch", "the member checks a field map with assigned formation markers"], claim_ids=common, limitation="Camouflage and equipment alone do not prove military membership without coherent unit identity and task relation.", tags=["adult_only", "fictional_unit", "field_task"]),
        _candidate(element_id=element_id, slug="formation_signal", subtype_id="formation_signal_unit", novelty=0, canonical=False, representation_mode="single_frame", integration_role="participatory_action", cues=["대형", "수신호", "훈련"], preference_profile={"duty_context": "training", "uniform_mode": "utility"}, prompt="Depict multiple clearly adult members in the same fictional unit uniform, repeating one unit patch and uniform cut, as one leader gives a formation hand signal and the others move to the matching marked positions during a non-combat exercise.", evidence=["multiple clearly adult members wearing the same fictional unit uniform", "the same uniform cut and color system across unit members", "the unit responds to one formation signal"], claim_ids=common, limitation="A crowd in matching outdoor clothes is insufficient unless rank, unit markings, and coordinated formation are readable.", tags=["adult_only", "fictional_unit", "formation_training"]),
        _candidate(element_id=element_id, slug="service_ceremony", subtype_id="service_dress_officer", novelty=2, canonical=False, representation_mode="single_frame", integration_role="character_state", cues=["정복", "장교", "의식"], preference_profile={"duty_context": "ceremony", "uniform_mode": "service_dress"}, prompt="Frame one clearly adult member in an original fictional service-dress military uniform, with readable fictional rank structure and a unit patch repeated on a nearby standard, standing in an organized ceremony beside other adult unit members in the same uniform system.", evidence=["one clearly adult member wearing one coherent fictional military uniform", "one readable fictional rank structure", "the member stands in an organized service ceremony with unit standards"], claim_ids=common, limitation="Avoid real national emblems, protected uniforms, and assumptions that rank reveals morality or combat history.", tags=["adult_only", "fictional_unit", "service_dress"]),
    ]
    groups = [group["id"] for group in meaning["component_groups"]]
    variants = [
        _variant(variant_id="field_unit_member", subtype_ids=["field_map_unit_member", "formation_signal_unit"], group_ids=groups, all_of=["clearly adult members wear one coherent fictional military utility-uniform system", "one fictional unit patch and rank structure repeat consistently", "one field-map or formation task visibly organizes the unit"], any_of=["load-bearing field equipment", "slung inactive weapon", "radio or field pack", "marked training positions"], any_minimum=1, topology=["uniform markings identify the same unit while map markers or hand signals connect each adult member to an assigned position"], camera=["medium-wide unit framing retaining full uniform silhouettes, repeated patches, task leader, and mapped or marked positions"], temporal=[], interaction=["adult unit members respond to one shared field-map assignment or formation signal"], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
        _variant(variant_id="service_dress_member", subtype_ids=["service_dress_officer"], group_ids=groups, all_of=["one clearly adult member wears an original fictional service-dress military uniform", "fictional rank and unit markings remain readable and internally consistent", "an organized ceremony and matching unit standard establish military membership"], any_of=["same uniform system on nearby adult members", "formal formation spacing", "one fictional unit standard"], any_minimum=1, topology=["rank marks, unit patch, matching uniforms, formation spacing, and standard form one coherent fictional unit system"], camera=["full or three-quarter ceremonial framing retaining rank, patch, matching members, and unit standard"], temporal=[], interaction=[], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
    ]
    return _new_profile(element_id=element_id, ordinal=42, category="occupational_role", label_ko="군인", label_en="soldier", aliases=aliases, summary="군복 하나가 아니라 성인 인물, 가상의 일관된 부대·계급 표지, 편제·훈련·야전·의식 과업을 묶어 군 조직 구성원을 드러낸다. 총기·위장무늬만으로 군인을 추론하지 않으며 국적·진영·선악은 고정하지 않는다.", claims=claims, evidence=_evidence("moe_add_image_evidence_soldier", queries=["soldier definition army uniform", "military uniform unit insignia identification ICRC"], confidence="high", recurring=["coherent uniform system", "repeated unit and rank insignia", "formation or assigned task", "field or service-dress context"], confounds=false, urls=["https://dictionary.cambridge.org/us/dictionary/english/soldier", "https://casebook.icrc.org/a_to_z/glossary/uniform"], limitations=["The Korean word 군인 is broader than the ordinary English army-specific sense of soldier.", "Uniform evidence does not by itself establish nationality, morality, combat experience, or legal combatant status.", "Runtime uses fictional insignia to avoid copying or implying a real unit."]), meaning=meaning, axes=[_axis("duty_context", "observable military duty", [("field", ["야전", "지도"]), ("training", ["훈련", "수신호"]), ("ceremony", ["의식", "사열"]) ]), _axis("uniform_mode", "uniform family", [("utility", ["전투복", "야전복"]), ("service_dress", ["정복", "장교"])])], candidates=candidates, default_variant_id="field_unit_member", variants=variants, compatibility=_compatibility(element_id, frame="single_frame", camera="camera_relational_medium", mechanisms=["actor_action_target_triangle", "identity_face_feature_anchor"], tags=["adult_only", "fictional_unit_identity", "task_based_role"]))


def _pilot_profile() -> dict[str, Any]:
    element_id = "moe_pilot"
    aliases = [
        _alias("파일럿"),
        _alias("조종사"),
        _alias("pilot"),
        _alias("aviator"),
        _alias("민항기 조종사", "variant", "civil_flight_deck"),
        _alias("airline pilot", "variant", "civil_flight_deck"),
        _alias("전투기 조종사", "variant", "high_performance_flight_deck"),
        _alias("fighter pilot", "variant", "high_performance_flight_deck"),
        _alias("mecha pilot", "related"),
        _alias("racing driver", "related"),
        _alias("ship pilot", "related"),
        _alias("cabin crew", "related"),
    ]
    false = ["a flight helmet alone", "a flight suit outside any aircraft relation", "cabin crew", "air-traffic control staff", "a racing driver", "a mecha operator"]
    meaning = _meaning(element_id=element_id, ordinal=43, definition="파일럿·조종사는 여기서 항공기의 비행경로를 책임지고 비행 조종장치와 계기를 실제로 운용하는 성인 항공기 조종사를 뜻한다. 헬멧·헤드셋·비행복은 보조 표지이며, 손의 조종장치 접촉과 계기·기체 상태의 대응이 핵심이다.", essential=["명백한 성인 항공기 운항자", "비행 조종장치에 대한 실제 접촉·조작", "계기 표시와 항공기 상태의 일치"], non_equivalents=["헬멧이나 비행복만 입은 인물", "객실 승무원", "항공교통관제사", "레이싱 드라이버", "메카 조종자", "선박 도선사"], axes=["aircraft_context", "flight_phase", "control_interface"], label_policy="allow", forbidden_labels=[], fidelity="exact_componentized", groups=[("adult_aircraft_operator", 1, ["one clearly adult aircraft operator seated at the active flight controls", "one clearly adult aircraft operator performing a direct preflight control check"]), ("control_contact", 2, ["one hand physically contacts the yoke or control stick", "the other hand adjusts a throttle or flight-system control", "feet align with visible rudder pedals"]), ("flight_state_evidence", 2, ["primary flight display attitude matches the visible horizon", "navigation display route matches one external runway or waypoint", "control-surface indicator changes with the touched control", "preflight checklist item points to the same tested control"] )], optional=["headset", "microphone", "flight helmet", "harness", "flight suit", "checklist", "civil or high-performance cockpit"], false_substitutes=false, do_not_infer=["nationality", "specific airline", "military allegiance", "gender", "heroic status", "aircraft type from clothing alone"], adult_requirement="explicit_adult_always")
    claims = _claims(("moe_add_claim_pilot_definition", "Cambridge의 항공 의미에서 pilot는 항공기를 비행시키는 사람이며 선박·시험 프로그램 의미와 구분된다.", ["add_src_pilot_cambridge"], "high"), ("moe_add_claim_pilot_controls", "FAA 교재는 조종장치, 주 비행표시장치, 항법표시장치와 비행 상태의 대응을 항공기 운용의 핵심 정보로 다룬다.", ["add_src_pilot_faa"], "high"))
    common = ["moe_add_claim_pilot_definition", "moe_add_claim_pilot_controls"]
    candidates = [
        _candidate(element_id=element_id, slug="civil_flight_deck", subtype_id="civil_aircraft_flight_deck", novelty=1, canonical=True, representation_mode="single_frame", integration_role="participatory_action", cues=["민항", "콕핏", "이륙"], preference_profile={"aircraft_context": "civil", "flight_phase": "departure"}, prompt="Show one clearly adult aircraft operator seated at active civil flight controls, one hand on the yoke and the other adjusting thrust, while the primary flight display attitude matches the runway horizon and the navigation display route begins at that same runway.", evidence=["one clearly adult aircraft operator seated at the active flight controls", "one hand physically contacts the yoke or control stick", "primary flight display attitude matches the visible horizon"], claim_ids=common, limitation="A uniform, headset, or cockpit background alone is insufficient without active control contact and matched instrument state.", tags=["adult_only", "aircraft_controls", "civil_flight_deck"]),
        _candidate(element_id=element_id, slug="light_aircraft_preflight", subtype_id="light_aircraft_control_check", novelty=0, canonical=False, representation_mode="single_frame", integration_role="participatory_action", cues=["소형기", "비행 전 점검", "체크리스트"], preference_profile={"aircraft_context": "light_aircraft", "flight_phase": "preflight"}, prompt="Depict one clearly adult aircraft operator in a light-aircraft cockpit performing a direct preflight control check: one hand moves the yoke while the matching control-surface indicator changes, and the other points to the same item on an open checklist.", evidence=["one clearly adult aircraft operator performing a direct preflight control check", "one hand physically contacts the yoke or control stick", "preflight checklist item points to the same tested control"], claim_ids=common, limitation="The checklist, hand motion, and indicator must refer to the same control rather than serving as unrelated props.", tags=["adult_only", "aircraft_preflight", "control_check_relation"]),
        _candidate(element_id=element_id, slug="high_performance_cockpit", subtype_id="high_performance_aircraft_operator", novelty=2, canonical=False, representation_mode="single_frame", integration_role="participatory_action", cues=["전투기", "고성능기", "HUD"], preference_profile={"aircraft_context": "high_performance", "flight_phase": "airborne"}, prompt="Frame one clearly adult aircraft operator secured in a high-performance cockpit, one hand on the control stick and the other on the throttle, with the attitude display and head-up horizon aligned to the same visible bank angle; keep all insignia fictional.", evidence=["one clearly adult aircraft operator seated at the active flight controls", "the other hand adjusts a throttle or flight-system control", "primary flight display attitude matches the visible horizon"], claim_ids=common, limitation="Helmet, oxygen gear, or harness alone does not prove aircraft operation, and the scene must not imply a real military faction.", tags=["adult_only", "high_performance_aircraft", "fictional_insignia"]),
    ]
    groups = [group["id"] for group in meaning["component_groups"]]
    variants = [
        _variant(variant_id="civil_flight_deck", subtype_ids=["civil_aircraft_flight_deck", "light_aircraft_control_check"], group_ids=groups, all_of=["one clearly adult aircraft operator directly contacts the active flight controls", "a second hand, checklist, or pedal relation confirms an ongoing control task", "instrument attitude or route data matches the visible aircraft environment"], any_of=["civil yoke and thrust controls", "light-aircraft yoke and control-surface check", "headset used while both hands retain control roles"], any_minimum=1, topology=["adult operator, touched control, relevant display or checklist item, and external runway or horizon form one continuous flight-operation relation"], camera=["over-shoulder cockpit view retaining both hands, primary controls, relevant displays, and the matching outside horizon"], temporal=[], interaction=["the adult operator manipulates the control whose state is shown on the corresponding display or checklist"], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
        _variant(variant_id="high_performance_flight_deck", subtype_ids=["high_performance_aircraft_operator"], group_ids=groups, all_of=["one clearly adult aircraft operator is secured at a high-performance flight deck", "one hand contacts the control stick and the other contacts the throttle", "head-up and primary attitude indications match the same visible bank angle"], any_of=["oxygen mask connected to the cockpit system", "flight harness", "fictional unit insignia"], any_minimum=1, topology=["operator hands, stick, throttle, head-up horizon, primary display, and exterior horizon align to one aircraft state"], camera=["tight over-shoulder cockpit framing that preserves both controls, displays, harness, and outside horizon"], temporal=[], interaction=["the adult operator actively maintains the displayed flight attitude"], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
    ]
    return _new_profile(element_id=element_id, ordinal=43, category="occupational_role", label_ko="파일럿·항공기 조종사", label_en="aircraft pilot", aliases=aliases, summary="항공기 의미로 범위를 고정하고, 성인 운항자·조종장치 접촉·계기와 외부 비행상태의 일치를 핵심으로 삼았다. 헬멧·비행복·헤드셋만으로 파일럿을 판정하지 않으며 메카·레이싱·객실승무·선박 의미는 분리한다.", claims=claims, evidence=_evidence("moe_add_image_evidence_pilot", queries=["aircraft pilot definition operates controls", "FAA flight controls primary flight display cockpit visual"], confidence="high", recurring=["adult operator in flight-control seat", "hands on primary controls", "instrument-state and horizon match", "checklist or flight-phase relation"], confounds=false, urls=["https://dictionary.cambridge.org/us/dictionary/english/pilot", "https://www.faa.gov/sites/faa.gov/files/pilots/pilot_handbook.pdf"], limitations=["Pilot has maritime and trial-program meanings; this contract intentionally selects the aircraft sense.", "Uniform and helmet conventions vary by aircraft and operator.", "Displays are simplified visual evidence and must not copy a real airline or military cockpit verbatim."]), meaning=meaning, axes=[_axis("aircraft_context", "aircraft operating environment", [("civil", ["민항", "여객기"]), ("light_aircraft", ["소형기", "훈련기"]), ("high_performance", ["전투기", "고성능기"]) ]), _axis("flight_phase", "observable phase of operation", [("preflight", ["비행 전", "점검"]), ("departure", ["이륙", "활주로"]), ("airborne", ["비행 중", "선회"])])], candidates=candidates, default_variant_id="civil_flight_deck", variants=variants, compatibility=_compatibility(element_id, frame="single_frame", camera="camera_torso_three_quarter", mechanisms=["actor_action_target_triangle", "ev_visible_anchor_point"], tags=["adult_only", "aircraft_controls", "instrument_state_match"]))


def _tights_profile() -> dict[str, Any]:
    element_id = "moe_tights"
    aliases = [
        _alias("타이즈"),
        _alias("tights"),
        _alias("팬티스타킹", "variant", "sheer_footed_pantyhose"),
        _alias("pantyhose", "variant", "sheer_footed_pantyhose"),
        _alias("opaque tights", "variant", "opaque_footed_tights"),
        _alias("불투명 타이즈", "variant", "opaque_footed_tights"),
        _alias("footless tights", "variant", "footless_performance_tights"),
        _alias("발없는 타이즈", "variant", "footless_performance_tights"),
        _alias("leggings", "related"),
        _alias("레깅스", "related"),
    ]
    false = ["two separate thigh-high stockings", "leggings without a visible waist construction", "socks", "a one-piece bodysuit extending over the torso", "body paint"]
    meaning = _meaning(element_id=element_id, ordinal=44, definition="타이즈는 허리에서 양쪽 다리로 하나로 이어져 발 또는 발목까지 밀착해 덮는 편성 의복이다. 팬티스타킹은 얇고 발까지 이어지는 변형이며, 불투명·무발 변형도 있지만 좌우가 분리된 스타킹과는 구조가 다르다.", essential=["허리에서 양쪽 다리로 갈라지는 한 벌 구조", "다리 윤곽을 따르는 밀착 소재", "발을 감싸거나 양쪽 발목에서 끝나는 명확한 종단"], non_equivalents=["좌우가 분리된 스타킹", "허리 구조가 보이지 않는 레깅스", "양말", "상체까지 잇는 보디수트", "바디페인트"], axes=["opacity", "foot_construction", "use_context"], label_policy="allow", forbidden_labels=[], fidelity="exact_componentized", groups=[("waist_to_both_legs", 2, ["one continuous waistband spanning the pelvis", "the same garment divides from the waist into both covered legs", "one continuous gusset or upper join visibly connects both leg tubes"]), ("close_fit_material", 1, ["smooth close-fitting knit follows both leg contours without loose trouser folds", "sheer elastic material shows controlled tonal continuity across both legs", "opaque elastic knit stretches consistently across knees and ankles"]), ("terminal_construction", 1, ["the same garment encloses both feet", "both garment legs end cleanly at the ankles with bare feet beyond"] )], optional=["reinforced toe", "flat waistband", "subtle gusset seam", "dance or fashion context", "nonsexual layered outfit"], false_substitutes=false, do_not_infer=["gender", "sexual intent", "underwear exposure", "school context", "separate stocking construction", "nudity"], adult_requirement="explicit_adult_for_body_focus")
    claims = _claims(("moe_add_claim_tights_definition", "Cambridge는 tights를 허리부터 양쪽 다리와 보통 발까지 밀착해 덮는 의복으로 설명하며 영국식 용법은 팬티스타킹과 겹친다.", ["add_src_tights_cambridge"], "high"), ("moe_add_claim_tights_construction", "V&A 자료는 허리까지 이어진 편성 다리 의복과 탄성섬유가 만드는 매끈한 밀착 구조를 역사적으로 설명한다.", ["add_src_tights_va"], "medium"))
    common = ["moe_add_claim_tights_definition", "moe_add_claim_tights_construction"]
    candidates = [
        _candidate(element_id=element_id, slug="opaque_footed", subtype_id="opaque_footed_fashion_tights", novelty=1, canonical=True, representation_mode="single_frame", integration_role="wardrobe", cues=["불투명", "발까지", "패션"], preference_profile={"opacity": "opaque", "foot_construction": "footed"}, prompt="Dress one clearly adult person in one opaque close-fitting knit garment with a continuous waistband, one visible upper join dividing into both covered legs, consistent stretch across both knees, and the same garment enclosing both feet under a nonsexual layered outfit.", evidence=["one continuous waistband spanning the pelvis", "the same garment divides from the waist into both covered legs", "the same garment encloses both feet"], claim_ids=common, limitation="The garment must read as one waist-to-feet construction, not two thigh-high pieces, socks, body paint, or a torso bodysuit.", tags=["adult_only", "one_piece_legwear", "opaque_footed"]),
        _candidate(element_id=element_id, slug="sheer_pantyhose", subtype_id="sheer_footed_pantyhose", novelty=0, canonical=False, representation_mode="single_frame", integration_role="wardrobe", cues=["팬티스타킹", "시어", "얇은"], preference_profile={"opacity": "sheer", "foot_construction": "footed"}, prompt="Show one clearly adult person wearing one sheer elastic waist-to-feet garment: keep the continuous waistband and upper join visible through a tasteful layered outfit, preserve equal tonal continuity down both legs, and show reinforced toes enclosing both feet.", evidence=["one continuous waistband spanning the pelvis", "sheer elastic material shows controlled tonal continuity across both legs", "the same garment encloses both feet"], claim_ids=common, limitation="Sheerness must not erase the one-piece waistband and join or become a request for underwear exposure.", tags=["adult_only", "one_piece_legwear", "sheer_footed"]),
        _candidate(element_id=element_id, slug="footless_performance", subtype_id="footless_performance_tights", novelty=2, canonical=False, representation_mode="single_frame", integration_role="wardrobe", cues=["무발", "댄스", "발목"], preference_profile={"opacity": "opaque", "foot_construction": "footless"}, prompt="Depict one clearly adult dancer in one opaque close-fitting knit garment with a continuous waistband and upper join, the same material running down both legs with consistent knee stretch, and both garment legs ending cleanly at the ankles above bare feet.", evidence=["one continuous waistband spanning the pelvis", "opaque elastic knit stretches consistently across knees and ankles", "both garment legs end cleanly at the ankles with bare feet beyond"], claim_ids=common, limitation="Footless construction still needs an explicit continuous waist and upper join so it does not collapse into generic leggings.", tags=["adult_only", "one_piece_legwear", "footless_performance"]),
    ]
    groups = [group["id"] for group in meaning["component_groups"]]
    variants = [
        _variant(variant_id="opaque_footed_tights", subtype_ids=["opaque_footed_fashion_tights"], group_ids=groups, all_of=["one clearly adult wearer in one opaque waist-to-feet garment", "one continuous waistband and upper join divide into both close-fitting legs", "the same knit encloses both feet"], any_of=["consistent knee stretch", "reinforced toe shape", "nonsexual layered fashion outfit"], any_minimum=1, topology=["one waistband continues through one upper join into two leg tubes and two enclosed feet without separate stocking tops"], camera=["full-length front or three-quarter view retaining the waistband under a safe layered opening, both legs, ankles, and feet"], temporal=[], interaction=[], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
        _variant(variant_id="sheer_footed_pantyhose", subtype_ids=["sheer_footed_pantyhose"], group_ids=groups, all_of=["one clearly adult wearer in one sheer elastic waist-to-feet garment", "one continuous waistband and upper join remain structurally readable", "equal material tone continues down both legs and encloses both feet"], any_of=["reinforced toes", "flat waistband", "subtle upper join seam"], any_minimum=1, topology=["one waistband continues through the joined upper section into both sheer leg tubes and both enclosed feet"], camera=["tasteful full-length garment view with a layered outfit, avoiding underwear exposure while retaining waist-to-feet continuity"], temporal=[], interaction=[], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
        _variant(variant_id="footless_performance_tights", subtype_ids=["footless_performance_tights"], group_ids=groups, all_of=["one clearly adult wearer in one opaque continuous waist-to-ankle garment", "one waistband and upper join divide into both close-fitting legs", "both garment legs terminate at matching ankle edges above bare feet"], any_of=["dance movement showing knee stretch", "flat waistband", "reinforced ankle bands"], any_minimum=1, topology=["one waistband continues through the upper join into two leg tubes that end symmetrically at the ankles"], camera=["full-body movement framing retaining the continuous waist, both knees, both ankle endings, and bare feet"], temporal=[], interaction=[], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
    ]
    return _new_profile(element_id=element_id, ordinal=44, category="wardrobe", label_ko="타이즈", label_en="tights", aliases=aliases, summary="타이즈를 허리에서 양쪽 다리로 이어지는 한 벌 구조로 정의하고 불투명 유발, 시어 팬티스타킹, 무발 퍼포먼스 변형을 분리했다. 기존의 좌우 분리형 스타킹, 레깅스, 양말, 보디수트와 혼동하지 않는다.", claims=claims, evidence=_evidence("moe_add_image_evidence_tights", queries=["tights definition waist feet joined garment", "V&A history tights elastic waist high legwear"], confidence="high", recurring=["continuous waistband", "joined upper construction", "close fit over both legs", "footed or matching ankle termination"], confounds=false, urls=["https://dictionary.cambridge.org/us/dictionary/english/tights", "https://www.vam.ac.uk/articles/knitted-underwear"], limitations=["British tights overlaps American pantyhose, while fashion and dance usage also includes opaque or footless forms.", "Waist visibility is used only to prove garment construction and must remain nonsexual and adult-only.", "Separate stockings and generic leggings remain distinct even when materials look similar."]), meaning=meaning, axes=[_axis("opacity", "material transparency", [("opaque", ["불투명", "두꺼운"]), ("sheer", ["시어", "얇은", "팬티스타킹"]) ]), _axis("foot_construction", "lower termination", [("footed", ["발까지", "발을 감싼"]), ("footless", ["무발", "발목에서 끝나는"])])], candidates=candidates, default_variant_id="opaque_footed_tights", variants=variants, compatibility=_compatibility(element_id, frame="single_frame", camera="camera_legwear_full_length", mechanisms=["material_specific_response", "internal_part_boundary"], tags=["adult_only", "waist_to_both_legs", "nonsexual_legwear"]))


def _bandage_profile() -> dict[str, Any]:
    element_id = "moe_bandage"
    aliases = [
        _alias("붕대"),
        _alias("bandage"),
        _alias("roller bandage"),
        _alias("롤 붕대"),
        _alias("압박붕대", "variant", "support_compression_wrap"),
        _alias("compression bandage", "variant", "support_compression_wrap"),
        _alias("탄력붕대", "variant", "support_compression_wrap"),
        _alias("elastic bandage", "variant", "support_compression_wrap"),
        _alias("반창고", "related"),
        _alias("adhesive bandage", "related"),
        _alias("Band-Aid", "related"),
        _alias("mummy wrapping", "related"),
        _alias("bandage dress", "related"),
    ]
    false = ["one small adhesive strip", "loose decorative cloth", "full-body mummy wrapping", "a fashion bandage dress", "a restraint or blindfold", "blood or an exposed wound used as the identifier"]
    meaning = _meaning(element_id=element_id, ordinal=45, definition="붕대는 다친 부위를 보호하거나 지지하고 드레싱을 고정하기 위해 신체 일부에 감는 길고 좁은 천·탄성 재료다. 겹치는 감김, 국소 부위, 끝의 고정이 핵심이며 상처·피를 노출할 필요는 없다.", essential=["특정 신체 부위에 국소적으로 감긴 긴 띠", "너비가 일정한 겹침 회전", "매듭·클립·테이프 등 끝 고정 또는 드레싱 지지"], non_equivalents=["작은 접착 반창고", "헐거운 패션 천", "전신 미라 포장", "붕대 드레스", "구속·눈가리개", "피나 상처만 있는 장면"], axes=["care_function", "body_location", "wrap_material"], label_policy="allow", forbidden_labels=[], fidelity="exact_componentized", groups=[("localized_body_wrap", 1, ["one long narrow strip wrapped around one forearm", "one elastic strip wrapped around one ankle joint", "one long narrow strip securing a scalp dressing"]), ("overlap_construction", 2, ["multiple turns overlap by a consistent fraction", "parallel strip edges remain visible across successive turns", "the wrap follows the local limb or head contour without loose trailing cloth"]), ("secure_care_relation", 1, ["one visible clip or taped end secures the final turn", "the wrap visibly retains one clean covered dressing", "the elastic wrap supports the joint while fingers or toes remain unobstructed"] )], optional=["clean covered dressing", "small fastening clip", "medical tape", "circulation-readable fingers or toes", "non-graphic care context"], false_substitutes=false, do_not_infer=["self-harm", "abuse", "captivity", "illness severity", "visible wound", "blood", "mummy identity", "fashion intent"], adult_requirement="none")
    claims = _claims(("moe_add_claim_bandage_definition", "Cambridge는 붕대를 다친 신체 부위를 보호하거나 지지하기 위해 감는 길고 좁은 천으로 정의한다.", ["add_src_bandage_cambridge"], "high"), ("moe_add_claim_bandage_application", "미국 적십자 교재는 롤 붕대가 겹치는 회전으로 드레싱을 덮고 끝을 고정하며 지나치게 조이지 않아야 한다고 설명한다.", ["add_src_bandage_redcross"], "high"))
    common = ["moe_add_claim_bandage_definition", "moe_add_claim_bandage_application"]
    candidates = [
        _candidate(element_id=element_id, slug="forearm_dressing", subtype_id="forearm_dressing_retention", novelty=1, canonical=True, representation_mode="single_frame", integration_role="character_state", cues=["팔", "드레싱", "롤 붕대"], preference_profile={"care_function": "dressing_retention", "body_location": "forearm"}, prompt="Wrap one long narrow clean strip around one forearm, using several turns that overlap by a consistent fraction and retain one fully covered dressing, with the final turn secured by one visible taped end; show no blood or exposed wound.", evidence=["one long narrow strip wrapped around one forearm", "multiple turns overlap by a consistent fraction", "one visible clip or taped end secures the final turn"], claim_ids=common, limitation="Loose cloth, a single adhesive strip, or visible injury without the wrap construction is insufficient.", tags=["non_graphic_care", "localized_wrap", "dressing_retention"]),
        _candidate(element_id=element_id, slug="ankle_support", subtype_id="ankle_compression_support", novelty=0, canonical=False, representation_mode="single_frame", integration_role="character_state", cues=["발목", "압박", "탄력"], preference_profile={"care_function": "joint_support", "body_location": "ankle"}, prompt="Apply one elastic strip around one ankle joint in repeated overlapping turns, keeping parallel strip edges and a visible fastening clip while the toes remain uncovered and naturally colored; show support without an exposed wound.", evidence=["one elastic strip wrapped around one ankle joint", "parallel strip edges remain visible across successive turns", "the elastic wrap supports the joint while fingers or toes remain unobstructed"], claim_ids=common, limitation="Do not render a sock, ankle cuff, or loose ribbon; the repeated wrap path and secured end must remain visible.", tags=["non_graphic_care", "compression_support", "circulation_visible"]),
        _candidate(element_id=element_id, slug="scalp_dressing", subtype_id="scalp_dressing_retention", novelty=2, canonical=False, representation_mode="single_frame", integration_role="character_state", cues=["머리", "드레싱", "고정"], preference_profile={"care_function": "dressing_retention", "body_location": "scalp"}, prompt="Show one long narrow clean strip making several contour-following overlapping turns around the scalp to retain one fully covered dressing, with a visible taped final end and the face, ears, eyes, nose, and mouth unobstructed; show no blood.", evidence=["one long narrow strip securing a scalp dressing", "the wrap follows the local limb or head contour without loose trailing cloth", "the wrap visibly retains one clean covered dressing"], claim_ids=common, limitation="The wrap must not become a blindfold, gag, full mummy covering, or fashion headband.", tags=["non_graphic_care", "localized_wrap", "scalp_dressing"]),
    ]
    groups = [group["id"] for group in meaning["component_groups"]]
    variants = [
        _variant(variant_id="medical_dressing_wrap", subtype_ids=["forearm_dressing_retention", "scalp_dressing_retention"], group_ids=groups, all_of=["one long narrow clean strip wraps one localized body area", "successive turns overlap consistently and follow the body contour", "one secured final end retains one fully covered clean dressing"], any_of=["visible taped end", "small fastening clip", "parallel strip edges across turns"], any_minimum=1, topology=["one continuous strip circles the localized body area through overlapping turns and terminates at one visible fastener over the covered dressing"], camera=["close three-quarter care view retaining the entire wrapped region, successive overlap edges, covered dressing, and final fastener"], temporal=[], interaction=[], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
        _variant(variant_id="support_compression_wrap", subtype_ids=["ankle_compression_support"], group_ids=groups, all_of=["one elastic strip wraps one ankle joint through repeated overlapping turns", "parallel strip edges and one secured final end remain visible", "toes remain uncovered and visually unobstructed beyond the supported joint"], any_of=["small fastening clip", "figure-eight turn around the joint", "consistent elastic stretch"], any_minimum=1, topology=["one continuous elastic strip crosses and circles the joint while ending at one visible fastener short of the toes"], camera=["close full-joint view retaining the lower leg, complete wrap path, ankle, fastening point, and uncovered toes"], temporal=[], interaction=[], confounds=false, modes=["single_frame", "paired_frame", "sequence"]),
    ]
    return _new_profile(element_id=element_id, ordinal=45, category="medical_accessory", label_ko="붕대", label_en="bandage", aliases=aliases, summary="붕대를 국소 신체 부위의 긴 띠, 일정한 겹침 회전, 끝 고정·드레싱 또는 관절 지지로 정의했다. 피나 노출 상처는 요구하지 않으며 반창고·장식 천·미라 포장·구속·붕대 드레스와 분리한다.", claims=claims, evidence=_evidence("moe_add_image_evidence_bandage", queries=["bandage definition long narrow cloth injury support", "Red Cross roller bandage overlapping turns secure dressing"], confidence="high", recurring=["localized long-strip wrap", "consistent overlapping turns", "visible secured end", "covered dressing or supported joint"], confounds=false, urls=["https://dictionary.cambridge.org/us/dictionary/english/bandage", "https://www.redcross.org/content/dam/redcross/training-services/no-index/First%20Aid-CPR-AED-Participant%27s-Manual.pdf"], limitations=["Bandaging technique varies by body part and clinical purpose; the runtime variants are visual constructions, not medical instructions.", "No exposed wound, blood, diagnosis, or cause of injury is required.", "Adhesive strips, restraints, mummy wrapping, and fashion garments remain related or non-equivalent forms."]), meaning=meaning, axes=[_axis("care_function", "visible care purpose", [("dressing_retention", ["드레싱", "보호"]), ("joint_support", ["압박", "지지"]) ]), _axis("body_location", "localized wrapped region", [("forearm", ["팔", "전완"]), ("ankle", ["발목"]), ("scalp", ["머리", "두피"])])], candidates=candidates, default_variant_id="medical_dressing_wrap", variants=variants, compatibility=_compatibility(element_id, frame="single_frame", camera="camera_torso_three_quarter", mechanisms=["internal_part_boundary", "material_specific_response"], tags=["non_graphic_care", "localized_overlap_wrap", "no_injury_cause_inference"]))


def build_asset(asset_dir: str | Path) -> dict[str, Any]:
    root = Path(asset_dir).expanduser().resolve()
    base_path = root / "illustration_moe_grammar_v4.json"
    base_raw = base_path.read_bytes()
    base = json.loads(base_raw.decode("utf-8"))
    base_elements = {str(row["id"]): row for row in base["elements"]}
    profiles = [
        _ntr_refinement(base_elements["moe_ntr_relationship_displacement"]),
        _female_leopard_profile(),
        _cat_pose_profile(),
        _brief_glimpse_profile(),
        _goldsun_profile(),
        _glasses_woman_profile(),
        _literary_woman_profile(),
        _gumiho_profile(),
        _dragon_profile(),
        _dokkaebi_profile(),
        _ghost_profile(),
        _robot_profile(),
        _assassin_profile(),
        _soldier_profile(),
        _pilot_profile(),
        _tights_profile(),
        _bandage_profile(),
    ]
    return {
        "schema": ADDITION_SCHEMA,
        "created_at": CREATED_AT,
        "base_grammar_schema": "subculture-illustration-moe-grammar/v4",
        "base_grammar_v4_sha256": hashlib.sha256(base_raw).hexdigest(),
        "methodology": {
            "research_scope": "Korean, Japanese, and English lexical, academic, museum, standards, cultural-institution, and instructional sources for seventeen visual-semantics profiles: one refinement and sixteen independently selectable concepts.",
            "content_filter": "Exclude minors, age-ambiguous sexualized examples, explicit sexual acts, protected-character copying, and ethnicity inference from appearance.",
            "interpretation_limit": "Definitions and recurring visual features support prompt contracts only; they do not prove popularity, fixed personality, consent, legality, or rendered pixels.",
        },
        "source_count": len(SOURCES),
        "sources": SOURCES,
        "profile_count": len(profiles),
        "compatibility_rules": {
            "hard_conflicts": [
                ["moe_cat_pose_family", "moe_female_leopard_pose"],
                ["moe_glasses", "moe_glasses_woman_archetype"],
                ["moe_stockings", "moe_tights"],
            ],
            "synergies": [
                {
                    "element_ids": ["moe_blond_tanned_delinq_archetype", "moe_ntr_relationship_displacement"],
                    "bridge_clause_en": "Keep the adult man's blond-tan styling independent from the separately evidenced three-role relationship displacement; appearance alone must not create the relationship claim.",
                },
                {
                    "element_ids": ["moe_glasses_woman_archetype", "moe_literary_woman_archetype"],
                    "bridge_clause_en": "Let the same adult woman retain complete identity-salient glasses while her open text, hand action, and gaze independently prove literary engagement.",
                },
            ],
        },
        "profiles": profiles,
    }


def _encoded(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--asset-dir", type=Path, default=Path(__file__).resolve().parents[1] / "assets")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.asset_dir.expanduser().resolve()
    output = root / "research_evidence_moe_elements" / ADDITION_FILENAME
    encoded = _encoded(build_asset(root))
    if args.check:
        if not output.is_file() or output.read_bytes() != encoded:
            raise SystemExit("moe visual additions v1 are stale")
    else:
        output.write_bytes(encoded)
    print(json.dumps({"output": str(output), "sha256": hashlib.sha256(encoded).hexdigest(), "check": args.check}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
