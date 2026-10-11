# Condillac《逻辑》I.IX：习惯与记忆的低成本重构

这是原创的 Python 标准库教学模型，配合《La Logique》第一部第九章“感觉能力与记忆的原因”阅读。依据扫描本为 1798 年版，印刷页 72–94，PDF 第 80–102 页。1780 仅为已核一版书目年；未独立认证最早版次、1780 年版页码或文字。它并非本次扫描本的出版年。

核心区分：当前发生的观念事件可以清除，学会的反应倾向仍然存在；提示能触发一串重现，但共享提示、重复状态、容量淘汰和未练习后的衰减都可能让重现失败。模型还显式区分外部输入、内部回放和自身动作引起的感觉反馈。

它是思想实验，不是历史代码复原，不是现代脑科学或心理学模型的实证验证。

## 直接运行

需要 Python 3.10 或更新版本；只使用标准库。记录的实测版本见 environment.json；未声称跨版本全部验证。无需 pip、网络、API 密钥、GPU 或数据下载。

```bash
python3 -B run_all.py  # 一次生成全部证据与环境记录
python3 demo.py
python3 -m unittest -v test_model
python3 -O -m unittest -v test_model
python3 -OO -m unittest -v test_model
python3 mutation_check.py
```

mutation_check.py 会在本目录临时创建并清理隔离副本，写入 logs/mutation。它不会修改 model.py 或测试文件。更改实现以后，旧日志不再证明新代码通过，须重新运行。

## 先看什么

1. [WALKTHROUGH.zh-CN.md](WALKTHROUGH.zh-CN.md)：从 do、mi、sol 开始逐步练习，含反例及已回答习题。
2. [MODEL.zh-CN.md](MODEL.zh-CN.md)：所有符号、状态与假设；准确恢复的充要条件、信息丢失不可能性、上下文修复的边界。
3. [model.py](model.py)：稀疏计数表、序列回放、当前激活与双向身体接口。
4. [test_model.py](test_model.py)：40 项 unittest 方法；其中两项分别穷举 363 条单序列与 392 次双序列目标查询。
5. [mutation_check.py](mutation_check.py)：15 个定点行为突变，在正常、-O、-OO 三种模式下运行；将行为检出与测试框架/导入错误分开。
6. [logs/demo.json](logs/demo.json)、[logs/tests-normal.log](logs/tests-normal.log)、[logs/tests-O.log](logs/tests-O.log)、[logs/tests-OO.log](logs/tests-OO.log)：实际运行输出。
7. [logs/mutation-summary.json](logs/mutation-summary.json)：突变检查概要；完整结果和每次原始输出在 logs/mutation。
8. [environment.json](environment.json)：实际 Python、系统信息、运行时间与代码摘要。

## 四个必须保留的边界

- 强度是现代设定的整数计数。衰减、边数上限和淘汰规则不是 Condillac 的数学理论，也不是经验遗忘规律。
- 回放采用固定上下文的一阶后继规则。练习 A、B、A、C 后依然不能精确复现；不能把“经常练习”误当成普遍恢复保证。
- 上下文标签由实验者给出。给两首曲目不同标签可以解除跨曲目冲突，但不能自动解决曲目内部的重复状态。
- 来源标签由执行路径提供。保留标签便于检查；它并未解决真实的人类来源归因问题。

## 原典核对

开发时完整阅读了所提供本地扫描 PDF 第 80–102 页的文字抽取，并渲染核对印刷页 83、93 的扫描图像。OCR 有旧拼写和识别错误，不能当作可靠逐字转录。发布包不含原书扫描或整章转录，也不依赖这些材料运行；原典版本与页码仅用于追溯解释依据。

## 如何解释验证数字

40 是测试方法数；363 和 392 是两项测试内的确定性枚举用例数，不能相加后声称有 795 个独立测试方法。突变检查的 15 个案例是人工选择的语义错误，三模式合计 45 次行为突变运行；这既不是穷尽所有错误，也不是泛化正确性的证明。正常通过、行为杀死、基础设施失败和故意触发的控制错误分别统计。

所有数字以当前 logs 中的实际结果为准，完整日志保留，不凭预期生成通过证明。

## 独立复核与复现

另有两组独立检查，不导入作者测试来充当独立参考：

- independent_check.py：每模式检查 729 种双状态权重表、8,748 次参考回放、21,870 次充要条件与 10,000 次容量/遗忘完整状态，并检查历史碰撞及来源边界。结果在 logs/independent-checks.json。
- independent-review/test_independent.py：每模式 8 个测试方法，内含 15,309 次回放、86,022 次充要条件、16,384 条容量/遗忘操作历史及其 65,536 个前缀、1,092 条离线经历、2,916 个最少练习的状态/目标组合及 10,196 次判定、1,080 个有限容量练习案例。详细计数在对应 logs/tests-*.log 中以 INDEPENDENT_RESULT 开头的结果行。
- independent-review/audit_harness.py：每模式实际运行 9 个子进程控制案例和 11 个分类器案例，包括真实超时、导入/语法错误、空套件、运行时异常、提前退出与重复完成标记。这些控制必须按类别识别，不能被算成语义检出。

run_all.py 包含这些检查的正常、-O 和 -OO 三模式执行。独立脚本也可单独运行；所有检查仍只需标准库。两组检查有重叠，数字不应相加后称为彼此独立的样本。有限测试不代替 MODEL 中的证明，也不验证关于人的经验命题。

environment.json 会记录每个实际命令的退出码与全部发布源文件的 SHA-256 摘要。运行后先检查 logs/run-all-summary.json 中 success；如果你没有把 run_all.py 的输出重定向到此文件，它会显示在终端，可自行保存。历史记录不会自动覆盖为新运行的终端输出。
