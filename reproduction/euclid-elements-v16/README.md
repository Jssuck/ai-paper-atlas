# 《几何原本》V.16 教学复现：交换中项

返回[中文精读](../../papers/ancient/euclid-elements-v16.zh-CN.md)。用带类别标签的正有理量模拟卷五命题 16。输入需要在同一类别内先换成同一单位；程序不会换算单位，也不凭数值判断量的类别。这里的 Fraction 商是现代参照值，用来比对各数学步骤；它不是欧几里得证明的前提。样例和有限网格均不能证明一般命题。

## 运行环境与命令

Linux，CPython 3.12.14，仅 Python 标准库。在本目录运行：

~~~sh
export PYTHONDONTWRITEBYTECODE=1
python --version
python ratio_alternation.py
python -m unittest -v
python -O -m unittest -v
python -OO -m unittest -v
python replay_notebook.py
~~~

[演示与普通模式](normal.log) · [优化模式](O.log) · [双优化模式](OO.log) · [Notebook 回放](notebook-replay.log)。

可用 Python 3 内核打开 [Notebook](euclid-v16.ipynb)。本环境无 Jupyter Notebook、JupyterLab、nbformat 或 ipykernel，实际按原顺序用标准库运行三个代码单元并记录输出；未运行 Jupyter 内核，未预填内核输出。仅对本目录已审查的 Notebook 使用本回放脚本。

## 样例怎样核查

- [实现](ratio_alternation.py) 先检查原始两比及跨对类别，再用各自的整数倍得到 E=mA、F=mB、G=nC、H=nD。检查两次 V.15 同倍保比、两次 V.11 同比传递，以及 V.14 所保证的比较符号一致。最后以交替后两比同阈值 n/m 的精确比较核对符号，模拟 V.Def.5 的探针方向；实际只跑了指定的有限个探针。
- 对 A、B、C、D 依次为 2、3、4、6，原始两比均为 2/3，交替后两比均为 1/2。探针 (1,1)、(2,1)、(3,1) 分别使两个比较同为小于、等于、大于。注意倍数是在原始对内相同，不要求不同对选同一个倍数。
- 若前两数是长度、后两数是面积，两个原始比各自在同类中定义，其精确商可同为 2/3；程序仍拒绝构造长度与面积的交替比。若把 D 改成同类的 5，则前提不再成立。
- [测试](test_ratio_alternation.py) 在三种模式均通过 9 项。有限网格取六个独立整数 u、v、s、t、m、n，各在 1 至 4；构造 (A,B,C,D)=(us,vs,ut,vt)，然后对照 s/t 和 n/m。4,096 个输入组合（并非 4,096 组不同的原始比）中，符号分布为 1,792 次小于、512 次等于、1,792 次大于。另测了分数输入、失效前提、跨类量及非法倍数。
