# Euclid《几何原本》I.8：来源与证据台账

## 版本与实际阅读范围

本单元是古代演绎方法前史的补读，不是现代 AI 论文。作品年代、传世命题、现代译注和本仓库的教学重构分别处理。

| 来源 | 版本与入口 | 实际阅读位置 | 用途与边界 |
|---|---|---|---|
| Heath 英译及评论 | Euclid, *The Thirteen Books of Euclid’s Elements*, translated with introduction and commentary by T. L. Heath, vol. I, Cambridge University Press, 1908。[扫描本](https://archive.org/details/thirteenbookseu02heibgoog) | I.8 正文印刷 261–262 页／扫描 PDF 282–283 页；评论印刷 262–264 页／PDF 283–285 页 | 实际目视原页和图。标识中的 `02` 不表示第二卷。区分命题正文、译者脚注、评论引用的古代证明。 |
| Fitzpatrick 希英对照 | Richard Fitzpatrick, *Euclid’s Elements of Geometry*, revised and corrected edition, 2008；希腊文本基于 Heiberg 1883–1885 年版。[PDF](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf) | I.8 印刷／PDF 14–15 页；第 15 页 I.9 中引用 I.8 的一段 | 实际读取文字并目视双栏。I.8 英文末尾结语跨至第 15 页，不应把完整范围记成仅第 14 页。不是 Euclid 手稿影印。 |
| Heath 卷首勘误表 | 同一 1908 年扫描本 | PDF 第 16 页 | 逐项目视；未列出 I.8 或印刷 261–264 页的修正。此结论仅限该表，不表示所有版本、后续研究均无问题。 |
| Clay Mathematics Institute 历史档案 | [《原本》历史版本入口](https://www.claymath.org/library/historical/euclid/index.html) | 作品、抄本与文本来源说明 | 作品约公元前 300 年；D’Orville 301 抄本抄于公元 888 年。两者均不是 I.8 发现日期。 |

本台账仅公开原创概述与必要书目链接，不复制扫描页，不提供原文或译注的全文翻译。没有宣称校勘全部手稿或穷尽所有前驱。

## 主张—证据定位

| 主张 | 精确位置 | 解释纪律 |
|---|---|---|
| 条件是三组指定对应边相等；目标是两等边所夹的角相等 | Heath 261；Fitzpatrick 14 | AB 对 DE、AC 对 DF、BC 对 EF，目标 BAC 对 EDF。不能用无序长度集合代替指定点对应。 |
| I.8 没有在结语直接追加所有余角相等和三角形相等 | Heath 262 正文及紧随的评论；Fitzpatrick 14–15 | Heath 特意指出此范围，并解释余下结论可再由 I.4 得到。其所谓 vertical angles 指这里的顶角，不是相交两直线的“对顶角”。 |
| 底边叠合时 B 放到 E，BC 沿 EF，等长使 C 落到 F | Heath 261 末段；Fitzpatrick 14 中部 | 必须保持端点方向。将 B 错放 F 会改变指定对应关系。 |
| 假定叠合后的顶点另在 G，由 I.7 排除 | Heath 262 第 18–33 行附近；Fitzpatrick 14 下半 | I.7 要求同一底边、同侧、两端分别相等。叠合安排使顶点处于同侧是必要的解释环节；正文并未另立运动公理逐条证明这一操作。 |
| 角重合因此相等 | Heath 262 第 34–35 行附近；Fitzpatrick 14 末段 | Fitzpatrick 显式标注公理／共同概念 4；不要把“重合”当作三边相等后的无依据跳步。 |
| 原证使用叠合，且依赖 I.7 | 两版上述证明 | 现代坐标、Gram 矩阵或正交矩阵证书是另一套明示基础下的教学重构，不是传世原文。 |
| Philo 的替代证明以异侧叠合及三个图形情况避开 I.7 | Heath 263–264 的专节 | Heath 经 Proclus 转述：共线、内角、外角三类，使用等腰三角形底角和角的加减。不得误称为 Euclid I.8 正文，也不因其避开 I.7 就说它避免了叠合。 |
| Aristotle 的彩虹讨论与该命题有历史关联 | Heath 262–263，指向 *Meteorologica* III.3，373a5–16 | 本单元只核查 Heath 的转述，没有单独校读 Aristotle 原文。Heath 不赞同仅凭该段语言推断前 Euclid 命题的原始结论；不能把转述升级为确定的发现史或传承链。 |
| I.9 调用 I.8 证明构造出的两角相等 | Heath 264；Fitzpatrick 15 | 只作后续依赖定位，不等于本轮已完成 I.9 深读。 |

## 版本细节与边界

- Fitzpatrick 希腊栏的辅助点为 Η，英语图的对应标签为 G；这属于字母对应方案，不是两个不同的几何论证。正文统一使用英语图的 A、B、C、D、E、F、G。
- Heath 262 的行文脚注说明其正文 `BA, AC` 对应文本中的 `BA, CA`；这里线段无向，不改变长度条件或证明目标。
- 原始结论不能不加说明改写为“只准平移旋转即可重合”。异向三角形可能需要反射；现代全等通常允许这种等距变换。补显同侧安排不等于偷用待证的 SSS。
- 非退化三角形、不同底边端点、严格正的面积是教学建模应明示的范围。零边、共线三点不自动包含在原文命题中；对这些输入的程序拒绝是模型边界检查，不是古代原文算法。
- 有限枚举和有理数算例只能检查实现及所枚举的输入；一般结论必须来自逐步论证，不能由测试次数替代。

## 关联文件

- [中文深读](euclid-elements-i8.zh-CN.md)
- [独立来源审查](euclid-elements-i8.source-audit.zh-CN.md)
