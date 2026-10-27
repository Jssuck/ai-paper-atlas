# Euclid《几何原本》I.12：来源、版本与证据边界

本台账对应 [I.12 中文深读](euclid-elements-i12.zh-CN.md)。收录的是线外点向无限直线作垂线这一古代构造单元，属于AI推理前史补读，不是现代AI论文。约前300年是作品传统年代，命题排列不是发现顺序；本次不声称穷尽前驱、古注及所有传本。

## 实际阅读版本

| 来源 | 位置与用途 | 边界 |
|---|---|---|
| [Heath 1908 第一卷扫描](https://archive.org/details/thirteenbookseu02heibgoog) | T. L. Heath 编译，*The Thirteen Books of Euclid’s Elements*, vol. I，Cambridge University Press，1908。I.12题面在印270/PDF291底，主文在印271/PDF292，相关评论至印275/PDF296首。 | 实际逐页目视主文、图、边注和评论。档案标识里的02不是卷号。印270前半属I.11，印275其余属I.13，不能混计I.12全文。 |
| [Fitzpatrick 希英对照本](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf) | Richard Fitzpatrick，*Euclid’s Elements of Geometry*，2007初版、2008修订纠正本；题名页称希腊文本据Heiberg 1883–1885编本。I.12在印/PDF17至18首句。 | 实际目视题名、版本、导言、主文及图；现代排印编译本不是古代手稿或Heiberg原版影印。 |
| [TCD Heath I.12转录](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIProp12_Heath1908.php) | David Wilkins 托管，标注Heath1908；用于核对主文措辞和命题链接。 | 未完整保留原扫描边注及历史评论，不能替代扫描。平分处的I.10依赖已回查扫描，而非只看网页。 |
| [Joyce I.12及Guide](https://mathcs.clarku.edu/~djoyce/elements/bookI/propI12.html) | Clark University托管的现代教学页面，用于交叉核对割线、切线、不中线三种情形。 | Guide中一处交点字母写为C、E，与自身图及主文不符；此处依原典采用G、E。现代指南不是古注原文，未把它升级为独立首创史证据。 |
| [Clay历史档案说明](https://www.claymath.org/library/historical/euclid/) | 支持作品约前300年与Bodleian MS D’Orville 301抄于888年的区别。 | 不支持I.12精确发现年份；未转载该档案图像。 |

**勘误核验范围。** 已目视Heath扫描PDF16的ERRATA；第一卷列举条目不涉及270–275。这只表示该张勘误表未列本次页段，不表示穷尽后版、全部古注及手稿差异。Fitzpatrick采用2008修订本，也不保证绝无残余错误。

## 主张与证据位置

| 主张 | 可核查位置 | 使用层级 |
|---|---|---|
| 给定无限直线AB和线外点C | Heath270底–271首；Fitzpatrick17题面 | 原文输入。A、B不是限制答案的线段端点。 |
| 在相对C的异侧选D，以C为圆心、CD为半径作圆 | Heath271构造段；Fitzpatrick17 | 原文。公设3许可作圆，但圆线交点存在还需额外背景。 |
| 将弦EG平分于H，连接CG、CH、CE | Heath271及I.10、公设1边注 | 原文构造。H在G、E之间、点不退化是现代接口显式检查的位置条件。 |
| GH=HE、HC公共、CG=CE推出H处角相等 | Heath271证明段和I.8边注；Fitzpatrick17 | 原文证明；不先用直角三角形判定或圆心弦中点垂直定理。 |
| 相邻角相等，所以各为直角，CH为垂线 | Heath271末、定义10边注；Fitzpatrick17至18首 | 原文定义应用，不需要先借I.13或角度数值。 |
| Oenopides研究该问题、天文学用途及gnomon术语 | Heath271末–272首，转述Proclus p.283,7–10 | 后世注释传统。未直接校读Proclus原文，不断言唯一首创或精确发现日期。 |
| 异侧D与两个交点的存在需要连续性说明 | Heath272中段 | Heath的基础讨论，不是原文已列现代连续性公理。 |
| 排除更多交点与垂线唯一性需另论证 | Heath272–274 | Heath批评Proclus部分论证，讨论I.16和I.7路线；不能当作I.12主文已证唯一性。 |
| 异侧D是充分但非必要条件 | Heath274末–275首，经Proclus p.289,18等转述 | 注释替代作法允许在线上取点，必要时增大半径；不是任意线上点都保证直接成功。 |

## 直接依赖与现代重构

独立回查Fitzpatrick页6的定义10、15，页7的公设1–3，页14的I.8，页15–16的I.10。I.10提供已证的线段二等分构造；本次教学代码直接算术取中点，不能称完整重演I.10尺规步骤。

正文中的参数直线、行列式、点积、二次方程、正平方根、唯一垂足、最近点和证书接口均为现代教学重构或另证推论。有限实跑只检查具体实现；不证明原文已经采用这些表达，也不替代一般定理或认证欧几里得公理体系。

本台账只公开原创证据概述和必要书目链接，不公开原PDF、原页图、长篇原文或全文翻译。最终正文版本由 [独立来源审查](euclid-elements-i12.source-audit.zh-CN.md) 的SHA-256绑定。
