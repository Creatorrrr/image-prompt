"""Immutable source/fact draft note and byte manifest."""
import datetime,hashlib,json,runpy
from pathlib import Path
R=Path(__file__).resolve().parents[1];prefix='native_05250_05250_06250.05750_05800';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads((R/f'authored/{prefix}.draft.json').read_text());D=runpy.run_path(str(R/f'authored/{prefix}.literals.py'))['D'];checks=json.loads((R/f'authored/{prefix}.partial-checks.json').read_text());n=json.loads((R/'worker-notes/native_05250_05250_06250.05700_05750.json').read_text());packet=R/f'authored/{prefix}.packet.json';birth=getattr(packet.stat(),'st_birthtime',None)
n.update(checkpoint=[5750,5800],prepared_packet_file_birth_utc=datetime.datetime.fromtimestamp(birth,datetime.timezone.utc).isoformat() if birth else None,review_stop_clock_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),counts=checks,cumulative_distinct_read_authored=550,remaining_assignment=[5800,6250])
n['catalog'].pop('prior_frozen_450_untouched',None);n['catalog']['prior_frozen_500_untouched']=True
n['validation_implementation_status']='Root unpublished working prototype, partial integrity only. No new published GEN/INPUT/ASSIGNMENT received.'
n['validation_module_hashes']=checks['validation_module_hashes']
n['limitations']=[
 'Formal INPUT/ASSIGNMENT absent; owner maps/signatures/proofs null, qualified0. Source/owner/variant corrections and creation permissions all unapproved.',
 'Validator working module is unpublished prototype; actual module byte SHAs saved. Span/hash/unit/effect checks do not prove independent semantics/native pixels/runtime/user acceptance. No automatic proofhash/signature conversion.',
 '5751/5787 exact historical corrected belt-selected/pocket-selected after source fully read, original before/corrections preserved. New native draft not an edit of those histories.',
 '5751/5755/5762/5772/5777 actual accessories remain E or source-defined P, but wearer-dependent fine wearable_accessory held without declared worn owner. Fine garment_fit/wardrobe_style similarly held where no wearer, actual outfit/fit E retained.',
 'Prior frozen checkpoints unchanged. Fullspec reread flagged possible historical native draft fine accessory proposals from type alone, e.g. 5704 headcover P and 5723 sash E; root notified separately. This is an unqualified-draft limitation, no silent retroactive revision.',
 '5757 original canonical main_subject entity_form is explicit, used only in unapproved literal ENsource harmonization. Existing one-cup/type/count P distinct actual form E; original two structured relations all six scalar leaves individually read/anchored plus full concepts/ENmeaning, no fake whole-JSON quote.',
 '5758 actual monochrome-or-restrained palette scope/local-vs-global unknown, E empty receivers retained; no arbitrary main/foreground or automatic global grade. 5761 E0 follows original same-grid carries/remains-coherent interpretation contingent independent material/grid/fold witnesses/root approval, not generic E0 material policy.',
 '5763 repair result E remains but specific physical event-residue manifestation not enough for fine aftermath trace. 5766 major joints/plate-textile-underlayer/straps/buckles attachment-load all retained, receiver/load path unknown; underlayer not automatically distinct garment.',
 '5771 Korean overlapping revision trace E retained separately from ENlayered permits with exact carrier scope unresolved. 5774 Maction-mismatch purpose clause actual scope versus existing-purpose unresolved, retained pending E rather than invented concrete actions or guard optionalization.',
 '5776 advisory label does not cancel positive distinguish/layer demand: actual separate overlay E plus mandatory sourced past-trace/anchor prerequisites. Exact past trace/source unspecified; no fabricated provenance/memory proof/impossible law.',
 '5778 actual graphic shadow/short penumbra E but unknown receiver/spatial owner, fine shape/quality held. 5779 explicit pool region and ambient level balance retained with Kbright-around-source requirement; no warm/cool color from cluster name.',
 '5781 neutral daylight balance E versus recorded white-balance/illumination color scope unresolved, source unchanged/no arbitrary material-color owner list. 5782 owned hair continuity distinct band attachment; natural/wig/represented actual owner native mapping pending, no new scalp/wearer.',
 '5783 broad skeletal frame is relative proportion not anatomical join/body_form-only fact; exact comparison baseline unknown. 5784 selected theremin keeps EN/Kcables/gaps despite Mbranch, actual light setup/soft edge/practical levels remain E with exact softness/placement pending.',
 '5786 actual under-diagnosis operation and task light retained despite unknown method/actor/configuration; no successful repair inferred. 5787 one integrated dress, internal shorts/pocket not distinct garment layers, actual fitted liner E retained.',
 '5790 row-following/autonomous behavior E retained rather than historical general-behavior dismissal; exact row/motion/control proof unknown, no actual spraying/crops invented. 5792 strap crossing/opposite attachment E retained, actual garment/back/lower receiver unspecified, no garment identity from slot/tag.',
 '5794 boundary exposure E corrected during prefreeze audit because original source says distinct, not remain. Earlier partial45 preservation wording retained as history only; no final E0 of boundary. 5795 focal person arrival positive literal proposal unapproved, familiar reaction E actors/forms unresolved, no invented crowd.',
 '5798 exact Ktypo correction retained, no measurement plane; source kind explicit but side/front frame/receiver and wrap precision pending. 5799 actual midstage/target/intermediate continuity E versus original source-feature preservation, forms/material unknown; no impossible law from metamorphosis alone.',
 'No provider/network/model/Git/canonical/register/delegation performed; source-local dynamic guard v2 not formally handed to worker and not assumed.'
]
n['manual_precision_audit']=[
 'Full50 whole SOURCE/registered5B after/compiled decisions + file-row hashes/all binding fields/intrinsic conditions/effects/base RID and empty required closure directly read; all new after strings directly reread and sameCID whole canonical equality traced for reused strings.',
 'All positive concept units, structured scalar relations and paraphrases included even when primary_paths implementation coverage is provisional. Aliases/keywords/tags/facets remain discovery, not positive evidence.',
 '5750 full construction quote supports vertical seam; 5751 Kcentral-trim relation separately typed rather than borrowing ENcontinuous precision; 5753 full distributed-one-body quote. No new wearable owner from garment/accessory names.',
 '5760 precise numeric7/8 EN/Klength harmonized into M; exact fit/ensemble quotes updated in standalone anchor-fix history. Optional socks/studio may clause remains conditional context, not selected E.',
 '5766 full attachment/load construction quotes; 5767 common anatomy.face.presence/v1,present + atomic perimeter regions, hairline not automatic hair entity. 5769 artificial eye/hardware distinct biological eye; explicit reticle symbol exact, no fabricated graphic shape.',
 '5774 entire source paragraph grounds simultaneous comparison visibility and unresolved mismatch clause, no tags-only action inference. 5775 one-thread precision Mquote only, no ENsingle-thread inference. 5777 both English pair and exact Korean pair count/metal-wire paraphrase anchored separately.',
 '5779 full bright-pool antecedent quote, 5782 full same-band hair-tail continuity and gathered-fold quotes. 5783 full frontal upperbody view and 5784 complete local owner/soft-edge/level/gap quotes avoid missing antecedents.',
 '5785 tool names do not imply actual bone chemistry/count of all scene objects. 5789 complete fastening quote binds both points/current state. 5791 Korean capture context separately typed rather than silently asserting ENset-dressing precision.',
 '5793 full deep-route door quote; 5794 original distinct boundary corrected to actual E before freeze; 5795 explicit selected one-person arrival literal proposal + full camera-attention owner quote; 5799 complete recognizable-source preservation quote.',
 'Every role/fact/effect/requires/receiver/condition/weight manually authored, exact property-prefix checks only mechanical. Pending meaning precision not automatic semantic approval.'
]
n['per_ordinal_substantive_review']=[dict(ordinal=r['ordinal'],candidate_id=r['candidate_id'],review=D[r['ordinal']]['meaning'],rejected_boundaries=r['rejected_boundaries'],binding_intent=D[r['ordinal']]['binding_intent'],remaining_owner_or_precision_issue=D[r['ordinal']]['owner_issue']) for r in d['records']]
files=set((R/'authored').glob('native_05250_05250_06250.05750_*.json'))|set((R/'authored').glob(prefix+'*.py'))
for start in range(5750,5800,5):files.add(R/f'authored/native_05250_05250_06250.{start:05d}_{start+5:05d}.append.py')
n['immutable_manifest']=[dict(file=str(p.relative_to(R)),byte_sha256=H(p)) for p in sorted(files)]
out=R/f'worker-notes/{prefix}.json'
with out.open('x') as f:f.write(json.dumps(n,ensure_ascii=False,indent=2)+'\n')
with (R/f'worker-notes/{prefix}.sha256').open('x') as f:f.write(H(out)+'  '+out.name+'\n')
assert all(H(R/a['file'])==a['byte_sha256'] for a in n['immutable_manifest'])
print(json.dumps(dict(note=str(out.relative_to(R)),byte_sha256=H(out),manifest_files=len(files),manifest_recheck_errors=0,qualified=0,cumulative_actual_read_authored=550)))
