# 《几何原本》I.25：来源与主张位置台账

本台账记录实际阅读范围及本文原创解释所依据的位置。它不是原文翻译、手稿校勘全集或穷尽性书目。日期约为公元前300年是作品通常采用的历史定位，不是本命题可考的发表日期。

## 一、版本及核看范围

1. **T. L. Heath，1908，卷 I。** *The Thirteen Books of Euclid's Elements*，Cambridge University Press。[扫描本](https://archive.org/details/thirteenbookseu02heibgoog)。实际核看印页299–301（所读PDF第320–322页），以及前置ERRATA（PDF第16页）。I.25完整命题及证明在299；300–301为编译者列出的评论及替代证明。301下部开始I.26，不算本篇完成范围。
2. **Richard Fitzpatrick，2008修订版。** *Euclid's Elements of Geometry*，初版2007；希腊文据J. L. Heiberg的1883–1885年版，附现代英文。[作者托管PDF](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf)。I.25全文在印页/PDF第28页；前一命题末句与后一命题开头同页，均不改变I.25的边界。导言印页4用于作品背景和版本说明。
3. **Trinity College Dublin，Heath正文转录。** [I.25网页](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIProp25_Heath1908.php)。用于对读，而不是取代扫描本。读取日期：2026-10-27。

公开仓库仅存原创分析、必要链接、自有教学代码与运行证据，不存上述PDF、扫描页或全文翻译。

## 二、版本问题

- TCD转录在第一次排除等角后的结句使用角名DEF；Heath印页299的扫描同句是EDF，Fitzpatrick印页28也是EDF。给定相等边为DE、DF，夹角顶点必须为D。因此正文采用EDF，并显式报告这一转录差异，不把网页误写归为欧几里得原证缺陷。
- 已核看的Heath附录ERRATA未列印页299–301的更正。这个结论仅涵盖该扫描本所附清单，不表示全部印次、译本和研究传统都没有勘误。
- Fitzpatrick为2008修订版；I.25本页没有额外校注脚标。本篇未声称完成该书所有版本的校勘检索。

## 三、主张与证据位置

| 正文主张 | 直接位置 | 证据层次与限制 |
|---|---|---|
| 两对对应边分别相等且底边较大，推出两边所夹角较大 | Heath印299命题及设定；Fitzpatrick印28命题及设定 | 原命题；“底”是该夹角对边，非纸面方向 |
| 等角分支导致底边相等 | Heath印299，图后第一排除段，旁标I.4；Fitzpatrick印28标Prop.1.4 | 原证调用SAS，不是用角相等单独推边相等 |
| 较小角分支导致底边较小 | Heath印299第二排除段，旁标I.24；Fitzpatrick印28标Prop.1.24 | 教学展开须交换两个三角形的角色 |
| 排除相等和较小后得到较大 | Heath印299开头分支句与最后归结；Fitzpatrick印28同结构 | 原文使用可比较角量的次序；三分表是教学显写，不是逐字公设 |
| I.25以及I.8可从I.4与I.24的三种对应关系作逻辑恢复 | Heath印300首段及两组三行分类 | Heath援引De Morgan的后世分析；不声称历史上I.8原证依赖I.24 |
| Proclus传述两种直接证明 | Heath印300说明段，标Proclus pp.345–7 | 本篇只核Heath转述，未独立校读Proclus完整文本 |
| Menelaus路线以截段、复制角、全等、等腰及交点比较角 | Heath印300“Proof by Menelaus of Alexandria” | 正文为结构概述；未声称补全所有交点、角相加的位置条件 |
| Heron路线以两个圆构造第三边相等的三角形，再比较角包含 | Heath印301“Heron's proof” | 正文为结构概述；圆交点存在与选侧仍是完整重建的义务 |
| 约前300年、亚历山大里亚的作品背景 | Fitzpatrick导言印4 | 不据此确定I.25个人发现者或独立年代 |

## 四、哪些是本篇新增内容

正文的符号H、三分表、Gram矩阵/点积模型、手算例与删前提反例、与自动推理的联系、证书格式及测试均为现代原创教学重构或分析，不是古代原文。余弦单调性与平方距离展开属于现代欧氏模型，不替代原证的I.4/I.24依赖。

本篇“前驱”首先指已核实的书内逻辑依赖。Heath、De Morgan、Proclus、Menelaus及Heron的后世讨论不被倒置为欧几里得的前驱或同时代证据。没有足够材料为I.25断定首创者，也不补造所谓同期竞争文献。

有限运行只核查实现与样例，不证明一般定理。真实命令、环境、结果和独立核验范围见[复现目录](../../reproduction/euclid-elements-i25/README.md)；一般证明与各层次区分见[深读正文](euclid-elements-i25.zh-CN.md)。
