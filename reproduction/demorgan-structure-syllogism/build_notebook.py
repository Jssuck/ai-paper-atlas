"""Fill the tutorial scaffold with original lessons; rerunning clears outputs."""
from pathlib import Path
import json

path=Path(__file__).with_name('tutorial.ipynb')
doc=json.loads(path.read_text(encoding='utf-8'))
cells=[]

def md(text):
    cells.append({'cell_type':'markdown','id':f'dm-{len(cells):02d}',
                  'metadata':{},'source':text.strip().splitlines(keepends=True)})

def code(text):
    cells.append({'cell_type':'code','id':f'dm-{len(cells):02d}','metadata':{},
                  'source':text.strip().splitlines(keepends=True),'execution_count':None,'outputs':[]})

md('''# De Morgan 1847：集合、比例与条件概率

这是一份原创现代教学重构，依据 *On the Structure of the Syllogism, and on the Application of the Theory of Probabilities to Questions of Argument and Authority*，印页379–408。

**读者与前置知识：** 会读简单 Python、集合与分数即可。目标是亲手检查八种命题、量化交集、两种随机模型、论证与权威的概率组合，以及附录的七种类关系。

**运行：** Python 3.10+，仅标准库，无下载、服务、安装或随机种子。打开现成 Jupyter 后“重启并运行全部”，或在本目录执行 `python execute_notebook.py tutorial.ipynb`。交付记录来自后者：共享命名空间的 CPython 顺序执行，不是 Jupyter kernel。所有代码均为普通 Python。只执行可信 notebook。

**路线：** ①论域与八命题 → ②存在假定与数量 → ③随机模型 → ④条件概率与未知权威 → ⑤一般规则与依赖反例 → ⑥附录与测试边界。

原文符号、印式审计和明确省略部分见 `SOURCE_LEDGER.md`。有限测试不能替代一般证明；本教程也不是整篇论文的形式化验证。''')
code('''from fractions import Fraction as F
from itertools import product
import demorgan as d
print('精确分数示例：', F(3, 5) + F(7, 10))
print('八命题记号：', ', '.join(d.PROPOSITIONS))''')
md('''## 1. 论域不是可省略的背景（pp.379–382）

固定 U；小写 x、y 是相对于 U 的补集。大写/小写命题字母不同：A 是 X⊆Y，a 是 Y⊆X；E 是不相交，e 是并集覆盖 U；I 是有共同个体，i 是有个体既非 X 也非 Y；O 是 X\\Y 非空，o 是 Y\\X 非空。

这里的 a 不是“非 A”；A 的矛盾命题是 O。e 也不等于“X 与 Y 恰好互补”：覆盖并不排除相交。''')
code('''U = frozenset(range(4))
X, Y = frozenset({0, 1}), frozenset({1, 2})
print('U =', sorted(U), 'X =', sorted(X), 'Y =', sorted(Y))
print(d.propositions(U, X, Y))
for p, q in [('A','O'), ('a','o'), ('E','I'), ('e','i')]:
    values = d.propositions(U, X, Y)
    assert values[p] != values[q]
print('四组矛盾对检查通过')''')
md('''## 2. 空项改变了什么？（pp.382–383；407–408）

程序的底层采用现代集合语义：空集是任意集合的子集，全称不自动带存在蕴涵。若同时要求 X、Y 及其补集非空，则 A/a 蕴涵 I 和 i；E/e 蕴涵 O 和 o。此额外条件必须单列，不能藏进布尔函数。

附录七分类按本实现的明确工作域“非空、非全域的项”使用。允许退化项时，原式分类可能重叠。''')
code('''ordinary = d.propositions({0,1,2}, {0}, {0,1})
empty_subject = d.propositions({0,1,2}, set(), {0,1})
print('非空 proper terms：A, I, i =', ordinary['A'], ordinary['I'], ordinary['i'])
print('空主词：A, I =', empty_subject['A'], empty_subject['I'])
print('两项都空时同时成立的分类：',
      [k for k,v in d.relation_matches({0}, set(), set()).items() if v])''')
