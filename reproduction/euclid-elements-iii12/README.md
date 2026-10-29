# Euclid《几何原本》III.12：外切与严格介于的精确实验

[中文深读](../../papers/ancient/euclid-elements-iii12.zh-CN.md) · [教学 Notebook](teaching.zh-CN.ipynb) · [原创示意图](diagram.svg)

## 模型和证据职责

这是现代二维欧氏有理坐标教学实验，不是古典证明器。原命题见 [III.12 原文读本](https://mathcs.clarku.edu/~djoyce/elements/bookIII/propIII12.html)。原证使用 I.20 反证；本程序不模拟古典图形公理，而核对正文所解释的现代外切模型。

`Circle` 只接收整数与 `Fraction` 坐标、严格正半径。`verify_contact(a,b,t)` 先检查两个前提：两开圆盘不交、独立输入的 t 同时位于两圆周。不先要求两圆心距等于半径和，不先要求共线或介于。再分别核对距离平方等式、叉积为零、投影严格处于 0 与圆心距平方之间。任一结论失败均显式抛出异常，不靠可被 `-O` 移除的裸 assert。

**重要建模边界：**`interiors_disjoint` 把内域不交实现为 d²≥(R+r)²。这里 R+r>0，故平方保持不等号。该判据与圆盘内域不交的等价性必须在正文中由几何论证建立，程序并未遍历所有盘内点来证明它。公共圆周点给出另一方向的三角不等式，进而得到等号；这是一般数学证明的任务，而不是执行布尔判断就获得的证明。

`contact_candidate` 是独立构造接口：确认外切分类后返回 F+R(G−F)/(R+r)。不把这个构造自产的点当唯一测试证据；网格另外由有理单位方向直接提供接点，并交换两个圆的次序。`relation` 使用精确平方距离区分重合、同心不同半径、严格内含、内切、两交点、外切、外离。`concentric_disjoint` 指同心不同圆的**圆周**不交，绝不指圆盘内域不交。

## 运行与真实日志

进入本目录后执行：

```sh
python run_all.py
```

只用 Python 标准库，不联网、不装包。具体版本见 [environment.json](environment.json)。编排执行并记录实际 stdout、stderr、返回码：

```sh
python -m unittest -v test_geometry
python -O -m unittest -v test_geometry
python -OO -m unittest -v test_geometry
python run_examples.py
python create_notebook.py
python verify_notebook.py
```

- 30 个单元测试分别在普通、`-O`、`-OO` 三模式通过。
- 每模式 960 个精确外切构形：4 平移 × 6 有理单位方向 × 4 第一半径 × 10 第二半径；每个构形在两种圆序下核验，共 1920 份前提/结论证书。方向有坐标轴、反射和非轴向 3/5–4/5、−5/13–12/13。相同确定性网格重复三模式不是新增独立样本。
- 4 个命名合法例：水平、平移旋转、等半径竖直、反射。3 个拒绝对照：非共线公共点的相交圆、共线内切、外离圆。内切即使共线也不满足内域分离，说明“共线”不是外切定义。
- 覆盖零/负/浮点/布尔半径、浮点坐标、坏维度、错误圆周点，及 `10^-50` 量级间隙与重叠。精确有理运算不使用浮点容差；没有承诺浮点输入的鲁棒几何。
- Notebook 五代码格按顺序真正 `compile/exec` 并保存输出，再用只读回放脚本执行比对。**不是 Jupyter kernel 运行。** 已读安装技能，但规定的 helper 路径不存在，技能资源读取失败，故本地 nbformat4 scaffold；没有安装替代软件。

[运行摘要](run-summary.json) · [普通](logs/tests.log) · [一级优化](logs/tests-O.log) · [二级优化](logs/tests-OO.log) · [算例](logs/examples.log) · [Notebook 执行](logs/notebook.log) · [Notebook 回放](logs/notebook-replay.log)

## 限制与源码

有限有理例不证明任意实数圆的定理，不自动核验古典“接触”定义的拓扑含义，不计算任意两圆的无理交点，也不验证圆盘分离判据的一般正确性。原创图左是实际外切构形，右是实际内切对照；两者均不是原证的反事实图。

[模型](geometry.py) · [单测](test_geometry.py) · [算例](run_examples.py) · [编排](run_all.py) · [Notebook 构建执行](create_notebook.py) · [只读回放](verify_notebook.py)

[独立来源审查](source-review.zh-CN.md) · [独立技术审查](technical-review.zh-CN.md)。独立审查的额外统计及最终绑定哈希以各审查记录为准。
