# II.27：迹象推理的最小逻辑核验

配合[中文深读](../../papers/ancient/aristotle-prior-analytics-ii27.zh-CN.md)与[来源台账](../../papers/ancient/aristotle-prior-analytics-ii27.sources.zh-CN.md)。本包是原创教学重构，不是古代程序的复刻，更不是医学、相面或人格识别实验。没有采集人或动物数据，没有训练分类器；所有集合和布尔行都是人为构造。

## 1. 范围与假设

实读《前分析篇》II.27 的三格迹象讨论和卷末条件性论证；程序核验其中可明确形式化的包含、存在与条件方向，不模拟所有历史语义。原文中的生理例只是原典材料；程序不认可其经验正确性，也不能据身体特征推断任何人的性格。

有限论域取大小0至4，包含空域作为现代语义边界测试，不声称Aristotle接受空域。每个谓词是论域子集，以整数位掩码存储：第i位为1表示对象i满足该谓词。空项允许；特称结论必须有见证。C既可为任意类，也可为单元素类以表示原文的个体例。第二格/第三格反模型另报告A、B、C都非空的最小实例，避免把无效性仅归因于空项。

以下A、B、C按**每一行的项位**解释；原文在不同例子中重新分配字母，不能把所有行里的A理解为同一经验属性。

| 路线名 | 前提 | 被检查结论 | 意义 |
|---|---|---|---|
| `first` | $`B\subseteq A,\ C\subseteq B`$ | $`C\subseteq A`$ | 第一格包含传递 |
| `second_affirmative` | $`B\subseteq A,\ C\subseteq A`$ | $`C\subseteq B`$ | 两类共有性质，不保证类间包含 |
| `third_particular` | $`C\subseteq A,\ C\subseteq B,\ C\ne\varnothing`$ | $`A\cap B\ne\varnothing`$ | 共同的实际见证 |
| `third_universal_overreach` | 同上 | $`B\subseteq A`$ | 从一例越界到全类 |
| `third_missing_existence` | $`C\subseteq A,\ C\subseteq B`$ | $`A\cap B\ne\varnothing`$ | 漏掉存在前提的变体 |
| `correlative_sign` | $`A=B,\ C\subseteq B`$ | $`C\subseteq A`$ | 卷末强对应条件的蕴涵片段 |
| `one_way_sign_inverse` | $`A\subseteq B,\ C\subseteq B`$ | $`C\subseteq A`$ | 仅有“性质推出符号”不能倒推 |

`correlative_sign`没有把原文“B严格广于C”的描述作为必需条件；本测试使用较弱的C包含于B，所以也覆盖原文的严格包含子情形。测试另有A=B={0,1}、C={0}的具体严格包含实例。由B推出A的正向推理只需B包含于A，A=B是更强的双向条件；程序不误称双向对应为所有第一格推理的必要条件。

## 2. 一般论证与反模型

第一格：任取C中的对象，它因小前提属于B，再因大前提属于A，所以C包含于A。第三格：从非空C选取见证，它同时属于A和B，所以交集非空。这两个论证不依赖有限大小。A=B的路线可直接替换；这些一般理由才说明有效性，枚举零反例只核验代码和小域的一致性。

反模型中的掩码1代表{0}，2代表{1}，3代表{0,1}：

- 第二格：A={0,1}、B={0}、C={1}。两个包含前提真，但C不包含于B。
- 第三格越界：A=C={0}、B={0,1}。共同见证真实，但对象1反驳“所有B为A”。
- 缺存在：A=B=C=空集。两个全称前提真，却没有交集见证；非空论域内也可以令三项全空，所以问题不依赖空域。
- 单向符号倒推：A={0}、B={0,1}、C={1}。A推出B、C满足B，但C没有A。这说明必须检查方向，而不是给“符号”贴标签就得到证明。

原文第三格论证可有有效的特称结论；它不能支持目标全称。原文所批评的第二格是这里的双肯定排列，**不是所有第二格三段论均无效**。形式有效也不保证历史经验前提真。

## 3. “通常”不是“全称”

`majority_example`制造10个布尔值，9真1假，用精确有理数记录9/10；此时严格多数为真，全称为假。二分之一阈值只是本文选定的现代教学阈值，**不是将原文eikos定义成频率超过二分之一**。本例没有抽样统计、置信区间、基线数据或总体推广，不能拿一个例外否定“通常如此”，也不能拿多数替代无例外的大前提。

## 4. 共同出现与对应关系的识别

`mappings`处理四个抽象布尔列T0、T1、S0、S1。教学中额外假设：两性质与两符号形成一一对应，且对应列在观察对象上严格同真同假。它枚举仅有的两种双射，不推断因果。

1. 只有行(真,真,真,真)：两种对应均吻合。共同出现不足以区分。
2. 加入行(真,假,真,假)：在既定模型内，只剩T0对应S0、T1对应S1。
3. 再加入行(真,假,假,真)：两种全局双射都被这些行排除。

第二步不是证明未观察对象也服从对应；第三步就是反例。双射、无噪声、准确测量、观测覆盖均是强假设，不是由代码建立的事实。原文关于身体与心理状态共同变化、每种状态有唯一符号及跨类适用的设定，必须另外论证；本教学模块不替它们提供经验支持。

## 5. 运行与环境

仅Python标准库，无网络、密钥、付费服务、第三方依赖。运行：

```bash
cd reproduction/aristotle-prior-analytics-ii27
bash run.sh
```

`run.sh`在普通、`-O`、`-OO`模式各执行：

```bash
python3 -m unittest -v test_signs.py
python3 signs.py --max-n 4
```

优化模式在`python3`后插入对应开关。测试采用`unittest`检查方法和显式异常，不以会被优化删除的Python `assert`语句作为核验。环境见[environment.json](environment.json)。脚本只重写本目录的真实运行日志和环境文件；重复运行测试耗时可能不同，不宣称日志逐字可重复。

## 6. 实跑结果与证据

本次18项测试在三种模式全部通过。每模式遍历4681个世界（各域大小的8的n次方之和），每世界检查7路线，共32767组前提/结论；三份结果JSON的语义完全一致。

| 路线 | 满足前提模型数 | 结论不成立模型数 |
|---|---:|---:|
| first | 341 | 0 |
| second_affirmative | 781 | 440 |
| third_particular | 440 | 0 |
| third_universal_overreach | 440 | 220 |
| third_missing_existence | 781 | 121 |
| correlative_sign | 121 | 0 |
| one_way_sign_inverse | 781 | 440 |

这些模型数不是自然界发生率；它们来自带标签的全部子集组合，不去除同构，不能用比例估计现实概率。

- 源码：[signs.py](signs.py)、[test_signs.py](test_signs.py)、[run.sh](run.sh)。
- 测试：[normal](logs/tests-normal.log)、[-O](logs/tests-O.log)、[-OO](logs/tests-OO.log)。
- 结果：[normal](logs/results-normal.json)、[-O](logs/results-O.json)、[-OO](logs/results-OO.json)。
- 模式比对：[comparison.log](logs/comparison.log)。

独立核验见[audit/README.md](audit/README.md)与[独立技术审查](../../papers/ancient/aristotle-prior-analytics-ii27.technical-review.zh-CN.md)：独立逐对象重算4681模型、32767路线，比较生产七路线全部28聚合/首反例字段及合成多数/映射字段，三模式一致；另5项独立测试×3包含5种损坏结果拒绝。这不是生产逐世界中间证书的逐项比较，也不把生产测试自身当作独立审查。这个有限实验既不是全部原典的形式化，也不是对一般定理、因果关系或相面假设的实验证明。
