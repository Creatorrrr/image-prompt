"""Replay an actual frozen scene through the installed default, offline.

No policy/store/generation options are supplied to the managed CLI. A cold
query cache proves local inference on two directly authored new H texts. This
is an integration check, not a new semantic-quality or image assessment.
"""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[4]
E = Path(__file__).parent
S = ROOT / 'skills/photo-prompt-image-generator/scripts'
C = Path('/Users/chasoik/.cache/image-prompt/h-f2-default-install-20261018')
sys.path.insert(0, str(S))
from photo_workflow_state import load_state, bound_path, value, verify_freeze
from photo_installed_h_f2 import default_store, read, release


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


origin = C.parent / 'h-f2-skill-integration-20261018/managed-smoke'
original = load_state(origin)
verify_freeze(original)
run = C / 'installed-managed-run'
assert not run.exists(), 'preserve prior runs; choose a fresh test directory'
(run / 'frozen').mkdir(parents=True)
neutral = {'authorial_core_input', 'authorial_core_normalized', 'baseline', 'catalog',
           'creative_controls', 'embodiment_review', 'feature_selection', 'feature_selection_audit',
           'freeze_author_input_hashes', 'freeze_receipt', 'request_envelope_input',
           'request_envelope_normalized', 'request_raw'}
state = {k: copy.deepcopy(original[k]) for k in ('schema_version', 'mode', 'render_scope', 'operations')}
state.update(run_id=uuid.uuid4().hex, phase='core_frozen', artifacts={}, source_binding=None)
for role in neutral:
    source = bound_path(original, role)
    path = run / 'frozen' / (role + source.suffix)
    shutil.copyfile(source, path)
    state['artifacts'][role] = {'path': str(path), 'sha256': sha(path)}
write(run / 'workflow.json', state)
verify_freeze(state)

blocked = [Path('/Users/chasoik/.codex/worktrees/slot-search-relevance'),
           C.parent / 'h-f2-skill-integration-20261018',
           C.parent / 'd1-s-full-corpus-20261018',
           C.parent / 'd1-s-whole-pool-lane-factorial-20261018',
           C.parent / 'd1-s-query-rrf-field-ablation-20261018']
profile = C / 'offline.sb'
profile.write_text('(version 1)\n(allow default)\n(deny network*)\n' + ''.join(
    '(deny file-read* (subpath ' + json.dumps(str(p)) + '))\n' for p in blocked))
prefix = ['/usr/bin/sandbox-exec', '-f', str(profile)]
probe = subprocess.run(prefix + [sys.executable, '-c',
    "import socket; s=socket.socket(); s.connect(('127.0.0.1',9))"], capture_output=True, text=True)
assert probe.returncode != 0 and 'Operation not permitted' in probe.stderr, probe.stderr
denied = subprocess.run(prefix + [sys.executable, '-c',
    'from pathlib import Path;Path(' + repr(str(origin / 'workflow.json')) + ').read_bytes()'], capture_output=True, text=True)
assert denied.returncode != 0 and 'Operation not permitted' in denied.stderr, denied.stderr
log = []


