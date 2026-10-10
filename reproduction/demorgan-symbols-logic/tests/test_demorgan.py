"""Finite enumeration, exact independent oracles, and negative controls."""
from fractions import Fraction as F
from itertools import product
import unittest
import demorgan as d


def subsets(n):
    return tuple(frozenset(i for i in range(n) if m & (1 << i)) for m in range(1 << n))


def quantifier_oracle(symbol, u, x, y):
    return {
        '))': all(a not in x or a in y for a in u),
        '((': all(a not in y or a in x for a in u),
        ').(': all(a not in x or a not in y for a in u),
        '(.)': all(a in x or a in y for a in u),
        '()': any(a in x and a in y for a in u),
        ')(': any(a not in x and a not in y for a in u),
        '(.(': any(a in x and a not in y for a in u),
        ').)': any(a not in x and a in y for a in u),
    }[symbol]


class SymbolTests(unittest.TestCase):
    def test_all_forms_transformations_and_contradictions(self):
        count = 0
        for n in range(6):
            u = frozenset(range(n))
            for x, y in product(subsets(n), repeat=2):
                count += 1
                for p in d.FORMS:
                    v = p.holds(u, x, y)
                    self.assertEqual(v, quantifier_oracle(str(p), u, x, y))
                    self.assertNotEqual(v, p.contradictory().holds(u, x, y))
                    self.assertEqual(v, p.contrary_term('left').holds(u, u-x, y))
                    self.assertEqual(v, p.contrary_term('right').holds(u, x, u-y))
        self.assertEqual(count, 1365)

    def test_canon_32_and_24_without_strengthening(self):
        models = tuple(d.atom_models())
        self.assertEqual(len(models), 193)
        counts = {'universal': 0, 'particular': 0, 'strengthened': 0}
        for p, q in product(d.FORMS, repeat=2):
            conclusion = d.symbolic_inference(p, q)
            compatible = [(u,x,y,z) for u,x,y,z in models if p.holds(u,x,y) and q.holds(u,y,z)]
            self.assertTrue(compatible)
            semantic = [r for r in d.FORMS if all(r.holds(u,x,z) for u,x,y,z in compatible)]
            if conclusion is None:
                self.assertFalse(semantic)
            else:
                self.assertIn(conclusion, semantic)
                kind = ('universal' if conclusion.universal else
                        'strengthened' if p.universal and q.universal else 'particular')
                counts[kind] += 1
        self.assertEqual(counts, {'universal': 8, 'particular': 16, 'strengthened': 8})
        all_models = tuple(d.atom_models(proper=False))
        valid = 0
        for p,q in product(d.FORMS, repeat=2):
            r = d.symbolic_inference(p,q)
            if r is not None and all(not(p.holds(u,x,y) and q.holds(u,y,z)) or r.holds(u,x,z)
                                     for u,x,y,z in all_models):
                valid += 1
        self.assertEqual(valid, 24)

    def test_exemplar_36_and_21_common_schemas(self):
        # Multiplicity 0,1,2 per membership atom distinguishes singleton identity
        # from mere set equality. One occupant per atom would miss this boundary.
        models=[]
        for multiplicities in product(range(3),repeat=8):
            objects=[(atom,j) for atom,c in enumerate(multiplicities) for j in range(c)]
            terms=tuple(frozenset(o for o in objects if o[0] & (1<<bit)) for bit in range(3))
            if all(terms): models.append(terms)
        truths=[]
        for x,y,z in models:
            truths.append(tuple(tuple(d.exemplar_holds(p,a,b) for p in d.FORMS)
                                for a,b in ((x,y),(y,z),(x,z))))
        licensed=common=0
        for i,p in enumerate(d.FORMS):
            for j,q in enumerate(d.FORMS):
                r=d.exemplar_inference(p,q)
                compatible=[t for t in truths if t[0][i] and t[1][j]]
                self.assertTrue(compatible)
                semantic=[k for k in range(8) if all(t[2][k] for t in compatible)]
                if r is None:
                    self.assertFalse(semantic)
                else:
                    licensed+=1
                    self.assertIn(d.FORMS.index(r),semantic)
                    common+=d.symbolic_inference(p,q)==r
        self.assertEqual((licensed,common),(36,21))
        self.assertEqual(len(models),6342)
        # Equality of plural sets is weaker than identity of any selected pair.
        p=d.Proposition.parse(')(')
        self.assertFalse(d.exemplar_holds(p,{0,1},{0,1}))
        self.assertTrue(d.exemplar_holds(p,{0},{0}))

    def test_existential_negative_control(self):
        u, x, y, z = {0}, {0}, set(), {0}
        p,q = d.Proposition.parse('(('), d.Proposition.parse('))')
        self.assertTrue(p.holds(u,x,y) and q.holds(u,y,z))
        # Choose disjoint outer terms: the same universal premises can hold vacuously.
        z = set()
        self.assertTrue(p.holds(u,x,y) and q.holds(u,y,z))
        self.assertFalse(d.symbolic_inference(p,q).holds(u,x,z))

    def test_p95_printed_conclusion_regression(self):
        # Source-image audit: lower right last cell prints ))(.)=(.(.
        # The p.94 canon and repeated upper block instead yield ).).
        u,x,y,z={1,2,3},{1},{1,2},{1,3}
        first,second=d.Proposition.parse('))'),d.Proposition.parse('(.)')
        printed=d.Proposition.parse('(.(')
        corrected=d.symbolic_inference(first,second)
        self.assertTrue(first.holds(u,x,y) and second.holds(u,y,z))
        self.assertFalse(printed.holds(u,x,z))
        self.assertEqual(str(corrected),').)')
        self.assertTrue(corrected.holds(u,x,z))

    def test_syntax_and_validation(self):
        self.assertEqual(d.Proposition.parse(')....)'), d.Proposition.parse('))'))
        self.assertEqual(d.Proposition.parse('(.....('), d.Proposition.parse('(.('))
        for bad in ['', '(', 'abc', ')x(', ' ) )']:
            with self.assertRaises(ValueError): d.Proposition.parse(bad)
        with self.assertRaises(ValueError): d.FORMS[0].holds({0},{1},set())
        with self.assertRaises(ValueError): d.FORMS[0].contrary_term('middle')


