# 《前分析篇》II.8：独立数学与代码审查

## 结论与范围

**通过当前绑定版本的数学与代码审查。** 检查正文逐步证明、12题答案、16格矩阵、复现README与代码实际行为；不把软件检查作为古代文本的唯一解释。来源审查另列，本文不冒充重新完成其版本校勘。

### 一般证明核验

1. 二值推理 `(p且q)推出r` 下，保留p并给出非r可反驳q；两条分别成立的条件论证不能合并成两条前提同时已假。正文有清楚区分。
2. U/O、E/I是真正否定；本章反对替换U/E在空主项可同真，I/O即使主项非空也可同真。正文保留历史术语边界，没有偷换成现代互斥定义。
3. 全称原式的4个反对转换格，其反驳皆需C非空。其中保留大前提的2格能无条件得到E(B,C)，但还不足以反驳U(B,C)；另2格的特称结果本身就需见证。正文和程序都分别检查“结果成立”与“目标被排除”。
4. 8个矛盾转换格在允许空项的现代语义中成立；特称材料自行提供需要的见证。4个特称反对格失败的两点模型所有项非空，不能借非空假设修复。
5. 反例中C外B对象阻断全称加强，独立特称见证不能拼接；答案与论证一致。255模型的覆盖根据是三位类型支持压缩，正文明确另给一般论证；不扩展到基数、关系或模态语言。

## 独立实现和真实运行

[独立量词核验器](../../reproduction/aristotle-prior-analytics-ii8/independent_check.py)不导入作者`model.py`：用布尔三元组的组合生成模型，逐对象`all`/`any`定义命题，独立列出四原式、替换和16格结果，再对已保存报告核查假设、目标、结果、模型数、全部计数、有限候选语言后果及反模型重放。与作者用集合外延运算的实现不同，但共享明确声明的数学语义；独立实现不保证绝无共同概念错误，所以仍逐步审查一般证明。

- 允许空项255个模型；C非空240个；三项非空218个。
- 共48行（三政策×16格），所有假设均可满足，所有计数、声明和保存反模型匹配。
- 3份作者JSON逐字一致。独立核验器normal、`-O`、`-OO`真实执行通过；作者10项测试由审查方在三模式分别重跑通过。
- 三项非空时，4个特称反对格各有16个保留原目标前提的反模型；“无结果”只限被移除大前提的有序A/B项对上U/E/I/O，不等于没有任何逻辑后果。
- 模型输入拒绝空论域、越界类型、bool及非frozenset；命题严格三元tuple，生成器先物化并验证全部输入，避免短路隐藏尾部非法语句。生产校验为显式异常，优化不会删除。

真实证据：[独立normal](../../reproduction/aristotle-prior-analytics-ii8/logs/independent-normal.json)、[独立-O](../../reproduction/aristotle-prior-analytics-ii8/logs/independent-O.json)、[独立-OO](../../reproduction/aristotle-prior-analytics-ii8/logs/independent-OO.json)、[复跑normal](../../reproduction/aristotle-prior-analytics-ii8/logs/reviewer-test-normal.txt)、[复跑-O](../../reproduction/aristotle-prior-analytics-ii8/logs/reviewer-test-O.txt)、[复跑-OO](../../reproduction/aristotle-prior-analytics-ii8/logs/reviewer-test-OO.txt)、[执行命令](../../reproduction/aristotle-prior-analytics-ii8/logs/reviewer-commands.txt)。测试是本地实跑，不是声称GitHub CI通过。

## 绑定版本（SHA-256）

以下哈希绑定已审查正文、作者源码、测试、独立核验器和作者normal结果；任何后续内容变动需重新核验相应部分。

|文件|SHA-256|
|---|---|
|`papers/ancient/aristotle-prior-analytics-ii8.zh-CN.md`|`a223186dbbf38acbea1be638f68035d019891e790b6666bd214bb058573c71d2`|
|`reproduction/aristotle-prior-analytics-ii8/model.py`|`8977a040d0ab2361cdd7447307922ccd00c9b36c00e23adf176f2f98a1ca23e9`|
|`reproduction/aristotle-prior-analytics-ii8/test_model.py`|`e33ac6f53f968fe039be09eb9c5754722ef93d90e05cddd2696ad5314829e828`|
|`reproduction/aristotle-prior-analytics-ii8/independent_check.py`|`d7fc5e8ea26aec138ea80aa41c932aa1ed03bf29a87d3c73096709e95c1d1095`|
|`reproduction/aristotle-prior-analytics-ii8/logs/run-normal.json`|`dc6adaa13573c138badd1d3c30c05db11b110bac13b326aa54cc4582f982b840`|
|`reproduction/aristotle-prior-analytics-ii8/README.md`|`2e662d338958cff9b2e7df96bf8ee206627b924c2d2bdaa1bbbe92c0f00df5fd`|
