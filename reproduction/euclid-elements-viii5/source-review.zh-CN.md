# VIII.5 原典与证明核对

核读 [Clay 希英对照](https://www.claymath.org/library/historical/euclid/files/elem.8.5.html)、Heath 1908 卷 II 印刷页 354–355（扫描物理页 367–368；正文和图在 354，评注延续至 355）、[Fitzpatrick 希英对照](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=233) 印刷页 233–234，以及 [Joyce VIII.5](https://mathcs.clarku.edu/~djoyce/elements/bookVIII/propVIII5.html)。

按第 VII 卷定义 16，所谓平面数是以两个数相乘所得的数，“边”是这次分解使用的两因数。英图 A、B 是平面数，C、D 为 A 的两边，E、F 为 B 的两边。希文 Γ、Δ、Ε、Ζ 对应 C、D、E、F；Η、Θ、Κ 为英图 G、H、K，Λ 为 L。所复合的两个比是 C:E 与 D:F，并非平面数各自内部的 C:D 与 E:F。给定分解就按位置配对，原证不要求分解唯一。

用 [VIII.4](https://mathcs.clarku.edu/~djoyce/elements/bookVIII/propVIII4.html) 取 G:H=C:E、H:K=D:F 的最小三项链，以 G:K 表示复合比。VIII.4 接收最简比，VIII.5 没有另写出约分步骤；现代执行应先分别约分，再拼接共用中项。另取 L=D×E。第一次用 VII.17，以 D 同乘 C、E 得 A:L=C:E；交换 L 的两因子（Fitzpatrick 在此标 VII.16），再以 E 同乘 D、F，第二次用 VII.17 得 L:B=D:F。最后 VII.14 从两组相同邻比推出 G:K=A:B。这里先比较两个实在的中间量 H、L 所在的各自链，不要求 H=L。

Clay 英栏在最后端点比例处截断，希文、Heath、Fitzpatrick 和 Joyce 继续说明 G:K 的复合比含义并转给 A:B。Joyce 网页的等距推比句在两个“as”前各多出 H、L 字母，不能据以改写等式；其导读亦有一处误列 c:d 和 e:f，正确值由原证和该导读推导明确为 c:e、d:f。Fitzpatrick 234 页的“相乘”是对复合比的现代解释。VI.23 是矩形与平行四边形上的几何类比，不是 VIII.5 证明直接引用的依据。

Heath 355 页的代数评注先取 C:E 和 D:F 的内部相接项 E、D 的最小公倍数，未另明写边比各自的约分。如果对未经约分的边直接使用，这一步确能接成同比链，却未必给出最小链。例如两数的边分别为 (6,10) 和 (9,14)，直接得到 60、90、126，而约去全列公因数 6 后是 10、15、21。预先将 6:9、10:14 约成 2:3、5:7 再用 VIII.4，也得到这个最小链；两种链的端点比相同，因此不影响复合比结论。
