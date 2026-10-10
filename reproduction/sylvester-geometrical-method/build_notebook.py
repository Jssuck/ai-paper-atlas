"""Build the original Chinese tutorial notebook."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
cells=[]

def md(source):
    cells.append({'cell_type':'markdown','id':f'md-{len(cells):02d}',
                  'metadata':{},'source':source.strip().splitlines(keepends=True)})

def code(source):
    cells.append({'cell_type':'code','id':f'code-{len(cells):02d}',
                  'metadata':{},'execution_count':None,'outputs':[],
                  'source':source.strip().splitlines(keepends=True)})

md(r'''
# Sylvester 1852：几何证明、可容许域与计算核查

面向了解高中三角函数、基本代数和 Python 的读者。读完后应能区分：原式与校核式、带符号参数与普通长度、有限实验与全域证明。

原文：J. J. Sylvester，*Philosophical Magazine*，series 4，vol. 4，1852 年 11 月，pp. 366–369；[DOI](https://doi.org/10.1080/14786445208647142)。作者署日 1852-10-04，不作为确证出版日。

本笔记是原创现代重建，不宣称复刻所有历史几何证明。没有嵌入来源扫描或 OCR 全文。讨论的普遍“证明方法猜想”没有被这些实验解决。

路径：1. 有向几何 → 2. n=2 全域因式分解 → 3. 退化边界 → 4. 半整数式校核 → 5. 抽样的局限 → 6. 弦段正根。
''')
md('''
## 运行说明

本次保存输出由 CPython 顺序执行代码单元产生，不是 Jupyter 内核执行。运行只用标准库；`validate_notebook.py --execute` 可重新生成相同的代码输出。结构验证是自带的基础验证，不冒称官方 nbformat 全量验证。

从本目录启动笔记本或普通 Python 运行器。代码不访问网络、不调用模型、不下载资料。大多数输出是示例数值；精确多项式证书另用整数运算。
''')
code('''
from pathlib import Path
import math
from sylvester import (
    Triangle, DomainError, DegenerateIntersection, divider_geometry,
    sine_residual, cross_residual, tangent_ratios, parameters,
    bisector_squares, factored_bisector_difference,
    near_segment, remote_segment, circle_chord, opposite_sign_example, exact_opposite_sign_example,
)
from polynomial_certificate import certificate
from reproduce import finite_sweeps, main as regenerate_outputs
assert Path("sylvester.py").exists(), "请从本复现目录启动"
print("标准库重建：接口角度为度，内部三角计算为弧度。")
''')
md(r'''
## 1. 正弦式到底编码哪一种长度？

要求 $A,B>0$、$A+B<\pi$、$c=AB>0$、$n\ne0$。取 $A=2n\alpha$、$B=2n\beta$，以及 $\theta=A/n$、$\phi=B/n$。

置 $A=(0,0)$、$B=(c,0)$。从 A 出发的方向为 $(\cos\theta,\sin\theta)$，从 B 出发的方向为 $(-\cos\phi,\sin\phi)$。与对边支撑直线相交的带符号参数是

$$t_A=\frac{c\sin B}{\sin(B+A/n)},\qquad t_B=\frac{c\sin A}{\sin(A+B/n)}.$$

分母必须非零。原 p. 367 的正弦比式在交点存在时等价于 $t_A=t_B$。普通长度则是 $|t_A|,|t_B|$；其等长还有 $t_A=-t_B$ 一支。两条所选正向射线都命中，另需两个参数都为正；内部劈线还要求交点位于对边开线段内部。
''')
code('''
g = divider_geometry(Triangle(50, 70), 2)
print(f"n=2: t_A={g.t_A:.9f}, t_B={g.t_B:.9f}")
print("两条正向射线:", g.both_forward_rays)
print("两条内部劈线:", g.both_internal_cevians)
print("原正弦式残差:", round(sine_residual(g.triangle, g.n), 9))
''')
md(r'''
## 2. n=2：从数值核查走到全域论证

令 $a=BC$、$b=CA$、$c=AB$，三边均为正并满足严格三角不等式。内部角平分线平方为

$$\ell_A^2=bc\left(1-\frac{a^2}{(b+c)^2}\right),\quad\ell_B^2=ac\left(1-\frac{b^2}{(a+c)^2}\right).$$

通分后可因式分解成

$$\ell_A^2-\ell_B^2=\frac{(b-a)c(a+b+c)P}{(a+c)^2(b+c)^2},$$

$$P=a^2b+ab^2+3abc+ac^2+bc^2+c^3.$$

下面比较通分后两端多项式的**全部整数系数**，不只代入若干三角形。
''')
code('''
cert = certificate()
print("精确多项式证书:", cert)
assert cert["identity_verified"]
for sides in [(3,4,5), (4,3,5), (4,4,5)]:
    x,y = bisector_squares(*sides)
    factor = factored_bisector_difference(*sides)
    print(sides, "平方差 =", round(x-y,10), "因式式 =", round(factor,10))
''')
md(r'''
对于任意满足上述域条件的三角形，$P,c,a+b+c$ 及分母均严格为正。因此平方差的符号就是 $b-a$ 的符号；特别有

$$\ell_A=\ell_B\iff\ell_A^2=\ell_B^2\iff a=b.$$

这是全域的现代代数论证。准确地说，系数证书核查恒等式，正性与几何域分析完成推论。40 个单元测试中的 4,010 个精确整数三角形代入只是额外实现检查。

它没有形式化历史术语“纯几何”“直接证明”及“所有可能的证明”，故不能仅凭这一实现宣布原文的普遍证明方法猜想已经解决。
''')
md(r'''
## 3. 端点、平行线与被除掉的等腰解

- $n=0$ 无定义。
- $n=1$ 时 D、E 都是 C，已不是两条内部劈线。
- $n=-1$、$A=B$ 时正弦式为 $0=0$，但交点退化为平行线。
- $A=B$ 会使正切比的一项成为 $0/0$；不能因此删除等腰解。
- 分角方向绕转、延长线、正切极点与数值近退化，都需要另外检查。

下面有意触发两次域错误。捕获这些预期错误属于测试，不是静默失败。
''')
code('''
g1 = divider_geometry(Triangle(40,60), 1)
print("n=1 的两个交点都是 C:",
      all(math.isclose(p[i],g1.triangle.C[i],abs_tol=1e-12)
          for p in (g1.D,g1.E) for i in (0,1)))
print("n=-1、等腰时的正弦残差:", sine_residual(Triangle(50,50),-1))
for label, operation in [
    ("平行交点", lambda: divider_geometry(Triangle(50,50),-1)),
    ("等腰正切比", lambda: tangent_ratios(Triangle(50,50),2)),
]:
    try:
        operation()
    except DomainError as error:
        print(label, "→", type(error).__name__)
''')
md(r'''
## 4. p. 368：可见字形不等于校核后的公式

从 p. 367 正切式代入 $n=1/2$ 与 $n=-1/2$，在每项有定义时应得到

$$\frac{\tan(3(\alpha+\beta)/2)}{\tan((\alpha+\beta)/2)}=-1,$$

$$\frac{\tan(3(\alpha-\beta)/2)}{\tan((\alpha-\beta)/2)}=-1.$$

扫描中两个右端可辨为 `=1`，第二分子可辨为 `(3α−β)/2`，未清楚显示 `3(α−β)/2` 的分组。这里保留字形与重建式的区别，不推断差异由哪一个历史制作环节造成。

优先回到正弦式验证实例：$n=1/2,A=30^\circ,B=60^\circ$；$n=-1/2,A=15^\circ,B=105^\circ$。两例都不等腰。
''')
code('''
for A,B,n in [(30,60,.5),(15,105,-.5)]:
    g = divider_geometry(Triangle(A,B), n)
    ratios = tangent_ratios(g.triangle,n)
    print(f"n={n:+g}, A={A}, B={B}: t_A={g.t_A:.9f}, t_B={g.t_B:.9f}")
    print("  正弦残差 =", round(sine_residual(g.triangle,n),12),
          "; 正切比 =", tuple(round(v,12) for v in ratios))
    print("  两条正向射线:",g.both_forward_rays,"; 内部劈线:",g.both_internal_cevians)
''')
md(r'''
令 $F_n=\sin(A+B/n)\sin B-\sin(B+A/n)\sin A$。积化和差直接给出

$$F_{1/2}=-\sin(2(A+B))\sin(A-B),$$
$$F_{-1/2}=\sin(2(A-B))\sin(A+B).$$

在三角形域且 $A\ne B$ 时，两个正弦方程分别给出 $A+B=90^\circ$ 和 $|A-B|=90^\circ$。这与原文紧随公式后的角条件一致。再检查交点分母与符号，就得到上面的可用实例。此步骤并未把所有正弦方程根自动认作内部劈线。
''')
md('''
## 5. 为什么粗网格不等于不存在证明？

以下扫描 8 个 n 值，各 595 个三角形。角度间隔 5°，每点用浮点容差 10⁻¹⁰ 判断相等。把退化交点分开计数，切勿把被拒绝的点解释为有效反例或有效等长。
''')
code('''
sweeps = finite_sweeps()
print("n | 点数 | 退化 | 非等腰带符号等长 | 非等腰普通等长")
for r in sweeps:
    print(f"{r['n']:4g} | {r['triangles_tested']:3d} | {r['degenerate_intersections']:3d} | "
          f"{r['signed_equal_nonisosceles']:3d} | {r['absolute_equal_nonisosceles']:3d}")
print("共",sum(r['triangles_tested'] for r in sweeps),"个样本；不能外推成普遍命题。")
''')
md(r'''
网格中 $n=-2$ 没出现非等腰普通等长，但定向求根会找到一个。它的参数异号，所以不是原正弦式编码的等长，也不是两条正向射线同时取到的交点。

还有无需求根的精确角度实例：$n=-2,A=96^\circ,B=24^\circ$，此时 $t_A=\sin24^\circ/\sin(-24^\circ)=-1$、$t_B=\sin96^\circ/\sin84^\circ=1$。下方图像采用此例；下面代码保留数值求根的独立补充。

这是对“带符号参数、射线与任意延长线段可以不加说明地互换”的反例；并未裁定原文所有可能的几何解读。
''')
code('''
extended = opposite_sign_example()
print(f"A=90°, B≈{extended.triangle.B_deg:.13f}°, n=-2")
print(f"t_A={extended.t_A:.13f}, t_B={extended.t_B:.13f}")
print("普通长度相等:",math.isclose(abs(extended.t_A),abs(extended.t_B),rel_tol=1e-12))
print("带符号相等:",math.isclose(extended.t_A,extended.t_B,rel_tol=1e-12))
print("两条正向射线:",extended.both_forward_rays)
''')
md('''
### 原创坐标图

蓝色表示 AD，橙色表示 BE，灰虚线表示对边延长线。最后一图的蓝虚线落在所选 A 射线的反方向。

![四种几何域](output/divider-domains.svg)

SVG 由 `reproduce.py` 的坐标生成，没有复制原扫描图。负二特例使用 A=96°、B=24° 的精确角度构造，坐标由浮点三角函数生成。独立审阅者已使用 Inkscape 栅格化并检查两幅图。
''')
md(r'''
## 6. 弧中点引弦：同一个方程的不同可容许根

设 P 是弧 UV 的中点，两弦从 P 引出。基弦 UV 把它们截成近段 $x$ 与远段 $a$，且 $b=PU=PV$。p. 369 给出

$$x^2+ax=b^2.$$

API 中 `half_chord` 表示半个给定圆弧所对的弦 b=PU=PV；不是基弦 UV 的一半。本图 b=1，而 UV/2=√3/2。

$a,b>0$ 时，两根一正一负。正根是近段长度的唯一代数候选；固定圆与固定基弦还可能给出额外的位置限制。下面取单位圆、基弦高度 $1/2$，方向为 ±30°，构成明确的合法例子。
''')
code('''
left,right = circle_chord(-30),circle_chord(30)
for name,g in [("左弦",left),("右弦",right)]:
    x,a,b=g['near'],g['remote'],g['half_chord']
    print(f"{name}: 近段x={x:.9f}, 远段a={a:.9f}, b={b:.1f}")
    print("  x(x+a) =",round(x*(x+a),12),"; 正根重建 =",round(near_segment(a,b),9))
print("远段相等:",math.isclose(left['remote'],right['remote']))
print("近段相等:",math.isclose(left['near'],right['near']))
''')
md(r'''
![弧中点的等远段与等近段](output/equal-chords.svg)

### 不依赖样本数量的正根唯一性

对 $x,y,a>0$，

$$(x^2+ax)-(y^2+ay)=(x-y)(x+y+a).$$

若左边为零，由 $x+y+a>0$ 得 $x=y$。这是一条完整的正实数域代数论证；它不是关于一切纯几何证明的穷举。

### 逆命题重置了符号

原文随后令给定近段为 $a$，远段为 $x$。方程是 $a(a+x)=b^2$，右端不是 OCR 可能误出的 0。因而 $x=(b^2-a^2)/a$，正远段要求 $0<a<b$。
''')
code('''
a,b = .6,1.0
x = remote_segment(a,b)
print("逆命题：给定近段a =",a,"，远段x =",round(x,9))
print("a(a+x) =",round(a*(a+x),12),"= b²")
for invalid_near in [0,1,2]:
    try:
        remote_segment(invalid_near,1)
    except DomainError:
        print("拒绝不符合正远段域的 a =",invalid_near)
''')
md('''
## 练习：相同角度换 n 后，还能直接比较长度吗？

试把 A=30°、B=60° 的 n 从 1/2 改为 −1/2。先计算分母，再决定是否存在有限交点。请不要只查看交叉相乘后的残差。

下面是答案脚手架及实际域检查。
''')
code('''
t = Triangle(30,60)
n = -.5
_,_,theta,phi = parameters(t,n)
print("两个交点分母:",round(math.sin(t.B+theta),12),round(math.sin(t.A+phi),12))
try:
    divider_geometry(t,n)
except DegenerateIntersection:
    print("答案：至少一个目标交点平行退化，不能读取两个有限长度。")
''')
md('''
## 重新检查并生成图像

这一格执行同一组单元测试，输出汇总；它不启动 Jupyter，也不使用网络。测试数和日志以真实执行为准。
''')
code('''
import io
import unittest
import test_sylvester
stream=io.StringIO()
suite=unittest.defaultTestLoader.loadTestsFromModule(test_sylvester)
result=unittest.TextTestRunner(stream=stream,verbosity=0).run(suite)
print(f"tests={result.testsRun}, failures={len(result.failures)}, errors={len(result.errors)}")
assert result.wasSuccessful(),stream.getvalue()
regenerate_outputs()
''')
md('''
## 结论与边界

1. 恒等式的精确系数证书与正性分析，支持 n=2 在全部非退化三角形中的结论。
2. p. 368 的校核必须回到 p. 367 的式子；可见字形、重建式和几何实例分开保存。
3. n=0、n=±1、等腰点、平行交点和正切极点不能在除法变形中消失。
4. 正根唯一性有全域解析论证；有限网格没有这种覆盖能力。
5. 本包没有证明所有 |n|>1 的一般命题，也没有用有限计算裁决原作者关于一切证明方法的猜想。

可进一步研究：为具体 n 建立完整的有向角与线段可容许域，再区分解析解集、射线解集和内部劈线解集。需要更强结论时，应给出新证明而非只加密网格。
''')

nb={'cells':cells,'metadata':{
    'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
    'language_info':{'name':'python','version':'3.12'},
    'reproduction':{'source':'Original tutorial content',
                    'execution':'Unexecuted until validate_notebook.py --execute',
                    'dependencies':'Python standard library only'}},
    'nbformat':4,'nbformat_minor':5}
(ROOT/'tutorial.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
print(f'Built tutorial.ipynb: {len(cells)} cells; {sum(c["cell_type"]=="code" for c in cells)} code cells.')
