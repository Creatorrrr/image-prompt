"""Read-only corpus observation; all outputs stay inside this research folder."""
from pathlib import Path
import collections, hashlib, json
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[3]; ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((ASSETS/'photo_candidate_corpus_manifest.json').read_text())
terms=['uncanny','abject','grotesque','surreal','biomorph','vanitas','reliquary','mirror','negative space','tableau','haptic','art horror','arthouse','tenebris','chiaroscuro','giallo','monstrous','gynaehorror','acousmatic','mise en abyme','scopophilia','doppelg','expressionis','butoh','institutional critique']
targets={
 'V01':'cand_62b2336d58395b0688f96fd1cc511216',
 'V07':'cand_adedeca2e608587e8585c7112575611a',
 'V08':'cand_251dffe09ca15e9c93647415b13a41d3',
 'V11':'cand_d16fd394d2ef5dc39c5b0b51b446560c',
 'V16':'cand_d721153af85f50f0be0896d11bde19d8',
 'V20':'cand_4f9aa7915bdd53f5b9a974059bebf7d7',
 'V25':'cand_95c0893727b35d5c97537ec39a454aa2',
 'V26':'cand_9d1213229e6757e18c9bc2472067997c',
 'V31':'cand_87bfef4aae77597ca226eec19c993f93',
 'V32':'cand_577175d2238f5266825a75fefb755d7f',
 'V35':'cand_d43d9575faec53a48e8c35b5c60a6487',
 'V42':'cand_1e0f80a818b552e1a664c716445637b9',
 'V43':'cand_c73c675fcbb95197afe210ad76644853',
 'V46':'cand_2da0ba86c4aa5e309a69093d3304e36c',
 'V50':'cand_25b9386ea05954b8b4eb94ee648fbebd',
}
all_records={};bindings={};counts=collections.Counter();examples={t:[] for t in terms};kinds=collections.Counter();module_hashes={}
for module in manifest['modules']:
 p=ASSETS/module['file']; module_hashes[str(p.relative_to(ROOT))]=digest(p)
 d=json.loads(p.read_text())
 if module['kind']=='candidates':
  for cid,r in d['candidates'].items():
   all_records[cid]=(module['file'],r);kinds[r.get('record_kind','unspecified')]+=1
   c=r.get('content',{});t=' '.join(str(c.get(k,'')) for k in ['en','ko','definition','aliases']).lower()
   for term in terms:
    if term in t:
     counts[term]+=1
     if len(examples[term])<4:examples[term].append(dict(candidate_id=cid,module=module['file'],record_kind=r.get('record_kind'),en=c.get('en'),ko=c.get('ko')))
 elif module['kind']=='slot_bindings':bindings.update(d['slot_bindings'])

snapshots=[]
for card,cid in targets.items():
 if cid not in all_records:continue
 file,r=all_records[cid]
 related={k:v for k,v in bindings.items() if cid in json.dumps(v,ensure_ascii=False)}
 decision='priority_reuse_review; whole bilingual equivalence and every qualifier remain unapproved' if card in ['V01','V08','V20','V25','V31','V35','V43'] else 'related_source_only; preserve original; new difference requires separate review'
 snapshots.append(dict(card_id=card,candidate_id=cid,module=file,module_sha256=digest(ASSETS/file),record=r,bindings=related,reuse_decision=decision,native_qualification='NOT_ASSESSED_BY_THIS_RESEARCH',claim_limit='full source/guards/effects and actual selected realization remain authoritative; matching words grant no adoption authority'))
audit=dict(observed_date='2026-10-23',scope='literal occurrence in candidate content en/ko/definition/aliases only; not native eligibility or semantic coverage',manifest_sha256=digest(ASSETS/'photo_candidate_corpus_manifest.json'),candidate_count=len(all_records),binding_count=len(bindings),record_kinds=dict(kinds),counts=dict(counts),examples=examples,module_hashes=module_hashes)
(BASE/'corpus-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
(BASE/'existing-source-snapshots.json').write_text(json.dumps(snapshots,ensure_ascii=False,indent=2)+'\n')
catalog=json.loads((ASSETS/'photo_candidate_slot_catalog.json').read_text())['slot_catalog']
mapping={
 'subject_relation':['relational_action','proxemics','contact_point'], 'prop_relation':['prop_placement','contact_point'],
 'medium_relation':['medium','reflection_logic','image_artifact'], 'environment_relation':['environment_detail','space_condition','composition'],
 'prop_scale':['scale_relation'], 'environment':['environment_detail'], 'subject_structure':['body_form','anatomical_connection','object_structure'],
 'surface_material':['surface_material'], 'surface_pattern':['surface_pattern'], 'image_surface':['image_artifact','grain_profile'],
 'prop_state':['prop_state'], 'photographic_treatment':['image_detail','texture'], 'gaze':['gaze_direction','gaze_target','gaze_engagement'],
 'framing':['shot_scale','subject_framing'], 'environment_scale':['scale_relation','environment_detail'],
 'environment_structure':['object_structure','environment_detail'], 'prop_arrangement':['prop_placement','composition'], 'material':['surface_material','material_form'],
 'lighting':['light_quality','light_intensity','light_color','light_shape','lighting'], 'composition':['composition'],
 'subject_state':['body_marking','skin_condition'], 'surface_state':['prop_state','surface_material'],
}
assert all(x in catalog for xs in mapping.values() for x in xs)
(BASE/'slot-mapping.json').write_text(json.dumps(dict(catalog_count=len(catalog),catalog_sha256=digest(ASSETS/'photo_candidate_slot_catalog.json'),research_dimension_to_possible_existing_slot_ids=mapping,disposition='alternative roles requiring individual source-field review; not simultaneous automatic bindings',native_approved=False,no_new_runtime_slot_proposed=True,warning='lighting requires a complete positively declared source-placement-receiver setup; highlights alone may only support a narrower light role'),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(candidate_count=len(all_records),binding_count=len(bindings),mapped_sources=len(snapshots),catalog_count=len(catalog)),ensure_ascii=False))
