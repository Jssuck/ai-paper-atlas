"""Unit and small exhaustive checks; assertions remain active under -O/-OO."""
from dataclasses import FrozenInstanceError
from itertools import product, combinations
import unittest
import condillac_model as m
from examples import chips, query_example, selector, causal_toy, causal_run


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.u = m.Universe(('x',), ((0,), (1,)))
        self.t = m.Table(self.u, 'x', (0,1))
        self.p = m.Problem(self.u,self.t)

    def test_worlds_reject_bool_float_and_mutability(self):
        for bad in (True, 1.0, None, [1], (1,)):
            with self.subTest(bad=bad), self.assertRaises(TypeError):
                m.Universe(('x',), ((bad,),))
        with self.assertRaises(TypeError): m.Universe(('x',), [(0,)])
        with self.assertRaises(TypeError): m.Universe(['x'], ((0,),))
        with self.assertRaises(TypeError): m.Universe((), ((),))

    def test_names_dimensions_and_duplicate_worlds(self):
        for fields, worlds in ((('x','x'),((0,1),)), (('x',),((0,),(0,))),
                               (('x',),((0,1),)), (('',),((0,),)), ((1,),((0,),))):
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                m.Universe(fields,worlds)

    def test_tables_are_total_exact_and_immutable(self):
        for values in ((0,), [0,1], (0,True), (0,1.0), (0,[1]), (0,('ok',False))):
            with self.subTest(values=values), self.assertRaises((TypeError,ValueError)):
                m.Table(self.u,'bad',values)
        self.assertEqual(m.Table(self.u,'nested',((1,('a',)),())).values, ((1,('a',)),()))
        with self.assertRaises(FrozenInstanceError): self.t.name='changed'
        with self.assertRaises(ValueError): m.Table(self.u,'  ',(0,1))
        with self.assertRaises(TypeError): m.Table(None,'x',())

    def test_constraint_outputs_must_be_actual_booleans(self):
        for mask in ((0,1), (False,), [False,True], (False,None)):
            with self.subTest(mask=mask), self.assertRaises((TypeError,ValueError)):
                m.Constraint(self.u,'bad',mask)
        with self.assertRaises(TypeError): m.constraint(self.u,'truthy',lambda w:w[0])
        self.assertEqual(m.constraint(self.u,'positive',lambda w:w[0]>0).mask,(False,True))

    def test_problem_requires_same_ordered_universe(self):
        v=m.Universe(('x',),((1,),(0,)))
        with self.assertRaises(ValueError): m.Problem(v,self.t)
        with self.assertRaises(ValueError): m.Problem(self.u,self.t,(m.Constraint(v,'a',(True,True)),))
        with self.assertRaises(TypeError): m.Problem(self.u,self.t,[])
        with self.assertRaises(TypeError): m.Problem(self.u,self.t,(self.t,))
        with self.assertRaises(TypeError): m.analyze(None)
        with self.assertRaises(TypeError): m.add_evidence(self.p,self.t)

    def test_materialization_samples_once(self):
        calls=[]
        t=m.table(self.u,'sample',lambda w:(calls.append(w),w[0])[1])
        self.assertEqual(calls,list(self.u.worlds))
        m.analyze(m.Problem(self.u,t)); m.analyze(m.Problem(self.u,t))
        self.assertEqual(len(calls),2)
        for factory in (m.table,m.constraint):
            with self.assertRaises(TypeError): factory(self.u,'x',None)
            with self.assertRaises(TypeError): factory(None,'x',lambda w:0)

    def test_question_and_index_validation(self):
        with self.assertRaises(TypeError): m.minimax_tree(self.p,[self.t])
        with self.assertRaises(ValueError): m.minimax_tree(self.p,(self.t,self.t))
        with self.assertRaises(ValueError): m.minimax_tree(self.p,(None,))
        tree=m.minimax_tree(self.p,(self.t,))
        with self.assertRaises(TypeError): m.follow_tree(self.p,(self.t,),tree,True)
        with self.assertRaises(ValueError): m.follow_tree(self.p,(self.t,),tree,2)
        with self.assertRaises(ValueError): chips(True)
        with self.assertRaises(ValueError): chips(0)


