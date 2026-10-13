"""Offline, reproducible migration of authored roles; no runtime aliases.

The reviewed exceptions below name exact immutable source identities. The
remaining bindings use the stage-0 semantic role decision, not keyword tagging.
This is existing-relation migration, not the later full-corpus enrichment.
"""
import copy
import argparse
from itertools import product
import json
from pathlib import Path
import sys
import uuid
import subprocess

from upgrade_contract import ROOT, OUT, ASSETS, write_source
sys.path.insert(0, str(ASSETS.parent / "scripts"))
import photo_candidate_corpus as c
import photo_global_index as index

# Short source identities are resolved uniquely and stored as full IDs in the
# ledger. Lists were reviewed against the frozen EN/KO bodies and owned effects.
OVERRIDES = {}
def assign(role, short_ids):
    for short in short_ids.split():
        if short in OVERRIDES:
            raise ValueError("duplicate reviewed exception " + short)
        OVERRIDES[short] = role.split(",")

# The retired quality bucket mixes recorded detail, skin, signal and staging.
assign("image_artifact", "01ee75a5 0f493a95 1b4dcf56 47558426 4c919787 9510d7cf ad639903 c9e24ed6 e5e6d807 e675a56d ed1064de f2e2648f")
assign("image_artifact,color_grading", "657829ef cbfb3a86 f41d8bcc fc7da674")
assign("skin_finish", "28f1115c")
assign("grain_profile,image_detail", "298ace28")
assign("composition", "2fed9cfb")
assign("staging_degree", "347f6f91 42900109 720aeacf e7b59808")
assign("capture_context", "4018e87b 80194aa5")
assign("lens_artifact", "899e6c9a c94d88f7")
assign("image_detail", "00452495 1652909e 98c31436 9e6e9ad9 dd1a8d43")
assign("attire_context", "620e884d")
# Frame anchors are actual arrangements, optical depth, crop or grain.
assign("spatial_depth", "3d4e6285")
assign("depth_of_field", "6b503023 dd3ca134")
assign("subject_framing", "9fdc903f")
assign("grain_profile", "bf82e071")
assign("composition,image_artifact", "4408dc45")
assign("composition,reality_anchor", "8f34fb60 9e8b554e")
# Relation statements retain the participants; no feeling is inferred from gap.
assign("proxemics,body_orientation,action", "0266ffb6")
assign("proxemics,body_orientation,participant_role", "2bcbae3f")
assign("proxemics,body_orientation,reflection_logic", "6b1e280d")
assign("proxemics,body_orientation", "9fdefaa3")
assign("proxemics,relational_action", "b7ff7d0e")
# Image motion, camera stability and actual physical motion are distinct.
assign("camera_movement,motion_rendering", "192e6d80 66c55c10 889c67f7 89ab046c ccdfa70e")
assign("camera_movement", "67eec20d 84752600 f4d0c3a0")
assign("camera_direction,staging_degree", "43172dfa")
assign("reflection_logic", "5414f1ce")
assign("image_artifact,motion_rendering", "53f3d85c 6d3e607b e2faf628")
assign("motion_rendering", "02ed6951 0bae0f54 104be516 18781de6 1ec1d06d 2250c7f7 2a0f6456 383cb3ba 496e7e97 4a7adbfe 4f65fdf2 5fdabeca 67ad6897 895537ab 9c3d975a b0164ba1 be1da890 cd0dfc14 d06b6579 d0d29140 d740bbca f31a36db")
# One former air entry actually describes still hanging material.
assign("physical_motion", "7660d708")
# The former medium bucket includes genres, purposes and device configurations.
assign("capture_configuration,camera_type", "3c3310d0 41862287 46b02e00 49365c86 972386b6 daf9569c dc2cdcdc dfb17c92 feaad513")
assign("capture_context", "0edf0006 139e706d 6e537b2f 80cfc519 8c0ac8b6 976b2e22 a2baf2ad eef70e66 e8e23c55 f7f30173 b7ea6fbd 4d054ff5 ec6a22ae 08b587b9")
assign("capture_context,staging_degree", "3350e77a 79ec3322 87bbc626 bedd5645 f579376f")
assign("capture_configuration,medium", "f085ef8b")
assign("genre", "03f19e48 09fcdd8a 1514238f 1c9ec7b3 1e3bb6e7 20933e7b 2ccc3dcd 3073fe1d 3e02d2ad 41f04e08 429cc171 43abdc16 5958f24b 622483ef 6d430ac9 7531a55a 85fa5c84 86651b59 9b3a0c0f 9c2db778 9e0deda9 b53efefa cd760d7d d1a04691 eea12c19 f28a512f f3b31ad9 f85f192b fc225055")
# Bare world rules and purpose declarations are not photographic genres.
assign("genre", "d0ea20c7")
assign("aesthetic_trend", "28a68e06 153334cd 4adb20ad 627460c3")
assign("capture_context", "08504a40 6c386cfb 79db97e6 880d166a d08324f2")
assign("adult_presentation_context,genre", "1f55e995")
assign("fetish_styling,genre", "7e70e3f5")
# Texture names referring to image plane, optical path and airborne carriers.
assign("image_artifact", "140d3835 2facd459 af526eea cba0c85c e4f70575 e65b54b5 09dc4590 2d705d2d e288d532")
assign("grain_profile", "4f124e82 a19f2d47 b92d6950")
assign("image_artifact,grain_profile", "8b62a60a")
assign("image_detail", "8c62acf4 134ce5bc bcd97eab")
assign("image_detail,capture_context", "f43395d6 d9070fa6")
assign("lens_artifact", "08c01879 9cecbe02 e8195c29 0cb018e7 6da11235")
assign("motion_rendering", "0a7c8f38")
assign("ambient_particle", "20520367 78899977 a00b9322 cfa2f168 db199967 2ceb8303 3a72f448")
assign("atmospheric_medium", "8cb61d10")
assign("weather", "b959f84b")
assign("light_shape", "67f3debc")
assign("light_type", "9a38fa3d")
assign("medium", "5bf749ed fbf5f35d")
assign("composition", "ec876d95")
assign("skin_finish", "b3ffab0b")
assign("body_hair,texture", "0b7a6fb3 e5331758")
assign("species_marker,texture", "8baa17bf")
assign("wardrobe_layering,texture", "541d9bf4")
# Exposure, recorded clipping and bloom are not incident light level.
assign("exposure", "01afbd0f 0fe30f6d 12346019 1b2f62bc 2100719e 2a5b0428 32e0ec94 3eddae7b 550da252 977b3544 d2008d7c d880e0ff")
assign("lens_artifact", "147d8f99 8c3daa6d")
# Personal presentation examples that actually carry another declared meaning.
assign("gender_presentation,presentation_style", "7e3ae8f7")
assign("wardrobe_style,wardrobe_layering", "e6dbc6f1")
assign("surreal_concept", "957d6aa4")
assign("fetish_styling,presentation_style", "c7df2f75")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--from-commit',help='Explicit offline native V2 checkpoint; its full source hash must equal stage 2')
    args=parser.parse_args()
    if args.from_commit:
        def committed(relative):
            return c.decode(subprocess.check_output(['git','show',args.from_commit+':skills/photo-prompt-image-generator/assets/'+relative],cwd=ROOT))
        manifest=committed(c.MANIFEST_NAME)
        if manifest['schema']!=c.MANIFEST_SCHEMA:raise ValueError('only a native V2 checkpoint is accepted')
        source={'schema':c.SCHEMA,**{kind:{} for kind in c.MODULE_SCHEMAS}}
        for module in manifest['modules']:
            payload=committed(module['file']);kind=module['kind']
            if payload['schema']!=c.MODULE_SCHEMAS[kind]:raise ValueError('native module checkpoint required')
            if set(source[kind])&set(payload[kind]):raise ValueError('duplicate checkpoint owner')
            source[kind].update(payload[kind])
        c.validate(source)
    else:
        source = c.load(ASSETS)
    verification = json.loads((OUT / "STAGE02-SOURCE-VERIFICATION.json").read_text())
    if c.digest(source) != verification["corpus_after_sha256"]:
        raise ValueError("stage-2 input changed; migration is not a compatibility adapter")
    before = copy.deepcopy(source)
    target = json.loads((OUT / "TARGET-CATALOG.json").read_text())
    decisions = json.loads((OUT / "SLOT-DECISIONS.json").read_text())
    source["slot_catalog"] = target
    catalog_refinements=[]
    native_paths={'texture':['surface_structure','surface.texture'],
        'surface_material':['surface.optical_response'], 'capture_configuration':['capture.mode'],
        'motion_rendering':['optical.motion'], 'camera_distance':['viewpoint.distance']}
    for tag,values in native_paths.items():
        spec=target[tag];original=list(spec['property_prefixes'])
        spec['property_prefixes']=list(dict.fromkeys(original+values))
        catalog_refinements.append({'slot':tag,'before':original,'after':spec['property_prefixes'],
            'reason':'accept the already authored native property of the same owner and meaning; not a retired slot alias'})
    short_lookup = {cid[5:13]: cid for cid in source["candidates"]}
    assert len(short_lookup) == len(source["candidates"])
    assert set(OVERRIDES) <= set(short_lookup)
    overrides = {short_lookup[k]: v for k,v in OVERRIDES.items()}
    review_input = [json.loads(line) for line in (OUT / "MIGRATION-REVIEW-INPUT.jsonl").read_text().splitlines()]
    review_ids = {r["candidate_id"] for r in review_input}
    assert set(overrides) <= review_ids
    manifest = c.decode((ASSETS / c.MANIFEST_NAME).read_bytes())
    owners = {bid: m["file"] for m in manifest["modules"] if m["kind"] == "slot_bindings"
              for bid in c.decode((ASSETS / m["file"]).read_bytes())["slot_bindings"]}
    final, new_owners, ledger, mapping, pairs = {}, {}, [], {}, {}
    for bid,binding in sorted(before["slot_bindings"].items()):
        cid, old = binding["candidate_id"], binding["slot_id"]
        roles = (overrides.get(cid) if cid in review_ids and any(r['candidate_id']==cid and r['old_slot']==old for r in review_input) else None) or (["image_detail"] if old == "quality" else
                              ["subject_framing", "composition"] if old == "partner_framing" else
                              [decisions[old]["targets"][0]])
        if old == "partner_framing" and cid.startswith("cand_96236df9"):
            roles = ["composition", "offscreen_context"]  # implied partner does not add a visible person
        output = []
        for position, role in enumerate(roles):
            if role not in target: raise ValueError("unknown target role " + role)
            row = copy.deepcopy(binding)
            key = cid, role
            row["slot_id"] = role
            row["semantic_role"] = target[role]["semantic_role"]
            row["id"] = bid if position == 0 else "bind_" + uuid.uuid5(uuid.NAMESPACE_URL, "photo-role:" + cid + ":" + role).hex
            if key in pairs:
                prior = final[pairs[key]]
                assert {k:v for k,v in row.items() if k!='id'} == {k:v for k,v in prior.items() if k!='id'}, "different relationship contracts cannot merge silently"
                row = prior
            else:
                pairs[key] = row["id"]; final[row["id"]] = row
                new_owners[row["id"]] = owners[bid]
            output.append(row["id"])
        mapping[bid] = output
        ledger.append({"old_binding_id": bid, "candidate_id": cid, "old_slot_id": old,
            "new_binding_ids": output, "new_slot_ids": roles,
            "reason": "exact-body boundary review" if cid in overrides or old in {"quality","partner_framing"} else decisions[old]["rationale"],
            "review_type": "existing-binding semantic migration; not full-corpus enrichment",
            "source_conditions_sha256": c.digest(before["candidates"][cid]["conditions"]),
            "role_conditions_preserved": True})
    source["slot_bindings"] = final
    # Exact binding references keep their previously declared member contract;
    # split relations have a primary relation plus additional role presentations.
    def refs(value):
        if isinstance(value,str):return mapping[value][0] if value in mapping else value
        if isinstance(value,list):return [refs(v) for v in value]
        if isinstance(value,dict):return {refs(k):refs(v) for k,v in value.items()}
        return value
    source["candidates"] = refs(source["candidates"])
    source["policies"] = refs(source["policies"])
    coherence = source["policies"].get("coherence_rules", {})
    for key in ["slot_conflicts", "slot_context_rules"]:
        expanded = []
        for row in coherence.get(key,[]):
            if key == "slot_context_rules":
                row["slots"] = sorted({r for old in row["slots"] for r in decisions.get(old,{"targets":[old]})["targets"]})
                expanded.append(row)
            else:
                left = decisions.get(row["left"]["slot"], {"targets":[row["left"]["slot"]]})["targets"]
                right = decisions.get(row["right"]["slot"], {"targets":[row["right"]["slot"]]})["targets"]
                for a,b in product(left,right):
                    item=copy.deepcopy(row);item["left"]["slot"]=a;item["right"]["slot"]=b;expanded.append(item)
        if key in coherence:coherence[key]=expanded
    # Properties have semantic names, independent of role IDs. Keep authored
    # properties except the retired generic quality property; it cannot remain
    # the supposed proof of sixteen different image/body/optical properties.
    effect_changes = []
    primitive = {"image_detail":("style","image.detail","image_plane"),
        "image_artifact":("style","image.artifact","image_plane"),
        "color_grading":("color","image.grading","image_plane"),
        "lens_artifact":("camera","optics.artifact","optical_path"),
        "grain_profile":("camera","image.grain","image_plane"),
        "skin_finish":("appearance","skin.finish","main_subject"),
        "staging_degree":("role","capture.staging","declared_scene"),
        "capture_context":("camera","capture.context","declared_capture"),
        "composition":("composition","layout.layering","image_plane"),
        "atmospheric_medium":("atmosphere","air.medium","scene_air"),
        "attire_context":("appearance","wardrobe.context","main_subject")}
    for old_row in review_input:
        cid = old_row["candidate_id"]; record=source["candidates"][cid]
        if old_row["old_slot"] == "quality":
            effects=copy.deepcopy(record["effects"])
            roles=next(row["new_slot_ids"] for row in ledger if row["old_binding_id"]==old_row["binding_id"])
            props=[p for p in effects["properties"] if p["property"]!='rendering.quality']
            for role in roles:
                dimension,path,owner=primitive[role]
                prop={"dimension":dimension,"property":path,"target":owner}
                if prop not in props:props.append(prop)
            # Preserve other authored dimensions/properties rather than infer
            # freedom solely from the chosen tag.
            effects["properties"]=props
            effects["dimensions"]=sorted(set(effects["dimensions"])|{p["dimension"] for p in props})
            if effects!=record["effects"]:
                effect_changes.append({"candidate_id":cid,"before":record["effects"],"after":effects,
                    "reason":"replace generic quality effect with the recorded body/image/optical property"})
                record["effects"]=effects
    for b in final.values():
        if b["slot_id"] in {"adult_presentation_context","fetish_styling"}:
            record=source["candidates"][b["candidate_id"]]
            record["conditions"]["requires_adult_context"]=True
            record["conditions"].setdefault("for_any",["human"])
    assert set(before["candidates"])==set(source["candidates"])
    assert len(ledger)==len(before["slot_bindings"])
    assert all(index.text(before["candidates"][cid])==index.text(record) for cid,record in source["candidates"].items())
    c.validate(source)
    report={"verified":True,"before_corpus_sha256":c.digest(before),"after_corpus_sha256":c.digest(source),
        "candidate_count":len(source["candidates"]),"positive_count":sum(r["record_kind"] in index.POSITIVE_KINDS for r in source["candidates"].values()),
        "catalog_count":len(target),"old_bindings_accounted_for":len(ledger),"new_binding_count":len(final),
        "additional_role_relations":len(final)-len(before["slot_bindings"]),"boundary_review_rows":len(review_input),
        "exact_body_exception_count":len(overrides),"effect_refinements":len(effect_changes),
        "native_property_refinements":len(catalog_refinements),
        "positive_texts_preserved":True,"canonical_ids_preserved":True,"binding_reference_closure":True,
        "duplicate_candidate_role_pairs":0,"retired_operating_slot_ids":sorted(set(before["slot_catalog"])-set(target)),
        "boundary":"Existing role migration with reviewed mixed-bucket exceptions. Full-corpus new tag review is stages 4-8."}
    if args.apply:
        (OUT / "BINDING-MIGRATION.jsonl").write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in ledger))
        (OUT / "EFFECT-REFINEMENTS.json").write_text(json.dumps(effect_changes,ensure_ascii=False,indent=2)+'\n')
        (OUT / "CATALOG-REFINEMENTS.json").write_text(json.dumps(catalog_refinements,ensure_ascii=False,indent=2)+'\n')
        write_source(source,new_owners)
        (OUT / "STAGE03-SOURCE-VERIFICATION.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    else:
        report['plan_only']=True
    print(json.dumps(report,ensure_ascii=False))


if __name__ == "__main__":main()
