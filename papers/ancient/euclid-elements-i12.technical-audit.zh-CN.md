# Euclid I.12：独立数学与代码审查

结论：**通过本次声明范围的独立技术核验，无阻断问题。**

正文绑定 SHA-256：`94e02dc661e043a31ec96adbc21b0b8d655667380a9887de7be906fee91ef600`。正文修改后需重新核对或重新绑定；本报告不是证明助理认证，也不是对任意软件环境的保证。

## 1 一般数学论证

已逐项检查正文第4–7节及练习中的等量、对应、非退化条件和现代推论。

- 原证明的对应为C↔C、H↔H、G↔E；半径、半弦、公共边支持I.8，而非预设直角后使用斜边直角边判定。H严格居中保证相反射线，再依定义10；不需偷用后续I.13。
- v=B−A，q=v·v>0，p=(C−A)·v。展开圆线条件得二次方程；完成平方中的k=|C−A|²−p²/q与δ=(r²−k)/q一致。
- 单位方向分解中cd<0严格推出r²−k=s²+d²−2dc>0。正文明确这只是现代欧氏坐标分析，并非古代构造的免费前置垂线操作。
- 两根平均消去根号，H=A+(p/q)v；点积为零。垂足唯一、最多两交点与最近点分别有另外论证，未冒称原文已逐项证明。
- 同侧、线上D既可失败也可成功的例子算术正确；异侧只是本算法充分性契约。无限直线与有限线段目标分开。

这些一般论证经人工式逐步审读；下面的有限代码运行不承担它们的普遍量词。

## 2 程序与表示核对

读取 `geometry.py`、`cases.py`、`test_geometry.py`、运行器、Notebook及说明。核心程序未由审查者修改。

- 分数与单二次扩域运算、平方根完全平方归约、精确符号比较及除法共轭公式一致。只在同一非平方根底数内运算；跨表示等价不被自动识别，正文与README已明示。
- 构造器接收有理点，先检查A≠B、C线外、D严格异侧，才作除法。所得δ为有理且正，当前单一扩域足够表达交点；这不覆盖任意实数或一般代数数表达树。
- 核验器没有通过重新调用构造器并比较其输出来认证证书；它检查圆心/半径与输入绑定、两点在线及指定圆上、相异、中点/介于、半弦相等、非零和非退化、现代垂直点积。构造器与检查器共用输入参数代码，因此另做独立Fraction投影检查降低共享错误风险，未声称完全无共享依赖。
- 正确垂足不等于指定圆构造记录正确；伪造圆心、半径、交点或移植输入必须被拒绝。交换E/G标签不应拒绝。
- 直接解交点和取算术中点是现代重构，不是I.10尺规操作历史重演。精确输出不是图形测量、也不是公理系统完整形式化。

## 3 真实独立执行

命令、UTC时间与退出码：[run.json](../../reproduction/euclid-elements-i12/independent-review/run.json)。所有四条独立命令真实退出0。

| 检查 | 结果与范围 |
|---|---|
| `python test_geometry.py` | 28测试通过 |
| `python -O test_geometry.py` | 28测试通过 |
| `python -OO test_geometry.py` | 28测试通过 |
| 三模式测试内有限证书族 | 每模式648正证书、16负证书；不是额外三倍独立输入域 |
| 独立算术 | 504配对，检查乘法、除法及相应符号判断 |
| 独立几何 | 96个包含分数方向/原点的输入，另算有理投影与圆半径，再核对交点方程 |
| 独立篡改 | 上述每例改动圆心/E/G/H，合计384项拒绝 |
| Notebook重放 | 6代码格以标准库compile/exec独立执行，与已存stream输出逐字匹配 |

源码：[checks.py](../../reproduction/euclid-elements-i12/independent-review/checks.py)；日志：[checks.log](../../reproduction/euclid-elements-i12/independent-review/checks.log)、[普通](../../reproduction/euclid-elements-i12/independent-review/tests-normal.log)、[-O](../../reproduction/euclid-elements-i12/independent-review/tests-O.log)、[-OO](../../reproduction/euclid-elements-i12/independent-review/tests-OO.log)。Notebook未使用Jupyter kernel，未检查Notebook网页渲染。这里重放不修改提交的Notebook。

核对主运行记录确有8条命令退出0，三模式结果一致；正文统计与文件相符。有限枚举不能证明所有输入均无软件缺陷，更不能证明古代所有语义或连续性公理。

## 4 绑定与剩余边界

- geometry.py SHA-256：`0ca16d546a2cf8ad553c82b28b0a0913e66be7f5c6939a990a2d2b198d8e5e0f`
- test_geometry.py SHA-256：`7372151cbca4f258961fd8bdf378ce647abf0183da018da2513fef4b6fffc7e8`
- Notebook SHA-256：`40e35128241636a3bee3abf0b51f248d44afd43f9aba9218e39f17c3e6613a2e`

本技术审查不替代独立来源审查，也不预先认证GitHub远端内容与公式实际显示。后两项由发布阶段另核。审查日期：2026年10月27日。
