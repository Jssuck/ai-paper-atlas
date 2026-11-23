# VII.20 原典与证明核对

核读 [Clay VII.20](https://www.claymath.org/library/historical/euclid/files/elem.7.20.html)、Heath 1908 卷 II 印刷页 320–321（扫描物理页 333–334；图在 320，末段与现代比例评注在 321，评注续至 322）、[Fitzpatrick 希英本](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=210) 印刷页 210–211 及 [Joyce VII.20](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII20.html)。

原文设 CD、EF 为与 A、B 同比的最小数对。希文 ΓΔ、ΕΖ 对应英图 CD、EF，内部拆块 ΓΗ、ΗΔ 和 ΕΘ、ΘΖ 则分别对应 CG、GD 与 EH、HF。这里是将候选最小的两数 CD、EF 各自拆开，不是拆 A、B。“较大配较大，较小配较小”在用法上是按同一比例位置比较，不能把两个比独立重排后再错配。

在候选与目标严格不等的分支，由 VII.13 将 CD:EF=A:B 交替成 CD:A=EF:B。反设 CD 是 A 的若干同样大小的单位分数部分、且不是一个单份，依定义 20，EF 就是 B 的同样种类、同样份数的部分。拆开后，CG=GD、EH=HF；每个比例的前项来自 CD，后项来自 EF，不能把两块横跨不同原量的部分说成大小相等。由 VII.12，CG:EH 等于各自合计的 CD:EF；CG、EH 又各小于相应的候选，于是违反最小性。图取两块仅作示意。按 VII.4 的分类，反证排除“若干份”后留下“一个单份”；再用 VII.13 和定义 20 确定 EF 是 B 的同一单份，因此两测量次数相同。若候选恰好就是目标对，现代写法直接取测量次数一，不把严格小数的 VII.4 生搬到相等分支。

Clay 的 VII.20 页面英栏在 CD 是 A 的一个单份处截断，未写 EF 与 B 的同一单份及同次数结论；该命题的完整希文实际排列在 [Clay VII.19](https://www.claymath.org/library/historical/euclid/files/elem.7.19.html) 的希文证毕之后。Heath、Fitzpatrick、Joyce 均保留收尾。Joyce 导读例中的 91:132 与 7:11 不相等，因为 91/7=13，132/11=12；保持其余数字可将 132 改为 143。该算例不在希腊命题中，不是原典错误。

[VII.21](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII21.html) 直接用 VII.20 从假设存在更小同比分量推出共同测量次数，之后另用 VII.16 与互素定义。VII.20 本身是给定最小对之后的同比倍数定理，不是互素刻画、最简对构造算法，更不凭此声称某一现代约分实现源自此命题。
