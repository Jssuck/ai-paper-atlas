# 可手算的运行走读

先运行 `python3 demo.py`，或阅读已运行的 `logs/demo.json`。JSON 中 `true/false` 是布尔值；分数字符串 `"3/5"` 表示精确的 3/5，不是近似小数。下面每一步都使用人为规定的模型。

## 1. 同一个效果，四种不同问题

`example_model()` 创建四个世界：

- none：观测 0，没有所指原因
- A：观测 1，一个原因 A，属性 red
- B：观测 1，一个原因 B，属性 blue
- A+B：观测 1，两个原因共同出现，属性 red

执行 `model.candidates((1,))` 得到 `(A, B, A+B)`。

现在依次计算：

1. `cause_exists` 的候选答案为 `{True}`，所以 `identified`。
2. `number_of_causes` 的候选答案为 `{1,2}`，所以 `ambiguous`。不能断言只有一个原因。
3. `cause_identity` 的候选答案为 `{A,B,A+B}`，所以 `ambiguous`。
4. `attribute` 的候选答案为 `{red,blue}`，所以 `ambiguous`。

注意：这里只判定这四个允许世界中哪些与观察一致。第一项答案之所以一致，是因为我们在设定模型时排除了“没有所指原因却观察到 1”的世界。

## 2. 一个名称不会替你挑中世界

`with_labels` 把每个假设的显示标签都改成 `force`。实际候选集仍是 `(A,B,A+B)`，原观测签名没有改动，`labels_preserve_fibers` 为 `true`。

再增加 `effect_word=effect+100`，观察 1 的三个世界都增加字段 101。新记录 `(1,101)` 仍有三个候选，`derived_word_preserves_fibers` 为 `true`。

即使用三个不同的名字称呼 A、B、A+B，也只能描述区别，不能据此观测出真实世界是哪一个。单元测试特意检查这种情况。

## 3. 新探针确实有信息，但仍未必什么都知道

另行规定一项新探针：none→0，A→7，B→8，A+B→7。这张表就是新增实验的预测模型，不能从“探针”二字凭空得到。

实际得到两个观测 `(1,7)`：

1. 保留旧观测 1，相容者为 A、B、A+B。
2. 新值 7 排除 B，剩 A、A+B。
3. 剩余两者的属性都是 red，因此属性现在 `identified`。
4. 原因数目仍可能为 1 或 2，因此数目仍 `ambiguous`，身份也仍不唯一。

对应输出：`new_probe_candidates=["A","A+B"]`；`new_probe_attribute.values=["red"]`；`new_probe_number.status="ambiguous"`。

## 4. 强前提也能让答案唯一，但并未增加观测

调用 `model.restrict(("B",))`，意为暂且只容许 B。仍然只观察 `(1,)`，现在身份只能是 B。因此 `assume_B_identity.status="identified"`，同时 `assumption_preserves_columns=true`。

这说明的是“如果只可能是 B，那么答案是 B”。它不显示我们已经找到支持排除 A 和 A+B 的新实验。

反向操作：往原模型加入 spontaneous，规定它没有所指原因但同样给出 `(1,)`。原来的原因存在问题现在同时容许 `True` 和 `False`，`wider_model_existence.status="ambiguous"`。这明确展示识别结论如何依赖模型边界。

## 5. 数据不在模型里时，不报成功

原模型只预测 0 或 1。询问 `(2,)` 时相容集合为空，`out_of_model_observation.status="inconsistent"`。

“所有零个候选都同意”不是有根据的识别。应检查观测、扩充模型或修改前提；本例不会任选一个答案，也不会自动静默修正数据。

## 6. 从测量求比例

现在换成另一个明确独立的现代例子：`y=gku`。规定 k=3、g=2，输入 1、2、3，于是输出依次为：

- 2×3×1=6
- 2×3×2=12
- 2×3×3=18

除以各自非零输入：6/1=12/2=18/3=6。因此 `infer_product` 输出 `identified`、`product="6"`。已知 g=2 时，`calibrated_coefficient` 返回 k=6/2=3。

这里求出的参数必须连同响应式及校准前提理解，不是从实际历史文本里读出的一条物理定律。

## 7. 未校准时，有无穷多个等价参数世界

`equivalent_parameters(3,2,c)` 分别取 c=1/2、1、2，给出 `(k,g)`：

- (3/2,4)
- (3,2)
- (6,1)

每一对乘积都是 6，因此每次输入的输出都一样，`all_pairs_match=true`。其一般理由是 `(g/c)(ck)u=gku`；并非只验了三对就宣称全部成立。继续用同一响应规律尝试输入 4、100 或任意有理数，都不能区分这些参数世界。

## 8. 零输入、冲突数据与相对系数

- 输入 `(0,0)`、输出 `(0,0)`：任何正乘积都相容，结果 `uninformative`。
- 输入 `(1,2)`、输出 `(6,13)`：6/1≠13/2，结果 `inconsistent`。精确无噪声模型不容许把 13 当成约等于 12。
- 第二个系统 k_B=5，使用相同增益 g=2，得到响应乘积 10。两个系统的乘积比为 6/10=3/5，正好等于 k_A/k_B。
- 若第二个增益改为 3，乘积比成为 6/15=2/5，便不等于系数比 3/5。共同增益是额外前提，不能漏写。

## 9. 亲自验证与审慎解读

运行 `python3 verify.py` 后：

- `logs/unit-tests.txt`：应显示 23 个测试、`OK`
- `logs/finite-oracle.json`：三类数量为 4,681、23,405、4,681，结果 `PASS`
- `logs/mutations.json`：九项均为 `KILLED`，基线 `PASS`
- `logs/mutation-details.txt`：每个故意破坏的副本具体失败在哪条断言；这些预期失败不表示原程序失败
- `logs/environment.json` 与 `logs/verification.json`：本次真实版本、时间、命令、退出码、用时与文件校验和

如修改代码或文档，应重新运行总验证，避免让旧日志看起来像覆盖了新版本。有限测试、一般证明与历史原文核验分属三个层次，不能互相冒充。
