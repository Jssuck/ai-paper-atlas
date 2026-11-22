# VII.6 原典与证明核对

核读 [Clay 希英对照](https://www.claymath.org/library/historical/euclid/files/elem.7.6.html)、Heath 1908 卷 II 印刷页 305–306（扫描 PDF 物理页 318–319；305 页含图和正文，306 页续校注）、[Fitzpatrick 希英对照本](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=200) 印刷页 200–201（图在 200）。扫描本无可用文本层不等于此页空白；正文与图须读页影。

## 图和步骤

- 按英文图号，AB 是 C 的若干份，DE 是 F 的同样若干份。AB 拆作 AG、GB，DE 拆作 DH、HE。希腊图 ΑΗ、ΗΒ、ΔΘ、ΘΕ 对应四段；希腊分母 Ζ 对应英文 F，拼法不能逐字母照抄。图画两份，不限制一般命题只有两份，也不要求示意长度按数值精确绘制。
- [VII.4](https://www.claymath.org/library/historical/euclid/files/elem.7.4.html) 可用来理解「若干份」如何组成；本题已假定两边是同样若干份。卷 VII 定义 3–4 的单份/若干份之别不可抹平。除了份数相同，所取份的种类也必须相同：若 C 和 F 分别拆成 n 个各自相等的单位块，AB 和 DE 必须都取 m 块；块的绝对大小可以不同。
- 对每一对相应单份，先用 [VII.5](https://www.claymath.org/library/historical/euclid/files/elem.7.5.html) 得 AG+DH（或 GB+HE）仍为 C+F 的同一单份。汇合等量的配对块，才得 AB+DE 对 C+F 仍是同样若干份。用现代记号写成 C=nu、F=nv、AB=mu、DE=mv；配对得到 m 块 u+v，整体有 n 块。正文不是把分子、分母分别相加的一般分数加法规则。
- 严格原题是小数为大数的复数份且不整除大数；可用最低项 m/n 表示，1<m<n。只给某种拆法的 m>1 不足以排除单份，例如 2/4 仍是一半，归入 VII.5 的单份情形。现代等比加总公式可覆盖更广范围，不应反投给古题。

## 版本与用例

Clay 英栏止于第二对单份，希腊栏与两种印本还有最终的若干份结论。Fitzpatrick 的 [Prop. 7.5] 是译本的交叉引用标识，不是希腊正文里的方括号异文；第 201 页公式脚注是现代说明。Heath 页 305–306 写出更一般的公式，并将 VII.5–6 与 V.1 的倍数结论对照；这不是原证实际援引 V.1。

[VII.10](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII10.html) 的证明在分别得到各组成片的比例后，实际用 VII.5 或 VII.6 汇合片段；复数份分支对应 VII.6。
