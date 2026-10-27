# Euclid《几何原本》I.11：来源、版本与证据边界

本表对应 [I.11 中文深读](euclid-elements-i11.zh-CN.md)。收录对象是线上给定点作垂线这一构造问题，属于形式推理前史补读，不是现代 AI 论文；命题编排次序不是发现次序。

## 实际阅读版本

| 来源 | 定位 | 使用边界 |
|---|---|---|
| [Heath 1908 第一卷扫描](https://archive.org/details/thirteenbookseu02heibgoog) | Euclid, *The Thirteen Books of Euclid’s Elements*, translated with introduction and commentary by T. L. Heath, vol. I, Cambridge University Press, 1908；I.11 本文在印刷页269/PDF第290页，注释延续到印刷页270/PDF第291页。 | 实际目视全文、图及注释；档案标识中的02不是卷号。270页下部已开始I.12，不混入本篇。 |
| [TCD 的 Heath I.11 转录](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIProp11_Heath1908.php) | David Wilkins 托管，页面标注Heath 1908。 | 核对主文；网页未完整保留扫描本的历史评论及全部边注，不能代替原页。 |
| [Fitzpatrick 希英对照本](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf) | Richard Fitzpatrick, *Euclid’s Elements of Geometry*；题名页说明希腊文据Heiberg 1883–1885编本；版本页为2007初版、2008修订纠正。I.11在印刷/PDF页16–17。 | 实际目视题名、版本、导言、主文及图。它是现代编译排印本，不是古代手稿或Heiberg原版影印。 |
| [Joyce I.11及Guide](https://mathcs.clarku.edu/~djoyce/elements/bookI/propI11.html) | Clark University 托管的现代教学页面。 | 核对主文和线上点/线外点的区别；其双等边三角形展开是现代教学解释，不当作古注或首创见证。 |
| [Clay 历史档案说明](https://www.claymath.org/library/historical/euclid/) | 《原本》约前300年；Bodleian MS D’Orville 301抄于888年。 | 只支持作品年代与特定传本年代的区别，不支持I.11精确发现年份。未转载其抄本图像。 |

**勘误范围。** 已目视Heath该扫描PDF第16页ERRATA，第一卷所列页码19、105、106、182、415中没有269–270或I.11条目。此结论只覆盖这一张勘误表，不声称穷尽各卷补遗、后续版及全部传本。Fitzpatrick使用2008修订本，也不保证绝无残余错误。

## 核心主张与证据

| 主张 | 证据位置 | 判定 |
|---|---|---|
| 输入为给定直线及其上给定点C | Heath269题面；Fitzpatrick16题面 | 不是从线外点下垂线。两版本配图均把C画在A、B之间。 |
| 取AC上的D，令CE=CD，在DE上作等边三角形FDE并连FC | Heath269构造段；Fitzpatrick16 | I.3负责截取等长线段，I.1负责等边构造。D≠C、E在C另一侧、可供截取的长度足够，是现代实现必须显式检查的非退化与位置条件；原图承载D-C-E顺序。 |
| 三边对应相等推出C处角相等 | Heath269证明段及I.8边注；Fitzpatrick16 | DC=CE、CF公共、DF=EF，比较DCF与ECF。不是先知道直角再用直角三角形定理。 |
| 相邻角相等所以各为直角 | Heath269末及Def10边注；Fitzpatrick16–17 | 直接使用定义10，不需要先引用I.13或180度角和，也不以公设4代替定义。 |
| 端点且禁止延长是需另处理的情形 | Heath270下半 | Heath转述Proclus提出不许延长时的端点构造，并说明an-Nairizi注释将其归于Heron。不能把这个限制问题说成I.11主文已经逐案证明。 |
| 平角平分与I.9的关系 | Heath269末至270首 | De Morgan提出可把I.11视为I.9特殊情形；Heath认为值得注意，但怀疑据此重排命题的好处。是后世评论，不能直接把平角代入原文的非退化三角形论证。 |
| 重新画圆与调用已证I.1不同 | Heath270上半 | Heath经Proclus p.282,8记Apollonius替代构造：仍先取距C相等的D、E，再依I.1方式画交圆并重新证DF=FE。Heath区分理论编排与实用几何的适切性。 |

**直接依赖回查。** 已目视Fitzpatrick页6定义10及等边三角形定义20，页7公设1–3，页8的I.1及其交圆存在脚注，页9–10的I.3，页14的I.8。I.3题面是从较长线段截取等于较短者；因此任意给定D并不自动保证E留在原有限线段CB内。可选足够近的D，或允许按公设2延长，但须把这一补充与原文简写区分。

## 历史层级及不作出的推断

- 约前300年是作品传统年代。Heath导论印刷页1/PDF22转述Proclus，把Euclid置于第一位Ptolemy时代，并提到Eudoxus、Theaetetus的前驱成果；同时提醒生平证据贫乏。这不能把I.11具体归给某位前驱或断言Euclid亲自首创。
- Heath导论印刷页29/PDF50说明Proclus属公元五世纪，远晚于Euclid。Apollonius和Heron相关归属在本单元只按“经Heath转述的注释传统”报告，未直接校读Proclus或an-Nairizi原文，也没有据此建立作者机构影响力排名。
- 印刷页271/PDF292提到Oenopides研究垂线的传统，但那段属于I.12的注释，**不得移用为I.11首创史**。本次只查看边界，不把I.12另立为已完成任务。
- 本文关于垂直直线唯一性、上下两支射线、坐标、点积、参数范围、错误分支、数值稳定性及程序契约均为现代教学分析。它们不能冒充古代操作或原文已给出的完整现代公理化；有限运行记录也不能替代一般证明。

公开材料仅含原创梳理及必要书目链接。不公开原PDF、原页图、长篇摘录或全文翻译。本台账不替代对最终正文按SHA-256绑定的独立来源审查。
