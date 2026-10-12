# 逐步演练：先固定对象，再检查名称与次序

以下代码块可在本目录的 Python 交互环境逐段执行。它们是新写的教学例子，符号 `p`、`q` 不对应孔狄亚克某个未经核对的历史原例。一般证明见 [模型说明](MODEL.zh-CN.md)。

## 1. 四个世界并未因定义而减少

先设两个原始布尔量 `p`、`q`，再给它们的合取取名 `both`，给其否定取名 `not_both`。

```python
from condillac_model import *

system = DefinitionSystem(
    ("p", "q"),
    (
        Definition("both", And(Var("p"), Var("q"))),
        Definition("not_both", Not(Var("both"))),
    ),
)
worlds = system.worlds()
print(worlds)
```

逐行计算：

| `p` | `q` | `both = p and q` | `not_both` |
| --- | --- | --- | --- |
| False | False | False | True |
| False | True | False | True |
| True | False | False | True |
| True | True | True | False |

1. 固定原始行，例如 `p=True, q=False`。
2. 右式只用原始值，故 `both=False`。
3. `not_both` 引用已经得到的 `both`，故为 `True`。
4. 没有第二种满足两个等式的扩张；也没有任何原始行被排除。

原始命题 `p` 仍不在全部四个世界为真：

```python
print(entails(worlds, Var("p")))  # False
```

`both` 这个名称可以省略长表达式，也可以使讨论清楚，但尚未告诉我们现实对应哪一行。

## 2. 加证据才会过滤世界

现在另行断言 `both=True`：

```python
remaining = filter_evidence(worlds, Var("both"))
print(remaining)
print(entails(remaining, Var("p")))  # True
```

只剩 `p=True, q=True, both=True, not_both=False`。变化来自新增的事实约束，而不是定义自身。

如果证据自相矛盾：

```python
impossible = filter_evidence(worlds, And(Var("p"), Not(Var("p"))))
print(len(impossible))                         # 0
print(entails(impossible, Var("p")))          # True
print(entails(impossible, Not(Var("p"))))     # True
```

两个 `True` 是空集全称量化的数学约定。先检查有没有剩余世界，再解释蕴涵结果；不能把矛盾过滤后的空真宣传为发现了事实。

## 3. 方程不都享有显式定义的保证

显式系统会拒绝以下环；穷举方程 oracle 则能显示它们为什么不同：

```python
print(satisfying_extensions({}, (Definition("d", Not(Var("d"))),)))
# ()

print(satisfying_extensions({}, (Definition("d", Var("d")),)))
# ({'d': False}, {'d': True})

print(satisfying_extensions({}, (Definition("d", And(Var("d"), Const(False))),)))
# ({'d': False},)
```

第一式逐试 `d=False` 和 `d=True`，均与自身的否定不同，故零解。第二式两个值都满足，故多解。第三式右侧恒为假，只有 `d=False` 满足。无环保证足够强、容易检查，但不是“唯一解”的必要条件。

旧名等式也另当别论：

```python
force_p = (Definition("p", Const(True)),)
print(satisfying_extensions({"p": False}, force_p))  # ()
print(satisfying_extensions({"p": True}, force_p))   # ({'p': True},)
```

oracle 固定旧值，并不把 `False` 偷改为 `True`。这条等式排除原始世界，因此不符合保守扩张的前提。

## 4. 同一观察下存在相反目标，就无法仅凭观察表达它

观察 `p`，目标是尚未观察的 `q`：

```python
base_worlds = enumerate_worlds(("p", "q"))
result = analyze_observations(base_worlds, (Var("p"),), Var("q"))
print(result.definable)  # False
print(result.witness)
# ({'p': False, 'q': False}, {'p': False, 'q': True})
```

检查这两个世界：

1. 观察输出都是 `(False,)`。
2. 目标分别是 `False` 与 `True`。
3. 任意只接受 `(False,)` 作为输入的确定函数，不能同时输出两个不同值。
4. 因而失败不只是搜索暂未找到公式，而是有一个可检查的不可能性见证。

把观察扩成 `p`、`q`，目标改为二者合取：

```python
result = analyze_observations(
    base_worlds, (Var("p"), Var("q")), And(Var("p"), Var("q"))
)
print(result.definable)  # True
formula = observed_formula(result, ("x", "y"))
print(evaluate(formula, {"x": True, "y": False}))  # False
print(evaluate(formula, {"x": True, "y": True}))   # True
```

