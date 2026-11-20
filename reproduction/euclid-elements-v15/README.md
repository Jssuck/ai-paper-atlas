# 《几何原本》V.15 教学复现：共同整数倍不改变比

返回[中文精读](../../papers/ancient/euclid-elements-v15.zh-CN.md)。这里用正有理数模拟原证的“分成等份、各对同比（V.7）、合为两列总量（V.12）”。代码不是古代证明的机器验证，也不穷举实数或几何量。两量在同类且已换算为同一单位的前提下取值；程序没有记录单位，不接受混合单位为同类的证据。

## 运行环境与命令

Linux，CPython 3.12.14，仅 Python 标准库。在本目录运行：

~~~sh
export PYTHONDONTWRITEBYTECODE=1
python --version
python ratio_scaling.py
python -m unittest -v
python -O -m unittest -v
python -OO -m unittest -v
python replay_notebook.py
~~~

[演示与普通模式](normal.log) · [优化模式](O.log) · [双优化模式](OO.log) · [Notebook 回放](notebook-replay.log)。

可用 Python 3 内核打开 [Notebook](euclid-v15.ipynb)。本环境无 Jupyter、nbformat 或 ipykernel；实际用标准库按顺序执行三个代码单元并记录输出，不是 Jupyter 内核执行，也没有预填内核输出。

## 代码做了什么

- [ratio_scaling.py](ratio_scaling.py) 把对应的等份排列为有序对；例如 2 和 3 同取 4 倍时，两列分别由四个 2、四个 3 构成，总量为 8 和 12。所有份对相同这一事实对应 V.7；分别求和后比较，对应 V.12 中合并同比分量的步骤。代码里的 Fraction 商用于报告和核对，不是原证的推理前提。
- 比较探针 (m,n) 为两个独立的正整数，不是公共放大倍数 k。检查 2:3 和 8:12 时，探针 (1,1)、(3,2)、(2,1) 分别得到双方符号 −1、0、+1。只放大不同倍数会出错：把 2、3 分别乘 2、3 得到 4:9，同一探针 (3,2) 将等号变为小于。
- [测试](test_ratio_scaling.py) 含完整三分支、等份与两列合计、不同倍数反例、分数输入、1 倍及非法边界。三种解释器模式均通过 10 项测试。有限网格遍历 1 至 4 的 c、f、k、m、n，共 1,024 个输入；预期与阈值 n/m 用精确比比较，符号分布为 448 次小于、128 次等于、448 次大于。网格检验可查程序错误，不能代替任意正整数倍的一般论证。
