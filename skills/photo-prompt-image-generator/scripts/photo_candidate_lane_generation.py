"""Sealed independent-lane experiment generations; never updates CURRENT/config.

Baseline D/fields are copied with their original content-addressed manifest.
Every new value is reconstructed from those qualified parts and approved reviews.
The generation carries the exact kernel and projection code needed to replay it.
"""
from pathlib import Path
import hashlib
import importlib
import os
import shutil
import sys
import tempfile

from photo_candidate_authoring import read, write, digest, file_sha
from photo_candidate_documents import field_index
from photo_candidate_lane_documents import project, RECIPE, ARMS

SCHEMA = 'photo-independent-lane-generation/v1'
LOCAL_NAMES = ('photo_candidate_lane_generation.py','photo_candidate_lane_documents.py',
               'photo_candidate_authoring.py','photo_candidate_documents.py','photo_candidate_review.py')
LOCAL_CODE = {name:file_sha(Path(__file__).parent/name) for name in LOCAL_NAMES}
POLICY = {'whole_positive_pool':True,'BM25F':1,'local_cosine':1,'rrf':10,'top_k':8,
          'single_query':True,'native_authority':False,'projection':RECIPE}


def require(value, reason):
    if not value:raise ValueError(reason)


def member(root, relative):
    relative = Path(relative)
    require(not relative.is_absolute() and '..' not in relative.parts and bool(relative.parts),'unsafe member')
    root=Path(root).resolve();result=root/relative
    chain=[result];parent=result.parent
    while parent!=root:
        chain.append(parent);parent=parent.parent
    require(result.is_file() and not any(p.is_symlink() for p in chain),'missing or linked member')
    return result


def verify_files(root, files):
    for relative, expected in files.items():
        require(file_sha(member(root,relative))==expected,'sealed member changed: '+relative)


def baseline(skill_root):
    from photo_installed_h_f2 import default_store, release
    config = read(Path(skill_root)/'retrieval-runtime.json')
    native, manifest, native_manifest = release(default_store(),config['generation_id'],full=True)
    sys.path.insert(0,str(native/'scripts'))
    for name in ['photo_candidate_corpus','photo_recall_first','photo_recall_generation','photo_h_f2_generation']:
        if name in sys.modules:
            require(file_sha(sys.modules[name].__file__)==file_sha(native/'scripts'/(name+'.py')),
                    'use a fresh process; foreign native module already loaded: '+name)
    cls = importlib.import_module('photo_h_f2_generation').Generation
    return cls(default_store(),config['generation_id'],full=True),native,native_manifest


def kernel(root):
    scripts = Path(root)/'runtime-code/scripts'
    sys.path.insert(0,str(scripts))
    modules = {}
    for name in ['photo_candidate_corpus','photo_recall_generation','photo_recall_first','photo_h_f2_search']:
        if name in sys.modules:
            require(file_sha(sys.modules[name].__file__)==file_sha(scripts/(name+'.py')),'foreign loaded kernel: '+name)
        modules[name] = importlib.import_module(name)
    return modules


def accepted_reviews(rows, approval):
    require(approval.get('status')=='PASS','source comparison incomplete')
    for cid,row in rows.items():
        item = approval['reviews'][cid]
        require(row['candidate_id']==cid and row['decision']=='enrich' and
                item['sha256']==digest(row) and item['source_sha256']==row['source_sha256'],
                'review differs from parent-accepted sidecar')


