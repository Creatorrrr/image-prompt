"""Explicit manual precision after rereading source and full specs; no semantic classifier."""
import runpy
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'authored/native_05250_05250_06250.06100_06150.literals.py';D=runpy.run_path(str(p))['D']
# One actual bilateral rise is one effect, not two renamed mutations to obtain tags.
d=D[6117];d['claims'].pop('edge');d['anchors']=[x for x in d['anchors'] if x[0]!='m_edge'];d['units']['/content/embedding_text'].remove('m_edge');d['roles']['garment_detail']=(['m_garment'],['prerequisite']);d['owner_issue']+=' Manualprecision: remove redundant appearance-garment.rise effect; same actual bilateral rise retained once as owned wardrobe.silhouette.rise E. Existing waistband construction remains garment_detail P.'
# Korean exact instant is finer than English before; preserve it with the exact pointer.
d=D[6119];v=list(d['claims']['phase']);v[5]='immediately_before_shift_change';d['claims']['phase']=tuple(v);d['anchors']=[x for x in d['anchors'] if x[0]!='e_phase'];d['units']['/content/en'].remove('e_phase');d['anchors'].append(('k_phase','/content/ko','phase','교대 직전의 작은 야간 정비 작업대'));d['units']['/content/ko'].append('k_phase');d['roles']['narrative_phase']=(['k_phase'],['effect']);d['owner_issue']=d['owner_issue'].replace('ENbefore/Kimmediatelybefore precisionKretainedcontext, exactnativeinstantunknown.','K교대직전 actualfinerphaseEanchoredexactK; ENbeforebroadcompatible, exactclockinstantunspecified.')
# Explicit recorded night exposure meets exposure spec; no extra requirement of measured values.
d=D[6124];d['roles']['exposure']=(['m_exposure'],['effect']);d['owner_issue']=d['owner_issue'].replace('Exposurefine roleheldinformationpreservation/levelunspecifiedbutnight-renderingEkept.','Exposurefine roleintent supportedexplicitnaturalnightrecordedexposure; exactnumeric/tonalinformationconstraintsunspecified, notrequiredtoinvent. ActualEunchanged.')
# Actual nonanatomical shell-to-rock structural attachment is directly declared in Korean.
d=D[6144];d['roles']['object_structure']=(['k_shells'],['effect']);d['owner_issue']=d['owner_issue'].replace('Object_structurefineheldattachmentcarrierdetailsgeneric,','Kexactphysicalshell-to-rockattachmentsupportsobject_structureintent; preciseindependentcarrier/jointwitnesspending,')
for o in [6117,6119,6124,6144]:D[o]['effects']=sorted({(v[0],v[1],v[2]) for v in D[o]['claims'].values() if v[3]=='effect'})
with p.open('w') as f:
 f.write('"""Explicit manually authored native meaning/fact cells; no semantic inference code."""\nD={}\n')
 for o,a in D.items():f.write('D['+str(o)+']='+repr(a)+'\n')
