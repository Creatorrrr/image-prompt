from pathlib import Path
import math,re,sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
if not (Path(__file__).resolve().parents[1]/'scripts/photo_recall_first.py').exists():
 import os,json
 from photo_installed_h_f2 import default_store
 skill=Path(__file__).resolve().parents[1]
 config=json.loads((skill/'retrieval-runtime.json').read_bytes())
 native=Path(os.environ.get('PHOTO_H_F2_TEST_NATIVE',default_store()/'generations'/config['native_generation_id']))
 sys.path.append(str(native/'scripts'))
from photo_h_f2_query_scope import analyze,correct,counterpart_matches
from photo_h_f2_search import fuse,field_scores,known_row_contributions
T=lambda text:re.findall(r'[^\W_]+',text.casefold(),re.UNICODE)

class BoundedCorrectionTests(unittest.TestCase):
 def setup_case(self,kind):
  n=1000;m=[{'cid':f'cand_{i:032x}','rid':'base','id':f'cand_{i:032x}|base'} for i in range(n)];s=[0.]*n;s[0]=10.;s[1]=9.;d=[(n-i)/n for i in range(n)];d[0]=0.;d[1]=.7
  if kind=='format':
   q='Photographic role: Observation interpretation of an event with visible trace and declared owner.';p={0:{'role':6.,'owner':4.},1:{'observation':4.5,'interpretation':4.5}};docs={0:'palette role hierarchy and owner',1:'observation and interpretation of an event'}
  else:
   q='An observed signal, distinct from a synthetic pattern.';p={0:{'an':4.,'synthetic':3.,'pattern':3.},1:{'observed':4.5,'signal':4.5}};docs={0:'An explicit synthetic pattern',1:'An observed signal'}
  df=lambda term:{'role':159,'observation':1,'interpretation':2,'event':100,'trace':100,'visible':900,'declared':900,'owner':900}.get(term,1000)
  return m,s,d,analyze(q,T),p,docs,df
 def run_case(self,data):
  m,s,d,a,p,docs,df=data;return correct(m,s,d,a,T,fuse,lambda i:p.get(i,{}),lambda i:docs.get(i,''),df)
 def test_format_requires_semantic_agreement_and_discriminative_terms(self):
  data=self.setup_case('format');s,order,c=self.run_case(data)
  self.assertTrue(c['applied']);self.assertEqual(c['kind'],'format');self.assertEqual(order[0]['id'],data[0][1]['id']);self.assertEqual(c['new_discriminative_terms'],['interpretation','observation']);self.assertEqual(sum(a!=b for a,b in zip(s,data[1])),1);self.assertEqual(len(order),1000)
 def test_format_keeps_a_semantically_supported_winner(self):
  data=list(self.setup_case('format'));data[2][0]=1.1;s,order,c=self.run_case(data);self.assertFalse(c['applied']);self.assertEqual(s,data[1])
 def test_generic_positive_words_cannot_replace_winner(self):
  data=list(self.setup_case('format'));data[4][1]={'declared':4.5,'visible':4.5};s,order,c=self.run_case(data);self.assertFalse(c['applied']);self.assertEqual(s,data[1])
 def test_contrast_needs_owned_positive_and_counterpart_witnesses(self):
  data=self.setup_case('contrast');s,order,c=self.run_case(data);self.assertTrue(c['applied']);self.assertEqual(c['kind'],'contrast');self.assertTrue(c['positive_compound_witnesses']);self.assertEqual(len(c['counterpart_witnesses']),1);self.assertEqual(sum(a!=b for a,b in zip(s,data[1])),1)
 def test_scattered_words_are_not_a_counterpart_phrase(self):
  data=list(self.setup_case('contrast'));data[5][0]='synthetic instrument beside a pattern';s,o,c=self.run_case(data);self.assertFalse(c['applied'])
 def test_no_positive_source_compound_means_no_correction(self):
  data=list(self.setup_case('contrast'));data[5][1]='unrelated background';s,o,c=self.run_case(data);self.assertFalse(c['applied'])
 def test_replacement_must_not_repeat_counterpart(self):
  data=list(self.setup_case('contrast'));data[5][1]='observed signal in a synthetic pattern';s,o,c=self.run_case(data);self.assertFalse(c['applied'])
 def test_source_negation_is_not_positive_counterpart_evidence(self):
  a=analyze('An observed signal, distinct from a synthetic pattern.',T)
  for doc in ['not a synthetic pattern','an observed signal rather than a synthetic pattern','the words "synthetic pattern"']:
   with self.subTest(doc=doc):self.assertFalse(counterpart_matches(a,doc,T))
  self.assertTrue(counterpart_matches(a,'not only a synthetic pattern but also another thing',T))
 def test_nonfinite_contribution_fails_closed(self):
  data=list(self.setup_case('format'));data[4][0]['role']=float('nan')
  with self.assertRaises(ValueError):self.run_case(data)
 def test_known_row_arithmetic_matches_single_posting_pass(self):
  fields={'n':3,'postings':{'role':[[0,{'labels':2}],[2,{'labels':1}]],'a':[[0,{'labels':1}],[1,{'labels':1}]]},'fields':{'labels':{'b':.75,'weight':3.}},'lengths':{'labels':[3,1,1]},'average_lengths':{'labels':5/3}}
  scores,trace=field_scores(fields,'role a',T,True,trace=True)
  for i in range(3):
   known=known_row_contributions(fields,'role a',T,i);self.assertEqual(known,{t:r[i] for t,r in trace.items() if i in r});self.assertAlmostEqual(scores[i],sum(known.values()))

if __name__=='__main__':unittest.main()
