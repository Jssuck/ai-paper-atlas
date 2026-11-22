# VII.8 原典与证明核对

核读 [Clay 希英对照](https://www.claymath.org/library/historical/euclid/files/elem.7.8.html)、Heath 1908 卷 II 印刷页 307–308（物理页 320–321，图在 307）、[Fitzpatrick 希英对照本](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=201) 印刷页 201–202（题述在 201 起，图和证明在 202）与 [Joyce VII.8](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII8.html)。

## 复制、逐份消去与汇合

题设是 AB 对 CD 与 AE 对 CF 为同样的若干份；AE 为 AB 的正的被减段，CF 为 CD 的正的被减段。余段分别 EB、FD。把 AB 另作副本 GH，是为了能够分别在副本各份上对齐并复制要减去的份，不是改换原数。英语图上的 G–M–K–N–H 对应希腊图的 Η–Μ–Κ–Ν–Θ；末端希腊 Θ 对英 H，不能按字形逐个照抄。

先将 GH 拆作 GK、KH，每段是 CD 的同一单份；将 AE 拆作 AL、LE，每段是 CF 的相同单份，份数一致。因为 CD>CF，相应单份也严格大，故能在 GK 内取 GM=AL，在 KH 内取 KN=LE。各对都由 VII.7 得到余段 MK、NH 分别是 FD 的同一单份。再把这些同份汇合，计数仍与拆分 GH 相同；不是用 VII.5 将两个不同分母的单份相加。由于 MK+NH=(GK+KH)−(GM+KN)=AB−AE=EB，EB 对 FD 便有原全数的若干份关系。图只画两份，不能推出分母固定或只适用于二份。

现代重构可取 CD=nu、CF=nv、AB=mu、AE=mv，u>v>0；则 FD=n(u−v)，EB=m(u−v)，各剩下份大小是 u−v。以最低项表示原题的技术用语，应是 1<m<n；表示式写成 2/4 之类不自动形成技术上的复数份，因为它仍是单份。若被减量等于全量，余数为零，不可把零当原题里正余项的份。

## 版本边界与直接用例

- Fitzpatrick 页 202 将两处逐份余段推理都标成 [Prop. 7.5]。这是译本交叉引用上的不合，而非另有加法证明或希腊正文异文；Heath 页 308、Clay、Joyce 均正确标作 VII.7。Fitzpatrick 页 202 脚注用现代差分式。Joyce 导读的显示式反而误用加号，和正确的正文及导读文字不合。
- Clay 英栏止于汇合后的 MK、NH，最后识别其和为 EB、HG 为 BA 的步骤仍见希腊栏和两种印本。不能因此略去从副本转回原数。
- [VII.11](https://mathcs.clarku.edu/~djoyce/elements/bookVII/propVII11.html) 在第七卷定义 20 的比例表述下，直接援用 VII.7 或 VII.8：单份走前者，复数份走后者。不能把 VII.11 的统一形式当作 VII.8 的原话。
