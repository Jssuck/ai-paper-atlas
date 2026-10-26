# 欧几里得几何原本 I.2 独立技术审查

本报告审查[正文](euclid-elements-i2.zh-CN.md)的数学推导、[教学代码](../../reproduction/euclid-elements-i2/README.md)、Notebook与运行证据。结论是：**在声明的实欧氏平面解释和规范输入族范围内，未发现使结论失效的数学或实现错误；真实重跑与已保存证据一致。** 独立扩大的是证书检查的测试样本，不是原构造器的接口，也不是古代公设的形式化证明。

审查于2026-10-26完成。正文、原实现和审查代码均为AI辅助工作；这里的“独立”指另行检查与另一套计算路径，不指人类专家签署、外部同行评审或证明助理认证。文献页码、版本与引文归属另见[来源台账](euclid-elements-i2.sources.zh-CN.md)，本报告不替代来源审查。

## 1 一般证明与严格点序

正文使用s=DA=DB>0、r=BC>0，令u=(A−D)/s、v=(B−D)/s。I.1给出相等的辅助边，因此u和v均为单位向量。取G=D+(s+r)v、L=D+(s+r)u，有G−B=rv、L−A=ru，直接得到BG=AL=r及DG=DL=s+r。因为r>0，两个交点严格越过B、A；这与合成证明使用的DG=DB+BG、DL=DA+AL完全相符。

此处没有r<s、r=s或r>s的额外限制，也没有要求A、B、C不共线。程序规范族中的s、r必须是正有理数；正文一般证明允许正实长度。这两层范围不能混同。正文没有把向量计算称为欧氏原始操作，也没有用检查器通过来代替圆交点存在性与动作许可。

`beyond`以非零方向、共线和正点积判断向外点序，是正确的：若目标位移等于原方向的实数倍，共线性给出该倍数，正点积等价于继续向外的倍数严格为正。本次独立核验不用此函数，而用目标在整条直线上的仿射参数严格大于1来判定。

## 2 退化条件与数域边界

- A=B时直接返回C，前提仍是B≠C；这是独立分支，不能把s=0塞入一般公式或I.1。
- A=C而A≠B时，一般构造仍有效；A位于BC内部也不导致失败。原规范构造器没有声称能输入这些任意三点。本次在独立生成的证书中另外覆盖了这些位置。
- B=C的零给定线段被规格排除。`construct`拒绝非正s、r，`coincident_anchor`拒绝零给定线段，正常证书也检查非零BC。
- Q(√3)系数运算、乘法与符号实现符合所声明的代数表示。它不是任意尺规构造的封闭数域，不能接受所有有理坐标三点后保证所需长度或比例仍可表示。
- `certificate`检查输出点满足几何关系，不记录这些点来自哪次允许的尺规操作。它与构造器还共享原精确算术模块，单靠二者相互配合不构成完全独立的实现验证；因此本次引入另外的代数数域oracle。

## 3 手算与反例的逐项复核

正文主例是s=2、r=3，得到DG²=DL²=25、BG²=AL²=9。原演示和Notebook使用s=2、r=1，得到AB²=4、BC²=1、DG²=9、AL²=1。两套参数已在正文区分，不应把一套日志当成另一套手算的实跑。

对于s=2、r=1，把G换成B/2会保留BG²=BC²=1，但破坏D—B—G；此时DG²=1而DA²=4，不可能在A外侧找到第二圆交点。原日志只改G而保留原L，因此它还会正确报告第二圆条件不通过，最终AL²=BC²却仍通过。这恰好说明只检查最终等长会漏掉错误的中间过程。

取第二圆的反向交点也不能只靠圆方程通过：s=2、r=1时L′=(−3,0)给出AL′²=25≠1；正文s=2、r=3时L′=(−5,0)给出AL′²=49≠9。两者都满足第二圆方程，却不满足D—A—L′。独立核验分别记录了这两个例子，没有混用参数。实际布尔值与平方长度见[oracle结果](../../reproduction/euclid-elements-i2/independent-review/oracle-results.json)。

## 4 重跑原始复现

使用CPython 3.12.14重新执行所有25项单元测试，普通、`-O`、`-OO`三种模式分别通过。它们是同一套测试运行三遍，不是75个不同测试。原有限枚举仍为5×5×2×3=150组，违规数0；重新生成的JSON与原件逐值相同。原测试使用unittest，关键断言不会被优化模式删除。

