# III.6：有理相切证书最小复现

这是原创现代教学模型，不是 Euclid 原文的算法，也不是完整尺规系统、任意圆线求交器或古典证明检查器。输入是两个已知圆心和**正的有理半径**；不是只给一个公共点。只有两圆外切或内切时才生成接触证书。相交、外离、严格内含、同心不同半径与完全重合均明确区分，后五类不产生相切证书。

## 数学接口与一般推导

设圆心为 O1、O2，半径 r1、r2，n=O2−O1，d²=n·n。程序以精确平方比较判断：d²=(r1+r2)² 是外切；d²=(r1−r2)² 且 d²>0 是内切。d²=0 单独先处理，避免把等圆误认成内切。程序不用浮点容差，拒绝 bool、float、零或负半径。

外切点 T=O1+[r1/(r1+r2)]n；内切点 T=O1+[r1/(r1−r2)]n。后式允许 r1<r2，交换次序后仍给同一点。所有运算是 Fraction 精确算术。

为什么这不只得到一个公共点？任意公共点 X 满足两圆平方距离方程，相减得 n·X=k，其中 k=(|O2|²−|O1|²+r1²−r2²)/2。上述 T 同时满足两个圆方程，且 T−O1 平行 n。因而 n·(X−T)=0，展开平方得到 |X−O1|²=|T−O1|²+|X−T|²；前两项都是 r1²，所以 |X−T|²=0，X=T。这是现代欧氏坐标的一般推导，不是有限枚举证明；它依赖正定平方范数与所给圆方程。相切条件使 n非零，所以两圆不同心。它不是原文“较小等于较大”的反证。

`relation(o1,r1,o2,r2)` 返回七种关系之一。`certificate(...)` 仅接收内外切对，返回归一化有理字符串、接触点、两半径平方、根轴法向量/偏置及类型字段。`verify(c)` 从证书输入重算并按完整JSON精确比较，拒绝缺键、额外键、改动和 bool/int 混淆；它不是独立数学证明引擎。`unique_contact` 依赖上述推导和实现，不是扫描全部平面点所得。

## 复跑

Python 3 标准库，无下载、网络或第三方依赖。在本目录执行：

```sh
python3 run_all.py
```

该命令逐项运行并保存退出码：Python版本，24单测的 normal/-O/-OO 三模式，5命名证书及3关系对照，Notebook创建、顺序执行、只读回放，SVG生成。完整命令及真实返回码见 [run-summary.json](run-summary.json)，环境见 [environment.json](environment.json)。失败即中止，不使用可能被优化关闭的 `assert` 来承担输入验证。

- [源码](geometry.py) / [测试](test_geometry.py)
- [普通测试日志](logs/tests-normal.log) / [-O](logs/tests-O.log) / [-OO](logs/tests-OO.log)
- [实际算例输出](logs/examples.json)
- [Notebook](teaching.zh-CN.ipynb) / [执行日志](logs/notebook-execute.log) / [只读回放](logs/notebook-replay.log)
- [原创图](figures/tangency.svg)

每种模式的网格是5命名构形×5横移×3纵移×4正缩放×2镜像=600，不是600个本质不同定理。正缩放不冒称镜像；镜像只反转纵坐标。其他测试覆盖退化与证书篡改。输入仅有理中心/半径，虽然很多构形可精确表示，却不涵盖所有实数圆。

Notebook为五个代码单元，保存的stdout通过标准库compile/exec真实生成并逐格重放比对；不是Jupyter kernel执行，execution_count为null。创建脚本使用公开标准nbformat结构，不依赖外部模板路径。SVG两图比例独立，只用于教学，不来自原典，不证明一般命题。
