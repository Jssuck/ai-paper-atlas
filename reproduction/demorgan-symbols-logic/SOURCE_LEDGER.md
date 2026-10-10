# 原文—公式—实现对照与来源边界

## 来源与版本

Augustus De Morgan，*On the Symbols of Logic, the Theory of the Syllogism, and in particular of the Copula, and the application of the Theory of Probabilities to some questions of evidence*，*Transactions of the Cambridge Philosophical Society*，vol.IX，part I，pp.79–127。

- 宣读：1850-02-25（p.79标题下）。
- 本项目纪年：1851，按该卷第一部分印行；不把1850宣读年当作1851年的实验运行时间。
- 概率节独立提交注明1849-11-19（p.116脚注）；p.125署1850-01-07。
- pp.114–116方括号替换段：p.114脚注明1850-07-01。
- Addition：pp.126–127，末署1850-07-03。

底本：[原刊合订扫描](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf)，原印页79–127对应扫描PDF第95–143页；[分册题名页](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=15)为1851，[合订卷题名页](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=7)为1856。完整底本URL与页码已由主篇来源审计核验。本任务中未再进行网络下载。

依据原始扫描提取的49页PDF与OCR定位阅读；关键数学不单靠OCR。主篇源文复核已逐页检查49幅原图；本实现者另直接查看p.120与p.124原图，独立审计复查p.95等关键页。有关日期、页码与全篇分析，见[完整中文精读](../../papers/1851/demorgan-symbols-logic.zh-CN.md)、[copula审计](../../papers/1851/demorgan-copula-audit.zh-CN.md)、[概率审计](../../papers/1851/demorgan-probability-audit.zh-CN.md)。本包只记录必要公式和定位，不再复制整篇原文。

## 覆盖矩阵

| 原页 | 原文内容 | 现代实施/教学动作 | 范围与不做的声明 |
| --- | --- | --- | --- |
| 79 | 工作定位、与1847前文及Boole路径的区别 | 包标题、年份、README | 不声称直接复刻Boole算法或历史软件 |
| 80–85 | 反对关系、消元、复合项、大小替换原则 | `relational_term`，人的头/动物的头单调性例 | 不解析自然语言；给定head-of关系及类包含 |
| 86–89 | 括号量、负点、删中项及图形表达 | `Proposition.parse`与点奇偶性 | 不模拟原版字体粗细、图形排版与全部figure记号 |
| 90–93 | contrary八式、补项、矛盾、存在条件 | `holds`、`contrary_term`、`contradictory` | 固定有限U；现代全称真值可空，推论测试另加proper条件 |
| 94–96 | 32推论，8+16+8，删中括号 | `symbolic_inference`、193模型 | 实现p.94 canon；不是声称48个印表格全都逐字正确 |
| 95下半右下格 | 原印 `)) (.) = (.(` | 专门回归反例，规则给`).)` | 保留原印错误与修正规则的区别；上半对应格支持后者 |
| 96–99 | Hamilton系统与contrary的两种新式、双向包含与单称问题 | notebook区分集合相等和任取个体恒等 | 不实现Hamilton cumular的全部规则修饰 |
| 100–103 | exemplar选择，36式，21共有式 | `exemplar_holds`、`exemplar_inference`，6342重数模型 | ∀∃/∃∀次序显式；36式验证限恒等copula、非空项 |
| 104–107 | transitiveness、convertibility、correlative与figure | `transitive`、`symmetric`、`converse` | 不把全部自然语言关系默认判成传递或可换 |
| 108–111 | bicopular关系合成、负式分解、关系的抽象范围 | `compose`、两个负式对偶、逆序律与结合律测试 | R;S是最小复合关系；若原文control是更宽关系，还需包含前提 |
| 112–113 | exemplar/cumular区别；a×b个关系；计数下界 | `all_some`、`all_all`、`common_target_lower_bound` | 空域依现代规则虚真；历史例和下界限定非空源 |
| 114–116 | 7月1日替换的特殊关系/补项扩展 | notebook与负控制说明总关联/非混接条件 | **不声称复现这套全系统**；一般关系不会自动继承补项推论 |
| 116–119 | primary distribution；具名计数器与二元白球的比较 | 52标签报告模型对二元报告模型 | 先验与错误分布是输入，不是本程序或原文实测 |
| 120 | 一般与特定可信度；完整报告矩阵 | `posterior`、`general_credibility`、`report_distribution` | 原符号报告优先，代码真实事件优先；行列方向不能混 |
| 121 | 无偏错误的n标签闭式，均匀先验与大n | `symmetric_channel`、`symmetric_credibility` | 先验固定与先验1/n两种极限分开；n≥2 |
| 122–123上 | remarkability分组；否认事件 | notebook分组对照、`denial_posterior` | 分组现代审计保持同一联合分布；否认解释为非k报告 |
| 123–124上 | λ偏误，a=λ无信息，θ族 | `biased_channel`，无信息与θ族精确测试 | λ为接收者对证人预期的模型；退化零分母拒绝或确定性处理 |
| 124 | judgment与statement两阶段；Laplace闭式 | `compose_channels`与独立潜变量oracle | 给定belief后报告独立于真实事件的Markov结构 |
| 125 | 定向虚报、多证人、剩余案例 | `targeted_statement_channel`、`multiple_witnesses` | 多证人显式条件独立；其余事件须完整增行，不能凭空补似然 |
| 126–127 | Addition：关系合成、相关关系、隐藏公设与翻译问题 | copula教学的范围与反例说明 | 不做历史优先权裁定或把应然/实然混作同一关系 |

