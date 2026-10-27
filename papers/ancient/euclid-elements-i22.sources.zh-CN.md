# 《几何原本》I.22：来源台账

## 版本与阅读范围

本篇是古代演绎几何的前史补读，不把它命名为现代 AI 论文。约公元前 300 年是《几何原本》传统成书背景的约略定位，不是可核实的 I.22 单篇发表日期。本台账列出实际核读的两个版本及一个便利转录，不声称穷尽抄本、古代注释或现代公理化研究。

1. **Euclid / T. L. Heath, *The Thirteen Books of Euclid’s Elements*, vol. I, Cambridge University Press, 1908。**[Internet Archive 扫描本](https://archive.org/details/thirteenbookseu02heibgoog)。实际逐页目视核读印页 292–294（该 PDF 从 1 计的第 313–315 页）：I.22 原证在 292 下部至 293 上部；Heath 评论在 293 下部至 294 上部。另核读印页 242（PDF 第 263 页）的 I.1 连续性评论。印页 295 的 I.23 评论只用于区分“按三长度作三角形”与“在指定位置作三角形”。扫描标识中的 `02` 不用作卷号。另检查该扫描 PDF 第 16 页 ERRATA：未见针对印页 292–294 的条目；这是对本版所附勘误表的有限检查，不是所有版本无误的断言。
2. **Richard Fitzpatrick, *Euclid’s Elements*, revised and corrected 2008（初版 2007）。**[作者提供的双语 PDF](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf)。实际核读印页 / PDF 页 25–26 的 I.22、图示与证明，并核读引言的编辑说明。希腊文依 Heiberg 1883–1885 年版；英文为 Fitzpatrick 译文。引言说明方括号标示 Heiberg 视为后加的文字，圆括号为英文译者补出的隐含成分。方括号不是本项目自行认定原文真伪的证据。
3. **Trinity College Dublin 的 Heath I.22 网页转录。**[命题页](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIProp22_Heath1908.php)。只作检索与阅读导航；网页把应连接的第二条线段转录为 `FG`，扫描原版与 Fitzpatrick 均为 `KG`。本篇采用经两版核对的 `KF、KG`，不以该网页转录覆盖扫描证据。

## 主张—证据定位

| 主张 | 位置 | 层次与约束 |
|---|---|---|
| 三给定线段任意两条之和大于第三条是必要条件 | Heath 292；Fitzpatrick 25，I.22 命题及 I.20 引用 | 原命题条件；非负或允许等号的版本不是这里的非退化三角形问题 |
| 共线点依次 D、F、G、H，DF=A、FG=B、GH=C | Heath 292；Fitzpatrick 25 | 原构造；I.3 用于截取等长线段 |
| 圆心 F 半径 FD，圆心 G 半径 GH；连接 KF、KG | Heath 292–293；Fitzpatrick 25 | 原构造；不是把任意现成底边预先固定位置 |
| KF=A、FG=B、GK=C | Heath 293；Fitzpatrick 26 | 原证明：同圆半径相等及等量传递 |
| 原证没有单独证明两圆必相交 | Heath 293 评论；对照两版原证 | Heath 明确指出的论证省略；作圆公设本身不等于保证圆交点 |
| Proclus 的相离 / 外切排除没有覆盖内含 / 内切 | Heath 293 评论 | 对古代注释的二手报告；本项目未独立校读 Proclus 原希腊文本 |
| 外点 H 与内点 M 可支持连续性交点论证 | Heath 294 评论，回指 I.1 注释印页 242 | Heath 的补足，而非冒充 I.22 原证；若用坐标与实数平方根说明，另标现代教学重构 |
| 至多两个交点、底边两侧两三角形 | Heath 294 评论，引 I.7 | 与存在性分开；镜像坐标及 SSS 同余说明可作现代重构，不倒灌入原证 |
| I.22 是该书首个 diorismos 例 | Heath 293 评论 | 限定为 Heath 对《原本》编排的观察，不是全人类最早提出可解条件的断言 |
| I.22 不指定构造位置，I.23 为指定角构造而使用它 | Heath 295 评论；Fitzpatrick 26 I.23 | 后继用途，不扩充为本篇已完成 I.23 的深读 |

## 需要保留的文本与数学边界

- Heath 认为解释必要条件的 I.20 说明句有注释混入正文的迹象，同时报告其见于所有抄本及 Boethius、而某些注释传统略去；这不是已经证明该句伪作。Fitzpatrick 的方括号应随其编辑说明理解。
- Heath 294 的内点讨论按两半径布局分情形。教学版本若令两圆圆心距为 B、第二圆半径为 C，可补上 C=B 时反向轴上点 M 恰为 F；补齐这一等长情形属于明示的教学整理。
- 严格三角不等式保证非退化交点；等号只给共线退化构形，违反不等式没有欧氏三角形。数值枚举与画图不能替代所有正实数上的存在性证明。
- 两个可视镜像解，不等于两个不同的 SSS 全等类型；固定底边、允许刚体运动以及是否保持定向，是不同的解计数约定。
- 本仓库仅发布原创中文解析、书目信息和必要链接；不发布扫描 PDF、整篇翻译或大段原文。
