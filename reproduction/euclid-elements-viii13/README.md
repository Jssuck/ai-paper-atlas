# VIII.13：拼接和抽取平方链、立方链

现代整数教学重构，不是古代实跑或一般证明。设输入的前后项比恒为 a:b。对一对邻项 x、y，先按 VIII.11 插入平方桥 (x²,xy,y²)，或按 VIII.12 插入立方桥 (x³,x²y,xy²,y³)。每条局部桥都保持原比，以共同端点拼接时只保留一份。全链每隔两步或三步提取一项，依次得到原项的平方或立方，相邻比则为原比的两次或三次复合。原证明写出三项情形；程序也检查延长链。

(4,6,9) 的平方桥拼接为 (16,24,36,54,81)，立方桥拼接为 (64,96,144,216,324,486,729)。反转输入使全桥反转；整体乘 2 会把平方桥各项乘 4、立方桥各项乘 8。非恒比输入 (4,7,9) 不适用。程序只接受至少三项；仅在显式现代模式允许单位和恒比为 1 的常数列。

独立基线从首项的幂出发，按精确 Fraction 增长因子逐项推算全桥，与所有局部片段、整体和抽取结果分别核对。

## 重跑

在本目录使用 Python 3.9+ 标准库，不需联网。

```sh
python3 -B power_chains.py
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

每种模式运行 5 项测试；有限网格精确核对 198 组输入链与幂次组合。Notebook 的三个代码单元通过标准库实际按顺序回放，并非 Jupyter 内核运行。

实跑环境：Linux / CPython 3.12.14。回到[中文精读](../../papers/ancient/euclid-elements-viii13.zh-CN.md)，查看[原典核对](source-review.zh-CN.md)和[独立技术核对](technical-review.zh-CN.md)。

[实现](power_chains.py) · [测试](test_power_chains.py) · [Notebook](euclid-viii13.ipynb) · [重放脚本](replay_notebook.py)

[普通模式](normal.log) · [-O](O.log) · [-OO](OO.log) · [Notebook 重放](notebook-replay.log)
