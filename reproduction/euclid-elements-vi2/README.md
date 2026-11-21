# 《几何原本》VI.2：精确坐标教学复现

配套[中文精读](../../papers/ancient/euclid-elements-vi2.zh-CN.md)。这是现代坐标实验，不是对欧几里得写作环境、图版或原证明的复现，也不是用有限枚举代替一般证明。

## 怎样重跑

Python 3.12，只有标准库，无数据集、浮点容差及随机种子。进入本目录后运行：

```sh
python --version
python -B ratio_chains.py
python -B -m unittest -v
python -B -O -m unittest -v
python -B -OO -m unittest -v
python -B replay_notebook.py
```

对应真实日志：[普通](normal.log)、[优化](O.log)、[二级优化](OO.log)、[Notebook 代码单元](notebook-replay.log)。[教学 Notebook](euclid-vi2.ipynb) 可在已有 Jupyter 的环境按顺序运行；本轮未运行 Jupyter 内核，使用标准库回放其全部 3 个代码单元，日志记录实际输出。回放器只用于此仓库可信 Notebook，不应用于不可信文件。

## 测了什么

- 以非退化 ABC 和严格内点 D、E 为默认输入。拒绝端点、偏离对应直线、共线三角形及浮点输入。
- 使用 Fraction 度量无向线段比和两倍面积，另存带符号的 DE 与 BC 方向行列式和 B、C 对 DE 的同侧测试。面积顺序始终为 ADE、BDE、CDE。
- 正例两比均为 2，两倍面积依次为 1、2、2。负例两比为 2、1/2，两倍面积为 2、4、1；只倒置第二个比会制造假相等。
- 显式关闭内点限制才能运行越界反例：两比均为 1/2，外侧两片面积相等，但 B、C 分处 DE 两侧且 DE 不平行于 BC。反例反驳无向比的无条件推广，不反驳原命题。
- 六个有不同方向和形状的坐标框中，两个切分参数独立取十分之一到十分之九，合计 486 组：54 组平行、432 组不平行。用另一套展开的鞋带公式得到 ABC 有向面积，再按参数比例预测各面积和方向行列式，与直接从 D、E 计算的值逐项比较。测试同时核对比、同侧和两个蕴涵。有限格点不能覆盖任意实数，也不检验卷 V 定义的历史解释。
