# III.5：公共点、同心与重合 · 精确教学复现

对应[中文深读](../../papers/ancient/euclid-elements-iii5.zh-CN.md)，原文入口[Euclid III.5](https://mathcs.clarku.edu/~djoyce/elements/bookIII/propIII5.html)。原文用半径相等及大小矛盾反证。本目录是现代二维有理坐标与平方距离教学重构，不是古典证明器，不自动求圆交点，不从有限点认证未知圆周。

## 输入与接口

`circle_relation(O1,r1_squared,O2,r2_squared)` 接收两圆心与正半径平方。坐标及半径平方只能是整数、Fraction、规范有理数字符串；拒绝bool、float、非规范字符串及非正半径平方。半径本身可以不是有理数，例如平方半径1/2。

- 同心同平方半径返回 `coincident`，即模型中的同一圆周。
- 同心不同平方半径返回 `concentric-disjoint`。
- 不同圆心仅返回 `different-centers-unresolved`：没有据此断言相交、相切或分离。

`certificate(O1,r1_squared,O2,r2_squared,P)` 额外要求给定点P精确位于两个圆周上。输入不是先假设“互异”，因此重合圆可以作为删掉该条件后的对照进入。输出 `coincident` 或 `distinct-common-point`、圆心距离平方、两个点圆心距离平方及等式两边。一个公共点证书不能区分相交与相切，更不认证“恰有两个交点”。

`verify(c)`重新计算证书并进行严格规范JSON比较。布尔值不能用0/1替换，多余字段、缺字段及未规范输入均不接受。所有业务验证使用显式异常或分支，不用会被优化开关删除的assert。它认证的是此有限输入的算术一致性，不认证圆的实际测量或构造历史。

## 现代恒等式

令中心差Δ=O2−O1，两平方半径为r1²、r2²。由两个等距式相减，得到2P·Δ=|O2|²−|O1|²+r1²−r2²。若Δ=0，则r1²=r2²，于是两个圆周方程完全相同。反过来，互异圆且有公共点便不可能同心。一般推理来自这个代数论证，不来自600次通过。

代码不把“不同圆心”反推为“有公共点”，也不把两个重合圆的名字当作两个不同对象。原命题谈相交的两圆；这里单公共点表达含相切情形的现代扩展，不能据此声称已经完成下一命题的原文研究。

## 五个命名证书与两个关系对照

- crossing_upper/lower：圆心(-3,0)、(3,0)，平方半径均25，公共点(0,4)、(0,-4)。中心距离平方36；线性式两边均0。这两个点分别独立核验，不自动求出。
- external_tangent：中心(0,0)、(2,0)，平方半径均1，P=(1,0)。线性式4=4。
- internal_tangent：中心(0,0)、(3,0)，平方半径25、4，P=(5,0)。线性式30=30。
- coincident：中心均(0,0)，平方半径均25，P=(3,4)。输出重合，同心但不互异。
- relation_only：同心半径平方25/9分离；圆心(0,0)/(5,0)、平方半径1/1虽然事实上分离，接口只返回不同中心而关系待定。

“相切”是给定案例的人工数学说明，不是分类器输出。原创[示意图](figures/common-point-centers.svg)展示交圆、相切、重合；不同面板独立尺度，图片测量不作为证据。

## 真实运行与复查

在本目录执行：

```sh
python3 run_all.py
```

`run-summary.json`记录九条准确命令、真实返回码和日志路径；`environment.json`只含解释器/系统种类而无账户和机器身份。24项单测在normal、-O、-OO全部运行，各含600构形：5证书×5非零尺度×3平移×4旋转×2镜像。负尺度本身是中心缩放，显式单坐标变号才是镜像。600中120个重合、480个互异有公共点；测试不提供统计置信度或一般证明。

日志：`logs/tests-normal.log`、`logs/tests-O.log`、`logs/tests-OO.log`、`logs/examples.json`。源码、测试、算例、SVG生成脚本均为本目录教学代码，不需第三方包。

## Notebook

`create_notebook.py`生成五个小代码格；`verify_notebook.py`在独立进程中按次序compile/exec并捕获stdout。所有execution_count保持null，明确不是Jupyter内核运行，也不声称nbformat完整模式校验或Jupyter界面验收。`--read-only`重复执行并比对保存输出，不写文件。

```sh
python3 verify_notebook.py --read-only
```

`notebook-check.json`及执行/回放日志保存结果。已有Jupyter的读者也可自行顺序运行；本次没有为此安装软件。

练习：把交圆证书的same_center由false改成0，结果如何？答案：拒绝，JSON布尔型不能用数值代替。把同心不等半径的两圆输入certificate并随意选P能通过吗？答案：不能，同一个距离平方不可能同时等于两个不同数。
