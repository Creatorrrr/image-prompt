"""Reviewed pure prototype suites against new comparison code, not native proof."""
import copy,hashlib,importlib,io,json,sys,unittest
from pathlib import Path
ROOT=Path.cwd();O=Path(__file__).parent;P=O.parent/'permission-envelope-prototype-02'
sys.path[:0]=[str(ROOT/'skills/photo-prompt-image-generator/scripts'),str(P)]
import photo_permission_comparison as comparison
# Test-only lossless transport: old fixtures contain one base-RID effect set.
# New engine requires the explicitly supplied actual-RID effect set. This is
# not a production legacy adapter, semantic classifier or source qualification.
original_bind=comparison.bind_source
def bind_fixture(context,contract):
 ctx=copy.deepcopy(context);ctx.setdefault('actual_effect_set',copy.deepcopy(ctx['source_record']['effects']))
 return original_bind(ctx,contract)
comparison.bind_source=bind_fixture;sys.modules['envelope']=comparison
old=importlib.import_module('test_envelope');added=importlib.import_module('test_joint_paths_v2')
suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromModule(old),unittest.defaultTestLoader.loadTestsFromModule(added)])
stream=io.StringIO();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
x={'schema':'photo-native-comparison-pure-regression/v1','methods':r.testsRun,'original_scenarios':len(old.CASES),'added_scenarios':len(added.CASES),
 'successful':r.wasSuccessful(),'failures':[(t.id(),s)for t,s in r.failures],'errors':[(t.id(),s)for t,s in r.errors],'log':stream.getvalue(),
 'comparison_code_raw_sha256':hashlib.sha256(Path(comparison.__file__).read_bytes()).hexdigest(),
 'boundary':'Pure comparison with frozen actual B1/property primitives only. Old one-base-RID fixture effect set copied verbatim into new explicit actual_effect_set transport. No actual native1299 qualification, model, source edit or runtime publish.',
 'network_denied':True,'models':0}
p=O/'COMPARISON-REGRESSIONS-v1.json';assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');print({k:x[k]for k in ['methods','original_scenarios','added_scenarios','successful']});print(stream.getvalue() if not r.wasSuccessful()else'')
