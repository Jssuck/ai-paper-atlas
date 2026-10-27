# Euclid I.24 独立技术审查

审查对象为[正文](euclid-elements-i24.zh-CN.md)与[最小复现](../../reproduction/euclid-elements-i24/README.md)。审查者独立于正文、复现作者；这是 AI 辅助技术审查，不宣称人类专家认证、形式证明或 Jupyter 内核验收。

## 证明与模型核验

- 先核对 I.23 复制夹角、I.4 得 BC=EG，再由 DF=DG 引入 I.5；未以 I.25 或余弦定理替代原证。
- 外型严格角链依赖点/射线内部关系；共线型按 E-F-G 的线段和；内型由 I.21 得 DF+FE<DG+GE 后消去。三型以内部射线与对边交点作穷尽分类，不把一张示意图当作全域证明。
- Simson 短边选取的补证需 I.16、I.18/I.5、I.19 以及交点存在；不能仅凭 DE≤DF 断言位置。
- 正半角参数产生开区间普通角；坐标平方展开得到精确差，分母正、两边正、t>s，严格正性成立。此现代代数分析与历史原证分开。
- 行列式分类依赖指定输入域与反射因子，不是任意点的通用内外判别。平方比较无需假设底边长度为有理数。

## 独立实际复跑

在独立副本运行 `python run_all.py`，成功退出；CPython 3.12.14，Linux x86_64，只用标准库，无安装或网络操作。

| 核验 | 实际结果 |
| --- | --- |
| 普通、`-O`、`-OO` | 每模式 33 个测试方法通过 |
| 有限正例与非法输入 | 每模式 300 正证书、21 非法输入；结果一致 |
| Notebook | 6 格顺序 compile/exec；新命名空间重放相同 |
| 原文对应具名三型 | a=2、6、8，b=2，s=1/2，t=1，数值及分类匹配 |

Notebook 没有通过 Jupyter kernel 执行；`execution_count` 为 null，另以元数据记录顺序。运行结果不能被称为一般几何定理的实验性证明。

## 独立攻击与不同计算路径

新增[审查脚本](../../reproduction/euclid-elements-i24/technical_probe.py)，可在复现目录执行 `python technical_probe.py`；结果见[真实输出](../../reproduction/euclid-elements-i24/technical-probe.json)。该脚本不在 `run_all.py` 的八条命令中，须单独运行。

- 9,750 个输入：独立求射线 DF 与 EG 的交点 H=kF，检查边内参数严格在 0 与 1 之间，再按 k 与 1 比较位置；得到 724 内型、8,994 外型、32 共线型，与生产分类一致。
- 对共线型另核 F 严格位于 E、G 之间；对所有输入用距离平方展开另算差值，未用生产代码的分类条件当作分类判定依据。
- 将一个基准证书的全部整数叶逐个替换为 bool 或 float，72 次攻击全部拒绝。
- 嵌套重复键、负无穷和 NaN 三个补充 JSON 攻击均在解析层被拒绝。

原测试另覆盖错误输入绑定、坐标/差值/配置篡改、缺失与额外字段、零边、相等或反向角、近零/近平角、反射、缩放和面积不单调。`verify` 按精确类型递归比较，避免 Python `True == 1` 接受伪证书；它使用同一核心计算器重算，不是独立逻辑内核。

审查中澄清了输入边界：`case()` 是面向已信任参数的 Fraction 便利构造器，会先做规范化；严格拒绝 bool/float 的契约属于原始 JSON 数据进入 `certify`/`verify` 的入口，不能把便利构造器误当成原始 JSON 验证器。没有据此改写数学结论。

## 局限与绑定

有限网格与攻击测试帮助发现实现错误，不覆盖任意实数、任意巨大恶意输入的资源消耗、全部欧氏公理或历史文本传承。本审查没有使用证明助理。来源归属与版本证据由独立来源审查另行负责；网页实际数学显示由发布验收另行核看。

核验日期：2026-10-27。完整正文、12 题答案和附件推导已复核；上述输入入口澄清后无未解决技术阻断项。以下 SHA-256 对应本次审查字节；若正文或代码改变，应重新核对并重绑。

| 文件 | SHA-256 |
| --- | --- |
| `euclid-elements-i24.zh-CN.md` | `71e6cf286556e0dc442c2261139fec31ee6c6942d2f5ebb4f3093fa98b9bd62d` |
| `cases.py` | `fb588ed162a0fa80ae149733566f5a4282e16b7242f7aeaa122531db29c6e982` |
| `create_notebook.py` | `c0dd2b6f06e7f86af2fc64d705fc283fade82d5a96ae446568a1c45291157df7` |
| `geometry.py` | `c96c8bd8a6dda949d7de2a036b268411cbef1e8d28b9dfb13d3b9339235ebf45` |
| `run_all.py` | `9460bd3e842bcc5942153a9561d44cec3d72d567ae2886339b5537fd9dc09e99` |
| `run_examples.py` | `a33fb3837fe451b498915a14878c63c6c25a34d254175e59f309e7917fa94f67` |
| `technical_probe.py` | `e0b962b12daf2c557e4b01817ca62b77ae40a8b34444e43705ecf5b308fe3a6e` |
| `test_geometry.py` | `f9851df1470a2bef1458cd1eba9e4368b63c2bb4a4d58e213395f2abd09a45de` |
| `verify_notebook.py` | `bd543eaa855fe994a28e9351f6bd0aaed0ac580e9b63acdfa65baca5860a3130` |