class RelationTests(unittest.TestCase):
    def test_composition_oracle_and_negative_opponents(self):
        u = range(2)
        edges = tuple(product(u, repeat=2))
        relations = [frozenset(e for i,e in enumerate(edges) if mask & (1<<i)) for mask in range(16)]
        for r,s in product(relations, repeat=2):
            t = d.compose(r,s)
            oracle = frozenset((x,z) for x,z in edges if any((x,y) in r and (y,z) in s for y in u))
            self.assertEqual(t, oracle)
            self.assertEqual(d.converse(t),d.compose(d.converse(s),d.converse(r)))
            for x,y,z in product(u, repeat=3):
                if (x,z) not in t and (y,z) in s: self.assertNotIn((x,y),r)
                if (x,z) not in t and (x,y) in r: self.assertNotIn((y,z),s)
        for r,s,t in product(relations, repeat=3):
            self.assertEqual(d.compose(d.compose(r,s),t),d.compose(r,d.compose(s,t)))

    def test_transitivity_and_converse_512_relations(self):
        u = range(3)
        edges = tuple(product(u,repeat=2))
        for mask in range(512):
            r = frozenset(e for i,e in enumerate(edges) if mask & (1<<i))
            oracle = all((x,y) not in r or (y,z) not in r or (x,z) in r for x,y,z in product(u,repeat=3))
            self.assertEqual(d.transitive(r),oracle)
            self.assertEqual(d.transitive(r),d.transitive(d.converse(r)))
        persuasion = {('John','Thomas')}
        command = {('Thomas','William')}
        self.assertIn(('John','William'),d.compose(persuasion,command))
        self.assertNotIn(('John','William'),persuasion|command)

    def test_exemplar_is_not_bilateral_coverage(self):
        x,y = {0,1},{2,3}
        r = {(0,2),(1,3)}
        self.assertTrue(d.all_some(r,x,y) and d.all_some(d.converse(r),y,x))
        self.assertFalse(d.all_all(r,x,y))
        complete = set(product(x,y))
        self.assertTrue(d.all_all(complete,x,y))
        self.assertEqual(len(complete),4)
        # Modern empty-domain convention is explicitly vacuous.
        self.assertTrue(d.all_all(set(),set(),y))

    def test_relational_complex_term_monotonicity(self):
        edges = tuple(product(range(2),repeat=2))
        for mask in range(16):
            r = frozenset(e for i,e in enumerate(edges) if mask & (1<<i))
            for x,y in product(subsets(2),repeat=2):
                if x <= y: self.assertLessEqual(d.relational_term(r,x),d.relational_term(r,y))

    def test_common_target_bound_exhaustive(self):
        checked = 0
        for a,b in product(range(1,4),repeat=2):
            edges = tuple(product(range(a),range(b)))
            best = {}
            for mask in range(1 << (a*b)):
                r = frozenset(e for i,e in enumerate(edges) if mask & (1<<i))
                common = sum(all((x,y) in r for x in range(a)) for y in range(b))
                bound = d.common_target_lower_bound(a,b,len(r))
                self.assertGreaterEqual(common,bound)
                best[len(r)] = min(best.get(len(r), b+1),common)
                checked += 1
            for e, minimum in best.items():
                self.assertEqual(minimum,d.common_target_lower_bound(a,b,e))
        self.assertEqual(checked,682)

    def test_arbitrary_relations_do_not_inherit_contraries(self):
        # p.114–116 impose totality and non-mixing assumptions. An arbitrary
        # relation may simultaneously connect one x to y and to its contrary.
        r = {(0,1),(0,2)}
        self.assertTrue(d.all_some(r,{0},{1}))
        self.assertTrue(d.all_some(r,{0},{2}))


