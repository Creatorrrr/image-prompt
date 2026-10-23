"""Register source-scoped optional Atompunk realizations without changing old records."""
import copy
import csv
import hashlib
import json
import sys
import uuid
from pathlib import Path

ROOT = Path('/Users/chasoik/Projects/image-prompt')
SKILL = ROOT / 'skills/photo-prompt-image-generator'
ASSETS = SKILL / 'assets'
OUT = Path(__file__).resolve().parent
RESEARCH = OUT.parent
sys.path.insert(0, str(SKILL / 'scripts'))
import photo_candidate_corpus as corpus
from photo_runtime_sources import source_update
from photo_installed_h_f2 import default_store, release


def read(path):
    return json.loads(path.read_bytes())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


CONTEXT_EN = {
    'V05': 'BDSM iconography can be borrowed as fashion or appear in consensual or coercive contexts. Clothing and restraint-shaped objects alone do not establish consent, abuse, desire or a relationship.',
    'X01': 'Atompunk and neighboring retrofuturisms are contextual genre and historical references. Do not infer a universal date, American suburb, Googie building, green glow, catastrophe or absence of digital computation from the label.',
    'X02': 'Atomic optimism, peaceful-use policy, inexpensive-energy promises, nuclear fission, fusion, miniature reactors, nuclear thermal and pulse propulsion are distinct contexts. A depicted machine does not prove its reaction, power or historical realization; the Orion artifact reconstruction remains deferred.',
    'X03': 'Artificial gravity, feedback, servomechanisms and an electronic brain name processes or interpretations. A ring, joint, console or single still does not establish rotation, gravity, intelligence or a functioning feedback loop.',
    'X04': 'Populuxe, kitsch, camp and western Tiki borrowing have distinct cultural and critical scopes. A prop does not establish a real Pacific cultural identity, a viewer response or the authenticity of a regional object.',
    'X05': 'Bombshell glamour, erotic science fiction, sexploitation, an artificial lover, sexual liberation and objectification are contextual interpretations. An artificial human shape or costume alone does not establish desire, consent, identity or a sexual relationship.',
    'X06': 'Space-age pop, lounge, exotica, stereo, electronic tonalities, public-service films, newsreels and production aesthetics require their actual audio or temporal evidence. An instrument, speaker, poster or static set alone does not prove those effects.',
    'X07': 'The Cold War, Iron Curtain, Red Scare, McCarthyism, blacklisting, Lavender Scare, military-industrial complex and technocracy are historical or institutional contexts. Appearance does not establish political beliefs, sexuality, affiliation or victim identity.',
    'X08': 'Corporate paternalism, surveillance, loyalty tests, suburban conformity, nuclear family and gender roles concern institutions and relationships. A gate, card, uniform or repeated house does not establish ownership, citizenship, kinship, consent or loyalty.',
    'X09': 'Nuclear arms races, deterrence, mutual assured destruction, brinkmanship and doomsday devices concern strategy or fiction. A map, round table or cloud shape does not establish intent, retaliation capability or global destructive power.',
    'X10': 'Fallout, radiation illness, Downwinders, nuclear colonialism and nuclear winter require environmental, historical, medical or climate evidence. Dust, complexion, snow and clothing do not establish contamination, diagnosis, victim identity or nuclear causation.',
    'X11': 'Unethical experiments, replacement paranoia, mind control, supersoldiers, eugenics and sexual captivity or coercion are contextual issues of cause, power, identity and consent. A white coat, unusual body, expression or restraint alone does not establish them.',
    'X12': 'Alien invasion, body horror, gore, splatter and robot uprising concern selected fictional events and expression. Damage, red marks or an inactive machine alone do not establish blood, death, cause, hostile intent or a rebellion.',
}

APP = ('One complete optional authored visual realization. Preserve the entire English and Korean proposition, '
       'all stated owners, counts, parts, layers, material appearances, states, depicted media, scales and directed '
       'connections together. Use only where compatible with independently frozen requester meaning and every '
       'affected dimension and property. Research graphs and citations grant no native facts, owner choices, '
       'effects permissions or source qualification. A visible surface does not establish material chemistry, '
       'radiation, causation, diagnosis, nationality, identity, beliefs, consent, consciousness, history or elapsed '
       'time. Every selected distinguishing component and endpoint must remain observable together; partial '
       'or hidden required evidence cannot pass the full case.')

