"""Final explicit manual precision audit, before freeze; preserves actual probe-contact E."""
import runpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'authored/native_05250_05250_06250.06200_06250.literals.py';D=runpy.run_path(str(p))['D'];P=json.loads((R/'authored/native_05250_05250_06250.06200_06250.packet.json').read_text());e='/content/en';m='/content/embedding_text';k='/content/ko'
def val(o,key,value):
 x=list(D[o]['claims'][key]);x[5]=value;D[o]['claims'][key]=tuple(x)
def anchor(o,fid,path,key,q):D[o]['anchors']=[(fid,path,key,q) if x[0]==fid else x for x in D[o]['anchors']]
# 6210 EN lacks adjustment point; only full M anchors that full E value.
D[6210]['anchors']=[x for x in D[6210]['anchors'] if x[0]!='e_inspect'];D[6210]['roles']['action']=(['m_inspect'],['effect'])
# 6213 K actual gap and EN visible AIR gap differ in precision, don't borrow EN value.
D[6213]['claims']['kgap']=('relationship','existing_surfaces','spacing.noncontact.ko','preservation','spacing.noncontact.ko/v1','two_near_surfaces_keep_actual_gap_without_contact',[],None,None);anchor(6213,'p0_gap','/content/paraphrases/0','kgap','서로 가까운 두 표면 사이에 실제 간격이 남아 접촉하지 않은 배치')
# 6218 revert unapproved original-contact->PR proposal. Original positive M contact E retained,
# without fabricating probe-component contact endpoint or actual defect mutation.
a=D[6218];a['text_corrections']=[];q=P['records'][18]['after_existing5B']['content']['embedding_text'];a['meaning']='Existing failed component/board/prior-use condition P required by repair reference; actual repair record/inclusion AND probe contact E retained, second endpoint unspecified. No new failure or repair.'
val(6218,'component','failed_component_area');a['claims']['contact']=('relationship','probe_contact','contact.specified','effect','contact.specified/v1','actual_probe_contact_second_endpoint_unspecified',[],'set_value',[])
a['anchors']=[('e_generic',e,'generic',P['records'][18]['after_existing5B']['content']['en']),('k_generic',k,'kgeneric',P['records'][18]['after_existing5B']['content']['ko']),('m_component',m,'component','failed component area'),('m_board',m,'board','surrounding board context'),('m_state',m,'state',q),('m_record',m,'record','repair-log reference capture'),('m_visible',m,'visible',q),('m_contact',m,'contact','probe contact'),('m_purpose',m,'purpose','repair-log reference capture')];a['claims'].pop('guard');a['owner_issue']='Independent failed component/board/prior-use witnesses and actual record/display/contact E permissions pending. Actual positive probe contact is NOT changed to optional guard or PR: unknown second endpoint prevents qualified contact_point but actual contact E remains. Source unchanged. Root must resolve endpoints/scope and original E locks; prior mutable PR-only proposal rejected before freeze.'
a['boundary']='No guessed probe-to-component rather than board endpoint/patch, new failure/wear/technician/test result/repair success or macro camera from facets. Actual source contact cannot be deleted because endpoints unknown.'
# 6221 garment type alone is not garment construction; retain uniform E without fine role.
D[6221]['roles'].pop('garment_detail');D[6221]['owner_issue']='Actual uniform/equipment/coherent safety-system presentation E permissions pending. Wardrobe_style held no actual worn owner; garment_detail held garment type alone no construction/topology/trim/local form. No type/coherence E deleted. Adult/authorization contextual, no safety efficacy certification. Original appearance owner/property locks unresolved. Source unchanged.'
# 6234/6249 remove implementation wording inside literal prose, keep full meaning.
a=D[6234];c=a['text_corrections'][0];old=c['after'];new=old.replace(', preserving the Korean source joint list','');c['after']=new;a['anchors']=[(i,path,key,new if q==old else q.replace(', preserving the Korean source joint list','')) for i,path,key,q in a['anchors']]
# 6235 tiny quote didn't include additional input; full original-proposed cue does.
anchor(6235,'m_resource',m,'resource',D[6235]['text_corrections'][0]['after'])
# 6242 only EN includes service-hardware inventory; M handrails/panels not whole type union.
D[6242]['anchors']=[x for x in D[6242]['anchors'] if x[0]!='m_hardware']
a=D[6249];c=a['text_corrections'][0];old=c['after'];new=old.replace('with the Korean source moderate field-of-view intent','with a moderate field of view');c['after']=new;a['anchors']=[(i,path,key,new if q==old else q) for i,path,key,q in a['anchors']]
for o,a in D.items():
 a['units']={}
 for fid,path,key,q in a['anchors']:a['units'].setdefault(path,[]).append(fid)
 a['effects']=sorted({(x[0],x[1],x[2]) for x in a['claims'].values() if x[3]=='effect'})
with p.open('w') as f:
 f.write('"""Explicit manually authored native meaning/fact cells; no semantic inference code."""\nD={}\n')
 for o,a in D.items():f.write('D['+str(o)+']='+repr(a)+'\n')
