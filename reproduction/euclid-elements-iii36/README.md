# 《几何原本》III.36：切线平方与割线乘积

[返回中文精读](../../papers/ancient/euclid-elements-iii36.zh-CN.md)

这是基于坐标的**教学重构**，不是古代文本的程序翻译。给定圆心 O、正半径 r、圆外点 D、割线依次遇到的 C、A 以及切点 B，程序先独立核对外点、三点共圆、正向共线和近远顺序，再检查半径 OB 与 DB 垂直。程序不以待证的乘积判定切线。由于由 D 指向 C 和 A 的向量同向，它们的点积就是两段长度之积，无须开平方或引入浮点误差。

弦中点 F 等于 O 时为过中心分支，不等时为不过中心分支。两支均验证 II.6 对应的“割线乘积 + 半弦平方 = 中点到外点的距离平方”，并将两边分别用勾股关系还原为半径平方和圆心到 D 的距离平方；过中心时中垂距离为零，不能把它称为一个非退化直角三角形。最后核对 DB 的平方。两个固定示例分别给出 144 和 9；错误切点、无效半径、非外点、端点不共圆、顺序错误及非割线等由单元测试覆盖。

有限样本从两个有理圆各取 20 个候选切点，各用 3 个垂直位移造外点 D。由 20 个有理单位圆周点加上指向 D 的径向单位向量生成 C 候选（重复则去除），仅保留面向 D 的严格近交点。程序用已知交点 C 代入直线与圆的交点方程，因式分解计算第二交点 A；验证器则重新以共圆、共线和顺序验收。每个指定的圆、切点、位移组合都有一个通过圆心的割线。共检查 560 个配置（120 个过中心、440 个不过中心）；镜像、相似等配置不必代表彼此独立的几何形状。样本只有有理数输入，无需数据集或浮点容差，不能证明一般定理。

## 运行

Python 3.12.14，仅标准库。在本目录执行：

```sh
python secant_tangent.py
python -m unittest -v
python -O secant_tangent.py
python -O -m unittest -v
python -OO secant_tangent.py
python -OO -m unittest -v
python replay_notebook.py
```

- [构形与证书](secant_tangent.py) · [八项单测](test_secant_tangent.py)
- 实跑：[普通](normal.log) · [优化](O.log) · [二级优化](OO.log)
- [Notebook](euclid-iii36.ipynb) · [纯 Python 回放](replay_notebook.py) · [回放日志](notebook-replay.log)

三个解释器模式均通过八项测试与同一批有限构形。本次未使用 Jupyter 内核；用纯 Python 按顺序编译、执行 Notebook 的三个代码格。若有 Python 内核，可在本目录打开 Notebook 从头运行所有单元。
