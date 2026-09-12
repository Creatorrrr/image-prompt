"""Read-only inventory and exact profile diagnostics; writes only this research folder."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
sys.dont_write_bytecode = True
import prompt_generator as g

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

assets = SKILL / 'assets'
files = [assets / 'photo_prompt_tags.json', assets / 'photo_prompt_visual_obligations.json']
files += [assets / n for n in g.RESEARCH_EXTENSION_FILENAMES]
files += [assets / n for n in g.VISUAL_OBLIGATION_EXTENSION_FILENAMES]
registry = g.load_visual_obligation_registry(assets / 'photo_prompt_visual_obligations.json')
profile_targets = {'wide_angle_near_field_perspective', 'shallow_depth_focus_falloff_relation',
 'three_plane_depth_chain', 'highlight_rolloff_tone_response', 'hard_light_shadow_edge_relation',
 'soft_light_shadow_edge_relation', 'blue_hour_ambient_practical_balance',
 'window_seat_daylight_activity_relation', 'architectural_threshold_frame_depth_relation',
 'circulation_path_mid_action_depth_relation', 'wet_surface_light_reflection_owner_relation',
 'patterned_cast_shadow_receiver_continuity', 'volumetric_occluded_light_shafts',
 'computational_low_light_multiframe_look', 'mep_environment_relation',
 'negative_fill_shadow_deepening_relation'}
slot_targets = {'lived_in_clutter', 'documentary_photo', 'documentary_real_person',
 'photographic_grain_present', 'iso100_fine_grain', 'iso3200_noise_grain',
 'lit_practical_motivated_mixed_interior', 'lit_practical_warm_cool_spatial_zones',
 'lit_window_open_shadow_falloff', 'lit_window_large_soft_source'}
selected = []
def walk(v, pointer, file):
    if isinstance(v, dict):
        if v.get('id') in profile_targets | slot_targets:
            selected.append({'file': str(file.relative_to(ROOT)), 'json_pointer': pointer, 'record': v})
        for k,x in v.items(): walk(x, pointer+'/'+k.replace('~','~0').replace('/','~1'), file)
    elif isinstance(v,list):
        for i,x in enumerate(v): walk(x,pointer+'/'+str(i),file)
for f in files: walk(json.loads(f.read_text()),'',f)
queries = ['realistic background', '현실적인 배경', 'on-location photography', 'lived-in environment',
 'available light', 'mixed lighting', 'natural exposure', 'weathered surfaces',
 'realistic surface roughness', 'incidental background details', 'atmospheric haze',
 'natural optical depth of field', 'subtle sensor noise', 'minimally processed RAW photograph',
 'focus breathing', 'HDR', 'clean hotel lobby', '서울 주택가',
 'shallow-depth focus-falloff relation', 'three-plane depth-chain relation',
 'warm-cool mixed interior light motivated by a visible practical',
 'wet surface reflection from an in-frame owner']
diagnostics=[]
for q in queries:
    r=g.resolve_visual_profile_hits(registry,[{'source':'concept_lock','text':q,'polarity':'required',
        'priority':'critical','mandatory':True}],adult_context=True)
    diagnostics.append({'query':q,'exact_hard_profile_ids':[x['profile_id'] for x in r.get('hits',[])
        if x.get('match_basis')=='exact' and x.get('hard_eligible')]})
out={'schema_version':'photo-research-repo-audit/v1','captured_at':'2026-09-12',
 'git_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
 'source_files':[{'path':str(f.relative_to(ROOT)),'sha256':sha(f)} for f in files],
 'main_profile_count':len(json.loads((assets/'photo_prompt_visual_obligations.json').read_text())['profiles']),
 'loaded_profile_count':len(registry['profiles']),'selected_existing_records':selected,
 'exact_match_diagnostics':diagnostics,
 'limitations':['Exact deterministic resolution only, no vector index or candidate-pack execution.',
 'A missing exact hit is not proof of missing semantic retrieval or missing related data.',
 'Research drafts are not loaded; source, index, exposure, selection, audit and pixels remain distinct.']}
(HERE/'repo-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'loaded_profiles':len(registry['profiles']),'selected_records':len(selected),
 'diagnostics':diagnostics},ensure_ascii=False))
