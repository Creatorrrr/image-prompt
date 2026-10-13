import copy,json,unittest
from tests import photo_native_runtime as fixture
import prompt_generator as g
import photo_candidate_corpus as c

class CreativeControlWireReplayTests(unittest.TestCase):
 def test_canonical_json_preserves_the_original_frozen_control_hash(self):
  path=fixture.ROOT/'docs/research-evidence/photo-prompt/shared-candidate-pool-20261012/stage01/inputs/dev-02-blue-cup-en'
  snapshot=json.loads((path/'creative-controls.json').read_text());request=json.loads((path/'request-envelope.json').read_text())['request_text']
  wire=c.decode(c.canonical_bytes(snapshot));self.assertEqual(wire,snapshot)
  self.assertEqual(g.creative_controls.validate(wire,request),snapshot)
  self.assertEqual(snapshot['canonical_sha256'],'35017b45ff62bf58fdfc83aa83ea7a102eb7c1e472d32641fc1e4bd745dee698')
 def test_definition_and_control_mapping_order_cannot_change_meaning_or_brief(self):
  snapshot=g.creative_controls.resolve('A blue ceramic cup, no people.',overrides={'sensual':0,'fetish':0,'surreal':0,'creativity':1},seed=17)
  shuffled=copy.deepcopy(snapshot);shuffled['controls']=dict(reversed(list(shuffled['controls'].items())));shuffled['definitions']['controls']=dict(reversed(list(shuffled['definitions']['controls'].items())))
  self.assertEqual(g.creative_controls.validate(shuffled,'A blue ceramic cup, no people.'),snapshot)
