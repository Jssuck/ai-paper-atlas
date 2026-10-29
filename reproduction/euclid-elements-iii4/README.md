# III.4：相交弦的共同中点 · 精确教学复现

这是标准库有理坐标核验，不是欧几里得证明器，也不是任意曲线求交器。对应[中文深读](../../papers/ancient/euclid-elements-iii4.zh-CN.md)。原文参见[Euclid III.4](https://mathcs.clarku.edu/~djoyce/elements/bookIII/propIII4.html)。原文用III.3的两次垂直结论反证；下面的点积、行列式和JSON证书是现代教学重构。

## 输入、输出与边界

`certificate(O,r2,A,C,B,D)`接收圆心、正半径平方及同圆周的两组弦端点，所有坐标仅为整数、Fraction或规范有理数字符串。拒绝float和bool、零弦、非同圆、平行/重合支持线、非严格内部交点。用两直线的行列式公式计算交点E与参数t、u。因此实现的是非平行有理直线的交点，不声称一般圆线求交。

输出包括两条弦的中点布尔值、直径布尔值、原命题适用性和两条现代残差。`theorem_applies`只在两条均非直径时为真。`both_midpoints`是两个中点条件的合取；不能同时为真，不表示两个条件都必须为假。直径例允许进入扩展模型，用来解释原命题范围，而非偷偷扩大原文规格。

设v=C−A，w=D−B，E=A+t v=B+u w。同圆周等距展开给出(E−O)·v=(t−1/2)|v|²，另一个方向同理。两条残差皆零且方向行列式非零，在平面上迫使E=O。这个一般结论需要线性代数论证，600个样本不替代它；它也不代表验证了古典几何公设或原证中的角序。

`verify`重新计算证书，用严格规范JSON比较，能区分布尔量与0/1；它不认证输入圆的来源、不从有限点集合推断未知圆周。代码只处理二维正半径、互异端点及非平行相交弦，切线、三维、数值误差估计等不在范围内。

## 五个算例

- `neither_midpoint`：半径5，水平弦(-4,3)到(4,3)与竖直弦(3,4)到(3,-4)，E=(3,3)，t=7/8、u=1/8，两者都不被平分。
- `only_AC_midpoint`：水平弦保持，另一弦(3,4)到(-24/5,7/5)，E=(0,3)，t=1/2、u=5/13。两弦均非直径，但AC被平分；EB²=10、ED²=128/5。
- `only_BD_midpoint`：互换上例两弦的输入位置。
- `one_diameter`：水平弦与竖直直径相交于(0,3)，仅水平弦被平分。原命题两条非直径的规格不适用，但没有出现双中点。
- `two_diameters`：两条直径相交于圆心，确实互相平分。它是删除非直径条件后的反例。

原创图：[相交弦](figures/intersecting-chords.svg)。它是上述精确案例的数值显示，不通过测量图像来证定理。

## 实跑与重建

在本目录执行：

```sh
python3 run_all.py
```

`run-summary.json`记录九条准确命令、真实返回码和日志路径；`environment.json`记录不含机器身份的环境。核心测试24项，在normal、-O、-OO三模式全部通过。每模式检查600个变换构形：5基础例×5非零尺度×3平移×4旋转×2镜像。负尺度本身是中心缩放而非反射；反射由单坐标变号另行实现。600中原命题范围360个、双中点120个（均为两直径）。这是有限测试计数，不是随机统计置信度。

日志位于`logs/tests-normal.log`、`logs/tests-O.log`、`logs/tests-OO.log`、`logs/examples.json`，包含输入验证、预期参数、中点真假、证书修改及类型混淆测试。`geometry.py`不使用会被优化开关去掉的assert执行验证。缓存不属于发布物。

## Notebook

`create_notebook.py`生成五个小代码格的`teaching.zh-CN.ipynb`。`verify_notebook.py`使用标准库在一个新进程内顺序compile/exec代码格，捕获真实stdout；所有execution_count保留null，明确不是Jupyter内核执行。`--read-only`会重新执行并比较保存的输出，不改文件。`notebook-check.json`和两份日志保存核验结果。没有安装任何包；没有声称nbformat完整模式校验或Jupyter界面验证。

```sh
python3 verify_notebook.py --read-only
```

读者如已有Jupyter，可自行从头运行全部格；核心代码不依赖它。运行与保存输出不同不是定理失败，需要先检查解释器、文件和运行目录。

## 文件分工与练习

`geometry.py`定义精确模型；`test_geometry.py`测试；`run_examples.py`生成算例；`draw_figure.py`画原创SVG；`run_all.py`组织真实运行。不要把`theorem_applies=False`解释成命题被反驳，它表示不在原命题输入范围。

练习：给单平分例的证书把`midpoint_BD`改成true，验证器会接受吗？答案：不会，重新计算得到u=5/13，不等于1/2。若把`theorem_applies`从true改为1，同样拒绝；Python中True==1的宽松比较不适合作为证书类型规则。
