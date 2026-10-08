"""Compile planning artifacts outside runtime data; no network/provider calls."""
import collections
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BT = chr(96)


def dump(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def load_notes():
    sources, cards = [], []
    for line in (HERE / "source-notes.txt").read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        key, issuer, title, url, access, scope, limits = line.split("|")
        sources.append(dict(id=key, issuer=issuer, title=title, url=url,
                            access_level=access, verified_scope_ko=scope,
                            claim_limits_ko=limits, checked_date_kst="2026-10-08"))
    for line in (HERE / "research-cards.txt").read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        key, title, groups, axis, carrier, props, meaning, boundary, visible, refs, existing, priority, variants = line.split("|")
        cards.append(dict(id=key, title_ko=title, seed_groups=groups.split(","),
            axis=axis, carrier=carrier, property_suffixes=props.split(","),
            meaning_ko=meaning, confusion_boundary_ko=boundary,
            visibility_prerequisite_ko=visible, source_ids=refs.split(","),
            existing_record_ids_to_review=[] if existing == "-" else existing.split(","),
            priority=priority, alternative_clauses_en=[] if variants == "-" else variants.split("~"),
            status="research_proposal_not_runtime_registration",
            source_relation="Bounded source facts; component formulations and implementation choices are researcher interpretations.",
            variant_policy="Split alternative forms before promotion; never combine all examples into one required profile.",
            activation_plan="optional_postcore; similarity or bare label alone never makes a hard obligation",
            validation_status="not_rendered_not_live_retrieved"))
    return sources, cards


def routes_for_terms(inventory):
    routes = {t["id"]: [] for t in inventory["terms"]}
    groups = {g["id"]: g["term_ids"] for g in inventory["groups"]}

    def a(group, cards, positions=None):
        cards = [cards] if isinstance(cards, str) else cards
        positions = range(1, len(groups[group]) + 1) if positions is None else positions
        for pos in positions:
            target = routes[groups[group][pos-1]]
            target.extend(c for c in cards if c not in target)

    a("01","FF01",[1,9,10,11,12,13,14]); a("01","FF59",[2,4,6,7,8])
    a("01","FF06",[3]); a("01","FF64",[5]); a("01","FF07",[15]); a("01","FF38",[16])
    a("02a","FF02",[1,2,3,4,5,9,10,11,12,13]); a("02a","FF24",[6,7,8]); a("02a","FF38",[14])
    a("02b","FF03",range(1,9)); a("02b","FF38",[9]); a("02b","FF04",[10,16])
    a("02b","FF22",[11]); a("02b","FF34",[12]); a("02b","FF07",[13]); a("02b","FF05",[14,15])
    a("03","FF06",[1,2,3,4,5,6,8,10,11,13]); a("03","FF07",[7,9,12,16,17,18,19])
    a("03","FF08",[14,15]); a("03","FF64",[20])
    a("04a","FF10",[1,2,3,4,5,8]); a("04a","FF09",[6,7]); a("04a","FF11",[9,10])
    a("04a","FF12",[11,12,13]); a("04a","FF13",range(14,21))
    a("04b","FF13",[1,2]); a("04b","FF14",[3,8,9]); a("04b","FF15",[4,5,6,7,12,13,14]); a("04b","FF16",[10,11])
    a("05","FF17",range(1,12)); a("05","FF18",range(12,16)); a("05","FF19",range(16,22)); a("05","FF20",[22,23]); a("05","FF29",[24])
    a("06","FF23",[1]); a("06","FF21",[2,3,4,5,6,15]); a("06","FF22",range(7,13)); a("06","FF05",[13]); a("06","FF02",[14]); a("06",["FF21","FF29"],[16])
    a("07","FF23",list(range(1,10))+[17]); a("07","FF24",[10,11,12,13,14]); a("07","FF59",[15,16]); a("07","FF35",[18])
    a("08","FF24",range(1,12)); a("08","FF25",[12,13,14]); a("08","FF26",[15,16,17]); a("08","FF23",[18]); a("08","FF27",[19,20,21]); a("08","FF59",[22,23,24,25]); a("08","FF36",[26,27])
    a("09","FF28",[1,2,12,13,14,15,16]); a("09","FF29",[3,4,7,8,9,10]); a("09","FF37",[5]); a("09","FF36",[6]); a("09","FF07",[11]); a("09","FF60",[17,18,19])
    a("10","FF30",range(1,16)); a("10","FF20",[16]); a("10","FF32",[17]); a("10","FF36",[18]); a("10","FF31",range(19,27))
    a("11","FF38",[1,2]); a("11","FF59",[3,21]); a("11","FF32",list(range(4,10))+[18,19,20]); a("11","FF33",range(10,18))
    a("12a","FF34",list(range(1,7))+[12]); a("12a","FF35",[7,8,9,10]); a("12a","FF29",[11])
    a("12b","FF37",[1,2,3,4,14,15]); a("12b","FF36",range(5,13)); a("12b","FF59",[13,16])
    a("13","FF39",list(range(1,11))+[20,21,23,24,25,28]); a("13","FF38",range(11,20)); a("13",["FF02","FF38"],[22]); a("13","FF49",[26,27])
    a("14a","FF40",range(1,10)); a("14a","FF59",[10]); a("14b","FF41")
    a("15","FF43",list(range(1,10))+[12]); a("15","FF45",[10,11,17,18,19,20]); a("15","FF44",[13,14,15,16]); a("15","FF46",[21,22,23,24])
    a("16a","FF47",range(1,6)); a("16a","FF48",range(6,14)); a("16a","FF62",[14,15]); a("16a","FF20",[16]); a("16a","FF49",[17,18]); a("16a","FF50",[19,20,21])
    a("16b","FF50",[1,2,3]); a("16b","FF49",[4]); a("16b","FF51",range(5,12)); a("16b","FF64",[12])
    a("17","FF39",[1,2,3,6,16]); a("17","FF52",[4,5]); a("17","FF53",[7,8,9]); a("17","FF54",[10,11,12]); a("17","FF55",[13,14,15,18]); a("17","FF30",[17])
    a("18","FF56",list(range(1,14))+[20,27]); a("18","FF57",[14,21,22]); a("18","FF58",[15,16,17,18,19]); a("18","FF42",[23,24,25,26])
    a("19a","FF59",[1,2,3,4,5,6,7,9,10,11,12,13,14,15]); a("19a","FF54",[8]); a("19b","FF59")
    a("20","FF60",range(1,6)); a("20","FF61",[6,7,8,10]); a("20","FF62",[9,11,12,14,15,16]); a("20","FF44",[13])
    a("21","FF03",[1,2,15,23]); a("21","FF63",[3,4,6,7,8,9,10,11,24]); a("21","FF02",[5,22]); a("21","FF07",[12]); a("21","FF26",[13]); a("21","FF24",[14]); a("21","FF22",[16]); a("21","FF56",[17,18,19,20]); a("21","FF58",[21,25])
    assert all(routes.values()), [key for key,v in routes.items() if not v]
    return routes


MEASUREMENTS = set("""Size;Body measurements;Finished garment measurements;Ease;Wearing ease;Design ease;Positive ease;Zero ease;Negative ease;Shoulder width;Shoulder slope;Sleeve-cap height;Sleeve-cap ease;Sleeve pitch;Front rise;Back rise;Crotch depth;Crotch length;Crotch extension;Inseam;Outseam;Suit drop;Dart intake;Stretch percentage;Recovery;One-axis stretch;Multi-directional stretch;Two-way / Four-way stretch;Mechanical stretch;Elastane / Spandex;Woven;Knit;Hand / Handle;Fabric weight / GSM;Growth;Shrinkage;Bonded;Cup depth / Projection;Wire width;Sister size;Spiral steel bone;Flat steel bone;Waist tape / Stay;Hip spring;Rib spring;Waist reduction;Compression fit;Supportive fit;Low / Medium / High support;Power mesh;Grip tape;Movement ease;Layering ease;Binding;Full canvas;Half canvas;Fused construction;Unstructured;Soft tailoring;Fully lined;Half-lined;Unlined;Inlay""".split(";"))
BRAND = set("""Regular fit;Classic fit;Easy fit;Comfort fit;Super slim / Extra slim;Athletic fit;Curvy fit;Mom fit;Boyfriend fit;Girlfriend fit;Dad fit;Cheeky;Brazilian cut;French-cut;Full coverage;Moderate coverage;Mermaid;Trumpet;H-line;I-line;X-line;O-line;Horseshoe;T-shirt bra;Bralette;Shelf bra""".split(";"))
TEMPORAL = set("Riding up;Strap slipping;Band riding up;Sagging;Bagging out;Shrinkage;Growth;Swing silhouette".split(";"))
CONTEXT = set("Bulge;Camel toe;Wedgie;No-show;Quarter-cup / Open-cup;Cupless;Open-crotch".split(";"))


def disposition(t):
    en, group = t["en"], t["group"]
    if en in MEASUREMENTS or group == "19b" or (group == "19a" and en != "Adaptive clothing"):
        return "specification_or_process", "retain_specs; derive_visible_result_only_when_requested"
    if en in TEMPORAL:
        return "temporal_or_history", "current_state_only; sequence_or_measurement_required_for_change"
    if group == "21":
        return "contextual_colloquial", "advisory_context_resolution; no_body_change"
    if en in CONTEXT:
        return "explicit_context_or_product", "keep_term_and_context; direct_term_source_confirmation_before_promotion"
    if en in BRAND:
        return "brand_or_variable_boundary", "resolve_selected_components; no_numeric_or_body_default"
    return "visible_form_or_state", "review_existing_meaning; reuse_or_split_selected_variant"


RELATION_NOTES = """ease|garment side panels|spaced_from|the same torso
contact|garment fabric|follows_with_selected_contact|the same wearer contour
volume|garment outer edges|enclose_clearance_around|the same body
regional_ratio|garment waist region|has_less_room_than|the same garment hip or chest region
silhouette|garment outer contour|has_selected_width_distribution|its upper middle and lower regions
flare|skirt lower region|widens_from|the selected landmark on the same wearer
shoulder|sleeve attachment or head|positioned_relative_to|the same shoulder tip
attachment|sleeve panel or area|connected_to|the same garment torso panel or area
construction_measurement|armhole edge|positioned_relative_to|the same armpit
sleeve_volume|sleeve fabric|changes_volume_toward|its own edge or cuff
neckline|garment neck edges|form_selected_boundary|the same neckline or collar folds
coverage_topology|garment edge or support|connected_at|the selected garment region
waist_landmark|bodice skirt join|positioned_relative_to|the same waist or underbust landmark
waist_shaping|waist fabric|narrows_at|its own belt seam or gathered region
rise|trouser waistband or crotch join|positioned_relative_to|the same waist or crotch landmark
leg_geometry|trouser leg contour|changes_width_toward|its own knee and hem
leg_topology|torso or crotch fabric|divides_into|two leg tubes of the same garment
dress_geometry|skirt or dress side edges|follow_or_depart_from|the same waist and hip
panel_topology|component fabric panel|joined_or_overlapped_with|adjacent panels of the same garment
length|garment hem|ends_relative_to|the selected body landmark or support surface
hem_contact|trouser hem|contacts_or_departs_from|the same shoe or adjacent floor
jacket_topology|jacket front panels|overlap_or_separate_at|their own fastening region
hidden_construction|visible jacket lining|lies_inside|the same opened outer panel
panel_shaping|dart or curved seam|shapes_or_joins|fabric panels of the same bodice
fold_topology|fold ridges|fold_toward|the selected direction in the same panel
gather_topology|fabric folds|anchored_by|the same gathering seam or stitch rows
fabric_behavior|fabric folds and edge|fall_from_or_hold_at|their own support or contact region
support_topology|cup casing or reinforced panel|connected_to|the same garment band or fabric
fit_state|fabric edge seam or band|has_selected_gap_or_displacement_relative_to|its own neighboring body or fabric boundary
bodice_topology|bodice or corset panels|cover_and_connect_across|selected regions of the same torso
closure_topology|fastener lace or eyelet|joins|corresponding edges of the same bodice
garment_topology|garment torso section|continues_into|its own brief or leg sections
coverage|opening edge|borders|the selected region of the same wearer
layer_visibility|translucent outer layer|reveals_or_covers|the independently declared inner layer or body
surface_outline|outer fabric|carries_visible_trace_of|the requested underlying edge or gathering seam
strap_topology|two back straps|converge_or_cross_before_attachment|the same band or attachment sites
seam_topology|adjoining panels|joined_at_selected_location|the same visible seam
articulation|shaped knee or waist panels|fit_around|the already declared joint or seated position
adjustment|adjustment fold or string|connected_through|the same fixed seam or casing
historical_volume|gown skirt|projects_relative_to|its own waist and selected lateral or rear axis
historical_structure|bodice or support|extends_or_supports|the same garment lower torso or skirt
garment_topology|fashion strap or opening|connected_to|the same declared garment anchors
colloquial_interpretation|garment contour and folds|realize_contextual_impression_through|selected local shape and fabric behavior
composition|garment instances|combine_independent_properties_on|their own bound fit silhouette length and structure"""
RELATIONS = {}
for line in RELATION_NOTES.splitlines():
    axis, subject, op, obj = line.split("|")
    # The first garment_topology row belongs to bodywear; FF62 overrides it below.
    RELATIONS.setdefault(axis, (subject, op, obj))


COMPARISON_NOTES = """skinny / slim|부위별 밀착|몸 크기 변경
slim / tapered|여유와 폭 변화|아이라인 테이퍼
relaxed tapered / straight wide|허벅지 여유와 하부 폭|발목만 crop
baggy / barrel|분량과 볼록한 옆선|풍선 소품
oversized / boxy|큰 비율과 직사각 몸통|무조건 긴 옷
crop / tight|끝점과 밀착|짧음을 밀착으로 번역
curvy fit / curvy body|옷의 허리-힙 분량|몸 치수 변경
curvy / plus-size|부위 비율과 치수군|몸 크기 고정
athletic fit / muscular person|옷의 가슴·허벅지 여유|근육량 증가
body-skimming / body-hugging|국소 접촉과 처짐|비침 자동 추가
mermaid dress / mermaid body|직물과 퍼짐|물고기 꼬리
mermaid / trumpet|요청된 퍼짐 시작점|이름만으로 무릎선 고정
drop shoulder / padded shoulder|팔 쪽 연결선|넓은 신체 어깨
raglan / drop shoulder|목-겨드랑이 사선|소매 길이 기본값
bishop / bell|커프스 모음과 열린 끝단|상반된 끝단 동시 강제
high waist / high leg|허리단과 다리 개구부|둘 다 높게 변경
low rise / drop crotch|허리단과 다리 분기|밑위 전체 한 값
surplice / opening wrap|패널 겹침과 여밈|자동 풀림 동작
princess seam / princess dress|곡선 패널 연결|왕관 소품
dart shaping / darting gaze|몸판 끝점과 접힘|눈 행동 변경
godet / gored skirt|삽입과 전체 패널|삼각 인쇄무늬
shirring / smocking|반복 박음선과 주름 연결망|탄성실 항상성
trouser break / event break|밑단-신발 접촉|파괴 사건
unlined / unstructured|안감과 내부 보강|캔버스 무조건 제거
moulded / padded|성형과 충전층|몸 크기 증가
wireless / unsupported|와이어와 다른 지지 구성|지지 없음 단정
racerback / cross-back|Y 합류와 X 교차|끝점 가림
sheer / skin-tight|투과와 접촉|노출 강도 증가
illusion panel / real opening|직물 연결과 빈 구멍|안감 누락
VPL / exposed underwear|겉감 위 경계|직접 피부 노출
Wedgie product / wedgie state|상품과 끼임|명칭으로 상태 추정
puckering / small size|솔기 주변 주름|원인 한 가지 확정
rolling / riding up|접힘과 높아진 위치|전후 이력 발명
pannier / bustle|좌우 폭과 뒤 돌출|같은 큰 치마
corset / corset top|실제 패널·여밈·보강|금속 구성 전역 강제
no-front-seam / seamless|선택 구역과 제품 전체|모든 솔기 삭제
여리핏 / 마른 몸|소재·길이·여유 해석|체형·성격 추정
comfort fit / verified comfort|제품과 실제 평가|착용감 PASS"""


def main():
    sources, cards = load_notes()
    inventory = json.loads((HERE / "term-inventory.json").read_text())
    routes = routes_for_terms(inventory)
    card_index = {c["id"]:c for c in cards}
    source_ids = {s["id"] for s in sources}
    proposals, terms = [], []
    for c in cards:
        c["term_ids"] = [tid for tid,r in routes.items() if c["id"] in r]
        c["role"] = "cross-axis composition design" if c["id"] == "FF64" else "semantic family; split individual variants before promotion"
        for n, clause in enumerate(c["alternative_clauses_en"], 1):
            subject, op, obj = RELATIONS[c["axis"]]
            if c["id"] == "FF62":
                subject, op, obj = "fashion strap or opening", "connected_to", "the same declared garment anchors or layers"
            proposals.append(dict(id=f"fit_plan_{c['id'].lower()}_{n}", card_id=c["id"],
                priority=c["priority"], positive_clause_en=clause,
                slot_plan="wardrobe_style" if c["axis"] in {"composition","silhouette","dress_geometry","historical_volume","volume"} else "garment_detail",
                concept_units=[part.strip().rstrip(".") for part in clause.split(";")],
                relation_draft=dict(subject=subject, type=op, object=obj,
                    owner_binding="Bind concrete nodes of the same already declared garment and wearer for each selected variant."),
                affected_property_templates=["wardrobe.garments.<bound_garment_id>."+x for x in c["property_suffixes"]],
                prerequisites_ko=c["visibility_prerequisite_ko"],
                further_review=["Resolve all named garments, layers, shoes, surfaces and postures from existing/open requester scope.",
                    "Review complete effects: length, sleeves, materials, neckline, coverage and local fit.",
                    "Narrow family-level property templates to all and only the selected variant's effects; confirm actual schema paths.",
                    "Replace family relation operators and endpoint alternatives with one concrete relation per selected variant.",
                    "These are research templates, not executable runtime entries or compatibility proof."],
                pixel_gate=dict(selected_proposition=clause, owner_and_endpoint_visibility="all required endpoints on the same garment",
                                unobservable="UNOBSERVABLE_NOT_PASS", partial="partial_is_fail"),
                source_ids=c["source_ids"], existing_ids_to_compare=c["existing_record_ids_to_review"],
                state="research_draft; deduplication_effect_review_and_runtime_conversion_pending"))
    for t in inventory["terms"]:
        ids = routes[t["id"]]
        evidence, action = disposition(t)
        terms.append(dict(id=t["id"],source_term=t["source_term"],group=t["group"],
            semantic_card_ids=ids,evidence_class=evidence,recommended_action=action,
            priority=min((card_index[k]["priority"] for k in ids), key=lambda x:int(x[1:])),
            source_ids=sorted({sid for k in ids for sid in card_index[k]["source_ids"]}),
            source_verification_status="family mapping; not every synonym individually source-confirmed",
            candidate_lexical_ids=[x["id"] for x in t["positive_field_mentions"]["candidates"]],
            profile_lexical_ids=[x["id"] for x in t["positive_field_mentions"]["profiles"]],
            semantic_equivalence_status="Lexical neighbors are not approved reuse. Review each record's owner, meaning and scope."))
    comparisons=[]
    for n,line in enumerate(COMPARISON_NOTES.splitlines(),1):
        label, positive, negative = line.split("|")
        comparisons.append(dict(id=f"FIT-PAIR-{n:02d}",comparison=label,must_preserve=positive,
            must_reject=negative,languages=["ko","en"],status="planned_not_executed"))
    classes = dict(collections.Counter(t["evidence_class"] for t in terms))
    dump("sources.json",dict(count=len(sources),sources=sources,
        excluded_access=[dict(url="https://www.uen.org/cte/facs_cabinet/downloads/ClothingII/Sewing_With_Speciality_Fabrics.pdf",reason="Direct open failed; not a decisive source.")],
        limits=["Bounded primary excerpts, official indexed text, institutional synthesis and a dictionary entry.",
            "No full laboratory tests, current commercial availability, unseen image review or 513 separately confirmed definitions claimed."]))
    dump("semantic-cards.json",dict(schema="fashion-fit-research-cards/v1",count=len(cards),cards=cards))
    dump("candidate-proposals.json",dict(schema="fashion-fit-research-candidates/v1",count=len(proposals),
        runtime_registered=False,templates_are_executable=False,proposals=proposals))
    dump("term-plan.json",dict(count=len(terms),terms=terms,evidence_classes=classes))
    dump("regression-plan.json",dict(count=len(comparisons),comparisons=comparisons,
        method="Author independent frozen cores before runtime assets; make minimal pairs changing one fit axis.",
        mutations=["garment color","excluded transparency","requested sleeve length","different garment owner",
            "wearer body dimensions","flare landmark","unrequested inner lining","X instead of Y",
            "required boundary outside crop","label-only hit becomes a hard requirement"],
        pixel_clusters=["local contact","regional ratio","shoulder attachment","sleeve end","leg curve",
            "waist rise and leg opening","hem-shoe contact","layer transparency","cup edge gap",
            "back strap connectivity","closure endpoints","historical volume direction"],
        pixel_protocol="Only if generation is later requested: preserve frozen meaning/controls, save exact requests/images, inspect selected gates at native pixels; judge preference separately.",
        current_images=0,current_runtime_dispatch=0))
    fields=["id","source_term","group","evidence_class","semantic_card_ids","priority","recommended_action","source_ids","candidate_lexical_ids","profile_lexical_ids","source_verification_status"]
    with (HERE / "term-plan.csv").open("w",newline="",encoding="utf-8-sig") as f:
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader()
        for t in terms:
            writer.writerow({k:"; ".join(t[k]) if isinstance(t[k],list) else t[k] for k in fields})
    doc=["# 패션 핏 시각 의미 상세 카드","","2026-10-08 KST. 64개 의미군과 119개 후보 문장 초안이다. 실제 신규 엔트리 수가 아니다. 중복 검토·소유자 결속·효과 범위 검토·runtime 변환은 실행 계획에 남아 있다.","",
         "문장들은 서로 다른 선택형 변형이다. 카드 전체를 한 프로필의 필수 all-of로 합치지 않는다. 수치·촉감·제작 이력·숨은 구조·동적 성능은 정지 사진의 hard gate로 만들지 않는다.",""]
    for c in cards:
        doc += [f"## {c['id']} {c['title_ko']}","",c["meaning_ko"],"",
            f"- 소유자: {BT}{c['carrier']}{BT}. 축: {BT}{c['axis']}{BT}. 우선순위: {BT}{c['priority']}{BT}.",
            "- 속성 범위: "+", ".join(BT+x+BT for x in c["property_suffixes"])+".",
            "- 혼동 경계: "+c["confusion_boundary_ko"],
            "- 관찰 조건: "+c["visibility_prerequisite_ko"],
            "- 검토할 기존 ID: "+(", ".join(BT+x+BT for x in c["existing_record_ids_to_review"]) or "개별 동등성 검토 필요"),
            "- 한정된 근거: "+", ".join(f"[{s['issuer']}: {s['title']}]({s['url']})" for s in sources if s["id"] in c["source_ids"]),
            "","후보 표현 초안:",""]
        doc += ["- "+x for x in c["alternative_clauses_en"]] if c["alternative_clauses_en"] else ["측정·공정 메타데이터로 유지한다. 명칭만으로 pixel hard gate를 만들지 않는다."]
        doc += [""]
    (HERE / "semantic-cards.md").write_text("\n".join(doc)+"\n")
    checks=dict(terms_513=len(terms)==513,cards_64=len(cards)==64,sources_41=len(sources)==41,
        candidate_drafts_119=len(proposals)==119,comparison_pairs_38=len(comparisons)==38,
        every_term_mapped=all(routes.values()),source_references_valid=all(set(c["source_ids"])<=source_ids for c in cards),
        card_references_valid=all(k in card_index for t in terms for k in t["semantic_card_ids"]),
        term_ids_unique=len({t["id"] for t in terms})==513,
        draft_ids_unique=len({p["id"] for p in proposals})==len(proposals),
        no_runtime_registration_or_provider_calls=not json.loads((HERE/"candidate-proposals.json").read_text())["runtime_registered"]
            and not json.loads((HERE/"source-snapshot.json").read_text())["runtime_dispatch_executed"]
            and json.loads((HERE/"source-snapshot.json").read_text())["embedding_calls"] == 0
            and json.loads((HERE/"source-snapshot.json").read_text())["image_calls"] == 0)
    dump("research-validation.json",dict(scope="research_artifact_integrity_only",checks=checks,
        result="PASS" if all(checks.values()) else "FAIL",
        not_tested=["live retrieval","semantic/profile index freshness","prompt composition","native pixels","user preference"],
        artifact_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.iterdir()) if p.is_file() and p.name!="research-validation.json"}))
    assert all(checks.values()),checks
    print(json.dumps(dict(checks=checks,evidence_classes=classes,priorities=dict(collections.Counter(c["priority"] for c in cards))),ensure_ascii=False))


if __name__ == "__main__":
    main()
