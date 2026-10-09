"""Apply reviewed additive variants by identity, preserving existing authored rows."""
from pathlib import Path
import argparse, collections, copy, datetime, hashlib, json, os, re, shutil, sys

OUT=Path(__file__).resolve().parent
PRIMARY=Path('/Users/chasoik/Projects/image-prompt')
FAMILIES={'clothing_structure','fashion_fit','textile_surface','ornament_structure',
          'accessory_structure','color_relations','subculture_appearance','portrait_fashion_exposure'}

def read(path):return json.loads(path.read_text())
def canonical(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    data=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
    tmp=path.with_name(path.name+'.spring-tmp')
    tmp.write_bytes(data)
    if path.exists():os.chmod(tmp,path.stat().st_mode)
    os.replace(tmp,path)

def records(source):
    result={}
    if 'slots' in source:
        for slot,rows in source['slots'].items():
            result.update({f'slot:{slot}:{r["id"]}':r for r in rows})
        result.update({f'bundle:{r["id"]}':r for r in source.get('visual_semantics',[])})
    result.update({f'profile:{r["id"]}':r for r in source.get('profiles',[])})
    return result

parser=argparse.ArgumentParser()
parser.add_argument('--target-root',type=Path,required=True)
parser.add_argument('--phase',choices=['isolated','primary'],required=True)
parser.add_argument('--runtime-store',type=Path,required=True)
args=parser.parse_args()
root=args.target_root.resolve();skill=root/'skills/photo-prompt-image-generator';assets=skill/'assets'
sys.path.insert(0,str(skill/'scripts'))
from photo_runtime_sources import source_update
from photo_candidate_semantics import digest as authored_digest

fragments=[read(OUT/'arms'/arm/'data-fragment.json') for arm in ['knit_layer','bodice_hem','ornament_shoe']]
drafts=read(PRIMARY/'docs/research-evidence/photo-prompt/spring-fashion-20261009/candidate-drafts.json')['drafts']
all_decisions=[d for f in fragments for d in f['decisions']]
expected={d['draft_id'] for d in drafts}
assert len(all_decisions)==len(expected)==281
assert {d['draft_id'] for d in all_decisions}==expected
decisions={d['draft_id']:d for d in all_decisions}
assert all(d.get('reason') for d in all_decisions)
draft_lookup={d['draft_id']:d for d in drafts}
terms=read(PRIMARY/'docs/research-evidence/photo-prompt/spring-fashion-20261009/term-plan.json')['terms']
term_lookup={t['term_id']:t for t in terms}
keyword_bindings=[]
# These are optional lookup terms for the reviewed visible example, never hard
# activation aliases or proof of the manufacturing/property claims in a label.
for fragment in fragments:
    for group in fragment['domain_writes']:
        profiles={p['id']:p for p in group.get('profiles',[])}
        bundles={b['candidate_ids'][0]:b for b in group.get('visual_semantics',[])}
        for candidate in group.get('candidates',[]):
            decision=next(d for d in fragment['decisions'] if str(d.get('candidate_id','')).split(':')[-1]==candidate['id'])
            draft=draft_lookup[decision['draft_id']]
            labels=[]
            for term_id in draft['term_ids']:
                label=term_lookup[term_id]['label'].replace('†','').strip()
                labels.extend(part.strip() for part in label.split(' — ') if part.strip())
            labels=list(dict.fromkeys(labels))
            candidate['keywords']=list(dict.fromkeys([*candidate.get('keywords',[]),*labels]))
            candidate['embedding_text'] += ' | Optional fashion term lookup for this visible variant: ' + ' | '.join(labels)
            profile=profiles[str(decision['profile_id']).removeprefix('profile:')]
            profile.setdefault('concept_candidate',{}).setdefault('concept_terms',[]).extend(
                label+' visible variant' for label in labels)
            profile['semantics'].setdefault('claim_limits',[]).append(
                'Fashion labels provide optional discovery of this visible example only; they do not prove hidden material, process or support, or activate a family of variants.')
            if candidate['id'] in bundles:
                bundle=bundles[candidate['id']]
                bundle['source_keywords']=list(dict.fromkeys([*bundle.get('source_keywords',[]),*labels]))
            keyword_bindings.append({'draft_id':draft['draft_id'],'candidate_id':candidate['id'],
                'profile_id':profile['id'],'term_ids':draft['term_ids'],'optional_lookup_terms':labels,
                'hard_activation_expanded':False})

new_candidates,new_profiles,new_bundles=[],[],[]
planned={};before_hash={};protected={};profile_lookup={}
from photo_source_manifest import SourceInventory
inventory=SourceInventory.load(assets)
for filename,kind,required,order in inventory.rows:
    if kind=='visual_profile':
        profile_lookup.update({p['id']:p for p in read(assets/filename).get('profiles',[])})
profile_lookup.update({p['id']:p for p in read(assets/'photo_prompt_visual_obligations.json').get('profiles',[])})
for f in fragments:
    for group in f['domain_writes']:
        profile_lookup.update({p['id']:p for p in group.get('profiles',[])})

def planned_source(filename):
    if filename not in planned:
        path=assets/filename
        assert path.is_file()
        before_hash[filename]=sha(path)
        backup=OUT/f'source-before-{args.phase}'/filename
        if args.phase=='isolated' and backup.exists():
            base=read(backup)
        else:
            backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,backup);base=read(path)
        protected[filename]={key:authored_digest(row) for key,row in records(base).items()}
        planned[filename]=copy.deepcopy(base)
    return planned[filename]

