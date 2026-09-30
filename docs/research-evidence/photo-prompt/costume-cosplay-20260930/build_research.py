#!/usr/bin/env python3
"""Build research-only costume/cosplay artifacts. Does not edit runtime assets."""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
DATE = "2026-09-30"
STATUS = "research_proposal_not_integrated_not_render_qualified"


def digest(value):
    return sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


SOURCES = []


def source(sid, title, url, publisher, kind, review, facts, limits, date=None):
    SOURCES.append(dict(
        id=sid, title=title, url=url, publisher=publisher,
        source_kind=kind, review_level=review,
        retrieved_date=DATE, publication_or_event_date=date,
        factual_notes=facts, claim_limits=limits,
        original_text_or_images_redistributed=False,
    ))


source("S01", "FanimeCon 2026 Cosplay Gatherings Listing",
       "https://www.fanime.com/cosplay-gatherings/cosplay-gatherings-listing/",
       "FanimeCon", "organizer_schedule", "page_text",
       ["Games, anime, Vocaloid/UTAU, Project Sekai and Hololive have named gathering slots."],
       "Scheduled gatherings establish programming; participant counts and costume-version frequencies are absent.", "2026")
source("S02", "Anime Expo: Cosplay Gatherings help",
       "https://help.anime-expo.org/support/solutions/folders/70000471472",
       "Anime Expo", "organizer_definition", "search_excerpt",
       ["Gatherings are attendee-organized meetings for costumes sharing a series or game."],
       "The definition is not an attendance survey.")
source("S03", "World Cosplay Championship 2025 results",
       "https://wcc.worldcosplaysummit.jp/history/2025/",
       "World Cosplay Summit", "organizer_competition_results", "page_text",
       ["The results identify teams, works, characters and distinct craft/performance awards."],
       "Competition selection is not a sample of all event attendees.", "2025")
source("S04", "Comic-Con Masquerade page, 2025 winners section",
       "https://www.comic-con.org/cc/comic-con-international-2026-masquerade/",
       "Comic-Con International", "organizer_competition_results", "page_text",
       ["The inspected page includes a 2025 winners section with The Wiz and Bumblebee."],
       "The URL/header says 2026; do not relabel the embedded 2025 winners as 2026 results.", "2025 results")
source("S05", "WonderCon Masquerade, 2025 winners section",
       "https://www.comic-con.org/wc/things-to-do/masquerade/",
       "Comic-Con International", "organizer_competition_results", "search_excerpt",
       ["The excerpt includes original Night Sisters and a Super Sailor Jupiter entry."],
       "Page heading and result year differ; use the explicit 2025 section only.", "2025 results")
source("S06", "Dragon Con Masquerade Winners 2025",
       "https://dailydragon.dragoncon.org/2025/masquerade-winners-2025/",
       "Dragon Con Daily Dragon", "organizer_event_report", "search_excerpt",
       ["Listed entries span KPop Demon Hunters, Optimus Prime, Totoro and Medusa."],
       "Award entries cannot establish the frequency of these costumes on the convention floor.", "2025")
source("S07", "Pyrkon: winners of recent Masquerades",
       "https://pyrkon.pl/en/the-winners-of-recent-editions-of-the-masquerade/",
       "Pyrkon", "organizer_competition_results", "search_excerpt",
       ["The 2025 entry identifies Neve Gallus and Lucanis Dellamorte from Dragon Age: The Veilguard."],
       "Selected winners provide repertoire examples, not a popularity ranking.", "2025")
source("S08", "CONvergence 2025 Masquerade",
       "https://www.convergence-con.org/about/archive/2025-convention/2025-masquerade/",
       "CONvergence", "organizer_competition_results", "search_excerpt",
       ["The program includes a Rococo Hatsune Miku interpretation."],
       "An interpreted design should retain both its character and historical-style dimensions.", "2025")
source("S09", "G-STAR: previous event results",
       "https://www.gstar.or.kr/gstar/gstar_last_list.do",
       "G-STAR", "organizer_archive", "search_excerpt",
       ["The archive includes the 2025 game cosplay awards."],
       "The retrieved excerpt does not supply wearer counts or a character-frequency table.", "2025")
source("S10", "G-STAR 2025 cosplay scene report",
       "https://www.yna.co.kr/view/AKR20251115026500017",
       "Yonhap News", "reporter_event_observation", "search_excerpt",
       ["The report names StarCraft Zealot and Helldivers costumes outside BEXCO."],
       "A reporter-selected scene confirms examples, not their share of all costumes.", "2025-11-15")
source("S11", "C105 selected cosplay photo report",
       "https://s.inside-games.jp/article/2025/01/02/162946.html?pickup-text-list=1",
       "INSIDE", "reporter_selected_gallery", "search_excerpt",
       ["The selected gallery names NIKKE, Genshin Impact, Zenless Zone Zero, Blue Archive and VTuber cosplay."],
       "C105 occurred in December 2024; the article was published in January 2025. A curated gallery has no attendance denominator.", "2025-01-02")
source("S12", "Enako first major photobook, publisher catalog",
       "https://books.shueisha.co.jp/items/contents.html?isbn=978-4-08-780861-2",
       "Shueisha", "official_publisher_catalog", "page_text",
       ["The book combines licensed manga-character cosplay with an original design by Masakazu Katsura."],
       "This is a 2019 publishing case, not evidence of 2026 event popularity.", "2019")
source("S13", "NIKKE × Kyoto collaboration event report with Iori Moe",
       "https://prtimes.jp/main/html/rd/p/000000139.000145037.html",
       "Proxima Beta Pte. Ltd. via PR TIMES", "publisher_event_report", "page_text",
       ["Iori Moe appeared as Anis: Star in a bespoke Kyo-Yuzen kimono collaboration outfit."],
       "Keep the collaboration version separate from the character's standard game outfit and mascot representation.", "2026-09-15")
source("S14", "NIKKE Tokyo Game Show 2022 booth announcement",
       "https://prtimes.jp/main/html/rd/p/000000038.000084968.html",
       "Level Infinite / Proxima Beta via PR TIMES", "publisher_appearance_announcement", "search_excerpt",
       ["The announcement assigns Marian to Iori Moe and Neon to Kokoro Shinozaki."],
       "An announced appearance is not, by itself, verified attendance or a visual costume inspection.", "2022")
source("S15", "RZCOS C107 and Guangzhou BrownDust2 field report",
       "https://m.inven.co.kr/board/webzine/2898/2581?iskin=nikke",
       "RZCOS self-authored post on Inven", "creator_event_self_report", "search_indexed_post_text",
       ["C107 assignments include 나리땽: 쉐도우바니 에레니르 and 시루: 프로즌 퀸 빌헬미나.",
        "The Guangzhou report names 나리땽: 데이드림 바니 모르페아 and 야살: 프로즌 퀸 빌헬미나."],
       "Team self-report is explicit about assignments; embedded photos were not inspected here. Preserve the source's Korean spellings for matching.", "2026-01-14")
source("S16", "Spiral Cats interview: LoL cosplay project",
       "https://www.inven.co.kr/webzine/news/?news=166462",
       "Inven interview with Spiral Cats", "creator_interview", "search_excerpt",
       ["The interview discusses Arcade Ahri, Riven and Gnar in a team project."],
       "This older project illustrates skin versions and character types; it does not establish current frequency.", "2016")
source("S17", "NIKKE AGF 2025 booth announcement",
       "https://m.inven.co.kr/webzine/wznews.php?idx=311724&iskin=it",
       "NIKKE publisher material via Inven", "publisher_appearance_announcement", "search_excerpt",
       ["The announcement plans a professional cosplay runway for AGF 2025."],
       "Plans and actual participation are separate statuses.", "2025-11-28")
source("S18", "Kamui Cosplay costume project archive",
       "https://www.kamuicosplay.com/project_category/costumes/",
       "Kamui Cosplay", "creator_portfolio_index", "page_text",
       ["Projects cover game-character clothing, armor and film/game costumes."],
       "A portfolio is selected output; it cannot estimate either all cosplay or the creator's complete work history.")
source("S19", "Kamui Cosplay: Yelan",
       "https://www.kamuicosplay.com/project/yelan-genshin-impact/",
       "Kamui Cosplay", "creator_build_record", "page_text_and_browser_image",
       ["The maker describes asymmetric construction, a separate bow build and collaboration on wig styling."],
       "The inspected front/back composite supports visible asymmetry; hidden attachment methods require the maker record.")
source("S20", "Kamui Cosplay: Yelan making article",
       "https://www.kamuicosplay.com/2025/10/18/yelan-from-genshin-impact/",
       "Kamui Cosplay", "creator_build_record", "search_excerpt",
       ["The article lists multiple textile types and describes a Gamescom 2023 costume project."],
       "The 2025 publication date is not the project's event date.", "2025-10-18")
source("S21", "Kamui Cosplay: Iden Versio",
       "https://www.kamuicosplay.com/project/idenversio/",
       "Kamui Cosplay", "creator_commission_build_record", "page_text",
       ["The maker reports EVA foam helmet/armor/props paired with a cotton suit for an EA/Lucasfilm commission."],
       "Metal-like finish does not establish metal composition, ballistic protection or a functioning weapon.")
source("S22", "Kamui Cosplay: Demonic Brigitte",
       "https://www.kamuicosplay.com/project/brigitte/",
       "Kamui Cosplay", "creator_original_crossover_build", "page_text_and_browser_image",
       ["The record identifies an Overwatch/Diablo crossover design with foam construction and LEDs."],
       "The published image is edited; it cannot prove every photographed fire/glow effect is produced by the physical costume.")
source("S23", "Kamui Cosplay: Demonic Shield",
       "https://www.kamuicosplay.com/project/demonicshield/",
       "Kamui Cosplay", "creator_prop_build_record", "search_excerpt",
       ["The shield build uses foam, painting and programmed lighting effects."],
       "Electrical operation is maker-reported; a photograph can establish only appearance.")
source("S24", "Kamui Cosplay: an accessible hobby",
       "https://www.kamuicosplay.com/2024/01/09/cosplay-accessible-hobby/",
       "Kamui Cosplay", "creator_materials_overview", "search_excerpt",
       ["The maker describes a range from paper/fabric and thermoplastics to EVA foam and 3D printing."],
       "No material or tool is compulsory for every cosplay.", "2024-01-09")
source("S25", "Kinpatsu: Jinx Arcane tutorials and patterns",
       "https://kinpatsucosplay.com/product/jinx-arcane-cosplay-tutorials-patterns/",
       "Kinpatsu Cosplay", "creator_tutorial_catalog", "page_text",
       ["The tutorial covers sewing, wig styling, belts, boots and tattoo templates for the Arcane version."],
       "Catalog coverage does not demonstrate every technique in an inspected finished image.")
source("S26", "Kinpatsu: Jinx League of Legends props",
       "https://kinpatsucosplay.com/product/jinx-cosplay-props-league-of-legends/",
       "Kinpatsu Cosplay", "creator_tutorial_catalog", "search_excerpt",
       ["The prop tutorial describes foam finishing and illuminated details."],
       "Keep this League of Legends prop version distinct from the Arcane costume tutorial.")
source("S27", "Kinpatsu: K/DA Ahri",
       "https://kinpatsucosplay.com/product/kda-ahri-league-of-legends/",
       "Kinpatsu Cosplay", "creator_tutorial_catalog", "page_text",
       ["The tutorial describes a lightweight transparent tail with a harness, ears and styled wig."],
       "The source supports one K/DA interpretation, not a rule that every Ahri tail is transparent.")
source("S28", "Kinpatsu: Ears and Tails for Cosplay",
       "https://kinpatsucosplay.com/product/ears-and-tails-for-cosplay/",
       "Kinpatsu Cosplay", "creator_tutorial_catalog", "page_text",
       ["The book distinguishes shaped/poseable ears, fur treatment and tail attachment methods."],
       "Costume appendages are made objects; they do not establish wearer anatomy or species.")
source("S29", "Kinpatsu: Witch Hat Patterns",
       "https://kinpatsucosplay.com/product/witch-hat-patterns/",
       "Kinpatsu Cosplay", "creator_pattern_catalog", "search_excerpt",
       ["Multiple witch-hat variants are offered, including foam-based construction."],
       "A witch label alone does not specify brim width, cone curvature or construction.")
source("S30", "Yaya Han: Rumi",
       "https://www.yayahan.com/Portfolio/rumi",
       "Yaya Han", "creator_stage_costume_build_record", "page_text_and_browser_image",
       ["The maker explicitly describes a hanbok-inspired stage interpretation with layered textiles, applied motifs and lighting."],
       "Traditional clothing, a screen design and a stage reinterpretation have separate contracts. Hidden corsetry/electronics are maker-reported.")
source("S31", "Yaya Han: Carmilla",
       "https://www.yayahan.com/Portfolio/carmilla",
       "Yaya Han", "creator_build_record", "search_excerpt",
       ["The Vampire Hunter D: Bloodlust costume uses red velvet and contrasting gold fabric."],
       "These colors/materials belong to this version, not to every vampire costume.")
source("S32", "Yaya Han: Misty May",
       "https://www.yayahan.com/Portfolio/misty-may",
       "Yaya Han", "creator_build_record", "search_excerpt",
       ["The Otaku no Video project combines a bodysuit, cropped vest and a feathered tail."],
       "A bunny-themed costume does not imply a specific real body, material or sexual scene.")
source("S33", "Yaya Han: Jessica Rabbit",
       "https://www.yayahan.com/Portfolio/jessica-rabbit",
       "Yaya Han", "creator_build_record", "search_excerpt",
       ["The maker describes internal corsetry and hair styling for the character silhouette."],
       "The result is costume construction; it is not a measurement or claim about the wearer's natural body.")
source("S34", "Yaya Han: Lulu",
       "https://www.yayahan.com/Portfolio/lulu",
       "Yaya Han", "creator_build_record", "search_excerpt",
       ["The Final Fantasy X build combines corsetry, belt construction, fur trim and decorative work."],
       "The layered construction should not be collapsed into a single generic black dress.")
source("S35", "V&A Costume collection",
       "https://www.vam.ac.uk/collections/costume",
       "Victoria and Albert Museum", "museum_collection_overview", "page_text",
       ["Costume spans theater, opera, dance, popular music, cabaret and circus."],
       "A broad collecting category does not define every visual feature of each costume family.")
source("S36", "The Museum at FIT: Uniformity",
       "https://exhibitions.fitnyc.edu/uniformity/",
       "The Museum at FIT", "museum_exhibition", "page_text",
       ["The exhibition connects military, school, work and sports uniforms to fashion, including historical service and flight clothing."],
       "Historical uniform elements do not establish modern duty requirements or the wearer's actual occupation.")
source("S37", "The Museum at FIT: Gothic Dark Glamour",
       "https://www.fitnyc.edu/museum/exhibitions/gothic-dark-glamour.php",
       "The Museum at FIT", "museum_exhibition", "search_excerpt",
       ["Gothic is a fashion/aesthetic domain with several imaginative and historical references."],
       "It is not synonymous with vampire cosplay, Lolita fashion or exclusively black fabric.")
source("S38", "The Museum at FIT: Exposed, a History of Lingerie",
       "https://exhibitions.fitnyc.edu/exposed-lingerie-history/",
       "The Museum at FIT", "museum_exhibition", "search_excerpt",
       ["The exhibition distinguishes structured corsets and softer undergarments and their relation to outer fashion."],
       "A visible clothing construction does not supply a sexual activity or context.")
source("S39", "FIT Fashion History Timeline: Panniers",
       "https://fashionhistory.fitnyc.edu/panniers/",
       "FIT Fashion History Timeline", "museum_affiliated_terminology", "page_text",
       ["Panniers shape lateral skirt width while the front/back can remain comparatively flat."],
       "Skirt outline alone may not identify the hidden support material.")
