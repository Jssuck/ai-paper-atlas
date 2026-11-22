# VII.1 原典与证明核对

核读 [Clay 希英对照](https://www.claymath.org/library/historical/euclid/files/elem.7.1.html)、[Heath 1908 卷 II 印刷页 296–297](https://geometor.github.io/euclid/heath/volume_II/book_vii/propositions/01/)（图在 296 页，校注在 297 页）、[Fitzpatrick 希英对照本](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=195) 印刷页 195–196（图在 195 页）及 [Joyce VII.1](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII1.html)。Heath 指出，第 VII–IX 卷以线段表示整数是 Heiberg 据手稿采用的作图方式，不能把图的比例当成原文指定输入数值。

## 假设与归谬

命题的方向是：两个不等的数反复以小减大，在非单位余数尚不能整除前一项的情形下继续，若出现单位余数，就互素。这里的「量尽」是整数整除，不是小于或能放下一次。图中 AB=BF+FA、CD=DG+GC、AF=FH+HA；被整除的是 BF、DG、FH，余数依次为 FA、GC、HA。Heath 将首句解释为在 BA 上量取 CD 的最大整数倍 BF，得小于 CD 的 FA；不用把这一步解释成每次只减一次即交换。

假设共同量尺 E 是大于 1 的数。因为 E 整除 CD，而 CD 整除 BF，所以 E 整除 BF；E 也整除 BA，因此整除差 AF。同样先后传到 CG、AH。E 整除 AH=1 不可能。第 VII 卷定义 1–2 区分单位与多单位构成的数；[定义 12](https://mathcs.clarku.edu/~djoyce/elements/bookVII/defVII11.html) 以只有单位同时量尽两数来定义互素，而不是说两数各自都是质数。Heath 明指出证明默用了整数整除对差封闭。现代可另外证明双向公约数集合不变量；不能把这一补充及一般终止、最大公因数结论都算作 VII.1 的陈述。

## 版本差别与适用边界

- Clay、Fitzpatrick 的希腊文题述写「不等」且不加括号，随后重述对象处将同一词列入方括号。这个排印差别不取消原命题的输入限制。希腊文 ἀριθμὸς ὤν 的阳性形式说明此处「是数」指量尺 E，而非阴性的「单位」；Heath/Joyce 英译的代词位置容易误读。Fitzpatrick 页 196 用 E 明确作该句主语，但下一句否定词的英语位置容易误导；结论为「没有大于 1 的数同时量尽两数」，不只是「存在一个数不能同时量尽两数」。
- Joyce 导读称输入为 54 与 85，但所列的第一式 85=2×31+23 不是从这组数直接求余。从所称的输入出发，实际先得 85−54=31，然后 54−31=23；才接续 31=23+8、23=2×8+7、8=7+1。无法从这处不一致判断作者原本意图用哪对输入。原文没有这些具体数值。
- 例如 24、16 给出余数 8，随后 8 整除 16，不经过单位余数。现代余数记作 0 是整除的记录，不是古证里的「单位」。现代扩展的输入 1 或 0、相等两数，也不是本命题的原始设定。[VII.2](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII2.html) 在先设不互素时引用 VII.1 排除单位余数，再处理找到最大共同量尺的任务。第 X 卷的相互减法讨论几何量，是可比较的思路而不是这个整数论证的前提。
