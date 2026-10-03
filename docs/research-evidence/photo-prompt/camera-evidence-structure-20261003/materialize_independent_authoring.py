"""Freeze an intact independent stage2 source; serialize fields without repairs."""
import argparse, hashlib, json, shutil
from pathlib import Path

EXPECTED_SHA='2f8daf037ca1d931084eb6f24033ca88bf4af2fa2134c789d9ec519893759242'
EXPECTED_BYTES=78046

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--stage1',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();raw=a.source.read_bytes()
    assert len(raw)==EXPECTED_BYTES,(len(raw),EXPECTED_BYTES)
    assert hashlib.sha256(raw).hexdigest()==EXPECTED_SHA,'Independent original source hash mismatch'
    source=json.loads(raw)
    expected={x.name for x in a.stage1.iterdir() if x.is_dir()}
    assert set(source['cases'])==expected,'Six frozen stage1 requests must all be present'
    assert source['source_commit']=='bc8e93bcdf6d61835ec51cf64324b3b18113c2b9'
    assert not a.output.exists(),'Never overwrite an initial frozen authoring arm'
    a.output.mkdir(parents=True)
    (a.output/'original-stage2-source.json').write_bytes(raw)
    bindings={}
    for ident,case in source['cases'].items():
        folder=a.output/ident;folder.mkdir()
        fields={'request_envelope':'request-envelope.json','author_context':'author-context.json',
            'authorial_core':'authorial-core.json','precore_feature_selection':'precore_feature_selection.json',
            'embodiment_review':'embodiment-review.json'}
        for key,name in fields.items():
            # Only JSON field serialization. All semantics and technical hashes
            # are retained as initially authored, including any invalid fields.
            (folder/name).write_text(json.dumps(case[key],ensure_ascii=False,indent=2)+'\n')
        shutil.copyfile(a.stage1/ident/'creative-controls.json',folder/'creative-controls.json')
        bindings[ident]={
            'envelope_same_as_stage1':case['request_envelope']==json.loads((a.stage1/ident/'request-envelope.json').read_text()),
            'context_same_as_stage1':case['author_context']==json.loads((a.stage1/ident/'author-context.json').read_text()),
            'controls_reference_matches_stage1':case['authorial_core'].get('creative_controls_sha256')==json.loads((folder/'creative-controls.json').read_text())['canonical_sha256']}
    manifest={'original_source_sha256':EXPECTED_SHA,'original_source_bytes':len(raw),
        'original_source_preserved_exactly':(a.output/'original-stage2-source.json').read_bytes()==raw,
        'runtime_frozen_at':'6220d455e869b7779e788fd712ec1e23959f5455',
        'stage1_commit':source['source_commit'],'semantic_repairs':0,'technical_hash_repairs':0,
        'serialization_note':'Separate component files are JSON serializations of unchanged original fields; only original-stage2-source.json claims the original whole-file bytes.',
        'stage1_bindings':bindings,'files':{str(x.relative_to(a.output)):hashlib.sha256(x.read_bytes()).hexdigest() for x in sorted(a.output.rglob('*')) if x.is_file()}}
    (a.output/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'cases':len(source['cases']),'source_hash_verified':True,'stage1_bindings':bindings}),flush=True)

if __name__=='__main__':main()
