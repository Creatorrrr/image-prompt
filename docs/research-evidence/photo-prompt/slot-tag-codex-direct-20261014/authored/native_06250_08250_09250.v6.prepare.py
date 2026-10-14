"""Explicit next-management-input bookkeeping only; no semantic decisions or rebasing."""
from pathlib import Path
import json,hashlib,copy
R=Path(__file__).resolve().parent.parent
ROOT=R.parents[3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
canon=lambda x:hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
p=R/'authored/native_06250_08250_09250.inputs.json';assert sha(p)=='9f4f4dc0a4e299270d6ecafe7fb9d82fd5705ec361a3ccfcd3d039bc5bd0383e'
old=json.loads(p.read_text());cp=R/'CATALOG-FINAL-149-V6.json';cat=json.loads(cp.read_text());assert canon(cat)=='d9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15'
ap=R/'NATIVE-CATALOG-APPROVAL-149-V6.json';a=json.loads(ap.read_text());accp=R/'CATALOG-FINAL-149-V6-ACCEPTANCE.json';acc=json.loads(accp.read_text());assert a['actor']=='/root' and a['status']=='final_approved' and a['catalog_count']==len(cat)==149 and a['catalog_ids']==sorted(cat)
assert a['catalog']['file']==str(cp.relative_to(ROOT)) and a['catalog']['file_sha256']==sha(cp) and a['catalog_sha256']==canon(cat) and a['review']['after']==cat
assert acc['actor']=='/root' and acc['status']=='final_for_fresh_native_direct_reviews_not_canonical_application' and acc['catalog']['file_sha256']==sha(cp) and acc['catalog_sha256']==canon(cat)
assert [k for k in old['full_catalog_snapshot'] if cat[k]!=old['full_catalog_snapshot'][k]]==['body_pose']
assert set(cat)-set(old['full_catalog_snapshot'])=={'material_mechanics','material_thickness','physical_mass'}
new=copy.deepcopy(old);new.update(range=[8625,9250],prepared_count=625,actual_read_count_at_preparation=0,semantic_review_or_approval_count_at_preparation=0,catalog={'file':str(cp.relative_to(ROOT)),'raw_sha256':sha(cp),'canonical_sha256':canon(cat)},full_catalog_snapshot=cat,records=old['records'][375:],parent_input={'file':str(p.relative_to(ROOT)),'raw_sha256':sha(p),'retained_source_records_and_compiled_provenance_exact':True},catalog_root_authority={str(q.relative_to(ROOT)):sha(q) for q in [ap,accp]})
new['boundary']='Prepared625/read0 under explicit root149V6 catalog for future management batches only. Original/current/5Bcompiled/ownbindings/closure/policies copied exact from pinned88614 input, not newsource snapshots or semantic approval. Prior375 drafts/proofs/catalog/signatures untouched. Allsemantic meaning/facts/modes/owners/roles remain separately manually authored after actualwhole reads.'
out=R/'authored/native_06250_08250_09250.v6.inputs.json';assert not out.exists();out.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n');print(out,sha(out),'prepared625/read0')
for srcname,dstname in [('read.py','v6.read.py'),('freeze.py','v6.freeze.py')]:
 src=R/('authored/native_06250_08250_09250.'+srcname);dst=R/('authored/native_06250_08250_09250.'+dstname);assert not dst.exists();s=src.read_text().replace('native_06250_08250_09250.inputs.json','native_06250_08250_09250.v6.inputs.json').replace('start-8250:stop-8250','start-8625:stop-8625').replace('ordinal-8250','ordinal-8625').replace('assert 8250<=start','assert 8625<=start');dst.write_text(s);print(dst,sha(dst))
