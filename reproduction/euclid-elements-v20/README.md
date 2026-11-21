# V.20 教学复现：相邻比例和端点次序

[中文精读](../../papers/ancient/euclid-elements-v20.zh-CN.md) · [源码](ratio_chains.py) · [测试](test_ratio_chains.py) · [Notebook](euclid-v20.ipynb)

用正有理数重现 [V.20](https://mathcs.clarku.edu/~djoyce/elements/bookV/propV20.html) 的数值推理。给定两组 `(A,B,C)`、`(D,E,F)`，依次检查 `A:B = D:E`、`B:C = E:F`。第二对同时取倒比，再比较 `A:B` 与 `C:B`，把次序移到 `D:E` 与 `F:E`，最后核验 `D`、`F` 的大小关系。用一次三向比较实现大于、等于和小于三个分支，不把相邻的两个比相乘。原文详细写出大于分支；程序对三个分支的推广是教学重构。

每组量必须同类且采用一致单位；`kind` 只检查量类，不做单位换算。两组之间可以不同类。示例左组是 6、4、3，右组是 12、8、6。两组分别用各自中项作分母，比值序列都是 3/2、3/4，因此第一端都大于第三端。若右组改为 12、8、15，只有第一对相邻比例相同，次序翻转；右组若改为 12、20、15，则只有第二对相同，次序仍翻转。

## 重跑与结果

只用 Python 3.12.14 标准库，无外部依赖或历史实验数据。在本目录执行：

```sh
python -V
python -B -m unittest -v
python -O -B -m unittest -v
python -OO -B -m unittest -v
python -B ratio_chains.py
python -B replay_notebook.py
```

[普通模式及示例](normal.log)、[-O](O.log)、[-OO](OO.log) 各通过 9 项测试。[Notebook 回放日志](notebook-replay.log) 记录三个代码单元的实际顺序执行。本环境无 Jupyter 内核，因此用标准库编译同一 Notebook 的代码单元执行，未在 Jupyter 内核中实跑；不要用脚本回放不可信 Notebook。

两种补充基线：一是枚举四个独立的 1 到 8 的整数，生成 4,096 组分数输入，用构造时已知的左端点次序检查结果，分布为小于 1,792、等于 512、大于 1,792。二是穷举每项取 1 到 5 的 15,625 个整数六元组，用整数交叉乘积独立检查两条前提：157 组满足，用右端点的直接整数比较核验返回值；其余 15,468 组必须被拒。另测混合量类、非正值及非精确输入。分数商不是 V.Def.5 对任意整倍数的比较；这些有限数值检查既不覆盖不可公度量，也不是一般定理的证明。
