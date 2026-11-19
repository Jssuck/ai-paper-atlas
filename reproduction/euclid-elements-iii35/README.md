# 《几何原本》III.35：相交弦的乘积

[返回中文精读](../../papers/ancient/euclid-elements-iii35.zh-CN.md)

程序用标准库有理数验证同圆、线的唯一交点、交点在两条线段内部、无向乘积与弦中点分解。取弦从端点 A 到 C 的方向，交点写作 A+s(C−A)；由交点到两端点的有向参数分别为 −s、1−s，故有向长度的乘积可由 s(s−1) 乘以弦长平方得到，无须开平方。圆内分割的两个正长度之积为其相反数。用弦中点重算“半弦平方−交点到中点距离平方”，另核中垂线及半径平方关系。这个坐标验证不是欧几里得原证的程序翻译。

两条支撑线在圆外相交时，有向乘积同为正值；这是现代统一表达的控制，不计入 III.35。另设一端点不共圆的反例，其两乘积不等。有限枚举取两个圆，每圆 16 个经有理参数生成并以叉积排序的圆周点；每组循环四点取两条对角弦。共核验 3,640 组内交构形，无直径、单直径、双直径各 2,912、672、56，垂直的有 110 组（与直径分类有重叠）。枚举覆盖有限样本，不证明一般定理；未使用外部数据、随机性或浮点容差。

## 运行

Python 3.12.14，仅标准库。在本目录执行：

```sh
python chord_products.py
python -m unittest -v
python -O chord_products.py
python -O -m unittest -v
python -OO chord_products.py
python -OO -m unittest -v
python replay_notebook.py
```

- [构形与证书](chord_products.py) · [七项单测](test_chord_products.py)
- 实跑：[普通](normal.log) · [优化](O.log) · [二级优化](OO.log)
- [Notebook](euclid-iii35.ipynb) · [纯 Python 回放](replay_notebook.py) · [回放日志](notebook-replay.log)

三个解释器模式均通过七项测试以及同一批精确枚举，不能把这些重复模式算作更多构形。环境没有可用 Jupyter 内核，本次按顺序用纯 Python 编译执行 Notebook 的三个代码格。如果已有 Python 内核，可从本目录打开 Notebook 并从头运行所有单元。
