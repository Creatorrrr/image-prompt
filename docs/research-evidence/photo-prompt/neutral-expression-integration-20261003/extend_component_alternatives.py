"""Equivalent component phrasings retain all-of groups and owner duties."""
from pathlib import Path
import copy
import json

ROOT=Path(__file__).resolve().parents[4]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
MAPPING={
 'bm_long_limb_build':[['body torso length reference','몸통 길이 기준'],['elongated arms and legs','long upper and lower limb segments','길게 이어진 팔과 다리'],['slender limb widths','narrow limb volumes','가는 사지 가로 폭']],
 'bm_wiry_definition':[['narrow torso and limbs','가는 몸통과 사지'],['local muscle planes','얕게 읽히는 근육 면'],['tendon contours','힘줄 윤곽']],
 'bm_lip_volume':[['upper lip vermilion thickness','윗입술 붉은 면의 두께'],['lower lip vermilion thickness','아랫입술 붉은 면의 두께'],['the boundary of the lip opening','입술 틈의 경계']],
 'bm_eye_aperture':[['upper eye-opening border','윗눈꺼풀 가장자리'],['lower eye-opening border','아랫눈꺼풀 가장자리'],['medial and lateral eye corners','눈 안쪽과 바깥쪽 모서리']],
 'bm_breast_root_width':[['inner breast attachment boundary','가슴 안쪽 부착 경계'],['outer breast attachment boundary','가슴 바깥 부착 경계'],['the same breast chest-wall base','같은 가슴의 흉벽 바탕']],
 'bm_breast_root_height':[['upper breast attachment boundary','가슴 위쪽 부착 범위'],['lower breast attachment region','가슴 아래쪽 부착 범위'],['the same adult chest-wall reference','같은 성인의 흉벽 기준']],
 'bm_breast_projection':[['local chest-wall base plane','국소 흉벽 바탕 면'],['front breast boundary','가슴 앞쪽 경계'],['anterior projection depth','앞쪽으로 나온 깊이']],
 'bm_breast_fullness':[['specified upper lower medial or lateral partition','명시한 위아래 또는 안팎 구간'],['rounded volume in each stated partition','지정한 구간별 둥근 볼륨'],['the same breast owns all named regions','같은 가슴에 속한 모든 지정 구간']],
 'bm_abdominal_projection':[['upper belly region','상복부 구간'],['lower belly region','아래배 구간'],['continuous side-torso outline','이어지는 옆몸통 윤곽']],
 'bm_gluteal_projection':[['same adult lateral pelvic reference','같은 성인의 옆 골반 바탕'],['posterior buttock boundary','둔부 뒤쪽 경계'],['connected upper-thigh attachment','연결된 위허벅지 부착']],
 'bm_thigh_volume':[['upper-thigh transverse volume','위허벅지 가로 볼륨'],['middle-thigh outline','허벅지 중간 윤곽'],['continuous contour toward the knee','무릎 쪽으로 이어지는 윤곽']],
 'bm_skin_relief_texture':[['distribution of visible pores','표면에 분포한 작은 모공'],['low skin microrelief','피부의 얕은 미세 지형'],['specular finish is separately readable','별도로 읽히는 표면 반사광']],
 'bm_cellulite_relief':[['continuous adult skin surface','이어지는 성인 피부 표면'],['distributed small shallow depressions','국소적으로 분포한 얕은 오목함들'],['localized skin surface relief variation','국소 피부 지형 차이']],
 'bm_striae_surface':[['long narrow skin bands','길고 가는 피부 띠'],['localized color variation','국소 색 차이'],['bands continue on the same skin surface','같은 피부 표면에 이어진 띠']],
}


def main():
    path=ASSETS/'photo_prompt_visual_obligations_body_morphology.json';data=json.loads(path.read_text()); updates=[]
    existing={p['id']:p for p in data['profiles']}
    if (Path(__file__).parent/'COMPONENT-ALTERNATIVES.json').exists() and all(
        set(phrases)<=set(existing[profile_id]['semantics']['component_semantics']['groups'][i]['any_terms'])
        for profile_id,groups in MAPPING.items() for i,phrases in enumerate(groups)):
        print('Recorded component alternatives are present; original receipt preserved.')
        return
    for profile in data['profiles']:
        if profile['id'] not in MAPPING:continue
        groups=profile['semantics']['component_semantics']['groups']
        before=copy.deepcopy(profile['semantics']['component_semantics'])
        component_updates=[]
        for group,phrases in zip(groups[:3],MAPPING[profile['id']]):
            added=[p for p in phrases if p not in group['any_terms']];group['any_terms'].extend(added)
            requirement=profile['evidence_requirements'][group['id']+'_phrase']['must_mention_any']
            requirement.extend(p for p in added if p not in requirement)
            component_updates.append({'group_id':group['id'],'existing_component':before['groups'][len(component_updates)]['any_terms'][0],'equivalent_alternatives':added})
        # A complete context still needs explicit common ownership. Individual
        # body parts or a pronoun alone cannot replace this relation.
        owner=groups[-1];own_terms=['the same adult subject and named body region','같은 성인 인물의 지정한 몸 부위']
        added_owner=[p for p in own_terms if p not in owner['any_terms']];owner['any_terms'].extend(added_owner)
        profile['evidence_requirements']['owner_state_phrase']['must_mention_any'].extend(added_owner)
        updates.append({'profile_id':profile['id'],'component_alternatives':component_updates,'owner_alternatives':added_owner,'minimum_groups_and_required_group_ids_preserved':before['minimum_component_groups']==profile['semantics']['component_semantics']['minimum_component_groups'] and before['required_group_ids']==profile['semantics']['component_semantics']['required_group_ids']})
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    out={'profile_count':len(updates),'component_alternative_count':sum(len(g['equivalent_alternatives']) for u in updates for g in u['component_alternatives']),'owner_alternative_count':sum(len(u['owner_alternatives']) for u in updates),'updates':updates,'same_meaning_all_of_proof_preserved':True}
    (Path(__file__).parent/'COMPONENT-ALTERNATIVES.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print({k:v for k,v in out.items() if k!='updates'})


if __name__=='__main__':main()
