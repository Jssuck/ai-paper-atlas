# 《几何原本》VI.12：第四比例项的教学复现

对应[中文深读](../../papers/ancient/euclid-elements-vi12.zh-CN.md)。

原图的角色是 DG、GE、DH 分别承载给定正长度 a、b、c；过 E 作 GH 的平行线，交从 D 经 H 的第二条射线于 F。代码先只用给定长度放置 D、G、E、H，再在行列式非零时求交；不把预期的 HF 直接预置给相交程序。检查器核对两条射线、点序、长度平方、平行以及 a·HF=b·c；有限扫掠另把交点和直接公式 HF=bc/a 对照。

正例 a=4、b=6、c=8，D=(0,0)、G=(4,0)、E=(10,0)、H=(0,8)、F=(0,20)，所以 HF=12。若误复制 GE=4，平行条件可以仍成立，但 F=(0,16)、HF=8，不能作为原问题的解。将第三给定项设成 b，得到上一命题的第三比例项 b²/a。

## 运行

Python 标准库，无需安装；在本目录使用：

```sh
python -B -m unittest -v
python -O -B -m unittest -v
python -OO -B -m unittest -v
python -B replay_notebook.py
```

[普通](normal.log)、[-O](O.log)、[-OO](OO.log) 三种模式各通过 8 项测试。扫掠每次覆盖 1,536 个构形，其中 768 次由镜像生成；正长度来自四个有理数的有序三元组，并改变平移、角度和朝向。另有错复制、非平行、倒序和退化测试。有限有理坐标及有理单位方向测试不是一般定理的证明，更不是对古代尺规现场的复演。

[Notebook](euclid-vi12.ipynb) 的 3 个代码格由标准库编译并执行，实际输出见[回放日志](notebook-replay.log)；这不是 Jupyter 内核执行。Notebook 保留未执行状态以便重跑。
