# III.12 独立技术审查

审查日期：2026-10-29。结论：**通过已声明范围的技术审查**，不是人类专家或形式证明器认证。

绑定正文：`papers/ancient/euclid-elements-iii12.zh-CN.md`，SHA256 `546431469907c4ba6001facf68b73b9653d5fca88b5a6ddbecb1fbca3bbc510a`。

由不同于正文及复现实现者的审查代理独立阅读全文、全部源码、Notebook代码格、保存输出及运行说明；独立执行而非复制主作者日志。源码哈希见 [code-sha256.json](independent-review/code-sha256.json)。正文以后若修改，须重核受影响内容及重新绑定；源码改变则重跑受影响检查。

## 1 一般证明与输入规格

- 正半径现代圆盘模型明确把“内部不重叠”和“共同边界点”分开。加权点X=(rF+RG)/(R+r)在d<R+r时同时严格位于两内部，给出必要下界；共同点再给上界，未预设等式。新增的反向不等式论证补全`interiors_disjoint`接口的一般等价依据。
- a=A−F、b=G−A的等号推导正确，归一向量差的平方为零给同向，接点系数R/(R+r)严格介于0与1。唯一性在现代模型中直接得到，未调用III.13作为前提。
- 原证的C=D弱不等式和共线延长线分支与现代证明分开。后者不冒充古典拓扑公理的形式认证。
- 手算(0,0)、(3,4)、半径2与3的接点(6/5,8/5)正确；共同点不等于外切、不交不等于存在接点、内切不等于外切的三个反例正确。零半径破坏严格介于，排除合理。
- `Circle`构造明确拒绝零负半径及非整数/Fraction值；布尔数也拒绝。关系分类与验证接口没有依赖可被`-O`删除的裸断言。`contact_candidate`先确认外切，再构造；`verify_contact`独立接收点，先检前提再检等号、叉积及投影。
- 输入中的内域不交由平方距离判据实现，不是遍历所有盘内点。正文现已证明判据；代码检查仍不是一般证明。`concentric_disjoint`仅指圆周不交，README明确区分圆盘。

## 2 审查发现与修正闭环

1. 初稿只给“内部不交⇒d≥半径和”和等号时逆向论证，未完整写出一般下界充分性。已要求并复核补入：d≥R+r时若Y在两内部，则d≤FY+YG<R+r，矛盾。
2. 初稿以5−ε说明相交而未显式限定ε范围。已要求并复核改为0<ε<1，避免大ε进入内含或无效距离分支。

以上仅正文澄清，源码无需改动。当前正文实跑表与实际日志一致，无未填占位。

## 3 独立真实执行

CPython 3.12.14，仅标准库，无安装、无网络。以下每条真实返回码为0：

| 命令 | 结果 | 日志 |
|---|---|---|
| `python -m unittest -v test_geometry` | 30项；内部网格960构形×双圆序1920证书 | [普通](independent-review/tests.log) |
| `python -O -m unittest -v test_geometry` | 同一30项及同一确定性网格 | [优化](independent-review/tests-O.log) |
| `python -OO -m unittest -v test_geometry` | 同一30项及同一确定性网格 | [二级优化](independent-review/tests-OO.log) |
| `python run_examples.py` | 4合法、3预期拒绝，另运行960构形网格 | [算例](independent-review/examples.log) |
| `python verify_notebook.py` | 5代码格真实重执行，stdout逐格匹配 | [Notebook回放](independent-review/notebook.log) |
| `python independent-review/check.py` | 下列独立oracle检查通过 | [普通oracle](independent-review/oracle.log) |
| `python -O independent-review/check.py` | 同一独立检查通过 | [优化oracle](independent-review/oracle-O.log) |
| `python -OO independent-review/check.py` | 同一独立检查通过 | [二级优化oracle](independent-review/oracle-OO.log) |

Notebook回放没有改写源Notebook，不是Jupyter kernel、nbformat完整模式或前端渲染认证。审查未将`create_notebook.py`再写一遍文件的行为混称只读回放；实际另读了构建执行代码及原保存日志。

## 4 独立判定方法和边界覆盖

[独立脚本](independent-review/check.py)不调用被测`relation`来生成期望值。中心F固定(0,0)，G的两个整数坐标各取−5…5，两半径各取1…4，共1936圆对。以根轴脚点参数t=(d²+R²−r²)/(2d²)及垂距平方h²=R²−t²d²判交点类型；d=0单独处理。h²为零且0<t<1为外切，其他相应分支分开。这与被测代码直接比较半径和差的实现不同，但仍基于同一欧氏数学，不是独立公理证明。

每对另检查49个整数候选点，共94864次接受/拒绝核验，期望接受要求独立oracle为外切且点等于根轴接点。72外切圆对检查交换圆序和构造点一致；每个接点加三个精确扰动，共216次拒绝。另核15个非法半径或坐标输入、正文4个手算/反例。分类计数和候选接受计数完整保留于oracle日志。

三模式重跑同一确定性集合不是三倍不同样本；有限网格不是全实数圆对覆盖。平方运算精确，不提供带噪或浮点近似判定保证。审查没有验证任意无理交点求解、古代全部公理、未来命题或其他论文。
