# VII.35 原典与证明核对

核读 [Clay 希英对照](https://www.claymath.org/library/historical/euclid/files/elem.7.35.html)、Heath 1908 卷 II 印刷页 339（物理页 352，命题、图、证明与短评均在此页）、[Fitzpatrick 希英对照](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=222) 印刷页 222–223（图及希文在 222，英译末行续至 223），以及 [Joyce VII.35](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII35.html)。

A、B 同时量尽整个 CD（希文 ΓΔ），E 是它们共同量尽的最小正数。若 E 不量尽 CD，取由若干整个 E 组成的 DF（希文 ΔΖ），留下 CF（希文 ΓΖ），满足 0<CF<E。图中 F（希文 Ζ）在 C、D 之间；DF 与 FD 表示同一非定向长度，不能把它当作有符号差。因为 A、B 都量尽 E，而 E 量尽 DF，所以 A、B 都量尽 DF；它们也都量尽 CD，因此同样量尽差 CF。CF 于是成为更小的正公倍数，与 E 的最小性矛盾。逐次减去 E 或现代带余除法是对此步的教学实现；原文不提供程序，也未将 VII.1 或 VII.28 标为依赖。

[VII.34](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII34.html) 已给怎样找两个数的最小公倍数；VII.35 另外说明它量尽所有正公倍数，不能只根据“数值最小”就认作已证。两条通常的整除性质，即整除传递、同一数整除两个量就整除它们的差，在这里由文本直接使用。Clay 英栏止于矛盾，没有写出 E 量尽 CD 的回结；希栏、两印本、Joyce 都保留。希文的双重否定只是排除反设，不是新增条件。

[VII.36](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII36.html) 在三数构造中直接使用：任一三数公倍数先由第一对的最小公倍数量尽；若又要对第三数与这个最小公倍数应用构造，还要再次使用 VII.35。[VIII.4](https://mathcs.clarku.edu/~djoyce/elements/bookVIII/propVIII4.html) 的连比例证明中也直接用它，例如 B、C 都量尽候选项 O，因此二者的最小公倍数 G 也量尽 O。
