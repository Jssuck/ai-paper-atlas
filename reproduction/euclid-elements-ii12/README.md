# II.12：钝角三角形外投影的精确有理教学模型

这是原创的现代坐标教学重构，不是古代算法的逐指令仿真，也不是通用定理证明器。原文参照 [Fitzpatrick 的 Heiberg 希腊文／英译本](https://farside.ph.utexas.edu/Books/Euclid/Elements.pdf)，印刷页 64–65，II.12。原文先调用 II.4，再对两个直角三角形应用 I.47；程序分别保存这三个等式的检查结果。没有复制原文全文或原版插图。

## 命令与文件

在本目录执行：

```sh
python run_all.py
```

只用 Python 标准库，无需安装第三方依赖。具体解释器版本见 [environment.json](environment.json)，执行 UTC 时间与完整命令见 [run-summary.json](run-summary.json)。

- [geometry.py](geometry.py)：精确 `Fraction` 坐标、外垂足、平方长度、校正面积。
- [test_geometry.py](test_geometry.py)：20 项单元测试，分别在正常、`-O`、`-OO` 模式执行。
- [run_examples.py](run_examples.py)：5 个可复核算例。
- [teaching.zh-CN.ipynb](teaching.zh-CN.ipynb)：5 个代码单元，按顺序以 Python `compile/exec` 在同一命名空间执行；**没有启动 Jupyter kernel**。
- [create_notebook.py](create_notebook.py) / [verify_notebook.py](verify_notebook.py)：生成并执行 Notebook、在新命名空间重跑并逐字比对输出。安装技能的默认 scaffold 脚本在本机不存在，故使用自有标准格式生成器；未安装额外工具。
- [notebook-check.json](notebook-check.json)：独立重放的输出一致性记录。
- [draw_figure.py](draw_figure.py) / [原创 SVG](figures/ii12-external-projection.svg)：固定算例图，示意而非测量证明。
- 真实日志：[normal](logs/tests-normal.log)、[-O](logs/tests-O.log)、[-OO](logs/tests-OO.log)、[算例](logs/examples.log)、[Notebook 执行](logs/notebook-execute.log)、[Notebook 重放](logs/notebook-replay.log)、[制图](logs/figure.log)。

## 模型、假设与范围

`construct(A,B,C)` 接受三个二元点，每个坐标必须为整数或 `Fraction`；明确拒绝浮点数、布尔值、字符串和形状错误。要求 A 与 C 不重合、三点不共线、角 BAC 严格为钝角。令 u=C−A、v=B−A，垂足 D=A+t u，其中 t=(u·v)/(u·u)。钝角要求 u·v<0，因此 t<0，D 位于从 A 背离 C 的延长线上。

程序计算矩形面积 AC×AD=−u·v，故即使 AC 或 AD 的长度无理，也无需计算根号或采用浮点容差。返回 `AC_times_AD` 与 `correction=2*AC_times_AD`，以及两个勾股等式、II.4 展开式和 II.12 最终等式。这里的点积是现代分析解释，不是声称欧几里得用了向量。

`normalized(c,d,h)` 是方便入口：A=(0,0)、C=(c,0)、B=(−d,h)，要求 c>0、d>0、h≠0。h 可负，允许基线下方的镜像。它只是同一构形的坐标标准化，并不限制一般主 API 的方向。

## 实际检查结果

20 项测试包括：250 个不同的有理参数组合、平移、3/5 与 4/5 构成的精确旋转、镜像、放缩、无理边长但有理乘积、极小正校正、大整数、错误减号与漏二倍反例，以及锐角、直角、退化和不合法输入的拒绝。250 个组合是在一个测试中枚举，不虚报为 250 项独立单元测试；三种解释器优化模式也不是三个独立数学证明。

- c=5,d=2,h=3：AB²=13，AC²=25，BC²=58，校正=20。
- c=3/2,d=1/3,h=4/5：AB²=169/225，AC²=9/4，BC²=3601/900，校正=1。
- c=5,d=2,h=−3：同一平方结果，检验镜像不改变等式。
- c=1,d=1/1000,h=1：校正=1/500，仍严格为正。
- A=(0,0),B=(−2,0),C=(1,1)：AC²=AD²=2，但 AC×AD=2 精确有理。

这些有限样本验证实现与选定输入，不证明一般定理；一般论证应阅读[正文](../../papers/ancient/euclid-elements-ii12.zh-CN.md)。程序没有构造任意实数、符号实闭域或自动搜索证明。严格拒绝的边界并不表示相应现代多项式恒等式为假，只表示它不属于本命题的非退化钝角输入范围。

## 独立核验

[独立脚本](independent_check.py)与[真实技术日志](logs/independent-technical.log)以平方边长及鞋带面积作另一实现路径，记录每种模式的2401点对、216变换、69非法类型及手算/近直角核验。结论范围见[技术审查](technical-review.zh-CN.md)；原典及历史层次见[来源审查](source-review.zh-CN.md)。双审均绑定正文最终SHA256，不等同于人类专家或证明助理认证。