def append_identity(rows,new,kind):
    existing={r['id']:r for r in rows}
    for row in new:
        if row['id'] in existing:
            assert existing[row['id']]==row, f'Conflicting {kind} ID: {row["id"]}'
        else:
            rows.append(copy.deepcopy(row));existing[row['id']]=row

for fragment in fragments:
    for group in fragment['domain_writes']:
        cf=group['candidate_file'];pf=group['profile_file'];slot=group['slot']
        assert cf.startswith('photo_prompt_') and cf.endswith('_extension.json')
        family=cf[len('photo_prompt_'):-len('_extension.json')]
        assert family in FAMILIES and pf==f'photo_prompt_visual_obligations_{family}.json'
        candidate_source=planned_source(cf);profile_source=planned_source(pf)
        assert slot in candidate_source['slots'], f'No new slot authorized: {slot}'
        candidates=group.get('candidates',[]);profiles=group.get('profiles',[])
        append_identity(candidate_source['slots'][slot],candidates,'candidate')
        append_identity(profile_source['profiles'],profiles,'profile')
        new_candidates += [{'file':cf,'slot':slot,'id':c['id']} for c in candidates]
        new_profiles += [{'file':pf,'id':p['id']} for p in profiles]
        updates=group.get('context_extensions') or {}
        if updates:
            if isinstance(updates,list):
                updates={slot:{row['candidate_id']:{key:row[key] for key in ('paraphrases','contexts') if key in row}
                               for row in updates}}
            assert isinstance(updates,dict), 'Context additions use existing_slot_context_extensions shape'
            current_updates=candidate_source.setdefault('existing_slot_context_extensions',{})
            for target_slot,targets in updates.items():
                for target_id,addition in targets.items():
                    existing=current_updates.setdefault(target_slot,{}).setdefault(target_id,{})
                    for key in ('paraphrases','contexts'):
                        if key not in addition:continue
                        values=existing.setdefault(key,[])
                        for value in addition[key]:
                            if value not in values:values.append(copy.deepcopy(value))
        provided_bundles=group.get('visual_semantics',[])
        if provided_bundles:
            append_identity(candidate_source.setdefault('visual_semantics',[]),provided_bundles,'bundle')
            new_bundles += [{'file':cf,'id':b['id']} for b in provided_bundles]
        else:
            for candidate in candidates:
                matched=[d for d in all_decisions if str(d.get('candidate_id','')).split(':')[-1]==candidate['id']]
                assert len(matched)==1,(candidate['id'],len(matched))
                profile_id=str(matched[0]['profile_id']).removeprefix('profile:')
                assert profile_id in profile_lookup
                profile=profile_lookup[profile_id]
                units=candidate['concept_units'];assert units
                bundle={'id':candidate['id']+'_bundle','primary_visual_proposition':candidate['en'],
                    'hard_profile_ids':[profile_id],
                    'component_groups':[{'id':f'component_{i}','visible_evidence':[unit]} for i,unit in enumerate(units,1)],
                    'candidate_ids':[candidate['id']], 'candidate_slots':{candidate['id']:slot},
                    'confusion_boundaries':profile['semantics']['contrast_examples'],
                    'source_keywords':list(dict.fromkeys([candidate['en'],candidate['ko'],*candidate.get('keywords',[])])),
                    'candidate_only':True,'activation_mode':'component_complete_exact_only',
                    'relations':copy.deepcopy(candidate.get('relations',[]))}
                append_identity(candidate_source.setdefault('visual_semantics',[]),[bundle],'bundle')
                new_bundles.append({'file':cf,'id':bundle['id']})

