# 《几何原本》VI.19：相似三角形与平方比的教学复现

这里用现代有理坐标核对相似三角形的面积比，并重现第三比例点的角色。原证及量比定义的区别见[中文精读](../../papers/ancient/euclid-elements-vi19.zh-CN.md)。这不是对古代尺规公理或欧多克索斯比例论作形式化验证。

## 运行

Python 3.9+ 标准库，无外部数据；在本目录运行：

```sh
python -B -m unittest -v
python -B -O -m unittest -v
python -B -OO -m unittest -v
python -B replay_notebook.py
```

程序：[triangle_areas.py](triangle_areas.py)，测试：[test_triangle_areas.py](test_triangle_areas.py)。实跑：[常规](normal.log)、[`-O`](O.log)、[`-OO`](OO.log)。[Notebook](euclid-vi19.ipynb) 可在本地 Python Notebook 前端从头运行；这里使用 [replay_notebook.py](replay_notebook.py) 顺序编译执行 3 个纯 Python 单元，见[回放日志](notebook-replay.log)。没有调用 Jupyter 内核或验证前端渲染。

## 对照与限制

- 固定对应标签 `A → D, B → E, C → F`。令 `k = EF/BC`，第三比例点 `G` 位于从 `B` 向 `C` 的射线上，满足 `BG/BC=k²`。原命题并不要求 `G` 在 `B,C` 之间。工作例给出面积 `ABC, DEF, ABG = 6, 27/2, 27/2`，从而 `ABC:DEF=4/9`。
- 核对三角形面积时从坐标行列式取绝对值之半；核对边时由两点距离平方算出，不以预设的 `k²` 代替实算面积。第三比例和互易比例用正长度等式的平方交叉乘积精确比较。面积正负翻转不是面积改变；符号只承担检验反射的工作。
- 一共 320 个受控变换配置：4 个非共线基础三角形 × 5 个正比例因子 × 4 个旋转 × 2 个平移 × 2 个镜像选择。其中 `EF < BC`、相等、`EF > BC` 分别有 128、64、128 个，160 个使用镜像。该生成网格不是任意三角形的相似性判定算法；计算采用精确有理数，没有浮点容差。
- 保持例中的 `E=(0,0), F=(6,0)`，将顶点改为 `D′=(2,3)`。两三角形不相似，面积比 `D′EF/ABC=3/2`，而平方底比仍是 `9/4`。反过来，若取 `D′=(0,9/2)`，同一底边的平方比与面积比都为 `9/4`，但另一对应边平方比 `D′E²/AB²=81/40`，仍不相似。零底边或非正缩放不进入第三比例构造。本演示有限样本不证明一般命题。
