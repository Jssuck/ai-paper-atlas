# II.17：固定背景删除假设的原创教学实验

这是有限的**全称肯定包含图**模型，不是古代三段论全集、几何证明器、现实因果模型，也不是自动判定任意自然语言论证真假的系统。研究对象见[正文](../../papers/ancient/aristotle-prior-analytics-ii17.zh-CN.md)与[来源台账](../../papers/ancient/aristotle-prior-analytics-ii17.sources.zh-CN.md)。原文II.17的否定情形、归谬所需的已知不可能性、背景前提可信性未由程序认证。

## 1. 模型与接口

边 `(s,p)` 表示“所有 s 都是 p”，即包含方向由主项指向谓项。节点名仅为符号。`closure` 计算含自反关系的传递闭包；不要求每个类非空，不从全称关系推出特称存在。`hypothesis` 必须是当前边集的一条实际前提。

`analyze` 在**同一个节点集和固定剩余前提**上比较：

- `before`：原边集能否导出目标。
- `after_deleted`：只删指定假设后能否导出同一目标。
- `necessary_within_graph`：原来能导出且删除后不能，限当前受限演算。
- `supports`：推出目标的全部包含极小边子集，不是长度最短路径。
- `proof_uses_hypothesis`：给定一条合法证明路径是否实际用了假设；未提供路径时为null。

路径含该假设，不保证假设不可替代；另一路径可能避开它。初始目标就不可导时，`necessary_within_graph=false` 不应误读为已成功展示无关的归谬。程序报告的是目标关系，不自行把它标为矛盾；在用于归谬的教学情境中，“目标不可能”是额外的外部条件。

`minimal_supports` 枚举简单路径。理由：任何可达游走可删循环；简单路径上的每条边在该路径子图内都不可删；任何包含极小可达边集不能多于一条所含简单路径。自反目标由空支持导出。此为一般图论理由；下面有限测试仅检查实现。

## 2. 原文关联与新增例

65b20–39的下行链用B→A、C→B、D→C表示：D→B不需要B→A，而同一链的D→A需要它。上行链B→A、A→E、E→F中，A→F不需要B→A，B→F需要它。相同字母出现在背景里不等于实际依赖。

66a1–15强调删除与替换不同。原背景删B→A后，D→A不再可导；若另加C→K、K→A使目标重现，那是改变前提的另一推导，不能倒推原假设无关。我们另给同时已有两条路径的例子，此时删除后确实仍有目标。

其余自反、循环绕路、初始不可导和断开图是明确新增的教学边界例。不存在把负前提当正边或从不一致前提出任意结论的规则。

## 3. 环境与重跑

仅Python标准库，无安装步骤。在此目录运行 `sh run.sh`。脚本分别运行：`python3 -m unittest -v test_logic.py`、`python3 -O -m unittest -v test_logic.py`、`python3 -OO -m unittest -v test_logic.py`，并运行相同模式的`logic.py`输出JSON，最后逐字比较结果，执行独立核验并生成SHA256清单。测试使用unittest断言方法，不依赖被优化删除的Python assert。

环境：见[evidence/environment.txt](evidence/environment.txt)。真实日志：[normal](evidence/tests-normal.log)、[-O](evidence/tests-O.log)、[-OO](evidence/tests-OO.log)。结果：[normal](evidence/results-normal.json)、[-O](evidence/results-O.json)、[-OO](evidence/results-OO.json)。[源码](logic.py)、[测试](test_logic.py)、[脚本](run.sh)、[哈希](SHA256SUMS)。

## 4. 实跑结果

三模式各15项测试通过，三个JSON逐字一致。枚举3节点6种无自环边的全部64个图，对每条已有假设和9种有向目标检查共1728记录：原可导1416，删除后仍可导1176，原可导而删除后不可导240；1728次极小支持与删除结果等价核验通过。十个具名情境单独保存。

数字只描述固定枚举范围。有限枚举不证明所有数学定理，不证明背景真实，不认证任何历史人物的几何推理，也不保证在扩大规则集后依赖仍保持。

## 5. 独立核验

单独运行 `sh audit.sh` 可重跑[独立核验器](independent_oracle.py)。它不用简单路径枚举作为支持集真值：以三个类的单对象8种归属赋值核查包含有效性，并穷举原边集全部子集求极小支持，与实现比较全部64图的576个目标，再核查1728次删除。三模式均通过，独立统计亦为1416 / 1176 / 240；见[normal](evidence/oracle-normal.json)、[-O](evidence/oracle-O.json)、[-OO](evidence/oracle-OO.json)。单对象语义核查适用于本模型的纯全称包含关系，不扩展为任意量词或归谬系统的完备性证明。
