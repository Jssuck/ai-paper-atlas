# Euclid《几何原本》I.14：来源、版本和证据台账

本台账对应[中文深读](euclid-elements-i14.zh-CN.md)。研究对象是角量与位置条件如何判定两条射线相反，属于古代几何与推理前史补读，不是现代AI论文。约公元前300年是作品传统年代，不能当作本命题确切发现年；命题的论证顺序不证明历史先后或穷尽。

## 阅读版本及用途

| 来源 | 实读位置 | 使用边界 |
|---|---|---|
| [Heath 1908 第一卷扫描](https://archive.org/details/thirteenbookseu02heibgoog) | T. L. Heath，*The Thirteen Books of Euclid’s Elements*，vol.I，Cambridge University Press，1908；I.14印276下至277首，PDF297–298；相关评论印277。 | 实际目视主文、图、边注、评论。档案标识中的02不是卷号；印276上部仍属I.13，印277下部已起I.15。 |
| [Fitzpatrick 希英对照本](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf) | Richard Fitzpatrick，*Euclid’s Elements of Geometry*，2008修订纠正本，印/PDF19完整I.14；PDF6–7的定义、公设、共同概念。 | 现代编译排印，希腊文本据Heiberg编本，不是古代手稿或Heiberg原版扫描。与Heath论证相同不意味着所有引用标签完全相同。 |
| [TCD Heath I.14 转录](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIProp14_Heath1908.php) | 主文及I.13、公设4、C.N.1链接。 | 在线核对论证顺序；图、边注全貌及评论仍以扫描为准。不是另一个独立古代见证。 |
| [Joyce I.14与Guide](https://mathcs.clarku.edu/~djoyce/elements/bookI/propI14.html) | 主文、逆命题说明、平面背景及其他E位置说明。 | 现代教学解释，用于检查阅读边界；其中用语不能直接归给欧几里得。 |
| [Clay 历史档案](https://www.claymath.org/library/historical/euclid/) | 作品年代与传本背景。 | 不支持命题14精确发现年份、唯一首创者或完整传播史。 |

**勘误限定。** 已实际目视Heath扫描PDF16的ERRATA，未列印276–277。只报告该表未涉及本段，不声称所有传本、后版或残余错误已经穷尽。Fitzpatrick采用2008修订本，也不等于文本已获绝对无误认证。

## 主张定位

| 主张 | 定位 | 需要保留的限定 |
|---|---|---|
| 与共同基准在同一顶点成两角，异侧且角和为两直角，推出直线延续 | Heath276题面；Fitzpatrick19 | 异侧不能从数量等式中自动读出。现代开半平面、普通小角契约是显式重构。 |
| 反设BD不是延长方向，另设BE为CB延长 | Heath276证明开头；Fitzpatrick19 | E是比较对象；不能把目标BD预先认作延长而循环。 |
| 对CBE用I.13得到另一组两直角 | Heath276 I.13边注；Fitzpatrick19 | 对象须满足直线前提；不倒用I.15。 |
| 比较两对直角，再用相等传递 | Heath276 Post.4 and C.N.1边注；277注17 | Heath引Todhunter解释公设4的必要作用；Fitzpatrick对应处只印C.N.1，不能虚构相同显注。 |
| 同减公共CBA得到ABE等ABD | Heath276 C.N.3边注；Fitzpatrick19 | 只得到角量相等，还要保留位置关系才能识别射线。 |
| 小量等于大量不可能 | Heath276末；Fitzpatrick19 | 以C.N.5原则解释严格包含是合理显式化，但Heath此处未印C.N.5边注。 |
| 其他不同于BD的方向亦被排除 | Heath276末–277首；Fitzpatrick19 | 原图只示一种次序；本文展开另一分支，不说原文逐项列全。 |
| 同侧的半直角与一个半直角仍可合为两直角 | Heath277下段，经Proclus转述Porphyry | 本次直接读的是Heath；没有亲读Porphyry原作的主张，也没有由转述确定首创。 |

## 图、量与历史归属的边界

反证图把BE画斜以便与BD区别，而论证暂设CBE成直线；不能用像素测量同时认证互相冲突的假设。现代重构中的“C、D严格位于AB两侧”“B位于C与D之间”以及射线次序用于解释原证的关系，不冒称古文逐字给出了现代公理接口。

定义8排除处于同一直线上的两线所成倾斜关系，定义10描述直角；把相反方向的转动统一称作180度平角属于现代约定。普通角、模一周旋转和点的同一性不可混用。

点积、行列式、旋转对、负比例见证、精确有理运算、输入绑定证书和Python测试均为本篇教学重构。有限枚举只能核查所列输入与实现，不是原典的一般证明或全体系形式化。

台账只公开原创概述、必要书目信息与链接，不附原PDF、原页图片或全文翻译。最终正文绑定见[独立来源审查](euclid-elements-i14.source-audit.zh-CN.md)。
