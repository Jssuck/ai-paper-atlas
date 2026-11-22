# 欧几里得《几何原本》VI.30：怎样用「超出一个正方形」找黄金分点？

> AI 数学与形式推理前史补读。作品约公元前 300 年；实读 1908 / 2008 版。这里回填古典数学中的构造与证明，不把古代命题称为 AI 论文，也不声称穷尽早期文献。

## 1. 原典、问题与前后关系

- Euclid, *Elements*, VI.30。[Clay 希腊文与 Heath 英译](https://www.claymath.org/library/historical/euclid/files/elem.6.30.html)；T. L. Heath, *The Thirteen Books of Euclid’s Elements*, 卷 II（Cambridge University Press，1908），[正文、页影及校注入口](https://geometor.github.io/euclid/heath/volume_II/book_vi/propositions/30/)，印刷页 267–268；Richard Fitzpatrick, *Euclid’s Elements of Geometry*（2008 修订版），[希英对照 PDF](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=188)，页 188–189；[Joyce 教学读本](https://mathcs.clarku.edu/~djoyce/elements/bookVI/propVI30.html)。
- 输入仅是一条非零有限线段 AB。按[第六卷定义 3](https://mathcs.clarku.edu/~djoyce/elements/bookVI/defVI3.html)，把它分成较长段和较短段，使「全长 : 较长段」等于「较长段 : 较短段」。题目没有给定小数比值，也没有让人先画一个已知黄金比例的模板。主证通过调用 [VI.29](euclid-elements-vi29.zh-CN.md) **产生**所需长度，再用等面积矩形证明它满足定义。
- [II.11](https://mathcs.clarku.edu/~djoyce/elements/bookII/propII11.html) 已构造「全长乘短段等于长段平方」的分法。Heath 页 268 转述的异本另证由它和 [VI.17](https://mathcs.clarku.edu/~djoyce/elements/bookVI/propVI17.html) 直接得到比例；[XIII.17](https://mathcs.clarku.edu/~djoyce/elements/bookXIII/propXIII17.html) 则实际使用极中比切分。这些是文本联系，不是写作年代或作者归属的独立证据。

## 2. 图和对象：先沿 AC 作，不是沿 AB 作

下图是依据 Heath/Fitzpatrick 图的点位索引。补记 J 为左下角，不是传本新增点。两字母作为图形简称时指相对顶点；「BC 等于 CD」是面积相等，不是线段等长。

~~~text
C────────F────H
│        │    │
A────────E────B
│        │
J────────D
~~~

初始正方形 BC 的顶点为 A–B–H–C；贴入的矩形 CD 是 C–F–D–J；CE 是共用的 C–F–E–A；BF 是右上矩形 E–B–H–F；AD 是左下正方形 A–E–D–J。VI.29 的给定直线是 **AC**，从 C 向 A 贴，越过 A；它的目标面积是整个 BC，超出块是 AD。不是把两个已知面积相加作为 CD 的面积。

读本差异可具体定位：Joyce 正文第一个构造句将 CD 写成等于 BC 与 AD 之和，与其下一句的扣减逻辑冲突；Clay 希腊栏、Heath 印本和 Fitzpatrick 都是 CD 与 BC 等面积，另有 AD 同形的约束。Clay 的英译网页止于长短段比较，希腊栏及两部印刷本均有完成命题的收束。Heath 页 268 还记载某些传本在 FE＝AB 中插入 FE＝AC 的中间等量，并讨论 Heiberg 把 II.11 路线列到附录。本文不把校勘归属或网页更正写成正式勘误。

## 3. 重走原证：扣掉同一块，把面积变成比例

1. **先造出长度。** 用 [I.46](https://mathcs.clarku.edu/~djoyce/elements/bookI/propI46.html) 在 AB 上作正方形 BC；以 AC 为给定线，用 VI.29 作面积等于 BC 的 CD，朝 A 端超出一块与 BC 相似的 AD。与正方形相似的图形仍是正方形，所以 AD 的两边 AE、ED 等长。CD 与 BC 的布置如图，CD 的纵边是 FE＋ED，严格大于 AB。
2. **补明交叠不退化。** 原证按所示图形扣去 CE。为看清为何它真的只占左上部分：CD 与 BC 面积相等、纵边却比 BC 长，因此 CD 的横宽比 AB 短（也可用 VI.14）；宽为正，所以 E 严格落在 A、B 之间。这不是先接受目标比例再倒推 E 的位置。
3. **去共同部分。** 从 CD 与 BC 同时扣除 CE，得 AD 与 BF 等面积。两者也都为四个直角的图形。由 [VI.14](https://mathcs.clarku.edu/~djoyce/elements/bookVI/propVI14.html)，等面积等角的平行四边形，其相应角旁的两对边成反比例，具体是 FE : ED＝AE : EB。不要把 FE : ED 写成 EB : AE，也不要从等面积推出 BF 是正方形。
4. **转写到一条线上。** FE＝AB（原正方形的高度），ED＝AE（超出正方形）。代入得 AB : AE＝AE : EB；因 AB＞AE，由同一比值的大小关系得 AE＞EB（Fitzpatrick 显式标 [V.14](https://mathcs.clarku.edu/~djoyce/elements/bookV/propV14.html)）。现在满足定义，且长段确在 A 侧。原证给出了一个构造及核验，下面的实根分类是现代补充。

归因界线：主证的工作对象是线段、面积与比。Heath 的另证说明 Book II 已能取得相同的分点，但用的是另一条证明路线。不能用 II.11 的另证去替换 VI.29 那一步，再称重建了主证。

## 4. 教学重构：一个二次式，两种面积读法

设 $`L=AB>0`$，$`x=AE`$，$`y=EB=L-x`$。取 $`A=(0,0), B=(L,0), C=(0,L), H=(L,L)`$，则 $`E=(x,0), F=(x,L), D=(x,-x), J=(0,-x)`$。这里正交坐标只为把两份面积核算清楚：贴入矩形 CD 面积为 $`x(L+x)`$，与正方形 $`L^2`$ 相等；余下矩形 BF 面积为 $`Ly`$，等于超出正方形 $`x^2`$。一个等式来自整块约束，另一个来自去共同面积 $`Lx`$。

从 $`x(L+x)=L^2`$ 出发，把方程两边加上 $`L^2/4`$ 完成平方，对应 VI.29 先加半底基准面积。根号取正对应扩出后大块尺度为正。

$$
\left(x+\frac L2\right)^2=\frac{5L^2}{4},
\qquad x=\frac{\sqrt5-1}{2}L,\qquad y=\frac{3-\sqrt5}{2}L .
$$

这里 $`2<\sqrt5<3`$，直接给 $`L/2<x<L`$，因此 $`y`$ 正且比 $`x`$ 短。另一个代数根 $`-L(1+\sqrt5)/2`$ 为负；也可在非负域用 $`x(L+x)`$ 的严格递增证明唯一。**唯一的是长段在 A 侧时的分点**；若题目不固定哪端在长段一侧，镜像有另一个点，分段长度的无序对不变。

最后 $`Ly=x^2`$ 且 $`x,y>0`$，允许除法并得到书写顺序正确的比例：

$$
\frac{L}{x}=\frac{x}{y}=\frac{1+\sqrt5}{2}.
$$

一个逆向核验也很实用：给定内部点并指定 AE 为长段，只要验证 $`x^2=L(L-x)`$，便能推出原规格；若交换标签却继续把 A 侧长度放在比例中间，非对称的等式通常不保留。比例常数与 L 无关，但分点距离会随 L 缩放。

## 5. 算例、反例和证据位置

| 情形 | 精确或近似数值 | 核对结果 |
| --- | --- | --- |
| AB＝10 | $`x=5(\sqrt5-1)\approx6.18034`$；$`y=15-5\sqrt5\approx3.81966`$ | $`x^2=150-50\sqrt5=10y`$；贴图面积 100 |
| 取中点 5 | $`5^2=25`$，$`10(10-5)=50`$ | 等分不能满足极中比 |
| 取近似分点 6.2 | $`6.2^2=38.44`$，$`10(10-6.2)=38`$ | 接近不等于正好满足；舍入后的数字不能当作证明 |
| AB＝10，把 3.81966 对应的精确短段置于 A 侧 | 原方程中的变量若仍指 AE，则取的是短段 | 不能原样满足 AB : AE＝AE : EB；改用「全长 : EB＝EB : AE」才是镜像的规格 |

| 主张 | 读到哪里或怎样核查 |
| --- | --- |
| 在 AC 上等面积贴图，越出同形块 | Heath 页 267；Fitzpatrick 页 188 图、189 正文；与 VI.29 的输入逐一对应 |
| 扣 CE 后以面积导出反比 | Heath 页 267 末至 268 开头；VI.14 的方向从等面积至反比 |
| 所取确是较长段、原文另证来源 | Heath 页 268 的正文收束和其后的附录讨论 |
| 根、镜像、误差与有限复核 | 本文现代重构；另见[教学复现、Notebook 与实跑日志](../../reproduction/euclid-elements-vi30/README.md) |

## 6. 局限与复盘

原典处理正的长度和可作图关系，不计算十进制，也没用实验数据。代码基于有理系数加上 $`\sqrt5`$ 的精确表示，验证所选输入的点序、面积恒等和比例证书；这不是史料中的原始程序，不复现尺规的全部操作，也不由有限测试证明一般结论。AB 为零则两个比例的分母无法满足非零条件，排除。黄金分割在现代可以借助相似或自相似解释，但此命题本身没有断言某类美学、自然或建筑现象。

值得复盘的是**几何构造与证书分工**：依 VI.29 作出来的长度先有几何见证；扣去共同部分把见证化为简单的面积证书；VI.14 才把面积证书转成目标比例。现代符号推导给同一条链另一种读法。不应将这一教学类比倒推为古代算法直接影响某个现代 AI 系统。

## 7. 练习与答案

1. **VI.29 此处的输入面积为何是整个 BC，不是 BF？** BF 依赖尚未知的 E；BC 的面积只由 AB 决定，把它给 VI.29 才不循环。
2. **若误把 CD 的面积设为 BC＋AD，扣除后会怎样？** CD＝CE＋AD；代入再扣 AD，反而得 CE＝BC，挤掉正面积 BF，不能得到合法内点。
3. **用 AB＝2 写出长、短段。** 长段为 $`\sqrt5-1`$，短段为 $`3-\sqrt5`$；长段平方 $`6-2\sqrt5`$ 正好等于全长乘短段。
4. **为什么 AD 与 BF 同面积不要求它们全等？** 用等角与面积相同只推反比例。BF 可用一条较长的边配一条较短的边得到同面积，而 AD 的两边相等。
5. **若只知道 $`L:x=x:y`$，怎样排除 $`x\le y`$？** 内点给 $`0<x<L`$，所以左比大于一，右比也大于一，即 $`x>y`$；若允许外点或零长则必须先补域条件。
