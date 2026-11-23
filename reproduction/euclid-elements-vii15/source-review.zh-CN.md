# VII.15 原典与证明核对

核读 [Clay 希英对照](https://www.claymath.org/library/historical/euclid/files/elem.7.15.html)、Heath 1908 卷 II 印刷页 314–315（扫描物理页 327–328；315 页含图、完整证明及评注）、[Fitzpatrick 希英对照](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=207) 印刷页 207，以及 [Joyce VII.15](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII15.html)。

## 读图和两个计数

希腊栏中，整段是 ΒΓ、ΕΖ，英文记作 BC、EF；希文 Γ 可转写为 G，但不能直接套到英文图的 BG：那里 G 是第一处分点，BG 只是一单位，对应希文 ΒΗ。希文的三个单位是 ΒΗ、ΗΘ、ΘΓ，英语图作 BG、GH、HC；三个各等于 D 的整块是 ΕΚ、ΚΛ、ΛΖ，英语图作 EK、KL、LF。图中的三组是一般构造的示意，不是把测量次数限定为三次。

对应位置上，单位段在比的前项，D 大小的块在后项，即 BG:EK、GH:KL、HC:LF。因各前项等同为一单位，各后项同为 D，这些比相等；[VII.12](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII12.html) 将前项加在一起、后项加在一起，得到 BG:EK=BC:EF，而不是用同一行的块混作一个比。代回 BG=A 与 EK=D，有 A:D=BC:EF。最后依据数比例的定义，把前项是后项的同一单份关系，读回后项被对应前项量尽同样次数：A 量 D 的次数与 BC 量 EF 的次数一致。Fitzpatrick 与 Joyce 标注 VII.Def.20；Clay 希文和两个印本都保留这一步，Clay 网页英文却停在 A:D=BC:EF，不能据此说希腊文本没有读回测量结论。

## 特例与直接用途

Heath 在 315 页评注中指出，本命题与 [VII.9](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII9.html) 证明的结构相同，但第一项特意是一单位，且表述改用测量次数；Fitzpatrick 也标它为 VII.9 的特例。这是结构对照，不等于单位在第 VII 卷中就被当作通常的“数”。证明保留单位与数的区别，也不先诉诸已知的数乘法交换律。把单位记成现代的 1，再把量尽次数写为商，是教学改写。

直接下游见 [VII.16](https://www.claymath.org/library/historical/euclid/files/elem.7.16.html)：证明中以 E 为单位，已知 E 量 A 与 B 量 C 的次数相同，援用 VII.15 得 E 量 B 与 A 量 C 的次数相同，才可和另一种次序的乘积比较。Fitzpatrick 第 208 页明确标出这一引用。[VIII.2](https://mathcs.clarku.edu/~djoyce/elements/bookVIII/propVIII2.html) 中构造连比时援用的是 VII.17、VII.18，不宜写成直接引用 VII.15。
