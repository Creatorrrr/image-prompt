"""Author image-grounded supplemental judgments without adding runtime gates."""
from pathlib import Path
import copy
import hashlib
import json

ARM=Path(__file__).resolve().parent
META=json.loads((ARM/'native-result-metadata.json').read_text())
PLAN=ARM/'selected-new-candidate-observation-plan.json'
new=json.loads(PLAN.read_text())
evidence={
 'warm_bundle_owner':('pass','visible','The peach blouse and mushroom skirt are both worn by the single woman; neither surface is donated by another figure or background sample.','thumbnail and upper_body_projection'),
 'warm_bundle_hue':('pass','visible','The actual blouse is softly peach and the skirt warm mushroom-taupe. Their subdued adjacent warm hues remain distinguishable from the cooler sage inner garment, rather than relying on the room\'s warm cast alone.','thumbnail and skirt_boundaries'),
 'warm_bundle_boundaries':('fail','partially_visible','The blouse\'s stitched lower hem and the skirt surface are distinct, but the preplanned second endpoint was the skirt waistband. Its actual upper edge is concealed by the extending blouse. A visible skirt side outline cannot be substituted after rendering for that preplanned endpoint; the complete two-boundary test is unobservable.','knit_and_three_layers and skirt_boundaries'),
 'new_knit_topology':('pass','visible','Opaque ivory yarn visibly connects around many open diamond-shaped cells across the same vest. The strands carry loop texture and overlap relief; the cell interiors are actual views of lower clothing rather than printed dark marks.','knit_and_three_layers'),
 'new_knit_under_surface':('pass','visible','The same opaque ivory strands border gaps through which a separate peach translucent blouse is visible. Sage cloth and skin are then transmitted through that blouse in different chest regions, while the yarn remains an exterior opaque surface.','knit_and_three_layers'),
}
rows=[]
for original in new['rows']:
 row=copy.deepcopy(original)
 status,visibility,reason,view=evidence[row['id']]
 row.update(status=status,visibility=visibility,evidence=reason,reviewed_scales=['native','thumbnail'] if row['id'].startswith('warm_bundle') else ['native'],observation_view=view)
 rows.append(row)
review={
 'schema_version':'spring-new-candidate-supplemental-review/v1',
 'arm_id':'knit_layer','source_generation':new['source_generation'],'pack_id':new['pack_id'],
 'result_image':META['project_image_path'],'result_sha256':META['image_sha256'],
 'source_plan_path':str(PLAN),'source_plan_sha256':hashlib.sha256(PLAN.read_bytes()).hexdigest(),
 'authority':'Supplemental preplanned all-of observation set; excluded from runtime hard_gates.',
 'rows':rows,'all_of_result':'fail','pass_count':4,'fail_count':1,
 'per_selected_meaning':{
   'bundle:spf_sf104_2_bundle':{'status':'fail','passed_rows':2,'required_rows':3,'limit':'Palette and wearer relation observed; the preplanned waistband endpoint is concealed.'},
   'visual-concept:spring_sf057_02':{'status':'pass','passed_rows':2,'required_rows':2}},
 'associated_color_profile':'spring_sf104_2','associated_color_profile_hard_activation':False,
 'associated_color_profile_native_qualification':'not_tested_as_a_hard_profile',
 'user_judgment':{'source':'not_yet_received','status':'pending'},
}
(ARM/'supplemental-new-candidate-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')

topic_plan=ARM/'pre-render-observation-plan.json'
topic=json.loads(topic_plan.read_text())
observations={
 'O01':('pass','Continuous relief-bearing yarn loops enclose many true cells; lower clothing is visible inside those cells.'),
 'O02':('pass','Ivory exterior yarn, peach blouse textile and sage inner garment retain separate visible ownership and exterior-to-interior order.'),
 'O03':('pass','Through several open chest cells, the same peach textile passes across the sage inner top\'s upper boundary: skin-toned transmitted regions are above and green cloth regions below. The knit interrupts the view but does not erase ownership of the boundary.'),
 'O04':('pass','Peach sleeve cloth softens the visible arm underneath. Stitched wrist cuffs and gathering belong continuously to each sleeve.'),
 'O05':('pass','The neck and lower vest bands have dense raised and recessed ribs, physically joined to the openwork body.'),
 'O06':('fail','The vest hem and extending blouse strip are readable, but the skirt\'s sewn upper edge/waistband is covered. The strict preplanned three-edge relationship is therefore partially unobservable.'),
 'O07':('pass','Broad vertical cloth pleats coexist with a separate diagonal front overlap edge. Its edge relief and underlying pleated surface distinguish it from a mere diagonal shadow.'),
 'O08':('pass','The right thumb and index meet the metal clip at the upper dry paper margin. The line meets the upper clip while the clip extends over the paper edge; the load path is coherent. The rear jaw is naturally behind the paper and is not claimed independently visible.'),
 'O09':('pass','The left hand reaches across from its own cuff, with a continuous forearm chain, to steady the lower paper margin beside the torso. It remains separate from the raised right hand.'),
 'O10':('pass','The curtain bows inward and the free paper border gently curves while she pins the upper margin and holds the lower one. This supports a practical paper-stabilizing moment; exact shower timing and a newly opened window remain authored backstory, not proven temporal facts.'),
 'O11':('pass','The generated face keeps source-guided soft facial cues, short dark bob silhouette and wispy fringe in a visible three-quarter view. This is appearance guidance, not a claim to have established a real person\'s identity.'),
 'O12':('observed','The first impression is an airy, warm working-room portrait. Attention at the clip gives the woman agency, and textile layers carry the visual hierarchy. Her relaxed mouth and bearing lend subtle appeal. The full-body crop extends beyond the authored mid-calf suggestion; the extra shoes and room text remain subordinate. User preference is pending.'),
}
topic_rows=[]
for r in topic['observations']:
 status,reason=observations[r['id']]
 topic_rows.append({'id':r['id'],'topic':r['topic'],'status':status,'evidence':reason,
                    'authority':'supplemental; any independently derived runtime duty is assessed separately'})
topic_review={
 'schema_version':'spring-fashion-supplemental-topic-review/v1','arm_id':'knit_layer',
 'source_plan_path':str(topic_plan),'source_plan_sha256':hashlib.sha256(topic_plan.read_bytes()).hexdigest(),
 'result_image':META['project_image_path'],'result_sha256':META['image_sha256'],
 'scene_refinement':'Peach blouse and mushroom skirt are audited choices within the unchanged core\'s open color/material dimensions.',
 'observations':topic_rows,'pass_count':10,'fail_count':1,'qualitative_observation_count':1,
 'whole_image_impression':observations['O12'][1],
 'claim_limits':['No pixel claim for exact fiber, process, gauge, unseen lining or absent concealed garments.',
                 'No personality, biography or body-size inference from the source portrait.',
                 'Supplemental failures do not alter the exact runtime hard-gate set.'],
 'user_judgment':{'source':'not_yet_received','status':'pending'},
}
(ARM/'supplemental-topic-review.json').write_text(json.dumps(topic_review,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'new_source_observations':'4/5; waistband visibility fail','topic_observations':'10 pass, 1 fail, 1 qualitative'},ensure_ascii=False))
