# De Morgan1851：逐页来源、版本与主张账本

## 1 本轮究竟阅读了什么

底本为Augustus De Morgan第二篇三段论memoir，完整题名：*On the Symbols of Logic, the Theory of the Syllogism, and in particular of the Copula, and the application of the Theory of Probabilities to some questions of evidence*。原刊为*Transactions of the Cambridge Philosophical Society*，IX，Part I，1851，79–127页。

全文49页扫描图像已逐页查看，并以OCR辅助定位，包含114–116替换段与126–127Addition。阅读与核验各有分工：主篇作者查看49页全图；独立符号/系词审计查看79–110全32页，随后核对111–113及补篇相关页；独立概率/修订审计查看111–127全17页；代码审计另看95、101、120、124、125等关键页。不把“取到OCR”“定位题名”或“有限测试通过”写成完成了未读文本。

公开交付只含原创中文分析、必要符号、代码、证据与来源链接。原扫描与全篇OCR未纳入仓库，不提供整篇翻译。

## 2 来源与日期各自说明什么

- [整卷公开扫描](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf)。全文原刊79–127=PDF95–143；[下一篇首页128](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=144)确认边界，不误把后篇合入。
- [整卷目录](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=9)列本篇起页79；[卷末索引674](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=770)明确列79–127及概率段116–125；卷末673–678全六页均核图。索引中的方括号页码属Part II，不能用统一+16偏移套到整个装订卷。
- [分册题名页](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=15)印M.DCCC.LI，即1851。本文据此纪年，不把宣读年误作已核定发行年。
- [首页79](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=95)记宣读1850-02-25；[正文末125](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=141)署1850-01-07。
- [116页脚注](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=132)说概率节另行提交，署1849-11-19；不能把全篇都归为这一天完成。
- [114页脚注](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=130)明确方括号内段落替换原先段落，日期1850-07-01，直到116页闭合；原先被替换稿本文未取得，未声称逐字对勘。
- [Addition126–127](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=142)末署1850-07-03，与7月1日替换段是不同层次。
- [合订卷题名页](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=7)印M.DCCC.LVI，即1856。
- 确切发行日和独立DOI尚未核定；以卷、分册、页码识别文本足够，不补猜测值。

用于复核底本身份的SHA-256：

- 整卷扫描：`f063767a7cadb9fb2139e35e213bcca6ac9761b324d40d8de703848bc32c8307`
- 49页抽取本：`bcc75e168f3c9970f3ecc8e3a4d85ae90b2142b44f147f3246393022660d8b56`

抽取本仅用于内部核验，仓库不镜像PDF；校验值不代表对全部后期版本的校勘。

## 3 勘误、内含修订与本篇数学纠错分开

[卷内ERRATA（PDF13）](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=13)实际列出的页码为471、472、638、653以及573–574；本次核看未见79–127适用条目。卷末673–678是索引，并非给本篇追加的勘误表。这是对这一卷的有界阴性核查，不是“从无任何后期修订”。

正文自己包含明确的7月1日替换段和7月3日补篇，两者均已纳入阅读。另在95页下表右下发现原印疑误：`))(.) = (.(`；94页明确规则、同页上表重复式和旁列字母支持`).)`。高分辨率逐格检查48式，仅这一格不符该规则；有各项与补项均非空的反模型。详情及可复查转录轨迹见[系词审计](demorgan-copula-audit.zh-CN.md)与[源文数学证据](../../reproduction/demorgan-symbols-logic/evidence/source-math-review/README.md)。

此项标为**本篇原图/数学核查的原印疑误**，不冒称作者正式勘误。程序实现94页规则，同时保留错印负控制；没有将现代修正规则无声冒充每一格原印。

