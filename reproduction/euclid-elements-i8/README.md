# Euclid I.8：有理坐标中的三边—Gram—等距证书

这是**原创现代教学重构与真实有限实跑**，不是对古代叠合动作的模拟，也不是 Euclid I.8 的一般定理的计算机证明。I.8 原文明确结论是相等边所夹角相等；这里构造整个平面的等距变换，是额外说明其现代数学背景，不能冒充原文结论。

## 原文与对应

- [Euclid, Elements I.8（Clark University, D. E. Joyce）](https://mathcs.clarku.edu/~djoyce/elements/bookI/propI8.html)：叠合底边，再用 I.7 排除同侧不同顶点。
- [I.7](https://mathcs.clarku.edu/~djoyce/elements/bookI/propI7.html)：同底、同侧两点的相关距离唯一性；不是任意两圆在整个平面只有一个交点。

代码中的 `source=(A,B,C)`、`target=(A′,B′,C′)` 固定顶点对应，比较顺序为 `(AB², AC², BC²)`。它不把三条长度排序，也不自动搜索顶点置换。镜像允许，边长一样但指定对应不正确会被拒绝。

## 建模与非循环推导

所有输入坐标仅允许 `int` 或 `fractions.Fraction`，拒绝浮点与布尔值；没有浮点容差。记 `u=B−A`、`v=C−A`，目标向量为 `U,V`。极化恒等式给出：

$$
u\cdot v=\frac{AB^2+AC^2-BC^2}{2}.
$$

因此三条对应边平方相等，保证 `X=[u v]` 与 `Y=[U V]` 的 Gram 矩阵相同，即：

$$
X^{\mathsf T}X=Y^{\mathsf T}Y.
$$

非退化假设 `det(X)≠0` 使 `X` 可逆。显式计算：

$$
M=YX^{-1},\qquad t=A'-MA.
$$

这不是调用“SSS 判定法”，而是直接矩阵乘法。一般代数推导为：

$$
M^{\mathsf T}M=(X^{-1})^{\mathsf T}Y^{\mathsf T}YX^{-1}
=(X^{-1})^{\mathsf T}X^{\mathsf T}XX^{-1}=I.
$$

于是 `p↦Mp+t` 保持任意两点的平方距离，且逐个映射三个顶点。`verify_certificate` 另行核验正交性与逐点映射，不把构造函数的成功作为核验理由。行列式 `+1` 是保向，`−1` 是反向；反射并不破坏通常无向角的相等。

`angle_signature` 返回 `(余弦符号, 余弦平方)`，避免开平方与反三角函数，同时避免仅比较余弦平方会混淆锐角和钝角。对非零两臂，该对数据唯一确定 `[0,π]` 中的无向夹角。它不是有向角信息。

### 边界与 API

- `certificate(source,target)` 返回 `(M,t)`；任一三角形面积为零时抛出 `DegenerateTriangle`，三边指定对应不相等抛出 `CorrespondenceMismatch`。
- 退化被拒是可逆基构造的适用域限制，并非声称退化三点间不存在等距变换。
- `verify_certificate` 仅核验给定正交映射与逐点映射，故可核验退化点组的某个映射；不主张其唯一。
- `gram_from_sides` 只是极化公式，不验证任意三个数是否为可实现的三角形边平方。
- `angle_signature` 对共线但非零两臂仍返回角 0 或 π 的描述；只有零臂无定义。主构造始终要求非退化。
- Python 任意精度整数和 Fraction 避免本实验的舍入误差；此处不研究资源复杂度、超大输入或区间误差传播。

## 运行与文件

无需第三方依赖或安装。从本目录执行：

```sh
python3 run_all.py
```

该命令运行三种优化模式的测试与枚举，并顺序执行 Notebook 的普通 Python 代码格。各个可单独运行的命令为：

```sh
python3 test_geometry.py
python3 -O test_geometry.py
python3 -OO test_geometry.py
python3 run_examples.py
python3 -O run_examples.py
python3 -OO run_examples.py
python3 verify_notebook.py
```

- `geometry.py`：精确几何 API；核心检查使用显式异常，而非会被 `-O` 移除的 `assert`。
- `test_geometry.py`：25 项测试，包含对应、正交证书造假、反射、有理旋转、退化、输入类型、两边不足、锐钝角区别与大整数平移。
- `run_examples.py`：穷举指定**有限**网格中的非退化有序三角形和有序配对。
- `results-normal.json`、`results-O.json`、`results-OO.json`：三模式实际枚举输出，内容一致。
- `logs/`：实际标准输出/错误与退出码；时间耗时由 unittest 自己报告，不是估算。
- `environment.json`、`run-summary.json`：真实运行环境与命令终态；不记录机器账户或私有绝对路径。
- [teaching.zh-CN.ipynb](teaching.zh-CN.ipynb)：5 个代码格的教学 Notebook，含实际输出。
- `verify_notebook.py`、`notebook-check.json`：真实顺序执行方式是标准库 `compile/exec`，**未运行 Jupyter 内核**、未测试 Jupyter 前端；它不支持魔法命令。已装 Notebook 技能已读取，但其声明的模板脚本与参考资源在本执行环境不可用，故使用合法 nbformat 4 JSON 构建，并检查顺序执行。
- `SHA256SUMS.json`：自有交付文件 SHA-256 清单（不含该清单自身、缓存和后续独立审查文件）；重跑会改动日志/时间，须重新生成清单。

## 真实结果与限制

网格为整数坐标 `[-1,1]²`，固定 `A=(0,0)`。共 48 个非退化有序三角形、2304 个有序配对。384 个配对满足指定三边相等并通过显式等距证书；其中 `det(M)=+1` 与 `−1` 各 192 个。1920 个因对应边平方不等被拒绝。三个 Python 优化模式结果一致，25 项单测各全部通过。

这只是完整枚举该有限小网格，而非穷尽所有有理或实数三角形；测试中的判定与构造也共享部分辅助函数，不能当作完全独立的形式化验证。一般论证是上面的代数推导，真实实跑只检查代码与具体边界行为。

## 两边不足与练习答案

取 `A=(0,0), B=(3,0)`，分别令 `C=(0,4)` 与 `C′=(12/5,16/5)`。两臂平方均为 9、16，第三边平方却分别为 25 与 `53/5`。顶角余弦为 0 与 `3/5`，所以相等两边不足以确定夹角。

1. **为何固定对应？** 答：`AB↔A′B′`、`AC↔A′C′` 确定要比较哪个顶角；把三边排序会丢失这个信息，必须另外寻找并声明置换。
2. **能否只比较余弦平方？** 答：不能，锐角 θ 与钝角 π−θ 余弦平方相等，需保留符号。
3. **为何不只搜索旋转？** 答：三边确定的是允许反射的等距类型；镜像实例的证书行列式为 −1。
4. **48 个三角形全部通过是否证明 I.8？** 答：不，有限数据不能推出一般定理，且这是现代坐标模型，不是原文叠合及同侧安排的逻辑形式化。
5. **共线一定没有等距证书吗？** 答：不是；例如相同共线三点的恒等映射就是证书。本构造因 `X` 奇异不适用，拒绝的是算法前提，不是否定这种存在性。
