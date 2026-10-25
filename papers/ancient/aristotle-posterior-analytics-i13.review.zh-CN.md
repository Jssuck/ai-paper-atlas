# 后分析篇 I13 教学模型独立技术核验

## 结论与审查范围

**技术通过，限于明示的集合语义与二值结构模型。** [当前正文](aristotle-posterior-analytics-i13.zh-CN.md)的集合推导、反例、有限计数和干预计算与公开实现一致，未发现阻止技术通过的错误。此结论不认证古代天文学、呼吸生理或伤口命题，不是历史诠释或一般因果识别定理的认证，也不是人类专家认证。原文定位另见[来源核验](aristotle-posterior-analytics-i13.source-audit.zh-CN.md)。

审查逐项读取正文、[复现说明](../../reproduction/aristotle-posterior-analytics-i13/README.md)、[模型](../../reproduction/aristotle-posterior-analytics-i13/model.py)、[作者测试](../../reproduction/aristotle-posterior-analytics-i13/test_model.py)、[运行脚本](../../reproduction/aristotle-posterior-analytics-i13/run.sh)和[结果](../../reproduction/aristotle-posterior-analytics-i13/results.json)。独立方法采用组合计数和手算响应表，不导入作者测试中的 oracle。重新执行作者测试是附加交叉检查，不替代独立推导。此前正文的复现 README 链接路径问题已修复，当前链接指向本章目录。

## 集合证明与反例

正文的 `C⊆B⊆A ⇒ C⊆A` 可由任取元素连续应用两次包含得到；反向解释链需要另有 `A⊆B`，不能从 `B⊆A` 免费倒置。`A={1,2}, B={1}` 确实反驳倒置。复现中的 `S={1}, C={0}, E={0,1}` 同时满足 `C⊆E` 与 `S⊆E`，却不满足 `S⊆C`，三个集合均非空。若只问某个特定 S，`S=C={0}, E={0,1}` 又说明局部结论可能成立而无全局互换桥；说明书没有把充分桥梁误称为每次局部逆推的必要条件。

否定式 `B⊆A`、`W∩A=∅ ⇒ W∩B=∅` 的反证也成立：共同属于 W 与 B 的元素必属于 A，直接矛盾。正文 `A={a,b}, B={a}, W={c}` 给出有效否定结论和见证 `b∈A\B`；源码中的数字标签只是重命名。删去 `B⊆A` 后，正文练习的 `A={1}, W=B={2}` 保留不相交前提而否定结论为假。

这些一般证明不依赖三元素穷举。采用的全称语义允许空集，不裁定古代命题的存在预设；同时单列非空反例，故逆推失败和中项过宽都不依赖空集。尤其，**推理有效性不自动认证适切原因**；外延过宽也不足以穷尽现代机制中必要原因、充分条件与背景条件的关系。

## 独立组合计数

三元素论域共有 `8³=512` 个三集合配置。逐元素独立选择合法成员状态，可直接复得结果，不必复用作者的三元组 oracle。

- 事实链按 `(S,E,C)` 排列，单元素仅有 `000、001、011、111` 四态，故前提数为 `4³=64`，均满足结论。
- 缺逆向桥时按 `(S,C,E)` 排列有 `000、001、011、101、111` 五态，共 `5³=125`；要求结论再排除 `101`，余 `4³`，所以反模型为 `125−64=61`。反模型中 S、E 已非空，C 为空的有 `3³−2³=19`，故全非空者为 `61−19=42`。
- `C=E` 且 `S⊆E` 每元素三态，共 `3³=27`，无反模型。
- 否定式按 `(W,A,B)` 排列仅有 `000、010、011、100`，故前提数 `4³=64`，结论均真。中项过宽要求至少一个 `010`，数量为 `4³−3³=37`。再要求 W、B 和 `A\B` 各非空，三元素恰须各占一类，共 `3!=6`。

[独立检查器](../../reproduction/aristotle-posterior-analytics-i13/review/check_independent.py)还用算术拆位构造成员集合，核对接口允许的 size 0 至 8 全部 `Σ4ⁿ=87381` 个集合对，而不止作者测试的 size 0 至 4。包含、相交与成员输出全部一致。原生整数与范围检查、拒绝布尔值、未知模型或干预键等输入保护使用显式异常；生产源码没有依靠优化时会消失的裸 `assert`。

