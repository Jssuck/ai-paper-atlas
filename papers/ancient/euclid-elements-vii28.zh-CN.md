# 欧几里得《几何原本》VII.28：为什么加上一个数，不改变与它的公因数？

> AI 数学与形式推理前史补读。约公元前 300 年的古代算术，实读 1908／2008 版。从现代论文主线跳回古代；不是 AI 论文，也不声称穷尽前史。

## 1. 书目与问题

- Euclid, *Elements*, VII.28。T. L. Heath, *The Thirteen Books of Euclid’s Elements*, vol. II, Cambridge University Press, 1908，[印刷页 329–330](https://archive.org/details/thirteenbookseu01heibgoog)。329 页有题句、图及正证，逆向反证跨页，330 页接评注。
- Richard Fitzpatrick, *Euclid’s Elements of Geometry*（2008 修订），[印刷页 216–217，希英对照](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=216)。另对读 [Clay 希英文本](https://www.claymath.org/library/historical/euclid/files/elem.7.28.html)和 [Joyce 在线本](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII28.html)；见[原典核对](../../reproduction/euclid-elements-vii28/source-review.zh-CN.md)。

5 和 7 互素，其和 12 明明不是质数，却仍与 5、7 各自互素。这不是“质数相加”的规律，而是**保留一个加数时，共同约数不会因另一个数换成和而改变**。不同于相邻的 [VII.27](euclid-elements-vii27.zh-CN.md)靠乘法累积互素条件，这里只检查同一个共同度量在加、减之后还会不会存在。

## 2. 图和记号：整条等于两段之和

| 原文标号 | 现代记号 | 角色 |
|---|---|---|
| AB／BA | $`a`$ | 第一个加数；换顺序不换线段长度 |
| BC／CB | $`b`$ | 第二个加数 |
| AC／CA | $`s=a+b`$ | 把两段首尾相接的全长 |
| D（希文 Δ） | $`d`$ | 假设存在的非单位共同度量 |

图上 B 在 A 与 C 之间，故 BC 是 CA 去掉 AB 后的剩余。原图表达相加关系，不提供具体数值。古书[卷七定义 1、2](https://mathcs.clarku.edu/~djoyce/elements/bookVII/defVII1.html)区分单位和数；依[定义 12](https://mathcs.clarku.edu/~djoyce/elements/bookVII/defVII11.html)，互素意味着只有单位能共同度量。因此原文说没有“数”同时度量，在现代译成没有大于 1 的公因数，不是连 1 都不整除。两个方向各自假设一个 D，不要求正反两次取到的是同一数。

## 3. 原证：正向减去加数，反向加回加数

1. **从加数互素出发。** 假设 CA 和 AB 不互素，则可取 D 同时度量 CA 和 AB。它能度量差 BC，又度量 AB，就与给定的 AB、BC 互素矛盾。因此 CA 与 AB 互素。
2. **交换保留的加数。** 以同一理由，若 D 度量 AC 和 CB，则也度量 AB，亦矛盾。原文只用“同理”简写这一次，并不是从“CA 与 AB 互素”单独推出另一对的关系。
3. **反向只需和与一个加数互素。** 原文选 CA 与 AB 作已知。若 D 同时度量 AB 与 BC，D 就度量和 CA，同时仍度量 AB，与新前提矛盾。于是两加数互素。若已知的是 CA 与 BC，交换加数即可。

| 主张 | 原证位置 |
|---|---|
| 首尾相接构造 AC；D 从 CA、AB 移到 BC | Heath 329 页题句、图及图下；Fitzpatrick 217 页上部 |
| 对 CB 用同理，得到“与各加数” | Heath 329 页后半；Fitzpatrick 217 页正向段末 |
| 已知 CA 与 AB 互素；D 由二加数移到和 | Heath 329 页底起、330 页顶收束；Fitzpatrick 217 页逆向段 |

Clay 英栏在逆向否定共同度量后停住，希栏与两印本明确写出加数互素，Joyce 还重述题句。Heath 330 页评注记录 Heiberg 对整除封闭性的提醒，并指出 [VII.1](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII1.html) 和 [VII.2](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII2.html) 已使用相关的和差操作。这里是**论证方法上的承接**，不是说 VII.28 正文按编号调用这两条。

## 4. 教学重构：搬运的不是最大值，而是每个候选

令 $`\mathcal D(x,y)`$ 表示同时整除 x、y 的所有正整数。固定任一正整数 d。若 $`a=du,\ b=dv`$，则 $`s=d(u+v)`$；若 $`a=du,\ s=dw`$，则 $`b=d(w-u)`$。因为两加数为正，已知后一个差也是正的。交换 a、b，得到另一组同样的双向关系：

$$
\begin{aligned}
d\mid a,\ d\mid b &\iff d\mid a,\ d\mid (a+b),\\
\mathcal D(a,b)&=\mathcal D(a,a+b)=\mathcal D(b,a+b),\\
\gcd(a,b)&=\gcd(a,a+b)=\gcd(b,a+b).
\end{aligned}
$$

第一行的逗号表示“且”。等式中间一行说明整组证据都保留下来，最后一行只是取最大元素。原证检验有没有非单位共同度量；这里显式核对每个候选，得到更强的现代等式。不能把这个等式或集合记号当作原文原句。

| 教学输入 $`(a,b,s)`$ | 三组共同约数 | 能防止的误读 |
|---|---|---|
| (8,15,23) | 均为 $`\{1\}`$ | 加数互素时，和确与两个加数都互素 |
| (5,7,12) | 均为 $`\{1\}`$ | 和可以是合数 |
| (6,9,15) | 均为 $`\{1,3\}`$ | 缺互素前提，不会被相加修复；3 可双向传递 |
| (12,18,30) | 均为 $`\{1,2,3,6\}`$ | 不只最大值 6；2 和 3 也不会丢 |
| (1,12,13) | 均为 $`\{1\}`$ | 现代单位边界；不要据此扩张古书数域 |

只知道 d 整除和，**不够**推出 d 整除某个加数。例如 3 整除 5+7，却不整除 5 或 7。正向反证必须同时假设它整除和与**保留的那个加数**。

## 5. 后续用途、现代延伸与实跑

[IX.15](https://mathcs.clarku.edu/~djoyce/elements/bookIX/propIX15.html) 明用 VII.28：从最简比的两个互素底数，先让两底数的和分别与底数互素，再与乘积、平方规则配合。以比 2:3 为教学例，三项为 4、6、9；先得 5 与 2、3 互素，而 4+6=2×5。证明 10 与 9 互素还需 VII.24、VII.25 所体现的乘积及平方步骤，不是 VII.28 单独给出的结论。

现代延伸：若 $`x=qy+r`$，则同一个 d 同时整除 x、y 当且仅当同时整除 y、r。前向用 $`r=x-qy`$，逆向用 $`x=qy+r`$；只要另外说明非零余数严格减小，就得到现代辗转相除中的不变量与终止性。余数为零时，现代约定下 $`\gcd(y,0)=y`$；VII.28 本身既没有零的这个边界，也不是完整的算法叙述。

[源码、Notebook 和实跑日志](../../reproduction/euclid-elements-vii28/README.md)把加法、减法及互换加数三个方向分开，核对共同约数而不只核对最大值；另有[独立技术核对](../../reproduction/euclid-elements-vii28/technical-review.zh-CN.md)。实跑在两项各取 2 至 20 的 361 对输入中，核对了 212 个非单位共同度量见证；三种 Python 模式各通过 5 项测试。Notebook 的三个代码格由标准库顺序执行，未测试 Jupyter 内核。输入为教学整数，无历史数据、训练或性能对比。有限样本只检查代码和例子，不能证明一般结论。复盘记住：**在两组之间保留哪一个数，对应做哪一次加法或减法？**

## 6. 练习与答案

1. **23 与 8 互素，23=8+15。必须另算 23 和 15 吗？** 答：不必。先由逆向得 8 和 15 互素，再用正向得到 23 和 15 互素。
2. **21 和 9 有公因数 3；拆去 9 后怎样？** 答：余 12，而 21−9=3×4，故 3 仍同时度量 9、12。
3. **能把正向结论写成“和是质数”吗？** 答：不能。5 和 7 都与 12 互素，但 12 有非平凡因数。
4. **28、35、63 的三组共同约数是什么？** 答：都只有 1 和 7；例如 28=7×4、35=7×5。最大的共同约数是 7，互素结论不适用。
5. **用余数不变量算 57 和 21 的最大公因数。** 答：余数依次 15、6、3、0，所以最大公因数为 3。这里用了现代重复取余及终止条件，不是 VII.28 原文逐步给出的例题。
