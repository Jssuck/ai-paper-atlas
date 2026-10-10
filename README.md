# AI Paper Atlas · AI 论文历史精读

从人工智能的思想与数学前史出发，沿时间线逐篇阅读、解释和核验研究文献。目标是对不同方向、作者与影响力的论文采用一致的阅读标准，而非只整理名作。

## 当前状态

**持续精读阶段。** 深读 v2 标准已确认。已启用每小时定时推进：同一时间只处理一篇；研究、复现或核验超过一个周期时，继续该篇，后续论文顺延，不补发追赶。完成核验后逐篇公开发布。当前论文阶段见 [进度记录](workflow/progress.json)。这不是每小时必定完成一篇的承诺，也不表示某一年代文献已被穷尽。

## 阅读目录

| 时段 | 论文 | 定位 | 状态 |
| --- | --- | --- | --- |
| 1847 | [De Morgan《三段论的结构与论证概率》精读](papers/1847/demorgan-structure-syllogism.zh-CN.md) | AI前史回填：论域、数量推理、相容概率模型 | 深读v1 · 完整30页及Addition |
| 1851 | [De Morgan《逻辑符号与系词》精读](papers/1851/demorgan-symbols-logic.zh-CN.md) | AI前史回填：量化选择、关系合成与证言通道 | 深读v1 · 完整49页及两层修订 |
| 1852（十一月） | [Sylvester《几何方法的猜想原则》精读](papers/1852/sylvester-geometrical-method.zh-CN.md) | AI前史回填：几何可行域、代数根与直接/间接证明 | 深读v1 · 完整四页及独立审计 |
| 1852（十二月） | [De Morgan《间接证明》精读](papers/1852/demorgan-indirect-demonstration.zh-CN.md) | AI前史回填：命题逆否、几何证明与逻辑规则 | 深读v1 · 完整四页及独立审计 |
| 1852（十二月） | [Drach《评Sylvester第LVIII篇》精读](papers/1852/drach-sylvester-remark.zh-CN.md) | AI前史回填：虚部消去、几何约束与方法论边界 | 深读v1 · 完整短评及独立审计 |
| 1880 | [Peirce《逻辑代数》精读](papers/1880/peirce-algebra-of-logic.zh-CN.md) | AI前史回填：类消元、关系四运算与有条件展开 | 深读v1 · 完整已刊部分及自注 |
| 1904 | [Huntington《逻辑代数独立公设》精读](papers/1904/huntington-independent-postulates.zh-CN.md) | AI前史回填：三组公设、反模型与有限分类 | 深读v1 · 含实跑附件与正式勘误 |
| 1913 | [Sheffer《布尔代数五公设》精读](papers/1913/sheffer-five-postulates.zh-CN.md) | AI 前史回填：独立性、NOR与逻辑原语 | 深读 v1 · 含实跑附件 |
| 1924 | [Schönfinkel《数学逻辑的构件》精读](papers/1924/schonfinkel-building-blocks.zh-CN.md) | AI 前史回填：组合子与变量消除 | 深读 v1 · 含实跑附件 |
| 1930（第一部分） | [Curry《组合逻辑基础》第一部分精读](papers/1930/curry-foundations-part1.zh-CN.md) | AI 前史：形式系统与等式证明 | 深读 v1 · 第二部分待补 |
| 1931 | [哥德尔不完备性论文精读](papers/1931/godel-formally-undecidable.zh-CN.md) | AI 前史回填：算术化、自指与形式系统边界 | 深读 v1 · 含实跑附件 |
| 1932 | [Church《逻辑基础的一组公设》精读](papers/1932/church-postulates-logic.zh-CN.md) | AI 前史：函数、替换与逻辑基础 | 深读 v1 · 含实跑附件 |
| 1936–1937 | [图灵《论可计算数》精读](papers/1936-1937/turing-computable-numbers.zh-CN.md) | AI 前史：可计算性基础 | 深读样稿 v2 · 含实跑附件 |

样稿不等于历史起点已被唯一确定，也不意味着更早或同期工作会被跳过。后续正式目录需按公开来源、纳入规则和年代逐步补齐，不以名气或引用量决定处理优先级。

## 图灵篇可运行附件

- [复现说明、模型定义和执行命令](reproduction/turing-1936/README.zh-CN.md)
- [交互式教学 Notebook](reproduction/turing-1936/turing_teaching.zh-CN.ipynb)
- [测试日志](reproduction/turing-1936/tests.log) · [运行结果](reproduction/turing-1936/results.json)

