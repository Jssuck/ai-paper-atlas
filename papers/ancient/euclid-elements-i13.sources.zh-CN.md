# Euclid《几何原本》I.13：来源、版本与证据边界

本台账对应 [中文深读](euclid-elements-i13.zh-CN.md)。收录的是直线上相邻角与两直角总量的关系，属于 AI 推理前史补读，不是现代 AI 论文。约前300年是作品传统年代，不是命题13的确切发现日期。命题排列是论证依赖顺序，不据此声称历史穷尽或特定个人首创。

## 实际阅读版本

| 来源 | 阅读位置 | 使用范围与边界 |
|---|---|---|
| [Heath 1908 第一卷扫描](https://archive.org/details/thirteenbookseu02heibgoog) | T. L. Heath，*The Thirteen Books of Euclid’s Elements*，vol. I，Cambridge University Press，1908；I.13主文印275中至276首，PDF296–297。 | 实际目视正文、图、边注及印276翻译注。档案标识的02不是卷号；印275上部仍为I.12，印276下部已为I.14。 |
| [Fitzpatrick 希英对照本](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf) | Richard Fitzpatrick，*Euclid’s Elements of Geometry*，2007初版、2008修订纠正本；I.13印/PDF18。 | 实际读希英排版页及图，对照定义8、10和共同概念。题名说明希腊文本据Heiberg 1883–1885编本；这是现代编译排印，不是古代手稿或Heiberg初版影印。 |
| [TCD Heath I.13 转录](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIProp13_Heath1908.php) | David Wilkins托管的Heath1908主文转录。 | 在线核对两次分解、同加与传递的次序；不能替代扫描的图、边注和翻译评论。 |
| [Joyce I.13及Guide](https://mathcs.clarku.edu/~djoyce/elements/bookI/propI13.html) | Clark University现代教学页。 | 辅助检查角的形式总和与单个角的区别。属于现代说明，不把其中术语归为欧氏原文或独立古史证据。 |
| [Clay 历史档案说明](https://www.claymath.org/library/historical/euclid/) | 作品年代及传本背景。 | 只作书目历史背景，不支持I.13精确发现年份或唯一首创者。 |

**勘误范围。** 实际目视Heath扫描PDF16的ERRATA，所列第一卷条目没有印275–276。这里只说明这张表未涉及本段，不保证全部传本、后版或残余错误已经穷尽。Fitzpatrick采用2008修订本，并不据此声称文本绝无错误。

## 主张定位

| 主张 | 可核实位置 | 证据边界 |
|---|---|---|
| 所成两角或者各为直角，或者总量等于两直角 | Heath275题面；Fitzpatrick18 | 原文结论，不能偷换为每个角都等于直角。 |
| 相等目标角分支由定义10结束 | Heath275及Def.10边注；Fitzpatrick18 | 相邻且立于同一直线的背景不能删去。 |
| 不等分支作BE垂直CD | Heath275 I.11边注；Fitzpatrick18 | 输入点B已在线上，因此直接调用I.11而非I.12。 |
| CBE分成CBA与ABE，DBA分成DBE与EBA | Heath275原图及两段分解；Fitzpatrick18 | 按原图射线顺序成立；另一侧摆图的对称分支是教学补足。 |
| 两边分别同加相同角 | Heath275 C.N.2边注 | 等量相加；不是先把共同角消去。 |
| 两个角对都等于同三个角，故相等 | Heath275末–276首 C.N.1边注 | 原文把三个相同角量视作同一总量，现代解释明确交换与结合。 |
| “加于每一方”的翻译说明 | Heath276注17 | 编译者对共同加项措辞的讨论，不是欧氏新增公理。 |
| 两直角之和不必是定义8意义下的单个角 | Fitzpatrick6定义8、10；Joyce Guide | 原定义排除共线两线；现代平角、度数或周数须另标语义层。 |

## 防止相邻页误归属

Heath印275上部的异侧辅助点讨论属于I.12。印277关于使用公设4比较两对直角的提醒接续I.14，不是I.13的边注。前一命题I.12的Oenopides注记也不应搬入I.13。本文只据本次已读页段报告，没有建立I.13专属的首创者谱系。

## 原文与本篇新增内容

原文证明使用直角定义、I.11构造、角的分解、共同概念2与1。本文的有理向量、行列式、点积、复数式旋转对、乘积恒等式、角范围证明、输入绑定证书及Python测试都属于现代教学重构或另证推论。度数和有理周数示例不是原文的单位，有限运行不是一般几何证明。

本台账仅公开原创书目和证据概述、必要链接，不附原PDF、原页图、长篇原文或全文翻译。最终稿哈希见 [独立来源审查](euclid-elements-i13.source-audit.zh-CN.md)。
