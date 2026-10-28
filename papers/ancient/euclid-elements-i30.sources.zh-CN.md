# Euclid I.30 来源台账

核查日期：2026-10-28。范围为命题 I.30 的原证、版本差异和直接相关历史评论，不是古代数学或 AI 史的穷尽目录。原版页图只作阅读核验，不随本文公开转载。

## 实际阅读版本

| 来源 | 实读位置 | 用途与边界 |
|---|---|---|
| T. L. Heath，*The Thirteen Books of Euclid’s Elements*，vol. I，Cambridge University Press，1908 | 印页314完整 I.30；314末–315的评论，止于 I.31；卷前 ERRATA | 实际查看扫描页图，非仅依赖 OCR。PDF页序335–336，从1计；勘误表PDF页16 |
| Richard Fitzpatrick，*Euclid’s Elements of Geometry*，revised and corrected 2008 | 印/PDF页33完整 I.30；基础定义及版本导论沿前篇核查 | 希英对照、字母与命题引用核验；希腊本据Heiberg校本传统，未独立校勘手稿 |
| Trinity College Dublin，Heath I.30转录 | 完整网页 | 交叉核原证；不含Heath全部历史评论，不替代扫描 |

直达：[Heath扫描](https://archive.org/details/thirteenbookseu02heibgoog)；[Fitzpatrick希英本](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf)；[TCD I.30](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIProp30_Heath1908.php)。本次用此前取得的两份完整PDF实读并重新渲染所需页，另实际访问TCD转录。没有把链接存在当作已经阅读。

## 逐项证据

| 主张 | 原文位置 | 解释边界 |
|---|---|---|
| 分别平行于同一直线的直线彼此平行 | Heath314命题；Fitzpatrick33 | Book I平面几何背景，严格平行用定义23，不等于任意关系“都不相交” |
| AB、CD各平行于EF；截线GK交三者于G、H、K | 两版设定及图 | 图示H在G、K之间，线名与点角色不可仅按字母形状混配；希腊Η、Θ对应英文G、H |
| AGK=GHF | Heath314行6–10，I.29边注；Fitzpatrick33 | 对AB、EF用内错角相等 |
| GHF=GKD | Heath314行11–14，I.29边注；Fitzpatrick33 | 对EF、CD用相应的外角与内对角相等；不是同一对内错角 |
| AGK=GKD | Heath314行15–18，CN1边注；Fitzpatrick33 | 通过同一个中间角作相等传递；平行关系传递尚未预设 |
| AGK、GKD为内错角，故AB平行CD | Heath314行19–20；Fitzpatrick33明确标I.27 | 使用已经证明的充分判据；I.29则间接引入第五公设 |
| I.30与Playfair式唯一性有逻辑等价关系 | Heath314末–315首，归于De Morgan | 以共面、互异直线等背景为前提；不能把这段评论读作不需几何背景的纯符号等价 |
| 两角对应边分别平行或垂直时，角相等或互补 | Heath315评论及两图 | 据Heath转述De Morgan提出的扩展，并给证明；不是I.30原命题，也非本次独立实读De Morgan原著 |

## 版本与勘误

Heath314行20注指出，通常重复命题一般陈述的结语在此缺失；Fitzpatrick33则把末尾重复的一般结论放在方括号中。两版均有具体AB平行CD的结论，不能把结语差异说成证明缺失，也不推测方括号所涉手稿证据。本次查Heath卷前ERRATA，没有列出314–315页；Fitzpatrick此处未见专属脚注。此陈述仅限所查材料，不声称所有版次无误。

## 有来源的年代与范围

- 约公元前300年的Euclid及Alexandria定位沿Fitzpatrick导论采用，是作品传统的约略年代，不是单命题确切发表时间。作为推理与数学前史补读，不称现代AI论文。
- 书内前驱是定义23、I.27、I.29与共同概念1；I.29中第五公设的作用不能因I.30正文没有再次写出而消失。I.31以后不是本篇证明前提。
- 后世评论层：Heath以De Morgan名义讨论Playfair表述及对应边平行/垂直的角关系。本文只据1908译注转述，没有据此补造原著出版年份、首创权或完整传承链。
- 1883–1885的Heiberg校本传统、1908的Heath译注、2008的Fitzpatrick修订版属于版本时间，不与约前300年的作品年代混同。

## 不归给原文的内容

共面性和互异线限制的形式化、重合边界、任意截线次序的补全、行列式/方向向量证书、三维不相交反例、JSON严格类型、Notebook及有限枚举都是现代教学分析。原文没有机器学习数据、实验基线或模型评测。用欧氏坐标核验不能证明第五公设可省，有限实跑也不能证明一般定理或公理独立性。
