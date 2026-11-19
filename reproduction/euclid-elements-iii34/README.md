# 《几何原本》III.34：在已给圆里切出指定角的弓形

[返回中文精读](../../papers/ancient/euclid-elements-iii34.zh-CN.md)

本模型固定切点 $B=(0,0)$、圆心 $(0,R)$ 作教学归一化；切线的参考射线朝右。在这个坐标系，用有理方向向量 $(u,v)$ 表示从切点朝圆内复制的角，要求 $R>0,v>0$，按 $u$ 的正、零、负区分锐、直、钝。它算出第二交点，另取两条朝内的辅助射线给弦两侧各构造一个圆周见证。证书分开核对共圆、切线垂直、非零的同向弦、侧别与角签名，不把角大小和弓形身份混为一谈。反侧控制是相对于目标弧而言；它与参考切线射线处于弦的同侧，圆周角一般是目标角的补角，只有直角边界仍数值相等。

## 运行

实测 CPython 3.12.14，仅标准库，不用三角函数、浮点近似或外部数据。在本目录执行：

```sh
python cut_segment.py
python -m unittest -v
python -O cut_segment.py
python -O -m unittest -v
python -OO cut_segment.py
python -OO -m unittest -v
python replay_notebook.py
```

- [构造与证书](cut_segment.py) · [六项单测](test_cut_segment.py)
- 实跑：[普通](normal.log) · [优化](O.log) · [二级优化](OO.log)
- [Notebook](euclid-iii34.ipynb) · [纯 Python 回放](replay_notebook.py) · [回放日志](notebook-replay.log)

三个解释器模式各通过六项单测，并通过同一批 237 个精确输入组合的证书（117 锐角、3 直角、117 钝角；三种半径与去重后的 79 个有理方向）。这只是有限教学检查，不以组合数声称证明一般定理。构造部分不处理任意实数角的输入编码，也不宣称复刻古代尺规步骤。未发现可用的 Jupyter 内核；本次将 Notebook 三个 Python 代码格依次编译执行，没有声称运行 Jupyter 内核。已有内核时可从本目录打开 Notebook 并运行全部单元。
