"""Explicit manual precision edits after source/quote/spec comparison; no frozen file writes."""
import runpy
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'authored/native_05250_05250_06250.06050_06100.literals.py';D=runpy.run_path(str(p))['D']
def claim(o,key,**change):
 names=['dimension','target','property','mode','type','value','requires','operation','receivers'];v=dict(zip(names,D[o]['claims'][key]));v.update(change);D[o]['claims'][key]=tuple(v[x] for x in names)
claim(6053,'sparkle',property='image.bokeh.sparkle_appearance',type='image.bokeh.sparkle_appearance/v1')
D[6053]['owner_issue']=D[6053]['owner_issue'].replace('propertynamespaceimage.optical_artifact doesnotitselfgrantrole.','Plainimage.bokeh.sparkle_appearance retainsappearancewithoutclaimingartifact/defect.')
claim(6068,'color',property='lighting.color.hue',type='lighting.color.hue/v1',value='blue_ambient')
base=list(D[6068]['claims']['color']);base[2]='lighting.color.warm_cool';base[4]='lighting.color.warm_cool/v1';base[5]='cool_ambient';D[6068]['claims']['cool']=tuple(base)
D[6068]['anchors'].append(('e_cool','/content/en','cool','cool twilight ambient balanced with illuminated city practicals'))
D[6068]['units']['/content/en'].append('e_cool');D[6068]['roles']['light_color']=(['k_color','e_cool'],['effect'])
D[6068]['owner_issue']+=' Manualprecision: bluehueexactK andcoolwarm-coolqualityexactEN areseparate ownedfacts; no singleKquoteoverclaim.'
claim(6072,'nearby',value='nearby_in_same_workroom_exact_reference_unspecified')
D[6072]['owner_issue']+=' Nearby doesnotbindsimultaneouslytobothpatternANDcuttingsurface; precise reference remainsunspecified.'
D[6092]['roles'].pop('proxemics')
D[6092]['owner_issue']=D[6092]['owner_issue'].replace('Proxemicsintentdeclaredresponders+remainsrequiresindependentcarriers, exactdistanceundefined.','Proxemicsfine roleheldbecausehumanremainsnotindependentlydeclaredactiveparticipant; actualrespectfuldistanceE preservedwithoutrole-baseddeletion, exactdistanceundefined.')
for o in [6053,6068,6072,6092]:D[o]['effects']=sorted({(v[0],v[1],v[2]) for v in D[o]['claims'].values() if v[3]=='effect'})
with p.open('w') as f:
 f.write('"""Explicit manually authored native meaning/fact cells; no semantic inference code."""\nD={}\n')
 for o,a in D.items():f.write('D['+str(o)+']='+repr(a)+'\n')
