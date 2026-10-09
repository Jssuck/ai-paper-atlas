# Sheffer1913来源、逐页证据与校勘账本

核验日期：2026年10月9日。主文：[五公设精读](sheffer-five-postulates.zh-CN.md)。本文件记录实际来源和阅读范围，不把取得书目、取得全文、读过指定页、逐式证明和程序测试视为同一种完成状态。

## 1 主文本与版本身份

Henry Maurice Sheffer, *A Set of Five Independent Postulates for Boolean Algebras, with Application to Logical Constants*, **Transactions of the American Mathematical Society 14(4), October 1913, 481–488**。

- [JSTOR稳定项](https://www.jstor.org/stable/1988701)，[DOI 10.2307/1988701](https://doi.org/10.2307/1988701)：书目确认卷、期、月份及页码。
- [AMS DOI](https://doi.org/10.1090/S0002-9947-1913-1500960-1)：作者、题名、卷页由[出版社提交的Crossref元数据](https://api.crossref.org/works/10.1090/S0002-9947-1913-1500960-1)交叉核验。Crossref只给年，不用其缺失的月日覆盖JSTOR与原刊页眉。
- [实际使用的原刊扫描](https://archive.org/download/jstor-1988701/1988701.pdf)：9个PDF页，现代JSTOR说明封面1页，正文8页。全文获取、文字提取和逐页图像阅读均完成；公开仓库不镜像PDF。
- [另一份AMS盖印复制本](https://scispace.com/pdf/a-set-of-five-independent-postulates-for-boolean-algebras-8tk8kv2l82.pdf)：仅用可提取文字交叉检查，未声称第二套全页图像比对。托管页面自动生成的April 1日期不采纳；原刊页眉与JSTOR支持October。

题名中的Application为单数，Algebras为复数。481页报告日是1912年12月31日，488页Cornell署稿为1913年2月，二者不是1913年10月刊期。完整书目与三个日期在主文分别标注。

## 2 主论文逐页阅读记录

每行“已核”均包括实际查看该页扫描图像，不仅依赖OCR。PDF页序按上述9页文件计数。

| 原页 | PDF页 | 本页内容与已核位置 | 主文使用方式 |
|---:|---:|---|---|
| 481 | 2 | 题名、作者、引言第一段；报告日、复数algebras、前驱书目、K-rule及K-closed定义脚注 | 第1、2节；区分定义域与值域、一般模型与两元素模型 |
| 482 | 3 | 五公设全部；a′定义；P3–P5的“indicated combinations”条件；existence与closing分类 | 第2节完整解释，P2反模型不得删掉这些条件 |
| 483 | 4 | P1′；二元素一致性模型；五个独立性模型；三元素表；定理A、B、Ia | 第3节每个反模型的具体失败及保留条件；第4节目标 |
| 484 | 5 | Ib–V全部陈述；A、B证明及Ia/Ib封闭步骤；脚注C–G | 第4、5节；G疑似缺竖线单列校勘；不把省略证明当作作者已经逐步写出 |
| 485 | 6 | IIa、IIb、IIIa、IIIb、IVa、IVb、V证明 | 第5节逐步重构单位、交换、互分配及补元 |
| 486 | 7 | Huntington十条公设重列；双向定义；代数对偶脚注；逻辑应用开头 | 第5.6、6节；反向省略计算用现代布尔定律补齐并标明前提 |
| 487 | 8 | 同类型命题解释；rejection为neither-nor；定理1两方向定义；PM页码脚注 | 第7.1、7.2节；主解释NOR，原楔形符号改记↓并声明 |
| 488 | 9 | PM *1.7、*1.71；定理2及三方向证明；结论；署稿日期；逻辑NAND对偶脚注 | 第7.3节；构造合法命题不等于推导真理，NAND为明示对偶 |

## 3 原式、教学重构与证据强度

### 完整原公设骨架

原始对象是类K与binary K-rule。撇号是定义 $`a'=a\mid a`$；五公设为非平凡性、封闭性以及带K成员条件的三个等式：

```math
(a')'=a,\qquad a\mid(b\mid b')=a',\qquad
(a\mid(b\mid c))'=(b'\mid a)\mid(c'\mid a).
```

本稿先按原文保留适用条件，再在同时采用封闭公设后简写等式。代码的外部值标记、语法树和输入验证是现代实现约定，不是原文原始对象。

### 主证明的加工范围

- A：原文484页等式链；主文改成P5第二、第三变量同取b′的展开，再对两边取撇号。
- B：原文484页五行链；主文引入临时缩写t_a、t_b，显示P4与A怎样使它们的撇号相等。临时缩写不新增公设。
- IIa/IIb：原文485页构造z、u；主文额外补出单位唯一性短证，明确标成补充。
- IVa/IVb：原文485页两条证明均逐式解释，而非仅以对偶口号代替。
- V：原文取补元为a′；主文解释其与独立存在公设的区别。
- 反方向：原文486页仅给定义后宣布蕴涵；主文用已有布尔代数的幂等、德摩根和分配律写出计算，不声称从未读的Huntington所有步骤重新建立这些基础。
- 定理1、2：原文487–488页定义及构造封闭证明完整解释；结构归纳、析取范式、零元函数语法限制、公式与等价类区别是本文现代教学补充。

本稿未提供证明助理形式化认证。有限代码测试不作为上述一般数学证明的替代。

## 4 有界前驱与后继核查

### Huntington1904

Edward V. Huntington, *Sets of Independent Postulates for the Algebra of Logic*, **Transactions AMS 5(3), July 1904, 288–309**。

- [JSTOR与DOI 10.2307/1986459](https://www.jstor.org/stable/1986459)。
- [AMS DOI 10.1090/S0002-9947-1904-1500675-4](https://doi.org/10.1090/S0002-9947-1904-1500675-4)。
- [原JSTOR扫描的Iowa State镜像](https://home.engineering.iastate.edu/alexs/classes/2015_Fall_281/readings/Huntington_1904.pdf)。

实际核查为带原页码的提取文字：288–291背景与多种系统，292–293第一组十条，294相关推论与对偶，296独立性模型方法，306–307第三组单一组合规则。另以Sheffer486页原图核对其重列的第一组。镜像本地下载被主机拒绝，未宣称逐符视觉比对Huntington原图或全篇证明审计。

关键历史限制：Huntington第三组已经只用一种组合规则，因此不能把Sheffer写成第一个采用单一未定义二元规则的人。本篇具体进展是新的rejection公设组、条数经济性及特殊元素的定义构造。

### 更早书目线索

以下只核为Sheffer481页的实际引文，没有由此宣称读完这些著作：

- Boole，*An Investigation of the Laws of Thought*，London，1854。
- Schröder，*Vorlesungen über die Algebra der Logik (Exakte Logik)*，第一卷，1890。
- Whitehead，*A Treatise on Universal Algebra*，第一卷，1898，35–37页。
- E. Müller，*Abriss der Algebra der Logik*，第一部分，1909，20–21页；Sheffer用它定位分散于Schröder原书的公设表。

没有进行Peirce未刊手稿或全部逻辑史优先权调查。书目最早年份不自动成为下一篇已确认可精读论文，也不能用本轮来源窗口宣称“最早发明”。

### Whitehead–Russell1910第一版

*Principia Mathematica*，第一卷，Cambridge，1910，94–101页。

实际读的是[Project Gutenberg的有原页码转录](https://www.gutenberg.org/files/78050/78050-src/78050-src.htm)，并以关联1910扫描的Wikisource逐页转录交叉对照：[94页](https://en.wikisource.org/wiki/Page:Russell,_Whitehead_-_Principia_Mathematica,_vol._I,_1910.djvu/116)、[95页](https://en.wikisource.org/wiki/Page:Russell,_Whitehead_-_Principia_Mathematica,_vol._I,_1910.djvu/117)、[97页](https://en.wikisource.org/wiki/Page:Russell,_Whitehead_-_Principia_Mathematica,_vol._I,_1910.djvu/119)、[101页](https://en.wikisource.org/wiki/Page:Russell,_Whitehead_-_Principia_Mathematica,_vol._I,_1910.djvu/123)。

94–95页区分原始观念与原始命题、经济性与最低性的不同；97页列否定与包含性析取；98页定义材料蕴涵；101页列*1.7与*1.71，且还存在其他原始命题。没有把1925再版内容倒灌到1913的引用，也没有声称本轮完成该书原图审计。转录中一条无关*1.4公式疑似错误，因此不用于本文论证；所需*1.7、*1.71也可直接在Sheffer488页图像交叉核验。

### Schönfinkel1924的直接衔接

M. Schönfinkel，*Über die Bausteine der mathematischen Logik*，**Mathematische Annalen 92 (1924), 305–316**。

[EuDML书目](https://eudml.org/doc/159074)；[LMU镜像原刊扫描](https://www.cip.ifi.lmu.de/~langeh/test/1924%20-%20Schoenfinkel%20-%20Ueber%20die%20Bausteine%20der%20mathematischen%20Logik.pdf)。本轮亲自核图306页，未另起全文研究。该页脚注2直接引Trans. AMS14 (1913),481；正文局部采用NAND，写出重复输入实现否定及两个否定的NAND实现析取。镜像现代封面的自动1869字段不采用；出版年按原刊书目1924。

这足以支持具体引文关系，不足以证明1913到任何现代AI方法的直线因果影响。仓库既有1924全文精读记录仍独立保留。

## 5 后续修正检索与不完全独立性

### 本轮未找到正式勘误的准确含义

检索包括JSTOR文章元数据和参考条目、Crossref出版社记录，以及题名或缩短题名搭配correction、errata、erratum、corrigendum、corrigenda的公开搜索，另含AMS限定检索及Sheffer/484/error/correction/misprint窄查询。Crossref未显示relation或update-to关联；这对旧论文只是较弱的否定证据。

直接AMS文章、PDF和相关期目录多次返回403或不可用。未逐期检查所有后续AMS卷册，故仅能说**在上述范围未定位到适用的正式勘误**，不能说历史上不存在勘误。检索出现的Huntington1933 *Boolean Algebra. A Correction*，35卷557–558页，针对其1933论文274–304页，不适用于本篇或Huntington1904。[AMS1933期目录](https://www.ams.org/tran/1933-035-02/)

### Taylor1920是加强要求，非推翻五条普通独立性

J. S. Taylor，*Sheffer's Set of Five Postulates for Boolean Algebras in Terms of the Operation “Rejection” Made Completely Independent*，**Bulletin AMS26(10), July1920,449–454**，[DOI 10.1090/S0002-9904-1920-03334-3](https://doi.org/10.1090/S0002-9904-1920-03334-3)。

核对出版社提交的Crossref书目及[AMS盖印原文复制本](https://scispace.com/pdf/sheffer-s-set-of-five-postulates-for-boolean-algebras-in-34ru63fbk0.pdf)449–450页。449页肯定普通独立性并引Dines先前的诊断；450页说明P1失败迫使P3–P5成立，并将最少元素数改为四。完全独立要求实现五条的全部32种真假模式；普通独立只要求每条“独自失败”的模型。

本轮未读完Taylor六页或核验全部模型。其449页脚注给出L. L. Dines，*Complete Existential Theory of Sheffer's Postulates for Boolean Algebras*，**Bulletin AMS21 (January1915),183–188**。Dines全文未在本轮取得或精读，此处是经Taylor原文核实的引文线索，不冒充Dines全文核验。

主文第3.8节另给最多一个K元素时的短论证，以帮助理解完全独立为何不成立。这不改变Sheffer原五个独立性反模型的有效性。

### 484页脚注G的疑似排印遗漏

原扫描G的右端可见a后直接接(b竖线c)，中间未见竖线；另一份复制本的提取文字也缺该符号，未获得第二套可做逐像素比较的原图。主文只记录观察和一种自然的教学重构，不宣布已取得作者勘误。

拟补为 $`a\mid(b\mid c)`$时，在NOR解释下左侧为

```math
(a'\mid a)\mid[(b'\mid a)\mid(c'\mid a)]
=0\mid[(b\wedge\neg a)\mid(c\wedge\neg a)]
=\neg a\wedge(b\vee c)
=a\mid(b\mid c).
```

这里已在通常布尔语义中推导，不是原文五公设内的完整形式证书。G不被主证明A、B、Ia–V或两向定义使用，所以此疑点与核心论证分开处理。

## 6 公开材料与验证范围

- 主文为原创中文分析，公设、短公式及必要反模型用于解释与核验，不是全文逐段翻译。
- 原文PDF、整期刊物、扫描页及下载中间文件不进入发布清单。
- 原创教学代码与执行日志见[复现说明](../../reproduction/sheffer-1913/README.md)。运行环境、测试数量、样本范围及Notebook执行机制以实际保存输出为准。
- [独立复核记录](../../reproduction/sheffer-1913/independent-review.zh-CN.md)分别说明数学阅读、有限代码检查与未认证范围；“独立”指另一检查实现与另一次审阅，不等于人类专家认证。
- 候选表保留此前选择历史、Curry1930第二部分、Church1933后页以及新出现的前驱线索。Curry1929此次取得原刊全文只更新可得性，不计作第二篇全文精读。
