# I.8：必然前提与跨世界见证的最小教学实验

这是一份原创、仅用 Python 标准库的现代教学重构。它不是亚里士多德模态系统的唯一解释，不实现全部《前分析篇》，也不把有限枚举当一般证明。完整解释见[中文深读](../../papers/ancient/aristotle-prior-analytics-i8.zh-CN.md)。

## 语义合同

- 个体域固定且非空，世界列表固定且非空；同一个体在不同世界保有身份，但 P、S、M 的外延可以变化。
- A(S,P) 表示 S 包含于 P，E 表示交集为空，I 表示交集非空，O 表示 S 中存在不属于 P 的对象。A、E 在 S 为空时为真。
- NA、NE、NI、NO 表示每个列出的世界中相应 AEIO 命题都真。本实验不定义世界可达关系、嵌套模态或可能性运算。
- RI、RO 要求同一个体在所有世界都满足相应的肯定或否定特称关系。RI/RO 蕴含 NI/NO，反过来一般不成立。
- `require_middle=True` 明确要求每个世界中的 M 都非空；并不要求存在同一个体在所有世界都属于 M。这是一项独立的现代存在条件，不是程序从全称前提暗中获得的事实。

所有世界有序，允许重复世界，故4096是有序赋值表数量，不是模态结构的同构类数量。二对象域的每个世界有三个二位集合掩码，共64种赋值；两个世界共64×64=4096。掩码0为空集，1是{0}，2是{1}，3是{0,1}；每世界的列顺序始终是 P、S、M。

## 文件与复跑

- [modal_models.py](modal_models.py)：模型验证、AEIO、必然量化、固定见证、14式及Baroco/Bocardo逐世界见证算法。
- [test_modal_models.py](test_modal_models.py)：27项测试方法，含非法输入、空项、模式穷举和见证边界。
- [results.json](results.json)：完整枚举结果和机器可读例子。
- [WALKTHROUGH.zh-CN.md](WALKTHROUGH.zh-CN.md)：手算走查与一般论证范围。
- [logs/commands.txt](logs/commands.txt)、[logs/environment.json](logs/environment.json)：实际命令和环境。
- [普通模式日志](logs/tests-normal.txt)、[-O日志](logs/tests-O.txt)、[-OO日志](logs/tests-OO.txt)。三份JSON输出逐字一致，另两份见[O](logs/results-O.json)、[OO](logs/results-OO.json)。

在本目录运行：

```sh
python -m unittest -v test_modal_models
python -O -m unittest -v test_modal_models
python -OO -m unittest -v test_modal_models
python modal_models.py > results.json
```

无安装命令，无第三方依赖，无Notebook或Jupyter执行声明。模型关键检查采用显式异常和unittest，不依赖会被优化模式删除的`assert`。

## 本次真实结果

三模式各27测试方法通过，输出逐字一致。每模式枚举4096个模型，对14个模式分别检查，合计57,344个模式—模型对；每对比较自由空项政策与逐世界中项非空政策。这里不是把三次重复当作三倍不同语义覆盖。

| 模式 | 自由政策：前提真模型数 | 自由政策：失败数 | M逐世界非空：前提真模型数 | 限定政策失败数 |
|---|---:|---:|---:|---:|
| Barbara |256|0|144|0|
| Celarent |256|0|144|0|
| Darii |121|0|121|0|
| Ferio |121|0|121|0|
| Cesare |256|0|144|0|
| Camestres |256|0|144|0|
| Festino |121|0|121|0|
| Baroco |121|0|64|0|
| Darapti |625|369|81|0|
| Disamis |121|0|121|0|
| Datisi |121|0|121|0|
| Felapton |625|369|81|0|
| Bocardo |121|0|121|0|
| Ferison |121|0|121|0|

两个存在依赖式Darapti、Felapton在自由政策下失败，其余十二式无失败。要求所有世界M非空使14式都成立，但对十二式一般是多加的条件，不声称这是最弱统一条件。

另有NI真而RI无见证的模型288个、NO真而RO无见证的模型288个，RI/RO蕴含NI/NO的失败数均为0。Baroco和Bocardo前提成立模型合计242个，逐世界见证检查484次；其中固定特称前提有见证的模型142个，检查其原见证仍属于固定结论见证集。

## 不可外推的部分

1. 逐世界有效性的提升有一般逐世界证明；本枚举只是软件核验，不证明任意个体数、世界数的定理。
2. 当前语义中的混合必要/当前前提反例不能用来宣布I.9错误。I.9涉及不同的历史解释问题，恰好提示不能把本章教学合同当整套古代模态语义。
3. 必然特称的每世界见证可不同；程序返回逐世界列表，不把它伪称固定的古代exposition对象。
4. 有限测试不能保证程序没有全部缺陷；独立审计另存，不混同作者测试。
5. 只公开原创代码、解释与实际日志，不发布原书扫描或全文翻译；不关闭其他章节、版本和历史目录缺口。
