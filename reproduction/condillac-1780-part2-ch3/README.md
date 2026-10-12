# 孔狄亚克《逻辑学》II.III：可运行教学重构

实际底本：1798年《Œuvres de Condillac》卷XXII，*La Logique* 第二部第三章，印页118–124／IA PDF126–132。目录路径沿用作品初版书目年1780，不把实际读取版本写错。[正文精读](../../papers/1780/condillac-logic-part2-ch3.zh-CN.md)另述历史解释与来源。

这是新写的有限数学教学程序，不是历史算法复原，也不是心理学验证。四个小模型依次说明：经验过滤与可识别性；正Horn闭包与错误种子；语义对齐与可逆重命名；任务相对精确性与标签数量。

## 文件与阅读顺序

1. [MODEL.zh-CN.md](MODEL.zh-CN.md)：全部符号、输入条件、一般证明及反例边界
2. [WALKTHROUGH.zh-CN.md](WALKTHROUGH.zh-CN.md)：中文逐步手算导览
3. [logs/results.json](logs/results.json)：固定示例的实际输出
4. `model.py`、`demo.py`：核心实现与固定示例
5. `test_model.py`、`mutation_check.py`、`run_all.py`：作者测试、突变检查与一键证据生成

可执行词表限定为同一意义集上的双射编码，是正文一般字典存在定理的严格子情形；一般非单射定理没有声称经机器验证。附件固定例表true001/twin000/other111与正文A000/B001/C101不同，噪声输出请以附件本身的例表为准。

全部依赖为Python标准库。无安装、下载、网络调用、模型API或notebook。建议CPython 3.10及以上；**本次实际验证仅为CPython 3.12.14 / Linux**，精确解释器与平台见运行摘要，不声称测试过其他版本。

## 直接运行

从本目录执行：

```sh
python -B demo.py
python -B -m unittest -v test_model
python -O -B -m unittest -v test_model
python -OO -B -m unittest -v test_model
python -B mutation_check.py --mode normal
python -O -B mutation_check.py --mode O
python -OO -B mutation_check.py --mode OO
python -B run_all.py
```

最后一条完整重跑上述工作，覆盖本目录三个作者日志文件。`-B`避免新增字节码缓存；输入验证用显式异常，测试用unittest，未使用优化时会消失的裸assert；`run_all.py`会对五个Python源文件做AST检查。所有命令应在此目录运行，避免误导入别处同名模块。

常用API：

- `HypothesisSpace(points, rows).candidates(observations, max_errors=0)`返回预算内的候选名称冻结集合
- `HypothesisSpace.distinguishes(observed_points)`检查这些位置是否区分全类候选
- `HornSystem(atoms, rules).close(seeds)`返回种子、首次推导来源和最小闭包
- `HornSystem.verify_trace(result, seeds)`核查完整来源及固定点，不保证种子事实为真
- `Vocabulary(entries)`定义意义与词码间双射；`aligned_dictionary`构造正确对齐；`translation_preserves`检查意义保持
- `inverse_dictionary`只求到实际像集的逆；`rename_rule`和`translate_atoms`用于显式重命名
- `task_exact(worlds, labels, task_values)`判断标签能否确定当前任务答案

## 已验证的范围

正常、`-O`、`-OO`下各24个unittest方法通过。有限枚举包括：

- 8张三位置二值预测表的全部255个非空候选类；长度0–2的43种观察序列；预算0、1、2，共32,895个过滤案例，另检查可识别性与真候选保留
- 三原子的24种规则（每种前提子集乘三个结论）；取0–2条的301个系统，乘8种种子，共2,408个闭包案例，对照全部闭合集之交，并检查幂等、顺序无关、种子单调及有条件保真
- 两词表的6×6种编码排列，乘6张双射字典，共216种组合；各检查8种种子的往返与结构闭包交换
- 三世界的27种标签函数乘27种任务函数，共729对；另检查精细化保持精确性
- 噪声、类外真相、同预测候选、伪造来源、空前提、无种子循环、未知输入、不可逆字典、错误可逆字典和非单射闭包反例

每模式还运行10个人工行为突变、10个对应原版哨兵基线、11个故障分类控制。实测每模式`killed=10, survived=0, harness_failure=0`（仅指行为突变），基线全通过，十一个故障控制全被列为`harness_failure`。**每个突变只跑指定的一个哨兵测试，不是每个突变都跑全套24项测试。**手选突变通过也不意味着抓住任意bug。

突变框架的适用范围仅为源码中列出的十个不伪造报告的行为替换，不是恶意程序隔离或输出身份认证。同一子进程里的恶意代码若自行打印结构完全合法的假终止报告，仍可能误导分类；这些检查不能推广成对任意恶意程序的认证。

在上述范围内，分类要求测试完整执行；仅断言失败算行为检出。语法/导入失败、提前退出、超时、测试运行异常、非法JSON及缺字段/非对象/bool计数/负计数/不相容计数报告都不算检出。测试和这些证明都由附件作者制作；它们不是独立审计，若另有独立审计，应单独阅读其说明。

## 实测证据

- [verification.log](logs/verification.log)：所有阶段命令、stdout、stderr、退出码；突变记录包含每次子进程的实际输出。仅替换当前解释器路径为`${PYTHON_EXECUTABLE}`、临时目录前缀为`${MUTATION_DIR}`，子进程内联运行器在命令展示中标为`${SENTINEL_RUNNER}`，其完整代码在`mutation_check.py`
- [verification-summary.json](logs/verification-summary.json)：环境、执行起止时间、源码SHA-256、阶段状态、突变分类摘要
- [results.json](logs/results.json)：demo固定输出，便于独立阅读

一键实测通常在一分钟内完成，取决于解释器启动和系统负载；不使用GPU。日志只保留一份完整流水和一个紧凑摘要，避免为每个模式复制一套材料。

## 如何读成功与失败

候选数3→2→2→1说明新观察可能不增加区分力。误录第一项会唯一留下错误候选；预算1能保留真候选但仍不唯一。闭包{rain,wet,slip}再次计算不变，完整来源也通过检查，但错误种子仍可能让整个链条为假。错误双射字典能精确往返，还能在规则同样错译时保持形式闭包交换，却不保持意义。三个标签也可能比两个更混淆当前任务。

有限程序展示这些区分，不评判真实语言社群，不验证孔狄亚克关于语言历史、思想发生或人类认知的普遍断言。
