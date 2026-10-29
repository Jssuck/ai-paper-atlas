# III.13：内外切接点唯一性的精确教学实验

[中文深读](../../papers/ancient/euclid-elements-iii13.zh-CN.md) · [Notebook](teaching.zh-CN.ipynb) · [原创图](diagram.svg)

## 规格：不把唯一性藏进定义

这是现代二维欧氏有理坐标模型，不是古典证明器。[III.13读本](https://mathcs.clarku.edu/~djoyce/elements/bookIII/propIII13.html)分别处理内切与外切。本模型不把“恰有一个交点”定义为相切，再循环证明唯一性。

`contact_certificate(a,b,t,kind)`接收两个正半径圆和独立提供的共有圆周点t。外侧前提是开圆盘内部不交；内侧前提是真包含，排除重合圆。程序用平方距离实现分离/包含判据：外侧d²≥(R+r)²；内侧R≥r且d²≤(R−r)²。**这些有限代数判断与全体圆盘点的几何关系等价，是正文一般数学证明的责任，不是程序已经枚举所有点证明。** 给定公共点再强制等号及方向，得出唯一坐标公式。公式由程序检查，不能代替证明。

`same_contact`对两个给定点各自检查前提和候选公式，然后比较。网格的相同点两次输入只是回归测试，不证明不存在不同点；一般唯一性由正文给出。网格接点从外部有理单位方向构造，不是先调用候选公式再拿结果自证。

`chord_midpoint_certificate`接收两个不同的公共圆周点，核查中点平方余量恰为弦长平方的四分之一，严格正。这直接说明两交点与外侧内部不交不相容。**中点在两个盘内本身不否定内含**，内切唯一性仍需正文的等号方向论证。重合圆也满足弦中点恒等式，却不满足真包含的接触规格。

`relation`区分重合、同心不同、严格内含、内切、两交点、外切、外离。它分类圆周关系，不把同心不同圆的无公共圆周点混成圆盘不交。仅接收int与Fraction，拒绝bool、float、零/负半径和坏维度；不作浮点容差判断。

## 真实运行

进入本目录：

```sh
python run_all.py
```

编排命令（只用标准库，不联网、不安装）：

```sh
python -m unittest -v test_geometry
python -O -m unittest -v test_geometry
python -OO -m unittest -v test_geometry
python run_examples.py
python create_notebook.py
python verify_notebook.py
```

- 28单测分别在普通、-O、-OO三模式真实通过。结论与输入检查使用显式异常，不靠优化后消失的裸assert。
- 每模式432内/外切构形：3平移×6有理单位方向×4小半径×3半径差×2接触类型；两种圆序共864证书。三模式重复同一确定性网格，不算新增独立样本。
- 三个命名接触例（外切、内切、竖直外切），一个两交点弦中点例，三个拒绝例（相交圆当外切、当内切、重合圆当内切）。覆盖10^-50量级间隙及重叠、坏输入、错误见证与弦端点。
- Notebook五代码格真实顺序compile/exec并保存输出，再只读回放比较stdout。**不是Jupyter kernel运行。** 已读已安装技能，规定helper文件不存在且技能资源读取失败，故使用本地nbformat4 scaffold；未安装替代软件。

[运行摘要](run-summary.json) · [环境](environment.json) · [普通日志](logs/tests.log) · [优化一](logs/tests-O.log) · [优化二](logs/tests-OO.log) · [算例](logs/examples.log) · [Notebook执行](logs/notebook.log) · [只读回放](logs/notebook-replay.log)

## 限制与源文件

有限有理样例不能证明任意实数定理。程序不重建古代相接定义的全部拓扑内容，不求任意两圆的无理交点，不机械核查古典证明。内外切坐标公式和判据的正确性必须独立论证；拒绝某个见证也不等于证明没有任何公共点。原创图画三个实际可实现的现代例子，不冒充原典反事实图。

[模型](geometry.py) · [单测](test_geometry.py) · [算例](run_examples.py) · [编排](run_all.py) · [Notebook构建](create_notebook.py) · [回放](verify_notebook.py)

[独立来源审查](source-review.zh-CN.md) · [独立技术审查](technical-review.zh-CN.md)。独立审查统计和最终正文绑定哈希以审查报告为准。
