import contextlib,copy,hashlib,io,json,runpy,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');script=R/'authored/native_11870_formal03_remaining_pending_source_proposals_v1.py'
sys.argv=[str(script),'0']
with contextlib.redirect_stdout(io.StringIO()):v=runpy.run_path(str(script))
g=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/534cde26ba2156cf1760542d5be3a36e82b5457972d85f69d2a2fa8a7c0d50d2')
sys.path[:0]=[str(g/'scripts'),str(g/'scripts/precore')]
import photo_candidate_corpus as c,photo_candidate_realizations as real
rows=[]
for row in v['OUT']['proposals']:
 assert row['original_compiled_locator']['row_sha256']==row['original_compiled_row_sha256']
 for op in row['options']:
  after=op['whole_proposed_after_source'];c.validate_conditions(after['conditions'],after['id']);c.validate_effects(after['effects'],after['id']);real.validate_content(after)
  reconstructed=copy.deepcopy(row['whole_before_source'])
  for d in op['exact_delta']:
   parts=d['pointer'].strip('/').split('/');parent=reconstructed
   for k in parts[:-1]:parent=parent[k]
   assert (parts[-1] in parent)==d['before_exists'] and parent.get(parts[-1])==d['before']
   parent[parts[-1]]=copy.deepcopy(d['after'])
  assert reconstructed==after and v['sha'](after)==op['proposed_after_source_sha256']
  rows.append({'ordinal':row['ordinal'],'option_id':op['option_id'],'after_sha256':v['sha'](after),'conditions_effects_projection_shape':'passed','exact_delta_reconstruction':'passed'})
modulepins={name:{'path':m.__file__,'file_sha256':hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()} for name,m in sorted(sys.modules.items()) if name.startswith('photo_') and getattr(m,'__file__',None)}
assert all(str(g) in x['path'] for x in modulepins.values())
out={'schema':'source-proposal-structural-check-only/v1','rows':rows,'row_count':12,'option_count':len(rows),'modules':modulepins,'native_source_proof_validation':False,'admission':False,'root_acceptance':False,'operating':False,'boundary':'Only exact source delta reconstruction, source condition/effect/projected-text shape and source locator digest identity. Actual meaning manually judged; no native proof/signature/status/admission/root approval.'}
target=R/'authored/native_11870_formal03_remaining_pending_source_proposals_checks_v2.json';assert not target.exists();target.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(json.dumps({'file':str(target),'sha256':v['sha'](out),'file_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'options':len(rows)}))
