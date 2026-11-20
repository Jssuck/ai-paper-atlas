# V.19 教学复现：整体、减去部分与余量

[中文精读](../../papers/ancient/euclid-elements-v19.zh-CN.md) · [源码](ratio_remainders.py) · [测试](test_ratio_remainders.py) · [Notebook](euclid-v19.ipynb)

本目录用 Python 正有理数模型验证每一步的现代数值结果。冒号在程序中用精确分数商核验，这不是在古代语境中实施 V.Def.5 的所有整倍比较，也不是一般证明。每组输入需要用一致的单位表达；`kind` 检查量类，不换算单位。去掉的部分与余量必须为正。

## 两条路线

- **主命题，四量同类。** 设 `A,B` 是两个整体，`U,V` 是减去的部分，`R=A−U,S=B−V`。在 `A:B = U:V` 的前提下，依次核验 V.16（`A:U = B:V`）、V.17（`R:U = S:V`）、V.16（`R:S = U:V`）、V.11（`R:S = A:B`）。两次 V.16 的换位均要求四量同类。示例把 4、6 分别从 10、15 减去，余量 6、9 的比仍是整体比 2/3。
- **传本附论，另走一条重构路线。** 前提改成 `A:U = B:V`，结论是 `A:R = B:S`。先分比得到 `R:U = S:V`，再同时取倒比得到 `U:R = V:S`，最后合比得到 `A:R = B:S`。此教学重构不调用 V.16；只需 `A,U` 组内同类、`B,V` 组内同类，两组之间可不同。仍用 10、4 和 15、6，但可把前组视为长度、后组视为面积。两组合比均由 5/2 转成 5/3，而不是互换前后项。参见 [V.Def.16 与导读](https://mathcs.clarku.edu/~djoyce/elements/bookV/defV14.html)。

## 重跑与结果

环境为 Python 3.12.14，仅需标准库。无历史实验数据或外部依赖。

```sh
python -V
python -B -m unittest -v
python -O -B -m unittest -v
python -OO -B -m unittest -v
python -B ratio_remainders.py
python -B replay_notebook.py
```

[普通模式与示范](normal.log)、[-O](O.log)、[-OO](OO.log) 均通过 9 项测试。[Notebook 回放日志](notebook-replay.log) 来自三个单元依次实际执行。本环境缺少 Jupyter 内核，因此只用标准库读取同一 Notebook 文件、编译并顺序执行其 Python 单元；不要用回放脚本执行来源不明的 Notebook。

有界基线令 `r,u,p,q` 独立取 1 到 8，按 `((r+u)p,(r+u)q,up,uq)` 生成整体与去掉部分。4,096 组输入分别经过两条路线，结果与独立生成的 `p/q`、`(r+u)/r` 相符。另测非整数分数、失配前提、错误量类、零/负余量、不合法数值。这些检查不覆盖任意量或不可公度量，不证明一般定理。
