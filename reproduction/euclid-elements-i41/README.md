# I.41 最小复现：同底平行带中的二倍面积

这是原创 Python 标准库 `Fraction` 有理坐标教学模型。原证用 I.37 比较 ABC 与 EBC，再用 I.34 的对角线二分平行四边形。本程序以现代行列式检查具体实例，不是 Euclid 公理系统的形式化，不以有限试验替代一般证明。

## 输入与字母

五点 A、B、C、D、E，平行四边形边界顺序 **A–B–C–D**，共同底边 BC，对边 AD。程序要求 BC 非零、A 不在 BC 支持线上、D=A+(C−B)，E 在 AD 的整条支持线上。允许 E 在 AD 内、外或与 A、D 重合。E=A 时 AE 两点线名没有意义，但 AD 支持线仍有定义；不能因此误拒绝非退化三角形 EBC。

点必须是二元素 list，坐标只接受严格整数或规范有理数字符串，例如 `"1/2"`。拒绝 bool、float、NaN、无穷、非规范 `"2/4"`、错误键和点形状。整数与等值规范整数字符串归一化；绑定的是规范化几何，不是原始字节签名。

`make_certificate` 先验证全部几何前提，之后给出 ABC、ACD、EBC 与四边形 ABCD 的**二倍面积**。表中 ABCD=24、EBC=12，实际面积分别12与6，比例仍为2。证书同时给出原证依赖链标签，但这些标签不等于机器推导已证明 I.34 或 I.37。

## 文件与复跑

- [geometry.py](geometry.py)：精确输入、几何前提、面积、绑定证书与重算验证。
- [cases.py](cases.py)、[test_geometry.py](test_geometry.py)：固定例、参数族和22项单元测试。
- [run_examples.py](run_examples.py)、[results.json](results.json)：180个合法有理实例、10个非法输入直接拒绝。
- [Notebook](teaching.zh-CN.ipynb)、[构建器](create_notebook.py)、[回放器](verify_notebook.py)、[回放结果](notebook-check.json)：5代码格，实际标准库 compile/exec 和全新命名空间 stdout 对比，**不是 Jupyter kernel**。
- [environment.json](environment.json)、[run-summary.json](run-summary.json)：环境、真实命令、退出码与时间。
- [普通模式日志](logs/tests.log)、[-O日志](logs/tests-O.log)、[-OO日志](logs/tests-OO.log)、[示例](logs/examples.log)、[Notebook构建](logs/notebook-build.log)、[Notebook回放](logs/notebook-replay.log)。
- [原创位置示意](figures/positions.svg)：AD内、外和E=A边界，均属于原命题支持线条件，不是原书图复制。

在本目录执行：

```sh
python run_all.py
```

已用环境文件记录的CPython执行22项单测，各在普通、`-O`、`-OO`下通过。核心校验不依赖assert。180例含三种底方向、四种有向高度、三种剪切以及五个顶点参数：E=A36、E=D36、AD内36、AD外72。10项非法输入包含零底、退化、错误第四顶点、离开上支持线、相反高度、底线上顶点、错误标号及三种类型错误。参数族和测试不是互不重叠样本，不能把测试次数相加当独立几何实例数。

已读安装的Notebook技能；其默认路径的脚手架脚本不存在，因此没有安装依赖，使用原创标准库构建器。Notebook含真实输出，但未声称启动kernel或做过Jupyter界面渲染。

## 反例与证书边界

在B=(0,0)、C=(4,0)、A=(1,3)、D=(5,3)下，取E=(3,4)使三角形面积8、平行四边形面积12，二倍关系失效。取E=(3,-3)时面积比恰仍为2，但E不在AD支持线上，必须拒绝：结论偶然成立不替代前提。这是“去掉同带未必还能推出”的反例与“偶然成立仍非合法输入”的区分。

验证器仅收JSON string/list/object树，拒绝数字、布尔替换、循环、额外字段、篡改面积或依赖标签，并根据输入重算整个证书。同面积换顶点仍不能移绑证书。不过生成器与验证器共享计算函数，不构成独立数学证明核；独立技术审查另行检查其共同缺陷。程序仅实现同一底边BC的原命题，不暗中声称等长但不同底边推广已被实现。没有训练数据、学习基线或速度指标；主要复现条件是输入契约、精确算术和上述命令。
