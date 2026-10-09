# Peirce 1880：有限逻辑教学重构

对应 Charles S. Peirce, *On the Algebra of Logic*, *American Journal of Mathematics* 3(1), 1880, pp. 15–57。

这是原创现代 Python 实现，不是历史软件，也不是对全文所有定理的形式化证明。它用有限集合和有限关系把若干核心步骤变成可执行、可质疑的实验。历史公式核对记录见 [SOURCE_LEDGER.md](SOURCE_LEDGER.md)，教程见 [tutorial.ipynb](tutorial.ipynb)。

## 环境与快速运行

- Python 3.10 或更新版本，仅使用标准库；实际运行环境版本见 [evidence/environment.json](evidence/environment.json)
- 不需要 pip 安装、外部服务、网络、数据集或随机种子
- 文件全部位于同一目录，进入本目录后执行：

```sh
python demo.py
python -m unittest discover -v
python execute_notebook.py tutorial.ipynb
```

默认 unittest 递归发现能找到 17 个测试方法。测试失败会返回非零退出码。`execute_notebook.py` 会覆盖此 notebook 的执行计数和输出；运行前可另存副本。

### Notebook 的执行声明

`tutorial.ipynb` 由已安装的官方 notebook scaffold 工具以 tutorial 模板初始化，然后填入本项目原创内容。交付版 31 个单元中有 15 个代码单元，已全部顺序执行。

当前证据由 `execute_notebook.py` 产生：它对可信的普通 Python 单元使用一个全新的共享 globals 字典和 CPython `exec`，捕获标准输出/错误。**这不是 Jupyter kernel 执行**，不支持 magics、shell escapes、富显示或 widget。代码单元只使用普通 Python 和 print，因此也可以在现成 Jupyter 环境中重启内核、运行全部单元。不为本任务安装额外依赖。

运行任意 notebook 等同运行 Python 代码；只执行你信任的 notebook。

## 文件

- `peirce_finite.py`：类命题、布尔展开、子句消元、原文算例、关系四运算、分类、相等模式
- `demo.py`：八组短小可复核的具体输出
- `tutorial.ipynb`：中文逐步教程、运行结果、练习及答案
- `execute_notebook.py`：透明的标准库顺序执行器
- `tests/test_peirce_finite.py`：自动发现测试与范围计数
- `SOURCE_LEDGER.md`：每组实现与原文页码之间的对应，以及未实现部分
- `evidence/`：实际测试输出、示例输出、notebook 执行记录及脱敏环境记录

另有独立检查脚本 [independent_checks.py](independent_checks.py) 与 [logs/independent-checks.json](logs/independent-checks.json)。它使用独立的位掩码量词 oracle，扩展核验 n=0..3 的全部 262,405 个关系对子（1,049,620 个四运算结果）、531 个关系分类、1,057 个原文类赋值及 273 个投影。其范围与上述 17 个测试方法分开记录；没有穷举 n=3 的关系三元组。独立脚本可用 `python independent_checks.py` 重跑。完整范围与独立 notebook 执行核验见 [independent-review.zh-CN.md](independent-review.zh-CN.md)。

## 关系公式表的独立补充

[公式附录](../../papers/1880/peirce-relative-formulae.zh-CN.md)与[supplemental_relation_checks.py](supplemental_relation_checks.py)是单独的补充，不计入17个主测试方法。运行 `python supplemental_relation_checks.py` 可重做二元素论域的40条核心等式检查；[真实日志](evidence/supplemental-relation-checks.log)与[结构化结果](evidence/supplemental-relation-checks.json)随附。

覆盖八条简单分配、八条分配展开、八条简单结合、四类各四条条件展开，共163,840次外项赋值；条件展开只在各自的行/列非空前提下要求成立。所有前提内检查通过；前提外反例另列。这不等于自动逐字核验原印全部否定变式，p55否定表右首行的并/交异常另作负例。一般证明和适用边界见附录，有限结果不能替代一般定理。[补充脚本的独立复核](supplemental-review.zh-CN.md)另行检查循环、索引、条件、反例与最终证据。

## 语义约定

1. **类**是 U 的子集。A=`S⊆P`，E=`S∩P=∅`，I=`S∩P≠∅`，O=`S\P≠∅`。空 S 使 A、E 为真，I、O 为假。
2. **二元关系**是 `U×U` 的子集；程序中 `U={0,...,n-1}`。复合 `R;S` 先沿 R，再沿 S：`∃y(Rxy∧Syz)`。
3. **所有补集**相对于明确的 U 或 `U×U`。不能将大小不同的宇宙中的关系混算。
4. **四个运算**依据 p.52 的三标记规则现代化：
   - `compose(R,S) = R;S`，`(|||)`
   - `regressive(R,S) = ¬(R;¬S)`，`(|--)`
   - `progressive(R,S) = ¬(¬R;S)`，`(-|-)`
   - `transadd(R,S) = ¬R;¬S`，`(--|)`
