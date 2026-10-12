# 从“说清楚”到“还缺哪条资料”

在本目录运行 `python3 walkthrough.py`，它会按顺序执行下列全部 Python 块。也可把这些块依次复制到同一个 Python 3.10+ 会话。每块都带真正的结果核对，不依赖会被 `-O` 移除的 assert。这里只演示有限现代模型。

## 1. 唯一答案不要求唯一世界

资料告诉我们 x=0，但没有告诉我们标签。询问 x 已够；询问整个世界还不够。

```python
import condillac_model as m
from examples import query_example, chips, selector, causal_toy, causal_run

def check(actual, expected):
    if actual != expected:
        raise RuntimeError(f'expected {expected!r}, got {actual!r}')

full, known, narrower = query_example()
a = m.analyze(known)
check((a.status, a.candidates, a.answer), ('identified', (0, 1), 0))
print(a.status, 'worlds=', a.candidates, 'answer=', a.answer)
```

预期：identified，候选世界索引(0,1)，答案0。

## 2. 保住当前答案可能仍丢了世界

把标签强行定为A，删去第二个可能世界。对查询 x，答案集合没有变；却不能当作世界意义上等价。

```python
r = m.compare_rewrite(known, narrower)
check((r.worlds_preserved, r.answers_preserved, r.lost_worlds), (False, True, (1,)))
print('worlds preserved:', r.worlds_preserved, 'answers preserved:', r.answers_preserved)
try:
    m.translation_chain((known, narrower))
except ValueError:
    print('world-preserving translation rejected')
else:
    raise RuntimeError('loss of a possible world went undetected')
```

## 3. 筹码：改写与补资料分开

两个独立假设情景给出 x−1=y+1 与 x+1=2(y−1)。先只保留前者，可行域里仍有八种两手数量。加入后一条，才缩到(7,5)。接着的代数改写保持全部候选世界。

```python
original, expanded, eliminated, solved, insufficient = chips()
check(len(m.candidates(insufficient)), 8)
completed = m.add_evidence(insufficient, original.constraints[-1])
check(m.analyze(completed).answer, (7, 5))
reports = m.translation_chain((original, expanded, eliminated, solved))
check(tuple(r.worlds_preserved for r in reports), (True, True, True))
print('before:', m.analyze(insufficient).status, 'candidates=', len(m.candidates(insufficient)))
print('after:', m.analyze(completed).answer, 'rewrites=', len(reports))
check(m.analyze(chips(6)[0]).status, 'inconsistent')
print('bound 6 excludes the solution:', m.analyze(chips(6)[0]).status)
```

这里上界10是我们加的有限枚举条件。上界6的失败不是一般方程无解。

## 4. 同一编码纤维能否藏着不同答案？

以 x 为编码可以回答 x，不能还原标签；这只是编码已知时能否解码的语义检查，不声称无需观测即可得到 x。全域使用常数编码则不能分开0与1。若已有资料 x=0，同一常数编码在缩小后的候选域上足够。

```python
c = m.compression(full, full.target)
check((c.sufficient, c.decode(0), c.decode(1)), (True, 0, 1))
constant = m.table(full.universe, 'same code', lambda w: 0)
bad = m.compression(full, constant)
check((bad.sufficient, bad.witness), (False, (0, 2)))
check(m.compression(known, constant).sufficient, True)
print('decoder:', c.decoder)
print('conflicting fiber witness:', bad.witness)
```

## 5. 针对问题选择下一条资料

询问目标 t=a（s=0）或 t=b（s=1）。最优策略先问选择位s，然后只问相关位。所有世界回放，都核对答案及问题路径。

```python
p, questions = selector()
tree = m.minimax_tree(p, questions)
check((tree.status, tree.depth, tree.question_index), ('measurement', 2, 0))
for i, world in enumerate(p.universe.worlds):
    answer, path = m.follow_tree(p, questions, tree, i)
    expected = world[1] if world[0] == 0 else world[2]
    check(answer, expected)
    check(path, ('s', 'a') if world[0] == 0 else ('s', 'b'))
    print(world, '->', path, '->', answer)
```

固定的任何两问都不够。联合问齐三项则足够；下面直接检查每个固定问题集合的编码纤维。

```python
from itertools import combinations
for pair in combinations(range(3), 2):
    code = m.table(p.universe, 'fixed pair', lambda w: tuple(w[i] for i in pair))
    check(m.compression(p, code).sufficient, False)
    print('fixed pair insufficient:', tuple(questions[i].name for i in pair))
all_three = m.table(p.universe, 'all three', lambda w: w)
check(m.compression(p, all_three).sufficient, True)
print('adaptive worst case: 2; smallest sufficient fixed set: 3')
```

## 6. 共同出现并不能单独判定起源

这是人为设定并实际执行的两个机制：M1令S:=U、A:=S；M2令A:=U、S:=A。二者自然观测均为U=0时(S,A)=(0,0)，U=1时(1,1)。固定U=0并另行允许替换S方程为1时，它们才显示不同。程序不判断真实心理学。

```python
toy, observations = causal_toy()
plan = m.minimax_tree(toy, observations)
check((plan.status, plan.witness), ('impossible', (0, 1)))
print('same observation:', observations[0].values)
print('different stipulated models:', toy.universe.worlds)
print('result:', plan.status, 'witness=', plan.witness)
intervention = m.table(toy.universe, 'do(S=1),U=0', lambda w: causal_run(w[0], 0, do_s=1))
check(intervention.values, ((1, 1), (1, 0)))
augmented = m.minimax_tree(toy, observations + (intervention,))
check((augmented.status, augmented.depth), ('measurement', 1))
print('extra intervention:', intervention.values, 'new worst depth=', augmented.depth)
```

## 7. 空域的“空真”不等于得到答案

空候选上没有违反纤维条件的一对世界，但也没有能够解出的编码值。

```python
u = m.Universe(('x',), ())
empty = m.Problem(u, m.Table(u, 'target', ()))
result = m.compression(empty, m.Table(u, 'encoding', ()))
check((m.analyze(empty).status, result.sufficient, result.vacuous, result.decoder),
      ('inconsistent', True, True, ()))
try:
    result.decode(0)
except KeyError:
    print('empty decoder yields no answer')
else:
    raise RuntimeError('empty-domain answer was fabricated')
```

若想改动实验，优先明确“世界域是什么、已有哪些资料、到底要问什么、允许取得哪些额外观测”。把代码写短或表述写顺，都不能替代这些说明。
