import json,hashlib,sys,subprocess
from pathlib import Path
sys.dont_write_bytecode=True
R=Path('/workspace/scratch/ce8f20680f5a/image-prompt');O=R.parent/'daylong-progress/space-name-scout';A=R/'skills/photo-prompt-image-generator/assets'
D=json.loads((A/'photo_prompt_space_extension.json').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
source_groups={
 'small_body_encounter':{'record':'space_esa_active_comet_structure','url':'https://www.esa.int/ESA_Multimedia/Images/2023/11/Structure_of_a_comet','support':'Solar-heated activity creates a coma and connected tails; the dust tail may curve. The narrow authored geometry is retained without universalizing it.','decision':'keep'},
 'stellar_lifecycle_observation':{'record':'space_nasa_protostar_disks','url':'https://science.nasa.gov/missions/hubble/hubbles-album-of-planet-forming-disks/','support':'The original source depicts dust-obscured young stars, flattened disks and bipolar jets. Both lobes are not necessarily resolved in every cited view. Korean and English source rows keep the same narrow geometry.','decision':'append_official_synonym_to_subject_only'},
 'galaxy_structure_observation':{'record':'space_nasa_interacting_galaxy_tides','url':'https://science.nasa.gov/get-involved/citizen-science/help-galaxy-zoo-tidal-tales-open-cosmic-storybook/','support':'Gravity from close encounters creates tails, streams and shells. Existing paired-nucleus/bridge labels remain authored specializations; broader embedding alternatives are not contradictions.','decision':'keep'},
 'compact_object_visualization':{'record':'space_eht_reconstruction_boundary','url':'https://eventhorizontelescope.org/faq/can-we-really-photograph-black-hole-are-they-not-entirely-dark-no-light-can-escape-them','support':'EHT describes a computationally interpreted radiolight shadow image. Source labels and aliases retain measurement/reconstruction context rather than claim a classical photograph.','decision':'keep'},
 'solar_space_weather':{'record':'space_nasa_flare_cme_boundary','url':'https://science.nasa.gov/blogs/solar-cycle-25/2022/06/10/solar-flares-faqs/','support':'NASA distinguishes electromagnetic flare flashes from ejected plasma/magnetic-field clouds. Existing source rows consistently select a coronagraph-mask and outward-front observation. KASI likewise explains an occulting disk as the coronagraph mechanism.','decision':'keep'},
}
reviews=[]
for slot in ['subject','location','prop','aesthetic_trend']:
 for row in D['slots'][slot][:5]:
  group=next(x for x in row['tags'] if x in source_groups)
  reviews.append({'slot':slot,'id':row['id'],'ko':row['ko'],'en':row['en'],'aliases':row['aliases'],'source_group':group,'source_evidence_record':source_groups[group]['record'],'decision':'qualified_alias_proposal_only' if row['id']=='embedded_protostar_observation_subject' else 'keep','bilingual_process_contradiction_found':False})
assert len(reviews)==20
files=sorted(A.glob('*.json'))
absence=[str(p.relative_to(R)) for p in files if '원시성' in p.read_text()]
assert absence==[],absence
save('source-inventory-and-decisions.json',{
 'scope':'20 high-value non-action rows: first five astronomy clusters across subject, location, prop and aesthetic_trend. Full extension inventory was enumerated for orientation; only these twenty receive bounded source/meaning decisions.',
 'excluded_action_review':'All eight previously assessed action rows are excluded from repeated correctness claims. No action proposal or action correctness revalidation is made.',
 'row_count':len(reviews),'reviews':reviews,'source_groups':source_groups,
 'original_research_paths':['docs/research-evidence/photo-prompt/space-visual-semantics-20260901/source-research.md','docs/research-evidence/photo-prompt/space-visual-semantics-20260901/evidence.jsonl'],
 'source_check_limits':['This is bounded source consistency and name coverage, not validation of all astronomical physics or all space entries.','The narrower authored image specializations are preserved.','No official source is treated as proving rendered fidelity.'],
 'named_term_inventory':{'term':'원시성','searched':'Every top-level runtime assets/*.json file, including source dictionaries, visual registry and generated index manifests','file_count':len(files),'files_with_term':absence,'status':'absent_before_proposal'},
 'other_term_considerations':[
 {'term':'코로나 질량 방출','decision':'keep','reason':'Spacing-only variant of existing 코로나질량방출; does not qualify as meaningful name coverage.'},
 {'term':'광관의','decision':'no_proposal','reason':'KASI uses this instrument name, but mapping a bare instrument name to a specialized occulting-disk prop or CME field would mix whole-instrument and part/scene scope. This scout pursues only the one better-supported protostar alias.'},
 {'term':'코로나 물질 방출','decision':'not_selected','reason':'KASI also uses this alternate translation. Parent scoped continuation to the single protostar proposal; no extra alias or measurement is proposed.'}],
 'repository_files_written':[],'paid_calls':0,'query_retrieval_executions':0})
report=json.loads((O/'actual-v6-preservation-report.json').read_text())
freeze=json.loads((O/'frozen-proposal-and-unmeasured-probes.json').read_text())
summary={
 'status':'one_source_backed_alias_ready_for_separate_measured_gate',
 'exact_one_field_append':freeze['exact_delta'],'candidate_id':freeze['candidate_id'],
 'freeze_sha256':report['freeze_sha256'],'source_reviews':20,'keeps':19,'bilingual_process_contradictions_found':0,
 'official_term_source':'https://astro.kasi.re.kr/kor/post/stellarObjects/71429',
 'actual_v6_result':report,'probes':{'total':8,'languages':['en','ko'],'positives':4,'near_misses':4,'executions':0},
 'remaining_acceptance':'Meaningful named lexical gain, dense behavior and near-miss effects remain unmeasured. V6 equality demonstrates output preservation only, not improvement.',
 'no_mutation':{'source':True,'runtime':True,'schema':True,'guards':True,'weights':True,'compatibility':True,'index':True,'commits':True},
 'artifact_paths':{name:str(O/name) for name in ['frozen-proposal-and-unmeasured-probes.json','source-inventory-and-decisions.json','actual-v6-preservation-report.json','before-actual-v6-full-pack.json','proposed-actual-v6-full-pack.json','before-verified-detail.json','proposed-verified-detail.json']}}
save('summary.json',summary)
(O/'REPORT.md').write_text('''# Space technical-name scout\n\nOne qualified source-backed alias is ready for a separate measured gate: append **원시성 원반 분출계** to `embedded_protostar_observation_subject.aliases`. Keep the existing 원시별 alias and every other source field.\n\nKASI explicitly equates 원시성 with 원시별. Its research description pairs 원시성/protostars with circumstellar disks, envelopes and bipolar outflows, while the original NASA source supports the current disk/outflow visual specialization. The alias preserves the existing qualifier; the complete phrase is not presented as an official quotation. 원시성 was absent from all inspected top-level runtime assets.\n\nTwenty non-action rows received a bounded source/meaning review: nineteen keeps and one alias-only proposal. No genuine bilingual process contradiction was established. The eight previously reviewed action rows were excluded from repeated claims.\n\nActual production V6 full pack, overview and hash-verified detail are identical before/proposed. The diagnostic uses two existing astronomical environment subject alternatives and a real protostar subject-bearing compatibility check, including the narrow protostar location, with no forced choice. The frozen core, generated soft policy and negative guard remain unchanged. This is controlled output preservation, not natural retrieval or improvement.\n\nEight independently phrased EN/KO positive and near-miss probes were frozen before the check and remain unmeasured. Promotion still requires meaningful lexical gain and no unjustified dense or near-miss loss. No paid calls, repository edits or commits occurred.\n\nEvidence: `summary.json`, `source-inventory-and-decisions.json`, `frozen-proposal-and-unmeasured-probes.json`, `actual-v6-preservation-report.json`, and the before/proposed full-pack, overview and detail files.\n''')
print(json.dumps({k:v for k,v in summary.items() if k not in ['actual_v6_result','artifact_paths']},ensure_ascii=False,indent=2))
