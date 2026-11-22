# 《几何原本》VI.32：拼接两三角形得到一条直线

[中文精读](../../papers/ancient/euclid-elements-vi32.zh-CN.md)区分原文的拼接条件和现代坐标翻译。本目录以有理向量演示，不是古代证明的形式化执行。

## 运行

Python 3.9+ 标准库，无外部数据：

```sh
python -B -m unittest -v
python -B -O -m unittest -v
python -B -OO -m unittest -v
python -B replay_notebook.py
```

[程序](straight_on.py)、[测试](test_straight_on.py)、[Notebook](euclid-vi32.ipynb)。实跑：[普通](normal.log)、[`-O`](O.log)、[`-OO`](OO.log)、[回放](notebook-replay.log)。逐格执行 3 个纯 Python 单元，未调用 Jupyter 内核或验证前端渲染。

## 对照与边界

- 现代模型取有向 AB 与 DC 同向，AC 与 DE 同向；平方长度交叉乘积核对两组长度比。以 k>0 从 ABC 构造 DCE，独立从实际坐标核对两组对应边、BC 与 CE 的行列式，以及 CB 与 CE 的点积是否为负。这最后一项确保 C 在 B、E 之间，而不只是三点共线。
- 工作例 A=(0,0)、B=(0,2)、C=(3,0)、D=(3,−4)、E=(9,−4)，BC=(3,−2)、CE=(6,−4)，为 B–C–E。60 个精确配置来自 4 组不共线方向、3 个起点和 5 个正尺度；有限实跑不证明一般命题。
- 仅沿平行线反向放置第一组对应向量，得到 D=(3,4)、E=(9,4)。无向平行及长度比仍成立，但 det(BC,CE)=24。两组同时反向可仍共线，却重叠而非 B–C–E。另取 D=(7,0)、E=(7,6)，只保留两组长度比，不保持平行，仍不能得到所需结论。
