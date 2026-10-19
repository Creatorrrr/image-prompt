"""Verify up to three preserved Gemini receipts offline with the original archived validators."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

import bundles
import checks
import state
from history_state import new

WORKER = """
import base64,copy,hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(sys.argv[1])/'scripts'))
import photo_embedding_provider as original
from photo_candidate_corpus import digest
rows=[];first=None
for name in sys.argv[2:]:
 path=Path(name);row=json.loads(path.read_bytes());request=row['request'];space=request['space']
 if space!=original.GEMINI_SPACE:raise ValueError('historical_Gemini_receipt_required')
 if request['text_sha256']!=hashlib.sha256(request['text'].encode()).hexdigest():raise ValueError('request_text_checksum')
 if row['vector_sha256']!=digest(row['vector']):raise ValueError('vector_checksum')
 original.validate_space(space);original.validate_vector(row['vector'],space['dimensions'])
 original.validate_execution(row['execution'],space,request['text'],row['vector'])
 response=path.parent/('RESPONSE-'+str(row['execution']['attempt']).zfill(3)+'.json')
 if not response.is_file() or response.is_symlink():raise ValueError('preserved_raw_response_required')
 raw=json.loads(response.read_bytes());body=base64.b64decode(raw['body_base64'],validate=True)
 if raw['request_sha256']!=digest(request) or raw['http_status']!=200:raise ValueError('response_request_binding')
 if hashlib.sha256(body).hexdigest()!=raw['body_sha256'] or raw['body_sha256']!=row['execution']['response_sha256']:raise ValueError('response_body_checksum')
 rows.append({'path':str(path),'request_sha256':digest(request),'space':space,'raw_response_sha256':raw['body_sha256'],'original_validator':'PASS'})
 if first is None:first=row
rejected=[]
for label in ('not_executed','bad_http','bad_response_digest','nonfinite_vector'):
 row=copy.deepcopy(first)
 if label=='not_executed':row['execution']['provider_executed']=False
 elif label=='bad_http':row['execution']['http_status']=500
 elif label=='bad_response_digest':row['execution']['response_sha256']='bad'
 else:row['vector'][0]=float('nan')
 try:
  original.validate_vector(row['vector']);original.validate_execution(row['execution'],row['request']['space'],row['request']['text'],row['vector'])
 except ValueError:rejected.append(label)
 else:raise ValueError('invalid_historical_evidence_accepted: '+label)
print(json.dumps({'status':'PASS','receipts':rows,'negative_checks_rejected':rejected,
 'scope':'preserved receipt/raw-response consistency with original validators; no new provider execution',
 'Gemini_calls':0,'model_calls':0,'CURRENT_writes':0}))
"""


def verify(results):
    if not 1 <= len(results) <= 3 or len(set(map(str,results))) != len(results):
        raise ValueError('one to three distinct existing receipt paths required')
    paths = []
    for path in map(Path,results):
        if not path.is_file() or path.is_symlink():
            raise ValueError('regular existing RESULT required')
        row = state.read(path)
        paths += [path,path.parent/('RESPONSE-'+str(row['execution']['attempt']).zfill(3)+'.json')]
    before = {str(p):state.stamp(p) for p in paths}
    archive_root = state.ROOT/'docs/research-archives/photo-prompt'
    seal = state.read(archive_root/'SOURCE-LOCK.json')
    with tempfile.TemporaryDirectory(prefix='historical-evidence-') as temp:
        source = bundles.restore(archive_root/'h-f2-operating-source.zip',seal,Path(temp)/'source')
        python = state.ROOT/'skills/photo-prompt-image-generator/.runtime/embedding-python/bin/python'
        live = state.ROOT/'skills/photo-prompt-image-generator'
        policy = checks.profile()+'(deny file-read* '+ ' '.join(
            '(subpath '+json.dumps(str(live/p))+')' for p in ('scripts','precore'))+')'
        process = subprocess.run(['/usr/bin/sandbox-exec','-p',policy,str(python),'-I','-c',WORKER,
            str(source),*map(str,results)],env=checks.environment(),capture_output=True,text=True,timeout=60)
    if process.returncode:
        raise ValueError('original evidence verification failed: '+process.stderr[-3000:])
    if any(state.stamp(p) != before[str(p)] for p in paths):
        raise ValueError('original historical receipt changed')
    return {**json.loads(process.stdout),'source_archive_sha256':seal['archive_sha256'],
            'network_denied':True,'live_source_fallback_denied':True,'original_files':before}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,allow_abbrev=False)
    parser.add_argument('--result',type=Path,action='append',required=True)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('never overwrite evidence')
    result = verify(args.result)
    new(args.output,result)
    print('historical receipts PASS:',len(result['receipts']),'; negative checks:',len(result['negative_checks_rejected']),flush=True)