source("S40", "FIT Fashion History Timeline: Bustle",
       "https://fashionhistory.fitnyc.edu/bustle/",
       "FIT Fashion History Timeline", "museum_affiliated_terminology", "page_text",
       ["A bustle supports volume behind the body."],
       "Posterior volume and lateral pannier width are different relations.")
source("S41", "Theatrecrafts costume glossary",
       "https://theatrecrafts.com/pages/home/topics/costume/glossary/",
       "Theatrecrafts", "theater_practitioner_reference", "page_text",
       ["The glossary distinguishes bodice/corset terms and covers aging costumes and quick-change layering."],
       "Terminology supplies construction concepts, not a particular character's canonical design.")
source("S42", "V&A: Kimono",
       "https://www.vam.ac.uk/articles/kimono",
       "Victoria and Albert Museum", "museum_clothing_reference", "search_excerpt",
       ["Kimono discussion includes wrapped clothing and obi-related styling."],
       "Specific era, sleeve, closure and wearing contexts require variant-level evidence.")
source("S43", "V&A: Hanbok, traditional Korean dress",
       "https://www.vam.ac.uk/articles/hanbok-traditional-korean-dress",
       "Victoria and Albert Museum", "museum_clothing_reference", "page_text",
       ["Hanbok is a broad clothing tradition with components including jeogori and chima."],
       "A contemporary stage costume should not overwrite historical/traditional forms.")
source("S44", "V&A: Conserving a ballet tutu",
       "https://www.vam.ac.uk/articles/conserving-a-ballet-tutu",
       "Victoria and Albert Museum", "museum_conservation_record", "search_excerpt",
       ["The conservation example identifies layered tulle in a ballet tutu."],
       "One conserved tutu does not establish a single universal length or disk shape.")
source("S45", "V&A: The story of pantomime",
       "https://www.vam.ac.uk/articles/the-story-of-pantomime",
       "Victoria and Albert Museum", "museum_performance_history", "search_excerpt",
       ["Harlequin is described with a mask and patched clothing."],
       "Harlequin, Pierrot and a generic clown should retain separate variant labels.")
source("S46", "World of WearableArt 2025 People's Choice: The Autumn King",
       "https://www.worldofwearableart.com/content-hub/2025-peoples-choice-award",
       "World of WearableArt", "organizer_design_record", "page_text",
       ["Catherine Anderton's wearable-art design combines several textile and foam materials."],
       "Wearable sculpture is a representation mode; it need not depict a licensed character.", "2025")
source("S47", "World of WearableArt: Hidden Layers",
       "https://www.worldofwearableart.com/content-hub/2022-stuff-peoples-choice-award-winner",
       "World of WearableArt", "organizer_design_record", "search_excerpt",
       ["Anna Weszelovszky's Hidden Layers is described as a transforming garment."],
       "A still image does not verify the complete transformation sequence.", "2022")
source("S48", "UNESCO: Kebaya knowledge, skills, traditions and practices",
       "https://ich.unesco.org/en/RL/kebaya-knowledge-skills-traditions-and-practices-02090",
       "UNESCO Intangible Cultural Heritage", "heritage_reference", "search_excerpt",
       ["Kebaya includes front-opening tops, often embroidery and fasteners, across several Southeast Asian communities."],
       "Do not flatten regional variants into one national costume or infer wearer identity.")
source("S49", "Roots: Cheongsam tailoring",
       "https://www.roots.gov.sg/ich-landing/ich/cheongsam-tailoring",
       "National Heritage Board Singapore", "heritage_craft_reference", "search_excerpt",
       ["The reference discusses standing collars, diagonal openings and knotted fasteners."],
       "Do not force one fitted modern silhouette onto every qipao/cheongsam period.")
source("S50", "The Met: Chasuble, object 158329",
       "https://www.metmuseum.org/art/collection/search/158329",
       "The Metropolitan Museum of Art", "museum_object_record", "search_excerpt",
       ["This mid-nineteenth-century chasuble uses shaped appliquéd patches to create a textile illusion."],
       "A single object does not define all clergy, religious communities or vestments.")
source("S51", "The Met: The Chiton, Peplos, and Himation in Modern Dress",
       "https://www.metmuseum.org/pt/essays/the-chiton-peplos-and-himation-in-modern-dress",
       "The Metropolitan Museum of Art", "museum_essay", "search_indexed_article_text",
       ["The essay distinguishes structural garment types and warns that ancient clothing terminology and evidence vary."],
       "A modern draped costume is not direct proof of historically exact ancient dress.", "2003-10-01")
source("S52", "The Met: Kaftan, object 454043",
       "https://www.metmuseum.org/art/collection/search/454043",
       "The Metropolitan Museum of Art", "museum_object_record", "search_excerpt",
       ["An Ottoman kaftan fragment preserves large woven motifs on silk."],
       "A fragment provides textile/object evidence, not a complete worn silhouette.")
source("S53", "V&A: A celebration of carnival in seven objects",
       "https://www.vam.ac.uk/articles/a-vampa-celebration-of-carnival-in-seven-objects",
       "Victoria and Albert Museum", "museum_collection_essay", "search_indexed_article_text",
       ["The objects include a Keith Khan stilt-walker costume worn at Preston Carnival in 1988."],
       "Carnival has specific local histories; do not treat it as a single generic feathered showgirl design.", "2025-09-08")


# These are researcher-authored, request-selectable visual variants.
# Source references support context/construction distinctions, not universal definitions.
PROFILES = []


def c(slot, ko, en, owner, predicate, target):
    return dict(slot=slot, ko=ko, en=en, owner=owner,
                assertion=dict(type=predicate, subject=owner, object=target))


def profile(pid, ko, family, refs, evidence, broad, view, confusions, components,
            priority="P1", basis="source_informed_authored_variant"):
    authored = []
    for i, comp in enumerate(components, 1):
        cid = f"ccx_{pid.lower()}_{i:02d}"
        authored.append({
            "id": cid, **comp,
            "claim_type": "researcher_authored_observable_contract",
            "match_terms": [comp["en"]],
            "evidence_field": f"component_{i}_phrase",
            "evidence_terms": [comp["en"]],
            "min_content_words": 3,
            "render_gate": {
                "id": f"vo_{cid}", "review_scale": "native",
                "description": comp["en"] + "; inspect the declared owner and relation. "
                               "A nearby unrelated object or an occluded relation does not satisfy this gate.",
                "unseen_required_relation": "FAIL",
                "hidden_material_or_mechanism_without_visible_contract": "UNSCORED",
            },
        })
    PROFILES.append(dict(
        id=pid, label_ko=ko, family=family, source_refs=refs,
        evidence_basis=basis, qualification_status=STATUS, implementation_priority=priority,
        narrow_variant_evidence_examples=evidence, broad_terms_not_sufficient=broad,
        activation_policy="independent_request_evidence_only",
        activation_unit="independently_supported_component",
        profile_discovery_does_not_activate_all_components=True,
        wearer_scope="request_supported_pair" if pid == "CC09" else "request_supported_single_wearer",
        runtime_compilation_status="not_compiled",
        minimum_view=view, confusion_boundaries=confusions,
        components=authored,
        source_scope="References support the source context; component clauses are authored proposals, "
                     "not assertions that all members of the named family have these features.",
    ))


