"""Build research artifacts only. Never register or alter runtime assets."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PIN = "0adb5f6e56416e2656dfb4150d0724867530c2bc"


def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


SOURCES = []


def source(sid, title, url, kind, supports, limits, verification="page_text_read"):
    SOURCES.append(dict(id=sid, title=title, url=url, source_kind=kind,
                        checked_on_kst="2026-10-03", verification=verification,
                        supports=supports, limits=limits))


source("facs_official", "Paul Ekman Group: Facial Action Coding System", "https://www.paulekman.com/facial-action-coding-system/", "system_owner", "FACS describes visually discernible facial actions; action description and emotion inference are separate.", "The paid 2002 manual was not acquired; this research is not certified FACS coding.")
source("facs_cmu", "CMU facial expression laboratory: FACS reference", "https://www.cs.cmu.edu/~face/facs.htm", "research_lab_reference", "Names of the 22 AU identifiers in the source inventory.", "The page labels its reference as 1978; not a replacement for current manual criteria or intensity coding.")
source("openface", "OpenFace developer documentation: Action Units", "https://github.com/TadasBaltrusaitis/OpenFace/wiki/Action-Units", "developer_documentation", "Supported AU subset; presence/intensity differences; image and person-normalized sequence limitations.", "No software inference was run; a model score is not a sufficient render gate.")
source("barrett2019", "Barrett et al. 2019: Emotional Expressions Reconsidered", "https://pmc.ncbi.nlm.nih.gov/articles/PMC6640856/", "research_review", "Facial movements do not uniquely identify an emotion across people, situations and cultures.", "Does not supply a universal replacement emotion-to-face recipe.")
source("cowen2017", "Cowen and Keltner 2017: Self-report captures 27 categories of emotion bridged by continuous gradients", "https://doi.org/10.1073/pnas.1702247114", "research_paper", "Affective experience can contain many categories and continuous transitions.", "Self-report under the study protocol; not proof of 27 fixed faces or the reference's 32 families.", "search_abstract_read")
source("smile2021", "Martin et al. 2021: Evidence for Distinct Facial Signals of Reward, Affiliation, and Dominance from Both Perception and Production Tasks", "https://pmc.ncbi.nlm.nih.gov/articles/PMC8340880/", "research_paper", "Reward, affiliation and dominance functions; visible smile form, function and authenticity are distinct.", "A depicted configuration does not establish sincerity, disposition or consent.")
source("smile_dynamics", "Orlowska et al. 2018: Dynamics Matter: Recognition of Reward, Affiliative, and Dominance Smiles From Dynamic vs. Static Displays", "https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2018.00938/full", "research_paper", "Static and dynamic smile evidence are different experimental conditions; the observed dynamic advantage was significant for affiliative smiles.", "Study-specific recognition results do not validate a generated image.")
source("casme2", "Yan et al. 2014: CASME II", "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0086041", "dataset_paper", "Microexpression annotations involve temporal onset, apex and offset.", "Paper read only; no dataset download, license approval, training or lie-detection claim.")
source("body_context", "Aviezer et al. 2012: Body cues, not facial expressions, discriminate between intense positive and negative emotions", "https://pubmed.ncbi.nlm.nih.gov/23197536/", "research_paper", "Body and situation can affect interpretation of intense expressions.", "Controlled experiment; not a universal body-language decoder.", "abstract_read")
source("squinch", "Peter Hurley: Squinch", "https://peterhurley.com/blog/squinch-single-easiest-tip-looking-confident-photos", "originator_practice", "Portrait instruction emphasizes raising the lower eyelid, with a narrower visible eye opening.", "A posing practice, not a guaranteed confidence signal or certified AU equivalence.")
source("smize", "Collins: smize", "https://www.collinsdictionary.com/dictionary/english/smize", "lexicographic_primary", "Informal eye-focused smiling term.", "No uniquely specified muscle combination.")
for sid, word, support in [
    ("smirk", "smirk", "Self-satisfied or condescending smile; asymmetry is not a necessary definition."),
    ("coy", "coy", "Shyness, performed shyness or reluctance depends on context."),
    ("coquettish", "coquettish", "Flirtatious manner via the coquette sense; not fixed anatomy."),
    ("coquette", "coquette", "Flirtation as a social manner or action."),
    ("sultry", "sultry", "Weather, heated passion and attraction senses require disambiguation."),
    ("smolder", "smolder", "Literal burning and suppressed feeling senses; smoulder is a spelling variant."),
    ("leer", "leer", "An evaluative or lewd look is not interchangeable with mutual friendly flirtation."),
    ("ogle", "ogle", "Attentive appraisal may concern a person or a desired object; sense depends on context."),
    ("come_hither", "come-hither", "Invitation or attraction idiom; no mandatory eyelid formula."),
    ("side_eye", "side-eye", "Lateral looking with contextual evaluation; not always hostility."),
    ("deadpan", "deadpan", "Impassive or matter-of-fact manner; comic delivery can require sequence or speech."),
    ("double_take", "double%20take", "A reaction after delayed recognition; a temporal concept."),
    ("mug", "mug", "Camera-directed attention-seeking posing or faces; mug also has cup and robbery senses."),
    ("rizz", "rizz", "Romantic charm or charming action, rather than a facial configuration."),
    ("thirst_trap", "thirst%20trap", "Attention-seeking media function; no mandatory nudity or pose.")
]:
    source(sid, "Merriam-Webster: " + word.replace("%20", " "), "https://www.merriam-webster.com/dictionary/" + word, "lexicographic_primary", support, "Dictionary meaning only; the visual decomposition in this package is an authored proposal.")
source("korean_coy", "국립국어원 한국어기초사전: 새침하다", "https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=63384", "lexicographic_primary", "Korean definition includes a somewhat cold manner; coy translation does not establish sexual intent.", "One entry; not every colloquial use or character trope.")
source("aegyo", "국립국어원 한국어기초사전: 애교", "https://krdict.korean.go.kr/mon/dicSearch/SearchView?ParaWordNo=66380&nation=mon", "lexicographic_primary", "A manner intended to appear cute; not inherently sexual.", "Korean definition read on a multilingual page; no claim of a fixed facial recipe.")
source("o_face", "Wiktionary: o-face", "https://en.wiktionary.org/wiki/o-face", "collaborative_lexicography", "Explicit sexual reference category, distinct from general flirting or an open mouth.", "Lexical classification only; no explicit render recipe or candidate proposal.")
source("ahegao", "Wiktionary: ahegao", "https://en.wiktionary.org/wiki/ahegao", "collaborative_lexicography", "Explicit sexual media category, distinct from general adult appeal.", "Lexical classification only; no explicit render recipe or candidate proposal.")
source("rada_acting", "RADA: Focus on acting technique", "https://www.rada.ac.uk/about-us/blogs/focus-acting-technique-rada/", "training_institution", "Technique organizes action and scene work rather than one compulsory facial expression.", "No universal acting-method-to-AU mapping.")
source("rada_stanislavski", "RADA: Stanislavski workshop", "https://www.rada.ac.uk/short-courses/stanislavski-workshop/", "training_institution", "Given circumstances, objectives and action are useful scene-design concepts.", "Course description, not a complete manual or result verification.")
source("meisner", "Neighborhood Playhouse: Two-year conservatory", "https://www.neighborhoodplayhouse.org/two-year-conservatory", "training_institution", "Meisner-oriented training concerns responsive scene practice.", "Do not serialize an approach name as a fixed facial movement.")
source("strasberg", "Lee Strasberg Institute: What is Method Acting?", "https://strasberg.edu/about/what-is-method-acting/", "training_institution", "Method and memory-based actor preparation belong to method metadata.", "Not evidence of depicted internal memory or emotion.")
source("hagen", "HB Studio: The Uta approach", "https://www.hbstudio.org/hagen-institute/the-uta-approach/", "training_institution", "Actor preparation and circumstances can inform authored scene tasks.", "No method label should impose appearance or identity.")
source("adler", "Stella Adler Studio: Acting Technique 1", "https://stellaadler.com/workshops/acting-technique-1-foundation-online/", "training_institution", "Imagination and scene circumstances are preparation concepts.", "Training metadata, not a mandatory pose.")
source("chekhov", "Michael Chekhov Association", "https://www.michaelchekhov.org/", "training_institution", "Movement and imagination are aspects of the approach.", "Do not claim a standardized gesture-to-emotion conversion from the homepage.")
source("laban", "University of Maryland: Laban theory", "https://exhibitions.lib.umd.edu/bartenieff/laban-theory", "institutional_archive", "Effort axes include time, weight, space and flow.", "A still posture cannot demonstrate effort history or measured force.")
source("asha", "ASHA: Voice disorders practice portal", "https://www.asha.org/practice-portal/clinical-topics/voice-disorders/", "professional_body", "Pitch, loudness and voice quality are different acoustic descriptions.", "Vocabulary only; no diagnosis, audio test or inference from a face.")
source("sag", "SAG-AFTRA: Intimacy coordinator resources", "https://www.sagaftra.org/contracts-industry-resources/report-discrimination/intimacy-coordinator-resources", "professional_body", "Production choreography, boundaries and consent are distinct from portrayed attraction.", "No claim that facial expression establishes consent; no new product approval flow.")
write("SOURCES.json", {"schema_version": "acting-research-sources/v1", "sources": SOURCES,
    "method": "Primary system, paper, originator, training institution and dictionary pages were checked with web tools. Collaborative dictionaries are explicitly weaker lexical references. No article, image or dataset was downloaded for reuse.",
    "not_counted": ["Blocked Cambridge pages", "PMC CAPTCHA alternatives when publisher pages were used", "Unverified guessed LIMS pages", "ChatGPT reference as factual authority"]})


CONCEPTS = []


def concept(cid, ko, en, components, contrasts, sources, *, mode="static_form", reuse=None, slot="expression", profile=False, aliases=None, context=None):
    dimensions = ["pose"] if slot in {"hand_pose", "body_pose", "body_orientation"} else ["expression"]
    properties = [dict(dimension=dimensions[0], target="main_subject", property="hand.configuration" if slot == "hand_pose" else "face.expression")]
    row = dict(id="ae_" + cid, ko=ko, en=en, aliases=aliases or [ko, en],
               evidence_mode=mode, observable_components=components,
               confusion_boundaries=contrasts, source_ids=sources,
               source_vs_proposal="Sources support terminology or limitations; these exact visible components and alternatives are research authoring proposals.",
               candidate_slot=slot if mode in {"static_form", "context_variant"} else None,
               reuse_candidate_id=reuse, proposal_action="extend_existing_context" if reuse else ("new_candidate_draft" if mode in {"static_form", "context_variant"} else "metadata_only"),
               affected_dimensions=dimensions if mode in {"static_form", "context_variant"} else [],
               affected_properties=properties if mode in {"static_form", "context_variant"} else [],
               hard_profile_draft=profile,
               context_requirements=context or ["An explicitly requested human face or actor; preserve the frozen owner and crop."],
               activation_policy="Only explicit scoped form evidence or selected advisory data; an emotion/style label alone is not sufficient.",
               temporal_claims_allowed=False, hidden_state_claims_allowed=False,
               actor_binding="main_subject is a draft binding to be replaced by the exact frozen actor; never apply to every person.")
    CONCEPTS.append(row)


# Local form: reuse existing atoms before creating anything new.
concept("eyes_closed", "눈을 감은 상태", "both eyelids are closed", ["both eyelid openings are closed", "the two eyes belong to the declared actor"], ["a wink with only one eye closed", "sleep or serenity inferred without context"], ["facs_official"], reuse="pv_eyes_closed")
concept("half_lidded", "반쯤 내려온 눈꺼풀", "upper eyelids cover more of the iris while the eyes remain open", ["upper eyelids are lowered over part of the irises", "some eye opening remains visible"], ["eyes fully closed", "automatic sexual or sleepy meaning"], ["facs_official"], reuse="pv_half_lidded")
concept("closed_smile", "입을 다문 미소", "mouth corners rise while lips remain closed", ["mouth corners rise visibly", "the lip seam stays closed without exposed teeth"], ["lip pressing without raised corners", "a tooth-bearing smile"], ["smile2021"], reuse="pv_smile_closed")
concept("toothy_smile", "이를 보이는 미소", "raised mouth corners with visible teeth", ["mouth corners are raised", "teeth are visible between the lips"], ["closed-mouth smile", "a dropped jaw without a smile"], ["smile2021"], reuse="pv_smile_teeth")
concept("asymmetric_smile", "한쪽 입꼬리가 더 올라간 미소", "one mouth corner rises more than the other", ["the two mouth corners have different heights", "the declared side shows the greater lift"], ["all smirks treated as asymmetric", "unevenness caused only by head rotation"], ["smirk"], reuse="pv_asymmetric_mouth")
concept("parted_lips", "살짝 벌린 입술", "a small visible gap separates the lips", ["a narrow gap separates upper and lower lips", "the jaw does not visibly drop into a wide opening"], ["slack-jawed gape", "a mandatory sensual meaning"], ["facs_cmu"], reuse="pv_parted_lips")
concept("puffed_cheeks", "볼을 부풀린 상태", "rounded outward cheek contours while the lips stay closed", ["cheek contours are visibly rounded outward", "lips are closed"], ["ordinary facial fullness", "anger or childishness inferred from shape"], ["facs_official"], reuse="pv_puffed_cheeks")
concept("raised_brows", "양쪽 눈썹을 올린 상태", "both eyebrows are visibly raised", ["both eyebrow contours sit raised above the eyes", "laterality and eye opening remain independently specified"], ["only one eyebrow raised", "surprise imposed on the whole scene"], ["facs_cmu"], reuse="pv_raised_brows")
concept("wink", "한쪽 눈만 닫힌 윙크", "one eye is closed while the other remains open", ["only the requested eye is closed", "the opposite eye remains visibly open"], ["both eyes closed", "automatic flirtation"], ["facs_official"], reuse="pv_wink")
concept("lip_press", "입술을 꾹 누른 상태", "upper and lower lips press together along a closed seam", ["upper and lower lips meet along a fully closed seam", "the lip margins look compressed together"], ["lateral lip tightening alone", "puckered lips projecting forward"], ["facs_cmu"], profile=True, aliases=["입술 꾹 누르기", "입술을 꾹 누른", "lip pressing", "pressed lips"])
concept("lip_tighten", "입술을 가로로 팽팽하게 조인 상태", "lip margins look taut with reduced visible lip fullness", ["lip margins look taut and relatively thinned", "the mouth is not rounded into a protruding pucker"], ["simple vertical lip contact", "lip sucking or rolling inward"], ["facs_cmu"], profile=True, aliases=["입술 조이기", "입술을 가로로 팽팽하게", "lip tightening", "tightened lips"])
concept("purse", "입술을 좁게 오므린 상태", "lip opening narrows into a small rounded shape", ["the lip opening is narrowed and rounded", "the mouth corners move closer toward the center"], ["wide stretched lips", "a required kissing partner"], ["facs_cmu"], aliases=["오므린 입술", "pursed lips"])
concept("pucker", "앞으로 내민 키시 페이스", "rounded lips visibly project forward", ["the lips form a forward-projecting rounded contour", "the mouth corners gather toward the center"], ["mere lip pressing", "a kiss or consent inferred from lip shape"], ["facs_cmu"], aliases=["키시 페이스", "kissy face", "puckered lips"])
concept("mouth_down", "입꼬리가 내려간 상태", "both mouth corners angle downward", ["both mouth corners angle downward", "the central lip line remains distinct from the corner descent"], ["lip protrusion alone", "sadness or sulking automatically imposed"], ["facs_cmu"], profile=True, aliases=["입꼬리 내리기", "downturned mouth", "lowered mouth corners"])
concept("slack_jaw", "턱이 내려가 크게 벌어진 입", "the jaw lowers beneath a visibly open mouth", ["a visibly lowered jaw increases the mouth opening", "the opening is much larger than a narrow lip gap"], ["parted lips", "an implied shout with no audio"], ["facs_cmu"])
concept("lip_bite", "아랫입술을 가볍게 문 상태", "upper teeth gently contact the lower lip", ["upper teeth contact the lower lip", "the contact belongs to the actor's own mouth"], ["teeth clenched together", "a universal erotic meaning"], ["facs_official"], context=["Reuse the existing task-concentration lower-lip-bite candidate where appropriate; audit its exact ID before migration.", "Flirtation requires separately requested adult relational context."])
concept("lip_roll", "입술을 안쪽으로 말아 넣은 상태", "visible lip surfaces roll inward behind the mouth seam", ["visible lip surfaces are tucked inward", "the mouth seam remains closed"], ["lip pressing with lip surfaces still exposed", "tooth contact substituted"], ["facs_cmu"])
concept("set_jaw", "굳게 닫힌 턱선의 연기 형태", "the mouth is closed with a visibly held jaw contour", ["the mouth remains closed", "the actor holds a visibly firm jaw contour"], ["measured muscle force inferred", "anger or violence inferred"], ["facs_official"], context=["This is a stylized visible jaw configuration, not measured clenching force; verify relative to the same actor's relaxed baseline."])
concept("chin_up", "턱을 든 머리 방향", "the head tilts so the chin points upward", ["head orientation lifts the chin", "neck and chin retain the same actor connection"], ["AU17 chin raiser equated with head tilt", "camera height changed instead of head orientation"], ["facs_cmu"], slot="body_orientation")
concept("inner_brow", "눈썹 안쪽 끝이 올라간 상태", "inner eyebrow ends rise above their outer portions", ["the inner eyebrow ends are visibly lifted", "outer eyebrow ends are not required to rise equally"], ["both brows lifted uniformly", "sadness universally inferred"], ["facs_cmu"], profile=True, aliases=["눈썹 안쪽 끝을 올린", "inner brow raise", "raised inner brows"])
concept("knitted_brow", "미간 쪽으로 모이고 내려간 눈썹", "eyebrows draw inward and downward toward the glabella", ["eyebrow inner ends move toward the glabella", "the brow line visibly lowers toward the inner eye region"], ["a single eyebrow raised", "anger imposed on concentration"], ["facs_cmu"], profile=True, aliases=["미간 좁히기", "미간으로 모인 눈썹", "knitted brows", "brow lowering"])
concept("single_brow", "한쪽 눈썹만 올라간 상태", "one eyebrow rises above the opposite eyebrow", ["only the requested eyebrow is raised", "the opposite eyebrow retains a lower contour"], ["both brows raised", "head roll mistaken for brow asymmetry"], ["facs_cmu"], profile=True, aliases=["한쪽 눈썹 올리기", "한쪽 눈썹만 올린", "single-brow raise", "one raised eyebrow"])
concept("nose_wrinkle", "콧등이 찡그려진 상태", "the nose bridge region forms a visible wrinkle configuration", ["the nose bridge region is visibly scrunched", "the wrinkle follows the nose region rather than a cosmetic mark"], ["upper-lip lifting alone", "disgust inferred without context"], ["facs_cmu"], profile=True, aliases=["코 찡그리기", "코를 찡그린", "nose wrinkle", "wrinkled nose"])
concept("upper_lip", "윗입술 한가운데가 들린 상태", "the upper lip lifts toward the nose", ["the upper lip visibly lifts toward the nose", "the lift is distinct from an upward mouth-corner smile"], ["mouth-corner pulling alone", "a required contempt label"], ["facs_cmu"], profile=True, aliases=["윗입술 들기", "윗입술을 들어 올린", "upper-lip raise", "raised upper lip"])
concept("squinch", "아래 눈꺼풀을 가볍게 올린 스퀸치", "lower eyelids lift to narrow the visible eye openings", ["lower eyelid margins lift toward the irises", "both eyes remain visibly open through narrowed apertures"], ["full squint driven mainly by upper-lid closure", "a claimed confidence or sexual state"], ["squinch"], profile=True, aliases=["스퀸치", "squinch", "lifted lower eyelids"])
concept("smize", "눈 주변 움직임이 있는 미소 제안", "a smile with visible cheek lift and softened eye openings", ["mouth corners rise", "cheeks lift and the eye openings narrow without full closure"], ["one mandatory definition of smize", "genuineness inferred from eye crinkles"], ["smize", "smile2021"], context=["One permitted visual realization of the broad eye-smiling term; alternatives remain selectable."])
concept("duchenne_shape", "눈 주변과 입꼬리가 함께 움직인 미소 형태", "cheek raising accompanies mouth-corner pulling", ["mouth corners pull upward", "the cheek and outer-eye region shows accompanying compression"], ["a guarantee of sincerity", "age-related wrinkles alone treated as expression"], ["facs_cmu", "smile2021"], aliases=["뒤셴 미소 형태", "Duchenne-like smile configuration"])
concept("tears", "눈물 고임", "tear fluid is visibly pooled along the lower eyelid margins", ["tear fluid pools along lower eyelid margins", "eyes and tear margins belong to the same declared actor"], ["eye shine from lighting alone", "grief or relief inferred from moisture"], ["barrett2019"])
concept("held_tears_lips", "눈물을 고인 채 입술을 꾹 다문 형태", "pooled tears accompany a closed compressed lip seam", ["tear fluid is pooled along the lower eyelid margins", "upper and lower lips press together along a closed seam"], ["all tear suppression forced into this pose", "sobbing inferred from a still image"], ["barrett2019", "facs_cmu"], profile=True, aliases=["눈물이 고인 채 입술을 꾹 다문", "pooled tears with pressed lips"], context=["The request must specify both visible forms; generic 눈물 참기 alone remains a contextual candidate."])
concept("hand_mouth", "자기 입 앞을 자기 손으로 가린 형태", "the actor's own hand covers the front of their own mouth", ["the actor's hand is connected to their own wrist and arm", "that hand covers the front of the same actor's mouth"], ["another actor's hand over the mouth", "a hand at the cheek without mouth coverage", "automatic surprise or coercion"], ["body_context"], slot="hand_pose", profile=True, aliases=["자기 손으로 입을 가린", "own hand covering own mouth"], context=["입틀막 is a colloquial lookup term; the actual ownership/contact phrase controls activation."])
concept("lateral_look", "고개 방향과 구별되는 곁눈질", "irises are directed laterally relative to the face orientation", ["visible irises turn toward the declared side", "the eyeline is distinguishable from the head orientation"], ["head turned with centered irises", "scorn inferred from any lateral look"], ["side_eye"], slot="gaze_engagement", reuse="pv_side_eye")
concept("downcast", "아래를 향한 시선", "irises point below the actor's horizontal eyeline", ["the irises point toward the declared lower target", "head tilt is independently specified"], ["head bowed but eyes looking up", "shyness inferred without scene context"], ["facs_official"], slot="gaze_engagement")
concept("single_frame_eye_roll", "위로 치우친 시선의 한 프레임", "irises are directed upward in the selected frame", ["irises point upward in the selected frame", "head orientation is separately preserved"], ["the completed rolling motion claimed from one frame", "disdain imposed on a simple upward look"], ["facs_official"], slot="gaze_engagement")

# Context-bound variants are options, never fixed equations for feelings.
concept("polite_smile", "예의상 작은 미소의 선택형", "a small closed-mouth smile in an explicitly polite encounter", ["a small closed-mouth smile is visible", "the requested social encounter remains unchanged"], ["dishonesty or fake emotion inferred", "service occupation invented"], ["smile2021"], mode="context_variant", context=["The request identifies politeness or a social display task; no hidden sincerity classification."])
concept("smirk_context", "의기양양한 미소의 선택형", "a restrained smile in an explicitly self-satisfied performance context", ["a restrained mouth-corner lift is visible", "the self-satisfied portrayal comes from the user's context"], ["all one-sided smiles treated as smirks", "playfulness replaced by hostility"], ["smirk"], mode="context_variant", reuse="playful_smirk", context=["Existing playful_smirk may be reused only in a playful portrayal; smug/condescending senses need separate scoped variants."])
concept("sneer_variant", "경멸 연기를 위한 윗입술 들림 선택형", "a raised upper lip in an explicitly contemptuous portrayal", ["the upper lip lifts", "the user's contempt portrayal is preserved as scene context"], ["smirk without upper-lip motion", "every sneer forced into one muscle pattern"], ["barrett2019", "facs_cmu"], mode="context_variant")
concept("wry_variant", "곤란한 상황에서 한쪽 미소의 선택형", "an uneven small smile within an explicitly ironic or difficult situation", ["a small asymmetric mouth-corner lift is visible", "the difficult or ironic situation is already requested"], ["any asymmetry treated as regret", "a new failure event invented"], ["barrett2019"], mode="context_variant")
concept("bashful_direct", "수줍지만 시선을 유지하는 선택형", "a small smile while maintaining the requested eyeline", ["a small smile is visible", "the requested direct eyeline is retained"], ["all shyness automatically looks down", "eyeline lock overwritten"], ["barrett2019"], mode="context_variant", context=["Shyness is explicitly requested; direct gaze can coexist with it. A gaze change requires its own expression property declaration."])
concept("coy_variant", "머리를 약간 돌리면서 시선은 유지하는 선택형", "a slight head turn with an independently retained target-directed eyeline", ["the head turns slightly away", "the irises retain the declared target direction"], ["sexual intent inferred from 새침", "all coyness reduced to gaze avoidance"], ["coy", "korean_coy"], mode="context_variant", slot="body_orientation", context=["Only select when this exact head/eye realization is requested or accepted; it changes pose and expression, so both effects must be declared before runtime adoption."])
concept("coquettish_variant", "장난스러운 성인 교류의 윙크 선택형", "a wink and small smile in explicitly requested adult playful flirtation", ["one eye is closed and the other stays open", "a small smile remains visible"], ["nonsexual wink given erotic tone", "partner response or consent inferred"], ["coquettish", "sag"], mode="context_variant", context=["Explicit adult flirtation context is required; no added partner, contact, wardrobe or body shape."])
concept("sultry_variant", "차분한 성인 호감 표현의 선택형", "an adult subject retains a target-directed gaze with lowered upper eyelids", ["upper eyelids are partly lowered", "the requested target-directed eyeline is retained"], ["hot weather sultry treated as attraction", "drowsiness sexualized", "mandatory parted lips or body shape"], ["sultry", "barrett2019"], mode="context_variant", context=["An explicitly requested adult attraction portrayal selects this option; sultry alone must first be sense-disambiguated."])
concept("smolder_anger", "억눌린 분노 연기의 선택형", "an unchanged intense eyeline with a compressed lip seam in an explicitly restrained-anger portrayal", ["the requested intense eyeline is retained", "the lips press together"], ["smoldering embers treated as a face", "sexual tone added to restrained anger"], ["smolder", "barrett2019"], mode="context_variant", context=["Existing restrained surface axes can describe the authored portrayal; hidden real anger cannot be inferred."])
concept("smolder_attraction", "성인 호감 연기의 집중 시선 선택형", "a sustained-looking target-directed gaze in an explicitly adult attraction portrayal", ["the irises align with the already requested target", "the eye opening retains the requested form"], ["actual gaze duration claimed from a still", "restrained anger forced into adult attraction"], ["smolder", "sag"], mode="context_variant", context=["Adult attraction must be explicit; duration remains unverified from the still."])
concept("deadpan_form", "변화가 적은 입과 눈썹의 데드팬 선택형", "level mouth corners and comparatively unaccented brows in a deadpan portrayal", ["mouth corners remain level", "brows retain a comparatively unaccented contour"], ["clinical flat affect diagnosis", "comic timing claimed without sequence"], ["deadpan"], mode="context_variant", context=["One selectable deadpan configuration; existing deadpan_kindness is only reusable when kindness is already in the scene."])
concept("restrained_anger", "작게 드러나는 억눌린 분노의 선택형", "a compressed lip seam with a small inward brow draw", ["the lips press together", "the inner brows draw slightly inward"], ["full shout substituted", "violence or an opponent invented"], ["barrett2019", "facs_cmu"], mode="context_variant")
concept("smile_tears", "눈물 고임과 작은 미소가 공존하는 형태", "pooled tears coexist with a small raised mouth-corner smile", ["tear fluid is pooled at the eyelid margins", "mouth corners form a small smile"], ["every crying smile called relief", "sad eyes used without visible evidence"], ["barrett2019", "smile2021"], mode="context_variant")
concept("service_smile", "요청된 응대 장면의 작은 미소", "a small closed-mouth smile within the already requested service encounter", ["a small closed-mouth smile is visible", "the existing scene's service role and addressee are preserved"], ["service occupation invented", "insincerity judged from eye wrinkles"], ["smile2021"], mode="context_variant", context=["Do not reuse affiliative_reassurance_smile unless reassurance is part of the frozen scene."])
concept("mouth_cover_idiom", "입틀막의 손 소유권 명시형", "the actor covers their own mouth with their own hand", ["the hand belongs to the same actor", "the hand overlaps the front of that actor's mouth"], ["another person's hand", "mouth widened without hand coverage"], ["body_context"], mode="context_variant", slot="hand_pose", context=["Idiomatic 입틀막 can suggest this option; manual selection must preserve any locked hand action or prop."])
concept("mugging_variant", "카메라를 향한 과장 표정의 선택형", "exaggerated raised eyebrows and a wide smile directed toward the requested camera", ["eyebrows are conspicuously raised", "a wide smile is directed toward the requested camera"], ["a cup or robbery sense", "every mugging example forced into this exact form"], ["mug"], mode="context_variant", context=["The camera-directed comic performance sense must be explicit; don't redirect a locked off-camera gaze."])

# Temporal/audio/evaluative terms are deliberately not static candidate rows.
for cid, ko, en, mode, src, limit in [
    ("microexpression", "순간적인 미세표정", "brief microexpression sequence", "sequence_only", ["casme2"], "Requires ordered frames and duration; robot micro_precise_microexpression has a different existing meaning."),
    ("double_take", "더블 테이크", "delayed recognition and renewed reaction", "sequence_only", ["double_take"], "Initial notice, delay and second response require an ordered sequence."),
    ("returning_glance", "시선을 피했다 되돌리기", "averted gaze followed by a returning glance", "sequence_only", ["facs_official"], "One frame only verifies its selected eyeline, not the return."),
    ("eye_roll", "눈 굴리기", "an eye-rolling movement", "sequence_only", ["facs_official"], "Do not equate one upward gaze with the complete movement."),
    ("trembling_lips", "입술 떨림", "lip trembling over time", "sequence_only", ["casme2"], "A contour in one still does not prove oscillation."),
    ("dynamics", "시작·정점·해소·지연", "onset, apex, offset and latency", "sequence_only", ["casme2", "smile_dynamics"], "Record timestamps and a nominated reference event; do not invent durations."),
    ("voice", "목소리·말투", "pitch, loudness, voice quality and delivery", "audio_only", ["asha"], "Requires actual audio; do not use an open mouth as a voice-quality pass."),
    ("tactics", "상대에게 하려는 행동", "objective-directed interpersonal tactics", "scene_metadata", ["rada_acting"], "Targets and observable attempts are separate from proof that the recipient was persuaded."),
    ("methods", "연기 훈련 접근법", "actor-training approaches", "method_metadata", ["rada_stanislavski", "meisner", "strasberg", "hagen", "adler", "chekhov"], "Method labels do not activate fixed face geometry."),
    ("laban_effort", "라반 노력 요소", "time, weight, space and flow effort axes", "sequence_only", ["laban"], "Still body configuration does not prove speed, force or continuity."),
    ("rizz", "리즈", "romantic charm as a scene or media function", "scene_metadata", ["rizz"], "No compulsory grin, body type or flirting success."),
    ("thirst_trap", "서스트 트랩", "attention-seeking media function", "scene_metadata", ["thirst_trap"], "No automatic clothing, nudity, body shape or actual audience response."),
    ("aegyo", "애교", "a cute social manner", "scene_metadata", ["aegyo"], "Nonsexual uses remain nonsexual; facial variant is selected separately."),
    ("explicit_terms", "O-face·아헤가오", "explicit sexual reference categories", "lexical_only", ["o_face", "ahegao"], "Lexical research only; no render components or explicit candidate expansion."),
    ("style", "연기 질과 스타일", "naturalistic, stylized, restrained and evaluative performance labels", "evaluation_metadata", ["rada_acting"], "Operationalize visible amplitude separately; emotional truth, range and chemistry require contextual human assessment.")
]:
    concept(cid, ko, en, [], [limit], src, mode=mode)

# Fix effects for rows that span pose and eyeline; the default slot policy alone is insufficient.
for row in CONCEPTS:
    if row["id"] == "ae_coy_variant":
        row["affected_dimensions"] = ["pose", "expression"]
        row["affected_properties"] = [dict(dimension="pose", target="main_subject", property="head.orientation"), dict(dimension="expression", target="main_subject", property="eyes.eyeline")]
    elif row["id"] == "ae_chin_up":
        row["affected_properties"] = [dict(dimension="pose", target="main_subject", property="head.orientation")]
    elif row["id"] in {"ae_lateral_look", "ae_downcast", "ae_single_frame_eye_roll", "ae_bashful_direct", "ae_sultry_variant", "ae_smolder_anger", "ae_smolder_attraction", "ae_mugging_variant"}:
        row["affected_properties"].append(dict(dimension="expression", target="main_subject", property="eyes.eyeline"))
    if row["id"] == "ae_lip_bite":
        row["context_requirements"][0] = "Existing expression.ctx_c126 is the verified task-concentration lower-lip-bite candidate; use it for that context without widening its action/expression effects. A generic local-form variant is a separate proposal."
        row["related_existing_candidate"] = dict(slot="expression", id="ctx_c126", source="photo_prompt_contextual_appeal_extension.json", reuse_condition="Only the existing task-concentration context.")

write("PROPOSED-DATA.json", dict(schema_version="acting-expression-research-proposals/v1", status="research_draft_not_registered", source_commit=PIN, concepts=CONCEPTS,
    authoring_constraints=["The broad affect or style word alone cannot hard-activate one facial recipe.", "No proposal changes identity, actor count, clothing, sexual tone or consent.", "Static frames are not duration, audio, mental state or success evidence.", "All source-supported terms, authored options and runtime verification remain separate."],
    unresolved=["Contextual variants require native Korean/English review.", "Latest source assets must be re-audited after the concurrent merge.", "Render gates have not been image-tested."]))

profiles, candidates, bundles, reuse = [], {}, [], []
for row in CONCEPTS:
    slot = row["candidate_slot"]
    if slot is None:
        continue
    if row["reuse_candidate_id"]:
        reuse.append(dict(concept_id=row["id"], slot=slot, existing_candidate_id=row["reuse_candidate_id"], allowed_action="Add narrow context/paraphrase only after checking current meaning; don't overwrite guards or effects."))
        continue
    candidates.setdefault(slot, []).append(dict(id=row["id"], ko=row["ko"], en="; ".join(row["observable_components"]), weight=0.5,
        tags=["human", "acting_expression_research", slot], for_any=["human"],
        aliases=row["aliases"], keywords=row["aliases"],
        embedding_text="; ".join([row["ko"], *row["observable_components"]]),
        concept_units=row["observable_components"],
        relations=[dict(id="actor_owner", type="declared_owner_scope", subject="main_subject", object="the explicitly specified face, eyelids, mouth and contact configuration")],
        affected_dimensions=row["affected_dimensions"], affected_properties=row["affected_properties"], core_assertion_discovery=True))
    if not row["hard_profile_draft"]:
        continue
    pid = "ae_profile_" + row["id"][3:]
    profile = dict(id=pid, category="observable_facial_or_hand_configuration", activation=dict(exact_terms=row["aliases"], requires_adult_character=False,
        semantic_discovery_requires_component_evidence=True,
        hard_activation=dict(contract_version="photo-visual-hard-activation/v1", required_any_groups=[dict(id="actor_face_context", any_terms=["face", "facial", "portrait", "actor", "person", "human", "woman", "man", "얼굴", "표정", "인물", "사람", "배우", "초상"])])),
        semantics=dict(definition="; ".join(row["observable_components"]), paraphrase_examples=[row["en"]], visual_components=row["observable_components"], contrast_examples=row["confusion_boundaries"],
                       claim_limits=["Bind all parts and laterality to the frozen actor; no inferred real emotion, trait or consent.", "Retain the frozen crop and eyeline; a hidden prerequisite is unobservable, not a pass.", "Every required component must pass; partial evidence is a failure."]),
        concept_candidate=dict(concept_terms=[row["ko"], row["en"], *row["observable_components"]], core_assertion_discovery=True, affected_dimensions=row["affected_dimensions"], affected_properties=row["affected_properties"]),
        runtime_expression=dict(default_mode="definition_with_optional_label", prompt_label_terms=[], forbidden_prompt_terms=[], runtime_forbidden_labels=[]), reject_substitutes=row["confusion_boundaries"],
        authored_components=dict(contract_version="photo-authored-visual-components/v1", components=[]))
    for n, visible in enumerate(row["observable_components"], 1):
        profile["authored_components"]["components"].append(dict(id=f"component_{n}", match_terms=[visible], evidence_field=f"component_{n}_phrase", evidence_terms=[visible], min_content_words=3,
            instruction=f"Preserve the declared actor and show this facial or contact relation clearly: {visible}.",
            render_gate=dict(id=f"vo_{pid}_{n}", review_scale="native", description=f"Inspect the declared actor's original pixels for this complete relation: {visible}. Partial evidence fails; occlusion is unobservable.")))
    profiles.append(profile)
    bundles.append(dict(id="ae_bundle_" + row["id"][3:], candidate_only=True, primary_visual_proposition="; ".join(row["observable_components"]), candidate_ids=[row["id"]], candidate_slots={row["id"]: slot}, hard_profile_ids=[pid],
        component_groups=[dict(id=f"component_{n}", visible_evidence=[s]) for n,s in enumerate(row["observable_components"],1)], source_keywords=row["aliases"], confusion_boundaries=row["confusion_boundaries"],
        relations=[dict(id="actor_owner", type="declared_owner_scope", subject="main_subject", object="the explicitly stated face and contact configuration")]))

write("DRAFT-VISUAL-PROFILES.json", dict(schema_version="photo-visual-obligation-registry-extension/v1", relation_contract_version="photo-visual-relation/v1", profiles=profiles))
# These drafts use recognized schema keys, but are not approved for runtime merge.
# Context requirements remain in the research envelope: migrate them to actual supported guards before adoption.
write("DRAFT-CANDIDATE-EXTENSION.json", dict(schema_version="photo-prompt-research-extension/v1", slots=candidates, visual_semantics=bundles,
    maintenance_ref=dict(contract_version="photo-extension-maintenance-ref/v1", record_id="acting-expression-semantics-20261003", sha256=hashlib.sha256((HERE / "PROPOSED-DATA.json").read_bytes()).hexdigest())))
write("REUSE-PLAN.json", dict(schema_version="acting-research-reuse/v1", reuse=reuse,
    warning="Draft contextual candidates must acquire supported, tested guards. Similar meaning or lexical coverage does not establish runtime eligibility."))


INVENTORY = json.loads((HERE / "SOURCE-TERM-GROUPS.json").read_text())
routes = {
    0: ("contextual_portrayal", "P2", "32 affect families stay as scene meaning; select form variants, never fixed face equations."),
    1: ("gaze_form_or_sequence", "P1/P4", "Retain actor-relative target and head/iris distinction; scanning, return and latency need ordered frames."),
    2: ("eye_brow_form_or_impression", "P1/P2", "Local eyelid/brow motion is separate from soft, hard, pleading or wistful impressions."),
    3: ("smile_form_function_or_sequence", "P1/P2/P4", "Closed/toothy/asymmetric forms reuse atoms; social function uses context; spread/fade need time."),
    4: ("mouth_form_or_sequence", "P1/P4", "Press, tighten, pucker, jaw opening and head tilt are distinct; tremor needs sequence."),
    5: ("crying_form_audio_or_sequence", "P2/P4", "Separate wetness, tear tracks, hand wiping, sound and regulation history."),
    6: ("facs_metadata", "P1", "Action name cross-reference only; no automatic emotion, intensity or complete coding certification."),
    7: ("facs_metadata", "P1", "Keep action names apart; head chin-up is not AU17 and parted lips is not jaw drop."),
    8: ("regulation_or_temporal_metadata", "P2/P4", "Amplitude/symmetry can be still forms; onset/apex/offset/latency require sequence; leakage is an authored portrayal."),
    9: ("compound_portrayal", "P2", "Independent visible surface and context components, with actor ownership and no hidden-state diagnosis."),
    10: ("body_form_or_sequence", "P2/P4", "Reuse pose/contact configurations; approach, pace, mirroring and effort transitions need time."),
    11: ("audio_metadata", "P4", "All 22 voice descriptors require audio; no substitute facial test."),
    12: ("audio_or_visible_proxy", "P4", "Nonverbal sounds remain audio; a requested visible mouth/hand form is a separate assertion."),
    13: ("contextual_social_manner", "P2", "Adult flirtation, ordinary cuteness, reserve and teasing are different senses; no preset sexual tone."),
    14: ("adult_impression_or_polysemy", "P2", "Disambiguate literal weather/fire and relational portrayal; no compulsory anatomy or wardrobe."),
    15: ("idiom_form_or_sequence", "P2/P4", "Local lips/wink can reuse atoms; invitation and attraction need context; returning gaze needs sequence."),
    16: ("evaluative_appraisal", "P2", "Portrayed appraisal is not a diagnosis, real desire or consent inference; no fixed anatomy."),
    17: ("media_function_or_lexical_only", "P2", "Rizz/thirst trap are functions; O-face/ahegao remain lexical-only with no explicit render expansion."),
    18: ("relational_tactics", "P2", "Bind actor, recipient, attempted action and requested context; do not invent success, partner or contact."),
    19: ("scene_design_metadata", "P2/P4", "Objective/subtext are authoring metadata; eyeline/blocking need concrete relations; continuity needs sequence."),
    20: ("training_method_metadata", "P4", "Keep all eight methods as provenance/preparation, not facial synonyms."),
    21: ("comic_form_function_or_sequence", "P3/P4", "Deadpan/mugging may have selected still forms; double take/corpsing/slow burn require sequence."),
    22: ("korean_contextual_idiom", "P3", "Translate by whole request and concrete components; 동공지진 is not literally pupil vibration."),
    23: ("style_or_human_evaluation", "P3/P4", "Define selectable amplitude; quality, range, presence and chemistry stay human contextual judgments."),
    24: ("compound_scene", "P2/P4", "Preserve existing scene event; separate same-frame coexistence from event order, timing and unrequested characters.")
}
decisions = []
for table in INVENTORY["tables"]:
    route, phase, rule = routes[table["table_index"]]
    for n, term in enumerate(table["term_rows"], 1):
        decisions.append(dict(source_row_id=f"t{table['table_index']:02d}_r{n:02d}", table_index=table["table_index"], section=table["section"], term_group=term,
            route=route, phase=phase, authoring_rule=rule, evidence_status="routing_decision_not_individual_term_validation"))
write("TERM-DECISIONS.json", dict(schema_version="acting-research-term-decisions/v1", rows=decisions,
    additional_prose_terms=INVENTORY["additional_prose_terms"], limit="Every source row is routed, but routing is not a verified dictionary definition or runtime behavior for every comma-separated term."))


CASES = []


def case(cid, text, expected, excluded, layer="meaning", *, language="ko", refs=None):
    CASES.append(dict(id=cid, language=language, request=text, expected=expected, forbidden_outcomes=excluded,
                      assertion_layer=layer, related_concept_ids=refs or [], observed_status="not_run", pass_policy="All expected conditions must hold; no unrequested actor, pose, tone or relation may be added."))


for row in CONCEPTS:
    if not row["hard_profile_draft"]:
        continue
    case(row["id"]+"_ko", "한 명의 성인 배우의 얼굴 클로즈업. " + row["ko"] + ".", row["observable_components"], row["confusion_boundaries"], refs=[row["id"]])
    case(row["id"]+"_en", "Close-up of one adult actor. " + row["en"] + ".", row["observable_components"], row["confusion_boundaries"], language="en", refs=[row["id"]])
    case(row["id"]+"_negated", "한 명의 성인 배우의 얼굴. " + row["ko"] + "는 원하지 않는다. 편안한 입과 눈썹.", ["Do not hard-activate the negated form."], ["Any required obligation from the negated form."], layer="activation", refs=[row["id"]])

for args in [
    ("sultry_weather", "A sultry afternoon; the adult actor has a neutral expression.", ["Weather sense; retain neutral expression."], ["Seductive eyelids or lips."]),
    ("sultry_adult", "An adult actor portrays sultry attraction, keeping lips closed and gaze off-camera.", ["Adult portrayal; closed lips and off-camera gaze are locked."], ["Mandatory parted lips or camera gaze."]),
    ("smolder_fire", "Smoldering embers behind a neutrally posed adult actor.", ["Literal embers; preserve actor expression."], ["Attraction or anger face activation."]),
    ("smolder_anger", "The adult actor portrays smoldering anger with pressed lips.", ["Restrained anger context and lip pressing."], ["Sexual tone."]),
    ("smirk_symmetry", "A smug smile, with both mouth corners equally lifted.", ["Self-satisfied portrayal can retain symmetry."], ["Mandatory asymmetric mouth."]),
    ("smize_optional", "An adult actor smizes while the mouth remains neutral.", ["Eye-focused smile option; preserve neutral mouth lock."], ["Forced teeth or mouth-corner smile."]),
    ("lip_bite_task", "An adult carefully mends a jacket, lightly biting their lower lip in concentration.", ["Own teeth/lower-lip contact in task context."], ["Erotic context or clothing removal."]),
    ("lip_bite_flirt", "Two adults in a requested playful flirting scene; the first lightly bites their lower lip.", ["Bite binds only to the first actor; requested adult context retained."], ["Consent inference, new touch or shared facial expression."]),
    ("wink_nonsexual", "A magician gives the audience a playful wink after a trick.", ["One closed eye; nonsexual playfulness."], ["Seductive clothing or relationship."]),
    ("aegyo_plain", "성인 출연자가 예능 상황에서 애교 있는 인사를 한다. 성적 분위기는 없다.", ["Cute social manner; no sexual tone."], ["Adult attraction automatically activated."]),
    ("saechim_reserve", "성인 인물이 기자의 질문에 새침하고 차갑게 반응한다.", ["Reserved/cold portrayal."], ["Coquettish attraction automatically activated."]),
    ("gaze_owner", "두 성인 중 왼쪽 배우만 오른쪽 배우를 곁눈질한다.", ["Left actor owns lateral eyeline; right actor is target."], ["Both actors share the gaze or target is reversed."]),
    ("gaze_head", "고개는 오른쪽으로 돌렸지만 눈은 카메라를 향한다.", ["Head orientation and iris target are distinct."], ["Head turn substituted for iris direction."]),
    ("shy_direct", "수줍지만 상대를 똑바로 바라보는 성인 배우.", ["Shy portrayal retains direct eyeline."], ["Automatic downcast gaze."]),
    ("hand_owner", "오른쪽 배우가 자기 손으로 자기 입을 가린다. 왼쪽 배우는 책을 든다.", ["Right actor's own hand/mouth; left actor retains book."], ["Hand ownership reversal or lost book."]),
    ("crop_unobservable", "눈만 보이는 크롭을 유지하면서 입술을 꾹 누른 표정을 묘사한다.", ["Preserve crop; lip pixel evidence is UNOBSERVABLE."], ["Widened crop or PASS on hidden mouth."]),
    ("teeth_hidden", "입 전체를 가린 마스크를 쓴 성인의 입을 다문 미소.", ["Keep mask; lip/teeth gate is UNOBSERVABLE."], ["Mask removed to pass or teeth gate marked PASS."]),
    ("eye_roll_static", "눈 굴리기의 한 프레임, 시선은 위쪽에 있다.", ["Only the selected upward eyeline is observable."], ["Completed rolling motion claimed."]),
    ("double_take_static", "더블 테이크의 두 번째 반응을 보여주는 정지 사진.", ["Verify requested second-reaction form only; timing unverified."], ["Reaction latency scored as PASS."]),
    ("micro_robot", "A robot's overly precise micro-expression feels programmed and symmetrical.", ["Preserve the existing robot/uncanny meaning."], ["Biological microexpression timing inferred."]),
    ("micro_human", "A short video of an adult's brief microexpression with onset, apex and offset timestamps.", ["Sequence metadata, no robot substitution."], ["Lie, sincerity or hidden intention diagnosis."]),
    ("voice_static", "숨 섞인 목소리로 말하는 성인의 정지 사진.", ["Voice claim requires audio; requested visible pose can be separate."], ["Breathy voice PASS from parted lips."]),
    ("tears_no_cause", "눈물이 고인 성인 얼굴. 원인은 설명하지 않는다.", ["Tear pool only."], ["Bereavement, breakup, relief or shame invented."]),
    ("sincerity", "뒤셴 미소 형태로 연기하는 배우.", ["Cheek/eye and mouth-corner configuration only."], ["Real happiness or honesty certified."]),
    ("neutral_direct", "무표정으로 카메라를 똑바로 바라보는 배우.", ["Neutral surface and direct gaze can coexist."], ["Deadpan_kindness or hostile character invented."]),
    ("glare_light", "강한 빛 때문에 눈을 가늘게 뜬다. 화난 표정은 아니다.", ["Light-related squint; no anger."], ["Glare or hostile emotion."]),
    ("chin_au", "턱을 위로 든 머리 방향. 입술과 턱 피부는 편안하다.", ["Head orientation only."], ["AU17 lower-lip/chin action imposed."]),
    ("ogle_object", "The adult actor ogles an elaborate dessert display.", ["Desired-object appraisal; preserve dessert target."], ["Sexual partner or body gaze invented."]),
    ("mug_cup", "A coffee mug beside an adult actor with a neutral face.", ["Cup sense; retain neutral face."], ["Mugging performance activation."]),
    ("rizz_guard", "자연스러운 대화로 리즈를 보여주는 성인. 몸매·복장·표정은 그대로.", ["Scene/media function remains optional; locked appearance preserved."], ["Mandatory grin, body type or successful attraction."]),
    ("thirst_function", "성인 출연자의 서스트 트랩 콘셉트 사진. 겨울 코트와 중립 표정 유지.", ["Media function with winter coat and neutral face retained."], ["Nudity, lips or body shape automatically changed."]),
    ("explicit_classification", "O-face와 아헤가오가 플러팅 용어와 어떻게 다른지 설명한다.", ["Lexical distinction only."], ["Explicit render recipe or candidate generation."]),
    ("emotion_freeze", "기쁨을 표현하되 입은 다물고 미소도 없다.", ["Joy portrayal does not override explicit mouth constraints."], ["Smiling treated as compulsory joy shape."]),
    ("emotion_cause", "상실감이 있는 배우의 초상. 인물은 한 명뿐이고 배경은 빈 벽.", ["Preserve one actor and empty wall; selectable expression only."], ["Funeral props, missing partner or death event invented."]),
    ("tactic_attempt", "상대를 설득하려고 손바닥을 펼쳐 말하는 성인 배우.", ["Requested attempt and open-hand form; recipient response unspecified."], ["Recipient agreement or extra person inferred."]),
    ("method_only", "마이즈너 접근으로 연기한 장면. 표정은 편안하게 유지.", ["Preparation metadata; relaxed expression retained."], ["Mandatory intense listening eyes."]),
    ("idiom_pupil", "동공지진이라는 말로 당황한 리액션을 표현한 정지 사진.", ["Idiom/context; select a visible option separately."], ["Literal multiple pupils or vibration PASS."]),
    ("context_profile_scope", "행복한 배우의 초상. 이유나 성취 사건은 없다.", ["Broad joy only; achievement_reward_smile not automatically hard-activated."], ["Achievement, gift, audience or success event invented."]),
    ("retrieval_negative", "A calm portrait, with no smile and no wink.", ["Do not activate forms mentioned only in negation or contrast examples."], ["Positive retrieval based on counterexample or provenance text."]),
    ("pack_authority", "평온한 성인 배우의 초상. 후보팩에서 억눌린 분노 항목이 검색됨.", ["Advisory hit remains optional; frozen calm core retains authority."], ["Retrieved candidate treated as user request."]),
    ("label_equivalence", "별칭 없이 위아래 입술이 닿아 납작하게 눌린 경계가 보이게.", ["Component-supported lip pressing discovery without label."], ["A label is required to preserve the form."]),
    ("style_amplitude", "절제된 표정, 눈썹 움직임은 작고 입꼬리 상승도 작다.", ["Amplitude tied to stated components."], ["Personality, emotional truth or overall acting quality inferred."])
]:
    case(*args, language="en" if args[1][0].isascii() else "ko")
(HERE / "REGRESSION-CASES.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in CASES))

PIXELS = []
for cid in ["lip_press", "lip_tighten", "mouth_down", "inner_brow", "knitted_brow", "single_brow", "nose_wrinkle", "upper_lip", "squinch", "held_tears_lips", "hand_mouth"]:
    row = next(x for x in CONCEPTS if x["id"] == "ae_" + cid)
    PIXELS.append(dict(id="pixel_"+cid, concept_id=row["id"], frozen_request="A close-up of one adult actor explicitly showing: " + "; ".join(row["observable_components"]) + ". All other details are locked.",
        pair=dict(baseline="Current pinned data, after request/core/intent locks are frozen.", proposed="Same frozen request, core, locks, model and settings; adopt only the declared proposed components."),
        required_evidence=row["observable_components"], near_miss_controls=row["confusion_boundaries"],
        review="Original full-resolution pixels with the declared actor and mouth/eyelid regions visible; compare neutral baseline when relative position is ambiguous.",
        result_states=["PASS", "FAIL", "UNOBSERVABLE", "NOT_RUN", "MODERATION_BLOCKED"], aggregate_rule="Every applicable component must PASS. Partial is fail. UNOBSERVABLE is not qualification. Blocked image is unscored.",
        repetitions="Pilot: three independent samples per arm; this is a small-sample qualification exercise, not population generalization.",
        execution_status="NOT_RUN"))
write("PIXEL-PLAN.json", dict(schema_version="acting-research-pixel-plan/v1", static_pairs=PIXELS,
    future_sequence_pairs=["double take versus immediate reaction", "averted then returning gaze versus fixed gaze", "microexpression onset/apex/offset versus a sustained pose"],
    audio_plan="Pitch, loudness and quality require audio samples and separate assessors; no static image qualification.",
    interpretation="No generated image, runtime resolver result, model success or user acceptance is claimed by this package."))

summary = dict(source_rows=len(decisions), sources=len(SOURCES), concepts=len(CONCEPTS), new_candidate_drafts=sum(map(len,candidates.values())), reuse_candidates=len(reuse), authored_profile_drafts=len(profiles), bundles=len(bundles), regression_cases=len(CASES), static_pixel_pairs=len(PIXELS))
write("PACKAGE-COUNTS.json", summary)
catalogue = ["# 연기·표정 데이터 초안 목록", "", "연구 초안이다. 출처의 용어 근거와 아래의 구체적인 형태 제안은 구분한다. 모든 개념은 아직 검색·픽셀 검증 전이다.", "", "| 개념 | 처리 | 관찰 요소 또는 범위 | 혼동 경계 | 출처 |", "|---|---|---|---|---|"]
source_map = {x["id"]: x for x in SOURCES}
for r in CONCEPTS:
    link = ", ".join(f"[{sid}]({source_map[sid]['url']})" for sid in r["source_ids"])
    catalogue.append("| " + " | ".join([r["ko"] + " / " + r["id"], r["proposal_action"] + " / " + r["evidence_mode"], "; ".join(r["observable_components"]) or r["en"], "; ".join(r["confusion_boundaries"]), link]) + " |")
(HERE / "CATALOGUE.md").write_text("\n".join(catalogue) + "\n")
inventory_md = ["# 원 대화 368개 표 행의 반영 경로", "", "한 행에 여러 용어가 묶여 있다. 행 수는 고유 단어 수나 검증된 개념 수가 아니다. 각 용어를 동의어로 간주하지 않는다.", ""]
for t in INVENTORY["tables"]:
    inventory_md.extend([f"## {t['section']}절 / 표 {t['table_index']}: {t['topic']}", "", routes[t["table_index"]][2], "", "| 행 ID | 원 용어 묶음 | 반영 단계 |", "|---|---|---|"])
    inventory_md.extend(f"| {r['source_row_id']} | {r['term_group']} | {r['phase']} |" for r in decisions if r["table_index"] == t["table_index"])
    inventory_md.append("")
(HERE / "TERM-DECISIONS.md").write_text("\n".join(inventory_md).rstrip() + "\n")
references_md = ["# 출처와 확인 범위", "", "확인일: 2026-10-03 KST. 연구·용어·훈련의 근거이며 생성 성공의 증거가 아니다.", "", "| ID / 출처 | 확인 수준 | 지원하는 내용 | 한계 |", "|---|---|---|---|"]
for s in SOURCES:
    references_md.append(f"| {s['id']} / [{s['title']}]({s['url']}) | {s['verification']} | {s['supports']} | {s['limits']} |")
(HERE / "SOURCES.md").write_text("\n".join(references_md) + "\n")
print(json.dumps(summary, ensure_ascii=False))
