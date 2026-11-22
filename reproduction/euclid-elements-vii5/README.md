# 《几何原本》VII.5：相同一份相加仍是同一份

[中文精读](../../papers/ancient/euclid-elements-vii5.zh-CN.md)重建欧几里得的配对论证。本目录用两列等次数复制、逐项配对与独立分数计算做有限检查，不替代古代证明。

## 运行

仅用 Python 3.9+ 标准库，无外部数据：

```sh
python -B -m unittest -v
python -B -O -m unittest -v
python -B -OO -m unittest -v
python -B replay_notebook.py
```

[程序](same_part.py)、[测试](test_same_part.py)、[Notebook](euclid-vii5.ipynb)。实跑：[普通](normal.log)、[`-O`](O.log)、[`-OO`](OO.log)、[回放](notebook-replay.log)。回放逐格执行 3 个纯 Python 单元，未启动 Jupyter 内核或验证前端渲染。

## 核验与限制

- 输入两对正整数，所取的一份必须严格小于各自整体。只有当两整体分别是各自所取一份的同一个正整数倍 n 时，构造 n 个配对单元。例 3 与 12、5 与 20：两边各 4 份，每对合为 8，四对合为 32。
- 取两组所取一份的大小分别在 2 至 24，公共倍数在 2 至 14，共 6,877 组；交叉验证两列之和、配对之和和 `Fraction` 直接计算的三种相同比。复制列占用与 n 成正比的空间，只作教学用途。
- 两原比为 1/4、1/3 时，示例合并比为 8/27，既不是 1/4 也不是 1/3。相同的 2/3 也可在现代比值模型下合并，但不是本命题「同一份」的输入；复制见证拒绝这个情形。默认拒绝把单位 1 当作古代的数输入，显式开启现代扩展才接受。
