# VII.36 原典与证明核对

核读 [Clay 希英本](https://www.claymath.org/library/historical/euclid/files/elem.7.36.html)、Heath 1908 卷 II 印刷页 339–341（扫描物理页 352–354）、[Fitzpatrick 希英本](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=223) 印刷 223–224 页（希文在 223 页，英译收尾续至 224），以及 [Joyce VII.36](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII36.html)。

希文 Α、Β、Γ、Δ、Ε、Ζ 对应英文 A、B、C、D、E、F。先用 VII.34 找到 A、B 的最小公倍数 D。若 C 量尽 D，D 已是三数公倍数；取反设中较小的三数公倍数 E，由 VII.35 得 D 量尽 E，矛盾。若 C 不量尽 D，原文重新使用字母 E，令它是 C、D 的最小公倍数（再次使用 VII.34），此时反设中较小的三数公倍数改记 F。因此不可把两分支的 E 当作同一个对象。第二支先由整除传递证明 A、B、C 量尽 E；随后由 VII.35 从 A、B 量尽 F 推出 D 量尽 F，再对 D、C 使用 VII.35，由此得到 E 量尽 F，与 F 较小矛盾。第一次分支用一次 VII.35，第二次用两次。

Clay 希栏的几处方括号涉及不定代词及重复点明所量的 E，不改变证明中的对象或整除方向。Clay 英栏在第二分支排除较小公倍数后即止；希文、两印本和 Joyce 都保留 E 为三数最小公倍数的明确收尾。原题和证明只处理三个数。Heath 341 页评注则明说办法可继续用于更多数；现代用折叠算法表示这一延伸时，应把它标为评注或教学推广，而不是希腊正文附加的一般命题。

[VII.39](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII39.html) 直接使用 VII.36：先对与三种单位分数名称相应的三个数 D、E、F 构造最小公倍数 G，再用其他命题说明 G 具有这些分数部分及为何最小。后半并不是 VII.36 单独所证。
