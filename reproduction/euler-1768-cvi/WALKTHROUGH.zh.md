# 从 CVI 原文到可运行模型：逐步导读

本文件以原版 131–133 页的四格十九式为输入，讲清 `syllogisms.py` 怎样检查它们。数学证明单独见 `MATHEMATICS.zh.md`，真实命令输出在 `logs/`。

## 1. 先固定项的角色，而不是套用熟悉的字母习惯

[原版扫描，PDF 第 150 页／印刷页 129](https://archive.org/download/lettresuneprinc01eulegoog/lettresuneprinc01eulegoog.pdf#page=150) 将 P 定为结论主项，Q 定为结论谓项，M 定为中项。

程序的 `FIGURES` 按大前提、小前提保存有序项对。第一格是 ((M,Q),(P,M))，第四格是 ((Q,M),(M,P))。四格的结论统一为 (P,Q)。`EULER_LIST` 则独立保存原文十九式及其顺序，单元测试对照源图核定。

例如第三格 AAI 的输入被展开成：A(M,Q)、A(M,P)、I(P,Q)。同样的字符 AAI 放到第四格，会变成 A(Q,M)、A(M,P)、I(P,Q)。它们所需存在条件不同，不能只按三个字符分类。

## 2. 把八种隶属型变成数据，不画一张「代表所有情况」的图

每个对象只有三个有关属性：是否属于 P、Q、M。八种原子为 000、001、010、011、100、101、110、111。位序严格为 P,Q,M；原子编号是 4P+2Q+M。

`Model.support` 是一个八位整数。若原子 i 被占用，整数的第 i 位为 1。

- support=1 表示只有原子 000：有一个论域对象，但三个类皆空。
- support=32 表示只有原子 101：一个对象属于 P、M，不属于 Q。
- support=20=4+16 表示原子 010 与 100 各有一对象：Q 和 P 不相交，M 为空。

不能把 support=0 当作「所有类空」：它是空论域，本项目拒绝该输入。相同原子里有多个对象并不改变 A/E/I/O 的真假，因此只需记录「是否占用」。一般完备性证明解释了为什么这也覆盖无限模型。

## 3. 在单个模型中计算命题真假

`Model.holds(mood, subject, predicate)` 用两个区域来判定：

- 交集区域：既属主项又属谓项；E 要求它空，I 要求它非空。
- 差集区域：属主项但不属谓项；A 要求它空，O 要求它非空。

这一步不读取 `EULER_LIST`，没有「名单中就判真」的分支。A/E 的定义也不会自动令主项存在。

如 support=32 对应 P=M={x1}, Q=∅：A(Q,M) 真，A(M,P) 真，但 I(P,Q) 假。因此它是第四格 AAI 的反模型，即使 P、M 都非空也无济于事。

## 4. 在所有模型中检查一个式

`MODELS` 生成 1 到 255 的支持，并按占用原子数排序；`models_with` 筛选存在假设；`premise_models` 留下两前提同时为真的模型；`check_form` 找出其中结论为假的模型。

运行：

```sh
python3 syllogisms.py query 3 AAI
```

本次真实输出（完整见 `results/query-3-AAI-unrestricted.json`）：

- 允许的支持 255 个；满足两前提 31 个。
- `valid=false`；反模型共 7 个。
- 最小反模型 support=1，论域={x1}，P=Q=M=∅。
- 最小附加存在条件为 [[M]]。

再运行：

```sh
python3 syllogisms.py query 3 AAI --exists M
```

加入 M 非空后，允许支持 240 个，前提模型 16 个，反模型 0 个，`valid=true`。可见存在条件是显式加进模型筛选的，不是隐藏在 A 的含义中。

反模型总会给出 `domain` 和 `classes`，可脱离位运算用普通集合手算。输出选对象数最少者，而非只挑某个容易找到的例子。

## 5. 自动搜索最小存在条件

`all_assumptions` 枚举 ∅、{P}、{Q}、{M}、{P,Q}、{P,M}、{Q,M}、{P,Q,M}。

`minimal_existence_assumptions` 按假设数量递增检查有效性。若已经找到一个充分条件，其真超集不再作为「最小」条件。该枚举不把「存在 Q」误认为「存在 M」：

```sh
python3 syllogisms.py query 4 AAI --exists P M
python3 syllogisms.py query 4 AAI --exists Q
```

第一条仍无效，返回上面的 support=32 反例；第二条有效。对于这个特定前提对，Q⊆M⊆P，所以 Q 非空已经带来 M、P 非空。

报告 `conditional_listed_forms` 另外给出四个条件式的反例，让缺少的那个类之外的两类都非空。这比三类皆空的反例更能说明最小条件的必要性。

## 6. 从任意查询扩展为全部 256 式

`all_forms` 用四格与三次 A/E/I/O 的笛卡尔积生成候选式，不使用原表缩小候选范围。`valid_forms` 按语义筛选；`nonweakened_valid_forms` 再比较同格、同有序前提的有效结论。

结论强弱只依统一存在背景来比较。三类皆非空时，A 严格蕴涵 I、E 严格蕴涵 O；因此会删去五个结论弱化式。代码中的 `strictly_implies` 不将两前提加入结论比较，避免把「前提已经蕴涵的两个结论」误判为彼此等价。

```sh
python3 syllogisms.py report --output results/report.json
```

结果摘要为：255 个非空支持；218 个三类皆非空支持；256 个候选式；可空类时 15 个有效；三类皆非空时 24 个有效；后者保留非弱化结论后 19 个，与原表一致。

`all_eight_existence_regimes` 保存全部八种背景的有效式清单。其中仅 Q、M 非空也恰得原表 19 式，这个不同背景的对应同样是现代分析结果。

## 7. JSON 如何用于复查

- `source_listing_in_original_order`：原始表序。程序通用枚举的顺序不等于历史表序，请用此字段重建原表。
- `all_256_forms`：每个候选式是否在原表、两种核心背景下的真假及反例、全部最小类存在条件。
- `all_eight_existence_regimes`：八种背景各自的支持数、有效式数及清单。
- `conditional_listed_forms`：四个依赖额外存在条件的原列式；含其他两类非空仍失败的反例，以及充分条件下的成功检查。
- `weakened_extras`：24 中可按明确规则剔除的五式。
- `four_term_equivocation`：现代新作的 bank 歧义例，显示两真实前提对应的是 M₁、M₂，不能套用固定三项的 AAA。

`countermodel=null` 仅表示该背景下没有反例。`premises_satisfiable` 是另外的字段：一般逻辑中不一致前提也会没有反例；本次所有前提对在三类皆非空时仍可满足，已单独核对。

## 8. 如何知道程序没有自己证明自己

1. 源表转录与语义穷举是两个独立输入路径。
2. 单元测试用集合包含、交集、差集运算交叉核对位运算；同时检查无效输入、空类、四格项序和反模型大小。
3. `tests/independent_audit.py` 从布尔三元组另建模型与类集合，不借用生产解码器作为真值基准，检查全部 2048 个组合。
4. 该独立审计另枚举小于返回反模型的带标号论域，确认不存在更小反例；这次最大最小反模型有 3 个对象。
5. 将原表临时置为空，15/24/19 的语义结果仍不变，排除硬编码原表产生计数的循环。
6. 数学说明先独立证明支持压缩完备性；测试与运行日志只是实现证据，不替代一般证明。

实际运行环境与时刻见 `results/environment.json`、`logs/run-all.txt`。完整复跑不需要原图或网络；对照文献时才需要打开所附影像或公开扫描。
