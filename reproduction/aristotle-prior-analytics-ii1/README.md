# II.1：换位、子类与证明依赖的最小教学模型

这是原创的现代外延与证明树教学重构，不是古代程序、原作者唯一语义或完整三段论证明器。原文位置及版本差异见[深读正文](../../papers/ancient/aristotle-prior-analytics-ii1.zh-CN.md)和[来源台账](../../papers/ancient/aristotle-prior-analytics-ii1.sources.zh-CN.md)。本附件不扩展到II.2。

## 运行

Python 3，全部依赖为标准库，不需安装软件。在本目录运行：

```sh
python3 -m unittest -v test_model
python3 run_experiment.py
python3 -O -m unittest -v test_model
python3 -O run_experiment.py
python3 -OO -m unittest -v test_model
python3 -OO run_experiment.py
```

[环境](logs/environment.log)，[普通测试](logs/tests-normal.log)、[-O测试](logs/tests-O.log)、[-OO测试](logs/tests-OO.log)，[普通枚举](logs/experiment-normal.log)、[-O枚举](logs/experiment-O.log)、[-OO枚举](logs/experiment-OO.log)。运行检查使用显式异常与unittest，不依赖会被优化删除的assert语句。

## 声明的语义与API

`Statement(mood, subject, predicate)`总是**主项在前**：A(S,P)表示S包含于P；E表示交为空；I表示交非空；O表示S中有不在P的成员。Model的论域是range(n)，空论域也测试，所有项均可为空；这属于程序边界测试，不是断言Aristotle接受空论域。名称必须非空字符串，外延只接受论域内整数，bool不是对象编号。原文“P属于S”与这个参数顺序不能混淆。

`premise(label, mood, subject, predicate)`、`infer(rule, *parents)`构造有限规则树，`validate`重查规则、项对齐、结论与父节点。支持E/I换位，带I(S,S)显式存在叶的A转I，包含链、全称否定的子类限制，以及Cesare/Darii两个教学式。后世式名仅为标签。O换位和任意特称子类限制没有规则。

`Proof.dependencies()`返回这棵树实际使用的假设标签，不是全体可能证明的最小前提集，也不判定假设独立性或历史上的“通过同一三段论”。不同假设应由调用者采用不同标签；标签是展示元数据，而语法核验使用命题本身。

## 一般理由与反模型

1. E换位：S交P为空，集合交的交换律给出P交S为空。I换位使用同一个交集成员。这里不需额外存在假设。
2. A转I：由S包含于P和S非空，取x属于S，故x也属于P，即x在P交S。没有非空条件时，S为空便给反模型；程序把I(S,S)保留为单独假设。
3. 全称限制：若D包含于S，S包含于P，则任取D中成员均在P；若S与P不交，则D与P亦不交。不存在性不会破坏两个全称结论。
4. 特称不能任意下传：取S={0,1}、P={0}、D={1}。I(S,P)且非空D包含于S，但I(D,P)假。共同见证0不在D。这是结论子类的反例，不是否定一切附条件特称传递。
5. O不可一般换位：S={0,1}、P={0}，O(S,P)真，但O(P,S)假，两项都非空。程序另外记录允许空项下的最小反例。

这些是不限所枚举域大小的数学论证。有限枚举用来检验实现和展示反例，不替代一般证明。

## 依赖示例的读法

`examples()`保留原文第二格中的字母布局：p1为B与A不交，p2为C包含于A；原结论E(C,B)的树使用p1+p2。另加E类包含于A，则E(E,B)由该包含假设和p1换位直接导出，树中没有p2。这不是“E与B不交不成立”，而是它的展示路径不需要原来的第二前提。字母E类与E命题类型分属不同位置。

Darii示例使用B包含于A、I(C,B)得到I(C,A)；另加D包含于B，从B包含于A直接得到A(D,A)，不使用原有的存在见证前提。删去未用前提不会破坏这条树。对任意C的子类则不能照样保留原见证。

## 实跑覆盖与限制

18项测试在普通、-O、-OO三模式通过。每模式枚举n=0、1、2、3时S/P/D全部子集，共1+8+64+512=585模型：A带存在换位174例、E换位259例、I换位326例、A限制85例、E限制85例，均无失败；O换位反模型174个、非空子类丢见证反模型26个、缺存在条件A转I反模型85个。反模型计数取决于标号论域和枚举范围，不是历史“结论数量”。测试还在两对象、五项的1024模型中检查四个依赖示例的条件保真。

未实现全套证明搜索、自然语言解释、模态逻辑或最小依赖优化；不以有限模型或规则树裁定章末“同一三段论”的全部哲学解释。独立核验另存审查文件和真实日志，不把作者自测当独立审查。