# A conservative whole-source footprint; not a role-derived waiver or native fact projection.
def footprint(key):
    dims = {'appearance', 'setting', 'composition', 'relationship'}
    if key in {'E01','E02','E03','E04','E07','E08','E09','S01','S07','S09','M01','M02','M05',
               'M07','M08','M09','M12','B01','B04','B10','F01','F03','F05','F06','F07','F08',
               'L03','W03','W04','W05','W06','W07','W09','V01','V03','V04','G01','G02','H06'}:
        dims.add('material')
    if key in {'E07','E08','M01','M06','M07','F03','F05','L03','L04','V04'}:
        dims.add('lighting')
    if key in {'E08','M01','M06','M07','F05','W04','W05','W09','R07'}:
        dims.add('color')
    if key in {'E05','M11','L02','G01','R01','R04'}:
        dims.update({'action','pose'})
    if key in {'E06','S02','S06','S09','M03','M10','M12','B06','L02','W01','W02','W04','W05',
               'W06','W07','W08','V01','V02','V03','V04','G01','R01','R04','L09'}:
        dims.update({'subject','count','age'})
    if key in {'S06','M03','M10','L02','V03','V04','R01','R04','E06'}:
        dims.add('role')
    if key in {'M03','M10','B06','L02','R01','R04','L09'}:
        dims.add('pose')
    if key in {'S02','S06','S09','M11','M12','H02','H03','H04','H05','H06'}:
        dims.add('body_geometry')
    if key in {'H02','H03','H04','H05'}:
        dims.update({'subject','count','species'})
    if key in {'V01','L08','G02','B06','E03'}:
        dims.add('format')
    if key in {'W01','W02','W03','W04','W05','W06','W07','W08','W09','V01','V02','V03','V04'}:
        dims.add('style')
    if key in {'L03','L08','G02','R02','R07'}:
        dims.add('text')
    # Counts also include nonhuman objects, arms, panels, legs, antennae and depicted figures.
    if key in {'E01','E04','E09','S01','S04','S06','S08','M04','M07','M09','M11','B02','B03',
               'B04','B07','B08','B09','F01','F02','F03','F04','F05','F07','F08','F09','L01',
               'L03','L05','L07','L08','W03','G02','R03','R05','R06','R07','H06'}:
        dims.add('count')
    return sorted(dims)


