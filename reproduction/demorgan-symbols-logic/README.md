# De Morgan 1851：符号、关系与证言的教学复现

对应 Augustus De Morgan，*On the Symbols of Logic, the Theory of the Syllogism, and in particular of the Copula, and the application of the Theory of Probabilities to some questions of evidence*，原印页79–127。1850年2月25日宣读；本项目按卷IX第一部分的1851年印行纪年。p.114起的方括号修订日期为1850年7月1日，Addition pp.126–127署7月3日。

这是原创的现代 Python 教学重构，不是历史程序，也不是全文形式化证明。主体为标准库精确集合/关系/概率运算；没有数据集、第三方依赖、训练、服务、网络、安装或随机数。原文与实现的逐项映射见 [SOURCE_LEDGER.md](SOURCE_LEDGER.md)。

## 一分钟运行

Python 3.10+，进入本目录：

```sh
python demo.py
python -m unittest discover -v
python execute_notebook.py tutorial.ipynb
```

重做完整执行证据：

```sh
python run_checks.py
```

`run_checks.py`更新 notebook 输出、evidence 的实际日志、环境/命令清单及 SHA256SUMS。两份审计脚本若存在也自动重跑：`evidence/independent-review/independent_review.py` 和 `evidence/source-math-review/source_math_review.py`。源文数学审计保留 `evidence/source-math-review/results.json` 与 `run.log` 输出位置；先更新其局部SHA256SUMS，再让根目录SHA256SUMS覆盖包括该局部清单在内的全部交付文件。`build_notebook.py`重建教程正文并清空输出，之后必须再执行。不要运行未经审阅的第三方 notebook。

## 文件导航

- [tutorial.ipynb](tutorial.ipynb)：45个中文教学单元，22个代码单元；交付版逐单元实际执行，含练习与答案、假设对照和反例
- [demorgan.py](demorgan.py)：括号符号、两套推论规则、关系运算、条件报告矩阵与证人模型
- [tests/test_demorgan.py](tests/test_demorgan.py)：21个自动发现测试方法，量词/联合事件/潜变量独立 oracle 和负控制
- [demo.py](demo.py)：简短结果与全部32+36个许可符号式；输出 [evidence/results.json](evidence/results.json)
- [evidence/test-run.txt](evidence/test-run.txt)、[evidence/demo-output.txt](evidence/demo-output.txt)、[evidence/notebook-run.txt](evidence/notebook-run.txt)：实际日志
- [evidence/environment.json](evidence/environment.json)、[evidence/commands.json](evidence/commands.json)：脱敏环境、命令、退出码与耗时
- [evidence/notebook-validation.json](evidence/notebook-validation.json)：受限结构/执行输出校验

Notebook从已安装的官方 jupyter-notebook skill 的 tutorial 模板与 `new_notebook.py` 初始化，然后填入原创中文教程。执行方式为新的共享globals字典中顺序 CPython `exec`，**不是Jupyter kernel执行**。没有 magics、shell escapes、rich display、widgets 或异步顶层代码，可在已有 Jupyter 环境中重启内核后运行全部。项目校验不冒充 nbformat 官方校验。实际可选包可用性见环境JSON。

## 复现得到了什么？

### 1. 两套符号系统不可混读

- pp.91–95的 contrary 系统：8个全称推论、16个特称推论、8个加强式，共32。以193个非空proper三项原子占据模型逐一核验；同时为全部未许可前提组合寻找八式中的无结论证据。
- 将域扩大至含空项/全域项的全部256种模式，同样的32个指定结论只有24个始终成立。差额是存在假设的作用，不是把原文32改成24。
- pp.100–103的 exemplar 系统：恒等copula与非空项下，按声明的量词次序得到36式；与另一系统共有21个符号式。
- exemplar测试让每个成员原子有0、1、2个对象，6561种配置中6342种三项非空。只做“区域是否存在”的枚举无法区分单个对象和两个性质完全相同的对象，因而不足以核验双单称条件。

### 2. copula 的合成是新的结论关系

`compose(R,S)`表示先R后S。程序重构p.108的说服/命令例，验证逆关系的逆序合成、结合律与两个负式对偶。任意R不必传递、不必对称；即使R可取逆，也不等于R自身可换。`relational_term`重构p.85“人的头→动物的头”的单调性。

p.112中每个对应每个，与双向分别有对应对象不同。数量下界为 `max(0,E−(a−1)b)`：a个源、b个目标、E条边保证至少这些目标与全部源有关。3×3以内全部二部关系核查下界，并按每种边数验证可达到。

### 3. 证言不能只给一个“可信度”

使用原文p.120的完整报告概率矩阵。原文 `p_q`是报告p、实际q；代码是 `C[q][p]`，行真实事件、列报告，每行和1。所有概率输入要求int/Fraction，不接受浮点隐式精确化。

- 52种具名卡、均匀错误：先验1/52、准确率9/10，报告目标后仍9/10。
- 保持同一联合模型，把其他51种标签正确聚合：仍9/10；其他→目标的概率为1/510。
- 改成准确率9/10的二元报告模型：后验3/20。差别来自误报机制，不能说单纯改标签改变了概率。
- 两阶段判断/报告误差：n=4、p=3/4、r=4/5，后验37/60，含两错抵消项1/60。
- 两份条件独立的9/10准确证言：后验81/82；第二人完整转述第一人：仍9/10。
- 定向虚报：目标先验1/52、虚报概率1/10时，后验10/61。

## 独立复核

