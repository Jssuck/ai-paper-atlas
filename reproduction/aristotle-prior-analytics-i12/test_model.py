import unittest
from model import *

class ModelTests(unittest.TestCase):
    def test_total_models(self):
        self.assertEqual(len(set(models())),4096)
    def test_nonempty_subset(self):
        self.assertEqual(sum(all(z for w in m for z in w) for m in models()),729)
    def test_all_reference_values(self):
        count=0
        for m in models():
            for tag,kind,(s,p) in product(TAGS,('A','E','I','O'),(('B','A'),('C','B'),('C','A'))):
                self.assertEqual(modal(m,tag,kind,s,p),reference(m,tag,kind,s,p))
                count+=1
        self.assertEqual(count,196608)
    def test_empty_subject(self):
        self.assertTrue(categorical((0,0,0),'A','B','A'))
        self.assertTrue(categorical((0,0,0),'E','B','A'))
        self.assertFalse(categorical((0,0,0),'I','B','A'))
        self.assertFalse(categorical((0,0,0),'O','B','A'))
    def test_mixed(self):
        m=((1,1,1),(1,1,2))
        self.assertTrue(modal(m,'N','A','B','A'))
        self.assertTrue(modal(m,'D','A','C','B'))
        self.assertTrue(modal(m,'D','A','C','A'))
        self.assertFalse(modal(m,'N','A','C','A'))
    def test_incompatible(self):
        m=((1,1,2),(1,2,2))
        for t in ('P','C'):
            self.assertTrue(modal(m,t,'A','B','A'))
            self.assertTrue(modal(m,t,'A','C','B'))
        for t in ('D','N','P'):
            self.assertFalse(modal(m,t,'A','C','A'))
    def test_weakening(self):
        for m in models():
            for kind in ('A','E','I','O'):
                if modal(m,'N',kind,'C','A'):
                    self.assertTrue(modal(m,'D',kind,'C','A'))
                    self.assertTrue(modal(m,'P',kind,'C','A'))
    def test_contingency(self):
        for m in models():
            self.assertEqual(modal(m,'C','A','C','A'),modal(m,'P','A','C','A') and not modal(m,'N','A','C','A'))
    def test_world_order(self):
        m=((1,1,1),(1,1,2)); rev=m[::-1]
        self.assertNotEqual(modal(m,'D','A','C','A'),modal(rev,'D','A','C','A'))
        for tag in ('N','P','C'):
            self.assertEqual(modal(m,tag,'A','C','A'),modal(rev,tag,'A','C','A'))
    def test_invalid_models(self):
        for m in (None,[],(),((),),((0,0),),((0,0,4),),((0,0,-1),),((0,0,True),),((0,0,1.0),),([0,0,1],)):
            with self.subTest(m=m),self.assertRaises(ValueError): validate(m)
    def test_invalid_domain(self):
        for n in (0,-1,True,1.5,'2',None):
            with self.subTest(n=n),self.assertRaises(ValueError):validate(((0,0,0),),n)
    def test_invalid_tags(self):
        for tag in ('',None,1,True,[],{},'necessary'):
            with self.subTest(tag=tag),self.assertRaises(ValueError):modal(((1,1,1),),tag,'A','B','A')
    def test_invalid_categories(self):
        for kind in ('',None,1,True,[],{},'a'):
            with self.subTest(kind=kind),self.assertRaises(ValueError):categorical((1,1,1),kind,'B','A')
    def test_invalid_terms(self):
        for term in ('',None,1,True,[],{},'D'):
            for s,p in ((term,'A'),('B',term)):
                with self.subTest(s=s,p=p),self.assertRaises(ValueError):categorical((1,1,1),'A',s,p)
    def test_one_world(self):
        m=((1,1,1),)
        self.assertTrue(modal(m,'N','A','B','A'))
        self.assertFalse(modal(m,'C','A','B','A'))
    def test_report(self):
        r=report(); self.assertEqual(len(r['rows']),192)
        rows={(v['mood'],v['major'],v['minor'],v['conclusion']):v for v in r['rows']}
        for mood in MOODS:
            for key in (('D','D','D'),('N','N','N'),('N','N','D'),('N','D','D'),('D','N','D')):
                self.assertEqual(rows[(mood,)+key]['countermodels'],0)
                self.assertGreater(rows[(mood,)+key]['satisfying'],0)
        for tags in (('P','P','P'),('C','C','D'),('C','C','N')):
            self.assertGreater(rows[('Barbara',)+tags]['nonempty_countermodels'],0)
if __name__ == '__main__':unittest.main(verbosity=2)