这里应区分三种覆盖范围。一般集合式由逐元素证明保证；512 配置只检查三元素教学报告的统计；87381 个集合对检查所有受支持尺寸的底层函数，不等于在每个尺寸都枚举三集合组合。接口把尺寸上限设为 8 是资源约束，不是宣称集合论在更大论域失效。空宇宙只有一个空集合，包含和不相交都为真，与声明的现代语义相符。

## 二值模型与九种干预

令 M1 为 `X=U; Y=X`，M2 为 `Y=U; X=Y`，U 两值等权。下表每格依次列出 U 为 0、1 时的 `(X,Y)`，横线表示不替换该变量方程。它由方程手算，不调用作者候选解 oracle。

| X 替换 | Y 替换 | M1 两个响应 | M2 两个响应 |
|---|---|---|---|
| — | — | 00，11 | 00，11 |
| — | 0 | 00，10 | 00，00 |
| — | 1 | 01，11 | 11，11 |
| 0 | — | 00，00 | 00，01 |
| 0 | 0 | 00，00 | 00，00 |
| 0 | 1 | 01，01 | 01，01 |
| 1 | — | 11，11 | 10，11 |
| 1 | 0 | 10，10 | 10，10 |
| 1 | 1 | 11，11 | 11，11 |

九行乘两模型、两外生值为 36 个响应；各格两响应按 1/2 汇总，得到 18 个精确分布，均与实现及 JSON 一致。正常观察两模型同为 `P(00)=P(11)=1/2`，所以各自的 `P(Y=1｜X=1)=1`。但 `do(X=1)` 替换 X 方程而保留 U 分布，M1 的 `P(Y=1)=1`，M2 为 `1/2`；它不是筛选观察中 X 为 1 的记录。相同观察输入对应不同干预答案，只证明该候选模型类中的不可唯一确定，不证明所有因果问题不可解。

程序把方程方向作为输入，而非根据观察数据学得。两模型无环，给定外生值后确定；随机性完全来自已声明的均匀分布。干预可以同时替换两条内生方程，但不接受改变外生变量 U。调用方提供的字典会被复制，求值和分布计算不修改原输入。未知键、非法数值以及布尔与整数混用均被拒绝，避免把输入错误悄悄解释为另一个模型。

分布保留四个联合状态，包括概率为零的格子；使用分数而非浮点近似，概率非负且总和为一。手算表与序列化概率逐项对应，九种替换组合没有遗漏或重复。即使两模型的观察分布完全一致，也不能从概率表推出哪条方程应被替换；缺失的是生成规则，而非再增加一次相同类型的计算。若另外提供机制、实验或候选类限制，结论可能改变，但新增信息必须明说。

## 实际重跑与证据边界

[独立审查摘要](../../reproduction/aristotle-posterior-analytics-i13/review/summary.log)记录执行于 **2026-10-25T00:44:11+00:00**，CPython 3.12.14、仅标准库。[普通模式](../../reproduction/aristotle-posterior-analytics-i13/review/rerun-tests-normal.log)、[-O 模式](../../reproduction/aristotle-posterior-analytics-i13/review/rerun-tests-O.log)、[-OO 模式](../../reproduction/aristotle-posterior-analytics-i13/review/rerun-tests-OO.log)各 32 项测试通过，三次新生成模型输出均与公开 JSON 字节一致，SHA256 均为 `c0c1c613e08852c93737c1065a84788b79c26bf2aad61ab3eb18ec2f3bd01d1a`。这验证本次可重跑性，不是性能基准，也不保证未来环境或现实对象满足输入方程。

运行脚本先启用失败即停，分别执行测试和结果生成，再用逐字节比较检查优化模式；只有比较通过才更新最终结果。日志同时保留命令、退出状态、解释器版本与测试摘要，因而不只是一句成功声明。审查也核对了解析后的数值与见证结构，未把字节相同误当作数学正确的充分理由。三模式通过说明本次结果不依赖裸断言或文档字符串继续存在；它不等于覆盖所有异常输入、操作系统和未来解释器。

