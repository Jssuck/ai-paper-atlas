# VII.34 原典与证明核对

核读 [Clay 希英对照](https://www.claymath.org/library/historical/euclid/files/elem.7.34.html)、Heath 1908 卷 II 印刷页 336–338（扫描物理页 349–351，两分支分别配图，代数评注在 338）、[Fitzpatrick 希英本](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=220) 印刷页 220–222，以及 [Joyce VII.34](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII34.html)。

两个分支都令 A、B 为输入，C 为构造得到的公倍数，D 只表示反设中比 C 小的公倍数。希文 Γ、Δ 对应 C、D，Ε、Ζ 对应 E、F，Η、Θ 对应 G、H。互素分支令 C=A×B；若 D=A×E=B×F，则由 VII.19 得 A:B=F:E，再从 VII.21、VII.20 知 B 量尽 E。VII.17 以共同乘数 A 给出 B:E=C:D，故 C 也量尽 D，与 0<D<C 矛盾。

非互素分支里，F、E 的次序有意义：由 VII.33 取最小同比对 **F:E=A:B**，C=A×E=B×F。假设 D=A×G=B×H，先得 A:B=H:G，再得 F:E=H:G，所以 VII.20 给出 E 量尽 G；同乘 A 得 E:G=C:D，再归结为较大数 C 不可能量尽较小的正数 D。Heath 第 338 页的代数评注明确把 VII.33 的两个最小比项写作 a/g、b/g，故最小公倍数写作 ab/g；这不是以现代公式替换原证的两分支。现代重构可另允许最小比项等于单位；不要将单位直接等同于第 VII 卷的“数”而不说明。

Joyce 证明开头将乘法换位的行链接到 VII.18；Heath、Clay、Fitzpatrick 标的是 VII.16，后者才是交换乘法次序的命题。Joyce 导读文字说除以最大公因数正确，但其下公式分母误写 LCM，正确分母为 GCD。Clay 英栏互素分支的 F:E 有一处漏写介词，希文顺序清楚；英栏又在非互素分支的“不存在更小公倍数”处终止，未重申 C 最小，而其他见证保留结论。

[VII.36](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII36.html) 用两数构造再处理第三项；[VIII.4](https://mathcs.clarku.edu/~djoyce/elements/bookVIII/propVIII4.html) 的应用见 Joyce 本命题导读。VII.34 本身的表述是两数问题，不应把后续的多项构造算入本证。
