# Sheffer 1913：五条公设、独立性反模型与单联结词翻译

这是针对 H. M. Sheffer, *A Set of Five Independent Postulates for Boolean Algebras, with Application to Logical Constants* (1913), pp. 481–488 的**原创教学重构**。原论文没有软件、训练过程、数据集或机器学习评测。本目录不是作者代码，也不声称用有限实验证明了无限的一般定理。

读者只需理解真值表、函数与 Python 的基本循环。建议先打开 [`tutorial.zh-CN.ipynb`](tutorial.zh-CN.ipynb)，再查看实现与测试。Notebook 已按顺序执行，保留真实输出；执行方式为 Python 标准库 runner，而非 Jupyter/IPython kernel，详见后文。

## 1. 快速重跑

要求 Python 3.10 或更高版本；本次环境是 Python 3.12.14。**只用标准库，不需要安装包、联网、下载模型或 GPU。**

```bash
cd reproduction/sheffer-1913
python -m unittest -v
python run_experiments.py --out results/experiments.json
python execute_notebook.py tutorial.zh-CN.ipynb
```

测试会用两个不同实现交叉检查全部 19,700 个小型封闭运算表，通常比单独生成实验摘要耗时更长。实际环境、执行输出及耗时见 [`results/environment.txt`](results/environment.txt)、[`results/tests.log`](results/tests.log)、[`results/experiments.log`](results/experiments.log) 与 [`results/notebook-execution.log`](results/notebook-execution.log)。不把运行时间作为算法性能评测。

## 2. 原文的五条公设（第482页）

给定类 $`K`$ 和二元 K-rule $`a \mid b`$，定义 $`a' = a\mid a`$：

1. P1：K 至少有两个不同元素。
2. P2：若 a、b 在 K 中，则 a | b 也在 K 中。
3. P3：$`a^{\prime\prime}=a`$。
4. P4：$`a\mid(b\mid b')=a'`$。
5. P5：$`(a\mid(b\mid c))'=(b'\mid a)\mid(c'\mid a)`$。

**P3–P5 有条件：变量和式中指示的组合都必须是 K 元素。** 第481页脚注定义 K-rule：它的输入域是 K×K，不预先要求输出也在 K 中。是否封闭是 P2 的内容。

这影响独立性验证：若一开始把运算类型写死为 K×K→K，那么 P2 已经被当作程序前提，再搜索也不会找到 P2 的反模型。本实现的 `FiniteKRule` 允许输出 `outside`；表达式求值遇到不在 K 中的子项便停止，把该赋值记为 `guard_skipped`，不再把外部对象送入 K-rule。`holds=True` 且 `checked=0` 表示条件命题在该有限结构中空泛成立，不能读成已经计算出全部表达式的等式。

另一个 `closed_signature` 只服务于封闭表枚举，直接用整数索引检查。测试将它与通用的 guarded AST checker 在全部 n=1,2,3 运算表上交叉比较，减少同一处实现错误被重复使用的风险。

## 3. 原论文的一致性与五个独立性例子（第483页）

所有表都按所列元素顺序，以第一个参数为行、第二个参数为列。

- 一致性例：K={m,n}，$`m\mid m=n`$，其余三格均为 m。它满足五条公设。
- P1 反例：K={m}，$`m\mid m=m`$。只否定 P1。
- P2 反例：原文允许任意大于一的元素数；这里取 K={m,n}。对角为原元素，非对角输出 `outside`。只否定 P2。在 P4 的4个赋值中2个适用，在 P5 的8个赋值中2个适用；其余分别被条件排除。
- P3 反例：K={m,n}，四格恒为 m。只否定 P3，取 a=n 即得到 m≠n。
- P4 反例：K 是**全部有理数**，$`a\mid b=-(a+b)/2`$，不是某个截断的有理数样本。
- P5 反例：K={l,m,n}，三行依次为 `(l,m,n)`、`(n,n,l)`、`(m,l,m)`。只否定 P5。27个三元赋值中有16个使 P5 失败；例如 a=l,b=l,c=m，左边为 n、右边为 m。

有限模型的逐项结果与失败见证都保存在 [`results/experiments.json`](results/experiments.json)。

### 有理数反模型为什么是全局论证

这里不能用若干有理数上的穷举代替证明。对任意有理数 a、b、c：

- P1：0 和 1 是两个不同有理数。
- P2：有理数的和、取负及除以2仍是有理数。
- a′=−a，因此 a″=a，P3 成立。
- b|b′=−(b−b)/2=0；P4 左边为 −a/2，右边为 −a。因此 P4 只在 a=0 时成立，例如 a=1,b=0 时左边 −1/2≠−1。
- P5 左边：$`(a\mid(b\mid c))'=a/2-b/4-c/4`$。
- P5 右边：$`b'\mid a=(b-a)/2`$、$`c'\mid a=(c-a)/2`$，再组合得到 $`a/2-b/4-c/4`$。两边对任意有理数相等。

`rational_bar` 将整数先转换为 `Fraction` 再除以2，避免大整数被浮点舍入；混合整数与 `Fraction` 仍精确，浮点输入明确拒绝。符号检查只接受两个 `Linear` 形式，不将它们与数值输入混用。

`Linear` 用三维 `Fraction` 系数表示这些齐次线性式，机械核对系数相同。它是针对这些式子的精确符号演算，不是通用定理证明器。测试中的125个有理数三元组仅是额外的回归检查；有限样本本身不宣称构成此反模型的 K。