def stage(store, base, native, native_manifest, reviews, approval, *, arm, skill_root, embedding_cache):
    import numpy as np
    require(arm in ARMS,'unknown document experiment')
    require(LOCAL_CODE=={n:file_sha(Path(__file__).parent/n) for n in LOCAL_NAMES},'loaded projection code changed')
    accepted_reviews(reviews,approval)
    store = Path(store);store.mkdir(parents=True,exist_ok=True)
    inferred = 0
    with tempfile.TemporaryDirectory(prefix='.independent-lanes-',dir=store) as temporary:
        dest = Path(temporary)/'generation'
        shutil.copytree(base.root,dest)
        write(dest/'baseline-manifest.json',base.manifest)
        write(dest/'baseline-native-manifest.json',native_manifest)
        (dest/'manifest.json').unlink()
        for name in ['documents.json.gz','field-documents.json.gz','fields.json.gz']:
            (dest/name).rename(dest/('baseline-'+name))
        for relative,expected in native_manifest['source']['code'].items():
            source = Path(native)/relative
            require(file_sha(source)==expected,'baseline runtime code changed')
            target = dest/'runtime-code'/relative;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(source,target)
        for name,expected in LOCAL_CODE.items():
            target = dest/'runtime-code/scripts'/name
            if target.exists():require(file_sha(target)==expected,'kernel/projection name collision')
            shutil.copyfile(Path(__file__).parent/name,target)
        write(dest/'reviews.json.gz',{'rows':reviews})
        write(dest/'review-approval.json',approval)
        original = read(dest/'baseline-documents.json.gz')['rows']
        old_fields = read(dest/'baseline-field-documents.json.gz')['rows']
        source_header = read(dest/'source-header.json.gz')
        dense = [];sparse = [];ledger = [];changed = []
        for i,(meta,doc,field) in enumerate(zip(base.metadata,original,old_fields,strict=True)):
            require(meta['id']==doc['id']==field['id'],'baseline RID mismatch')
            record = base.body.record(meta['cid'])
            row = project(doc['text'],field['fields'],record,meta['rid'],arm=arm,
                          review=reviews.get(meta['cid']),catalog=source_header['slot_catalog'])
            require(row['source_sha256']==meta['source_sha256'],'baseline source changed')
            dense.append({**doc,'text':row['text'],'text_sha256':row['text_sha256']})
            sparse.append({**field,'fields':row['fields']})
            ledger.append({k:v for k,v in row.items() if k not in {'text','fields'}})
            if row['text']!=doc['text']:changed.append(i)
        fields = field_index(sparse,base.fields['fields'])
        write(dest/'documents.json.gz',{'rows':dense})
        write(dest/'field-documents.json.gz',{'rows':sparse})
        write(dest/'projection-ledger.json.gz',{'rows':ledger})
        write(dest/'fields.json.gz',fields)
        matrix = np.memmap(dest/'vectors.f64',dtype='<f8',mode='r+',shape=(len(dense),768))
        proofs = read(dest/'document-proofs.json.gz')['rows']
        cache = Path(embedding_cache);cache.mkdir(parents=True,exist_ok=True)
        missing = {}
        for i in changed:
            doc = dense[i];key=doc['text_sha256']
            if not (cache/(key+'.json.gz')).exists():missing[key]=doc['text']
        if missing:
            from photo_h_f2_encoder import LocalEncoder
            with LocalEncoder(skill_root) as encoder:
                require(encoder.binding==base.binding,'foreign local model space')
                items = list(missing.items())
                for offset in range(0,len(items),8):
                    batch = items[offset:offset+8]
                    encoded = encoder.encode([v for _,v in batch],'document')
                    for (key,text),row in zip(batch,encoded,strict=True):
                        write(cache/(key+'.json.gz'),{'text':text,'binding':base.binding,'row':row});inferred+=1
                    print('local document inputs',min(offset+8,len(items)),len(items),flush=True)
        rf = importlib.import_module('photo_recall_first')
        for i in changed:
            doc=dense[i];cached=read(cache/(doc['text_sha256']+'.json.gz'))
            require(cached['text']==doc['text'] and cached['binding']==base.binding,'foreign cached embedding')
            rf.check_embedding(cached['row'],base.binding,doc['text'],'document')
            matrix[i]=np.asarray(cached['row']['vector'],dtype=np.float64)
            proofs[doc['text_sha256']]=cached['row']['execution']
        matrix.flush();del matrix
        write(dest/'document-proofs.json.gz',{'rows':proofs})
        files = {str(p.relative_to(dest)):file_sha(p) for p in sorted(dest.rglob('*')) if p.is_file()}
        manifest = {'schema':SCHEMA,'policy':POLICY,'arm':arm,'binding':base.binding,
                    'baseline_generation_id':base.root.name,'source_sha256':read(dest/'source-manifest.json')['source_sha256'],
                    'native_generation_id':base.manifest['native_generation_id'],'files':files,'local_code':LOCAL_CODE,
                    'CID_count':len({r['cid'] for r in base.metadata}),'RID_count':len(base.metadata),
                    'parent_review_sha256':digest(approval),'changed_dense_RIDs':len(changed)}
        identifier=digest(manifest);write(dest/'manifest.json',manifest)
        validate_directory(dest,manifest)
        target=store/'independent-lane-generations'/identifier;target.parent.mkdir(parents=True,exist_ok=True)
        require(not target.exists(),'generation already built; preserve its result')
        os.rename(dest,target)
    return {'generation_id':identifier,'arm':arm,'new_local_document_inputs':inferred,'changed_dense_RIDs':len(changed),
            'dense_vector_sha256':file_sha(target/'vectors.f64'),'CURRENT_writes':0}


