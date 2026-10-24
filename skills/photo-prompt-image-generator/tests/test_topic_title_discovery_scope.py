"""A task-bearing title is not automatically the complete visual topic."""
import hashlib
import json
import os
from pathlib import Path
import sys
import unittest

SKILL=Path(__file__).resolve().parents[1]
config=json.loads((SKILL/'retrieval-runtime.json').read_bytes())
native=Path(os.environ.get('PHOTO_H_F2_TEST_NATIVE',Path.home()/'.cache/image-prompt/photo-shared-runtime/h-f2-installed/generations'/config['native_generation_id']))
sys.path.insert(0,str(native/'scripts'))
import prompt_generator as generator
import audit_composed_prompt as auditor
import photo_h_f2_queries as queries

class TopicTitleScope(unittest.TestCase):
 def check_title(self,title,topic):
  request='같은 첨부 이미지로 신규 데이터를 시험해줘.'
  spans=[]
  for key,quote in [('reference','같은 첨부 이미지'),('topic','신규 데이터')]:
   start=request.index(quote);spans.append(dict(span_id=key,start=start,end=start+len(quote),text=quote))
  topic_span=spans[1];start=title.index(topic)
  context=dict(contract_version='photo-request-topic-context/v1',links=[dict(context_id='previous-topic',active_span_id='topic',request_quote={k:topic_span[k] for k in ('start','end','text')},source_message=dict(provenance='requesting_user',locator='fixture:actual-prior-message',text=title,sha256=hashlib.sha256(title.encode()).hexdigest()),topic_quote=dict(start=start,end=start+len(topic),text=topic),review=dict(polarity='positive_topic',rationale='Exact topic including its governing visual modifiers; task suffix is workflow.'))])
  scope=dict(contract_version='photo-request-query-scope/v1',segments=[dict(active_span_id=s['span_id'],start=s['start'],end=s['end'],text=s['text'],purpose='reference_use' if s['span_id']=='reference' else 'topic_reference',reason='Reference meaning retained separately from exact prior-user topic.') for s in spans])
  envelope=dict(contract_version='photo-request-envelope/v1',provenance='requesting_user',request_id='mixed-title-regression',request_text=request,request_sha256=hashlib.sha256(request.encode()).hexdigest(),active_spans=spans,topic_context=context,query_scope=scope)
  normalized=generator._authoring_wire.normalize_request_envelope(envelope)
  core=dict(contract_version='photo-authorial-core/v3',canonical_sha256='a'*64,source_request=request,user_exclusions=[],baseline_prompt_en='A person stands beside a window in a complete photographic scene.',request_binding={k:normalized[k] for k in ('active_spans','topic_context','query_scope')})
  result=queries.whole_scene(core,{},dict(canonical_sha256='b'*64))
  self.assertEqual(result[queries.REQUEST_TOPIC]['text'],topic)
  self.assertEqual(result[queries.BASELINE_PROMPT]['text'],core['baseline_prompt_en'])
  self.assertEqual(normalized['topic_context']['links'][0]['source_message']['text'],title)
  self.assertEqual(normalized['request_text'],request)
  self.assertEqual(generator.authorial_core_retrieval_text(core)[1],auditor.expected_authorial_core_retrieval_provenance(core))

 def test_actual_research_title_suffix_is_not_the_visual_subject(self):
  self.check_title('해병문학 용어 조사','해병문학')

 def test_korean_visual_modifier_is_preserved_in_the_topic_quote(self):
  self.check_title('어두운 복도 사진 자료 조사','어두운 복도')

 def test_english_visual_modifier_is_preserved_in_the_topic_quote(self):
  self.check_title('Rain-soaked gaslamp streets — research notes','Rain-soaked gaslamp streets')

if __name__=='__main__':unittest.main()
