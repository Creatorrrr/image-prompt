"""Controlled source-only fingerprint experiments; never edit/publish original generations."""
import argparse
import ast
import json
from pathlib import Path
import subprocess
import tempfile

import checks
import logic_state as scope
import state

GROUPS = {'camera':['legacy_camera_clauses'],
    'gemini':['get_gemini_api_key','cached_gemini_client','extract_embedding_values','round_embedding_vector'],
    'search':['_bm25f_lexicon_from_documents','candidate_pack_float','candidate_pack_assertion_discovery','authorial_core_bm25f_query_fields']}
WORKER = """
import json,sys
from pathlib import Path
sys.dont_write_bytecode=True
root=Path(sys.argv[1]);manifest=json.loads(Path(sys.argv[2]).read_bytes())
sys.path.insert(0,str(root/'scripts'))
import photo_runtime_sources as runtime
result={'loaded_code_files':len(runtime.LOADED_CODE),'source_code_equal':runtime.LOADED_CODE==manifest['source']['code'],
 'algorithm_equal':runtime.algorithm_hash(None)==manifest['algorithm_sha256'],'Gemini_calls':0,'model_calls':0,'CURRENT_writes':0}
try:runtime._require_implementation(manifest['source'],None)
except runtime.FreshnessError as error:result.update(status='REJECTED',reason=error.state,message=str(error))
else:result.update(status='PASS')
print(json.dumps(result))
"""


def remove(raw,names):
    lines = raw.splitlines(keepends=True)
    nodes = {n.name:n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef)}
    ranges = []
    for name in names:
        node = nodes[name]
        first = min([node.lineno,*(d.lineno for d in node.decorator_list)])
        ranges.append((first-1,node.end_lineno))
    for first,last in sorted(ranges,reverse=True):
        del lines[first:last]
    result = b''.join(lines)
    ast.parse(result)
    return result


def run(kind):
    review = state.read(scope.E/'REFERENCE-REVIEW-FINAL.json')
    binding, = review['native_current_bindings']
    generation = state.SHARED/'generations'/binding['generation_id']
    manifest_path = generation/'manifest.json'
    manifest = state.read(manifest_path)
    original = {}
    for name,sha in manifest['source']['code'].items():
        path = generation/name
        if path.is_symlink() or state.sha(path) != sha:
            raise ValueError('original source closure changed')
        original[name] = path.read_bytes()
    if kind == 'boundary':
        cases = {'matched_original':{},'new_replay_module':{'scripts/_replay_boundary_probe.py':b'# source boundary probe only\n'}}
    elif kind == 'functions':
        cases = {'matched_original':{}}
        for name,names in {**GROUPS,'all_nine':list(scope.FUNCTIONS)}.items():
            changes = {}
            for filename in set(scope.FUNCTIONS[n] for n in names):
                relative = 'scripts/'+filename
                changes[relative] = remove(original[relative],[n for n in names if scope.FUNCTIONS[n] == filename])
            cases['remove_'+name] = changes
    else:
        relative = 'scripts/photo_embedding_provider.py'
        raw = original[relative]
        node = next(n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef) and n.name == 'embed')
        lines = raw.splitlines(keepends=True)
        changed = b''.join(lines[:node.body[0].lineno-1])+b"    raise RuntimeError('historical_transport_isolated')\n"+b''.join(lines[node.end_lineno:])
        fallback = raw.replace(b"if config.is_file() else 'gemini'",b'if config.is_file() else None')
        if fallback == raw:
            raise ValueError('provider fallback probe did not change source')
        cases = {'matched_original':{},'provider_transport_boundary':{relative:changed},
                 'missing_config_no_gemini_default':{relative:fallback}}
    results = {}
    python = scope.ROOT/'skills/photo-prompt-image-generator/.runtime/embedding-python/bin/python'
    for name,changes in cases.items():
        with tempfile.TemporaryDirectory(prefix='logic-'+kind+'-') as temp:
            temp = Path(temp)
            for relative,raw in {**original,**changes}.items():
                target = temp/relative
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(raw)
            process = subprocess.run(['/usr/bin/sandbox-exec','-p',checks.profile(),str(python),
                '-I','-c',WORKER,str(temp),str(manifest_path)],env=checks.environment(),
                capture_output=True,text=True,timeout=90)
            if process.returncode:
                results[name] = {'status':'HARNESS_UNAVAILABLE','exit_code':process.returncode,
                                 'stdout':process.stdout,'stderr':process.stderr}
            else:
                results[name] = json.loads(process.stdout)
            results[name]['changed_paths'] = sorted(changes)
    process = subprocess.run(['/usr/bin/sandbox-exec','-p',checks.profile(),str(python),
        '-I','-c',WORKER,str(scope.ROOT/'skills/photo-prompt-image-generator'),str(manifest_path)],
        env=checks.environment(),capture_output=True,text=True,timeout=90)
    actual = json.loads(process.stdout) if not process.returncode else {'status':'HARNESS_UNAVAILABLE','stderr':process.stderr}
    controlled = results['matched_original'].get('status') == 'PASS' and all(
        r.get('status') == 'REJECTED' and r.get('reason') == 'runtime_restart_required'
        for n,r in results.items() if n != 'matched_original')
    report = {'schema':'photo-logic-fingerprint-pilot/v1','kind':kind,
        'generation_id':binding['generation_id'],'original_code_files':len(original),
        'cases':results,'working_baseline':actual,
        'controlled_fingerprint_regression_proved':controlled,
        'decision':'DEFER_LIVE_SOURCE_CHANGE' if controlled else 'DEFER_UNRESOLVED_PILOT',
        'scope':'actual original implementation guard in matched source-only copies; not a provider/search quality trial',
        'original_source_writes':0,'Gemini_calls':0,'CURRENT_writes':0}
    scope.new(scope.E/('PILOT-'+kind+'.json'),report)
    print(json.dumps(report,ensure_ascii=False),flush=True)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kind',choices=('boundary','functions','provider'))
    run(parser.parse_args().kind)
