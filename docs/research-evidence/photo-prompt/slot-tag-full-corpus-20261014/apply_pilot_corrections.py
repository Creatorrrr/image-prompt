"""Hash-bound first stage-5 batch; no source record is deleted or duplicated."""
from pathlib import Path
import copy,json,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
import photo_candidate_corpus as c
import photo_global_index as index

def prop(d,t,p):return {'dimension':d,'target':t,'property':p}

def main():
 a=SKILL/'assets';data=c.load(a);before=copy.deepcopy(data)
 proposals=json.loads((HERE.parent/'slot-tag-pilot-20261013/CORRECTION-PROPOSALS.json').read_text())
 for change in proposals['changes']:
  cid=change['candidate_id'];assert c.digest(data['candidates'][cid])==change['before_record_sha256'],cid
  data['candidates'][cid]=copy.deepcopy(change['after'])
 cid='cand_aceaa5a1d9465f5a9e9ded075cefeac0';r=data['candidates'][cid]
 physical='Physical mixed-media carriers show tape stretch, antistatic packaging and distinct colored custody tabs.'
 r['content']['concept_units']=[physical]
 r['effects']={'dimensions':['material','appearance'],'properties':[prop('material','physical_tape_carrier','surface.state.stretch'),prop('material','antistatic_packaging','surface.material'),prop('appearance','custody_tabs','surface.color')],
  'realizations':{'mode':'optional','branches':[{'id':'visible_recorded_playback','conditions':{},'context_terms':['recorded playback','video playback','recorded footage','재생 영상','기록 영상'],
    'effects':{'dimensions':['style'],'properties':[prop('style','recorded_playback_image','image.artifact.signal_dropout')]},
    'concept_units':[physical,'Signal dropout appears only in the already declared recorded playback image.']}]}}
 cid='cand_cb45aeb918bc58e1b6dec41185207523';r=data['candidates'][cid]
 r['effects']={'dimensions':[],'properties':[],'realizations':{'mode':'one','branches':[]}}
 units=r['content']['components'][1]['concept_units']
 for rid,member,unit,owner in [('pink_sheath_dress','cand_48c8ae42e4f958bd9c1a2125b735ec6c',units[0],'selected_dress'),('nude_jersey_bustier','cand_66f7f70de95b536babb9e6f442a4ff78',units[1],'selected_bustier')]:
  eff={'dimensions':['appearance','material'],'properties':[prop('appearance','main_subject','wardrobe'),prop('appearance','main_subject','wardrobe.layer_boundary'),prop('appearance','main_subject','wardrobe.inner_layer.color'),prop('material','main_subject','surface.material'),prop('material','main_subject','wardrobe.material.inner_layer')]}
  # Keep the original wearer's broad wardrobe lock scope until the full
  # owned-effect review is qualified. Descriptive branch owner names must
  # never bypass main_subject/wardrobe property locks.
  # The referenced native member already owns this complete alternative.
  data['candidates'][member]['effects']=copy.deepcopy(eff)
  r['effects']['realizations']['branches'].append({'id':rid,'conditions':{},'context_terms':[],'member_candidate_ids':[member],
    'effects':copy.deepcopy(eff),'component_units':{'one_complete_garment_alternative':[unit]}})
 # Canonical endpoint effect ownership, without narrowing general lowering/rest members.
 for cid in ['cand_c4d6b55142e9537a9a59007ec6313a53','cand_0754e4248862538eb282a8451f28d4d7']:
  data['candidates'][cid]['effects']['properties']=[prop('action','main_subject','action.lowering.endpoint'),prop('relationship','cup_and_matching_saucer','relation.contact.support'),prop('relationship','main_subject_hand_and_cup_handle','relation.contact.grip'),prop('setting','reception_room_table_and_seating','setting.spatial_arrangement')]
  data['candidates'][cid]['effects']['dimensions']=sorted(set(data['candidates'][cid]['effects']['dimensions'])|{'action','relationship','setting'})
 c.validate(data)
 changes=[]
 for cid,row in data['candidates'].items():
  old=before['candidates'][cid]
  if row!=old:
   assert row['id']==old['id'] and row['conditions']==old['conditions'] and row['provenance']==old['provenance']
   changes.append({'candidate_id':cid,'before_record_sha256':c.digest(old),'after_record_sha256':c.digest(row),'before_kind':old['record_kind'],'after_kind':row['record_kind'],'positive_text_changed':index.text(old)!=index.text(row)})
 m=json.loads((a/c.MANIFEST_NAME).read_text())
 for ref in m['modules']:
  if ref['kind']!='candidates':continue
  p=a/ref['file'];payload=json.loads(p.read_text());updated={cid:data['candidates'][cid] for cid in payload['candidates']}
  if updated!=payload['candidates']:
   payload['candidates']=updated;p.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
 report={'schema':'photo-stage05-pilot-corrections/v1','source_schema':c.SCHEMA,'before_sha256':c.digest(before),'after_sha256':c.digest(data),'canonical_count':len(data['candidates']),'positive_count':len(index.documents(data)),'changes':changes,'native_applied':True,'deleted_candidates':[]}
 (HERE/'PILOT-CORRECTIONS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='changes'}))
if __name__=='__main__':main()
