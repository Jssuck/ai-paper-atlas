# Euclid I.34 来源台账

核查日期：2026-10-28。范围为I.34完整命题、证明及Heath直接相关评论。本文为AI推理与数学前史补读，不把古代命题称为现代AI论文，不宣称穷尽前史。扫描PDF及页图仅用于核读，不随原创稿公开。

## 实读版本与页码

| 来源 | 实读范围 | 核查方式 |
|---|---|---|
| T. L. Heath，*The Thirteen Books of Euclid’s Elements*，vol. I，Cambridge University Press，1908 | 印323末I.34命题与设定；324全部原证；325–326全部评论，止于I.35标题；卷前ERRATA | 复用已取得PDF，重新渲染并目视页序344–347及16（1起算），非仅据OCR |
| Richard Fitzpatrick，*Euclid’s Elements of Geometry*，revised and corrected 2008 | 印/PDF36–37完整I.34及脚注，止于I.35标题 | 目视希英页图，检查英文证明及涉及的希腊字母序，不声称校勘手稿 |
| Trinity College Dublin，Heath I.34原证转录 | 完整网页原证 | 本次实际访问，交叉核查I.29、I.26、共同概念2和I.4次序；转录不含Heath评论 |

直达：[Heath扫描](https://archive.org/details/thirteenbookseu02heibgoog)、[Fitzpatrick希英本](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf)、[TCD I.34转录](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIProp34_Heath1908.php)。年代约公元前300年采用作品传统定位，不给单一命题虚构精确写作日期；1908和2008分别是本次实读版本年代。

## 主张—证据—边界

| 主张 | 原始位置 | 本稿解释边界 |
|---|---|---|
| 平行四边形对边、对角相等，对角线将区域二等分 | Heath323末命题；Fitzpatrick36命题 | 这里的diameter是该四边形的对角线，不是圆的直径；不能误说所有角都相等 |
| 原图区域沿边界为ACDB，对角线BC | Heath323末设定、324图；Fitzpatrick36 | A、D为一对对角顶点，B、C为另一对；若现代改成ABCD边界顺序，必须显式重标 |
| 两组内错角分别相等 | Heath324约第8–15行，两处I.29边注；Fitzpatrick36 | 两对对边分别提供一组角，不是从单对平行直接取得全部结论；经I.29间接使用第五公设 |
| I.26与共同边BC给出两对对边相等及A、D处角相等 | Heath324第16–26行；Fitzpatrick36 | 两角的夹边相同；Heath按ABC↔DCB对应排列，不以待证边相等作输入 |
| B、C处整角由两组等角相加 | Heath324第27–30行，C.N.2；Fitzpatrick36 | 对角线射线处于对应整角内部，角量相加需位置条件；不能把局部角直接当整角 |
| 再次调用I.4，得到三角形相等，故区域二等分 | Heath324第33–42行；Fitzpatrick36末–37首 | 原文第二段确实重新用已得AB=CD、共同边BC及夹角相等；不把I.26文字所列结论无声扩充为原文已宣告等积 |
| 平行四边形名称及四边形范围 | Heath325第一段 | Heath转述Proclus的术语起源说；本次未独立实读Proclus，不能提升为现代历史定论 |
| 一般性/非一般性的评论争论 | Heath325中后段 | Proclus借Aristotle《后分析篇》I.4–5区分解释两部分，Heath随后质疑其比较口径；二者都不是Euclid原证 |
| 后世三等分及推广 | Heath326，An-Nairizi构造 | Heath把依赖I.33/I.34的后世说明安放于此；不是Euclid I.34原文，也不声称本次完整复现任意n分构造 |

## 字母序、译注与勘误

Heath325注明：324第17、18、40行的三角形写法DCB，对应希腊的BCD；第36行DC、CB对应希腊CD、BC。他沿用I.33的处理原则，按对应顶点的顺序整理英译。三角形区域仍由同样三点构成，重点是避免读者把ABC与BCD误当逐位置对应；这不是更换几何对象。

Fitzpatrick36–37在三角形名称中保留BCD，夹角写BCD，与Heath整理后的DCB表示同一普通无向角。37第一脚注指出希腊边序CD、BC；第二脚注指出末四边形写ABCD，英译改ACDB。36页希腊末句确为ΑΒΓΔ，而设定和图沿边界为ΑΓΔΒ。该版本的脚注有实在字母序根据，但本稿仅记录所读排印和按图解释，不据此虚构古代抄本谱系或宣称数学结论被推翻。

已目视Heath卷前ERRATA，未列印323–326页；此项只说明本次核对的勘误表没有针对这些页的条目，不等于证明所有版本没有错误。

## 历史与范围说明

本命题延续I.33从平行理论进入平行四边形研究的组织。直接证明前驱为I.29、I.26、共同概念2及I.4；I.35以后面积命题不是本证前提。Heath325–326还将讨论联系到Proclus、Aristotle、Apollonius和An-Nairizi，但这些人物在本单元只按Heath转述出现，没有假称已独立核读所有原作，也不据作者影响力改变证据标准。

Heath对Proclus的质疑尤其需要保留：若比较对象默许限定为四边形，就不能只在一部分扩大到圆、椭圆、偶数边多边形，再据此判别哪部分更一般。它提醒读者先固定量词范围，而不是替Euclid添写发现史。

精确坐标、行列式面积、输入类型、JSON证书、反例和Notebook属于现代教学及工程核验。它们不认证古代操作史、不等于证明助理认证，也不以有限运行替代一般数学证明。