已实际执行 15 项单元测试与 9 个 Notebook 代码单元；后者使用标准库顺序执行器，并未通过 Jupyter 内核执行或完成页面渲染验证。小模型实验不构成对一般不可判定性的实验证明，也不是原文通用机的完整复现。

## 哥德尔篇可运行附件

- [编码、替换和有限证明的复现说明](reproduction/godel-1931/README.zh-CN.md)
- [教学 Notebook](reproduction/godel-1931/godel1931_toy.ipynb)
- [45 项测试及演示运行日志](reproduction/godel-1931/logs/test-and-demo-run.txt)

Notebook 的 7 个代码单元使用标准库执行器运行；不声称执行过 Jupyter 内核。有限编码与证明检查示例并非对不完备定理的计算验证。

## Church 篇可运行附件

- [替换规则、历史限制与复现说明](experiments/church1932/README.zh-CN.md)
- [教学 Notebook](experiments/church1932/church1932.ipynb)
- [32 项测试日志](experiments/church1932/tests.log) · [独立交叉核查](experiments/church1932/independent_checks.log)

已运行 8 个 Notebook 代码单元，使用标准库执行器；不等同于 Jupyter 内核验证。代码区分现代 β 约简和 1932 年规则的非擦除限制，不声称复现全部原公设或证明系统。

## 已发现的早期文献缺口

[候选与来源覆盖记录](reading-paths/early-foundations-candidates.json)列出本轮有限搜索发现的更早及同期文献、全文可得性和核查范围。后续优先核验较早的未读候选；无法取得原文的保留待补，不以名气或影响力排序，不声称此清单穷尽历史。

## Schönfinkel 篇可运行附件

- [组合子、变量消除与有限逻辑模型复现](reproduction/schonfinkel-1924/README.md)
- [教学 Notebook](reproduction/schonfinkel-1924/tutorial.ipynb)
- [11 项测试及分项检查](reproduction/schonfinkel-1924/logs/unittest.txt)

实跑包含 1,400 个替换例、64 个谓词对、两个高阶 U 有限模型与 8 个 Notebook 代码单元。Notebook 用标准库顺序执行，不声称 Jupyter 内核验证；有限模型不构成一般逻辑一致性证明。

## Curry 1930 第一部分可运行附件

- [归约器与等式证书核说明](reproduction/curry-1930-part1/README.md)
- [教学 Notebook](reproduction/curry-1930-part1/tutorial.ipynb)
- [34 项测试日志](reproduction/curry-1930-part1/logs/unit-tests.txt) · [原文逐页来源账本](papers/1930/curry-foundations-part1.sources.zh-CN.md)

只完成第一部分 509–536 页；第二部分及其完整表示定理证明仍待补读。教学实验区分执行归约与形式等式推导，Notebook 使用标准库执行器，非 Jupyter 内核验证。

## Sheffer 1913可运行附件

- [五公设、反模型与单联结词翻译](reproduction/sheffer-1913/README.md)
- [教学Notebook](reproduction/sheffer-1913/tutorial.zh-CN.ipynb)
- [25项测试日志](reproduction/sheffer-1913/results/tests.log) · [逐页来源与校勘账本](papers/1913/sheffer-five-postulates.sources.zh-CN.md)
- [独立数学与代码复核](reproduction/sheffer-1913/independent-review.zh-CN.md)

1913原刊481–488八页全部核图。实际检查19,700张一至三元素封闭运算表及592次公式翻译真值比较；原非封闭反模型另保留成员条件。8个Notebook代码单元用标准库执行，非Jupyter内核。普通独立与完全独立分开解释；有限实验不替代一般证明。Huntington1904后续已另篇回填；更早来源与既有缺口继续保留，1913不是宣定历史起点。

## Huntington1904可运行附件

- [三组公设、条件化反模型与有限分类复现](reproduction/huntington-1904/README.md)
- [教学Notebook](reproduction/huntington-1904/tutorial.zh-CN.ipynb)
- [22项测试日志](reproduction/huntington-1904/results/tests.log) · [逐页来源与正式勘误](papers/1904/huntington-independent-postulates.sources.zh-CN.md)
- [独立数学与代码复核](reproduction/huntington-1904/independent-review.zh-CN.md)

