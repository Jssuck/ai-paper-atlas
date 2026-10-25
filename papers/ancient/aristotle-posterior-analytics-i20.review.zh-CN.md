# 《后分析篇》I.20：独立数学与代码审查

审查日期：2026-10-25。结论：下列已绑定版本在声明范围内通过独立技术核验；不是古代认识论的完整形式化证明，也不代替远端内容与公式显示检查。

## 1 数学论证

- 可数无限严格全序的枢轴构造成立：保留的剩余集合嵌套且无限；后续枢轴均位于之前所保留的一侧；两种方向至少一种出现无限次，对应枢轴子序列严格单调。正文已明确这是现代经典存在证明，不是有限数据即可运行的无限性判定算法。
- 条件命题没有误写为已证明所有科学解释终止。原文上下两方向的描述与现代仅需导出至少一条无限单调子序列的论证分开。
- 取枢轴后三分无限中项集依赖全序条件。任意偏序可能还有不可比较部分，因此不能省略该条件。
- 有限全序区间的内部节点数等于最长严格链边数减1，上下界论证完整。菱形反例展示区间宽度与链深度的差别，不被冒充同一假设下反驳结论。
- 正文的0、1、2缓冲例与代码的−1、0、1例整体相差1；第n步及余隙计算一致。有限有理前缀没有冒称完成无限实验。
- 循环拒绝、有限词表、科学自然谓述、原因和本质的边界均有说明。练习答案与模型一致。

## 2 独立执行与不同算法核验

主测试在普通、`-O`、`-OO`三种Python模式下各13项通过。独立重跑四个普通Python Notebook单元，输出和Notebook字节与原交付一致；这不是Jupyter内核或浏览器渲染验证。保存的results.json与重新调用report()结果一致。

另编写[独立oracle](../../reproduction/aristotle-posterior-analytics-i20/independent_oracle.py)，用DFS求可达关系，再枚举内部节点的排列求最长链，不以主代码的Floyd–Warshall和记忆化递归作为预期答案。全部4096个4节点无自环带标签有向图中，543个无环图、3553个循环图；后者全部被主代码拒绝。无环图形成219种不同带标签严格序，对2484个区间的中项、是否全序和最长边数逐项比较，差异0。[独立运行结果](../../reproduction/aristotle-posterior-analytics-i20/independent_oracle_results.json)

从同一枚举单独筛选所有边由较小编号指向较大编号的子集，独立得到40闭包、223区间出现次数、221全序和2非全序，与正文和主结果一致。此处保留原始图重复，不能把223说成不同偏序数。独立oracle在普通、`-O`、`-OO`模式的结果也一致，检查用显式异常，不会被优化移除。

复核循环、非法端点、重复边、空图、任意拓扑编号、资源上限、布尔值冒充整数以及精确分数边界。主实现的最长链递归只在已排除环的有限区间上运行；每个内部节点均能到达上端，因此递归中的后继集合不会无故为空。128节点上限与256步分数上限是资源约束，不是原文结论。

## 3 限制

没有真实科学分类数据、训练集、准确率或因果判定。4节点穷举不能证明任意规模实现正确；测试覆盖有限，未做定理证明器认证或所有Python异常输入的穷尽分析。无限序结构结论依靠正文明确的数学证明，有限运行只检查实现、例子和计数。

## 4 最终版本绑定

SHA-256绑定以下正文、来源台账与全部复现文件；审查报告自身不递归纳入哈希。后续实质改动应重新审查，排版改动也应重新绑定。

| 文件 | SHA-256 |
|---|---|
| papers/ancient/aristotle-posterior-analytics-i20.zh-CN.md | `259a334df87f9935a1bb8765b03c5f2640513ba1d44badbd23c32f4e12448221` |
| papers/ancient/aristotle-posterior-analytics-i20.sources.zh-CN.md | `a3dbfc0359e9c45fe20eea17f076657a49465d0612603687492abdd896a63bab` |
| reproduction/aristotle-posterior-analytics-i20/README.md | `cd49bce9e222bfd75b7201da01cd4fd7f24fd3a64a1986f1eaee3b15e43eda4d` |
| reproduction/aristotle-posterior-analytics-i20/independent_oracle.py | `12813416fbebd22aa7e1ad47368de49e715bffef8bc9cf65458db42cca5de4fe` |
| reproduction/aristotle-posterior-analytics-i20/independent_oracle_results.json | `4ec4fd20511d21a1b964d008be395cd63a0eb39bed13fa61862b52ea38de6f3e` |
| reproduction/aristotle-posterior-analytics-i20/intervals.py | `2de83636f63fad66b1bc5fefaff9756dd25b938360c57796d17b21988ca3afc6` |
| reproduction/aristotle-posterior-analytics-i20/logs/commands.txt | `a199338134771480b16707dab787bfbe85f58dccef587b2a31a9c8b7e360d9f0` |
| reproduction/aristotle-posterior-analytics-i20/logs/environment.log | `e8f16925c99f7e36685d22aae3738781e70cec8860e4b21d7971fa2fac90134b` |
| reproduction/aristotle-posterior-analytics-i20/logs/notebook.log | `5829fb970fa6b9d5768a290f0576d62505deca29b4b332c2d7ad87c42c691b36` |
| reproduction/aristotle-posterior-analytics-i20/logs/tests-O.log | `429f080b5b2a4a58ffabf55e133f5f0c57c9692a639f63bb336aef736e9d9a72` |
| reproduction/aristotle-posterior-analytics-i20/logs/tests-OO.log | `5a56918615eae75c90a7c482e4e62a27e113f7d96aaedada9a5bf7b326dd2837` |
| reproduction/aristotle-posterior-analytics-i20/logs/tests-normal.log | `5a56918615eae75c90a7c482e4e62a27e113f7d96aaedada9a5bf7b326dd2837` |
| reproduction/aristotle-posterior-analytics-i20/results.json | `0e0407d5e4d0ccab8306a44b5329fe43d3c2385644dd9b3222029ecae6a697e4` |
| reproduction/aristotle-posterior-analytics-i20/run_notebook.py | `8c17ba299417241e62a841eb2b6edb75c6107ddb0eb547e27f15cd45a8166d7f` |
| reproduction/aristotle-posterior-analytics-i20/test_intervals.py | `75654ceef715e192df56f3e0ff95535d34229797720de39fa246334bf54ef3c3` |
| reproduction/aristotle-posterior-analytics-i20/tutorial.ipynb | `f0b8d34d0e51995778074333f1dcdf26e9377f683895c1e83bba1b1c5ea1f63f` |