def cli(*arguments, script='photo_workflow.py'):
    command = prefix + [str(ROOT / '.venv/bin/python'), str(S / script), *map(str, arguments)]
    result = subprocess.run(command, capture_output=True, text=True)
    item = {'command': command, 'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
    log.append(item)
    write(C / 'cli-log.json', log)
    assert result.returncode == 0, item
    return json.loads(result.stdout)


slots = ['lighting', 'composition', 'weather']
args = ['--run', run]
slotargs = [v for slot in slots for v in ('--slot', slot)]
first = cli('retrieve', *args, *slotargs)
assert first['status'] == 'needs_slot_intent_authoring'
assert not (run / '.staging/h-f2').exists(), 'no material search before direct authoring'
material = cli('prepare-slot-intents', *args, *slotargs)['material']
core = material['core']
ground = {'source_pointer': '/baseline_prompt_en', 'start': 0, 'end': len(core['baseline_prompt_en']),
          'quote': core['baseline_prompt_en'], 'source_sha256': hashlib.sha256(core['baseline_prompt_en'].encode()).hexdigest()}
rows = {}
for slot, goal, focus in [
    ('lighting', '얼굴과 천을 바치는 두 손의 관계를 부드러운 창빛으로 읽히게 한다.',
     'gentle side window illumination on a chapel attendant face and both hands supporting folded linen; readable skin and fabric within soft interior shadows'),
    ('composition', '낮은 인물에서 바쳐진 천과 높은 제단으로 시선이 이어지는 배치를 탐색한다.',
     'environmental portrait composition connecting a kneeling attendant, both hands offering folded linen and the elevated altar; retain the complete kneeling silhouette, cushion and altar edge')]:
    rows[slot] = {'status': 'search', 'reason': goal, 'expressive_goal': goal,
        'observable_targets': ['얼굴, 천을 받친 양손, 무릎을 꿇은 인물과 제단'],
        'owner_relations': ['같은 인물이 양손으로 천을 받쳐 높은 제단을 향해 바친다.'],
        'required_constraints': ['절제된 신성과 종교적 봉사의 몸가짐', '참조는 얼굴과 머리 모양에만 적용한다.'],
        'preserved_choices': ['한 인물이 제단 앞에서 천을 바치는 중심 행위'],
        'open_scope': ['기존 인물과 행위를 보존하는 빛 또는 화면 배치'], 'unknowns': [],
        'role_focus': focus, 'scene_context': 'One kneeling woman offers a folded cloth toward a stone chapel altar after worship.',
        'language': 'en', 'grounds': [ground], 'review': {'author': 'Codex',
            'rationale': '실제 동결된 장면을 읽고 이 슬롯으로 표현할 목표와 검색문을 직접 작성했다. ' + goal}}
rows['weather'] = {**{k: [] for k in ('observable_targets', 'owner_relations', 'required_constraints',
    'preserved_choices', 'open_scope', 'unknowns', 'grounds')}, 'status': 'not_applicable',
    'reason': '실내 인물과 제단의 장면이며 날씨 자체를 표현할 목표는 없다.', 'expressive_goal': '',
    'role_focus': '', 'scene_context': '', 'language': 'en', 'review': {'author': 'Codex',
        'rationale': '창빛의 방향은 조명에서 검토하며 새로운 외부 날씨를 추가할 필요는 없다.'}}
authored = C / 'authored-intents.json'
plan = C / 'slot-plan.json'
write(authored, {'overall_intent': '절제된 종교적 봉사의 장면을 보존하면서 빛과 화면 내 관계를 구체화한다.', 'slots': rows})
cli('--run', run, '--authored', authored, '--output', plan, script='build_photo_slot_intents.py')
cli('seal-slot-intents', *args, '--plan', plan)
cache = C / 'cold-query-cache'
assert not cache.exists(), 'cold local query inference required'
retrieved = cli('retrieve', *args, '--query-cache', cache)
assert retrieved['searched_slots'] == 2 and retrieved['policy'] == 'photo-h-f2/v1'
view = cli('view', *args)
packet = value(load_state(run), 'h_f2_material')
assert set(packet['goals']) == {'lighting', 'composition'}
assert len(list(cache.glob('*.json'))) == 2
for slot, goal in packet['goals'].items():
    assert goal['lane_calls'] == {'BM25F': 1, 'local_cosine': 1}
    assert (goal['considered_CIDs'], goal['considered_RIDs']) == (18180, 18182)
    assert len(goal['top8']) == 8
    assert packet['queries'][slot]['cache_hit'] is False
    assert packet['queries'][slot]['row']['execution']['provider_executed'] is True
    assert packet['queries'][slot]['row']['execution']['space']['provider'] == 'embeddinggemma2-local'
cid = packet['goals']['lighting']['top8'][0]['cid']
cli('view', *args, '--candidate-id', cid)
hashes = {str(p): sha(p) for p in cache.glob('*.json')}
reused = cli('retrieve', *args)
assert reused['reused'] and reused['additional_lane_calls'] == 0
cli('resume', *args)
composed = copy.deepcopy(value(original, 'composed'))
composed.pop('pack_id', None)
composed.pop('global_retrieval_sha256', None)
allowed = {r['id'] for r in value(load_state(run), 'pack')['semantic_clarification']['candidates']}
composed['semantic_clarification_decisions'] = [r for r in composed['semantic_clarification_decisions'] if r['clarification_id'] in allowed]
composed['h_f2_material_decisions'] = [{'slot': 'lighting', 'candidate_id': cid,
    'realization_id': packet['goals']['lighting']['top8'][0]['rid'],
    'source_sha256': packet['goals']['lighting']['top8'][0]['source_sha256'], 'use': 'skip',
    'rationale': '기본 실행과 발급 증거의 통합 검증이며 새 소재 채택이나 예술적 개선을 주장하지 않는다.'}]
cp = C / 'composed.json'
write(cp, composed)
audit = cli('compose-audit', *args, '--composed', cp)
assert audit['status'] == 'pass'
delivered = cli('deliver', *args)
assert delivered['status'] == 'pass'
assert {str(p): sha(p) for p in cache.glob('*.json')} == hashes
assert value(original, 'composed')['prompt_en'] == value(load_state(run), 'composed')['prompt_en']
assert value(original, 'authorial_core_normalized') == value(load_state(run), 'authorial_core_normalized')
before = read(C / 'before.json')
assert all(sha(path) == expected for path, expected in before['CURRENT'].items())
manifest = read(ROOT/'skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json')
existing = set()
for module in manifest['modules']:
    if module['kind'] == 'candidates':
        existing.update(read(ROOT/'skills/photo-prompt-image-generator/assets'/module['file'])['candidates'])
binding = load_state(run)['h_f2_binding']
_, release_manifest, _ = release(binding['store'], binding['generation_id'], full=True)
import gzip
locator = json.loads(gzip.decompress((Path(binding['store'])/'h-f2-generations'/binding['generation_id']/'body-locator.json.gz').read_bytes()))
assert existing == set(locator) and len(existing) == 18250
report = {'status': 'PASS', 'installed_default': True, 'explicit_policy_generation_store_flags': False,
    'run': str(run), 'origin': 'existing actual managed request and unchanged frozen core',
    'searched_slots': ['lighting', 'composition'], 'unsearched_slots': ['weather'],
    'per_searched_slot_calls': {'BM25F': 1, 'local_cosine': 1}, 'top8_connections': 16,
    'positive_CIDs_per_slot': 18180, 'RIDs_per_slot': 18182, 'existing_source_CIDs': len(existing),
    'source_CID_set_equal_to_installed_working_corpus': True, 'fresh_local_query_inference': 2,
    'query_cache_hits': 0, 'repeat_view_resume_compose_deliver_additional_searches': 0,
    'final_prompt_and_core_unchanged': True, 'compose_audit': 'pass', 'prompt_delivery': 'pass',
    'CURRENT_unchanged': True, 'Gemini_calls': 0, 'network_denied_by_OS': True,
    'research_and_build_cache_reads_denied_by_OS': [str(p) for p in blocked],
    'generation_id': binding['generation_id'], 'full_release_files_verified': len(release_manifest['files']),
    'new_semantic_quality_judgments': 0, 'image_calls': 0}
write(E/'DEFAULT-SMOKE.json', report)
print(json.dumps(report, ensure_ascii=False, indent=2))
