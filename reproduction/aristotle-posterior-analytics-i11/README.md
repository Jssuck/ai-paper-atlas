# 《后分析篇》I.11：中项身份、局部冲突与排中范围

这是原创现代教学实验，不是亚里士多德逻辑的完整实现，也不是古代哲学主张的实验性证明。只使用Python标准库；没有数据下载、模型训练或付费服务。

## 标识和固定个体范围

正文的human(c)等记号用于解释一个固定个体c。实现把这些实例视为已ground（已代入个体）的命题标识；`Literal`没有对象参数、变量、量词实例化或合一机制，不能把只含human的标识当成可区分多个个体的完整一阶引擎。

## 三个问题，不混成一个逻辑系统

1. **中项是否同一。** `Literal`的`predicate_id`是显式语义标识。表面同名不自动建立规则连边；bank.financial与bank.river是不同标识。系统不替人判断自然语言是否同义，输入标识本身需要人工论证。
2. **局部推导是否需要全局一致。** `closure`对明确给出的Horn规则做最小闭包。正、负支持是两个独立的原子；出现human与负human，不会撤销human推出animal的路线。程序不含从矛盾推出任意结论的规则，也不含逆否推理。这是特意选定的非爆炸教学重构，不能据此称亚里士多德接受真实矛盾，更不等于对本章所有句子的形式化。
3. **列出的两种情形是否穷尽。** 独立的Kleene强三值模块把U作为未定值，否定U仍为U，析取按F<U<T取最大值。p或非p在T/F为T，在U为U。`cases_exhaustive`仅检查显式允许值是否被列举情形覆盖；不是自动反证证明器。若本地已明确限定p只取T或F，则二分覆盖；这不限制其他命题。该模块是缺口模型，不是前一模块的正负冲突模型，两者不可混用。

## 可手算的对照

给出human正支持和规则human→animal，即得到animal正支持。再加human负支持，原路线仍存在，但没有给出其他任意命题的支持。若还给出human→负animal，则animal同时具有正负支持。`support_status`的四个返回值依次表示“正支持有无、负支持有无”，不是四种已认证的现实真值。

特别重要：animal的状态(True,False)只说本次闭包有正支持、没有负支持。它**不是**对“否定animal为假”或双重否定animal的证明。缺少负证据不能替代否定证明。原文在大项上的限制比这一纯支持演示更强，必须由正文分别说明。

对排中模块，T和F两行的p或非p为T，U行为U。若有人声称“已检查p与非p，所以所有可能情况均完成”，其结论还依赖允许值确实只有T/F。未定行是现代教学边界反例，不是本章提出了三值逻辑，也不是反证法的一般反驳。

## 实现与核验

- `model.py`：不可变的显式项标识、Horn闭包、支持查询、K3与覆盖检查；输入检查用异常而非可被优化移除的assert。
- `test_model.py`：18项unittest，包含同名异义、双支持、不爆炸、不逆否、未获负支持、合取前件、空前件、循环无种子、局部二分与非法输入。
- `graph_oracle`：仅对一元规则特例使用独立Warshall传递闭包，不调用生产`closure`。四个有符号原子可形成12条非自环有向边，遍历全部4096规则图及16初始集合，共65536组合。生产实现支持多前件，但此枚举**不覆盖所有多前件规则系统**；生产检查中多前件由定向单测检查；独立审查另以闭集模型交集检查三个原子上的全部有序两规则系统，范围和局限见审查报告。
- `results.json`及`logs/`：本次真实运行结果、命令及环境。三种优化模式分别运行同一测试和枚举；模式一致不替代独立理论证明。

运行：`bash run.sh`。脚本以失败即停止方式运行，重跑会刷新日志；Python 3.10以上支持这里使用的标准库特性。没有第三方依赖。

## 一般性质的教学证明

闭包迭代只增加事实，且可加入的事实只来自有限初始集合及有限规则结论，所以必停。停止时每条已满足前件的规则结论都已在集合内。任何包含初始事实、对全部规则封闭的集合，在归纳的每一轮都包含本轮结果，因此停止集合是最小闭包。加事实不可能删除旧推导，由同样的轮数归纳得到单调性。此论证适用于这里定义的有限规则模型；不证明现实知识、语义同一、古代本体论或无限理论的性质。

## 复盘

原文关心证明实际需要哪些共同原则，而非先把所有原则作为显式前提堆进去。教学代码只展示输入身份、规则选择和情形覆盖会改变检查结果。它不能自动识别真实歧义、判定科学学科的对象属、验证共同公理的现实正确性，或替代本章独立来源阅读。

## 可点击源码与证据索引

- [模型源码](model.py) · [生产测试](test_model.py) · [运行脚本](run.sh) · [结果](results.json) · [文件摘要](SHA256SUMS)
- [生产环境](logs/environment.txt)；测试：[normal](logs/tests-normal.log)、[-O](logs/tests-O.log)、[-OO](logs/tests-OO.log)；枚举：[normal](logs/enumeration-normal.log)、[-O](logs/enumeration-O.log)、[-OO](logs/enumeration-OO.log)。
- [独立技术审查](../../papers/ancient/aristotle-posterior-analytics-i11.technical-review.zh-CN.md) · [独立测试源码](audit/independent_test.py) · [独立运行环境](audit/environment.log)
- 独立测试：[normal](audit/independent-normal.log)、[-O](audit/independent-O.log)、[-OO](audit/independent-OO.log)；生产测试复核：[normal](audit/production-repeat-normal.log)、[-O](audit/production-repeat-O.log)、[-OO](audit/production-repeat-OO.log)；枚举复核：[normal](audit/enumeration-repeat-normal.log)、[-O](audit/enumeration-repeat-O.log)、[-OO](audit/enumeration-repeat-OO.log)。
