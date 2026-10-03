#!/usr/bin/env python3
"""Author reviewed iconographic alternatives; never edit generated indexes here."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
ASSETS = SKILL / 'assets'
RESEARCH = HERE.parent / 'religion-myth-iconography-20261003'
sys.path.insert(0, str(SKILL / 'scripts'))
from visual_profile_contracts import compile_visual_profile


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def distinct(values):
    return list(dict.fromkeys(v.strip() for v in values if v.strip()))


# English alternatives are independently phrased observations of the same
# source-scoped component. Bare deity labels are discovery text, not exact duties.
COMPONENTS = {
    'attribute_owner': [
        'the diagnostic attribute has its selected recognizable form',
        'the attribute belongs to the specifically depicted figure',
        'the figure and attribute have a readable holding or placement connection'],
    'head_halo': [
        'a radiate or bounded halo is centered behind the depicted head',
        'the head contour remains distinct from the surrounding head halo',
        'the halo occupies the head region rather than enclosing the whole body'],
    'body_mandorla': [
        'an almond-shaped enclosure has distinct upper and lower tips',
        'the depicted full figure is contained inside the same enclosure',
        'the full-body enclosure has a different spatial extent from a head halo'],
    'empty_throne': [
        'an unoccupied throne remains the central represented seat',
        'the selected surrounding symbolic forms belong to that empty seat',
        'the throne remains legible as an unoccupied represented support'],
    'stupa_path': [
        'a central commemorative stupa structure anchors the selected space',
        'a railing surrounds the same central structure',
        'a circulation path runs outside and around the central structure'],
    'earth_touch': [
        'the selected Buddha figure remains seated on its support',
        'the figure own right hand descends toward the ground',
        'the descending hand has a readable position relative to the seat and ground'],
    'vajravarahi_red': [
        'the selected red Vajravarahi form has one face and two hands',
        'the figure own right hand holds the curved knife',
        'the figure own left hand holds the skull cup near the heart',
        'a khatvanga rests at the figure own left elbow or shoulder',
        'a separate small boar head appears above or beside the selected humanlike head'],
    'chakra_blue12': [
        'the selected blue Chakrasamvara figure has twelve connected arms',
        'the selected consort remains a separate embracing figure',
        'each diagnostic attribute belongs to its specified hand and figure'],
    'chakra_white2': [
        'the selected white Chakrasamvara form has one face and two hands',
        'the central figure remains seated in the selected posture',
        'the selected embrace preserves the ownership of the two figures'],
    'hevajra_eight16': [
        'eight faces belong to the same central Hevajra figure',
        'sixteen hands remain connected to that same central figure',
        'each of the sixteen owned hands holds its own skull cup',
        'the selected consort remains a separate figure in the embrace'],
    'cham_mask_performer': [
        'the sculpted face belongs to a separately worn dance mask',
        'the performer body and clothing remain visible beneath the mask',
        'the mask is worn by the performer in the selected dance setting'],
    'nataraja_chola': [
        'the upper hand on the figure own right holds the drum',
        'the upper hand on the figure own left holds the flame',
        'the lower right hand presents the selected protective gesture',
        'the front left arm points toward the raised left foot',
        'the figure own right foot rests upon the Apasmara figure'],
    'ardhana_cambodia': [
        'the Shiva and Parvati halves share one continuous body',
        'the two represented sides retain their selected diagnostic details',
        'the body remains a single joined figure rather than two separate partners'],
    'durga_eight': [
        'eight connected arms belong to the selected Chamba Durga figure',
        'the trident and the attacking foot belong to the same goddess',
        'the buffalo and the emerging humanlike adversary retain their selected relation'],
    'durga_four': [
        'four connected arms belong to the selected Cambodian Durga figure',
        'the four hands retain the wheel conch mace and earth clod attributes',
        'the severed buffalo head remains below the selected goddess figure'],
    'jina_kayotsarga': [
        'the selected Jina stands upright in the kayotsarga posture',
        'the represented body remains unadorned in the selected ascetic form',
        'the arms remain beside the upright body with the selected hand position'],
    'dastar_scope': [
        'the requested turban wrapping retains its selected overlapping cloth layers',
        'the wrapped cloth is visibly worn around the same depicted head'],
    'hodegetria_pointing': [
        'the Virgin own left arm supports the separate child figure',
        'the Virgin own right hand points toward that same child',
        'the two figures and their supporting and pointing hands retain clear ownership'],
    'eleousa_contact': [
        'the child face touches the Virgin cheek in the selected tender-contact form',
        'the child hands and arms belong to the same embracing child',
        'the intimate contact belongs to the two separate depicted figures'],
    'virgin_hybrid_variant': [
        'the Virgin hand points toward the child in the selected hybrid icon',
        'the child face turns upward toward the Virgin',
        'the child position remains separate from full neck-clinging contact'],
    'pieta_support': [
        'the adult dead Christ figure is supported across the Virgin lap',
        'the Virgin supports the body in the selected wrist or torso arrangement',
        'the adult body and its supporting figure remain separate depicted owners'],
    'lucy_plate_eyes': [
        'the two eye attributes rest on the selected wooden plate',
        'the Saint Lucy figure holds that same plate',
        'the other selected hand retains the martyr palm attribute'],
    'bartholomew_knife': [
        'a recognizable knife remains an identification attribute',
        'the knife belongs to the selected Bartholomew figure',
        'the held knife remains distinct from a flaying event'],
    'peter_keys': [
        'the selected keys remain separately recognizable attributes',
        'the keys belong to the depicted Peter figure',
        'the selected hand or garment placement makes key ownership readable'],
    'tefillin_pair': [
        'one tefillin box is worn on the depicted head',
        'a separate tefillin box is worn on the same person upper arm',
        'the visible straps connect to their corresponding head and arm boxes'],
    'tallit_corner_fringe': [
        'the selected tallit cloth has identifiable corners',
        'the tzitzit tassels attach to those selected corners',
        'the corner tassels remain distinct from an ordinary continuous border fringe'],
    'mihrab_minbar': [
        'a recessed mihrab niche occupies the selected prayer-direction wall',
        'a separate stepped minbar stands beside the same niche',
        'the wall niche and stepped pulpit remain distinct architectural structures'],
    'sema_motion_evidence': [
        'the selected performer wears the skirt and headwear of the depicted sema form',
        'the skirt has a readable spread around the moving body',
        'the performer remains supported in the selected turning posture'],
    'buraq_golconda': [
        'the selected Golconda Buraq has a female humanlike face',
        'small separate animal forms construct the selected composite body',
        'the selected independent Buraq figure remains without a rider'],
    'daoist_robe_sky': [
        'a large roundel containing a pagoda belongs to the robe surface',
        'the upper sun with golden crow and moon with jade rabbit occupy separate robe regions',
        'white crane embroidery remains visible across the same robe front'],
    'daoist_robe_xuanwu': [
        'a tortoise form belongs to the selected embroidered robe motif',
        'a separate snake winds around that same tortoise motif',
        'the tortoise and snake remain embroidery on cloth rather than wearer anatomy'],
    'sanshin_old_tiger': [
        'the selected Sanshin painting depicts an old white-haired male figure',
        'a separate tiger belongs to the same selected painting arrangement',
        'the old figure and tiger retain the documented spatial association'],
    'torii_boundary': [
        'two posts support the selected torii crosspiece arrangement',
        'an open passage remains between the same posts',
        'the torii marks the selected approach boundary rather than a filled doorway'],
    'tsukumogami_object_body': [
        'the original utensil form remains recognizable as the creature body',
        'a face or limbs attach to that same object body',
        'the animated object retains its object-specific connected structure'],
    'hyakki_scroll': [
        'multiple selected yokai or object creatures occupy one processional sequence',
        'the sequence belongs to the selected continuous scroll arrangement',
        'the original scroll format remains distinct from a staged creature reconstruction'],
    'meso_horn_crown': [
        'the selected divine headdress has multiple visible horn tiers',
        'the horn forms belong to the worn crown',
        'the crown remains distinct from biological horns growing from the wearer'],
    'marduk_nabu_emblems': [
        'the spade-shaped emblem belongs to the selected Marduk representation',
        'the wedge-shaped emblem belongs to the separate selected Nabu representation',
        'the two emblems retain distinct form and represented ownership'],
    'siren_human_bird': [
        'a human head or upper body belongs to the selected Greek Siren',
        'a bird body wings and feet form the same creature lower structure',
        'the human and avian parts join coherently in one connected creature'],
    'sphinx_greek': [
        'the selected Greek Sphinx has a represented female human head',
        'a lion body belongs to the same creature',
        'the wings attach to that same lion body'],
    'odin_attributes': [
        'the selected Odin representation has one readable eye state',
        'two separate ravens belong to the selected Odin arrangement',
        'the eye state and raven pair remain associated with the same represented figure'],
    'sleipnir_eight_legs': [
        'one continuous horse body belongs to the selected Sleipnir form',
        'eight separately traceable legs attach to that same horse body',
        'the eight legs remain one anatomy rather than two overlapping horses'],
    'babayaga_hut': [
        'the selected hut remains one recognizable building body',
        'chicken-like legs attach beneath that same hut body',
        'the attached legs support the building rather than standing as separate chickens'],
    'ballgame_player': [
        'the selected ballplayer retains the documented waist protection',
        'the protective equipment belongs to the same represented player body',
        'the selected ceramic representation remains distinct from actual stone equipment use'],
    'ganesha_chola': [
        'an elephant head joins the selected humanlike Ganesha body',
        'four connected arms belong to that same selected figure',
        'the upper left and upper right hands retain the lasso and axe',
        'the lower left and lower right hands retain the sweet and broken tusk'],
    'naga_seven_hood': [
        'snake coils form the support beneath the surviving central Buddha form',
        'the surviving central figure retains the selected fragment condition',
        'a seven-headed cobra hood spreads above that same central form'],
    'centaur_rimmer_form': [
        'the selected centaur has a human head and torso',
        'the human torso joins the same horse lower body',
        'the selected original sculpture retains its collapsed and incomplete form'],
    'centaur_nessos_human_knees': [
        'human knees belong to the selected early Nessos centaur form',
        'the figure hands extend forward in the selected kneeling posture',
        'the horse body continues behind that same human-front structure'],
    'centaur_pholos_horse_chest': [
        'a horse chest and body define the selected Pholos form',
        'human legs attach directly to that same equine body',
        'the documented junction retains the form without a separate human abdomen'],
    'chimera_topology': [
        'one lion body forms the connected Chimera creature',
        'a goat head grows from the back of that same lion body',
        'the tail of that same creature ends in a snake head'],
    'hera_polos': [
        'the selected Hera figure wears a tall polos crown',
        'the crown rests on the same represented head',
        'the crown retains its selected tall form rather than a generic low headband'],
    'athena_aegis': [
        'the selected Athena figure retains the helmet and armor',
        'an aegis with a snake-shaped fringe belongs to the same figure',
        'the separate spear belongs to that same represented Athena'],
    'apollo_kithara': [
        'a selected kithara retains its documented stringed instrument form',
        'the instrument belongs to the represented Apollo figure',
        'the hands and instrument retain the selected playing or holding connection'],
    'artemis_bow_quiver': [
        'the selected bow remains a separately recognizable attribute',
        'the quiver belongs to the same represented Artemis figure',
        'the bow and quiver retain their selected hand and body placements'],
    'hermes_staff_winged_sandals': [
        'a separate kerykeion messenger staff belongs to the represented Hermes',
        'wing markers attach to the sandals worn by that same figure',
        'the staff and footwear retain distinct ownership and placement'],
}

# Reviewed complete-role paraphrases of existing owners. No new exact aliases,
# no group removal, and no widening from feather to small Maat figure.
OLD_ALTERNATIVES = {
    'earth_diver_first_land_creation': (
        '태초의 물에서 잠수자가 건져 올린 흙이 수면 접촉을 거쳐 같은 최초 육지로 펼쳐지는 창세 관계',
        'A primordial diver returns with sediment that spreads into the first land through the same surface contact.'),
    'cosmic_egg_world_emergence': (
        '하나의 태초 알 안에 있던 미분화 세계가 같은 껍질 파열을 통해 질서 있는 바깥 세계로 나오는 관계',
        'The same enclosing world egg ruptures as its contained proto-world emerges into an ordered outside cosmos.'),
    'world_parent_separation_creation': (
        '서로 압축되어 있던 하늘과 땅이 힘에 의해 벌어지고 같은 틈에 첫 빛과 생명이 생기는 관계',
        'A force separates compressed sky and earth parents so the same growing interval reveals first light and life.'),
    'axis_mundi_three_realm_connection': (
        '하나의 끊기지 않는 세로 축이 지하·지상·천상과 두 경계를 함께 관통하는 삼계 연결',
        'One uninterrupted vertical world axis crosses both boundaries between distinct lower middle and upper realms.'),
    'moirai_fate_thread_life_allocation': (
        '세 운명 주체가 하나의 생명실을 이어서 뽑고 길이를 재고 끝을 자르는 역할 분담',
        'Three separate fate figures spin measure and cut the same continuous mortal life thread at distinct stations.'),
    'mythic_apotheosis_mortal_divine_transition': (
        '같은 필멸자가 이전 인간 상태의 흔적과 신적 인정 사이에서 신격 상태로 넘어가는 전환',
        'The same formerly mortal figure crosses into divinity while mortal residue and recognition by divine order remain readable.'),
    'katabasis_living_underworld_descent': (
        '살아 있는 여행자가 생자의 영역에서 경계를 내려가 죽은 자의 통치 영역으로 목적 있게 들어가는 사건',
        'A living traveler descends across the boundary into a governed realm of the dead for a readable objective.'),
    'egyptian_heart_weighing_judgment': (
        '심판 대상 앞에서 심장과 마아트 깃털을 단 양팔 저울을 아누비스가 다루고 토트가 기록하며 암미트나 오시리스가 결과를 기다리는 장면',
        'The deceased faces a heart-and-feather balance adjusted by Anubis while Thoth records and Ammit or Osiris establishes the outcome.'),
    'mythic_flood_preservation_vessel': (
        '온 땅을 덮는 홍수 속에서 준비된 보존선이 한정된 생명 계통과 필수 연속성을 지키는 사건',
        'A prepared preservation vessel carries a bounded living lineage and essential continuity through a world-covering deluge.'),
    'chaoskampf_cosmogonic_ordering': (
        '신적 투사가 바다 같은 혼돈 상대를 직접 제압하고 같은 프레임에 질서가 세워지는 결과를 남기는 전투',
        'A divine champion defeats a sea-like dissolutory adversary and the same frame shows the ordering consequence of that defeat.'),
}

# Preserve the full seed observation rather than substituting a nearby cue.
COMPONENTS.update({
    'empty_throne': ['an unoccupied throne remains the represented central seat',
        'a tree appears above or behind that same throne',
        'the worshipping figures remain separate from the empty seat'],
    'vajravarahi_red': ['one humanlike face has a separate small boar-head marker',
        'the figure own right hand holds the curved knife and the left hand holds the skull cup at chest height',
        'the selected red body retains its dancing posture'],
    'chakra_blue12': ['twelve connected arms belong to the selected blue central deity',
        'the main arms embrace the separate red consort while retaining the vajra and bell',
        'the central figure feet rest on blue Bhairava and red Kalaratri'],
    'chakra_white2': ['the selected white central figure has one face and two hands',
        'the vajra and bell remain crossed at the central figure chest',
        'the separate red consort sits on the lap and wraps her legs around the central figure'],
    'hevajra_eight16': ['eight faces belong to the same central Hevajra figure',
        'each of sixteen connected hands holds its own skull cup',
        'the light-blue Nairatmya consort joins the embrace of the central arms'],
    'nataraja_chola': ['the upper right hand holds the drum and the upper left hand holds the flame relative to the figure own body',
        'the lower right hand makes the protective gesture and the front left hand points toward the raised left foot',
        'the right foot presses Apasmara while a ring of flame surrounds the selected figure'],
    'ardhana_cambodia': ['the selected Shiva and Parvati halves share one continuous body',
        'the Parvati side retains its selected head details and long skirt',
        'the Shiva side retains its beard and third eye'],
    'durga_eight': ['eight connected arms of the selected Durga retain their individual weapons',
        'the goddess foot presses the selected buffalo',
        'the trident contact remains connected to the emerging humanlike Mahisha'],
    'jina_kayotsarga': ['the selected unadorned Jina body stands upright',
        'the arms descend beside that same body in the selected still posture',
        'the selected object retains its documented head form'],
    'eleousa_contact': ['the child face rises toward the Virgin neck and cheek',
        'the two faces retain their close selected contact',
        'the Virgin supports the separate child body'],
    'pieta_support': ['the Virgin remains a clothed supporting figure',
        'the adult Christ body remains limp in the selected representation',
        'the lap and arms support that body with the selected wrist grip'],
    'lucy_plate_eyes': ['one hand holds the selected round wooden plate',
        'two separate eye attributes rest on that same plate',
        'the other hand holds the martyr palm'],
    'bartholomew_knife': ['the selected saint and held knife retain a readable ownership connection',
        'the depicted body retains its intact form when a flaying event is not requested'],
    'peter_keys': ['the keys are gathered in the selected figure hand',
        'that same hand contacts the owned keys',
        'the other hand retains the selected distinct gesture'],
    'tefillin_pair': ['a black leather tefillin box is worn on the depicted head',
        'a separate tefillin box is worn on the same person upper arm',
        'the straps visibly connect the boxes to their corresponding body regions'],
    'tallit_corner_fringe': ['the selected shawl has identifiable cloth corners',
        'the tzitzit tassels attach at those same corners',
        'the shawl body and separate corner tassels retain their connected structure'],
    'sema_motion_evidence': ['the selected sema clothing and performer arrangement remain distinct',
        'the body and cloth spread suggest the selected turning posture in a still frame',
        'the selected ceremony setting remains distinct from the performer visible appearance'],
    'sanshin_old_tiger': ['the selected Sanshin figure has white hair and a long beard',
        'a mountain and valley setting surrounds the selected figure',
        'the same figure sits leaning against a separate tiger'],
    'torii_boundary': ['two posts and the selected transverse members form one torii gateway',
        'the gateway separates readable approach and beyond spaces'],
    'meso_horn_crown': ['a crown rests on the selected represented head',
        'overlapping pairs of horns form tiers of that same crown',
        'the horned crown remains distinct from the head own anatomy'],
    'sleipnir_eight_legs': ['eight legs attach to one continuous Sleipnir horse body',
        'each of the eight legs retains a traceable joint and hoof',
        'the selected anatomy remains one body rather than two overlapping horses'],
    'ballgame_player': ['the selected representation retains its ballplayer body',
        'the documented equipment surrounds the player waist',
        'the same player body visibly wears that waist equipment'],
    'ganesha_chola': ['the selected elephant head joins one humanlike body with four arms',
        'the upper left hand holds the lasso and the upper right hand holds the axe',
        'the lower left hand holds the sweet and the lower right hand holds the broken tusk'],
    'centaur_rimmer_form': ['the selected centaur retains its human head and torso',
        'that human torso joins the same horse lower body',
        'the original sculpture retains its rising-from-collapse pose and truncated sculpted arms'],
    'chimera_topology': ['a lion body and forward lion head form one connected Chimera',
        'a separate goat head grows from the middle of that same back',
        'the tail of that same creature ends in a snake head'],
    'hera_polos': ['the selected polos retains its tall crown form',
        'the crown is worn on the same represented head'],
    'apollo_kithara': ['the represented Apollo remains distinct from the separate kithara',
        'the same figure visibly holds the owned stringed instrument'],
    'artemis_bow_quiver': ['the selected bow retains its curved body and bowstring',
        'a separate quiver remains readable',
        'the same represented figure owns and holds or wears both attributes'],
})

OLD_COMPONENT_ALTERNATIVES = {
    'earth_diver_first_land_creation': [
        'an expanse of primordial water has no established shore or land before the retrieval event',
        'the same diving agent makes a connected trip below the water and back toward its surface',
        'the returning diver retains a small separate clod of sediment recovered from below the water',
        'the recovered sediment and its diver arrive together at the water surface along one continuous return path',
        'the first visible land expands from the very sediment that the diver has just recovered'],
    'cosmic_egg_world_emergence': [
        'one dominant primordial egg retains its enclosed form while opening along the selected rupture',
        'luminous or material potential for the world remains contained within the same bounded egg interior',
        'a single breaking line and outward opening visibly connect the enclosed egg with its emerging state',
        'the same shell and interior substance continue into the cosmic structures emerging from the egg',
        'distinct sky earth or ordered world layers emerge from the egg itself within the selected scene'],
    'world_parent_separation_creation': [
        'the sky parent and earth parent form two separate bodies or planes initially touching each other',
        'the compressed initial interval leaves no open habitable space between the upper and lower parents',
        'a traceable force or agent pushes the same upper and lower parent bodies away from each other',
        'a continuous vertical interval grows between the two parent bodies that previously remained in contact',
        'first light and newly habitable world space occupy the same interval opened by the separating force'],
    'axis_mundi_three_realm_connection': [
        'a single dominant vertical structure at the center of the scene forms the selected world axis',
        'three distinguishable lower middle and upper realms surround the very same central world axis',
        'the single axis passes through the actual boundary separating the lower realm from the middle realm',
        'the same axis passes through the actual boundary separating the middle realm from the upper realm',
        'a continuous path or energy flow along that same axis joins all three represented realms'],
    'moirai_fate_thread_life_allocation': [
        'three individually distinguishable fate figures each occupy a separate readable station of the thread work',
        'the first fate figure draws or spins the origin of the single represented life thread',
        'the second fate figure measures the allotted length of the very same continuous life thread',
        'the third fate figure uses its cutting action on the endpoint of that same life thread',
        'one unbroken mortal life thread links all three spinning measuring and cutting work stations'],
    'mythic_apotheosis_mortal_divine_transition': [
        'the same individual retains readable continuity between the former mortal state and current divine elevation',
        'a surviving worldly token garment tool or wound makes the earlier mortal status of that individual readable',
        'the same person traverses a visible threshold from mortal ground toward a separate divine level',
        'a distinguishable divine assembly receives crowns or invests the same mortal figure as it arrives',
        'new radiance regalia or a divine seat is visibly granted to that person during the elevation'],
    'katabasis_living_underworld_descent': [
        'a single traveler retains a visible sign of living agency such as breathing warmth or an active grip',
        'a daylight vegetation or settlement cue of the living human world remains behind that same traveler',
        'a stair slope gate or river passage gives the traveler a readable downward boundary crossing',
        'a separate chthonic destination occupies the space below or beyond the threshold crossed by that traveler',
        'a mission cue guide token named objective or retrieval object accompanies the same living traveler'],
    'egyptian_heart_weighing_judgment': [
        'one identifiable deceased person stands or kneels before the balance as the subject of the judgment',
        'the same two-pan scale places a human heart on one pan and the feather of Maat on the other',
        'Anubis attends adjusts or checks that same central balance as the clearly owned weighing role',
        'Thoth writes the result of that same weighing beside the balance as its separate recording role',
        'Ammit waits by the balance or Osiris receives the outcome as the readable consequence of that judgment'],
    'mythic_flood_preservation_vessel': [
        'the selected vessel shows provisions compartments or another organized preparation for the approaching flood',
        'a deliberately bounded lineage of living people animals or seeds occupies the same prepared vessel',
        'closed hatches tied provisions sheltered decks or sealed seams protect that selected living cargo',
        'the deluge covers ordinary ground markers at world scale rather than merely surrounding one local boat',
        'grounding receding water an exposed peak or a released bird establishes survival beyond that same flood'],
    'chaoskampf_cosmogonic_ordering': [
        'a champion belonging to the explicitly selected tradition stands separately from its adversary on the ordering side',
        'a primordial sea storm serpent or dissolving adversary belongs to that same selected tradition and remains distinguishable',
        'weapons forces opposing forces and contact connect the two combatants through a readable fight geometry',
        'the same adversary visibly changes from active resistance toward a defeated or divided bodily state',
        'new world boundaries matter stable realms or sovereign order arise visibly from that same defeat'],
    'griffin_eagle_lion_topology': [
        'one eagle head and hooked beak continue through a forward neck into the same creature forebody',
        'a pair of feathered wings attach behind the shoulders of that same eagle forebody',
        'the front chest and front feet retain avian structure or talons on the same hybrid creature',
        'the same creature rear retains a lion torso rear legs paws and a connected lion tail',
        'the feathered front and furred rear share continuous skeletal and limb junctions within one anatomy'],
}

# Reviewed source-scoped observations with source/variant review still pending.
# They are optional layout bundles only and have no automatic hard-profile link.
ADVISORY_COMPONENTS = {
    'five_buddha_families': ['the selected central Vairocana is white and has the wheel emblem',
        'the eastern blue Akshobhya has the vajra and western red Amitabha has the lotus',
        'the southern yellow Ratnasambhava has the jewel and northern green Amoghasiddhi has the crossed vajra'],
    'khatvanga_owner': ['the selected attribute remains a long staff',
        'the staff rests in the same figure own bent left elbow',
        'that staff extends toward the same figure left shoulder'],
    'vajrakila_dagger': ['the selected wrathful upper figure remains the represented owner',
        'the same lower body extends into a dagger blade',
        'three blade faces meet along the selected dagger structure'],
    'mandala_architecture': ['the square mandala palace has four selected entrances',
        'the central figure and lotus zone retain their selected placement',
        'outer vajra and flame rings surround that same selected palace'],
    'mandala_foundation': ['two intersecting triangles form the selected mandala foundation',
        'the central deity and that same foundation retain their selected relative position'],
    'chinnamasta_streams': ['the selected deity holds its own separate represented head',
        'three blood streams originate from the same represented neck',
        'the three streams connect separately to the held head and two companions'],
    'mithuna_couple': ['two adorned figures remain separate represented partners',
        'their arms bodies and gazes retain the selected embracing relationship',
        'the selected pair retains its temple-relief representation'],
    'five_ks_visible': ['the visible kara remains a metal bracelet on the selected wearer',
        'only the kanga and kirpan visible with the selected clothing enter the depicted arrangement'],
    'anastasis_harrowing': ['the Christ figure has readable lifting contact with the lower represented figure',
        'Adam and Eve retain their separate selected positions',
        'the lower realm retains its selected gates and space'],
    'dormition_soul': ['the Virgin body lies recumbent in the selected scene',
        'a separate Christ figure stands behind that same recumbent body',
        'a small soul representation is held by Christ rather than replacing the Virgin body'],
    'kaba_focus': ['a cubical central building anchors the selected space',
        'a separate surrounding worship space remains readable',
        'the central building remains distinct from the surrounding figures and paths'],
    'heart_maat_figure': ['one balance pan holds the represented heart',
        'the opposite pan holds a small seated Maat figure',
        'the feather marker belongs to the small Maat figure head'],
    'faience_visible_finish': ['the selected object retains its visible glaze sheen',
        'the selected specimen color and wear remain separately readable'],
    'enki_fish_streams': ['water streams extend from the selected represented figure',
        'fish remain inside those same streams',
        'the selected crown and seated form belong to that represented figure'],
    'babayaga_mortar': ['a mortar-shaped vessel forms the selected travel support',
        'the Baba Yaga figure remains inside that same vessel',
        'a separate pestle remains a distinct owned attribute'],
    'mami_wata_snake': ['a female figure is represented in the selected source form',
        'a snake is held or draped by that same represented figure',
        'the lower body retains only the form established by the selected original'],
    'coatlicue_sculpture': ['the selected skirt is composed of snake forms',
        'hands hearts and a central skull form the selected necklace',
        'a double-headed snake ornament belongs to the selected waist'],
    'ngalyod_regional': ['the selected artist work retains its represented snake body',
        'the composite animal parts belong to that same selected specimen',
        'a feather headdress is retained only when it belongs to that selected form'],
    'barong_rangda_balance': ['the two selected mask forms remain distinguishable',
        'each mask clothing and wearer has a readable wearing connection',
        'the selected performance retains the documented relative positions'],
    'rebis_two_heads': ['two heads connect to one represented body',
        'the wings belong to the selected print variant',
        'the mirror and stone attributes belong to their selected hands'],
    'rebis_three_legs': ['two head-and-torso regions remain distinguishable',
        'the two regions join at the pelvis',
        'three shared legs and the rear phoenix retain the selected arrangement'],
    'baphomet_levi_scope': ['the goat-like head belongs to the selected Levi representation',
        'the humanlike body retains only the contrasting signs of that selected print'],
    'anasyrma_lifting': ['the selected wearer retains a readable skirt boundary',
        'the same wearer hands grasp and lift that skirt',
        'the moving garment exposes only the body region specified in the selected request'],
    'danae_gold': ['the Danae figure remains the selected represented subject',
        'the represented golden shower descends from above that same figure',
        'the bed and companion retain the selected painting relationship'],
    'minotaur_bull_head': ['the selected creature has a bull head',
        'the visible arms and upper body retain their human form',
        'the lower body remains occluded behind the selected building'],
    'cerberus_two_heads': ['two dog heads attach to the same represented dog body',
        'a separate snake marker grows from the top of each selected head'],
}


# These are eligibility cues in the frozen subject/setting/event, not exact
# activation aliases. Distinctive observable wording supports discovery without
# letting generic words such as human, body, face or portrait select a variant.
PRIMARY_CUES = {
    'attribute_owner': 'iconographic iconography 지물 도상',
    'head_halo': 'halo nimbus radiate 두광 후광',
    'body_mandorla': 'mandorla almond-shaped 전신광 만돌라',
    'empty_throne': 'throne bodhi 보좌 보리수',
    'stupa_path': 'stupa circumambulation 탑 회랑',
    'earth_touch': 'buddha bhumisparsha earth-touching 부처 불상 항마성도',
    'vajravarahi_red': 'vajravarahi khatvanga boar 바즈라바라히 금강해모',
    'chakra_blue12': 'chakrasamvara twelve-armed 차크라삼바라 승락',
    'chakra_white2': 'chakrasamvara 차크라삼바라 승락',
    'hevajra_eight16': 'hevajra sixteen-armed 헤바즈라 희금강',
    'cham_mask_performer': 'cham 참춤 mask 가면',
    'nataraja_chola': 'nataraja apasmara 나타라자 아파스마라',
    'ardhana_cambodia': 'ardhanarishvara shiva parvati 아르다나리슈바라 시바 파르바티',
    'durga_eight': 'durga buffalo 두르가 물소',
    'durga_four': 'durga buffalo 두르가 물소',
    'jina_kayotsarga': 'jina kayotsarga digambara 지나 카요트사르가 디감바라',
    'dastar_scope': 'dastar turban 다스타르 터번',
    'hodegetria_pointing': 'hodegetria virgin theotokos 호데게트리아 성모',
    'eleousa_contact': 'eleousa virgin theotokos 엘레우사 성모',
    'virgin_hybrid_variant': 'hodegetria virgin theotokos 호데게트리아 성모',
    'pieta_support': 'pieta mary christ 피에타 성모 그리스도',
    'lucy_plate_eyes': 'lucy lucia 루치아',
    'bartholomew_knife': 'bartholomew 바르톨로메오',
    'peter_keys': 'peter apostle 베드로',
    'tefillin_pair': 'tefillin phylacteries 테필린',
    'tallit_corner_fringe': 'tallit tzitzit prayer-shawl 탈리트 치치트',
    'mihrab_minbar': 'mihrab minbar mosque 미흐라브 민바르 모스크',
    'sema_motion_evidence': 'sema mevlevi dervish 세마 데르비시 메블레비',
    'buraq_golconda': 'buraq 부라크',
    'daoist_robe_sky': 'daoist taoist crow rabbit 도교 도포 까마귀 옥토끼',
    'daoist_robe_xuanwu': 'daoist taoist xuanwu tortoise 도교 현무 거북',
    'sanshin_old_tiger': 'sanshin 산신 산신도',
    'torii_boundary': 'torii 도리이',
    'tsukumogami_object_body': 'tsukumogami animated-utensils 쓰쿠모가미',
    'hyakki_scroll': 'hyakki yokai 요괴 백귀야행',
    'meso_horn_crown': 'mesopotamian horned-crown 메소포타미아 뿔관',
    'marduk_nabu_emblems': 'marduk nabu 마르두크 나부',
    'siren_human_bird': 'siren sirens bird-bodied 사이렌 세이렌',
    'sphinx_greek': 'sphinx 스핑크스',
    'odin_attributes': 'odin ravens 오딘 까마귀',
    'sleipnir_eight_legs': 'sleipnir eight-legged 슬레이프니르',
    'babayaga_hut': 'babayaga baba chicken-legged 바바야가 닭발',
    'ballgame_player': 'ballgame mesoamerican 공놀이 메소아메리카',
    'ganesha_chola': 'ganesha elephant-headed 가네샤',
    'naga_seven_hood': 'naga seven-hooded 나가',
    'centaur_rimmer_form': 'centaur centaurs 켄타우로스',
    'centaur_nessos_human_knees': 'centaur nessos 켄타우로스 네소스',
    'centaur_pholos_horse_chest': 'centaur pholos 켄타우로스 폴로스',
    'chimera_topology': 'chimera chimaera lion-goat 키마이라',
    'hera_polos': 'hera polos 헤라 폴로스',
    'athena_aegis': 'athena aegis 아테나 아이기스',
    'apollo_kithara': 'apollo kithara cithara 아폴론 키타라',
    'artemis_bow_quiver': 'artemis 아르테미스',
    'hermes_staff_winged_sandals': 'hermes caduceus 헤르메스 전령장',
    'five_buddha_families': 'buddhas mandala 오불 만다라',
    'khatvanga_owner': 'khatvanga 캇방가',
    'vajrakila_dagger': 'vajrakila phurba 바즈라킬라 푸르바',
    'mandala_architecture': 'mandala 만다라',
    'mandala_foundation': 'mandala hexagram 만다라 육각별',
    'chinnamasta_streams': 'chinnamasta 친나마스타',
    'mithuna_couple': 'mithuna 미투나',
    'five_ks_visible': 'kirpan kangha kara kesh kachera 키르판 캉가 카라 케쉬 카체라',
    'anastasis_harrowing': 'anastasis harrowing 아나스타시스',
    'dormition_soul': 'dormition koimesis 안식 성모',
    'kaba_focus': 'kaaba kaba 카바',
    'heart_maat_figure': 'maat balance weighing 마아트 계량 저울',
    'faience_visible_finish': 'faience 파이앙스',
    'enki_fish_streams': 'enki ea 엔키',
    'babayaga_mortar': 'babayaga baba mortar 바바야가 절구',
    'mami_wata_snake': 'mami wata 마미와타',
    'coatlicue_sculpture': 'coatlicue 코아틀리쿠에',
    'ngalyod_regional': 'ngalyod rainbow-serpent 응갈리오드 무지개뱀',
    'barong_rangda_balance': 'barong rangda 바롱 랑다',
    'rebis_two_heads': 'rebis 레비스',
    'rebis_three_legs': 'rebis three-legged 레비스',
    'baphomet_levi_scope': 'baphomet 바포메트',
    'anasyrma_lifting': 'anasyrma 아나시르마',
    'danae_gold': 'danae 다나에',
    'minotaur_bull_head': 'minotaur bull-headed 미노타우로스',
    'cerberus_two_heads': 'cerberus kerberos 케르베로스',
}


# Alternative observations are scoped to the represented form, never to a real
# wearer's belief or identity. Short sense-specific phrases permit optional
# discovery; only the complete canonical request can create a hard obligation.
DISCOVERY_PARAPHRASES = {
    'attribute_owner': ['an iconographic attribute held by its represented owner', '지정된 인물이 직접 들거나 착용한 식별 지물'],
    'head_halo': ['head nimbus', 'head-centered halo', '머리 뒤에 중심을 둔 두광'],
    'body_mandorla': ['whole-body mandorla', 'full-body mandorla', '전신을 둘러싸는 끝이 뾰족한 아몬드형 광배'],
    'empty_throne': ['an empty throne beneath a Bodhi tree', '보리수 아래 인물이 앉지 않은 상징적 보좌'],
    'stupa_path': ['a circumambulation path around a railed stupa', '난간으로 둘러싼 탑의 바깥을 도는 순회 경로'],
    'earth_touch': ['a seated Buddha reaching the right hand down to earth', '앉은 부처가 자신의 오른손을 땅으로 내리는 항마성도 자세'],
    'vajravarahi_red': ['red two-armed Vajravarahi with a separate small boar head', '작은 멧돼지 머리가 덧붙은 붉은 두 팔 바즈라바라히'],
    'chakra_blue12': ['blue twelve-armed Chakrasamvara embracing a separate consort', '별도 배우자를 끌어안는 청색 열두 팔 차크라삼바라'],
    'chakra_white2': ['white seated two-armed Chakrasamvara with a separate consort', '흰색 두 팔 좌상 차크라삼바라와 별도 배우자'],
    'hevajra_eight16': ['eight-faced sixteen-handed Hevajra holding a cup in each hand', '여덟 얼굴과 열여섯 잔을 든 열여섯 손의 헤바즈라'],
    'cham_mask_performer': ['a cham dancer visibly wearing a sculpted face mask', '몸과 옷 위에 조형 얼굴 가면을 쓴 참춤 공연자'],
    'nataraja_chola': ['Chola Nataraja dancing on Apasmara with a drum and flame', '북과 불꽃을 들고 아파스마라를 밟은 촐라 나타라자'],
    'ardhana_cambodia': ['a single Cambodian Ardhanarishvara body joining Shiva and Parvati halves', '시바와 파르바티의 두 절반을 한 몸에 합친 캄보디아 아르다나리슈바라'],
    'durga_eight': ['eight-armed Chamba Durga attacking the emerging buffalo adversary', '물소에서 나오는 적을 공격하는 참바의 여덟 팔 두르가'],
    'durga_four': ['four-armed Cambodian Durga above a severed buffalo head', '잘린 물소 머리 위에 선 캄보디아의 네 팔 두르가'],
    'jina_kayotsarga': ['an unadorned upright Jina in kayotsarga', '장식 없이 곧게 선 카요트사르가 자세의 지나'],
    'dastar_scope': ['overlapping layers of cloth wrapped into a dastar', '겹친 천 층이 머리를 감싼 다스타르'],
    'hodegetria_pointing': ['the Virgin supports the child on her left arm and points with her right hand', '성모가 자신의 왼팔로 아기를 받치고 오른손으로 그 아기를 가리킨다'],
    'eleousa_contact': ['the child presses its cheek to the Virgin and clings to her neck', '아기가 성모의 볼에 얼굴을 맞대고 목을 감싸는 엘레우사'],
    'virgin_hybrid_variant': ['a pointing Virgin with an upward-looking child in a hybrid icon', '성모의 지시 손과 위로 올려다보는 아기가 함께 있는 혼합 성모상'],
    'pieta_support': ['the Virgin cradles the dead adult Christ across her lap', '성모가 무릎 위에 성인 그리스도의 죽은 몸을 받치는 피에타'],
    'lucy_plate_eyes': ['Saint Lucy holds a plate bearing two eyes and a martyr palm', '두 눈이 놓인 접시와 순교 야자 가지를 든 성 루치아'],
    'bartholomew_knife': ['Bartholomew holding a knife as an identifying attribute', '식별 지물인 칼을 든 바르톨로메오'],
    'peter_keys': ['keys visibly owned by the represented Apostle Peter', '사도 베드로의 손이나 옷에 소유가 드러나는 열쇠'],
    'tefillin_pair': ['paired tefillin boxes on the head and upper arm with their own straps', '머리와 윗팔의 별도 상자와 각 끈으로 이루어진 테필린'],
    'tallit_corner_fringe': ['tzitzit tassels attached to the corners of a tallit', '탈리트의 모서리에 각각 달린 치치트 술'],
    'mihrab_minbar': ['a recessed mihrab beside a separate stepped minbar', '오목한 미흐라브 옆의 별도 계단식 민바르'],
    'sema_motion_evidence': ['a sema performer turning with a spread skirt and selected headwear', '지정된 머리쓰개와 퍼진 치마를 착용한 세마 회전 공연자'],
    'buraq_golconda': ['a riderless Golconda Buraq assembled from small animals with a humanlike female face', '여성형 얼굴과 작은 동물들로 몸을 구성한 기수 없는 골콘다 부라크'],
    'daoist_robe_sky': ['Daoist robe embroidery showing a pagoda roundel, sun crow and moon rabbit', '탑 원형문과 해의 까마귀 및 달의 옥토끼가 놓인 도교 도포 자수'],
    'daoist_robe_xuanwu': ['tortoise-and-entwined-snake chest emblem', 'tortoise-and-coiled-snake emblem', '같은 거북 껍질을 뱀이 감싸는 현무 도포 자수'],
    'sanshin_old_tiger': ['a Sanshin painting pairing a white-haired old man with a tiger', '백발 노인과 호랑이를 함께 배치한 산신도'],
    'torii_boundary': ['an open torii passage between two supporting posts', '두 기둥 사이가 열린 도리이 경계 통로'],
    'tsukumogami_object_body': ['an animated utensil whose face and limbs attach to its original object body', '본래 기물 몸에 얼굴과 팔다리가 붙은 쓰쿠모가미'],
    'hyakki_scroll': ['a continuous Hyakki scroll procession of yokai and animated utensils', '연속 두루마리 안에서 요괴와 기물이 행렬을 이룬 백귀야행'],
    'meso_horn_crown': ['a Mesopotamian headdress with multiple tiers of attached horns', '여러 층의 뿔이 붙은 메소포타미아 관모'],
    'marduk_nabu_emblems': ['Marduk owns the spade emblem and Nabu owns the separate wedge emblem', '마르두크의 삽형 표식과 나부의 별도 쐐기형 표식'],
    'siren_human_bird': ['human-headed avian Greek siren', 'a human head joined to one feathered bird trunk with wings and bird feet', '인간 머리가 날개와 새 발이 달린 하나의 새 몸에 이어지는 그리스 세이렌'],
    'sphinx_greek': ['a winged Greek sphinx with a female human head on one lion body', '여성형 인간 머리와 날개가 한 사자 몸에 붙은 그리스 스핑크스'],
    'odin_attributes': ['one-eyed Odin accompanied by a pair of ravens', '한쪽 눈 상태와 두 까마귀를 함께 보이는 오딘'],
    'sleipnir_eight_legs': ['eight separately attached legs on one Sleipnir horse', '한 말 몸에 여덟 다리가 따로 연결된 슬레이프니르'],
    'babayaga_hut': ['one Baba Yaga hut standing on attached chicken legs', '닭 다리가 건물 아래에 붙어 받치는 바바야가의 오두막'],
    'ballgame_player': ['a ceramic Mesoamerican ballplayer wearing documented waist protection', '허리 보호 장비를 착용한 메소아메리카 공놀이 선수 도자상'],
    'ganesha_chola': ['four-armed Chola Ganesha with an elephant head, lasso, axe, sweet and tusk', '코끼리 머리와 올가미 도끼 과자 상아를 지닌 촐라의 네 팔 가네샤'],
    'naga_seven_hood': ['a fragmentary Buddha supported by snake coils beneath a seven-headed cobra hood', '뱀 코일 위의 잔존 부처와 그 위를 덮는 일곱 코브라 머리'],
    'centaur_rimmer_form': ['the collapsed incomplete Rimmer centaur sculpture joining human torso and horse body', '인간 몸통과 말 몸을 잇는 쓰러진 불완전 리머 켄타우로스 조각'],
    'centaur_nessos_human_knees': ['early Nessos with human knees and a horse body continuing behind', '인간 무릎 뒤로 말 몸이 이어지는 초기 네소스 켄타우로스'],
    'centaur_pholos_horse_chest': ['Pholos with a horse chest and human legs attached directly to the equine body', '말 가슴과 몸에 인간 다리가 직접 연결된 폴로스'],
    'chimera_topology': ['lion-goat-snake chimera', 'a leonine body with a horned goat head growing from the same back and an ophidian head at the end of its tail', '같은 사자 등에서 염소 머리가 자라고 그 꼬리 끝이 뱀 머리인 키마이라'],
    'hera_polos': ['Hera wearing a tall polos crown', '높은 폴로스 관을 머리에 쓴 헤라'],
    'athena_aegis': ['helmeted Athena with snake-fringed aegis and an owned spear', '투구와 뱀 술 아이기스 및 자신의 창을 지닌 아테나'],
    'apollo_kithara': ['Apollo visibly holding or playing the selected kithara', '지정된 키타라를 직접 들거나 연주하는 아폴론'],
    'artemis_bow_quiver': ['Artemis carrying her bow and wearing her quiver', '자신의 활을 들고 화살통을 착용한 아르테미스'],
    'hermes_staff_winged_sandals': ['Hermes with an owned messenger staff and wings on his worn sandals', '자신의 전령장과 착용한 샌들 날개를 함께 지닌 헤르메스'],
}

# Observation-level alternatives supplement the complete-form paraphrases.
# These are optional discovery cues for a represented body junction, not
# substitutes for any ALL_OF group or literal prompt-evidence field.
DISCOVERY_JUNCTIONS = {
    'siren_human_bird': ['human head and neck join directly into one feather-covered bird trunk',
        'a human neck connected directly to the same feathered bird torso',
        '인간 목이 같은 깃털 덮인 새 몸통으로 직접 이어진다'],
    'chimera_topology': ['goat head and neck grow upward from the middle of that same back',
        'a horned goat neck grows from the same lion back',
        '같은 사자 등의 가운데에서 염소 머리와 목이 자란다'],
}


def main():
    seeds = {u['unit_id']: u for u in read(RESEARCH / 'SEMANTIC-UNITS.json')['units']}
    profiles = []
    slot_entries = []
    bundles = []
    mappings = []
    for uid, english in COMPONENTS.items():
        unit = seeds[uid]
        pid = 'ri_' + uid
        # Canonical complete-form exact terms are deliberately longer than bare
        # deity names. Other labels and variants remain advisory discovery.
        exact_en = '; '.join(english)
        exact_ko = '; '.join(unit['observable_components'])
        alternatives = distinct([unit['title'], unit['description_en'],
            unit['title'] + ': ' + exact_ko, exact_en, *DISCOVERY_PARAPHRASES[uid]])
        authored = []
        for i, phrase in enumerate(english, 1):
            ko = unit['observable_components'][min(i-1, len(unit['observable_components'])-1)]
            # If the textual seed had fewer groups, do not duplicate a broad
            # Korean sentence as proof for multiple independent English parts.
            terms = [phrase, ko] if len(english) == len(unit['observable_components']) else [phrase]
            authored.append({
                'id': f'component_{i}', 'match_terms': distinct(terms),
                'evidence_field': f'component_{i}_phrase', 'evidence_terms': [phrase],
                'min_content_words': 3,
                'instruction': 'Preserve the selected depicted owner and complete relation: ' + phrase + '.',
                'render_gate': {'id': f'vo_{pid}_{i}', 'review_scale': 'both',
                    'description': phrase + '. Inspect the whole image and native detail. Every required part and its owner must be readable; partial evidence fails and occluded evidence is unobservable.'},
            })
        profile = {
            'id': pid, 'category': 'source_scoped_iconographic_relation',
            'activation': {'exact_terms': [exact_en],
                'requires_adult_character': False,
                'semantic_discovery_requires_component_evidence': True,
                'hard_activation': {'contract_version': 'photo-visual-hard-activation/v1',
                    'required_any_groups': [{'id': 'complete_selected_relation', 'any_terms': [exact_en]}]}},
            'semantics': {'definition': unit['description_en'] + ' Selected complete form: ' + exact_en + '.',
                'paraphrase_examples': distinct([text for text in alternatives if text != exact_en]
                    + DISCOVERY_JUNCTIONS.get(uid, [])),
                'visual_components': english,
                'contrast_examples': unit['confusion_boundaries'],
                'claim_limits': ['Scope to the explicitly selected represented form; a bare name does not require this complete variant.',
                    'Depicted iconography does not establish a real person religion, identity, consent, efficacy or hidden history.',
                    'Artifact documentation preserves the selected medium and original condition; reconstruction requires its own stated scope.']},
            'concept_candidate': {'concept_terms': distinct([unit['title'], *english, *DISCOVERY_PARAPHRASES[uid]]),
                'core_assertion_discovery': True,
                'affected_dimensions': ['composition'],
                'affected_properties': [{'dimension': 'composition', 'target': 'image_plane', 'property': 'layout'}]},
            'runtime_expression': {'default_mode': 'definition_with_optional_label',
                'prompt_label_terms': [], 'forbidden_prompt_terms': [], 'runtime_forbidden_labels': []},
            'authored_components': {'contract_version': 'photo-authored-visual-components/v1', 'components': authored},
            'reject_substitutes': unit['confusion_boundaries'],
        }
        profiles.append(compile_visual_profile(profile))
        # This candidate changes layout/legibility of already requested forms.
        # It does not add a deity, object, limb, act or new garment to the core.
        cid = pid + '_readable_composition'
        observation = 'Composition makes the already requested relation readable: ' + unit['description_en']
        entry = {
            'id': cid, 'ko': unit['title'] + '의 지정된 구성 요소와 소유 관계가 읽히는 구도',
            'en': observation, 'weight': 0.5,
            'tags': ['iconographic_layout', 'connected_visible_relation'],
            'paraphrases': distinct([*alternatives, 'Framing preserves the requested complete relation: ' + exact_en]),
            'keywords': english, 'embedding_text': ' '.join(alternatives),
            'concept_units': english,
            'relations': [{'id': f'{pid}_framing_owner', 'type': 'makes_readable',
                'subject': 'image_plane', 'object': exact_en}],
            'affected_dimensions': ['composition'],
            'affected_properties': [{'dimension': 'composition', 'target': 'image_plane', 'property': 'layout'}],
            'core_assertion_discovery': True,
            'requires_primary_any_tags': PRIMARY_CUES[uid].split(),
        }
        slot_entries.append(entry)
        bundles.append({
            'id': pid, 'primary_visual_proposition': 'Composition preserves the already requested complete form: ' + exact_en,
            'component_groups': english, 'candidate_ids': [cid],
            'hard_profile_id': pid, 'confusion_boundaries': unit['confusion_boundaries'],
            'source_keywords': alternatives,
            'relations': entry['relations'],
        })
        mappings.append({'research_unit_id': uid, 'profile_id': pid,
            'candidate_id': cid, 'source_ids': unit['source_ids'],
            'effect': 'image_plane.layout only; the requested core owns represented bodies, objects and events',
            'source_text_status': unit['evidence_level'], 'reference_pixel_review': 'NOT_PERFORMED'})
        mappings[-1]['primary_context_cues'] = PRIMARY_CUES[uid].split()

    for uid, english in ADVISORY_COMPONENTS.items():
        unit = seeds[uid]
        cid = 'ri_' + uid + '_readable_composition'
        alternatives = distinct([unit['title'], unit['description_en'], '; '.join(english),
            unit['title'] + ': ' + '; '.join(unit['observable_components'])])
        relation = {'id': 'ri_' + uid + '_framing_owner', 'type': 'makes_readable',
            'subject': 'image_plane', 'object': '; '.join(english)}
        slot_entries.append({'id': cid,
            'ko': unit['title'] + '의 이미 지정된 관계가 읽히는 구도',
            'en': 'Composition preserves the already requested source-scoped relation: ' + unit['description_en'],
            'weight': 0.5, 'tags': ['iconographic_layout', 'connected_visible_relation'],
            'paraphrases': alternatives, 'keywords': english, 'embedding_text': ' '.join(alternatives),
            'concept_units': english, 'relations': [relation],
            'affected_dimensions': ['composition'],
            'affected_properties': [{'dimension': 'composition', 'target': 'image_plane', 'property': 'layout'}],
            'core_assertion_discovery': True,
            'requires_primary_any_tags': PRIMARY_CUES[uid].split()})
        bundles.append({'id': 'ri_' + uid, 'candidate_only': True,
            'primary_visual_proposition': 'Keep the already selected relation readable: ' + '; '.join(english),
            'component_groups': english, 'candidate_ids': [cid], 'relations': [relation],
            'confusion_boundaries': unit['confusion_boundaries'], 'source_keywords': alternatives})
        mappings.append({'research_unit_id': uid, 'profile_id': None, 'candidate_id': cid,
            'source_ids': unit['source_ids'], 'activation': 'ADVISORY_LAYOUT_ONLY_NO_HARD_PROFILE',
            'effect': 'image_plane.layout only; no new object, anatomy, act or identity',
            'pending': unit['source_review_remaining'], 'source_text_status': unit['evidence_level'],
            'primary_context_cues': PRIMARY_CUES[uid].split()})

    # Existing canonical owners retain exact activation, required groups, and gates.
    original = read(HERE / 'input-snapshot/photo_prompt_visual_obligations.json')
    owner_updates = []
    for profile in original['profiles']:
        pid = profile['id']
        if pid not in OLD_ALTERNATIVES and pid != 'griffin_eagle_lion_topology':
            continue
        before = copy.deepcopy(profile)
        if pid in OLD_ALTERNATIVES:
            additions = list(OLD_ALTERNATIVES[pid])
        else:
            additions = ['독수리 머리와 날개·조류 앞부분이 사자의 몸통·뒷다리·꼬리로 이어지는 한 개체의 그리핀',
                'One griffin joins eagle head paired feathered wings and avian forequarters to the same lion torso hind legs paws and tail.']
        sem = profile['semantics']
        sem['paraphrase_examples'] = distinct(sem.get('paraphrase_examples', []) + additions)
        profile['concept_candidate']['concept_terms'] = distinct(profile['concept_candidate']['concept_terms'] + additions)
        # Full-component substitutions reuse the same English role and preserve
        # every existing invariant. They cannot become abbreviated noun proofs.
        assert len(OLD_COMPONENT_ALTERNATIVES[pid]) == len(sem['component_semantics']['groups'])
        fields = profile['required_evidence_fields']
        for index, group in enumerate(sem['component_semantics']['groups']):
            alternate = OLD_COMPONENT_ALTERNATIVES[pid][index]
            group['any_terms'] = distinct(group['any_terms'] + [alternate])
            proof = profile['evidence_requirements'][fields[index]]
            # These are full owned propositions, never shortened noun substitutes.
            if len(alternate.split()) < proof['min_content_words']:
                alternate += ' within the selected represented scene'
                group['any_terms'][-1] = alternate
            proof['must_mention_any'] = distinct(proof['must_mention_any'] + [alternate])
        assert profile['activation'] == before['activation']
        assert profile['render_gates'] == before['render_gates']
        assert sem['component_semantics']['required_group_ids'] == before['semantics']['component_semantics']['required_group_ids']
        owner_updates.append({'profile_id': pid, 'added_paraphrases': additions,
            'required_groups_preserved': True, 'exact_terms_preserved': True, 'pixel_gates_preserved': True})
    write(ASSETS / 'photo_prompt_visual_obligations.json', original)

    # The architecture owner already exists in its dedicated source extension.
    palace = read(HERE / 'input-snapshot/photo_prompt_visual_obligations_palace_fortification.json')
    muqarnas = next(p for p in palace['profiles'] if p['id'] == 'pf_muqarnas')
    muqarnas['semantics']['paraphrase_examples'] = distinct(muqarnas['semantics']['paraphrase_examples'] + [
        '작은 오목 셀이 층층이 겹치며 벽에서 천장으로 이어지는 입체 무카르나스',
        'Stacked recessed muqarnas cells retain real depth in a tiered wall-to-ceiling transition.'])
    muqarnas['concept_candidate']['concept_terms'] = distinct(muqarnas['concept_candidate']['concept_terms'] + [
        'tiered recessed cell volumes across the wall-to-ceiling junction'])
    owner_updates.append({'profile_id': 'pf_muqarnas', 'exact_terms_preserved': True,
        'required_groups_preserved': True, 'pixel_gates_preserved': True})
    write(ASSETS / 'photo_prompt_visual_obligations_palace_fortification.json', palace)

    contexts = {}
    myth = read(HERE / 'input-snapshot/photo_prompt_mythology_extension.json')
    for slot, entries in myth['slots'].items():
        for entry in entries:
            # Read the slot's own description; never copy an entire bundle's
            # mechanism into an individual aesthetic/action/prop candidate.
            contexts.setdefault(slot, {})[entry['id']] = {'paraphrases': distinct([
                entry['ko'] + '이 드러나는 선택된 신화 표현',
                'The requested scene retains ' + entry['en'].rstrip('.') + '.',
            ])}
    contexts.setdefault('subject', {})['griffin_eagle_lion_subject'] = {'paraphrases': [
        '갈고리 부리의 독수리 앞부분과 사자 뒷다리·꼬리가 같은 몸으로 이어진 그리핀',
        'one connected griffin with eagle head wings and avian forequarters transitioning into lion hindquarters']}
    contexts.setdefault('action', {})['griffin_turning_eagle_lion_profile'] = {'paraphrases': [
        '같은 그리핀의 독수리–사자 접합이 보이게 몸을 옆으로 돌리는 동작',
        'the same griffin turns so its eagle forebody and lion rear junction remain readable']}
    contexts.setdefault('location', {})['pf_muqarnas_location'] = {'paraphrases': [
        '층진 오목 셀의 깊이가 읽히는 벽–천장 사이 무카르나스 공간',
        'a muqarnas wall-to-ceiling space with stacked recessed cell volumes']}
    contexts.setdefault('composition', {})['pf_muqarnas_composition'] = {'paraphrases': [
        '인접 셀의 오목한 깊이를 분리해서 보여 주는 위쪽 사선 관찰 구도',
        'an upward oblique composition separates the depth of neighboring muqarnas cells']}

    maintenance = {
        'record_id': 'religion_myth_iconography_integration_20261003',
        'schema_version': 'religion-myth-authored-maintenance/v1',
        'maintenance_only': {'purpose': 'Source provenance, holds and authoring scope; not positive retrieval material.'},
        'source_research_path': str(RESEARCH.relative_to(ROOT)),
        'source_catalog_sha256': hashlib.sha256((RESEARCH / 'SOURCES.json').read_bytes()).hexdigest(),
        'mappings': mappings, 'existing_owner_updates': owner_updates,
        'existing_candidate_updates': {s: sorted(rows) for s, rows in contexts.items()},
        'holds': [{'unit_id': u['unit_id'], 'reason': 'No prop owner/dimension is defined; no relabeling as composition.'}
            for u in seeds.values() if u['slot_hint'] == 'prop'],
        'reused_research_units': {'griffin_eagle_lion': 'griffin_eagle_lion_topology',
            'muqarnas_cells': 'pf_muqarnas', 'heart_ani_roles': 'egyptian_heart_weighing_judgment'},
        'other_research_units': [{'unit_id': uid, 'status': 'RESEARCH_ONLY_NOT_INTEGRATED'}
            for uid in seeds if uid not in COMPONENTS and uid not in ADVISORY_COMPONENTS
            and uid not in {'griffin_eagle_lion', 'muqarnas_cells', 'heart_ani_roles'}],
        'limits': ['Text-based source authoring is not reference-pixel qualification.',
            'No source prose or bibliography is copied into positive retrieval fields.',
            'Generic labels remain advisory; exact complete-form duties require request evidence.',
            'New layout candidates cannot create bodies, limbs, events, props or wearer identity.'],
    }
    maintenance_path = HERE / 'MAINTENANCE.json'
    write(maintenance_path, maintenance)
    canonical_maintenance_path = HERE.parent / 'extension-maintenance' / (maintenance['record_id'] + '.json')
    write(canonical_maintenance_path, maintenance)
    maintenance_ref = {'contract_version': 'photo-extension-maintenance-ref/v1',
        'record_id': maintenance['record_id'], 'sha256': hashlib.sha256(json.dumps(
            maintenance, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()}
    write(ASSETS / 'photo_prompt_religion_iconography_extension.json', {
        'schema_version': 'photo-prompt-research-extension/v1', 'maintenance_ref': maintenance_ref,
        'slots': {'composition': slot_entries}, 'visual_semantics': bundles,
        'existing_slot_context_extensions': contexts,
    })
    write(ASSETS / 'photo_prompt_visual_obligations_religion_iconography.json', {
        'schema_version': 'photo-visual-obligation-registry-extension/v1',
        'relation_contract_version': 'photo-visual-relation/v1', 'profiles': profiles,
    })
    print(json.dumps({'new_profiles': len(profiles), 'new_candidates': len(slot_entries),
        'existing_profiles_enriched': len(owner_updates),
        'existing_candidates_enriched': sum(map(len, contexts.values())),
        'prop_holds': len(maintenance['holds'])}))


if __name__ == '__main__':
    main()
