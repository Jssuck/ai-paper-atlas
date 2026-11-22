# VI.30 原典与证明核对

独立核读 [Clay 希英对照](https://www.claymath.org/library/historical/euclid/files/elem.6.30.html)、Heath 1908 卷 II 印刷页 267–268、[Fitzpatrick 2008 希英对照](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=188) 印刷页 188–189（图在 188 页）、[Joyce VI.30](https://mathcs.clarku.edu/~djoyce/elements/bookVI/propVI30.html) 与 [VI.定义 3](https://www.claymath.org/library/historical/euclid/files/elem.6.def.3.html)。

- [I.46](https://mathcs.clarku.edu/~djoyce/elements/bookI/propI46.html) 在给定线段 AB 上作正方形 BC，其周界 A–B–H–C。用 VI.29 沿 **AC** 作矩形 CD，要求**整个 CD** 与正方形 BC 等面积，且超过 AC 的部分 AD 与 BC 相似（故也是正方形）。以双字母标两对角点，而非指两点连线的面积。
- 令 AC=AB=L，沿 AB 水平向右、沿 AC 竖直向上，则 A=(0,0)、B=(L,0)、C=(0,L)、H=(L,L)、E=(x,0)、F=(x,L)、D=(x,−x)。CD 的矩形右侧沿 FE 延至 D，超出正方形 AD 在 AB **下方**。等面积给 x(L+x)=L²，所以 0<x<L，E 确实在 AB 内，F 在 CH 内，公共块 CE 可以消去。这一位置说明是现代补明，不是原典的代数步骤。
- 去掉共同矩形 CE 后，剩余 BF 与 AD 等面积且等角。VI.14 给 FE:ED=AE:EB；因为 FE=AB，ED=AE，所以 AB:AE=AE:EB。由 AB>AE 和这组等比推出 AE>EB（Fitzpatrick 标 V.14）；结合 VI.定义 3 才完成命题。现代交叉核查为 L(L−x)=x²，正根唯一，负根不是长度；黄金比常用符号 φ 表示 L/x，不是 x/L。
- Joyce 构造句把 CD 写成与 BC 和 AD 的和等面积，和其下文的 BC=CD 自相矛盾；Clay 希腊文、印刷 Heath 和 Fitzpatrick 均明确 CD 等于 BC，AD 是形状指定的超出块，不是额外面积目标。Clay 英栏也没有最后的总结句，希腊栏和两种印本保留。Heath 页 268 报告部分见证把 FE=AB 扩为 FE=AC=AB，并将可能的 Theon 扩写与正文区分；结语之后另传的 II.11 路线由 Heiberg 移入附录，这是版本判断，不表示其数学失效。
- [II.11](https://mathcs.clarku.edu/~djoyce/elements/bookII/propII11.html) 作出等价的矩形／平方关系，[VI.17](https://mathcs.clarku.edu/~djoyce/elements/bookVI/propVI17.html) 可把该关系改写成连比；不要与 VI.30 的 VI.29 正文路线混称为同一证明。[IV.10](https://mathcs.clarku.edu/~djoyce/elements/bookIV/propIV10.html) 明示用的是 II.11 的面积关系，不能倒称直接引用 VI.30。[XIII.17](https://mathcs.clarku.edu/~djoyce/elements/bookXIII/propXIII17.html) 确实对 NP、PO、HQ 作此比分线用于正十二面体；Joyce 并列 II.11／VI.30 作为该步骤的构造来源，不能说它只依赖 VI.30。
