"""Select thirteen bounded source applications and prepare fresh first20 review."""
import copy
import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT=Path.cwd(); R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
sys.path.insert(0,str(R));import prepare_native_inputs as prep
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]


def read(p):
    raw=p.read_bytes();return json.loads(gzip.decompress(raw) if p.suffix=='.gz' else raw)


def save(p,v):
    with p.open('xb') as f:f.write(c.canonical_bytes(v)+b'\n')


def ref(p):
    return dict(file=str(p.relative_to(ROOT)),file_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),sha256=c.digest(read(p)))


REASONS={
0:'Select neon as the actual type of an independently chosen existing illumination source and its actual receivers. The bare source is ambiguous; this explicitly narrows application to illumination, retaining no invented sign, text or color.',
1:'Select LED illumination designated for laboratory use. Retain lab as contextual designation of that actual source, without adding a laboratory location, worker or scientific capability. Existing carriers and relation are a disclosed new applicability restriction.',
2:'Select a softbox as the illumination source modifier. A softbox name alone does not guarantee measured softness, a complete lighting setup or a newly added apparatus. Keep the existing illumination relation and complete receivers.',
6:'Retain both flash source type and hard received light quality. Neither can disappear into the other. Do not add frontal direction, measured power, exposure or a whole setup. Existing source/receiver application is explicitly selected.',
7:'Select fluorescent-source illumination rather than surface fluorescence. This is an explicit editorial disambiguation, with no new lamp, fluorescent material, green color, flicker or inferred location.',
8:'Retain the complete travel-photograph genre and subject-matter conventions. The selected image-genre application does not establish a real journey, destination, traveler, camera or physical medium.',
10:'Retain the complete pet-photography genre and pet theme. Require independently compatible image content instead of creating an animal or inferring pet identity/species from appearance. The applicability restriction is newly explicit, not claimed as the sole historical reading.',
11:'Select the actual natural-light golden-hour phase of the same scene and its declared illumination treatment. This explicitly adds timing permission to retained lighting permission. Reject the unselected imitation-only alternative for this source revision; do not infer exact sunrise/sunset, clock, weather, hue or direction.',
12:'Retain both window-mediated route and soft received quality, with an independently established actual illumination path and complete receivers. Do not add a window, room or curtain, or invent exact direction or softness.',
13:'Retain the complete food-photography genre and food theme, with independently compatible existing content. No dish, tableware, table, cooking action, stillness or physical medium is created from genre metadata.',
14:'Select an actual dieselpunk aesthetic interpretation while preserving the original setting permission dimension. A same-canonical-fact aesthetic role view may be manually justified without moving the effect to style. Do not invent world systems, machinery, history, entities or private emotion.',
15:'Retain street photography as a complete photographic genre/convention. This explicitly selects a genre application without inventing a city, street, crowd or candid capture. A possible historical physical-location interpretation is not claimed to have been impossible.',
19:'Retain the complete interior-photography genre and interior-space theme, with independently compatible existing content. No room, furniture, architecture, person, lens or photographic medium is created by the genre choice.',
}


