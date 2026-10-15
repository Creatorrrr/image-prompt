"""Exact source-only execution-contract proposal; no selected source write or native proof."""
import copy,gzip,hashlib,json
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');O=R/'permission-envelope-native-integration-01';P=R/'native-inputs/root-same-image-guard-source-plan-22-R02/CURRENT-PROPOSAL.json.gz'
def d(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
assert hashlib.sha256(P.read_bytes()).hexdigest()=='28650598d6e4f8260459e794938405fea4dc7879c512a54c696523f5d57514f2'
x=json.loads(gzip.decompress(P.read_bytes()));assert d(x)=='5ed4478da12e828918e4b65442c0444c00c3f639774a8900a88de5e3101af550'
cid='cand_2e72784a26885ceaa1d645d25bd9a468';before=copy.deepcopy(x['candidates'][cid]);after=copy.deepcopy(before)
addition=' This application requires the explicit photo-native-permission-envelope/v1 execution contract. Independently freeze the complete actual request/input owner, topology, member and protected-property inventory before discovery; after direct whole-source review freeze the exhaustive source-effect versus protected-anchor and joint selected-effect impact plan against the same complete selected B1 owner resolution. A missing, stale, unknown, incomplete, unreviewed or candidate-self-injected source authority, inventory or impact plan makes this application ineligible. The permission envelope is an additional permission conjunction: retain all three original canonical effects, complete values, modes, prerequisites and every actual target/receiver; it neither renames properties nor creates shadow effects or waives any existing property, ancestor, alias, whole-dimension or source guard check. For the literal item-visible preservation, final acceptance additionally requires independently reviewed typed after-state input showing that same item still visible in that same selected image, bound to the original scalar and image-relation assertion IDs, actual source spans and input bindings. Prompt substrings, desired hands-only prerequisites, relabeled supplements or a self-hashed result do not establish this preservation. Semantic completeness and correctness require independent review; no hash, selector or successful structural comparison proves them.'
after['content']['application_contract']+=addition
contract={'canonical_effect_refs':['macroApp','coverageApp','exchangeApp'],
 'basis':[{'fact_ref':'macroApp','unit_pointer':'/content/application_contract','rationale':'Whole App explicitly selects macro shot scale on actual existing image and every actual listed framing receiver.'},
          {'fact_ref':'coverageApp','unit_pointer':'/content/application_contract','rationale':'Whole App explicitly selects hands-only participant framing, preserving item visibility and complete affected owner inventory.'},
          {'fact_ref':'exchangeApp','unit_pointer':'/content/application_contract','rationale':'Whole App explicitly performs the in-progress physical item handoff with every actual participating hand as receiver.'}],
 'preservation':[{'fact_ref':'itemVisiblePreservation','image_target':'image','relation_guard_id':'item_visible_in_selected_image','relation_property':'framing.visible_in'}]}
after['content']['permission_envelope']={'schema':'photo-native-permission-envelope/v1','realizations':{'base':contract}}
assert after['effects']==before['effects'] and after['conditions']==before['conditions']
assert all(after['content'][k]==before['content'][k]for k in ['en','ko','tags'])
proposal={'schema':'photo-native-permission-source-optin-proposal/v1','task':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high',
 'method':'codex_subagent_direct_source_read','current_snapshot':{'file':str(P),'file_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'sha256':d(x)},
 'candidate_id':cid,'before':before,'before_sha256':d(before),'after':after,'after_sha256':d(after),
 'exact_delta':[{'pointer':'/content/application_contract','before':before['content']['application_contract'],'after':after['content']['application_contract'],'reason':'Explicit source opt-in to mandatory independent envelope and final typed same-item/image preservation; original effects/receivers/guards unchanged.'},
                {'pointer':'/content/permission_envelope','before_exists':False,'after':after['content']['permission_envelope'],'reason':'Versioned exact executable source contract and future manually authored native fact IDs; metadata is not positive semantic evidence.'}],
 'own_bindings':{k:v for k,v in x['slot_bindings'].items()if v['candidate_id']==cid},
 'scope':'This proposal deliberately adds a mandatory application eligibility contract. It is not a proof that all old exchange interpretations were preserved, not a native proof or actual request/inventory/after-state, and not selected by root yet. Future fact IDs are authoring locators; a fresh proof must independently support their exact values/modes/all actual receivers and meet the whole source.',
 'original_E3_and_all_Rx_guards_retained':True,'root_selected':False,'native_proof':None,'operating':False}
p=O/'SOURCE-OPTIN-PROPOSAL-v1.json';assert not p.exists();p.write_text(json.dumps(proposal,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(d(proposal));print(d(after))