class SufficiencyTests(unittest.TestCase):
    def test_sufficient_for_query_not_entire_world(self):
        full,known,narrower=query_example()
        result=m.analyze(known)
        self.assertEqual(result.status,'identified')
        self.assertEqual(result.candidates,(0,1))
        self.assertEqual(result.answer,0)
        self.assertEqual(m.analyze(full).status,'underdetermined')
        with self.assertRaises(ValueError): _=m.analyze(full).answer

    def test_inconsistent_and_empty_universe_not_solutions(self):
        full,known,_=query_example()
        contradictory=m.add_evidence(known,m.constraint(known.universe,'x=1',lambda w:w[0]==1))
        self.assertEqual(m.analyze(contradictory).status,'inconsistent')
        u=m.Universe(('x',),()); p=m.Problem(u,m.Table(u,'x',()))
        self.assertEqual(m.analyze(p),m.Analysis('inconsistent',(),()))
        with self.assertRaises(ValueError): _=m.analyze(p).answer
        self.assertEqual(m.minimax_tree(p,()).status,'inconsistent')

    def test_add_evidence_is_monotone_not_rewriting(self):
        full,known,narrower=query_example()
        self.assertEqual(m.candidates(full),(0,1,2,3))
        self.assertTrue(set(m.candidates(known)) <= set(m.candidates(full)))
        self.assertTrue(set(m.candidates(narrower)) <= set(m.candidates(known)))
        self.assertEqual(len(full.constraints),0)
        redundant=m.add_evidence(known,m.constraint(known.universe,'redundant',lambda w:w[0]==0))
        self.assertTrue(m.compare_rewrite(known,redundant).worlds_preserved)

    def test_answer_preservation_is_weaker(self):
        _,known,narrower=query_example()
        r=m.compare_rewrite(known,narrower)
        self.assertFalse(r.worlds_preserved); self.assertTrue(r.answers_preserved)
        self.assertEqual(r.lost_worlds,(1,)); self.assertEqual(r.gained_worlds,())
        with self.assertRaises(ValueError): m.translation_chain((known,narrower))
        self.assertEqual(len(m.translation_chain((known,narrower),'answers')),1)
        self.assertEqual(m.compare_rewrite(narrower,known).gained_worlds,(1,))

    def test_chain_validates_each_step_and_target(self):
        full,known,_=query_example()
        with self.assertRaises(ValueError): m.translation_chain((known,full,known))
        with self.assertRaises(ValueError): m.translation_chain((known,))
        with self.assertRaises(ValueError): m.translation_chain([known,known])
        with self.assertRaises(ValueError): m.translation_chain((known,known),'syntax')
        changed=m.Problem(full.universe,m.table(full.universe,'tag',lambda w:w[1]))
        with self.assertRaises(ValueError): m.compare_rewrite(full,changed)
        empty=m.add_evidence(full,m.constraint(full.universe,'false',lambda w:False))
        report=m.compare_rewrite(empty,empty)
        self.assertTrue(report.worlds_preserved); self.assertTrue(report.answers_preserved)
        self.assertFalse(report.nonvacuous)

    def test_chips_rewrites_and_explicit_finite_bound(self):
        original,expanded,eliminated,solved,insufficient=chips()
        self.assertEqual(m.analyze(original).answer,(7,5))
        self.assertEqual(len(m.candidates(insufficient)),8)
        self.assertEqual(m.analyze(insufficient).status,'underdetermined')
        self.assertEqual(len(m.translation_chain((original,expanded,eliminated,solved))),3)
        self.assertEqual(m.analyze(chips(6)[0]).status,'inconsistent')
        self.assertFalse(m.compare_rewrite(original,insufficient).worlds_preserved)

    def test_all_binary_masks_on_four_worlds(self):
        u=m.Universe(('i',),tuple((i,) for i in range(4)))
        for target in product((0,1),repeat=4):
            for mask in product((False,True),repeat=4):
                p=m.Problem(u,m.Table(u,'target',target),(m.Constraint(u,'given',mask),))
                selected=tuple(i for i in range(4) if mask[i])
                answers=set(target[i] for i in selected)
                result=m.analyze(p)
                self.assertEqual(result.candidates,selected)
                self.assertEqual(set(result.answers),answers)
                expected='inconsistent' if not selected else 'identified' if len(answers)==1 else 'underdetermined'
                self.assertEqual(result.status,expected)