## 核心公式与实现假设

### 两种`)(`不能混用

contrary系统：`X)(Y`为存在一个既非X也非Y的对象；`X(.)Y`为X∪Y=U。

exemplar系统：`X)(Y`为∀x∈X∀y∈Y R(x,y)；`X(.)Y`为∃x∈X∃y∈Y ¬R(x,y)。若R是恒等且X,Y非空，前式只有在X=Y为同一单元素类时成立。

混合exemplar式中：肯定的`X((Y`读∀y∈Y∃x∈X R(x,y)；矛盾的`X).)Y`读∃y∈Y∀x∈X ¬R(x,y)。全称先选/特称依赖，以及否定后的对偶次序不能隐藏。代码并没有以一般的∃x∀y解释前者。

### p.94规则

中括号同向：至少一前提全称；中括号异向：两前提全称。许可时，结论保留最左与最右括号，负点为两前提负点异或。这里“全称”是contrary系统的命题分类，不能搬到exemplar系统。

### p.112数量界

共有目标数c；不共有目标最多a−1条入边。因此 E≤ca+(b−c)(a−1)=(a−1)b+c，得到 c≥max(0,E−(a−1)b)。这是一般计数论证；小域枚举是额外检查。原文m个源各至少n条边给 E≥mn。只有m=a才可能使 mn>(a−1)b，因为n≤b。

### p.120报告通道

令C[q][p]=P(报告p | 真实q)，v为完整事件先验。

```text
P(真实q | 报告k) = v[q] C[q][k] / Σ_s v[s] C[s][k]
P_k = 后验第k项
事前总体正确率 μ = Σ_s v[s] C[s][s]
P(报告k) = Σ_s v[s] C[s][k]
```

p.120的“if he make any statement at all”需要单列：若C是给定已发言的条件通道，而v仍是发言前先验，必须再乘各状态的发言概率α[q]；或把沉默列加入完整通道。当前教学实例采用每次都有所列报告的完整通道。

当该报告有正概率且C[k][k]>0时，P_k=C[k][k]等价于v[k]=P(报告k)。若对角准确率为0，单凭这个等式不能反推先验/报告概率相等；教程没有宣称无条件的“当且仅当”。

### pp.121、123–124偏误

均匀误报：C[q][p]=(1−μ)/(n−1)，p≠q；特定可信度为 vμ/[vμ+(1−v)(1−μ)/(n−1)]。

λ偏误：`C[q][p]=λ[p](1−a[q])/(1−λ[q])`，p≠q。若a=λ，C的每一行都是λ，任何正概率报告不改变先验。若λ[q]=1而a[q]<1，其他候选事件的λ质量全零，模型无法分配错误概率，代码拒绝；a[q]=1时整行为确定性报告q，无需0/0。

θ族：a[s]=1−θ(1−λ[s])。只要各a[s]合法，并且报告有正概率，则P_k=v_k(θλ_k+1−θ)/[(1−θ)v_k+θλ_k]。测试包括θ=6/5的合法实例，不把θ机械限制在[0,1]，只检查实际通道概率范围。

### pp.124–125两层与多证人

```text
C[q][r] = Σ_b J[q][b] S[b][r]
P_k（均匀先验、均匀两层误报）= pr + (1−p)(1−r)/(n−1)
多证人：likelihood[q] = Π_i C_i[q][report_i]
```

前式以belief为中间状态，隐含报告只依赖belief；后式以真实q为条件，假定证人报告相互独立。真实事件、各证人belief及report的完整路径枚举是测试的独立oracle。复制证人用联合似然给反例，防止把重复信号算两次。

## 现代新增内容

`aggregate_model`、精确Fraction、原子/重数枚举、单元测试与notebook执行器都是现代教学和审计工具。聚合用原先验加权得到每个粗状态的条件报告行；零先验粗状态没有可识别的条件行，直接拒绝。没有声称De Morgan提出了这些程序、矩阵API、自动验证方法或现代术语。

## 代码与执行来源

数学主体 `demorgan.py`、测试、demo与中文notebook为此篇新写。通用执行/受限校验/日志脚本沿用本系列1847复现中的透明标准库工具，适配本项目路径与产物，不归于历史作者。Notebook模板来自已安装官方 jupyter-notebook skill，执行不依赖该skill继续存在；交付文件已包含全部内容。

所有概率和离散关系结果确定、可重复；耗时与UTC执行时间因重跑改变。SHA256SUMS在每次全套执行末尾更新。日志不收集账号、主机名、HOME、环境变量或凭据。