profile("CC01", "가슴판이 있는 메이드 앞치마", "service_uniform",
        ["S36", "S41"], ["가슴판과 어깨끈이 있는 앞치마"], ["메이드", "maid", "apron"],
        "front three-quarter torso including waist ties",
        ["허리 앞치마는 가슴판 앞치마의 대체 증거가 아니다.", "메이드 코스튬은 실제 접객 업무를 뜻하지 않는다."], [
    c("garment_detail", "어깨끈과 가슴판이 이어진 앞치마",
      "two apron shoulder straps join a separate chest bib above the waist band",
      "apron shoulder straps", "connected_to", "apron chest bib"),
    c("garment_detail", "드레스 바깥으로 묶인 앞치마 허리띠",
      "the apron waist band crosses over the dress and continues into visible side ties",
      "apron waist band", "layered_over", "costume dress"),
    c("garment_detail", "치맛자락과 구분되는 앞치마 패널",
      "the apron lower panel ends separately above the underlying dress hem",
      "apron lower panel", "distinct_from", "dress hem"),
], "P0")
profile("CC02", "집사 테일코트의 앞뒤 길이 차", "service_uniform",
        ["S35", "S41"], ["앞이 짧고 뒤 꼬리가 긴 집사 테일코트"], ["집사", "butler"],
        "front and side or three-quarter full body",
        ["일반 긴 코트와 테일코트를 구분한다.", "조끼 앞섶과 코트 라펠의 소유자를 구분한다."], [
    c("costume_style", "짧은 앞자락과 긴 뒤 꼬리",
      "the formal coat has a short front and two longer tails behind the hips",
      "formal coat", "directional_length", "front short and rear long"),
    c("garment_detail", "코트 안쪽의 독립된 조끼 앞섶",
      "a buttoned waistcoat remains visible inside the open coat lapels",
      "waistcoat", "layered_inside", "formal coat lapels"),
], basis="source_context_only_original_variant")
profile("CC03", "세일러 칼라와 별도 리본", "school_uniform_cosplay",
        ["S36"], ["등판까지 이어지는 세일러 칼라와 가슴 리본"], ["교복", "school uniform", "seifuku"],
        "front and three-quarter shoulder view",
        ["넥타이만으로 세일러 칼라를 충족하지 않는다.", "착용자의 나이·재학 여부를 의상에서 추정하지 않는다."], [
    c("garment_detail", "어깨에서 등판으로 이어지는 세일러 칼라",
      "the sailor collar spreads across both shoulders and continues onto the upper back",
      "sailor collar", "connected_across", "shoulders and upper back"),
    c("wearable_accessory", "칼라 아래 묶인 가슴 리본",
      "a tied chest ribbon sits below the collar opening without replacing the collar",
      "chest ribbon", "positioned_below", "collar opening"),
], "P0", "source_context_only_original_variant")
profile("CC04", "학란형 스탠드 칼라와 중앙 단추", "school_uniform_cosplay",
        ["S36"], ["서 있는 목깃과 세로 중앙 단추의 학란형 상의"], ["학란", "gakuran", "uniform"],
        "front torso with collar and lower buttons",
        ["블레이저 라펠과 스탠드 칼라를 구분한다.", "금색 단추는 실제 계급의 증거가 아니다."], [
    c("garment_detail", "라펠 없이 서 있는 칼라",
      "the jacket collar stands around the neck without folded lapels",
      "jacket collar", "surrounds", "neck opening"),
    c("garment_detail", "상하로 이어지는 중앙 단추 여밈",
      "a single central line of buttons closes the jacket front from collar toward waist",
      "jacket buttons", "aligned_along", "central front closure"),
], basis="source_context_only_original_variant")
profile("CC05", "장식 군복의 견장·브레이드·흉장", "fantasy_uniform",
        ["S36"], ["견장과 장식 끈을 단 판타지 정복"], ["군복", "military costume", "officer"],
        "front three-quarter upper body",
        ["의전 장식과 전투 장비는 다른 변형이다.", "장식 흉장은 실제 국가·계급·임무를 자동으로 지정하지 않는다."], [
    c("wearable_accessory", "어깨 위에 고정된 장식 견장",
      "decorative epaulettes sit on the jacket shoulders with visible bases",
      "epaulettes", "anchored_to", "jacket shoulders"),
    c("wearable_accessory", "재킷에 끝점이 붙은 가슴 브레이드",
      "a braided decorative cord crosses the chest with both ends attached to the jacket",
      "decorative cord", "attached_at_both_ends", "jacket front"),
], basis="source_context_only_original_variant")
profile("CC06", "비행·정비 코스튬의 연속 작업복", "work_uniform",
        ["S36", "S21"], ["몸통과 바지가 이어지는 작업용 점프수트"], ["비행사", "mechanic", "pilot"],
        "front full body with waist and legs",
        ["정복 재킷과 일체형 작업복을 구분한다.", "주머니와 지퍼만으로 실제 보호 성능을 주장하지 않는다."], [
    c("costume_style", "상하가 이어진 점프수트",
      "the work suit continues from the torso through the waist into both trouser legs",
      "work suit", "continuous_across", "torso waist and legs"),
    c("garment_detail", "몸통 앞에 붙은 기능성 포켓",
      "patch pockets are sewn onto the suit front and remain separate from the opening seam",
      "patch pockets", "attached_to", "suit front"),
])
profile("CC07", "역사 간호복을 인용한 칼라·커프·모자", "period_uniform_costume",
        ["S36"], ["흰 칼라와 커프를 붙인 복고 간호복 코스튬"], ["간호사", "nurse"],
        "head and front torso with forearms",
        ["역사적 캡을 현대 간호사의 필수 요소로 적용하지 않는다.", "코스튬은 임상 업무 프로필을 활성화하지 않는다."], [
    c("garment_detail", "목과 손목에 분리된 흰 장식",
      "white collar and cuff pieces border the darker costume at neck and wrists",
      "white trim pieces", "border", "neck and wrists"),
    c("wearable_accessory", "가발 위의 작은 접힌 모자",
      "a small folded costume cap rests visibly on top of the styled hair",
      "costume cap", "rests_on", "styled hair"),
])
profile("CC08", "마법소녀 무대복의 보디스·분리 소매·치마", "magical_girl_stage",
        ["S01", "S03", "S35"], ["분리 소매와 여러 겹 짧은 치마를 가진 무대복"], ["마법소녀", "magical girl"],
        "front full body with both upper arms",
        ["마법소녀라는 장르명은 특정 색·리본·노출 정도를 지정하지 않는다.", "분리 소매를 몸통 의상과 합쳐 그리지 않는다."], [
    c("costume_style", "몸통 아래로 겹친 짧은 치마",
      "a fitted stage bodice joins a short skirt with two visibly separate outer layers",
      "stage bodice", "joins", "layered short skirt"),
    c("garment_detail", "보디스와 떨어진 팔 소매",
      "detached sleeve cuffs encircle the arms with visible gaps from the bodice",
      "detached sleeves", "separated_from", "bodice"),
], "P0", "source_context_only_original_variant")
profile("CC09", "두 착용자의 아이돌 의상 반복 장식", "ensemble_stage",
        ["S01", "S30"], ["두 의상에서 같은 위치에 반복되는 팀 장식"], ["아이돌", "idol", "group"],
        "two wearer full bodies in one frame",
        ["색이 같아도 장식의 위치 관계가 다르면 같은 규격의 증거가 아니다.", "장식은 지정된 각 의상에 속해야 한다."], [
    c("garment_detail", "두 재킷의 같은 높이에 반복되는 테두리",
      "matching trim bands border both wearers jackets at the same structural positions",
      "paired jacket trim", "repeats_across", "both wearer jackets"),
    c("wearable_accessory", "각 허리에서 따로 늘어지는 리본",
      "each wearer has a separate ribbon hanging from their own waist attachment",
      "paired waist ribbons", "owned_separately_by", "each wearer waist"),
], basis="source_context_only_original_variant")
profile("CC10", "캐릭터 의상의 좌우 비대칭 패널", "character_version_structure",
        ["S19", "S20"], ["서로 다른 양팔 구조와 분리된 비대칭 치맛단"], ["게임 코스프레", "Yelan", "비대칭"],
        "front full body plus rear companion view",
        ["캐릭터 이름만으로 특정 비대칭 변형을 활성화하지 않는다.", "앞뒤 합성 사진은 동일한 순간·단일 장면이 아니다."], [
    c("garment_detail", "서로 다른 양팔 덮개",
      "one arm has a long fabric sleeve while the other uses a separate cuff",
      "arm coverings", "asymmetric_between", "two arms"),
    c("garment_detail", "길이가 다른 좌우 바깥 패널",
      "the two outer skirt panels end at different heights around the legs",
      "outer skirt panels", "asymmetric_length", "two sides of skirt"),
    c("garment_detail", "가슴 의상과 분리되는 모피 칼라",
      "the pale fur collar remains a separate outer piece above the bodice",
      "fur collar", "layered_over", "bodice"),
], "P0")
profile("CC11", "구조가 구분되는 마녀 모자", "fantasy_headwear",
        ["S29"], ["넓은 챙과 휘어진 원뿔이 만나는 마녀 모자"], ["마녀", "witch", "hat"],
        "head and hat edge with cone tip included",
        ["마녀는 챙 없는 두건·후드 변형도 가능하다.", "모자의 형태로 재료를 확정하지 않는다."], [
    c("wearable_accessory", "원뿔 아래를 둘러싼 넓은 챙",
      "a broad hat brim surrounds the base of the pointed crown",
      "hat brim", "surrounds", "pointed crown base"),
    c("wearable_accessory", "머리에서 이어져 휘어진 모자 끝",
      "the bent hat tip remains connected to the crown above the wearers head",
      "hat tip", "connected_to", "hat crown"),
], "P0")
profile("CC12", "연금술사·마법사의 로브와 내부 작업층", "fantasy_role",
        ["S35", "S41"], ["열린 로브 안에 조끼와 허리 도구가 보이는 의상"], ["마법사", "연금술사", "wizard", "alchemist"],
        "front three-quarter torso to knees",
        ["망토·로브·코트는 소매와 여밈 구조가 다르다.", "책·약병만으로 초자연 능력을 확정하지 않는다."], [
    c("costume_style", "내부 조끼가 보이는 열린 로브",
      "an open long robe frames a separate inner vest and waist belt",
      "outer robe", "frames", "inner vest and belt"),
    c("prop", "허리띠에 매달린 작은 용기",
      "small costume bottles hang from visible loops on the waist belt",
      "costume bottles", "suspended_from", "belt loops"),
], basis="source_context_only_original_variant")
profile("CC13", "갑옷 패널과 부드러운 관절층", "prop_armor",
        ["S21", "S22", "S24"], ["팔꿈치와 무릎에 천 층이 드러나는 소품 갑옷"], ["갑옷", "armor", "metal"],
        "full body with bent elbow or knee",
        ["금속 광택과 실제 금속 재료를 구분한다.", "소품 갑옷은 방호 성능 프로필을 자동 활성화하지 않는다."], [
    c("garment_detail", "단단한 패널 사이로 보이는 천 관절층",
      "dark flexible fabric remains visible between the rigid armor panels at the joints",
      "joint fabric", "visible_between", "armor panels"),
    c("garment_detail", "관절을 피해 겹치는 갑옷 패널",
      "overlapping armor edges stop around the bent joint instead of merging across it",
      "armor edges", "stop_around", "bent joint"),
    c("surface_material", "패널 표면에 국한된 금속 같은 도색",
      "metal-like painted highlights remain on the costume panels while the joint fabric stays matte",
      "painted highlights", "localized_on", "costume armor panels"),
], "P0")
profile("CC14", "특촬형 슈트의 패널과 장갑 경계", "tokusatsu_suit",
        ["S01", "S03"], ["천 슈트 위의 가슴 패널과 별도 장갑"], ["특촬", "tokusatsu", "hero suit"],
        "front full body with wrists",
        ["특촬의 모든 캐릭터가 같은 헬멧·색·벨트를 쓰지는 않는다.", "접합선을 몸의 해부 구조로 해석하지 않는다."], [
    c("costume_style", "천 슈트 위에 놓인 가슴 장식판",
      "a shaped chest panel sits over a continuous fabric hero suit",
      "chest panel", "layered_over", "fabric suit"),
    c("wearable_accessory", "소매 끝과 구분되는 장갑 커프",
      "separate glove cuffs overlap the sleeve ends at both wrists",
      "glove cuffs", "overlap", "sleeve ends"),
], basis="source_context_only_original_variant")
profile("CC15", "헬멧과 목 천 층의 접합", "helmet_costume",
        ["S21"], ["헬멧 아래에 목 천이 남는 장갑 코스튬"], ["helmet", "우주복", "soldier"],
        "head and shoulder detail",
        ["바이저 외관은 실제 밀폐·생명 유지 성능의 증거가 아니다.", "헬멧을 피부나 턱과 융합하지 않는다."], [
    c("wearable_accessory", "목 원단 위에서 끝나는 헬멧 아래쪽",
      "the helmet lower edge ends above a separate fabric neck covering",
      "helmet lower edge", "distinct_from", "fabric neck covering"),
    c("wearable_accessory", "헬멧 안쪽의 독립된 바이저",
      "the dark visor is bounded by the helmet shell with a visible edge",
      "visor", "bounded_by", "helmet shell"),
])
profile("CC16", "로봇 코스튬의 큰 몸통과 내부 팔다리", "mecha_costume",
        ["S03", "S04", "S24"], ["큰 상자형 몸통 바깥껍질 안으로 이어지는 천 관절"], ["로봇", "mecha", "Bumblebee"],
        "full body with joint openings",
        ["기계 코스튬과 실제 로봇을 구분한다.", "작품명·캐릭터명은 특정 내부 작동 장치를 뜻하지 않는다."], [
    c("costume_style", "큰 기계 몸통 아래의 분리된 다리",
      "a large angular costume torso remains separate from two articulated-looking leg shells",
      "costume torso shell", "distinct_from", "leg shells"),
    c("garment_detail", "기계 껍질 틈의 착용용 천 관절",
      "flexible fabric shows inside the gaps between the large costume shells",
      "flexible joint fabric", "visible_between", "costume shells"),
], basis="source_context_only_original_variant")
profile("CC17", "부착 위치가 보이는 동물 귀 장식", "animal_appendage",
        ["S28"], ["머리띠에 붙은 모피 귀 장식"], ["네코미미", "fox ears", "bunny"],
        "head detail including both ear bases",
        ["귀 장식은 실제 동물 귀·종족의 증거가 아니다.", "큰 토끼 귀와 작은 삼각 귀는 독립 변형이다."], [
    c("wearable_accessory", "머리띠에 고정된 모피 귀",
      "two faux-fur costume ears have visible bases attached to a hair band",
      "costume ear bases", "attached_to", "hair band"),
    c("wearable_accessory", "가발과 구분되는 귀 안쪽 패널",
      "contrasting inner ear panels remain inside the costume ear outlines above the wig",
      "inner ear panels", "contained_by", "costume ear outlines"),
], "P0")
profile("CC18", "허리 부착부가 보이는 코스튬 꼬리", "animal_appendage",
        ["S28"], ["허리 벨트에 뿌리가 붙은 꼬리 장식"], ["꼬리", "tail", "gijinka"],
        "rear three-quarter waist to tail tip",
        ["배경 동물의 꼬리는 착용자의 꼬리 장식을 충족하지 않는다.", "가려진 연결부는 벨트 부착을 증명하지 않는다."], [
    c("wearable_accessory", "뒤 허리띠에서 시작하는 꼬리",
      "the costume tail root connects visibly to a belt at the rear waist",
      "costume tail root", "connected_to", "rear waist belt"),
    c("wearable_accessory", "하의와 떨어져 곡선을 이루는 꼬리 끝",
      "the tail curves away from the lower garment and ends at a separate visible tip",
      "costume tail", "separated_from", "lower garment"),
], "P0")
profile("CC19", "투명 꼬리의 층과 외부 지지부", "stylized_tail",
        ["S27"], ["허리 지지부와 투명 면이 보이는 여우 꼬리 변형"], ["Ahri", "아리", "여우 꼬리"],
        "rear three-quarter torso with visible support segment",
        ["한 K/DA 변형을 모든 아리 의상에 적용하지 않는다.", "사진만으로 질량·지지 강도·재료 성분을 판단하지 않는다."], [
    c("wearable_accessory", "겹친 투명 꼬리 면",
      "separate transparent tail surfaces overlap while their outer edges remain readable",
      "transparent tail surfaces", "overlap_with_distinct_edges", "other tail surfaces"),
    c("wearable_accessory", "허리 지지부에서 이어지는 꼬리 뿌리",
      "the transparent tail bases extend from a visible external waist support",
      "transparent tail bases", "connected_to", "external waist support"),
], "P0")
profile("CC20", "머리 장식에 속하는 뿔", "fantasy_appendage",
        ["S22", "S28"], ["머리 장식에서 시작하는 한 쌍의 코스튬 뿔"], ["악마", "demon", "horns"],
        "head three-quarter showing horn bases",
        ["뿔 장식과 피부에서 자란 뿔을 구분한다.", "각도 때문에 한쪽이 가려지면 쌍의 관계는 확인되지 않는다."], [
    c("wearable_accessory", "독립된 머리 장식의 뿔 뿌리",
      "paired costume horns emerge from a separate headpiece rather than exposed skin",
      "costume horn bases", "attached_to", "headpiece"),
    c("wearable_accessory", "머리 위로 갈라지는 두 뿔의 끝",
      "two separate horn tips rise above the head with distinct silhouettes",
      "paired horn tips", "distinct_from_each_other", "head silhouette"),
])
profile("CC21", "등 지지부가 보이는 의상 날개", "fantasy_appendage",
        ["S24", "S35"], ["등쪽 하네스에 두 날개가 붙은 의상"], ["천사", "fairy", "wings"],
        "rear full body showing attachment and both spans",
        ["장식 날개는 비행 능력을 뜻하지 않는다.", "배경 날개·후광은 등 부착 날개의 대체 증거가 아니다."], [
    c("wearable_accessory", "하네스에 붙은 양쪽 날개 뿌리",
      "both costume wing roots attach visibly to a harness over the upper back",
      "costume wing roots", "attached_to", "back harness"),
    c("wearable_accessory", "몸통 양옆으로 분리되어 펼쳐진 날개",
      "two wing spans extend to opposite sides without merging with the arms",
      "wing spans", "extend_to_opposite_sides", "wearer torso"),
], basis="source_context_only_original_variant")
profile("CC22", "마스코트 전신 수트와 별도 머리", "mascot_fursuit",
        ["S24", "S35"], ["머리 전체를 덮는 마스코트 머리와 모피 수트"], ["케모미미", "mascot", "fursuit"],
        "front full body and neck seam detail",
        ["귀·꼬리만 더한 의상과 얼굴을 덮는 전신 수트를 구분한다.", "마스코트 외관은 내부 착용자 신원·체형을 특정하지 않는다."], [
    c("costume_style", "착용자 얼굴을 덮는 별도 마스코트 머리",
      "a large costume head encloses the wearer face and ends at a visible neck seam",
      "costume head", "encloses", "wearer face"),
    c("garment_detail", "수트 소매에 이어지는 모피 장갑",
      "faux-fur costume paws join the fur sleeves with distinct cuff boundaries",
      "costume paws", "join", "fur sleeves"),
], basis="source_context_only_original_variant")
profile("CC23", "천으로 만든 인어 꼬리 치마", "fantasy_garment",
        ["S35", "S24"], ["비늘무늬 천의 꼬리 치마와 부채형 밑단"], ["인어", "mermaid"],
        "full lower garment with unobstructed hem",
        ["꼬리 모양 치마와 생물학적 꼬리·별도 수영 핀을 구분한다.", "비늘무늬 인쇄와 실제 비늘 질감을 구분한다."], [
    c("costume_style", "의복 솔기가 남는 꼬리 치마",
      "the fitted textile tail skirt retains a visible garment seam along its side",
      "textile tail skirt", "has_visible_boundary", "side garment seam"),
    c("garment_detail", "치마 밑단에 붙은 부채형 지느러미",
      "a fan-shaped fabric fin is sewn to the lower tail-skirt hem",
      "fabric fin", "attached_to", "tail skirt hem"),
], basis="source_context_only_original_variant")
profile("CC24", "기모노를 인용한 지역 협업 의상", "regional_stage_interpretation",
        ["S13", "S42"], ["겹쳐 여미는 상의와 독립된 오비의 협업 의상"], ["기모노", "kimono", "Anis"],
        "front torso plus side waist view",
        ["지역 협업복·게임 기본복·전통복의 계약을 분리한다.", "작품명을 전통복의 시대·착용법 증거로 쓰지 않는다."], [
    c("garment_detail", "띠 아래로 겹쳐지는 상의 앞섶",
      "two overlapping front panels continue visibly beneath the broad waist sash",
      "front wrap panels", "continue_beneath", "waist sash"),
    c("wearable_accessory", "앞섶과 독립된 넓은 허리 띠",
      "the broad obi-like sash forms a separate band around the outer garment",
      "waist sash", "wraps_around", "outer garment"),
], "P0", "source_context_only_original_variant")
profile("CC25", "한복을 인용한 짧은 무대복 층", "regional_stage_interpretation",
        ["S30", "S43"], ["짧은 저고리풍 상의·겹친 짧은 치마·허리 장식의 무대복"], ["한복", "hanbok", "Rumi"],
        "front full body with waist attachments visible",
        ["전통 치마저고리와 짧은 무대 변형을 별도 유지한다.", "화면 디자인과 제작자의 재해석을 동일 버전으로 처리하지 않는다."], [
    c("costume_style", "짧은 상의 아래의 겹친 무대 치마",
      "the short jacket ends above a separate layered stage skirt",
      "short stage jacket", "ends_above", "layered stage skirt"),
    c("wearable_accessory", "허리에서 각각 시작하는 노리개와 리본",
      "a pendant ornament and ribbons hang from separate visible waist attachments",
      "pendant and ribbons", "suspended_from", "separate waist attachments"),
], "P0")
profile("CC26", "보디스와 구분되는 구조 코르셋", "structural_costume",
        ["S38", "S41", "S33"], ["수직 구조선과 독립된 여밈을 가진 코르셋 층"], ["보디스", "corset", "드레스"],
        "front and back torso details",
        ["보디스는 상의 부분의 이름이며 코르셋과 자동 동의어가 아니다.", "몸의 실제 비율은 코르셋 외형만으로 판정하지 않는다."], [
    c("garment_detail", "상의 겉면의 연속된 수직 구조선",
      "multiple vertical seam channels run continuously along the separate corset garment",
      "corset seam channels", "run_along", "corset garment"),
    c("garment_detail", "코르셋에 속한 끈 여밈",
      "paired lacing rows close the corset back rather than the outer cape",
      "corset lacing", "closes", "corset back"),
], "P0", "source_context_only_original_variant")
profile("CC27", "여러 겹 튤의 튀튀 변형", "ballet_stage",
        ["S44", "S35"], ["허리에서 바깥으로 펼쳐지는 겹친 튤 튀튀"], ["발레", "tutu"],
        "waist and skirt side view",
        ["로맨틱한 긴 튀튀와 수평 원반형 변형을 구분한다.", "겹친 튤이 보여도 숨겨진 후프를 입증하지 않는다."], [
    c("garment_detail", "허리 아래로 반복되는 튤 가장자리",
      "several tulle layers start below the waist and retain distinct outer edges",
      "tulle layers", "extend_from", "skirt waist"),
    c("costume_style", "다리 앞뒤로 펼쳐지는 튀튀의 폭",
      "the selected short tutu spreads outward around the hips rather than hanging to the ankles",
      "short tutu", "spreads_around", "hips"),
], basis="source_context_only_original_variant")
profile("CC28", "할리퀸의 패치와 독립된 가면", "masked_theater",
        ["S45", "S41"], ["조각 무늬 의상과 눈 가면의 할리퀸 변형"], ["광대", "clown", "Harlequin"],
        "front head and full garment",
        ["할리퀸·피에로·제스터를 단일 광대 정의로 합치지 않는다.", "다이아몬드 무늬와 실제 조각천 경계를 구분한다."], [
    c("garment_detail", "의상 면에 반복되는 조각 무늬",
      "contrasting patch-shaped panels repeat across the costume torso and legs",
      "patch panels", "repeat_across", "costume torso and legs"),
    c("wearable_accessory", "눈 주변의 독립된 가면 가장자리",
      "a separate eye mask has a visible border against the face",
      "eye mask", "distinct_from", "face surface"),
], basis="source_context_only_original_variant")
profile("CC29", "피에로를 인용한 넓은 칼라와 폼폼", "theater_archetype",
        ["S35", "S41"], ["넓은 흰 칼라와 앞면 폼폼의 피에로풍 의상"], ["피에로", "Pierrot", "clown"],
        "front head and torso",
        ["백색 의상만으로 피에로를 특정하지 않는다.", "독립 폼폼과 인쇄된 원 무늬를 구분한다."], [
    c("garment_detail", "목 주변의 넓고 부드러운 칼라",
      "a broad soft collar spreads over both shoulders above the loose top",
      "soft collar", "layered_over", "loose top shoulders"),
    c("garment_detail", "앞섶에서 튀어나온 독립 폼폼",
      "separate soft pompons project from the costume front in a vertical row",
      "pompons", "project_from", "costume front"),
], basis="source_context_only_original_variant")
profile("CC30", "카바레 머리 장식의 깃털과 지지대", "cabaret_stage",
        ["S35", "S53"], ["머리 장식 바탕에서 펼쳐지는 깃털"], ["카바레", "showgirl", "carnival"],
        "headpiece base and full feather span",
        ["카니발의 지역별 역사와 카바레 무대복을 구분한다.", "배경 깃털은 착용 머리 장식이 아니다."], [
    c("wearable_accessory", "머리 장식 바탕에 모인 깃털 뿌리",
      "feather stems converge into a visible headdress base above the hair",
      "feather stems", "attached_to", "headdress base"),
    c("wearable_accessory", "머리 양쪽으로 펼쳐지는 장식 깃털",
      "the feather fan spreads above and beside the head without merging into the hair",
      "feather fan", "separated_from", "hair silhouette"),
], basis="source_context_only_original_variant")
profile("CC31", "흡혈귀 드레스의 벨벳과 외부 금색 층", "vampire_character_variant",
        ["S31", "S37"], ["붉은 벨벳 드레스 바깥의 독립 금색 층"], ["흡혈귀", "vampire", "gothic"],
        "front three-quarter torso to skirt",
        ["이 배색은 선택 변형이며 모든 흡혈귀의 정의가 아니다.", "고딕 패션을 자동으로 흡혈귀 코스프레에 넣지 않는다."], [
    c("surface_material", "굽은 천 면에서 달라지는 벨벳 밝기",
      "the dark red pile fabric changes brightness across its folds",
      "pile fabric surface", "varies_across", "fabric folds"),
    c("garment_detail", "드레스 위에 분리되어 놓인 금색 장식층",
      "a gold-colored decorative layer remains separate over the red dress fabric",
      "gold decorative layer", "layered_over", "red dress"),
])
profile("CC32", "마모와 수선이 국소적으로 남은 의상", "costume_state",
        ["S41", "S24"], ["마모된 가장자리와 수선 패치가 남은 코스튬"], ["낡음", "post-apocalyptic", "distressed"],
        "garment edge and repair patch detail",
        ["균일한 회색 필터와 국소 마모 흔적은 다르다.", "소재 마모로 실제 부상·빈곤·폭력 사건을 추론하지 않는다."], [
    c("garment_detail", "의복 가장자리에 국한된 헤짐",
      "fraying is localized along the selected garment edge while the central fabric stays intact",
      "frayed fibers", "localized_on", "garment edge"),
    c("garment_detail", "기존 천 위에 꿰맨 수선 패치",
      "a repair patch overlaps the original cloth with a visible sewn border",
      "repair patch", "layered_over", "original cloth"),
], "P0")
profile("CC33", "가발에서 시작하는 긴 땋은 머리", "wig_structure",
        ["S25", "S30"], ["가발의 묶음에서 시작하는 긴 땋은 머리"], ["Jinx", "Rumi", "long braid"],
        "rear head and full braid length",
        ["가발 실루엣은 모델의 실제 모발·신원을 뜻하지 않는다.", "떠 있는 땋은 머리 장식은 연결된 가발 가닥을 충족하지 않는다."], [
    c("hair_style", "가발 뿌리에서 이어지는 땋은 가닥",
      "the long costume braid starts continuously from the gathered wig at the back of the head",
      "costume braid root", "continuous_with", "gathered wig"),
    c("hair_style", "반복 교차와 독립된 끝 묶음",
      "the braid has repeated crossing sections and a separate tied end",
      "braid crossing sections", "continue_toward", "tied braid end"),
], "P0", "source_context_only_original_variant")
profile("CC34", "자수와 평면 전사 문양의 차", "surface_application",
        ["S30", "S48", "S50"], ["입체 실 자수 옆에 평평한 전사 문양이 있는 의상"], ["문양", "embroidery", "gold motif"],
        "native close-up of both selected surface regions",
        ["금색이면 모두 금속 자수라고 판단하지 않는다.", "아플리케·브레이드·전사·프린트를 같은 표면으로 합치지 않는다."], [
    c("surface_material", "바탕천에서 높이가 드러나는 실 문양",
      "raised thread lines form the embroidered motif above the base fabric",
      "embroidered thread lines", "raised_above", "base fabric"),
    c("surface_material", "바탕천을 따라 평평하게 놓인 전사 문양",
      "the neighboring transfer motif stays flat against the fabric without raised stitches",
      "transfer motif", "flat_against", "base fabric"),
], "P0")
profile("CC35", "의상 패널에 국한된 발광 효과", "costume_lighting",
        ["S22", "S23", "S26"], ["갑옷 패널 안에 국한된 좁은 발광 띠"], ["LED", "glow", "마법"],
        "front armor or prop detail with adjacent unlit region",
        ["전체 화면의 발광 필터는 부착된 발광 띠의 대체 증거가 아니다.", "빛나는 사진은 전원·배선·실제 LED 작동을 입증하지 않는다."], [
    c("garment_detail", "패널 테두리 안쪽의 발광 띠",
      "narrow glowing strips follow selected costume panel edges",
      "glowing strips", "localized_on", "selected panel edges"),
    c("surface_material", "발광부 옆에 남는 비발광 천",
      "the adjacent fabric remains visibly unlit beside the localized costume glow",
      "adjacent fabric", "distinct_from", "glowing costume region"),
], "P0")
profile("CC36", "소품 손잡이와 장갑 손의 접촉", "prop_ownership",
        ["S19", "S25", "S26"], ["장갑 손으로 잡은 입체 소품 손잡이"], ["소품", "bow", "staff", "sword"],
        "hand and grip detail plus full prop silhouette",
        ["손 가까이에 떠 있는 소품은 잡은 상태가 아니다.", "의상 소품의 외형은 실제 무기 기능을 증명하지 않는다."], [
    c("prop", "손잡이를 감싸는 장갑 손가락",
      "gloved fingers curl around the costume prop handle with visible contact",
      "gloved fingers", "in_contact_with", "prop handle"),
    c("prop", "손잡이에서 이어지는 소품 본체",
      "the prop handle continues into one distinct sculpted prop body",
      "prop handle", "continuous_with", "sculpted prop body"),
], "P0")
profile("CC37", "분리형 소매와 손목 장식의 경계", "garment_attachment",
        ["S19", "S20"], ["몸통과 떨어져 있는 소매와 별도 손목 장식"], ["소매", "detached sleeve", "asymmetric outfit"],
        "upper arm and wrist detail",
        ["관절을 관통하는 장식이나 팔과 융합된 소매를 허용하지 않는다.", "소매 테두리와 팔 피부 경계를 구분한다."], [
    c("garment_detail", "팔에서 끝나는 독립 소매 윗단",
      "the detached sleeve ends around the upper arm with a visible fabric boundary",
      "detached sleeve edge", "encircles", "upper arm"),
    c("wearable_accessory", "소매 끝 바깥의 손목 장식",
      "a separate wrist ornament sits beyond the sleeve cuff without replacing it",
      "wrist ornament", "positioned_beyond", "sleeve cuff"),
])
profile("CC38", "겉층이 열리며 드러나는 퀵체인지", "costume_transformation",
        ["S41", "S47"], ["겉 의상이 열리면서 별도 내부 의상이 보이는 순간"], ["퀵체인지", "quick change", "transformation"],
        "full body action plus open seam detail",
        ["한 장의 정지 사진은 변신 과정 전체를 입증하지 않는다.", "합성 분할 화면과 실제 열린 의상 층을 구분한다."], [
    c("action", "잡아 당긴 겉층 가장자리",
      "the wearer holds the opened outer costume edge away from the torso",
      "wearer hand", "in_contact_with", "opened outer costume edge"),
    c("garment_detail", "열린 겉층 안쪽의 독립 의상",
      "a separate inner costume layer is visible through the opened outer garment",
      "inner costume layer", "visible_inside", "opened outer garment"),
], basis="source_context_only_original_variant")
profile("CC39", "회전하는 플리츠 치마의 고정점", "garment_motion",
        ["S30", "S35"], ["허리에 붙은 플리츠 치마가 회전으로 벌어진 순간"], ["회전", "spinning skirt", "pleats"],
        "full skirt including waistband and expanded hem",
        ["번진 색이나 떠 있는 원반은 움직이는 치마를 충족하지 않는다.", "주름과 허리 부착은 모션블러 안에서도 읽혀야 한다."], [
    c("action", "허리에서 바깥으로 펼쳐지는 회전 치마",
      "the rotating skirt flares outward while its waistband stays attached to the wearer",
      "rotating skirt", "anchored_to", "wearer waistband"),
    c("garment_detail", "움직이는 밑단까지 이어지는 플리츠",
      "repeated pleat folds continue from the waist toward the moving hem",
      "pleat folds", "continue_between", "waist and moving hem"),
], basis="source_context_only_original_variant")
profile("CC40", "착용 조형물의 외피와 신체 여유", "wearable_art",
        ["S46", "S53"], ["신체 바깥으로 크게 펼쳐진 착용 조형물"], ["wearable art", "음식 코스튬", "건축 코스튬"],
        "full body showing outer silhouette and wearer opening",
        ["착용 조형물과 배경 조각을 구분한다.", "식물·동물·건축 모티프는 착용자 정체성을 뜻하지 않는다."], [
    c("costume_style", "몸통 주위로 확장된 별도 조형 외피",
      "a sculptural costume envelope extends beyond the wearer torso with visible garment openings",
      "sculptural costume envelope", "surrounds", "wearer torso"),
    c("garment_detail", "외피와 구분되는 착용자의 팔다리",
      "the wearer limbs remain separately readable outside the sculptural costume edges",
      "wearer limbs", "distinct_from", "sculptural costume edges"),
], basis="source_context_only_original_variant")
profile("CC41", "고대 복식을 인용한 드레이프 패널", "ancient_dress_interpretation",
        ["S51"], ["어깨에서 잡고 허리에 묶은 드레이프 천 의상"], ["고대", "chiton", "peplos", "toga"],
        "shoulder closure and full draped panel",
        ["키톤·페플로스·히마티온·토가를 같은 이름으로 치환하지 않는다.", "이 변형은 고대 의복의 정확한 복원이 아니다."], [
    c("costume_style", "어깨의 고정점에서 내려오는 천",
      "draped cloth falls from visible shoulder fastening points into long vertical folds",
      "draped cloth", "suspended_from", "shoulder fastening points"),
    c("wearable_accessory", "드레이프 천을 모으는 허리 끈",
      "a separate waist cord gathers the draped cloth without replacing its shoulder support",
      "waist cord", "gathers", "draped cloth"),
], basis="source_context_only_original_variant")
profile("CC42", "전례복의 외부 패널과 별도 내부층", "ritual_clothing_variant",
        ["S50"], ["긴 내부 옷 위에 입은 전례복 패널과 아플리케"], ["종교복", "priest", "nun", "chasuble"],
        "front torso and overlayer hem",
        ["차수블·코프·달마티카·수도복을 하나의 케이프로 합치지 않는다.", "착용 장면은 개인의 신앙·소속을 증명하지 않는다."], [
    c("costume_style", "긴 내부 옷 위로 놓인 전례복 겉층",
      "a distinct vestment overlayer covers the torso above a separate long inner garment",
      "vestment overlayer", "layered_over", "long inner garment"),
    c("surface_material", "바탕천 위에 붙은 아플리케 경계",
      "shaped fabric appliques have visible attached borders against the vestment ground",
      "fabric appliques", "attached_to", "vestment ground"),
], basis="source_context_only_original_variant")


