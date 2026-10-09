"""Independent finite oracles, source examples and deliberate negative controls."""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import product
import unittest
import demorgan as d


class LogicTests(unittest.TestCase):
    def test_eight_propositions_direct_quantifiers(self):
        count = 0
        for n in range(6):
            u = frozenset(range(n))
            for x, y in product(d.subsets(u), repeat=2):
                expected = {'A': all(t not in x or t in y for t in u),
                            'a': all(t not in y or t in x for t in u),
                            'E': all(not (t in x and t in y) for t in u),
                            'e': all(t in x or t in y for t in u),
                            'I': any(t in x and t in y for t in u),
                            'i': any(t not in x and t not in y for t in u),
                            'O': any(t in x and t not in y for t in u),
                            'o': any(t in y and t not in x for t in u)}
                self.assertEqual(d.propositions(u, x, y), expected)
                for a, b in [('A','O'), ('a','o'), ('E','I'), ('e','i')]:
                    self.assertNotEqual(expected[a], expected[b])
                count += 1
        self.assertEqual(count, 1365)

    def test_twenty_four_forms_reduce_to_eight_triples(self):
        forms = defaultdict(list)
        canonical = defaultdict(list)
        count = 0
        for n in range(5):
            u = frozenset(range(n))
            for x, y in product(d.subsets(u), repeat=2):
                for i, (p, q) in enumerate(((x,y), (x,u-y), (u-x,y), (u-x,u-y))):
                    for j, truth in enumerate((p <= q, q <= p, not(p&q), bool(p&q), bool(p-q), bool(q-p))):
                        forms[i,j].append(bool(truth))
                for label, truth in d.propositions(u,x,y).items():
                    canonical[label].append(truth)
                count += 1
        signatures = {tuple(v): k for k,v in canonical.items()}
        self.assertEqual(len(signatures), 8)
        groups = Counter(signatures[tuple(v)] for v in forms.values())
        self.assertEqual(groups, Counter({k: 3 for k in d.PROPOSITIONS}))
        self.assertEqual(count, 341)

    def test_import_and_seven_way_classification(self):
        count = 0
        found = set()
        for n in range(2,6):
            u = frozenset(range(n))
            proper = [s for s in d.subsets(u) if s and s != u]
            for x, y in product(proper, repeat=2):
                p = d.propositions(u,x,y)
                if p['A'] or p['a']:
                    self.assertTrue(p['I'] and p['i'])
                if p['E'] or p['e']:
                    self.assertTrue(p['O'] and p['o'])
                matches = d.relation_matches(u,x,y)
                self.assertEqual(sum(matches.values()), 1)
                found.add(d.relation(u,x,y))
                count += 1
        self.assertEqual(count, 1136)
        self.assertEqual(found, set(d.RELATIONS))
        # Boundary controls: the existence assumption does real work.
        p = d.propositions({0}, set(), {0})
        self.assertTrue(p['A']); self.assertFalse(p['I'])
        self.assertGreater(sum(d.relation_matches({0}, set(), set()).values()), 1)
        with self.assertRaises(ValueError): d.relation({0}, set(), {0})
        with self.assertRaises(ValueError): d.propositions({0}, {1}, set())

    def test_addition_all_36_printed_cells_and_P_cases(self):
        # Parentheses in p.408 deny these relations; they are not positive lists.
        all_rel = set(d.RELATIONS)
        rows = [
            [('not','C','C_super'), 'D_sub','D_sub','C_sub','C_sub',('not','D','D_super')],
            ['D_super','D','D_sub','C_sub','C','C_super'],
            ['D_super','D_super',('not','C_sub','C'),('not','D_sub','D'),'C_super','C_super'],
            ['C_sub','C_sub',('not','D','D_super'),('not','C','C_super'),'D_sub','D_sub'],
            ['C_sub','C','C_super','D_super','D','D_sub'],
            [('not','D_sub','D'),'C_super','C_super','D_super','D_super',('not','C_sub','C')],
        ]
        computed, count = d.composition_from_atoms()
        self.assertEqual(count,193)
        for i, r in enumerate(d.RELATIONS[:6]):
            for j, s in enumerate(d.RELATIONS[:6]):
                entry = rows[i][j]
                expected = all_rel - set(entry[1:]) if isinstance(entry,tuple) else {entry}
                self.assertEqual(computed[r,s], expected, (r,s))
        for r in d.RELATIONS:
            for pair in [('P',r),(r,'P')]:
                if r in ('D','C'): self.assertEqual(computed[pair], {'P'})
                else: self.assertGreater(len(computed[pair]),1)
        # Separately enumerate every labelled proper-term triple through n=5.
        by_label = {(r,s):set() for r,s in product(d.RELATIONS,repeat=2)}
        total=0
        for n in range(2,6):
            u=frozenset(range(n)); proper=[t for t in d.subsets(u) if t and t != u]
            for x,y,z in product(proper,repeat=3):
                by_label[d.relation(u,x,y),d.relation(u,z,y)].add(d.relation(u,x,z)); total+=1
        self.assertEqual(total,29968)
        self.assertEqual(by_label,computed)

    def test_syllogism_census_and_weakening_scope(self):
        c=d.syllogism_census()
        self.assertEqual((c['premise_pairs'],c['concluding_pairs']),(64,32))
        self.assertEqual((c['minimal_directed'],c['counterpart_classes']),(24,12))
        self.assertEqual(c['redundant_pairs'],['AA','Ae','EE','Ea','aE','aa','eA','ee'])
        # Historical count retains AA and ee: 26 directed / 14 counterpart classes.
        # Modern blanket proper-term import permits these additional weakenings.
        self.assertEqual(c['strongest']['AA'], c['strongest']['Ai'])
        self.assertEqual(c['strongest']['ee'], c['strongest']['Oe'])

    def test_overlap_bound_and_every_tight_count(self):
        count=0; minima={}
        for n in range(1,8):
            u=frozenset(range(n))
            for x,y in product(d.subsets(u),repeat=2):
                bound=d.overlap_lower_bound(F(len(x),n),F(len(y),n))
                self.assertGreaterEqual(F(len(x&y),n),bound)
                key=(n,len(x),len(y)); minima[key]=min(minima.get(key,n),len(x&y)); count+=1
        self.assertEqual(count,21844)
        self.assertEqual(len(minima),203)
        for (n,a,b),minimum in minima.items():
            self.assertEqual(minimum,d.count_overlap_lower_bound(n,a,b))
        self.assertEqual(d.count_overlap_lower_bound(100,50,60),10)
        # p.406's concrete configuration, with the full 80 Ys and 20 Zs specified.
        y=set(range(100)); x=set(range(50)); mentioned_y=set(range(80))
        excluded_y=set(range(40,100)); z=set(range(20))
        self.assertTrue(x <= mentioned_y <= y); self.assertFalse(z & excluded_y)
        self.assertEqual(len(x & excluded_y),10); self.assertTrue((x & excluded_y).isdisjoint(z))