原刊288–309全22页及同年552页适用勘误已核图。勘误仅补Leibniz书目，不改公设。23个原文有限反模型完成检查；第二组原列十条，但必须删6或7才得到九条独立基。9个Notebook代码格用标准库执行，非Jupyter内核；独立对照26,857张表/关系及16个换标签模型通过。无限反模型与有限分类另有数学解释，有限实验不替代一般证明。Boole1854、Schröder1890、Whitehead1898等可得书籍仍未完成，新发现1883/1890等前驱线索保留待读，1904也不是宣定历史起点。

## Peirce1880可运行附件

- [类消元、关系四运算与有限反例复现](reproduction/peirce-1880/README.md)
- [教学Notebook](reproduction/peirce-1880/tutorial.ipynb)
- [17项主测试日志](reproduction/peirce-1880/evidence/test-run.txt) · [逐页来源与校读](papers/1880/peirce-algebra-of-logic.sources.zh-CN.md)
- [关系公式与条件展开附录](papers/1880/peirce-relative-formulae.zh-CN.md) · [独立代码复核](reproduction/peirce-1880/independent-review.zh-CN.md)

原刊15–57全43页及末页Note to Page47已核图；完成的是1880已刊部分，原文仍标“To be Continued”。17项主测试、15个Notebook代码格实跑，后者用标准库执行器，非Jupyter内核。独立oracle另核262,405关系对、1,049,620四运算结果。本文区分正式自注、印式反例与教学修复；有限检查不替代一般定理或无限极限方法。更早论文线索、可得未读书籍和所有既有缺口继续保留。

## De Morgan1847可运行附件

- [八命题、数量界与概率模型复现](reproduction/demorgan-structure-syllogism/README.md)
- [中文教学Notebook](reproduction/demorgan-structure-syllogism/tutorial.ipynb)
- [17项主测试日志](reproduction/demorgan-structure-syllogism/evidence/test-run.txt) · [逐页来源与版本账本](papers/1847/demorgan-structure-syllogism.sources.zh-CN.md)
- [独立数学复核与七类表](papers/1847/demorgan-mathematical-review.zh-CN.md) · [独立代码复核](reproduction/demorgan-structure-syllogism/evidence/independent-review/independent-review.zh-CN.md)

原刊379–408全部30页及Addition已读核图；分册刊年1847、宣读年1846与合订卷年1849分开记录。17项主测试和16个Notebook代码单元实跑，后者为标准库顺序执行，非Jupyter内核或页面渲染验证。核查保留396页原印公式不一致，以及原26/14分类与现代全语义弱化24/12的准则差异；概率公式明确依赖独立基础模型再条件化。有限实验不替代一般证明，Heath1966所述后期批注及修订仍未全校；所有旧候选、可得未读书籍和未完论文缺口继续保留。

## De Morgan1851可运行附件

- [符号、关系与证言通道复现](reproduction/demorgan-symbols-logic/README.md)
- [中文教学Notebook](reproduction/demorgan-symbols-logic/tutorial.ipynb)
- [21项主测试日志](reproduction/demorgan-symbols-logic/evidence/test-run.txt) · [逐页来源与版本账本](papers/1851/demorgan-symbols-logic.sources.zh-CN.md)
- [系词数学审计](papers/1851/demorgan-copula-audit.zh-CN.md) · [概率与修订审计](papers/1851/demorgan-probability-audit.zh-CN.md)
- [独立代码与Notebook复核](reproduction/demorgan-symbols-logic/evidence/independent-review/review.zh-CN.md)

原刊79–127全部49页已读核图，包含1850年7月1日替换段114–116与7月3日Addition126–127；1851分册、1850宣读和1856合订卷年分开。21项主测试、22个Notebook代码单元实跑，Notebook使用CPython顺序执行器，非Jupyter内核或页面渲染验证。反名32式、exemplar恒等36式与共有21式按明确存在/选择条件核验；95页原印疑误保留原式及反模型。证言模型显式区分报告方向、误报机制、两阶段结构与条件独立，复制证人不重复计证据。有限检查不替代一般证明；更早书籍、Hamilton文本及1847后期批注/修订等全部旧缺口继续保留。

## Sylvester1852可运行附件

