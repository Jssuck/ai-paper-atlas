# 《后分析篇》I.1：独立数学与代码核验

核验对象为[正文](aristotle-posterior-analytics-i1.zh-CN.md)与[教学复现](../../reproduction/aristotle-posterior-analytics-i1/README.md)。本报告独立于正文和生产代码编写；历史原文与版次由[来源审查](aristotle-posterior-analytics-i1.source-audit.zh-CN.md)另行核验。

## 1. 数学与语义检查

| 检查项 | 结论与范围 |
| --- | --- |
| 全称实例化 | 从任意域上的所有T都是A与真T(d)，可得A(d)；常元指称与对象存在前提已明示。 |
| 缺小前提的反例 | 单对象T假、A假使全称真而A(d)假，正确反驳仅凭全称推出该个体结论。 |
| 全称对子域的蕴涵 | P包含于Q蕴涵P与R交集包含于Q；证明对任意域成立。 |
| 反方向失败 | 两对象P={a,u}、R=Q={a}使子域判断真而全称假；已识别子域非空，反例有效。 |
| 反模型的对象类型 | 明确抽象P/Q反例不是反驳欧氏几何或偶数定理；没有偷换数学题材。 |
| 空对象与空类 | 正文假定固定非空域，允许P空；代码亦接受空域。独立空域诊断仅验证集合接口，不扩张古代论断。 |
| 不同认识方式 | 未把同一意义下知道且不知道同时成立；知识账本与外部真值不混同。 |
| 不默认逻辑全知 | 只有显式derive执行才改变账本derived_q；接受规则不会自动填所有对象结论。 |
| 记录与可靠性 | 词义字段只是登记；识别/规则接受可以出错，不自动被命名为知识。 |
| 无记录与否定 | 程序拒绝缺支持，不把缺少P识别当成外部非P。 |
| 个体身份 | 使用稳定对象ID，不依显示名合并对象；推理前后使用同一ID。 |
| 识别与应用时序 | 程序步骤展示依赖，不声称古代心理过程存在可测时间间隔。 |
| 一般命题与有限实跑 | 任意域保真由逐步证明承担，三对象枚举不被称作一般证明。 |
| 练习答案 | 推导、反模型、范围差别、偶然真结果与知识方式各题答案与模型一致。 |

## 2. 实现、证书与计数检查

- model.py的derive只有账本与对象ID输入，不读取World；返回新不可变账本，保留先前derived_q且加入当前对象。
- applicable同时检查两谓词词义登记、规则接受、对象登记及P识别，缺任一项拒绝应用。接口条件并不冒充本章所有学习的必要条件。
- syntactic_check核对证书固定规则/前后件字段及当前账本支持。它是**支持关系检查，不是执行历史的认证**；未执行derive但手动构造相同字段的Certificate也可通过。附件不是防伪凭证或历史追踪系统。
- semantic_check在形式支持之外要求全称规则真、目标确实存在且属于P、结论Q真。最后一项在前述真前提下逻辑冗余，但保留作显式诊断无害。
- 错误识别可以产出形式合格结果，真值审计拒绝；假规则配合碰巧为真结论也被拒绝。这些属于对论证根据的审查，不等价于判定结论为假。
- World强制P、Q外延位于域内；账本可含不存在ID，以测试错误存在登记，不因其可存储就承认对象真实。
- exhaustive.py的生产判断采用集合运算；oracle采用逐对象位/布尔条件，不调用被检验判断来产生预期结果。二者共享枚举驱动但运算独立；这不是形式证明工具。
- 64世界×8识别×8登记×2规则×4词义=32768状态；每状态3对象=98304查询。
- 3072形式应用、432真值支持应用、1536假输出、127限制域/全称差异均独立复跑一致。3072减去432与1536余1104次为前提支持审计未过但Q碰巧真，不可误报为可靠知识。
- 生产16项测试每模式通过，枚举oracle不一致数为0；unittest断言与显式异常在-O/-OO下仍执行，未依赖优化时删除的assert语句。
- 输出为确定性枚举，不是统计置信度、神经网络基准或人类心理实验。环境与日志未含个人路径、密钥或账户信息。

