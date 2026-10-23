"""Independent audit: direct object quantifiers, separate layout, witnesses."""
import itertools
import json
import unittest
import model as author


def truth(q, x, y, domain):
    if q == 'A': return all(t not in x or t in y for t in domain)
    if q == 'E': return all(not(t in x and t in y) for t in domain)
    if q == 'I': return any(t in x and t in y for t in domain)
    if q == 'O': return any(t in x and t not in y for t in domain)
    raise ValueError(q)


def layout(f, s, m, p):
    if f == 1: return ((m,p),(s,m))
    if f == 2: return ((p,m),(s,m))
    if f == 3: return ((m,p),(m,s))
    raise ValueError(f)


def values(f, mood, s, m, p, domain):
    a,b=layout(f,s,m,p)
    return truth(mood[0],*a,domain),truth(mood[1],*b,domain),truth(mood[2],s,p,domain)


def supports():
    types=list(itertools.product((False,True),repeat=3))[1:]
    for occupied in itertools.product((False,True),repeat=7):
        rows=[t for t,on in zip(types,occupied) if on] or [(False,False,False)]
        d=set(range(len(rows)))
        yield d,*[{i for i,row in enumerate(rows) if row[j]} for j in range(3)]


def subsets(d):
    return [{i for i in d if mask & (1<<i)} for mask in range(1<<len(d))]


class Independent(unittest.TestCase):
    def test_all_moods_and_witnesses(self):
        counts=[]; evaluated=0
        for policy in (False,True):
            valid={f:[] for f in (1,2,3)}
            models=[r for r in supports() if not policy or all(r[1:])]
            counts.append(len(models))
            for f in (1,2,3):
                for qs in itertools.product('AEIO',repeat=3):
                    mood=''.join(qs); bad=False
                    for d,s,m,p in models:
                        a,b,c=values(f,mood,s,m,p,d)
                        evaluated+=1
                        bad = bad or (a and b and not c)
                    witness=author.countermodel(f,mood,policy)
                    self.assertEqual(witness is not None,bad,(f,mood,policy))
                    if witness is not None:
                        self.assertEqual(values(f,mood,witness.s,witness.m,witness.p,witness.domain),(True,True,False))
                        if policy:self.assertTrue(witness.s and witness.m and witness.p)
                    else:valid[f].append(mood)
            self.assertEqual(valid,author.valid_moods(policy))
            expected={'A':(1,),'E':(1,2),'I':(1,3),'O':(1,2,3)}
            self.assertEqual({q:tuple(f for f in valid if any(x[-1]==q for x in valid[f])) for q in 'AEIO'},expected)
        self.assertEqual(counts,[128,109]);self.assertEqual(evaluated,45504)
        print(json.dumps({'independent_model_mood_checks':evaluated,'canonical_counts':counts}))

    def test_compression_four_objects(self):
        d=set(range(4)); n=0
        for s,m,p in itertools.product(subsets(d),repeat=3):
            patterns={(x in s,x in m,x in p) for x in d}-{(False,False,False)}
            rows=list(patterns) or [(False,False,False)]
            small=set(range(len(rows)))
            terms=[{i for i,row in enumerate(rows) if row[j]} for j in range(3)]
            for x,y in itertools.product(range(3),repeat=2):
                for q in 'AEIO':
                    self.assertEqual(truth(q,(s,m,p)[x],(s,m,p)[y],d),truth(q,terms[x],terms[y],small))
            self.assertEqual([bool(x) for x in (s,m,p)],[bool(x) for x in terms]);n+=1
        self.assertEqual(n,4096)
        print(json.dumps({'compression_assignments':n,'categorical_truth_comparisons':n*36}))

    def test_arbitrary_labels_and_duplicate_types(self):
        x=author.Model({10,20,30},{10,20},{10,20,30},{30})
        for f in (1,2,3):
            for qs in itertools.product('AEIO',repeat=3):
                q=''.join(qs)
                self.assertEqual(author.evaluate(x,f,q),values(f,q,x.s,x.m,x.p,x.domain))

    def test_mixed_and_converted_steps(self):
        self.assertEqual(author.classify_step(('A','M','P'),('A','S','M'),('A','S','P')),1)
        self.assertEqual(author.classify_step(('E','Q','P'),('A','S','P'),('E','S','Q')),2)
        self.assertEqual(author.classify_step(('E','P','Q'),('A','S','P'),('E','S','Q')),1)
        d=set(range(3)); count=good=0
        for s,m,p,q in itertools.product(subsets(d),repeat=4):
            count+=1
            if truth('A',s,m,d) and truth('A',m,p,d) and truth('E',q,p,d):
                good+=1
                self.assertTrue(truth('A',s,p,d));self.assertTrue(truth('E',s,q,d))
        self.assertEqual((count,good),(4096,125))

    def test_classification_is_not_validity(self):
        step=(('E','M','P'),('E','S','M'),('E','S','P'))
        self.assertEqual(author.classify_step(*step),1)
        x=author.Model({0,1},{1},{0},{1})
        self.assertEqual(author.evaluate(x,1,'EEE'),(True,True,False))

    def test_empty_middle_and_policy(self):
        x=author.Model({0,1},{0},set(),{1})
        self.assertEqual(author.evaluate(x,3,'AAI'),(True,True,False))
        self.assertIsNotNone(author.countermodel(3,'AAI',False))
        self.assertIsNone(author.countermodel(3,'AAI',True))

    def test_validation(self):
        for f in (True,False,1.0,'1',0,4):
            with self.assertRaises(ValueError):author.countermodel(f,'AAA')
        for q in ('AAX','',None,3,('A','A','A')):
            with self.assertRaises(ValueError):author.countermodel(1,q)
        for p in (0,1,None,'false'):
            with self.assertRaises(ValueError):author.countermodel(1,'AAA',p)
        for d,s,m,p in [(set(),set(),set(),set()),({0},{1},set(),set()),({False},set(),set(),set()),({-1},set(),set(),set())]:
            with self.assertRaises(ValueError):author.Model(d,s,m,p)
        for step in [(('A','M','P'),('A','S','M'),('A','S','S')), (('A','','P'),('A','S',''),('A','S','P'))]:
            with self.assertRaises(ValueError):author.classify_step(*step)

    def test_single_use_inputs(self):
        x=author.Model(iter([0,1]),iter([0]),iter([0,1]),iter([1]))
        self.assertEqual((x.s,x.m,x.p),(frozenset({0}),frozenset({0,1}),frozenset({1})))

if __name__=='__main__':unittest.main(verbosity=2)
