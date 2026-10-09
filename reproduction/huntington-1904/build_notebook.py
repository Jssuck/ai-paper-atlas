"""Fill the tutorial scaffold reproducibly; preserves the nbformat envelope."""
import json
from pathlib import Path

path=Path(__file__).with_name('tutorial.zh-CN.ipynb')
nb=json.loads(path.read_text(encoding='utf-8'))
cells=[]
def md(text):
    cells.append({'cell_type':'markdown','metadata':{},'source':text.splitlines(keepends=True)})
def code(text):
    cells.append({'cell_type':'code','metadata':{},'source':text.splitlines(keepends=True),'execution_count':None,'outputs':[]})
md('''# Huntington 1904：三组公设与独立性反模型

对象：会读Python函数、循环和简单真值表的读者。无需机器学习、群论或定理证明器背景。

目标：区分运算与关系语言；理解“满足其余条件而恰好违反一条”；保留原文的条件与封闭性；知道有限实验能说明什么、不能说明什么。

路线：1. 两元素正例 → 2. 原文23个有限反模型 → 3. 条件守卫 → 4. 14元素例子 → 5. 多值补元 → 6. 三种语言互相恢复 → 7. 有界枚举 → 8. 教学改编 → 9. 练习。

这是原创教学实现，原论文没有软件。所有保留输出由Python标准库顺序执行器生成，不是Jupyter/IPython kernel执行。先从本目录运行；不需要安装包或联网。
''')
code('''from huntington import (
    first, second, third, failed, first_original_models, second_original_models,
    third_original_models, powerset_algebra, induced_relation,
    relation_complements, operation_complements, fourteen_domain, mask_label,
    small_enumeration, teaching_saturated_addition,
)
model = powerset_algebra(1)
print('K =', model.elements)
print('plus table =', list(model.operations['+'].values()))
print('times table =', list(model.operations['*'].values()))
print('Failed:', failed(first(model)), failed(second(induced_relation(model))), failed(third(model)))
''')
md('''## 1. 独立性不是“每条看起来都重要”

一个反模型要使目标公设为假，其余保留公设全部为真。下面按扫描逐格转录的23个有限结构分别检查。§2的“6,7”例子同时否定两条；它服务于删去其中一条后的九条系统，不能称为显示的十条全独立。
''')
code('''for title, factory, check in [
    ('section 1', first_original_models, first),
    ('section 2', second_original_models, second),
    ('section 3', third_original_models, third),
]:
    print(title)
    for label, m in factory().items():
        actual = failed(check(m))
        assert actual == label.split(',')
        print(' ', label, 'size', len(m.elements), 'fails', actual)
''')
md('''## 2. 不能预先把“封闭”写进类型

原文pp.289、292–293允许组合规则输出K之外的对象；Ia或Ib才提出封闭性。下面1+1输出outside，但outside并不是K的一员。

交换／分配／结合等式带有“所指中间项和最终项都在K内”的守卫。不满足守卫的赋值会跳过。跳过不是找到了一个等式反例，也不是证明了无条件等式。
''')
code('''m = first_original_models()['Ia']
print('K =', m.elements, '; 1+1 =', m.op('+', 1, 1))
for key, result in first(m).items():
    print(key, 'holds=', result.holds, 'checked=', result.checked, 'skipped=', result.skipped)
print('IIa model V:', first(first_original_models()['IIa'])['V'].note)
''')
md('''## 3. 14元素：缺少一个并集，不等于公设中所有东西都失效

把u0固定下标0略去，用4位编码自由下标1、2、3、4。缺少u014和u023，整数编码分别为9、6。

§2寻找“存在于K里的最小上界／最大下界”；§3 F直接要求并集输出也在K里。注意两种表述在没有封闭性时的区别。
''')
code('''print('Domain labels:', [mask_label(a) for a in fourteen_domain()])
r = second_original_models()['6,7']
checks = second(r)
print('Full second list fails:', failed(checks))
print('Omit 6:', failed({k:v for k,v in checks.items() if k != '6'}))
print('Omit 7:', failed({k:v for k,v in checks.items() if k != '7'}))
m = third_original_models()['F']
print(mask_label(1), '+', mask_label(8), '=', mask_label(m.op('+',1,8)), '(outside K)')
print('Third list fails:', failed(third(m)))
print('Conditional associativity: checked', third(m)['C'].checked, 'skipped', third(m)['C'].skipped)
''')
md('''## 4. 补元必须检查全部候选

五元素例子中，元素3有两个补元2和4。不能在验证9/H时只挑一个方便的补元。

原文§3 H的前提是A、D、E、G，扫描中的D容易被OCR误识别成B；补元上的横线也容易丢失。这里用原文的a=4、b=3、补元(b)=2明确展示失败。
''')
code('''r = second_original_models()['9']
print('Relation complements:', relation_complements(r,0,1))
m = third_original_models()['H']
print('Operation complements:', operation_complements(m,0,1))
a, b, bar_b = 4, 3, 2
print('a+bar_b =', m.op('+',a,bar_b), '; bar_b =', bar_b)
common = [x for x in m.elements if m.op('+',a,x)==a and m.op('+',b,x)==b]
print('Common lower elements:', common)
assert common == [0]
print('No nonzero witness; H holds =', third(m)['H'].holds)
''')
md('''## 5. 三种语言恢复同一个有限结构

在合法的幂集例子上，定义R(a,b)当且仅当a+b=b；从R可找补元和界；再用“两个补元之并的补元”恢复交。

这验证具体结构的定义转换，不能代替原文的一般推导。附录的一般结论是有限逻辑域有2^m个元素且每一阶在同构意义下唯一；只跑几个幂集不足以证明它。
''')
code('''for bits in range(1,5):
    m = powerset_algebra(bits)
    r = induced_relation(m)
    full = (1 << bits) - 1
    complements = relation_complements(r,0,full)
    mismatches = 0
    for a in m.elements:
        for b in m.elements:
            reconstructed = complements[complements[a][0] | complements[b][0]][0]
            mismatches += reconstructed != m.op('*',a,b)
    assert mismatches == 0
    print('size', len(m.elements), 'failed lists', failed(first(m)), failed(second(r)), failed(third(m)),
          'reconstruction mismatches', mismatches)
''')
md('''## 6. 完整枚举仍然有边界

枚举固定标签集合：§1 n≤2，§2 n≤3，§3 n≤3。不是抽样，也不按同构去重。§1枚举两张封闭表，数量是n^(2n²)；§3是一张表，n^(n²)；§2是关系表，2^(n²)。

运算表枚举已预设封闭，不能拿它研究封闭性条款独立性。n=2的两张合格表只是底与顶互换标签。n=3没有模型不等于证明所有非2的幂阶数都没有模型。
''')
code('''enumerated = small_enumeration()
for section, rows in enumerated.items():
    for row in rows:
        print(section, row)
''')
md('''## 7. 原例与教学重构必须分开

原文§3 A用非负整数加∞，普通加法且∞吸收；无限结构不能被有限循环穷举。D、E以及§2的4、5也使用无限的“所有有限整数集”类，有限截断会产生原来不存在的全局界。

下面是另行设计的有限教学例：K={0,1,2}，a+b=min(2,a+b)。它恰好只否定A，但不是原文的模型。README给出原文无限例子的数学说明，不把采样当证明。
''')
code('''modern = teaching_saturated_addition()
print('Modern saturated-addition table:')
for a in modern.elements:
    print([modern.op('+',a,b) for b in modern.elements])
print('Failed:', failed(third(modern)))
print('A witness: 1+1 =', modern.op('+',1,1), '!= 1')
print('H:', third(modern)['H'].note)
''')
md('''## 8. 练习：哪条前提被你悄悄加强了？

先预测：§2的1反例中，R(0,0)和R(1,1)为假。若你把4、5误写成现代“对所有元素都小于／大于”的界，会不会错误地让4、5也失败？

答案：会。原文4、5对a=底或a=顶有相等豁免。下面显示错误加强造成的额外失败。另一个练习：不要运行代码，手算§3 C中的(2+4)+3与2+(4+3)，应分别为3和1。
''')
code('''m = second_original_models()['1']
print('Original bounds hold:', second(m)['4'].holds, second(m)['5'].holds)
wrong_bottoms = [z for z in m.elements if all(m.le(z,a) for a in m.elements)]
wrong_tops = [u for u in m.elements if all(m.le(a,u) for a in m.elements)]
print('Incorrectly strengthened bottom/top candidates:', wrong_bottoms, wrong_tops)
assert not wrong_bottoms and not wrong_tops
m = third_original_models()['C']
f = lambda a,b: m.op('+',a,b)
print('(2+4)+3 =', f(f(2,4),3), '; 2+(4+3) =', f(2,f(4,3)))
''')
md('''## 下一步与限制

查看 `results/experiments.json` 中每条条件的失败见证与跳过次数；用 `python -m unittest -v` 重跑22项测试。建议先尝试单格改表，看失败条款如何变化，不要直接扩展到天文数量的高阶枚举。

这里没有训练过程、准确率排行榜或现代AI性能结论。代码也没有自动验证原文全文所有证明。一个具体反模型可反驳“这条由其余推出”；某个有限搜索范围内找不到反模型，则不能据此证明可推出。
''')
for i,c in enumerate(cells): c['id']=f'huntington-{i:02d}'
nb['cells']=cells
nb.setdefault('metadata',{})['language_info']={'name':'python','version':'3.10+'}
nb['metadata']['kernelspec']={'display_name':'Python 3','language':'python','name':'python3'}
nb['metadata'].pop('execution_provenance',None)
path.write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Wrote {path.name}: {sum(c["cell_type"]=="code" for c in cells)} code cells')
