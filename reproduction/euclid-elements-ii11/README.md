# Euclid II.11：精确代数域中的构造证书

这是原创教学重构，不是古代作图过程的机械复刻，也不是一般定理的机器证明。原命题与证明见 [Joyce II.11](https://mathcs.clarku.edu/~djoyce/elements/bookII/propII11.html)，详细来源比较见本目录独立来源审查及[中文深读](../../papers/ancient/euclid-elements-ii11.zh-CN.md)。

## 模型和单位

本地坐标取 A=(0,0)、B=(a,0)、C=(0,a)、D=(a,a)、E=(0,a/2)，a 为严格正有理数。令 x=a(√5−1)/2，取 F=(0,−x)、G=(x,−x)、H=(x,0)、K=(x,a)。这是根据几何构造导出的坐标模型，不是拿最终面积恒等式当筛选输入的条件。EF²=EB² 检查半径搬移，0<x<a 检查截点确实在内部；负根不能冒充另一合法截点。

支持有理原点及任意有理正交、等长、非零基 u、v，包括旋转、反射、统一缩放。坐标经过 origin + local_x*u + local_y*v 变换。scale2=dot(u,u)。x 是本地坐标系数；物理长度 AH=x*sqrt(scale2)，不是在所有基下都等于 x。所有面积与平方距离乘 scale2。基不等长或不正交，已不是这套正方形模型，显式拒绝。

## 精确计算与接口

- `Q5(p,q)` 表示 p+q√5，系数为 `fractions.Fraction`；四则、非负整数幂与符号比较全为精确有理操作。异号相加的符号由 p² 与 5q² 比较，不调用浮点 sqrt。非零有理数不可能平方等于5倍另一非零有理数平方，因此表示唯一。
- `make_certificate(a, origin=(0,0), u=(1,0), v=(0,1))` 返回含 a、origin、u、v、points 的字典。a/原点/基只接受 int 或 Fraction，拒绝 bool、float、字符串。
- `points` 包含 A/B/C/D/E/F/G/H/K，每坐标分量必须为 Q5。外部检查器可以自行构造字典，不必调用构造器。
- `validate_certificate(c)` 返回 metrics，并以显式 ValueError 拒绝非法参数、缺失/额外字段、错误点或不满足的几何关系。优化模式不会移除生产校验。
- Q5 与 Q5 作精确相等比较；请写 `Q5(0)` 而不是整数0来比较相等。大小比较接受有理数。

生产验证器用规范点复算检查构造身份，再用鞋带公式独立计算 FK、AK、FH、HD 的区域面积，并显式核对 II.6、I.47、共同面积相减及结论。规范点复算与构造器共享定义，不能宣称二者独立：根式 x=a(√5−1)/2 已预先给定，因此这是固定解析构型的精确回归检查，不是只由欧氏局部约束独立求根的通用证书验证器。外部技术检查可从不同公式生成外证书并校验，但也不改变生产验证器这一范围。面积鞋带公式也是现代教学工具，不替代原论证的等积原则。

区域：FK 对应 F-G-K-C 整矩形，AD 对应 A-B-D-C 整平方；共同 AK 为 A-H-K-C，剩余分别是 F-G-H-A 的小平方和 H-B-D-K 的右矩形。图中蓝色与橙色等积，灰色是同减部分。SVG 的屏幕坐标使用浮点近似以显示图形；算法与全部证明关系检查不使用浮点。

## 运行

在本目录运行（Python 3，只有标准库，无安装步骤）：

```sh
python run_all.py
```

该命令实际运行以下七步，任一步非零立即失败。每个日志含原命令和退出码：

```sh
python -m unittest test_geometry -v
python -O -m unittest test_geometry -v
python -OO -m unittest test_geometry -v
python run_examples.py
python create_notebook.py
python verify_notebook.py
python draw_figure.py
```

环境记录见 [environment.json](environment.json)，命令与执行时间见 [run-summary.json](run-summary.json)。20个单测各在 normal/-O/-OO 下通过；其中网格项含64个正有理规模，另测反射、平移、尺度、域运算、符号、非法参数、错误点、负根。四算例覆盖单位、分数、旋转缩放、反射。a=1且单位基时 FK=1，AK=(√5−1)/2，FH=HD=(3−√5)/2。

[Notebook](teaching.zh-CN.ipynb) 的五个代码格实际通过标准库 compile/exec 顺序执行，并在新命名空间回放比较输出。这**不是 Jupyter kernel 执行**；未声称启动 kernel。execution_count 记录此次教学执行顺序。可在自己的 Jupyter 环境重新运行。 [notebook-check.json](notebook-check.json) 保存回放结果。

## 证据和边界

[普通测试](logs/tests-normal.log)、[-O测试](logs/tests-O.log)、[-OO测试](logs/tests-OO.log)、[四算例](logs/examples.log)、[Notebook执行](logs/notebook-execute.log)、[回放](logs/notebook-replay.log)、[图形生成](logs/figure.log) 均是本次真实运行的文本。时间耗时仅记录执行，不是性能基准。

输入仅覆盖正有理a及有理正交等长基，构造结果允许Q(√5)坐标；不能称覆盖所有实数线段、全部尺规程序或全部可能坐标系。有限样本及篡改拒绝不能证明一般命题、验证器完备性或形式化正确性。本文的几何证明负责一般性，程序用于揭示对象身份、边界和面积关系。

## 独立审查

[来源审查](source-review.zh-CN.md)与[技术审查](technical-review.zh-CN.md)绑定正文最终SHA256。[独立检查脚本](independent_check.py)可在本目录用 `python independent_check.py` 重跑，[真实日志](logs/independent-technical.log)保存此次执行；其手工坐标、符号对照与有限覆盖不改变上述固定构型范围。
