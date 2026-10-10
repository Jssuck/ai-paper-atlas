# De Morgan 1852：逆否形式与间接证明的教学复现

核验日期：2026-10-10。全部实现和测试只使用 Python 标准库，无需网络、没有安装依赖。这里复现的是可检验的现代语义模型，不是历史程序，不是自动证明器，也不复刻原文几何证明。

## 1. 来源与边界

一手文献：Augustus De Morgan，*On Indirect Demonstration*，*Philosophical Magazine*，第四辑第4卷第27期，1852年12月，第435–438页；文末署1852年11月1日。[出版社条目](https://doi.org/10.1080/14786445208647158)；[原卷扫描](https://archive.org/download/londonedinburghp04maga/londonedinburghp04maga.pdf)。扫描 PDF 第449–452页对应原刊435–438页，438页后半已是下一篇文章。

原文435页区分 direct positive、direct contrapositive、indirect positive、indirect contrapositive；两种全称形式为 Every A is B 与 Every not-B is not-A，两种被反驳的存在形式分别找 A 中的 not-B 与 not-B 中的 A。436–438页讨论逻辑转换、几何证明和教学用途。

本包三层各有不同地位：

1. 经典二值表和共同论域上的类解释，是对原文两种命题“同义”的现代教学重构。
2. 两种反例集合相同，并不证明两种证明写法、发现路线、知识难度相同。程序没有判断几何证明是否“直接”，也不裁决 Sylvester 的一般性主张。
3. 直觉主义 Kripke 模型只用于说明现代语义边界。它不是 De Morgan 原文内容；不能把1852年的论断改写为跨所有逻辑都成立的定理。

## 2. 经典定义：先命题，再证明

经典真值仅有真、假；物质蕴涵定义为：

```math
p\to q\quad\equiv\quad\neg p\lor q.
```

四行表直接检验：

```math
(p\to q)\quad\equiv\quad(\neg q\to\neg p).
```

这里的“等值”指对每个二值赋值真值相同。它没有说两份证明包含相同的步骤，也没有把条件倒过来。逆命题 $`q\to p`$ 在 $`p`$ 假、$`q`$ 真时为假，而原命题为真。

`logic.py` 的 `implication` 拒绝把整数1或字符串当作布尔值，以免数据类型悄悄改变含义。

## 3. 类解释与相同的反例

固定同一个有限论域 $`U`$，且 $`A,B\subseteq U`$。not-A 和 not-B 分别严格解释为 $`U\setminus A`$ 与 $`U\setminus B`$。

```math
\text{Every A is B}\quad\Longleftrightarrow\quad A\subseteq B,
```

```math
\text{Every not-B is not-A}\quad\Longleftrightarrow\quad
U\setminus B\subseteq U\setminus A.
```

它们失败的见证集合分别为：

```math
W_1=A\cap(U\setminus B),\qquad
W_2=(U\setminus B)\cap A.
```

$`W_1=W_2`$ 由交集交换律成立。每个元素同时是两句的反例；两个全称句都恰在这个集合为空时成立。这是普遍的集合恒等式，有限测试只是检查实现，不是靠5,461个例子证明任意集合的恒等式。

手算例：$`U=\{0,1,2\}`$，$`A=\{0,1\}`$，$`B=\{1,2\}`$。not-B 为 $`\{0\}`$，两种反例集合都是 $`\{0\}`$，因此两句同为假。

本模型的全称量化不带存在承诺：A 为空时 Every A is B 为真；空论域也单独测试。不能由这些结果推出历史上每种全称句用法都没有存在预设。超出共同论域的类会被拒绝，避免对两次补集暗中改换论域。

枚举 $`\lvert U\rvert=n`$ 时，每个元素对于 A、B 的归属有4种选择，故共有 $`4^n`$ 类对；A 是 B 的子集排除“在 A 不在 B”一种，故两句皆真的类对恰有 $`3^n`$。程序对 $`n=0,1,\ldots,6`$ 全部枚举，共5,461对；没有真假或见证集合不一致。

## 4. 现代边界：真正的递归强迫

框架是非空有限世界集 $`W=\{0,\ldots,n-1\}`$ 和自反、传递的关系 $`\preceq`$。这里只要求预序，不要求反对称性，因此枚举包含彼此可达的不同标号世界。原子赋值 $`V(p)\subseteq W`$ 必须向上封闭：若 $`w\in V(p)`$ 且 $`w\preceq v`$，则 $`v\in V(p)`$。

定义 $`w\Vdash F`$ 表示世界 w 强迫公式 F：

- 原子：$`w\Vdash p`$ 当且仅当 $`w\in V(p)`$。
- 假式：任何世界都不强迫 $`\bot`$。
- 合取：同一世界同时强迫两个子公式。
- 析取：同一世界至少强迫一个子公式。
- 蕴涵：所有可达未来都满足“若强迫前件，就强迫后件”，包括当前世界本身。

```math
w\Vdash(F\to G)
\quad\Longleftrightarrow\quad
\forall v\in W\,[w\preceq v\Rightarrow(v\Vdash F\Rightarrow v\Vdash G)].
```

```math
\neg F:=F\to\bot.
```

因此，强迫否定要求每个可达世界都不强迫被否定公式，不能替换成当前世界求值结果的 Python `not`。递归求值器内部出现的 `not visit(v,a) or visit(v,b)` 只是用经典元语言判断已遍历的每个未来是否违反强迫定义，不是在把对象语言否定改为真值取反。

`Frame` 检查自反性、传递性和世界编号；`Model` 检查所有原子赋值的持久性与重复名称；未赋值的原子报错而非默认为假。`force` 递归下降公式树，并对蕴涵遍历所有可达未来。没有用经典真值表代替它。

### 可逐项手算的两世界反例

$`0\preceq0`$、$`0\preceq1`$、$`1\preceq1`$；$`V(p)=\{0,1\}`$，$`V(q)=\{1\}`$。

1. 0 强迫 p，但不强迫 q，所以当前世界已经见证 0 不强迫 $`p\to q`$。
2. 0 不强迫 $`\neg q`$，因为它的未来1强迫 q；1也不强迫 $`\neg q`$，因为它自身强迫 q。
3. 两个可达未来都不强迫 $`\neg q`$，所以0强迫 $`\neg q\to\neg p`$。
4. 1 强迫 $`p\to q`$，因为它唯一可达的世界1同时强迫 p、q。因此0也不强迫 $`\neg(p\to q)`$。

第4步尤其重要：“0不强迫原命题”不是“0强迫原命题的否定”。这个模型反驳逆向恢复的普遍有效性；没有反驳经典二值等值，也没有否定直觉主义中由 $`p\to q`$ 推出 $`\neg q\to\neg p`$ 的方向。

## 5. 独立解释器与有限穷举

`oracle.py` 不调用 `Model.force` 或 `Frame.future`。它用栈自底向上建立每个公式的强迫世界集合：合取是交集，析取是并集；蕴涵先计算“前件成立、后件不成立”的坏世界，再排除一切能到达坏世界的世界。

对1、2、3个带标号世界，程序枚举所有自反、传递关系，再枚举 p、q 的所有向上封闭赋值，并检查每个世界。公式集是 `formula_suite()` 中明确列出的25个公式，包含前向/反向逆否式、排中律、双重否定消去、合取/析取、否定合取与否定析取。这里只把后几类作为语义实现的交叉测试，不假定所有列出的公式都是有效式。

实际数目：

| 世界数 | 预序数 | 赋值模型数 | 带指定世界模型数 | 公式-世界比较数 | 逆向公式不强迫数 |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 4 | 4 | 100 | 0 |
| 2 | 4 | 38 | 76 | 1,900 | 2 |
| 3 | 29 | 632 | 1,896 | 47,400 | 90 |
| 合计 | 34 | 674 | 1,976 | 49,400 | 92 |

两个解释器没有出现不一致，任何被检查公式的强迫集合都保持向上封闭。前向公式 $`(p\to q)\to(\neg q\to\neg p)`$ 的不强迫数为0；逆向公式 $`(\neg q\to\neg p)\to(p\to q)`$ 的不强迫数为92。这里按带指定世界的模型计数，未除去同构副本，也不只检查能到达全框架的根。

这不是任意逻辑有效性的自动判定，也不是形式验证。穷举范围不包含4世界及以上框架、其他原子数、全部公式或全部证明。两个实现共享公式和框架结构，因此交叉检验不能消除所有共同建模错误；手算轨迹、精确预期测试及独立审查补充这一限制。

## 6. 准确运行方法与实跑记录

在本 README 所在目录执行：

```sh
python3 reproduce.py
python3 reproduce.py --check
```

聚合命令会按顺序实际执行以下命令，写入实际返回码，并最后生成校验清单：

```sh
python3 -m unittest -v test_logic > tests.log 2>&1
python3 run_examples.py > results.json 2>&1
python3 make_report.py > trace_tables.zh-CN.md 2>&1
python3 build_notebook.py > notebook_build.log 2>&1
python3 verify_notebook.py > notebook_verify.log 2>&1
```

实际24项单元测试全部通过，覆盖四行真值、逆命题反例、空类/空论域、共同论域约束、精确见证、非法公式、缺失赋值、自反性、传递性、赋值持久性、当前/未来/分支世界、循环预序、输入集合拷贝、递归嵌套、非强迫与否定区别、一世界退化为经典模型、有限穷举、重复执行一致性。

`environment.json` 保存 Python 实现/版本、系统、CPU 架构及 libc，不收集用户名、主机名、密钥或绝对路径。`commands.log` 保存相对命令和实际退出码。`results.json`、状态表和 notebook 捕获输出应逐字确定；测试日志中的实测耗时以及环境信息允许因机器变化。校验和对应本次交付的实际字节，并非跨环境固定值。

## 7. 8格中文 notebook 与诚实的验证边界

`tutorial.ipynb` 有4个 Markdown 单元和4个 Python 单元：真值表、类见证、两世界模型、有限全检。标准库逐格读取和执行4个代码单元，全部通过，共享一个新进程中的命名空间；输出来自真实捕获，`execution_count` 全部保持 null。

这里没有运行 Jupyter 内核，没有使用 nbformat 的完整 schema 校验器，没有完成 Jupyter 界面渲染检查；基础 JSON 与单元结构检查不能冒充上述检查。Notebook 由随附 `build_notebook.py` 生成；没有安装任何额外依赖。读者已有 Jupyter 时，可在同目录打开并从头运行所有单元；核心复现完全不需要它。

## 8. 文件与建议顺序

- `logic.py`：经典/类语义、不可变公式树、预序与递归强迫。
- `oracle.py`：独立集合解释与有界全检。
- `test_logic.py`：24项测试。
- `run_examples.py`、`results.json`：确定性实验及实际原始结果。
- `make_report.py`、`trace_tables.zh-CN.md`：从结果生成的易读表和手算路线。
- `tutorial.ipynb`、`build_notebook.py`、`verify_notebook.py`、`notebook_check.json`：教学 notebook 及可审计的生成/执行过程。
- `reproduce.py`：按顺序重建证据、记录环境和返回码，并计算 SHA-256。
- `tests.log`、`commands.log`、`notebook_build.log`、`notebook_verify.log`、`environment.json`：本次实际执行证据。
- `code_review.zh-CN.md`：独立代码与数学审查摘要。
- `SHA256SUMS`：本目录所有交付文件的校验值，排除清单自身及缓存目录。

建议先手算两行真值、一个集合反例与两世界的0点，再对照状态表，最后运行测试。能说清“公式在当前世界不被强迫”和“公式的否定被强迫”的区别，比仅记住92这个枚举数字重要。
