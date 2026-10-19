"""Review known consumers; absence of static calls is only a provisional gate."""
import argparse
import ast
from collections import Counter, defaultdict
import hashlib
from pathlib import Path
import zipfile

import bundles
import logic_state as scope
import state


def main(refined=False):
    baseline = scope.load_baseline()
    targets = state.read(scope.E/'TARGETS.json')['targets']
    names = set(scope.FUNCTIONS)
    references = defaultdict(list)
    strings = defaultdict(list)
    failures = []
    scanned = Counter()

    def scan(label, data, kind):
        scanned[kind] += 1
        try:
            tree = ast.parse(data,filename=label)
        except (SyntaxError,ValueError) as error:
            failures.append({'path':label,'error':str(error),
                             'target_text_mentions':[name for name in names if name.encode() in data]})
            return
        for node in ast.walk(tree):
            name = node.id if isinstance(node,ast.Name) and isinstance(node.ctx,ast.Load) else (
                node.attr if isinstance(node,ast.Attribute) and isinstance(node.ctx,ast.Load) else None)
            if name in names:
                references[name].append({'path':label,'line':node.lineno,'kind':kind})
            if isinstance(node,ast.Constant) and isinstance(node.value,str) and node.value in names:
                strings[node.value].append({'path':label,'line':node.lineno,'kind':kind})

    for path,stamp in baseline['files'].items():
        p = Path(path)
        if p.suffix == '.py' and stamp['kind'] == 'file':
            live_roots = [scope.ROOT/'tests', *(scope.ROOT/'skills/photo-prompt-image-generator'/part
                                              for part in ('scripts','precore'))]
            live = any(p.is_relative_to(directory) for directory in live_roots)
            scan(path,p.read_bytes(),'working_source' if live else 'preserved_source')
    archive_root = scope.ROOT/'docs/research-archives/photo-prompt'
    for lockname,name in [('SOURCE-LOCK.json','h-f2-operating-source.zip'),
                          ('EXPERIMENT-LOCK.json','source-review-and-lane-experiments.zip')]:
        seal = state.read(archive_root/lockname)
        with bundles.joined_archive(archive_root/name,seal) as joined:
            if state.sha(joined) != seal['archive_sha256']:
                raise ValueError('archive changed')
            with zipfile.ZipFile(joined) as archive:
                if set(archive.namelist()) != set(seal['files']):
                    raise ValueError('archive closure changed')
                for item in archive.infolist():
                    raw = archive.read(item)
                    if hashlib.sha256(raw).hexdigest() != seal['files'][item.filename]['sha256']:
                        raise ValueError('archive member changed')
                    if item.filename.endswith('.py'):
                        scan(name+'::'+item.filename,raw,'archive')
    rows = []
    for target in targets:
        raw = state.git(scope.ROOT,'show','HEAD:'+target['path'])
        node = next(n for n in ast.parse(raw).body
                    if isinstance(n,ast.FunctionDef) and n.name == target['name'])
        same = hashlib.sha256(ast.dump(node,include_attributes=False).encode()).hexdigest() == target['ast_sha256']
        name = target['name']
        live_refs = [r for r in references[name] if r['kind'] == 'working_source']
        rows.append({**target,'same_function_AST_as_HEAD':same,
            'loaded_references':references[name],'exact_string_mentions':strings[name],
            'decision':'REMOVE_CANDIDATE_REPLAY_GATE_PENDING' if not live_refs and same else 'DEFER_REFERENCE_OR_SOURCE',
            'release_authorized':False})
    current = scope.pointers()
    working_code = {'scripts/'+p.name:state.sha(p) for p in (scope.ROOT/'skills/photo-prompt-image-generator/scripts').glob('*.py')}
    working_code.update({'precore/'+p.name:state.sha(p) for p in (scope.ROOT/'skills/photo-prompt-image-generator/precore').glob('*.py')})
    native = []
    for path in current:
        pointer = Path(path)
        if pointer.parent.parent.name == 'local' and pointer.is_relative_to(state.SHARED):
            body = state.read(pointer)
            manifest = state.read(state.SHARED/'generations'/body['generation_id']/'manifest.json')
            code = manifest['source']['code']
            native.append({'pointer':path,'generation_id':body['generation_id'],
                'generation_code_files':len(code),'working_code_files':len(working_code),
                'added':sorted(set(working_code)-set(code)), 'removed':sorted(set(code)-set(working_code)),
                'changed':sorted(p for p in set(code)&set(working_code) if code[p] != working_code[p]),
                'baseline_code_equal':working_code == code})
    report = {'schema':'photo-logic-reference-review/v1','scanned':dict(scanned),
        'parse_failures':failures,'rows':rows,'native_current_bindings':native,
        'scope':'known protected sources and original verified archives; unknown external callers are not proved absent',
        'Gemini_calls':0,'CURRENT_writes':0}
    suffix = '-FINAL' if refined else ''
    scope.new(scope.E/('REFERENCE-REVIEW'+suffix+'.json'),report)
    scope.new(scope.E/('STAGE02'+suffix+'.json'),{'status':'PASS_WITH_PENDING_GATES','functions':9,
        'provisional':dict(Counter(r['decision'] for r in rows)), 'scanned':dict(scanned),
        'parse_failures':len(failures),'historical_references':sum(len(r['loaded_references']) for r in rows),
        'native_baseline_equal':[r['baseline_code_equal'] for r in native],
        'source_changes':0,'Gemini_calls':0,'CURRENT_writes':0})
    print('review complete:',dict(scanned),'parse failures',len(failures),flush=True)
    print('provisional:',dict(Counter(r['decision'] for r in rows)),flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--refined',action='store_true')
    main(parser.parse_args().refined)
