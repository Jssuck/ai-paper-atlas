import unittest
from model import Invalid,Model,check,infer,expression,fact
P=('atom','P'); Q=('atom','Q'); G=('atom','G'); EP=('some','of',P)
class Tests(unittest.TestCase):
 def test_wisdom(self):
  premises=(('member',P,'wisdom'),('edge','of','wisdom','good'))
  goal=('member',EP,'good')
  self.assertEqual(check(premises,({'rule':'project','refs':(0,1),'conclusion':goal},))[-1],goal)
 def test_having_vs_being(self):
  for target in (G,('some','of',G)):
   self.assertEqual(infer('instantiate',(('subset',EP,target),('member',EP,'good'))),('member',target,'good'))
 def test_negative(self):
  self.assertEqual(infer('exclude',(('disjoint',EP,G),('member',EP,'pleasure'))),('notmember',G,'pleasure'))
 def test_difference(self):
  self.assertEqual(infer('difference',(('member',P,'god'),('notmember',Q,'god'))),('not_subset',P,Q))
 def test_transitive(self):
  self.assertEqual(infer('transitive',(('subset',P,Q),('subset',Q,G))),('subset',P,G))
 def test_mismatches(self):
  bad=[('project',(('member',P,'a'),('edge','of','b','a'))),('instantiate',(('subset',EP,Q),('member',P,'a'))),('exclude',(('disjoint',P,Q),('member',Q,'a'))),('difference',(('member',P,'a'),('notmember',Q,'b'))),('transitive',(('subset',P,Q),('subset',P,G))),('unknown',(('subset',P,Q),('subset',Q,G)))]
  for r,fs in bad:
   with self.subTest(r=r), self.assertRaises(Invalid):infer(r,fs)
 def test_expression_validation(self):
  for e in (['atom','P'],('atom',''),('atom','P','x'),('some','of'),('some','of',('bad','P')),('atom',True)):
   with self.subTest(e=e),self.assertRaises(Invalid):expression(e)
 def test_fact_validation(self):
  for f in ((),('member',P),('edge','of','a'),('member',P,True),('subset',P,'Q')):
   with self.subTest(f=f),self.assertRaises(Invalid):fact(f)
 def test_certificate_refs(self):
  for refs in ((True,1),(-1,1),(0,2),[0,1],(0,)):
   with self.subTest(refs=refs),self.assertRaises(Invalid):check((('member',P,'a'),('edge','of','a','b')),({'rule':'project','refs':refs,'conclusion':('member',EP,'b')},))
 def test_certificate_forgery(self):
  for step in ({'rule':'project','refs':(0,1),'conclusion':('member',P,'b')},{'rule':'project','refs':(0,1),'conclusion':('member',EP,'b'),'extra':True}):
   with self.assertRaises(Invalid):check((('member',P,'a'),('edge','of','a','b')),(step,))
 def test_model_validation(self):
  bad=[(frozenset(),{},{}),(frozenset({'a'}),{'P':frozenset({'b'})},{}),(frozenset({'a'}),{}, {'of':frozenset({('a','b')})})]
  for args in bad:
   with self.assertRaises(Invalid):Model(*args)
 def test_unknown_interpretation(self):
  m=Model(frozenset({'a'}),{'P':frozenset()}, {'of':frozenset()})
  for f in (('member',Q,'a'),('member',P,'b'),('edge','other','a','a')):
   with self.assertRaises(Invalid):m.true(f)
 def test_empty_classes(self):
  m=Model(frozenset({'a'}),{'P':frozenset()},{'of':frozenset()})
  self.assertTrue(m.true(('subset',P,EP)))
  self.assertFalse(m.true(('member',EP,'a')))
if __name__=='__main__':unittest.main()
