# 《几何原本》VII.4：较小数是较大数的一份或若干份

[中文精读](../../papers/ancient/euclid-elements-vii4.zh-CN.md)区分古代份数说法和现代分数模型。这里用有限整数样本核验，不代替古代证明。

## 运行

只依赖 Python 3.9+ 标准库，无外部数据：

```sh
python -B -m unittest -v
python -B -O -m unittest -v
python -B -OO -m unittest -v
python -B replay_notebook.py
```

[程序](part_or_parts.py)、[测试](test_part_or_parts.py)、[Notebook](euclid-vii4.ipynb)；实跑：[普通](normal.log)、[`-O`](O.log)、[`-OO`](OO.log)、[回放](notebook-replay.log)。回放逐格编译执行 3 个纯 Python 单元，未调用 Jupyter 内核或验证前端渲染。

## 对照与边界

- 输入较小数 a 和较大数 b，要求 0<a<b。求最大共同量数 g，分成 a/g 与 b/g 个相同大小的单位块；现代分数模型中前者是最简分子，后者是最简分母。这里「一份」以最简表示的分子等于 1 判定，也就是 a 量尽 b。
- 复现三种情形：互素 (5,8) 以单位取 5/8；量尽 (4,12) 得一份 1/3；非互素但不能量尽 (6,15) 用共同量数 3 得 2/5。若改用较小的共同量数也可给出细分，但不会比最简表示需要更少份。例 12、18 得 12/18、6/9、4/6 或 2/3。
- 独立标准库分数与枚举共同因子两路对照；穷举较大数 2 至 80 的 3,160 对。互素且非单位 1,886 对、非互素量尽 209 对、有共同非单位但不量尽 986 对、现代初始单位 79 对。可选古域标志拒绝将单位 1 作为数输入，不拒绝证明中用单位作为共同度量。
