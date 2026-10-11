# 从反复行动到意向与规范：现代教学附件

为孔狄亚克《逻辑》第一部第六章制作的原创、低成本、标准库Python装置。实际参照1798年《全集》第二十二卷印第54—57页。目录名1780仅为作品书目年，不认证初版本文字。

本附件不是历史算法复现、心理实验或伦理判断工具。递推、情境表、规范代码都是现代教学设定；不能证明作者的自然法或神学结论。

## 一分钟运行

需要Python 3.10或更新版本；实际环境见[logs/environment.json](logs/environment.json)。无第三方依赖、无网络、无账户、无模型调用、无GPU。

在本目录执行：

```sh
python3 -B demo.py
python3 -B verify.py
```

第二条会实际运行普通、-O、-OO三种模式，保存完整日志。所有检查均不依赖可被优化移除的裸assert；三个模式都受支持。也可分别运行：

```sh
python3 -B -m unittest discover -s tests -v
python3 -B finite_oracle.py
python3 -B mutation_check.py
python3 -B -OO verify.py
```

verify.py从任何工作目录启动都可定位自己的代码和logs/；演示和测试命令按本目录执行。验证会更新本附件的logs/，变异只写本目录的临时副本并自动清理，不改生产代码。

## 读什么、运行什么

- [MODEL.zh-CN.md](MODEL.zh-CN.md)：全部记号、假设、一般证明、历史对应及界限。
- [WALKTHROUGH.zh-CN.md](WALKTHROUGH.zh-CN.md)：分数手算、三层相连的示例、迁移反例、检查过程及练习答案。
- [habit_model.py](habit_model.py)：精确习惯递推、闭式、单个动作的执行标记。
- [action_model.py](action_model.py)：情境动作表、相容意向、行为等价类、显式规范约束。
- [demo.py](demo.py)：一组虚构场景的完整JSON结果。
- [tests/test_model.py](tests/test_model.py)：27个测试方法；非法输入检查含多个子例。
- [finite_oracle.py](finite_oracle.py)：独立算法构造预期值的有界枚举器，由本附件作者编写，不冒充外部独立审计。
- [mutation_check.py](mutation_check.py)：10个有效语义变异，在-OO模式运行全部单元测试。
- [verify.py](verify.py)：一键检查、实际环境、命令、退出码、用时、源文件SHA-256和优化模式一致性。
- [logs/verification.json](logs/verification.json)：真实执行结果的最终汇总。
- [演示输出](logs/demo-normal.json) · [单元测试日志](logs/unit-tests-normal.txt) · [有限oracle结果](logs/finite-oracle-normal.json)：可直接打开的证据。

没有Notebook；本示例无需交互组件，不声称Jupyter验证。

## 三个必须分开的结论

1. 重复使规定的$`h`$上升、停用使其下降，顺序也影响结果。$`h`$不是“道德良好度”。
2. 同一动作可以符合多个意向；更多情境有时能区分，表格错误时唯一候选也可能错。
3. 给定规范可以计算合规性；只给描述性的行动记录，本模型没有偷偷获得一套唯一规范。原文需要—能力—自然—上帝的论证仍须阅读和评价。

精确示例：$`\alpha=1/2`$、$`h_0=0`$、输入 $`(1,1,1,0,0)`$ 的状态为 $`(0,1/2,3/4,7/8,7/16,7/32)`$。输入 $`(1,0)`$ 与 $`(0,1)`$ 末值分别为$`1/4`$与$`1/2`$。三个候选意向从一个情境中的三者不可区分，经过第二、第三情境后逐步区分。3个动作在无规范约束时有8套代码；一个必须纳入、一个必须排除时剩2套；再指定第三个动作时剩1套。

## API摘要

```text
habit_trace(alpha, initial, inputs) -> tuple[Fraction, ...]
habit_closed_form(alpha, initial, inputs) -> Fraction
action_inputs(actions, tracked_action) -> tuple[int, ...]
Policy(contexts, intentions, actions, rows)
compatible_intentions(policy, observations) -> tuple[str, ...]
behavioral_classes(policy, contexts) -> tuple[tuple[str, ...], ...]
admissible_norms(universe, required=(), forbidden=()) -> tuple[frozenset, ...]
normative_status(action, universe, candidate_norms) -> str
```

`Policy`行对应意向、列对应情境。`normative_status`返回`all_permit`、`all_forbid`、`underdetermined`或`inconsistent`。最后一种专门处理空代码族，避免空真歧义。参数、空集及错误输入约定见 [MODEL](MODEL.zh-CN.md)。

## 验证边界和诚实计数

每种模式实际跑27个单元测试。有限枚举覆盖6,375条习惯历史及44,825个前缀值；64张动作表的576次候选查询、256个分区和576个细化对；64个规范桥梁对及192次判断。计数所指对象不同，不应相加成“总实验数”；重复前缀和三种优化模式也不是独立样本。

10个变异必须语法合法、跑满27个测试、产生检查失败且没有测试错误，才记为KILLED。初轮发现闭式权重反转变异逃过单元测试；补入非回文输入的闭式检查后再次验证。初轮FAIL保存在[logs/mutations-initial.json](logs/mutations-initial.json)及[mutation-details-initial.txt](logs/mutation-details-initial.txt)；当前结果在[logs/mutations.json](logs/mutations.json)。故意破坏版本的错误回溯是预期检出证据，不能当成最终生产代码失败。

`verify.py` 返回0且最终 [verification.json](logs/verification.json) 为PASS，仅表示所列检查通过。`source_sha256`记录本附件作者文件；独立审查若另行添加文件，不在这份作者清单中冒充作者验证对象。有限oracle的整数多项式与位掩码路线不同于生产实现，但仍由同一作者编写；真正独立代码审查需另列来源。

默认检查在本次环境约数秒完成，精确用时以日志为准。源文件和回溯中的工作目录规范为相对路径，Python版本、UTC执行时间和真实退出码保留。有限集合枚举为指数成本，默认边界很小；本程序不是大规模行为识别或规范推理服务。
