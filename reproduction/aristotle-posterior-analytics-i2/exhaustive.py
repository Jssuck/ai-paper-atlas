"""Independent per-world oracle vs production bitmask inclusion; finite only."""
import json
from itertools import product
from dataclasses import replace
from model import entails, inspect_candidate, classify_starting_point
from test_model import fixture

def run():
    pairs=valid=disagreements=0
    for p,q in product(range(256),repeat=2):
        expected=all(not ((p >> w) & 1) or bool((q >> w) & 1) for w in range(8))
        observed=entails([p],q)
        pairs+=1; valid+=expected; disagreements+=expected != observed
    c=fixture(); samples={}
    samples['declared_all']=inspect_candidate(c)
    samples['same_truths_no_cause']=inspect_candidate(replace(c,cause_links_declared=frozenset()))
    samples['equivalence_no_cause']=inspect_candidate(replace(c,conclusion_mask=c.premises[0].truth_mask,cause_links_declared=frozenset()))
    samples['false_actual_valid_inference']=inspect_candidate(replace(c,actual_world=0))
    samples['confidence_equal']=inspect_candidate(replace(c,conclusion_confidence=3))
    flags=passes=0
    for primary, immediate, prior, confidence, cause in product((False,True),repeat=5):
        p=replace(c.premises[0],primary_declared=primary,immediate_declared=immediate,priority_rank=0 if prior else 1,confidence_rank=3 if confidence else 2)
        r=inspect_candidate(replace(c,premises=(p,),cause_links_declared=c.cause_links_declared if cause else frozenset()))
        flags+=1; passes+=r['declared_policy_pass']
    return {'finite_worlds':8,'truth_mask_pairs':pairs,'valid_pairs':valid,'oracle_disagreements':disagreements,
            'fixed_semantics_metadata_variants':flags,'policy_pass_variants':passes,'examples':samples,
            'limits':'Truth masks and supplied metadata cannot establish causes, immediacy, necessity, or human knowledge.'}
if __name__=='__main__':
    result=run()
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if result['oracle_disagreements'] != 0: raise SystemExit('oracle disagreement')
