"""Natural relation descriptions following the independent retrieval audit.

No evaluation sentence becomes an exact alias. Definitions, effects, minimum
evidence, and existing native gates stay intact; concise equivalents are soft.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"

# Slug | concise English component relations | Korean component relations.
# Each group still describes its own necessary part of the selected relation.
NATURAL = r"""
contrasting_robe_sleeves|a solid-color robe body; contrast-colored sleeves at its armholes|단색 몸판의 긴 옷; 그 진동에 붙은 배색 소매
sleeveless_robe_over_inner_sleeves|a sleeveless outer robe; inner sleeves through its armholes|소매 없는 겉포; 그 진동으로 나오는 안쪽 소매
robe_waist_join_pleats|the robe's sewn waist seam; pleats falling from that seam|포의 봉제된 허리선; 그 허리선에서 내려오는 주름
shoulder_draped_empty_sleeve|a fur-edged coat draped on one shoulder; its empty hanging sleeve; its own supporting cord|한 어깨에 걸친 모피 테두리 코트; 그 코트의 비어 늘어진 소매; 같은 코트의 지지끈
angular_czapka_top_brim|a four-cornered cap crown; a separate brim below it|모자의 사각 윗판; 그 아래 별도의 챙
tall_fur_headwear|a tall fur cap; its rim separate from the hair|높은 모피 모자; 머리카락과 구분되는 모자 테두리
jacket_attached_false_vest|an imitation vest sewn to the jacket; its jacket-attached front panel|재킷에 봉제된 모조 조끼; 같은 재킷에 붙은 앞패널
green_coat_tan_shirt_taupe_trousers|a green coat over a tan shirt; separate taupe trousers below|탠 셔츠 위의 녹색 코트; 그 아래 별도 토프색 바지
blue_coat_over_white_shirt|a blue outer coat; a white shirt within its lapels|청색 겉코트; 그 라펠 안의 흰 셔츠
utility_pockets_beside_closure|the work jacket's center-front closure; separate pocket mouths beside it|작업 재킷의 중앙 앞여밈; 그 옆의 독립된 주머니 입구
blue_frock_collar_cuffs|a blue collar matching the frock; its matching blue cuffs|프록과 같은 청색 칼라; 같은 청색으로 맞춘 커프
separate_flared_trouser_hems|separate left and right trouser legs; flared hems on both legs|분리된 좌우 바지통; 양쪽 바지통의 넓어진 밑단
norfolk_pleats_under_belt|the coat's vertical pleats; an outer belt crossing them|코트 몸판의 세로 주름; 그 위를 가로지르는 겉벨트
fabric_flight_coverall_zips|a one-piece fabric flight suit; its front zipper separate from pocket zips|몸통과 바지로 이어진 직물 비행복; 주머니 지퍼와 구분되는 앞지퍼
helmet_connected_suit_neck|an enclosing helmet and visor; its rim joined to the suit neck|머리를 감싸는 헬멧과 바이저; 복장 목부에 이어진 헬멧 테두리
breastplate_cloth_ruff_layers|a rigid breastplate over cloth; a separate fabric ruff above it|천 위에 겹친 단단한 가슴판; 그 위의 별도 천 러프
yellow_black_uniform_sections|yellow and black uniform panels; their boundaries within the same garment|제복의 황색과 검정 패널; 같은 의복 안의 배색 경계
domed_helmet_with_tunic|a domed helmet with a distinct rim; a separate tunic beneath it|구분되는 테두리의 둥근 헬멧; 그 아래 별도 튜닉
red_coat_outer_leg_stripe|a red coat over separate trousers; a yellow stripe along their outer legs|별도 바지 위의 붉은 코트; 그 바지의 바깥다리 황색 세로선
continuous_coverall_front_closure|a one-piece jumpsuit crossing the waist; its central front zipper|허리를 가로질러 이어진 일체형 작업복; 같은 작업복의 중앙 앞지퍼
plain_top_separate_trousers|a plain independently edged top; a separate pair of trousers|독립된 밑단의 무지 상의; 따로 입은 한 벌의 바지
loose_scrub_separates|a loose scrub top with its own hem; separate loose scrub trousers|자체 밑단이 있는 헐렁한 스크럽 상의; 별도의 헐렁한 스크럽 바지
fabric_hood_coverall_face_opening|the coverall's attached cloth hood; its open face aperture|일체복에 이어진 천 후드; 그 후드의 열린 얼굴 구멍
single_uniform_button_row|one row of uniform buttons; their matching single front closure|제복 단추의 한 줄 배열; 그 배열과 맞물리는 한 줄 앞여밈
front_belt_rear_dress_zip|a red belt around the dress front; that dress's rear zipper|드레스 앞 허리의 붉은 벨트; 같은 드레스의 뒤지퍼
neck_scarf_separate_hair_ornament|an upright end on the neck scarf; a distinct ornament attached in the same wearer's hair|목 스카프의 위로 선 끝; 같은 착용자의 머리카락에 붙은 구분되는 장식
chef_overlapping_double_front|overlapping chef-jacket fronts; two button rows on those fronts|겹치는 조리복 재킷 앞판; 그 앞판 위 두 줄 단추
white_collar_cuffs_black_dress|a white collar on the black dress; white cuffs on its sleeves|검정 드레스의 흰 칼라; 같은 드레스 소매의 흰 커프
sailor_lines_follow_collar|a broad sailor collar; parallel stripes along its edges|폭넓은 세일러 칼라; 그 가장자리를 따르는 나란한 줄
gown_separate_selected_cap|a selected academic cap with its own crown edge; a separate gown on that wearer's shoulders|자체 정수리 경계의 선택한 학위 모자; 같은 착용자의 어깨 위 별도 가운
habit_hood_separate_waist_cord|a distinct hood belonging to the habit; a separate cord around its waist; the cord ends below its tie|수도복에 속한 구분되는 후드; 그 허리를 둘러싼 별도 끈; 묶임 아래로 남는 끈 끝
kesa_patchwork_outer_border|joined rectangular robe patches; a continuous border around their outer edge|이어진 직사각 가사 조각; 그 바깥 가장자리의 연속된 테두리
white_top_red_hakama_layers|a white upper garment with its own hem; a separate red hakama below it|자체 밑단이 있는 흰색 상의; 그 아래 입은 별도 붉은 하카마
grey_yoke_black_body_color_neck|a grey shoulder yoke on a black jacket; its separate colored inner collar|검정 재킷의 회색 어깨 요크; 그 안의 별도 색 있는 속깃
lapel_chain_separate_inner_neck|a chain attached to the burgundy lapel; a separate raised undershirt collar behind it|버건디 라펠에 붙은 사슬; 그 뒤 별도로 올라온 속셔츠 깃
work_suit_narrow_shoulder_color|one continuous work suit; narrow contrasting shoulder trim|하나로 이어진 작업복 몸체; 그 어깨의 가는 배색 장식
hood_belt_cape_layers|a separate outer hood; a cape supported by the waist belt; the cape's independent lower edge|복장 바깥의 별도 후드; 허리 벨트에 지지된 케이프; 그 케이프의 독립된 아랫단
"""

EXISTING = r"""
costume_ccx_cc01_01|apron shoulder straps attached to its bib|앞치마 가슴판에 이어진 어깨끈
costume_ccx_cc01_02|the apron waist band with separate side ties|별도 옆 묶임이 있는 앞치마 허리 띠
costume_ccx_cc01_03|the apron hem above a separate dress hem|별도 드레스 밑단 위의 앞치마 밑단
costume_ccx_cc02_01|a short-front tailcoat with two long rear tails|앞이 짧고 뒤자락 두 개가 긴 연미복
costume_ccx_cc02_02|an independent buttoned waistcoat inside open coat lapels|열린 코트 라펠 안의 독립된 단추 조끼
costume_ccx_cc03_01|a broad sailor collar across both shoulders and upper back|양 어깨와 등 위쪽을 가로지르는 넓은 세일러 칼라
costume_ccx_cc03_02|a separate knotted chest ribbon beneath the collar|칼라 아래의 별도로 매듭진 가슴 리본
costume_ccx_cc05_01|epaulettes on separate jacket shoulder bases|재킷의 별도 어깨 밑판 위 견장
costume_ccx_cc05_02|a braided chest cord attached at both jacket ends|재킷 양끝에 연결된 땋은 가슴 끈
costume_ccx_cc13_01|dark flexible joint cloth between separate armor plates|분리된 갑주 판 사이의 어두운 유연한 관절 천
costume_ccx_cc13_02|overlapping armor edges leave an articulated joint gap|겹치는 갑주 가장자리가 남긴 움직이는 관절 틈
costume_ccx_cc13_03|metallic-painted plates beside matte joint fabric|무광 관절 직물 옆의 금속풍으로 칠한 판
costume_ccx_cc15_01|a separate cloth neck layer below the helmet rim|헬멧 테두리 아래의 별도 천 목층
costume_ccx_cc15_02|a bounded dark visor within the helmet shell|헬멧 외피 안의 경계 있는 어두운 바이저
costume_ccx_cc17_01|two faux-fur ears rooted in one headband|한 머리띠에 밑동이 붙은 모피 모조 귀 두 개
costume_ccx_cc17_02|the artificial ear's contrast inner panel separate from the wig|가발과 분리된 인공 귀의 배색 안쪽 면
costume_ccx_cc26_01|vertical stitched channels within the separate corset|별도 코르셋 안에 놓인 세로 봉제 채널
costume_ccx_cc26_02|crossed back lacing between the corset's opposing loop rows|코르셋 양쪽 고리 줄 사이의 교차 뒷끈
costume_ccx_cc32_01|localized edge fraying beside an intact garment panel|온전한 의복 패널 옆의 국소 가장자리 헤짐
costume_ccx_cc32_02|a repair patch stitched around its own perimeter|자체 둘레를 따라 꿰맨 수선 패치
costume_ccx_cc35_01|thin luminous trim along selected costume plate edges|선택한 코스튬 판 경계의 가는 발광 장식
costume_ccx_cc35_02|non-glowing cloth next to localized costume lights|국소 코스튬 조명 옆의 빛나지 않는 천
costume_ccx_cc36_01|visible gloved finger contact around the prop handle|소품 손잡이 주위의 보이는 장갑 손가락 접촉
costume_ccx_cc36_02|the prop handle continuously joins one sculpted body|하나의 조형 몸체에 연속해서 이어진 소품 손잡이
clothing_ct028_v1|reflective bands sewn across the work jacket|작업 재킷을 가로질러 봉제된 반사 띠
clothing_ct041_v2|a rectangular sailor-collar back panel|직사각형 세일러 칼라 등 패널
clothing_ct043_v1|a pleated cloth ruff encircling the neck|목을 둘러싼 주름 천 러프
clothing_ct141_v1|three linked kerosang bridging the kebaya front edges|케바야 앞판 가장자리를 잇는 연결된 케로상 세 개
clothing_ct141_v2|a separate kebaya top over a wrapped sarong|감아 입은 사롱 위의 별도 케바야 상의
"""

def read(p): return json.loads(p.read_text())
def digest(v): return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def add(seq,values):
    result=[]
    for value in values:
        if value not in seq:
            seq.append(value);result.append(value)
    return result

def main():
    paths=[ASSETS/p for p in [r["path"].split("/")[-1] for r in read(HERE/"INTEGRATION-LEDGER.json")["source_files"]]]
    docs={p:read(p) for p in paths};original=copy.deepcopy(docs)
    baseline=HERE/"before-natural-enhancement";baseline.mkdir(exist_ok=True)
    for p in paths:
        dest=baseline/p.name
        if not dest.exists():dest.write_bytes(p.read_bytes())
    profiles={p["id"]:(path,p) for path,d in docs.items() for p in d.get("profiles",[])}
    entries={e["id"]:(path,e) for path,d in docs.items() for rows in d.get("slots",{}).values() for e in rows}
    ledger=read(HERE/"INTEGRATION-LEDGER.json")
    old_ledger=HERE/"INTEGRATION-LEDGER-initial.json"
    if not old_ledger.exists():old_ledger.write_bytes((HERE/"INTEGRATION-LEDGER.json").read_bytes())
    events=[]
    def equivalents(pid,cid,en,ko,units,kunits):
        pp,p=profiles[pid];cp,e=entries[cid]
        assert len(p["authored_components"]["components"])==len(units)==len(kunits),pid
        additions=add(p["semantics"].setdefault("paraphrase_examples",[]),[en,ko])
        add(p["concept_candidate"].setdefault("concept_terms",[]),[en,ko,*units,*kunits])
        for c,u,k in zip(p["authored_components"]["components"],units,kunits):
            add(c["match_terms"],[u,k]);add(c["evidence_terms"],[u,k])
        add(e.setdefault("paraphrases",[]),[en,ko]);add(e.setdefault("keywords",[]),[en,ko,*units,*kunits])
        e["embedding_text"] += " | " + " | ".join(v for v in [en,ko] if v not in e["embedding_text"])
        for r in ledger["candidate_changes"]:
            if r["id"]==cid:add(r["added_paraphrases"],[en,ko])
        events.append({"profile_id":pid,"candidate_id":cid,"full_equivalents":additions,"components_en":units,"components_ko":kunits,"hard_aliases_changed":False})
    for line in EXISTING.strip().splitlines():
        pid,en,ko=line.split("|")
        cid=pid.removeprefix("costume_") if pid.startswith("costume_") else pid.replace("clothing_","clt_",1)
        equivalents(pid,cid,en,ko,[en],[ko])
        r=next(r for r in ledger["existing_profiles"] if r["id"]==pid);add(r["added_paraphrases"],[en,ko]);r["component_alternatives"].append([en,ko])
    for line in NATURAL.strip().splitlines():
        slug,en,ko=line.split("|");units=[x.strip() for x in en.split(";")];kunits=[x.strip() for x in ko.split(";")]
        equivalents("uniform_"+slug,"unif_"+slug,en,ko,units,kunits)
    # Generic one-piece and closure expressions remain separate necessary groups.
    pid="uniform_continuous_coverall_front_closure";p=profiles[pid][1];e=entries["unif_continuous_coverall_front_closure"][1]
    variants=[["one-piece flight suit","one-piece jumpsuit","one-piece coverall","일체형 비행복","원피스 작업복"],["zipped center front","central front zipper","center-front closure","같은 일체복의 앞여밈","중앙 앞지퍼"]]
    for c,terms in zip(p["authored_components"]["components"],variants):
        add(c["match_terms"],terms);add(c["evidence_terms"],terms)
    add(e["keywords"],[*variants[0],*variants[1]])
    # Newly confirmed U10: Met's actual ensemble explicitly lists full-cut
    # trousers with cuff ties. This is a selected shape, not a universal Zouave.
    template=copy.deepcopy(profiles["uniform_separate_flared_trouser_hems"][1])
    pid="uniform_full_trousers_gathered_cuffs";cid="unif_full_trousers_gathered_cuffs"
    assert pid not in profiles and cid not in entries
    en="the two full-cut trouser legs retain distinct loose volumes; their lower cloth gathers into separate narrow cuff boundaries"
    ko="넓게 재단된 두 바지통이 각각의 헐렁한 부피를 유지한다; 아래 천이 각각의 좁은 커프 경계로 모인다"
    units=[x.strip() for x in en.split(";")];kunits=[x.strip() for x in ko.split(";")]
    soft=["voluminous trouser legs; gathered trouser cuffs","부피 큰 각각의 바지통; 모여 좁아진 각각의 바지 커프"]
    effects=[{"dimension":"appearance","target":"main_subject","property":"wardrobe.details.gathered_trouser_cuffs"}]
    template["id"]=pid;template["activation"]["exact_terms"]=[en,ko];template["activation"]["hard_activation"]["required_any_groups"][0]["any_terms"]=[en,ko]
    template["semantics"].update({"definition":en,"paraphrase_examples":soft,"visual_components":units,"contrast_examples":["Straight trouser legs, a skirt or a gaiter on a different wearer do not prove two full leg volumes gathering into their own cuffs."]})
    template["concept_candidate"].update({"concept_terms":[en,ko,*soft,*units,*kunits],"affected_properties":effects})
    template["reject_substitutes"]=["Do not substitute straight trousers, a single skirt silhouette or an unrelated gaiter for the gathered lower boundaries of two full trouser legs."]
    short_groups=[["voluminous trousers","baggy trousers","full-cut trouser legs","넓은 바지통"],["gathered trouser cuffs","gathered toward the ankles","trousers gathered at the cuffs","모여 좁아진 바지 커프"]]
    for i,(c,u,k) in enumerate(zip(template["authored_components"]["components"],units,kunits),1):
        phrases=list(dict.fromkeys([u,k,soft[0].split(";")[i-1].strip(),soft[1].split(";")[i-1].strip(),*short_groups[i-1]]))
        c.update({"match_terms":phrases,"evidence_terms":phrases,"instruction":"Keep this selected relation literal on the declared wearer: "+u+".","render_gate":{"id":f"vo_{pid}_{i}","review_scale":"native","description":u+". Inspect the original image at native resolution on the same wearer; partial or wrong-owner evidence fails and hidden connections are unobservable."}})
    pp=ASSETS/"photo_prompt_visual_obligations_clothing_structure.json";cp=ASSETS/"photo_prompt_clothing_structure_extension.json"
    docs[pp]["profiles"].append(template)
    candidate={"id":cid,"ko":ko,"en":en,"weight":0.45,"tags":["human","observable_relation"],"for_any":["human"],"aliases":[],"paraphrases":[en,ko,*soft],"keywords":[*units,*kunits,*short_groups[0],*short_groups[1]],"embedding_text":" | ".join([en,ko,*soft]),"concept_units":units,"relations":[{"id":"declared_owner","type":"declared_owner_scope","subject":"wardrobe.details.gathered_trouser_cuffs","object":"main_subject"},{"id":"gathered_lower_boundary","type":"gathered_into","subject":"the two full trouser leg volumes","object":"their own narrow cuff openings"}],"affected_dimensions":["appearance"],"affected_properties":effects,"core_assertion_discovery":True}
    docs[cp]["slots"]["garment_detail"].append(candidate)
    ledger["new_profiles"].append({"atom_id":"U10","id":pid,"candidate_id":cid,"profile_file":pp.name,"candidate_file":cp.name,"slot":"garment_detail","components":2,"canonical_components":units,"alternative_components":[x.strip() for x in soft[0].split(";")],"alternative_components_ko":[x.strip() for x in soft[1].split(";")],"source_ids":["S06"],"source_scope":"Additional primary verification confirms full-cut pants with cuff ties; only the selected visible gathering relation is asserted."})
    ledger["candidate_changes"].append({"id":cid,"profile_id":pid,"file":cp.name,"slot":"garment_detail","new":True,"added_paraphrases":[en,ko,*soft]})
    r=next(r for r in ledger["research_dispositions"] if r["atom_id"]=="U10");r.update({"disposition":"new_bounded_relation","profile_ids":[pid],"additional_primary_verification":"additional-source-verification.json"})
    for path,doc in docs.items():
        if doc==original[path]:continue
        if "slots" in doc:
            prior=doc["maintenance_ref"];plain=copy.deepcopy(doc);plain.pop("maintenance_ref",None)
            record_id=path.stem+"-uniform-natural-equivalents-20261004"
            record={"schema_version":"photo-extension-maintenance/v1","record_id":record_id,"authored_source_sha256":digest(plain),"prior_maintenance_ref":prior,"scope":"Concise soft relation descriptions preserve exact activation, definitions, effects and native gate duties. U10 additionally verified through the Met ensemble record.","candidate_changes":[r for r in ledger["candidate_changes"] if r["file"]==path.name]}
            dest=ROOT/"docs/research-evidence/photo-prompt/extension-maintenance"/(record_id+".json");dest.write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n")
            doc["maintenance_ref"]={"contract_version":"photo-extension-maintenance-ref/v1","record_id":record_id,"sha256":digest(record)}
        assert read(path)==original[path],"Concurrent source mutation: "+str(path)
        path.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n")
        next(r for r in ledger["source_files"] if r["path"]==str(path.relative_to(ROOT)))["after_sha256"]=hashlib.sha256(path.read_bytes()).hexdigest()
    ledger["counts"].update({"new_profiles":len(ledger["new_profiles"]),"new_candidates":sum(r["new"] for r in ledger["candidate_changes"]),"existing_profile_full_paraphrases_added":sum(len(r["added_paraphrases"]) for r in ledger["existing_profiles"]),"new_profile_full_paraphrases":sum(len(p["semantics"]["paraphrase_examples"]) for d in docs.values() for p in d.get("profiles",[]) if p["id"].startswith("uniform_"))})
    ledger["natural_enhancement"]={"soft_full_equivalents_added":sum(len(r["full_equivalents"]) for r in events),"event_record":"NATURAL-ENHANCEMENT-LEDGER.json","exact_aliases_from_evaluation_cases":0}
    (HERE/"NATURAL-ENHANCEMENT-LEDGER.json").write_text(json.dumps({"schema_version":"uniform-natural-enhancement/v1","events":events,"preserves":"Every original exact activation, evidence minimum, gate, definition and property effect. New short descriptions are advisory; pixel ownership remains mandatory."},ensure_ascii=False,indent=2)+"\n")
    (HERE/"INTEGRATION-LEDGER.json").write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(ledger["counts"],ensure_ascii=False))

if __name__=="__main__":main()
