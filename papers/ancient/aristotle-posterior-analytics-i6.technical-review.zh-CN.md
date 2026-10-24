# 《后分析篇》I.6：独立数学与代码核验

结论：在正文明确规定的有限情形、固定对象域、整句全称语义范围内，核验通过。不是对古代唯一模态语义、现实必要因果或完整科学知识的认证。

## 最终稿绑定

- [正文](aristotle-posterior-analytics-i6.zh-CN.md) SHA256：`f7bf41197464e7813d170051a400b25572b4de6656c47945555874e7b6e9991d`。
- [代码与真实日志](../../reproduction/aristotle-posterior-analytics-i6/README.md)。生产源码、运行结果、独立测试及日志的逐文件SHA256见[清单](../../reproduction/aristotle-posterior-analytics-i6/SHA256SUMS)。
- 独立核验读取正文、模型、生产测试、运行脚本、结果和复现说明，未改动生产代码。本文所用N的参数顺序是主项在前，代码necessary_ab等字段则按传统项名字母命名，已核对映射而非按字母猜方向。

## 数学检查

| 检查项 | 判定 |
| --- | --- |
| C到B到A，逐同一情形、同一对象的传递证明 | 正确；证明不依赖有限枚举大小 |
| N推出实际情形T | 正确，实际情形已明确属于W |
| 结论不必要仅排除两前提共同必要 | 正确，未加强为每条都不必要 |
| 第5节非空反例：C=B={c}，A从{c}变{d} | 正确；小前提必要，结论及大前提非必要 |
| 第6节两情形所有项非空，A=C不变、B改变 | 正确；必要结论但给定两桥非必要 |
| 单对象B消失的辅助例 | 正确；小前提失效，大前提空泛真，不混淆整条路线 |
| 必要结论具有该性质，不等于当前普通前提证明了其必要性 | 正文明确，未误引必要化规则 |
| 真值一致不能判定本质/原因 | 正文与代码均明确未编码该层 |
| “无遗忘而失去知识” | 明确作为带认识论前提的重构，非程序证明心理事实 |
| 两否定对照 | 限定三项该项位、全部非空，且不冒充本章原文主张 |
| 练习答案与主文、代码一致性 | 12题逐项检查，未发现必须修正项 |

## 独立实际运行

独立审查者另写[Boolean成员表检查程序](../../reproduction/aristotle-posterior-analytics-i6/audit/independent_check.py)，从12位成员事实生成2情形×2对象×3项，不调用生产`object_oracle`，也不把生产枚举结果作为预期结果来源。用逐成员蕴涵重算7个判定字段，比较生产实现的全部4096输入。

每种模式均真实运行：

- `python [优化选项] -m unittest -v test_model`：21项生产测试通过。
- `python [优化选项] audit/independent_check.py`：6项独立测试通过。
- 优化选项依次为空、`-O`、`-OO`，测试使用unittest失败机制，非会被优化删除的裸assert。

独立重算得到：4096模型，其中729全项非空；256必要双前提、1024当前真双前提；必要结论且当前双前提真、给定路线非必要320例，其中56例全项非空。所有必要双前提模型的结论必要、所有当前真双前提模型的当前结论真，无反例。独立Boolean表示与生产mask表示零差异。

附加三对象双否定检查从9位成员事实遍历512组三集合，保留30组全项非空模型；A/E/I/O结论分别真18/6/24/12、假12/24/6/18，四种结论均有正反例。另查空情形、非法域大小、bool或越界mask、单对象消失中项、重复情形，以及因果状态未建模字段。

[normal独立日志](../../reproduction/aristotle-posterior-analytics-i6/audit/check-normal.log) · [-O独立日志](../../reproduction/aristotle-posterior-analytics-i6/audit/check-O.log) · [-OO独立日志](../../reproduction/aristotle-posterior-analytics-i6/audit/check-OO.log)

[normal生产重跑](../../reproduction/aristotle-posterior-analytics-i6/audit/replay-normal.log) · [-O生产重跑](../../reproduction/aristotle-posterior-analytics-i6/audit/replay-O.log) · [-OO生产重跑](../../reproduction/aristotle-posterior-analytics-i6/audit/replay-OO.log)

## 仍然不证明什么

两套实现和三种优化模式只能核查明定模型与实现。它们不能证明W穷尽真实可能情况，不能验证本质或因果，不能替代逐情形一般证明，也不等于古代论证全部复现。正文关于时代、原文与译注的结论另由来源审查负责；GitHub公式实际显示与远端完整性另做发布验收。
