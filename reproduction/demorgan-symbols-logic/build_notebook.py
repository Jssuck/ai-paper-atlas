"""Fill the tutorial scaffold made by the installed official notebook helper.

Retains the scaffold format/version/metadata, builds deterministic cell IDs,
and clears outputs. Run execute_notebook.py afterward for real output.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
path=ROOT/'tutorial.ipynb'
doc=json.loads(path.read_text(encoding='utf-8'))
cells=[]

def add(kind,text):
    cell={'cell_type':kind,'id':f'demorgan-{len(cells)+1:03d}','metadata':{},
          'source':text.strip().splitlines(keepends=True)}
    if kind=='code': cell.update(execution_count=None,outputs=[])
    cells.append(cell)


def md(text): add('markdown',text)
def code(text): add('code',text)

md('''# De Morgan 1851：从符号到关系与证言

**中文教学重构，不是历史软件，也不是全文形式化证明。** 对应第二篇 memoir，原印页79–127；1850年2月25日宣读，卷IX第一部分1851年印行。本文使用原创的有限集合、二元关系与精确有理数程序。

**读者**：会基础 Python，了解集合、全称/存在量词与条件概率。**目标**：区分符号规则与语义假设；把 copula 的合成变成可执行操作；识别证言概率对误报机制及独立性的依赖。

路线：①括号符号与32/36式；②关系合成与数量；③报告矩阵与证言；④负控制、练习和复现边界。

所有代码只用标准库。交付输出由全新共享命名空间中的 CPython `exec` 顺序执行获得，**不是 Jupyter kernel 执行**。在已有 Jupyter 环境可重启内核后 Run All。运行陌生 notebook 前先审阅代码。''')
code('''from fractions import Fraction as F
from itertools import product
import platform
import demorgan as d
print('Python:', platform.python_version())
print('精确概率示例:', F(1, 3) + F(1, 6))''')
md('''## 1. 符号为什么不只是缩写？（pp.86–94）

括号曲率记录左右项的量；负点只保留奇偶性。`))` 表示 X⊆Y，`() `表示交集非空。本文的 contrary 系统中 `)(` 表示两项之外尚有对象，而 `(.)` 表示两项覆盖论域。

这里的 Python 判定采用现代有限集合语义；全称式自身不带存在承诺。原文有效性规则所需的非空项及非空补项会在后面单列。''')
code('''U, X, Y = {0, 1, 2, 3}, {0}, {0, 1}
for p in d.FORMS:
    print(f'{str(p):3} 全称={str(p.universal):5} 真值={p.holds(U,X,Y)}')''')
md('''### 补项变换与命题否定不是同一操作（p.92）

把 X 换成补项 x，同时反转 X 一侧括号并增减一个负点，保持原命题意义。把两侧量与负点一起反转，得到矛盾命题。补集必须始终相对同一个 U。''')
code('''p = d.Proposition.parse('))')
q = p.contrary_term('left')
r = p.contradictory()
print('同义变形:', p, '→', q, p.holds(U,X,Y), q.holds(U,U-X,Y))
print('矛盾命题:', r, r.holds(U,X,Y))
assert p.holds(U,X,Y) == q.holds(U,U-X,Y)
assert p.holds(U,X,Y) != r.holds(U,X,Y)''')
md('''### 删中项规则与32式（pp.94–95）

按 XY、YZ、XZ 排列；若规则允许推论，就删去两枚中项括号，再把负点按奇偶性合并。程序实现 p.94 的文字规则，不把 p.95 的排印表当作无误的逐字 oracle。原图核对发现下半表右下角印作 `)) (.) = (.(`，按规则与上半对应格应为 `).)`；测试保留此原印式的反例，不无声改写。

在 X、Y、Z 与各补项都非空时：8个全称式、16个通常特称式、8个加强前提后得特称的式。''')
code('''counts = {'全称': 0, '特称': 0, '加强': 0}
for p, q in product(d.FORMS, repeat=2):
    r = d.symbolic_inference(p, q)
    if r is not None:
        category = '全称' if r.universal else '加强' if p.universal and q.universal else '特称'
        counts[category] += 1
print(counts, '合计=', sum(counts.values()))
print('proper 原子占据模型数:', len(tuple(d.atom_models())))''')
md('''### 存在假设一删，答案就变（pp.91–94）

下例的中项为空。Y⊆X 与 Y⊆Z 都真，但不能推出 X∩Z 非空。全套测试枚举256种原子占据模式；取消非空 proper 条件后，32个指定推论只剩24个始终成立。

这不是修正原文的32，而是更换语义域后得到的对照。''')
code('''u, x, y, z = {0,1}, {0}, set(), {1}
p, q = d.Proposition.parse('(('), d.Proposition.parse('))')
r = d.symbolic_inference(p,q)
print('前提:', p.holds(u,x,y), q.holds(u,y,z), '结论', r, ':', r.holds(u,x,z))
assert not r.holds(u,x,z)''')
md('''## 2. 同样的括号，可能是另一个系统（pp.99–103）

exemplar 系统的 `)(` 是任取一个 X 与任取一个 Y 都在 copula 关系中。copula 为恒等时，它要求两项都是同一个单元素类；不能只用 X=Y 代替。

**量词次序很关键。** 肯定混合量按 ∀∃ 读，否定式取其完整对偶 ∃∀；不是从左到右机械地读。`((` 在恒等关系下是“对每个 Y，可选到相同的 X”，即 Y⊆X。程序把这种选择约定公开写在 `exemplar_holds` 中。''')
code('''p = d.Proposition.parse(')(')
print('相同的复数集合:', d.exemplar_holds(p,{0,1},{0,1}))
print('同一单元素类:', d.exemplar_holds(p,{0},{0}))
exemplar_count = common_count = 0
for p,q in product(d.FORMS,repeat=2):
    e = d.exemplar_inference(p,q)
    if e is not None:
        exemplar_count += 1
        common_count += d.symbolic_inference(p,q) == e
print('exemplar 规则许可:', exemplar_count, '与另一系统共有的符号式:', common_count)''')
md('''全套测试为每个三项成员原子保留0、1、2个对象，共6561种重数模式，其中6342种使三项都非空。保留两个对象是为了发现“同一类”不等于“同一个体”的区别。测试得到36式与21个共有符号式（pp.101–103）。这是指定语义的模型核查，不是全文一般证明。

## 3. copula 可以合成，不必都叫“是”（pp.108–111；Addition pp.126–127）

把关系写成有序对：John 可说服 Thomas，Thomas 可命令 William，推出 John 与 William 有复合关系。原文允许把复合关系包含在更宽的“control”中；程序直接计算最小复合关系 R;S。不能把结果直接归回 R 或 S。''')
code('''persuade = {('John','Thomas')}
command = {('Thomas','William')}
control = d.compose(persuade,command)
print('说服后命令:', sorted(control))
print('直接说服？', ('John','William') in persuade)
print('直接命令？', ('John','William') in command)
assert ('John','William') in control''')
md('''### 逆关系、可换性、传递性要分开（pp.104–109）

父亲/子女一类关系方向可逆，但原关系通常不等于逆关系。任意 R 都有 R⁻¹，不代表 R 自己对称。R 有传递性时，R⁻¹也有传递性（p.114）。数学例子使用显式边，不把自然语言“朋友”“兄弟”等词的法律当作已经证明。''')
code('''R = {(0,1),(1,2),(0,2)}
print('R传递:', d.transitive(R), 'R对称:', d.symmetric(R))
print('逆关系也传递:', d.transitive(d.converse(R)))
assert d.converse(control) == d.compose(d.converse(command),d.converse(persuade))
print('逆序合成恒等式通过')''')
md('''### 复合项的单调性（p.85）

“每个人都是动物”能推出“人的头都是动物的头”。现代重构把“某类的头”解释为：与该类某对象有 head-of 关系的对象。这是关系的逆像运算；不要求 head-of 本身具有传递性。''')
code('''head_of = {('h1','person1'),('h2','dog1')}
people, animals = {'person1'}, {'person1','dog1'}
heads_people = d.relational_term(head_of,people)
heads_animals = d.relational_term(head_of,animals)
print('人的头:', sorted(heads_people), '动物的头:', sorted(heads_animals))
assert heads_people <= heads_animals''')
md('''## 4. 每个对应某个，还是每个对应每个？（pp.112–113）

双方都被覆盖只需要一组匹配；exemplar 的双全称要求全部笛卡尔积。原文以10×10个对象说明10个 agreement 与100个 agreement 的差别。下例缩小为2×2。''')
code('''subjects, predicates = {0,1}, {2,3}
matching = {(0,2),(1,3)}
print('两个方向都覆盖:', d.all_some(matching,subjects,predicates) and
      d.all_some(d.converse(matching),predicates,subjects))
print('每个对应每个:', d.all_all(matching,subjects,predicates))
print('完整关系需要边数:', len(set(product(subjects,predicates))))''')
md('''### 一个可检验的数量下界（p.112括注）

设有 a 个源、b 个目标、E 条关系边。没有被所有源共同关联的目标至多承受 a−1 条边。因此共有目标数至少 max(0, E−(a−1)b)。

若已知 m 个源每个至少 n 条边，可代 E≥mn；原文正是从这种计数出发。程序验证到3×3的全部682个二部关系，并检验每个给定边数都可达到下界。''')
code('''a,b,E = 3,5,12
print('共有目标数至少:', d.common_target_lower_bound(a,b,E))
# 两个共有目标各3边，另三个各2边，恰好达到2。
edges = {(x,y) for x in range(a) for y in range(b) if y<2 or x<2}
common = [y for y in range(b) if all((x,y) in edges for x in range(a))]
print('边数:', len(edges), '共有目标:', common)
assert len(common) == d.common_target_lower_bound(a,b,len(edges))''')
md('''### 不把修订段落读成无限制的关系公理（pp.114–116）

1850年7月1日替换的方括号段，讨论特定的总关联、补项、不得混接等条件。任意二元关系并不自动满足这些条件。下面一个源同时连到 Y 与 y，因此不能把“连到 Y”直接当作“不连到 y”。本项目不声称复现修订段的全套带上下标系统。''')
code('''R = {(0,1),(0,2)}
print('连到Y:', d.all_some(R,{0},{1}), '也连到y:', d.all_some(R,{0},{2}))
print('一般关系不自动满足补项排斥条件。')''')
md('''## 5. 证人的可靠性是一张条件概率表（pp.120–121）

原文 p_q = P(报告 p | 实际 q)。代码将下标转置为 C[q][p]，即**行是真实事件、列是报告**，每行和为1。先验 v_q 给出实际事件的概率。

收到报告 k 后，后验的每一项为 v_q C[q][k] / Σ_s v_s C[s][k]。原文的 particular credibility 是后验第 k 项；事前总体正确率是 Σ_s v_s C[s][s]，一般不能混为同一量。

p.120还有限定“如果他作任何陈述”。本例把报告列满；若只有发言者被观察，且发言概率随真实事件变化，还需加入沉默输出或发言选择似然，不能忽略选择过程。''')
code('''prior = (F(1,10),F(3,10),F(6,10))
C = ((F(9,10),F(1,20),F(1,20)),
     (F(1,5),F(7,10),F(1,10)),
     (F(1,10),F(1,10),F(4,5)))
print('报告0之后:', tuple(map(str,d.posterior(prior,C,0))))
print('事前总体正确率:', d.general_credibility(prior,C))
print('各报告事前概率:', tuple(map(str,d.report_distribution(prior,C))))''')
md('''### 52张具名卡与二元白/黑模型（pp.118–121）

都取先验1/52、一般准确率9/10，但错误怎样落在“目标”上不同。

- 52种名称：错误均摊给其余51个名字，错报目标概率为(1−μ)/51。
- 二元模型：错误只能落到另一个标签，错报目标概率为1−μ。

这两个模型回答不同的问题；不是贝叶斯定理自相矛盾。''')
code('''n,mu = 52,F(9,10)
uniform = (F(1,n),)*n
cards = d.symmetric_channel(n,mu)
card_credit = d.posterior(uniform,cards,0)[0]
binary_prior = (F(1,n),F(n-1,n))
binary_credit = d.posterior(binary_prior,d.symmetric_channel(2,mu),0)[0]
print('具名卡后验:',card_credit,'；二元误报模型后验:',binary_credit)''')
md('''### 负控制：忠实地合并标签并不改变结论

保持同一联合分布，把其余51种事件与报告聚成“其他”，其错报目标概率仍应是1/510，而非1/10。`aggregate_model` 以原先验加权各条件行；这是现代审计工具，不是原文声称的算法。''')
code('''groups = ((0,),tuple(range(1,n)))
grouped_prior,grouped_channel = d.aggregate_model(uniform,cards,groups,groups)
print('聚合后其他→目标的概率:',grouped_channel[1][0])
print('聚合后后验:',d.posterior(grouped_prior,grouped_channel,0)[0])
assert d.posterior(grouped_prior,grouped_channel,0)[0] == card_credit''')
md('''## 6. 偏误能使证言完全没有信息（pp.123–124）

设 λ 是接收者推测的证人心中各事件概率。正确概率为 a_q，误报按 λ_p/(1−λ_q) 分配。若 a_q=λ_q，所有实际事件对应同一报告分布 λ，证言完全独立于真实事件，后验等于先验。''')
code('''beliefs = (F(1,5),F(3,10),F(1,2))
no_information = d.biased_channel(beliefs,beliefs)
print('各条件行相同:',len(set(no_information)) == 1)
print('报告0后:',tuple(map(str,d.posterior(prior,no_information,0))))
assert d.posterior(prior,no_information,0) == prior''')
md('''### “否认事件k”还需要规定报告协议（p.123）

本实现对齐原式的 1−C[q][k]：观察到的是“报告不是k”。若证人另被问一个是/否问题，其回答机制可能不同，不能无声套用同一似然。''')
code('''print('观察报告不是0后的分布:',tuple(map(str,d.denial_posterior(prior,C,0))))
assert sum(d.denial_posterior(prior,C,0)) == 1''')
md('''## 7. 判断错误与有意改说是两层（p.124）

J[q][b]：实际 q 时相信 b；S[b][r]：相信 b 时报告 r。总通道 C=JS。该结构假定给定信念后，报告过程不再额外依赖真实事件；这就是代码公开采用的 Markov 条件。

均匀先验、两层误报均匀时，最终正确率为 pr+(1−p)(1−r)/(n−1)。第二项是两次错误恰好抵消的贡献。''')
code('''n,p,r = 4,F(3,4),F(4,5)
J,S = d.symmetric_channel(n,p),d.symmetric_channel(n,r)
combined = d.compose_channels(J,S)
actual = d.posterior((F(1,n),)*n,combined,0)[0]
formula = p*r+(1-p)*(1-r)/(n-1)
print('矩阵:',actual,'闭式:',formula,'两错抵消项:',(1-p)*(1-r)/(n-1))
assert actual == formula''')
md('''### 定向虚报（p.125）

若判断本身无误，实际目标总会报告目标；实际为其他事件时，以 κ 的概率改报目标。后验为 v/[(1−κ)v+κ]。在这个模型中，虚报倾向从0增到1，证言由完美识别逐渐退化为完全没信息。''')
code('''v=F(1,52)
for kappa in (F(0),F(1,10),F(1,2),F(1)):
    T=d.targeted_statement_channel(2,0,kappa)
    print('κ=',kappa,'后验=',d.posterior((v,1-v),T,0)[0])''')
md('''## 8. 两个人说同样的话，不必是两份独立证据（p.125）

原文多证人的乘积在现代概率语义中需要**给定真实事件的条件独立性**。两个独立9/10准确证人、先验1/2，一致报告目标时得81/82。若第二人完整转述第一人，只是重复同一个信号，后验仍9/10。

程序不从“有两个证人”推断独立性；相关证言应直接提供联合报告似然。''')
code('''prior_two=(F(1,2),)*2
accurate=d.symmetric_channel(2,F(9,10))
independent=d.multiple_witnesses(prior_two,(accurate,accurate),(0,0))[0]
copying=d.condition(prior_two,(F(9,10),F(1,10)))[0]
print('独立:',independent,'完全转述:',copying)
assert independent > copying''')
md('''## 9. 练习与答案

练习1：固定 μ=1/2。把 n 从2增至100，但始终给目标固定先验1/10，后验怎样变化？若改为均匀先验1/n，又怎样？这对应 p.121 的大n讨论；必须说清哪个量保持固定。先做预测，再运行下一单元。''')
code('''for n in (2,10,100):
    fixed=d.symmetric_credibility(F(1,10),n,F(1,2))
    uniform_case=d.symmetric_credibility(F(1,n),n,F(1,2))
    print('n=',n,'固定先验1/10:',fixed,'均匀先验1/n:',uniform_case)
print('答案：固定目标先验时后验趋近1；均匀先验时始终等于1/2。')''')
md('''练习2：如果模型认为某报告绝不可能出现，应该把后验设成0、1/2，还是报错？试试一个只会报告0的通道，却观察到报告1。

答案：归一化分母为0，原模型没有定义这个后验。先审查模型、事件列表或观察，而不是编造数值。''')
code('''try:
    d.posterior((F(1,2),)*2,((F(1),F(0)),(F(1),F(0))),1)
except ValueError as error:
    print('正确拒绝:',error)''')
md('''## 10. 怎样继续验证？

本目录运行 `python run_checks.py`：执行21个主测试、demo、全部 notebook 单元、受限结构/输出检查；保存真实日志与 SHA256SUMS。每项实际命令、退出码、耗时记录在 evidence 中，环境记录不包含用户名、主机名、HOME或环境变量。

阅读 [README.md](README.md) 的完整复现边界与 [SOURCE_LEDGER.md](SOURCE_LEDGER.md) 的原文页码/函数映射。可选扩展：为相关证人构造一个联合报告通道，比较复制概率从0到1的后验变化。

**不覆盖**：原文全部历史优先权论辩、Hamilton cumular 的全部变式、pp.114–116 带相关符号的全系统、自然语言推理自动解析、真实证人校准或心理学实验。有限枚举检查所列模型，不能取代这些工作的独立论证。''')
doc['cells']=cells
doc['metadata']['kernelspec']={'display_name':'Python 3','language':'python','name':'python3'}
doc['metadata']['language_info']={'name':'python'}
doc['metadata']['scaffold_note']='Initialized using installed official jupyter-notebook skill scripts/new_notebook.py --kind tutorial; filled with original project content.'
doc['metadata'].pop('execution_note',None)
path.write_text(json.dumps(doc,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
print(f'Built {len(cells)} cells ({sum(c["cell_type"]=="code" for c in cells)} code); outputs cleared.')
