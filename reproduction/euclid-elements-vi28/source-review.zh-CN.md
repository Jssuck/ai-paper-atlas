# VI.28 原典与证明核对

核对 [Clay 希腊文与 Heath 英译](https://www.claymath.org/library/historical/euclid/files/elem.6.28.html)、Heath 1908 卷 II 印刷页 260–263、[Fitzpatrick 2008 希英对照](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=185) 印刷页 185–187，以及 [Joyce VI.28](https://mathcs.clarku.edu/~djoyce/elements/bookVI/propVI28.html)。罗马字母依 Heath／Joyce；Fitzpatrick 的命题图和证明都可以用以下点位核查。

## 图与证明链

- 输入 AB、作为面积目标的直线形 C、作为亏缺形状模板的平行四边形 D。C 不得大于同样布置且在半条线段上构成的模板相似形。二等分于 E，在 EB 上作 EBFG，补左侧 AG；其面积等于右侧 GB。达到上界时 AG 即答案，不继续构造面积为零的辅助图。
- 严格小于上界时，VI.25 作 KLMN，面积为 GB 减 C，形状同 D；VI.21 使它也同 GB 相似。GB 面积较大，故对应边 GE、GF 各大于 KL、LM。在 G 处沿 GE 取 GO、沿 GF 取 GP，复制 KLMN 为 OGPQ；由 VI.26 得 G、Q、B 共线。
- 用沿 AB、EG 方向的斜坐标，在图的相同布置中取 A=(0,0)、E=(m,0)、B=(2m,0)、H=(0,m)、G=(m,m)、F=(2m,m)。若 GO 与 EG 的比例为 d/m，那么 O=(m,m−d)、P=(m+d,m)、Q=(m+d,m−d)。设 T=(0,m−d)；证明的平行四边形可只用 T、O、Q 和 S=(m+d,0)、R=(2m,m−d) 核对。UWV／VWU 是曲尺形标记，不是三角形顶点。
- GB 去掉 GQ 的曲尺形，面积就是 C。以 QB 为对角线的小平行四边形是共同块；PR 与 OS 是 GB 中 GQ、QB 的两块互补图（I.43），所以 PB=OB。沿 AB 的 AE=EB 且同高，得 TE=OB，再加 OS，得 TS 等于曲尺形，因而 TS=C。亏缺 QB 由 VI.24 与 GQ 相似，再接回模板 D。
- 这里 GE、GF 的坐标单位并不假定两边等长。若单位面积系数为正数 k，图中保留的亏缺底边 SB=m−d，则 TS 面积为 k(m+d)(m−d)。另一个亏缺底边 m+d 是现代代数的对称分支，不宜说传本正文同时构造了两根。

## 版本边界

Clay、Fitzpatrick 希腊文均以方括号标示题述中的若干语句，且严格小于分支的复制步骤也含括号措辞；这里不从排印括号推断作者或年代。Fitzpatrick 页 187 脚注以现代二次方程作解释，写了严格的参数上界并说正文找到较小根；严格式可用于两个不同根的情况，但主文明确接纳等号，等号给重根，不能照抄成可解性的必要严格不等式。Heath 卷 II 的校注与现代代数读法不是希腊正文；正文是面积作图，不是符号求根。

Heath 页 262 把题述限制部分的部分扩写归于 Theon，并认为 P 的较短读法较清楚；这是编辑判断。他还指出 VI.28、VI.29 都默用了「相似平行四边形若面积较大，则对应边较长」，可用 VI.20 的平方比例补明。二等分线段应援 I.10（Fitzpatrick）；Joyce 本页在这一步链接 I.9，而 I.9 是二等分角。Clay 网页的英文栏少了最后一段结语，希腊栏、Heath 印刷本及 Fitzpatrick 均有；不可据网文缺尾截断相似性的核验。