CASES = []


def case(cid, label, refs, context, works, characters, versions, mode, facts,
         implications, evidence_status, event_date=None, costume_maker=None):
    CASES.append(dict(
        id=cid, label_ko=label, source_refs=refs, context=context,
        franchise_or_work=works, character_labels=characters, version_labels=versions,
        representation_mode=mode, facts=facts, authored_data_implications=implications,
        appearance_evidence_status=evidence_status, event_date=event_date,
        credited_creator_or_performer=costume_maker,
        commonness=dict(status="unknown", denominator=None, observed_wearer_count=None),
        identity_or_body_inference=False,
    ))


case("E01", "FanimeCon: 모바일·온라인 게임 집합", ["S01"], "scheduled_fandom_gathering",
     ["Genshin Impact", "Honkai Impact 3rd", "Honkai Star Rail", "Zenless Zone Zero",
      "GODDESS OF VICTORY: NIKKE", "Blue Archive", "Arknights & Arknights Endfield",
      "Wuthering Waves"], [], [], "version_not_specified",
     ["Named gathering slots are present."],
     ["Prioritize version-aware garment panels, wig roots and prop attachments; do not assign one generic battle outfit to all games."],
     "schedule_confirmed_participation_unmeasured", "2026")
case("E02", "FanimeCon: 대전·슈터·RPG 팬덤", ["S01"], "scheduled_fandom_gathering",
     ["League of Legends", "Overwatch", "Marvel Rivals", "Fire Emblem", "Monster Hunter"],
     [], [], "version_not_specified", ["Named gathering slots are present."],
     ["Maintain separate clothing, armor, helmet and prop recipes."],
     "schedule_confirmed_participation_unmeasured", "2026")
case("E03", "FanimeCon: 소년만화·애니메이션", ["S01"], "scheduled_fandom_gathering",
     ["One Piece", "Dragon Ball", "Jujutsu Kaisen", "Chainsaw Man", "My Hero Academia"],
     [], [], "version_not_specified", ["Named gathering slots are present."],
     ["Separate school clothing, suit panels, robes and character-specific props rather than matching by color alone."],
     "schedule_confirmed_participation_unmeasured", "2026")
case("E04", "FanimeCon: 음악·버추얼 캐릭터", ["S01"], "scheduled_fandom_gathering",
     ["Vocaloid/UTAU", "Project Sekai", "Hololive", "THE iDOLM@STER"], [], [],
     "version_not_specified", ["Named gathering slots are present."],
     ["Store hairstyle construction, stage version and repeated costume trim as independent fields."],
     "schedule_confirmed_participation_unmeasured", "2026")
case("E05", "FanimeCon: 마법소녀·마녀·특촬", ["S01"], "scheduled_fandom_gathering",
     ["Puella Magi Madoka Magica", "Witch Hat Atelier", "Tokusatsu"], [], [],
     "version_not_specified", ["Named gathering slots are present."],
     ["Keep hat, detached sleeve, cape and helmet variants optional until independently specified."],
     "schedule_confirmed_participation_unmeasured", "2026")
case("E06", "WCC 2025: Fire Emblem Engage 미국 팀", ["S03"], "selected_competition_team",
     ["Fire Emblem Engage"], ["Princess", "Prince"], [], "character_recreation",
     ["The organizer labels the American winning team's characters Princess and Prince."],
     ["Do not silently replace the organizer's character labels with the cosplayers' handles."],
     "organizer_result_confirmed", "2025")
