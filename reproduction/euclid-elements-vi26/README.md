# 《几何原本》VI.26：相似角格与对角线

[中文精读](../../papers/ancient/euclid-elements-vi26.zh-CN.md)重建古证明。这里以有理坐标表示同一顶角与按平行边的固定对应，是现代有限验证，不是一般证明。

## 运行

仅依赖 Python 3.9+ 标准库：

```sh
python -B -m unittest -v
python -B -O -m unittest -v
python -B -OO -m unittest -v
python -B replay_notebook.py
```

[程序](same_diagonal.py)、[测试](test_same_diagonal.py)、[Notebook](euclid-vi26.ipynb)。实跑：[常规](normal.log)、[`-O`](O.log)、[`-OO`](OO.log)、[Notebook 回放](notebook-replay.log)。顺次编译、执行 3 个纯 Python 单元，未调用 Jupyter 内核或验证前端渲染。

## 构造与对照

- 从 A 出发的两边为不共线向量 u、v。取 E=A+su、G=A+tv、F=A+su+tv；从 G 沿平行 u 的直线与对角线 AC 相交于 H=A+t(u+v)，从 H 平行 v 至 AB 得 K=A+tu。独立从顶点距离计算沿两轴的边长平方比，从顶点差算行列式比较共线，并以鞋带公式核对面积。
- 取 u=(6,0)、v=(2,4)、s=1/2、t=1/3，F=(11/3,4/3)，H=(8/3,4/3)，K=(2,0)。沿 u、v 的对应边平方比是 1/4、1/9，不是同一尺度；以 AC、AF 依序计算行列式为 −4。
- 200 个精确配置：4 对边向量 × 2 个起点 × 5 个 s × 5 个 t，其中 s<t、s=t、s>t 分别 80、40、80 个。覆盖斜形、矩形、反向取向及有理平移。只有 s=t 时两个方向尺度一致且 F=H；符号可随取向翻转，零条件不变。
- 两组切分 (s,t)=(1/4,1/4) 与 (1/2,1/8) 给出相同面积 3/2，并有同一顶角、同向边，但后一组没有沿两轴等比，F 不在 AC 上。只比较面积或只比较角不足。拒绝零边、共线边与非内部切分；不自动重标边或搜索任意多边形的相似映射。
