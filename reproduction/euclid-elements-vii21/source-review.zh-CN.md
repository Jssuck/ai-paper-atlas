# VII.21 原典与证明核对

核读 [Clay 希英对照](https://www.claymath.org/library/historical/euclid/files/elem.7.21.html)、Heath 1908 卷 II 印刷页 322–323（扫描物理页 335–336，图在 322，评注在 323）、[Fitzpatrick 希英本](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=211) 印刷页 211–212 与 [Joyce VII.21](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII21.html)。

## 反证的两个隐含条件

希文 Α、Β、Γ、Δ、Ε 对应英图 A、B、C、D、E。假设互素的 A、B 不是同比数对中最小的一对。原文起初只说有较小的同比数 C、D，接着却按 [VII.20](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII20.html) 使用它们；Heath 323 页明确指出，必须从较小的同比数对中**选最小对**，不是任选一对。现代补足可在非空的同比正整数对中取第一项最小的对：固定正比，第一项更小则第二项也更小，且先有一对两项严格较小，保证所取的最小对确实严格小于 A、B。此处不需要先给出用最大公因数求最小对的算法。

VII.20 给出 C 量 A 与 D 量 B 的共同次数；E 是单位个数等于该次数的数，不是原先任取的公因子。由于 C<A 且 C 量尽 A，E 不可能只有一个单位。再用 [VII.16](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII16.html) 对调“每份有多少”与“有多少份”：A 与 B 都可由若干个 E 组成，故 E 是超过一单位的公量。这与第 VII 卷定义 12 的互素条件矛盾。Heath 在正文标 VII.16，并于评注提到 Heiberg 将相同的计数转换读作 VII.15；Heath 依据定义 15 的表述倾向前者。Fitzpatrick 与 Joyce 也标 VII.16。这是编辑对证明依赖的说明，不是希腊正文自行列出编号。

## 版本收尾与用途

Clay 英栏停在“不存在更小的同比数”，希栏与两种印本仍明确把它归结为“A、B 是最小的”。希栏引用 VII.20 的措辞中括出一个“与它们”的代词，不改变命题含义。Heath 323 页正文及代数评注均在互素矛盾处标 Def. 12。

[VII.22](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII22.html) 是逆命题，不是 VII.21 正文已经证明的结论；其原证使用共同因子和 VII.17，并不直接援用 VII.21。[VII.24](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII24.html) 则确实使用 VII.21：已知 E、A 互素，于是 E、A 是其同比中的最小数，再按 VII.20 推出相应测量关系。
