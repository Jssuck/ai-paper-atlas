# II.17 独立技术核验

核验对象为[中文深读](aristotle-prior-analytics-ii17.zh-CN.md)及[原创教学代码](../../reproduction/aristotle-prior-analytics-ii17/README.md)。本报告只评价下述限定模型与正文数学，不认证古代逻辑全集，也不替代来源审查或发布后的页面检查。

## 1. 方法及结论

**通过（限绑定版本及注明范围）。** 独立阅读 Jenkinson II.17 连续正文，并目读 Owen 印页219–221的本章部分，对照原文的下行、上行链及章末删除/替换区别。正文四类证据层次清楚；没有把现代图模型冒称原文算法。

技术核验没有把另一份传递闭包程序当作独立裁判：[independent_oracle.py](../../reproduction/aristotle-prior-analytics-ii17/independent_oracle.py) 枚举单个对象对三个项的8种布尔归属，以“非主项或谓项”直接评价每条全称包含；对所有前提成立的赋值检查目标。极小支持则穷举全部边子集并按包含关系极小化，与生产代码的路径枚举独立。

这种语义方法的适用理由是：全称包含逐对象成立；若存在一个集合模型违反目标，其中的反例对象自身就提供一个违反目标而满足所有前提的布尔位型。反之，每个位型都可由一个单对象模型实现。因此它适用于本肯定包含语言的任意集合解释，不要求各项非空。这里的一般语义论证与下面有限实现测试不可混淆。

## 2. 真实执行与复核

- 生产测试实际重跑普通、`-O`、`-OO` 模式，各15项通过。
- 独立检查三种模式各覆盖64个三节点无自环图、576个目标的闭包判断、576个目标的完整极小支持族、1728个删除记录，均通过，三份独立输出逐字一致。
- 独立统计原来可导1416条、删除后仍可导1176条、删除必要240条，与生产统计相同；312条原来不可导，不计作成功反证或已证无关。
- [audit.sh](../../reproduction/aristotle-prior-analytics-ii17/audit.sh) 可重跑独立审查；[normal证据](../../reproduction/aristotle-prior-analytics-ii17/evidence/oracle-normal.json)、[-O证据](../../reproduction/aristotle-prior-analytics-ii17/evidence/oracle-O.json)、[-OO证据](../../reproduction/aristotle-prior-analytics-ii17/evidence/oracle-OO.json) 保存真实结果。生产命令、环境、日志及校验清单见复现目录。
- 测试用显式异常或unittest断言方法，不依赖优化模式会删除的`assert`。已核验现有`SHA256SUMS`各条一致。

## 3. 逐项数学核验

1. `U(A,B)`对应B→A；下行目标D→B不依赖B→A，而仅有原三条边时D→A依赖它；上行目标A→F与B→F区分正确。
2. 两个删除后的非空项反模型满足全部剩余背景、违反指定目标；不要求反模型满足已删除假设。负关系教学例中的A=D与B=C两组不交集合也确实构成反模型，代码明确不覆盖否定式。
3. 章末固定背景与新增K链的区分正确。已使用假设只是某条证明的事实，不等价于每个支持都需要它；本来就在背景中的第二路径可否定必要性。
4. 极小支持为包含极小而非最短：非自反目标的极小支持恰是简单路径边集，自反目标的空支持正确。循环绕路可以使用冗余假设，却不改变空/简单支持的判定。
5. 输入要求实际存在的假设边，给定证明路径检查端点及所有边；初始不可导单独报告。闭包的中介节点归纳与生产Floyd–Warshall循环相符。
6. 七道练习及答案均与限定模型吻合。必要性不认证前提真实性、目标不可能性或唯一责任来源；在扩展演算中依赖可能改变。

审查修订：将正文对独立检查的描述精确改为集合语义/子集法；将闭包证明补为与实际实现相符的中介节点不变式。未发现需改变本章主要结论的数学错误。

## 4. 版本绑定（SHA-256）

以下绑定正文及关键可执行文件；修改这些文件后应重新核验。本报告不以有限枚举声称一般历史理论完整复现。

```text
497626fe627ef02118bc06719b8c455967ac1bb1cddb06d6a1ec966f98507817  papers/ancient/aristotle-prior-analytics-ii17.zh-CN.md
ec55b2bff94c72e80cc6ee7a976acaa86624ca9087456ca52174a9c056284145  reproduction/aristotle-prior-analytics-ii17/logic.py
33a9662e8c5acbffb6bf877798d53bd746e58b47af5161847e8700d04f5371cf  reproduction/aristotle-prior-analytics-ii17/test_logic.py
2593d3f5f94ff847c9ef4c52c4bb2c72978b12cb445709cf43822d265baa11f8  reproduction/aristotle-prior-analytics-ii17/independent_oracle.py
9b4823e17c4c21a076f4ef62c8b4e8412be69fb84f3246be1b16a215d7437dda  reproduction/aristotle-prior-analytics-ii17/audit.sh
c7dcafa42f6290f032f9c3eabbd2b2332b538822578403503b15d501f5c40386  reproduction/aristotle-prior-analytics-ii17/run.sh
baf538ddc6fa5ea84f341fb500cf6f596aa3fbc038f67c4463562761d549091f  reproduction/aristotle-prior-analytics-ii17/SHA256SUMS
```