尚未纳入模型的因素包括真实测量误差、统计抽样、隐变量学习、循环结构与多路径机制。本次未用计算给适切原因打分，也未把月面呈现唯一反推球形、几何面积决定愈合时间等额外桥梁加入模型。正文把这些问题留在各自的证据边界内，与技术通过结论相容。

本报告为 AI 辅助的独立技术审查；独立指核算方法与作者 oracle 分离，不表示机构背书或不可错性。通过结论仅绑定下列版本，文件改变后须重新核验并重绑哈希。

## 版本绑定清单

以下为 19 个受审对象的 SHA256，路径以仓库 `publish` 目录为基准。清单覆盖正文、复现说明、全部作者源码、结果、全部作者日志和独立检查器及日志；不包含本报告自身，避免循环自哈希。

```text
bf4d3d243f8d187b0f8a718c8bd6039feb5b55bc1b32136f054035ea823cac1c  papers/ancient/aristotle-posterior-analytics-i13.zh-CN.md
a053c7d674cb0ea61019eaa20b807ba455000f8b44e4ed82f8dda733bea3b9fa  reproduction/aristotle-posterior-analytics-i13/README.md
dfe9996482e1b42e52293c697db751b543206f2106d7f49ff2354c9579e9773d  reproduction/aristotle-posterior-analytics-i13/model.py
51499daccc9db1d0bcd24b0e4c98e6677e9b1ac0fdb921a2ad2eca8c0444b356  reproduction/aristotle-posterior-analytics-i13/test_model.py
b512d97d921eb6c740ff737e2abc8c1293483eca40d9e617fc2b0f7b3f08551f  reproduction/aristotle-posterior-analytics-i13/run.sh
c0c1c613e08852c93737c1065a84788b79c26bf2aad61ab3eb18ec2f3bd01d1a  reproduction/aristotle-posterior-analytics-i13/results.json
0687c46f00fd8228e3e3e4abab9f608a0764f8125f2f1538f61c738e40deee28  reproduction/aristotle-posterior-analytics-i13/logs/commands.log
c0c1c613e08852c93737c1065a84788b79c26bf2aad61ab3eb18ec2f3bd01d1a  reproduction/aristotle-posterior-analytics-i13/logs/enumeration-O.json
c0c1c613e08852c93737c1065a84788b79c26bf2aad61ab3eb18ec2f3bd01d1a  reproduction/aristotle-posterior-analytics-i13/logs/enumeration-OO.json
c0c1c613e08852c93737c1065a84788b79c26bf2aad61ab3eb18ec2f3bd01d1a  reproduction/aristotle-posterior-analytics-i13/logs/enumeration-normal.json
1d342558b3453c1be00b432e4798e995ec3cfc9b1efa8c7b9c6d8d29673b4cbf  reproduction/aristotle-posterior-analytics-i13/logs/environment.txt
e59f49d6114cd3aa74b052a8ab3234ce1dd98e3315e65d00e502253308c79861  reproduction/aristotle-posterior-analytics-i13/logs/tests-O.log
61d5361733a081f8c409399aee03e5bceef23a079335f105907ec2049a508c5b  reproduction/aristotle-posterior-analytics-i13/logs/tests-OO.log
1fdbaab88b19baad674f0d5fcdfde554993f33e4530f53b7eab898c26db72997  reproduction/aristotle-posterior-analytics-i13/logs/tests-normal.log
703dc0ba4e21cd96ab963f54449a5bef447fff6a6ce45a827031cd4c0be390e8  reproduction/aristotle-posterior-analytics-i13/review/check_independent.py
9e91b43b890b129f788f3d23686938358dac15a8e7b8139bede2000bf421be93  reproduction/aristotle-posterior-analytics-i13/review/rerun-tests-O.log
6ac7f05766cf8d5925b2787b317ab8762264decb758f532b7c0624e8589bffea  reproduction/aristotle-posterior-analytics-i13/review/rerun-tests-OO.log
6ac7f05766cf8d5925b2787b317ab8762264decb758f532b7c0624e8589bffea  reproduction/aristotle-posterior-analytics-i13/review/rerun-tests-normal.log
4f4ffbf29771520fd9008d3e72f41dea74f4e09c8b1a88fdfa03823c03b74c37  reproduction/aristotle-posterior-analytics-i13/review/summary.log
```