## 3. 独立新增测试与真实复跑

[独立测试源码](../../reproduction/aristotle-posterior-analytics-i1/audit/test_independent.py)不修改生产实现。六项覆盖：

1. 使用显式逐对象三布尔真值行，检查域大小0–4共4681种P/Q/R解释，逐一比较全称、子域及正向蕴涵。
2. 在两个真值不同的World上使用同一账本，验证derive不依赖World，同时保留既有结果且不改原账本。
3. P识别假、全称空泛真、Q碰巧真时，形式支持通过但真值审计仍拒绝。
4. 两对象共享显示名时，证书不能把一者识别转移给另一者。
5. 明示证书检查只核当前支持而非执行历史；撤销规则接受后原证书不再有当前支持。
6. 独立枚举五个操作门槛的32种组合，只有全部满足时可应用。

独立测试在normal、-O、-OO各实跑6项通过；随后对生产16项测试及完整枚举在相同三模式分别重新执行。日志：

- 独立测试：[normal](../../reproduction/aristotle-posterior-analytics-i1/audit/tests-normal.log)、[-O](../../reproduction/aristotle-posterior-analytics-i1/audit/tests-O.log)、[-OO](../../reproduction/aristotle-posterior-analytics-i1/audit/tests-OO.log)。
- 生产复跑：[normal](../../reproduction/aristotle-posterior-analytics-i1/audit/production-rerun-normal.log)、[-O](../../reproduction/aristotle-posterior-analytics-i1/audit/production-rerun-O.log)、[-OO](../../reproduction/aristotle-posterior-analytics-i1/audit/production-rerun-OO.log)。
- [审查环境](../../reproduction/aristotle-posterior-analytics-i1/audit/environment.json)。

在复现目录可重放：

```sh
python3 -m unittest -v audit/test_independent.py
python3 -O -m unittest -v audit/test_independent.py
python3 -OO -m unittest -v audit/test_independent.py
```

## 4. 冻结版本

最终复核通过，绑定下列SHA-256。任何后续正文、证明或代码改变均需重新核验。有限实跑只支持本报告列明的范围，不认证古代唯一解释，也不代表已证明所有输入上的程序正确性。

| 文件 | SHA-256 |
| --- | --- |
| papers/ancient/aristotle-posterior-analytics-i1.zh-CN.md | `55be161bbdd78320287452904e6ae3f06b94f85ec1703561db12bd4fcf504837` |
| reproduction/aristotle-posterior-analytics-i1/README.md | `10d265ffb482bc518013d94662136cd97dce6c4cee3a6e0cd382a1756135bce8` |
| reproduction/aristotle-posterior-analytics-i1/model.py | `687556b0388fbb8c63d3cbf71905cddbfd1f3113170da4454fd2b140d76c5d97` |
| reproduction/aristotle-posterior-analytics-i1/test_model.py | `a141bead90414e3067fa49b75bf049ba3ceda3383a549855dbcf9e1a06eb8fa2` |
| reproduction/aristotle-posterior-analytics-i1/exhaustive.py | `f20a6eaa0e934096ae9343c69cd007f79d424195aa5929ca2ef6fe5c4ce2eafe` |
| reproduction/aristotle-posterior-analytics-i1/results.json | `4f9c8c5b71233276420b482390646c2786f106719c866dd74ea08274faecd0c7` |
| reproduction/aristotle-posterior-analytics-i1/environment.json | `8a7e6eeb012f1fe61cbcd7a92d2b895fd06527666508be0cfca4e68799e63216` |
| reproduction/aristotle-posterior-analytics-i1/audit/test_independent.py | `ac9bc38937a86ac47e64d22c756f2b8d312e56cce845975aa708caad365888bb` |
