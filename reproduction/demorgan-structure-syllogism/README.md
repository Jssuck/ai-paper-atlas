# De Morgan 1847：有限逻辑与概率的教学重构

对应 Augustus De Morgan，*On the Structure of the Syllogism, and on the Application of the Theory of Probabilities to Questions of Argument and Authority*，1847，印页379–408，含406–408页 Addition。

这是原创、低成本的现代 Python 实现，不是历史软件，也不是对30页全部命题的形式化证明。主文见[全篇精读](../../papers/1847/demorgan-structure-syllogism.zh-CN.md)，公式定位及实施边界见 [SOURCE_LEDGER.md](SOURCE_LEDGER.md)。

## 一分钟运行

Python 3.10+，仅标准库，无第三方安装、服务、网络、数据集或随机种子。进入本目录后：

```sh
python demo.py
python -m unittest discover -v
python execute_notebook.py tutorial.ipynb
```

一条命令重做全部执行证据：

```sh
python run_checks.py
```

`run_checks.py` 会更新 notebook 输出、evidence目录的真实日志与 SHA256SUMS。`build_notebook.py` 则重建教程正文并清除旧输出；通常无需运行。只执行可信 notebook，因为代码单元就是可执行的 Python。

## 先打开哪个文件？

- [tutorial.ipynb](tutorial.ipynb)：中文教学流程；32个单元，其中16个代码单元，交付版已全部顺序执行；含练习、答案和负控制
- [demorgan.py](demorgan.py)：八命题、七关系、数量下界、两种随机模型、条件概率、未知 authority 的积分与分类审计
- [tests/test_demorgan.py](tests/test_demorgan.py)：17个自动发现测试方法，含独立量词/枚举 oracle 与负例
- [demo.py](demo.py)：精简例子，生成 [evidence/results.json](evidence/results.json)
- [execute_notebook.py](execute_notebook.py)：透明的标准库顺序执行器
- [evidence/test-run.txt](evidence/test-run.txt)、[evidence/demo-output.txt](evidence/demo-output.txt)、[evidence/notebook-run.txt](evidence/notebook-run.txt)：实际执行输出
- [evidence/environment.json](evidence/environment.json)、[evidence/commands.json](evidence/commands.json)：脱敏环境、实际命令、退出码与耗时

### Notebook 执行方式

教程从已安装的 jupyter-notebook tutorial 模板初始化，再填入本项目内容。运行证据来自新的共享 globals 字典中按序进行的 CPython `exec`，**不是 Jupyter kernel 执行**。当前环境没有 nbformat、nbclient、ipykernel；不为本任务安装它们。代码不使用 magics、shell escapes、富输出、异步顶层语法或 widgets，因此可直接在现有 Jupyter 环境中重启内核并运行全部。

结构检查是本项目的受限 JSON/输出检查，不冒充 nbformat 官方校验。每个代码单元均编译，执行计数连续，输出无错误；详情见 [evidence/notebook-validation.json](evidence/notebook-validation.json)。

## 独立复核

另有[独立代码审计](evidence/independent-review/independent-review.zh-CN.md)和[额外oracle](evidence/independent-review/independent_review.py)。它不导入主测试套件，重新构造成员位型、区间多边形面积、兼容性概率及矩级数；记录见[独立结果](evidence/independent-review/independent-results.json)。

除复核全部49关系格和计数外，额外检查819组多horn参数（298定义、521零质量）、340组非空证言向量、547组恰k模型（405定义、142零质量）、441组精确有理数区间面积、10组接近r=1的矩级数及14组logit变量积分。它还在全新进程中独立重放16个notebook代码单元。

审计曾发现p.401原直接浮点闭式的接近1消减误差及大r溢出，现已改用100位Decimal中间计算；前后日志均保留。固定网格积分的极端参数精度不受保证，相关界限已明示。`run_checks.py`会在主运行之后重跑独立oracle，使其哈希对应最终notebook。

## 数学与历史边界

