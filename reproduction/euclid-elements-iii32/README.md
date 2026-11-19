# 《几何原本》III.32：弦与切线的两个角

[返回正文](../../papers/ancient/euclid-elements-iii32.zh-CN.md)

这是现代坐标教学模型。它把同圆、点互异、非零切向、半平面配对和角值相等分开记录；不把几何结论当成输入，也不试图复刻欧几里得的作图证明。

对非零向量，角签名是 `(dot(u,v), abs(cross(u,v)))`，即余弦和正弦对乘上相同正因子。两个角在零到平角之间时，签名同向共线才相等；只验共线而不验同向，会误把零角和平角混为一谈。弦向量分别与切线射线、顶点方向作叉积，乘积严格为负标记异侧。切线条件独立用半径与射线垂直来检验。直径时，数值相等不能代替侧别判定。

## 运行

在本目录运行。实测 Python 3.12.14，仅依赖标准库；未安装额外包、未使用外部数据。三个模式分别执行相同算例与单元测试：

```sh
python alternate_segments.py
python -m unittest -v
python -O alternate_segments.py
python -O -m unittest -v
python -OO alternate_segments.py
python -OO -m unittest -v
python replay_notebook.py
```

- [模型源码](alternate_segments.py) · [6 项单元测试](test_alternate_segments.py)
- [普通模式](normal.log) · [优化模式](O.log) · [二级优化模式](OO.log)
- [教程 Notebook](euclid-iii32.ipynb) · [纯 Python 回放脚本](replay_notebook.py) · [回放实跑日志](notebook-replay.log)

此环境没有 Jupyter 或 ipykernel。Notebook 保留为清洁、未存输出的教程；本次实际逐个编译执行了三个纯 Python 代码单元，未运行 Jupyter 内核。若已有 Python 内核，可在该目录打开 Notebook 后从头运行所有单元。

## 范围

选两种圆半径，对每种生成 47 个互异的圆上点（切点另计），穷举弦端点、圆周角顶点、切线射线共 8,648 个组合。4,324 个异侧配对全相等，其中 92 个为直径；4,324 个同侧对照有 4,232 个不等，其余 92 个为直径。单元测试另外校验非切线、退化输入和有理相似变换含反射。不估计任何统计准确率；这个有限枚举不能证明一般定理。
