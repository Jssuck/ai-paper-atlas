# Euclid《几何原本》I.1：来源与版本台账

## 阅读范围与版本原则

本单元精读第一卷命题1，并核对所需定义、公设、共同概念。原始作品约公元前300年；本次所读是后世校订、翻译和扫描，不是作者手稿。以下分开记录文本、编辑评论与现代研究，范围不等于穷尽版本史。未公开原版PDF、扫描图片或全文翻译。

### 1. Heath 1908第一版

Thomas L. Heath, *The Thirteen Books of Euclid’s Elements*, vol. I, Cambridge University Press, 1908。[原版扫描及书目](https://archive.org/details/thirteenbookseu02heibgoog)。

实读印刷页241—243：命题正文在241页开始、242页结束，其余为Heath评论。正文依次画两圆、取交点、连接两边、用同圆半径相等和共同概念1推出三边相等。它要求给出一个等边三角形，不要求枚举全部解。242页评注讨论相交的存在保证；243页讨论解的数量等问题。评论不是古代命题正文，也不是新发现的欧几里得自我批评。

另核看本扫描所附ERRATA页：其列出的第一卷订正页包括19、105、106、182、415，没有命题1所在的241—243页。本次仅报告这张勘误表的覆盖，不声称检查完全部后世版本或已排除一切异文。

导论第1页转述Proclus关于Euclid汇集、整理前驱成果的记述，涉及Eudoxus和Theaetetus；Heath也提醒欧几里得生卒信息有限。这是后世见证，不能推出某人原创I.1，亦不能建立亚里士多德与本命题的直接写作因果链。

### 2. Trinity College Dublin托管转录

- [命题I.1](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIProp01_Heath1908.php)：逐句核对上述正文，保留公设与定义引注。
- [定义](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIDefinitions_Heath1908.php)：核对定义15、16、19、20；其中15说明圆的中心到圆周的距离相等，19、20分类三边形与等边三角形。
- [公设](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookIPostulates_Heath1908.php)：读全部五条；本命题直接用第3条画圆、第1条连线。
- [共同概念](https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Heath1908/EuclidBookICommonNotions_Heath1908.php)：核对全部列项，直接使用第1条等式传递。

**转录出处警示：** 定义页面的URL路径带Heath1908，但可见标题出现Lardner1855，故不单凭URL认定其版本归属。定义内容另与[Clark大学定义15](https://mathcs.clarku.edu/~djoyce/elements/bookI/defI15.html)、[定义20](https://mathcs.clarku.edu/~djoyce/elements/bookI/defI20.html)及下列希英本交叉核对。正文引注的公设/共同概念`_Content.php`页面也实际打开检查，非臆造链接。

### 3. 希腊文与现代英译对照

Richard Fitzpatrick, *Euclid’s Elements of Geometry*，2007初版、2008修订订正版；希腊文本依据J. L. Heiberg 1883—1885校本重排，附Fitzpatrick新英译。[University of Texas托管PDF](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf)。实读版权/版本页、第一卷相关基础材料和印刷页8的I.1希英对照。

这是现代重排本，不称为1883原版影印。第8页的构造收束语对应“所要求作的已经作成”。同页脚注对相交许可提出现代编辑意见，不能混进Euclid正文。本文以Heath为主要译本、以此书核对结构及术语，没有制作或公开整页翻译。

### 4. 年代与传本

[Clay Mathematics Institute历史文献页](https://www.claymath.org/library/historical/euclid/index.html)将作品时代写为约公元前300年，并说明其展示的Bodleian MS D’Orville 301由Stephen the Clerk于公元888年为Arethas抄写。约前300年、888年、1883—1885年、1908年、2008年分别是作品估计、特定抄本、近代校本与译本的时间，不可合并为一个“发表年份”。本单元只为推理前史补读；没有给出全部前驱文献目录或穷尽性断言。

### 5. 当代形式化研究

Michael Beeson, Julien Narboux, Freek Wiedijk, *Proof-checking Euclid*, arXiv:1710.00787v2，[版本页](https://arxiv.org/abs/1710.00787v2)，[全文](https://arxiv.org/html/1710.00787v2)。采用v2版本记录日期2018-10-18；动态HTML生成日期不是论文年代。

实读§1和附录1的I.1形式证明：交点存在与非共线分别需要处理；附录先获得等边条件，再排除退化共线情形。本文只据此标出论证义务，不照搬其完整公理体系，也没有复现其Coq或HOL Light工程。

## 主张定位与原创部分

| 正文主张 | 来源位置或性质 |
|---|---|
| 两圆、交点、连线、半径等式、三边相等 | Heath1908 I.1，印刷页241—242 |
| 公设1、3及定义15、共同概念1的用途 | I.1边注与对应基础条目 |
| 交点存在值得单独处理 | Heath评注242页；现代论文§1及附录1 |
| 非共线义务 | 现代论文§1及附录1；本文坐标证明 |
| 只要求一个构造结果 | I.1题面与正文；Heath243页评论 |
| 约前300年与888抄本区别 | Clay历史文献页 |
| 前驱的编纂传统 | Heath导论第1页转述Proclus；不作具体构造归属 |
| 两支坐标公式、全部解、模3反证与失败案例 | 本文现代教学重构；不是原文引文 |
| Python和Notebook的结果 | 本仓原创附件实跑，不由古代来源背书 |

本文未以小实验证明一般定理；未以有理坐标失败例宣称建立全部欧几里得公设的独立性模型；未将古代图示习惯简化为“古人证明错误”。