[独立审计报告](evidence/independent-review/review.zh-CN.md)及[执行与哈希](evidence/independent-review/review-execution.json)已通过。另写的oracle重建两套逻辑语义、原文报告优先的列随机矩阵、整数联合事件计数、邻接路径与入度向量，不调用主测试的预期值生成器。

额外检查包括4096对矩形关系、15029个入度向量、255个可达计数组合、2160组三事件报告模型（4455定义后验、2025零质量拒绝）、50个分组后验，以及发言选择、Markov条件与复制证人的反例。独立只读执行器重新运行全部22个Notebook代码单元，输出与交付文件逐字一致。

审计还修正了一处跨环境元数据表述：校验器现在说明“未执行官方nbformat校验”，不再假定所有重跑环境都没有nbformat。数学主体未发现与声明语义相冲突的缺陷。完整独立证据可用 `python evidence/independent-review/capture_review.py` 重做。

[第二份源文数学核查](evidence/source-math-review/README.md)另从原图独立转录p.95的全部48格，不导入数学主体；它保留原印错误，确认唯一不一致位于下半最右列第8行，同时在四对象域核查32/36/21计数及补项反例。详细逐格轨迹见[results.json](evidence/source-math-review/results.json)，真实执行见[run.log](evidence/source-math-review/run.log)。

## 原印式与实现不能悄悄互换

原图核查p.95的48格：下半表最右列最后一格印为 `)) (.) = (.(`，与p.94删中项规则及上半对应格不一致；正确规则给 `).)`。本包明确重现规则，并单独保留错印负控制：

```text
U={1,2,3}, X={1}, Y={1,2}, Z={1,3}
X⊆Y，Y∪Z=U，两个前提真。
原印结论 X−Z 非空：假。
规则结论 Z−X 非空：真。
```

这项原图定位由全篇源文复核提供，回归测试独立核验真假；不据此推断其他印式都有错误。

## 数学/历史边界

1. **补集有固定论域。** contrary的全称式采用现代无存在蕴涵集合语义；p.91原文项与补项存在的约束在32式枚举中显式加入。
2. **exemplar量词不是机械左到右。** 肯定混合式按全称先选、存在依赖于它，否定式取完整对偶。`((`为∀y∃x R(x,y)；其矛盾式`).)`为∃y∀x ¬R(x,y)。双全称恒等式要求相同单元素类，不能替换成一般集合相等。
3. **36式测试限定恒等copula。** 对任意关系，必须另外检查pp.104–113的copula法律。辅助函数可以计算任意关系上的exemplar真值，但语法许可不保证任意关系都有效。
4. **修订pp.114–116没有被过度泛化。** 总关联、补项范围与不得混接条件不是任意关系的性质；程序给出违例，不声称完整形式化带上下标/相关符号的修订系统。
5. **发言选择与否认的报告协议。** 本例通道将每次试验的报告列满。若通道仅描述“已经发言”时的报告，先验也必须已条件化于发言；若发言概率依真实事件变化，应加入沉默输出或另乘发言似然。 `denial_posterior`采用p.123的似然1−C[q][k]，即报告不是k。另行被问“k有没有发生”的证人，需要另建二元回答通道。
6. **多层和多证人有条件假设。** 两阶段模型假定给定信念后报告只依赖信念；多证人乘积需要给定真实事件的条件独立。模仿、共源、串通必须另建联合似然。
7. **零质量拒绝。** 概率必须归一；不自动给缺失事件分配报告机制。p.125所说“其他事件”可显式增加为一个完整状态及通道行，不能只加剩余先验。不可能报告给出错误，不设任意默认后验。
8. **primary distribution不是由程序发现的客观事实。** pp.116–123强调建模前的案例划分与权重，本包把它们作为输入，不把原文心理学说法、证人能力、错误均匀性当作实测。
9. **有限枚举不是全文一般证明。** 占据模型忽略大小；重数0/1/2模型只用于涉及空性/单称的指定语言。没有自然语言解析、真实证据校准或历史优先权裁判，也不重现Hamilton cumular全部变式。

## 实际主测试范围

数字是模型/参数数量，不是测试方法数，彼此可能重叠。

| 部分 | 范围 | 数量 |
| --- | --- | --- |
| 八式、补项变换、矛盾 | n=0..5全部类对 | 1365个类对 |
| contrary规则 | 64个前提组合，193个proper占据模型 | 32个许可结论；8+16+8 |
| 存在约束负控制 | 全部256占据模型 | 32中24个无存在条件仍有效 |
| exemplar恒等语义 | 8原子各0/1/2个对象 | 6342个非空配置；36式；21共有符号式 |
| 合成及负式 | 2元素域全部关系对 | 256对 |
| 合成结合律 | 2元素域全部关系三元组 | 4096组 |
| 传递性与逆关系 | 3元素域全部二元关系 | 512个 |
| 数量共有下界 | 源/目标各1..3，全部边子集 | 682个关系，按边数验证可达到 |
| 二元报告概率 | 5点先验×5点两种准确率×2报告 | 224定义值；26零质量拒绝 |
| Laplace两层闭式 | n=2..6，两层各5点参数，逐报告 | 500个值 |
| 三份证人的潜变量枚举 | 两状态、三证人、全部报告序列 | 8种报告，各16条实际/潜状态路径 |

此外还有原印p.95负控制、具名卡/二元模型/忠实聚合、θ偏误族、无信息通道、定向虚报、复制证人、输入维数与范围测试。耗时以日志为准，不当作性能基准；主要测试约秒量级。模型枚举的指数成本被刻意限制在很小的域。
