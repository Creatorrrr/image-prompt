from pathlib import Path
O=Path(__file__).resolve().parent
prior=O.parent/'integration-evidence/current-default-successor/build_release.py'
s=prior.read_text();start=s.index('def collect():');end=s.index('\n\ndef main():',start)
s=s[:start]+'''def collect():
 reviewed=read(O/'reviewed-native-records.json');original=c.load(N/'assets');out={cid:convert(r) for cid,r in reviewed.items()}
 fresh={cid:r for cid,r in reviewed.items() if cid not in original['candidates']}
 changed={cid:r for cid,r in reviewed.items() if cid in original['candidates']}
 write(O/'new-native-records.json',fresh);write(O/'release-changed-native-records.json',changed)
 return out
'''+s[end:]
s=s.replace("shutil.copyfile(Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/SKILL.md'),STAGE/'SKILL.md')", """shutil.copyfile(Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/SKILL.md'),STAGE/'SKILL.md')
 for rel in ('references/composition-contract.md','references/romcom-visual-semantics.md'):
  shutil.copyfile(Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator')/rel,STAGE/rel)""")
s=s.replace("write(STAGE/'assets'/module,{'schema':c.MODULE_SCHEMAS['candidates'],'candidates':{cid:new[cid] for cid in fresh}})","""allraw=read(Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets')/module)['candidates']
 write(STAGE/'assets'/module,{'schema':c.MODULE_SCHEMAS['candidates'],'candidates':{cid:(new[cid] if cid in new else original_record) for cid,original_record in c.load(N/'assets')['candidates'].items() if cid in allraw} | {cid:new[cid] for cid in fresh}})""")
s=s.replace("source['modules'].append({'file':module,'kind':'candidates'})", "assert any(m['file']==module for m in source['modules'])")
s=s.replace("source['modules'].append({'file':binding_module,'kind':'slot_bindings'});", "assert any(m['file']==binding_module for m in source['modules']);")
s=s.replace("assert all(prior[k]==current[k] for k in ['conditions','effects','provenance']), 'Existing intrinsic guard/effect/provenance changed'", "assert all(prior[k]==current[k] for k in ['conditions','effects','provenance']), 'Existing intrinsic guard/effect/provenance changed'\n  assert all(prior['content'][k]==current['content'][k] for k in ['en','ko','definition','application_contract','research_semantics'])")
(O/'build_release.py').write_text(s)
