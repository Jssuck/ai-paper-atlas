# 《几何原本》I.24：来源台账

## 版本与实际阅读

本条为古代演绎几何的 AI 前史补读，不是现代 AI 论文。约公元前 300 年仅是《原本》传统成书背景的约略定位，不是 I.24 的独立发表年。本台账不声称穷尽版本、注释及现代公理化研究。

1. **Euclid / T. L. Heath, *The Thirteen Books of Euclid’s Elements*, vol. I, Cambridge University Press, 1908。**[扫描本](https://archive.org/details/thirteenbookseu02heibgoog)。实际逐页目视核读印页 296–299（所用扫描 PDF 从 1 计第 317–320 页）：I.24 命题与原证在 296 下部至 297 上部；图形分类、Simson 增补、补足位置论证及替代证明在 297–298；面积评论跨至 299 顶部。另查看所附 ERRATA（PDF 第 16 页）：没有针对这些印页的条目；这不是不存在其他勘误的断言。扫描标识中的 `02` 不是本书卷号。
2. **Richard Fitzpatrick, *Euclid’s Elements*, revised and corrected 2008，初版 2007。**[作者双语 PDF](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf)。实际目视核读印页 / PDF 页 27 的 I.24 英希对照文本和图，以及 28 页顶部的结句；并对读 28 页 I.25 对 I.24 的依赖标注；英语标注 I.23、I.3、I.4、I.5、I.19。希腊文据 Heiberg 1883–1885 年版，英语为 Fitzpatrick 译文。现代译本不等于未经传承变动的古代手稿。

3. **Trinity College Dublin，Heath I.24 网页转录。**[命题页](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIProp24_Heath1908.php)。实际读取其完整命题与证明，交叉核对原证引用次序；此页不含 Heath 的上述图形分类评论，不能用它替代扫描本评论。

## 主张与证据位置

| 主张 | 位置 | 层次与限制 |
|---|---|---|
| 两对边对应相等时，较大夹角对较大第三边 | Heath 296；Fitzpatrick 27 | 原命题；不是仅一对边相等，也不是比较任意非夹角 |
| 在 DE 的 D 端复制 BAC 为 EDG，再取 DG=DF | Heath 296；Fitzpatrick 27 | 原构造；教学需补明与 F 同侧及 DF 射线处于 EDG 内部的选择 |
| BC=EG | Heath 297；Fitzpatrick 27 | I.4 的两边及夹角全等；不是使用尚待证的比较结论 |
| DF=DG 推出角 DFG=角 DGF | 同上 | I.5；原图中再由角的包含关系得到角 EFG>角 EGF |
| 由角 EFG>角 EGF 得 EG>EF | 同上 | I.19；将等量 EG=BC 代入即结论 |
| 未加长度约定时还存在另两种配置 | Heath 297 评论 | 一种 E-F-G 共线；一种 F 在三角形 DEG 内。后者用 I.21 比较 DF+FE 与 DG+GE，再消去相等长度 |
| Simson 添加 DE 不大于 DF 的约定 | Heath 297 评论 | 后世增补，不应作为欧几里得原文转述；Heath 刻意未将它纳入所译原命题 |
| 增补长度约定后仍须证明 F 的位置 | Heath 298 评论 | 令射线 DF 交 EG 于 H，I.16、I.18、I.19 给 DH<DG=DF；故 H 位于 D 与 F 之间 |
| 角平分线提供另一种比较证明 | Heath 298，Alternative proof | Heath 所列现代替代法，不是原证；由 SAS 得 HF=HG，再用三角不等式。共线退化须单列处理 |
| 底边比较不能无条件升级为面积比较 | Heath 298–299 评论 | Heath 转述 Proclus 的问题与讨论；未独立校读 Proclus、an-Nairizi 或 Heron 原文本，不能把此转述当作直接古代原典核验 |
| I.25 证明调用 I.24 | Heath 299 | 仅核对依赖方向；不能拿 I.25 作为本篇 I.24 的前提 |

## 重构边界与审读提醒

- “大角压住小角”的移置必须选对半平面。仅说“作相等角”不足以确定所需图形。原图含有位置关系，教学重构应把它们显写为条件或给出证明。
- 在约定 DE≤DF 后，先得到射线 DF 位于角 EDG 内部，因而与线段 EG 相交于 H；再用长度链判明 F 在 H 之后。不能先把 F 画在外面，再以所画位置证明同一位置。
- 原证只给典型图；Heath 补述其他情况。三情况应按 F 相对线段 EG 的位置分为外侧、边上、内部，不应把“图的上方/下方”当作坐标无关的定义。
- 对内部情况的 I.21 使用，应确保 F 是三角形 DEG 的严格内点；对共线边界则直接使用线段加法，不能套严格内点定理。
- 用数值角、点积、平方距离、参数化圆或精确有理数检验，是现代教学分析或实跑，不是原文算法。有限检验不能证明一般定理；余弦定理可作旁证，不能替代原证与图形分类。
- 面积可能随夹角增大而增大、相等或减小；这与底边的严格比较不同。涉及正弦或面积公式时应标作现代说明。
- 人物归属只采用可核验版本中的明确陈述；本篇不建立作者、机构或文明的“第一”排名。公开成果仅为原创中文分析、必要书目链接、自有教学代码与经检查的运行证据，不附扫描 PDF 或全文翻译。
