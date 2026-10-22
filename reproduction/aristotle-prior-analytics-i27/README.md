# I.27：有方向的前提库与可检查证书

这是《前分析篇》I.27 的**原创教学重构**，不是亚里士多德的算法转录，也不是古代词项逻辑的完整复现。只用 Python 标准库。原文定位：Owen 1853，印刷 pp.144–146（扫描 PDF pp.163–165）；方向性收集与全称限制在 p.145，沿属种关系避免重复收集及普遍谓词警告在 p.146。原文书目与解释见[配套深读](../../papers/ancient/aristotle-prior-analytics-i27.zh-CN.md)。

## 模型与输入承诺

类名对应集合；没有非空性预设。输入 `(a,b)`：

- `inclusions`：已作为前提提供的全称包含，$a\subseteq b$。
- `exclusions`：已作为前提提供的互斥，$a\cap b=\varnothing$。

输入并不会自动变成现实真理：程序不核查历史、经验或科学事实。`model_holds` 只能核查一个显式有限解释是否满足输入。某个学生是人之类的**个体观测不能作为全称包含的证据**；本接口根本不接收个体观测。不要把若干样本全为正当作“每个”。

`catalog(x)` 返回：

- `sup`：可由已给规则推出的上位项（包含自身）。
- `sub`：可推出的下位项（包含自身）。
- `excl`：可推出与它互斥的项。

方向不能交换。两类同在一个普遍上位项之下，不推出二者相含或相斥。目录没有删除共同上位项；这恰好保留了“收集到某谓词”与“它提供了可用中项”之间的区别，程序不声称自动发明所有三段论。

## 恰好实现的规则

1. 包含自反和传递：有原始边路径 $a=x_0\subseteq x_1\subseteq\cdots\subseteq x_n=b$ 时给出包含证书。长度零的路径表示自反，不是假装来自原文前提。
2. 互斥对称：$u\cap v=\varnothing$ 可交换两端。
3. 沿子类向下传播互斥：$a\subseteq u$、$b\subseteq v$、$u\cap v=\varnothing$ 推出 $a\cap b=\varnothing$。

一般有效性的教学理由不是实验数字：若任取 $z\in a$，沿每条包含边逐步得到 $z\in b$，所以包含传递；若某 $z\in a\cap b$，两条路径给出 $z\in u\cap v$，与原始互斥前提冲突，故没有这种元素。

**不实现**：包含反向、由缺失生成否定、从子类属性反推上位类属性、存在推理、概率/“通常”推理、必然模态、本质/属性/偶性的知识论分类、完整三段论搜索。尤其原文末段“通常”的材料并不混作全称规则。

允许空类；`exclusions=[('a','a')]` 使 a 必须为空，但不使知识库自动爆炸。按照集合语义，空 a 确实包含于任何类；本程序仍只沿原始包含边求包含，**不会补出这一切语义后果**。故称“指定规则的闭包”，不能称完整集合语义后果引擎。`None` 表示该规则系统未找到证书，不表示命题为假；也不表示命题在所有模型中不成立。

## 接口与证据

```python
from model import KnowledgeBase
k = KnowledgeBase(
    ('human', 'animal', 'stone', 'student'),
    (('human', 'animal'), ('student', 'human')),
    (('animal', 'stone'),),
)
p = k.inclusion('student', 'animal')
print(p.path)  # ('student', 'human', 'animal')
print(k.verify('student', 'animal', p))  # True
q = k.exclusion('student', 'stone')
print(q.source_pair)  # ('animal', 'stone')
```

这些英文类名只是一个**假设性教学前提库**；不构成分类学或经验断言。`inclusions`/`exclusions` 保留输入事实边，推导结果用 `Inclusion(path)` 或 `Exclusion(left_path,right_path,source_pair)` 分开表示。证书可由 `verify` 对原始边逐项检查；它不调用搜索算法来确认自身。直接前提是单边路径，传递是多边路径；互斥证书同时记录输入边原方向与两条路径，允许交换使用该输入边。枚举顺序固定，包含使用最短 BFS 路径；这不是最短整体互斥证明优化器。

参数要求：非空且不重名的 stripped 字符串类名；容器为 list/tuple；边恰好两端且属于类名集合；重复边去重；支持环（共同外延）和自边。非法构造、查询或解释抛 `ValueError`，未知类名不是知识库中“未知的关系”。`verify` 对格式错误/伪造的证书返回 `False`，但错误查询类名仍抛 `ValueError`。`model_holds` 要求恰好为每个类名给出 set/frozenset；元素是普通可散列 Python 对象，按 Python 集合相等性解释。所有校验不依赖会被优化删除的 `assert`。

## 实跑与复查命令

在本目录运行：

```bash
python -m unittest -v test_model
python experiment.py
python -O -m unittest -v test_model
python -O experiment.py
python -OO -m unittest -v test_model
python -OO experiment.py
# 按上述三个模式重跑并保存真实合并 stdout/stderr、命令、退出码及环境：
python run_evidence.py
```

`logs/environment.json` 记录实际 Python 版本、平台、UTC 时间；三个日志对应普通、`-O`、`-OO`。每个模式均为 **20 个单测通过、两个进程 exit 0**。实验结果一致：

| 检查量 | 每种运行模式的数量 |
|---|---:|
| 有限代表解释 | 255 |
| 前提选择实例 | 1,020 |
| 包含证书 | 3,848 |
| 互斥证书 | 1,326 |
| 总证书 | 5,174 |

有限解释的构造：三个类的每个元素有 3 个隶属位，共 8 种类型；遍历这些类型的每个非空子集，形成 255 个代表宇宙，保留零隶属类型。类的外延仍可为空。相同隶属类型的重复对象不枚举；空宇宙不枚举（各类都空的真值情况在只含零隶属类型的宇宙已有代表）。对每个解释，先列出其中成立的所有有向包含和互斥关系，再取完整列表与按索引模 3 分出的三个列表，得到四个**确定前提选择**。它们不保证彼此不同，1,020 是检查实例数而非不同知识库数；这**不是全部子前提库穷举**。所有返回证书既查原始边，也用该显式解释的集合关系独立检查。

20 单测包括包含传递、否定对称/双侧向下传播、缺失不作否定、共同上位项不推出包含、循环终止、空类不爆炸、伪造路径/互斥证书拒绝、非法输入、有限解释及去重。有限实跑能发现实现错误，不能证明一般数学定理、不能代替对规则的一般证明，也不支持古代作者实际使用此数据结构的历史判断。

## 文件

- `model.py`：有方向的规则搜索与原始边证书检查。
- `test_model.py`：20 个单元测试。
- `experiment.py`：有限集合 oracle 与可读演示输出。
- `run_evidence.py`：重新生成环境与三模式日志。
- `logs/`：真实运行记录。
- `AUTHOR_SHA256.txt`：作者交付文件摘要（不包含摘要文件自身；独立审查另行提供）。