def validate_directory(root, manifest):
    import numpy as np
    root=Path(root)
    require(manifest['schema']==SCHEMA and manifest['policy']==POLICY and manifest['arm'] in ARMS,'foreign lane contract')
    require(manifest['local_code']==LOCAL_CODE,'projection implementation differs from generation')
    verify_files(root,manifest['files'])
    require({str(p.relative_to(root)):file_sha(p) for p in (root/'runtime-code').rglob('*.py')} ==
            {p:h for p,h in manifest['files'].items() if p.startswith('runtime-code/') and p.endswith('.py')},
            'unsealed executable added')
    old=read(root/'baseline-manifest.json')
    require(digest(old)==manifest['baseline_generation_id'] and old['schema']=='photo-h-f2-generation/v1','qualified baseline changed')
    native=read(root/'baseline-native-manifest.json')
    require(digest(native)==old['native_generation_id']==manifest['native_generation_id'] and
            native['schema']=='photo-runtime-generation/v3','native code/source pairing changed')
    require(manifest['binding']==old['binding'],'local model binding changed')
    for relative,expected in native['source']['code'].items():
        require(file_sha(member(root,'runtime-code/'+relative))==expected,'kernel differs from qualified baseline')
    for name,expected in LOCAL_CODE.items():
        require(file_sha(member(root,'runtime-code/scripts/'+name))==expected,'projection code changed')
    renamed={'documents.json.gz':'baseline-documents.json.gz','field-documents.json.gz':'baseline-field-documents.json.gz','fields.json.gz':'baseline-fields.json.gz'}
    replaced=set(renamed)|{'vectors.f64','document-proofs.json.gz'}
    for name,sha in old['files'].items():
        if name in renamed:require(file_sha(root/renamed[name])==sha,'baseline projection changed')
        elif name not in replaced:require(file_sha(root/name)==sha,'native/source snapshot changed')
    header=read(root/'source-header.json.gz');source=read(root/'source-manifest.json')
    require(source['source_sha256']==manifest['source_sha256'],'corpus identity changed')
    modules=kernel(root);rf=modules['photo_recall_first'];corpus=modules['photo_candidate_corpus']
    body=modules['photo_recall_generation'].BodyReader(root)
    meta=read(root/'indexed-documents.json.gz');dense=read(root/'documents.json.gz')['rows']
    sparse=read(root/'field-documents.json.gz')['rows'];ledger=read(root/'projection-ledger.json.gz')['rows']
    original=read(root/'baseline-documents.json.gz')['rows'];original_fields=read(root/'baseline-field-documents.json.gz')['rows']
    approval=read(root/'review-approval.json');reviews=read(root/'reviews.json.gz')['rows'];accepted_reviews(reviews,approval)
    require(digest(approval)==manifest['parent_review_sha256'],'approval binding changed')
    require(len(meta)==manifest['RID_count']>0 and len({r['cid'] for r in meta})==manifest['CID_count'],'population mismatch')
    require(len({r['id'] for r in meta})==len(meta),'duplicate actual RID')
    matrix=np.memmap(root/'vectors.f64',dtype='<f8',mode='r',shape=(len(meta),768))
    require((root/'vectors.f64').stat().st_size==len(meta)*768*8,'vector extent mismatch')
    proofs=read(root/'document-proofs.json.gz')['rows']
    for i,(m,d,f,l,od,of) in enumerate(zip(meta,dense,sparse,ledger,original,original_fields,strict=True)):
        record=body.record(m['cid'])
        require(m['id']==m['cid']+'|'+m['rid']==d['id']==f['id']==l['id']==od['id']==of['id'],'crossed CID/RID')
        require(corpus.digest(record)==m['source_sha256']==d['source_sha256']==f['source_sha256'],'source identity changed')
        expected=project(od['text'],of['fields'],record,m['rid'],arm=manifest['arm'],review=reviews.get(m['cid']),catalog=header['slot_catalog'])
        require(d=={**od,'text':expected['text'],'text_sha256':expected['text_sha256']},'dense not exact declared source projection')
        require(f=={**of,'fields':expected['fields']},'sparse not exact declared source projection')
        require(l=={k:v for k,v in expected.items() if k not in {'text','fields'}},'projection provenance changed')
        proof=proofs[d['text_sha256']]
        rf.check_embedding({'vector':matrix[i].tolist(),'execution':proof},manifest['binding'],d['text'],'document')
    field=read(root/'fields.json.gz');old_field=read(root/'baseline-fields.json.gz')
    require(field['fields']==old_field['fields'],'F2 weights or normalization policy changed')
    require(field==field_index(sparse,old_field['fields']),'full-pool F2 statistics differ')
    require((manifest['arm']!='D1') or file_sha(root/'vectors.f64')==old['files']['vectors.f64'],'D1 changed dense vectors')
    return {'status':'PASS','CIDs':manifest['CID_count'],'RIDs':len(meta),'source_sha256':manifest['source_sha256']}


class Generation:
    def __init__(self,store,identifier):
        import re
        require(isinstance(identifier,str) and re.fullmatch('[0-9a-f]{64}',identifier),'explicit generation ID required')
        self.root=Path(store)/'independent-lane-generations'/identifier
        self.manifest=read(self.root/'manifest.json');require(digest(self.manifest)==identifier,'generation seal changed')
        self.validation=validate_directory(self.root,self.manifest)
        self.metadata=read(self.root/'indexed-documents.json.gz');self.fields=read(self.root/'fields.json.gz')
        self.binding=self.manifest['binding']

    def index(self):
        import numpy as np
        return kernel(self.root)['photo_h_f2_search'].Index(self.metadata,self.fields,
            np.memmap(self.root/'vectors.f64',dtype='<f8',mode='r',shape=(len(self.metadata),768)))
