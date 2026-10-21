import unittest
from modal import Model,evaluate,models,premises,witness_route,MOODS,experiment

def reference(m,mode,q,s,p):
    objects=range(m.n)
    def member(w,t,x):return bool(m.worlds[w][t] & (1<<x))
    def plain(w):
        pairs=[(member(w,s,x),member(w,p,x)) for x in objects]
        if q=='A':return all(not a or b for a,b in pairs)
        if q=='E':return all(not a or not b for a,b in pairs)
        if q=='I':return any(a and b for a,b in pairs)
        return any(a and not b for a,b in pairs)
    if mode=='T':return plain(0)
    if mode=='D':return all(plain(w) for w in range(len(m.worlds)))
    target=lambda x:all(member(w,p,x)==(q in 'AI') for w in range(len(m.worlds)))
    if q in 'AE':return all(not member(0,s,x) or target(x) for x in objects)
    return any(member(0,s,x) and target(x) for x in objects)

class Tests(unittest.TestCase):
    def test_reference_exhaustive(self):
        count=0
        for m in models():
            for mode in ('T','N','D'):
                for q in 'AEIO':
                    for s,p in ((1,0),(2,1),(2,0)):
                        self.assertEqual(evaluate(m,mode,q,s,p),reference(m,mode,q,s,p));count+=1
        self.assertEqual(count,147456)
    def test_single_world_collapses(self):
        for m in models(2,1):
            for q in 'AEIO':
                self.assertEqual(evaluate(m,'N',q,2,0),evaluate(m,'T',q,2,0))
                self.assertEqual(evaluate(m,'D',q,2,0),evaluate(m,'T',q,2,0))
    def test_major_theorem_finite(self):
        for m in models():
            for name,(_,_,q) in MOODS.items():
                if premises(m,name,'major'):
                    self.assertTrue(evaluate(m,'N',q,2,0));witness_route(m,name)
    def test_necessity_implies_actual(self):
        for m in models():
            for q in 'AEIO':self.assertFalse(evaluate(m,'N',q,2,0) and not evaluate(m,'T',q,2,0))
    def test_ordinary_conclusion_all(self):
        for m in models():
            for name,(_,_,q) in MOODS.items():
                for place in ('major','minor'):
                    if premises(m,name,place):self.assertTrue(evaluate(m,'T',q,2,0))
    def test_minor_positive_counterexamples(self):
        m=Model(1,((1,1,1),(0,1,1)))
        for name in ('Barbara','Darii'):
            self.assertTrue(premises(m,name,'minor'));self.assertFalse(evaluate(m,'N',MOODS[name][2],2,0))
    def test_minor_negative_counterexamples(self):
        m=Model(1,((0,1,1),(1,1,1)))
        for name in ('Celarent','Ferio'):
            self.assertTrue(premises(m,name,'minor'));self.assertFalse(evaluate(m,'N',MOODS[name][2],2,0))
    def test_de_dicto_major_failure(self):
        for name in MOODS:
            self.assertTrue(any(premises(m,name,'major','D') and not evaluate(m,'D',MOODS[name][2],2,0) for m in models()))
    def test_universal_semantics_incomparable(self):
        for q in 'AE':
            for a,b in (('N','D'),('D','N')):
                self.assertTrue(any(evaluate(m,a,q,2,0) and not evaluate(m,b,q,2,0) for m in models()))
    def test_particular_semantics_incomparable(self):
        for q in 'IO':
            for a,b in (('N','D'),('D','N')):
                self.assertTrue(any(evaluate(m,a,q,2,0) and not evaluate(m,b,q,2,0) for m in models()))
    def test_negation_duality(self):
        for m in models():
            self.assertEqual(not evaluate(m,'N','A',2,0),any(m.worlds[0][2]&~w[0]!=0 for w in m.worlds))
    def test_empty_subject(self):
        m=Model(1,((0,0,0),(1,1,1)))
        for q in 'AE':self.assertTrue(evaluate(m,'N',q,2,0))
        for q in 'IO':self.assertFalse(evaluate(m,'N',q,2,0))
    def test_world_permutation_nonactual(self):
        for masks in ((1,2,3),(3,1,2),(0,3,1)):
            a=Model(2,((3,3,3),masks,(1,1,1)));b=Model(2,(a.worlds[0],a.worlds[2],a.worlds[1]))
            for q in 'AEIO':self.assertEqual(evaluate(a,'N',q,2,0),evaluate(b,'N',q,2,0))
    def test_three_world_witness(self):
        m=Model(2,((1,1,3),(1,0,0),(3,3,1)))
        self.assertEqual(witness_route(m,'Darii'),[0]);self.assertTrue(evaluate(m,'N','I',2,0))
    def test_empty_universal_route(self):self.assertEqual(witness_route(Model(1,((0,0,0),)),'Barbara'),[])
    def test_route_rejects_false(self):
        with self.assertRaises(ValueError):witness_route(Model(1,((0,1,1),)),'Barbara')
    def test_wrong_mood(self):
        with self.assertRaises(ValueError):premises(Model(1,((0,0,0),)),'bad','major')
        with self.assertRaises(ValueError):witness_route(Model(1,((0,0,0),)),'bad')
    def test_wrong_place(self):
        with self.assertRaises(ValueError):premises(Model(1,((0,0,0),)),'Barbara','bad')
    def test_bad_premise_modality(self):
        for place in ('major','minor'):
            with self.assertRaises(ValueError):premises(Model(1,((0,1,1),)),'Barbara',place,'bad')
    def test_bad_model(self):
        for n,w in ((0,((0,0,0),)),(True,((0,0,0),)),(1,()),(1,[]),(1,((0,0),)),(1,((0,-1,0),)),(1,((0,2,0),)),(1,((0,True,0),))):
            with self.assertRaises(ValueError):Model(n,w)
    def test_bad_evaluation(self):
        m=Model(1,((0,0,0),))
        for args in ((m,'bad','A',0,1),(m,'N','X',0,1),(m,'N','A',-1,1),(m,'N','A',0,3),(m,'N','A',True,1),(None,'N','A',0,1)):
            with self.assertRaises(ValueError):evaluate(*args)
    def test_bad_generator(self):
        for a,b in ((0,2),(2,0),(True,2),(2,True)):
            with self.assertRaises(ValueError):next(models(a,b))
    def test_generator_count(self):self.assertEqual(len(list(models())),4096)
    def test_summary(self):
        r=experiment();self.assertEqual(len(r['rows']),16)
        for row in r['rows']:
            self.assertEqual(row['models'],4096);self.assertEqual(row['actual_failures'],0)
            valid=row['semantics']=='N' and row['necessary_position']=='major'
            self.assertEqual(row['necessary_failures']==0,valid)
            self.assertEqual(row['first_countermodel'] is None,valid)

if __name__=='__main__':unittest.main(verbosity=2)
