# Church 1932：λ 替换与归约的现代教学重建

本目录是文章配套的可运行小实验，不是 1932 年论文的全部逻辑系统，也不是其定理的机器证明。只有 Python 标准库；未安装任何新依赖。

## 先看历史边界

原始文献：Alonzo Church, “A Set of Postulates for the Foundation of Logic,” *Annals of Mathematics* 33(2), 1932, pp.346–366；[JSTOR 原始条目](https://www.jstor.org/stable/1968337)。页码指纸面页码。

- **p.352 的语法**允许从任意良构 M 写出 λx[M]，没有要求 x 必须在 M 中出现。因此不能把原文的全部良构语法直接说成“禁止常量抽象的 λI 子集”。
- **pp.355–356 的 Rule II/III**另有发生条件：x 必须在 M 中出现；M 的绑定变量还须避开 x 及 N 的自由变量。原规则属于真命题 J 内的转换，并非这里独立运行的现代解释器。
- 本实验的 `modern` 模式是现代捕获避免 β 归约，允许擦除未使用的实参；`non_erasing` 模式仅在 x∈FV(M) 时收缩 (λx.M)N，自动进行需要的 α 改名。它是在现代项表示中抽出历史发生限制的**教学近似**，没有逐字实现原文全部避碰条件、Rule I/III、Rule IV/V、逻辑常量及 37 条公理。
- 原文避碰条件排除了 M 内对 x 的绑定，因此其发生条件可在适当 α 整理后用自由发生表达。本程序直接检查自由发生；仅有内层同名绑定不算。例如 (λx.λx.x)z 的外层参数并未使用。
- 原文 p.357 用 Rules I、II、III 的有限序列说明 conversion；本程序只执行定向的 β 收缩，没有把“完整转换关系”替换成某一种求值策略。
- **数字编码、加法、乘法是后来的教学重建**；这里不声称 1932 年这篇论文已经给出这些编码，也不将其冒充历史原实验。

## 文件

- `experiment.py`：不可变抽象语法树、捕获避免替换、α 等价、两种策略和两种规则模式、预算与循环报告、数字示例
- `test_experiment.py`：32 项单元测试，内含 6,084 组小项替换与自由变量性质检查及 64 个加乘网格组合
- `independent_checks.py`、`independent_checks.log`：额外的独立有限交叉检查及真实日志，覆盖 333,384 组替换、4,304 个实际收缩步骤、72 组加乘输入和 3 个新鲜名称冲突例
- `church1932.ipynb`：中文说明与已经实际执行的 8 个代码单元
- `execute_notebook.py`：无需 Jupyter 依赖的受限执行器
- `results.json`：实际运行得到的完整实验结果与归约轨迹
- `tests.log`、`notebook_execution.log`：实际测试和逐格执行日志

## 运行

需要 Python 3.10 或更新版本。进入本目录后：

```sh
PYTHONDONTWRITEBYTECODE=1 python experiment.py --output results.json
PYTHONDONTWRITEBYTECODE=1 python -m unittest -v test_experiment
PYTHONDONTWRITEBYTECODE=1 python independent_checks.py
PYTHONDONTWRITEBYTECODE=1 python execute_notebook.py
```

若希望重写日志：

```sh
PYTHONDONTWRITEBYTECODE=1 python -m unittest -v test_experiment > tests.log 2>&1
PYTHONDONTWRITEBYTECODE=1 python independent_checks.py > independent_checks.log
PYTHONDONTWRITEBYTECODE=1 python execute_notebook.py > notebook_execution.log 2>&1
```

Notebook 使用标准 nbformat 4 格式。本次环境没有 Jupyter 内核包，因此已用附带标准库执行器从第一格到最后一格执行，并将真实 stdout/stderr 写入 `.ipynb`。这不是通过 Jupyter 内核执行的声称。执行器不支持 IPython magic、富显示或末行表达式自动显示；本 notebook 只用普通 Python 和显式 `print`。已有 Jupyter 的读者也可从本目录启动 Python 内核正常逐格运行；导入模块就在 notebook 同目录，无绝对路径依赖。请仅执行可信 notebook。

## 关键结果

1. 身份函数 (λx.x)a 在两种策略与两种模式下均一步得到 a。
2. λy.x 中替换 x:=y 时，正确结果为 λy_0.y，自由变量仍为 y；故意错误的替换器得到 λy.y，错误地捕获 y。两者不是 α 等价。
3. 令 K=λa.λb.a，Ω=(λx.x x)(λx.x x)：现代最左最外归约使 K y Ω 两步得到 y；现代最左最内在第 2 步观察到循环。
4. **同一个 K y Ω 在非擦除最左最外模式下也观察到循环**：得到 (λb.y)Ω 后不能擦除 Ω。这正是不能把现代示例当作 1932 原规则演示的原因。
5. (λx.y)z 在现代模式下一步得到 y；在非擦除模式下零步停止。后者只相对于当前规则模式是正规形，仍含现代 β 可归约式。
6. 数字示例在现代最左最外模式下得到 2+3=5、2×3=6、0×3=0，分别执行 6、7、3 次 β 收缩。

## 术语与结果语义

- `normal`：最左最外的**强**归约；`applicative`：最左最内的**强**归约。两者都会进入 λ 体，后者不等于常见编程语言里不进入 λ 体的弱 call-by-value。
- `alpha_equivalent` 用 de Bruijn 结构键比较：绑定变量编码为距离最近绑定处的索引，自由变量保留原名。它不是 β 或 η 可转换性判定器。
- 一次收缩即使得到字面相同的项，也算一步。Ω→Ω 不能误报为没有可归约式。
- `normal_form`：当前模式下没有获准的收缩位置；不是关于原论文可证性的判断。
- `cycle_detected`：固定确定策略下出现重复的 α 等价类，并给出循环起点和长度。对于 Ω，这能直接展示特定序列的自循环。
- `step_limit`：已经用完给定 β 收缩预算，**结论未定**。超限不能独自证明发散。程序同时给出关闭循环检测的 Ω 例子与八步内持续增长而未重复的例子。

## 检验范围与限制

32 项测试全部通过。替换性质检查遍历深度不超过 2 的 507 个项，配 3 个变量和 4 个替换项，并与独立的局部无名结构替换参照实现比较；数字网格对 0–3 的输入，在两种策略下分别检查加法及乘法，共 64 组。这些都是有限检查，不能证明一般合流性、一般正规化性质或不可判定性，更不能证明 1932 年完整体系的一致性。

额外交叉检查枚举变量名为 x、y、节点数为 1–7 的全部 2,874 个项，使用节点数为 1–4 的 58 个项作为替换对象，并用独立编写的无名结构和替换参照核对结果；两种模式、两种策略中的实际单步收缩另检查自由变量不变式。72 组算术检查是 0–5 的加法和乘法网格，使用现代最左最外策略。这些计数与上面的单元测试覆盖分开列示，不把重叠检查当成互不相交的样本。

这里没有 η 归约、类型系统、解析器、图共享、弱求值或完整逻辑推理引擎。递归实现面向小型教学项；极大的用户自建项可能触及 Python 递归深度或内存限制。β 步数上限也不是内存或墙钟时间上限。源文件中唯一故意错误的函数是标注为演示用的 `naive_substitute`，正式归约器不会调用它。
