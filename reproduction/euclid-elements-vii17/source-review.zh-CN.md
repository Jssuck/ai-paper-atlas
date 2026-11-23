# VII.17 原典与证明核对

核读 [Clay 希英对照](https://www.claymath.org/library/historical/euclid/files/elem.7.17.html)、Heath 1908 卷 II 印刷页 317（扫描物理页 330，含图和评注）、[Fitzpatrick 希英对照](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=208) 印刷页 208–209（图及证明开头在 208）、[Joyce VII.17](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII17.html)。

希腊 Α、Β、Γ、Δ、Ε、Ζ 对应英图 A、B、C、D、E、F。注意最后的 Ζ 对应单位 F；E 则是 A 乘 C 得到的数，不是单位。示意图的 B、C 在同一行，D、E 在对应的下一行，F 另绘；这些独立线段不构成几何证明。同一个 A 是发出乘法动作的数：按定义 15，用 A 内单位的个数决定各自取多少份 B 和 C。这是与 VII.18 的方向差异。

先用测量次数提出两个局部事实：F 量 A 的次数与 B 量 D 的次数相同，也与 C 量 E 的次数相同。按定义 20，这是同一种“单份”关系，于是 F:A=B:D、F:A=C:E。借共同比 F:A 传递得到 B:D=C:E，再按 [VII.13](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII13.html) 交换中项，得到题设要求的 B:C=D:E。Joyce 在传递处括注 [V.11](https://mathcs.clarku.edu/~djoyce/elements/bookV/propV11.html)；这是一般量中同一比的传递性质的对应参照，不能说希腊原证明直接引用 V.11。此处还可直接用两对数均满足同一单份测量关系解释传递，不必使用后来 VII.19 的交叉乘积。

Clay 英文证明止于 B:D=C:E，末次交替省略，但其命题和证明开头仍陈述目标；希文、Heath、Fitzpatrick、Joyce 都保留末次交替。Heath 317 页的评注指出，这次欧几里得确实把测量改写成比例；该页上半部 VII.16 评注里的另一种比例式写法，不应与 VII.17 正文混读。

后续有两处可确认的直接使用。[VII.18](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII18.html) 先用 VII.16 交换两个乘积中的因子，使同一个数居前，再按 VII.17 得比例。[VII.19](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII19.html) 构造辅助积 G，让 A 乘 C、D 分别生成 G、E，从 VII.17 得 C:D=G:E；逆向证明同样使用此比例。两处用法都不能反过来作为 VII.17 的前提。