case("E07", "WCC 2025: Witch Hat Atelier 프랑스 팀", ["S03"], "selected_competition_team",
     ["Witch Hat Atelier"], ["Coco", "Coco"], [], "character_recreation",
     ["The official result records a Coco/Coco pair."],
     ["A duplicate character label can still represent distinct costume moments or versions; resolve references before authoring."],
     "organizer_result_confirmed", "2025")
case("E08", "WCC 2025: Resident Evil Village 브라질 팀", ["S03"], "selected_competition_team",
     ["Resident Evil Village"], ["Mother Miranda", "Karl Heisenberg"], [], "character_recreation",
     ["Both characters are named in the result."],
     ["Distinguish headpiece/wing, coat and carried-prop ownership in a two-person scene."],
     "organizer_result_confirmed", "2025")
case("E09", "WCC 2025: Godzilla·Gigan 기술 연출", ["S03"], "selected_competition_team",
     ["Godzilla"], ["Godzilla", "Gigan"], [], "full_creature_costume",
     ["The Italian team's entry receives a technology/gimmick award."],
     ["Record creature shells and visible joints separately; an award does not specify a particular motorized mechanism."],
     "organizer_result_confirmed", "2025")
case("E10", "WCC 2025: Elden Ring 조형 제작", ["S03"], "selected_competition_team",
     ["Elden Ring"], ["Promised Consort Radahn", "Tarnished"], [], "character_recreation",
     ["The Indian team's entry receives a construction award."],
     ["Prioritize armor overlap, support/attachment and separate soft joints; exact character morphology still needs a versioned reference."],
     "organizer_result_confirmed", "2025")
case("E11", "Comic-Con 2025: The Wiz와 Bumblebee", ["S04"], "selected_masquerade_entries",
     ["The Wiz", "Transformers"], ["Bumblebee"], [], "mixed_performance_and_character",
     ["These appear in the inspected 2025 winners section."],
     ["Stage ensemble costumes and bulky mechanical shells require different profiles."],
     "organizer_result_confirmed", "2025")
case("E12", "WonderCon·Dragon Con의 장르 폭", ["S05", "S06"], "selected_masquerade_entries",
     ["Sailor Moon", "KPop Demon Hunters", "Transformers", "My Neighbor Totoro"],
     ["Super Sailor Jupiter", "Optimus Prime", "Totoro", "Medusa"], ["Night Sisters original design"],
     "mixed_character_and_original_design", ["The retrieved award excerpts contain this range of entries."],
     ["Do not let a game-only dataset erase original ensembles, mythology or creature suits."],
     "organizer_excerpt_confirmed", "2025")
case("E13", "유럽·미국 대회의 캐릭터 버전과 역사적 재해석", ["S07", "S08"],
     "selected_masquerade_entries", ["Dragon Age: The Veilguard", "Hatsune Miku"],
     ["Neve Gallus", "Lucanis Dellamorte", "Hatsune Miku"], ["Rococo interpretation"],
     "mixed_character_recreation_and_historical_reinterpretation",
     ["The two organizer excerpts supply character and reinterpretation labels."],
     ["Keep canonical character recreation and a Rococo mashup as separate representation modes."],
     "organizer_excerpt_confirmed", "2025")
case("E14", "G-STAR 2025: 실제 현장 기사 사례", ["S09", "S10"], "reporter_selected_convention_scene",
     ["StarCraft", "Helldivers"], ["Zealot"], [], "character_recreation",
     ["The field report names both costume examples."],
     ["Maintain both large creature/armor forms and military-style fabric suits in domestic event research."],
     "reporter_excerpt_confirmed_not_pixel_inspected", "2025-11-15")
case("E15", "C105: 일본 행사에서 선정된 게임·VTuber 사진", ["S11"],
     "reporter_selected_gallery", ["NIKKE", "Genshin Impact", "Zenless Zone Zero", "Blue Archive", "VTuber"],
     [], [], "version_not_specified", ["These categories are named in the selected gallery."],
     ["Cross-context recurrence can guide research priority; gallery selection cannot determine a wearing-frequency ranking."],
     "reporter_excerpt_confirmed_not_pixel_inspected", "2024-12")
case("M01", "에나코: 공식 작품 코스프레와 오리지널 디자인", ["S12"], "licensed_photobook",
     ["To LOVE-Ru", "Dragon Ball", "Ranma 1/2", "One Piece", "My Hero Academia"],
     [], ["Masakazu Katsura original design"], "licensed_and_original_design",
     ["The publisher identifies both licensed works and an original-design contribution."],
     ["Keep licensed character/version metadata separate from original costume recipes."],
     "publisher_text_confirmed", "2019", "Enako")
case("M02", "이오리 모에: 아니스:스타 교토 협업복", ["S13"], "publisher_collaboration_event",
     ["GODDESS OF VICTORY: NIKKE"], ["Anis: Star"], ["Kyo-Yuzen kimono collaboration"],
     "regional_collaboration_reinterpretation", ["The publisher reports the kimono collaboration appearance."],
     ["Traditional textile practice, character identity and collaboration garment are separate axes."],
     "publisher_event_report_confirmed_not_pixel_inspected", "2026", "Iori Moe")
case("M03", "TGS 2022 공식 부스 배역 공지", ["S14"], "publisher_booth_announcement",
     ["GODDESS OF VICTORY: NIKKE"], ["Marian", "Neon"], [], "character_recreation",
     ["The publisher announced performer-to-character assignments."],
     ["Use planned_appearance status rather than silently converting the announcement into confirmed attendance."],
     "planned_appearance_only", "2022", "Iori Moe; Kokoro Shinozaki")
case("M04", "RZCOS C107: 나리땽·시루", ["S15"], "professional_game_booth",
     ["브라운더스트2"], ["에레니르", "빌헬미나"], ["쉐도우바니", "프로즌 퀸"],
     "game_skin_recreation", ["The team names these assignments in its C107 report."],
     ["Store Korean source character spelling, skin label and performer separately; defer unverified English normalization."],
     "creator_event_self_report_not_pixel_inspected", "2025-12-30/2025-12-31", "나리땽; 시루")
case("M05", "RZCOS 광저우: 나리땽·야살", ["S15"], "professional_game_booth",
     ["브라운더스트2"], ["모르페아", "빌헬미나"], ["데이드림 바니", "프로즌 퀸"],
     "game_skin_recreation", ["The team reports a different Nari character/skin and another Wilhelmina performer."],
     ["The same character/skin can have different wearers; model identity must not be embedded into costume semantics."],
     "creator_event_self_report_not_pixel_inspected", "2026-01-01/2026-01-03", "나리땽; 야살")
case("M06", "스파이럴캣츠: LoL 팀 제작 사례", ["S16"], "professional_team_interview",
     ["League of Legends"], ["Ahri", "Riven", "Gnar"], ["Arcade Ahri"],
     "character_recreation_version_partial", ["The interview identifies this project repertoire."],
     ["Character labels alone do not settle a skin, creature-to-human adaptation or exact garment details."],
     "creator_interview_excerpt_not_pixel_inspected", "2016", "Spiral Cats")
case("M07", "AGF 2025 NIKKE 코스프레 런웨이 공지", ["S17"], "publisher_booth_announcement",
     ["GODDESS OF VICTORY: NIKKE"], [], [], "version_not_specified",
     ["The announcement includes a planned cosplay runway."],
     ["Model-event programming is a separate sample from ordinary event attendees."],
     "planned_appearance_only", "2025", None)
case("M08", "Kamui: Yelan의 비대칭 의상", ["S19", "S20"], "maker_portfolio_and_build",
     ["Genshin Impact"], ["Yelan"], ["maker recreation"], "character_recreation",
     ["The maker documents separate asymmetric textile and prop construction."],
     ["Inspect arm covering, front/back panel differences and hand/prop attachment as independent relations."],
     "maker_text_plus_selected_browser_image", "Gamescom 2023 project; 2025 making article", "Kamui Cosplay")
case("M09", "Kamui: Iden Versio의 소품 갑옷", ["S21"], "commissioned_costume_build",
     ["Star Wars Battlefront II"], ["Iden Versio"], ["commission build"], "character_recreation",
     ["The maker distinguishes foam components from the cotton suit."],
     ["Store construction material metadata separately from visible metal-like finish and joint behavior."],
     "maker_text_confirmed_not_pixel_inspected", None, "Kamui Cosplay")
case("M10", "Kamui: Demonic Brigitte의 크로스오버", ["S22", "S23"], "maker_original_crossover",
     ["Overwatch", "Diablo"], ["Brigitte"], ["Demonic crossover"], "crossover_design",
     ["The maker identifies the crossover and separate illuminated prop work."],
     ["Keep base character, crossover designer and visible effect appearance distinct."],
     "maker_text_plus_selected_browser_image", None, "Kamui Cosplay; design credited to Zach Fischer")
case("M11", "Kinpatsu: Arcane Jinx와 LoL 소품 자료", ["S25", "S26"], "maker_tutorial_catalog",
     ["Arcane", "League of Legends"], ["Jinx"], ["Arcane clothing", "League of Legends props"],
     "versioned_character_tutorial", ["Two tutorials cover different version scopes."],
     ["Do not combine tattoo, wig, clothing and prop units from different versions without an explicit mashup request."],
     "maker_catalog_text_confirmed", None, "Kinpatsu Cosplay")
case("M12", "Kinpatsu: K/DA 아리의 투명 꼬리", ["S27", "S28"], "maker_tutorial_catalog",
     ["League of Legends"], ["Ahri"], ["K/DA"], "character_skin_recreation",
     ["The tutorial describes the transparent-tail and attachment approach."],
     ["Tail surface, root support, wig and ears should be selectable components rather than a mandatory anatomy bundle."],
     "maker_catalog_text_confirmed", None, "Kinpatsu Cosplay")
case("M13", "Yaya Han: Rumi의 한복풍 무대 재해석", ["S30", "S43"], "maker_stage_reinterpretation",
     ["KPop Demon Hunters"], ["Rumi"], ["hanbok-inspired stage interpretation"],
     "regional_stage_reinterpretation", ["The maker explicitly labels this a stage interpretation."],
     ["Separate short jacket, layered skirt, waist ornament and surface application contracts."],
     "maker_text_plus_selected_browser_image", None, "Yaya Han")
case("M14", "Yaya Han: 뱀파이어·버니·애니메이션 의상", ["S31", "S32", "S33", "S34"],
     "maker_portfolio", ["Vampire Hunter D: Bloodlust", "Otaku no Video", "Who Framed Roger Rabbit", "Final Fantasy X"],
     ["Carmilla", "Misty May", "Jessica Rabbit", "Lulu"], [], "multiple_character_recreations",
     ["The maker records distinct fabrics and layered construction choices."],
     ["Repertoire includes gowns, bodysuits, internal structure and belt-heavy clothing; do not reduce model cosplay to one silhouette."],
     "maker_text_excerpts_not_pixel_inspected", None, "Yaya Han")
case("A01", "WOW: 착용 조형물과 변형 의상", ["S46", "S47"], "wearable_art_competition",
     ["The Autumn King", "Hidden Layers"], [], [], "wearable_sculpture_and_transformation",
     ["The organizer describes sculptural and transforming designs."],
     ["Maintain wearable-art and transformation axes even when no franchise/character metadata exists."],
     "organizer_design_text_confirmed", "2022; 2025")


REUSE = [
    ("hw_lateral_pannier", "reuse", ["S39"], "좌우 폭을 만드는 파니에 관계를 재사용"),
    ("hw_shelf_bustle", "reuse", ["S40"], "뒤쪽 돌출 볼륨을 만드는 버슬 관계를 재사용"),
    ("hw_francaise_free_back", "reuse", [], "기존 역사복식의 자유롭게 내려오는 등 주름 관계를 재사용"),
    ("hw_anglaise_fitted_back", "reuse", [], "기존 역사복식의 몸에 맞는 등 구성 관계를 재사용"),
    ("hw_kosode_small_opening", "reuse", ["S42"], "기모노 계열 전체를 좁은 소매 트임 프로필로 대체하지 않음"),
    ("qipao_standing_collar_diagonal_closure_system", "reuse", ["S49"], "칼라·대각 여밈 관계를 재사용"),
    ("kebaya_front_open_blouse_sarong_system", "reuse", ["S48"], "앞이 열리는 블라우스와 별도 사롱 관계를 재사용"),
    ("nivi_sari_continuous_pleat_pallu_system", "reuse", [], "사리의 특정 드레이프 변형은 기존 계약을 보존; 이번에 외부 근거 재검토하지 않음"),
    ("clinical_nursing_duty_system", "scope_exclusion", ["S36"], "간호복 코스튬만으로 임상 임무를 활성화하지 않음"),
    ("police_public_safety_duty_system", "scope_exclusion", ["S36"], "경찰복 코스튬만으로 실제 공공안전 임무를 활성화하지 않음"),
    ("military_uniform_duty_system", "scope_exclusion", ["S36"], "장식 군복만으로 실제 군사 임무를 활성화하지 않음"),
    ("wearable_protective_armor_system", "scope_exclusion", ["S21", "S24"], "소품 갑옷만으로 실제 보호 성능 계약을 활성화하지 않음"),
]


ALIGNMENT = []


def align(aid, group, terms, refs, profiles, existing, state, gap):
    ALIGNMENT.append(dict(
        id=aid, seed_keyword_group=group, seed_terms=terms,
        source_refs=refs, proposed_profile_refs=profiles,
        existing_candidate_or_profile_ids=existing,
        coverage_status=state, remaining_gap=gap,
        coverage_meaning="research topic alignment; not runtime routing or pixel qualification",
    ))


align("K01", "접객·서비스", ["메이드", "집사", "호텔 벨보이", "객실 승무원", "다이너 종업원", "안내원"],
      ["S36", "S41"], ["CC01", "CC02"],
      ["akihabara_maid_cafe_uniform", "anime_butler_uniform", "hotelier_concierge_uniform", "flight_attendant_uniform_costume"],
      "existing_plus_specific_proposals", "벨보이·다이너·승무원은 시대·브랜드별 구조를 별도로 조사해야 함")
align("K02", "작업·전문직", ["요리사", "정비사", "연구원", "의료인", "정원사", "공예가"],
      ["S36", "S21"], ["CC06", "CC07"],
      ["chef_uniform_costume", "medical_lab_coat_costume", "nurse_uniform_costume"],
      "existing_plus_specific_proposals", "기능성 의복과 역할 코스튬 사이의 활성화 회귀 검증 필요")
align("K03", "군복·공공 제복", ["해군", "비행사", "장교", "의장대", "소방관", "구조대"],
      ["S36"], ["CC05", "CC06"],
      ["naval_sailor_uniform_costume", "military_dress_uniform_costume", "firefighter_uniform_costume"],
      "existing_plus_specific_proposals", "실제 국가·부대·계급·방호 규격은 현재 근거에서 지정하지 않음")
align("K04", "학교·학술", ["세일러형 교복", "블레이저 교복", "기숙학교", "대학 가운", "학자", "서기관"],
      ["S36"], ["CC03", "CC04", "CC12"],
      ["seifuku_sailor_uniform_cosplay", "gakuran_uniform_cosplay", "adult_school_uniform_cosplay_costume"],
      "existing_plus_specific_proposals", "학술 가운의 국가·학교별 후드와 학위 장식은 별도 조사 필요")
align("K05", "스포츠·팀 활동", ["펜싱", "승마", "모터레이싱", "피겨스케이팅", "치어리딩", "무술", "마칭밴드"],
      ["S36", "S35"], ["CC09"], [],
      "broad_source_context_no_new_specific_profile", "각 종목의 장비·움직임·팀 표식은 전문 구조 근거 확보 후 추가")
