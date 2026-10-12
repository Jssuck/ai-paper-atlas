# 定义能做什么：一个可运行的现代教学附录

这是配合孔狄亚克《逻辑》第二部第六章阅读的原创小模型。不是历史原程序复现，不是感知心理学实验，也不据此证明作者对综合法的全部判断。详细假设、一般证明和反例在 [MODEL.zh-CN.md](MODEL.zh-CN.md)；初读者可从 [逐步演练](WALKTHROUGH.zh-CN.md) 开始。

## 快速运行

要求 Python 3.10 或以上；实际验证版本见 [验证记录](VERIFICATION.zh-CN.md)。仅使用标准库，无安装、账号、网络、随机数或外部数据要求。

在本目录运行：

```sh
export PYTHONDONTWRITEBYTECODE=1
python3 demo.py
python3 -m unittest -v
python3 mutation_check.py
python3 -O -m unittest -v
python3 -OO -m unittest -v
python3 -O mutation_check.py
python3 -OO mutation_check.py
```

`demo.py` 输出确定性的 JSON。`mutation_check.py` 注入六个临时的内存级错误，然后自动恢复原函数；不编辑源文件。正常结果为六个基线通过、六个行为差异被检测、零个测试框架错误。

所有运行时验证使用明确的异常检查；测试使用 `unittest` 的比较方法，不依靠可被优化模式删除的裸 `assert`。`-OO` 会去掉文档字符串，程序行为不依赖文档字符串。

## 三件事，三个模型

1. 新鲜、无环的显式定义：对每个原始世界都有唯一扩张，不自动筛掉旧世界。
2. 从观察表达目标：当且仅当每个观察纤维内的目标值相同；失败返回两个可检查的反例世界。
3. 按规则学习：每一步都要求其全部前提已经可用；规则可导出不等于现实为真。

## 文件

| 文件 | 用途 |
| --- | --- |
| `condillac_model.py` | 表达式、定义、观察及规则模型的公开 API |
| `demo.py` | 一次跑完核心例子，输出 JSON |
| `test_condillac_model.py` | 单元测试及有边界的穷举 oracle |
| `mutation_check.py` | 六种有意义的故障注入；区分行为差异和意外异常 |
| `test_mutation_check.py` | 验证变异分类器不会把测试框架崩溃算作检测成功 |
| `MODEL.zh-CN.md` | 完整设定、一般证明、限制与反例 |
| `WALKTHROUGH.zh-CN.md` | 逐步手算和可运行的调用例子 |
| `verify.py` | 重跑普通、`-O`、`-OO` 三种模式并写出本地证据日志 |
| `VERIFICATION.zh-CN.md` | 实际环境、命令、结果与验证范围 |
| `evidence/` | 本次实际执行的标准输出、标准错误和结构化汇总 |

## 公开 API

| API | 输入、结果与重要限制 |
| --- | --- |
| `Const`, `Var`, `Not`, `And`, `Or` | 不可变表达式节点；常量必须是真正的 `bool` |
| `variables(expr)` | 返回表达式名称的 `frozenset` |
| `evaluate(expr, world)` | 求值为 `bool`；拒绝未绑定名称及非布尔赋值 |
| `enumerate_worlds(names)` | 全部原始世界的元组；零个名称产生一个空字典 |
| `Definition(name, expression)` | 可作显式定义，也可在穷举 oracle 中作等式 |
| `DefinitionSystem(primitives, definitions)` | 检查名称新鲜、唯一、依赖完整且无环；拒绝无效输入 |
| `system.topological_definitions()` | 返回稳定的拓扑排序；同可用性下按输入顺序选取 |
| `system.expand(world)` | 旧世界必须恰好给原始名称赋值；返回独立的新字典 |
| `system.worlds()` | 扩张所有原始世界，不加证据过滤 |
| `satisfying_extensions(base, equations)` | 固定旧值，穷举新增名称；允许环与旧名等式，不覆盖旧值 |
| `filter_evidence(worlds, evidence)` | 返回恰好满足证据的世界；可得到空集 |
| `entails(worlds, proposition)` | 在全部输入世界为真；空集时为空真，须另检查一致性 |
| `analyze_observations(worlds, features, target)` | 返回 `ObservationAnalysis`；成功时是实际观察表，失败时是两个反例世界 |
| `observed_formula(analysis, feature_names)` | 从预给目标的成功表生成合成观察坐标 DNF；未见观察值按约定补为假 |
| `Rule(premises, conclusion)` | 前提为有限名称集；同结论可有多条替代规则 |
| `forward_closure(seeds, rules)` | 返回给定种子和规则的最小闭包 `frozenset` |
| `plan_learning(seeds, rules)` | 返回所有可导出新名称的一个合法顺序 |
| `verify_order(seeds, rules, order)` | 返回 `OrderReport`；失败索引从 0 开始；有效前缀不要求覆盖整个闭包 |

目标真值由调用者预先给定；程序检验可表示性，不学习未知目标标签。`observed_formula` 的名称是相互不同的合成观察坐标，求值时必须把它们绑定为特征值，而不是凭同名去取原始量。

`ObservationAnalysis` 字段为 `definable`、`table`、`witness`。表是 `(观察布尔元组, 目标布尔值)` 行的元组，按观察元组排序。不可表示时表为空，`witness` 有两个独立世界字典。结果中的字典是快照但并非只读对象。`observed_formula` 要求实际的 `ObservationAnalysis` 记录和严格布尔类型的 `definable` 字段，并检查表的行宽、布尔值与重复签名；`OrderReport` 仅为输出记录。

`OrderReport` 字段为 `valid`、`known`、`failure_index`、`reason`、`missing_alternatives`。失败时 `known` 只包含合法前缀已得到的名称；`missing_alternatives` 对每条同结论的候选规则列出尚缺前提。没有候选规则时该字段为空。

## 验证覆盖与未覆盖

- 求值器：全部 0、1、2 个原始变量的 22 张布尔真值表。
- 保守扩张：176 个有序输入系统，共 592 个原始世界个案；枚举首定义的全部小布尔函数，次定义的全部一元布尔函数，以及两种输入顺序。另检查全部小旧语言布尔谓词的真值不变。
- 观察可表示性：0、1、2 个原始变量以及 0、1、2 个特征下，共 4,466 组全世界真值表组合。独立 oracle 枚举所有观察值到布尔值的函数。
- 规则闭包：两个名称上的全部 256 个规则集、全部 4 个种子集，共 1,024 个案；另核对 5,120 个不重复的提议次序。闭包 oracle 取全部闭合超集的交。
- 人工边界：空世界、空观察、循环方程的零解/多解/唯一解、旧名复用、空前提、替代规则、带种子的规则环、重复步骤、不可导出步骤及严格输入检查。

这不是性能基准、安全审计或一般定理的机器证明。测试规模有限；模型舍弃了概率、噪声、时间成本、心理机制和自然语言歧义。没有把这些未建模部分当作已经验证。