目标真值在调用时已由表达式给定；程序只是检查能否通过观察表达它。`x`、`y` 是合成的观察坐标，分别绑定两个观察特征的输出，不能未经转换就当作原始世界的同名量。

这里只有 `(True, True)` 的目标为真，所以生成的 DNF 与 `x and y` 等值。生成器会保留教学上直观的常量与连接词，不做公式最简化。

## 5. 零观察和局部世界集

没有任何特征时，每个世界都映到同一个空元组：

```python
print(analyze_observations(enumerate_worlds(("p",)), (), Var("p")).definable)
# False
print(analyze_observations(enumerate_worlds(("p",)), (), Const(True)).table)
# (((), True),)
```

常值目标可表示，变化的目标不可表示。

若只给一行 `p=True, q=True`，目标 `q` 相对于这一个世界当然可从 `p` 表示：

```python
local = analyze_observations(({"p": True, "q": True},), (Var("p"),), Var("q"))
print(local.table)  # (((True,), True),)
local_formula = observed_formula(local, ("x",))
print(evaluate(local_formula, {"x": False}))  # False
```

最后的 `False` 来自程序对未见观察值的默认补全。它不是“已经观察到 `p=False` 时 `q=False`”的结论。如果把先前反例世界重新加入，可表示性就可能消失。

## 6. 逐步验证学习计划

用标签 `sense`、`compare`、`name` 演示一个声明的前提链。标签只为方便阅读，不是人的感觉、比较和命名过程的心理学测量。

```python
rules = (
    Rule(frozenset(("sense",)), "compare"),
    Rule(frozenset(("compare",)), "name"),
)
plan = plan_learning(("sense",), rules)
print(plan)  # ('compare', 'name')
print(verify_order(("sense",), rules, plan).valid)  # True
```

逐步检查：

| 步骤 | 此前可用集合 | 本步 | 检查结果 |
| --- | --- | --- | --- |
| 0 | `sense` | `compare` | 全部前提 `sense` 已有，可加入 |
| 1 | `sense, compare` | `name` | 全部前提 `compare` 已有，可加入 |

反过来：

```python
report = verify_order(("sense",), rules, reversed(plan))
print(report.valid)                 # False
print(report.failure_index)         # 0
print(report.missing_alternatives)  # (frozenset({'compare'}),)
```

第一步就要求尚不可用的 `compare`。它证明这条反序在当前种子和规则下失败；没有证明一切反向叙述、演绎或综合都不合法。

如果两项都只依赖同一个种子，两个顺序都合法：

```python
independent = (
    Rule(frozenset(("a",)), "b"),
    Rule(frozenset(("a",)), "c"),
)
print(verify_order(("a",), independent, ("b", "c")).valid)  # True
print(verify_order(("a",), independent, ("c", "b")).valid)  # True
```

## 7. 有环不等于有种子也无法推进

```python
cycle = (
    Rule(frozenset(("a",)), "b"),
    Rule(frozenset(("b",)), "a"),
)
print(sorted(forward_closure((), cycle)))        # []
print(sorted(forward_closure(("a",), cycle)))  # ['a', 'b']
```

没有种子时，两条规则都等待对方；给定 `a` 后，第一条规则可启动。规则循环与定义方程循环属于不同模型，不能混为一个反例。

最后再分开“规则可导出”与“在世界中为真”：

```python
declared = (Rule(frozenset(("p",)), "q"),)
print("q" in forward_closure(("p",), declared))       # True
print(evaluate(Var("q"), {"p": True, "q": False}))  # False
```

这不是算法矛盾；而是给定规则在该世界中不保真。要从可导出进一步保证真实，必须额外假设初始事实为真，而且每条规则保真。

## 8. 如何验证，不只看演示输出

运行 `python3 verify.py` 会在本目录下写入 `evidence/`，逐一执行普通、`-O`、`-OO` 模式的测试、变异检测与 JSON 演示，并比较三份演示输出。该脚本覆盖本次证据文件，适用于你自己的重跑；随附文件是一次实际执行记录。

单元测试故意检查错误输入与反例，而不仅比较漂亮的正例。六个定向变异分别破坏定义值、观察冲突检测、全部前提条件、时间顺序、证据过滤及旧值固定。只有明确的行为比较失败才记为检测成功，意外异常另计并导致验证失败。