md('''## 3. “多数 + 多数”是确定的交集下界（p.384；Addition p.406）

若中项 Y 内两群的比例是 m、n，则共同部分至少 `max(0,m+n−1)`。一般证明是一行容斥：|S∩T|=|S|+|T|−|S∪T|≥|S|+|T|−|Y|；下界可由尽量分开的两群达到。这里不需要独立性。

当 m+n=1 时可以完全不相交；必须严格大于1才能保证存在交集。p.406 将同一鸽巢思想写成“有效个数”。''')
code('''print('3/5 与 7/10：至少', d.overlap_lower_bound(F(3,5), F(7,10)))
print('1/2 与 1/2：至少', d.overlap_lower_bound(F(1,2), F(1,2)))
Y100 = set(range(100))
first, second = set(range(60)), set(range(30,100))
assert len(first & second) == 30
print('紧例：两群 60 与 70 人，共同 30 人')
print('p.406 有效数：50 + 60 − 100 =', d.count_overlap_lower_bound(100,50,60))''')
md('''## 4. 相同比例，换抽样机制，概率大变（pp.385–387）

模型一：在 s 个对象中独立均匀选 m 个、n 个。无交集概率为 C(s−m,n)/C(s,n)。模型二：在单位线段里独立均匀放置两段连续区间，长度 μ、μ′；无交叠概率为 `(1−μ−μ′)²/((1−μ)(1−μ′))`，此处 μ+μ′≤1。

“没有已知关联”不能逻辑上证明均匀性或独立性；这两者是各模型的选择。原文用二者对比，正好提醒我们把抽样结构写清楚。''')
code('''p_none = d.random_subset_disjoint(1000, 100, 100)
print('随机子集：P(无共同者) ≈ %.10f' % float(p_none))
print('随机子集：有共同者的赔率 ≈ %.3f : 1' % float((1-p_none)/p_none))
p_interval = d.interval_overlap_cdf(F(1,10), F(1,10))
print('连续区间：P(无交叠) =', p_interval, '；有交叠 =', 1-p_interval)
print('原文近似：前者约 70,000:1 倾向有交集；后者 64:17 倾向无交集')''')
md('''## 5. 权威的合并：先说明怎样的联合模型（pp.393–395）

原文的 testimony μ 是概率；authority a=2μ−1 可为负。相同颜色球的模型给出 `∏μ/(∏μ+∏(1−μ))`。

现代重构：先取独立的伯努利旗标，再条件化到“全部真或全部假”。输入是条件化以前的参数，条件化后的边际通常会改变。这不是凭各人的单独准确率就能普遍推断真实证词可靠性的定理。''')
code('''mu, mp = F(3,4), F(4,5)
q = d.joint_testimony([mu, mp])
law = d.conditional_product([d.bernoulli(mu), d.bernoulli(mp)], lambda s: s[0] == s[1])
print('合并 testimony =', q, '；odds =', q/(1-q))
print('独立产品条件化 oracle：', law)
print('合并 authority =', d.authority(q))
assert q == law[True, True]''')
md('''### 印式审计，而非无声修正（p.396）

二权威偏倚模型先写混合式 `λμ+(1−λ)joint(μ,μ′)`。相邻的 authority 印式分子是 `a+a′−2λa′(1−a)`。按 a=2μ−1 代回混合式，应得到 `a+a′−λa′(1−a²)`，分母均为 `1+aa′`。

以下输入使差异不再被特殊值掩盖。程序保留原印式供审计，不把它当修正式使用。λ 也是额外模型参数，并不能由 μ、μ′自行推出。''')
code('''lam = F(1,3)
mixed = d.biased_testimony(mu, mp, lam)
print('混合 testimony =', mixed)
print('由混合式得到 authority =', d.authority(mixed))
print('字面 authority 印式 =', d.printed_biased_authority(mu, mp, lam))
assert d.authority(mixed) == F(19,26)
assert d.printed_biased_authority(mu, mp, lam) == F(9,13)''')
md('''## 6. 论证失败，不等于结论为假（pp.393–398）

互相矛盾的结论不能都被有效论证证明。p.397 的特定兼容模型留下三个权重：a(1−b)、b(1−a)、(1−a)(1−b)，归一化分母为1−ab。第三项是“都未证明”，并非第三种真值。

原文 p.396–397 已讨论更一般的配对依赖，随后选择每一兼容笛卡尔组合都可发生的特例。本实现精确复现这个特例，不把“所有依赖都已解决”作为结论。''')
code('''a, b = F(3,4), F(1,2)
arguments = d.opposing_arguments(a, b)
print('只看论证：', arguments)
lo = arguments['for']
hi = 1-arguments['against']
print('未分配不定项时，结论真概率可在', lo, '到', hi, '之间')
print('p.398 另加 authority 参数 μ=2/3：', d.conclusion_probability(a,b,F(2,3)))
try:
    d.opposing_arguments(1, 1)
except ValueError as exc:
    print('两个绝对证明相互矛盾：', str(exc))''')