1. **八命题采用明确的现代集合语义。** U、X、Y均为有限集合，补集相对于U。全称A/E不内置存在蕴涵；空主词可使A/E为真而I/O为假。原文的存在讨论见p.383。
2. **非退化域单列。** 七分类及原文式的存在推论使用非空 proper terms，即每项及其补集都非空。`relation()`拒绝空项或全域项，`relation_matches()`允许检查其退化冲突。
3. **重叠下界不依赖概率。** `max(0,m+n−1)`来自容斥，可给出一般有限集证明和达到下界的构造。测试只是额外证据。
4. **随机子集不同于随机区间。** p.385–387两种机制不能混算。“未观察到依赖”不等于已证明独立、均匀。1000个对象中两份各100个的均匀随机子集，有交集的赔率约68040.847:1；两段长度1/10的均匀随机区间，无交叠概率64/81。
5. **概率公式是一种受约束的产品模型。** `conditional_product()`先选独立基准分布，再删除不兼容状态并归一化。输入参数通常不再等于条件化后的边际。仅给边际与允许组合，不足以恢复任意依赖。
6. **论证失败不等于结论为假。** p.397保留支持、反对、均不定三项；p.398另用authority参数分配结论真伪。零兼容质量报错，不将0/0强行填成0或1/2。
7. **p.401单独用浮点数值实验。** 核心离散模型都用Fraction；未知authority闭式用100位Decimal中间精度后返回float，独立Simpson积分用float，显式对比误差。原文计算的是按给定密度平均已归一化结果，不自动等于把同一密度当成条件化前超先验的完整层次更新。高精度中间计算防止r接近1时的消减误差及大r的浮点溢出；固定网格积分仅作为r=0.1..10的温和参数核查，不承诺极端r时的精度。
8. **有限穷举不是全文一般证明。** 八原子占据模型只保留区域是否为空，不保留个数、比例或无穷结构；不能用于替代数量定理。程序不复现原文全部渐近级数、历史优先权论证或每个修辞例子。

## 两处必须保留的审计区别

### p.396：原印式与代数换元不一致

原文二权威混合式为：

```text
q = λμ + (1−λ) μμ′/[μμ′+(1−μ)(1−μ′)]
```

同页随后给authority印式：

```text
(a+a′−2λa′(1−a))/(1+aa′)
```

若按p.393的定义a=2μ−1，混合式应变成：

```text
(a+a′−λa′(1−a²))/(1+aa′)
```

取μ=3/4、μ′=4/5、λ=1/3，混合给q=45/52，故authority=19/26；字面印式给9/13。源码保留 `printed_biased_authority()` 供对照，未无声修改历史公式。这个局部不一致不否定全部概率讨论，也不裁定后来是否有勘误。

### pp.388–392：原文26/14，不是本算法的24/12

原文报告64个前提对，32个有结论，删6个后剩26个有向形式，即12对+2单式、14个对换类。程序也得到32个有结论，但若允许非空proper项下**所有语义有效的单前提弱化**，则删8个，余24个有向/12个对换类。

额外两项是原文保留的AA和ee：A蕴涵i，所以AA→i可弱化为Ai→i；e蕴涵O，所以ee→I可弱化为Oe→I。反过来，加强这些较弱式的一项前提可分别得到AA→i与ee→I。这是本实现明确准则下的差异；不将现代24/12写成原文数，也不声称历史26/14已按同一算法复现。源码及结果把两者并列。

## 实际主测试范围

数字是模型、参数或格子数，不是测试方法数；各组可能重叠，不应加成一个含糊的“总验证量”。

| 对象 | 范围 | 数量 |
| --- | --- | ---: |
| 八命题与独立逐对象量词、四矛盾对 | n=0..5全部类对 | 1,365 |
| 24种表达归为8组三个等价式 | n=0..4全部类对 | 341个类对，各24式 |
| 存在蕴涵与七关系互斥完备 | n=2..5非空proper类对 | 1,136 |
| 交集下界 | n=1..7全部类对 | 21,844 |
| 每组基数的下界可达到 | n=1..7全部(|S|,|T|) | 203 |
| p.408原表 | 6×6原表及P相关情形 | 36个印表格；共49个关系对 |
| 三项原子占据 | 全部256模式，保留proper项 | 193 |
| 交叉检查p.408组合表 | n=2..5全部proper三项 | 29,968 |
| p.388有无结论与现代弱化 | 8×8前提对 | 64 |
| 随机固定大小子集的直接统计 | n=0..6全部类对，按基数分组 | 5,461个类对；140组 |
| 连续区间独立位置网格 | 5组参数，每组400×400中点 | 800,000个位置对；数值误差容限0.005 |
| 三份authority产品条件化 | 9点网格的三元组 | 681个定义值；48个零质量拒绝 |
| 反对论证产品条件化 | 9点网格的二元组 | 80个定义值；1个零质量拒绝 |
| p.398及其二horn化约 | 9点网格的三元组 | 704个定义值；25个零质量拒绝 |
| p.401闭式对独立Simpson积分 | 两种密度×7个r | 14组，每组20,000区间 |

另有p.396印式负控制、p.405原三瓮组合及删黑球不变性、恰k子集权重、相同边际但不同联合分布、输入校验与零质量边界。

## 代价与复现原则

默认全套主测试约1秒量级，具体以 `evidence/commands.json` 的本次实测为准。没有训练或性能基准，不把单机耗时当理论复杂度。集合枚举类对数量为4^n，三项为8^n；示例上界刻意很小。日志只保留命令、输出、时间和一般环境信息，不收集主机名、用户名、HOME、环境变量或任何凭据。
