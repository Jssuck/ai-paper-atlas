# 从两种假设动作到两条方程

以下片段在本目录 `python3` 交互环境中可直接运行；完整同构演练是 `python3 walkthrough.py`，三种优化模式的真实输出保存在 evidence 中。

## 1. 先固定量的含义

R、L 始终是初始数量。两次“如果”各自从初始状态出发。

```python
from fractions import Fraction as F
from condillac_model import *
rows = transfer()
print(rows)
print(solve(rows))
```

两行依次为 Aff(1,−1,−2)、Aff(1,−2,3)，表示 R−L−2=0 与 R−2L+3=0。唯一有理解为 (7,5)。实际转移检查：右移出1后两边为6；左移出1后右8、左4。

## 2. 每次保留整个方程组

```python
trace = certificate(rows, [('add',1,0,-1), ('scale',1,-1), ('add',0,1,1)])
for state in trace:
    print(state, equivalent(rows,state))
```

所有判断为 True。四个状态依次是原组；(R−L−2,−L+5)；(R−L−2,L−5)；(R−7,L−5)。每个表达式均被理解为等于零。

## 3. 派生式可以丢掉信息

```python
only_consequence = (rows[1]-rows[0],)
print(holds(only_consequence,0,5), holds(rows,0,5))
print(equivalent(only_consequence,rows))
```

结果依次为 True、False、False。一个推出的条件未必等价于所有前提。

## 4. 改变动作次序就是改变问题

```python
print(solve(sequential()))
print(holds(sequential(),7,5))
```

结果是唯一解 (4,2)，随后 False。先转一个再转回一个，第二步回到初始状态；其两倍关系不再是原来的第二个假设。

## 5. 有理解、自然数解和有界观察

```python
print(solve(transfer(1,1,4)))
print(feasible(F(13,3),F(7,3)))
print(oracle(transfer(),12))
print(solve(transfer(1,1,1)))
print(solve(transfer(0,0,1)))
```

依次是 (13/3,7/3)、False、((7,5),)、none、infinite。分数不能成为不可分筹码；参数公式与退化证明见 MODEL。只枚举0–12不能排除外部解；这里原题的全局唯一性来自消元证明。

## 6. 故障检查

```sh
python3 mutation_check.py
python3 -O mutation_check.py
python3 -OO mutation_check.py
```

八种行为变体均应显示 killed；这表示预定输出差异已发现，不表示程序没有其他错误。崩溃显示 error，不能冒充有效检测。单元测试会专门检查这一分类规则。