5. **消元**计算布尔 CNF 的存在投影。全称类包含可逐对象编码；程序没有在 CNF 中表示 I/O 的存在证人。不能把它当作完整一阶逻辑或关系演算求解器。
6. **分类**采用 p.47 定义并落实 p.57 勘误：0 同时 concurrent 与 alio；top 同时 negative-of-concurrent 与 negative-of-alio。`negative_of_X` 指补关系具有 X，不是“不具有 X”。
7. **相等模式**是变量位置的集合划分；Bell 数对应可用对象足够多的情况。大小为 n 的宇宙只能实现不超过 n 个块的划分。

## 原文算例与现代重构的区别

`boole_original` 逐项转录扫描图像上 p.39 的三组前提。`boole_six_clauses` 转录 p.41 的六个简化前提。测试在全部 16 个 x,y,z,w 赋值上，用 `v=0,1` 的直接枚举验证两者等价。

现代化简的完整约束是：

```text
x = F
F = (z AND NOT w) OR (NOT z AND w) OR (NOT y AND NOT z AND NOT w)
```

p.42 最后显示的 `top ⊆ x OR (z AND w) OR (y AND NOT z AND NOT w)` 只保留 `F⊆x`，没有保留 `x⊆F`。它允许 11 个赋值，正确投影允许 8 个；额外的 xyzw 为 1011、1100、1111。代码保留原式单独核验，没有将修订后的式子冒充原文。

p.40 中间展开出现的加号/上划线问题不被机械转写；这里直接从 p.39 前提重建，并与 p.41 六前提核对。对 p.33“由上下界规则得分配律”的过强局部声称，用 M₃ 格给出反模型；这不否认有限集合模型中的分配律。

## 实际穷举范围

下列数量是模型、赋值或检查次数，不是测试方法数量。这些数字在测试代码中有计数断言，或可由明确的循环边界直接确定。

| 检查对象 | 范围 | 精确数量 |
|---|---|---:|
| A/E/I/O、矛盾对及空主词 | n=0,1,2,3 的全部类对 | 85 |
| 两个分配律、De Morgan、吸收 | n=0,1,2,3 的全部类三元组 | 585 |
| 展开 | 全部 256 个三变量布尔函数 × 8 行 × 3 个展开变量 | 6,144 |
| 完整 CNF 的独立真值核对 | 256 个三变量函数 × 8 行 | 2,048 |
| p.39 消元规则的类语义 | n=0,1,2 的全部五类赋值 | 1,057 |
| CNF 存在投影 | 两变量的 9 个非重言子句的全部 512 个子集 × 2 个主元 × 2 行 | 2,048 |
| CNF 存在投影 | 三变量的 27 个非重言子句的 729 个有序对子 × 3 个主元 × 4 行 | 8,748 |
| 四运算的独立量词 oracle、逆关系 | n=0,1,2 的全部关系对 | 261 |
| p.55 八条简单肯定分配律 + 普通复合结合律 | n=0,1,2 的全部关系三元组 | 4,105 |
| 四种输入单调/反单调规则 | n=0,1,2 全部 `(A⊆B,C⊆D)` | 6,571 |
| 分类、补集、逆关系、单位元 | n=0,1,2,3 的全部单关系 | 531 |
| 相等模式生成器对元组直接归一化 | n=0..4，arity=0..5 | 1,799 个元组 |
| Bell 数双路径核对 | arity=0..7 | 1,1,2,5,15,52,203,877 |

另有输入校验、空公式/空子句、原文算例、非分配反例、量词交换反例、混合运算非结合反例和 M₃ 格验证。

## 边界与代价

- 本程序刻意允许空宇宙作为软件边界测试；这不是把 Peirce 的无限极限解释为一个空域。n=0、1 也不能照搬所有依赖足够多个体的历史分类叙述。
- 关系数量为 `2^(n²)`，全关系三元组为 `2^(3n²)`。n=2 有 4,096 个三元组；n=3 有 134,217,728 个，故三元穷举只做到 n=2。主测试穷举 n=3 的 512 个单关系；独立审查还穷举 n=3 的全部 262,144 个关系对子。本次没有穷举 n=3 的关系三元组。
- 复合采用可读的有序对连接，最坏比较 `|R|×|S|` 对边；不是高性能关系数据库。
- 完整真值 CNF 需要 `2^k` 行；一个变量的消元生成最多 `正子句数×负子句数` 个候选 resolvent，重复消元可能指数膨胀。
- `equality_patterns` 输出本身有 Bell 数那么多项，不能无限扩展。
- 有限验证不构成一般证明，也不能据此宣称整个 1880 系统完备、可判定或正确。
- 主模块未实现无限个体/简单项极限、所有高元关系运算、历史原符号排版系统或关系公式展开求解器。另附补充脚本只核指定40条核心式的有限语义；它不是任意规模的符号推导引擎，也不自动验证全部原印否定变式。

## 可复核性

[evidence/test-run.txt](evidence/test-run.txt)、[evidence/demo-output.txt](evidence/demo-output.txt)、[evidence/notebook-run.txt](evidence/notebook-run.txt) 均来自实际执行。输出不包含账户、凭证、主机名、远程地址或用户目录。环境记录只记录复现所需的 Python/平台信息、命令及来源 PDF 校验值。

测试是安全的只读有限计算；notebook 执行器只会改写指定本地 notebook 的输出。没有远程写入、提交、发布或第三方通信。
