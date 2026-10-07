"""Small independent paraphrase probe of the full current visual index.

This is maintenance evaluation, not a live arm's pre-core input. No scores,
thresholds or weights are changed. Embedding-only is kept separate from hybrid.
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

CASES=[
 ('rear_slit','occluded_vertical_emissive_slit','Behind her, an illuminated hairline gap runs upright, disappearing where her head and shoulders block it. The separate visible pieces line up.'),
 ('gold_mosaic','gold_mosaic_tesserae','The gold backdrop is assembled from many little adjoining squares, each with a thin join and a slightly different glint.'),
 ('sparse_mume','mume_on_leafless_woody_branches','White blossoms are dotted sparingly down a woody leafless spray, with brown twigs exposed between them.'),
 ('petal_frost','frost_on_petals','Tiny pale jagged crystals cling to the dark flower folds; its petal outlines are still distinguishable beneath the ice.'),
 ('lace_collar','high_collar_lace_structure','At the throat a lace stand-up collar rises from the garment; its small scallops run along the upper border.'),
 ('pleated_net','micropleated_tulle_panel','Rows of narrow folds cross a gauzy net panel; the little open cells can still be distinguished within those folds.'),
]
NEGATIVES=[
 'a fine grain pattern covering the whole photograph',
 'a smooth gold-painted wall with softly varying light',
 'painted white blossoms on a flat screen',
 'clear round drops resting on dark petal edges',
 'a low flat lace strip around a garment opening',
 'a continuous translucent sheet of fabric with soft broad folds',
]

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);a=parser.parse_args()
 skill=a.root/'skills/photo-prompt-image-generator';sys.path.insert(0,str(skill/'scripts'))
 import prompt_generator as g
 for line in Path('/Users/chasoik/Projects/image-prompt/.env').read_text().splitlines():
  if not line.strip() or line.lstrip().startswith('#') or '=' not in line:continue
  key,value=line.split('=',1);key=key.strip()
  if key in {'GEMINI_API_KEY','GOOGLE_API_KEY'} and key not in os.environ:os.environ[key]=value.strip().strip('\"\'')
 reg=g.load_visual_obligation_registry(skill/'assets/photo_prompt_visual_obligations.json')
 index=g.load_visual_profile_index(skill/'assets/photo_prompt_visual_profile_index.json',reg)
 rows=[]
 for (cid,target,text),negative in zip(CASES,NEGATIVES):
  vector=g.embed_texts_with_gemini([text],model=index['embedding_model'],dimensions=index['embedding_dimensions'])[0]
  source=[dict(source='authorial_core_interpretation',text=text,polarity='advisory')]
  observed={}
  for lane,fields in [('embedding_only',None),('hybrid',{'baseline_prompt':text})]:
   result=g.resolve_visual_profile_hits(reg,source,visual_profile_index=index,query_text=text,query_fields=fields,query_vector=vector,adult_context=False)
   hits=sorted([dict(profile_id=h['profile_id'],match_basis=h['match_basis'],hard_eligible=h['hard_eligible'],optional_eligible=h['optional_eligible']) for h in result['hits']],key=lambda h:h['profile_id'])
   observed[lane]=dict(target_returned=any(h['profile_id']=='egr_profile_'+target and h['optional_eligible'] for h in hits),hard_count=sum(h['hard_eligible'] for h in hits),hits=hits)
  negative_result=g.resolve_visual_profile_hits(reg,[dict(source='concept_lock',text=negative,polarity='required',mandatory=True)],visual_profile_index=index,adult_context=False)
  negative_hard=[h['profile_id'] for h in negative_result['hits'] if h['hard_eligible'] and h['profile_id'].startswith('egr_profile_')]
  rows.append(dict(case_id=cid,target_profile_id='egr_profile_'+target,paraphrase=text,observed=observed,adjacent_negative=negative,adjacent_negative_new_hard_hits=negative_hard))
  print(cid, observed['embedding_only']['target_returned'],observed['hybrid']['target_returned'],len(negative_hard),flush=True)
 output=dict(schema_version='ethereal-gothic-live-retrieval-probe/v1',provider=index['provider'],model=index['embedding_model'],dimensions=index['embedding_dimensions'],batch_size=1,
  registry_sha256=index['registry_sha256'],index_manifest_sha256=hashlib.sha256((skill/'assets/photo_prompt_visual_profile_index.json').read_bytes()).hexdigest(),cases=rows,
  summary=dict(positive_count=len(rows),embedding_only_targets_returned=sum(r['observed']['embedding_only']['target_returned'] for r in rows),hybrid_targets_returned=sum(r['observed']['hybrid']['target_returned'] for r in rows),adjacent_negative_new_hard_count=sum(len(r['adjacent_negative_new_hard_hits']) for r in rows)),
  limits=['Six probes are not the unexecuted ninety-case research plan or a coverage estimate.','Fake-vector authority tests and these real query probes have different evidence roles.','Optional retrieval never proves complete semantic compatibility, candidate adoption or image implementation.'])
 a.output.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
