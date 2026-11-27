# 《几何原本》IX.35：从端点差求连比前缀和

给定至少三项递增的正整数连比链。先计算相邻差，并验证每个差与其前项的比都和第一差与首项的比相同；再按端点差与第一差的比对首项缩放。结果等于除末项外各项之和。例：$`(8,12,18,27)`$ 的相邻差是 $`4,6,9`$，端点差是 $`19`$，得到 $`8\cdot(19/4)=38`$，不是含末项的 $`65`$。输入不要求整数乘率。含单位首项的例子属于现代正整数边界；程序不接受二项、退化平链、下降链或非连比。

在此目录用 Python 3.9+ 标准库运行：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

独立基线以精确分数比较全部相邻比，并直接累加前缀。检查长度 3、4，坐标各取 1 至 20 的有序输入。有限检验不代替一般证明。Notebook 日志记录标准库实跑三个代码单元，不是 Jupyter 内核运行。

直接打开 [Notebook](euclid-ix35.ipynb)；核对 [普通模式](normal.log)、[-O](O.log)、[-OO](OO.log) 和 [Notebook 回放](notebook-replay.log)。
