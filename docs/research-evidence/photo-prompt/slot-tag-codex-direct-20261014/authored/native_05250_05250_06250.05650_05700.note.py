"""Immutable checkpoint note and byte manifest; no semantic classifier."""
import datetime,hashlib,json,runpy
from pathlib import Path
R=Path(__file__).resolve().parents[1];prefix='native_05250_05250_06250.05650_05700';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads((R/f'authored/{prefix}.draft.json').read_text());D=runpy.run_path(str(R/f'authored/{prefix}.literals.py'))['D'];checks=json.loads((R/f'authored/{prefix}.partial-checks.json').read_text())
n=json.loads((R/'worker-notes/native_05250_05250_06250.05600_05650.json').read_text())
packet=R/f'authored/{prefix}.packet.json';birth=getattr(packet.stat(),'st_birthtime',None)
n.update(checkpoint=[5650,5700],prepared_packet_file_birth_utc=datetime.datetime.fromtimestamp(birth,datetime.timezone.utc).isoformat() if birth else None,review_stop_clock_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),counts=checks,cumulative_distinct_read_authored=450,remaining_assignment=[5700,6250])
n['catalog'].pop('prior_frozen_350_untouched',None);n['catalog']['prior_frozen_400_untouched']=True
n['read_basis'].pop('truncated_attempt_5635_5640_not_counted_until_complete_reread',None)
n['limitations']=[
 'No formal INPUT/ASSIGNMENT. Owner maps/signatures/proofs null, qualified0. All source/owner/variant harmonization and creation permissions unapproved.',
 'Integrity/hash/span/coverage/effect/spec-prefix checks do not establish independent semantic proof, native pixels, runtime or acceptance.',
 '5651 selected minimal nontext vector and actual tail-away geometry need exact comet/solar-reference owners; symbol not physical prop. 5652 existing local hands/antennas do not establish whole body pose.',
 '5657 actual warm color E keeps any previously named neutral exceptions guard unresolved; no invented field/default owner or empty-exception assumption.',
 '5660 K candle flame and 5689 K actual riding retained as explicit source harmonizations; historical no-lit/prop-only interpretations not blindly reused.',
 '5664 actual Korean concurrent decay/regeneration, 5675 calibration/measured movement/diagnostic light, 5686 compare operation and 5692 navigation behavior E retained despite unresolved observable precision.',
 '5668 literal Korean ear-to-device origin conflicts with EN/M/concept tabletop earbuds. Both actual path requirements retained, no fake ear/listener/source rewrite; root source adjudication needed.',
 '5673 original embedding kept exactly unchanged. Stem contact feature-vs-relation unresolved, no invented exact-original/dynamic guard. E0 retaining interpretation root pending, not qualified.',
 '5678 newly added performer/instrument versus original remain-visible preservation tension retained pending independent witnesses/source adjudication; no missing mechanism/support endpoint guessed.',
 '5680 Korean underwear layer selected within broader inner clothing alternative; no automatic generic-inner substitution. 5681 thermal-gauze name is not temperature/weave proof, modest coverage actual E with regions unspecified.',
 '5684 E0 preserves explicit primary product/support contact/silhouette/secondary hierarchy per retain/remain wording, contingent on independent exact witnesses/root approval; no arbitrary main selection.',
 '5694 actual cooling/gradient/removal/inspection remains E while preservation concerns prior-process evidence rather than frozen changing-gradient geometry. 5695 scanning-view motion method unspecified. 5698 terminal clock change/action exact value remains mandatory unresolved.',
 'No provider/network/model/Git/canonical/register/delegation performed.'
]
n['manual_precision_audit']=[
 '5650/5662/5688 adult modifier scoped explicitly first named staff/player/surveyor group; not expanded to second group.',
 '5651 full comet/coma/tail/reference quote, 5652 hand-each-field quote, 5655 full wax-resist quote, 5656 contact wear value not extra visibility, 5659 full cable/destination quote.',
 '5660 Korean 촛불 anchors actual flame; 5661 M environmental hydrology context not EN-only mosaic type precision; 5663 matching reference unspecified rather than invented matching contents; 5664 meta source-language phrase removed from proposed positive cue.',
 '5668 actual two-earbud count separately authored and K ear-origin value kept semantically clean; owner conflict recorded outside value. 5669 exact existing skin-feature list quote.',
 '5671 V4 explicit hot pavement separate actual panel/matte/placement; 5672 atomic landmark P/common face namespace rather than body.parts exact anatomy-list set. 5673 original unresolved stem contact source kept unchanged.',
 '5674 complete ensemble E not erased for missing wearer; 5676 actual repeated-anchor/local impossible change retained without inventing actual anchor identity; 5677 actual smooth/drape/optics/light geometry distinct from existing textile carrier.',
 '5680 actual K underwear and original open-front alternative, no long sleeves from long robe. 5683 both-temple observability/natural-hair preservation separate actual swept-hair E.',
 '5684 primary is literal source, full hierarchy quote resolves owner reference. 5685 preserved occluder pattern not blanket E0 of new shaft geometry. 5686 full comparison/placement quotes, 5689 whole K riding/broom quote.',
 '5690 whole M layer quote binds opaque undershirt and outer cloth, K thinness separate translucency. 5691 discrete solder joints not microtexture, tool contact not donated exact diagnostic point from nearby wear.',
 '5692 robot context role withheld from human-gated participant_role; asset-tag presence not lettering proof. 5693 only apron-readable fact, no whole-ensemble readability borrowed. 5694 prior evidence preservation not frozen thermal gradient. 5696 first unreadable modifier not universal all-prop text ban. 5699 metal existing rings P, actual construction/texture/aperture E.'
]
n['per_ordinal_substantive_review']=[dict(ordinal=r['ordinal'],candidate_id=r['candidate_id'],review=D[r['ordinal']]['meaning'],rejected_boundaries=r['rejected_boundaries'],binding_intent=D[r['ordinal']]['binding_intent'],remaining_owner_or_precision_issue=D[r['ordinal']]['owner_issue']) for r in d['records']]
files=set((R/'authored').glob('native_05250_05250_06250.05650_*.json'))|set((R/'authored').glob(prefix+'*.py'))
for start in range(5650,5700,5):files.add(R/f'authored/native_05250_05250_06250.{start:05d}_{start+5:05d}.append.py')
n['immutable_manifest']=[dict(file=str(p.relative_to(R)),byte_sha256=H(p)) for p in sorted(files)]
out=R/f'worker-notes/{prefix}.json'
with out.open('x') as f:f.write(json.dumps(n,ensure_ascii=False,indent=2)+'\n')
with (R/f'worker-notes/{prefix}.sha256').open('x') as f:f.write(H(out)+'  '+out.name+'\n')
assert all(H(R/a['file'])==a['byte_sha256'] for a in n['immutable_manifest'])
print(json.dumps(dict(note=str(out.relative_to(R)),byte_sha256=H(out),manifest_files=len(files),manifest_recheck_errors=0,qualified=0,cumulative_actual_read_authored=450)))
