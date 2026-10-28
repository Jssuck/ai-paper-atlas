# Euclid I.36 来源台账

核查日期：2026-10-28。收录范围为完整I.36及Heath对I.36/37评论的直接关联部分，作为AI推理与数学前史补读；不把古代命题称作现代AI论文，不声称穷尽前史。作品传统年代约公元前300年，不是本命题可精确确定的写作日期。扫描PDF及页图仅供私下核读，不公开。

## 书目、版本与实读范围

| 来源 | 本次实际核读 | 边界 |
|---|---|---|
| T. L. Heath，*The Thirteen Books of Euclid’s Elements*，vol. I，Cambridge University Press，1908 | 印331完整I.36；印332末至333的I.36/37评论，止于I.38标题；卷前ERRATA | PDF352–354及16页重新目视；332的I.37正文仅为定位评论边界，不计本次完成I.37 |
| Richard Fitzpatrick，*Euclid’s Elements of Geometry*，revised and corrected 2008 | 印/PDF37末命题与设定，38上半图形及完整I.36证明 | 希英排印并看，核对译者引用号；不声称校勘古代手稿 |
| Trinity College Dublin，Heath I.36正文转录 | 完整命题与证明网页 | 作为原证次序交叉核查，不替代扫描评论与勘误 |

直达：[Heath扫描](https://archive.org/details/thirteenbookseu02heibgoog)、[Fitzpatrick希英本](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf)、[TCD I.36](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIProp36_Heath1908.php)。1908与2008是实读版本年代，不是古代成书年份。

## 主张—证据—解释边界

| 主张 | 证据位置 | 限定 |
|---|---|---|
| 等底且处于同一对平行线间的平行四边形等积 | Heath331命题、设定；Fitzpatrick37末 | 不要求两底是同一线段，也不意味着目标四边形全等 |
| 两目标为ABCD、EFGH，底BC、FG，边界直线AH、BG | Heath331设定及图；Fitzpatrick37末–38图 | AH/BG是原图直线命名，跨图形点重合时可换用不同点标同一直线；不能把退化的点对当作直线 |
| 加入BE、CH构造中介EBCH | Heath331证明首句；Fitzpatrick38 | 是连接既有端点，不是先用等积结论创造中介 |
| BC=FG且FG=EH，故BC=EH；BC与EH又平行 | Heath331证明前段；Fitzpatrick38明确在FG=EH旁标I.34 | FG=EH来自第二平行四边形的对边相等；长度传递用共同概念1 |
| 同向端点连接保证EB、HC平行，从而EBCH为平行四边形 | Heath331中段I.33；Fitzpatrick38 | I.33方向条件不可省；反向或交叉配对不能照搬 |
| 第一次I.35以BC为共同底比较ABCD、EBCH | Heath331下段；Fitzpatrick38 | 两者同在原两平行线间，必须核实中介已经满足平行四边形条件 |
| 第二次I.35以EH为共同底比较EFGH、EBCH | Heath331倒数证明段明确标I.35 | 原文说“同理”；共同底由BC换成EH是教学展开，不是与原命题冲突 |
| 两目标通过共同中介等积 | Heath331末，共同概念1；Fitzpatrick38 | 等积传递不要求三图重叠，不是全等传递 |
| Proclus的I.36/37注释存在缺文 | Heath332末评论首段 | Heath说看似前一注结尾及后一注开头缺失；后续对缺失内容的重构不能写成现存原文已明说 |
| 周长本身不是面积的判据 | Heath332末–333首，含城市/土地等事例转述 | 历史事例通过Heath转述Proclus、Cantor等，不声称独立核对各古籍；这些事例不用于证明I.36 |
| 等周比较另有数学传统 | Heath333中段Theon、Zenodorus、Pappus介绍 | 是相关评论；不把其中圆/球极值命题当作本次已证明，也不把Heath的宽年代估计改成确定生卒年 |

## 引用号与勘误核查

Fitzpatrick38在第二次比较EFGH与EBCH相等的句末印为“Prop. 1.34”。本次交叉核读Heath331（该处为I.35）并检查命题内容：这里所需的是同底EH、同平行线间的等积命题I.35，I.34不能直接给出两不同平行四边形的等积。因此将此处记为所读译本的引用号疑误，正文按数学依赖明确使用I.35；不据此宣布古代定理错误。

Heath331把一个I.34旁注排在“EBCH是平行四边形”句旁。I.34确用于较前的FG=EH；而EBCH为平行四边形由两组对边平行判定。这里记录排印位置和实际依赖，不把旁注位置直接升级为已证实的正文错误。

已目视Heath卷前ERRATA，本表条目不涉及印331–333。这个结果不代表所有版本都无错误。I.37中“相等量之半相等”的插文讨论位于332脚注，属于下一命题，不误标为I.36文本的插文。

## 公开与教学范围

公开原创中文分析、上述必要书目链接、自有教学代码与实跑证据。参数化坐标、行列式等式、端点重合/重叠/分离的系统分类，以及程序证书，均是教学重构；不能声称Euclid原文采用现代代数、机器核验或已给出本程序的形式化证明。原文的中介构造和两次同底归约保持独立于数值面积公式。
