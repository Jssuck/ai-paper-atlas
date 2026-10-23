# II.13 独立数学与代码审查

结论：**通过**。审查针对下列冻结文件；正文或实现变化后必须复核受影响内容并重新绑定，不能把此结论外推到未来版本。

## 审查方法和边界

独立实读Owen1853印208–209中XIII全文，并对照Jenkinson第13章转录；来源校勘责任另见[来源独审](aristotle-prior-analytics-ii13.source-audit.zh-CN.md)。本报告检查第三格内部步骤、外部归谬撤除、存在条件、反模型、模型压缩说明与12题答案，不裁定古代唯一存在语义。

另写[显式集合oracle](../../reproduction/aristotle-prior-analytics-ii13/independent/oracle.py)，不导入生产求值器：把占用类型实例化为对象集合，用包含、交集、差集独立判定。生产JSON仅作为待核数据输入。已实际运行普通、-O、-OO三个模式，均核对256条内部/外部记录及17项具名检查；有效性、前提模型数、反模型数及最小反模型逐字段相同。另实际重跑生产13项单元测试成功。日志与命令见[独立核验说明](../../reproduction/aristotle-prior-analytics-ii13/independent/README.md)。

## 数学核验

1. 四条原文路线分别以O、E、I、U为假设，内部结论O、O、I、I；它们是共同主项B的第三格步骤。固定背景否定内部结果，最终输出与假设矛盾，依次恢复U、I、E、O。内部中项与最终目标项的身份没有混淆。
2. 两个全称目标的临时特称假设自带见证；两个特称目标的固定I(C,B)负责存在。四条标准路线不另需所有项非空。
3. 错误E假设加U(C,B)得到O(A,C)，以及错误U假设加U(C,B)得到I(A,C)，均须B存在。空B反例及B存在修复已核；默认允许空项时正文没有把传统省略存在条件无条件化。
4. 排除E只直接给I，排除U只直接给O。正文明确完整原背景仍可另证原目标，没有声称存在满足完整有效背景却反驳目标的模型。I/O共真与两个特称前提可由不同对象满足的例子均正确。
5. 内部无全称结论的一般新增对象构造有效：新增对象不在B，故两个以B为主项的前提不变；选择在C非A或在A交C分别反驳U或E。保留了前提可满足、可扩展论域、无额外覆盖约束的限定。
6. 非空论域八种一元类型支持给255模式，三项均非空218，只B非空240。保留每种已占类型的代表保持四型句真值，理由独立于运行次数。有限实跑没有冒充一般自然语言推理或古代算法的完整复现。
7. 两政策64条固定项位路线，按U/E/I/O目标计有效证书为1/1/1/1及1/1/2/2，与独立实现一致。内部与外部各自前提可满足才接受，排除了不相容背景造成的真空证书。
8. 全部12道练习的答案与正文符号、背景、存在政策和反例一致。

## 代码检查

生产输入检查排除空论域、重复/越界/布尔类型编码、非法形式和项名、错误政策及非法前提容器；所有公式在语义判断前校验，非法结论不能被不相容前提短路隐藏。测试使用unittest方法，独立oracle使用显式异常，均不依赖会被-O删去的裸assert。普通及两优化模式的生产JSON逐字一致；独立oracle也三模式通过。这里只报告实际运行的单元和有限模型检查，不声称仓库CI或外部环境通过。

## 冻结SHA-256

|文件|SHA-256|
|---|---|
| `papers/ancient/aristotle-prior-analytics-ii13.zh-CN.md` | `6c2bd72fa078308b9043b73291be88e8580f5048e47cca94923fffec44b63ac5` |
| `reproduction/aristotle-prior-analytics-ii13/reproduce.py` | `fb36aa4fdec7ad652db15b7c0e37a2fb8f0581aff2027efb7413620a19ab0554` |
| `reproduction/aristotle-prior-analytics-ii13/test_reproduce.py` | `c2146f1fc552c29fabe81d968fb4f603ab2b87090eac6ff470d990c6b9e59b2c` |
| `reproduction/aristotle-prior-analytics-ii13/run_all.py` | `9c5a8a7eebe25901906cd97168ea20ba03438d7beca10567677815011a2a8135` |
| `reproduction/aristotle-prior-analytics-ii13/run.sh` | `51fce7de32b54582a66a9ab2921b32bdd5410820dff85f5b4c8b78122668b8ff` |
| `reproduction/aristotle-prior-analytics-ii13/independent/oracle.py` | `76b50ac146ebcc6e34c663e6572e9e86e2e40abd234da915ea750360b8ba49a7` |
| `reproduction/aristotle-prior-analytics-ii13/evidence/results-normal.json` | `125b022196813de070cf67d2d71c0d1261b5d9bb840e5373a09843dc4cd22b0d` |

审查公开内容仅含原创分析、独立教学核验代码与真实运行证据，不含原书扫描或私人记录。
