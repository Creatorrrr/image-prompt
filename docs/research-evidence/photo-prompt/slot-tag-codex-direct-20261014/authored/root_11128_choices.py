"""Root-authored literal choice correction after complete source/spec reread.

This serializes one explicitly judged source. It never classifies other rows.
"""
import copy, gzip, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import direct_review as d
source = json.loads(gzip.decompress((HERE/'SOURCE.json.gz').read_bytes()))
order = json.loads((HERE/'ORDER.json').read_text())
cid = order[11128]; original = source['candidates'][cid]
assert cid == 'cand_17f21e3dd66a5d1aa97b3b38efaab469'
choices = {
 'standing': {'en': 'an adult wearing a pencil skirt in a natural standing posture',
  'ko': '성인이 펜슬 스커트 차림으로 자연스럽게 서 있는 자세.',
  'embedding_text': 'an adult wearing a pencil skirt in a natural standing posture',
  'concept_units': ['an adult wearing a pencil skirt in a natural standing posture'],
  'relations': [{'id':'pencil_skirt_standing','subject':'the established adult subject',
                 'type':'visible_configuration','object':'wearing a pencil skirt in a natural standing posture'}]},
 'walking': {'en': 'an adult wearing a pencil skirt in a natural walking posture',
  'ko': '성인이 펜슬 스커트 차림으로 자연스럽게 걷는 자세.',
  'embedding_text': 'an adult wearing a pencil skirt in a natural walking posture',
  'concept_units': ['an adult wearing a pencil skirt in a natural walking posture'],
  'relations': [{'id':'pencil_skirt_walking','subject':'the established adult subject',
                 'type':'visible_configuration','object':'wearing a pencil skirt in a natural walking posture'}]}}
common = [
 {'dimension':'age','target':'main_subject','property':'age.declared'},
 {'dimension':'appearance','target':'main_subject','property':'wardrobe.ensemble'},
 {'dimension':'pose','target':'main_subject','property':'body.pose'}]
effects = {'dimensions':['age','appearance','pose'],'properties':common,
 'realizations': {'mode':'one','branches':[
  {'id':'standing','conditions':{},'context_terms':[],
   'effects':{'dimensions':[],'properties':[]}},
  {'id':'walking','conditions':{},'context_terms':[],
   'effects':{'dimensions':['action'],'properties':[
    {'dimension':'action','target':'main_subject','property':'action.walking'}]}}]}}
corrections = [
 {'pointer':'/effects','before':copy.deepcopy(original['effects']), 'after':effects,
  'reason':'Preserve common declared adult/outfit/posture; walking activity belongs only to the walking realization, not standing.'},
 {'pointer':'/conditions','before':copy.deepcopy(original['conditions']),
  'after':{**copy.deepcopy(original['conditions']), 'requires_adult_context':True},
  'reason':'Adult is already declared source context. Another selected role cannot introduce adulthood or override age intent.'},
 {'pointer':'/content/realization_content','before':None,'after':choices,
  'reason':'Standing OR walking are mutually selected source alternatives. Render exactly the selected positive body while retaining the one canonical search document and contextual limitations.'}]
def fact(pointer, quote, dimension, prop):
 return {'pointer':pointer,'quote':quote,'dimension':dimension,'target':'main_subject','property':prop}
common_facts = [
 ('age_presentation',fact('/content/en','adult','age','age.declared'),
  'Explicit declared adult range; adulthood remains an intrinsic prerequisite and never proof from skirt shape.'),
 ('wardrobe_style',fact('/content/en','wearing a pencil skirt','appearance','wardrobe.ensemble'),
  'The declared wearer is in the pencil-skirt outfit; no additional profession, material or outfit pieces.'),
 ('body_pose',fact('/content/en','natural standing or walking posture','pose','body.pose'),
  'Both actual choices supply the whole-body posture. The selected body determines which posture; this does not specify frame crop.')]
roles=[]; facts=[]
for tag, evidence, reason in common_facts:
 roles.append({'slot_id':tag,'semantic_role':source['slot_catalog'][tag]['semantic_role'],
  'scope':'whole_record','realization_ids':['standing','walking'],'rationale':reason,'evidence':[evidence]})
 facts += [{**evidence,'realization_id':rid} for rid in ['standing','walking']]
walk = fact('/content/realization_content/walking/en','walking posture','action','action.walking')
roles.append({'slot_id':'action','semantic_role':source['slot_catalog']['action']['semantic_role'],
 'scope':'positive_alternative','realization_ids':['walking'],
 'rationale':'Only the selected walking realization supplies the concrete walking activity.', 'evidence':[walk]})
facts.append({**walk,'realization_id':'walking'})
decision={'candidate_id':cid,'meaning_summary':'An already declared adult wears a pencil skirt in exactly one natural posture: standing, or walking. Walking activity is conditional. Whole posture supplies no mandatory crop, profession or erotic meaning.',
 'recommended_kind':'visual_option','corrections':corrections,'roles':roles,'facts':facts,
 'rejected_boundaries':['The Korean 전체 자세 means the whole posture and supplies no explicit frame inclusion or crop. Withdraw the earlier subject_framing role.',
 'A standing posture does not perform walking. Native realization_content keeps the other choice out of selected rendering.',
 'The contextual ordinary office/daily example does not declare an office, occupation, submission, power, desire, consent or fetish styling.',
 'Do not infer age from outfit. Adulthood is explicit source context and must already be established.',
 'No particular cloth material, surface texture, garment construction, added body shape, exposed area, lighting or location is asserted.'],
 'uncertainties':[],'status':'approved','all_roles_considered':True}
path=HERE/'authored/root_11128_choices.json'
d.write(path,{'decisions':[decision]})
print(json.dumps({'corrected_record':d.corrected_record(original,corrections),'decision':decision},ensure_ascii=False,indent=2))
