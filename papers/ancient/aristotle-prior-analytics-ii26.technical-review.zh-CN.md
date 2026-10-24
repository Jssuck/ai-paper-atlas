# II.26 独立数学与代码审查

## 结论与范围

**通过本单元的技术审查。** 审查者未撰写主稿或生产实现；独立阅读全文、六条形式路线、反模型和16题答案，另用逐对象布尔成员表示复算生产位掩码实现。结论只覆盖明确的集合语义、检查过的文件与真实运行范围，不替原文版本校勘、科学分类事实或无限域定理提供实验认证。

[主稿](aristotle-prior-analytics-ii26.zh-CN.md)完整范围69a37–70a2；[复现说明](../../reproduction/aristotle-prior-analytics-ii26/README.md)和[独立运行附件](../../reproduction/aristotle-prior-analytics-ii26/audit/README.md)列可重跑命令。

## 数学核对

1. 全称负路线由B包含于C、C与A无交推出B与A无交；全称正路线由包含传递推出B包含于A。这两项蕴涵均允许空B，但要用结论排除另一全称目标，确实需要B非空。正文把“结论有效”与“确实反驳”分开，没有把存在前提错误放到包含传递本身。
2. 两条特称路线从同一个非空C中选取成员，分别产生B中非A见证或B、A共同见证。正文空C反模型正确，且未拼接两个不同存在对象。
3. All/NotAll、None/Some互为精确否定；All/None在空B时同真，在混合B时同假。正文例8.1同时体现两个特称命题可同真，不能升级为全称反面。
4. 单点证书的双向论证正确：存在反例即可取单元素C，反向证书必给同一反例。正文明确这只是语义存在性，不提供无限域搜索算法或共同知识。
5. 第二格负路线由A包含于C及B与C无交推出B与A无交，确有效；B非空时可反全称肯定。省略A与C关系的反模型正确。第一格特称正、负两式的同一见证论证也正确。主稿不把原文两格分类伪装为一般逻辑不可能性定理，保留论辩直接性与章尾张力。
6. 原例以对象对作为论域成员的类型说明可用，但其分类真假仍是条件，未由代码证实。正文明确第三格证书是存在重构，Owen表格漏显量词不能升级结论。
7. 16题答案逐题核对通过：尤其题1前提假不推出结论假、题3反对不等于矛盾、题8存在条件位置、题9第二格边界、题15译注猜测以及题16有限实验范围均无推理跳步。

## 实现与真实运行

生产实现`validate()`明确排除负数、超界掩码、布尔值冒充整数与未知路线；掩码验证后`x & ~y == 0`精确表达包含。`accepted`仅表示所有前提为真，不等于结论碰巧真。`rejects_target`同时要求证书被接受及目标为假。对空主项的记录不被误算为程序失败。

审查者实际重跑16项`unittest`测试，normal、`-O`、`-OO`全部通过。检查不依靠会被优化删除的裸`assert`。独立oracle不复用生产谓词或生产枚举作为期望值；它按每个对象的三项布尔身份展开，计算完整证书的每个字段，再与生产结果比较。每模式4681个带标签世界、28086个完整证书比较，无差异。聚合计数也匹配：上位两路线及第二格负路线各341，其中220真正反驳、121空B不反驳；下位两路线各440；第一格特称正路线774。各路线结论失败数均0。

独立计数复核见audit说明：允许身份数给出341、121、440、774的几何和，避免把同一程序输出互相抄写当作独立依据。三模式解码后的oracle结果一致。日志来自实际执行，重跑耗时可以变化；有限枚举不穷尽任意域，不模拟“立即明了”或自然语言事实核查。第一格特称负在正文中证明，但不是已枚举的第七路线，主稿已明确标注。

## 修订与冻结规则

审查确认复现README将论域写成带范围条件的整数集合，因而n=0确为空域；正文oracle描述采用逐对象布尔成员，与实际实现一致。下列SHA256绑定所审版本。任一受审文件变更后应重核相关内容并更新绑定；本审查文件不自我绑定。

| 文件（仓库相对路径） | SHA256 |
|---|---|
| `papers/ancient/aristotle-prior-analytics-ii26.zh-CN.md` | `41602ac244425c7b9599b31857244edfa18ed7eb285b7d439dbae29ad56e3db7` |
| `reproduction/aristotle-prior-analytics-ii26/objections.py` | `bf80334afceb668c246bd18cd75bb9b36bd5f0f2171994e205e802af678851e5` |
| `reproduction/aristotle-prior-analytics-ii26/test_objections.py` | `9fbb204f7d37d8667e645f2dd23815352b6b0b9dfcfd33951d62abecabb1e244` |
| `reproduction/aristotle-prior-analytics-ii26/README.md` | `923b7e2dce041c5509de5eec7cad1ddaee81360be586211fd887420b5d5474ac` |
| `reproduction/aristotle-prior-analytics-ii26/run.sh` | `8f321e7137359ca8e4827e5155a2bb5fc6e9cc19ed97c8a2cb9932dfe3b4bb88` |
| `reproduction/aristotle-prior-analytics-ii26/audit/independent_oracle.py` | `07a381af45832bf365fd107317737eff947844e2556e56120cb41659bbac5a4f` |
| `reproduction/aristotle-prior-analytics-ii26/audit/run.sh` | `213be86e739929f5121d4474bb2a484b8f051fab5b5c5c1172eddb098ed98cf8` |
| `reproduction/aristotle-prior-analytics-ii26/audit/README.md` | `c60220222326c62015fe5a8bbc903d7fb5157de494ec4483ab4b0e291aabe79b` |
