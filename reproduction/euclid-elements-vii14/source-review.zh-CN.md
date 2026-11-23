# VII.14 原典与证明核对

核读 [Clay 希英对照](https://www.claymath.org/library/historical/euclid/files/elem.7.14.html)、Heath 1908 卷 II 印刷页 313–314（扫描物理页 326–327；图在 313，校注在 314）、[Fitzpatrick 希英对照](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=206) 印刷页 206–207（图在 206），以及 [Joyce VII.14](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII14.html)。

原题要求等长的两列数，同一位置的相邻比例对应相等；不是要求一列内部每个相邻比都相同。图以 A、B、C 和 D、E、F 各三项示范，分别对应希腊 Α、Β、Γ 与 Δ、Ε、Ζ。用 VII.13 各做一次交替，将 A:B=D:E 改成 A:D=B:E、B:C=E:F 改成 B:E=C:F。借共同比 B:E 传递得 A:D=C:F，再用第三次交替得 A:C=D:F。Clay 英栏到了 A:D=C:F 就结束；希腊栏和两个印本仍有最后一次交替，不能把前者当作题目写法。Fitzpatrick 明标三次 VII.13。

原证没有给中间比传递步骤指定编号。Heath 314 页报告 Heiberg 可能将它读作一般量的 [V.11](https://mathcs.clarku.edu/~djoyce/elements/bookV/propV11.html) 在数的情形；Heath 自己更倾向看作同一整数或同一真分数关系的直接传递，即由数比例定义读出，不是另添命题。Joyce 也注明第 VII 卷没有单独的对应命题。这里是等比传递，不是运用现代分数乘法约掉中项；用乘法连乘是另一种现代说明。图只有三项可用同一传递链延长到任意有限等长数列；Heath 亦明确指出三项示例并不限定命题规模。

本命题是一般量 [V.22](https://mathcs.clarku.edu/~djoyce/elements/bookV/propV22.html) 的数论对应。Heath 强调，不可把这里三次交替的证明原封不动搬给 V.22：两列可以各为不同种类的量，原先列内比例可以比较，但交替后 A:D 等跨列的比可能不成立为同类量的比。这解释了结论类比而证明路线不同。

[VIII.1](https://mathcs.clarku.edu/~djoyce/elements/bookVIII/propVIII1.html) 实际援用 VII.14：比较两个等长且对应同连比的四项数列，由对应邻比得到端点比 A:D=E:H，然后才用互素、最小比与量尽关系。后者并非 VII.14 本身的结论。