独立日志：[普通](../../reproduction/euclid-elements-i2/independent-review/tests.log)、[优化](../../reproduction/euclid-elements-i2/independent-review/tests-O.log)、[双优化](../../reproduction/euclid-elements-i2/independent-review/tests-OO.log)、[重跑JSON](../../reproduction/euclid-elements-i2/independent-review/results-rerun.json)。原代码无需第三方包，这与独立审查使用已存在的SymPy并不冲突。

Notebook在副本上由原`run_notebook.py`重跑：新Python进程中共享命名空间，五个代码单元按顺序经标准库`exec`执行，计数为1至5，保存内容与原Notebook一致。另检查nbformat版本字段、单元ID唯一性、单元及输出类型、源码结构和执行计数，未发现结构问题。[执行日志](../../reproduction/euclid-elements-i2/independent-review/notebook-exec.log)和[结构检查结果](../../reproduction/euclid-elements-i2/independent-review/notebook-review.json)明确说明范围：**没有Jupyter内核执行，没有完整nbformat JSON-schema验证，也没有Notebook页面渲染。** 不能把这些未进行的检查列为通过项。

## 5 独立oracle与扩大覆盖

[原创审查源码](../../reproduction/euclid-elements-i2/independent-review/independent_oracle.py)使用SymPy 1.14.0的QQ⟨√3⟩代数数域。它只读取原Q3对象的两个有理系数进行适配，不调用原`distance2`、`orientation`、`beyond`、`dot`或`Q3.sign`作为几何oracle。距离和行列式通过另一算术实现重算；点序通过精确仿射参数判断。原Q3运算仅在被测对象的位置执行，并与SymPy结果比较。

| 检查项目 | 实际覆盖 | 结果 |
|---|---:|---|
| 原construct生成的规范族输出 | 294组 | 每项证书条件与独立oracle一致，目标与全长平方正确 |
| 独立生成的更广有效证书 | 1568组 | 所有条件通过，与原certificate一致 |
| 有意破坏的证书 | 216组 | 9类各24组，均拒绝且逐项布尔值一致 |
| Q3加、减、乘与另一实现比较 | 1875次 | 无差异 |
| Q3符号与另一实现比较 | 153次 | 无差异，含128个Pell近抵消用例 |
| A=B直接分支 | 3组 | 返回指定C |

294组令s、r各取1/97、1/3、1/2、1、2、3、97，两种反射及三种有理平移；r/s从1/9409至9409。1568组另取四种精确旋转、两种反射、平移(2+√3,1/3−√3)和四种给定BC方向。这些证书不经原construct生成，其中56组A=C、168组A严格位于BC内部；这两项是1568组内的子集，不能另加到几何样本总数。

故障覆盖第一圆另一交点、第二圆另一侧、G=B、L=A、BC退化、AB退化、错误辅助顶点、正确射线上错误半径，以及偏离射线。它们分别在r<s、r=s、r>s及四种旋转、两种反射下检查，不靠多抄相同测试增加数量。

独立oracle也实际在普通、`-O`、`-OO`下各运行一次，样本计数、反例值及所有判定相同；分别见[普通结果](../../reproduction/euclid-elements-i2/independent-review/oracle-results.json)、[优化结果](../../reproduction/euclid-elements-i2/independent-review/oracle-results-O.json)、[双优化结果](../../reproduction/euclid-elements-i2/independent-review/oracle-results-OO.json)。它使用显式失败收集与非零退出，不依赖裸assert。所有结果的失败列表为空；有限检查仍不是对全部实平面输入的穷尽。

## 6 结论与版本绑定

本次没有发现需要修复的数学或代码缺陷。已核对的关键边界是正长度、严格向外顺序、重合锚点分支、规范族与一般实平面的区别、原实现与独立审查的依赖区别，以及Notebook实际执行方式。代码通过所支持的几何证书检查，不能推广成未建模的动作历史认证、原始公设形式证明或任意三点构造器。

本报告绑定正文SHA-256：

```text
59d9bba18948ff2ac85d001b31dee89e3625d63d052e537a82b6772f93d4b7e3
```

原源码、Notebook与审查证据的散列及命令见[核验清单](../../reproduction/euclid-elements-i2/independent-review/review-manifest.json)。修改正文或实现后，应针对受影响内容重新审查与绑定，不能把本报告自动沿用于新版本。