align("K06", "고대·중세", ["키톤", "토가", "튜닉", "중세 여행자", "상인", "기사"],
      ["S51"], ["CC41", "CC13"], ["knight_armor_cloak_costume"],
      "partial_source_specific_proposal", "키톤·페플로스·히마티온 구분 확보; 토가와 중세 남성복은 좁은 변형 조사 필요")
align("K07", "근세·근대", ["르네상스", "바로크", "로코코", "엠파이어", "빅토리아"],
      ["S39", "S40", "S41"], ["CC26"],
      ["hw_francaise_free_back", "hw_anglaise_fitted_back", "hw_lateral_pannier", "hw_shelf_bustle"],
      "reuse_existing_specific_profiles", "후보팩에서 역사적 실루엣을 캐릭터 해석 축과 함께 묶는 회귀 검증 필요")
align("K08", "지역 전통복식", ["한복", "도포", "당의", "기모노", "한푸", "치파오", "사리", "아오자이", "케바야", "카프탄", "킬트"],
      ["S42", "S43", "S48", "S49", "S52"], ["CC24", "CC25"],
      ["hw_dangui_open_sides", "hw_kosode_small_opening", "qipao_standing_collar_diagonal_closure_system",
       "kebaya_front_open_blouse_sarong_system", "nivi_sari_continuous_pleat_pallu_system"],
      "existing_and_stage_variants_separated", "한푸·도포·아오자이·킬트의 시대/지역별 변형 및 카프탄 완전 착용 구조는 추가 조사")
align("K09", "왕실·신분·의전", ["궁중복", "대관식 복식", "귀족 예복", "관복", "의장복"],
      ["S52", "S36"], ["CC05"],
      ["royal_guard_regalia_uniform"], "existing_with_limited_source_context",
      "왕관·흉배·휘장의 상징과 신분을 한 가지 보편 정의로 만들지 않음")
align("K10", "종교·통과의례", ["성직자 복식", "수도복", "승복", "혼례복", "상복", "졸업 예복"],
      ["S50"], ["CC42"], [], "partial_source_specific_proposal",
      "차수블 사례 확보; 승복·혼례·상복은 종교/지역/시대마다 추가 근거 필요")
align("K11", "근현대 레트로", ["플래퍼", "로커빌리", "모드", "디스코", "빈티지 운동복"],
      ["S35", "S36"], [], ["hw_drop_waist_1920", "hw_cloche_bell"],
      "reuse_existing_and_backlog", "플래퍼 외의 변형은 시대복식 조사와 별도 연결")
align("K12", "작품·캐릭터 재현", ["영화", "만화", "게임", "슈퍼히어로", "마법소녀", "특촬 히어로"],
      ["S01", "S03", "S04", "S12", "S15", "S19", "S25"], ["CC08", "CC10", "CC14", "CC15", "CC16", "CC33", "CC36"],
      ["anime_hero_battle_suit", "tokusatsu_hero_suit", "vtuber_avatar_cosplay"],
      "versioned_case_research_and_proposals", "캐릭터별 공식 설정화와 각 의상 버전의 부품 매핑은 아직 완성되지 않음")
align("K13", "판타지 직업", ["마법사", "마녀", "기사", "성기사", "레인저", "연금술사", "음유시인"],
      ["S29", "S35", "S41"], ["CC11", "CC12", "CC13"],
      ["fantasy_costume_staff", "knight_armor_cloak_costume"],
      "source_informed_original_variants", "직업명만으로 모자·갑옷·악기를 필수화하지 않음")
align("K14", "신화·초자연적 존재", ["천사", "악마", "요정", "엘프", "인어", "정령"],
      ["S22", "S28", "S35"], ["CC20", "CC21", "CC23"],
      ["angel_halo_wings_tail_set", "mermaid_scale_shell_prop"],
      "authored_appendage_and_garment_variants", "후광·엘프 귀는 좁은 부착 구조의 추가 자료 확보 필요")
align("K15", "모험·장르", ["해적", "카우보이", "탐험가", "비행 모험가", "느와르 탐정"],
      ["S35", "S36"], ["CC02", "CC06"], [],
      "broad_source_context_no_new_specific_profile", "삼각모·홀스터·코트의 장르별 조합은 후보 소재로만 남김")
align("K16", "호러·기괴함", ["흡혈귀", "유령", "좀비", "미라", "저주받은 인형", "허수아비", "기괴한 광대"],
      ["S31", "S37", "S41"], ["CC28", "CC29", "CC31", "CC32"], [],
      "partial_variants_with_state_axis", "붕대·인형 분절·특수분장의 정확한 부착은 별도 자료 필요")
align("K17", "SF·미래", ["우주비행사", "안드로이드", "사이보그", "외계인", "우주 정비사"],
      ["S21", "S04", "S24"], ["CC06", "CC13", "CC15", "CC16"], [],
      "authored_shell_and_joint_variants", "생명 유지·기계 작동·신체 개조는 외형만으로 추론하지 않음")
align("K18", "포스트아포칼립스", ["생존자", "폐품 수집가"], ["S41", "S24"], ["CC32"], [],
      "specific_state_proposal", "폐품 소품의 실제 작동이나 손상 사건은 별도 요청 근거 필요")
align("K19", "공연·무대", ["발레", "플라멩코", "볼룸댄스", "아이돌", "록", "오페라"],
      ["S35", "S44", "S30"], ["CC09", "CC25", "CC27", "CC39"], [],
      "partial_specific_stage_variants", "플라멩코와 볼룸 의상의 움직임/자락 구조는 별도 전문 근거 필요")
align("K20", "카바레·서커스·가면극", ["쇼걸", "카바레", "벌레스크", "드래그", "링마스터", "곡예사", "제스터", "피에로", "할리퀸"],
      ["S35", "S45", "S53"], ["CC28", "CC29", "CC30"], [],
      "partial_source_and_authored_variants", "공연 역할·미학으로 분류; 의상에서 젠더 정체성이나 성적 장면을 추론하지 않음")
align("K21", "축제·시즌", ["가면무도회", "카니발", "할로윈", "산타", "호두까기 인형", "사계절"],
      ["S35", "S53"], ["CC28", "CC30", "CC40"],
      ["covered_santa_fur_trim_costume"], "existing_and_context_proposals",
      "카니발 지역별 역사·산타 변형은 유지; 축제명으로 한 의상을 필수화하지 않음")
align("K22", "동물·생물", ["귀", "꼬리", "퍼슈트", "마스코트", "곤충", "괴수"],
      ["S28", "S03", "S04"], ["CC16", "CC17", "CC18", "CC19", "CC22"],
      ["nekomimi_cat_ear_costume", "original_family_friendly_fursuit_build", "original_public_mascot_suit_build"],
      "attachment_and_representation_modes_separated", "곤충 더듬이·다지 구조는 개별 외형 근거 필요")
align("K23", "추상·오브젝트", ["카드", "체스", "음식", "꽃", "구름", "시계", "거울", "건축", "웨어러블 아트"],
      ["S46", "S47", "S53"], ["CC38", "CC40"], [],
      "wearable_sculpture_proposal", "각 사물의 상징 도상은 자동 주입하지 않음")
align("K24", "독립 미학", ["고딕", "로리타 패션", "펑크", "록", "비주얼계", "스팀펑크", "사이버", "테크니컬"],
      ["S37", "S35"], ["CC31", "CC16"],
      ["gothic_lolita_dress", "complete_lolita_fashion_coordinate"],
      "style_axis_kept_independent", "로리타 패션은 독립 패션 좌표이며 코스프레/성적 문맥의 동의어가 아님")
align("K25", "표면·실루엣 미학", ["핀업", "란제리 영감", "페티시 소재", "아방가르드", "초현실", "캠프", "키치"],
      ["S38", "S33", "S46"], ["CC26", "CC40"], [],
      "construction_and_aesthetic_separated", "광택·코르셋·노출로 성적 활동을 자동 추론하지 않음")
align("K26", "실루엣·길이", ["피티드", "스트레이트", "A라인", "벨", "아워글라스", "코쿤", "역삼각", "비대칭", "조형적", "크롭", "미니", "미디", "바닥 길이", "하이로우", "트레인"],
      ["S39", "S40", "S46", "S19"], ["CC02", "CC10", "CC25", "CC27", "CC40"],
      ["hw_lateral_pannier", "hw_shelf_bustle"], "observable_directional_relations",
      "소재 내부 지지 구조와 외곽 실루엣은 따로 기록")
align("K27", "몸통·칼라·소매", ["보디스", "조끼", "코르셋", "흉갑", "패널", "요크", "스탠드 칼라", "세일러 칼라", "러프", "견장", "퍼프", "벨 슬리브", "비숍", "지고", "분리 소매", "커프"],
      ["S36", "S41", "S19"], ["CC02", "CC03", "CC04", "CC05", "CC13", "CC26", "CC37"], [],
      "relation_specific_proposals", "러프·지고·비숍 소매는 기존 구조 검토 후 좁은 변형 추가")
align("K28", "치마·겉층", ["플리츠", "티어드", "오버스커트", "앞치마", "큐롯", "브리치스", "드레이프", "케이프", "클로크", "로브", "후드", "코트", "숄", "볼레로"],
      ["S41", "S30", "S51"], ["CC01", "CC12", "CC25", "CC38", "CC39", "CC41"], [],
      "layer_and_owner_specific_proposals", "케이프·클로크·로브의 여밈/소매 차이는 단어 수준으로 통합하지 않음")
align("K29", "머리·손발 장식", ["크라운", "티아라", "보닛", "베일", "캡", "삼각모", "가면", "바이저", "가발", "장갑", "건틀릿", "커프", "타이츠", "스타킹", "게이터", "부츠", "플랫폼"],
      ["S21", "S25", "S28", "S29"], ["CC07", "CC11", "CC15", "CC17", "CC20", "CC28", "CC30", "CC33", "CC36"], [],
      "selected_attachments_and_wig_contracts", "왕관·베일·부츠의 시대/버전별 구조는 기존 후보와 추가 연결 필요")
align("K30", "소품과 표식", ["배지", "문장", "열쇠", "책", "약병", "벨트", "지팡이", "가방"],
      ["S19", "S25", "S26"], ["CC05", "CC12", "CC36"], ["fantasy_costume_staff", "cosplay_prop_katana", "cosplay_prop_broadsword"],
      "ownership_and_contact_proposals", "상징물의 실제 소속·권한·효능은 외형에서 추론하지 않음")
align("K31", "형태 지지 용어", ["엠파이어 라인", "크리놀린", "파니에", "버슬", "프로그 장식", "파스망트리"],
      ["S39", "S40", "S41", "S49"], ["CC05", "CC26"],
      ["hw_empire_raised_waist", "hw_lateral_pannier", "hw_shelf_bustle"],
      "existing_narrow_variants_reused", "크리놀린과 파니에의 지지체, 장식 끈과 여밈 끈을 분리")
align("K32", "표면 재료", ["튤", "오간자", "쉬폰", "메시", "레이스", "새틴", "에나멜", "라텍스", "메탈릭 직물", "시퀸", "거울", "벨벳", "인조 모피", "깃털"],
      ["S20", "S27", "S31", "S38", "S44"], ["CC13", "CC17", "CC19", "CC27", "CC30", "CC31"], [],
      "appearance_separated_from_composition", "정확한 재료 성분은 사진만으로 확정하지 않음")
align("K33", "장식·제작", ["자수", "비즈", "진주", "아플리케", "브레이드", "파이핑", "스모킹", "수지", "몰딩", "3D 프린트", "종이", "프레임", "목재", "재활용 플라스틱", "기계 부품", "공기 주입"],
      ["S24", "S30", "S50", "S46"], ["CC05", "CC34", "CC36", "CC40"], [],
      "selected_surface_and_making_proposals", "몰딩·프린트·기계 부품의 실제 제작 이력은 메타데이터로만 보존")
align("K34", "상태·동작", ["마모", "주름", "패치", "수선", "젖음", "먼지", "그을림", "휘장 제거", "회전", "프린지 흔들림", "접히는 날개", "탈착", "리버서블", "퀵체인지"],
      ["S41", "S47", "S30"], ["CC32", "CC38", "CC39"], ["constructing_and_repairing_original_cosplay"],
      "state_and_transformation_proposals", "젖음·그을림·날개 구동은 개별 상태 근거 필요; 정지 사진은 전 과정 증거가 아님")
align("K35", "재현 방식", ["충실한 재현", "현대적 재해석", "부분적 힌트", "매시업", "의인화", "추상화"],
      ["S12", "S13", "S22", "S30", "S46"], [], [],
      "representation_metadata_proposal", "작품·캐릭터·버전·재현 방식을 독립 필드로 유지")


BUNDLE_ROWS = [
    ("B01", "가슴판 앞치마 메이드", ["CC01"], ["frill_apron_maid_costume"],
     "apron straps join the bib and waistband over the separate dress",
     "front three-quarter torso through skirt hem"),
    ("B02", "테일코트 집사", ["CC02"], ["anime_butler_uniform"],
     "the inner waistcoat remains inside the short-front long-back coat",
     "front and side full body"),
    ("B03", "세일러 칼라 교복 코스튬", ["CC03"], ["seifuku_sailor_uniform_cosplay"],
     "the ribbon sits below the same wearers sailor collar",
     "front and shoulder three-quarter view"),
    ("B04", "견장·브레이드 판타지 정복", ["CC05"], ["military_dress_uniform_costume"],
     "epaulettes and both cord endpoints belong to the same decorative jacket",
     "front upper body with both shoulders"),
    ("B05", "분리 소매 마법소녀 무대복", ["CC08"], ["magical_girl_stage_costume"],
     "the sleeves remain detached above the bodice and layered short skirt",
     "front full body with upper arm gaps"),
    ("B06", "비대칭 캐릭터 의상과 잡은 소품", ["CC10", "CC36"], [],
     "the asymmetrically dressed wearer grips their own sculpted prop",
     "full body plus native hand detail"),
    ("B07", "마녀 모자와 열린 로브", ["CC11", "CC12"], [],
     "the attached hat crown sits above the wearer whose open robe exposes the inner layer",
     "head to knees and hat tip"),
    ("B08", "소품 갑옷·헬멧·천 관절", ["CC13", "CC15"], ["rpg_armor_costume_set"],
     "helmet edges and overlapping panels remain distinct from fabric neck and joint coverings",
     "full body plus neck and bent-joint details"),
    ("B09", "천 슈트 위의 특촬 패널", ["CC14"], ["tokusatsu_hero_suit"],
     "the chest panel and glove cuffs sit over the same fabric suit",
     "front full body with wrists"),
    ("B10", "큰 로봇 외피와 내부 천 관절", ["CC16"], [],
     "the mechanical-looking shells remain wearable outer pieces separated by visible cloth",
     "full body with open joint regions"),
    ("B11", "머리띠 귀와 벨트 꼬리", ["CC17", "CC18"], ["nekomimi_cat_ear_costume"],
     "the ears attach to the head band and the separate tail attaches to the same wearers belt",
     "rear three-quarter full body with ear bases and tail root"),
    ("B12", "투명 꼬리와 의상 귀", ["CC19", "CC17"], [],
     "transparent tail planes extend from the waist support below head-band ears",
     "rear three-quarter full body with exposed support"),
    ("B13", "지지부가 보이는 장식 날개", ["CC21"], [],
     "both wings extend from the same upper-back harness",
     "rear full body with wing roots"),
    ("B14", "마스코트 전신 수트", ["CC22"], ["original_public_mascot_suit_build"],
     "the separate oversized head and costume paws connect to the enclosing suit",
     "front full body and neck boundary"),
    ("B15", "지역 협업 기모노풍 의상", ["CC24"], [],
     "the wrapped front panels continue beneath a separate broad waist band",
     "front and side torso"),
    ("B16", "한복풍 무대복과 표면 장식", ["CC25", "CC34"], [],
     "the short stage jacket sits above the skirt and owns the selected raised and flat motifs",
     "front full body plus native surface details"),
    ("B17", "독립된 구조 코르셋 층", ["CC26"], [],
     "the vertical channels and back lacing belong to the corset rather than the outer garment",
     "front and back torso details"),
    ("B18", "겹친 튤의 짧은 튀튀", ["CC27"], [],
     "the distinct tulle layer edges radiate from the same waist",
     "waist and skirt side view"),
    ("B19", "할리퀸풍 패치와 눈 가면", ["CC28"], [],
     "the patch panels belong to the garment while the mask stays a separate facial object",
     "front head and full garment"),
    ("B20", "벨벳·금색 층의 흡혈귀 변형", ["CC31"], [],
     "the gold outer decoration remains separate above the folded red pile fabric",
     "front three-quarter torso to skirt"),
    ("B21", "헤짐과 수선 흔적 의상", ["CC32"], [],
     "localized fraying and the sewn patch occupy specified parts of the same garment",
     "native garment detail"),
    ("B22", "연결된 가발 땋은 머리와 소품 접촉", ["CC33", "CC36"], [],
     "the same wearers braid joins the wig and their gloved hand grips the prop",
     "rear three-quarter full body plus native hand crop of the same frame"),
    ("B23", "천 관절 갑옷의 국소 발광", ["CC13", "CC35"], [],
     "glowing panel edges remain separate from the unlit fabric joints",
     "full body plus lit-edge and joint details"),
    ("B24", "퀵체인지가 드러나는 한 순간", ["CC38"], [],
     "the held outer edge opens onto a distinct inner garment in one frame",
     "full body with hand and opening visible"),
    ("B25", "신체 외곽의 착용 조형물", ["CC40"], [],
     "the sculptural envelope surrounds the torso while the limbs remain readable",
     "full body including the whole envelope"),
    ("B26", "고대복을 인용한 드레이프 변형", ["CC41"], [],
     "shoulder fasteners support the cloth while the separate cord gathers the waist",
     "shoulder detail and full garment"),
    ("B27", "전례복 겉층과 아플리케", ["CC42"], [],
     "attached appliques belong to the outer vestment above the separate inner garment",
     "front torso and overlayer hem"),
]


