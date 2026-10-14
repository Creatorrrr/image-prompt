"""Pinned metadata and bounded, checksum-verified on-demand shard readers."""
from array import array
from collections import OrderedDict
from collections.abc import Mapping
import copy
import base64
import gzip
import hashlib
import os
from pathlib import Path
import sys
import threading
import zlib
import photo_candidate_corpus as c
import photo_search_layout as layout
from photo_embedding_provider import SPACE, validate_space


def identity(path):
    st=path.stat()
    return (st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns)


def regular(assets, relative):
    if not relative or '\\' in relative or ':' in relative or any(p in {'','.', '..'} for p in relative.split('/')):
        raise ValueError('unsafe search shard path')
    p=Path(assets)
    for part in relative.split('/'):
        p=p/part
        if p.is_symlink(): raise ValueError('search shard symlink')
    if not p.is_file(): raise ValueError('missing required search shard: '+relative)
    return p


def weight(value, seen=None):
    if isinstance(value,layout.PostingPage):return value.cache_weight
    seen=set() if seen is None else seen
    if id(value) in seen: return 0
    seen.add(id(value));result=sys.getsizeof(value)
    if isinstance(value,memoryview): result+=value.nbytes
    elif isinstance(value,dict): result+=sum(weight(k,seen)+weight(v,seen) for k,v in value.items())
    elif isinstance(value,(list,tuple)): result+=sum(weight(v,seen) for v in value)
    return result


class SearchReader:
    def __init__(self, assets, *, manifest_name=layout.MANIFEST, cache_limit=64*1024*1024):
        self.assets=Path(assets).resolve();self.lock=threading.RLock();self.cache=OrderedDict();self.cache_bytes=0;self.cache_limit=cache_limit;self.descriptors=OrderedDict()
        self.metrics={'reads':0,'read_bytes':0,'vector_reads':0,'vector_bytes':0,'payload_reads':0,'posting_reads':0,'cache_hits':0,'cache_peak_bytes':0}
        path=regular(self.assets,manifest_name);self.manifest=c.decode(path.read_bytes())
        validate_space(self.manifest.get('space'))
        if (self.manifest.get('schema')!=layout.SCHEMA
                or self.manifest.get('vector_type')!='float64' or self.manifest.get('endianness')!='little'
                or self.manifest.get('posting_codec')!=layout.POSTING_CODEC or self.manifest.get('vector_codec')!=layout.VECTOR_CODEC):
            raise ValueError('native search layout required')
        rows=self.manifest['shards']+[self.manifest['metadata']]
        if len({r['path'] for r in rows})!=len(rows): raise ValueError('duplicate search member')
        self.identities={r['path']:identity(regular(self.assets,r['path'])) for r in rows}
        raw=self._read(self.manifest['metadata'],'metadata')
        from photo_runtime_sources import freeze
        self.meta=freeze(c.decode(gzip.decompress(raw)))
        if self.meta['corpus_sha256']!=self.manifest['corpus_sha256']: raise ValueError('metadata corpus mismatch')
        if self.manifest.get('routing_recipe')!=layout.ROUTING_RECIPE:raise ValueError('current certified routing recipe required')
        self.quant_codes=base64.b64decode(self.meta['quantization']['codes_base64'],validate=True)
        if len(self.quant_codes)!=len(self.meta['positive_ids'])*384:raise ValueError('quantization code coverage mismatch')
        self.candidates=LazyCandidates(self)

    def check_presence(self):
        for rel,expected in self.identities.items():
            if identity(regular(self.assets,rel))!=expected: raise ValueError('pinned search shard identity changed: '+rel)

    def _read(self,row,kind):
        p=regular(self.assets,row['path'])
        if identity(p)!=self.identities[row['path']]: raise ValueError('search shard changed before read')
        if 'offset' in row:
            key=row['path'];fd=self.descriptors.pop(key,None)
            if fd is None:fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
            self.descriptors[key]=fd
            while len(self.descriptors)>64:os.close(self.descriptors.popitem(last=False)[1])
            st=os.fstat(fd)
            if (st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns)!=self.identities[key]:raise ValueError('pinned vector descriptor changed')
            raw=os.pread(fd,row['bytes'],row['offset'])
        else:raw=p.read_bytes()
        if identity(p)!=self.identities[row['path']] or len(raw)!=row['bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']:
            raise ValueError('search shard checksum/identity mismatch')
        self.metrics['reads']+=1;self.metrics['read_bytes']+=len(raw)
        if kind=='vector': self.metrics['vector_reads']+=1;self.metrics['vector_bytes']+=len(raw)
        elif kind in {'payload','posting'}: self.metrics[kind+'_reads']+=1
        return raw

    def block(self,kind,number):
        with self.lock:
            collection={'vector':'vector_shards','payload':'payload_shards','posting':'posting_shards'}[kind]
            row=self.meta[collection][number];key=(kind,row['sha256'])
            if key in self.cache:
                if identity(regular(self.assets,row['path']))!=self.identities[row['path']]: raise ValueError('cached shard identity changed')
                value,size=self.cache.pop(key);self.cache[key]=(value,size);self.metrics['cache_hits']+=1;return value
            raw=self._read(row,kind)
            if kind=='vector':
                body=layout.vector_body(raw,row)
                value=memoryview(body).cast('d')
                if len(value)!=row['count']*SPACE['dimensions']: raise ValueError('vector block length mismatch')
            elif kind=='posting':
                value=layout.PostingPage(zlib.decompress(raw),self.meta['positive_ids'])
                if len(value)!=row['count']:raise ValueError('posting block count mismatch')
            else:
                from photo_runtime_sources import freeze
                value=freeze(c.decode(gzip.decompress(raw)))
                if len(value)!=row['count']: raise ValueError('payload/posting block count mismatch')
            size=weight(value)
            while self.cache and self.cache_bytes+size>self.cache_limit:
                _,(_,old)=self.cache.popitem(last=False);self.cache_bytes-=old
            if size<=self.cache_limit:
                self.cache[key]=(value,size);self.cache_bytes+=size
                self.metrics['cache_peak_bytes']=max(self.metrics['cache_peak_bytes'],self.cache_bytes)
            return value

    def close(self):
        with self.lock:
            while self.descriptors:os.close(self.descriptors.popitem()[1])

    def __del__(self):
        if hasattr(self,'descriptors'):
            for fd in self.descriptors.values():
                try:os.close(fd)
                except OSError:pass

    def record(self,cid):
        block=self.meta['payload_locator'][cid];row=self.block('payload',block)[cid]
        if c.digest(row)!=self.meta['record_sha256'][cid]: raise ValueError('candidate locator/row hash mismatch')
        return row


