# 《几何原本》VI.5 · 精确坐标教学复现

[正文](../../papers/ancient/euclid-elements-vi5.zh-CN.md)。在有理坐标里，用基底投影构造共底辅助点 G，独立用点积的符号及其归一平方判等角，用长度平方判同比和共底三边相等。保留余弦符号避免把补角误判成相等；长度为正，故可安全比较平方。镜像 D 可以不等于 G，却仍满足三边全等和对应角相等。

## 运行

从本目录执行以下命令，仅需 Python 标准库（实跑 CPython 3.12.14）。

```sh
python -B -m unittest -v
python -B ratio_chains.py
python -B -O -m unittest -v
python -B -O ratio_chains.py
python -B -OO -m unittest -v
python -B -OO ratio_chains.py
python -B replay_notebook.py
```

[普通](normal.log)、[优化](O.log)、[二级优化](OO.log)各运行 6 个 unittest 测试并独立打印 216 个网格配置。网格组合四个原顶点、三个平移、三个缩放、三个旋转和两种反射状态；另外检查错配顶点、只保留两边比例以及退化输入。可打开[教学 Notebook](euclid-vi5.ipynb)逐格运行；[日志](notebook-replay.log)是标准库按顺序执行三个代码格的实测，不是 Jupyter 内核输出。有限样本用于教学核对，不证明任意实坐标下的定理，也不复现历史证明过程。
