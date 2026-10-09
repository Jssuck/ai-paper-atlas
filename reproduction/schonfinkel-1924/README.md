# Schönfinkel 1924：纯标准库教学复现

这是一份用现代 Python 编写的教学模型，帮助理解组合子如何消去变量。它不是 1924 年论文的原始实验代码，不包含原文 PDF，也不声称实现了原论文的全部逻辑体系。核心代码只依赖 Python 标准库，无网络、随机性、凭证或安装步骤。

## 记号先对齐

| 本项目 / 原论文记号 | 常见现代记号 | 行为 |
|---|---|---|
| I | I | I x → x |
| C | K | C x y → x |
| T | C | T f x y → f y x |
| Z | B | Z f g x → f (g x) |
| S | S | S f g x → f x (g x) |

Python 导出的 K 是原 C 的同一对象别名；输出仍打印 C。原 C 与现代表示交换参数的 C 不能混淆。应用左结合，例如 `app(f,x,y)` 表示 `(f x) y`。

## 文件

- `combinators.py`：不可变 Var/Comb/App、最左最外一步约化、带预算正规化、现代括号抽象、有限域 U
- `test_combinators.py`：11 个测试方法，覆盖有限穷举和边界条件
- `tutorial.ipynb`：中文教学 notebook，保存了实际执行输出
- `execute_notebook.py`：仅标准库的顺序执行器
- `logs/unittest.txt`：实际测试输出
- `logs/notebook_execution.txt`：实际 notebook 执行输出
- `logs/environment.txt`：执行环境与命令
- `logs/artifact_validation.txt`：结构、输出与可移植性检查结果

## 精确运行命令

需要 Python 3.8 或更新版本；实际验收使用的版本见 `logs/environment.txt`。先进入本 README 所在目录。完整交付包中可执行：

```sh
cd reproduction/schonfinkel-1924
python -m unittest -v test_combinators
python execute_notebook.py tutorial.ipynb
```

也可在已有 Jupyter 环境打开 `tutorial.ipynb`，将工作目录设为本文件夹后从头运行。无需安装 Jupyter 即可使用上述标准库命令。本项目不会为了运行 notebook 安装依赖。

如需更新日志：

```sh
python -m unittest -v test_combinators > logs/unittest.txt 2>&1
python execute_notebook.py tutorial.ipynb > logs/notebook_execution.txt 2>&1
```

`execute_notebook.py` 支持从任意工作目录传入 notebook 的实际路径；它会将工作目录和模块搜索路径设为 notebook 所在目录。执行会原地更新 notebook 的输出。只应对可信 notebook 使用它，因其会执行任意 Python 代码。

## 执行方法的诚实边界

交付 notebook **不是通过 Jupyter 内核执行的**。执行器读取 nbformat 4 JSON，将八个普通 Python 代码单元按顺序在共享 namespace 中 `compile` / `exec`，捕获 stdout、stderr，保存单元执行序号及实际输出。它不支持魔法命令、富媒体显示、交互输入或异步单元。本 notebook 仅使用 print、普通 Python 和断言，适合这种执行方式。

文件采用 nbformat 4.5 JSON，并已检查单元 ID 唯一、执行序号连续、输出非空及无错误输出。

## 测试范围和结果

实际日志显示 11 个测试方法全部通过；notebook 的 8 个代码单元全部执行成功，其中再次运行同一测试套件。

- 五个原始组合子的每条约化规则
- 不足参数保持不可约；部分应用与额外参数保留
- 最左最外顺序：`C x Ω` 一步得到 x；也检查应用参数内的正规化
- 冻结 AST，不变更变量、组合子或应用字段
- 三条现代括号抽象规则
- 替换性质的 **1,400 个有限穷举案例**：全部 280 个 AST 节点数为 1、3、5，叶子来自 `{x,y,I,C,S}` 的表达式，分别以 `{y,I,C,I y,C y}` 替换 x
- 无捕获：自由变量 y 在替换后仍自由；变量名使用精确匹配
- 补足新鲜变量参数后验证 `I=SCC`、`Z=S(CS)C`、`T=S(ZZS)(CC)`；展开侧分别用 2、4、6 步得到预期结果
- Ω 的 25 步预算耗尽、零预算、精确预算边界和非法负预算
- 高阶 U：分别以对象域 D 和谓词域 P 构造 U；全部八个谓词时编码与 `∀f∃g` 直接枚举都为真，仅恒真谓词时两者都为假
- 三元素域 `{0,1,2}` 上全部 8 个布尔谓词的 64 个有序谓词对，验证 U 的语义；额外检查示例和空域拒绝

这些穷举是有限测试，不是一般定理的机械化证明；恒等式测试是补足参数后的约化等式，不是声称两个 AST 字面相等，也不是通用外延等价判定器。

## 替换性质为何成立：简短结构归纳

记 `[x]E` 为 `abstract('x', E)`，原 C 等同现代 K。对 E 的构造分类：

1. E 就是 x：`([x]x) N = I N → N`，正是替换结果。
2. x 不出现在 E 中：`([x]E) N = C E N → E`，而替换不改变 E。
3. 剩余情况 E 为 P Q：`S ([x]P) ([x]Q) N → ([x]P) N (([x]Q) N)`。由归纳假设，两个子项可分别约化为 `P[x:=N]` 和 `Q[x:=N]`，组合后正是 `E[x:=N]`。

这是有限语法项上存在约化序列的数学论证；它并不保证所有项有正规形。本测试器以比较正规形来检查选定的可终止案例。AST 不含 λ 绑定器，因此这里无需 α 改名；若以后扩展 λ 语法，不能直接沿用本替换函数作为捕获规避替换。

## U 是语义演示，不是第六条语法约化规则

`finite_u(domain)(f)(g)` 计算 `all(not (f(x) and g(x)) for x in domain)`，即全称量化后的「没有共同成立对象」，不是只对一个 x 的 NAND。示例要求域非空，并要求 f、g 在域中是纯、全定义布尔谓词。

高阶例子显式区分 U_D 与 U_P：`A(f)=U_P(U_D(f))(U_D(f))`，再用 `U_P(A)(A)` 编码 `∀f∈P ∃g∈P U_D(f)(g)`。每个 U 的量化域依出现位置而定，不是把同一个 U_D 闭包直接应用于自身。全部八个谓词与仅含恒真谓词的两个域分别给出真、假结果。

有限三元素枚举不等同于原论文的任意对象域量化。空域拒绝是本教学 API 的选择，不是对现代逻辑空域语义的否认。它也没有实现原论文全部量词、变量消去系统或一般逻辑有效性判定。

## 资源与模型限制

- `normalize` 的预算只计算成功约化步，不限制树大小、内存、递归深度或墙钟时间。
- 预算耗尽本身不证明发散。Ω 是特意选择的熟知自应用示例。
- S 可以重复使用参数，树表示可能快速增大；深项可能触发 Python 递归深度限制。
- 本实现没有解析器、类型系统、λ AST、α 改名、缓存、图约化或 T/Z 优化抽象。
- 关于原文 `I=SCφ` 的更一般表述，本实现不将其扩大成没有定义域/全定义条件的断言；这里只测试明确的 `I=SCC`。
