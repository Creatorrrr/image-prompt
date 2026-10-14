"""Prepare immutable bookkeeping inputs for explicitly assigned native rereview.

No source meaning, correction, role, fact, mode, owner, proof, worker status or
read completion is authored here. Root supplies exact approved snapshots and
complete before/after proposals. Shape checks never confer native approval.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re

import native_reviews as reviews

c = reviews.dr.c
PLAN = 'photo-codex-native-input-preparation-plan/v1'
CATALOG = 'photo-codex-native-input-catalog-approval/v1'
SOURCE = 'photo-codex-native-input-source-approval/v1'
SELECTION = 'photo-codex-native-input-original-selection/v1'
PACKET = 'photo-codex-native-prepared-packet/v1'
RECEIPT = 'photo-codex-native-input-preparation-receipt/v1'


def provenance(root, refs):
    if not isinstance(refs,list) or not refs:
        raise ValueError('explicit immutable proposal provenance required')
    for ref in refs: reviews.artifact(root,ref)


def snapshot(value):
    reviews.fields(value,c.CORPUS_FIELDS,'full input snapshot')
    if value['schema'] != c.SCHEMA or any(not isinstance(value[k],dict) for k in c.CORPUS_FIELDS-{'schema'}):
        raise ValueError('full canonical source snapshot required')
    for cid,record in value['candidates'].items():
        reviews.fields(record,{'id','record_kind','content','conditions','effects','provenance'},'full source record')
        if (not c.ID.fullmatch(cid) or record['id'] != cid or record['record_kind'] not in c.KINDS
                or not isinstance(record['content'],dict) or not isinstance(record['provenance'],list)):
            raise ValueError('full source identity/kind/content/provenance shape required')
        c.validate_conditions(record['conditions'],cid); c.validate_effects(record['effects'],cid)


def approve_source(root, original, current, approval):
    """Compare only exact complete authored proposals; never derive corrections."""
    reviews.fields(approval,{'schema','actor','original_source_sha256','current_source_sha256',
        'changes','binding_changes','policy_change','reason'},'root source proposal approval')
    reviews.text(approval['reason'],'source proposal approval rationale')
    if (approval['schema'] != SOURCE or approval['actor'] != '/root'
            or approval['original_source_sha256'] != c.digest(original)
            or approval['current_source_sha256'] != c.digest(current)
            or not isinstance(approval['changes'],list) or not isinstance(approval['binding_changes'],list)):
        raise ValueError('exact root-approved full source proposal required')
    changed={cid for cid in original['candidates'] if not reviews.exact(original['candidates'][cid],current['candidates'][cid])}
    seen=set()
    for change in approval['changes']:
        reviews.fields(change,{'candidate_id','before','after','delta','reason','provenance'},'complete authored source proposal')
        cid=change['candidate_id']; reviews.text(change['reason'],'authored source proposal rationale'); provenance(root,change['provenance'])
        if (cid not in changed or cid in seen or not reviews.exact(change['before'],original['candidates'][cid])
                or not reviews.exact(change['after'],current['candidates'][cid])
                or not reviews.exact(reviews.apply_delta(change['before'],change['delta']),change['after'])
                or change['after']['provenance'][:len(change['before']['provenance'])] != change['before']['provenance']):
            raise ValueError('source correction needs exact complete before/after/delta and preserved provenance')
        seen.add(cid)
    if seen != changed: raise ValueError('every changed CID needs an explicitly approved complete source proposal')
    # Preparation may preserve historical proof bytes as given but can neither
    # install nor rewrite proof/reviewer fields through a source correction.
    for cid,before in original['candidates'].items():
        after=current['candidates'][cid]
        if (('role_evidence' in before['content']) != ('role_evidence' in after['content'])
                or not reviews.exact(before['content'].get('role_evidence'),after['content'].get('role_evidence'))):
            raise ValueError('input preparation cannot create, convert or re-sign native proofs')
    changed_bindings={bid for bid in set(original['slot_bindings'])|set(current['slot_bindings'])
        if not reviews.exact(original['slot_bindings'].get(bid),current['slot_bindings'].get(bid))}
    seen=set()
    for change in approval['binding_changes']:
        reviews.fields(change,{'binding_id','before','after','reason','provenance'},'complete authored binding proposal')
        bid=change['binding_id']; reviews.text(change['reason'],'binding proposal rationale'); provenance(root,change['provenance'])
        if (bid not in changed_bindings or bid in seen or not c.BINDING_ID.fullmatch(bid)
                or not reviews.exact(change['before'],original['slot_bindings'].get(bid))
                or not reviews.exact(change['after'],current['slot_bindings'].get(bid))
                or any(value is not None and value.get('id')!=bid for value in (change['before'],change['after']))):
            raise ValueError('binding changes require exact explicit before/after proposals')
        seen.add(bid)
    if seen!=changed_bindings: raise ValueError('all binding changes need exact root-approved proposals')
    policy=approval['policy_change']
    if reviews.exact(original['policies'],current['policies']):
        if policy is not None: raise ValueError('unchanged policies require explicit null approval')
    else:
        reviews.fields(policy,{'before','after','reason','provenance'},'complete authored policy proposal')
        reviews.text(policy['reason'],'policy proposal rationale'); provenance(root,policy['provenance'])
        if not reviews.exact(policy['before'],original['policies']) or not reviews.exact(policy['after'],current['policies']):
            raise ValueError('exact complete global policy proposal required')


def required_revisions(root, required, ids):
    if not isinstance(required,dict) or not set(required)<=set(ids):
        raise ValueError('root revision requirements must address assigned CIDs exactly')
    for value in required.values():
        reviews.fields(value,{'prior_review','memo_artifacts','reason'},'required native revision')
        reviews.text(value['reason'],'root revision requirement')
        prior=value['prior_review']; reviews.fields(prior,{'artifact','pointer','sha256'},'prior immutable judgement')
        previous=reviews.artifact(root,prior['artifact'])
        for part in reviews.pointer_parts(prior['pointer']):
            try: previous=previous[int(part)] if isinstance(previous,list) else previous[part]
            except (KeyError,IndexError,ValueError,TypeError) as exc: raise ValueError('prior judgement pointer missing') from exc
        if c.digest(previous)!=prior['sha256']: raise ValueError('prior judgement digest changed')
        provenance(root,value['memo_artifacts'])


def file_ref(root,path,value):
    """Only future file identity/hash bookkeeping, not approval or re-signing."""
    raw=c.canonical_bytes(value)+b'\n'
    return {'file':str(path.relative_to(root)),'file_sha256':hashlib.sha256(raw).hexdigest(),'sha256':c.digest(value)}


def prepare(plan_ref, name, *, actor, root=None, here=None, expected_count=reviews.PRODUCTION_COUNT):
    """Pure validation/build. Fixture count override is never exposed by CLI."""
    root=Path(root or reviews.dr.ROOT).resolve(); here=Path(here or reviews.dr.HERE).resolve()
    if actor!='/root': raise ValueError('native input preparation is root-only')
    if not isinstance(name,str) or not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,79}',name): raise ValueError('explicit new preparation name required')
    output=(here/'native-inputs'/'prepared'/name).resolve()
    if not output.is_relative_to(here/'native-inputs'/'prepared') or output.exists():
        raise ValueError('prepared inputs must use a new immutable directory')
    plan=reviews.artifact(root,plan_ref)
    reviews.fields(plan,{'schema','actor','original_snapshot','current_proposal','order','catalog_approval',
        'source_approval','original_selection','assignment','required_revisions','reason'},'root preparation plan')
    reviews.text(plan['reason'],'root preparation rationale')
    if plan['schema']!=PLAN or plan['actor']!='/root': raise ValueError('explicit root preparation plan required')
    original=reviews.artifact(root,plan['original_snapshot']); current=reviews.artifact(root,plan['current_proposal'])
    snapshot(original); snapshot(current); order=reviews.artifact(root,plan['order'])
    if (type(expected_count) is not int or expected_count<1 or not isinstance(order,list)
            or len(order)!=expected_count or len(order)!=len(set(order))
            or set(order)!=set(original['candidates']) or set(order)!=set(current['candidates'])):
        raise ValueError('full18250 exact source/current/order inventory required')
    assignment=plan['assignment']
    reviews.fields(assignment,{'task_name','model','reasoning_effort','start','end','ids'},'explicit root range assignment')
    reviews.text(assignment['task_name'],'actual assigned task')
    start,end=assignment['start'],assignment['end']; ids=assignment['ids']
    if (assignment['model']!='gpt-6.1-sol' or assignment['reasoning_effort']!='high'
            or type(start) is not int or type(end) is not int or not 0<=start<end<=len(order)
            or not isinstance(ids,list) or ids!=order[start:end]):
        raise ValueError('exact root task/model/high/CID/order range required')
    catalog=reviews.artifact(root,plan['catalog_approval'])
    reviews.fields(catalog,{'schema','actor','status','catalog','catalog_count','catalog_ids','catalog_sha256','review','reason'},'root final catalog approval')
    reviews.text(catalog['reason'],'final catalog approval rationale')
    final_catalog=reviews.artifact(root,catalog['catalog'])
    if (catalog['schema']!=CATALOG or catalog['actor']!='/root' or catalog['status']!='final_approved'
            or not reviews.exact(final_catalog,current['slot_catalog'])
            or type(catalog['catalog_count']) is not int or catalog['catalog_count']!=len(final_catalog)
            or catalog['catalog_ids']!=sorted(final_catalog) or catalog['catalog_sha256']!=c.digest(final_catalog)):
        raise ValueError('explicit root final catalog identity/count/hash approval required; provisional cannot prepare')
    reviews.verify_catalog(original['slot_catalog'],final_catalog,catalog['review'],root)
    approve_source(root,original,current,reviews.artifact(root,plan['source_approval']))
    selection=reviews.artifact(root,plan['original_selection'])
    reviews.fields(selection,{'schema','actor','original_source_sha256','records','reason'},'root original compiled selection')
    reviews.text(selection['reason'],'original selection rationale')
    if (selection['schema']!=SELECTION or selection['actor']!='/root'
            or selection['original_source_sha256']!=c.digest(original) or not isinstance(selection['records'],dict)
            or set(selection['records'])!=set(ids)):
        raise ValueError('exact root-selected original compiled/packet inventory required')
    required_revisions(root,plan['required_revisions'],ids)
    historical={}; closures={}; reference_bindings={}; cache={}
    original_sha256=c.digest(original); current_sha256=c.digest(current); original_catalog_sha256=c.digest(original['slot_catalog'])
    for cid in ids:
        selected=selection['records'][cid]
        reviews.fields(selected,{'locator','packet','reason'},'explicit original compiled item')
        reviews.text(selected['reason'],'selected historical original rationale')
        # Includes exact archived bytes + REVISION/root manifest mapping where
        # supplied; retains original declared file/item/raw/row hashes verbatim.
        historical[cid]=reviews.compiled_review(root,here,selected['locator'],original,cid,selected['packet'],
            original_sha256,original_catalog_sha256,cache)
        hashes=reviews.native.referenced_records(current['candidates'][cid],current)
        closures[cid]={key:copy.deepcopy(current['candidates'][key]) for key in hashes if c.ID.fullmatch(key)}
        reference_bindings[cid]={key:copy.deepcopy(current['slot_bindings'][key]) for key in hashes if c.BINDING_ID.fullmatch(key)}
    inp=dict(schema=reviews.INPUT,actor=plan['actor'],ids=copy.deepcopy(ids),original_snapshot=copy.deepcopy(plan['original_snapshot']),
        current_snapshot=copy.deepcopy(plan['current_proposal']),order=copy.deepcopy(plan['order']),catalog_review=copy.deepcopy(catalog['review']),
        original_decisions={cid:copy.deepcopy(selection['records'][cid]['locator']) for cid in ids},
        original_packets={cid:copy.deepcopy(selection['records'][cid]['packet']) for cid in ids},required_revisions=copy.deepcopy(plan['required_revisions']))
    assigned=dict(schema=reviews.ASSIGNMENT,actor=plan['actor'],task_name=assignment['task_name'],model=assignment['model'],
        reasoning_effort=assignment['reasoning_effort'],ids=copy.deepcopy(ids),ordinals=list(range(start,end)),input=file_ref(root,output/'INPUT.json',inp))
    packet=dict(schema=PACKET,preparation_plan=copy.deepcopy(plan_ref),assignment_sha256=c.digest(assigned),input_sha256=c.digest(inp),
        prepared_count=len(ids),actual_read_count=0,ids=copy.deepcopy(ids),ordinals=list(range(start,end)),
        original_records={cid:copy.deepcopy(original['candidates'][cid]) for cid in ids},
        current_records={cid:copy.deepcopy(current['candidates'][cid]) for cid in ids},
        references=closures,reference_bindings=reference_bindings,historical_compiled_rows=copy.deepcopy(historical),
        historical_statuses={cid:row['status'] for cid,row in historical.items()},
        original_compiled_artifacts={cid:selection['records'][cid]['locator']['file']+'#item='+str(selection['records'][cid]['locator']['item']) for cid in ids})
    documents={'INPUT.json':inp,'ASSIGNMENT.json':assigned,'PREPARED-PACKET.json':packet}
    receipt=dict(schema=RECEIPT,preparation_plan=copy.deepcopy(plan_ref),prepared_count=len(ids),actual_read_count=0,
        production_count_gate=expected_count==reviews.PRODUCTION_COUNT,original_source_sha256=original_sha256,
        current_source_sha256=current_sha256,catalog_sha256=c.digest(final_catalog),
        historical_statuses=copy.deepcopy(packet['historical_statuses']),operational_native_qualified_count=0,
        documents={filename:file_ref(root,output/filename,value) for filename,value in documents.items()},
        native_batch_written=False,native_proof_written=False,worker_read_attestation_written=False,root_acceptance_written=False,
        canonical_applied=False,semantic_accuracy_certified=False)
    documents['PREPARATION.json']=receipt
    return output,documents


def write_inputs(plan_ref,name,*,actor,root=None,here=None,expected_count=reviews.PRODUCTION_COUNT):
    """Revalidate explicit inputs immediately; only create a new research bundle."""
    output,documents=prepare(plan_ref,name,actor=actor,root=root,here=here,expected_count=expected_count)
    output.mkdir(parents=True,exist_ok=False)
    for filename,value in documents.items():
        with (output/filename).open('xb') as stream: stream.write(c.canonical_bytes(value)+b'\n')
    return output,documents['PREPARATION.json']


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--actor',required=True,choices=['/root'])
    parser.add_argument('--plan',required=True); parser.add_argument('--plan-file-sha256',required=True); parser.add_argument('--plan-sha256',required=True)
    parser.add_argument('--output-name',required=True); parser.add_argument('--check',action='store_true'); args=parser.parse_args()
    ref={'file':args.plan,'file_sha256':args.plan_file_sha256,'sha256':args.plan_sha256}
    if args.check:
        output,documents=prepare(ref,args.output_name,actor=args.actor); receipt=documents['PREPARATION.json']
    else:
        output,receipt=write_inputs(ref,args.output_name,actor=args.actor)
    print(json.dumps({'prepared_input_directory':str(output),'prepared_count':receipt['prepared_count'],
        'actual_read_count':receipt['actual_read_count'],'written':not args.check,'operational_native_qualified_count':0,'canonical_applied':False},sort_keys=True))


if __name__=='__main__': main()