CONTEXT_CANDIDATES = [
    ("capture_context", "ccx_convention_floor_portrait", "행사장 전신 의상 사진",
     "a full-body costume portrait with a convention hall visible behind the wearer",
     "scene frame", "contains", "wearer and convention hall", ["S01", "S10"]),
    ("capture_context", "ccx_studio_costume_catalog", "스튜디오 의상 구조 기록",
     "a studio costume photograph with the full garment silhouette unobstructed",
     "scene frame", "contains", "unobstructed garment silhouette", ["S12", "S18"]),
    ("capture_context", "ccx_two_wearer_stage_scene", "두 착용자의 무대 의상 장면",
     "two costume wearers remain separately readable on one performance stage",
     "scene frame", "contains", "two distinct costume wearers", ["S03", "S35"]),
    ("location", "ccx_costume_fitting_corner", "입은 상태로 수선하는 의상 작업 구역",
     "a costume fitting corner has a mirror and a repair work surface beside the wearer",
     "fitting corner", "contains", "mirror and work surface", ["S24", "S41"]),
    ("action", "ccx_repair_detached_cuff", "착용한 분리 소매의 커프 수선",
     "the maker hand holds the detached cuff edge while adjusting its visible attachment",
     "maker hand", "in_contact_with", "detached cuff attachment", ["S24", "S28"]),
    ("prop", "ccx_loose_ear_tail_components", "분리된 귀·꼬리 의상 부품",
     "separate costume ear and tail pieces rest on the workbench before attachment",
     "costume ear and tail pieces", "rest_on", "workbench", ["S28"]),
    ("garment_detail", "ccx_waist_apron_variant", "가슴판 없는 허리 앞치마",
     "a waist-only apron starts at the belt with no chest bib or shoulder straps",
     "waist apron", "starts_at", "waist belt", ["S36"]),
]


FIXTURES = [
    ("T01", "간호사 코스튬 촬영", [], ["clinical_nursing_duty_system"], "clothing name does not supply clinical duty"),
    ("T02", "경찰복 코스튬 스튜디오 사진", [], ["police_public_safety_duty_system"], "costume is not operational policing"),
    ("T03", "금속처럼 칠한 EVA 소품 갑옷", [], ["wearable_protective_armor_system"], "finish is not protective performance"),
    ("T04", "마녀 코스프레", [], ["CC11"], "family term does not select a hat variant"),
    ("T05", "가슴판과 어깨끈이 있는 앞치마가 드레스 바깥에 묶임", ["CC01"], [], "explicit topology supports the proposed apron contract"),
    ("T06", "가슴판 없는 허리 앞치마", [], ["CC01"], "waist apron must not become bib apron"),
    ("T07", "Yelan 코스프레", [], ["CC10"], "unresolved character/version name alone is insufficient for a hard narrow contract"),
    ("T08", "한 팔은 긴 천 소매, 다른 팔은 별도 커프이며 좌우 치마 패널 길이가 다름", ["CC10"], [], "explicit asymmetric component relations"),
    ("T09", "아리 코스프레", [], ["CC19"], "a character label does not force the transparent-tail version"),
    ("T10", "투명 꼬리의 뿌리가 노출된 외부 허리 지지부에 연결됨", ["CC19"], [], "explicit support and surface variant"),
    ("T11", "고딕 로리타 패션 코디", [], ["CC31"], "independent fashion coordinate is not vampire cosplay"),
    ("T12", "한복", [], ["CC25"], "traditional family label does not select cropped stagewear"),
    ("T13", "짧은 저고리풍 상의 아래 겹친 무대 치마와 독립 허리 장식", ["CC25"], [], "explicit stage interpretation"),
    ("T14", "커다란 치마", [], ["hw_lateral_pannier", "hw_shelf_bustle"], "generic volume does not select its directional support"),
    ("T15", "뒤쪽으로만 돌출된 버슬 변형", ["hw_shelf_bustle"], ["hw_lateral_pannier"], "posterior versus lateral volume"),
    ("T16", "후보팩 B11을 검색 결과로 얻음; 사용자 요청은 평범한 재킷", [], ["CC17", "CC18"], "retrieval alone supplies no hard appendage obligations"),
    ("T17", "A의 머리띠 귀와 B의 벨트 꼬리", [], ["B11_same_owner_contract"], "different owners cannot satisfy one-wearer bundle"),
    ("T18", "갑옷 패널 가장자리만 발광하며 관절 천은 비발광", ["CC35"], [], "localized appearance without electrical-function claim"),
    ("T19", "전체 화면의 노란 빛 필터", [], ["CC35"], "global grading is not an attached costume glow strip"),
    ("T20", "겉층을 손으로 벌려 독립 내부층이 보이는 한 순간", ["CC38"], [], "a visible opening does not prove the complete change sequence"),
    ("T21", "기모노", [], ["hw_kosode_small_opening", "CC24"], "broad family does not establish a historical opening or collaboration variant"),
    ("T22", "코르셋 후보만 선택됨; 요청에는 구조 상의가 없음", [], ["CC26"], "candidate selection cannot supply independent request evidence"),
    ("T23", "Arcane Jinx 의상과 LoL Jinx 소품을 하나의 공식 버전으로 자동 합침",
     [], ["canonical_version_merge"], "version scopes need explicit alignment or mashup intent"),
    ("T24", "옆 인물의 소품이 주인공 손 근처에 있음", [], ["CC36"], "proximity is not contact or ownership"),
]


RENDER_ARMS = [
    ("RN01", "가슴판 앞치마", ["CC01"], "성인 착용자: 두 어깨끈이 가슴판에 이어지고, 드레스 바깥 허리띠가 옆 매듭까지 이어지며, 앞치마 밑단이 드레스 밑단보다 위에서 끝남; 앞쪽 3/4 구도",
     "apron strap-to-bib continuity, waistband owner, separate lower hems"),
    ("RN02", "비대칭 의상과 소품", ["CC10", "CC36"], "성인 착용자: 한 팔의 긴 소매와 다른 팔의 별도 커프, 길이가 다른 치마 패널, 몸통 위의 독립된 밝은 모피 칼라, 장갑 손가락이 연속된 소품 손잡이를 감쌈; 전신 사진",
     "asymmetric arm/skirt relations and exact fingers-to-handle contact"),
    ("RN03", "소품 갑옷의 관절", ["CC13", "CC15"], "성인 착용자: 금속처럼 칠한 패널은 구부린 관절 앞에서 겹침을 끝내고 관절 천은 무광으로 노출됨; 헬멧 아래 목 천과 쉘 안쪽의 독립 바이저 가장자리가 보임",
     "panel/fabric boundaries, visible bend clearance and separate neck covering"),
    ("RN04", "귀와 꼬리의 부착", ["CC17", "CC18"], "성인 착용자: 안쪽 대비 패널을 가진 모피 귀의 바탕이 머리띠에 붙고 꼬리 뿌리는 뒤 허리 벨트에 연결됨; 꼬리는 하의와 떨어져 휘며 독립된 끝까지 보임; 뒤쪽 3/4 전신 사진",
     "same-wearer ownership, exposed ear bases and tail root"),
    ("RN05", "한복풍 무대 변형", ["CC25"], "성인 착용자의 짧은 저고리풍 상의, 별도 겹친 무대 치마, 허리에 따로 붙은 노리개와 리본",
     "jacket/skirt separation and pendant/ribbon attachment ownership"),
    ("RN06", "퀵체인지 순간", ["CC38"], "성인 착용자가 겉 의상 가장자리를 손으로 벌려 내부 의상이 드러나는 한 순간",
     "hand/edge contact and distinct inner/outer layers"),
    ("RN07", "자수와 전사의 근접 비교", ["CC34"], "의상의 같은 구역에서 높이가 있는 실 문양과 평평한 전사 문양을 함께 기록한 근접 사진",
     "raised stitches versus flat neighboring transfer"),
    ("RN08", "착용 조형물", ["CC40"], "성인 착용자: 몸통 바깥으로 확장된 조형 외피에 착용 개구부가 보이고, 외피 가장자리 밖 팔다리가 별도로 읽힘; 외피 전체를 포함한 전신 사진",
     "wearable envelope versus background sculpture and readable wearer openings"),
]


REFERENCE_OBSERVATIONS = [
    {
        "id": "IMG01", "source_id": "S19",
        "published_image_url": "https://assets.kamuicosplay.com/wp-content/uploads/2023/12/Yelan-Front-Back-Genshin-Impact-by-Kamui-Cosplay.jpg",
        "view": "front/back composite, displayed scaled in browser",
        "visible_observations_ko": [
            "양팔의 천 덮개와 커프 구성이 서로 다르게 보임",
            "밝은 모피 외부층과 어두운 의상 패널이 구분됨",
            "활 소품과 착용자의 손이 함께 보임",
        ],
        "not_established": ["exact native finger contact", "hidden supports", "chemical fabric composition"],
        "relation_lessons": ["arm asymmetry", "outer-layer ownership", "prop contact needs native review"],
    },
    {
        "id": "IMG02", "source_id": "S22",
        "published_image_url": "https://assets.kamuicosplay.com/wp-content/uploads/2022/02/03_Demonic_Brigitte_Cosplay_Kamui_Cosplay-714x1024.jpg",
        "view": "published full costume photograph, displayed scaled in browser",
        "visible_observations_ko": [
            "큰 갑옷 패널 사이에 어두운 내부층이 남아 있음",
            "일부 갑옷·소품 영역에 밝은 발광 외관이 보임",
            "머리의 뿔과 손에 든 소품이 별도 구성으로 읽힘",
        ],
        "not_established": ["real metal protection", "hidden wiring or mechanics", "physical fire", "all effects produced in camera"],
        "relation_lessons": ["shell versus joint layer", "localized glow versus background effects", "made appendages"],
    },
    {
        "id": "IMG03", "source_id": "S30",
        "published_gallery_url": "https://www.yayahan.com/Portfolio/rumi?pgid=jt5kqp02-eef180_80ab795c4d3b45429ddba9add6d39229mv2.jpg",
        "published_gallery_caption": "huntrx holmat fxdandy9.JPG",
        "view": "selected three-person stage costume photograph in browser lightbox",
        "visible_observations_ko": [
            "보라색 계열의 짧은 상의와 별도의 짧은 겹친 치마가 보임",
            "허리의 늘어진 장식과 땋은 가발 형태가 의상 층과 구분됨",
            "세 착용자의 배색은 다르지만 무대복 조합의 관계를 비교할 수 있음",
        ],
        "not_established": ["hidden boning or batteries", "identity from appearance", "traditional historical hanbok accuracy"],
        "relation_lessons": ["stage interpretation separate from traditional family", "same-frame wearer ownership"],
    },
]


