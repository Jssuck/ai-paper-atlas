# I.1 来源、版本、读取范围与选择账本

本账本仅对应 Aristotle, *Prior Analytics* 第一卷第一章 **24a10–24b30**。核验日期2026-10-13 UTC。主文见[完整中文精读](aristotle-prior-analytics-i1.zh-CN.md)，模型见[复现README](../../reproduction/aristotle-prior-analytics-i1/README.md)。这里发布原创分析和来源指针，不镜像希腊全文、英译全文、PDF或扫描。

## 1 三种版本依据，各自支持什么

### G1831：实际查看原页的希腊历史编辑本

完整书目信息：*Aristoteles Graece ex recensione Immanuelis Bekkeri*, edidit Academia Regia Borussica, volumen prius, Berolini apud Georgium Reimerum, 1831。题名页说1831；馆藏集合可能标1831–1870，不能把多卷集合的范围当作本卷刊年。更不能把本卷刊年当作古代作品成书年。

- [题名页](https://archive.org/download/aristotelisopera01arisrich/page/n8.jpg)：编辑、刊行机构、出版地、出版商与1831年实际核图。
- [印刷24页](https://archive.org/download/aristotelisopera01arisrich/page/n39.jpg)：I.1全章，始于左栏24a10，止于右栏24b30；同页顶部仍为《解释篇》结尾。
- [下一印刷25页](https://archive.org/download/aristotelisopera01arisrich/page/n40.jpg)：左栏25a1开始I.2，作为边界核验，不把其整章并入本次完成。
- [前言及抄本符号](https://archive.org/download/aristotelisopera01arisrich/page/n10.jpg)：包括A=Urbinas35、B=Marcianus201、C=Coislinianus330。
- [卷本记录](https://archive.org/details/aristotelisopera01arisrich)。

完整希腊正文与页下适用校勘实际读取。它是十九世纪编辑后的古代文本，不是作者手稿或古代首印。印刷页码、栏行号和平台图像n编号分开记录；n39不是古代页码39。书内I.1不带现代中文说明标题，也没有作者绘制的原则树。

### G1837：电子文本，不冒称原页扫描

[Graeco-Arabic Studies文本](https://www.graeco-arabic-studies.org/view/arist.analytpriora-orig-gr1)明确标示来源：Bekker, *Aristotelis Opera*, Oxford: Oxford University Press, 1837, volumeI, pp61–181。本次读完整I.1电子章文。

[First1KGreek TEI](https://raw.githubusercontent.com/OpenGreekAndLatin/First1KGreek/master/data/tlg0086/tlg001/tlg0086.tlg001.1st1K-grc1.xml)的头部明确承接Graeco-Arabic项目，含2016电子发布及CC-BY-SA4.0说明。它的章前分页标61、章内标62，故电子底本页界为1837印61–62。两个电子呈现具有来源关系，不能计为两份独立手稿校勘。没有独立目验1837原书61–62页图，也不认证1831与1837逐字相同。

此层用于帮助读出希腊文和核章边界；1831可见文字与校勘仍以实际图像为依据。电子文本许可不等于有必要公开复制数据库，本篇只发表原创释读和少量必要术语。

### O1853：英译、脚注和图示分层读取

Octavius Freire Owen, *The Organon, or Logical Treatises, of Aristotle, with the Introduction of Porphyry*, translated with notes, syllogistic examples, analysis and introduction, volumeI, London: Henry G. Bohn, 1853。

- [卷本及PDF入口](https://archive.org/details/Aristotles_Organon_vol_01_1853)
- [实际扫描PDF](https://archive.org/download/Aristotles_Organon_vol_01_1853/Aristotles_Organon_vol_01_1853.pdf)
- [Wikisource扫描索引](https://en.wikisource.org/wiki/Index:O._F._Owen%27s_Organon_of_Aristotle_Vol._1_(1853).djvu)
- [便于检索的转录](https://en.wikisource.org/wiki/Organon_(Owen)/Prior_Analytics/Book_1)

所读PDF第10页为题名，第18页为ERRATA；第99–101页对应原印80–82，完整I.1；第102页即印83，开始I.2。这个映射只适用于所列PDF，不可自动套到另一份DjVu的页序。

题名MDCCCLIII、译者与出版社都实际核图。正文三页、八条编号脚注、边栏1–8分析和81页图均实际查看，OCR只用于定位。没有用OCR错乱的希腊字母或树形图重造原式。

## 2 本章完整主张范围

| 顺序 | 原文定位 | Owen页 | 实际覆盖 |
|---|---|---|---|
| 研究对象与定义次序 | 24a10–16 | 80 | 论证、论证性知识及所需基本概念 |
| 量质分类与未定量例句 | 24a16–22 | 80–81 | 全称、特称、未定量；例句与立论区别 |
| 取得前提的方式 | 24a22–28 | 81 | 取矛盾的一边与问答；推理结构共通 |
| 前提的地位 | 24a28–24b12 | 81 | 推论、论证、辩证与Topics自引 |
| 当前界定的限度 | 24b12–15 | 81–82 | 更精确讨论留待以后 |
| 项 | 24b16–18 | 82 | 谓项与主项、肯否联结 |
| 推论 | 24b18–22 | 82 | 不同结果、必然性、通过这些、外在项 |
| 完善与不完善 | 24b22–26 | 82 | 必然性显明与必要补充环节 |
| 整体与全称述谓 | 24b26–30 | 82 | 每一、无一及包含方向 |

这是完整章块账本，不只摘取与现代程序相似的句子。原文此处并未给出一个限定两前提、三项的完整演算，也未列出本文AEIO、类型支持、有限枚举或Python规则；这些明确另标现代重构。

## 3 实际校勘与勘误

### 3.1 G1831的页脚异文不是“没有校勘”

适用I.1的页脚定位如下：24a29；24b18；24b19两条；24b20；24b21；24b26–29；24b27；24b29。按实际印刷分隔符计为9条、8组定位。同页更前面a1–9和b4–6的记录属于《解释篇》，不能并入I.1。

这些包括文字异读、省略以及某抄本的改写状态。例如24a29记C早期状态的省略；24b19一条涉及A的覆写，另一条记B省去一组词；24b27记BC的另一排列。它们是编辑者记录的手稿差异，不是作者发出的正式勘误表，也不自动命令读者替换编辑正文。

本篇以Bekker1831正文解释本章，承认上述异文存在；没有重新校勘每个原手稿，没有断言每一异文都语义无影响，也没有认证当代最佳定本。

### 3.2 独立勘误表的有界负面结果

实际检查1831卷前n6–15和卷末n804–811。前部包括空白、题名、前言、抄本符号与目录；末部n804为印789终页，随后为空白／透印、馆藏及封皮。此范围未见独立勘误页。先前对同卷全部OCR的errat/corrigend/addend/emendan检索没有给出可信的勘误表线索，但希腊OCR质量差，不能扩大为“全卷无勘误”。

未查的其他卷、其他印次、手稿和后续校本仍可能提供更正；本次没有关闭全部修订史。

### 3.3 O1853的正式ERRATA

第18PDF页整页核图，仅列以下三处：

| 印刷页 | 表中位置 | 更正要点 | I.1适用性 |
|---|---|---|---|
| 219 | 第2行、XVII章题头 | an account改on account | 不在80–82 |
| 273 | 边注4 | syllogistic改asyllogistic，并解释非三段论 | 不在80–82 |
| 594 | XXV章题头 | simply前加not | 不在80–82 |

所以该表没有直接适用于I.1的条目。它不能证明I.1没有翻译或排印问题。本文既不编造一条本章正式勘误，也不把自己的现代解释当成译本更正通知。

## 4 Owen全部脚注、边栏与一幅图

脚注编号在每页重起：80页1–3，81页1–2，82页1–3，共八条。下表概括全部，避免把译编知识倒署给古代作者。

| 页与注号 | 实际内容范围 | 本文采用与限制 |
|---|---|---|
| 80注1 | 篇名与注释传统；Galen、St Hilaire、Waitz、Pacius | 记录为Owen的历史说明；不据此认证命名起源或完整传播史 |
| 80注2 | Aldrich、Boethius的定义用语，译者偏好 | 属译编比较，不当原章新增命题 |
| 80注3 | ὑπάρχειν译法；Taylor、Pacius及53页回指 | 说明词义和方向风险；不是全面词源研究 |
| 81注1 | Alexander及论证、辩证等分类 | 不把后世注解当本章作者自注 |
| 81注2 | Waitz的公理说明、Mansel附录原则树 | 全图读核；来源归属明确，非亚里士多德原图 |
| 82注1 | Aldrich、Aulus Gellius拉丁定义、Mansel乞题讨论 | 只核译本记载，所引著作没有逐篇完成 |
| 82注2 | Aquinas、Scotus、Occam；经院直接／间接与完善性区别 | 保留术语不等同警告；不认证所有经院文献 |
| 82注3 | “对无一”、dictum de omni et nullo、Whately及Categories3 | 注释解释与原文简述区分，不完成Categories3 |

81页树的结构是：原则分共同和特殊；共同一支是公理；特殊一支经θέσεις分定义和假设，并说明主体存在与属性证明。它展示的是译编者转引的原则分类，不是古代原章的计算流程。

80注3实际回指的53页注2另有界查看（同PDF第72页），用于方向澄清；它又回指80页。该一条脚注不等于完成《解释篇》相关章。正文对“P述谓所有S”采用S包含于P的现代方向说明，避免把“谓项属于主项”与“主项在谓项整体内”两种说法误作同方向集合包含。

边栏1–8及子项为Owen的分析编排，不是古代原文八小节。所有八脚注和一图已经覆盖，但脚注所引全套后世文献的来源、版本与观点仍待研究。

## 5 自引和前后章的有界比较

### Topics I.1

本章24b10–12自引Topics。实际有界读取[Greek Topics](https://www.graeco-arabic-studies.org/view/arist.top-orig-gr1)的第一编号部分（网页标Bekker1837, I258–422），以及[Pickard-Cambridge英译Part1](https://classics.mit.edu/Aristotle/topics.1.i.html)。用于核对推论定义、真实首要起点、endoxa和论争式推理的区别。

不是其原书页图审计，不认证网页“350 BCE”为准确成书年，也不据自引确定两书精确年代。主文只使用上述相关定义；不把Topics全章计为第二个完成单位。

### I.2、I.3、I.4、I.5

完整电子I.1–3用于章节选择与主题区分，I.5只读开头／证明部分。I.2换项和I.3模态换项需要独立处理；本次不把它们的全部内容计为已完成。I.4的前次完成记录保持，正文引用其第一格作为已经有的上下文，不重复计数。

本篇涉及E换项等现代小证明，是为解释“必要中间步骤不等于外加事实”，并非把I.2偷偷拼进I.1。代码也不覆盖模态。未完成邻章、全书和整个《工具论》的状态继续开放。

## 6 为什么本轮选择I.1，而不是机械续到I.5

先复核当前README、完整候选注册、progress和Turing1936–37深读v2基准。README和候选注册的本地字节与当前远端Git blob核同；注册有52个候选、49个历史事件、42个背景缺口。旧条目里的历史“未读”快照与当前有效状态分开看，不能拿旧快照抹去后来的完成或更正。

前次只把I.1–3当必要背景，古代单元唯一已完成者是I.4。没有规则说下次必须I.5。按实际可得、完整边界、推理／表征关联、未完成状态和可核性共同评估：

| 候选或时段 | 本轮证据 | 选择与保留 |
|---|---|---|
| Aristotle I.1 | 原语言整章单页扫描，完整电子对读，Owen三页及勘误 | 本轮唯一选定；补齐被明确留下的基础章节 |
| Aristotle I.2 | 完整电子章，换项及存在问题边界清楚 | 有价值的未完成候选，不并入本轮 |
| Aristotle I.3 | 完整电子章；多义可能性和模态换项 | 需要独立模型和来源解释，仍未完成 |
| Aristotle I.5 | 开头与证明部分可读，第二格主题明确 | 不因相邻I.4而自动优先；全章仍开放 |
| Topics I.1 | 直接自引、相关定义可读 | 有界比较，不新增完成单位；相对成书顺序未定 |
| Plato Meno | [Jowett英译入口](https://classics.mit.edu/Plato/meno.html)可见教学／回忆和几何问答线索 | 新增更早希腊来源可能性；尚未核定原语言全本与完整单元，不把著名片段当完整对话或实证实验 |
| Galen Institutio logica | [BBAW1896编辑本入口](https://cmg.bbaw.de/epubl/online/wa_galen_inst_log.php)可访问，列补注及Addenda et corrigenda | 未独立界定并精读一个完整章，保留古代缺口；1896不是古代成书年 |
| Bacon、Descartes、Port-Royal、's Gravesande | 前次具体来源和限制复读，本次不新增全篇读取声称 | 近代缺口全部保留，不因古代回填而删去 |

I.1优先于I.5的理由是**传本结构中的较前基础缺口**，不是已证明I.1较I.5先写，更不是断言它先于Plato或一切其他推理传统。Meno的网页惯用年代也不当精确年；未完成原语言与单位边界核验是证据不足，不是因其名气大而排除或强行抢先。

所有旧Boole、De Morgan、Solly、Hamilton、Euler、Condillac、Curry、Church等候选、书籍、扫描与修订缺口原样保留。Locke/Berkeley的已刊更正和Condillac正式勘误继续保持解决；本文没有重新打开已解决的问题。

## 7 各项证据能支撑到哪里

- 1831图像支持实际编辑文字、栏行、正文／校勘的分层；不支持古代精确成书年或作者手稿状态。
- 1837转录支持一份有关联来源的电子对读；不支持两独立校本或目验1837纸页的声称。
- Owen图像支持这三页英译、全部脚注、边栏与原则树的真实存在；不证明脚注所有历史判断。
- 指定ERRATA支持“此表无80–82条目”；不支持“本章绝无错误”。
- 全称、特称、后承、支持压缩与证书规则是现代定义；一般证明和有限实跑分开。
- 程序无权认证首要性、真实社会公认、古代“通过这些”的全部含义、完善性的历史归类或直接AI影响。

独立来源审查见[来源审计](aristotle-prior-analytics-i1.source-audit.zh-CN.md)，完整论证审查见[论证与数学审计](aristotle-prior-analytics-i1.audit.zh-CN.md)，实现审查见[代码审计](../../reproduction/aristotle-prior-analytics-i1/CODE-AUDIT.zh-CN.md)。三种检查不彼此冒名。文件哈希只绑定实际审过的字节，不把任一哈希当成历史解释正确性的证明。
