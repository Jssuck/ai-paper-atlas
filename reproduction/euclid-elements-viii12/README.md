# VIII.12：两个立方数之间的两个等比中项

现代整数教学重构，不是历史实跑或一般定理的计算证明。给定生成边 c、d，先取 E=c²、F=cd、G=d²；再取 A=cE、H=cF、K=dF、B=dG。两中项为 c²d、cd²，三个相邻前后项的比均为 c:d，首末比为其三次复合。构造函数选择不同且大于 1 的整数。

另一函数处理现代任意正整数端点：先用最大公因数约分，再用整数二分查找检验约分后的端点是否都是立方。若两中项存在，既约增长比 d/c 的三次方恰为末首比，约分后端点必为 c³、d³；反过来以同一公因数放大混合幂链即可。16、54 可插入 24、36；4、16 不行，因为 4 没有有理立方根。现代模式允许倒序、相等、单位端点。测试从两端之间枚举首个中项，用 Fraction 推导后续项，另有大整数检查。

## 重跑

在本目录使用 Python 3.9+ 标准库，不需联网。

```sh
python3 -B cube_means.py
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

三种模式各运行 5 项测试。有限基线扫描两端各取 1 至 40 的 1,600 对，其中 54 对有解、1,546 对无解。Notebook 的三个代码单元实际用标准库顺序回放，并非 Jupyter 内核运行。

实跑环境 Linux / CPython 3.12.14。回到[中文精读](../../papers/ancient/euclid-elements-viii12.zh-CN.md)，查看[原典核对](source-review.zh-CN.md)、[独立技术核对](technical-review.zh-CN.md)。

[实现](cube_means.py) · [测试](test_cube_means.py) · [Notebook](euclid-viii12.ipynb) · [重放脚本](replay_notebook.py)

[普通模式](normal.log) · [-O](O.log) · [-OO](OO.log) · [Notebook 重放](notebook-replay.log)