class CompressionTests(unittest.TestCase):
    def test_decoder_need_not_reconstruct_world(self):
        full,_,_=query_example()
        result=m.compression(full,full.target)
        self.assertTrue(result.sufficient); self.assertFalse(result.vacuous)
        self.assertEqual(result.decoder,((0,0),(1,1)))
        self.assertEqual(result.decode(1),1)
        with self.assertRaises(KeyError): result.decode(9)
        with self.assertRaises(TypeError): result.decode(True)

    def test_bad_fiber_has_counterexample(self):
        full,_,_=query_example()
        result=m.compression(full,m.table(full.universe,'constant',lambda w:0))
        self.assertFalse(result.sufficient); self.assertEqual(result.witness,(0,2))
        self.assertEqual(result.decoder,())
        with self.assertRaises(ValueError): result.decode(0)

    def test_fibers_are_relative_to_current_candidates(self):
        full,known,_=query_example()
        encoding=m.table(full.universe,'constant',lambda w:0)
        self.assertFalse(m.compression(full,encoding).sufficient)
        self.assertTrue(m.compression(known,encoding).sufficient)
        self.assertEqual(m.compression(known,encoding).decode(0),0)
        with self.assertRaises(ValueError): m.compression(known,None)

    def test_empty_decoder_is_vacuous_and_has_no_answers(self):
        u=m.Universe(('x',),()); p=m.Problem(u,m.Table(u,'t',()))
        result=m.compression(p,m.Table(u,'code',()))
        self.assertTrue(result.sufficient); self.assertTrue(result.vacuous)
        self.assertEqual(result.decoder,())
        with self.assertRaises(KeyError): result.decode(0)

    def test_exhaustive_binary_fibers(self):
        u=m.Universe(('i',),tuple((i,) for i in range(3)))
        for target in product((0,1),repeat=3):
            for code in product((0,1),repeat=3):
                for mask in product((False,True),repeat=3):
                    p=m.Problem(u,m.Table(u,'target',target),(m.Constraint(u,'mask',mask),))
                    result=m.compression(p,m.Table(u,'code',code))
                    conflicts=[(i,j) for i in range(3) for j in range(i+1,3)
                               if mask[i] and mask[j] and code[i]==code[j] and target[i]!=target[j]]
                    self.assertEqual(result.sufficient,not conflicts)
                    self.assertEqual(result.vacuous,not any(mask))
                    if result.sufficient:
                        for i in range(3):
                            if mask[i]: self.assertEqual(result.decode(code[i]),target[i])
                    else: self.assertIn(result.witness,conflicts)


