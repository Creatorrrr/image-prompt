"""Re-sign tampered experiment members; source/projection proofs must still reject."""
from pathlib import Path
import copy
import shutil
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[4];E=Path(__file__).parent
CACHE=Path.home()/'.cache/image-prompt/candidate-recall-followup-20261019'
sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
from photo_candidate_authoring import read,write,file_sha,digest
from photo_candidate_lane_generation import baseline,validate_directory


if __name__=='__main__':
    baseline(ROOT/'skills/photo-prompt-image-generator') # exact known kernel, no search
    gid=read(E/'BUILD-D1.json')['generation_id'];source=CACHE/'store/independent-lane-generations'/gid
    manifest=read(source/'manifest.json');cases={}
    mutations={
      'sparse_injection':('field-documents.json.gz',lambda x:x['rows'][0]['fields']['aliases'].append('unapproved unrelated claim')),
      'dense_injection':('documents.json.gz',lambda x:x['rows'][0].update(text=x['rows'][0]['text']+'\nunapproved unrelated claim')),
      'crossed_RID':('field-documents.json.gz',lambda x:x['rows'][0].update(id=x['rows'][1]['id'])),
      'forged_vector_proof':('document-proofs.json.gz',lambda x:next(iter(x['rows'].values())).update(vector_sha256='0'*64)),
      'unapproved_review':('reviews.json.gz',lambda x:next(iter(x['rows'].values()))['realizations']['base'].update(summary_en='unapproved replacement')),
    }
    with tempfile.TemporaryDirectory(prefix='lane-tamper-',dir=CACHE) as temp:
        root=Path(temp)/'copy';shutil.copytree(source,root)
        for name,(relative,mutation) in mutations.items():
            original=(root/relative).read_bytes();value=read(root/relative);mutation(value);write(root/relative,value)
            altered=copy.deepcopy(manifest);altered['files'][relative]=file_sha(root/relative)
            try:validate_directory(root,altered)
            except ValueError as error:cases[name]={'rejected':True,'reason':str(error)}
            else:raise AssertionError('re-signed tamper accepted: '+name)
            finally:(root/relative).write_bytes(original)
        extra=root/'runtime-code/scripts/unsealed_extra.py';extra.write_text('pass\n')
        try:validate_directory(root,manifest)
        except ValueError as error:cases['unsealed_executable']={'rejected':True,'reason':str(error)}
        else:raise AssertionError('extra executable accepted')
        extra.unlink()
        validate_directory(root,manifest)
    write(E/'GENERATION-TAMPER-CHECK.json',{'status':'PASS','cases':cases,'original_copy_revalidated':True,
        'new_search_calls':0,'new_embedding_calls':0,'source_generation_sha256':digest(manifest)})
    print('re-signed tamper rejected',len(cases),'original copy revalidated',flush=True)
