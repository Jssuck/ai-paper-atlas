# VII.4 原典与证明核对

核读 [Clay 希英对照](https://www.claymath.org/library/historical/euclid/files/elem.7.4.html)、Heath 1908 卷 II 印刷页 303（正文、图与校注皆在此页）、[Fitzpatrick 希英对照本](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=198) 印刷页 198–199（图在 199）及 [Joyce VII.4](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII4.html)。Clay 希腊栏与印本有题旨复述，网页英栏止于末一构造。希腊图 ΒΕ、ΕΖ、ΖΓ 对英文 BE、EF、FC；三个分段只是图示，命题不限制为三份。

## 单份、若干份与证明

[第七卷定义 3–5](https://mathcs.clarku.edu/~djoyce/elements/bookVII/defVII3.html) 区分：小数量尽大数时是单数的 μέρος（份），不量尽时是复数的 μέρη（若干份）；反向说，被量尽的大数是小数的倍数。这里量尽指整除。命题证明复数情形确能分出若干相同的、各自可量尽大数的份，并非只重述“不整除”。

设原图大数 A=b，小数 BC=a。互素时，把 BC 按单位拆分，每单位都是 A 的同一份。此处以单位作量尺，不改变第 VII 卷定义 1–2 对单位和“数”的区分。非互素时先问 BC 是否整除 A；若是，BC 本身就是 A 的一份。若否，由 [VII.2](https://www.claymath.org/library/historical/euclid/files/elem.7.2.html) 取最大共同量尺 D=d。**BC 被 D 整除**，故能拆成等于 D 的份；**A 也被 D 整除**，故每一份量尽 A。这两个方向缺一不可：只找能整除 A 的量尺，未必能无余地拆分 BC。

按现代记号，b=nd、a=md，故 a 为 A 的 m 个 1/n 份。d=a 当且仅当 a 整除 b，这时 m=1；否则 m>1。Heath 303 页用「真分数」表达数个同份的情况，但现代“真分数”也含单位分数，不能单用“真分数”区分原题两个词。“最低项”“最少份数”可由最大共同量尺补证，且呼应 Joyce 导读；原题并未另行陈述唯一性定理。任取共同量尺可以作出可重复份，但不保证份数最少，例如 8 是 12 的八个十二分之一，却可用较大共同量尺 4 表示为两个三分之一。

## 直接用例

[第七卷定义 20](https://mathcs.clarku.edu/~djoyce/elements/bookVII/defVII20.html) 的数比例术语要求“同一份／同样若干份”，可作概念对读。[VII.20](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII20.html) 的证明直接依赖此分类：在假设最小同比分数中的小项是若干份后，拆出更小而同样成比的对子以归谬，再从不是若干份判定此项为单份。Joyce 的 VII.20 导读数例写成 91:132 对应 7:11，但 91=13×7，13×11=143，切勿沿用该数例。
