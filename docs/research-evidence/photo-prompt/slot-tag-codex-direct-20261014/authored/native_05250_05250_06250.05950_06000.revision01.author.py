"""Explicit manual full-spec recheck; preserve first frozen internal draft unchanged."""
import runpy
from pathlib import Path
R=Path(__file__).resolve().parents[1];A=R/'authored';D=runpy.run_path(str(A/'native_05250_05250_06250.05950_06000.literals.py'))['D']
# space_condition concerns use/maintenance/damage/preparation, explicitly distinct from structural location.
# Narrow room is structural width, not a use/maintenance state. Preserve actual requirement E.
D[5999]['roles'].pop('space_condition')
v=list(D[5999]['claims']['space']);v[2]='setting.geometry.width';v[4]='setting.geometry.width/v1';D[5999]['claims']['space']=tuple(v)
D[5999]['owner_issue']+=' Full space_condition spec recheck: narrow is structural width, not current use/maintenance/damage/preparation state; positive narrow requirement remains setting.geometry.width E, role removed. Initial internal frozen draft retained historical.'
D[5999]['binding_intent']='Preserve optional/direct location weight1 emptybinding plus dungeon_synth_world_chronicle_scene primary. Actualroom/location direct; narrow structuralwidth E retained independently without space_condition use-state tag. No production/prop union.'
# Formal alone supplies a declared formality context; it does not name the role/culture/era/ceremony required by attire_context.
D[5986]['roles'].pop('attire_context')
D[5986]['owner_issue']+=' Full attire_context spec recheck: generic formal upper-garment adjective does not itself specify role/culture/era/ceremony, so that tag removed while original formal-use context fact stays. No inferred actual wearer/cultural identity.'
D[5986]['binding_intent']='Preserve optional/contextual attire_context .58 human/sixdeny plus intrinsic human. Actual garmentform/state/optics/distinctundershirt layers direct; generic formal adjective preserved context but fine attire_context held exact role/culture/era/ceremony absent.'
for o in [5986,5999]:D[o]['effects']=sorted({(v[0],v[1],v[2]) for v in D[o]['claims'].values() if v[3]=='effect'})
p=A/'native_05250_05250_06250.05950_06000.revision01.literals.py'
with p.open('x') as f:
 f.write('"""Explicit manual full-spec revision01 cells; first internal frozen files unchanged."""\nD={}\n')
 for o,a in D.items():f.write('D['+str(o)+']='+repr(a)+'\n')
