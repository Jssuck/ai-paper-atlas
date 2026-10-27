# Euclid《几何原本》I.17：来源、版本与论证位置

对应[中文深读](euclid-elements-i17.zh-CN.md)。本单元是几何与推理前史补读，不称现代 AI 论文。约公元前300年为作品传统年代估计，不是 I.17 独立发现年份；书内依赖次序不等于历史首创次序，收录不声称穷尽。

## 实际核读

| 来源 | 阅读位置 | 使用范围 |
|---|---|---|
| [Heath1908第一卷扫描](https://archive.org/details/thirteenbookseu02heibgoog) | T. L. Heath, *The Thirteen Books of Euclid’s Elements*, vol. I, Cambridge University Press, 1908；印281下–282，PDF302–303 | 实际目视题面、图、证明及282页评论。281上仍是 I.16 评论，不把它全部算作 I.17 正文。档案标识中的02不是第二卷编号。 |
| [Fitzpatrick希英对照本](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf) | Richard Fitzpatrick, *Euclid’s Elements of Geometry*, 2008修订纠正本；印/PDF21下–22上 | 实际目视并提取希英排印内容；是现代编译本，不是古代手稿。21上仍属 I.16，22中已进入 I.18。 |
| [TCD Heath1908 I.17转录](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIProp17_Heath1908.php) | 全命题、引据及“同理”句 | 用于交叉核对扫描受墨迹影响的文字；不是独立古代文本见证，不能替代扫描评论。 |
| [Joyce I.17及Guide](https://mathcs.clarku.edu/~djoyce/elements/bookI/propI17.html) | 全命题和现代导读 | 用于核对严格同加保序的公理边界和 I.32 的后续关系；Guide 不归给欧几里得。 |

**勘误。** 已目视 Heath 扫描 PDF16 的 ERRATA，表中未见印281–282条目。这个否定结论仅限所查勘误表，不保证全部版本或排印无误。Fitzpatrick 标作修订纠正本也不能当作一切字句绝对无误的证明。

## 主张与证据位置

| 主张 | 证据位置 | 解读边界 |
|---|---|---|
| 任取三角形的两个内角，其和严格小于两直角 | Heath281下题面；Fitzpatrick21下题面 | “任取”是三个不同顶点组成的三对，不是只证明有一对，也不是任意重复取同一角。 |
| 将 BC 越过 C 延长至 D | Heath281证明开端与Post.2边注；Fitzpatrick22首句 | D的位置和方向不可省略；任取BC直线上的点不足以产生所需外角。 |
| 外角 ACD 严格大于内对角 ABC | Heath281末；Fitzpatrick22首段，I.16引据 | 使用前一命题，不使用后续 I.32 的外角和等式。 |
| 给不等式两边同加 ACB | Heath282首句；Fitzpatrick22首段 | 原证确实采用量的严格同加保序；并不因此等于 C.N.2 原文已列出不等式规则。Joyce Guide 明确提醒其与列出的 Common Notions 的区别。 |
| ACD与ACB合为两直角 | Heath282图下，I.13边注；Fitzpatrick22首段 | 普通相邻角及相反射线条件使 I.13 可用。角量加法的现代代数表述属于教学重构。 |
| 得出 ABC与BCA和的严格上界 | Heath282第一段；Fitzpatrick22首段 | ACB/BCA在这里指同一个普通无向角；不能随意套入有向角或模角系统。 |
| 其余两对“同理” | Heath282证明末；Fitzpatrick22证明末 | 原文没有逐对列出全部辅助点。重新标记顶点或补充延长线是教学展开，应说明而非伪造原文步骤。 |
| “任意方式取两个”指任意一对相加 | Heath282题面短注 | 不是对角取任意整数倍，也不是连同外角任意组合。 |
| Proclus区分证明与原因说明 | Heath282评论首段，转述Proclus311,17–21 | 这里实际阅读的是 Heath 对 Proclus 的引述和解释，不是独立核读全部古代原典；不能冒称欧几里得的自述动机。 |
| 不延长原三角形边的替代证明 | Heath282评论中段 | 在 BC 内部取 D，连接 AD；利用两小三角形的外角不等式后相加。没有在原三角形外延长边，不等于不使用 I.16。 |
| 线外一点到直线的垂线至多一条 | Heath282评论末段 | 两不同垂足将形成两个直角的三角形，违背 I.17。这是唯一性论证，不独自证明垂线存在。 |

## 重构与历史归属限制

1. 用实数、有理数、向量、行列式、旋转对和证书实现该命题，都属于现代教学或核验模型，不是原文的形式语言。
2. 从三个两角和的不等式不能仅凭加法就推出三角形总角和恰等于两直角。后者是后续 I.32 的更强结论，不能倒过来作为本文原证的前提。
3. 局部论证不显式调用平行公设，不等于所有曲面或所有非欧几何都满足这些步骤；其前提仍包括可用的 I.16、延长、角序和同加保序。
4. Proclus 的替代证明以及垂线唯一性推论按 Heath 的评论报告，不并入欧几里得 I.17 原命题正文。关于“为什么有效”的当代分析也不冒充作者已经提出的现代 AI 观点。
5. 原PDF、阅读页图、内部工作记录不公开上传；本文件只含原创概述与必要书目链接，不是全文翻译。

最终正文的独立来源核验和哈希绑定见[来源审查](euclid-elements-i17.source-audit.zh-CN.md)。代码实跑、数据统计和数学实现由独立技术审查另行核验。