class ObservationTests(unittest.TestCase):
    def test_selector_adaptive_two_fixed_three(self):
        p,qs=selector(); tree=m.minimax_tree(p,qs)
        self.assertEqual(tree.status,'measurement'); self.assertEqual(tree.depth,2)
        self.assertEqual(tree.question_index,0)
        for i,w in enumerate(p.universe.worlds):
            answer,path=m.follow_tree(p,qs,tree,i)
            self.assertEqual(answer,w[1] if w[0]==0 else w[2])
            self.assertEqual(path,('s','a') if w[0]==0 else ('s','b'))
        for subset in combinations(range(3),2):
            encoding=m.table(p.universe,'fixed pair',lambda w:tuple(w[i] for i in subset))
            self.assertFalse(m.compression(p,encoding).sufficient)
        self.assertTrue(m.compression(p,m.table(p.universe,'all',lambda w:w)).sufficient)

    def test_no_questions_and_zero_question_solution(self):
        full,known,_=query_example()
        self.assertEqual(m.minimax_tree(known,()).depth,0)
        result=m.minimax_tree(full,())
        self.assertEqual(result.status,'impossible'); self.assertEqual(result.witness,(0,2))
        with self.assertRaises(ValueError): m.follow_tree(full,(),result,0)

    def test_common_presence_does_not_determine_origin(self):
        p,qs=causal_toy(); node=m.minimax_tree(p,qs)
        self.assertEqual(node.status,'impossible'); self.assertEqual(node.witness,(0,1))
        self.assertEqual(qs[0].values,(((0,0),(1,1)),((0,0),(1,1))))
        self.assertEqual(m.analyze(p).status,'underdetermined')


    def test_causal_mechanisms_natural_equivalence(self):
        for u in (0,1):
            self.assertEqual(causal_run('M1',u),(u,u))
            self.assertEqual(causal_run('M2',u),(u,u))

    def test_causal_intervention_changes_available_information(self):
        p,qs=causal_toy()
        intervention=m.table(p.universe,'do S=1 at U=0',lambda w:causal_run(w[0],0,do_s=1))
        self.assertEqual(intervention.values,((1,1),(1,0)))
        augmented=qs+(intervention,)
        node=m.minimax_tree(p,augmented)
        self.assertEqual((node.status,node.depth,node.question_index),('measurement',1,1))
        for i in (0,1): self.assertEqual(m.follow_tree(p,augmented,node,i)[0],p.target.values[i])
        self.assertEqual(causal_run('M1',1,do_s=0),(0,0))
        self.assertEqual(causal_run('M2',1,do_s=0),(0,1))

    def test_causal_inputs_reject_aliases_and_unknown_models(self):
        for args in (('M3',0,None),('M1',True,None),('M1',0,False),
                     ('M1',0,1.0),('M1',2,None),(1,0,None)):
            with self.subTest(args=args), self.assertRaises(ValueError): causal_run(*args)

    def test_tie_break_and_nonbinary_observation(self):
        u=m.Universe(('x',),((0,),(1,),(2,)))
        p=m.Problem(u,m.Table(u,'target',(0,1,2)))
        qs=(m.Table(u,'first',(0,1,2)),m.Table(u,'second',('a','b','c')))
        tree=m.minimax_tree(p,qs)
        self.assertEqual(tree.question_index,0); self.assertEqual(tree.depth,1)
        self.assertEqual(tuple(v for v,_ in tree.branches),(0,1,2))

    def test_question_order_changes_tie_only(self):
        u=m.Universe(('x',),((0,),(1,)))
        p=m.Problem(u,m.Table(u,'target',(0,1)))
        q1=m.Table(u,'q1',(0,1)); q2=m.Table(u,'q2',('a','b'))
        for qs in ((q1,q2),(q2,q1)):
            tree=m.minimax_tree(p,qs)
            self.assertEqual(tree.question_index,0); self.assertEqual(tree.depth,1)

    def test_joint_signatures_determine_possibility_exhaustively(self):
        u=m.Universe(('i',),((0,),(1,),(2,)))
        vectors=tuple(product((0,1),repeat=3))
        for target in vectors:
            p=m.Problem(u,m.Table(u,'t',target))
            for a in vectors:
                for b in vectors:
                    qs=(m.Table(u,'a',a),m.Table(u,'b',b))
                    tree=m.minimax_tree(p,qs)
                    impossible=any(target[i]!=target[j] and a[i]==a[j] and b[i]==b[j]
                                   for i in range(3) for j in range(3))
                    self.assertEqual(tree.status=='impossible',impossible)
                    if not impossible:
                        self.assertLessEqual(tree.depth,2)
                        for i in range(3): self.assertEqual(m.follow_tree(p,qs,tree,i)[0],target[i])


if __name__ == '__main__': unittest.main()
