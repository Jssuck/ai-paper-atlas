# VI.32 原典与证明核对

核读 [Clay 希英对照](https://www.claymath.org/library/historical/euclid/files/elem.6.32.html)、Heath 1908 卷 II 印刷页 270–272（正文 270–271，布置条件的校注跨 271–272）、[Fitzpatrick 希英对照](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=190) 印刷页 190–191（图在 190 页）、[Joyce VI.32](https://mathcs.clarku.edu/~djoyce/elements/bookVI/propVI32.html)。印本和 Clay 希腊文均明确指出，在 C 处参与最后一步的两条射线不在直线 AC 的同一侧；Clay 英栏在推得共线后结束，希腊文和 Fitzpatrick 还重述命题。

## 原图证明

1. 两三角形在 C 共顶点；AB∥DC、AC∥DE，且 AB:AC=DC:DE（此处为正长度）。图中 AC、CD 分别作为两组平行线的截线，用 I.29 得 ∠BAC=∠ACD=∠CDE。不是任何两组无向平行都使所选的夹角相等。
2. 由 VI.6 的两邻边成比例与夹角相等，顶点 A→D、B→C、C→E 对应；于是 ∠ABC=∠DCE。图示中 CD 射线在角 ACE 内，故 ∠ACE=∠ACD+∠DCE=∠BAC+∠ABC。
3. 两边加 ∠ACB，用 I.32 得 ∠ACE+∠ACB 恰为两个直角。CB、CE 两条射线分居 AC 两侧，故满足 I.14 而构成同一直线的相反方向；不是先把 B、C、E 排成直线再拿图证结论。

## 布置反例与现代检查

取 C 为原点，A=u、B=u+v，u、v 不共线，比例因子 λ>0。图示方向取 D=−λv、E=−λ(v+u)，即有向 AB 与 DC 同向、有向 AC 与 DE 同向。于是 CE 向量等于 CB 向量的负 λ 倍。长度式书写 BA 或 AB 无关，但谈有向向量时不可互换。若只令支撑线平行，比例条件会允许不同符号选择。

例如取 u=(1,1)、v=(−2,0)、λ=2。改取 D=2v、E=2(v−u)，则 B=(−1,1)、E=(−6,−2)，两组对应边仍平行且等比例，夹角变为互补，det(CB,CE)=8，故不共线。另若改取 D=λv、E=λ(u+v)，虽然点共线，CB、CE 却同向重叠，不是 I.14 所证的相接情形。

Heath 页 271–272 指出题述若不配合图示可能被过宽理解，并给出夹角互补时的反例思路；这不是说原证允许取消方向约束。Joyce 的导读也指出对应边方向隐含于题述。[XIII.17](https://mathcs.clarku.edu/~djoyce/elements/bookXIII/propXIII17.html) 确实把 VI.32 用于证明 X、H、W 共线，这是正十二面体五边形面共面的证明步骤之一。
