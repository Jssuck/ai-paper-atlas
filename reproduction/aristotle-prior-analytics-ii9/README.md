# II.9：第二格结论替换的最小教学核验

对应[中文深读](../../papers/ancient/aristotle-prior-analytics-ii9.zh-CN.md)。本目录是原创的现代集合语义教学程序，不是古代算法的恢复，不是对原书或全部逻辑系统的完整复现。

## 范围和输入

实读依据是《前分析篇》II.9，以及1853年Owen印201章IX至202章X之前和[Jenkinson英译电子转录第9章](https://en.wikisource.org/wiki/The_Works_of_Aristotle/Prior_Analytics/Book_II)。原书扫描不随代码发布。版本及注释问题见正文来源台账。

`Prop(kind, predicate, subject)`中后两项先谓项、后主项。`A(P,S)`表示S包含于P，`E(P,S)`表示S与P不交，`I(P,S)`表示交集非空，`O(P,S)`表示S中至少有一个非P对象。全称命题不暗含主项存在。程序的A/B/C字母是项名，与命题种类A必须区分。

原四式为：

|式名（后世助记名）|大前提AB|小前提AC|结论BC|
|---|---|---|---|
|Camestres|A(A,B)|E(A,C)|E(B,C)|
|Cesare|E(A,B)|A(A,C)|E(B,C)|
|Festino|E(A,B)|I(A,C)|O(B,C)|
|Baroco|A(A,B)|O(A,C)|O(B,C)|

`contrary`按本章承接II.8的用法，将E结论换A、O结论换I；后者不是互斥关系。`contradictory`将E换I、O换A。每次只保留一原前提：`retain_major`保留AB、检查AC，`retain_minor`保留AC、检查AB。不要把被检查的原前提偷偷保留在背景里。

## 模型与判准

三谓词给出000至111八种成员类型；非空论域用其已占类型的非空子集表示，共255种。`model(mask)`用1至255的八位占用码构造每种类型的一个代表；000对象允许不属于任一项。`C_nonempty`留下240种，`all_nonempty`留下218种。这里是明示的现代语义参数，不裁定古代唯一存在理论。

同一类型的多个对象对本程序四类命题没有区别，所以去重不会改变这些命题的真值；这解释本有限检查的覆盖范围。含对象计数、二元关系、模态或时间的扩展不由此覆盖。**有限实跑不是一般定理的证明，正文仍需独立的任意对象/见证推导。**

每格报告两种不同判准：

- `result_countermodel_count`：背景成立、表定新结论不成立的模型数；`null`表示没有指定该结论，不是零。
- `refutation_countermodel_count`：背景成立、原目标仍成立的模型数；零才表示在该政策下真正反驳目标。
- `background_count`：背景可满足模型数，防止把空背景上的空洞蕴涵冒充有效反驳。
- `all_valid_target_pair_forms`只列目标的有向项对上必然成立的A/E/I/O式；空列表不等于没有任何逻辑后果。
- 首个反模型有类型表和三个项集合，可直接重放；它是枚举顺序首例，不声称唯一或最小。

## 真实结果

[results.json](results.json)保存48格（三政策各16格）与四个原式的检查。四原式在三政策均无保真反例；8个矛盾替换方向也都反驳目标且背景可满足。结果不是由只检查原式后推测出来，而是逐个替换背景重新计算。

|格的类别|允许空项|C非空|三项全非空|
|---|---|---|---|
|全称两式×反对替换×两个保留方向（4格）|每格7个未反驳目标的模型|每格0|每格0|
|特称两式×反对替换×两个保留方向（4格）|每格16个未反驳目标的模型|每格16|每格16|
|四式×矛盾替换×两个方向（8格）|每格0|每格0|每格0|

全称反对替换保留AB时，新全称A/E结论本身即使C空仍成立，但并不因此排除原来的E/A；保留AC时，新特称I/O结论自身便需要C存在。两种失败不能混写。特称反对替换保留AB时，可推出O或I，却与原I或O兼容；保留AC时，目标项对四式无一必然成立。三项全非空也不能补救这四格失败。

## 运行与环境

Python标准库即可；本次CPython 3.12.14，Linux x86_64，零第三方依赖。完整版本与核心文件SHA-256见[环境和输出一致性日志](logs/environment-and-reproduction.log)。从本目录运行：

```sh
python3 check.py > local-results.json
python3 -m unittest -v test_check.py
python3 -O -m unittest -v test_check.py
python3 -OO -m unittest -v test_check.py
sh run.sh rerun
```

`run.sh`不覆盖已检查日志，会在指定输出目录保存新证据，并将三模式结果相互及与已存results.json逐字比较。源码：[check.py](check.py)、[test_check.py](test_check.py)、[run.sh](run.sh)。

本次真实实跑10项测试，每项分别在[普通模式](logs/tests-normal.log)、[-O模式](logs/tests-O.log)、[-OO模式](logs/tests-OO.log)通过，退出码均0。三个模式生成的结果逐字一致。测试使用unittest检查，而不是会在优化模式被移除的裸assert。测试覆盖输入拒绝、模型数、A/O及E/I互补、原式保真、全部矛盾替换、全称空C边界、特称反对失败、I/O同真和反模型重放。

没有机器学习数据集、训练、随机种子、经验基线或精度指标；研究对象是明示逻辑语义。程序不识别自然语言、不从扫描自动抽取论证、不认证现实前提、不证明古代文本无误。
