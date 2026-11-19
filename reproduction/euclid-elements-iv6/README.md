# 欧几里得《几何原本》IV.6：作圆的内接正方形

[中文深读](../../papers/ancient/euclid-elements-iv6.zh-CN.md)

这是现代有理坐标的教学重构，并非模拟古代尺规操作。输入圆心和一个不同于圆心的圆周点，先取指向该点的半径向量，再作逆时针四分之一转。两个向量和它们的反向向量确定四个按圆周顺序排列的顶点。检验器不调用构造函数，直接从候选顶点测量平方距离、相邻边的点积、转向、对角线与有向面积；它检查的是本程序规定的起点和逆时针次序，不是任意顶点标记的通用识别器。

输入坐标为 Python 整数或标准库 Fraction，不接收浮点。只用半径平方，半径本身可以是无理数。选了坐标表示就不能覆盖无法以有理坐标给出圆心或指定圆周点的所有输入。两条不垂直的等长直径是对照：四角仍直，两条对角线仍等长，但边长交替不等。把正确四点连成自交次序同样不满足输出要求。

## 执行

实跑环境为 Python 3.12.14，仅标准库，无下载数据。从本目录运行：

```sh
python -B -m unittest -v
python -B inscribed_square.py
python -B -O -m unittest -v
python -B -O inscribed_square.py
python -B -OO -m unittest -v
python -B -OO inscribed_square.py
python -B replay_notebook.py
```

[普通](normal.log)、[优化](O.log)、[最高优化](OO.log)各通过 8 项测试。三个有理圆心分别配以半径向量 `(x/3, y/5)`，其中 `x, y` 独立遍历 -5 到 5 的整数。360 个非零输入通过全部坐标检验，3 个零半径输入被拒；这是带圆心和初始向量的输入计数，不是按旋转、缩放、平移等价分类的图形个数。有限网格不能代替一般证明，也不测量带噪浮点作图的稳定性。

[教学 Notebook](euclid-iv6.ipynb)含示例、反例和参数网格。环境中没有可用 Jupyter 内核，未安装任何包；[回放脚本](replay_notebook.py)用标准库实际依次执行三个代码单元，见[回放日志](notebook-replay.log)。
