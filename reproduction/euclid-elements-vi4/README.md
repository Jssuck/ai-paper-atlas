# 《几何原本》VI.4 教学复现

[返回中文精读](../../papers/ancient/euclid-elements-vi4.zh-CN.md)。

这不是古证明的计算机形式化。它用有理坐标复核样例中辅助图的约束与比例，不以有限样本代替一般证明。

- 以角的余弦符号及其平方分别检查三对角，不从边长比倒推输入。
- 要求 B–C–E、A 和 D 同侧，求两条射线的交点 F 后检查 B–A–F、E–D–F；再用行列式验平行。
- 计算三个正比的平方以检查两次 VI.2（BA:AF、BC:CE、FD:DE），检查 AF=DC、FD=AC，再检查替换、两次 V.16 和一次 V.22 得到的三个终式。正比的平方相等当且仅当比相等；有理坐标的边长本身可以是无理数。
- 坐标示例的两组三边分别为 3、4、5 与 9/2、6、15/2，截线比都是 2/3。负例包括错误角对应、退化输入、单独镜像造成辅助图不满足同侧条件；镜像本身并不破坏三角形等角。
- 216 组构造样本来自三个平移、三种基向量、四种缩放、三种斜度、两种朝向的组合，不是历史数据或性能实验。

用 CPython 3.12.14，标准库即可。在本目录运行：

```sh
python -B -m unittest -v
python -B -O -m unittest -v
python -B -OO -m unittest -v
python -B replay_notebook.py
```

[普通](normal.log)、[-O](O.log)、[-OO](OO.log) 每种模式 6 项测试；[Notebook](euclid-vi4.ipynb) 的 3 个代码单元另用 Python 标准库实际顺序执行，[见日志](notebook-replay.log)，未使用 Jupyter 内核。