class LazyCandidates(Mapping):
    def __init__(self,reader): self.reader=reader
    def __getitem__(self,cid): return self.reader.record(cid)
    def __iter__(self): return iter(self.reader.meta['payload_locator'])
    def __len__(self): return len(self.reader.meta['payload_locator'])
    def __contains__(self,cid): return cid in self.reader.meta['payload_locator']
    def __deepcopy__(self,memo): return {cid:copy.deepcopy(self[cid],memo) for cid in self}


class LazyRuntimeData(dict):
    def __init__(self,reader):
        meta=reader.meta
        super().__init__(schema=c.SCHEMA,candidates=reader.candidates,slot_catalog=meta['slot_catalog'],
                         slot_bindings=meta['slot_bindings'],policies=meta['policies'])
        self.update(meta['policies']);self.reader=reader;self.matched_profiles=set()
        self['_search_reader']=reader;self['_corpus_sha256']=meta['corpus_sha256'];self['_global_index_sha256']=c.digest(reader.manifest)
        self['_guard_source']={key:self[key] for key in c.CORPUS_FIELDS};self['_guard_source']['candidates']=meta['guards']
        self['_binding_tags']={tag:[] for tag in self['slot_catalog']}
        for bid,row in self['slot_bindings'].items():self['_binding_tags'][row['slot_id']].append(bid)
        self['_visual_meaning']={**meta['policies']['visual_meaning_contract'],'profiles':[]}
        self['_visual_meaning_lookup']={'exact_lookup':meta['profile_lookup']}
        self['candidate_bundles']=[];self['relationship_graph']={**meta['policies']['relationship_graph'],'runtime_nodes':[],'concept_profiles':[]}

    def for_core(self,core):
        import prompt_generator as g
        core_digest=c.digest(core)
        if getattr(self,'_bound_core_sha256',None)==core_digest:
            return copy.copy(self)
        result=copy.copy(self);text,_=g.authorial_core_retrieval_text(core)
        result._bound_core_sha256=core_digest
        result.matched_profiles={r['profile_id'] for r in self.reader.meta['profile_lookup'] if g.intent_alias_matches(text,r['term']) or g.intent_term_is_negated(text,r['term'])}
        result['_visual_meaning']={**self.reader.meta['policies']['visual_meaning_contract'],
                                  'profiles':[c.entry(result,cid) for cid in sorted(result.matched_profiles)]}
        graph=copy.deepcopy(self.reader.meta['policies']['relationship_graph'])
        graph['runtime_nodes']=[c.entry(self['_guard_source'],cid) for cid in graph.pop('runtime_node_refs')]
        graph['concept_profiles']=[]
        for cid in graph.pop('concept_profile_refs'):
            row=c.entry(result,cid);row['confounders']=[c.entry(result,r['candidate_ref']) for r in row['confounders']];graph['concept_profiles'].append(row)
        result['relationship_graph']=graph
        return result

    def presentations(self,ids):
        result=copy.copy(self);ids=set(ids)
        result['_visual_meaning']={**self['_visual_meaning'], 'profiles':[c.entry(result,cid) for cid in sorted(
            self.matched_profiles | {cid for cid in ids if self.reader.meta['guards'][cid]['record_kind']=='visual_profile'})]}
        bundles=[]
        for cid in sorted(ids & set(self.reader.meta['policies']['bundle_refs'])):
            row=c.entry(result,cid);members=[]
            from photo_shared_views import materialize_member
            for pointer in row['member_candidates']:
                members.append(materialize_member(result,pointer))
            row['member_candidates']=members;bundles.append(row)
        result['candidate_bundles']=bundles
        return result
