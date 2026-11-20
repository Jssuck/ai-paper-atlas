# 《几何原本》V.9 教学复现：同一参照下，怎样排除不等？

回到[中文精读](../../papers/ancient/euclid-elements-v9.zh-CN.md)。这是以正有理数实现的原创教学模型，程序不鉴定古典文献，也不替代一般量的证明。

## 环境与实跑

Linux，CPython 3.12.14，仅标准库。在本目录运行：

~~~sh
export PYTHONDONTWRITEBYTECODE=1
python --version
python equality_probes.py
python -m unittest -v
python -O -m unittest -v
python -OO -m unittest -v
python replay_notebook.py
~~~

[普通模式](normal.log)、[优化模式](O.log)、[双优化模式](OO.log)、[Notebook 实跑记录](notebook-replay.log)。[Notebook](euclid-v9.ipynb)可用同目录 Python 3 内核运行。这次环境未有 Jupyter、nbformat 或 ipykernel，以标准库在同一命名空间实际顺次执行 3 个代码单元，不算 Jupyter 内核运行。

## 复现逻辑

- 两个待比较量是 a、b，共同参照为 c。给定 m、n，前向记录 m·a 对 n·c、m·b 对 n·c 的两个符号，反向记录 n·c 对 m·a、n·c 对 m·b 的符号。后者把倍数角色换过来，两个比较符号各自取反。
- 若输入量 a 与 b 不等，先识别较大与较小的量，再使用 V.8 的严格夹逼构造。把较大的量拆成较小量与差量；用最小正整数 m 令两部分的 m 倍均大于 c；令 n·c 为严格大于两倍量中较大者的最小 c 倍量。这样得到 m·较小量 < n·c < m·较大量。返回的两组符号均不一致，任一组已足以否定该方向上 V.Def.5 的全称同比断言。
- 若 a = b，任意同倍数下两端一致，这是由输入精确相等推出，不靠探针数量；程序的 `distinguish` 先直接比较精确输入，并非未知量的黑箱同比判定器。
- 独立的 `bounded_mismatch` 返回窗口内找到的首个不一致，或在未找到时返回 None；它从不声称同比。a=102、b=101、c=100 在双上界 20 的窗口内都一致，扩大到 51 首个不一致是 (50,51)：5100 = 5100，而 5050 < 5100。V.8 的构造另给 (101,103)，同一证书可排除两个方向的同比。构造不以最短证书为目标。
- 三种解释器模式分别通过 11 项测试，包含以 19 种正有理数生成的 6,859 个有序三元组，其中 361 组首两量相等、6,498 组不等。另外检查弱见证（含等号）、前后角色互换、异类量和输入验证。有限有理数网格检查实现，不证明一般量的定理。