md('''## 7. 未知 authority：平均参数 ≠ 平均结论（p.401）

记 r=(1−b)/(1−a)，固定 μ 时结论概率为 f(μ)=rμ/(rμ+1−μ)。原文再平均这个非线性函数：先试均匀密度，再用密度6μ(1−μ)，即现代所谓 Beta(2,2)。两者的 μ 均值都为1/2，但结果通常不等于 f(1/2)。

此处单独标为浮点数值实验：闭式与独立复合 Simpson 积分对照。其余离散概率保留 Fraction。原文接着批评把未知 authority 的所有值等权看待；程序不将均匀先验说成中性的唯一选择。这里平均的是已归一化函数；若将同一密度当作条件化前的超先验，兼容性事件也会重加权 μ，不能把两种次序自动视为同一层次更新。''')
code('''r = 4
print('固定 μ=1/2：', r/(r+1))
for prior in ('uniform', 'beta22'):
    formula = d.averaged_authority(r, prior)
    quadrature = d.averaged_authority_quadrature(r, prior)
    print(prior, '闭式 = %.12f，积分 = %.12f，差 = %.2g' %
          (formula, quadrature, abs(formula-quadrature)))
    assert abs(formula-quadrature) < 1e-10
print('r=1 的连续极限：', d.averaged_authority(1))''')
md('''## 8. 多选一与恰选 k 个（pp.403–405）

若恰有一个命题为真，原文把各项指数写成 `e_i=μ_i/((1−a_i)(1−μ_i))`，然后归一化。恰 k 项为真时，对每个 k 元子集乘其指数，再归一化。它是明确约束下的积权模型。

程序对单选保留未约分乘积式，避免概率0或1导致人为的 odds 除零；总兼容质量真的为零时仍会报错。''')
code('''print('三选一：', d.hypothesis_weights([F(1,2),F(1,3),F(1,4)],
                                      [F(2,3),F(3,5),F(4,7)]))
exact_two = d.exactly_k([1,2,3,4], 2)
print('四项指数1,2,3,4，恰好两项为真：')
for chosen, probability in exact_two.items():
    print(' ', tuple(i+1 for i in chosen), probability)
print('第1项为真的边际 =', sum(p for chosen,p in exact_two.items() if 0 in chosen))''')
md('''## 9. 重做原文三瓮例（p.405）

允许组合只有 WWB、WBW、WBB、RBW、RWB。颜色概率由本教程指定，允许组合逐字依据原例。我们枚举产品质量，删去不兼容组合，再归一化。原文红球公式也等价于这个计算。

先把第一瓮不可抽取的黑球移除，再将白/红概率同时重新归一化，结果不变；这是共同因子约去的结果，不是忽略概率归一化。''')
code('''urn = d.urn_example()
for state, probability in urn.items():
    print(''.join(state), probability)
print('红球概率 =', sum(p for state,p in urn.items() if state[0]=='R'))
assert sum(urn.values()) == 1''')
md('''## 10. 负控制：同样边际、同样支持，也能不同联合概率

考虑两个0/1事件，边际均为1/2，四种状态都可能。模型一四项各1/4；模型二的00/11各2/5、01/10各1/10。它们的 P(11) 不同。

因此，即使知道所有禁止/允许组合和边际，通常仍不能由 p.405 的乘积规则唯一恢复未知依赖。正确的现代读法应保留“选择产品基准分布，再按约束条件化”的限定。''')
code('''independent = {(0,0):F(1,4), (0,1):F(1,4), (1,0):F(1,4), (1,1):F(1,4)}
correlated = {(0,0):F(2,5), (0,1):F(1,10), (1,0):F(1,10), (1,1):F(2,5)}
for name, law in [('独立',independent), ('相关',correlated)]:
    marginals = [sum(p for s,p in law.items() if s[i]) for i in range(2)]
    print(name, '边际 =', list(map(str,marginals)), 'P(11) =', law[1,1],
          'P(至少一个) =', sum(p for s,p in law.items() if any(s)))
assert set(independent) == set(correlated)''')
md('''## 11. Addition：七种关系与表格方向（pp.407–408）

D=相等；D_sub=真包含于；D_super=真包含；C=互补；C_sub=不交且不覆盖；C_super=相交且覆盖；P=四个Venn区域都非空。它们不是八命题的改名，而是八命题的完整组合。

原表的前提方向是 X:Y 与 Z:Y，结论是 X:Z。括号表示被排除的关系，不是可能结果。下面生成全部八个 X/Y/Z 原子区域的256种有/无占据模型，其中193种满足三项及补集非空；每个已占区域只放一个代表。''')
code('''table, occupancy_count = d.composition_from_atoms()
print('合格占据模型数：', occupancy_count)
for pair in [('D_sub','D_sub'), ('C_super','C_sub'), ('P','D'), ('P','P')]:
    print('X:Y=%s，Z:Y=%s -> X:Z 可能为' % pair, ', '.join(sorted(table[pair])))
assert table['C_super','C_sub'] == {'D_super'}
print('第一例正好排除 C 和 C_super，与印表括号一致')''')
md('''### 分类计数与现代化简的界限（pp.388–392）

原文64个前提对中32个有结论，再删6个，保留26个有向形式，即12对+2个单式，共14个对换类。

我们的明确模型也得到32个有结论，但若把所有“非空 proper term”带来的语义弱化都允许使用，会再删去原文保留的 AA 与 ee：A 蕴涵 i，所以 AA→i 可弱化为 Ai→i；e 蕴涵 O，所以 ee→I 可弱化为 Oe→I。于是该现代准则得到24/12。两种计数必须分开报告；不能把后一准则冒充原文的归约规则，也不能声称历史26/14已由这一算法复现。''')
code('''census = d.syllogism_census()
print('前提对：', census['premise_pairs'], '；有结论：', census['concluding_pairs'])
print('允许全部语义弱化后：', census['minimal_directed'], '有向 /', census['counterpart_classes'], '对换类')
print('该准则删去：', ', '.join(census['redundant_pairs']))
print('原文报告：26 有向 / 14 对换类，保留 AA 与 ee')''')
md('''## 12. 练习：两种“相同证词”是否应得到相同答案？

两份证词的单独参数都为3/4。情形一：模型先取独立旗标，再观察它们一致。情形二：两旗标总是完全相同，只是同一信息的复制。

先预测两个合并概率，再运行答案。说明为何这个区别不能从“都是3/4”这句话看出来。''')
code('''product_model = d.joint_testimony([F(3,4),F(3,4)])
copied_law = {(False,False):F(1,4), (True,True):F(3,4)}
copied_model = copied_law[True,True] / sum(copied_law.values())
print('产品 + 一致性条件化：', product_model)
print('完全复制，已必然一致：', copied_model)
assert product_model == F(9,10) and copied_model == F(3,4)
print('答案：边际只给单项概率，没有指定联合分布或证据是否新增。')''')
md('''## 13. 如何检验本教程？

执行 `python -m unittest discover -v`。测试含独立逐对象量词 oracle、24表达归并、退化反例、21,844个交集检查与203组紧界、36个原表格、29,968个标号三项模型、三个概率公式对条件化枚举、p.401闭式对数值积分，以及故意不成立的依赖/印式对照。

**验证边界：** 测试通过不等于原论文本身的所有命题都对，也不等于一般定理证明。八区域占据方法只保留区域是否为空，不保留基数、比例或无穷结构；不能用它代替数量问题。概率实验检查已声明的模型，不替真实证词建立可校准性。

**可选延伸：** 自己给四种状态指定另一个同边际联合分布；或者改变连续区间抽样规则，观察数值如何变。修改模型时先说明新机制，再改公式。''')
code('''import unittest
suite = unittest.defaultTestLoader.discover('tests')
result = unittest.TextTestRunner(verbosity=1).run(suite)
assert result.wasSuccessful()
print('实际测试方法数：', result.testsRun)''')

doc['cells']=cells
doc['metadata'].pop('execution_note',None)
doc['metadata']['kernelspec']={'display_name':'Python 3','language':'python','name':'python3'}
doc['metadata']['language_info']={'name':'python','version':'3.10+'}
doc['metadata']['reconstruction']={'historical_source':'De Morgan 1847, printed pp.379-408',
                                  'dependencies':'Python standard library only',
                                  'scaffold':'installed jupyter-notebook tutorial template'}
path.write_text(json.dumps(doc,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
print(f'Built tutorial: {len(cells)} total cells, {sum(c["cell_type"]=="code" for c in cells)} code cells.')
