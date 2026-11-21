# VI.13 教学复现：半圆、中比例项与精确平方证书

这是现代坐标模型，不是原文证明的程序化版本。给定两段正长度，令 A=(-a,0)、B=(0,0)、C=(b,0)。取 AC 中点为圆心，半径是 AC 的一半；将直线 x=0 代入圆方程，得到上半圆交点的高度平方。用这个结果再检查 AD 与 CD 的点积为零，相当于核验这一模型中的直角。源码不会用乘积直接代替圆方程；测试另以乘积为参照。

输入限正整数或正有理数，不将浮点数隐式转为有理数。精确平方证书可表达不可公度实例：a=1、b=2 时高度平方恰为 2，高度存在却不是有理数，`rational_altitude` 返回 `None`。若约分后的分子与分母各为完全平方才返回精确有理高度。a=9、b=16 时高度为 12；半径 25/2 不能代替高度，圆的最高点不在 x=0。若给定某一侧，则另一侧的镜像不作为本构造输出。

从本目录运行，无需第三方包。实跑使用 CPython 3.12.14：

```sh
PYTHONDONTWRITEBYTECODE=1 python -m unittest -v
PYTHONDONTWRITEBYTECODE=1 python -O -m unittest -v
PYTHONDONTWRITEBYTECODE=1 python -OO -m unittest -v
PYTHONDONTWRITEBYTECODE=1 python replay_notebook.py
```

三种模式各跑 9 个测试，覆盖 1,024 组有序正有理数组合及交换两段后的镜像关系，另含有理与无理高度、等长、零长、负长、非支持输入及错误交点。日志见 [普通](normal.log)、[-O](O.log)、[-OO](OO.log) 与 [Notebook](notebook-replay.log)。Notebook 的 3 个代码格由标准库在共享命名空间逐格编译执行，没有启动 Jupyter kernel；输出保存于实跑日志而非 Notebook。有限实例不能代替一般几何证明。