class ProbabilityTests(unittest.TestCase):
    def test_binary_grid_independent_joint_mass_oracle(self):
        values = [F(i,4) for i in range(5)]
        defined = rejected = 0
        for v,a,b,k in product(values,values,values,range(2)):
            prior = (v,1-v)
            rows = ((a,1-a),(1-b,b))
            joint = {(event,report): prior[event]*rows[event][report] for event,report in product(range(2),repeat=2)}
            mass = sum(prob for (event,report),prob in joint.items() if report==k)
            if mass:
                expected = tuple(joint[event,k]/mass for event in range(2))
                self.assertEqual(d.posterior(prior,rows,k),expected)
                self.assertEqual(d.denial_posterior(prior,rows,1-k),expected)
                defined += 1
            else:
                with self.assertRaises(ValueError): d.posterior(prior,rows,k)
                rejected += 1
        self.assertEqual((defined,rejected),(224,26))

    def test_uniform_error_formula_and_stationarity(self):
        for n in range(2,8):
            for a in [F(0),F(1,4),F(1,2),F(9,10),F(1)]:
                c=d.symmetric_channel(n,a)
                prior=(F(1,n),)*n
                self.assertEqual(d.report_distribution(prior,c),prior)
                self.assertEqual(d.general_credibility(prior,c),a)
                for k in range(n):
                    self.assertEqual(d.posterior(prior,c,k)[k],a)
                for v in (F(1,100),F(1,n),F(3,4)):
                    p=(v,)+((1-v)/(n-1),)*(n-1)
                    self.assertEqual(d.posterior(p,c,0)[0],d.symmetric_credibility(v,n,a))

    def test_card_vs_binary_and_correct_aggregation(self):
        n,a=52,F(9,10)
        prior=(F(1,n),)*n
        c=d.symmetric_channel(n,a)
        self.assertEqual(d.posterior(prior,c,0)[0],a)
        groups=((0,),tuple(range(1,n)))
        p,cg=d.aggregate_model(prior,c,groups,groups)
        self.assertEqual(d.posterior(p,cg,0)[0],a)
        self.assertEqual(cg[1][0],F(1,510))
        self.assertEqual(d.posterior(p,d.symmetric_channel(2,a),0)[0],F(3,20))

    def test_bias_no_information_and_theta_family(self):
        prior=(F(1,10),F(3,10),F(6,10))
        beliefs=(F(1,5),F(3,10),F(1,2))
        c=d.biased_channel(beliefs,beliefs)
        self.assertEqual(c,(beliefs,)*3)
        for k in range(3): self.assertEqual(d.posterior(prior,c,k),prior)
        for theta in [F(0),F(1,4),F(1,2),F(1),F(6,5)]:
            accuracy=tuple(1-theta*(1-l) for l in beliefs)
            c=d.biased_channel(beliefs,accuracy)
            for k in range(3):
                formula=prior[k]*(theta*beliefs[k]+1-theta)/((1-theta)*prior[k]+theta*beliefs[k])
                self.assertEqual(d.posterior(prior,c,k)[k],formula)

    def test_two_stage_full_latent_enumeration(self):
        prior=(F(1,6),F(1,3),F(1,2))
        judgment=((F(1,2),F(1,4),F(1,4)),(F(1,3),F(2,3),F(0)),(F(1,5),F(1,5),F(3,5)))
        statement=d.biased_channel((F(1,5),F(3,10),F(1,2)),(F(3,4),F(4,5),F(2,3)))
        composed=d.compose_channels(judgment,statement)
        for k in range(3):
            masses=[sum(prior[t]*judgment[t][b]*statement[b][k] for b in range(3)) for t in range(3)]
            self.assertEqual(d.posterior(prior,composed,k),tuple(v/sum(masses) for v in masses))

    def test_laplace_closed_form_all_parameters(self):
        checked=0
        for n,p,r in product(range(2,7),[F(i,4) for i in range(5)],[F(i,4) for i in range(5)]):
            c=d.compose_channels(d.symmetric_channel(n,p),d.symmetric_channel(n,r))
            prior=(F(1,n),)*n
            for k in range(n):
                self.assertEqual(d.posterior(prior,c,k)[k],p*r+(1-p)*(1-r)/(n-1))
                checked+=1
        self.assertEqual(checked,500)

    def test_targeted_falsehood(self):
        v=F(1,52)
        prior=(v,1-v)
        for bias in [F(i,4) for i in range(5)]:
            c=d.targeted_statement_channel(2,0,bias)
            self.assertEqual(d.posterior(prior,c,0)[0],v/((1-bias)*v+bias))

    def test_independent_witnesses_latent_oracle_and_copying(self):
        prior=(F(1,3),F(2,3))
        j=d.symmetric_channel(2,F(3,4))
        s=d.symmetric_channel(2,F(4,5))
        c=d.compose_channels(j,s)
        for observed in product(range(2),repeat=3):
            masses=[sum(prior[t]*j[t][a]*s[a][observed[0]]*j[t][b]*s[b][observed[1]]*
                        j[t][e]*s[e][observed[2]] for a,b,e in product(range(2),repeat=3)) for t in range(2)]
            self.assertEqual(d.multiple_witnesses(prior,(c,)*3,observed),tuple(v/sum(masses) for v in masses))
        fair=(F(1,2),)*2
        accurate=d.symmetric_channel(2,F(9,10))
        self.assertEqual(d.multiple_witnesses(fair,(accurate,)*2,(0,0))[0],F(81,82))
        self.assertEqual(d.condition(fair,(F(9,10),F(1,10)))[0],F(9,10)) # perfect copy
        self.assertEqual(d.multiple_witnesses(prior,(),()),prior)

    def test_probability_validation(self):
        for bad in [(),(F(1,4),F(1,4)),(F(-1),F(2)),(0.5,0.5)]:
            with self.assertRaises((ValueError,TypeError)): d.distribution(bad)
        for rows in [(),((1,0),(1,)),((1,1),(0,1))]:
            with self.assertRaises(ValueError): d.channel(rows)
        with self.assertRaises(ValueError): d.posterior((1,0),((1,0),(1,0)),1)
        with self.assertRaises(ValueError): d.posterior((1,0),((1,0),(0,1)),-1)
        with self.assertRaises(ValueError): d.biased_channel((1,0),(F(1,2),F(1,2)))
        with self.assertRaises(ValueError): d.compose_channels(((1,0),),((1,),))
        with self.assertRaises(ValueError): d.multiple_witnesses((1,0),(),(0,))
        with self.assertRaises(ValueError): d.aggregate_model((1,0),((1,0),(0,1)),((0,),(1,)),((0,),(1,)))
        with self.assertRaises(ValueError): d.aggregate_model((F(1,2),)*2,((1,0),(0,1)),((0,0),(1,)),((0,),(1,)))


if __name__=='__main__': unittest.main()
