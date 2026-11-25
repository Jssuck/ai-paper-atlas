# 《几何原本》IX.1：相似平面数的积

正整数教学重构。给定有序因子对 $`(a,b),(c,d)`$，先核对 $`bc=ad`$，再构造平面数连比 $`(A,M,B)=(ab,bc,cd)`$。按首项 $`A`$ 放大得到 $`(A^2,AM,AB)`$，把中项除以已知首端的平方根 $`A`$，取得末端的根 $`M`$；程序再验 $`M^2=AB`$。

例如 $`(3,6),(2,4)`$ 给出 $`(18,12,8)`$，放大得到 $`(324,216,144)`$，故 $`144=12^2`$。$`(3,6),(1,8)`$ 的积仍是 $`144`$，但这两组指定因子不是相似的，不能用它们作为见证；$`(2,3),(2,5)`$ 则既不相似，积也不是平方。相等及单位按照现代正整数约定测试。

在本目录运行（Python 3.9+，仅标准库）：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

测试枚举四因子各取 1 至 12，以精确分数和端点积的整数平方根作独立对照。有限枚举不是一般证明。Notebook 日志来自标准库实跑三个代码单元，并非 Jupyter 内核。

## 文件

[深读正文](../../papers/ancient/euclid-elements-ix1.zh-CN.md) · [原典记录](source-review.zh-CN.md) · [独立核对](technical-review.zh-CN.md) · [源码](square_product.py) · [测试](test_square_product.py) · [Notebook](euclid-ix1.ipynb)

[普通](normal.log)、[优化](O.log)、[双优化](OO.log)、[Notebook 回放](notebook-replay.log)均为实际日志。
