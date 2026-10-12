"""Small reproducible examples; JSON values are deterministic and sorted."""
import json
from model import (HypothesisSpace, HornSystem, Rule, Vocabulary, aligned_dictionary,
                   inverse_dictionary, translate_atoms, translation_preserves,
                   rename_rule, task_exact)


def main():
    hypotheses = HypothesisSpace(('x', 'y', 'z'), (
        ('true', ('0', '0', '1')), ('twin', ('0', '0', '0')), ('other', ('1', '1', '1'))))
    observations = [('x', '0'), ('y', '0'), ('z', '1')]
    prefix_candidates = [sorted(hypotheses.candidates(observations[:k])) for k in range(4)]
    noise = [('x', '1'), ('y', '0'), ('z', '1')]
    horn = HornSystem(('rain', 'wet', 'slip'), (
        Rule('wet_to_slip', {'wet'}, 'slip'), Rule('rain_to_wet', {'rain'}, 'wet')))
    closure = horn.close({'rain'})
    vocabulary_a = Vocabulary((('rain', 'rain'), ('wet', 'wet'), ('dry', 'dry')))
    vocabulary_b = Vocabulary((('rain', 'lluvia'), ('wet', 'mojado'), ('dry', 'seco')))
    correct = aligned_dictionary(vocabulary_a, vocabulary_b)
    wrong = {'rain': 'lluvia', 'wet': 'seco', 'dry': 'mojado'}
    source_rule = Rule('rain_to_wet', {'rain'}, 'wet')
    source = HornSystem(tuple(sorted(vocabulary_a.words)), (source_rule,))
    target = HornSystem(tuple(sorted(vocabulary_b.words)), (rename_rule(source_rule, correct),))
    wrong_target = HornSystem(tuple(sorted(vocabulary_b.words)), (rename_rule(source_rule, wrong),))
    source_closure = source.close({'rain'}).atoms
    worlds = ('w1', 'w2', 'w3', 'w4')
    task = dict(zip(worlds, ('safe', 'safe', 'unsafe', 'unsafe')))
    small = dict(zip(worlds, ('A', 'A', 'B', 'B')))
    large = dict(zip(worlds, ('X', 'Y', 'X', 'Z')))
    output = {
        'status': 'modern teaching reconstruction; not historical algorithm or psychological evidence',
        'hypotheses': {
            'prefix_candidates': prefix_candidates,
            'candidate_counts': list(map(len, prefix_candidates)),
            'xy_distinguishes_all': hypotheses.distinguishes(('x', 'y')),
            'xz_distinguishes_all': hypotheses.distinguishes(('x', 'z')),
            'noisy_exact_candidates': sorted(hypotheses.candidates(noise)),
            'noisy_budget_one_candidates': sorted(hypotheses.candidates(noise, 1)),
            'noisy_singleton_wrong': sorted(hypotheses.candidates([('x', '1')]))},
        'horn': {
            'seeds': sorted(closure.seeds), 'closure': sorted(closure.atoms),
            'trace': [{'rule': s.rule, 'premises': list(s.premises), 'conclusion': s.conclusion}
                      for s in closure.steps],
            'trace_verified': horn.verify_trace(closure, {'rain'}),
            'closed_again': sorted(horn.close(closure.atoms).atoms),
            'second_trace_length': len(horn.close(closure.atoms).steps),
            'empty_truth_satisfies_rules': horn.closed(set()),
            'false_atoms_if_truth_empty': sorted(closure.atoms)},
        'translation': {
            'correct_dictionary': correct, 'wrong_dictionary': wrong,
            'correct_preserves_semantics': translation_preserves(vocabulary_a, vocabulary_b, correct),
            'wrong_preserves_semantics': translation_preserves(vocabulary_a, vocabulary_b, wrong),
            'wrong_round_trip_wet': sorted(translate_atoms(translate_atoms({'wet'}, wrong), inverse_dictionary(wrong))),
            'wrong_target_meaning_of_wet': sorted(vocabulary_b.decode(translate_atoms({'wet'}, wrong))),
            'translated_source_closure_correct': sorted(translate_atoms(source_closure, correct)),
            'genuine_target_closure': sorted(target.close({'lluvia'}).atoms),
            'translated_source_closure_wrong': sorted(translate_atoms(source_closure, wrong)),
            'wrong_transported_rule_closure': sorted(wrong_target.close({'lluvia'}).atoms)},
        'task_precision': {
            'worlds': list(worlds), 'task': task, 'small_labels': small, 'large_labels': large,
            'small_label_count': len(set(small.values())), 'large_label_count': len(set(large.values())),
            'small_exact': task_exact(worlds, small, task), 'large_exact': task_exact(worlds, large, task)}}
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
