"""Prepare exact, hash-bound corrections; this never writes operating sources."""
import copy
import json
import sys
from sample import HERE, SKILL, refs

sys.path.insert(0, str(SKILL / "scripts"))
import photo_candidate_corpus as c
import photo_global_index as index


def replace_strings(value, replacements):
    if isinstance(value, str):
        for before, after in replacements.items():
            value = value.replace(before, after)
        return value
    if isinstance(value, list):
        return [replace_strings(item, replacements) for item in value]
    if isinstance(value, dict):
        return {key: replace_strings(item, replacements) for key, item in value.items()}
    return value


def pointers(value, needle, path=""):
    if value == needle:
        yield path
    if isinstance(value, dict):
        for key, nested in value.items():
            yield from pointers(nested, needle, path + "/" + key.replace("~", "~0").replace("/", "~1"))
    elif isinstance(value, list):
        for number, nested in enumerate(value):
            yield from pointers(nested, needle, path + "/" + str(number))


def main():
    source = c.validate(c.load(SKILL / "assets"))
    samples = {row["number"]: row for row in map(json.loads, (HERE / "SAMPLE.jsonl").read_text().splitlines())}
    proposed = copy.deepcopy(source)
    changes = []

    def propose(cid, after, reason, obligations):
        before = source["candidates"][cid]
        assert before["id"] == after["id"] and before != after
        assert before["conditions"] == after["conditions"]
        assert before["effects"] == after["effects"]
        assert before["provenance"] == after["provenance"]
        assert set(refs(before["content"])) == set(refs(after["content"]))
        proposed["candidates"][cid] = after
        changes.append({"candidate_id": cid, "before_record_sha256": c.digest(before),
            "after_record_sha256": c.digest(after), "before": before, "after": after,
            "reason_ko": reason, "required_before_application": obligations,
            "incoming_policy_references": list(pointers(source["policies"], cid)),
            "native_applied": False, "semantic_decision": "resolved",
            "runtime_validation": "stage05_required"})

    cid = samples[116]["candidate_id"]
    after = copy.deepcopy(source["candidates"][cid])
    after["content"]["ko"] = "중성적이고 차가운 분위기의 표현"
    after["content"]["aliases"] = [x for x in after["content"]["aliases"] if x != "boyish cool"]
    after["content"]["keywords"] = [x for x in after["content"]["keywords"] if x != "boyish"]
    propose(cid, after, "androgynous와 boyish를 같은 뜻으로 취급하지 않고 한국어와 positive alias를 일치시킨다.",
        ["새 검색 본문·벡터를 갱신한다.", "표현 분위기로 성별 정체성·성·성격을 추정하지 않는다."])

    cid = samples[273]["candidate_id"]
    after = copy.deepcopy(source["candidates"][cid])
    english = ("physical mixed-media carriers show tape stretch, antistatic packaging, and distinct colored custody tabs; "
        "only when an already-declared recorded playback is visible, signal dropout appears in that playback image rather than on the physical tape surface")
    korean = "물리 혼합 매체 지지체의 테이프 늘어짐·정전기 방지 포장·구별 색 보관 탭; 이미 선언된 기록 재생 영상이 보이는 경우에만 신호 dropout을 재생 영상 면에 두고 테이프 표면 결함으로 표현하지 않는다"
    after["content"].update(en=english, ko=korean, aliases=[english, korean], embedding_text=english)
    propose(cid, after, "물리 테이프 지지체와 재생 신호의 dropout 소유자를 분리하고 새 재생 장치를 발명하지 않는다.",
        ["물리 carrier 효과와 조건부 playback-image 효과를 각각 소유자·속성으로 명시한다.",
         "실제 선택한 분기의 효과만 adoption 검사에 들어가도록 계약과 검증을 갖춘 뒤 적용한다.", "긍정 본문 변경에 맞춰 벡터를 갱신한다."])

    bundle = samples[474]["candidate_id"]
    profile = "cand_0754e4248862538eb282a8451f28d4d7"
    replacements = {
        "a small handled cup rests on its own matching saucer": "a small handled cup has just reached its own matching saucer at the end of lowering",
        "the subject lowers the cup toward the saucer": "the subject completes lowering the cup as its base reaches the matching saucer",
    }
    for cid in (bundle, profile):
        after = copy.deepcopy(source["candidates"][cid])
        after["content"] = replace_strings(after["content"], replacements)
        propose(cid, after, "같은 순간에 잔이 정지 지지되어 있고 아직 공중에서 내려오는 모순을 접촉 시작 순간으로 정렬한다.",
            ["원래 손잡이 접촉·반대 손 비접촉·방 배치와 모든 member 조건을 보존한다.",
             "참조된 일반 lowering/rest 후보는 더 넓은 뜻을 보존하고 이 묶음의 선택 시점에 함께 실현되는지 검증한다.",
             "프로필의 match/evidence/render gate 문구도 동일 보정하고 검색·구성·시점 회귀를 검증한다."])

    cid = samples[480]["candidate_id"]
    after = copy.deepcopy(source["candidates"][cid])
    after["content"]["components"] = [
        {"id": "visible_layer_boundary", "concept_units": ["Record only the visible boundary between the two textile layers of the one selected garment."], "minimum_realizations": 1},
        {"id": "one_complete_garment_alternative", "concept_units": [
            "One dress has a pink inner sheath beneath its black lace outer layer; its lace openings reveal that same dress's pink inner layer.",
            "One bustier has black lace over its nude-colored jersey inner layer; its bodice boundary belongs to that same bustier."], "minimum_realizations": 1},
    ]
    after["content"]["relations"] = [{"id": "sff_pack_extra_xq13_one_alternative",
        "subject": "one selected complete dress OR bustier alternative",
        "type": "one_complete_alternative_with_same_owner",
        "object": "preserve the selected garment's own inner-layer color and material"}]
    after["content"]["confusion_boundaries"] = [
        "Do not impose both pink sheath and nude jersey on one garment.",
        "Do not combine the dress's inner color with the bustier's owner or material.",
    ]
    propose(cid, after, "분홍 시스 드레스와 누드 저지 버스티에의 두 원전을 각각 완전한 대안으로 보존한다.",
        ["구성 시 완전한 대안 한 개를 명시 선택하고 member별 조건·효과·색 잠금을 그 선택에 귀속시킨다.",
         "현재 native source shape validation 통과는 대안 선택의 runtime 의미 검증이 아니다.",
         "서로 다른 owner/color를 합칠 수 없다는 회귀와 선택 분기 효과 검사 후에만 적용한다.",
         "문장·관계·구성 검증 계약과 검색 본문·벡터를 같이 갱신한다."])

    for number in (497, 503, 508, 517, 519, 522):
        cid = samples[number]["candidate_id"]
        after = copy.deepcopy(source["candidates"][cid])
        after["record_kind"] = "diagnostic"
        propose(cid, after, "구체 시각 값 없는 guard·조율·연속성 작성 규칙을 diagnostic으로 분류한다.",
            ["원래 ID·본문·가족·topic·모든 incoming 참조를 유지한다.",
             "실행 graph의 diagnostic/router 계약에 맞춰 참조 소비자를 갱신하고 긍정 검색에서 제외되는지 검증한다.",
             "positive 예외 대장과 index/runtime closure를 갱신한다."])
    c.validate(proposed)
    report = {"schema": "photo-slot-pilot-correction-proposals/v1", "source_sha256": c.digest(source),
        "projected_corpus_sha256": c.digest(proposed), "proposal_count": len(changes),
        "projected_source_shape_and_reference_validation": "pass",
        "projected_positive_count": len(index.documents(proposed)), "native_positive_count": len(index.documents(source)),
        "native_sources_written": False, "changes": changes,
        "boundary": "Resolved semantic corrections with exact projected records; branch/runtime/effect implementation is required in stage 5 before stage 6 tag application."}
    (HERE / "CORRECTION-PROPOSALS.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ("proposal_count", "projected_positive_count", "native_positive_count", "native_sources_written")}))


if __name__ == "__main__":
    main()
