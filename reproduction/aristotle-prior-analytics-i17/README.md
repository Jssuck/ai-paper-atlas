# I.17 最小教学复现：双偶然第二格与否定的两个分支

这是自写的有限模型工具，检验正文明确指定的 **现代实际主项语义**，不声称亚里士多德使用可能世界、位掩码或本程序。没有训练集、模型拟合、经验基线或性能指标；本章是理论论证，适合小型反模型与证明义务核查。原书的“无三段论”有历史语境，本代码只检测指定类别的端项结论，不把它扩张为逻辑上毫无可推信息。

## 环境与命令

只用 Python 3 标准库。确切解释器版本见 [environment.json](environment.json)。从本目录运行：

```bash
python -m unittest -v > results/tests-normal.log 2>&1
python -O -m unittest -v > results/tests-O.log 2>&1
python -OO -m unittest -v > results/tests-OO.log 2>&1
python demo.py > results/demo.json
python -O demo.py > results/demo-O.json
python -OO demo.py > results/demo-OO.json
cmp results/demo.json results/demo-O.json
cmp results/demo.json results/demo-OO.json
```

三种模式的 24 项测试都实际执行；三份演示 JSON 字节一致。`unittest` 的断言方法及 `require` 的显式异常不会被 `-O` 删除。没有声称运行 Jupyter 内核；本附件不是 Notebook，也不是完整古代模态逻辑判定器。

## 数据与算子

`Model(n, worlds, actual=0)`：论域为 `0..n-1`；`worlds` 为非空元组，每行依次是 A/B/C 的非负整型位掩码。位 `1 << x` 表示对象 x 属于该项。所有列出的世界对实际世界均可达，实际世界也在其中。对象身份固定，项外延可变化。模型不可变；非法大小、掩码、项名、世界下标、对象下标、形式、模态均显式抛错。

`categorical(P,S,form,modality)` 先选定实际世界中的 S 对象，再逐对象量化世界：

- `form`: A=全称肯定，E=全称否定，I=特称肯定，O=特称否定。
- `actual`：在实际世界满足对应正／负谓词。
- `necessary`：同一对象在所有世界满足对应正／负谓词。
- `possible`：同一对象在至少一个世界满足对应正／负谓词，即弱可能。
- `contingent`：同一对象有正例世界且有反例世界，即双向偶然。

最后全称用 `all`，特称用 `any`。因此双向偶然 A/E 同值、I/O 同值，但不等于实然 A/E 同值。空主项时全称为真、特称为假；主要第二格反模型均取 B/C 非空，不靠空项制造失败。`jointly_possible` 单独检验全体实际 S 对象在 **同一个世界** 满足某质，不能和逐对象弱可能混用。

`noncontingency_witnesses(P,S)` 列出实际 S 中所有必然 P 与必然非 P 的对象。全称偶然失败当且仅当这两张列表至少一张非空；不是必须正分支，也不是必须负分支。两种见证还可能分别来自不同对象。

## 七个命名算例

见 [model.py](model.py) 的 `examples()`，完整掩码保存在 [演示结果](results/demo.json)。

|名称|作用|
|---|---|
|`disjoint`|两个世界 A 从全部对象变为空；B 始终为{0}，C 始终为{1}。两个偶然前提成立，端项必然排斥|
|`identical`|A 同样切换；B、C 始终同为{0}。相同偶然前提成立，端项必然包含|
|`conversion_failure`|A 为{0,1}／{1}，B 始终{0}；A 对全部 B 偶然，但 B 对实际 A 不偶然，交换主谓失败|
|`necessary_positive`|非偶然只由必然肯定造成，排除“非偶然必是否定”的误推|
|`necessary_negative`|非偶然只由必然否定造成，排除“非偶然必是肯定”的误推|
|`mixed_fixed`|对象0必然肯定、对象1必然否定，两个分支同时存在但见证不同|
|`alternating_witnesses`|A 在{0}与{1}之间变化，B={0,1}；每个对象双向偶然，却没有一个世界全 B 都 A 或全 B 都非 A|

## 有界实跑覆盖

`endpoint_checks()` 检查 16 种偶然前提形式对，每对都在 `disjoint` 和 `identical` 为真。每对又逐项检验 4 种模态 × 4 种 A/E/I/O 端项结论，保存至少一个反模型名称，共 256 个候选蕴涵的有名反例证据。两个模型均使所有双向偶然端项结论为假；肯定的实然／必然／弱可能结论在排斥模型失败，否定的在同一模型失败。它们不反驳诸如某个析取式或含中项的新公式。

`exhaustive_checks()` 遍历论域大小1与2、两个世界、全部 A/B/C 掩码及两个实际世界选择，共 8,320 个带实际点配置。每个配置检查九个有序项对，共 74,880 项对；检查偶然改质等值、非偶然分支分解，以及必要⇒实际、实际⇒弱可能、偶然⇒弱可能等有限性质。准确计数在 JSON 的 `exhaustive` 字段。重复世界和空项被保留以检验边界；这不是只枚举主要反例。

[测试](test_model.py)另覆盖同一对象、量词次序、空项、单世界、实际点变化、非法输入、模型不可变性及优化模式。以上枚举不是一般定理的证明，更不证明某个现代语义是古代文本唯一解释。一般证明、原文层次、历史反例和译义风险见[正文](../../papers/ancient/aristotle-prior-analytics-i17.zh-CN.md)。

## 独立审查与证据

- [原典与译注独立审查](../../papers/ancient/aristotle-prior-analytics-i17.source-review.zh-CN.md)
- [完整论证与数学独立审查](argument-review/README.md)
- [实现、独立集合预言器及变异检查](CODE_REVIEW.md)

三路审查针对不同义务；它们的有限枚举不是古代语义唯一性的认证。审查记录绑定相应最终文件摘要，远端提交与页面显示另作发布验证。
