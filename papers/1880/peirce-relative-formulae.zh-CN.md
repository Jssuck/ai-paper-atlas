# 关系公式附录：把 Peirce 1880 的分配与结合表读清楚

本附录配合[精读主文](peirce-algebra-of-logic.zh-CN.md)，完整列出原刊53页四条原子工具式、55页八条简单分配式与八条展开式、56页八条简单结合式与十六条有条件结合展开式。它是带证明与边界说明的现代数学重构，**不是原文的逐字全译，也不以现代公式悄悄修正印本**。

公式都由扫描图中的上下标、否定线和基线位置核读。原刊每行另列的否定等价形式，可以由下面的运算定义复原；本附录选取主等式，不重复所有排印变体。44页扫描PDF包含一张后加封面，原刊页码减13即PDF页序。

- 原刊定位：[52–53页，四运算与工具式](https://archive.org/download/jstor-2369442/2369442.pdf#page=39)；[54页，非空前提](https://archive.org/download/jstor-2369442/2369442.pdf#page=41)；[55页，分配表](https://archive.org/download/jstor-2369442/2369442.pdf#page=42)；[56–57页，结合表与规则](https://archive.org/download/jstor-2369442/2369442.pdf#page=43)。
- 文献：Charles S. Peirce, “On the Algebra of Logic,” *American Journal of Mathematics* 3.1 (1880), 15–57；[DOI](https://doi.org/10.2307/2369442)。
- 可复算：[独立补充脚本](../../reproduction/peirce-1880/supplemental_relation_checks.py)、[实际运行日志](../../reproduction/peirce-1880/evidence/supplemental-relation-checks.log)、[结构化结果](../../reproduction/peirce-1880/evidence/supplemental-relation-checks.json)。有限测试负责检查转录与实现，一般性论证在下文给出。

## 1 四个运算：上标不是乘方

固定非空论域 $`U`$，所有关系都是 $`U^2`$ 的子集。补集以整个 $`U^2`$ 为界，记作 $`\overline a`$；$`\top=U^2`$，$`0=\varnothing`$。普通关系复合写作分号：

```math
(a;b)(x,z)\iff\exists y\,[a(x,y)\land b(y,z)].
```

下表保持与主文相同的 E/G/P/T 记号。原刊三标记依次控制第一输入、第二输入、输出，竖线表示不取补，短横表示取补。

| 本附录 | 原刊写法 | 三标记 | 现代定义 | 含义 |
| --- | --- | --- | --- | --- |
| $`E(a,b)`$ | $`ab`$ | $`(\vert\vert\vert)`$ | $`a;b`$ | 存在共同中介 |
| $`G(a,b)`$ | $`{}^a b`$ | $`(\vert-- )`$ | $`\overline{a;\overline b}`$ | a所指向者全满足b |
| $`P(a,b)`$ | $`a^b`$ | $`(-\vert-)`$ | $`\overline{\overline a;b}`$ | b的全部前驱都满足a |
| $`T(a,b)`$ | $`a\circ b`$ | $`(--\vert)`$ | $`\overline a;\overline b`$ | 有一个两边均不满足的中介 |

展开量词便不会把左右上标认反：

```math
\begin{aligned}
E(a,b)(x,z)&\iff\exists y\,[a(x,y)\land b(y,z)],\\
G(a,b)(x,z)&\iff\forall y\,[a(x,y)\Rightarrow b(y,z)],\\
P(a,b)(x,z)&\iff\forall y\,[b(y,z)\Rightarrow a(x,y)],\\
T(a,b)(x,z)&\iff\exists y\,[\neg a(x,y)\land\neg b(y,z)].
\end{aligned}
```

原刊称 G、P 为 regressive/progressive involution，T 为 transaddition。这里的 T **不是**全称式关系加法。原刊53页“lover/servant”的四个语例与这些量词方向一致。

若用三个比特表示无逆关系弧线的八种方案，0为竖线、1为短横，则统一写成：

```math
O_{s_1s_2s_3}(a,b)
=\neg^{s_3}E(\neg^{s_1}a,\neg^{s_2}b).
```

三标记只是一个操作的编码，不是三个对象位置的三元谓词。带弧线的其他方案还使用逆关系；需要同时遵守 $`(a;b)^\smile=b^\smile;a^\smile`$。

## 2 四条原子工具式：空真区域在哪里

以下对应[原刊53页](https://archive.org/download/jstor-2369442/2369442.pdf#page=40)编号1–4。取单点关系 $`Q=\{(A,B)\}`$，令：

```math
R_{\ne A}=\{(x,z):x\ne A\},\qquad
C_{\ne B}=\{(x,z):z\ne B\}.
```

则：

```math
\begin{aligned}
\text{A1}\quad P(l,Q)&=E(l,Q)\cup C_{\ne B},\\
\text{A2}\quad G(Q,l)&=E(Q,l)\cup R_{\ne A},\\
\text{A3}\quad P(\overline Q,l)&=E(Q,\overline l)\cup R_{\ne A},\\
\text{A4}\quad G(l,\overline Q)&=E(\overline l,Q)\cup C_{\ne B}.
\end{aligned}
```

**A1的证明。**当 $`z\ne B`$，$`Q(y,z)`$ 对所有y都假，因此P中的全称蕴含空真。当 $`z=B`$，它恰好要求 $`l(x,A)`$，这也是 $`E(l,Q)(x,B)`$ 的条件。A2左右对偶；A3、A4再取适当补集即可。

这些额外行、列不是可忽略的小项。它们解释了为什么原刊54页需要unlimited前提、56页需要选择适用的一类展开式。

## 3 分配表：八条简单式

对应[原刊55页](https://archive.org/download/jstor-2369442/2369442.pdf#page=42)“Affirmative / Simple Formulae”。D1、D2是第一行左右两项，以此类推。

```math
\begin{aligned}
\text{D1}\quad E(a\cup b,c)&=E(a,c)\cup E(b,c),\\
\text{D2}\quad E(a,b\cup c)&=E(a,b)\cup E(a,c),\\
\text{D3}\quad P(a\cap b,c)&=P(a,c)\cap P(b,c),\\
\text{D4}\quad P(a,b\cup c)&=P(a,b)\cap P(a,c),\\
\text{D5}\quad G(a\cup b,c)&=G(a,c)\cap G(b,c),\\
\text{D6}\quad G(a,b\cap c)&=G(a,b)\cap G(a,c),\\
\text{D7}\quad T(a\cap b,c)&=T(a,c)\cup T(b,c),\\
\text{D8}\quad T(a,b\cap c)&=T(a,b)\cup T(a,c).
\end{aligned}
```

例如D1由存在量词对析取分配得到；其余各式由定义、De Morgan律及左右方向对应导出。不能把交、并随意调换。

**错误推广的反例。**在 $`U=\{0,1\}`$ 中取 $`a=\{(0,0)\}`$、$`b=\{(0,1)\}`$、$`c=\top`$。$`E(a,c)\cap E(b,c)`$ 含有 $`(0,0)`$，但 $`a\cap b=0`$，所以 $`E(a\cap b,c)=0`$。两个存在见证不是同一个见证。

## 4 分配表：八条展开式

对应55页“Affirmative / Developments”。下面以标准关系幂集语义解释：$`p`$ 遍历**全部**二元关系，$`\bigcap_p`$、$`\bigcup_p`$ 分别是全体这些项的交、并。

```math
\begin{aligned}
\text{DD1}\quad E(a\cap b,c)
 &=\bigcap_p\,[E(a,c\cap p)\cup E(b,c\cap\overline p)],\\
\text{DD2}\quad E(a,b\cap c)
 &=\bigcap_p\,[E(a\cap p,b)\cup E(a\cap\overline p,c)],\\
\text{DD3}\quad P(a\cup b,c)
 &=\bigcup_p\,[P(a,c\cap p)\cap P(b,c\cap\overline p)],\\
\text{DD4}\quad P(a,b\cap c)
 &=\bigcup_p\,[P(a\cup p,b)\cap P(a\cup\overline p,c)],\\
\text{DD5}\quad G(a\cap b,c)
 &=\bigcup_p\,[G(a,c\cup p)\cap G(b,c\cup\overline p)],\\
\text{DD6}\quad G(a,b\cup c)
 &=\bigcup_p\,[G(a\cap p,b)\cap G(a\cap\overline p,c)],\\
\text{DD7}\quad T(a\cup b,c)
 &=\bigcap_p\,[T(a,c\cup p)\cup T(b,c\cup\overline p)],\\
\text{DD8}\quad T(a,b\cup c)
 &=\bigcap_p\,[T(a\cup p,b)\cup T(a\cup\overline p,c)].
\end{aligned}
```

**文本与重构的界线。**原表没有另写一句精确定义p的量化域。“所有二元关系”是这里采用的充分、明确的现代读法，不是声称原文已逐字给出这项域定义。对DD1，事实上遍历所有一元集合产生的柱状关系也足够；关键是能取得证明所需的任意划分，不能只固定一个p。

### DD1的逐点证明

固定输出 $`(x,z)`$。若左侧有见证y，则a、b、c三项都真。对任意p，要么 $`p(y,z)`$ 真，为第一项提供见证；要么它假，为第二项提供见证。所以左侧包含于右侧。

反过来，若左侧在 $`(x,z)`$ 为假，选择一个柱状关系：

```math
p(y,t)\iff\neg a(x,y)\quad\text{对所有 }t.
```

第一项的见证要求 $`a(x,y)\land\neg a(x,y)`$，不可能。第二项的见证要求a、b、c同时真，也被假设排除。于是这个p使交积中的一项为假，右侧也不含 $`(x,z)`$。

这里允许依正在检查的x选择p，因为右侧的逐点条件是“对所有p都真”；没有声称一个预先选定的p就能替代整个交积。DD2由取逆并对调方向得到；其余六式由同一式的补运算变换得到。

### 原刊Negative两表怎么读

数学上，正确的负式应对上面等式的**整个两侧**取补，再用De Morgan交换总和与总积。它们不是另外一套独立公理；但这不保证原刊负表的每个印刷符号都正确。

**本文核查：否定简单表右栏首行有一处异常。**[原刊55页](https://archive.org/download/jstor-2369442/2369442.pdf#page=42)清楚印成：

```math
\overline{a(b+c)}=\overline{ab}+\overline{ac}.
```

其中“+”不是OCR误认。取单元素论域，$`a=b=\top`$、$`c=0`$，左侧为0，右侧为全域，原印式不成立。正确的De Morgan对偶是：

```math
\overline{E(a,b\cup c)}
=\overline{E(a,b)}\cap\overline{E(a,c)}.
```

因此这里保留原印异常并单独给出正确重构；不能把后文肯定核心式的测试结果说成“整页负表原印全部通过”。其他负式排印变体也未在补充程序中逐条独立转录。校对时还须区分整式上横线和单个字母上横线。

## 5 八条简单结合式

对应[原刊56页](https://archive.org/download/jstor-2369442/2369442.pdf#page=43)“Affirmative / Simple Formulae”。原表每行有四个等价表达式；下列取中间两项。S1–S4为左列，S5–S8为右列，各自从上到下。

```math
\begin{aligned}
\text{S1}\quad E(a,E(b,c))&=E(E(a,b),c),\\
\text{S2}\quad P(a,T(b,c))&=G(T(a,b),c),\\
\text{S3}\quad P(a,E(b,c))&=P(P(a,b),c),\\
\text{S4}\quad E(a,T(b,c))&=T(G(a,b),c),\\
\text{S5}\quad G(a,P(b,c))&=P(G(a,b),c),\\
\text{S6}\quad T(a,G(b,c))&=T(P(a,b),c),\\
\text{S7}\quad G(a,G(b,c))&=G(E(a,b),c),\\
\text{S8}\quad T(a,P(b,c))&=E(T(a,b),c).
\end{aligned}
```

S1是普通关系复合的结合律：

```math
E(a,E(b,c))(x,z)
\iff\exists y\exists t\,[a(x,y)\land b(y,t)\land c(t,z)]
\iff E(E(a,b),c)(x,z).
```

S3两侧都化为 $`\overline{\overline a;b;c}`$。其余简单式同样在取补抵消后化为三项关系复合（有些最后还需整体取补）。因此没有交换不同类型量词的危险。

**不能随便取消括号。**下面不是简单结合式：

```math
G(a,E(b,c))\stackrel{?}{=}E(G(a,b),c).
```

取 $`U=\{0,1\}`$、$`a=c=\top`$、$`b=\Delta`$，左侧为 $`\top`$，右侧为0。左侧允许每个y选不同的t；右侧企图找一个对所有y都适用的t。接下来的原子展开正是为这些情况准备的。

## 6 四类结合展开：必须先选对前提

### 6.1 原文限定与索引

56页表前说的是：对任意c，Class 1或Class 2的全部式子成立，且Class 3或Class 4的全部式子成立。它**没有**说四类对每个c全都成立。[原文56–57页](https://archive.org/download/jstor-2369442/2369442.pdf#page=43)

以下索引域都必须完整：

- A遍历a中的全部单点原子；α遍历所有包含a的余原子。
- Q遍历e中的全部单点原子；ε遍历所有包含e的余原子。
- 原刊第二组大写字母为E；这里改写为Q，避免与复合运算E冲突。
- 空并等于0，空交等于 $`\top`$。

“余原子”就是全域减一个单点。例如α包含a，等价于α所删除的单点不在a中。

为避免把原文模糊条件当作无条件恒等式，这里给出**由现代集合语义推导的充分条件**：

| 原刊类别 | 本附录的充分条件 | 矩阵直观 |
| --- | --- | --- |
| Class 1 | $`\mathrm{ran}(c)=U`$ | c每列非空 |
| Class 2 | $`\mathrm{dom}(\overline c)=U`$ | c每行至少缺一格 |
| Class 3 | $`\mathrm{ran}(\overline c)=U`$ | c每列至少缺一格 |
| Class 4 | $`\mathrm{dom}(c)=U`$ | c每行非空 |

这是重构条件，不是给Peirce补写一段他已经明说的原话。任意c确实被覆盖：若c有空列，补c的每行必非空，因此可用Class 2；否则可用Class 1。若补c有空列，c有一整满列，故可用Class 4；否则可用Class 3。

### 6.2 Class 1：c每列非空

按原刊左上表从上到下：

```math
\begin{aligned}
\text{C1.1}\quad G(a,E(b,c))&=\bigcap_A E(G(A,b),c),\\
\text{C1.2}\quad T(a,E(b,c))&=\bigcup_\alpha P(T(\alpha,b),c),\\
\text{C1.3}\quad P(a,P(b,c))&=\bigcap_\alpha E(P(\alpha,b),c),\\
\text{C1.4}\quad E(a,P(b,c))&=\bigcup_A P(E(A,b),c).
\end{aligned}
```

### 6.3 Class 2：补c每行非空

按原刊右上表从上到下：

```math
\begin{aligned}
\text{C2.1}\quad P(T(c,d),e)&=\bigcap_Q T(c,E(d,Q)),\\
\text{C2.2}\quad T(T(c,d),e)&=\bigcup_\varepsilon P(c,G(d,\varepsilon)),\\
\text{C2.3}\quad G(P(c,d),e)&=\bigcap_\varepsilon T(c,T(d,\varepsilon)),\\
\text{C2.4}\quad E(P(c,d),e)&=\bigcup_Q P(c,P(d,Q)).
\end{aligned}
```

### 6.4 Class 3：补c每列非空

按原刊左下表从上到下：

```math
\begin{aligned}
\text{C3.1}\quad T(a,T(b,c))&=\bigcup_\alpha G(P(\alpha,b),c),\\
\text{C3.2}\quad G(a,T(b,c))&=\bigcap_A T(E(A,b),c),\\
\text{C3.3}\quad E(a,G(b,c))&=\bigcup_A G(G(A,b),c),\\
\text{C3.4}\quad P(a,G(b,c))&=\bigcap_\alpha T(T(\alpha,b),c).
\end{aligned}
```

### 6.5 Class 4：c每行非空

按原刊右下表从上到下：

```math
\begin{aligned}
\text{C4.1}\quad T(E(c,d),e)&=\bigcup_\varepsilon G(c,T(d,\varepsilon)),\\
\text{C4.2}\quad P(E(c,d),e)&=\bigcap_Q E(c,P(d,Q)),\\
\text{C4.3}\quad E(G(c,d),e)&=\bigcup_Q G(c,E(d,Q)),\\
\text{C4.4}\quad G(G(c,d),e)&=\bigcap_\varepsilon E(c,G(d,\varepsilon)).
\end{aligned}
```

注意C4.2与C4.4右侧最外层是普通复合E。嵌套上标很容易让这两处被误读成G或P。

### 6.6 C1.1的证明，以及其他十五式从哪里来

固定 $`(x,z)`$。C1.1左侧展开为：

```math
\forall y\,[a(x,y)\Rightarrow\exists t\,(b(y,t)\land c(t,z))].
```

取一个原子 $`A=\{(i,j)\}\subseteq a`$。右侧相应因子在 $`(x,z)`$ 的条件是：

```math
E(G(A,b),c)(x,z)\iff
\begin{cases}
\exists t\,[b(j,t)\land c(t,z)],&x=i,\\
\exists t\,c(t,z),&x\ne i.
\end{cases}
```

c每列非空，使第二种情况自动真。对全部原子取交，只保留第一种情况下逐j所需的条件，与左侧恰好相同。如果a为空，双方都是 $`\top`$。

其余式子不需要任意交换量词：

1. 对C1.1的a、b取补，并按需要对整式取补，可得Class 1其他三式。原子与其补余原子相互对应，交与并也随整体补互换。
2. 将c改为补c，用E/G/P/T的定义重新整理，得到Class 3；相应前提变为补c每列非空。
3. 对关系取逆，交换复合顺序，Class 1变为Class 4。例如C1.1取逆，利用 $`G(a,b)^\smile=P(b^\smile,a^\smile)`$，正得到重命名后的C4.2；“每列非空”变成“每行非空”。
4. 同样对Class 3取逆，得到Class 2。

所以这十六式有一个共同的原子论证和明确的对偶变换，不是仅因小域测试没找出反例就认定成立。

### 6.7 去掉前提会发生什么

令 $`U=\{0,1\}`$、$`a=\{(0,0)\}`$、$`b=c=0`$。C1.1左侧含整行 $`x=1`$，右侧只有一个因子，而它与0复合为0。Class 1在这里失败；但Class 2的充分条件成立。这与原文的择类断言一致。

## 7 54页的前提，以及不能静默改掉的坐标错位

### 7.1 最终包含关系成立

原文假设l、b均totally unlimited，也就是各自每行、每列均非空，推出：

```math
G(l,b)\subseteq E(l,b),\qquad P(l,b)\subseteq E(l,b).
```

其实第一式只需l每行非空；第二式只需b每列非空。第一式从l对应行任选一个中介，全称蕴含就让它也满足b；第二式对b的对应列做相同选择。

当补l、补b均totally unlimited时，原刊还得到：

```math
P(l,b)\subseteq T(l,b),\qquad G(l,b)\subseteq T(l,b).
```

分别只需补l每行非空、补b每列非空。没有这些条件，全称式会因前件为空而真，存在式却没有见证。

### 7.2 本文核查：B下标应对应哪个坐标

[原刊54页](https://archive.org/download/jstor-2369442/2369442.pdf#page=41)先写：

```math
b=\sum_j(B_j:C_j),
```

随后右栏印成：

```math
l^b\subseteq l(B_j:C_j)+k\overline{B_j}.
```

这里图像确实印B，不是OCR误认。按53页工具式A1，单点关系的额外空真区域由**第二坐标**决定，所以应是 $`k\overline{C_j}`$。

这一错位即使在原段的totally unlimited假设下也会破坏中间步骤。取：

```math
U=\{0,1\},\qquad
l=b=\{(0,1),(1,0)\},\qquad Q=\{(0,1)\}.
```

两关系都每行、每列非空。左侧 $`P(l,b)=\Delta`$；印文右侧只有整列 $`z=1`$，漏了 $`(0,0)`$。将B改为C后，这个中间包含式恢复成立，后续也应相应改用b的值域覆盖。

这属于本附录独立发现的印本文字／坐标问题，不冒充作者或出版社勘误；也不推翻上一节已独立证明的最终包含关系。原文该处提“second and third propositions”，而右栏实际需A1，也有引式序号疑点。

## 8 如何读57页的通则

[原刊57页](https://archive.org/download/jstor-2369442/2369442.pdf#page=44)把括号内运算叫interior、与第三项相接的运算叫exterior，junction marks是两运算在相接位置控制输入的标记。

若外层接合标记与内层输出标记相同，补操作在接合处抵消，或两处都不取补，可以化为连续普通复合，给出简单结合式。若标记不同，就在复合内部留下一个补，不能直接靠普通结合律改括号；这时要分解为原子或余原子，再按极性取总交或总并。

这套通则的数学重点，是追踪**补的极性与量词作用域**。不能把它压缩成“四运算都有普通结合律”，更不能压缩成“全称和存在可以换序”。

## 9 实跑范围：四十条核心式，而非整个历史理论

[补充脚本](../../reproduction/peirce-1880/supplemental_relation_checks.py)只用Python标准库，采用独立的四位布尔矩阵编码。在 $`U=\{0,1\}`$ 上有16个二元关系，p遍历全部16个，原子与余原子索引也全部枚举。

实际结果见[日志](../../reproduction/peirce-1880/evidence/supplemental-relation-checks.log)与[JSON](../../reproduction/peirce-1880/evidence/supplemental-relation-checks.json)：

- E/G/P/T的补定义对直接量词定义：1,024次操作比较，0处不符。
- 四条原子工具式：256次赋值比较，0处不符。
- 八条简单分配、八条展开分配、八条简单结合：每条4,096次外项赋值，全部相符。
- 十六条条件结合展开：每条检查4,096次赋值，其中2,304次满足所属类前提，全部相符；每条另找到672次在前提以外失败的赋值。程序保留首个反例，而不把这些预期边界当成测试失败。
- 各类四式对其余变量全部赋值均成立的c，恰与第6节条件在这个有限论域中的范围匹配。这不是从有限检查推断任意论域上的必要条件。
- 54页坐标错位、55页否定表右首行、错误混合结合、Class 1去掉前提的反例均被实际重算。

脚本检验的是这里逐条编号的**核心等式**，没有声称自动解析原刊全部排印变体；正确负式可由定义与De Morgan律导出，但原印负表存在上述异常；也没有把“未发现反例”冒充任意论域证明。一般证明依赖前面完整写出的集合语义、原子分析及对偶变换。

返回[精读主文](peirce-algebra-of-logic.zh-CN.md)；继续查看[来源账本](peirce-algebra-of-logic.sources.zh-CN.md)与[运行说明](../../reproduction/peirce-1880/README.md)。