def main():
    proposals=R/'authored/native_06250_first20_149_02.source-alternatives.json'
    assert hashlib.sha256(proposals.read_bytes()).hexdigest()=='e73b57d9dbe738674a86e75144263b54dd2ca4ae4ec2a5ab73782e097d7d1fc1'
    alternatives=read(proposals)['records']
    selected=[r for r in alternatives if r['alternative_id']!='named_golden_hour_light_treatment_only']
    assert len(selected)==len(REASONS)==13 and {r['ordinal'] for r in selected}==set(REASONS)
    parent=R/'native-inputs/root-diagnostic-kind-source-plan-18'
    current=read(parent/'CURRENT-PROPOSAL.json.gz'); original=read(R/'SOURCE.json.gz')
    assert c.digest(current)=='08c699d25b3b6117c26f1ab6f05175b7db013ad17c69e44a9d2fd7acbcb5ea9c'
    previous=copy.deepcopy(current); approval=read(parent/'SOURCE-APPROVAL.json')
    D=R/'native-inputs/root-first20-source-plan-19';D.mkdir(exist_ok=False)
    chosen=[]
    for r in selected:
        cid=r['candidate_id']; before=current['candidates'][cid]; after=r['source_after']
        assert before==r['source_before']==original['candidates'][cid]
        assert c.digest(before)==r['source_before_sha256'] and c.digest(after)==r['source_after_sha256']
        assert prep.reviews.apply_delta(before,r['delta'])==after
        assert before['conditions']==after['conditions'] and before['provenance']==after['provenance'] and before['record_kind']==after['record_kind']
        assert before['effects']['properties']==[] and set(before['effects']['dimensions'])<=set(after['effects']['dimensions'])
        assert {k:v for k,v in after['content'].items() if k!='application_contract'}==before['content']
        assert {x['pointer'] for x in r['delta']}=={'/content/application_contract','/effects'}
        current['candidates'][cid]=copy.deepcopy(after)
        chosen.append(dict(ordinal=r['ordinal'],candidate_id=cid,alternative_id=r['alternative_id'],whole_before=before,whole_after=after,reason=REASONS[r['ordinal']],decision='selected_bounded_source_application_for_fresh_native_review_only'))
    memo=dict(schema='photo-root-first20-source-selection/v1',actor='/root',parent_source=ref(parent/'CURRENT-PROPOSAL.json.gz'),proposals=ref(proposals),selected=chosen,
        unselected_alternatives=['named_golden_hour_light_treatment_only'],
        read_scope='Root previously read all20 complete original/current sources and7 accepted native payloads. Root now directly read all14 complete proposed after records and full light_type, light_quality, time_of_day, genre, aesthetic_trend, world, subject, location, light_direction, space_condition, lighting, mood, light_color, light_shape and light_intensity specs. These rereads are not new unique corpus-review counts.',
        requirements=[
          'Freshly read each complete selected after, exact original5B and own binding/closure before writing any new fact, role or approval. Keep source intent and existing/new applicability restrictions explicit.',
          'For all illumination effects independently ground the actual existing source, whole receiving scope and physical illumination relation before discovery. The receiver scope is not a candidate-chosen subset. Preserve all original canonical/coarse permissions and actual receiver/ancestor/alias/whole locks.',
          'Retain every new actual effect, including lighting plus timing for actual golden hour, hard flash source plus quality, and soft window route plus quality. No time-named treatment to automatic aesthetic/quality/type role; no complete-setup role from a source label alone.',
          'Keep lab/pet/food/interior/travel/street qualifiers and their source-selected conditions. A generic presence witness cannot establish image-theme compatibility or lab-use designation. No genre label creates subjects or location.',
          'For dieselpunk keep setting/image/setting.aesthetic_reading; use a justified same-fact role view only after full source/spec review and actual original setting locks. No style-only permission substitution.',
          'The7 previously accepted source/proof pairs are unchanged perCID, catalog and required closure. They may be reused verbatim after checking exact equality and still-valid specs; do not manufacture7 new signatures or claim7 new semantic reviews from copying.',
          'Use controlled independent actual-source full/compact tests with old bindings, original canonical properties, every receiver, alias, ancestor, whole and unsupported-owner cases. Unknown application/scope/contract remains pending.',
          'No model/Gemini/network, operating source, production code/runtime or Git actions.'],
        source_choices=13,native_proofs_created=0,operating_changes=0,Gemini_calls=0)
    save(D/'ROOT-SOURCE-SELECTION.json',memo)
    for r in selected:
        approval['changes'].append(dict(candidate_id=r['candidate_id'],before=r['source_before'],after=r['source_after'],delta=r['delta'],reason=REASONS[r['ordinal']],provenance=[ref(proposals),ref(D/'ROOT-SOURCE-SELECTION.json')]))
    approval['current_source_sha256']=c.digest(current); approval['reason']+=' Root explicitly selects13 bounded first20 applications, without native or operating approval.'
    prep.approve_source(ROOT,original,current,approval);c.validate(current)
    assert len(approval['changes'])==84
    assert {cid for cid in current['candidates'] if current['candidates'][cid]!=previous['candidates'][cid]}=={r['candidate_id'] for r in selected}
    assert all(current[k]==previous[k] for k in ('slot_catalog','slot_bindings','policies'))
    with (D/'CURRENT-PROPOSAL.json.gz').open('xb') as f:f.write(gzip.compress(c.canonical_bytes(current),mtime=0))
    save(D/'SOURCE-APPROVAL.json',approval)
    plan=read(R/'native-inputs/first20-catalog149-recheck-plan-15/PLAN.json')
    prior=R/'native_batches/review06250-00000-00020-149-02/BATCH.json'; old=read(prior)
    plan.update(current_proposal=ref(D/'CURRENT-PROPOSAL.json.gz'),source_approval=ref(D/'SOURCE-APPROVAL.json'),
        required_revisions={r['candidate_id']:dict(prior_review=dict(artifact=ref(prior),pointer='/records/'+str(i),sha256=c.digest(r)),memo_artifacts=[ref(D/'ROOT-SOURCE-SELECTION.json')],reason='New source application selected for13 previous pending rows; retain7 exact unchanged proofs only after equality/spec/closure checks. All20 need explicit latest status.') for i,r in enumerate(old['records'])},
        reason='Fresh20 review after13 root-selected bounded applications. No automatic native transfer for changed sources; unchanged7 proofs may be reused exactly under disclosed revalidation.')
    save(D/'PLAN.json',plan)
    out,receipt=prep.write_inputs(ref(D/'PLAN.json'),'review06250-00000-00020-149-03',actor='/root',root=ROOT,here=R)
    report=dict(schema='photo-root-source-choice-preparation/v1',source=ref(D/'CURRENT-PROPOSAL.json.gz'),source_changes_total=84,new_source_choices=13,
        prepared=str(out.relative_to(ROOT)),prepared_count=20,actual_worker_read_count=0,unchanged_prior_approved_pairs=7,
        native_proofs_created=0,operating_changes=0,Gemini_calls=0,all_original_dimensions_retained=True,original_properties_renamed=0,catalog_bindings_policies_unchanged=True)
    save(D/'ROOT-PREPARATION-VERIFICATION.json',report)
    print(json.dumps(report))


if __name__=='__main__':main()