- [有向分角线、圆弦与证明方法边界](reproduction/sylvester-geometrical-method/README.md)
- [中文教学Notebook](reproduction/sylvester-geometrical-method/tutorial.ipynb)
- [逐页来源与字形账本](papers/1852/sylvester-geometrical-method.sources.zh-CN.md) · [独立数学审计](papers/1852/sylvester-geometrical-method.audit.zh-CN.md)
- [运行与独立代码复核](reproduction/sylvester-geometrical-method/independent-review.zh-CN.md)

原刊366–369全四页、图与脚注已读核；同卷viii页勘误只针对359页。十一月刊期与10月4日署日分开。368页半参数式的可辨字形与通式/90°例子冲突，保留原式与教学修复；369页逆向式为a(a+x)=b²。代码严格区分有向射线与任意整直线绝对长度；40项主测试、4,010个精确分数代入、4,760个有限网格样本实跑，另有一般多项式系数证书。11个Notebook代码格按标准库顺序执行，非Jupyter内核验证；日志与独立复核见附件。几何定理与关于所有证明方法的猜想分开，有限实验不证明后者。该篇先读新发现十一月前驱；当时十二月De Morgan与Drach仅作回应上下文。De Morgan与Drach现均已另篇完成；全部旧候选、书籍及版本缺口保留。

## De Morgan1852十二月可运行附件

- [经典类包含与构造性逆否边界复现](reproduction/demorgan-indirect-demonstration/README.md)
- [中文教学Notebook](reproduction/demorgan-indirect-demonstration/tutorial.ipynb)
- [逐页来源与版本核查](papers/1852/demorgan-indirect-demonstration.sources.zh-CN.md) · [独立来源与数学审计](papers/1852/demorgan-indirect-demonstration.audit.zh-CN.md)

原刊435–438全四页与脚注读核，十二月刊期和11月1日署日分开；卷勘误仅改359页。四种证明的分类、Euclid I.6的匹配边条件与圆弦回应逐步展开；原文观点、现代重构和实跑分开。现代两世界Kripke反模型显示一般反向逆否的构造性边界，不归给1852原文。24项主测试、5,461类对、34个预序上的674持久模型/49,400公式比较通过；反向式有92个不强迫点，正向0。4格Notebook代码实跑；精确范围与独立复核见附件。有限实跑不是一般证明或全部几何证明的分类。Notebook为标准库顺序执行，非Jupyter内核验证。全部18个旧候选对象、历史前缀和更早书籍/版本缺口保留；该轮未将Drach算为第二篇完成，Drach现已随后另篇精读。

## Drach1852十二月可运行附件

- [虚部抵消与实数域条件复现](reproduction/drach-sylvester-remark/README.md)
- [原文逐句证据与版本账本](papers/1852/drach-sylvester-remark.sources.zh-CN.md) · [独立来源与数学审计](papers/1852/drach-sylvester-remark.audit.zh-CN.md)
- [8项测试日志](reproduction/drach-sylvester-remark/tests.log) · [实际结果](reproduction/drach-sylvester-remark/results.json) · [独立代码复核](reproduction/drach-sylvester-remark/code_review.zh-CN.md)

原刊479页短评全文、目录与同卷不适用勘误核图；十二月刊期与11月22日署日分开。实系数下虚部消去成立，但几何两量到系数的映射未给出，不把启发性短评写成普遍归谬定理。8项主测试含625个精确有理数组合实跑；非实中间量、实负根不可作正长度及系数域反例分开。附件规模与原文相称，不制作无必要Notebook；代码不是历史实验或猜想证明。登记新增当前有效状态，保留旧候选与全部历史；此前De Morgan完成状态可直接检索，所有旧书籍与版本缺口继续开放。

## 每篇解析的共同标准

- 原始书目信息、版本和全文来源
- 当时的问题背景及与前人工作的关系
- 方法、定义、关键公式与论证的逐步解释
- 对实验型论文核对实验设置、对照与结果；对理论论文核对假设、证明结构与适用边界
- 作者主张、原文证据与分析判断分别呈现
- 局限、修正记录、可复核步骤，以及实际执行与未执行项目
- 对后续研究的关联保持证据约束，避免以今日观点替代历史事实

## 公开内容与核验边界

这里发布 AI 辅助撰写的原创中文解析、书目与原文链接，不镜像论文全文或 PDF。每篇注明实际阅读与核验范围；示意推导不冒充原文公式，概念练习不冒充已运行实验。发现错误后保留更正记录。原论文版权归各权利人所有。








