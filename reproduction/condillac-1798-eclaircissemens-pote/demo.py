"""Small adversarial examples, printed deterministically."""
from fractions import Fraction as F
from model import change_count, idea_word, synchronize


def show_rows(rows):
    return '; '.join(f'[{a},{b}):{",".join(labels)}' for a,b,labels in rows)


def main():
    h = {'a':'still', 'b':'still'}
    print('HIDDEN CHANGES (one observation label, unequal latent counts)')
    for trace in [('a',), ('a','b','a','b')]:
        print(f'trace={trace}; idea_word={idea_word(trace,h)}; latent_changes={change_count(trace)}')
    print('JOINT OBSERVATION (neither marginal injective; product injective)')
    h1, h2 = {'a':'0','b':'0','c':'1'}, {'a':'0','b':'1','c':'0'}
    print(tuple((state,h1[state],h2[state]) for state in 'abc'))
    print('ALIGNMENT LOSS (same marginal idea words, two supplied timelines)')
    early = ((F(0),'0'), (F(1,3),'1'))
    late = ((F(0),'0'), (F(2,3),'1'))
    print('A early, B late: ' + show_rows(synchronize((early,late))))
    print('A late, B early: ' + show_rows(synchronize((late,early))))
    print('Both marginal compressed words are (0,1); they do not determine event order.')
    print('These event coordinates are inputs, not inferred absolute time.')

if __name__ == '__main__':
    main()
