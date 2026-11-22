# VII.7 原典与证明核对

核读 [Clay 希英对照](https://www.claymath.org/library/historical/euclid/files/elem.7.7.html)、Heath 1908 卷 II 印刷页 306–307（扫描物理页 319–320，图在 306、结论与校注在 307）、[Fitzpatrick 希英对照本](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=201) 印刷页 201（含图和正文）、[Joyce VII.7](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII7.html)。

## 原图与构造

- 上方 A–E–B 表示全数 AB、删去 AE、剩下 EB；下方 G–C–F–D，原来全数 CD，删去 CF，剩下 FD。G 在 C 的外侧而非 CD 内；辅助全数 GF=GC+CF，比较对象 CD=CF+FD。希腊图对应点 G 为 Η，F 为 Ζ。
- 两组原关系是 AB 对 CD、AE 对 CF 为同一「单份」，即同一个正整数倍数 k 满足 CD=k·AB、CF=k·AE。依该倍数取辅助 CG=k·EB，使 EB 对 CG 成为同一份；CG 不是先假定与 FD 相等。
- 由 VII.5 对两对同份加总，得 AB=AE+EB 对 GF=CF+CG 也为一份。GF、CD 都是同一个 AB 的同倍数，因此相等。消去两者共有的 CF 得 GC=FD；原先赋给 EB 对 GC 的份关系可转给 EB 对 FD，结论成立。现代公式是等式的直写，原证则先补出辅助量再消去共有量。
- 示意例：全数 AB=7、CD=21，删去 AE=2、CF=6。剩下 EB=5，取 GC=15，得到 GF=15+6=21；消去 CF 后 FD=15，5 仍是 15 的三分之一。若两个份的倍数不同，不能用 VII.5；相等全删给零余数，也不是古题两组正数余项的情形。

## 版本与用例

Clay 和 Fitzpatrick 的希腊文都在最后重述关系处标出 [ἐστὶ]；这不改变推导。卷 VII.5 的编号是译注给出的前提指认。Clay 英栏止于 EB 对 FD 与 AE 对 CF 为同一份；希腊栏及 Heath、Fitzpatrick 印本还明确接回全数 AB 对 CD。Fitzpatrick 201 页脚注与 Heath 307 页展开的是现代代数说明，不是原文中的变量式。

[VII.11](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII11.html) 直接使用 VII.7 和 VII.8：先用第 VII 卷定义 20 识别原全数与被减数的相同比，再按单份或若干份选择对应的消去命题，最后写回比例。VII.7 自身只处理单份，不能把后者的宽范围倒归于本题。