class ProbabilityTests(unittest.TestCase):
    def test_fixed_subset_model_exhaustive(self):
        comparisons=0; pairs=0
        for n in range(7):
            tally=Counter(); totals=Counter()
            for x,y in product(d.subsets(range(n)),repeat=2):
                key=(len(x),len(y)); totals[key]+=1; tally[key]+=not bool(x&y); pairs+=1
            for (a,b),total in totals.items():
                self.assertEqual(F(tally[a,b],total),d.random_subset_disjoint(n,a,b)); comparisons+=1
        self.assertEqual((comparisons,pairs),(140,5461))
        p0=d.random_subset_disjoint(1000,100,100)
        self.assertLess(p0,F(1,60000)); self.assertGreater(p0,F(1,80000))
        self.assertEqual(d.interval_overlap_cdf(F(1,10),F(1,10)),F(64,81))

    def test_interval_model_against_independent_position_grid(self):
        # Midpoint quadrature of the placement rectangle; NOT an exact random draw.
        grid=400
        cases=[(F(1,10),F(1,10),F(0)),(F(1,5),F(3,10),F(0)),
               (F(1,5),F(3,10),F(1,10)),(F(3,5),F(7,10),F(1,5)),
               (F(3,5),F(7,10),F(2,5))]
        for a,b,t in cases:
            af,bf,tf=map(float,(a,b,t)); accepted=0
            for i in range(grid):
                l=(i+0.5)/grid*(1-af)
                for j in range(grid):
                    r=(j+0.5)/grid*(1-bf)
                    overlap=max(0,min(l+af,r+bf)-max(l,r))
                    accepted += overlap <= tf
            self.assertAlmostEqual(accepted/grid**2,float(d.interval_overlap_cdf(a,b,t)),delta=0.005)
        self.assertEqual(d.interval_overlap_cdf(F(1,5),F(3,10),F(1,5)),1)

    def test_authorities_against_conditioning(self):
        grid=[F(i,8) for i in range(9)]; checked=0; impossible=0
        for ps in product(grid,repeat=3):
            if 0 in ps and 1 in ps:
                with self.assertRaises(ValueError): d.joint_testimony(ps)
                impossible+=1; continue
            law=d.conditional_product([d.bernoulli(p) for p in ps],lambda s: len(set(s))==1)
            self.assertEqual(law[True,True,True],d.joint_testimony(ps)); checked+=1
        self.assertEqual((checked,impossible),(681,48))
        self.assertEqual(d.joint_testimony([F(3,4),F(4,5)]),F(12,13))
        self.assertEqual(d.joint_testimony([]),F(1,2))

    def test_p396_mixture_and_printed_mismatch(self):
        mu,mp,lam=F(3,4),F(4,5),F(1,3)
        mixed=d.biased_testimony(mu,mp,lam)
        self.assertEqual(mixed,F(45,52))
        self.assertEqual(d.authority(mixed),F(19,26))
        self.assertEqual(d.printed_biased_authority(mu,mp,lam),F(9,13))
        a,ap=d.authority(mu),d.authority(mp)
        corrected=(a+ap-lam*ap*(1-a*a))/(1+a*ap)
        self.assertEqual(corrected,d.authority(mixed))
        self.assertNotEqual(corrected,d.printed_biased_authority(mu,mp,lam))
        self.assertEqual(d.biased_testimony(0,1,1),0)

    def test_opposing_arguments_against_conditioning(self):
        grid=[F(i,8) for i in range(9)]; count=0
        for a,b in product(grid,repeat=2):
            if a==b==1:
                with self.assertRaises(ValueError): d.opposing_arguments(a,b)
                continue
            law=d.conditional_product([d.bernoulli(a),d.bernoulli(b)],lambda s: not all(s))
            actual=d.opposing_arguments(a,b)
            self.assertEqual(actual,{'for':law[True,False],'against':law[False,True],
                                     'inconclusive':law[False,False]}); count+=1
        self.assertEqual(count,80)
        self.assertEqual(d.opposing_arguments(F(3,4),F(1,2)),
                         {'for':F(3,5),'against':F(1,5),'inconclusive':F(1,5)})

    def test_p398_combination_against_full_three_bit_model(self):
        grid=[F(i,8) for i in range(9)]; count=0; singular=0
        for a,b,mu in product(grid,repeat=3):
            if (1-b)*mu+(1-a)*(1-mu)==0:
                with self.assertRaises(ValueError): d.conclusion_probability(a,b,mu)
                singular+=1; continue
            law=d.conditional_product([d.bernoulli(a),d.bernoulli(b),d.bernoulli(mu)],
                    lambda s: (not s[0] or s[2]) and (not s[1] or not s[2]))
            self.assertEqual(sum(w for s,w in law.items() if s[2]),d.conclusion_probability(a,b,mu))
            self.assertEqual(d.hypothesis_weights([a,b],[mu,F(1,2)])[0],d.conclusion_probability(a,b,mu))
            count+=1
        self.assertEqual((count,singular),(704,25))
        self.assertEqual(d.conclusion_probability(F(3,4),F(1,2),F(2,3)),F(4,5))

    def test_unknown_authority_p401_closed_forms_against_quadrature(self):
        for prior in ('uniform','beta22'):
            for r in (F(1,10),F(1,4),F(1,2),1,2,4,10):
                expected=d.averaged_authority_quadrature(r,prior)
                self.assertAlmostEqual(d.averaged_authority(r,prior),expected,places=10)
                self.assertAlmostEqual(d.averaged_authority(r,prior)+d.averaged_authority(1/r,prior),1,places=10)
        self.assertAlmostEqual(d.averaged_authority(4),0.7172025061689375)
        self.assertAlmostEqual(d.averaged_authority(4,'beta22'),0.7541266502161664)
        self.assertNotAlmostEqual(d.averaged_authority(4),4/5)  # Averaging is nonlinear.
        # Numerical edges found by independent review; no fixed-grid oracle here.
        for prior in ('uniform','beta22'):
            for r in (1e-300,1.000000000000001,1.01000001,1e78,1e300):
                self.assertTrue(0 <= d.averaged_authority(r,prior) <= 1)
                self.assertAlmostEqual(d.averaged_authority(r,prior)+d.averaged_authority(1/r,prior),1,places=14)
        self.assertAlmostEqual(d.averaged_authority(1.01000001,'beta22'),
                               d.averaged_authority_quadrature(1.01000001,'beta22'),places=13)

    def test_multihorn_and_exactly_k_weights(self):
        aa=[F(1,2),F(1,3),F(1,4)]; mm=[F(2,3),F(3,5),F(4,7)]
        weights=[mm[i]/((1-aa[i])*(1-mm[i])) for i in range(3)]
        self.assertEqual(d.hypothesis_weights(aa,mm),d.normalize(dict(enumerate(weights))))
        exponents=[F(1),F(2),F(3),F(4)]
        law=d.exactly_k(exponents,2)
        self.assertEqual(sum(v for s,v in law.items() if 0 in s),F(9,35))
        # Independent Bernoullis with odds e_i, conditioned on exactly two truths.
        bits=d.conditional_product([d.bernoulli(e/(1+e)) for e in exponents],lambda s: sum(s)==2)
        self.assertEqual(law,{tuple(i for i,b in enumerate(s) if b):v for s,v in bits.items()})
        self.assertEqual(d.exactly_k([],0),{():F(1)})

    def test_original_urn_example_and_removed_black_invariance(self):
        law=d.urn_example()
        self.assertEqual(set(''.join(s) for s in law),{'WWB','WBW','WBB','RBW','RWB'})
        self.assertEqual(sum(v for s,v in law.items() if s[0]=='R'),F(5,14))
        removed=d.urn_example(({'W':F(3,5),'R':F(2,5)},
                              {'W':F(2,3),'B':F(1,3)},{'W':F(3,4),'B':F(1,4)}))
        self.assertEqual(law,removed)

    def test_marginals_do_not_fix_dependence(self):
        # Two strictly positive joint laws, same support AND same marginals 1/2.
        independent={(False,False):F(1,4),(False,True):F(1,4),
                     (True,False):F(1,4),(True,True):F(1,4)}
        correlated={(False,False):F(2,5),(False,True):F(1,10),
                    (True,False):F(1,10),(True,True):F(2,5)}
        for law in (independent,correlated):
            self.assertEqual(sum(law.values()),1)
            for i in range(2): self.assertEqual(sum(p for s,p in law.items() if s[i]),F(1,2))
        self.assertEqual(set(independent),set(correlated))
        self.assertNotEqual(independent[True,True],correlated[True,True])
        self.assertEqual(d.independent_any([F(1,2),F(1,2)]),F(3,4))
        self.assertEqual(sum(p for s,p in correlated.items() if any(s)),F(3,5))
        # Identical Bernoulli(3/4) testimonies add no evidence on agreement;
        # the product-conditioning model with the same base marginals yields 9/10.
        self.assertEqual(d.joint_testimony([F(3,4),F(3,4)]),F(9,10))
        dependent={(False,False):F(1,4),(True,True):F(3,4)}
        self.assertEqual(dependent[True,True],F(3,4))

    def test_invalid_inputs_and_zero_mass(self):
        for p in (-1,F(3,2),0.5):
            with self.assertRaises((ValueError,TypeError)): d.probability(p)
        with self.assertRaises(ValueError): d.normalize({'a':0})
        with self.assertRaises(ValueError): d.normalize({'a':-1,'b':2})
        with self.assertRaises(ValueError): d.conditional_product([{'x':F(1,2)}],lambda s:True)
        with self.assertRaises(ValueError): d.conditional_product([d.bernoulli(1)],lambda s:False)
        with self.assertRaises(ValueError): d.count_overlap_lower_bound(5,6,0)
        with self.assertRaises(ValueError): d.hypothesis_weights([1],[0])
        with self.assertRaises(ValueError): d.exactly_k([1],2)
        with self.assertRaises(ValueError): d.interval_overlap_cdf(1,F(1,2))
        with self.assertRaises(ValueError): d.averaged_authority_quadrature(2,panels=3)
        self.assertEqual(d.conditional_product([],lambda s:True),{():F(1)})


if __name__=='__main__': unittest.main()
