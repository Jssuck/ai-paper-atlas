# Euclid《几何原本》I.16：来源、版本与证据台账

对应[中文深读](euclid-elements-i16.zh-CN.md)。范围为 I.16 的题面、证明及相关评论，是几何与推理前史补读，不称现代 AI 论文。约公元前300年是作品的传统年代估计，不是本命题可确定的发现年。书内依赖次序不等同历史发现顺序，收录不声称穷尽。

## 实际阅读与版本边界

| 来源 | 实读位置 | 使用边界 |
|---|---|---|
| [Heath1908第一卷扫描](https://archive.org/details/thirteenbookseu02heibgoog) | T. L. Heath, *The Thirteen Books of Euclid’s Elements*, vol. I, Cambridge University Press, 1908；I.16 印279下–280上，相关评论印280–281上；PDF300–302。 | 已目视题面、图、证明、引据和评论。档案标识中的02不表示本书是第二卷。印279上是 I.15 评论，印281下已开始 I.17。 |
| [Fitzpatrick希英对照本](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf) | Richard Fitzpatrick, *Euclid’s Elements of Geometry*, 2008修订纠正本；印/PDF20下–21中。 | 现代编译排印本，希腊文本据 Heiberg；不是古代手稿。21页脚注与C顶点处的论证条件应区分，见下。 |
| [TCD Heath1908 I.16转录](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIProp16_Heath1908.php) | 全命题及引据。 | 交叉核对证明次序，不视作独立古代文本见证；历史与几何评论仍以扫描为据。 |
| [Joyce I.16及Guide](https://mathcs.clarku.edu/~djoyce/elements/bookI/propI16.html) | 命题与现代导读。 | 仅作现代教学参照，不把 Guide 的椭圆几何解释归给欧几里得。 |
| [Clay历史档案](https://www.claymath.org/library/historical/euclid/) | 作品传统年代、传本背景。 | 只作书目背景，不用于认证 I.16 的唯一首创者或确切发现日期。 |

**勘误核查。** 已目视 Heath 扫描 PDF16 的 ERRATA；该表未列印279–281。此结论只限该表，不保证所有传本或现代排印无误。Fitzpatrick 文件标为2008修订纠正本，也不因此排除具体标签错误。

## 可复核的论证位置

| 主张 | 位置 | 限定 |
|---|---|---|
| 外角大于每一个内对角 | Heath印279题面和第1–6行；Fitzpatrick20下 | 是两个分别成立的不等式，不是外角等于两内对角之和；后者属于后续 I.32。 |
| BC越C延至D，目标为ACD对CBA和BAC | Heath279设图；Fitzpatrick20 | 方向和点序是条件，D不能任意取在BC直线上。 |
| AC中点E、BE延至F且EF=BE、连FC、AC延至G | Heath279第7–12行；Fitzpatrick20末 | 引 I.10、I.3、公设1和2。作等长延长须保留越过E的方向。 |
| AE=EC、BE=EF、AEB=FEC | Heath279第13–19行；Fitzpatrick20–21 | 最后一步用 I.15 对顶角，不是使用平行线或角和定理。 |
| SAS得到BAE=ECF | Heath279第20–24行；Fitzpatrick21首 | 引 I.4。现代中心反射或坐标恒等式可重构，但不是原文符号。 |
| ECD大于ECF，推出ACD大于BAE | Heath280第25行起，C.N.5边注；Fitzpatrick21 | “整体大于部分”需CF确实处于外角内部；不能仅从图像或全等结论无条件推出。 |
| 第二不等式以BC平分“同理”，并以BCG=ACD换角 | Heath280证明末尾，I.15边注；Fitzpatrick21 | 原文省略第二辅助构造细节。补出新中点和延长点属于教学展开，应明确标注。 |
| CF必须在ACD内部 | Heath280中部评论 | 作者在讨论非欧情形时明确指出此条件。本文的半平面/正锥证明是现代补证，不把它说成原文已完整公理化。 |
| 闭合直线的Riemann情形可出现相等或反向大小 | Heath280评论 | Heath采用其时代的几何表述。不能概括为所有非欧几里得几何都使 I.16 失败，也不能将球面模型与射影椭圆平面无条件等同。 |
| 一些人合并 I.16 与 I.17 的陈述 | Heath280末段，转述Proclus307,1–12 | 是Heath所引Proclus的报告；本次未独立核读所有古代见证，不称欧几里得原文自述。 |
| 一点到同一直线不可能有三条等长线段的推论 | Heath280末–281上 | Heath转述Proclus，使用 I.5 与 I.16。不是 I.16 原命题的一部分。 |
| 等外角/内对角阻止两线相交；与 I.27 的关系 | Heath281中部 | 属评论中的后续用途，不拿后面的平行线结论反过来证明 I.16。 |
| 保持 I.16 而仍有不相交线的可能性 | Heath281评论末 | Heath联系Bolyai–Lobachewsky假设；支持区分双曲与闭合直线情形，不认证完整非欧几何理论。 |

## Fitzpatrick脚注与论证条件的区别

Fitzpatrick 印21脚注实际写的是点 F 位于角 **ABC** 内部。本台账保留这个原标签，不把改为 ACD 的文字冒充原文。Heath印280明确讨论的则是 CF 位于角 **ACD** 内部；证明中用于整体与部分比较的也是 ECD 与 ECF，且 E 在 CA 上。因此论证的 C 顶点条件不能被 B 顶点条件直接替代。

但不能仅凭两个标签不同，宣称脚注是已证实的排印错误。在现代平面坐标重构中，F=A+C−B，所以 F−B=(A−B)+(C−B)。两个非共线边向量的正系数和确实落在角ABC内部。同时，F−C=(A−C)+(C−B)，又给出其在外角ACD内部的正锥表示。这是两个不同而都可成立的包含关系；关键是分别证明它们，不将一个当作另一个的同义语。这里的坐标说明是本文分析，不是Fitzpatrick的新增勘误，也不是欧几里得原文采用的证明。

## 公开内容范围

本台账为原创概述与必要书目链接，不是原文全译。原PDF、阅读页图和工作记录不随公开稿上传。来源审查仅核查来源和主张归属，代码的真实运行与实现边界由独立技术审查另核；最终正文哈希绑定见[独立来源审查](euclid-elements-i16.source-audit.zh-CN.md)。
