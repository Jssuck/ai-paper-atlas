# 《前分析篇》I.4：第一格的现代教学复现

这是对 Aristotle, *Prior Analytics* I.4 整章分类论证的现代集合语义辅助实验，**不是声称作者写过或采用过这个程序**。只使用 Python 标准库；无需联网、安装、模型调用、API 密钥或付费服务。Python 3.10 以上可运行；此次实测版本见 `logs/environment.txt`。

## 阅读与运行

```sh
python walkthrough.py
python walkthrough.py --format json
python -m unittest discover -s tests -v
python -O -m unittest discover -s tests -v
python -OO -m unittest discover -s tests -v
python mutation_checks.py
```

在本目录执行 `sh run_checks.sh`，可重新生成 `results/` 和 `logs/`。它只读写本地文件；任一检验失败会以非零状态退出。已有日志是实际执行记录，不是预填结果。

- `categorical.py`：集合语义、规范模型、有效性检查、最小反模型
- `walkthrough.py`：中文讲解、JSON，以及 CSV 导出
- `WALKTHROUGH.md`：逐步手算与程序阅读路线
- `tests/test_categorical.py`：32 个测试方法，包括独立逐点真值 oracle
- `mutation_checks.py`：16 个有针对性的故障注入，不代表独立审计或全部可能错误
- `results/report.json`：两种语义各 64 个正向形式及全部反向诊断，每个无效形式的最小反模型
- `results/premise-pairs.csv`：16 组前提对的完整结论表
- `results/forms.csv`：每种语义 64 个正向形式，共 128 行
- `results/walkthrough.txt`：可读教学输出
- `results/mutations.json`：16 次故障注入的真实测试输出

## 语义、符号与边界

论域 U 非空，三个一元项的外延分别为 P（原文 A，大项）、M（原文 B，中项）、S（原文 Γ，小项）。程序中的 A/E/I/O 是现代命题类型标签，**不是原文项字母**。

- A(X,Y)：X ⊆ Y
- E(X,Y)：X ∩ Y = ∅
- I(X,Y)：X ∩ Y ≠ ∅
- O(X,Y)：X ∖ Y ≠ ∅

前提顺序固定为：大前提 `major(M,P)`，小前提 `minor(S,M)`；正向结论固定为 `conclusion(S,P)`。如 AAA 表示 A(M,P)、A(S,M) 推出 A(S,P)。后缀 `reverse=True` 仅交换结论的主谓项，不交换前提；这一诊断不列入 I.4 的四条正向路线。

两种语义保留相同的 A/E/I/O 定义，仅改变允许的模型：

1. `empty-allowed`：项可为空，论域仍非空。
2. `all-nonempty`：另要求 P、M、S 三项全非空。

这是一项明确声明的语义比较，不把任何一种简单地断定为已解决全部亚里士多德存在预设争议。I.4 中不定命题按其在本章推理中与特称相同的作用讨论；程序不把所有自然语言不定句自动翻译成存在量化句，也不实现模态三段论。

## 规范模型与“最小”

每个对象只记录是否属于 P、M、S，共八种成员类型。按 PMS 顺序，类型为三位二进制数，P=4、M=2、S=1；类型 0 表示三项之外的对象，必须保留。

`Model((1, 6))` 表示一个 S-only 对象和一个同时属于 P、M 的对象。规范模型每种已占用类型取一个代表；非空支撑共 2⁸−1=255 个，三项全非空的支撑有 218 个。枚举先按支撑大小、再按类型元组字典序排列。因此返回的反模型在这一语义中具有最小论域基数，平局按字典序打破。

为什么不限于“小世界”的偶然结果：对任意非空论域，取所有实际出现的 PMS 成员类型作为新论域。每个 A/E/I/O 命题只取决于是否出现违反全称或满足特称的类型，故压缩前后真值相同；三项非空也被保留。反过来，每个非空类型支撑都是合法的集合模型。因此穷举这 255 个支撑覆盖全部相关语义情形。这是一般论证；测试中长度不超过 3 的重复类型压缩只是例证，不能替代它。此压缩不保留人数、二元关系、模态或其他未实现的语言结构。

## 已验证结果

允许空项时恰有四个有效正向形式：AAA、AII、EAE、EIO。

三项非空时恰有六个：AAA、AAI、AII、EAE、EAO、EIO。新增的 AAI、EAO 分别是 AAA、EAE 在存在条件下的弱化结论，**不是另外两条原章最强路线**。原章的四条最强路线仍是 AA→A、EA→E、AI→I、EI→O。

其余十二组前提对：AE、AO、EE、EO、IA、IE、II、IO、OA、OE、OI、OO。每组都能找到满足同一前提、S 非空、结论为 A(S,P) 的模型，以及满足同一前提、结论为 E(S,P) 的另一模型；程序输出全部见证。A 见证使 E 与 O 为假，E 见证使 A 与 I 为假，故四种正向结论均非必然。两见证不是同一模型中的矛盾断言。

重要方向检查：IE 能推出反向 O(P,S)，不能据此把 IE 计为本章的正向有效前提对。程序对反向结果另行输出。

## API

```python
from categorical import Model, models, analyze_form, all_forms, nonproductive_witnesses

model = Model((1, 6))
model.holds("I", "M", "P")           # True
model.holds("O", "P", "S")           # True
model.holds("I", "S", "P")           # False

result = analyze_form("A", "A", "I")
result.valid                         # False
result.countermodel.support          # (0,)
result = analyze_form("A", "A", "I", mode="all-nonempty")
result.valid                         # True
len(all_forms())                     # 64
len(models("all-nonempty"))           # 218
```

`Model` 只接受非空、严格递增、无重复的整数元组，值域为 0..7。布尔值、浮点数、整数子类不当作类型整数；错误类型抛出 TypeError，错误值抛出 ValueError。`Model.from_mask(mask)` 接受 1..255 的严格整数。命题必须是单个大写 A/E/I/O，项必须是 P/M/S，模式必须是上述完整字符串，`reverse` 必须是严格布尔值。验证不依赖会被 `-O` 删除的 assert。

`FormResult.countermodel` 为 None 表示有效，否则为最小反模型；`premise_model_count` 给出满足两前提的规范模型数。本次全部前提对均有模型，未以不可能前提掩盖有效性。

## 原文入口

- 希腊原文：<https://www.graeco-arabic-studies.org/view/arist.analytpriora-orig-gr1>，I.4
- Owen 英译：<https://en.wikisource.org/wiki/Organon_(Owen)/Prior_Analytics/Book_1>，Chap. IV

来源用于解释原章，代码与有限模型是本次教学重构。译文中的现代编辑标题、脚注、后世名称应与亚里士多德原文区分。