有理数 P5 的共同结果也可写为：

```math
\left(a\mid(b\mid c)\right)'=(b'\mid a)\mid(c'\mid a)=\frac{a}{2}-\frac{b}{4}-\frac{c}{4}.
```

## 4. 有限封闭运算表枚举：结果与边界

在固定带标签集合 `{0,…,n−1}` 上，二元封闭表共有 $`n^{n^2}`$ 张。这里完整枚举 n=1,2,3，既不随机采样，也不按同构去重：

| n | 检查的表数 | 满足 P1–P5 的表数 |
|---|---:|---:|
| 1 | 1 | 0 |
| 2 | 16 | 2 |
| 3 | 19,683 | 0 |

n=1 的表满足 P2–P5，但失败于 P1。n=2 的两张合格表，按 `(0,0),(0,1),(1,0),(1,1)` 顺序分别为 `[1,0,0,0]` 和 `[1,1,1,0]`，在固定 0=false、1=true 的解释下就是 NOR 与 NAND。交换底层元素的命名可以把这两个抽象运算结构对应起来；在固定真值编码下，它们仍是不同真值函数。

**这些实验只覆盖上述有限阶数。** n=3 未发现模型不是对于任意阶数的枚举结果，也不代替原文从五条公设导出 Boolean algebra 性质的证明。n=4 有 4^16=4,294,967,296 张表，本教学程序明确拒绝直接穷举。封闭枚举中 P2 自动为真，不能拿这个枚举讨论 P2 独立性。

## 5. 原文的 rejection 是 NOR；NAND 在对偶说明中出现

第487页的主解释是 $`p\mathbin{\mathrm{rejection}}q=\neg(p\lor q)`$，即 neither–nor：

| p | q | NOR | NAND |
|---:|---:|---:|---:|
| 0 | 0 | 1 | 1 |
| 0 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 1 | 0 | 0 |

原文给出 $`\neg p=\mathrm{NOR}(p,p)`$ 和 $`p\lor q=\mathrm{NOR}(\mathrm{NOR}(p,q),\mathrm{NOR}(p,q))`$。第488页脚注说，通过对偶，第二节的结果也可在 “either not-p or not-q” 的解释下成立，即 NAND。不能把正文的 neither–nor 默默替换成今天经常称为 Sheffer stroke 的 NAND。

`translate` 按语法树递归构造只含一种二元门的表达式。对 NOR，以上两条定义正对应原文；对 NAND，NOT 为 $`\mathrm{NAND}(p,p)`$，OR 为 $`\mathrm{NAND}(\mathrm{NAND}(p,p),\mathrm{NAND}(q,q))`$。解析器的 `&` 和 `->` 是**现代教学扩展**，并非声称原文给出了编译器。

解析器接受变量、`~` 或 `!`（NOT）、`&`（AND）、`|`（OR）、`->`（蕴含）及括号，优先级依次降低；蕴含向右结合。注意：**解析器输入里的 `|` 表示普通 OR，不是前面公设中的历史运算 `|`。** 输出用文字 `nor`/`nand` 消除歧义。程序不使用 `eval`，不接受 Python 程序作为公式。

语义保持的一般说明可用结构归纳：变量不变；假定较小子式已保持真值，对 NOT/OR 使用相应定义即可保持外层真值。实验则只检查高度≤2、变量 p,q、联结词 NOT/OR 的74个语法树；两个目标基、每式四个赋值，共592项检查，0个不匹配。额外测试覆盖 AND、蕴含和三变量例子。这个递归构造及其归纳说明与有限回归实验必须区分。

两个故意错误的负对照都被抓到：把 OR 直接写成 NOR，赋值 p=q=false 时失败；把原 NOR 的 OR 公式仅改名为 NAND，p=false,q=true 时失败。正确的 NAND 对偶翻译需要改变定义，不能只换名字。

## 6. 文件与执行方式

- `sheffer.py`：guarded 公设检查、原文反模型、精确有理数线性式、封闭表枚举、解析及单门翻译。
- `test_sheffer.py`：25个 `unittest` 测试，包括全部小表交叉检查、正例、负例、输入错误和范围保护。
- `run_experiments.py`：生成实验摘要及 JSON。
- `tutorial.zh-CN.ipynb`：8个代码单元，按教学顺序配有说明、练习、答案及保留输出。
- `execute_notebook.py`：标准库顺序执行器；共享干净的命名空间、保存 stdout/stderr、执行编号及错误状态。本教程不含 IPython magic 或富媒体显示。它不是 Jupyter kernel，不能据此声称测试了 kernel 相关行为。
- `SOURCES.md`：一手来源、扫描页码映射与转录核对。
- `results/`：实际输出、环境和命令记录。

普通 Jupyter 环境也可以打开 Notebook，从其所在目录 Restart & Run All。已经保留的输出来自上述标准库执行器；metadata 明确标明执行方式，未伪称 kernel 执行。

## 7. 练习与可选延伸

先不看答案：为什么 P2 反模型中 P4 只有 a=b 的赋值需要检查？因为 b′=b，b|b′=b，而 a|b 仅在 a=b 时属于 K；这时左右均为 a。P5 的完整指示组合属于 K 则要求 a=b=c。

可选延伸：用部分表剪枝搜索 n=4，或者为任意 NOT/OR 语法树写形式化的结构归纳证明。前者仍不能替代后者，也不能替代原文第一节的表示论证。本目录没有神经网络、学习指标、现代 AI 性能结论或对一般定理的自动证明声称。