[Heath1966选集的编者说明预览](https://api.pageplace.de/preview/DT0400.9780429511394_A38476725/preview-9780429511394_A38476725.pdf)提供作者批注单行本、印刷修订与编辑取舍的线索；该预览本身不能支持全部改动逐项比对。该选集第二memoir删去概率节，不能代替这49页完整底本。本次未取得并穷尽各版修订；上一篇1847的后期批注与印刷修订校勘仍开放，尤其不能说本次7月1日替换段就是1847的修正。

## 4 逐页阅读与核查表

以下“内容”是原创定位摘要，“核查”是本篇解释或审计动作，不是原文逐句翻译。所有页均核图；每个页码链接直达整卷相应PDF页。

| 原刊页 | 本页内容 | 本篇核查与边界 |
| --- | --- | --- |
| [79](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=95) | 题名、署名、1850-02-25宣读；前篇、Formal Logic、Hamilton、Boole定位 | 本篇比较反名与发明量化两系统；不把“方法不同”夸张为无共同背景。 |
| [80](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=96) | Section I；代数正负与逻辑诸对立的类比 | 区分项否定与系词否定；自然语言双否定可能有语气，不能都当形式同义。 |
| [81](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=97) | 全称/特称与其他对立的对应；宇宙与复合项 | 全称包含的反例区域为空；有些不等于仅有些。 |
| [82](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=98) | 合取/析取、可转换、单一/复数等类比 | 作者承认有些类比是为系统而寻找；不升级成所有逻辑概念的同一性。 |
| [83](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=99) | 推理工具部分、机器与代数消元 | 只说工具性部分，不是所有思维都已化约机械运算。 |
| [84](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=100) | John/Thomas消去；代换与不能倒推；复杂词项 | 共享名字被消去会失去可恢复性；现代关系例与原文区分。 |
| [85](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=101) | dictum de majore et minore；人的头/动物的头；Section II | 关系像的单调性为现代重构；原挑战的历史范围不据此穷尽。 |
| [86](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=102) | 基本符号应拆开；括号量与项的相对位置 | 右括号不恒定表示全称：它相对左项/右项的方向不同。 |
| [87](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=103) | 奇偶点、可逆向读、删中项、线图 | 先判有推论再消去；不是任意字符串都可产有效结论。 |
| [88](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=104) | 三项线图、见证保留；Hamilton/Thomson图示 | 有些Z非Y且X/Y覆盖，推出相应Z在X；图线不是比例概率。 |
| [89](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=105) | 双项量化贡献归于Hamilton；相对记号优势 | 按作者明确承认记录贡献，不代判全部优先权争论。 |
| [90](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=106) | Section III；反名扩张与数量分布 | 作者承认前篇中没有明确注意全部量化组合；不据后见替他补上早期认识。 |
| [91](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=107) | 八式新旧记号表；归纳核验；存在反名 | 所有项为非空真子集的复现约定显式；表中全称命题不等于两个全称项。 |
| [92](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=108) | 反名变换、三种否定因素、对当及下降 | 同时反转括号/点；等价与存在性弱化分开。 |
| [93](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=109) | 概率上的同伴/对立；基本肯定三段论 | 无先验的概率支持说法有现代反模型；基本型的见证须一致。 |
| [94](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=110) | 8全称、16特称、8加强；有效性与删项规则 | 32为指定系统分类；加强式依赖项/反名非空。 |
| [95](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=111) | 两表48格、重复式、opponent变换 | 全部公式格高分辨率核对；下表右下原印错向，保留原式、规则及反模型。 |
| [96](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=112) | 换阅读方向；Section IV；Hamilton八式与Solly1839 | 同字形跨体系改义；Solly书仅是原文引出的未读前驱。 |
| [97](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=113) | extension的标准；Fesapo；两个特称前提的不同个体结论 | 反名见证依赖非Y存在；不能把Hamilton不同个体结论译成通常O。 |
| [98](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=114) | 对Hamilton三个反对：复合、否定不封闭、spurious | 相等的否定是两差集非空的析取；不同个体的否定为共同单例（非空背景下）。 |
| [99](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=115) | 改用exemplar；any one/some one；1839旧著脚注 | 选择可依前项而变；历史脚注为作者证词，未代替独立原著核查。 |
| [100](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=116) | exemplar证明、自然语言与任意选择 | 全称不是任取一次就证明；Euclid类比是作者方法论陈述。 |
| [101](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=117) | 八种exemplar；64−16−12=36 | 混合量词须按右栏释义重建；不能表面左到右，包含与共同单例分开。 |
| [102](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=118) | cumular消去修饰；36式表 | Y=Z不使X=Z；Y/Z同一单例的强条件才允许相应结论。 |
| [103](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=119) | 两系统共有21式；Section V | 共有的是符号推论结构，不是同字形始终有同一真值条件。 |
| [104](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=120) | 抽象系词、传递、可换位、相反系词 | convertibility指对称；兄弟关系例按通常非自反读法须限制。 |
| [105](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=121) | 局部互补系词；外延与内涵 | 至少一真不足以当矛盾关系；内涵包含推断需属性/决定条件区分。 |
| [106](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=122) | 内涵表、必要与充分属性；只传递时的三格 | 不是Y不代表缺少Y每一属性；负式由反证得出。 |
| [107](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=123) | correlative、g助记、支撑例与图形 | 逆关系不等于原关系；支持之支持须另承认传递意义。 |
| [108](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=124) | bicopular：说服→命令→控制；复合关系 | control只须包含复合路径；原文脚注不要求二者外延相等。 |
| [109](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=125) | 合成消中项；两种负式；第四格 | 现代关系R;S、否定与逆序律另明确；不偷把复合关系改回原关系。 |
| [110](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=126) | 纯同一IS与同色；逻辑书的隐含系词条件 | 作者类比及古典文本脚注不视为本轮已独立校勘的Aristotle/Proclus事实。 |
| [111](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=127) | 玫瑰—红色—美；词项与系词的类型差别 | 不是红物一概美；现代有类型关系说明不归功为已完成类型系统。 |
| [112](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=128) | 一般关系的量；10与100个关系；数量旁注 | 边计数推出共同目标下界；需要正整数项数，严格不等号不能删。 |
| [113](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=129) | 一般关系八式、among them、双全称 | ∀y∃x覆盖不是∃x∀y；转回反名讨论前需标记解释切换。 |
| [114](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=130) | 强关系/补项条件；开始7月1日替换括号 | 脚注明替换原稿段落；总入出关联、不能混接补类是实质假设。 |
| [115](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=131) | 逐步放松关系条件；等价式及各格规则 | 仅有传递/总关联不够；≤二元素反例揭示缺失的非混接条件。 |
| [116](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=132) | 替换段结束与作者说明；Section VI脚注 | 概率另稿1849-11-19；更一般体系融合留待研究，不能冒称全文已完备。 |
| [117](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=133) | primary distribution；球/币及主观先验 | 数学算式不决定抽样权重；对d’Alembert生前改正的说法保持作者推测层级。 |
| [118](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=134) | 三种证言现象；大脑概率计算比喻；黑桃七 | 心理观察非本篇受控实验；比喻不是运行机器。 |
| [119](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=135) | Laplace两个证言模型与罕见事件 | 具名均匀误报与黑白二分类误报不同；忠实聚合不会凭空改变后验。 |
| [120](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=136) | general/particular credibility；完整报告概率表 | 原符号报告在前、真相在后；正文列随机，代码真相优先转置。 |
| [121](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=137) | 均匀错误闭式；与1/n比较；大n极限 | 固定目标先验和均匀先验一起变动不同；无偏误为模型假设。 |
| [122](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=138) | 长等待经验、显著性分组、全称证言 | 22,000数量级现代复算22,713；历史实验为原作者报告，不冒称本项目重做。 |
| [123](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=139) | 否認互补公式、lambda偏误、无信息条件 | 发言/否认协议与概率矩阵须一致；无信息证人每个真相列相同。 |
| [124](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=140) | theta偏误、两阶段误判/误述、Laplace闭式 | 完整路径求和；两次错误可回真；Markov条件显式，p/r交换不改对称式。 |
| [125](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=141) | 定向虚报、多证人、剩余事件；正文署日 | 乘积需给定真相后的条件独立；剩余状态还须补报告似然；署1850-01-07。 |
| [126](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=142) | Addition；普通三段论也可加关系原则大前提 | 将原则变为一个前提不解释掉关系合成本身；不把补篇遗漏。 |
| [127](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=143) | Reid/Hamilton、Mansel、父子与Port Royal译词；署日 | 父的逆关系与儿子的性别条件区分；is/ought不混；Addition署1850-07-03。 |

## 5 前驱线索、未读来源与保留缺口

原文引文提供定位，不代表本轮已精读相应原著：

- De Morgan首篇1847原刊底本已另篇完成；其后期修订及作者批注没有因此全校。
- 本篇79、85、90等页多次指*Formal Logic*；99页脚注指*First Notions of Logic*1839。本轮未读完这些书。
- 96页明引Thomas Solly，*Syllabus of Logic*1839，第47页，记为早期未读线索。
- 88–89页引William Thomson，*Outline of the Necessary Laws of Thought*第2版1849，第265–267页；113页另指188–189。此处不以De Morgan的引文代替独立逐页核读Thomson全书。
- Hamilton在Reid版的附录/说明、后续著作以及Mansel的Aldrich编注有各自版本问题；126–127页引用足以说明本篇争论对象，不足以判定各方所有观点或优先权。
- Laplace第3版446–451页在119页被作者明引；本次重建的是De Morgan所呈两题与124页复推，没有声称另读完Laplace全书。
- Boole1847/1854、Schröder1890、Whitehead1898等可得未读书籍，Curry/Church等既有未完论文，所有原候选与历史记录继续保留。

本轮只推进此一论文。它在当前已核实的De Morgan后续论文线索中早于1858/1862，并早于登记的Peirce1867/1870、McColl1877/1878线索；这不等于检索穷尽整个逻辑史，也不把书籍视作不存在或不能获取。

## 6 如何追踪分析、代码与实际证据

- [主篇深读](demorgan-symbols-logic.zh-CN.md)：21节，逐步推导、例与反例、主张账本、12题含答案。
- [系词与符号审计](demorgan-copula-audit.zh-CN.md)：原图48格与32/36/21分类，存在、量词选择与关系边界。
- [概率与修订审计](demorgan-probability-audit.zh-CN.md)：完整报告矩阵、偏误、两阶段、依赖结构与修订条件。
- [复现说明](../../reproduction/demorgan-symbols-logic/README.md)及[原文—代码映射](../../reproduction/demorgan-symbols-logic/SOURCE_LEDGER.md)。
- [独立代码审计](../../reproduction/demorgan-symbols-logic/evidence/independent-review/review.zh-CN.md)：单独oracle、真实日志及22个Notebook代码单元的独立重放；CPython执行而非Jupyter内核。

手算与一般证明、作者观察与本项目实跑、原印式与教学修正均在对应位置标清；有限模型通过不据此被称为全文普遍定理的机器证明。
