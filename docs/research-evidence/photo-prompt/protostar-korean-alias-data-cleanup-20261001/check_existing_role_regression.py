"""Read-only lexical regression comparison for three existing role fixtures."""
import argparse,hashlib,json,sys,pathlib
E=pathlib.Path(__file__).resolve().parent
R=next(p for p in E.parents if (p/'skills/photo-prompt-image-generator/scripts/prompt_generator.py').is_file())
sys.path.insert(0,str(E))
from cycle_common import g,load_freeze,states_from_freeze
from bm25f_retrieval import rank_bm25f
states=states_from_freeze(load_freeze())
queries=['마녀 빗자루 달빛 주문 수행','트레저헌터 단서 지도 발견 직전','도내 1등 초절정 미소녀 지역 평판 여러 사람 시선']
result={'source':'tests/test_photo_concept_candidate_expansion.py::test_semantic_index_ranks_new_keyword_families_near_the_top','source_sha256':hashlib.sha256((R/'tests/test_photo_concept_candidate_expansion.py').read_bytes()).hexdigest(),'scope':'Three existing lexical regression queries, not added experimental probes; zero API calls','states':{}}
for label,data in states.items():
 bm=g.build_semantic_bm25f_payload(data)
 result['states'][label]=[{'query':q,'top12':rank_bm25f(bm,{'active_request':q},limit=12)} for q in queries]
result['all_three_top12_orders_identical']=all([x['document_id'] for x in a['top12']]==[x['document_id'] for x in b['top12']] for a,b in zip(result['states']['baseline'],result['states']['proposal']))
assert result['all_three_top12_orders_identical']
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--record',action='store_true')
args=parser.parse_args()
if args.record:
 (E/'existing-role-regression-comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
else:
 assert json.loads((E/'existing-role-regression-comparison.json').read_text()) == result
print('PASS: all three existing role-query top12 orders identical; known broader fixture failure is not repaired')
