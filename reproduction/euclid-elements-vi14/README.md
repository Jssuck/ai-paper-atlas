# VI.14 教学复现：等角平行四边形与交叉边比

[中文深读](../../papers/ancient/euclid-elements-vi14.zh-CN.md)

这份 Python 标准库代码以有理坐标重建辅助平行四边形，不是古代尺规操作的重演。设共享顶点 B 为原点，方向 u、v 不共线，端点 D=-xu、E=yu、F=-zv、G=wv；x、y、z、w 都为正。平行四边形 AB 由 BD 与 BF 张成，BC 由 BE 与 BG 张成，辅助图形 FE 由 BE 与 BF 张成。若记行列式绝对值为 d，则三面积分别为 xzd、ywd、yzd。AB/FE 与 BC/FE 分别为 x/y、w/z。方向不必单位化；消去的是同方向的长度因子，并非把一般向量的系数当作长度。

## 复跑

在本目录用 CPython 3.12.14 执行，无第三方依赖或外部数据：

```sh
export PYTHONDONTWRITEBYTECODE=1
python3 -m unittest -v
python3 -O -m unittest -v
python3 -OO -m unittest -v
python3 replay_notebook.py
```

前三个命令分别生成 [normal.log](normal.log)、[O.log](O.log)、[OO.log](OO.log)。每种模式有九项测试，其中一项用独立鞋带公式核对 1,024 组坐标的面积和比例；其他用例核对命题的两侧、非退化条件、倾角改变后的反例，以及共同线性变换。9 是测试方法数，不是几何用例总数。

[教学 Notebook](euclid-vi14.ipynb)可在已有 Jupyter 环境打开。本次用 [回放脚本](replay_notebook.py)按顺序运行三格 Python 代码并保留[实际输出](notebook-replay.log)，未启动 Jupyter 内核。Notebook 不缓存假造的执行结果。只用回放脚本执行可信的本仓库 Notebook。

## 如何读结果

- 直角例 x=6、y=4、z=2、w=3：AB=12、BC=12、FE=8，两个与 FE 的面积比都为 3/2。
- 去掉等角前提时，将 BC 的第二条单位方向从 (0,1) 换为 (3/5,4/5)，保留 AB 为原直角：保持四边长度是 12 对 48/5，不等积；把 BC 的 w 增至 15/4 又可等积，但交叉边比变为 3/2 对 15/8，不再相等。
- 有限有理数样例只检查教学实现、算例和反例，不证明一般几何定理。
