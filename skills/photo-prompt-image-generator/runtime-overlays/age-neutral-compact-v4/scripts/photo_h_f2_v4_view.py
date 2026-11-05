"""Isolated proposal; never import into or install over source-literal v3."""
import copy, re
import photo_h_f2_workflow as workflow
import photo_h_f2_sampling as sampling
import photo_candidate_corpus as corpus
import photo_canonical_source as canonical
import photo_h_f2_receipts as receipts
import photo_h_f2_v4_projection as projection
from photo_workflow_state import value
from photo_h_f2_v4_inventory import MANIFEST, MANIFEST_SHA256
from photo_h_f2_v4_extra_inventory import MANIFEST as EXTRA_MANIFEST, MANIFEST_SHA256 as EXTRA_MANIFEST_SHA256
import photo_h_f2_v4_extra_projection as extra_projection

SCHEMA='photo-h-f2-compact-material-view/v4-display-alias-experiment'

def view(state, candidate_ids=None, page=0):
    manifest=MANIFEST
    # v3 verifies the existing issued receipt and constructs its actual view.
    # A deep copy makes subsequent evidence checks operate on that same input.
    snapshot=copy.deepcopy(state)
    result=workflow.view(snapshot,candidate_ids=candidate_ids,page=page)
    if result.get('schema')!='photo-h-f2-compact-material-view/v3':
        raise ValueError('unexpected source display contract')
    # Reverify instead of trusting a separate disk read after v3 returned.
    packet=receipts.verify_bound(snapshot)
    receipt=value(snapshot,'h_f2_receipt')
    receipt_sha=receipt['canonical_sha256']
    if receipt_sha!=corpus.digest({k:v for k,v in receipt.items() if k!='canonical_sha256'}) or receipt['material_sha256']!=packet['canonical_sha256'] or receipt['generation_id']!=snapshot['h_f2_binding']['generation_id']:
        raise ValueError('current receipt identity mismatch')
    evidence=[]
    for slot,items in result['materials'].items():
        rows=sampling.candidates(packet['goals'][slot])
        for i,material in enumerate(items):
            cid=material['candidate_id'];matches=[r for r in rows if r['cid']==cid]
            if len(matches)!=1: raise ValueError('candidate not uniquely issued in slot')
            row=matches[0];source=packet['sources'][cid]
            if row['source_sha256']!=corpus.digest(source):raise ValueError('issued source mismatch')
            if row['rid'] not in source['meaning']['primary']:raise ValueError('foreign RID')
            if workflow.compact_material(source,row)!=material:raise ValueError('issued material changed')
            native=canonical.native_snapshot(source)
            # A newer/older source may reuse the CID.  An explicit adult guard
            # requires the source-literal version and must never be aliased.
            spec=manifest.get(cid)
            if spec and projection.digest(native)!=spec['sha256'] and native.get('conditions',{}).get('requires_adult_context') is True:
                continue
            projected,info=projection.project(material,native,manifest,issued_material=material)
            if cid in EXTRA_MANIFEST:
                if info['state']!='unchanged_unmatched':raise ValueError('overlapping display inventories')
                projected,info=extra_projection.project(material,native,rid=row['rid'])
            items[i]=projected
            if info['state']=='projected':
                evidence.append({'slot':slot,'candidate_id':cid,'rid':row['rid'],
                    'issued_source_sha256':row['source_sha256'],'native_snapshot_sha256':info['source_sha256'],
                    'display_to_source':info['reverse_aliases'],
                    'reviewed_sites':info.get('reviewed_sites',spec['pointers'] if spec else []),
                    'additional_sites':info.get('additional_sites',[])})
    result['schema']=SCHEMA
    result['display_contract']='Source-bound display aliases are not original identifier literals; native decisions retain issued identities.'
    proof={'schema':'photo-h-f2-v4-alias-evidence/v1','material_sha256':packet['canonical_sha256'],'receipt_sha256':receipt_sha,'request_id':receipt['request_id'],'generation_id':receipt['generation_id'],'entries':evidence}
    proof['canonical_sha256']=corpus.digest(proof)
    if receipts.verify_bound(snapshot)!=packet or value(snapshot,'h_f2_receipt')!=receipt:
        raise ValueError('current receipt changed during projection')
    result['display_binding']={'receipt_sha256':receipt_sha,'material_sha256':packet['canonical_sha256'],'projection_evidence_sha256':proof['canonical_sha256'],'reviewed_inventory_sha256':corpus.digest({'base':MANIFEST_SHA256,'additional':EXTRA_MANIFEST_SHA256})}
    return result,proof

def resolve_selector(evidence, *, receipt_sha256, material_sha256, slot, candidate_id, rid, issued_source_sha256, namespace, selector):
    """Translate one reviewed display alias before any native owner/gate consumer.

    The trusted caller supplies material_sha256 from the currently verified
    receipt, never from the model or its submitted evidence. Deliberately
    accepts only aliases explicitly emitted by this material view; callers
    keep already-native IDs on their normal source-bound path.
    """
    if namespace not in ('owner','gate'):raise ValueError('unknown selector namespace')
    if evidence.get('canonical_sha256')!=corpus.digest({k:v for k,v in evidence.items() if k!='canonical_sha256'}):
        raise ValueError('alias evidence changed')
    if (not isinstance(material_sha256,str) or not re.fullmatch(r'[0-9a-f]{64}',material_sha256)
        or not isinstance(receipt_sha256,str) or not re.fullmatch(r'[0-9a-f]{64}',receipt_sha256) or evidence.get('receipt_sha256')!=receipt_sha256
        or evidence.get('schema')!='photo-h-f2-v4-alias-evidence/v1' or evidence.get('material_sha256')!=material_sha256):
        raise ValueError('alias evidence bound to another material receipt')
    rows=[e for e in evidence['entries'] if (e['slot'],e['candidate_id'],e['rid'],e['issued_source_sha256'])==
          (slot,candidate_id,rid,issued_source_sha256)]
    if len(rows)!=1:raise ValueError('selector scope is not uniquely bound')
    mapping=rows[0]['display_to_source']
    if not selector.startswith(namespace+'_') or selector not in mapping:raise ValueError('foreign display selector')
    return mapping[selector]
