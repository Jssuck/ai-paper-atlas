# Euclid I.31 来源台账

核查日期：2026-10-28。收录范围为命题 I.31 的构造、证明与直接相关历史评论；这是一项 AI 推理与数学前史补读，不称现代 AI 论文，不声称穷尽早期文献。原版 PDF 和页图只供阅读核查，不随原创解析公开转载。

## 实际阅读版本

| 来源 | 实读位置 | 用途与边界 |
|---|---|---|
| T. L. Heath，*The Thirteen Books of Euclid’s Elements*，vol. I，Cambridge University Press，1908 | 印页315末至316：完整 I.31及其评论，止于 I.32标题；卷前ERRATA | 已实际查看扫描页图，PDF页序336–337及16，从1计；不只凭OCR |
| Richard Fitzpatrick，*Euclid’s Elements of Geometry*，revised and corrected 2008 | 印/PDF页33末至34上部完整 I.31 | 希英对照、图形和命题引用交叉核查；希腊本承Heiberg校本传统，未独立校勘手稿 |
| Trinity College Dublin，Heath I.31转录 | 完整网页正文 | 交叉核原证；未包含Heath全部历史评论，不替代扫描 |

直达：[Heath扫描](https://archive.org/details/thirteenbookseu02heibgoog)；[Fitzpatrick希英本](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf)；[TCD I.31](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIProp31_Heath1908.php)。本次重新渲染此前取得的完整PDF相应页，并实际访问TCD正文。没有把链接存在当作完成阅读。

## 主张与证据位置

| 主张 | 可复核位置 | 解释边界 |
|---|---|---|
| 经给定点作给定直线的平行线 | Heath315末命题及设定；Fitzpatrick33末 | 原命题简写“给定点”，图示线外点；将A不在BC上写成显式输入条件属于教学补显，依据严格平行定义23 |
| 在BC上任取D，连接AD | Heath316首段；Fitzpatrick33末 | 为使用非退化角ADC，应有D不等于C；图示D在B、C之间，但无限直线上一般选点不必被误读为唯一指定点 |
| 在A以DA为基线复制角ADC，得角DAE | Heath316首段I.23边注；Fitzpatrick33–34跨页 | 两版图中E、C位于AD异侧；文字未另列该侧向选择。将其写成明确构造义务，是对下文“内错角”的条件展开 |
| 将EA沿直线过A延长至F | Heath316首段；Fitzpatrick34顶端 | A位于E、F之间，输出为完整直线EAF，不是只取一条任意角复制射线 |
| EAD与ADC为相等内错角，故EAF平行BC | Heath316第二段I.27边注；Fitzpatrick34 | DAE与EAD是同一普通无向角的反向命名；I.27为充分判据，不调用I.29逆向结论 |
| 构造可以排在I.27之后 | Heath316评论，转述Proclus p.376,14–20 | 评论强调平行判据的依赖；不能据“只依I.27”抹去显式角复制I.23及连接、延长的基础操作 |
| 唯一性可用I.30推出 | Heath316评论 | 假设两条互异直线均过A且平行BC，I.30使它们彼此平行，却在A相交，矛盾；I.30经I.29依赖第五公设 |
| 为先确立唯一性才将构造排在I.29、I.30之后 | Heath316评论中的“Presumably”及末段 | 是Heath对Euclid编排意图的推测，部分依据Proclus；不是Euclid正文的自述或已证明的历史事实 |

## 版本与适用勘误

Heath卷前ERRATA没有列出315–316页；Fitzpatrick I.31处未见专属修订脚注。两版的基本构造与引用一致。Fitzpatrick希腊字母Δ、Ε、Ζ分别对应英文字母D、E、F，不能把希腊Ζ误当英文Z。DAE/EAD角名转换是普通无向角的同一性，不是印刷错误。这里仅报告实际检查范围，不声称一切版次或传抄本均无误。

## 有来源的年代及前驱

- 约公元前300年的Euclid作品传统、Alexandria定位沿Fitzpatrick导论采用；单个命题没有据此获得确切发表日期。作品年代与1908、2008的所读版本年代分开。
- 书内直接前驱为I.23、I.27及连接/延长操作；I.29、I.30只在评论层解释唯一性，不能混入原构造的必要依赖。后续I.32使用本构造，不是本篇证明前提。
- Proclus评论的本次证据是Heath316的转述及所标p.376,14–20，未独立读取Proclus原书；不据此补造其原话、版本年份或首创权。
- Heiberg的1883–1885校本传统、Heath1908译注、Fitzpatrick2008修订本分别属于文本传播层。该短目录只展示可核实直接关系，不宣称同期研究或几何前史已穷尽。

## 明确不归给原文

有理坐标参数化、叉积侧向判定、点积角证书、复制错误侧向的数值反例、输入类型检查、机器核验、Notebook和有限枚举都是现代教学分析或真实计算。结果证书不是古代圆规直尺操作日志；欧氏坐标中的唯一性不说明第五公设可省。命题没有机器学习数据、基线或实验指标，有限程序运行不能代替一般证明或公理独立性证明。