def main():
    seed = json.loads((HERE / "source-conversation.json").read_text())
    seed.pop("source_text_sha256_pending", None)
    seed["assistant_keyword_overview_sha256"] = sha256(seed["assistant_keyword_overview"].encode()).hexdigest()
    write("source-conversation.json", seed)
    protected = [
        ROOT / "skills/photo-prompt-image-generator/scripts/prompt_generator.py",
        ROOT / "tests/test_photo_control_span_ownership.py",
    ]
    protected_path = HERE / "preexisting-work.json"
    if not protected_path.exists():
        write("preexisting-work.json", {
            "recorded_before_generated_research_artifacts": True,
            "files": [{"path": str(p.relative_to(ROOT)),
                       "sha256": sha256(p.read_bytes()).hexdigest()} for p in protected],
        })

    for s in SOURCES:
        s["source_record_sha256"] = digest(s)
    source_map = {s["id"]: s for s in SOURCES}

    def bindings(refs):
        return [{"source_id": sid, "source_record_sha256": source_map[sid]["source_record_sha256"]}
                for sid in refs]

    local_paths = [
        ASSETS / "photo_prompt_tags.json",
        ASSETS / "photo_prompt_subculture_extension.json",
        ASSETS / "photo_prompt_historical_womenswear_extension.json",
        ASSETS / "photo_prompt_visual_obligations.json",
        ASSETS / "photo_prompt_visual_obligations_historical_womenswear.json",
        ASSETS / "photo_prompt_visual_profile_index.json",
    ]
    local_records = []
    existing_candidates = {}
    existing_profiles = {}
    slot_counts = {}
    for p in local_paths:
        d = json.loads(p.read_text())
        rec = dict(path=str(p.relative_to(ROOT)), sha256=sha256(p.read_bytes()).hexdigest())
        if "slots" in d:
            rec["slot_counts"] = {k: len(v) for k, v in d["slots"].items()}
            for slot, entries in d["slots"].items():
                for i, entry in enumerate(entries):
                    existing_candidates[entry["id"]] = dict(
                        id=entry["id"], slot=slot, ko=entry.get("ko"), en=entry.get("en"),
                        source_file=rec["path"], source_file_sha256=rec["sha256"],
                        json_pointer=f"/slots/{slot}/{i}",
                    )
        if p.name == "photo_prompt_tags.json":
            slot_counts = rec["slot_counts"]
        if "profiles" in d:
            rec["profile_count"] = len(d["profiles"])
            for i, entry in enumerate(d["profiles"]):
                existing_profiles[entry["id"]] = dict(
                    id=entry["id"], source_file=rec["path"],
                    source_file_sha256=rec["sha256"], json_pointer=f"/profiles/{i}",
                )
        if p.name == "photo_prompt_visual_profile_index.json":
            rec["index_entry_count"] = len(d["entries"])
            rec["index_evidence_limit"] = "entry count only; no coverage, freshness or runtime success claim"
        local_records.append(rec)

    reuse_records = []
    for pid, strategy, refs, note in REUSE:
        assert pid in existing_profiles, pid
        reuse_records.append(dict(
            **existing_profiles[pid], strategy=strategy, note_ko=note,
            source_refs=refs, source_record_bindings=bindings(refs),
            qualification_status="existing_contract_not_requalified_in_this_research",
        ))

    dimensions = {
        "costume_style": ["wardrobe", "silhouette", "garment_topology"],
        "garment_detail": ["garment_topology", "attachment", "layering"],
        "wearable_accessory": ["attachment", "owner_scope"],
        "surface_material": ["surface_appearance"],
        "hair_style": ["hair_structure", "attachment"],
        "prop": ["prop_geometry", "owner_scope", "contact"],
        "action": ["action", "contact", "garment_motion"],
        "capture_context": ["capture_context"],
        "location": ["location"],
    }
    slots = {}
    for p in PROFILES:
        p["source_record_bindings"] = bindings(p["source_refs"])
        for comp in p["components"]:
            cand = {
                "id": comp["id"], "ko": comp["ko"], "en": comp["en"],
                "weight": 0.45,
                "weight_basis": "uniform_research_placeholder_not_popularity",
                "tags": ["costume", "cosplay", "research_proposal"],
                "for_any": ["human"], "aliases": [],
                "keywords": p["narrow_variant_evidence_examples"],
                "embedding_text": comp["en"],
                "concept_units": [comp["en"]],
                "relations": [
                    {"id": comp["id"] + "_owner", "type": "declared_owner_scope",
                     "subject": comp["owner"], "object":
                     "the request-supported pair of costume wearers" if p["id"] == "CC09"
                     else "the request-supported costume wearer"},
                    {"id": comp["id"] + "_assertion", **comp["assertion"]},
                ],
                "affected_dimensions": dimensions[comp["slot"]],
                "source_refs": p["source_refs"],
                "source_record_bindings": bindings(p["source_refs"]),
                "proposal_profile_ref": p["id"],
                "profile_activation": "independent_request_evidence_only",
                "qualification_status": STATUS,
                "integration_strategy": "semantic_overlap_audit_then_reuse_or_add",
            }
            slots.setdefault(comp["slot"], []).append(cand)
    for slot, cid, ko, en, owner, predicate, target, refs in CONTEXT_CANDIDATES:
        slots.setdefault(slot, []).append(dict(
            id=cid, ko=ko, en=en, weight=0.45,
            weight_basis="uniform_research_placeholder_not_popularity",
            tags=["costume", "cosplay", "research_proposal"], for_any=["human"], aliases=[],
            keywords=[ko], embedding_text=en, concept_units=[en],
            relations=[dict(id=cid + "_owner", type="declared_owner_scope",
                            subject=owner, object="the request-supported scene"),
                       dict(id=cid + "_assertion", type=predicate, subject=owner, object=target)],
            affected_dimensions=dimensions[slot], source_refs=refs,
            source_record_bindings=bindings(refs),
            evidence_basis="source_context_only_original_scene_variant",
            profile_activation="independent_request_evidence_only",
            qualification_status=STATUS,
            integration_strategy="semantic_overlap_audit_then_reuse_or_add",
        ))

    profile_map = {p["id"]: p for p in PROFILES}
    bundles = []
    for bid, label, pids, anchors, relation, view in BUNDLE_ROWS:
        refs = sorted({s for pid in pids for s in profile_map[pid]["source_refs"]})
        for anchor in anchors:
            assert anchor in existing_candidates, anchor
        bundles.append(dict(
            id=bid, label_ko=label,
            component_ids=[c["id"] for pid in pids for c in profile_map[pid]["components"]],
            optional_existing_candidate_anchors=[existing_candidates[a] for a in anchors],
            proposed_profile_refs=pids, source_refs=refs,
            source_record_bindings=bindings(refs),
            same_frame_relation=relation, minimum_view=view,
            all_members_jointly_optional=True,
            relation_required_only_when_bundle_is_requested=True,
            profile_activation="independent_request_evidence_only",
            compilation_status="research_recipe_not_runtime_compiled_bundle",
            qualification_status=STATUS,
            compatibility_policy={
                "character_versions": "do_not_merge_unresolved_versions",
                "wearer": "bind_each_required_member_to_declared_owner",
                "source_images": "do_not_copy_model_identity_body_or_unrequested_pose",
                "source_hash_type": "authored_source_record_not_downloaded_page_bytes",
            },
        ))

    for item in ALIGNMENT:
        item["source_record_bindings"] = bindings(item["source_refs"])
        for pid in item["proposed_profile_refs"]:
            assert pid in profile_map, pid
        for eid in item["existing_candidate_or_profile_ids"]:
            assert eid in existing_candidates or eid in existing_profiles, eid

    for item in CASES:
        item["source_record_bindings"] = bindings(item["source_refs"])

    base = dict(researched_date=DATE, status=STATUS)
    write("sources.json", {
        "schema_version": "costume-cosplay-source-ledger/v1", **base,
        "hash_policy": "source_record_sha256 binds authored ledger metadata; no raw-page checksum claim",
        "review_levels": {
            "page_text": "opened page text inspected",
            "page_text_and_browser_image": "page text plus one selected publicly published image visually inspected in browser",
            "search_excerpt": "search-returned excerpt inspected; complete page and embedded image not verified",
            "search_indexed_post_text": "substantial indexed self-authored post text inspected; direct page open failed",
            "search_indexed_article_text": "substantial indexed article text inspected",
        },
        "sources": SOURCES,
    })
    write("event-and-model-cases.json", {
        "schema_version": "costume-cosplay-case-ledger/v1", **base,
        "popularity_policy": "No global popularity ranking; schedules, selected galleries, awards and paid appearances lack a shared denominator.",
        "dates_policy": "Keep publication dates, event dates and project dates distinct.",
        "cases": CASES,
    })
    for observation in REFERENCE_OBSERVATIONS:
        observation["source_record_bindings"] = bindings([observation["source_id"]])
        observation["review_surface"] = "browser_display_of_selected_published_photo"
        observation["native_pixels_inspected"] = False
        observation["generation_or_pixel_qualification"] = False
        observation["original_photo_downloaded_or_redistributed"] = False
    write("reference-image-observations.json", {
        "schema_version": "costume-cosplay-reference-observations/v1", **base,
        "review_limit": "Selected browser-sized published references, not generated native-pixel qualification.",
        "observations": REFERENCE_OBSERVATIONS,
    })
    write("visual-semantics.proposed.json", {
        "schema_version": "costume-cosplay-visual-research/v1", **base,
        "contract_version_target": "photo-authored-visual-components/v1",
        "schema_note": "Research envelope with typed component proposals; runtime profile adapter and validation remain pending.",
        "claim_policy": {
            "source_facts": "sources.json and facts in event-and-model-cases.json",
            "visual_contracts": "researcher-authored selectable variants, not universal source definitions",
            "hard_activation": "independent_request_evidence_only",
            "character_reference": "resolve work, character, version and visual reference before applying a hard canonical-character contract",
            "physical_material": "do not derive chemical composition or hidden mechanisms from a photograph",
            "body_and_identity": "costume terms supply no wearer identity, ethnicity, age, occupation or natural body measurements",
            "pixel_policy": "partial_is_fail",
        },
        "profiles": PROFILES, "reuse_and_scope_exclusions": reuse_records,
    })
    write("candidate-data.proposed.json", {
        "schema_version": "photo-prompt-research-extension/v1", **base,
        "default_activation": "off_until_runtime_integration_and_qualification",
        "subject_policy": "Use request-supported wearer and existing age policy; garment/character labels supply no age.",
        "schema_note": "Research candidates preserve source/owner metadata. An explicit adapter is required before adding to production assets.",
        "slots": slots,
    })
    write("candidate-bundles.proposed.json", {
        "schema_version": "costume-cosplay-candidate-bundle-research/v1", **base,
        "bundle_policy": "Jointly optional recipes; retrieval or selection alone cannot activate hard profiles.",
        "bundles": bundles,
    })
    write("keyword-alignment.json", {
        "schema_version": "costume-cosplay-keyword-alignment/v1", **base,
        "source_conversation": "source-conversation.json",
        "seed_status": "untrusted_research_seed_not_authority",
        "matching_policy": "Semantically grouped keyword crosswalk, not exhaustive verbatim token extraction.",
        "groups": ALIGNMENT,
    })
    write("qualification-plan.json", {
        "schema_version": "costume-cosplay-qualification-plan/v1", **base,
        "execution_status": "not_run",
        "fixture_activation_unit": "independently_supported_component",
        "fixture_policy": "Profile eligibility is discovery only. Each hard component still requires its own independent request evidence; the other components do not activate automatically.",
        "pipeline_gates": [
            "Resolve source versions and semantic overlaps with existing profiles/candidates.",
            "Compile research proposals through an explicit runtime adapter.",
            "Run activation, exclusions, ownership and optional-bundle regression fixtures.",
            "Rebuild only affected indexes and verify source/candidate bindings.",
            "Freeze per-arm core, request evidence, source snapshot and native pixel gates before candidate exposure.",
            "Retain first outputs, prompts, tool records and native images; review every required relation.",
            "Record user judgment separately from structural gate results.",
        ],
        "schema_and_routing_fixtures": [
            dict(id=i, request=q, expected_eligible_profiles_or_contracts=yes,
                 must_not_activate=no, reason=why, result="NOT_RUN")
            for i, q, yes, no, why in FIXTURES
        ],
        "native_pixel_arms": [
            dict(id=i, label_ko=label, proposed_profile_refs=pids,
                 core_brief_ko=brief, inspect=inspect, result="NOT_RUN",
                 proposed_core_component_clauses=[c["en"] for pid in pids for c in profile_map[pid]["components"]],
                 proposed_generation_limit=1, proposed_retry_count=0,
                 gate_ids=[c["render_gate"]["id"] for pid in pids for c in profile_map[pid]["components"]],
                 evidence_required=["frozen request/core", "source and data hashes", "exact prompt/tool record",
                                    "retained native image", "per-gate pixel review"],
                 image_workflow="future image task; no generation was performed by this research")
            for i, label, pids, brief, inspect in RENDER_ARMS
        ],
        "pixel_rules": {
            "aggregate": "partial_is_fail",
            "occluded_required_visible_relation": "FAIL",
            "hidden_physical_function_without_visual_contract": "UNSCORED",
            "prompt_runtime_pass": "does_not_establish_pixel_pass",
            "causal_improvement": "requires separately frozen baseline/comparison; no effect-size claim from isolated examples",
        },
    })

    seed = json.loads((HERE / "source-conversation.json").read_text())
    seed_hash = digest(seed)
    protected_before = json.loads(protected_path.read_text())
    protected_checks = [
        dict(**rec, unchanged=sha256((ROOT / rec["path"]).read_bytes()).hexdigest() == rec["sha256"])
        for rec in protected_before["files"]
    ]
    assert all(r["unchanged"] for r in protected_checks), "Preexisting work changed."
    all_candidates = [c for rows in slots.values() for c in rows]
    counts = dict(
        source_records=len(SOURCES), event_and_model_cases=len(CASES),
        proposed_profiles=len(PROFILES),
        observable_components=sum(len(p["components"]) for p in PROFILES),
        proposed_candidates=len(all_candidates), candidate_bundles=len(bundles),
        keyword_groups=len(ALIGNMENT), reuse_profiles=sum(x[1] == "reuse" for x in REUSE),
        scope_exclusion_profiles=sum(x[1] == "scope_exclusion" for x in REUSE),
        planned_routing_fixtures=len(FIXTURES), planned_native_pixel_arms=len(RENDER_ARMS),
        candidate_slots={s: len(rows) for s, rows in slots.items()},
        source_review_levels=dict(Counter(s["review_level"] for s in SOURCES)),
    )
    write("coverage-audit.json", {
        "schema_version": "costume-cosplay-coverage-audit/v1", **base, "counts": counts,
        "live_local_files": local_records,
        "base_dictionary_selected_slot_counts": {s: slot_counts[s] for s in
            ["costume_style", "wardrobe_style", "garment_detail", "wearable_accessory",
             "prop", "surface_material", "hair_style", "action"]},
        "source_conversation_authored_record_sha256": seed_hash,
        "preexisting_dirty_file_checks": protected_checks,
        "research_task_runtime_asset_writes": [],
        "excluded_evidence": [
            "Cosplay popularity lists without a measurement method or denominator.",
            "Doujin circle counts used as a substitute for costume wearer counts.",
            "Follower counts, likes and photo counts treated as candidate weights.",
            "Event appearance announcements treated as confirmed attendance.",
            "Creator portfolio images treated as identity or natural body-shape evidence.",
        ],
        "open_gaps": [
            "No representative wearer-frequency dataset was found in the inspected sources.",
            "Character-by-character canonical references and skin/version graphs are not complete.",
            "Several regional, religious, sport and retro variants remain explicitly in the keyword backlog.",
            "Source excerpts have narrower verification than opened page text.",
            "Runtime compilation, routing tests, index updates and generated-pixel qualification are not performed.",
        ],
    })

    ids = [c["id"] for c in all_candidates]
    assert len(ids) == len(set(ids))
    assert not set(ids).intersection(existing_candidates), "Research candidate ID collision."
    assert len(source_map) == len(SOURCES)
    assert len(profile_map) == len(PROFILES)
    candidate_ids = set(ids)
    gate_ids = {c["render_gate"]["id"] for p in PROFILES for c in p["components"]}
    for p in PROFILES:
        for comp in p["components"]:
            assert comp["id"] in candidate_ids
            assert len(comp["en"].split()) >= 3
            assert comp["assertion"]["subject"] == comp["owner"]
    for bundle in bundles:
        assert set(bundle["component_ids"]).issubset(candidate_ids)
        assert bundle["all_members_jointly_optional"]
        assert bundle["profile_activation"] == "independent_request_evidence_only"
    for _, _, pids, _, _ in RENDER_ARMS:
        assert all(pid in profile_map for pid in pids)

    generated_files = [
        "source-conversation.json", "preexisting-work.json", "sources.json",
        "event-and-model-cases.json", "visual-semantics.proposed.json",
        "candidate-data.proposed.json", "candidate-bundles.proposed.json",
        "keyword-alignment.json", "qualification-plan.json", "coverage-audit.json",
        "reference-image-observations.json",
    ]
    if (HERE / "research-report.md").exists():
        generated_files.append("research-report.md")
    for name in generated_files:
        if not name.endswith(".json"):
            continue
        data = json.loads((HERE / name).read_text())

        def check_refs(node):
            if isinstance(node, dict):
                if "source_refs" in node:
                    assert set(node["source_refs"]).issubset(source_map), (name, node["source_refs"])
                for binding in node.get("source_record_bindings", []):
                    assert binding["source_record_sha256"] == source_map[binding["source_id"]]["source_record_sha256"]
                for value in node.values():
                    check_refs(value)
            elif isinstance(node, list):
                for value in node:
                    check_refs(value)

        check_refs(data)
    write("artifact-check.json", {
        "schema_version": "costume-cosplay-artifact-check/v1", "checked_date": DATE,
        "result": "PASS_RESEARCH_ARTIFACT_INTEGRITY",
        "checks": [
            "JSON parsing", "unique source/profile/candidate IDs", "no collision with inspected existing candidate IDs",
            "source references and authored source-record hashes", "bundle candidate references",
            "planned render profile references", "keyword references to live inspected local IDs",
            "component owner/assertion consistency", "preexisting dirty file hashes unchanged",
        ],
        "files": [
            dict(path=name, sha256=sha256((HERE / name).read_bytes()).hexdigest())
            for name in generated_files
        ],
        "counts": counts, "native_pixel_gate_count": len(gate_ids),
        "verification_limit": "Research artifact integrity only; runtime adapter, activation fixtures and generation arms are NOT_RUN.",
    })
    print(json.dumps({"result": "PASS_RESEARCH_ARTIFACT_INTEGRITY", **counts}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