def main():
    original = corpus.load(ASSETS)
    config = read(SKILL / 'retrieval-runtime.json')
    native, hm, nm = release(default_store(), config['generation_id'])
    before = {'config': config, 'store': str(default_store()), 'native': str(native),
              'corpus_sha256': corpus.digest(original), 'candidate_count': len(original['candidates']),
              'binding_count': len(original['slot_bindings']),
              'module_sha256': {m['file']: file_sha(ASSETS / m['file']) for m in read(ASSETS / corpus.MANIFEST_NAME)['modules']},
              'research_sha256': {p.name: file_sha(p) for p in RESEARCH.iterdir() if p.is_file()},
              'code_sha256': nm['source']['code']}
    assert not (OUT / 'before.json').exists(), 'Existing integration evidence must not be overwritten'
    write(OUT / 'before.json', before)
    cards = read(RESEARCH / 'semantic-cards.json')['cards']
    routes = read(RESEARCH / 'keyword-routes.json')['routes']
    sources = {s['id']: s for s in read(RESEARCH / 'sources.json')['sources']}
    with (OUT / 'POSITIVE-SOURCES.tsv').open() as f:
        prose = {r['card_id']: r for r in csv.DictReader(f, delimiter='\t')}
    positive_ids = {c['id'] for c in cards if c['mode'] in {'still','proxy','versioned'}}
    assert set(prose) == positive_ids and len(prose) == 88
    assert set(CONTEXT_EN) == {c['id'] for c in cards} - positive_ids
    seed_map = {r['id']: r for r in routes}
    candidates, bindings, registry, lookup = {}, {}, [], {}
    for card in cards:
        key = card['id']; positive = key in prose
        cid = 'cand_' + uuid.uuid5(uuid.NAMESPACE_URL, 'image-prompt/atompunk/20261023/' + key).hex
        lookup[key] = cid
        assert cid not in original['candidates']
        en = prose[key]['en'] if positive else CONTEXT_EN[key]
        ko = prose[key]['ko'] if positive else card['positive_proposal_ko'] + ' ' + card['claim_limit_ko']
        aliases = list(dict.fromkeys([seed_map[s]['en'] for s in card['seed_ids']] +
                                     [seed_map[s]['ko'] for s in card['seed_ids']]))
        meta = {**copy.deepcopy(card), 'schema':'photo-atompunk-visual-semantics/v1',
                'candidate_id':cid, 'positive_en':en if positive else None,
                'positive_ko':ko if positive else None,
                'source_details':[sources[s] for s in card['source_ids']],
                'registration_status':'authored_optional_source' if positive else 'context_diagnostic',
                'runtime_importable': True, 'native_approval':False,
                'native_qualification':'not_qualified',
                'source_provenance':'Research file SHA values, not remote page content hashes',
                'graph_scope':'Advisory reviewed authored graph; no typed native facts or owner permissions',
                'bilingual_review':'Whole English and Korean source authored together, including all source-defining owners and endpoints',
                'status':'registered_source_not_native_qualified_not_pixel_qualified'}
        registry.append(meta)
        candidates[cid] = {'id':cid, 'record_kind':'visual_option' if positive else 'diagnostic',
                           'content': {'en':en, 'ko':ko,
                                       'definition':('Complete optional authored Atompunk-compatible visual alternative: ' + en) if positive
                                       else 'Context-only distinction, excluded from positive material retrieval.',
                                       'aliases':aliases, 'application_contract':APP if positive else
                                       'Context and proof limits only. Do not prescribe an automatic still-image recipe or native permission.',
                                       'research_semantics':meta},
                           'conditions':{}, 'effects':{'dimensions':footprint(key) if positive else [], 'properties':[]},
                           'provenance':[{'source':sources[s]['url'], 'sha256':file_sha(OUT/'POSITIVE-SOURCES.tsv') if positive
                                          else file_sha(RESEARCH/'semantic-cards.json')} for s in card['source_ids']]}
        if positive:
            for slot in card['planned_slots']:
                assert slot in original['slot_catalog']
                bid = 'bind_' + uuid.uuid5(uuid.NAMESPACE_URL,cid+'/'+slot).hex
                bindings[bid] = {'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional',
                                 'semantic_role':original['slot_catalog'][slot]['semantic_role'],
                                 'conditions':{'subject_applicability':{}},'weight':1}
    proposed = copy.deepcopy(original)
    proposed['candidates'].update(candidates); proposed['slot_bindings'].update(bindings)
    corpus.validate(proposed)
    cm='photo_candidate_atompunk_20261023.json'; bm='photo_candidate_atompunk_bindings_20261023.json'
    result={'schema':'photo-atompunk-semantic-registry/v1','cards':registry,
            'keyword_routes':[{**r,'candidate_ids':[lookup[k] for k in r['card_ids']]} for r in routes],
            'existing_source_triage':read(RESEARCH/'existing-source-mapping.json')['records'],
            'counts':{'cards':len(cards),'keyword_routes':len(routes),'new_visual_options':len(prose),
                      'context_diagnostics':len(CONTEXT_EN),'new_bindings':len(bindings)},
            'native_approval':False,'pixel_qualification':'NOT_RUN'}
    with source_update(SKILL):
        assert corpus.digest(corpus.load(ASSETS)) == before['corpus_sha256'], 'Concurrent source changed; rebase required'
        manifest=read(ASSETS/corpus.MANIFEST_NAME)
        assert not any(m['file'] in {cm,bm} for m in manifest['modules'])
        write(ASSETS/cm,{'schema':corpus.MODULE_SCHEMAS['candidates'],'candidates':candidates})
        write(ASSETS/bm,{'schema':corpus.MODULE_SCHEMAS['slot_bindings'],'slot_bindings':bindings})
        manifest['modules'] += [{'file':cm,'kind':'candidates'},{'file':bm,'kind':'slot_bindings'}]
        write(ASSETS/corpus.MANIFEST_NAME,manifest)
        write(ASSETS/'photo_atompunk_semantics_20261023.json',result)
        actual=corpus.load(ASSETS); assert actual==proposed
    assert all(actual['candidates'][k]==v for k,v in original['candidates'].items())
    assert all(actual['slot_bindings'][k]==v for k,v in original['slot_bindings'].items())
    assert all(actual[k]==original[k] for k in ['slot_catalog','policies'])
    preservation={'status':'pass','old_candidates_preserved':len(original['candidates']),
                  'old_bindings_preserved':len(original['slot_bindings']),
                  'old_module_bytes_preserved':all(file_sha(ASSETS/k)==v for k,v in before['module_sha256'].items()),
                  'total_candidates':len(actual['candidates']),'total_bindings':len(actual['slot_bindings']),**result['counts']}
    write(OUT/'data-integration.json',result)
    write(OUT/'new-native-records.json',candidates)
    write(OUT/'changed-native-records.json',{})
    write(OUT/'source-preservation.json',preservation)
    print(json.dumps(preservation,ensure_ascii=False),flush=True)


if __name__ == '__main__':
    main()
