# II.11 独立数学与代码核验

结论：所列冻结文件通过本次独立技术核验。有限模型核验不替代一般证明，也不裁定古代唯一语义。来源校勘另见[独立来源审查](aristotle-prior-analytics-ii11.source-audit.zh-CN.md)。

## 核验边界与独立性

独立阅读Owen印204–207及Jenkinson第二卷第11章之后，先以占用的三位成员类型实现oracle，再读取生产结果进行比较。oracle不导入生产模块、不调用其truth、models或classify函数：它逐一检查对象位并独立计算量词真值。双方都使用已声明的有限集合语义，因此这是实现层独立核验，不是两个独立历史语义学理论。

[独立代码](../../reproduction/aristotle-prior-analytics-ii11/independent/check_independent.py)使用显式异常检查，不会在优化模式下被删除。

## 数学与正文审阅

1. 核对谓项在前的U/E/I/O定义以及U/O、E/I整句矛盾；允许空项时配对仍精确。两个全称相反可同真，两个特称可由不同对象共真。
2. 检查第3节的任意模型归谬证明：可靠背景保留，仅撤除临时假设；最终目标必须是该假设的否定或另有已证桥。背景可满足只是诊断条件，不证明现实可靠性。
3. 逐步核对I、E、O三类路线中的同一见证和项位。全称I路线需C存在，特称小前提自带见证；否定前提放在大前提与小前提不是同一情形。
4. 核对错误反对假设的两组完整反例、混合I/O共真例，以及第4节两种第一格位置的失败例。第一格限制明确限于单个内部三段论，没有扩大为任意多步逻辑不可证。
5. 核对12题答案。第5题已明确C存在是这条路线的充分补充，而非I(A,B)在一切模型中的必要条件。
6. 核对八类型压缩理由：无等号的一元四型命题只依赖类型是否出现，不依赖重数。正文的一般证明与程序的有限检查分开陈述。

## 真实独立实跑

每种模式均得到相同结果：

- 非空论域允许空项255模型；三个项都非空218模型。
- 每种政策独立穷举64个第一格式，分别得到4个基本有效式和6个包含弱化的有效式。
- 每个有效式把两条前提分别视为假设，得到8/12条反证证书；所有独立背景都有模型，目标类别均只有E/I/O，没有U。
- 独立逐项对照生产256条候选记录：内部有效性、内部前提模型数、撤除有效性、背景模型数、证书标记、内部与撤除的最小支持集反模型均一致。
- 对照11项具名关系、混合实例的位编码与真值；另独立检验空C反例、C存在修补及真I假设的32个保真模型。
- 三份生产JSON逐字相同。独立重运行生产源码，结果再次逐字吻合；普通、-O、-OO模式的12项生产测试均成功。

日志：[普通独审](../../reproduction/aristotle-prior-analytics-ii11/independent/normal.log)、[-O独审](../../reproduction/aristotle-prior-analytics-ii11/independent/O.log)、[-OO独审](../../reproduction/aristotle-prior-analytics-ii11/independent/OO.log)、[生产重运行](../../reproduction/aristotle-prior-analytics-ii11/independent/production-rerun.log)。

这里的有效式与证书数字是明示模型下的教学分类，不是原文自报数量。检验一个证书的语义蕴涵不是机械证明助理内核的完整证明对象验证。

## 代码修正与检查

检查了成员类型和展示集合的一致性。生产最终混合实例为A={7}、B=C={6,7}，与三位编码相符；回归测试核对每一项。输入验证改为离散成员检查，拒绝空字符串及多字元子串，新增相关回归；最终12项测试在三模式都实际执行。审阅一键运行脚本：子过程失败停止、保留输出、比较三结果字节并生成生产SHA清单；未安装第三方依赖。

## 冻结SHA-256

以下哈希绑定本次通过状态。后续更改正文、源码、测试或范围声明须重新核验，而不是沿用结论。

|文件|SHA-256|
|---|---|
|`papers/ancient/aristotle-prior-analytics-ii11.zh-CN.md`|`eee779cfec981cbc3416037dd71e83ce532344c31fdf4f49858e8a1553e27f2f`|
|`reproduction/aristotle-prior-analytics-ii11/reproduce.py`|`465d9d714e4f7c81314a135362fbb8d56fb19c976d6c10d7934b31a381bf97ed`|
|`reproduction/aristotle-prior-analytics-ii11/test_reproduce.py`|`98fac29bf782bc5cb79b78698027bca6ad9eac9b4d8951921c5c2be45c68b649`|
|`reproduction/aristotle-prior-analytics-ii11/run_all.py`|`0ba9568374c8d56bbcc124bb327de2c8e568413f303ca36dae57b6c076dd3541`|
|`reproduction/aristotle-prior-analytics-ii11/README.md`|`a9a83eb5722174ce730ce18feb9641c9139dba62ca5881ef80a5fe878d16d81f`|
|`reproduction/aristotle-prior-analytics-ii11/independent/check_independent.py`|`cab01389dd6e3faad7719a923e3a87596da776d97e6ef701937a21b7e6705a00`|
|`reproduction/aristotle-prior-analytics-ii11/evidence/results-normal.json`|`930c3eda354901a2e55174022997802e9b01d2981aaf850c26043bb40a25827d`|

检查日期：2026-10-23（UTC）。本报告未验证现实背景事实、自然语言自动解析、所有古代解释、模态或多步系统。无未解决技术阻碍。
