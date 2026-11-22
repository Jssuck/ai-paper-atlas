# VI.31 原典与证明核对

核读 [Clay 希英对照](https://www.claymath.org/library/historical/euclid/files/elem.6.31.html)、Heath 1908 卷 II 印刷页 268–270（正文 268–269，校注跨 269–270）、[Fitzpatrick 希英对照本](https://farside.ph.utexas.edu/books/Euclid/Elements.pdf#page=189) 印刷页 189–190、[Joyce VI.31](https://mathcs.clarku.edu/~djoyce/elements/bookVI/propVI31.html)。Clay 英栏止于推得面积等式，希腊栏及两种印本另有重述题旨的结语。Fitzpatrick（印刷页 189）与 Heath（印刷页 269）的原图都在直角三角形三边外画出矩形轮廓；命题并不限于矩形。

## 比例链

直角在 A；AD 垂直 BC，D 在 B、C 之间。记 a=BA，b=CA，c=BC，p=BD，q=DC；X、Y、Z 分别是作在 c、a、b 上的同形面积，三边各作该形状的 **同一对应边**。VI.8 给整体及两个子三角形相似；匹配顶点 (A,B,C)→(D,B,A) 得 c:a=a:p，匹配 (A,B,C)→(D,A,C) 得 c:b=b:q。用 VI.19 推论，分别得 c:p=X:Y、c:q=X:Z。底边分拆 c=p+q，把长度关系转化成面积可加关系；主证不需先使用 I.47。

## 合并比例的省步

Joyce 和 Fitzpatrick 都在合并时标 V.24，但 Heath 269–270 页指出，该命题现存表述直接处理的是 **同后项** 的加法；这里两式是同前项，不能直接对分母加法。先把两条比例倒转成 p:c=Y:X 和 q:c=Z:X（由 V.定义 5 的比较条件交换两组倍数），再由 V.24 得 (p+q):c=(Y+Z):X。因 p+q=c，取 V.定义 5 中两倍数均为 1，左边相等迫使 Y+Z=X；不把长度和面积当成同种量相互比较。Heath 对两步分别提及 Simson 的补编命题 B、A，这不是《原本》正文编号。Fitzpatrick 末尾标 V.9 不等于用该条直接比较长度与面积；这里用定义写明跨量种的等比读法。Heath 还给出 V.22、V.18、V.9 的另一条路线，并报告有借 I.47 的另一证明被 Heiberg 移入附录。勿将两种补充当成此处印本正文。

## 历史和范围

I.47 是三个正方形的特例；VI.31 在相似、同样布置下换成同一模板。后世 [Proclus 对 I.47 的校注](https://www.maths.tcd.ie/~dwilkins/Euclid/Proclus_Taylor1792/ProclusCommentaryOnEuclid_Taylor_ElementsBk1Prop47_DraftTranscription.pdf) 点名称赞《原本》第六卷的推广（Friedlein 426 起；如 Heath 的 VI.31 校注所述），是后世归属证言，不是成书同期的首创证明。Joyce 用 Hippocrates 的月牙形例子说明早期曲边面积论证与同一平方缩放思想有关，不能凭此认定其拥有传本 VI.31 的一般证明。把标准可测曲边区域纳入相似缩放是现代延伸；本文古证所需的 VI.19 推论在第六卷的平面直线形比例框架内使用。三模板若形状不同或其承载边的对应不一致，则不会共享一个面积系数，不能套用命题。