maintenance=[]
for filename,source in planned.items():
    if 'slots' in source:
        previous=source.get('maintenance_ref')
        record_id=f'{Path(filename).stem}-spring-variants-20261009'
        record={'schema_version':'photo-extension-maintenance/v1','source_filename':filename,
            'prior_maintenance_ref':previous,'change':'Add reviewed optional spring-fashion visible variants without changing prior authored records.',
            'candidate_ids':sorted(c['id'] for c in new_candidates if c['file']==filename),
            'bundle_ids':sorted(b['id'] for b in new_bundles if b['file']==filename),
            'candidate_record_sha256':{c['id']:authored_digest(next(r for r in source['slots'][c['slot']] if r['id']==c['id']))
                                       for c in new_candidates if c['file']==filename},
            'bundle_record_sha256':{b['id']:authored_digest(next(r for r in source['visual_semantics'] if r['id']==b['id']))
                                    for b in new_bundles if b['file']==filename},
            'profile_record_sha256':{p['id']:authored_digest(next(r for r in planned[p['file']]['profiles'] if r['id']==p['id']))
                                     for p in new_profiles if p['file']==filename.replace('_extension.json','.json').replace('photo_prompt_','photo_prompt_visual_obligations_',1)},
            'source_before_sha256':sha(OUT/f'source-before-{args.phase}'/filename),
            'research_source':'docs/research-evidence/photo-prompt/spring-fashion-20261009/sources.json',
            'claim_limit':'Data/index integration is distinct from retrieval, selection, rendered pixels and user acceptance.'}
        unbound_source=copy.deepcopy(source)
        unbound_source.pop('maintenance_ref',None)
        record['authored_source_sha256']=authored_digest(unbound_source)
        if previous is None:record['maintenance_only']=True
        record_path=root/'docs/research-evidence/photo-prompt/extension-maintenance'/f'{record_id}.json'
        maintenance.append((record_path,record))
        source['maintenance_ref']={'contract_version':'photo-extension-maintenance-ref/v1','record_id':record_id,'sha256':authored_digest(record)}
    after=records(source)
    assert all(key in after and authored_digest(after[key])==h for key,h in protected[filename].items()),filename

for filename,source in planned.items():
    payload=json.dumps(source,ensure_ascii=False)
    assert 'https://' not in payload or 'https://' in json.dumps(read(OUT/f'source-before-{args.phase}'/filename),ensure_ascii=False)
    assert not re.search(r'(SPR_DRAFT_|family_blueprint_not_variant_bound|Not yet bound|TODO|TBD)',payload)

for filename,expected_sha in before_hash.items():
    assert sha(assets/filename)==expected_sha,f'Source changed during merge planning: {filename}'
with source_update(skill,args.runtime_store):
    for filename,source in planned.items():write(assets/filename,source)
    for path,record in maintenance:write(path,record)
receipt={'schema_version':'spring-fashion-source-integration/v1','phase':args.phase,
    'observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_root':str(skill),
    'decisions':all_decisions,'decision_counts':dict(collections.Counter(d['decision'] for d in all_decisions)),
    'fragment_sha256':{arm:sha(OUT/'arms'/arm/'data-fragment.json') for arm in ['knit_layer','bodice_hem','ornament_shoe']},
    'optional_keyword_bindings':keyword_bindings,
    'added_candidates':new_candidates,'added_profiles':new_profiles,'added_bundles':new_bundles,
    'source_files':[{'file':name,'before_sha256':before_hash[name],'after_sha256':sha(assets/name),
                     'prior_authored_rows_preserved':len(protected[name])} for name in sorted(planned)],
    'runtime_status':'not_yet_rebuilt_or_published','metadata_only_term_ids':['SPT10-01','SPT10-02','SPT10-03','SPT10-04','SPT10-23','SPT15-06'],
    'note':'Candidate bundles remain optional; associated profiles require independent request evidence or explicit opt-in selection.'}
write(OUT/f'{args.phase.upper()}-SOURCE-INTEGRATION.json',receipt)
print(json.dumps({'phase':args.phase,'candidate_variants':len(new_candidates),'visual_profiles':len(new_profiles),
    'optional_bundles':len(new_bundles),'reviewed_drafts':len(all_decisions),'source_files':len(planned),
    'prior_authored_rows_preserved':sum(map(len,protected.values()))},indent=2))
