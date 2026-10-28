# Euclid I.33 来源台账

核查日期：2026-10-28。范围为I.33完整命题、证明、直接相关译注与必要前驱。属于AI推理与数学前史补读，不称古代命题为现代AI论文，不声称前史穷尽。扫描与页图仅内部阅读，不随公开稿发布。

## 实读版本与定位

| 来源 | 实读范围 | 核查方式 |
|---|---|---|
| T. L. Heath，*The Thirteen Books of Euclid’s Elements*，vol. I，Cambridge University Press，1908 | 印322末命题及设定；323全部I.33证明与评论，止于I.34标题；卷前ERRATA | 已渲染并目视PDF页序343–344、16（1起算），不是仅据OCR；此PDF无可用文本层 |
| Richard Fitzpatrick，*Euclid’s Elements of Geometry*，revised and corrected 2008 | 印/PDF35下半至36上部完整I.33及两脚注 | 已读希英页图与英文文本；希腊字母序仅核此处，不声称独立校勘古代手稿 |
| Trinity College Dublin，Heath I.33转录 | 完整网页正文 | 实际访问交叉核查命题、I.29/I.4/I.27及对应序；网页不含Heath评论 |

直达：[Heath扫描](https://archive.org/details/thirteenbookseu02heibgoog)；[Fitzpatrick希英本](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf)；[TCD I.33](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIProp33_Heath1908.php)。本次复用此前取得的PDF重新渲染指定页；可打开链接不等于已经阅读。

## 主张—证据—边界

| 主张 | 证据位置 | 解释边界 |
|---|---|---|
| 等长且平行的两线段，连接同方向端点的两线段也等长平行 | Heath322末；Fitzpatrick35命题 | “同方向端点”不是说任意配对均可；AB与CD作为有向向量同向是本稿现代接口表达，非古代向量原式 |
| 以AB、CD为已知，AC、BD为待证连接线 | Heath322末–323首行及图；Fitzpatrick35 | 原图四点顺序沿边界为A-B-D-C；不能换成自交连接却保留同一证明 |
| 加辅助线BC | Heath323第8行附近；Fitzpatrick35 | 公设1式连线；不是预先调用平行四边形性质 |
| ABC与BCD是相等内错角 | Heath323第9–12行，边注I.29；Fitzpatrick35 | 平行前提与端点位置共同确定内错角角色；I.29含第五公设依赖 |
| AB=DC、BC=CB及夹角等使ABC与DCB按A↔D、B↔C、C↔B对应 | Heath323第13–20行及对应序评论；Fitzpatrick35 | I.4一次调用同时给AC=BD及角ACB=CBD；不能把字母顺序误作任意对应 |
| 由ACB=CBD得到AC平行BD | Heath323第21–25行，边注I.27；Fitzpatrick35 | 第二次使用BC作为截线，但被截两线已改为AC、BD；原文并非从等长直接推出平行 |
| I.33承接平行理论并引入平行四边形研究 | Heath323末评论，引用Proclus p.385,5 | 本次只读Heath转述，未直接核读Proclus；I.34是后续而非I.33证明前提 |

## 译法、字母序与适用勘误

Heath323第一注说明，命题中“在相应方向的端点”这一括号补足是为澄清含义；希腊原措辞可译为向同一方向或在相同侧。他认为“towards the same parts”不甚满意。本稿据原图与证明解释端点配对，不把Heath括号当原希腊逐字内容。

Heath323第二注明确：两组边和三角形的希腊排列分别为BC、CD及BCD；英译改成DC、CB及DCB，以按全等对应排列。他指出Euclid往往偏好字母序，而未始终按对应点排序。这是表示习惯与教学排版问题，不应无条件宣称Euclid的SAS推理错误。

Fitzpatrick35英文同样用DC、CB及DCB，并在36附两处“mistake”脚注。第一脚注所报BC、CD与Heath相合；第二脚注字面称希腊为DCB，但35左栏实际为ΒΓΔ（BCD），亦与Heath所报BCD相合。因此第二脚注的字母序存在自身疑误：本稿保留这一差别，不据此虚构古代手稿异文，也不无声改写版本。几何对应关系独立由角、边位置核定。

Heath卷前ERRATA未列322–323页。此结论只覆盖本次核查的页，不宣称所有版本无误。

## 年代、前驱与后继目录

- 作品按Fitzpatrick导论传统定位约公元前300年；不能为I.33编造精确写作或发表日。1908及2008是本次阅读的版本年代。
- 直接书内前驱：I.29把已知平行转换为夹角相等；I.4以两边夹角推出另一边和对应角相等；I.27从另一组内错角相等转回平行。第五公设经I.29间接进入；I.33不是独立于全部平行公设的结论展示。
- 后继I.34研究平行四边形对边、对角与对角线分割。Heath依Proclus所说的“连接”解释篇章组织，而不是给出独立发现年代。
- 本目录只展示本单元可核实的直接关系，不按作者声望增加或降低证据要求，也非穷尽几何或AI前史。

## 非原文内容

向量等式、叉积判别、严格输入类型、JSON证书、反向端点反例及Notebook测试为现代教学与工程核验；不冒充Euclid原符号、原实验或机器学习经验研究。现代欧氏坐标已选定模型，有限实跑不证明一般定理，也不证明第五公设可删除。
