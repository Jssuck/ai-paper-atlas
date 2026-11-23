# 欧几里得《几何原本》VII.30：素数怎样从乘积追到一个因数？

> AI 数学与形式推理前史补读。约公元前 300 年的古代算术，实读 1908／2008 版。从现代论文主线回看形式推理前史；这不是 AI 论文，也不声称穷尽前史。

## 1. 问题与书目

7 整除 15×14，但不整除 15，所以它必定整除 14。6 则整除 4×9，却不整除 4 或 9。区别在哪里？原证没有预先拆出所有素因数，而是把同一乘积写成两种形式，造出一个**最简比**，然后读出整倍数。这和 [VII.24](euclid-elements-vii24.zh-CN.md) 的证明装置相同，变化在于互素从哪里来、整除最后读到哪里。

- Euclid, *Elements*, VII.30，T. L. Heath, *The Thirteen Books of Euclid’s Elements*, vol. II, Cambridge University Press, 1908，[印刷页 331–332](https://archive.org/details/thirteenbookseu01heibgoog)。331 页为题句、图及全证；332 页顶部是符号简述。
- Richard Fitzpatrick, *Euclid’s Elements of Geometry*（2008 修订），[印刷页 218，希英对栏](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=218)。对读 [Clay 希英本](https://www.claymath.org/library/historical/euclid/files/elem.7.30.html)与 [Joyce 正文及导读](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII30.html)；见[原典核对](../../reproduction/euclid-elements-vii30/source-review.zh-CN.md)。

## 2. 对象、条件和结论

| 原文标号 | 教学记号 | 作用 |
|---|---|---|
| A／Α；B／Β | $`a,b`$ | 给定的两个因数，不要求互素 |
| C／Γ | $`c=ab`$ | 两因数的积 |
| D／Δ | $`p`$ | 已知度量 C 的素数 |
| E／Ε | $`e`$ | D 度量 C 的次数，故 $`c=pe`$ |

现代写法是：对正整数因数，若 p 为素数且 $`p\mid ab`$，则 $`p\mid a`$ 或 $`p\mid b`$，这里的“或”是**至少一个**。原图的五条线段给对象命名，不靠量图求商。古书[卷七定义 1、2](https://mathcs.clarku.edu/~djoyce/elements/bookVII/defVII1.html)区分单位与数；实跑按古书给定数取大于 1，现代版本另可允许因数为 1。

## 3. 逐步重建原证

1. **处理不整除的一侧。** 若 D 已度量 A，结论已满足。原证展开 D 不度量 A 的情形：D 是素数，用 [VII.29](euclid-elements-vii29.zh-CN.md) 得 D 与 A 互素。
2. **造整数商 E。** 因 D 度量积 C，令 E 为量度次数。用[乘法定义 15](https://mathcs.clarku.edu/~djoyce/elements/bookVII/defVII15.html)读回相同的整数乘积 D×E=C=A×B。若严格区分定义中重复加法的主客位置，D 被加 E 次按定义写成 E 乘 D，调回原文次序可用 [VII.16](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII16.html) 的交换性；这处原证只引了定义 15。这里没有假定 D 已经度量 B。
3. **把等积写成有序的比。** 用 [VII.19](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII19.html) 的等积到比例方向，得 D:A=B:E。外项是 D 与 E，内项才是 A 与 B。
4. **从最简比读出同一整数倍。** 用 [VII.21](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII21.html) 把 D、A 的互素变成同一比下的最小数对；[VII.20](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII20.html) 说最小对的前项度量另一对的前项，后项度量后项，次数相同。所以 D 度量 B，A 度量 E。原文只需读出 D 度量 B。
5. **交换因数。** 原文在末段也指出，若 D 不度量 B，同理度量 A。这不是排他的二择；两项同时被度量时，两个条件句都没有被触发，但结论仍真。

$$
\begin{aligned}
p\nmid a &\Longrightarrow \gcd(p,a)=1 \qquad (\mathrm{VII.29}),\\
pe=ab &\Longrightarrow p:a=b:e \qquad (\mathrm{VII.19}),\\
\gcd(p,a)=1,\ p:a=b:e
&\Longrightarrow (b,e)=k(p,a),\quad k\in\mathbb Z_{>0}
\qquad (\mathrm{VII.21,\ VII.20}).
\end{aligned}
$$

第三行是现代压缩写法：整数尺度来自 VII.20，**不是**来自交叉相乘本身。以 VII.24 的原标号对照，那一证用 E:A=B:F，先确认 E、A 互素，再读出 E 度量 B；本证换为 D:A=B:E，让 VII.29 负责证明首对互素。两个命题没有要求把比例的两个分量从小到大排序；它们按前项、后项分别对应。

| 主张 | 原证证据位置 |
|---|---|
| D 不度量 A，仍可由素性取得互素 | Heath 331 页图旁首条边注；Fitzpatrick 218 页图下 VII.29 |
| E 是度量次数，外项积等于内项积 | Heath 331 页中段定义 15、VII.19；Fitzpatrick 218 页相应两处 |
| 最简及同倍数的职责分别来自 VII.21、VII.20 | 两版结束前的相邻引注；Joyce 正文同引 |
| 交换 A、B 后仍能推导，并写出结论 | Heath 331 页末；Fitzpatrick 218 页末段；Clay 希栏末 |

Heath 与 Clay 英栏把 VII.21 附近写得像“素数也是最小的”。前一句刚确立 D、A **互素**，且 VII.21 的对象是互素数对，并不要求 A 是素数。Fitzpatrick 与 Joyce 明写相互关系。Clay 英栏以对换情形收尾，希栏及两印本仍明写至少度量一个因数。

## 4. 手算和反例

| $`(p,a,b)`$ | 等积与比例 | 结论或失败点 |
|---|---|---|
| (7,15,14) | $`210=7\cdot30=15\cdot14`$；$`7:15=14:30`$ | 最简对按 2 倍放大，7 度量 14 |
| (7,14,15) | 交换后可重用上一行 | 首因数已被 7 度量；无需说 7 也度量 15 |
| (7,14,21) | 两因数都能被 7 度量 | “至少一个”允许两个都成立 |
| (6,4,9) | $`36=6\cdot6=4\cdot9`$；$`6:4=9:6`$ | 比例成立，但首对公因数为 2；比例尺度是 3/2，不是整数，无法读出 6 度量 9 |
| (7,15,8) | $`120`$ 不被 7 整除 | E 不存在为整数；不满足起始前提 |

合数例可先把 6:4 约为 3:2，得到 9:6 是该**最简对**的 3 倍。由此可见，错的不是比例定理，而是把未约分的 6:4 当作最简对。

## 5. 后继、现代延伸和实跑

[IX.14](https://mathcs.clarku.edu/~djoyce/elements/bookIX/propIX14.html) 明用本命题：若给定素数的最小公倍数还被另一个不同的素数 E 整除，把该数写成 E×F；原给定的各素数无法整除 E，便只能都整除更小的 F，与最小性矛盾。它不是本命题直接证明全部正整数的素因数分解存在且唯一。

**现代延伸，不冒充原证。** 若只给定 $`\gcd(m,a)=1`$，已知 $`m\mid ab`$，则 m 仍整除 b，即使 m 是合数。用现代贝祖等式选整数 u、v 使 $`um+va=1`$，乘 b 得 $`b=umb+vab`$，右侧两项均被 m 整除。因此素性在原证中的关键作用，是把“不整除”变成互素；直接给互素，就可以换用更广的条件。另对素数可按因数个数归纳推广；原证只展开两个因数。

[源码、Notebook、命令与实跑日志](../../reproduction/euclid-elements-vii30/README.md)分开核对商、比项顺序、共同整数尺度以及两侧或同时整除的情形；[独立技术核对](../../reproduction/euclid-elements-vii30/technical-review.zh-CN.md)检查推导与运行。三种 Python 模式各过 5 项，2 至 15 的 2,744 组三元组中有 443 组满足前提，其中仅一侧两种情形各 177 组，两侧都整除 89 组。Notebook 三个代码格由标准库按序实跑，未运行 Jupyter 内核。输入为教学整数，无历史数据或现代性能基准；有限枚举核查实现，不代替证明。复盘时问：何时才有 E？何时首对才是最简？哪个位置读出目标整除？

## 6. 带答案练习

1. **11 度量 8×33；按原证写等式和比例。** 答：264=11×24=8×33，11:8=33:24，整数尺度为 3。
2. **能仅用等积推出尺度是整数吗？** 答：不能。6:4=9:6 的尺度是 3/2；需要证明左侧为最简对。
3. **11 与 13 相乘，素数 11 此时度量哪一项？7 对 14×21 呢？** 答：前者只度量 11；后者同时度量 14、21，都符合“至少一个”。
4. **若 8 与 15 互素，且 8 整除 15×b，能推出 8 整除 b 吗？** 答：能，用现代互素版本；不能从“8 不整除 15”这一条信息直接用 VII.29，因为 8 不是素数。
5. **在 IX.14 的用法里，为什么要说明 E 不等于任何给定素数？** 答：这样它们才都不整除 E，进而逐一转到 F；若允许某个等于 E，就不能把那个整除关系强行转给 F。
